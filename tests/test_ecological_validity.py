"""
Unit and integration tests for Phase 10: Ecological Validity & National Composite Econometric Audit.

Verifies:
1. InSituWorkflowSimulator execution, output schema, accuracy, DLR, and latency wedge.
2. Domain-specific budget scaling across Finance, Cyber, Medicine, and Legal.
3. OECD/JRC data completeness audit (missingness < 5.0%).
4. Multicollinearity condition number (< 30.0) and PCA variance extraction (>= 65.0%).
5. Monte Carlo rank stability (rho >= 0.850) and Kendall's W (>= 0.850).
6. End-to-end MasterEcologicalValidityRunner execution and gating clearance (G1-G8).
"""

from pathlib import Path
import sys
import pytest
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.ecological_validity_runner import (
    InSituWorkflowSimulator,
    OecdEconometricAuditor,
    MasterEcologicalValidityRunner,
)


@pytest.fixture
def repo_paths():
    repo_root = Path(__file__).resolve().parent.parent
    data_dir = repo_root / "data"
    output_report = repo_root / "research" / "evidence" / "phase-10-ecological-validity-report.md"
    protocol_doc = repo_root / "research" / "evidence" / "phase-10-ecological-validity-protocol.md"
    return {
        "repo_root": repo_root,
        "data_dir": data_dir,
        "output_report": output_report,
        "protocol_doc": protocol_doc,
    }


def test_in_situ_workflow_simulator_schema_and_metrics():
    """Verify in-situ operator simulation returns valid metrics and meets core thresholds."""
    sim = InSituWorkflowSimulator(n_operators=40, trials_per_op=20, seed=42)
    res = sim.run_simulation()

    assert res["n_operators"] == 40
    assert res["total_trials"] == 800
    assert 0.70 <= res["mean_situ_accuracy"] <= 1.00
    assert 0.00 <= res["mean_defect_leakage_rate"] <= 0.25
    assert res["mean_verification_wedge_sec"] > 0.0
    assert res["concordance_margin"] <= 0.080


def test_domain_breakdown_consistency():
    """Verify domain-specific latency budgets scale appropriately across professional domains."""
    sim = InSituWorkflowSimulator(n_operators=40, trials_per_op=10, seed=123)
    res = sim.run_simulation()
    domains = res["domain_breakdown"]

    assert set(domains.keys()) == {"DOM-FIN", "DOM-CYB", "DOM-MED", "DOM-LEG"}
    # Finance should have lowest verification wedge, Legal highest
    assert domains["DOM-FIN"]["mean_wedge_sec"] < domains["DOM-CYB"]["mean_wedge_sec"]
    assert domains["DOM-CYB"]["mean_wedge_sec"] < domains["DOM-MED"]["mean_wedge_sec"]
    assert domains["DOM-MED"]["mean_wedge_sec"] < domains["DOM-LEG"]["mean_wedge_sec"]


def test_oecd_data_completeness_and_missingness(repo_paths):
    """Verify OECD/JRC data completeness audit satisfies missingness threshold (< 5%)."""
    auditor = OecdEconometricAuditor(data_dir=repo_paths["data_dir"], b_iterations=50, seed=42)
    res = auditor.audit()

    assert res["n_countries"] == 39
    assert res["n_indicators"] == 17
    assert res["missing_data_rate"] < 0.050
    assert res["missing_cells"] == 23


def test_oecd_multicollinearity_and_pca_variance(repo_paths):
    """Verify SVD condition index (< 30.0) and PCA cumulative variance extraction (>= 65%)."""
    auditor = OecdEconometricAuditor(data_dir=repo_paths["data_dir"], b_iterations=50, seed=42)
    res = auditor.audit()

    assert res["condition_number"] < 30.0
    assert res["pca_cumulative_var_4"] >= 0.650


def test_monte_carlo_rank_stability_and_kendalls_w(repo_paths):
    """Verify Monte Carlo sensitivity analysis exhibits high rank stability (rho, W >= 0.850)."""
    auditor = OecdEconometricAuditor(data_dir=repo_paths["data_dir"], b_iterations=100, seed=99)
    res = auditor.audit()

    assert res["mean_spearman_rho"] >= 0.850
    assert res["kendalls_w"] >= 0.850
    assert len(res["pilot_cohort"]) == 5
    pilot_iso3s = {p["iso3"] for p in res["pilot_cohort"]}
    assert pilot_iso3s == {"USA", "DEU", "JPN", "SGP", "GBR"}


def test_master_runner_end_to_end_and_gating(repo_paths, tmp_path):
    """Verify end-to-end master runner clears all G1-G8 gates and generates markdown report."""
    test_output = tmp_path / "test_phase10_report.md"
    runner = MasterEcologicalValidityRunner(
        data_dir=repo_paths["data_dir"],
        output_file=test_output,
        n_ops=60,
        mc_iters=100,
    )
    results = runner.run()

    assert test_output.exists()
    assert results["phase_10_gating_cleared"] is True
    for gid, ginfo in results["gates"].items():
        assert ginfo["passed"] is True, f"Gate {gid} failed: {ginfo}"

    # Also verify official protocol and report files exist in repo
    assert repo_paths["protocol_doc"].exists()
    assert repo_paths["output_report"].exists()
