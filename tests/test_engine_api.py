"""
tests/test_engine_api.py - Unit & Integration Test Suite for HSRI Engine Core API
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hsri_engine.api import app
from hsri_engine.models import (
    PillarInput,
    RawTelemetryInput,
    EvaluationRequest,
    MonteCarloRequest,
)
from hsri_engine import core

client = TestClient(app)


def test_root_endpoint():
    """Verify API root metadata, archival DOI, and documentation links."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["engine"] == "HSRI 2.0 Engine Core"
    assert data["version"] == "2.4.0"
    assert data["doi"] == "10.5281/zenodo.10842000"
    assert data["status"] == "operational"
    assert "/docs" in data["docs_swagger"]


def test_health_check_endpoint():
    """Verify health status endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.4.0"


def test_evaluate_endpoint_standard_profile():
    """Verify evaluation of a standard national profile."""
    payload = {
        "entity_id": "TEST-NOR",
        "entity_name": "Nordic Benchmark Test",
        "pillars": {
            "p1": 0.88,
            "p2": 0.90,
            "p3": 0.94,
            "p4": 0.89,
            "p5": 0.87,
            "p6": 0.72,
            "p7": 0.80,
            "p8": 0.75,
        },
        "apply_negative_cross_elasticity": False,
    }
    response = client.post("/v1/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["entity_id"] == "TEST-NOR"
    assert 0.85 <= data["layer1_score"] <= 0.95
    assert 0.70 <= data["layer2_score"] <= 0.85
    assert data["is_high_compute_trap"] is False
    assert data["weakest_link_pillar"] == "P6"
    assert data["weakest_link_score"] == 0.72


def test_evaluate_endpoint_high_compute_trap():
    """Verify detection of the High-Compute Vulnerability Trap (e.g. Singapore / US profile)."""
    payload = {
        "entity_id": "TEST-TRAP",
        "entity_name": "High Compute Vulnerable Node",
        "pillars": {
            "p1": 0.92,
            "p2": 0.70,
            "p3": 0.85,
            "p4": 0.98,
            "p5": 0.30,
            "p6": 0.10,
            "p7": 0.40,
            "p8": 0.35,
        },
    }
    response = client.post("/v1/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["layer1_score"] >= 0.80
    assert data["layer2_score"] < 0.20
    assert data["master_vulnerability_index"] >= 0.25
    assert data["is_high_compute_trap"] is True
    assert data["weakest_link_pillar"] == "P6"


def test_evaluate_with_raw_telemetry():
    """Verify dynamic pillar derivation from raw operational telemetry."""
    payload = {
        "entity_id": "TEL-NODE",
        "entity_name": "Operational Infrastructure Node",
        "pillars": {
            "p1": 0.80,
            "p2": 0.75,
            "p3": 0.80,
            "p4": 0.85,
        },
        "telemetry": {
            "human_verifications": 900,
            "total_critical_verifications": 1000,
            "adversarial_persuasion_resilience": 0.90,
            "t_energy": 48.0,
            "t_finance": 24.0,
            "t_logistics": 72.0,
            "t_info": 48.0,
            "tau_modify": 120.0,
            "tau_verify_treaty": 240.0,
            "gini_compute": 0.40,
            "safety_net_coverage": 0.85,
            "labor_tax_reliance": 0.45,
            "tau_verify": 3600.0,
            "tau_gen": 1.2,
        },
    }
    response = client.post("/v1/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    diag = data["sovereignty_diagnostics"]
    assert diag["vsr"] == 0.9
    assert diag["persuasion_resilience"] == 0.9
    assert diag["t_half_hours"] == 24.0
    assert diag["t_half_limiting_subsystem"] == "finance"
    assert diag["v_coord"] == 0.5
    assert diag["delta_t_wedge_seconds"] == 3598.8
    assert diag["wedge_ratio"] == 3000.0


def test_negative_cross_elasticity_activation():
    """Verify that enabling negative cross elasticity decays effective P2 when P4 > 0.50."""
    base_payload = {
        "entity_id": "DECAY-TEST",
        "pillars": {"p1": 0.8, "p2": 0.9, "p3": 0.8, "p4": 0.95, "p5": 0.8, "p6": 0.8, "p7": 0.8, "p8": 0.8},
        "apply_negative_cross_elasticity": False,
    }
    resp_no_decay = client.post("/v1/evaluate", json=base_payload).json()
    
    decay_payload = dict(base_payload)
    decay_payload["apply_negative_cross_elasticity"] = True
    resp_decay = client.post("/v1/evaluate", json=decay_payload).json()
    
    assert resp_decay["pillars"]["P2_Critical_Discernment"] < resp_no_decay["pillars"]["P2_Critical_Discernment"]
    assert resp_decay["layer1_score"] < resp_no_decay["layer1_score"]


def test_monte_carlo_audit_endpoint():
    """Verify Dirichlet Monte Carlo sensitivity analysis endpoint."""
    payload = {
        "evaluation_request": {
            "entity_id": "MC-NODE",
            "pillars": {
                "p1": 0.85, "p2": 0.80, "p3": 0.85, "p4": 0.85,
                "p5": 0.70, "p6": 0.50, "p7": 0.60, "p8": 0.65,
            },
        },
        "iterations": 150,
        "alpha_dirichlet": 1.0,
    }
    response = client.post("/v1/audit/monte-carlo", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["iterations"] == 150
    assert 0.40 <= data["mean_layer2_score"] <= 0.70
    assert data["std_layer2_score"] >= 0.0
    assert data["ci_95_lower"] <= data["ci_95_upper"]
    assert data["kendall_w_concordance"] == 0.9986


def test_benchmark_summary_endpoint():
    """Verify retrieval of official 39-nation benchmark overview."""
    response = client.get("/v1/benchmark/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_nations"] >= 39
    assert data["doi"] == "10.5281/zenodo.10842000"
    assert "top_sovereign_nations" in data


def test_precursor_telemetry_endpoint():
    """Verify real-time precursor telemetry endpoint."""
    response = client.get("/v1/telemetry/precursors")
    assert response.status_code == 200
    data = response.json()
    assert data["master_threat_score"] >= 8.0
    assert data["cors_score"] == 10.0
    assert data["latency_wedge_seconds"] > 3000.0
    assert data["total_tripwires"] == 14


def test_validation_error_handling():
    """Verify schema enforcement rejects out-of-bounds inputs with HTTP 422."""
    # Out of bounds pillar value (> 1.0)
    invalid_payload = {
        "entity_id": "ERR-NODE",
        "pillars": {"p1": 1.5, "p2": 0.5, "p3": 0.5, "p4": 0.5},
    }
    response = client.post("/v1/evaluate", json=invalid_payload)
    assert response.status_code == 422

    # Weights not summing to 1.0
    invalid_weights = {
        "entity_id": "ERR-WEIGHTS",
        "pillars": {"p1": 0.5, "p2": 0.5, "p3": 0.5, "p4": 0.5},
        "layer1_weights": [0.5, 0.5, 0.5, 0.5],
    }
    response = client.post("/v1/evaluate", json=invalid_weights)
    assert response.status_code == 422


def test_leontief_weakest_link_zero_property():
    """Verify the core mathematical Leontief property: zero in any pillar collapses score to zero."""
    res_zero = core.calculate_layer2_leontief_score(0.0, 0.9, 0.9, 0.9)
    assert res_zero == 0.0

    res_pos = core.calculate_layer2_leontief_score(0.2, 0.9, 0.9, 0.9)
    assert res_pos > 0.0
