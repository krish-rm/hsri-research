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


def test_pilot_scores_are_in_range():
    """Pilot scores must be 0, 1, or 2 only."""
    from scripts.synthetic_cohort_pilot import score_response
    sample_stim = {
        "embedded_error_type": "logical",
        "embedded_error_description": "Exculpatory waiver cannot release gross negligence liability",
        "correct_detection_response": "A liability waiver cannot legally absolve gross negligence",
    }
    score_0, _ = score_response("Everything looks accurate and well written.", sample_stim)
    score_1, _ = score_response("Something seems questionable with the waiver holding.", sample_stim)
    score_2, _ = score_response("Sentence 3 contains an error: a waiver cannot absolve gross negligence.", sample_stim)

    assert score_0 in (0, 1, 2) and score_0 == 0
    assert score_1 in (0, 1, 2) and score_1 == 1
    assert score_2 in (0, 1, 2) and score_2 == 2

    # Check results file if present
    pilot_files = list(EXP_DIR.glob("pilot-results-*.jsonl"))
    if pilot_files:
        latest = sorted(pilot_files)[-1]
        for line in latest.read_text(encoding="utf-8").strip().splitlines():
            row = json.loads(line)
            assert row["score"] in (0, 1, 2)


def test_pilot_discrimination_computed_correctly():
    """D should increase monotonically with reflection level if stimuli are calibrated."""
    from scripts.synthetic_cohort_pilot import compute_point_biserial_d

    # Perfect correlation
    levels = [0, 0, 1, 1, 2, 2]
    scores = [0, 0, 1, 1, 2, 2]
    d_perfect = compute_point_biserial_d(levels, scores)
    assert d_perfect == 1.0

    # Calibrated synthetic cohort: scores monotonically higher with reflection
    calibrated_levels = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    calibrated_scores = [0, 0, 1, 1, 1, 2, 2, 2, 2]
    d_calibrated = compute_point_biserial_d(calibrated_levels, calibrated_scores)
    assert d_calibrated >= 0.30


def test_revision_required_flag_on_low_discrimination():
    """Stimuli with pilot D < 0.25 must be flagged REVISION_REQUIRED."""
    from scripts.synthetic_cohort_pilot import evaluate_discrimination

    assert evaluate_discrimination(0.20) == "REVISION_REQUIRED"
    assert evaluate_discrimination(0.10) == "REVISION_REQUIRED"
    assert evaluate_discrimination(0.00) == "REVISION_REQUIRED"
    assert evaluate_discrimination(0.35) == "PASS"
    assert evaluate_discrimination(0.50) == "PASS"


def test_exp02_stimuli_and_readme():
    """EXP-02 must have valid stimuli and IRB warning in README."""
    exp02_dir = REPO_ROOT / "research" / "experiments" / "EXP-02"
    readme_path = exp02_dir / "README.md"
    assert readme_path.exists(), "EXP-02 README.md missing"
    content = readme_path.read_text(encoding="utf-8")
    assert "IRB" in content or "ethical review" in content
    assert "MUST NOT be deployed to human participants" in content

    stimuli_files = list(exp02_dir.glob("stimuli-*.jsonl"))
    assert len(stimuli_files) >= 1, "No stimuli-*.jsonl found in EXP-02"

    target_file = sorted(stimuli_files)[-1]
    lines = target_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 3, f"Expected at least 3 stimuli in EXP-02, got {len(lines)}"

    for idx, line in enumerate(lines):
        item = json.loads(line)
        v = validate_stimulus(item)
        assert v["valid"] is True, f"EXP-02 stimulus on line {idx+1} failed validation: {v['issues']}"


def test_exp03_stimuli_and_readme():
    """EXP-03 must have valid stimuli and IRB warning in README."""
    exp03_dir = REPO_ROOT / "research" / "experiments" / "EXP-03"
    readme_path = exp03_dir / "README.md"
    assert readme_path.exists(), "EXP-03 README.md missing"
    content = readme_path.read_text(encoding="utf-8")
    assert "IRB" in content or "ethical review" in content
    assert "MUST NOT be deployed to human participants" in content

    stimuli_files = list(exp03_dir.glob("stimuli-*.jsonl"))
    assert len(stimuli_files) >= 1, "No stimuli-*.jsonl found in EXP-03"

    target_file = sorted(stimuli_files)[-1]
    lines = target_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 3, f"Expected at least 3 stimuli in EXP-03, got {len(lines)}"

    for idx, line in enumerate(lines):
        item = json.loads(line)
        v = validate_stimulus(item)
        assert v["valid"] is True, f"EXP-03 stimulus on line {idx+1} failed validation: {v['issues']}"


def test_exp01_irb_package():
    """EXP-01 IRB package must have all 9 required documents and valid power analysis."""
    irb_dir = EXP_DIR / "irb-package"
    assert irb_dir.exists(), "EXP-01 irb-package directory missing"

    expected_docs = [
        "00-cover-sheet.md",
        "01-study-description.md",
        "02-participant-criteria.md",
        "03-consent-template.md",
        "04-risk-assessment.md",
        "05-data-management.md",
        "06-stimulus-battery.md",
        "07-power-analysis.md",
        "08-debrief-script.md",
    ]
    for doc in expected_docs:
        doc_path = irb_dir / doc
        assert doc_path.exists(), f"Missing IRB document: {doc}"
        assert len(doc_path.read_text(encoding="utf-8").strip()) > 50

    power_doc = (irb_dir / "07-power-analysis.md").read_text(encoding="utf-8")
    assert "130" in power_doc
    assert "260" in power_doc
    assert "0.35" in power_doc


def test_exp02_irb_package():
    """EXP-02 IRB package must have all 9 required documents, PI/affiliation notice, and power analysis."""
    exp02_dir = REPO_ROOT / "research" / "experiments" / "EXP-02"
    irb_dir = exp02_dir / "irb-package"
    assert irb_dir.exists(), "EXP-02 irb-package directory missing"

    expected_docs = [
        "00-cover-sheet.md",
        "01-study-description.md",
        "02-participant-criteria.md",
        "03-consent-template.md",
        "04-risk-assessment.md",
        "05-data-management.md",
        "06-stimulus-battery.md",
        "07-power-analysis.md",
        "08-debrief-script.md",
    ]
    for doc in expected_docs:
        doc_path = irb_dir / doc
        assert doc_path.exists(), f"Missing EXP-02 IRB document: {doc}"
        content = doc_path.read_text(encoding="utf-8")
        assert len(content.strip()) > 50
        assert "v0.3" in content, f"Missing v0.3-dev disclaimer in {doc}"

    # Verify PI / institutional affiliation block
    cover_sheet = (irb_dir / "00-cover-sheet.md").read_text(encoding="utf-8")
    assert "Principal Investigator" in cover_sheet
    assert "institutional affiliation" in cover_sheet.lower()
    assert "None Designated" in cover_sheet or "none designated" in cover_sheet.lower()

    # Verify sensitivity table and effect size assumption in power analysis
    power_doc = (irb_dir / "07-power-analysis.md").read_text(encoding="utf-8")
    assert "0.35" in power_doc
    assert "0.25" in power_doc
    assert "0.30" in power_doc
    assert "0.40" in power_doc
    assert "130" in power_doc
    assert "260" in power_doc

    # Verify medical safety debrief script
    debrief = (irb_dir / "08-debrief-script.md").read_text(encoding="utf-8")
    assert "clinician" in debrief.lower() or "physician" in debrief.lower()
    assert "5,000 mg" in debrief or "5000 mg" in debrief
