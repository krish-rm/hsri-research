import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent
import sys
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hsri_engine.api import app
from hsri_engine import core

client = TestClient(app)

def test_regulatory_crosswalk_document_integrity():
    doc_path = REPO_ROOT / "docs" / "regulatory_crosswalk.md"
    assert doc_path.exists(), f"Missing {doc_path}"
    
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    assert "Krishnakumar Radhakrishnan" in text
    assert "EU Artificial Intelligence Act" in text
    assert "Article 14" in text
    assert "NIST AI Risk Management Framework" in text
    assert "ISO/IEC 42001" in text
    assert "EU NIS 2 Directive" in text
    assert "Solvency II" in text
    assert "10.5281/zenodo.23441742" in text

def test_anticipated_objections_rebuttal_integrity():
    reb_path = REPO_ROOT / "research" / "preprint" / "anticipated_objections_rebuttal.md"
    assert reb_path.exists(), f"Missing {reb_path}"
    
    with open(reb_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    assert "Krishnakumar Radhakrishnan" in text
    assert "Leontief Floor" in text
    assert "Cognitive Oversight Richter Scale" in text
    assert "EXP-07-SYN" in text
    assert "86 Unrated Nations Register" in text
    assert "Singapore" in text
    assert "10.5281/zenodo.23441742" in text

def test_telemetry_provenance_and_schema():
    telem = core.get_precursor_telemetry()
    assert hasattr(telem, "is_fallback")
    assert isinstance(telem.is_fallback, bool)
    assert hasattr(telem, "provenance")
    assert telem.provenance in ["live_sentinel_telemetry", "deterministic_calibration_fallback"]
    assert hasattr(telem, "data_timestamp")

def test_hardened_cors_institutional_origins():
    # Preflight check for allowed institutional origin
    headers = {
        "Origin": "https://humanreadinessindex.org",
        "Access-Control-Request-Method": "GET"
    }
    resp = client.options("/v1/telemetry/precursors", headers=headers)
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == "https://humanreadinessindex.org"
    
    # Preflight check for unauthorized origin
    bad_headers = {
        "Origin": "https://unauthorized-crawler.net",
        "Access-Control-Request-Method": "GET"
    }
    bad_resp = client.options("/v1/telemetry/precursors", headers=bad_headers)
    assert bad_resp.headers.get("access-control-allow-origin") != "https://unauthorized-crawler.net"
