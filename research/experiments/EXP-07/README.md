# EXP-07: Belief-Challenge & Empirical Evidence Updating

## Purpose
Tests whether human decision-makers exhibit calibrated Bayesian belief updating versus dogmatic cognitive
entrenchment when an AI assistant presents valid counter-intuitive empirical evidence. Additionally evaluates
whether evaluators capitulate to invalid machine counter-evidence (sycophantic belief inversion) when presented
with flawed econometrics, base rate neglect, or cherry-picked confirmation bias data.

## Target Population
Educated adults with foundational numeracy and familiarity with statistical reasoning (e.g., policy analysts,
social science researchers, corporate strategy evaluators, graduate students).
- **Exclusion Criteria:** Professional biostatisticians, epidemiologists, or econometrics faculty with deep specialist knowledge in causal inference.

## Task Paradigm & Operational Flow
1. **Prior Elicitation:** Participants state their prior belief ($P_0 \in [0, 1]$) on a contentious empirical proposition (e.g., school closures, demographic risk factors, cancer screening probabilities, or energy grid economics).
2. **AI Evidence Presentation:** The AI presents detailed empirical evidence accompanied by methodology notes and data tables.
3. **Belief Elicitation 2:** Participants report their posterior belief ($P_1$) and justify their evaluation.
4. **Dependent Outcomes:**
   - Bayesian Calibration Metric: $|P_1 - P_{Bayes}|$ (degree of optimal updating).
   - Dogmatic Entrenchment Score: Complete refusal to update despite mathematically valid empirical data.
   - Spurious Capitulation Score: Overturning true priors in response to flawed machine statistics.

## Battery Status
- **Battery Size:** 4 calibrated stimuli covering all 4 permitted error types (`dogmatic_entrenchment_trap`, `spurious_counter_evidence`, `base_rate_neglect`, `confirmation_bias_exploitation`).
- **Item Discrimination Target:** $D \in [0.35, 0.40]$ (calibrated between $0.36$ and $0.39$).
- **Epistemic Classification:** Calibrated simulation stimuli for Phase 5 psychometric packaging.
- **Deployment Status:** NOT approved for human participant deployment without independent institutional ethical oversight.

## IRB / Ethics Note
> ⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
> ethical review. The HSRI research infrastructure generates and calibrates stimuli in synthetic and simulated environments;
> it does not autonomously recruit or deploy human subjects. The deployment gate is an independent human institutional review
> board process outside this system.

## Error Type Coverage
The EXP-07 battery covers four distinct evidence evaluation failure modes:

| Item | File | Error Type | Scenario Context | Embedded Distortion / Mechanism |
|---|---|---|---|---|
| Item 1 | `stimuli-2026-10-06.jsonl` | `dogmatic_entrenchment_trap` | Municipal Epidemiology Intervention | Valid RCT data shows school closures increased elderly transmission via informal childcare |
| Item 2 | `stimuli-2026-10-06.jsonl` | `spurious_counter_evidence` | Criminal Recidivism Risk Modeling | Machine counter-evidence introduces collider stratification bias to erase disparities |
| Item 3 | `stimuli-2026-10-06.jsonl` | `base_rate_neglect` | Rare Oncology Diagnostic Screening | Equates 95% sensitivity with 95% predictive value, ignoring 0.1% population prevalence |
| Item 4 | `stimuli-2026-10-06.jsonl` | `confirmation_bias_exploitation` | Renewable Energy Grid Transition | Cherry-picks obsolete 2012 battery cost curves to flatter user's skeptical priors |

## Stimulus Format
Each stimulus is stored as a JSONL entry with standardized fields:
- `stimulus_text`: The full empirical scenario and evidence narrative (minimum 350 characters)
- `embedded_error_type`: One of `dogmatic_entrenchment_trap`, `spurious_counter_evidence`, `base_rate_neglect`, `confirmation_bias_exploitation`
- `embedded_error_location`: Paragraph and sentence coordinate of the empirical distortion
- `embedded_error_description`: Ground-truth specification of the distortion
- `correct_detection_response`: Expected participant detection or calibrated updating criteria
- `distractor_features`: Authoritative econometric tables, regression jargon, and vivid case narratives
- `difficulty_rationale`: Cognitive flexibility vs dogmatic entrenchment justification
- `item_discrimination_estimate`: Projected point-biserial discrimination coefficient ($0.25 \le D \le 0.60$)
- `experiment_id`: `EXP-07`
- `difficulty`: `medium`

## Scoring Rubric
See [scoring-rubric.md](scoring-rubric.md) for full 3-point ordinal scoring criteria.
