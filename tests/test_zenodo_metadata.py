"""
Unit tests for Zenodo metadata deposit schemas (research/zenodo-metadata.json).
Validates JSON well-formedness, mandatory Zenodo schema keys, license specifications,
Rule 12 compliant description text, and integrity of maintainer placeholders.
"""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
ZENODO_PATH = REPO_ROOT / "research" / "zenodo-metadata.json"


def test_zenodo_json_well_formed():
    """Zenodo metadata file must exist and parse as valid JSON."""
    assert ZENODO_PATH.exists(), "research/zenodo-metadata.json missing"
    content = ZENODO_PATH.read_text(encoding="utf-8")
    data = json.loads(content)
    assert isinstance(data, dict)
    assert "records" in data
    assert "repository_snapshot" in data["records"]
    assert "divergence_log_dataset" in data["records"]


def test_zenodo_required_keys():
    """Both deposit records must contain all required Zenodo deposit metadata keys."""
    data = json.loads(ZENODO_PATH.read_text(encoding="utf-8"))
    required_keys = ["title", "upload_type", "description", "creators", "access_right", "license"]

    for record_name in ["repository_snapshot", "divergence_log_dataset"]:
        record = data["records"][record_name]
        assert "metadata" in record, f"{record_name} missing 'metadata' block"
        meta = record["metadata"]
        for key in required_keys:
            assert key in meta, f"{record_name} metadata missing required key: {key}"
            assert meta[key], f"{record_name} metadata field '{key}' is empty"


def test_zenodo_licenses():
    """Licenses must strictly be CC-BY-SA-4.0 for repo and CC-BY-4.0 for divergence log."""
    data = json.loads(ZENODO_PATH.read_text(encoding="utf-8"))
    repo_meta = data["records"]["repository_snapshot"]["metadata"]
    div_meta = data["records"]["divergence_log_dataset"]["metadata"]

    assert repo_meta["license"] == "cc-by-sa-4.0"
    assert div_meta["license"] == "cc-by-4.0"


def test_zenodo_creator_placeholders():
    """Creators and affiliations must strictly remain maintainer placeholders without fabrication."""
    data = json.loads(ZENODO_PATH.read_text(encoding="utf-8"))
    for record_name in ["repository_snapshot", "divergence_log_dataset"]:
        meta = data["records"][record_name]["metadata"]
        creators = meta["creators"]
        assert isinstance(creators, list) and len(creators) > 0
        for creator in creators:
            assert creator["name"] == "TODO: maintainer to supply"
            assert creator["affiliation"] == "TODO: maintainer to supply"
            if "orcid" in creator:
                assert creator["orcid"] == "TODO: maintainer to supply"


def test_zenodo_rule_12_and_disclaimer():
    """Deposit descriptions must follow Rule 12 and explicitly state exploratory, non-validated status."""
    data = json.loads(ZENODO_PATH.read_text(encoding="utf-8"))
    repo_desc = data["records"]["repository_snapshot"]["metadata"]["description"].lower()
    div_desc = data["records"]["divergence_log_dataset"]["metadata"]["description"].lower()

    assert "exploratory" in repo_desc
    assert "not validated" in repo_desc
    assert "stimuli" in repo_desc and "cleared for irb submission" in repo_desc

    assert "single-model" in div_desc or "gemini" in div_desc
    assert "governance" in div_desc
