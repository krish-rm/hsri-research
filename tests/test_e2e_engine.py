"""
tests/test_e2e_engine.py — End-to-End API Integration & Container Contract Tests

Validates full client-to-engine API integration, telemetry provenance contract,
CORS lockdown security, and Docker containerization specifications for HSRI 2.0.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hsri_engine.api import app

client = TestClient(app)


# ============================================================================
# 1. Container Specification & Architecture Contract
# ============================================================================

def test_dockerfile_specification_contract():
    """Verify Dockerfile contains required base image, dependencies, and healthcheck."""
    dockerfile = REPO_ROOT / "Dockerfile"
    assert dockerfile.exists(), "Dockerfile missing at repository root"
    content = dockerfile.read_text(encoding="utf-8")

    assert "FROM python:3.10-slim" in content
    assert "EXPOSE 8000" in content
    assert "HEALTHCHECK" in content
    assert "http://localhost:8000/health" in content
    assert "ENTRYPOINT" in content
    assert "hsri_engine.api:app" in content

    # Check copy commands
    for path in ["pyproject.toml", "hsri_engine", "scripts", "data"]:
        assert path in content, f"Expected {path} to be copied into container"


def test_docker_compose_specification():
    """Verify docker-compose.yml configuration and port mapping."""
    compose_file = REPO_ROOT / "docker-compose.yml"
    assert compose_file.exists(), "docker-compose.yml missing at repository root"
    content = compose_file.read_text(encoding="utf-8")

    assert "hsri-engine" in content
    assert "8000:8000" in content
    assert "healthcheck:" in content
    assert "curl" in content


# ============================================================================
# 2. End-to-End API Health & Metadata
# ============================================================================

def test_e2e_root_metadata_endpoint():
    """Verify root / returns compliant metadata, permanent DOI, and status."""
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()

    assert data["engine"] == "HSRI 2.0 Engine Core"
    assert data["status"] == "operational"
    assert data["doi"] == "10.5281/zenodo.10842000"
    assert "https://humanreadinessindex.org/" in data["portal_url"]
    assert "openapi_json" in data


def test_e2e_healthcheck_endpoint():
    """Verify container orchestrator health check endpoint."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["engine"] == "hsri-engine-core"
    assert "timestamp" in data


# ============================================================================
# 3. Telemetry Precursor Seismograph & Provenance Contract (Sprint 36/37)
# ============================================================================

def test_e2e_telemetry_precursor_contract():
    """Verify GET /v1/telemetry/precursors returns provenance, fallback flag, and valid scores."""
    res = client.get("/v1/telemetry/precursors")
    assert res.status_code == 200
    data = res.json()

    # Sprint 36/37 transparency contract
    assert "is_fallback" in data
    assert isinstance(data["is_fallback"], bool)

    assert "provenance" in data
    assert data["provenance"] in [
        "live_sentinel_telemetry",
        "deterministic_calibration_fallback",
    ]

    assert "data_timestamp" in data
    assert "master_threat_score" in data
    assert 0.0 <= data["master_threat_score"] <= 10.0
    assert data["master_threat_score"] >= 8.0  # Critical regime

    # Check CORS and latency wedge
    assert "cors_score" in data
    assert data["cors_score"] == 10.0
    assert data["latency_wedge_ratio"] >= 3000.0


# ============================================================================
# 4. Sovereignty Evaluation & Vulnerability Trap Detection
# ============================================================================

def test_e2e_sovereignty_evaluation_hyper_connected_hub():
    """Evaluate an Archetype A hyper-connected nation (e.g. Singapore-like) showing Vulnerability Trap."""
    req_payload = {
        "entity_id": "SGP",
        "entity_name": "Singapore",
        "pillars": {
            "p1": 0.92,
            "p2": 0.55,
            "p3": 0.63,
            "p4": 0.98,
            "p5": 0.45,
            "p6": 0.12,  # 8h half-life -> massive bottleneck
            "p7": 0.85,
            "p8": 0.40,
        },
    }

    res = client.post("/v1/evaluate", json=req_payload)
    assert res.status_code == 200
    data = res.json()

    # Layer 1 adoption should be high (> 0.70)
    assert data["layer1_score"] > 0.70

    # Layer 2 Leontief floor should be constrained heavily by p6 (< 0.35)
    assert data["layer2_score"] < 0.35

    # Master Vulnerability Index V_ASI must trigger High-Compute Vulnerability Trap
    assert data["master_vulnerability_index"] > 0.40
    assert data["is_high_compute_trap"] is True
    assert "p6" in data["weakest_link_pillar"].lower()


def test_e2e_sovereignty_evaluation_resilient_sovereign():
    """Evaluate an Archetype C decentralized nation (e.g. Norway-like) showing resilient balance."""
    req_payload = {
        "entity_id": "NOR",
        "entity_name": "Norway",
        "pillars": {
            "p1": 0.78,
            "p2": 0.89,
            "p3": 0.87,
            "p4": 0.92,
            "p5": 0.82,
            "p6": 0.95,  # 336h+ decentralized resilience
            "p7": 0.75,
            "p8": 0.70,
        },
    }

    res = client.post("/v1/evaluate", json=req_payload)
    assert res.status_code == 200
    data = res.json()

    # Balanced profile: High sovereignty score and low vulnerability
    assert data["layer2_score"] > 0.70
    assert data["is_high_compute_trap"] is False
    assert data["master_vulnerability_index"] < 0.20


# ============================================================================
# 5. Benchmark Summary & JRC Step 7 Monte Carlo Sensitivity
# ============================================================================

def test_e2e_benchmark_summary():
    """Verify 39-nation official benchmark summary retrieval."""
    res = client.get("/v1/benchmark/summary")
    assert res.status_code == 200
    data = res.json()

    assert data["total_nations"] == 39
    assert len(data["top_sovereign_nations"]) > 0
    assert len(data["high_compute_traps"]) > 0

    # Singapore or USA must appear in vulnerability traps
    trap_isos = [t["nation_iso"] for t in data["high_compute_traps"]]
    assert "SGP" in trap_isos or "USA" in trap_isos


def test_e2e_monte_carlo_sensitivity():
    """Run Dirichlet Monte Carlo sensitivity test on Layer 2 pillars."""
    req_payload = {
        "evaluation_request": {
            "entity_id": "FIN",
            "entity_name": "Finland",
            "pillars": {
                "p1": 0.85,
                "p2": 0.90,
                "p3": 0.88,
                "p4": 0.82,
                "p5": 0.85,
                "p6": 0.90,
                "p7": 0.80,
                "p8": 0.75,
            },
        },
        "iterations": 100,
        "alpha_dirichlet": 1.0,
    }

    res = client.post("/v1/audit/monte-carlo", json=req_payload)
    assert res.status_code == 200
    data = res.json()

    assert data["entity_id"] == "FIN"
    assert data["iterations"] == 100
    assert 0.0 <= data["mean_layer2_score"] <= 1.0
    assert data["std_layer2_score"] >= 0.0
    assert data["ci_95_lower"] <= data["ci_95_upper"]
    assert 0.0 <= data["kendall_w_concordance"] <= 1.0


# ============================================================================
# 6. CORS Lockdown Security Policy
# ============================================================================

def test_e2e_cors_allowed_origin():
    """Verify CORS preflight succeeds for authorized institutional domains."""
    headers = {
        "Origin": "https://humanreadinessindex.org",
        "Access-Control-Request-Method": "POST",
    }
    res = client.options("/v1/evaluate", headers=headers)
    assert res.status_code == 200
    assert res.headers.get("access-control-allow-origin") == "https://humanreadinessindex.org"


def test_e2e_cors_disallowed_origin():
    """Verify CORS rejects unauthorized external origins."""
    headers = {
        "Origin": "https://unauthorized-malicious-site.com",
        "Access-Control-Request-Method": "POST",
    }
    res = client.options("/v1/evaluate", headers=headers)
    assert res.headers.get("access-control-allow-origin") is None
