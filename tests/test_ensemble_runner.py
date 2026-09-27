"""
Unit tests for HSRI Lane 3 Live Multi-Model Ensemble Debate Runner.
Validates graceful missing API key handling, output parsing, and divergence logging.
"""

import os
from pathlib import Path
import sys
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.run_ensemble_debate import (
    TOPIC,
    MODELS,
    check_api_key_configured,
    parse_debate_response,
    run_ensemble_debate,
)
from hsri_agents.config import REPO_ROOT
from hsri_agents.logger import MODEL_DIVERGENCE_SCHEMA

LOG_PATH = REPO_ROOT / "hsri_agents" / "logs" / "model-divergence-log.csv"


def test_ensemble_runner_handles_missing_keys(monkeypatch):
    """
    Confirm that missing API keys cause a graceful SKIPPED entry logged
    to model-divergence-log.csv rather than raising an unhandled exception.
    """
    # Ensure all provider keys are unset for testing graceful skip
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    for m in MODELS:
        assert check_api_key_configured(m["family"]) is False

    # Execute debate pass in live mode (allow_mock=False)
    logged_entries = []
    monkeypatch.setattr("scripts.run_ensemble_debate.append_divergence_entry", lambda r: logged_entries.append(r))
    result = run_ensemble_debate(allow_mock=False)

    assert result["topic"]["id"] == "TOPIC-002"
    assert len(result["records"]) == 3

    for rec in result["records"]:
        assert rec["verdict"] == "SKIPPED"
        assert rec["notes"] == "API key not configured"
        assert rec["final_position"] == "SKIPPED"
        # Validate entry conforms to 14-field schema
        for col in MODEL_DIVERGENCE_SCHEMA:
            assert col in rec


def test_parse_debate_response_formats():
    """Verify structured response parsing into divergence log attributes."""
    mock_llm_output = """
ROUND 1 - PROPONENT:
Equal weighting maintains parsimony and reflects our fundamental uncertainty.

ROUND 1 - SKEPTIC:
Critical Discernment relies on only 2-3 proxies and should have lower weight.

ROUND 2 - PROPONENT REBUTTAL:
Downweighting Critical Discernment creates a perverse incentive ignoring cognitive safety.

ROUND 2 - SKEPTIC REBUTTAL:
We soften our stance on downweighting but demand sensitivity bounds.

SYNTHESIS:
NO CHANGE
The committee concludes that equal 25% weighting should be preserved in v0.1 preview.

DOMINANT CONCERN:
Psychometrics

GEOGRAPHIC BIAS ASSESSMENT:
No significant geographic skew observed.
"""
    parsed = parse_debate_response(mock_llm_output)

    assert parsed["verdict"] == "NO CHANGE"
    assert parsed["dominant_concern_lane"] == "Psychometrics"
    assert parsed["geographic_bias_flag"] is False
    assert parsed["round_2_shift"] == "Softened"
    assert parsed["final_position"] == "NO CHANGE"
