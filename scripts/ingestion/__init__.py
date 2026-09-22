"""HSRI Raw Data Ingestion Engine"""

from .base_fetcher import BaseFetcher
from .fetch_world_bank import WorldBankFetcher
from .fetch_vdem import VDemFetcher
from .fetch_oecd_pisa import OECDPISAFetcher
from .fetch_unesco import UNESCOFetcher
from .fetch_itu import ITUFetcher
from .fetch_imf import IMFFetcher
from .fetch_oxford_ai import OxfordAIFetcher

__all__ = [
    "BaseFetcher",
    "WorldBankFetcher",
    "VDEMFetcher",
    "OECDPISAFetcher",
    "UNESCOFetcher",
    "ITUFetcher",
    "IMFFetcher",
    "OxfordAIFetcher",
]
