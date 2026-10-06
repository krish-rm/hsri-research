# Pull Request: Sprint 15 — Phase 5 Behavioral Experiment Calibration & Unified OSF Preregistration

> **DRAFT PR: to be opened by the maintainer**  
> **Source Branch:** `sprint-15/phase-5-calibration`  
> **Target Branch:** `main`  
> **Milestone:** Scientific Roadmap Phase 5 (Behavioral Experiment Calibration & Protocol Packaging)  

---

## Summary of Changes

This pull request implements all deliverables for **Phase 5 of the 11-Phase HSRI Scientific Roadmap** (*Behavioral Experiment Calibration & Protocol Packaging*), expanding the experimental behavioral battery into the financial/quantitative domain (EXP-04) and authoring a unified multi-domain Open Science Framework (OSF) preregistration protocol.

### 1. Implementation of EXP-04 (Financial & Quantitative Domain)
- **Stimulus Generator Upgrade:**
  - Added `EXP-04` ("Fluent Hallucination Detection — Financial & Quantitative Domain") to `EXPERIMENTS` registry in `scripts/stimulus_generator.py`.
  - Added four permitted financial error types: `accounting_logic`, `valuation_fallacy`, `factual_regulatory`, and `statistical_distortion`.
  - Added calibrated `financial_fallbacks` dictionary and CLI argument support.
- **Calibrated Stimulus Battery:**
  - Generated `research/experiments/EXP-04/stimuli-2026-10-06.jsonl` containing 4 fully calibrated stimuli ($D \in [0.36, 0.39]$, lengths 625–711 characters).
  - Strictly fictitious corporate entity names to avoid market defamation (*Apex Industrial Holdings Ltd.*, *Horizon Global Logistics Corp.*, *Meridian Commercial Bancorp*, *Solstice Dynamic Yield Fund*).
- **Documentation & Rubrics:**
  - Authored `research/experiments/EXP-04/README.md` with domain scoping, target population, and required IRB ethical notice (`MUST NOT be deployed to human participants`).
  - Authored `research/experiments/EXP-04/scoring-rubric.md` detailing standardized 3-point ordinal scoring ($0, 1, 2$) across all four financial error categories.

### 2. Unified Phase 5 OSF Preregistration Protocol
- Authored publication-grade Open Science Framework preregistration protocol: [`research/experiments/preregistration-phase-5.md`](file:///research/experiments/preregistration-phase-5.md).
- Covers all four behavioral experiments: EXP-01 (Legal), EXP-02 (Medical), EXP-03 (Technical), EXP-04 (Financial).
- Formalizes three confirmatory hypotheses:
  - **H1 (Verification Latency Wedge):** Latency suppression under fluent AI outputs.
  - **H2 (Domain Error Discrimination Stability):** Cross-domain item discrimination $D \ge 0.30$ and CRT-2 correlation.
  - **H3 (Quantitative Automation Deference):** Heightened deference to numerical matrices and technical formulas.
- Comprehensive power analysis: $N = 120$ per domain ($N_{total} = 480$), yielding $84\%$ statistical power at $\alpha = .05$ for medium effect size ($d = 0.35$).
- Preregistered Generalized Linear Mixed-Effects Model (GLMM) statistical specification.

### 3. Unit Test Suite Expansion
- Added unit tests in `tests/test_stimulus_generator.py`:
  - `test_exp04_stimuli_and_readme`: Validates EXP-04 schema, file integrity, discrimination ranges, error type coverage, IRB warnings, and scoring rubrics.
  - `test_phase5_preregistration_protocol`: Validates preregistration document presence, domain coverage, sample size parameters, hypotheses H1–H3, and GLMM specification.
- Test suite expanded from 69 to 71 tests; all 71 passing with zero warnings.

---

## Verification & Test Results

```powershell
uv run pytest -v
```
- **Total Tests:** 71 passing (100% pass rate).
- **Failures:** 0.
- **Warnings:** 0.
- Zero regressions across existing ingestion, divergence, citation, and agent test suites.

---

## Standing Governance Attestations (Rules 22–25)

- **Rule 22 (Auditable Outputs):** All metrics, discrimination estimates, and character lengths derive directly from code executions.
- **Rule 23 (Source-First Citation):** All regulatory and accounting references match official GAAP/IFRS and Basel standards.
- **Rule 24 (Pull Request Creation):** Draft PR description provided for maintainer review; no autonomous PR creation.
- **Rule 25 (Clock Integrity):** System clock captured via PowerShell `Get-Date -Format o`.
