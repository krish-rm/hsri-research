"""
Unit tests for HSRI Unrated Nations & Scope Audit (Task 4.3).
Validates schema, completeness, and non-overlapping denominator integrity
(39 benchmark rated + 86 unrated = 125 evaluated, 70 no data of 195 sovereign states).
"""

import csv
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
UNRATED_CSV = REPO_ROOT / "data" / "unrated-nations.csv"
FINAL_SCORES_CSV = REPO_ROOT / "data" / "final_country_scores.csv"

EXPECTED_SCHEMA = [
    "country_iso3",
    "country_name",
    "region",
    "un_subregion",
    "available_pillars",
    "missing_pillars",
    "primary_data_gap",
    "partial_coverage_notes",
]


def test_unrated_nations_csv_exists_and_schema_valid():
    """Verify that data/unrated-nations.csv exists and conforms to the canonical schema."""
    assert UNRATED_CSV.exists(), "data/unrated-nations.csv does not exist"

    with open(UNRATED_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == EXPECTED_SCHEMA, f"Schema mismatch: {reader.fieldnames}"
        rows = list(reader)

    assert len(rows) == 86, f"Expected exactly 86 unrated nations, found {len(rows)}"

    for row in rows:
        assert len(row["country_iso3"]) == 3, f"Invalid ISO3 in row: {row}"
        assert row["country_name"], f"Missing country_name in row: {row}"
        assert row["region"] in ["Africa", "Americas", "Asia", "Europe", "Oceania"], f"Invalid region in row: {row}"
        assert row["un_subregion"], f"Missing un_subregion in row: {row}"
        assert int(row["available_pillars"]) in range(0, 5), f"Invalid available_pillars in row: {row}"
        assert row["primary_data_gap"], f"Missing primary_data_gap in row: {row}"


def test_scope_denominators_and_disjointness():
    """
    Verify that 86 unrated + 39 rated = 125 total evaluated nations,
    with 195 - 125 = 70 nations having no data at all, and no overlap.
    """
    assert FINAL_SCORES_CSV.exists(), "data/final_country_scores.csv does not exist"

    with open(FINAL_SCORES_CSV, "r", encoding="utf-8") as f:
        rated_rows = list(csv.DictReader(f))

    with open(UNRATED_CSV, "r", encoding="utf-8") as f:
        unrated_rows = list(csv.DictReader(f))

    rated_count = len(rated_rows)
    unrated_count = len(unrated_rows)
    total_evaluated = rated_count + unrated_count
    global_universe = 195
    no_data_universe = global_universe - total_evaluated

    assert rated_count == 39, f"Expected 39 benchmark rated nations, got {rated_count}"
    assert unrated_count == 86, f"Expected 86 unrated nations, got {unrated_count}"
    assert total_evaluated == 125, f"Expected 125 evaluated nations, got {total_evaluated}"
    assert no_data_universe == 70, f"Expected 70 unmonitored nations, got {no_data_universe}"

    # Verify disjointness between rated and unrated ISO3 sets
    # (Checking case-insensitively)
    rated_iso3 = {r.get("country_iso3", r.get("iso3", r.get("country_code", ""))).upper() for r in rated_rows}
    unrated_iso3 = {r["country_iso3"].upper() for r in unrated_rows}

    overlap = rated_iso3.intersection(unrated_iso3)
    assert not overlap, f"Found overlapping ISO3 codes between rated and unrated: {overlap}"
