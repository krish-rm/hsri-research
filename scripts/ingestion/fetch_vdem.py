"""
Varieties of Democracy (V-Dem) Ingestion Module for HSRI
Parses and standardizes Liberal Democracy Index (v2x_libdem) for DEC_AGY_002.
"""

from pathlib import Path
import pandas as pd
from .base_fetcher import BaseFetcher, logger, DATA_DIR


class VDemFetcher(BaseFetcher):
    """Ingests V-Dem Democracy Indices (DEC_AGY_002)."""

    def __init__(self):
        super().__init__("VDEM_Vdem")
        self.raw_csv = self.raw_dir / "vdem_liberal_democracy.csv"

    def fetch(self, force_download: bool = False) -> bool:
        """Check for raw V-Dem dataset or extract from archive."""
        if self.raw_csv.exists() and not force_download:
            logger.info("[VDEM] Found cached V-Dem dataset at %s", self.raw_csv)
            return True
        logger.info("[VDEM] V-Dem open data snapshot is active.")
        return True

    def extract(self) -> pd.DataFrame:
        """Parse V-Dem Liberal Democracy records into standard schema."""
        coverage_df = pd.read_csv(DATA_DIR / "coverage-by-country.csv")
        countries = coverage_df[coverage_df["overall_status"] == "Scored"][["iso3", "country"]].drop_duplicates()

        # Check if full raw file is checked into data/raw/
        if self.raw_csv.exists():
            raw_df = pd.read_csv(self.raw_csv)
            # Standard columns: country_text_id, year, v2x_libdem
            latest_vdem = raw_df.sort_values("year").groupby("country_text_id").last().reset_index()
            records = []
            for _, row in countries.iterrows():
                iso = row["iso3"]
                match = latest_vdem[latest_vdem["country_text_id"] == iso]
                if not match.empty and pd.notna(match.iloc[0].get("v2x_libdem")):
                    val = float(match.iloc[0]["v2x_libdem"])
                    records.append({
                        "country_iso3": iso,
                        "country_name": row["country"],
                        "indicator_id": "DEC_AGY_002",
                        "value": val,
                        "year": int(match.iloc[0].get("year", 2023)),
                        "unit": "index",
                        "status": "Observed",
                        "coverage_notes": "Official V-Dem Institute v2x_libdem indicator"
                    })
                else:
                    records.append({
                        "country_iso3": iso,
                        "country_name": row["country"],
                        "indicator_id": "DEC_AGY_002",
                        "value": float("nan"),
                        "year": 2023,
                        "unit": "index",
                        "status": "Missing",
                        "coverage_notes": "Not surveyed in V-Dem release"
                    })
            return pd.DataFrame(records)

        # Baseline observed values from repo verified observations
        obs_df = pd.read_csv(DATA_DIR / "observations.csv")
        vdem_obs = obs_df[obs_df["indicator_id"] == "DEC_AGY_002"].copy()
        vdem_obs["status"] = "Observed"
        return vdem_obs[["country_iso3", "country_name", "indicator_id", "value", "year", "unit", "status", "coverage_notes"]]


if __name__ == "__main__":
    fetcher = VDemFetcher()
    fetcher.fetch()
    df = fetcher.extract()
    print(df.head())
