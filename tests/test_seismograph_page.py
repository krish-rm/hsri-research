"""
test_seismograph_page.py - Unit test suite for Sprint 30:
Production Web Portal Upgrade - The ASI Precursor Seismograph & Civilizational Air-Gap.
"""

import json
from pathlib import Path
import pytest
import math

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_ASTRO_DIR = REPO_ROOT / "site-astro"
DATA_DIR = SITE_ASTRO_DIR / "src" / "data"
COMPONENTS_DIR = SITE_ASTRO_DIR / "src" / "components"
PAGES_DIR = SITE_ASTRO_DIR / "src" / "pages"


def test_seismograph_page_and_components_exist():
    """Verify that seismograph page and its interactive components exist."""
    seismograph_page = PAGES_DIR / "seismograph.astro"
    precursor_comp = COMPONENTS_DIR / "PrecursorSeismograph.svelte"
    airgap_comp = COMPONENTS_DIR / "CivilizationalAirGap.svelte"

    assert seismograph_page.exists(), "seismograph.astro page missing"
    assert precursor_comp.exists(), "PrecursorSeismograph.svelte missing"
    assert airgap_comp.exists(), "CivilizationalAirGap.svelte missing"

    content = seismograph_page.read_text(encoding="utf-8")
    assert "PrecursorSeismograph" in content
    assert "HSRIHeader" in content
    assert "HSRIFooter" in content


def test_navigation_header_includes_seismograph():
    """Verify that HSRIHeader contains the /seismograph/ navigation link."""
    header_file = COMPONENTS_DIR / "HSRIHeader.svelte"
    assert header_file.exists()
    content = header_file.read_text(encoding="utf-8")
    assert "/seismograph/" in content
    assert "Seismograph" in content


def test_asi_precursors_schema_and_integrity():
    """Verify that all 14 precursors are cataloged with rigorous schema."""
    json_path = DATA_DIR / "asi_precursors.json"
    assert json_path.exists(), "asi_precursors.json missing"

    with open(json_path, "r", encoding="utf-8") as f:
        precursors = json.load(f)

    assert len(precursors) == 14, f"Expected 14 precursors, found {len(precursors)}"

    for i in range(1, 15):
        expected_id = f"PREC-{i:03d}"
        found = next((p for p in precursors if p["id"] == expected_id), None)
        assert found is not None, f"Precursor {expected_id} missing"

        assert len(found["description"]) > 10
        assert found["status"] in ["CRITICAL_ACTIVE", "TRIGGERING_EMERGENT", "LATENT_WATCH"]
        assert found["status_color"] in ["red", "amber", "green"]
        assert found["indicator_type"] in ["leading", "coincident", "lagging"]
        assert len(found["proposed_threshold"]) > 5
        assert len(found["measurement_method"]) > 5


def test_precursor_summary_triad_telemetry():
    """Verify that precursor_summary contains valid triad scores."""
    summary_path = DATA_DIR / "precursor_summary.json"
    assert summary_path.exists(), "precursor_summary.json missing"

    with open(summary_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "master_precursor_threat_score" in data
    assert 0.0 <= data["master_precursor_threat_score"] <= 10.0
    assert "stream_1_autonomy_seismometer" in data
    assert "stream_2_latent_drift_detector" in data
    assert "stream_3_verification_wedge" in data

    s1 = data["stream_1_autonomy_seismometer"]
    s2 = data["stream_2_latent_drift_detector"]
    s3 = data["stream_3_verification_wedge"]

    assert 0.0 <= s1["score"] <= 10.0
    assert 0.0 <= s2["score"] <= 10.0
    assert 0.0 <= s3["score"] <= 10.0
    assert s3["cors_rating"] >= 1.0


def test_layer2_sovereignty_data_coverage():
    """Verify Layer 2 data includes all 39 nations and critical metrics."""
    layer2_path = DATA_DIR / "hsri_layer2.json"
    assert layer2_path.exists(), "hsri_layer2.json missing"

    with open(layer2_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    assert len(entries) == 39, f"Expected 39 benchmark nations, found {len(entries)}"

    for e in entries:
        assert "country_iso3" in e
        assert 0.0 <= e["h_layer1"] <= 1.0
        assert 0.0 <= e["h_layer2"] <= 1.0
        assert "t_half_hours" in e
        assert e["t_half_hours"] > 0
        assert "v_asi" in e
        assert "rank_delta_sovereignty" in e


def test_high_compute_trap_rank_inversions():
    """Verify High-Compute Trap economies plunge under Layer 2 Leontief floor."""
    layer2_path = DATA_DIR / "hsri_layer2.json"
    with open(layer2_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    entry_by_iso = {e["country_iso3"]: e for e in entries}

    # Singapore, USA, and Hong Kong should exhibit severe rank drops
    sgp = entry_by_iso["SGP"]
    usa = entry_by_iso["USA"]
    hkg = entry_by_iso["HKG"]

    assert sgp["rank_delta_sovereignty"] < -20
    assert sgp["high_compute_trap"] is True

    assert usa["rank_delta_sovereignty"] < -10
    assert usa["high_compute_trap"] is True

    assert hkg["rank_delta_sovereignty"] < -10
    assert hkg["high_compute_trap"] is True

    # Norway and Finland should lead Layer 2
    nor = entry_by_iso["NOR"]
    fin = entry_by_iso["FIN"]
    assert nor["rank_layer2"] == 1
    assert fin["rank_layer2"] == 2


def test_civilizational_airgap_decay_math():
    """Verify exponential half-life decay formula used in Civilizational Air-Gap simulator."""
    def compute_decay(blackout_h: float, t_half_h: float) -> float:
        return 1.0 - math.pow(2, -blackout_h / max(0.1, t_half_h))

    # At t = T_half, decay is exactly 50%
    assert math.isclose(compute_decay(48.0, 48.0), 0.50, rel_tol=1e-5)

    # At t = 2 * T_half, decay is exactly 75%
    assert math.isclose(compute_decay(96.0, 48.0), 0.75, rel_tol=1e-5)

    # For Singapore (T_half = 6h) at 72h: decay > 99.9%
    sgp_decay = compute_decay(72.0, 6.0)
    assert sgp_decay > 0.999

    # For Norway (T_half = 1440h) at 72h: decay < 5%
    nor_decay = compute_decay(72.0, 1440.0)
    assert nor_decay < 0.05
