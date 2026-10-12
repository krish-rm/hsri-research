"""
test_wedge_accelerometer.py - Unit test suite for Sprint 28:
Precursor Stream 3: Live Verification Wedge Accelerometer & CORS Mapping.
"""

import math
from pathlib import Path
import json
import pytest
import numpy as np

import sys
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_ROOT / "scripts"))
import wedge_accelerometer as wa


def test_calculate_wedge_basic_and_divergence():
    """Test 1: Verify Delta T_wedge and Wedge Ratio calculations."""
    delta_t, ratio = wa.calculate_wedge(tau_verify=60.0, tau_gen=1.0)
    assert delta_t == 59.0
    assert ratio == 60.0

    # Near zero tau_gen
    delta_t_fast, ratio_fast = wa.calculate_wedge(tau_verify=100.0, tau_gen=0.001)
    assert math.isclose(delta_t_fast, 99.999, rel_tol=1e-4)
    assert math.isclose(ratio_fast, 100000.0, rel_tol=1e-4)

    # Invariants and exceptions
    with pytest.raises(ValueError):
        wa.calculate_wedge(-5.0, 10.0)
    with pytest.raises(ValueError):
        wa.calculate_wedge(10.0, -2.0)


def test_cors_logarithmic_bounds():
    """Test 2: Verify CORS output is strictly bounded in [1.0, 10.0]."""
    for val in [0.0, 0.5, 1.0, 5.0, 50.0, 500.0, 5000.0, 50000.0, 500000.0]:
        score = wa.calculate_cors(val)
        assert 1.0 <= score <= 10.0, f"CORS {score} out of bounds for Delta T {val}"


def test_cors_anchors_and_monotonicity():
    """Test 3: Verify calibrated anchors and strict monotonicity of CORS."""
    assert wa.calculate_cors(1.0) == 1.0
    assert math.isclose(wa.calculate_cors(10.0), 3.5, abs_tol=1e-2)
    assert math.isclose(wa.calculate_cors(100.0), 6.0, abs_tol=1e-2)
    assert math.isclose(wa.calculate_cors(1000.0), 8.5, abs_tol=1e-2)
    assert wa.calculate_cors(4000.0) == 10.0

    # Monotonicity check
    prev = 1.0
    for delta_t in np.linspace(1.0, 5000.0, 50):
        current = wa.calculate_cors(delta_t)
        assert current >= prev
        prev = current


def test_classify_cors_regimes():
    """Test 4: Verify qualitative regime classification across CORS tiers."""
    assert wa.classify_cors_regime(2.0) == "Direct Biological Verification"
    assert wa.classify_cors_regime(4.0) == "Assistive Sampling"
    assert wa.classify_cors_regime(6.0) == "Complacent Delegation"
    assert wa.classify_cors_regime(7.5) == "Epistemic Surrender"
    assert wa.classify_cors_regime(9.0) == "Steganographic Blindness"
    assert wa.classify_cors_regime(9.8) == "Recursive Event Horizon"
    assert wa.classify_cors_regime(10.0) == "Recursive Event Horizon"


def test_discrete_derivatives_velocity_and_acceleration():
    """Test 5: Verify finite-difference velocity and acceleration calculations."""
    synthetic_records = [
        {"model_label": "M1", "timestamp_year": 2024.0, "tau_verify_seconds": 10.0, "tau_gen_seconds": 2.0},
        {"model_label": "M2", "timestamp_year": 2024.25, "tau_verify_seconds": 40.0, "tau_gen_seconds": 1.0}, # dt=3 mo, delta_t=39, v=(39-8)/3 = 31/3 ≈ 10.33
        {"model_label": "M3", "timestamp_year": 2024.50, "tau_verify_seconds": 100.0, "tau_gen_seconds": 1.0}, # dt=3 mo, delta_t=99, v=(99-39)/3 = 60/3 = 20.0, a=(20 - 10.33)/3 ≈ 3.22
    ]
    processed = wa.compute_discrete_derivatives(synthetic_records)
    assert len(processed) == 3
    assert processed[0]["velocity_s_per_month"] == 0.0
    assert math.isclose(processed[1]["velocity_s_per_month"], 31.0 / 3.0, abs_tol=1e-2)
    assert math.isclose(processed[2]["velocity_s_per_month"], 20.0, abs_tol=1e-2)
    assert processed[2]["acceleration_s_per_month2"] > 0.0


def test_epistemic_singularity_projection():
    """Test 6: Verify quadratic kinematic projection of Epistemic Singularity Horizon."""
    # Already exceeded threshold
    assert wa.project_epistemic_singularity_horizon(90000.0, 100.0, 2.0, 86400.0) == 0.0

    # Linear projection: current 40000s, v=1000s/mo, a=0 => target 46400s / 1000 = 46.4 mo
    months_linear = wa.project_epistemic_singularity_horizon(40000.0, 1000.0, 0.0, 86400.0)
    assert math.isclose(months_linear, 46.4, abs_tol=1e-1)

    # Accelerated projection should arrive sooner than linear
    months_accel = wa.project_epistemic_singularity_horizon(40000.0, 1000.0, 50.0, 86400.0)
    assert 0 < months_accel < months_linear


def test_wedge_history_json_structure():
    """Test 7: Verify generated data/telemetry/wedge_history.json schema and active values."""
    telemetry_file = REPO_ROOT / "data" / "telemetry" / "wedge_history.json"
    assert telemetry_file.exists(), "wedge_history.json missing"

    with open(telemetry_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["telemetry_stream"] == "STREAM-3"
    assert data["status"] == "ACTIVE_CRITICAL"
    rating = data["active_rating"]
    assert 1.0 <= rating["current_cors_level"] <= 10.0
    assert rating["current_delta_t_seconds"] > 0
    assert rating["velocity_seconds_per_month"] > 0
    assert len(data["benchmark_trajectory"]) >= 6


def test_site_astro_telemetry_sync():
    """Test 8: Verify wedge_history.json exported and synced to site-astro."""
    src_file = REPO_ROOT / "site-astro" / "src" / "data" / "wedge_history.json"
    pub_file = REPO_ROOT / "site-astro" / "public" / "data" / "wedge_history.json"

    assert src_file.exists(), "site-astro/src/data/wedge_history.json missing"
    assert pub_file.exists(), "site-astro/public/data/wedge_history.json missing"

    with open(src_file, "r", encoding="utf-8") as f:
        src_data = json.load(f)
    assert src_data["telemetry_stream"] == "STREAM-3"
    assert src_data["active_rating"]["current_cors_level"] == 10.0
