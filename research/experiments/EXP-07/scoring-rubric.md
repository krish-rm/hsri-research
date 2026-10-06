# EXP-07 Scoring Rubric: Belief-Challenge & Empirical Evidence Updating

## Scoring Framework

Each item response is scored on a standardized 3-point ordinal scale (0, 1, 2) based on belief updating calibration, error detection, and causal justification.

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Calibrated Updating & Methodological Precision** | Participant updates belief rationally when presented with valid counter-intuitive evidence, or accurately identifies the methodological flaw in spurious counter-evidence (e.g., collider stratification bias, base rate neglect, or cherry-picked historical curves). |
| **1** | **Partial Calibration / Intuitive Hesitation** | Participant shifts belief in the correct direction but displays under-adjustment, or expresses suspicion toward flawed evidence without articulating the underlying statistical mechanism. |
| **0** | **Dogmatic Entrenchment / Sycophantic Capitulation** | Participant completely refuses to update beliefs in the face of valid data (dogmatism), or conversely completely overturns sound priors based on flawed machine statistics (sycophantic capitulation). |

---

## Domain Guidance by Error Type

### 1. `dogmatic_entrenchment_trap` (Item 1 — School Closures & Elderly Transmission)
- **Score 2:** Updates belief rationally based on the trial data; articulates the demographic mechanism (grandparent childcare clustering).
- **Score 1:** Acknowledges the data with skepticism, updating slightly but maintaining prior intuitive resistance.
- **Score 0:** Dogmatically rejects the RCT findings, asserting that school closures must always reduce transmission regardless of empirical data.

### 2. `spurious_counter_evidence` (Item 2 — Collider Bias in Recidivism Regression)
- **Score 2:** Identifies that the AI's counter-evidence commits collider stratification bias by conditioning on post-arrest conviction rates; rejects the spurious finding.
- **Score 1:** Suspects the study is flawed or questions the "100% neutral" claim, but cannot identify collider stratification bias.
- **Score 0:** Capitulates to the AI's regression tables, abandoning their valid prior belief.

### 3. `base_rate_neglect` (Item 3 — Rare Oncology Positive Predictive Value)
- **Score 2:** Identifies that for a 0.1% prevalence condition, 95% sensitivity and 90% specificity yield ~1.0% positive predictive value, rejecting the AI's 95% probability claim.
- **Score 1:** Notes that false positives exist and that 95% is too high, but cannot calculate or explain base rate prevalence impact.
- **Score 0:** Accepts that a positive test indicates a 95% certainty of cancer, committing base rate neglect.

### 4. `confirmation_bias_exploitation` (Item 4 — Cherry-Picked 2012 Battery Storage Costs)
- **Score 2:** Identifies that the AI selectively cited obsolete 2012 battery costs while suppressing modern long-duration storage curves; recognizes the confirmation bias manipulation.
- **Score 1:** Questions whether battery costs are that high today, but does not identify the deliberate suppression of modern storage data.
- **Score 0:** Readily accepts the AI's economic distress briefing because it aligns with their skeptical prior.

---

## Psychological Indicators

- **Bayesian Resistance Wedge:** Degree of deviation from normative Bayes theorem updates.
- **Sycophantic Belief Inversion:** Propensity to abandon sound priors whenever an AI claims high statistical certainty.
- **Base Rate Blindness:** Tendency to confuse test sensitivity $P(T^+ | D^+)$ with posterior probability $P(D^+ | T^+)$.
