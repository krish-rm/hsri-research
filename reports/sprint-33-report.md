# HSRI Sprint 33 Report: The HSRI Engine API Productization

> **Generated**: `2026-10-13T22:50:00+05:30`  
> **Milestone**: `v2.4.0-EngineProductization` (Sprint 33 Closure — Standalone Microservice & Software Asset)  
> **Branch**: `main`  
> **Status**: Verified & Passing (`201/201` tests passing green, `50/50` Astro pages cleanly built in 5.75s)  
> **Live Benchmark**: `https://humanreadinessindex.org/`  
> **Interactive Seismograph**: `https://humanreadinessindex.org/seismograph/`  
> **Permanent DOI**: `10.5281/zenodo.10842000`  
> **Developer Guide**: [`docs/api/developer_guide.md`](../docs/api/developer_guide.md)  
> **OpenAPI Schema**: [`docs/api/openapi.json`](../docs/api/openapi.json)  

---

## 1. Executive Summary & Productization Objective

**Sprint 33** achieves a pivotal commercial and technical milestone under **Phase 4: Sovereign Tabletop & Engine API Commercialization**: transforming the open-science HSRI research repository into an enterprise-grade, high-margin software asset (`hsri-engine`).

Without hiring a sales team or raising dilutive capital, `hsri-engine` productizes the Dual-Layer Sovereignty Engine, Leontief floor bottleneck auditing, and real-time precursor telemetry into:
1. A clean, pip-installable Python SDK.
2. A production-ready REST API built with `FastAPI` and `uvicorn`.
3. Complete OpenAPI 3.1 Swagger and ReDoc interactive documentation.
4. Production Docker containerization (`Dockerfile` and `docker-compose.yml`).

This microservice enables external institutional clients &mdash; including national security councils, defense intelligence enclaves, sovereign wealth funds (GIC, Temasek, PIF), and reinsurance underwriters (Lloyd's, Munich Re, Swiss Re) &mdash; to ingest proprietary operational telemetry and receive instantaneous, mathematically proven Leontief bottleneck diagnoses and civilizational decoupling ratings.

---

## 2. Key Architecture & Engineered Modules

### A. The Standalone `hsri_engine` Package
The engine has been architected under `hsri_engine/`:
* **[`hsri_engine/models.py`](../hsri_engine/models.py)**: Pydantic schemas validating all inputs/outputs (`PillarInput`, `RawTelemetryInput`, `EvaluationRequest`, `EvaluationResponse`, `MonteCarloRequest`, `MonteCarloResponse`, `BenchmarkSummaryResponse`, `PrecursorTelemetryResponse`).
* **[`hsri_engine/core.py`](../hsri_engine/core.py)**: Pure computation engine executing:
  * Linear Layer 1 baseline adoption.
  * Leontief Minimum Floor ($eta = 0.50$) Layer 2 sovereignty aggregation ($H_{\text{Layer2}} = \sqrt{\min_j P_j \cdot \bar{P}}$).
  * Non-compensatory Geometric Mean and Choquet 2-additive capacity integrals.
  * Master ASI Vulnerability Index ($V_{\text{ASI}} = H_{\text{Layer1}} - H_{\text{Layer2}}$).
  * High-Compute Vulnerability Trap detection ($V_{\text{ASI}} \ge 0.25$ and $P_4 \ge 0.70$).
  * Dynamic derivation of P5 (VSR), P6 ($T_{\text{half}}$ in hours), P7 ($V_{\text{coord}}$), P8 (PLIE), and the Verification Latency Wedge ($\Delta T_{\text{wedge}}$).
  * OECD/JRC Step 7 Dirichlet Monte Carlo sensitivity analysis ($B=100..2,000$ iterations) verifying rank and score stability.
* **[`hsri_engine/api.py`](../hsri_engine/api.py)**: High-performance FastAPI server with CORS, OpenAPI metadata, error handlers, and typed routes.
* **[`hsri_engine/cli.py`](../hsri_engine/cli.py)**: Terminal CLI supporting `hsri-engine serve`, `hsri-engine evaluate`, and `hsri-engine export-openapi`.
* **[`hsri_engine/__init__.py`](../hsri_engine/__init__.py)**: High-level Python exports for SDK usage.

### B. REST Endpoints Operationalized
| Method | Path | Summary | Description |
|---|---|---|---|
| `GET` | `/` | Metadata & Status | Returns engine version, DOI, status, and navigation URLs |
| `GET` | `/health` | Health Check | High-frequency container healthcheck |
| `POST` | `/v1/evaluate` | Dual-Layer Evaluation | Computes Layer 1, Layer 2 Leontief, $V_{\text{ASI}}$, Trap status, and bottleneck |
| `POST` | `/v1/audit/monte-carlo` | JRC Sensitivity Audit | Runs Dirichlet Monte Carlo simulation returning confidence intervals & stability |
| `GET` | `/v1/benchmark/summary` | Official 39 Benchmark | Returns top sovereign leaders, global rank shifts, and trap flags |
| `GET` | `/v1/telemetry/precursors` | Live Seismograph | Returns CORS 10.0 score, latency wedge metrics, and 14 tripwires |

### C. Containerization & Documentation
* **`Dockerfile`**: Minimal Debian slim container (`python:3.10-slim`) installing dependencies, curl healthchecks, and launching Uvicorn on port 8000.
* **`docker-compose.yml`**: Production compose specification for one-command container deployment (`docker compose up -d`).
* **`docs/api/developer_guide.md`**: Complete developer whitepaper with CLI examples, Python SDK snippets, curl payloads, and schema definitions.
* **`docs/api/openapi.json`**: Static OpenAPI 3.1 schema export for client SDK generators.

---

## 3. Verification & Validation Metrics

| Subsystem | Metric | Target | Result | Status |
|---|---|---|---|---|
| **Full Pytest Suite** | `uv run pytest` | $\ge 200$ passing | **201 / 201 Passing (8.78s)** | **PASS (100%)** |
| **Engine API Tests** | `tests/test_engine_api.py` | 11 unit tests | **11 / 11 Passing (1.50s)** | **PASS** |
| **Astro Production Build** | `npm run build` | 50 HTML pages | **50 / 50 Static Pages Built (5.75s)** | **PASS** |
| **CLI Verification** | `hsri-engine evaluate` | Successful output | **Verified clean console output** | **PASS** |
| **OpenAPI Export** | `hsri-engine export-openapi` | Valid schema JSON | **Exported cleanly to `docs/api/`** | **PASS** |
| **Security Leak Audit** | Local git diff scan | 0 secrets/cross-repo IP | **0 Leaks Found** | **PASS** |

---

## 4. Next Phase Transition: Sprint 34

With the engine productized into a scalable API and microservice, HSRI 2.0 proceeds to **Sprint 34: The First Civilizational Decoupling Drill (Small-State Tabletop)**:

* **Task 1**: Author the master tabletop exercise protocol (`research/tabletop/decoupling_drill_protocol.md`) simulating a 14-day global recursive model containment quarantine across 4 critical subsystems: Power Grid, Financial Clearing, Food Supply, and Telecom.
* **Task 2**: Model decoupling survival curves for three archetypes:
  * *Archetype A (The Hyper-Automated Hostage)*: Singapore / Hong Kong ($T_{\text{half}} < 48\text{h}$)
  * *Archetype B (The Fragmented Superpower)*: United States ($T_{\text{half}} \approx 7\text{ days}$)
  * *Archetype C (The Resilient Decentralizer)*: Switzerland / Nordic ($T_{\text{half}} > 30\text{ days}$)
* **Task 3**: Publish whitepaper: *"When the Cloud Goes Silent: Simulating Civilizational Decoupling Half-Life Under Sudden AI Cutoff"*.
