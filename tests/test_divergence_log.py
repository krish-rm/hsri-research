"""
Unit tests for HSRI Model Divergence Log.
Validates the citable 14-field CSV dataset schema, documented TOPIC-001 example row,
and strict pre-append entry validation.
"""

import csv
from pathlib import Path
import tempfile
import pytest

from hsri_agents.config import REPO_ROOT
from hsri_agents.logger import (
    MODEL_DIVERGENCE_SCHEMA,
    append_divergence_entry,
    validate_divergence_entry,
)

LOG_CSV_PATH = REPO_ROOT / "hsri_agents" / "logs" / "model-divergence-log.csv"
README_PATH = REPO_ROOT / "hsri_agents" / "logs" / "README.md"

EXPECTED_HEADERS = [
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


def test_divergence_log_schema_matches_citable_spec():
    """Verify that model-divergence-log.csv exists and has the exact 14 citable columns in order."""
    assert LOG_CSV_PATH.exists(), f"Log file does not exist at {LOG_CSV_PATH}"
    assert README_PATH.exists(), f"Dataset README does not exist at {README_PATH}"

    with open(LOG_CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

    assert header == EXPECTED_HEADERS, f"Header mismatch:\nFound:    {header}\nExpected: {EXPECTED_HEADERS}"
    assert len(header) == 14, f"Expected 14 columns, found {len(header)}"
    assert MODEL_DIVERGENCE_SCHEMA == EXPECTED_HEADERS


def test_topic_001_example_row_integrity():
    """Verify the documented TOPIC-001 benchmark entry row."""
    with open(LOG_CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) >= 1, "model-divergence-log.csv must contain at least the documented example row"
    row = rows[0]

    assert row["topic_id"] == "TOPIC-001"
    assert row["topic_description"] == "PIAAC PSTRE NaN policy validity"
    assert row["model_family"] == "anthropic"
    assert row["model_version"] == "claude-sonnet-4-6"
    assert row["verdict"] == "NO CHANGE"
    assert row["dominant_concern_lane"] == "Cross-Cultural Methods"
    assert row["concordance_with_majority"].lower() in ["true", "1"]
    assert row["round_1_position"] == "Conservative"
    assert row["round_2_shift"] == "Maintained"
    assert row["final_position"] == "NO CHANGE"


def test_validation_rejects_missing_fields():
    """Confirm validation helper fails if required schema fields are missing."""
    incomplete_entry = {
        "timestamp": "2026-09-27T12:00:00Z",
        "topic_id": "TOPIC-002",
        "topic_description": "Incomplete entry test",
        "model_family": "openai",
        # Missing model_version, verdict, dominant_concern_lane, etc.
    }
    is_valid, errors = validate_divergence_entry(incomplete_entry)
    assert is_valid is False
    assert any("model_version" in e for e in errors)
    assert any("verdict" in e for e in errors)


def test_validation_rejects_unauthorized_extra_fields():
    """Confirm validation helper rejects entries with unauthorized extra fields."""
    valid_entry = {col: "test" for col in EXPECTED_HEADERS}
    valid_entry["extra_unauthorized_field"] = "bad"

    is_valid, errors = validate_divergence_entry(valid_entry)
    assert is_valid is False
    assert any("extra_unauthorized_field" in e for e in errors)


def test_append_divergence_entry_enforces_schema():
    """Confirm append_divergence_entry writes valid rows and raises ValueError on invalid rows."""
    valid_entry = {
        "timestamp": "2026-09-27T12:00:00Z",
        "topic_id": "TOPIC-002",
        "topic_description": "Valid append test",
        "model_family": "google",
        "model_version": "gemini-1.5-pro",
        "verdict": "PROPOSED DIFF",
        "dominant_concern_lane": "Adversarial Skeptic",
        "geographic_bias_flag": False,
        "geographic_bias_notes": "",
        "concordance_with_majority": True,
        "round_1_position": "Revisionist",
        "round_2_shift": "Maintained",
        "final_position": "PROPOSED DIFF",
        "notes": "Testing append functionality",
    }

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        # Appending valid entry succeeds
        assert append_divergence_entry(valid_entry, csv_path=tmp_path) is True

        with open(tmp_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1
            assert rows[0]["topic_id"] == "TOPIC-002"
            assert rows[0]["model_family"] == "google"

        # Appending invalid entry raises ValueError
        invalid_entry = dict(valid_entry)
        del invalid_entry["topic_id"]
        with pytest.raises(ValueError, match="Divergence entry validation failed"):
            append_divergence_entry(invalid_entry, csv_path=tmp_path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
