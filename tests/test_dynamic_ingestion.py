"""
Unit and integration tests for Phase 11: Real-Time Dynamic Ingestion & Global Continuous Calibration Pipeline.

Verifies:
1. Kalman indicator smoother noise attenuation and variance reduction ratio (VRR <= 0.850).
2. Kalman filter resilience to missing data / NaNs.
3. Statistical drift detection via Population Stability Index (PSI) and Kolmogorov-Smirnov test.
4. Active indicator connectors coverage (100% health rate).
5. Continuous re-calibration rank stability (rho >= 0.950).
6. End-to-end pipeline execution, gating clearance (G1-G6), and report generation.
"""

from pathlib import Path
import sys
import pytest
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.dynamic_ingestion_pipeline import (
    KalmanIndicatorSmoother,
    StatisticalDriftDetector,
    DynamicIngestionPipeline,
)


@pytest.fixture
def repo_paths():
    repo_root = Path(__file__).resolve().parent.parent
    data_dir = repo_root / "data"
    output_report = repo_root / "research" / "evidence" / "phase-11-dynamic-ingestion-report.md"
    protocol_doc = repo_root / "research" / "evidence" / "phase-11-dynamic-ingestion-protocol.md"
    return {
        "repo_root": repo_root,
        "data_dir": data_dir,
        "output_report": output_report,
        "protocol_doc": protocol_doc,
    }


def test_kalman_filter_smoother_reduces_noise():
    """Verify Kalman filter attenuates observation noise and produces low VRR."""
    np.random.seed(42)
    true_signal = np.linspace(0.40, 0.65, 30)
    noisy_obs = true_signal + np.random.normal(0, 0.08, len(true_signal))

    smoother = KalmanIndicatorSmoother(process_noise_q=0.0025, measurement_noise_r=0.0400)
    res = smoother.filter_series(noisy_obs)

    assert len(res["smoothed"]) == len(noisy_obs)
    assert res["vrr"] <= 0.850
    assert abs(res["mean_innovation"]) <= 0.050


def test_kalman_filter_nan_resilience():
    """Verify Kalman filter smoothly bridges over missing data / NaNs without divergence."""
    obs_with_nans = np.array([np.nan, 0.50, 0.52, np.nan, np.nan, 0.55, 0.54, np.nan])
    smoother = KalmanIndicatorSmoother()
    res = smoother.filter_series(obs_with_nans)

    assert not np.isnan(res["smoothed"]).any()
    assert not np.isnan(res["variances"]).any()
    assert 0.40 <= res["final_estimate"] <= 0.65


def test_statistical_drift_detector_psi_and_ks():
    """Verify drift detector accurately classifies stable vs severely drifted batches."""
    np.random.seed(42)
    ref = np.random.normal(0.50, 0.10, 500)
    stream_stable = np.random.normal(0.50, 0.10, 500)
    stream_drift = np.random.normal(0.72, 0.10, 500)

    stable_eval = StatisticalDriftDetector.evaluate_drift(ref, stream_stable)
    drift_eval = StatisticalDriftDetector.evaluate_drift(ref, stream_drift)

    assert stable_eval["status"] == "STABLE"
    assert stable_eval["psi"] < 0.100
    assert stable_eval["ks_pvalue"] > 0.05

    assert drift_eval["status"] == "SIGNIFICANT_DRIFT"
    assert drift_eval["psi"] >= 0.250
    assert drift_eval["ks_pvalue"] < 0.01


def test_dynamic_ingestion_pipeline_connectors_and_data(repo_paths):
    """Verify all 17 core indicators are tracked across upstream multilateral sources."""
    pipeline = DynamicIngestionPipeline(data_dir=repo_paths["data_dir"], output_file=repo_paths["output_report"])
    assert len(pipeline.INDICATOR_SOURCES) == 17
    assert "AI_LIT_001" in pipeline.INDICATOR_SOURCES
    assert "ENAB_005" in pipeline.INDICATOR_SOURCES


def test_continuous_recalibration_rank_stability(repo_paths, tmp_path):
    """Verify continuous dynamic re-calibration preserves rank stability (rho >= 0.950)."""
    tmp_out = tmp_path / "test_report.md"
    pipeline = DynamicIngestionPipeline(data_dir=repo_paths["data_dir"], output_file=tmp_out, seed=123)
    results = pipeline.execute_pipeline()

    assert results["recalibration_rho"] >= 0.950
    assert results["connector_health_rate"] == 1.0


def test_end_to_end_phase_11_gating_clearance(repo_paths, tmp_path):
    """Verify master pipeline clears all G1-G6 gates and generates official report."""
    tmp_out = tmp_path / "phase11_test.md"
    pipeline = DynamicIngestionPipeline(data_dir=repo_paths["data_dir"], output_file=tmp_out, seed=42)
    results = pipeline.execute_pipeline()

    assert results["phase_11_gating_cleared"] is True
    for gid, ginfo in results["gates"].items():
        assert ginfo["passed"] is True, f"Gate {gid} failed: {ginfo}"

    assert repo_paths["protocol_doc"].exists()
    assert repo_paths["output_report"].exists()
