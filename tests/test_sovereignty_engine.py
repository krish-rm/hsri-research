"""
test_sovereignty_engine.py - Unit test suite for Sprint 27:
Dual-Layer Econometric Sovereignty Engine & Master ASI Vulnerability Index.
"""

import math
from pathlib import Path
import json
import pytest
import numpy as np
import pandas as pd

import sys
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_ROOT / "scripts"))
import dual_layer_formalization as dlf
import sovereignty_engine as se


@pytest.fixture
def sovereignty_results():
    """Returns the processed 39-country Dual-Layer DataFrame."""
    input_path = REPO_ROOT / "data" / "final_country_scores.csv"
    if not input_path.exists():
        input_path = REPO_ROOT / "data" / "hsri_variants.csv"
    base_df = pd.read_csv(input_path)
    return se.compute_dual_layer_sovereignty(base_df)


# -----------------------------------------------------------------------------
# 15 ECONOMETRIC UNIT TESTS FOR SPRINT 27
# -----------------------------------------------------------------------------

def test_layer1_reproducibility(sovereignty_results):
    """Test 1: Verify Layer 1 computed score matches linear composite."""
    df = sovereignty_results
    assert len(df) == 39
    for _, row in df.iterrows():
        p1 = row["AI_Literacy_score"] if "AI_Literacy_score" in row else row["p_lit"]
        p2 = row["Critical_Discernment_score"] if "Critical_Discernment_score" in row else row["p_disc"]
        p3 = row["Institutional_Governance_score"] if "Institutional_Governance_score" in row else row["p_gov"]
        p4 = row["Digital_Infrastructure_score"] if "Digital_Infrastructure_score" in row else row["p_infra"]
        expected = 0.25 * (p1 + p2 + p3 + p4)
        assert math.isclose(row["h_layer1"], expected, abs_tol=1e-3)


def test_layer2_leontief_floor_annihilation():
    """Test 2: Verify zero-annihilation property of Leontief sovereignty floor."""
    # If any single pillar is 0, entire Layer 2 score collapses to 0
    assert dlf.calculate_layer2_sovereignty_score(0.0, 0.8, 0.8, 0.8) == 0.0
    assert dlf.calculate_layer2_sovereignty_score(0.8, 0.0, 0.8, 0.8) == 0.0
    assert dlf.calculate_layer2_sovereignty_score(0.8, 0.8, 0.0, 0.8) == 0.0
    assert dlf.calculate_layer2_sovereignty_score(0.8, 0.8, 0.8, 0.0) == 0.0


def test_layer2_bounds_across_all_nations(sovereignty_results):
    """Test 3: Verify Layer 2 scores strictly bounded in [0, 1] for all 39 nations."""
    df = sovereignty_results
    for _, row in df.iterrows():
        assert 0.0 <= row["h_layer2"] <= 1.0, f"{row['country_iso3']} Layer 2 out of bounds: {row['h_layer2']}"


def test_layer2_monotonicity():
    """Test 4: Verify monotonic non-decreasing property of Leontief sovereignty score."""
    base = dlf.calculate_layer2_sovereignty_score(0.5, 0.5, 0.5, 0.5)
    higher_p5 = dlf.calculate_layer2_sovereignty_score(0.7, 0.5, 0.5, 0.5)
    higher_all = dlf.calculate_layer2_sovereignty_score(0.7, 0.7, 0.7, 0.7)
    assert higher_p5 >= base
    assert higher_all > higher_p5


def test_master_asi_vulnerability_index_bounds(sovereignty_results):
    """Test 5: Verify V_ASI = H_Layer1 - H_Layer2 bounded in [-1, 1]."""
    df = sovereignty_results
    for _, row in df.iterrows():
        v = row["v_asi"]
        assert -1.0 <= v <= 1.0, f"{row['country_iso3']} V_ASI out of bounds: {v}"
        assert math.isclose(v, row["h_layer1"] - row["h_layer2"], abs_tol=1e-4)


def test_high_compute_trap_identification(sovereignty_results):
    """Test 6: Verify High-Compute Vulnerability Trap identifies SGP, USA, and HKG."""
    df = sovereignty_results.set_index("country_iso3")
    for iso in ["SGP", "USA", "HKG"]:
        assert iso in df.index, f"Missing country: {iso}"
        assert df.loc[iso, "high_compute_trap"] is True or df.loc[iso, "high_compute_trap"] == 1
        assert df.loc[iso, "v_asi"] >= 0.25


def test_sovereign_leaderboard_stability(sovereignty_results):
    """Test 7: Verify Nordic decentralizers occupy top 5 Layer 2 positions."""
    df = sovereignty_results.sort_values("rank_layer2")
    top_5_iso = df["country_iso3"].head(5).tolist()
    # NOR, FIN, ISL, DNK, SWE
    for expected_iso in ["NOR", "FIN", "ISL", "DNK", "SWE"]:
        assert expected_iso in top_5_iso, f"{expected_iso} not in top 5 Layer 2 sovereign nations"


def test_p5_epistemic_inviolability_seeds(sovereignty_results):
    """Test 8: Verify P5 and VSR values are valid across all 39 nations."""
    df = sovereignty_results
    for _, row in df.iterrows():
        p5 = row["p5_epistemic"]
        vsr = row["vsr"]
        assert 0.0 <= p5 <= 1.0
        assert 0.0 <= vsr <= 1.0
        assert p5 <= vsr, "P5 cannot exceed VSR (rho <= 1)"


def test_p6_decoupling_half_life_mapping(sovereignty_results):
    """Test 9: Verify P6 and T_half mappings satisfy hyperbolic normalization."""
    df = sovereignty_results
    for _, row in df.iterrows():
        t_half = row["t_half_hours"]
        p6 = row["p6_decoupling"]
        assert t_half > 0
        expected_p6 = t_half / (t_half + 720.0)
        assert math.isclose(p6, expected_p6, abs_tol=1e-3)


def test_p7_coordination_velocity_seeds(sovereignty_results):
    """Test 10: Verify P7 Multipolar Coordination Velocity is bounded in [0, 1]."""
    df = sovereignty_results
    for _, row in df.iterrows():
        p7 = row["p7_coordination"]
        v_coord = row["v_coord"]
        assert 0.0 <= p7 <= 1.0
        assert v_coord > 0
        assert p7 == min(1.0, max(0.0, v_coord))


def test_p8_post_labor_elasticity_seeds(sovereignty_results):
    """Test 11: Verify P8 Post-Labor Institutional Elasticity is strictly in [0, 1]."""
    df = sovereignty_results
    for _, row in df.iterrows():
        p8 = row["p8_post_labor"]
        assert 0.0 <= p8 <= 1.0


def test_rank_shift_bounds_and_conservation(sovereignty_results):
    """Test 12: Verify ranks and rank deltas are well-formed across 39 countries."""
    df = sovereignty_results
    assert len(df) == 39
    assert df["rank_layer1"].min() >= 1 and df["rank_layer1"].max() <= 39
    assert df["rank_layer2"].min() >= 1 and df["rank_layer2"].max() <= 39
    assert len(df["rank_layer1"].unique()) >= 35
    assert len(df["rank_layer2"].unique()) >= 35
    for _, row in df.iterrows():
        assert row["rank_delta_sovereignty"] == row["rank_layer1"] - row["rank_layer2"]
        assert -38 <= row["rank_delta_sovereignty"] <= 38


def test_bottleneck_pillar_identification(sovereignty_results):
    """Test 13: Verify each country has an identified valid Layer 2 bottleneck pillar."""
    df = sovereignty_results
    valid_bottlenecks = {
        "Epistemic Inviolability (P5)",
        "Decoupling Half-Life (P6)",
        "Coordination Velocity (P7)",
        "Post-Labor Elasticity (P8)"
    }
    for _, row in df.iterrows():
        b = row["layer2_bottleneck"]
        assert b in valid_bottlenecks, f"Invalid bottleneck: {b}"


def test_dirichlet_monte_carlo_audit_stability():
    """Test 14: Verify B=1,000 Dirichlet Monte Carlo audit achieves Kendall W >= 0.90."""
    audit_path = REPO_ROOT / "data" / "monte_carlo_layer2_audit.json"
    assert audit_path.exists(), "Monte Carlo audit JSON missing"

    with open(audit_path, "r", encoding="utf-8") as f:
        audit = json.load(f)

    assert audit["n_draws"] == 1000
    kendall_w = audit["kendall_w_layer2"]
    assert kendall_w >= 0.90, f"Kendall W too low: {kendall_w}"
    assert "spearman_l1_vs_l2" in audit
    assert "country_stability" in audit
    assert len(audit["country_stability"]) == 39


def test_exported_artifacts_schema_and_sync():
    """Test 15: Verify all exported Layer 2 files exist and match 39-country schema."""
    csv_path = REPO_ROOT / "data" / "hsri_layer2_variants.csv"
    json_path = REPO_ROOT / "site-astro" / "src" / "data" / "hsri_layer2.json"
    seeds_path = REPO_ROOT / "data" / "layer2_sovereignty_seeds.csv"

    assert csv_path.exists(), "hsri_layer2_variants.csv missing"
    assert json_path.exists(), "hsri_layer2.json missing"
    assert seeds_path.exists(), "layer2_sovereignty_seeds.csv missing"

    df_csv = pd.read_csv(csv_path)
    assert len(df_csv) == 39
    assert "v_asi" in df_csv.columns
    assert "high_compute_trap" in df_csv.columns

    with open(json_path, "r", encoding="utf-8") as f:
        json_records = json.load(f)
    assert len(json_records) == 39
    assert json_records[0]["country_iso3"] == df_csv.iloc[0]["country_iso3"]
