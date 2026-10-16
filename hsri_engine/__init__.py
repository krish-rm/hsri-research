"""
hsri_engine - HSRI 2.0 Engine Core Package
"""

__version__ = "2.4.0"
__author__ = "HSRI Research Consortium"

from hsri_engine.models import (
    PillarInput,
    RawTelemetryInput,
    EvaluationRequest,
    EvaluationResponse,
    MonteCarloRequest,
    MonteCarloResponse,
    BenchmarkSummaryResponse,
    PrecursorTelemetryResponse,
)
from hsri_engine.core import evaluate_profile, run_monte_carlo_sensitivity
from hsri_engine.api import app

__all__ = [
    "__version__",
    "app",
    "PillarInput",
    "RawTelemetryInput",
    "EvaluationRequest",
    "EvaluationResponse",
    "MonteCarloRequest",
    "MonteCarloResponse",
    "BenchmarkSummaryResponse",
    "PrecursorTelemetryResponse",
    "evaluate_profile",
    "run_monte_carlo_sensitivity",
]

from hsri_engine.reinsurance import (
    calculate_reinsurance_pricing,
    generate_syndicate_slip_markdown,
)

__all__.extend([
    "calculate_reinsurance_pricing",
    "generate_syndicate_slip_markdown",
])
