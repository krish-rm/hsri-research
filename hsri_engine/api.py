"""
hsri_engine.api - FastAPI REST Server for HSRI 2.0 Engine Core
"""

from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from hsri_engine.models import (
    EvaluationRequest,
    EvaluationResponse,
    MonteCarloRequest,
    MonteCarloResponse,
    BenchmarkSummaryResponse,
    PrecursorTelemetryResponse,
)
from hsri_engine import core

app = FastAPI(
    title="HSRI 2.0 Engine Core API",
    version="2.4.0",
    description=(
        "Production REST API for sovereign AI preparedness, Dual-Layer non-compensatory "
        "Leontief floor aggregation (beta=0.50), JRC Step 7 sensitivity auditing, and "
        "real-time ASI precursor telemetry."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "HSRI Research Consortium",
        "url": "https://humanreadinessindex.org",
        "email": "contact@hsri-research.org",
    },
    license_info={
        "name": "CC BY-SA 4.0",
        "url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
)

# Enable CORS for external research portals & dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Metadata"])
def root_info():
    """Returns engine version, archival DOI, and navigation links."""
    return {
        "engine": "HSRI 2.0 Engine Core",
        "version": "2.4.0",
        "architecture": "Dual-Layer Sovereignty Engine (Leontief Floor beta=0.50)",
        "doi": "10.5281/zenodo.10842000",
        "portal_url": "https://humanreadinessindex.org/",
        "documentation_url": "https://humanreadinessindex.org/methodology/",
        "docs_swagger": "/docs",
        "docs_redoc": "/redoc",
        "openapi_json": "/openapi.json",
        "status": "operational",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for container orchestrators and load balancers."""
    return {
        "status": "healthy",
        "engine": "hsri-engine-core",
        "version": "2.4.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post(
    "/v1/evaluate",
    response_model=EvaluationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Evaluation"],
    summary="Evaluate Infrastructure Sovereignty Profile",
    description=(
        "Calculates Layer 1 Adoption, Layer 2 ASI Sovereignty (Leontief Floor beta=0.50), "
        "the Master ASI Vulnerability Index (V_ASI), and identifies governing bottleneck pillars."
    ),
)
def evaluate_profile(request: EvaluationRequest):
    try:
        return core.evaluate_profile(request)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Evaluation failed: {str(exc)}",
        )


@app.post(
    "/v1/audit/monte-carlo",
    response_model=MonteCarloResponse,
    status_code=status.HTTP_200_OK,
    tags=["Audit"],
    summary="JRC Step 7 Dirichlet Monte Carlo Sensitivity Audit",
    description="Runs a Dirichlet Monte Carlo weight perturbation audit on Layer 2 pillars to assess rank and score stability.",
)
def monte_carlo_audit(request: MonteCarloRequest):
    try:
        return core.run_monte_carlo_sensitivity(request)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Monte Carlo simulation failed: {str(exc)}",
        )


@app.get(
    "/v1/benchmark/summary",
    response_model=BenchmarkSummaryResponse,
    tags=["Benchmark"],
    summary="Get 39-Nation Official Benchmark Summary",
    description="Returns top sovereign leaders, High-Compute Vulnerability Traps, and global benchmark metadata.",
)
def benchmark_summary():
    try:
        return core.get_benchmark_summary()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load benchmark summary: {str(exc)}",
        )


@app.get(
    "/v1/telemetry/precursors",
    response_model=PrecursorTelemetryResponse,
    tags=["Telemetry"],
    summary="Get Real-Time Precursor Seismograph Telemetry",
    description="Returns live Cognitive Oversight Richter Scale (CORS 10.0), latency wedge divergence, and 14 tripwires status.",
)
def precursor_telemetry():
    try:
        return core.get_precursor_telemetry()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch precursor telemetry: {str(exc)}",
        )
