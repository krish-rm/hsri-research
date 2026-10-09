"""
Unit and integration tests for HSRI Phase 8 Longitudinal Stability Engine,
Test-Retest Reliability, and Parallel Alternate Forms Specification.
"""

from pathlib import Path
import sys
import pytest
import pandas as pd
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.longitudinal_stability_validator import (
    generate_longitudinal_cohort,
    compute_test_retest_metrics,
    compute_lst_variance_decomposition,
    compute_reliable_change_index,
    run_longitudinal_validation,
    ROOT_DIR,
)


def test_generate_longitudinal_cohort_schema_and_balance():
    """Verify longitudinal cohort schema, balance, and counterbalancing."""
    n = 200
    df = generate_longitudinal_cohort(n=n, seed=42)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == n

    # Check counterbalancing balance
    counts = df["form_order"].value_counts().to_dict()
    assert abs(counts["A_then_B"] - counts["B_then_A"]) <= 1

    # Verify column schema
    required_cols = [
        "subject_id", "form_order",
        "f1_discernment_t0", "f1_discernment_t1",
        "f2_default_res_t0", "f2_default_res_t1",
        "f3_agency_t0", "f3_agency_t1",
        "f4_epistemic_t0", "f4_epistemic_t1",
        "hsri_composite_t0", "hsri_composite_t1",
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"


def test_test_retest_reliability_thresholds():
    """Verify 30-day temporal stability (r_tt >= 0.80, ICC(3,1) >= 0.75, Cohen's d < 0.20)."""
    df = generate_longitudinal_cohort(n=600, seed=42)
    res = compute_test_retest_metrics(df)
    factors = res["factors"]

    # Composite HSRI must be stable
    hsri_meta = factors["Composite HSRI Score"]
    assert hsri_meta["r_tt"] >= 0.80, f"r_tt was {hsri_meta['r_tt']:.3f}, expected >= 0.80"
    assert hsri_meta["icc_3_1"] >= 0.75, f"ICC was {hsri_meta['icc_3_1']:.3f}, expected >= 0.75"
    assert hsri_meta["cohens_d"] < 0.20, f"Practice effect was {hsri_meta['cohens_d']:.3f}, expected < 0.20"
    assert hsri_meta["is_stable"] is True
    assert res["composite_stable"] is True

    # Individual factors must all satisfy minimum stability
    for name, f in factors.items():
        assert f["r_tt"] >= 0.80, f"Factor {name} r_tt failed: {f['r_tt']:.3f}"
        assert f["icc_3_1"] >= 0.75, f"Factor {name} ICC failed: {f['icc_3_1']:.3f}"


def test_lst_variance_decomposition():
    """Verify Latent State-Trait consistency (CO >= 0.70, SP <= 0.20, ERR <= 0.10)."""
    df = generate_longitudinal_cohort(n=600, seed=42)
    lst = compute_lst_variance_decomposition(df)

    assert lst["consistency_co"] >= 0.70
    assert lst["specificity_sp"] <= 0.20
    assert lst["error_err"] <= 0.10
    assert lst["lst_gating_pass"] is True


def test_reliable_change_index_calibration():
    """Verify Reliable Change Index (RCI) critical difference under Jacobson & Truax (1991)."""
    df = generate_longitudinal_cohort(n=600, seed=42)
    rci = compute_reliable_change_index(df, r_tt=0.918)

    assert rci["sample_sd"] > 0
    assert rci["se_measurement"] > 0
    assert rci["s_diff"] > 0
    assert 0.30 <= rci["rci_critical_diff_95"] <= 0.90


def test_phase_8_protocol_and_parallel_forms_spec_exist():
    """Verify existence and academic completeness of Phase 8 protocol and parallel forms spec."""
    psych_dir = ROOT_DIR / "research" / "psychometrics"
    proto_file = psych_dir / "phase-8-longitudinal-protocol.md"
    forms_file = psych_dir / "parallel-forms-specification.md"

    assert proto_file.exists(), "Phase 8 longitudinal protocol missing"
    assert forms_file.exists(), "Parallel forms specification missing"

    proto_text = proto_file.read_text(encoding="utf-8")
    assert "Latent State-Trait" in proto_text
    assert "Intraclass Correlation" in proto_text
    assert "Reliable Change Index" in proto_text

    forms_text = forms_file.read_text(encoding="utf-8")
    assert "Form A" in forms_text
    assert "Form B" in forms_text
    assert "EXP-01" in forms_text
    assert "EXP-09" in forms_text


def test_run_longitudinal_validation_pipeline(tmp_path):
    """Verify full end-to-end execution of longitudinal validation pipeline."""
    report_file = tmp_path / "test-longitudinal-report.md"
    results = run_longitudinal_validation(n=200, output_file=report_file)

    assert results["retest_metrics"]["composite_stable"] is True
    assert report_file.exists()
    content = report_file.read_text(encoding="utf-8")
    assert "GATE CLEARED (BUILD / ADVANCE TO PHASE 9: MULTI-AGENT ADVERSARIAL CONSENSUS)" in content
    assert "Latent State-Trait (LST) Variance Decomposition" in content
