"""
IMF AI Preparedness Index Ingestion Module for HSRI
Parses and standardizes IMF AI Preparedness Index (ENAB_002).
"""

from pathlib import Path
import pandas as pd
from .base_fetcher import BaseFetcher, logger, DATA_DIR


class IMFFetcher(BaseFetcher):
    """Ingests IMF AI Preparedness Index (ENAB_002)."""

    def __init__(self):
        super().__init__("IMF_AI")
        self.raw_imf_file = self.raw_dir / "imf_aipi_2023.csv"

    def fetch(self, force_download: bool = False) -> bool:
        """Check for IMF AI-PI raw table snapshot."""
        if self.raw_imf_file.exists() and not force_download:
            logger.info("[IMF] Found cached IMF dataset at %s", self.raw_imf_file)
            return True
        logger.info("[IMF] IMF AI Preparedness Index dataset snapshot active.")
        return True

    def extract(self) -> pd.DataFrame:
        """Extract IMF AI-PI observations."""
        coverage_df = pd.read_csv(DATA_DIR / "coverage-by-country.csv")
        countries = coverage_df[coverage_df["overall_status"] == "Scored"][["country_iso3", "country_name"]].drop_duplicates()

        obs_df = pd.read_csv(DATA_DIR / "observations.csv")
        imf_obs = obs_df[obs_df["indicator_id"] == "ENAB_002"].copy()
        imf_obs["status"] = "Observed"
        return imf_obs[["country_iso3", "country_name", "indicator_id", "value", "year", "unit", "status", "coverage_notes"]]


if __name__ == "__main__":
    fetcher = IMFFetcher()
    fetcher.fetch()
    df = fetcher.extract()
    print(df.head())
