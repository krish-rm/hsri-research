"""Tests for ASI Transition Scenarios schema integrity and enrichments."""
import json
import pathlib
import pytest

SRC_PATH = pathlib.Path(__file__).parent.parent / "site-astro" / "src" / "data" / "asi_scenarios.json"
PUB_PATH = pathlib.Path(__file__).parent.parent / "site-astro" / "public" / "data" / "asi_scenarios.json"

VALID_CATEGORIES = {
    "Instrumental Catastrophe",
    "Strategic Deception",
    "Epistemic Collapse",
    "Economic Displacement",
    "Systemic Disempowerment",
    "Governance & Coordination"
}

VALID_ACCENTS = {"crimson", "amber", "indigo", "jade"}


def test_scenario_files_exist_and_match():
    assert SRC_PATH.exists(), f"Missing {SRC_PATH}"
    assert PUB_PATH.exists(), f"Missing {PUB_PATH}"
    src_data = json.loads(SRC_PATH.read_text(encoding="utf-8"))
    pub_data = json.loads(PUB_PATH.read_text(encoding="utf-8"))
    assert src_data == pub_data, "Source and Public asi_scenarios.json must remain identical."


def test_all_26_scenarios_have_required_enrichments():
    src_data = json.loads(SRC_PATH.read_text(encoding="utf-8"))
    scenarios = src_data.get("scenarios", [])
    assert len(scenarios) == 26, f"Expected 26 scenarios, got {len(scenarios)}"

    for sc in scenarios:
        sc_id = sc.get("id")
        assert sc_id and sc_id.startswith("SC-"), f"Invalid scenario ID {sc_id}"
        
        # Original academic fields preserved
        assert "name" in sc and sc["name"]
        assert "mechanism" in sc and sc["mechanism"]
        assert "failureMode" in sc and sc["failureMode"]
        assert "severity" in sc and sc["severity"]

        # Additive Speculative Field Guide fields
        assert "shortTitle" in sc, f"{sc_id} missing shortTitle"
        assert len(sc["shortTitle"]) <= 32, f"{sc_id} shortTitle too long: {sc['shortTitle']}"

        assert "categoryTag" in sc, f"{sc_id} missing categoryTag"
        assert sc["categoryTag"] in VALID_CATEGORIES, f"{sc_id} invalid categoryTag: {sc['categoryTag']}"

        assert "teaser" in sc, f"{sc_id} missing teaser"
        assert 10 <= len(sc["teaser"]) <= 190, f"{sc_id} teaser length out of bounds ({len(sc['teaser'])}): {sc['teaser']}"

        assert "previewImage" in sc, f"{sc_id} missing previewImage"
        assert sc["previewImage"].endswith(".webp"), f"{sc_id} previewImage must be .webp: {sc['previewImage']}"

        assert "accentColor" in sc, f"{sc_id} missing accentColor"
        assert sc["accentColor"] in VALID_ACCENTS, f"{sc_id} invalid accentColor: {sc['accentColor']}"

        assert "visualPrompt" in sc and len(sc["visualPrompt"]) > 20, f"{sc_id} missing visualPrompt"
