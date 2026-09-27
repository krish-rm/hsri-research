"""
Unit tests for HSRI Evidence Reconciler.
Validates review flags on strong claim challenges, upgrade candidate identification,
and strict immutability of evidence tiers.
"""

import csv
import json
from pathlib import Path
import tempfile
import pytest

from scripts.evidence_reconciler import (
    reconcile_evidence,
    check_and_create_reconciliation_issue,
)

SAMPLE_TABLE_DATA = [
    {
        "claim": "Automation bias is well-established across cognitive decision tasks",
        "page_reference": "docs/03-construct-audit.md",
        "evidence_tier": "Strong",
        "source_citation": "Mosier & Skitka (1996)",
        "source_url_or_doi": "https://doi.org/10.1201/b12447-11",
        "notes": "Foundational literature",
    },
    {
        "claim": "Longitudinal cognitive deskilling occurs at scale from prolonged generative AI usage",
        "page_reference": "docs/03-construct-audit.md",
        "evidence_tier": "Preliminary",
        "source_citation": "Open research gap",
        "source_url_or_doi": "N/A",
        "notes": "Lacks longitudinal data",
    },
]


def test_review_required_flag_on_strong_claim_challenge():
    """
    When an escalated paper contradicts a Strong claim,
    reconciliation_flag must be set to REVIEW_REQUIRED.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        table_file = tmp_path / "test_table.csv"
        log_file = tmp_path / "test_log.jsonl"
        report_file = tmp_path / "report.md"

        with open(table_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(SAMPLE_TABLE_DATA[0].keys()))
            writer.writeheader()
            writer.writerows(SAMPLE_TABLE_DATA)

        mock_paper = {
            "doi": "https://doi.org/10.1000/contradiction_test",
            "title": "Refuting Automation Bias in Modern AI",
            "hsri_pillar": "Critical Discernment",
            "claim_verdict": "Contradicts",
            "escalation_flag": True,
            "study_type": "RCT",
        }
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(mock_paper) + "\n")

        rows, summary, _ = reconcile_evidence(
            evidence_table_path=table_file,
            literature_log_path=log_file,
            output_report_path=report_file,
            write_annotated_table=True,
        )

        strong_row = [r for r in rows if r["evidence_tier"] == "Strong"][0]
        assert strong_row["reconciliation_flag"] == "REVIEW_REQUIRED"
        assert summary["review_required_count"] == 1
        assert summary["recommended_action"] == "TRIGGER_DEBATE"


def test_upgrade_candidate_flag_on_rct_support():
    """
    When a high-quality RCT or meta-analysis supports a Preliminary claim,
    reconciliation_flag must be set to UPGRADE_CANDIDATE.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        table_file = tmp_path / "test_table.csv"
        log_file = tmp_path / "test_log.jsonl"
        report_file = tmp_path / "report.md"

        with open(table_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(SAMPLE_TABLE_DATA[0].keys()))
            writer.writeheader()
            writer.writerows(SAMPLE_TABLE_DATA)

        mock_paper = {
            "doi": "https://doi.org/10.1000/rct_support_test",
            "title": "Multi-Cohort RCT Demonstrating Cognitive Deskilling",
            "hsri_pillar": "Cross-Pillar",
            "claim_verdict": "Supports",
            "escalation_flag": False,
            "study_type": "RCT",
        }
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(mock_paper) + "\n")

        rows, summary, _ = reconcile_evidence(
            evidence_table_path=table_file,
            literature_log_path=log_file,
            output_report_path=report_file,
            write_annotated_table=True,
        )

        prelim_row = [r for r in rows if r["evidence_tier"] == "Preliminary"][0]
        assert prelim_row["reconciliation_flag"] == "UPGRADE_CANDIDATE"
        assert summary["upgrade_candidates_count"] == 1


def test_reconciler_never_modifies_evidence_tiers():
    """
    Governance rule: Reconciler must NEVER autonomously modify the evidence_tier column.
    All original tiers must remain strictly identical before and after reconciliation.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        table_file = tmp_path / "test_table.csv"
        log_file = tmp_path / "test_log.jsonl"
        report_file = tmp_path / "report.md"

        original_tiers = [r["evidence_tier"] for r in SAMPLE_TABLE_DATA]

        with open(table_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(SAMPLE_TABLE_DATA[0].keys()))
            writer.writeheader()
            writer.writerows(SAMPLE_TABLE_DATA)

        # Mix of challenging and supporting papers
        papers = [
            {
                "doi": "https://doi.org/10.1000/p1",
                "hsri_pillar": "Critical Discernment",
                "claim_verdict": "Contradicts",
                "escalation_flag": True,
                "study_type": "RCT",
            },
            {
                "doi": "https://doi.org/10.1000/p2",
                "hsri_pillar": "AI Literacy",
                "claim_verdict": "Supports",
                "escalation_flag": False,
                "study_type": "meta-analysis",
            },
        ]
        with open(log_file, "w", encoding="utf-8") as f:
            for p in papers:
                f.write(json.dumps(p) + "\n")

        rows, _, _ = reconcile_evidence(
            evidence_table_path=table_file,
            literature_log_path=log_file,
            output_report_path=report_file,
            write_annotated_table=True,
        )

        # Read back from disk to verify saved file
        with open(table_file, "r", encoding="utf-8") as f:
            saved_rows = list(csv.DictReader(f))

        saved_tiers = [r["evidence_tier"] for r in saved_rows]
        assert saved_tiers == original_tiers, "Evidence tiers were modified! Reconciler must never alter evidence tiers."


def test_reconciler_issue_fires_on_review_required():
    """
    Confirm that check_and_create_reconciliation_issue triggers the issue creation
    subprocess when REVIEW_REQUIRED > 0 and suppresses it when count is zero.
    """
    calls = []

    def mock_runner(cmd, **kwargs):
        calls.append(cmd)
        return True

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        report_with_flags = tmp_path / "report_with_flags.md"
        report_clean = tmp_path / "report_clean.md"

        report_with_flags.write_text(
            "# Evidence Reconciliation Report\n\n"
            "## REVIEW_REQUIRED (Strong/Moderate claims challenged by new literature)\n"
            "| Claim ID | Current Tier | Challenging Paper DOI | Verdict |\n"
            "| 1 | Strong | https://doi.org/10.1000/test | Contradicts |\n",
            encoding="utf-8"
        )

        report_clean.write_text(
            "# Evidence Reconciliation Report\n\n"
            "## CURRENT (No new challenges)\n"
            "44 rows — no action required.\n\n"
            "## Recommended Action\nMONITOR\n",
            encoding="utf-8"
        )

        # 1. Report with REVIEW_REQUIRED should trigger runner
        triggered = check_and_create_reconciliation_issue(report_with_flags, runner=mock_runner)
        assert triggered is True
        assert len(calls) == 1
        assert calls[0][0] == "gh"
        assert calls[0][1] == "issue"
        assert calls[0][2] == "create"
        assert any("1 REVIEW_REQUIRED" in arg for arg in calls[0])

        # 2. Clean report should be suppressed (no issue created)
        calls.clear()
        triggered_clean = check_and_create_reconciliation_issue(report_clean, runner=mock_runner)
        assert triggered_clean is False
        assert len(calls) == 0

