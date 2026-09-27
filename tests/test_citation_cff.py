"""
Unit test for CITATION.cff schema validity and metadata completeness.
"""

from pathlib import Path
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CITATION_PATH = REPO_ROOT / "CITATION.cff"


def test_citation_cff_valid_schema():
    """
    Confirm CITATION.cff exists, parses as valid YAML, and contains all required metadata:
    cff-version, title, version, url, license, and at least one author entry.
    """
    assert CITATION_PATH.exists(), "CITATION.cff does not exist at repository root"

    with open(CITATION_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict), "CITATION.cff did not parse into a dictionary"

    # Required keys
    required_keys = ["cff-version", "title", "version", "url", "license", "authors"]
    for key in required_keys:
        assert key in data, f"Missing required key in CITATION.cff: {key}"

    # Verify content
    assert data["cff-version"] == "1.2.0"
    assert "Human Superintelligence Readiness Index" in data["title"]
    assert "0.2" in data["version"]
    assert data["url"] == "https://krish-rm.github.io/hsri-research/"
    assert data["license"] == "CC-BY-SA-4.0"
    assert isinstance(data["authors"], list) and len(data["authors"]) >= 1
    assert "name" in data["authors"][0] or "family-names" in data["authors"][0]
