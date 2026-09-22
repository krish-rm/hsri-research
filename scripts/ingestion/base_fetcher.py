"""
Base Fetcher Module for HSRI Raw Data Ingestion Engine
Standardizes fetching, caching, extracting, and normalizing primary data.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ingestion")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"


class BaseFetcher(ABC):
    """Abstract base class for all institutional data fetchers."""

    def __init__(self, source_id: str):
        self.source_id = source_id
        self.raw_dir = RAW_DIR / source_id
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def fetch(self, force_download: bool = False) -> bool:
        """
        Download or retrieve the raw source dataset into self.raw_dir.
        Returns True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """
        Parse raw source files into standardized observation records.
        Must return a DataFrame with columns:
        ['country_iso3', 'country_name', 'indicator_id', 'value', 'year', 'unit', 'status', 'coverage_notes']
        Missing values must explicitly be float('nan') or None.
        """
        pass

    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Ensure the extracted DataFrame complies with HSRI schema requirements."""
        required = [
            "country_iso3",
            "country_name",
            "indicator_id",
            "value",
            "year",
            "unit",
            "status",
            "coverage_notes",
        ]
        missing = [col for col in required if col not in df.columns]
        if missing:
            logger.error(f"[{self.source_id}] Missing required columns: {missing}")
            return False
        return True
