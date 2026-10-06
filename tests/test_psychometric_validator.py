"""
Unit and integration tests for HSRI Phase 6 Psychometric Validation Engine
and IRB Ethics Protocol Dossier.
"""

from pathlib import Path
import sys
import pytest
import pandas as pd
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.psychometric_validator import (
    generate_validation_cohort,
    compute_mtmm_matrix,
    compute_incremental_validity,
    compute_cfa_fit_indices,
    run_psychometric_validation,
    ROOT_DIR,
)


def test_generate_validation_cohort():
    """Verify synthetic validation cohort generation and schema."""
    n = 200
    df = generate_validation_cohort(n=n, seed=42)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == n

    required_cols = [
        "subject_id", "theta",
        "eta_1_discernment", "eta_2_default_res", "eta_3_agency", "eta_4_epistemic",
        "crt2", "ai_literacy", "trust_automation", "self_efficacy",
        "exp_01", "exp_02", "exp_03", "exp_04", "exp_05", "exp_06", "exp_07", "exp_08", "exp_09",
        "diag_discernment", "diag_default", "diag_agency",
        "neuroticism", "tech_optimism", "y_override",
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"

    assert df["subject_id"].iloc[0] == "SUBJ-0001"
    assert df["subject_id"].iloc[-1] == f"SUBJ-{n:04d}"


def test_mtmm_matrix_construct_validity():
    """Verify Campbell & Fiske Multitrait-Multimethod convergent and discriminant thresholds."""
    df = generate_validation_cohort(n=1080, seed=42)
    mtmm = compute_mtmm_matrix(df)

    # Convergent validity: Monotrait-heteromethod correlation must be strong (> 0.50)
    assert mtmm["convergent_discernment"] > 0.50
    assert mtmm["convergent_default"] > 0.50
    assert mtmm["convergent_agency"] > 0.50

    # Discriminant validity: Heterotrait correlation must be lower than convergent (< 0.35)
    assert mtmm["discriminant_cross_trait_avg"] < 0.35
    assert mtmm["discriminant_cross_trait_avg"] < mtmm["convergent_discernment"]

    # Divergent validity: Unrelated personality/attitude traits must correlate near zero (|r| < 0.15)
    assert abs(mtmm["divergent_neuroticism"]) < 0.15
    assert abs(mtmm["divergent_tech_optimism"]) < 0.15


def test_incremental_validity_decisive_gate():
    """Verify that HSRI passes the core Phase 6 gating requirement (Delta R^2 >= 0.15, p < .001)."""
    df = generate_validation_cohort(n=1080, seed=42)
    inc_val = compute_incremental_validity(df)

    assert inc_val["r2_full"] > inc_val["r2_baseline"]
    assert inc_val["delta_r2"] >= 0.15, f"Delta R^2 was {inc_val['delta_r2']:.4f}, expected >= 0.15"
    assert inc_val["p_value"] < 0.001, f"p-value was {inc_val['p_value']}, expected < 0.001"
    assert inc_val["incremental_validity_pass"] is True


def test_cfa_fit_indices():
    """Verify Confirmatory Factor Analysis fit indices satisfy Hu & Bentler (1999) standards."""
    df = generate_validation_cohort(n=1080, seed=42)
    cfa = compute_cfa_fit_indices(df)

    assert cfa["rmsea"] <= 0.05
    assert cfa["cfi"] >= 0.95
    assert cfa["tli"] >= 0.95
    assert cfa["srmr"] <= 0.08


def test_irb_dossier_documents_exist_and_complete():
    """Verify that all 4 university IRB ethics dossier documents are present and rigorous."""
    irb_dir = ROOT_DIR / "research" / "irb-protocol"
    assert irb_dir.exists() and irb_dir.is_dir()

    expected_files = [
        ("00-master-irb-protocol.md", ["HSRI-IRB-2026-088", "Minimal Risk", "45 CFR 46"]),
        ("01-human-subjects-consent-form.md", ["Informed Consent", "Voluntary Participation", "I AGREE TO PARTICIPATE"]),
        ("02-risk-mitigation-and-debriefing.md", ["Debriefing", "Incomplete Disclosure", "automation complacency"]),
        ("03-data-protection-and-zenodo-plan.md", ["Zenodo", "CC-BY-4.0", "SHA-256", "FAIR Data"]),
    ]

    for filename, expected_keywords in expected_files:
        doc_path = irb_dir / filename
        assert doc_path.exists(), f"IRB file missing: {filename}"
        content = doc_path.read_text(encoding="utf-8")
        assert len(content) > 500, f"IRB file {filename} is too short"
        for kw in expected_keywords:
            assert kw.lower() in content.lower(), f"Keyword '{kw}' missing from {filename}"


def test_run_psychometric_validation_pipeline(tmp_path):
    """Verify full end-to-end execution of psychometric validation engine."""
    report_file = tmp_path / "test-validation-report.md"
    results = run_psychometric_validation(n=300, output_file=report_file)

    assert results["incremental_validity"]["incremental_validity_pass"] is True
    assert report_file.exists()
    content = report_file.read_text(encoding="utf-8")
    assert "GATE CLEARED (BUILD / ADVANCE TO PHASE 7)" in content
    assert "Confirmatory Factor Analysis (CFA)" in content
