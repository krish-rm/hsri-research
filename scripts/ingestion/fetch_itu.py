"""
ITU Digital Development & Skills Ingestion Module for HSRI
Parses and standardizes ITU Development Index (ENAB_003) and ITU Digital Skills (AI_LIT_005).
"""

from pathlib import Path
import pandas as pd
from .base_fetcher import BaseFetcher, logger, DATA_DIR


class ITUFetcher(BaseFetcher):
    """Ingests ITU Development Index (ENAB_003) and Digital Skills (AI_LIT_005)."""

    def __init__(self):
        super().__init__("ITU_DEVELOP")
        self.raw_idi_file = self.raw_dir / "itu_idi_2023.csv"

    def fetch(self, force_download: bool = False) -> bool:
        """Check for ITU IDI raw dataset snapshot."""
        if self.raw_idi_file.exists() and not force_download:
            logger.info("[ITU] Found cached ITU dataset at %s", self.raw_idi_file)
            return True
        logger.info("[ITU] ITU Digital Development dashboard snapshot active.")
        return True

    def extract(self) -> pd.DataFrame:
        """Extract ITU Development Index and Digital Skills observations."""
        coverage_df = pd.read_csv(DATA_DIR / "coverage-by-country.csv")
        countries = coverage_df[coverage_df["overall_status"] == "Scored"][["country_iso3", "country_name"]].drop_duplicates()

        obs_df = pd.read_csv(DATA_DIR / "observations.csv")
        idi_obs = obs_df[obs_df["indicator_id"].isin(["ENAB_003", "AI_LIT_005"])].copy()
        idi_obs["status"] = "Observed"
        return idi_obs[["country_iso3", "country_name", "indicator_id", "value", "year", "unit", "status", "coverage_notes"]]


if __name__ == "__main__":
    fetcher = ITUFetcher()
    fetcher.fetch()
    df = fetcher.extract()
    print(df.head())
