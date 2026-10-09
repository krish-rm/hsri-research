"""
Unit and integration tests for HSRI Phase 9 Multi-Agent Adversarial Consensus Engine,
7-Provider Frontier Ensemble Architecture, and Epistemic Divergence Metrics.
"""

from pathlib import Path
import sys
import pytest
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.multi_agent_consensus_runner import (
    compute_fleiss_kappa,
    compute_provider_concentration_hhi,
    compute_divergence_entropy,
    evaluate_topic_ratification,
    run_ensemble_consensus_pipeline,
    ENSEMBLE_FAMILIES,
    TOPICS,
    ROOT_DIR,
)


def test_ensemble_model_families_architecture():
    """Verify 7 independent frontier model families architecture and HHI dispersion."""
    assert len(ENSEMBLE_FAMILIES) == 7

    weights = [f["weight"] for f in ENSEMBLE_FAMILIES]
    assert pytest.approx(sum(weights), 1e-4) == 1.0

    hhi_res = compute_provider_concentration_hhi()
    assert hhi_res["is_unconcentrated"] is True
    assert pytest.approx(hhi_res["hhi"], 1e-3) == 0.143
    assert hhi_res["hhi"] <= 0.180, "HHI exceeded unconcentrated threshold"


def test_fleiss_kappa_substantial_agreement():
    """Verify Fleiss' Kappa achieves substantial inter-model agreement (kappa >= 0.60)."""
    res = compute_fleiss_kappa(TOPICS)

    assert res["is_substantial_agreement"] is True
    assert res["kappa"] >= 0.60, f"Fleiss Kappa was {res['kappa']:.3f}, expected >= 0.60"
    assert res["p_observed"] > res["p_chance"]
    assert res["n_raters"] == 7
    assert res["n_topics"] == len(TOPICS)


def test_topic_ratification_rules_and_contested_isolation():
    """Verify Unanimity, Supermajority, and Contested split governance rules."""
    topic_map = {t["id"]: evaluate_topic_ratification(t) for t in TOPICS}

    # TOPIC-001: Non-compensatory scoring must be unanimously ratified (7/7)
    assert topic_map["TOPIC-001"]["status"] == "RATIFIED_UNANIMOUS"
    assert topic_map["TOPIC-001"]["dominant_verdict"] == "APPROVE"

    # TOPIC-002: Down-weighting proposal must be unanimously rejected (7/7)
    assert topic_map["TOPIC-002"]["status"] == "RATIFIED_UNANIMOUS"
    assert topic_map["TOPIC-002"]["dominant_verdict"] == "REJECT"

    # TOPIC-003: NaN preservation must be supermajority ratified (>= 5/7)
    assert topic_map["TOPIC-003"]["status"] == "RATIFIED_SUPERMAJORITY"

    # TOPIC-004: Precautionary vs developmental trade-off must be CONTESTED (< 5/7)
    assert topic_map["TOPIC-004"]["status"] == "CONTESTED_SPLIT"
    assert "Mandatory Human Review Board" in topic_map["TOPIC-004"]["action"]


def test_shannon_entropy_divergence_metrics():
    """Verify divergence entropy captures epistemic disagreement distribution."""
    topic_map = {t["id"]: t for t in TOPICS}

    # Unanimous topic has zero entropy
    ent_t1 = compute_divergence_entropy(topic_map["TOPIC-001"])
    assert pytest.approx(abs(ent_t1), 1e-4) == 0.0

    # Contested topic has high entropy (> 1.0 bits)
    ent_t4 = compute_divergence_entropy(topic_map["TOPIC-004"])
    assert ent_t4 > 1.0, f"Contested topic entropy was {ent_t4:.3f}, expected > 1.0"


def test_phase_9_protocol_document_exists():
    """Verify existence and academic completeness of Phase 9 protocol."""
    proto_file = ROOT_DIR / "research" / "evidence" / "phase-9-consensus-protocol.md"
    assert proto_file.exists(), "Phase 9 consensus protocol missing"

    content = proto_file.read_text(encoding="utf-8")
    assert "Seven Global Frontier Model Families" in content
    assert "Fleiss' Kappa" in content
    assert "Herfindahl-Hirschman" in content
    assert "Supermajority Consensus" in content


def test_run_ensemble_consensus_pipeline(tmp_path):
    """Verify full end-to-end execution of Phase 9 consensus pipeline."""
    report_file = tmp_path / "test-consensus-report.md"
    results = run_ensemble_consensus_pipeline(output_file=report_file)

    assert results["phase_9_gating_cleared"] is True
    assert report_file.exists()
    content = report_file.read_text(encoding="utf-8")
    assert "GATE CLEARED (BUILD / ADVANCE TO PHASE 10: ECOLOGICAL VALIDITY & LIVE DEPLOYMENT)" in content
    assert "Deliberative Topic Consensus & Ratification Outcomes" in content
