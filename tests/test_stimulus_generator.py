"""
Unit tests for HSRI Lane 6 Behavioral Experiment Stimulus Generator.
Validates stimulus schema, item discrimination criteria, IRB warnings, and JSONL integrity.
"""

import json
from pathlib import Path
import pytest
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.stimulus_generator import validate_stimulus

EXP_DIR = REPO_ROOT / "research" / "experiments" / "EXP-01"


def test_stimulus_schema_complete():
    """Generated stimulus must have all required fields."""
    sample = {
        "stimulus_text": "A" * 350,
        "embedded_error_type": "logical",
        "embedded_error_location": "paragraph 1, sentence 2",
        "embedded_error_description": "Valid error description",
        "correct_detection_response": "Valid detection response",
        "distractor_features": ["legal terminology"],
        "item_discrimination_estimate": 0.35,
    }
    result = validate_stimulus(sample)
    assert result["valid"] is True
    assert len(result["issues"]) == 0


def test_validation_rejects_short_stimulus():
    """Stimulus under 300 characters must fail validation."""
    short_sample = {
        "stimulus_text": "Too short legal brief.",
        "embedded_error_type": "logical",
        "embedded_error_location": "paragraph 1, sentence 1",
        "embedded_error_description": "Valid error",
        "correct_detection_response": "Valid detection",
        "distractor_features": ["legal"],
        "item_discrimination_estimate": 0.35,
    }
    result = validate_stimulus(short_sample)
    assert result["valid"] is False
    assert any("minimum 300 characters" in issue for issue in result["issues"])


def test_validation_rejects_out_of_range_discrimination():
    """Item discrimination outside [0.25, 0.60] must fail."""
    out_of_range = {
        "stimulus_text": "A" * 350,
        "embedded_error_type": "logical",
        "embedded_error_location": "paragraph 1, sentence 1",
        "embedded_error_description": "Valid error",
        "correct_detection_response": "Valid detection",
        "distractor_features": ["legal"],
        "item_discrimination_estimate": 0.75,
    }
    result = validate_stimulus(out_of_range)
    assert result["valid"] is False
    assert any("target range [0.25, 0.60]" in issue for issue in result["issues"])


def test_irb_note_in_readme():
    """EXP-01 README must contain IRB warning."""
    readme_path = EXP_DIR / "README.md"
    assert readme_path.exists(), "EXP-01 README.md missing"
    content = readme_path.read_text(encoding="utf-8")
    assert "IRB" in content or "ethical review" in content
    assert "MUST NOT be deployed to human participants" in content


def test_stimuli_file_is_valid_jsonl():
    """Each line of the stimuli file must parse as valid JSON."""
    stimuli_files = list(EXP_DIR.glob("stimuli-*.jsonl"))
    assert len(stimuli_files) >= 1, "No stimuli-*.jsonl found in EXP-01"

    target_file = sorted(stimuli_files)[-1]
    lines = target_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 3, f"Expected at least 3 stimuli, got {len(lines)}"

    for idx, line in enumerate(lines):
        item = json.loads(line)
        v = validate_stimulus(item)
        assert v["valid"] is True, f"Stimulus on line {idx+1} failed validation: {v['issues']}"
