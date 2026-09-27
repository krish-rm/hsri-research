"""
HSRI Evidence Reconciler
Scans literature-log.jsonl for papers with claim_verdict != "Neutral"
and flags rows in master-evidence-table.csv where the cited evidence
may need updating.

Outputs:
  - research/evidence/reconciliation-report-YYYY-MM-DD.md
  - Annotates master-evidence-table.csv with a `reconciliation_flag` column
    (does NOT modify existing rows, only appends the flag column)

Governance: Never autonomously updates evidence tiers. Flags only.
"""

import csv
import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("hsri.evidence_reconciler")

ROOT_DIR = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = ROOT_DIR / "research" / "evidence"
MASTER_EVIDENCE_TABLE_PATH = EVIDENCE_DIR / "master-evidence-table.csv"
LITERATURE_LOG_PATH = EVIDENCE_DIR / "literature-log.jsonl"


def detect_claim_pillar(claim_text: str, notes_text: str = "") -> str:
    """Infer the primary HSRI pillar for a claim row."""
    combined = f"{claim_text} {notes_text}".lower()
    if any(w in combined for w in ["automation bias", "cognitive forcing", "discernment", "skepticism", "meditation", "over-reliance", "trust calibration"]):
        return "Critical Discernment"
    if any(w in combined for w in ["literacy", "cognitive offloading", "piaac", "pisa", "skills"]):
        return "AI Literacy"
    if any(w in combined for w in ["governance", "index", "hdi", "spi", "mpi", "accountability", "regulation", "wgi"]):
        return "Institutional Governance"
    if any(w in combined for w in ["infrastructure", "compute", "broadband", "network", "grid"]):
        return "Digital Infrastructure"
    return "Cross-Pillar"


def load_literature_papers(log_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Load logged papers from literature-log.jsonl."""
    target_path = log_path or LITERATURE_LOG_PATH
    if not target_path.exists():
        return []

    papers = []
    with open(target_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    papers.append(json.loads(line.strip()))
                except Exception as e:
                    logger.warning(f"Skipping malformed jsonl line: {e}")
    return papers


def reconcile_evidence(
    evidence_table_path: Optional[Path] = None,
    literature_log_path: Optional[Path] = None,
    output_report_path: Optional[Path] = None,
    write_annotated_table: bool = True,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Path]:
    """
    Scan literature-log.jsonl against master-evidence-table.csv.
    Identifies claims needing human review or upgrade candidates.
    Annotates table with reconciliation_flag without modifying tiers.
    """
    table_path = evidence_table_path or MASTER_EVIDENCE_TABLE_PATH
    log_path = literature_log_path or LITERATURE_LOG_PATH

    papers = load_literature_papers(log_path)

    # Read master evidence table
    rows = []
    fieldnames = []
    if table_path.exists():
        with open(table_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)

    if "reconciliation_flag" not in fieldnames:
        fieldnames.append("reconciliation_flag")

    review_required = []
    upgrade_candidates = []
    current_count = 0

    for idx, row in enumerate(rows):
        tier = (row.get("evidence_tier") or "").strip()
        claim = row.get("claim", "")
        notes = row.get("notes", "")
        claim_id = f"CLAIM-{idx+1:03d}"
        pillar = detect_claim_pillar(claim, notes)

        flag = "CURRENT"
        matched_dois = []

        # Check for REVIEW_REQUIRED on Strong or Moderate claims
        if tier in ["Strong", "Moderate"]:
            for p in papers:
                p_verdict = p.get("claim_verdict", "Neutral")
                p_pillar = p.get("hsri_pillar", "Cross-Pillar")
                p_escalation = p.get("escalation_flag", False)
                p_doi = p.get("doi", "")

                pillar_match = (p_pillar == pillar or p_pillar == "Cross-Pillar" or pillar == "Cross-Pillar")
                if pillar_match and p_verdict in ["Contradicts", "Challenges"] and p_escalation:
                    flag = "REVIEW_REQUIRED"
                    matched_dois.append((p_doi, p_verdict))

            if flag == "REVIEW_REQUIRED":
                review_required.append({
                    "claim_id": claim_id,
                    "claim": claim,
                    "evidence_tier": tier,
                    "dois": matched_dois,
                })

        # Check for UPGRADE_CANDIDATE on Preliminary or Speculative claims
        elif tier in ["Preliminary", "Speculative", "[UNVERIFIED — NEEDS SOURCE]"]:
            for p in papers:
                p_verdict = p.get("claim_verdict", "Neutral")
                p_pillar = p.get("hsri_pillar", "Cross-Pillar")
                p_study_type = p.get("study_type", "")
                p_doi = p.get("doi", "")

                pillar_match = (p_pillar == pillar or p_pillar == "Cross-Pillar" or pillar == "Cross-Pillar")
                if pillar_match and p_verdict == "Supports" and p_study_type in ["RCT", "meta-analysis"]:
                    flag = "UPGRADE_CANDIDATE"
                    matched_dois.append((p_doi, p_study_type))

            if flag == "UPGRADE_CANDIDATE":
                upgrade_candidates.append({
                    "claim_id": claim_id,
                    "claim": claim,
                    "evidence_tier": tier,
                    "dois": matched_dois,
                })

        if flag == "CURRENT":
            current_count += 1

        row["reconciliation_flag"] = flag

    # Write annotated table if requested
    if write_annotated_table and rows:
        with open(table_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)

    # Format report
    today_str = datetime.date.today().isoformat()
    report_file = output_report_path or (EVIDENCE_DIR / f"reconciliation-report-{today_str}.md")

    if review_required:
        rec_action = "TRIGGER_DEBATE"
    elif upgrade_candidates:
        rec_action = "REVIEW"
    else:
        rec_action = "MONITOR"

    report_lines = [
        f"# Evidence Reconciliation Report — {today_str}",
        "",
        "## REVIEW_REQUIRED (Strong/Moderate claims challenged by new literature)",
    ]

    if review_required:
        report_lines.extend([
            "| Claim ID | Current Tier | Challenging Paper DOI | Verdict |",
            "|----------|-------------|----------------------|---------|",
        ])
        for item in review_required:
            dois_str = ", ".join(d[0] for d in item["dois"])
            verdict_str = ", ".join(d[1] for d in item["dois"])
            report_lines.append(f"| `{item['claim_id']}` | {item['evidence_tier']} | {dois_str} | {verdict_str} |")
    else:
        report_lines.append("No Strong or Moderate claims currently challenged by escalated literature.")

    report_lines.extend([
        "",
        "## UPGRADE_CANDIDATE (Preliminary claims now supported by stronger evidence)",
    ])

    if upgrade_candidates:
        report_lines.extend([
            "| Claim ID | Current Tier | Supporting Paper DOI | Study Type |",
            "|----------|-------------|---------------------|------------|",
        ])
        for item in upgrade_candidates:
            dois_str = ", ".join(d[0] for d in item["dois"])
            type_str = ", ".join(d[1] for d in item["dois"])
            report_lines.append(f"| `{item['claim_id']}` | {item['evidence_tier']} | {dois_str} | {type_str} |")
    else:
        report_lines.append("No Preliminary/Speculative claims currently identified for evidence upgrade.")

    report_lines.extend([
        "",
        "## CURRENT (No new challenges)",
        f"{current_count} rows — no action required.",
        "",
        "## Recommended Action",
        rec_action,
        "",
    ])

    if rec_action == "TRIGGER_DEBATE":
        first_rr = review_required[0]
        claim_trunc = (first_rr["claim"][:80] + "...") if len(first_rr["claim"]) > 80 else first_rr["claim"]
        doi_val = first_rr["dois"][0][0] if first_rr["dois"] else "N/A"
        report_lines.extend([
            "### Pre-Formatted Lane 3 Invocation",
            "```",
            f'@hsri-ops debate "{claim_trunc} — new contradicting evidence from {doi_val}"',
            "```",
            "",
        ])

    report_content = "\n".join(report_lines)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    summary = {
        "review_required_count": len(review_required),
        "upgrade_candidates_count": len(upgrade_candidates),
        "current_count": current_count,
        "recommended_action": rec_action,
    }

    return rows, summary, report_file


if __name__ == "__main__":
    rows, summary, report_file = reconcile_evidence()
    print(f"Reconciliation complete: {summary['review_required_count']} review required, "
          f"{summary['upgrade_candidates_count']} upgrade candidates, {summary['current_count']} current. "
          f"Report generated at {report_file.name}.")
