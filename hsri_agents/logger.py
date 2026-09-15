"""
Logging and Persistence Module.

Maintains the durable audit trail for HSRI-Agents:
1. research_memory.md: Full debate transcripts, analyst briefs, and seated verdicts.
2. model-divergence-log.csv: Cross-provider reliability matrix tracking verdict concordance.
"""

import csv
import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from hsri_agents.config import (
    MODEL_DIVERGENCE_LOG_PATH,
    REAL_ENSEMBLE_PROVIDERS,
    RESEARCH_MEMORY_PATH,
    SUPPORTED_PROVIDERS,
)

RESEARCH_MEMORY_HEADER = """# HSRI Research Memory: Multi-Agent Review Audit Trail

> [!NOTE]
> **Manual-First Operational Notice:** This system is operated strictly in manual-first mode.
> Scheduled automation, cron triggers, and webhooks are **intentionally deferred** until the repository
> maintainer has completed manual operational testing and explicitly defined a review cadence.
> Every entry below represents a human-reviewed, multi-agent evaluation pass.

---
"""

DIVERGENCE_CSV_HEADERS = [
    "timestamp",
    "triggering_paper",
    "anthropic",
    "openai",
    "google",
    "xai",
    "deepseek",
    "qwen",
    "glm",
    "mock",
    "divergence_summary",
    "notes",
]

def initialize_ledgers() -> None:
    """Initialize research_memory.md and model-divergence-log.csv if not present."""
    if not RESEARCH_MEMORY_PATH.exists():
        with open(RESEARCH_MEMORY_PATH, "w", encoding="utf-8") as f:
            f.write(RESEARCH_MEMORY_HEADER)

    if not MODEL_DIVERGENCE_LOG_PATH.exists():
        with open(MODEL_DIVERGENCE_LOG_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(DIVERGENCE_CSV_HEADERS)

def log_research_memory_entry(
    hit: Dict[str, Any],
    provider: str,
    analysts_result: Dict[str, Any],
    debate_result: Dict[str, Any],
    synthesizer_result: Dict[str, Any],
    review_board_result: Dict[str, Any],
    pr_status: str = "Staged locally for human maintainer review",
) -> None:
    """Append a full, unsummarized audit entry to research_memory.md."""
    initialize_ledgers()
    date_str = datetime.date.today().isoformat()
    citation = f"{hit.get('title')} ({', '.join(hit.get('authors', [])[:2])}, {hit.get('date', '')[:4]}; {hit.get('url_or_doi', '')})"

    # Format analyst briefs
    briefs_md = ""
    for lane, b in analysts_result.get("briefs", {}).items():
        briefs_md += f"\n- **{lane.replace('_', ' ').title()} ({b['impact_status']}):**\n  {b['brief_text'].strip()}\n"

    # Format debate transcript
    debate_md = debate_result.get("full_dialogue_text", "").strip()

    # Format review board seats
    board_md = f"Overall Status: {'APPROVED (3/3 seats)' if review_board_result.get('is_approved') else 'REJECTED / BLOCKED'}\n"
    for seat_id, s in review_board_result.get("seats", {}).items():
        board_md += f"- **{seat_id.replace('_', ' ').title()}:** {s['verdict']} — {s['evaluation_text'].strip()}\n"

    entry = f"""
## [{date_str}] — [{provider.upper()}] — Triggered by: {citation}

**Analyst briefs:**
{briefs_md}

**Debate transcript:**
{debate_md}

**Synthesizer verdict:**
- Verdict: `{synthesizer_result.get('verdict')}`
- Synthesis & Proposed Diff:
{synthesizer_result.get('synthesis_text', '').strip()}

**Review Board verdict:**
{board_md}

**PR / Git Readiness:**
- {pr_status}

---
"""

    with open(RESEARCH_MEMORY_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

def log_divergence_entry(
    triggering_paper: str,
    provider: str,
    verdict: str,
    notes: str = "",
) -> None:
    """
    Record or update cross-provider verdicts in model-divergence-log.csv.
    Verdicts are categorized as: 'diff-proposed', 'no-change', or 'rejected-at-board'.
    """
    initialize_ledgers()
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Read existing rows to check if an entry exists for this paper
    rows = []
    found = False
    if MODEL_DIVERGENCE_LOG_PATH.exists():
        with open(MODEL_DIVERGENCE_LOG_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("triggering_paper") == triggering_paper:
                    r[provider] = verdict
                    r["notes"] = notes or r.get("notes", "")
                    found = True
                rows.append(r)

    if not found:
        new_row = {col: "" for col in DIVERGENCE_CSV_HEADERS}
        new_row["timestamp"] = timestamp
        new_row["triggering_paper"] = triggering_paper
        new_row[provider] = verdict
        new_row["divergence_summary"] = "Single provider evaluated"
        new_row["notes"] = notes
        rows.append(new_row)

    # Re-evaluate divergence summary across real providers ONLY (mock strictly excluded)
    for r in rows:
        provider_verdicts = [r.get(p) for p in REAL_ENSEMBLE_PROVIDERS if r.get(p)]
        if len(provider_verdicts) > 1:
            if len(set(provider_verdicts)) == 1:
                r["divergence_summary"] = f"Full consensus ({len(provider_verdicts)}/{len(REAL_ENSEMBLE_PROVIDERS)} providers): {provider_verdicts[0]}"
            else:
                r["divergence_summary"] = f"Divergence detected across {len(provider_verdicts)}/{len(REAL_ENSEMBLE_PROVIDERS)} providers: {dict((p, r.get(p)) for p in REAL_ENSEMBLE_PROVIDERS if r.get(p))}"
        elif len(provider_verdicts) == 1:
            r["divergence_summary"] = f"Single real provider evaluated (1/{len(REAL_ENSEMBLE_PROVIDERS)})"
        else:
            r["divergence_summary"] = "No real frontier provider evaluated (offline/mock only)"

    with open(MODEL_DIVERGENCE_LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=DIVERGENCE_CSV_HEADERS, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
