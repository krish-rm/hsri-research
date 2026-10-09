# Phase 8 Protocol: Longitudinal Stability, Test-Retest Reliability, and Latent State-Trait Decomposition

> **Roadmap Phase:** Phase 8 — Longitudinal Stability & Test-Retest Calibration  
> **Document Type:** Pre-Data Collection Longitudinal Reliability & Trait Stability Protocol  
> **Version:** 1.0.0  
> **Date:** October 2026  
> **Status:** Active Scientific Protocol  
> **Gating Criterion:** Demonstrated 30-day temporal stability ($\text{ICC}(3,1) \ge 0.75$, Pearson $r_{tt} \ge 0.80$, Latent Trait Consistency $CO \ge 0.70$), proving that HSRI measures enduring cognitive traits rather than transient day-to-day state fluctuations.

---

## 1. Theoretical Grounding & The Longitudinal Trait Mandate

A persistent challenge in cognitive ergonomics and human-computer interaction is determining whether behavioral performance reflects:
1. **An Enduring Cognitive Trait:** A durable individual disposition toward critical discernment, agency preservation, default resistance, and epistemic friction.
2. **A Transient Cognitive State:** An ephemeral artifact of immediate fatigue, momentary vigilance, time-of-day circadian rhythms, or idiosyncratic luck on specific task items.

Under Section 8.1 of the HSRI Scientific Architecture, Phase 8 applies **Latent State-Trait (LST) Theory** (Steyer, Schmitt, & Eid, 1999; Geiser, 2013) to decompose longitudinal measurement variance across repeated administrations separated by a 30-day interval ($T_0$ to $T_1$).

---

## 2. Latent State-Trait (LST) Variance Decomposition

For an observed task score $Y_{it}$ of participant $i$ on occasion $t \in \{T_0, T_1\}$:
$$Y_{it} = \xi_{trait} + \zeta_{state\_occasion} + \epsilon_{error}$$

Where:
- $\xi_{trait}$ is the invariant latent trait reflecting enduring cognitive AI readiness.
- $\zeta_{state\_occasion}$ is occasion-specific variance (situational vigilance, sleep quality, daily stressors).
- $\epsilon_{error}$ is random measurement error.

### Key Psychometric Coefficients:
1. **Consistency Coefficient ($CO$):** Proportion of true score variance explained by the enduring latent trait:
   $$CO = \frac{\text{Var}(\xi_{trait})}{\text{Var}(Y_{it})}$$
   **Benchmark Target:** $CO \ge 0.70$ (indicating $\ge 70\%$ stable trait composition).
2. **Occasion Specificity ($SP$):** Proportion of variance attributable to transient occasion states:
   $$SP = \frac{\text{Var}(\zeta_{state})}{\text{Var}(Y_{it})}$$
   **Benchmark Target:** $SP \le 0.20$.
3. **Unreliability / Error Variance ($ERR$):**
   $$ERR = \frac{\text{Var}(\epsilon)}{\text{Var}(Y_{it})} \le 0.10$$

---

## 3. Parallel Alternate Forms Design ($Form_A$ vs. $Form_B$)

To eliminate **memory recall carry-over effects** while preserving identical construct difficulty, Phase 8 introduces counterbalanced Parallel Alternate Forms:
- **Form A (Baseline $T_0$):** Canonical stimulus scenarios across EXP-01 to EXP-09.
- **Form B (Retest $T_1$):** Isomorphic alternate scenarios with identical underlying cognitive trap structures, equivalent IRT difficulty ($\Delta \beta \le 0.08$), and matching discrimination ($\alpha$), but entirely novel domain context narratives (see `parallel-forms-specification.md`).

### Counterbalanced Administration:
- Cohort 1 ($N = 300$): Form A at $T_0$ $\to$ 30-day washout $\to$ Form B at $T_1$.
- Cohort 2 ($N = 300$): Form B at $T_0$ $\to$ 30-day washout $\to$ Form A at $T_1$.
- Total Sample: $N = 600$ longitudinal retest cohort.

---

## 4. Test-Retest Metrics & Reliability Standards

1. **Intraclass Correlation Coefficient ($\text{ICC}(3,1)$):**
   Two-way mixed-effects model for absolute agreement (Shrout & Fleiss, 1979; Koo & Li, 2016):
   $$\text{ICC}(3,1) = \frac{MS_R - MS_E}{MS_R + (k - 1) MS_E}$$
   - **Threshold:** $\text{ICC} \ge 0.75$ (Good), $\ge 0.85$ (Excellent).
2. **Pearson Product-Moment Correlation ($r_{tt}$):**
   - **Threshold:** $r_{tt} \ge 0.80$ across the 30-day interval for composite HSRI and all 4 latent factors.
3. **Practice Effect Bound (Cohen's $d$):**
   Mean score difference between $T_0$ and $T_1$ must satisfy:
   $$d = \frac{\bar{X}_{T1} - \bar{X}_{T0}}{S_{\text{pooled}}} < 0.20 \quad (\text{Negligible practice gain})$$

---

## 5. Reliable Change Index (RCI) Specification

To distinguish genuine changes in an individual's AI readiness (e.g., following educational intervention or institutional training) from random test-retest fluctuation, Phase 8 establishes the **Reliable Change Index** (Jacobson & Truax, 1991):
$$\text{RCI} = \frac{X_2 - X_1}{S_{\text{diff}}}, \quad S_{\text{diff}} = \sqrt{2 \cdot \text{SE}_{\text{meas}}^2}, \quad \text{SE}_{\text{meas}} = s \sqrt{1 - r_{tt}}$$

- A participant's score shift is statistically reliable at the 95% confidence level if:
  $$|X_2 - X_1| > 1.96 \cdot S_{\text{diff}}$$

---

## 6. Phase 8 Gating Decision Rules

1. Composite HSRI test-retest reliability must satisfy $r_{tt} \ge 0.80$ and $\text{ICC}(3,1) \ge 0.75$.
2. Latent Trait Consistency must satisfy $CO \ge 0.70$.
3. Parallel form equivalence must satisfy $|\beta_A - \beta_B| \le 0.10$.
4. Practice effect must be bounded: Cohen's $d < 0.20$.
5. Satisfying these criteria officially clears **PHASE 8**, authorizing transition to **Phase 9: Multi-Agent Adversarial Consensus**.
