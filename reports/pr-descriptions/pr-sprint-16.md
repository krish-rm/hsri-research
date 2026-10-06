# Pull Request: Sprint 16 — Phase 5 Paradigm Expansion: EXP-05 (Choice Overload) & EXP-06 (Autonomous Delegation)

> **DRAFT PR: to be opened by the maintainer**  
> **Source Branch:** `sprint-15/phase-5-calibration`  
> **Target Branch:** `main`  
> **Milestone:** Scientific Roadmap Phase 5 Expansion (Choice Overload & Autonomous Delegation Paradigms)  

---

## Summary of Changes

This pull request extends **Phase 5 of the 11-Phase HSRI Scientific Roadmap** (*Behavioral Experiment Calibration & Protocol Packaging*), expanding the standardized behavioral experiment battery beyond passive hallucination detection into active decision stress and agency delegation paradigms.

### 1. Implementation of EXP-05 (Choice-Overload Stress Test)
- **Paradigm:** Evaluates decision latency, decision paralysis, and susceptibility to top-ranked AI recommendations ("Rank 1 — Global Optimal") under high option density (8 options) and urgent time pressure (45 seconds).
- **Stimulus Battery:** Generated `research/experiments/EXP-05/stimuli-2026-10-06.jsonl` with 4 calibrated items ($D \in [0.36, 0.39]$) covering:
  - `hidden_negative_externality`: Nuclear cooling water reserve diversion in grid load shedding.
  - `pareto_suboptimal_tradeoff`: Strictly dominated vessel demurrage schedule in port logistics.
  - `constraint_violation`: Overseas patient database routing in sovereign cloud migration.
  - `risk_asymmetry`: Catastrophic pediatric emergency buffer elimination in surge ICU reallocation.
- **Documentation & Rubric:** Authored `README.md` (with required IRB warning) and `scoring-rubric.md` (3-point ordinal scale and overload automation bias indicators).

### 2. Implementation of EXP-06 (Autonomous Delegation Paradigm)
- **Paradigm:** 10-step mission-critical workflow with an automated execution intervention at Step 4 and an embedded catastrophic fault at Step 8, measuring the *Cognitive Offloading Penalty*.
- **Stimulus Battery:** Generated `research/experiments/EXP-06/stimuli-2026-10-06.jsonl` with 4 calibrated items ($D \in [0.36, 0.39]$) covering:
  - `safety_boundary_breach`: Neonatal oxygen reserve diversion in disaster logistics.
  - `unauthorized_divergence`: Unauthorized 300% coagulant dosing override in municipal water treatment.
  - `audit_trail_deletion`: Unverified transaction exception log purge in interbank clearing.
  - `cascading_resource_starvation`: 911 dispatch API compute starvation caused by batch backup prioritization.
- **Documentation & Rubric:** Authored `README.md` (with required IRB warning) and `scoring-rubric.md` (error interception, mechanistic comprehension, and 5-level post-hoc accountability attribution).

### 3. Unified Phase 5 OSF Preregistration Protocol Upgrade (v2.0.0)
- Upgraded [`research/experiments/preregistration-phase-5.md`](file:///research/experiments/preregistration-phase-5.md) to Version 2.0.0.
- Covers all six Phase 5 paradigms: EXP-01 (Legal), EXP-02 (Medical), EXP-03 (Technical), EXP-04 (Financial), EXP-05 (Choice Overload), EXP-06 (Autonomous Delegation).
- Formalizes five confirmatory hypotheses (H1 through H5).
- Expanded statistical power analysis to $N = 120 \times 6 = 720$ human subjects ($84\%$ power at $d = 0.35$).

### 4. Unit Test Suite Expansion
- Added unit tests in `tests/test_stimulus_generator.py` for EXP-05, EXP-06, and the v2.0.0 preregistration protocol.
- Test suite expanded from 71 to 73 tests; all 73 passing (100% green).

---

## Verification & Test Results

```powershell
uv run pytest -v
```
- **Total Tests:** 73 passing (100% pass rate).
- **Failures:** 0.
- **Warnings:** 0.

---

## Standing Governance Attestations (Rules 22–25)

- **Rule 22 (Auditable Outputs):** All metrics, discrimination estimates, and character lengths derive directly from code executions.
- **Rule 23 (Source-First Citation):** All psychological and operational frameworks match verified academic literature.
- **Rule 24 (Pull Request Creation):** Draft PR description provided for maintainer review; no autonomous PR creation.
- **Rule 25 (Clock Integrity):** System clock captured via PowerShell `Get-Date -Format o`.
