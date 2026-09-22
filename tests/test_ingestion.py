"""
Automated Data Quality & Ingestion Unit Tests for HSRI
Validates empirical missingness preservation, normalized score bounds,
coverage thresholds, and web export synchronization.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
SITE_DATA_DIR = ROOT_DIR / "site-astro" / "src" / "data"


class TestHarmonizedObservations:
    """Validate empirical observations and missingness preservation."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.obs_file = DATA_DIR / "raw_observations_harmonized.csv"
        assert self.obs_file.exists(), "data/raw_observations_harmonized.csv must exist"
        self.df = pd.read_csv(self.obs_file)

    def test_record_count_and_columns(self):
        required_cols = [
            "country_iso3", "country_name", "indicator_id", "value",
            "year", "unit", "source_id", "status", "coverage_notes"
        ]
        for col in required_cols:
            assert col in self.df.columns, f"Missing column: {col}"
        assert len(self.df) == 780, "Expected 780 observation records (39 countries x 20 indicators)"

    def test_emli_geographic_missingness(self):
        """EMLI (META_COG_002) must be NaN for non-European economies."""
        non_euro = ["USA", "CAN", "JPN", "KOR", "AUS", "NZL", "SGP", "HKG", "ISR"]
        emli_records = self.df[self.df["indicator_id"] == "META_COG_002"]

        for iso in non_euro:
            match = emli_records[emli_records["country_iso3"] == iso]
            assert not match.empty, f"No EMLI record for {iso}"
            val = match.iloc[0]["value"]
            status = match.iloc[0]["status"]
            assert pd.isna(val), f"Expected NaN for EMLI in {iso}, got {val}"
            assert status == "Missing", f"Expected 'Missing' status for {iso}, got {status}"

    def test_emli_european_observed(self):
        """EMLI (META_COG_002) must be observed for European economies."""
        euro_sample = ["DEU", "FRA", "GBR", "NLD", "FIN", "SWE", "DNK"]
        emli_records = self.df[self.df["indicator_id"] == "META_COG_002"]

        for iso in euro_sample:
            match = emli_records[emli_records["country_iso3"] == iso]
            assert not match.empty
            val = match.iloc[0]["value"]
            status = match.iloc[0]["status"]
            assert pd.notna(val) and val > 0, f"Expected observed value for EMLI in {iso}"
            assert status == "Observed"

    def test_piaac_pstre_missingness(self):
        """PIAAC PSTRE (AI_LIT_001) must be NaN for countries without PSTRE modules."""
        piaac_missing = ["BGR", "CYP", "ISL", "MLT", "MKD", "ROU"]
        records = self.df[self.df["indicator_id"] == "AI_LIT_001"]

        for iso in piaac_missing:
            match = records[records["country_iso3"] == iso]
            assert not match.empty
            assert pd.isna(match.iloc[0]["value"])
            assert match.iloc[0]["status"] == "Missing"


class TestNormalizedMatrix:
    """Validate normalized indicators matrix."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.norm_file = DATA_DIR / "normalized_indicators.csv"
        assert self.norm_file.exists()
        self.df = pd.read_csv(self.norm_file, index_col="country_iso3")

    def test_dimension_and_bounds(self):
        assert len(self.df) == 39, "Expected 39 benchmark economies"
        assert self.df.shape[1] == 17, "Expected 17 retained indicator columns"

        for col in self.df.columns:
            observed = self.df[col].dropna()
            assert (observed >= 0.0).all(), f"Values in {col} must be >= 0.0"
            assert (observed <= 1.0).all(), f"Values in {col} must be <= 1.0"

    def test_nan_preservation_in_normalization(self):
        """NaN values from raw observations must remain NaN after normalization."""
        assert pd.isna(self.df.loc["USA", "META_COG_002"])
        assert pd.isna(self.df.loc["AUS", "META_COG_002"])
        assert pd.isna(self.df.loc["CYP", "AI_LIT_001"])
        assert pd.isna(self.df.loc["BGR", "AI_LIT_001"])


class TestIndexScoresAndCoverage:
    """Validate pillar scores, overall scores, and coverage rules."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.scores_file = DATA_DIR / "final_country_scores.csv"
        assert self.scores_file.exists()
        self.df = pd.read_csv(self.scores_file, index_col="country_iso3")

    def test_coverage_bounds_and_completeness(self):
        """All countries must have coverage >= 60% and global average >= 95%."""
        coverages = self.df["overall_coverage"].astype(float)
        assert (coverages >= 0.60).all(), "Every scored country must satisfy 60% minimum coverage"
        assert coverages.min() >= 0.80, f"Expected minimum coverage >= 80%, found {coverages.min()}"
        assert coverages.mean() >= 0.95, f"Expected global average coverage >= 95%, found {coverages.mean():.3f}"

    def test_pillar_coverage_consistency(self):
        """Check pillar-specific coverage fractions match missingness expectations."""
        # Non-European countries have 2/3 Critical Discernment indicators (0.6667)
        assert abs(float(self.df.loc["USA", "Critical_Discernment_coverage"]) - 0.6667) < 0.001
        assert abs(float(self.df.loc["AUS", "Critical_Discernment_coverage"]) - 0.6667) < 0.001

        # Core European countries have 3/3 (1.0)
        assert float(self.df.loc["DEU", "Critical_Discernment_coverage"]) == 1.0
        assert float(self.df.loc["FRA", "Critical_Discernment_coverage"]) == 1.0

    def test_score_ranges(self):
        scores = self.df["overall_score"].astype(float)
        assert (scores >= 0.0).all() and (scores <= 1.0).all()


class TestWebExportSynchronization:
    """Validate JSON artifacts consumed by Astro website."""

    def test_country_scores_json(self):
        json_path = SITE_DATA_DIR / "country_scores.json"
        assert json_path.exists()
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "countries" in data
        assert "metadata" in data
        assert len(data["countries"]) == 39
        assert data["metadata"]["benchmarkRatedCountries"] == 39
        assert data["metadata"]["globalNations"] == 195
        assert data["metadata"]["avgCoverage"] >= 95.0

        for country in data["countries"]:
            assert "indicatorsBreakdown" in country
            assert len(country["indicatorsBreakdown"]) == 30
            assert "coverage" in country
            assert country["coverage"] >= 80.0


class TestModularFetchers:
    """Validate that all modular fetchers instantiate and extract records."""

    def test_all_fetchers(self):
        from scripts.ingestion import (
            WorldBankFetcher, VDemFetcher, OECDPISAFetcher,
            UNESCOFetcher, ITUFetcher, IMFFetcher, OxfordAIFetcher
        )
        fetchers = [
            WorldBankFetcher(), VDemFetcher(), OECDPISAFetcher(),
            UNESCOFetcher(), ITUFetcher(), IMFFetcher(), OxfordAIFetcher()
        ]
        for f in fetchers:
            assert f.fetch() is True
            extracted = f.extract()
            assert not extracted.empty, f"Fetcher {f.source_id} returned empty DataFrame"
            assert f.validate_schema(extracted) is True, f"Fetcher {f.source_id} failed schema validation"
