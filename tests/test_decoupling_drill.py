"""
tests/test_decoupling_drill.py - Unit & Verification Tests for Sprint 34 Decoupling Drill
"""

import json
from pathlib import Path
import pytest
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import decoupling_simulator

DATA_FILE = REPO_ROOT / "data" / "telemetry" / "decoupling_drill_results.json"
ASTRO_DATA_FILE = REPO_ROOT / "site-astro" / "src" / "data" / "decoupling_drill_results.json"
PROTOCOL_FILE = REPO_ROOT / "research" / "tabletop" / "decoupling_drill_protocol.md"
WHITEPAPER_FILE = REPO_ROOT / "research" / "tabletop" / "when_the_cloud_goes_silent.md"
SVELTE_COMPONENT = REPO_ROOT / "site-astro" / "src" / "components" / "DecouplingDrillViewer.svelte"
ASTRO_PAGE = REPO_ROOT / "site-astro" / "src" / "pages" / "research" / "decoupling-drill.astro"


def test_decoupling_simulation_engine_math():
    """Verify mathematical properties of the decoupling trajectory engine."""
    # Health at t=0 must be 1.0
    h_zero = decoupling_simulator.calculate_subsystem_health(0.0, 12.0, 36.0)
    assert h_zero == 1.0

    # Health within buffer must remain 1.0
    h_buffer = decoupling_simulator.calculate_subsystem_health(10.0, 12.0, 36.0)
    assert h_buffer == 1.0

    # Health at t = buffer + half_life must be 0.50
    h_half = decoupling_simulator.calculate_subsystem_health(48.0, 12.0, 36.0)
    assert pytest.approx(h_half, rel=1e-3) == 0.50

    # Monotonic decay after buffer
    h_later = decoupling_simulator.calculate_subsystem_health(84.0, 12.0, 36.0)
    assert h_later < h_half


def test_decoupling_results_json_schema():
    """Verify structure and contents of exported simulation results."""
    assert DATA_FILE.exists(), f"Results file missing at {DATA_FILE}"
    assert ASTRO_DATA_FILE.exists(), f"Astro data file missing at {ASTRO_DATA_FILE}"

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "metadata" in data
    assert "archetypes" in data
    assert "crisis_injects" in data
    assert "comparative_metrics" in data

    # 3 Archetypes present
    assert len(data["archetypes"]) == 3
    assert "archetype_a" in data["archetypes"]
    assert "archetype_b" in data["archetypes"]
    assert "archetype_c" in data["archetypes"]

    # 8 Crisis Injects present
    assert len(data["crisis_injects"]) == 8

    # Compare metrics: Archetype C must heavily outperform Archetype A
    res_a = data["archetypes"]["archetype_a"]["metrics"]["day_14_residual_functionality"]
    res_b = data["archetypes"]["archetype_b"]["metrics"]["day_14_residual_functionality"]
    res_c = data["archetypes"]["archetype_c"]["metrics"]["day_14_residual_functionality"]

    assert res_c > res_b > res_a
    assert res_a <= 0.05
    assert res_c >= 0.50


def test_tabletop_protocol_document():
    """Verify existence and institutional depth of exercise protocol."""
    assert PROTOCOL_FILE.exists(), f"Protocol file missing at {PROTOCOL_FILE}"
    content = PROTOCOL_FILE.read_text(encoding="utf-8")

    assert "Operation Silent Cloud" in content
    assert "Krishnakumar Radhakrishnan" in content
    assert "10.5281/zenodo.10842000" in content
    assert "Leontief" in content
    assert "INJ-01" in content
    assert "INJ-08" in content
    assert len(content) > 3000


def test_whitepaper_document():
    """Verify publication-grade depth of decoupling whitepaper."""
    assert WHITEPAPER_FILE.exists(), f"Whitepaper file missing at {WHITEPAPER_FILE}"
    content = WHITEPAPER_FILE.read_text(encoding="utf-8")

    assert "When the Cloud Goes Silent" in content
    assert "Krishnakumar Radhakrishnan" in content
    assert "10.5281/zenodo.10842000" in content
    assert "Archetype A" in content
    assert "Archetype B" in content
    assert "Archetype C" in content
    assert len(content) > 5000


def test_web_portal_components_exist():
    """Verify interactive Svelte component and Astro route exist."""
    assert SVELTE_COMPONENT.exists(), f"Svelte viewer missing at {SVELTE_COMPONENT}"
    assert ASTRO_PAGE.exists(), f"Astro page missing at {ASTRO_PAGE}"

    svelte_text = SVELTE_COMPONENT.read_text(encoding="utf-8")
    assert "Operation Silent Cloud" in svelte_text
    assert "archetype_a" in svelte_text
    assert "time-slider" in svelte_text


PILOT_BRIEF_FILE = REPO_ROOT / "research" / "tabletop" / "institutional_pilot_brief.md"
PILOT_BRIEF_PDF = REPO_ROOT / "research" / "tabletop" / "institutional_pilot_brief.pdf"


def test_institutional_pilot_brief():
    """Verify depth, partner targeting, and MOU structure in institutional pilot brief."""
    assert PILOT_BRIEF_FILE.exists(), f"Pilot brief missing at {PILOT_BRIEF_FILE}"
    assert PILOT_BRIEF_PDF.exists(), f"Pilot brief PDF missing at {PILOT_BRIEF_PDF}"

    text = PILOT_BRIEF_FILE.read_text(encoding="utf-8")
    assert "RSIS Singapore" in text
    assert "ETH Zurich" in text
    assert "MBZUAI" in text
    assert "Krishnakumar Radhakrishnan" in text
    assert "10.5281/zenodo.10842000" in text
    assert "Chatham House Rule" in text
    assert "HSRI Case Study 01" in text
    assert "MEMORANDUM OF UNDERSTANDING" in text
    assert len(text) > 8000


def test_decoupling_facilitator_console_component():
    """Verify Sprint 38 Tabletop Facilitator Console interactive features and export capability."""
    console_path = REPO_ROOT / "site-astro" / "src" / "components" / "DecouplingDrillConsole.svelte"
    assert console_path.exists(), f"DecouplingDrillConsole missing at {console_path}"
    
    text = console_path.read_text(encoding="utf-8")
    
    # Check host presets
    assert "rsis_singapore" in text
    assert "eth_zurich" in text
    assert "mbzuai" in text
    assert "federal_us" in text
    
    # Check 45-min timer
    assert "timerMinutes = 45" in text
    assert "toggleTimer" in text
    assert "resetTimer" in text
    assert "addMinutes" in text
    
    # Check 4 rounds and 8 crisis injects
    assert "r1_islanding" in text
    assert "r2_analog_dispatch" in text
    assert "r3_diesel_priority" in text
    assert "r4_airgap_equilibrium" in text
    assert "INJ-01" in text
    assert "INJ-08" in text
    
    # Check weakest-link calculation
    assert "liveHealth" in text
    assert "leontiefScore" in text
    assert "weakestPillar" in text
    
    # Check Markdown AAR export
    assert "exportReport" in text
    assert "Krishnakumar Radhakrishnan" in text
    assert "10.5281/zenodo.10842000" in text
    assert "Chatham House Rule" in text
    assert "HSRI_After_Action_Report" in text
    
    # Check parent viewer integration
    viewer_path = REPO_ROOT / "site-astro" / "src" / "components" / "DecouplingDrillViewer.svelte"
    viewer_text = viewer_path.read_text(encoding="utf-8")
    assert "DecouplingDrillConsole" in viewer_text
    assert "viewMode" in viewer_text
    assert "mode-switcher" in viewer_text
