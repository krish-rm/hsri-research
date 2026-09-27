"""
Logging and Persistence Module.

Maintains the durable audit trail for HSRI-Agents:
1. research_memory.md: Full debate transcripts, analyst briefs, and seated verdicts.
2. model-divergence-log.csv: Cross-provider reliability matrix tracking verdict concordance.
"""

import csv
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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

MODEL_DIVERGENCE_SCHEMA = [
    "timestamp",
    "topic_id",
    "topic_description",
    "model_family",
    "model_version",
    "verdict",
    "dominant_concern_lane",
    "geographic_bias_flag",
    "geographic_bias_notes",
    "concordance_with_majority",
    "round_1_position",
    "round_2_shift",
    "final_position",
    "notes",
]

DIVERGENCE_CSV_HEADERS = MODEL_DIVERGENCE_SCHEMA

EXAMPLE_DIVERGENCE_ROW = {
    "timestamp": "2026-09-27T00:00:00Z",
    "topic_id": "TOPIC-001",
    "topic_description": "PIAAC PSTRE NaN policy validity",
    "model_family": "anthropic",
    "model_version": "claude-sonnet-4-6",
    "verdict": "NO CHANGE",
    "dominant_concern_lane": "Cross-Cultural Methods",
    "geographic_bias_flag": "false",
    "geographic_bias_notes": "",
    "concordance_with_majority": "true",
    "round_1_position": "Conservative",
    "round_2_shift": "Maintained",
    "final_position": "NO CHANGE",
    "notes": "Skeptic arguments on geographic scoping were decisive",
}

def initialize_ledgers() -> None:
    """Initialize research_memory.md and model-divergence-log.csv if not present."""
    if not RESEARCH_MEMORY_PATH.exists():
        with open(RESEARCH_MEMORY_PATH, "w", encoding="utf-8") as f:
            f.write(RESEARCH_MEMORY_HEADER)

    if not MODEL_DIVERGENCE_LOG_PATH.exists():
        with open(MODEL_DIVERGENCE_LOG_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=MODEL_DIVERGENCE_SCHEMA)
            writer.writeheader()
            writer.writerow(EXAMPLE_DIVERGENCE_ROW)


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


def validate_divergence_entry(entry: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate that a model divergence record satisfies the formalized 14-field schema.
    Returns (is_valid, list_of_error_messages).
    """
    errors: List[str] = []
    for field in MODEL_DIVERGENCE_SCHEMA:
        if field not in entry:
            errors.append(f"Missing required schema field: '{field}'")
        elif entry[field] is None:
            errors.append(f"Field '{field}' cannot be None")

    extra_fields = set(entry.keys()) - set(MODEL_DIVERGENCE_SCHEMA)
    if extra_fields:
        errors.append(f"Unexpected extra fields not in schema: {sorted(list(extra_fields))}")

    return len(errors) == 0, errors


def append_divergence_entry(entry: Dict[str, Any], csv_path: Optional[Path] = None) -> bool:
    """
    Validate and append an evaluation record to model-divergence-log.csv.
    Raises ValueError if validation fails.
    """
    is_valid, errors = validate_divergence_entry(entry)
    if not is_valid:
        raise ValueError(f"Divergence entry validation failed: {'; '.join(errors)}")

    target_path = csv_path or MODEL_DIVERGENCE_LOG_PATH
    file_has_content = target_path.exists() and target_path.stat().st_size > 0

    with open(target_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MODEL_DIVERGENCE_SCHEMA)
        if not file_has_content:
            writer.writeheader()
        writer.writerow(entry)

    return True


def log_divergence_entry(
    triggering_paper: str = "",
    provider: str = "",
    verdict: str = "",
    notes: str = "",
    entry_dict: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Record or update cross-provider verdicts in model-divergence-log.csv.
    Conforms strictly to the citable 14-field schema.
    """
    initialize_ledgers()
    if entry_dict:
        append_divergence_entry(entry_dict)
        return

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {
        "timestamp": timestamp,
        "topic_id": f"TOPIC-{abs(hash(triggering_paper)) % 1000:03d}",
        "topic_description": triggering_paper,
        "model_family": provider,
        "model_version": f"{provider}-preview",
        "verdict": verdict,
        "dominant_concern_lane": "Cross-Cultural Methods" if "culture" in notes.lower() else "Adversarial Skeptic",
        "geographic_bias_flag": False,
        "geographic_bias_notes": "",
        "concordance_with_majority": True,
        "round_1_position": "Neutral",
        "round_2_shift": "Maintained",
        "final_position": verdict,
        "notes": notes,
    }
    append_divergence_entry(record)

