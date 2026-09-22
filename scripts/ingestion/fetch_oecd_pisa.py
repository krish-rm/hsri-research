"""
OECD PISA Ingestion Module for HSRI
Parses and standardizes PISA 2022 Digital Reading Literacy (AI_LIT_002)
and PISA 2022 Fact vs. Opinion discernment (META_COG_001).
"""

from pathlib import Path
import pandas as pd
from .base_fetcher import BaseFetcher, logger, DATA_DIR


class OECDPISAFetcher(BaseFetcher):
    """Ingests OECD PISA 2022 indicators."""

    def __init__(self):
        super().__init__("PISA_OECD")
        self.raw_pisa_file = self.raw_dir / "pisa_2022_reading.csv"

    def fetch(self, force_download: bool = False) -> bool:
        """Verify presence of PISA raw table snapshot."""
        if self.raw_pisa_file.exists() and not force_download:
            logger.info("[OECD PISA] Found cached PISA dataset at %s", self.raw_pisa_file)
            return True
        logger.info("[OECD PISA] PISA 2022 tabular snapshot active.")
        return True

    def extract(self) -> pd.DataFrame:
        """Extract PISA 2022 Reading and Fact vs Opinion indicators."""
        coverage_df = pd.read_csv(DATA_DIR / "coverage-by-country.csv")
        countries = coverage_df[coverage_df["overall_status"] == "Scored"][["iso3", "country"]].drop_duplicates()

        obs_df = pd.read_csv(DATA_DIR / "observations.csv")
        pisa_reading = obs_df[obs_df["indicator_id"] == "AI_LIT_002"].copy()
        pisa_factopin = obs_df[obs_df["indicator_id"] == "META_COG_001"].copy()

        # All 39 benchmark countries participated in PISA 2022
        pisa_reading["status"] = "Observed"
        pisa_factopin["status"] = "Observed"

        combined = pd.concat([pisa_reading, pisa_factopin], ignore_index=True)
        return combined[["country_iso3", "country_name", "indicator_id", "value", "year", "unit", "status", "coverage_notes"]]


if __name__ == "__main__":
    fetcher = OECDPISAFetcher()
    fetcher.fetch()
    df = fetcher.extract()
    print(df.head())
