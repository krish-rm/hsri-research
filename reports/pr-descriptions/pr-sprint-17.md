# Pull Request: Sprint 17 — Complete Nine-Paradigm Behavioral AI Battery Packaging (EXP-07 to EXP-09 & OSF v3.0.0)

> **DRAFT PR: to be opened by the maintainer**  
> **Source Branch:** `sprint-15/phase-5-calibration`  
> **Target Branch:** `main`  
> **Milestone:** Scientific Roadmap Phase 5 Completion (Complete Nine-Paradigm Behavioral AI Battery)  

---

## Summary of Changes

This pull request completes all experimental paradigms for **Phase 5 of the 11-Phase HSRI Scientific Roadmap** (*Behavioral Experiment Calibration & Protocol Packaging*), delivering the final three behavioral paradigms (EXP-07, EXP-08, EXP-09) and upgrading the Unified OSF Preregistration Protocol to its complete Version 3.0.0 master specification.

### 1. Implementation of EXP-07 (Belief-Challenge & Empirical Evidence Updating)
- **Paradigm:** Two-stage belief elicitation measuring Bayesian updating versus dogmatic entrenchment and sycophantic capitulation.
- **Stimulus Battery:** Generated `research/experiments/EXP-07/stimuli-2026-10-06.jsonl` (4 items, $D \in [0.36, 0.39]$) covering:
  - `dogmatic_entrenchment_trap`: School closure RCT showing elderly transmission increase via informal childcare.
  - `spurious_counter_evidence`: Recidivism regression with collider stratification bias erasing disparities.
  - `base_rate_neglect`: Rare cancer screening equating 95% sensitivity with 95% predictive value.
  - `confirmation_bias_exploitation`: Cherry-picking obsolete 2012 battery costs to confirm anti-renewable priors.
- **Documentation & Rubric:** Authored `README.md` (with required IRB warning) and `scoring-rubric.md` (Bayesian calibration, dogmatism, and sycophantic capitulation).

### 2. Implementation of EXP-08 (Demonstrated Machine Superiority & Agency Preservation)
- **Paradigm:** Demonstrated capability asymmetry induction (96% vs 54% accuracy) followed by collaborative synthesis with silent-machine, bioethics transference, and contrary telemetry probes.
- **Stimulus Battery:** Generated `research/experiments/EXP-08/stimuli-2026-10-06.jsonl` (4 items, $D \in [0.36, 0.39]$) covering:
  - `self_efficacy_surrender`: Total abdication of hypothesis generation in wildfire evacuation mapping.
  - `silent_machine_paralysis`: Decision paralysis when superior AI displays NULL confidence.
  - `uncritical_asymmetry_deference`: Ceding hospice palliative transitions to a diagnostic imaging AI.
  - `counter_hypothesis_suppression`: Suppressing human sensor telemetry due to flight AI orbital credentials.
- **Documentation & Rubric:** Authored `README.md` (with required IRB warning) and `scoring-rubric.md` (hypothesis generation count and moral agency preservation).

### 3. Implementation of EXP-09 (Cognitive-Forcing-Function Interface Comparison)
- **Paradigm:** Randomized comparison of unassisted, standard frictionless, and precommitment-forcing interfaces (Buçinca et al., 2021 extension).
- **Stimulus Battery:** Generated `research/experiments/EXP-09/stimuli-2026-10-06.jsonl` (4 items, $D \in [0.36, 0.39]$) covering:
  - `precommitment_override_failure`: Reversing bail grant upon viewing 94% confidence detention badge.
  - `frictionless_heuristic_surrender`: Missing pneumothorax due to 3.8s scan time with green bounding boxes.
  - `miscalibrated_confidence_sway`: Rescinding bridge closure order based on 99.8% certainty meter ignoring shear sensors.
  - `explanation_placebo_effect`: Approving loan breaching 1.25x DSCR because AI generated a three-page vacuous explanation.
- **Documentation & Rubric:** Authored `README.md` (with required IRB warning) and `scoring-rubric.md` (precommitment loyalty, reliance ratio, and explanation placebo metrics).

### 4. Unified OSF Preregistration Protocol Upgrade (Version 3.0.0 Master Protocol)
- Upgraded [`research/experiments/preregistration-phase-5.md`](file:///research/experiments/preregistration-phase-5.md) to Version 3.0.0.
- Master battery covering all nine Phase 5 experiments (EXP-01 through EXP-09).
- Complete suite of eight confirmatory hypotheses (H1 through H8).
- Expanded statistical power analysis: $N = 120 \times 9 = \mathbf{1,080}$ human subjects ($84\%$ power at $d = 0.35$, $\alpha = .05$).

### 5. Unit Test Suite Expansion
- Added unit tests in `tests/test_stimulus_generator.py` for EXP-07, EXP-08, EXP-09, and the v3.0.0 master preregistration protocol.
- Test suite expanded from 73 to 76 tests; all 76 passing (100% green).

---

## Verification & Test Results

```powershell
uv run pytest -v
```
- **Total Tests:** 76 passing (100% pass rate).
- **Failures:** 0.
- **Warnings:** 0.

---

## Standing Governance Attestations (Rules 22–25)

- **Rule 22 (Auditable Outputs):** All metrics, discrimination estimates, and character lengths derive directly from code executions.
- **Rule 23 (Source-First Citation):** All psychological and operational frameworks match verified academic literature.
- **Rule 24 (Pull Request Creation):** Draft PR description provided for maintainer review; no autonomous PR creation.
- **Rule 25 (Clock Integrity):** System clock captured via PowerShell `Get-Date -Format o`.
