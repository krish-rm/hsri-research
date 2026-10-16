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

def test_precursor_telemetry_provenance_and_fallback():
    """Verify that telemetry exposes explicit provenance and fallback status."""
    response = client.get("/v1/telemetry/precursors")
    assert response.status_code == 200
    data = response.json()
    assert "is_fallback" in data
    assert isinstance(data["is_fallback"], bool)
    assert "provenance" in data
    assert data["provenance"] in ["live_sentinel_telemetry", "deterministic_calibration_fallback"]


def test_hardened_cors_policy():
    """Verify that the API enforces configured institutional CORS origins."""
    # Allowed origin gets explicit Access-Control-Allow-Origin header on preflight
    headers = {
        "Origin": "https://humanreadinessindex.org",
        "Access-Control-Request-Method": "GET",
    }
    resp = client.options("/v1/telemetry/precursors", headers=headers)
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == "https://humanreadinessindex.org"

    # Allowed origin on direct GET
    resp_get = client.get("/v1/telemetry/precursors", headers={"Origin": "https://humanreadinessindex.org"})
    assert resp_get.headers.get("access-control-allow-origin") == "https://humanreadinessindex.org"

    # Unauthorized origin does not receive wildcard or unauthorized allow header
    unauth_headers = {
        "Origin": "https://malicious-tracker.com",
        "Access-Control-Request-Method": "GET",
    }
    resp_unauth = client.options("/v1/telemetry/precursors", headers=unauth_headers)
    assert resp_unauth.headers.get("access-control-allow-origin") != "https://malicious-tracker.com"


def test_reinsurance_pricing_math_and_archetypes():
    """Verify hsri_engine.reinsurance actuarial pricing engine calculations."""
    from hsri_engine.reinsurance import calculate_reinsurance_pricing, generate_syndicate_slip_markdown
    
    # Archetype A
    res_a = calculate_reinsurance_pricing("A", tiv_billion=10.0)
    assert res_a["archetype_name"] == "Small Open Tech Hub"
    assert res_a["gross_loss_billion_usd"] == 9.42
    assert res_a["actuarial_risk_loading_factor_phi"] >= 1.8
    assert res_a["sovereignty_discount_or_surcharge_pct"] > 0
    assert res_a["solvency_ii_99_5_capital_charge_billion_usd"] > 5.0

    # Archetype C
    res_c = calculate_reinsurance_pricing("C", tiv_billion=10.0)
    assert res_c["actuarial_risk_loading_factor_phi"] <= 0.50
    assert res_c["sovereignty_discount_or_surcharge_pct"] < 0
    assert res_c["solvency_ii_99_5_capital_charge_billion_usd"] < res_a["solvency_ii_99_5_capital_charge_billion_usd"]

    # Invalid archetype
    import pytest
    with pytest.raises(ValueError):
        calculate_reinsurance_pricing("NON_EXISTENT_ARCHETYPE")

    # Slip markdown generation
    slip_md = generate_syndicate_slip_markdown(res_a)
    assert "LLOYD'S SYNDICATE PLACEMENT SLIP" in slip_md
    assert "Solvency II" in slip_md
    assert "Krishnakumar Radhakrishnan" in slip_md
    assert "10.5281/zenodo.10842000" in slip_md


def test_cli_reinsurance_slip_subcommand(monkeypatch, capsys):
    """Verify CLI execution of 'hsri-engine reinsurance slip'."""
    import sys
    from hsri_engine.cli import main

    # 1. Test markdown slip output
    monkeypatch.setattr(sys, "argv", ["hsri-engine", "reinsurance", "slip", "--archetype", "A", "--tiv", "10.0"])
    main()
    captured = capsys.readouterr()
    assert "LLOYD'S SYNDICATE PLACEMENT SLIP" in captured.out
    assert "Small Open Tech Hub" in captured.out
    assert "Solvency II" in captured.out
    assert "10.5281/zenodo.10842000" in captured.out

    # 2. Test JSON output
    monkeypatch.setattr(sys, "argv", ["hsri-engine", "reinsurance", "slip", "--archetype", "C", "--tiv", "20.0", "--json"])
    main()
    captured_json = capsys.readouterr()
    import json
    parsed = json.loads(captured_json.out)
    assert parsed["archetype_key"] == "archetype_c"
    assert parsed["tiv_billion_usd"] == 20.0
    assert parsed["sovereignty_discount_or_surcharge_pct"] < 0
