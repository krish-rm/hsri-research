"""
Unit and integration tests for HSRI Phase 7 Cross-Cultural Measurement Invariance Engine
and International Test Commission (ITC) Adaptation Guidelines.
"""

from pathlib import Path
import sys
import pytest
import pandas as pd
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.cross_cultural_invariance import (
    generate_multigroup_cohort,
    compute_mgcfa_invariance_hierarchy,
    compute_differential_item_functioning,
    run_cross_cultural_validation,
    COHORTS,
    ROOT_DIR,
)


def test_generate_multigroup_cohort_balance_and_schema():
    """Verify multi-group cohort generation produces balanced international cohorts."""
    n_per_group = 100
    df = generate_multigroup_cohort(n_per_group=n_per_group, seed=42)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == n_per_group * len(COHORTS)

    # Check cohort balance
    cohort_counts = df["cohort_id"].value_counts().to_dict()
    for c in COHORTS:
        assert cohort_counts[c["id"]] == n_per_group

    # Verify column schema
    required_cols = [
        "subject_id", "cohort_id", "region",
        "eta_1", "eta_2", "eta_3", "eta_4",
        "exp_01", "exp_02", "exp_03", "exp_04", "exp_05", "exp_06", "exp_07", "exp_08", "exp_09",
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing column: {col}"


def test_mgcfa_invariance_hierarchy_standards():
    """Verify Configural, Metric, Scalar, and Strict invariance criteria (Chen 2007; Cheung & Rensvold 2002)."""
    df = generate_multigroup_cohort(n_per_group=500, seed=42)
    res = compute_mgcfa_invariance_hierarchy(df)
    models = res["models"]

    # Model 1: Configural fit
    assert models["configural"]["cfi"] >= 0.95
    assert models["configural"]["rmsea"] <= 0.05

    # Model 2: Metric fit (Weak invariance)
    assert models["metric"]["delta_cfi"] >= -0.010
    assert models["metric"]["delta_rmsea"] <= 0.015

    # Model 3: Scalar fit (Strong invariance — Core Gate)
    assert models["scalar"]["delta_cfi"] >= -0.010
    assert models["scalar"]["delta_rmsea"] <= 0.015
    assert models["scalar"]["delta_srmr"] <= 0.010
    assert res["scalar_invariance_pass"] is True
    assert res["phase_7_gating_cleared"] is True

    # Model 4: Strict fit
    assert models["strict"]["delta_cfi"] >= -0.010


def test_differential_item_functioning_zero_bias():
    """Verify that all 9 behavioral task items exhibit zero cultural bias (ETS Category A)."""
    df = generate_multigroup_cohort(n_per_group=500, seed=42)
    dif_items = compute_differential_item_functioning(df)
    assert len(dif_items) == 9

    for item in dif_items:
        assert item["is_invariant"] is True
        assert item["delta_alpha"] < 1.0, f"Item {item['item_code']} exceeded DIF threshold"
        assert "Category A" in item["ets_class"]


def test_phase_7_protocol_and_adaptation_guidelines_exist():
    """Verify existence and academic completeness of Phase 7 protocol and ITC guidelines."""
    psych_dir = ROOT_DIR / "research" / "psychometrics"
    proto_file = psych_dir / "phase-7-invariance-protocol.md"
    adapt_file = psych_dir / "cross-cultural-adaptation-guidelines.md"

    assert proto_file.exists(), "Phase 7 invariance protocol missing"
    assert adapt_file.exists(), "Cross-cultural adaptation guidelines missing"

    proto_text = proto_file.read_text(encoding="utf-8")
    assert "Configural Invariance" in proto_text
    assert "Scalar (Strong) Invariance" in proto_text
    assert "COHORT-A" in proto_text
    assert "COHORT-D" in proto_text

    adapt_text = adapt_file.read_text(encoding="utf-8")
    assert "International Test Commission" in adapt_text
    assert "Forward-Backward Translation" in adapt_text
    assert "Common Law" in adapt_text
    assert "Civil Law" in adapt_text


def test_run_cross_cultural_validation_pipeline(tmp_path):
    """Verify full end-to-end execution of cross-cultural validation pipeline."""
    report_file = tmp_path / "test-invariance-report.md"
    results = run_cross_cultural_validation(n_per_group=100, output_file=report_file)

    assert results["mgcfa"]["scalar_invariance_pass"] is True
    assert report_file.exists()
    content = report_file.read_text(encoding="utf-8")
    assert "GATE CLEARED (BUILD / ADVANCE TO PHASE 8: LONGITUDINAL STABILITY)" in content
    assert "Multi-Group CFA Invariance Hierarchy Results" in content
