import os
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTREACH_DIR = REPO_ROOT / "reports" / "outreach"

EXPECTED_FILES = [
    "long_form_article_the_verification_illusion.md",
    "policy_brief_uk_aisi.md",
    "policy_brief_us_nist_aisi.md",
    "policy_brief_eu_ai_office.md",
    "policy_brief_oecd_un_advisory.md",
    "press_release_hsri_2_0.md",
    "viral_x_thread_breakdown.md",
    "media_pitch_matrix.md",
]


def test_outreach_files_exist():
    """Verify that all 8 Sprint 32 outreach and policy documents exist."""
    assert OUTREACH_DIR.exists(), f"Outreach directory missing at {OUTREACH_DIR}"
    for fname in EXPECTED_FILES:
        target = OUTREACH_DIR / fname
        assert target.exists(), f"Expected outreach document missing: {fname}"
        assert target.stat().st_size > 500, f"Document {fname} is too small"


def test_long_form_article_content():
    """Verify scientific and empirical depth of the long-form manifesto article."""
    article_path = OUTREACH_DIR / "long_form_article_the_verification_illusion.md"
    content = article_path.read_text(encoding="utf-8")
    
    assert "The Verification Illusion" in content
    assert "10.5281/zenodo.23441742" in content
    assert "Leontief Minimum Floor" in content or "Leontief" in content
    assert "Cognitive Oversight Richter Scale" in content or "CORS" in content
    assert "humanreadinessindex.org" in content
    assert "Singapore" in content
    assert "Norway" in content
    assert "United States" in content
    assert len(content) > 5000, "Long-form article is insufficiently detailed"


def test_multilateral_policy_briefs():
    """Verify that all 4 policy briefs contain appropriate institutional targeting and empirical metrics."""
    targets = {
        "policy_brief_uk_aisi.md": ("UK AI Safety Institute", "Verification Latency Wedge"),
        "policy_brief_us_nist_aisi.md": ("US AISI", "Decoupling Half-Life"),
        "policy_brief_eu_ai_office.md": ("Article 14", "European AI Office"),
        "policy_brief_oecd_un_advisory.md": ("OECD", "Leontief"),
    }
    for fname, (inst_term, metric_term) in targets.items():
        content = (OUTREACH_DIR / fname).read_text(encoding="utf-8")
        assert inst_term in content, f"{fname} missing reference to {inst_term}"
        assert metric_term in content, f"{fname} missing reference to {metric_term}"
        assert "10.5281/zenodo.23441742" in content, f"{fname} missing Zenodo DOI"


def test_press_release_and_viral_thread():
    """Verify press release formatting and viral social thread breakdown."""
    pr_content = (OUTREACH_DIR / "press_release_hsri_2_0.md").read_text(encoding="utf-8")
    assert "FOR IMMEDIATE RELEASE" in pr_content
    assert "contact@hsri-research.org" in pr_content
    assert "High-Compute Vulnerability Trap" in pr_content
    assert "10.5281/zenodo.23441742" in pr_content

    thread_content = (OUTREACH_DIR / "viral_x_thread_breakdown.md").read_text(encoding="utf-8")
    assert "Tweet 1/10" in thread_content
    assert "Tweet 10/10" in thread_content
    assert "@" in thread_content, "Viral thread must include target thought leaders"


def test_media_pitch_matrix():
    """Verify media pitch mapping covers major international technology publications."""
    matrix_content = (OUTREACH_DIR / "media_pitch_matrix.md").read_text(encoding="utf-8")
    assert "Financial Times" in matrix_content
    assert "Wired" in matrix_content
    assert "Politico" in matrix_content
    assert "MIT Technology Review" in matrix_content
    assert "Subject" in matrix_content
