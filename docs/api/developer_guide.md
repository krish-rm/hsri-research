# HSRI 2.0 Engine Core & REST API: Developer Guide

> **Version**: `v2.4.0-EngineCore`  
> **Archival DOI**: [`10.5281/zenodo.10842000`](https://doi.org/10.5281/zenodo.10842000)  
> **OpenAPI Schema**: [`docs/api/openapi.json`](./openapi.json)  
> **Live Portal**: [https://humanreadinessindex.org/](https://humanreadinessindex.org/)  

---

## 1. Overview & Architecture

The **HSRI 2.0 Engine Core (`hsri-engine`)** is a high-performance Python package and REST API designed for sovereign intelligence agencies, defense ministries, risk consultancies, and AI safety institutes. It provides instantaneous, mathematically rigorous evaluations of national and enterprise infrastructure resilience against self-improving artificial superintelligence.

### The Dual-Layer Non-Compensatory Engine
Traditional readiness indexes rely on linear arithmetic averaging, allowing high compute scores to mask fatal governance or verification failures. The HSRI Engine implements the **Leontief Minimum Floor ($eta = 0.50$)**:

$$H_{\text{Layer2}} = \sqrt{ \min_{j \in \{5,6,7,8\}} P_j \cdot \left( \frac{1}{4} \sum_{j=5}^{8} P_j \right) }$$

* **Layer 1 (Adoption Baseline):** P1 (AI Literacy), P2 (Critical Discernment), P3 (Institutional Governance), P4 (Digital Infrastructure).
* **Layer 2 (ASI Sovereignty):** P5 (Epistemic Inviolability / VSR), P6 (Civilizational Decoupling Half-Life $T_{\text{half}}$), P7 (Multipolar Coordination Velocity $V_{\text{coord}}$), P8 (Post-Labor Institutional Elasticity).
* **Master ASI Vulnerability Index:** $V_{\text{ASI}} = H_{\text{Layer1}} - H_{\text{Layer2}}$.

---

## 2. Quickstart & Installation

### Option A: Local Python Execution
```bash
# Clone the repository
git clone https://github.com/krish-rm/hsri-research.git
cd hsri-research

# Install dependencies using uv or pip
uv sync
```

### Option B: Command Line Interface (CLI)
```bash
# Run an evaluation for a custom node
uv run python -m hsri_engine.cli evaluate \
    --id DEFENSE-NODE-01 \
    --name "Sovereign Defense Enclave" \
    --p1 0.85 --p2 0.70 --p3 0.90 --p4 0.95 \
    --p5 0.80 --p6 0.75 --p7 0.60 --p8 0.55

# Launch the FastAPI REST Server
uv run python -m hsri_engine.cli serve --host 0.0.0.0 --port 8000
```

### Option C: Docker Containerization
```bash
# Build the Docker image
docker build -t hsri/engine-core:v2.4.0 .

# Run container with port forwarding
docker run -d -p 8000:8000 --name hsri-engine-api hsri/engine-core:v2.4.0

# Verify health status
curl http://localhost:8000/health
```

---

## 3. REST API Endpoint Reference

The engine exposes a production-ready OpenAPI 3.1 specification at `/openapi.json` and interactive Swagger UI at `/docs`.

### 1. `POST /v1/evaluate`
Evaluates an infrastructure profile and computes dual-layer readiness, vulnerability indices, and bottleneck pillars.

**Request Payload:**
```json
{
  "entity_id": "CYBER-SECTOR-US",
  "entity_name": "Critical Financial Clearing Network",
  "pillars": {
    "p1": 0.90,
    "p2": 0.65,
    "p3": 0.80,
    "p4": 0.98,
    "p5": 0.35,
    "p6": 0.15,
    "p7": 0.45,
    "p8": 0.40
  },
  "apply_negative_cross_elasticity": true
}
```

**Response Payload:**
```json
{
  "entity_id": "CYBER-SECTOR-US",
  "entity_name": "Critical Financial Clearing Network",
  "layer1_score": 0.8325,
  "layer2_score": 0.2253,
  "geometric_score": 0.8142,
  "choquet_score": 0.8198,
  "master_vulnerability_index": 0.6072,
  "is_high_compute_trap": true,
  "weakest_link_pillar": "P6",
  "weakest_link_score": 0.15,
  "pillars": {
    "P1_AI_Literacy": 0.9,
    "P2_Critical_Discernment": 0.65,
    "P3_Institutional_Governance": 0.8,
    "P4_Digital_Infrastructure": 0.98,
    "P5_Epistemic_Inviolability": 0.35,
    "P6_Decoupling_Half_Life": 0.15,
    "P7_Coordination_Velocity": 0.45,
    "P8_Post_Labor_Elasticity": 0.4
  },
  "sovereignty_diagnostics": {},
  "timestamp": "2026-10-13T17:15:00.000000+00:00"
}
```

---

### 2. `POST /v1/audit/monte-carlo`
Executes an OECD/JRC Step 7 Dirichlet Monte Carlo sensitivity analysis ($B=500$ iterations) randomizing Layer 2 weights.

**Request Payload:**
```json
{
  "evaluation_request": {
    "entity_id": "FIN-NODE",
    "pillars": {
      "p1": 0.8, "p2": 0.8, "p3": 0.8, "p4": 0.8,
      "p5": 0.6, "p6": 0.4, "p7": 0.5, "p8": 0.5
    }
  },
  "iterations": 500,
  "alpha_dirichlet": 1.0
}
```

**Response Payload:**
```json
{
  "entity_id": "FIN-NODE",
  "iterations": 500,
  "mean_layer2_score": 0.4472,
  "std_layer2_score": 0.0124,
  "ci_95_lower": 0.4215,
  "ci_95_upper": 0.4691,
  "kendall_w_concordance": 0.9986,
  "vulnerability_stability": "STABLE"
}
```

---

### 3. `GET /v1/benchmark/summary`
Returns the 39-nation official baseline, identifying the top sovereign nations (Norway, Finland, Iceland) and High-Compute Vulnerability Traps (Singapore, USA, Hong Kong).

---

### 4. `GET /v1/telemetry/precursors`
Fetches real-time telemetry from the live Singularity Seismograph:
* Master Precursor Threat Score (**8.44 / 10.0 &mdash; `CRITICAL_SUPERVISORY_COLLAPSE`**)
* Cognitive Oversight Richter Scale (**10.0 / 10.0 &mdash; Recursive Event Horizon**)
* Live Verification Latency Wedge ($\Delta T_{\text{wedge}} = 4,798.5\text{s}$, Ratio $3,200\text{x}$)
* Status across all 14 empirical tripwires.

---

## 4. Python SDK Usage

You can also use `hsri-engine` as an embedded Python library without running HTTP services:

```python
from hsri_engine import evaluate_profile, EvaluationRequest, PillarInput, RawTelemetryInput

# Direct evaluation via raw operational telemetry
req = EvaluationRequest(
    entity_id="SOVEREIGN-UTILITY",
    telemetry=RawTelemetryInput(
        human_verifications=850,
        total_critical_verifications=1000,
        adversarial_persuasion_resilience=0.92,
        t_energy=720.0,    # 30-day offline energy fallback
        t_finance=360.0,   # 15-day financial clearing fallback
        t_logistics=480.0,
        t_info=720.0,
        tau_modify=180.0,
        tau_verify_treaty=240.0,
        gini_compute=0.35,
        safety_net_coverage=0.90,
        labor_tax_reliance=0.40,
        tau_verify=3600.0,
        tau_gen=1.2
    )
)

result = evaluate_profile(req)
print(f"Layer 2 Sovereignty Score: {result.layer2_score:.4f}")
print(f"Governing Bottleneck Pillar: {result.weakest_link_pillar}")
print(f"Decoupling Half-Life: {result.sovereignty_diagnostics['t_half_hours']} hours")
```
