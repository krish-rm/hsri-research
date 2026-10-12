"""
Unit and econometric validation tests for HSRI Non-Compensatory & Weakest-Link Aggregation
(Sprint 25 - Study 2).

Validates:
- Scale invariance across all four aggregation families (Linear, Geometric, Leontief, Choquet)
- Leontief critical zero-floor penalization
- Strict monotonicity and unit interval boundedness [0, 1]
- AM-GM inequality non-negativity of Vulnerability Index (V_n >= 0) and Floor Fragility (F_n >= 0)
- High-Compute Vulnerability Trap detection and balanced profile immunity
- Choquet integral 2-additive capacity subadditivity / synergistic resilience
- Rule 3 NaN governance
- 39-country dataset integrity, Spearman correlation ranges, and fragility tier assignments
- Deterministic B=1,000 Dirichlet Monte Carlo sensitivity analysis
"""

from pathlib import Path
import sys
import json
import pytest
import numpy as np
import pandas as pd
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.non_compensatory_engine import (
    calculate_linear,
    calculate_geometric,
    calculate_leontief,
    calculate_choquet,
    compute_country_variants,
    run_dirichlet_monte_carlo,
    assign_fragility_tier,
    DEFAULT_WEIGHTS,
)


# Test 1: Linear equal pillar invariance
def test_linear_equal_pillar_invariance():
    for val in [0.1, 0.45, 0.75, 1.0]:
        p = np.array([val, val, val, val])
        score = calculate_linear(p)
        assert pytest.approx(score, abs=1e-5) == val


# Test 2: Geometric equal pillar invariance
def test_geometric_equal_pillar_invariance():
    for val in [0.05, 0.3, 0.7, 0.95]:
        p = np.array([val, val, val, val])
        score = calculate_geometric(p, eps=0.01)
        assert pytest.approx(score, abs=1e-4) == val


# Test 3: Leontief equal pillar invariance
def test_leontief_equal_pillar_invariance():
    for val in [0.15, 0.5, 0.85, 1.0]:
        p = np.array([val, val, val, val])
        score = calculate_leontief(p, beta=0.5)
        assert pytest.approx(score, abs=1e-5) == val


# Test 4: Choquet equal pillar invariance
def test_choquet_equal_pillar_invariance():
    for val in [0.2, 0.6, 0.8, 1.0]:
        p = np.array([val, val, val, val])
        score = calculate_choquet(p)
        assert pytest.approx(score, abs=1e-5) == val


# Test 5: Zero floor penalization (Leontief collapses when weakest link is zero)
def test_zero_floor_penalization_leontief():
    # Unbalanced nation: 3 pillars at 0.9, but 1 critical pillar collapses to 0.0
    p = np.array([0.9, 0.0, 0.9, 0.9])
    h_lin = calculate_linear(p)
    h_leo = calculate_leontief(p, beta=0.5)
    
    # Linear compensatory hides the collapse: 3 * 0.9 / 4 = 0.675
    assert h_lin > 0.65
    # Leontief strictly penalizes the broken link to zero
    assert h_leo == 0.0


# Test 6: Strict monotonicity across all 4 models
def test_strict_monotonicity():
    p_base = np.array([0.5, 0.5, 0.5, 0.5])
    p_inc = np.array([0.5, 0.7, 0.5, 0.5])  # Improved discernment
    
    assert calculate_linear(p_inc) > calculate_linear(p_base)
    assert calculate_geometric(p_inc) > calculate_geometric(p_base)
    # Leontief increases because linear increases (min stays 0.5, linear increases)
    assert calculate_leontief(p_inc) > calculate_leontief(p_base)
    assert calculate_choquet(p_inc) > calculate_choquet(p_base)


# Test 7: Boundedness within the unit interval [0, 1]
def test_boundedness_unit_interval():
    test_cases = [
        np.array([0.0, 0.0, 0.0, 0.0]),
        np.array([1.0, 1.0, 1.0, 1.0]),
        np.array([0.001, 0.999, 0.05, 0.8]),
        np.array([0.3, 0.1, 0.95, 0.4]),
    ]
    for p in test_cases:
        for fn in [calculate_linear, calculate_geometric, calculate_leontief, calculate_choquet]:
            score = fn(p)
            assert 0.0 <= score <= 1.0, f"Function {fn.__name__} yielded out-of-bounds score: {score}"


# Test 8: Vulnerability Index non-negativity (AM-GM inequality)
def test_vulnerability_index_non_negative():
    rng = np.random.default_rng(101)
    for _ in range(50):
        p = rng.uniform(0.01, 1.0, size=4)
        h_lin = calculate_linear(p)
        h_geo = calculate_geometric(p, eps=0.01)
        v_n = h_lin - h_geo
        assert v_n >= -1e-6, f"AM-GM inequality violated: h_lin={h_lin}, h_geo={h_geo}, v_n={v_n}"


# Test 9: Floor Fragility non-negativity
def test_floor_fragility_non_negative():
    rng = np.random.default_rng(202)
    for _ in range(50):
        p = rng.uniform(0.01, 1.0, size=4)
        h_lin = calculate_linear(p)
        h_leo = calculate_leontief(p, beta=0.5)
        f_n = h_lin - h_leo
        assert f_n >= -1e-6, f"Weakest link fragility violated: h_lin={h_lin}, h_leo={h_leo}"


# Test 10: High-Compute Vulnerability Trap detection
def test_high_compute_trap_detection():
    # Profile: World-class data centers (P_infra=0.95) but low critical discernment (P_disc=0.20)
    trap_df = pd.DataFrame([{
        "country_iso3": "TRP",
        "AI_Literacy_score": 0.65,
        "Critical_Discernment_score": 0.20,
        "Institutional_Governance_score": 0.60,
        "Digital_Infrastructure_score": 0.95,
    }])
    res = compute_country_variants(trap_df)
    row = res.iloc[0]
    
    assert row["vulnerability_index"] > 0.02
    assert row["high_compute_trap"] is True or row["high_compute_trap"] == 1
    assert row["bottleneck_pillar"] == "Critical Discernment"


# Test 11: Balanced profile immunity
def test_balanced_profile_immunity():
    # Balanced nation with harmonious development across all pillars
    bal_df = pd.DataFrame([{
        "country_iso3": "BAL",
        "AI_Literacy_score": 0.70,
        "Critical_Discernment_score": 0.70,
        "Institutional_Governance_score": 0.70,
        "Digital_Infrastructure_score": 0.70,
    }])
    res = compute_country_variants(bal_df)
    row = res.iloc[0]
    
    assert row["vulnerability_index"] < 0.001
    assert row["high_compute_trap"] is False or row["high_compute_trap"] == 0
    assert row["fragility_tier"] == "Low"


# Test 12: Choquet 2-additive capacity subadditivity / synergy
def test_choquet_subadditivity_infrastructure_penalty():
    # Isolated infrastructure without discernment vs with discernment
    p_isolated_infra = np.array([0.2, 0.2, 0.2, 0.8])
    p_synergistic = np.array([0.2, 0.8, 0.2, 0.8])
    
    h_choq_isolated = calculate_choquet(p_isolated_infra)
    h_lin_isolated = calculate_linear(p_isolated_infra)
    
    # In isolated infrastructure, Choquet score should be suppressed compared to linear
    assert h_choq_isolated < h_lin_isolated


# Test 13: 39 benchmark countries complete coverage
def test_all_39_countries_coverage():
    data_file = REPO_ROOT / "data" / "final_country_scores.csv"
    assert data_file.exists()
    df = pd.read_csv(data_file)
    res = compute_country_variants(df)
    
    assert len(res) == 39
    assert set(res["country_iso3"]) == set(df["country_iso3"])
    assert not res[["hsri_linear", "hsri_geometric", "hsri_leontief", "hsri_choquet"]].isna().any().any()


# Test 14: Spearman rank correlation ranges
def test_spearman_rank_correlation_ranges():
    csv_file = REPO_ROOT / "data" / "hsri_variants.csv"
    assert csv_file.exists()
    df = pd.read_csv(csv_file)
    
    spearman_geo, _ = stats.spearmanr(df["rank_linear"], df["rank_geometric"])
    spearman_leo, _ = stats.spearmanr(df["rank_linear"], df["rank_leontief"])
    spearman_choq, _ = stats.spearmanr(df["rank_linear"], df["rank_choquet"])
    
    assert spearman_geo > 0.95
    assert spearman_leo > 0.90
    assert spearman_choq > 0.95


# Test 15: Dirichlet Monte Carlo determinism
def test_dirichlet_monte_carlo_determinism():
    data_file = REPO_ROOT / "data" / "final_country_scores.csv"
    df = pd.read_csv(data_file)
    
    audit1 = run_dirichlet_monte_carlo(df, n_draws=50, seed=123)
    audit2 = run_dirichlet_monte_carlo(df, n_draws=50, seed=123)
    
    assert audit1["kendall_w"] == audit2["kendall_w"]
    assert audit1["spearman_correlations"]["lin_vs_leo"]["mean"] == audit2["spearman_correlations"]["lin_vs_leo"]["mean"]


# Test 16: Rule 3 NaN handling
def test_rule_3_nan_handling():
    p_with_nan = np.array([0.5, np.nan, 0.7, 0.8])
    with pytest.raises(ValueError, match="Rule 3"):
        calculate_linear(p_with_nan)
    with pytest.raises(ValueError, match="Rule 3"):
        calculate_geometric(p_with_nan)
    with pytest.raises(ValueError, match="Rule 3"):
        calculate_leontief(p_with_nan)
    with pytest.raises(ValueError, match="Rule 3"):
        calculate_choquet(p_with_nan)


# Test 17: Export CSV and JSON schema consistency
def test_export_csv_and_json_schema():
    csv_path = REPO_ROOT / "data" / "hsri_variants.csv"
    json_path = REPO_ROOT / "site-astro" / "src" / "data" / "hsri_variants.json"
    
    assert csv_path.exists()
    assert json_path.exists()
    
    csv_df = pd.read_csv(csv_path)
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        
    assert len(csv_df) == len(json_data) == 39
    required_cols = [
        "country_iso3", "hsri_linear", "hsri_geometric", "hsri_leontief", "hsri_choquet",
        "rank_linear", "rank_geometric", "rank_leontief", "rank_choquet",
        "vulnerability_index", "floor_fragility", "fragility_tier", "high_compute_trap"
    ]
    for col in required_cols:
        assert col in csv_df.columns
        assert col in json_data[0]


# Test 18: Fragility tier assignment
def test_fragility_tier_assignment():
    assert assign_fragility_tier(0.06) == "Critical"
    assert assign_fragility_tier(0.05) == "Critical"
    assert assign_fragility_tier(0.03) == "High"
    assert assign_fragility_tier(0.02) == "High"
    assert assign_fragility_tier(0.01) == "Moderate"
    assert assign_fragility_tier(0.005) == "Moderate"
    assert assign_fragility_tier(0.002) == "Low"
    assert assign_fragility_tier(0.0) == "Low"
