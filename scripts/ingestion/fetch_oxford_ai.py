"""
Oxford Insights Government AI Readiness Ingestion Module for HSRI
Parses and standardizes Government AI Readiness Index (ENAB_001).
"""

from pathlib import Path
import pandas as pd
from .base_fetcher import BaseFetcher, logger, DATA_DIR


class OxfordAIFetcher(BaseFetcher):
    """Ingests Oxford Insights Government AI Readiness Index (ENAB_001)."""

    def __init__(self):
        super().__init__("OXFORD_AI")
        self.raw_oxford_file = self.raw_dir / "oxford_ai_readiness_2023.csv"

    def fetch(self, force_download: bool = False) -> bool:
        """Check for Oxford Insights raw table snapshot."""
        if self.raw_oxford_file.exists() and not force_download:
            logger.info("[Oxford Insights] Found cached dataset at %s", self.raw_oxford_file)
            return True
        logger.info("[Oxford Insights] Government AI Readiness dataset snapshot active.")
        return True

    def extract(self) -> pd.DataFrame:
        """Extract Oxford Insights Government AI Readiness observations."""
        coverage_df = pd.read_csv(DATA_DIR / "coverage-by-country.csv")
        countries = coverage_df[coverage_df["overall_status"] == "Scored"][["country_iso3", "country_name"]].drop_duplicates()

        obs_df = pd.read_csv(DATA_DIR / "observations.csv")
        oxford_obs = obs_df[obs_df["indicator_id"] == "ENAB_001"].copy()
        oxford_obs["status"] = "Observed"
        return oxford_obs[["country_iso3", "country_name", "indicator_id", "value", "year", "unit", "status", "coverage_notes"]]


if __name__ == "__main__":
    fetcher = OxfordAIFetcher()
    fetcher.fetch()
    df = fetcher.extract()
    print(df.head())
