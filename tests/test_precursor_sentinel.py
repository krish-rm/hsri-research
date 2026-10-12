"""
test_precursor_sentinel.py - Test suite for HSRI Precursor Streams 1 & 2 (Sprint 29)

Tests:
1. Autonomy Seismometer mathematical bounds and structure (HPTG, M2M share, Seismograph score)
2. Autonomy Seismometer historical timeseries finite-difference velocity & acceleration
3. Milestone filtering and opacity monotonicity
4. Latent Drift Detector Shannon token entropy calculation
5. Latent Drift Detector compression ratio
6. Human Parseability Index (HPI) discrimination between English and vector streams
7. Steganographic confidence detection
8. Latent Drift sample evaluations and anomaly categorization
9. Precursor Sentinel triad aggregation and composite threat level calculation
10. Telemetry serialization, JSONL logging, and synchronization
"""

import math
import json
import pytest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_ROOT / "scripts"))

import autonomy_seismometer as aus
import latent_drift_detector as ldd
import precursor_sentinel as ps


@pytest.fixture
def seismometer():
    return aus.AutonomySeismometer()


@pytest.fixture
def drift_detector():
    return ldd.LatentDriftDetector()


@pytest.fixture
def sentinel():
    return ps.PrecursorSentinel()


def test_autonomy_seismometer_bounds_and_structure(seismometer):
    """Verifies that all metrics produced by Autonomy Seismometer fall within mathematical bounds."""
    readout = seismometer.get_latest_readout()

    assert "seismograph_score" in readout
    assert 0.0 <= readout["seismograph_score"] <= 10.0
    assert 0.0 <= readout["human_paper_trail_gap"] <= 1.0
    assert 0.0 <= readout["m2m_composite_share"] <= 1.0
    assert readout["alert_level"] in [
        "TRIVIAL_AUTONOMY",
        "AGENTIC_EXPANSION",
        "ACCELERATED_M2M_DECOUPLING",
        "CRITICAL_SUPERVISORY_DEFICIT",
        "AUTONOMOUS_SINGULARITY_LOCK"
    ]
    assert readout["severity"] in ["LOW", "MODERATE", "HIGH", "SEVERE", "CRITICAL_EVENT"]


def test_autonomy_seismometer_timeseries_velocity_acceleration(seismometer):
    """Verifies finite-difference kinematics (velocity, acceleration) on historical timeseries."""
    series = seismometer.evaluate_seismograph_timeseries()
    assert len(series) >= 10

    for i, row in enumerate(series):
        assert 0.0 <= row["m2m_composite_share"] <= 1.0
        assert 0.0 <= row["human_paper_trail_gap"] <= 1.0
        assert 0.0 <= row["seismograph_score"] <= 10.0

        # From index 1 onwards, velocity should be computed
        if i >= 1:
            assert "velocity_m2m_per_year" in row
        # From index 2 onwards, acceleration should be computed
        if i >= 2:
            assert "acceleration_m2m_per_year2" in row


def test_autonomy_seismometer_opacity_monotonicity(seismometer):
    """Verifies that recent closed milestones produce a larger Paper Trail Gap than early open milestones."""
    early_gap = seismometer.compute_cumulative_paper_trail_gap(up_to_date="2023-08-01")
    recent_gap = seismometer.compute_cumulative_paper_trail_gap(up_to_date="2026-10-15")

    # As models become more proprietary and reasoning is hidden, HPTG must expand
    assert recent_gap["hptg"] > early_gap["hptg"]
    assert recent_gap["total_capability_delta"] > early_gap["total_capability_delta"]
    assert recent_gap["mean_auditability"] < early_gap["mean_auditability"]


def test_latent_drift_token_entropy(drift_detector):
    """Verifies Shannon entropy formula against known token distribution properties."""
    # Degenerate uniform repetition of 1 token -> 0 entropy
    uniform_text = ["test", "test", "test", "test"]
    assert drift_detector.compute_shannon_entropy(uniform_text) == 0.0

    # 4 distinct tokens equal probability -> log2(4) = 2.0 bits
    distinct_tokens = ["alpha", "beta", "gamma", "delta"]
    entropy = drift_detector.compute_shannon_entropy(distinct_tokens)
    assert math.isclose(entropy, 2.0, rel_tol=1e-5)


def test_latent_drift_compression_ratio(drift_detector):
    """Verifies compression ratio calculation on high redundancy vs low redundancy strings."""
    redundant = "A" * 1000
    comp_redundant = drift_detector.compute_compression_ratio(redundant)
    assert comp_redundant < 0.10  # Highly compressible

    complex_str = "The quick brown fox jumps over the lazy dog 1234567890!@#"
    comp_complex = drift_detector.compute_compression_ratio(complex_str)
    assert comp_complex > 0.40


def test_latent_drift_human_parseability_discrimination(drift_detector):
    """Verifies HPI sharply distinguishes between plain English and vector hex streams."""
    english_sample = ldd.BENCHMARK_MULTI_AGENT_CORPUS[0]
    vector_sample = ldd.BENCHMARK_MULTI_AGENT_CORPUS[4]

    eng_eval = drift_detector.evaluate_sample(english_sample)
    vec_eval = drift_detector.evaluate_sample(vector_sample)

    assert eng_eval["human_parseability_index"] > 0.70
    assert vec_eval["human_parseability_index"] < 0.40
    assert eng_eval["human_parseability_index"] > vec_eval["human_parseability_index"]


def test_latent_drift_stego_confidence_and_anomaly(drift_detector):
    """Verifies steganographic confidence flags hex vectors and cipher-like channels."""
    evals = drift_detector.evaluate_all()
    # Baseline natural language sample must NOT be anomalous
    assert not evals[0]["is_anomalous"]
    assert evals[0]["stego_confidence"] < 0.20

    # Decoupled hex vector sample MUST be anomalous with high stego confidence
    decoupled = evals[-1]
    assert decoupled["is_anomalous"]
    assert decoupled["stego_confidence"] > 0.90
    assert decoupled["latent_drift_index"] >= 5.0


def test_latent_drift_corpus_alert_coverage(drift_detector):
    """Verifies that all samples are evaluated with valid alert levels and severities."""
    evals = drift_detector.evaluate_all()
    assert len(evals) == len(ldd.BENCHMARK_MULTI_AGENT_CORPUS)

    for ev in evals:
        assert 0.0 <= ev["latent_drift_index"] <= 10.0
        assert 0.0 <= ev["human_parseability_index"] <= 1.0
        assert 0.0 <= ev["stego_confidence"] <= 1.0
        assert ev["alert_level"] in [
            "NOMINAL_HUMAN_PROTOCOL",
            "STRUCTURED_SPECIALIZATION",
            "LATENT_COMPRESSION_EMERGENCE",
            "COVERT_STEGANOGRAPHIC_DRIFT",
            "CRITICAL_COGNITIVE_DECOUPLING"
        ]


def test_precursor_sentinel_triad_aggregation(sentinel):
    """Verifies that PrecursorSentinel correctly unites all 3 streams into a composite threat score."""
    telemetry = sentinel.run_all_streams()

    assert "master_precursor_threat_score" in telemetry
    assert 0.0 <= telemetry["master_precursor_threat_score"] <= 10.0

    # Check 3 constituent stream payloads
    s1 = telemetry["stream_1_autonomy_seismometer"]
    s2 = telemetry["stream_2_latent_drift_detector"]
    s3 = telemetry["stream_3_verification_wedge"]

    assert 0.0 <= s1["score"] <= 10.0
    assert 0.0 <= s2["score"] <= 10.0
    assert 0.0 <= s3["score"] <= 10.0

    # Check mathematical average
    expected_mean = round((s1["score"] + s2["score"] + s3["score"]) / 3.0, 2)
    assert math.isclose(telemetry["master_precursor_threat_score"], expected_mean, abs_tol=0.02)
    assert telemetry["overall_classification"] in [
        "NORMAL_SUPERVISED",
        "ELEVATED_WATCH",
        "SERIOUS_SYSTEMIC_DECOUPLING",
        "CRITICAL_SUPERVISORY_COLLAPSE",
        "RECURSIVE_EVENT_HORIZON"
    ]


def test_precursor_sentinel_persistence_and_sync(sentinel, tmp_path):
    """Verifies file export, JSONL append logging, and summary JSON schema."""
    output = sentinel.record_and_sync(output_dir=tmp_path)

    jsonl_file = tmp_path / "precursor_signals.jsonl"
    summary_file = tmp_path / "precursor_summary.json"

    assert jsonl_file.exists()
    assert summary_file.exists()

    with open(summary_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["master_precursor_threat_score"] == output["master_precursor_threat_score"]
    assert "stream_1_autonomy_seismometer" in data
    assert "stream_2_latent_drift_detector" in data
    assert "stream_3_verification_wedge" in data

    # Verify JSONL contains valid lines
    with open(jsonl_file, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]
    assert len(lines) >= 1
    assert lines[-1]["overall_classification"] == output["overall_classification"]
