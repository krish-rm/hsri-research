"""
Unit and integration tests for ASI Synthetic Experiments (EXP-07-SYN and EXP-08-SYN).

Verifies:
1. AutonomousRdsSimulator multi-step swarm execution across 8h, 16h, and 24h horizons.
2. Error cascading dynamics and survival half-life in closed-loop reflection vs oracle feedback.
3. PersuasiveBeliefInversionSimulator identification of critical belief inversion boundary (Delta C*).
4. Epistemic verification depth buffering against persuasive machine asymmetry.
5. End-to-end MasterAsiSyntheticRunner execution, gating clearance (G1-G4), and report generation.
"""

from pathlib import Path
import sys
import pytest
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.asi_synthetic_experiments_runner import (
    AutonomousRdsSimulator,
    PersuasiveBeliefInversionSimulator,
    MasterAsiSyntheticRunner,
)


@pytest.fixture
def repo_paths():
    repo_root = Path(__file__).resolve().parent.parent
    protocol_doc = repo_root / "research" / "asi-transition" / "exp-07-08-syn-protocol.md"
    output_report = repo_root / "research" / "asi-transition" / "exp-07-08-syn-report.md"
    return {
        "repo_root": repo_root,
        "protocol_doc": protocol_doc,
        "output_report": output_report,
    }


def test_autonomous_rds_simulator_schema_and_metrics():
    """Verify autonomous R&D simulator produces valid schema and survival statistics."""
    sim = AutonomousRdsSimulator(n_trials=20, seed=42)
    res = sim.run_simulation()

    assert res["n_trials"] == 20
    assert res["max_steps"] == 48
    assert res["oracle_survival_h16_8h"] >= res["closed_survival_h16_8h"]
    assert res["survival_ratio_h48"] >= 1.0
    assert res["closed_half_life_steps"] > 0


def test_autonomous_rds_compounding_decay():
    """Verify compounding error cascades lead to survival collapse in closed loop."""
    sim = AutonomousRdsSimulator(n_trials=40, seed=123)
    res = sim.run_simulation()

    # Closed-loop survival should drop strictly over time: 8h >= 16h >= 24h
    assert res["closed_survival_h16_8h"] >= res["closed_survival_h32_16h"]
    assert res["closed_survival_h32_16h"] >= res["closed_survival_h48_24h"]
    # Oracle condition should maintain superior completion rates
    assert res["oracle_survival_h48_24h"] > res["closed_survival_h48_24h"]


def test_persuasive_belief_inversion_boundary():
    """Verify belief inversion simulator identifies non-trivial tipping point Delta C*."""
    sim = PersuasiveBeliefInversionSimulator(n_propositions=50, seed=42)
    res = sim.run_simulation()

    assert 1.00 <= res["inversion_boundary_dc"] <= 2.50
    assert res["buffer_ratio"] >= 0.50
    assert len(res["delta_c_grid"]) == 11


def test_verification_depth_armor_effect():
    """Verify epistemic verification depth buffers against persuasive asymmetry."""
    sim = PersuasiveBeliefInversionSimulator(n_propositions=50, seed=99)
    res = sim.run_simulation()
    curves = res["inversion_curves"]

    # At any given capability delta, deeper verification should have lower inversion rate
    for i in range(len(res["delta_c_grid"])):
        assert curves[4][i] <= curves[1][i] + 0.05


def test_master_asi_synthetic_runner_gating_and_report(repo_paths, tmp_path):
    """Verify master runner clears all G1-G4 gates and generates official report."""
    tmp_out = tmp_path / "test_syn_report.md"
    runner = MasterAsiSyntheticRunner(output_file=tmp_out)
    results = runner.run()

    assert tmp_out.exists()
    assert results["asi_synthetic_gating_cleared"] is True
    for gid, ginfo in results["gates"].items():
        assert ginfo["passed"] is True, f"Gate {gid} failed: {ginfo}"

    assert repo_paths["protocol_doc"].exists()
    assert repo_paths["output_report"].exists()
