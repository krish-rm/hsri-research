"""
UNESCO UIS Tertiary STEM Ingestion Module for HSRI
Parses and standardizes Tertiary STEM Enrollment percentages (AI_LIT_004).
"""

from pathlib import Path
import pandas as pd
from .base_fetcher import BaseFetcher, logger, DATA_DIR


class UNESCOFetcher(BaseFetcher):
    """Ingests UNESCO UIS Tertiary STEM Enrollment (AI_LIT_004)."""

    def __init__(self):
        super().__init__("UNESCO_STEM")
        self.raw_stem_file = self.raw_dir / "unesco_tertiary_stem.csv"

    def fetch(self, force_download: bool = False) -> bool:
        """Check for UNESCO UIS raw dataset snapshot."""
        if self.raw_stem_file.exists() and not force_download:
            logger.info("[UNESCO] Found cached STEM dataset at %s", self.raw_stem_file)
            return True
        logger.info("[UNESCO] UNESCO UIS Tertiary database snapshot active.")
        return True

    def extract(self) -> pd.DataFrame:
        """Extract Tertiary STEM Enrollment observations."""
        coverage_df = pd.read_csv(DATA_DIR / "coverage-by-country.csv")
        countries = coverage_df[coverage_df["overall_status"] == "Scored"][["country_iso3", "country_name"]].drop_duplicates()

        obs_df = pd.read_csv(DATA_DIR / "observations.csv")
        stem_obs = obs_df[obs_df["indicator_id"] == "AI_LIT_004"].copy()
        stem_obs["status"] = "Observed"
        return stem_obs[["country_iso3", "country_name", "indicator_id", "value", "year", "unit", "status", "coverage_notes"]]


if __name__ == "__main__":
    fetcher = UNESCOFetcher()
    fetcher.fetch()
    df = fetcher.extract()
    print(df.head())
