"""
Unit tests for HSRI Lane 1 Literature Sentinel.
Validates JSONL schema completeness, escalation triggers on high-powered contradictions,
and WEIRD sampling detection.
"""

import json
from pathlib import Path
import pytest

from scripts.literature_sentinel import (
    REQUIRED_SCHEMA_FIELDS,
    build_paper_record,
    detect_weird_flag,
    evaluate_escalation,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
LITERATURE_LOG_PATH = ROOT_DIR / "research" / "evidence" / "literature-log.jsonl"


def test_jsonl_schema_complete():
    """Verify that every entry in literature-log.jsonl contains all required schema fields."""
    assert LITERATURE_LOG_PATH.exists(), f"Log file missing: {LITERATURE_LOG_PATH}"
    with open(LITERATURE_LOG_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "literature-log.jsonl must contain at least one logged paper"

    for idx, line in enumerate(lines):
        record = json.loads(line)
        for field in REQUIRED_SCHEMA_FIELDS:
            assert field in record, f"Line {idx} missing required field '{field}'"
            assert record[field] is not None, f"Line {idx} field '{field}' is None"

        assert isinstance(record["weird_flag"], bool), f"Line {idx} weird_flag must be boolean"
        assert isinstance(record["pre_registered"], bool), f"Line {idx} pre_registered must be boolean"
        assert isinstance(record["escalation_flag"], bool), f"Line {idx} escalation_flag must be boolean"
        assert isinstance(record["sample_size"], int), f"Line {idx} sample_size must be int"


def test_escalation_fires_on_strong_contradiction():
    """
    Mock a high-N pre-registered paper contradicting a Strong claim.
    Confirm escalation_flag == True and escalation_reason is documented.
    """
    mock_paper = {
        "title": "Large-Scale Multi-Site Trial Finds Zero Evidence of Automation Bias in Diagnostic AI",
        "sample_size": 612,
        "pre_registered": True,
        "weird_flag": False,  # Non-WEIRD majority (e.g. Kenya, India, Brazil)
        "claim_verdict": "Contradicts",
        "hsri_pillar": "Critical Discernment",
        "current_evidence_tier": "Strong",
        "study_type": "RCT",
    }
    result = evaluate_escalation(mock_paper)

    assert result["escalation_flag"] is True
    assert result["escalation_reason"] != ""
    assert "Critical Discernment" in result["escalation_reason"]
    assert "Strong" in result["escalation_reason"]


def test_weird_flag_detection():
    """
    Verify WEIRD flag detection:
    - US-only / MTurk / undergraduate sample -> weird_flag = True
    - Diverse non-Western / Global South sample -> weird_flag = False
    """
    us_sample = "Conducted with 450 US undergraduate participants recruited via Amazon Mechanical Turk."
    assert detect_weird_flag(us_sample) is True

    us_prolific = "A sample of 500 adult participants in the United States and the United Kingdom via Prolific."
    assert detect_weird_flag(us_prolific) is True

    non_weird_sample = "A cross-cultural sample of 720 participants recruited across rural Kenya, India, and Brazil."
    assert detect_weird_flag(non_weird_sample) is False
