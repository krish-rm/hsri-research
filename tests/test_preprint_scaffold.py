"""
Unit tests for HSRI Preprint Scaffold (research/preprint/draft-v0.1.md).
Validates required sections, substantive limitations, disclaimer integrity,
and verification markers on all bibliographic citations.
"""

from pathlib import Path
import re
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PREPRINT_PATH = REPO_ROOT / "research" / "preprint" / "draft-v0.1.md"


def test_preprint_file_exists():
    """Preprint draft scaffold must exist and be non-empty."""
    assert PREPRINT_PATH.exists(), "Preprint draft-v0.1.md missing"
    content = PREPRINT_PATH.read_text(encoding="utf-8")
    assert len(content.strip()) > 500


def test_preprint_required_sections():
    """Preprint must contain all mandatory structural sections."""
    content = PREPRINT_PATH.read_text(encoding="utf-8")

    required_section_keywords = [
        "Abstract",
        "Introduction",
        "Methods",
        "Multi-Model",
        "Behavioral",
        "Limitations",
        "Roadmap",
        "References",
    ]
    for sec in required_section_keywords:
        assert sec.lower() in content.lower(), f"Missing section keyword: {sec}"


def test_preprint_abstract_and_framing():
    """Abstract must describe HSRI as exploratory, non-psychometrically-validated proxy benchmark."""
    content = PREPRINT_PATH.read_text(encoding="utf-8")
    abstract_match = re.search(r"## Abstract\s+(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert abstract_match is not None, "Abstract section missing"
    abstract_text = abstract_match.group(1).strip()

    assert "exploratory" in abstract_text.lower()
    assert "non-psychometrically-validated" in abstract_text.lower() or "not psychometrically validated" in abstract_text.lower()
    assert "proxy benchmark" in abstract_text.lower()

    # Final sentences of abstract must explicitly state limitations
    last_150_chars = abstract_text[-250:].lower()
    assert "limitation" in last_150_chars or "not validated" in last_150_chars or "exploratory" in last_150_chars or "synthetic" in last_150_chars


def test_preprint_limitations_substantive():
    """Limitations section must be substantive and address core epistemic bounds."""
    content = PREPRINT_PATH.read_text(encoding="utf-8")
    lim_match = re.search(r"## (?:5\.\s*)?Limitations\s+(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert lim_match is not None, "Limitations section missing"
    lim_text = lim_match.group(1).strip()

    # Must be substantive (> 200 characters)
    assert len(lim_text) > 200

    # Must cover mandatory limitations
    assert "proxy" in lim_text.lower()
    assert "psychometric" in lim_text.lower()
    assert "single-model" in lim_text.lower()
    assert "synthetic" in lim_text.lower()
    assert "phase 4" in lim_text.lower()
    assert "topic-004" in lim_text.lower()


def test_preprint_references_marked_verify():
    """Every reference entry in the references section must be marked with [VERIFY]. No unmarked entries allowed."""
    content = PREPRINT_PATH.read_text(encoding="utf-8")
    ref_match = re.search(r"## (?:7\.\s*)?References\s+(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert ref_match is not None, "References section missing"
    ref_text = ref_match.group(1).strip()

    # Extract all numbered list items: e.g. "1. Author..." or "1) Author..."
    entries = re.findall(r"^\s*\d+[\.\)]\s*(.+)$", ref_text, re.MULTILINE)
    assert len(entries) > 0, "No numbered reference entries found in References section"

    for idx, entry in enumerate(entries, 1):
        assert "[VERIFY]" in entry, f"Reference #{idx} is not marked with [VERIFY]: '{entry}'"
