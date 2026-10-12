"""
test_manifesto_scaffold.py - Unit test suite for Sprint 26:
Dual-Layer Mathematical Formalization and Manifesto v2.0 Scaffold.
"""

import math
from pathlib import Path
import pytest
import numpy as np

import sys
sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))
import dual_layer_formalization as dlf


# -----------------------------------------------------------------------------
# 1. LAYER 1 TESTS
# -----------------------------------------------------------------------------

def test_layer1_score_bounds_and_calculation():
    """Verify Layer 1 score computes equal-weighted arithmetic mean bounded in [0, 1]."""
    score = dlf.calculate_layer1_score(0.8, 0.6, 0.7, 0.9)
    assert math.isclose(score, 0.75, rel_tol=1e-5)
    
    # Boundary checks
    assert dlf.calculate_layer1_score(0.0, 0.0, 0.0, 0.0) == 0.0
    assert dlf.calculate_layer1_score(1.0, 1.0, 1.0, 1.0) == 1.0

    # Invalid input raises
    with pytest.raises(ValueError):
        dlf.calculate_layer1_score(-0.1, 0.5, 0.5, 0.5)
    with pytest.raises(ValueError):
        dlf.calculate_layer1_score(1.1, 0.5, 0.5, 0.5)


# -----------------------------------------------------------------------------
# 2. NEGATIVE CROSS-ELASTICITY TESTS: dP2 / dP4 < 0
# -----------------------------------------------------------------------------

def test_negative_cross_elasticity_assistive_vs_adversarial():
    """Verify P2 is invariant below P4* and decays exponentially above P4*."""
    p2_base = 0.80
    p4_star = 0.50
    alpha = 1.25

    # Below threshold (assistive regime): no decay, zero derivative
    p2_low = dlf.critical_discernment_decay(p4=0.30, p2_baseline=p2_base, p4_threshold=p4_star, alpha=alpha)
    assert p2_low == p2_base
    assert dlf.d_p2_d_p4(p4=0.30, p2_baseline=p2_base, p4_threshold=p4_star, alpha=alpha) == 0.0
    assert dlf.cross_elasticity_p2_p4(p4=0.30, p2_baseline=p2_base, p4_threshold=p4_star, alpha=alpha) == 0.0

    # At threshold
    p2_thresh = dlf.critical_discernment_decay(p4=0.50, p2_baseline=p2_base, p4_threshold=p4_star, alpha=alpha)
    assert math.isclose(p2_thresh, p2_base, rel_tol=1e-5)

    # Above threshold (adversarial regime): dP2/dP4 strictly negative
    p2_high = dlf.critical_discernment_decay(p4=0.80, p2_baseline=p2_base, p4_threshold=p4_star, alpha=alpha)
    assert p2_high < p2_base
    deriv = dlf.d_p2_d_p4(p4=0.80, p2_baseline=p2_base, p4_threshold=p4_star, alpha=alpha)
    assert deriv < 0.0

    # Cross elasticity is strictly negative
    elasticity = dlf.cross_elasticity_p2_p4(p4=0.80, p2_baseline=p2_base, p4_threshold=p4_star, alpha=alpha)
    assert elasticity < 0.0
    assert math.isclose(elasticity, -1.25 * 0.80, rel_tol=1e-5)


def test_analytical_vs_numerical_derivative_p2_p4():
    """Verify analytical derivative d_p2_d_p4 matches finite-difference numerical derivative."""
    p2_base = 0.75
    p4_star = 0.45
    alpha = 1.50
    h = 1e-6

    for test_p4 in [0.55, 0.70, 0.90]:
        analytical = dlf.d_p2_d_p4(test_p4, p2_base, p4_star, alpha)
        f_plus = dlf.critical_discernment_decay(test_p4 + h, p2_base, p4_star, alpha)
        f_minus = dlf.critical_discernment_decay(test_p4 - h, p2_base, p4_star, alpha)
        numerical = (f_plus - f_minus) / (2 * h)
        assert math.isclose(analytical, numerical, rel_tol=1e-4)


def test_verification_latency_wedge_divergence():
    """Verify Delta T_wedge expands and ratio diverges as machine generation speed surges."""
    tau_verify = 60.0  # seconds (biological audit time)
    
    # Slow model
    delta_t_slow, ratio_slow = dlf.verification_latency_wedge(tau_verify, tau_gen=10.0)
    assert delta_t_slow == 50.0
    assert ratio_slow == 6.0

    # Fast frontier agent swarm (0.01s per batch)
    delta_t_fast, ratio_fast = dlf.verification_latency_wedge(tau_verify, tau_gen=0.01)
    assert delta_t_fast == 59.99
    assert ratio_fast == 6000.0


# -----------------------------------------------------------------------------
# 3. LAYER 2 SOVEREIGNTY PILLARS TESTS (P5 - P8)
# -----------------------------------------------------------------------------

def test_p5_epistemic_inviolability_boundaries():
    """Verify P5 Epistemic Inviolability and Verification Sovereignty Ratio (VSR)."""
    # 80 human out of 100, 0.90 persuasion resilience
    p5, vsr = dlf.calculate_p5_epistemic_inviolability(80, 100, 0.90)
    assert vsr == 0.80
    assert math.isclose(p5, 0.72, rel_tol=1e-5)

    # Complete delegation (0 human verifications) => P5 collapses to 0
    p5_zero, vsr_zero = dlf.calculate_p5_epistemic_inviolability(0, 100, 0.95)
    assert vsr_zero == 0.0
    assert p5_zero == 0.0

    # Complete persuasion capture (rho = 0) => P5 collapses to 0
    p5_captured, _ = dlf.calculate_p5_epistemic_inviolability(100, 100, 0.0)
    assert p5_captured == 0.0


def test_p6_decoupling_half_life_weakest_link():
    """Verify P6 Decoupling Half-Life takes minimum across critical systems and normalizes."""
    # System with logistics bottleneck (24 hours)
    p6, t_half = dlf.calculate_p6_decoupling_half_life(
        t_energy=720.0,
        t_finance=360.0,
        t_logistics=24.0,   # bottleneck
        t_info=500.0,
        t_half_saturation_hours=720.0
    )
    assert t_half == 24.0
    # P6 = 24 / (24 + 720) = 24 / 744 ≈ 0.032258
    assert math.isclose(p6, 24.0 / 744.0, rel_tol=1e-5)

    # Catastrophic blackout (energy = 0) => T_half = 0, P6 = 0
    p6_zero, t_half_zero = dlf.calculate_p6_decoupling_half_life(0.0, 100.0, 100.0, 100.0)
    assert t_half_zero == 0.0
    assert p6_zero == 0.0

    # Resilient decentralizer (30 days = 720h)
    p6_30d, t_half_30d = dlf.calculate_p6_decoupling_half_life(720.0, 720.0, 720.0, 720.0, 720.0)
    assert t_half_30d == 720.0
    assert p6_30d == 0.50  # half-saturation point


def test_p7_coordination_velocity():
    """Verify P7 Multipolar Coordination Velocity dynamics."""
    # Regulatory lag: self-modification in 2 hours, treaty inspection takes 200 hours
    p7_lag, v_coord_lag = dlf.calculate_p7_coordination_velocity(tau_modify=2.0, tau_verify_treaty=200.0)
    assert math.isclose(v_coord_lag, 0.01, rel_tol=1e-5)
    assert math.isclose(p7_lag, 0.01, rel_tol=1e-5)

    # Stable governance: self-modification requires 500h, inspection takes 100h
    p7_stable, v_coord_stable = dlf.calculate_p7_coordination_velocity(tau_modify=500.0, tau_verify_treaty=100.0)
    assert v_coord_stable == 5.0
    assert p7_stable == 1.0  # capped at 1.0


def test_p8_post_labor_elasticity():
    """Verify P8 Post-Labor Institutional Elasticity (PLIE)."""
    # Gini=0.4, SafetyNet=0.8, LaborTax=0.3
    # PLIE = (1 - 0.4) * 0.8 * (1 - 0.3) = 0.6 * 0.8 * 0.7 = 0.336
    plie = dlf.calculate_p8_post_labor_elasticity(0.4, 0.8, 0.3)
    assert math.isclose(plie, 0.336, rel_tol=1e-5)

    # Complete monopoly: compute Gini = 1.0 => PLIE = 0
    assert dlf.calculate_p8_post_labor_elasticity(1.0, 0.9, 0.1) == 0.0

    # Complete payroll dependence: 100% tax on labor => PLIE = 0
    assert dlf.calculate_p8_post_labor_elasticity(0.2, 0.9, 1.0) == 0.0


# -----------------------------------------------------------------------------
# 4. DUAL-LAYER AGGREGATION & MASTER ASI VULNERABILITY TESTS
# -----------------------------------------------------------------------------

def test_layer2_leontief_floor_and_vulnerability_index():
    """Verify Leontief floor on Layer 2 collapses on weakest link and detects vulnerability trap."""
    # Balanced resilient nation (Nordic archetype)
    l1_nordic = dlf.calculate_layer1_score(0.85, 0.80, 0.82, 0.78)  # 0.8125
    l2_nordic = dlf.calculate_layer2_sovereignty_score(p5=0.80, p6=0.75, p7=0.70, p8=0.75)
    # floor = 0.70, mean = 0.75, sqrt(0.70 * 0.75) ≈ 0.72457
    v_asi_nordic = dlf.calculate_master_asi_vulnerability_index(l1_nordic, l2_nordic)
    assert v_asi_nordic < 0.15  # Low vulnerability

    # High-Compute Vulnerability Trap (Hyper-Automated Hostage archetype)
    # High Layer 1 adoption (0.90), but near-zero decoupling half-life (P6 = 0.02)
    l1_trap = dlf.calculate_layer1_score(0.90, 0.85, 0.90, 0.95)   # 0.90
    l2_trap = dlf.calculate_layer2_sovereignty_score(p5=0.70, p6=0.02, p7=0.60, p8=0.50)
    # floor = 0.02, mean = 0.455, sqrt(0.02 * 0.455) = sqrt(0.0091) ≈ 0.09539
    v_asi_trap = dlf.calculate_master_asi_vulnerability_index(l1_trap, l2_trap)
    assert v_asi_trap > 0.75  # Extreme vulnerability trap exposed!

    # Zero floor total collapse
    l2_zero = dlf.calculate_layer2_sovereignty_score(p5=0.0, p6=0.9, p7=0.9, p8=0.9)
    assert l2_zero == 0.0


# -----------------------------------------------------------------------------
# 5. MANIFESTO ARTIFACT STRUCTURE & CITATION SCAFFOLD TEST
# -----------------------------------------------------------------------------

def test_manifesto_v2_scaffold_integrity():
    """Verify Manifesto v2.0 file exists, contains all required sections and mathematical tokens."""
    manifesto_path = Path(__file__).resolve().parent.parent / "research" / "preprint" / "manifesto_v2.0_the_verification_illusion.md"
    assert manifesto_path.exists(), f"Manifesto not found at {manifesto_path}"

    content = manifesto_path.read_text(encoding="utf-8")
    assert len(content) > 15000, "Manifesto must be a comprehensive master document (>15,000 chars)"

    # Check key theoretical symbols and terms (case-insensitive where appropriate)
    required_tokens = [
        "The Verification Illusion",
        "Verification Latency Wedge",
        r"\Delta T_{\text{wedge}}",
        r"\frac{\partial P_2}{\partial P_4} < 0",
        "Cognitive Oversight Richter Scale",
        "High-Compute Vulnerability Trap",
        "Adoption Baseline",
        "Sovereignty Layer",
        "Verification Sovereignty Ratio",
        r"\text{VSR}",
        "Civilizational Decoupling Half-Life",
        r"T_{\text{half}}",
        "Multipolar Coordination Velocity",
        r"V_{\text{coord}}",
        "Post-Labor Institutional Elasticity",
        "PLIE",
        r"V_{\text{ASI}}",
        "Article 14",
        "bibtex"
    ]
    for token in required_tokens:
        assert token.lower() in content.lower(), f"Manifesto missing required theoretical token: '{token}'"
