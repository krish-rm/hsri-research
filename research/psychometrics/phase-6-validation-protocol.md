# Phase 6 Psychometric Validation Protocol: Latent Construct Modeling, MTMM, and Incremental Validity

> **Roadmap Phase:** Phase 6 — Psychometric Validation (The Decisive Phase)  
> **Document Type:** Pre-Data Collection Formal Statistical & Psychometric Validation Protocol  
> **Version:** 1.0.0  
> **Date:** 2026-10-06  
> **Status:** Active Scientific Protocol  
> **Gating Criterion:** Demonstrated Incremental Validity: HSRI explains statistically significant unique variance in real-world human-AI override accuracy beyond existing standalone instruments ($\\Delta R^2 > 0$, $p < .01$).

---

## 1. Theoretical Grounding & The Decisive Phase Mandate

A foundational flaw in contemporary AI readiness benchmarks is construct contamination: frameworks aggregate subjective self-report questionnaires (e.g., self-assessed digital literacy, general self-efficacy, or subjective comfort with technology) without demonstrating that the composite explains actual behavioral variance.

Phase 6 serves as the **decisive gate** of the HSRI program. Under Section 8.1 of the HSRI Scientific Architecture, Phase 6 must empirically establish:
1. **Structural Construct Validity:** The four behavioral pillars reflect a coherent, multi-dimensional latent trait architecture rather than an uncoordinated collection of ad-hoc tasks.
2. **Convergent and Discriminant Validity:** The instrument demonstrates appropriate convergent correlation with related cognitive traits (cognitive reflection, working memory) while maintaining strict discriminant separation from unrelated traits (agreeableness, neuroticism, general tech optimism).
3. **Incremental Validity (The Core Gate):** The HSRI composite accounts for significant unique variance ($\\Delta R^2 > 0$) in downstream error interception and agency preservation above and beyond existing standalone instruments.

---

## 2. Four-Pillar Latent Construct Architecture

The 9 standardized behavioral tasks (EXP-01 through EXP-09) map onto a 4-factor latent structural model:

```
                            [ GENERAL HSRI LATENT TRAIT ]
                                         │
        ┌───────────────────┬────────────┴───────┬───────────────────┐
        ▼                   ▼                    ▼                   ▼
    [Factor 1]          [Factor 2]           [Factor 3]          [Factor 4]
   Cognitive           Overload &           Autonomous          Calibrated
   Discernment         Default              Agency              Epistemic
   & Fallacy           Resistance           Preservation        Friction
   Interception                             
        │                   │                    │                   │
   ├── EXP-01 (Legal)  └── EXP-05 (Choice   ├── EXP-06 (Deleg.) ├── EXP-07 (Belief)
   ├── EXP-02 (Med.)       Overload)        └── EXP-08 (Super.) └── EXP-09 (Forcing)
   ├── EXP-03 (Tech.)
   └── EXP-04 (Fin.)
```

### Factor Definitions & Measurement Indicators:
- **Factor 1: Cognitive Discernment & Fallacy Interception ($\\eta_1$):**  
  Measures substantive domain error detection accuracy across legal, clinical, technical, and quantitative environments under authoritative AI surface fluency.
- **Factor 2: Overload & Default Resistance ($\\eta_2$):**  
  Measures preservation of critical evaluation under high choice density (8-option matrices) and strict time pressure (45s), resisting top-ranked machine anchors.
- **Factor 3: Autonomous Agency Preservation ($\\eta_3$):**  
  Measures refusal to abdicate decision ownership, maintenance of situational comprehension despite automation, and independent hypothesis generation following capability asymmetry.
- **Factor 4: Calibrated Epistemic Friction ($\\eta_4$):**  
  Measures Bayesian belief updating in response to counter-intuitive data, resistance to spurious machine 'evidence', and loyalty to verified independent precommitments.

---

## 3. Structural Equation Model & CFA Goodness-of-Fit Criteria

Confirmatory Factor Analysis (CFA) will evaluate the fit of the proposed 4-factor correlated model against alternative 1-factor (unidimensional) and orthogonal models.

### Target Fit Thresholds:
- **Root Mean Square Error of Approximation (RMSEA):** $\\le 0.05$ (acceptable up to $0.06$).
- **Comparative Fit Index (CFI):** $\\ge 0.95$ (acceptable $\\ge 0.90$).
- **Tucker-Lewis Index (TLI):** $\\ge 0.95$ (acceptable $\\ge 0.90$).
- **Standardized Root Mean Square Residual (SRMR):** $\\le 0.08$.

If the 4-factor model fails to meet CFI $\\ge 0.90$ or RMSEA $\\le 0.06$, modification indices will be audited and non-invariant items quarantined.

---

## 4. Multitrait-Multimethod (MTMM) Matrix Specification

Following Campbell and Fiske (1959), construct validity is evaluated across three cognitive traits measured by two independent methods (Standardized Interactive Tasks vs. Calibrated Scenario Diagnostics):

| Trait | Method 1 (Interactive Simulation Task) | Method 2 (Calibrated Vignette Scenario) |
|---|---|---|
| **Trait A:** Cognitive Discernment | EXP-01 to EXP-04 Task Scores | Scenario Verification Test |
| **Trait B:** Default Resistance | EXP-05 Matrix Choice Override | High-Density Case Audit |
| **Trait C:** Agency Preservation | EXP-06 / EXP-08 Delegation & Hypothesis Log | Supervisory Override Vignette |

### MTMM Validation Criteria:
1. **Monotrait-Heteromethod (Convergent Validity):** $r(A_1, A_2) > 0.50$, $r(B_1, B_2) > 0.50$, $r(C_1, C_2) > 0.50$ (all $p < .001$).
2. **Heterotrait-Heteromethod (Discriminant Validity):** $r(A_1, B_2) < r(A_1, A_2)$, with average discriminant correlation $r < 0.35$.
3. **Discriminant Divergence from Unrelated Constructs:** Correlation with Big Five Neuroticism ($|r| < 0.15$) and Technology Optimism ($|r| < 0.20$).

---

## 5. Hierarchical Incremental Validity Model (The Gating Test)

### 5.1 Dependent Criterion: Real-World AI Override Accuracy ($Y_{override}$)
The criterion variable $Y_{override}$ is an independent, high-fidelity composite score measuring successful interception of critical errors in simulated professional workflows across 30 real-world scenarios.

### 5.2 Competing Baseline Instruments:
1. **Cognitive Reflection Test (CRT-2; Thomson & Oppenheimer, 2016):** Standard 4-item measure of reflective vs intuitive cognitive style.
2. **AI Literacy Scale (Ng et al., 2024):** 12-item validated self-report instrument of AI technical awareness and evaluation.
3. **Trust in Automation Scale (Jian et al., 2000):** Standard 12-item subjective trust inventory.
4. **General Self-Efficacy Scale (Schwarzer & Jerusalem, 1995):** 10-item self-efficacy measure.

### 5.3 Hierarchical Regression Model Specification:

$$\\text{Model 1 (Baseline Covariates): } Y = \\beta_0 + \\beta_1 \\text{CRT} + \\beta_2 \\text{AILit} + \\beta_3 \\text{Trust} + \\beta_4 \\text{SelfEfficacy} + \\epsilon$$

$$\\text{Model 2 (HSRI Augmented Model): } Y = \\beta_0 + \\beta_1 \\text{CRT} + \\beta_2 \\text{AILit} + \\beta_3 \\text{Trust} + \\beta_4 \\text{SelfEfficacy} + \\gamma_1 \\text{HSRI}_1 + \\gamma_2 \\text{HSRI}_2 + \\gamma_3 \\text{HSRI}_3 + \\gamma_4 \\text{HSRI}_4 + \\epsilon$$

### 5.4 Falsifiable Gating Hypotheses:
- **Null Hypothesis ($H_0$):** $\\Delta R^2 = R_2^2 - R_1^2 = 0$ (HSRI provides zero incremental explanatory power over existing surveys).
- **Alternative Hypothesis ($H_1$):** $\\Delta R^2 \\ge 0.15$ with $F_{\\Delta}(4, N-9) > F_{\\text{crit}}$ and $p < .001$.
- **Gating Rule:** If $\\Delta R^2$ fails to achieve statistical significance ($p \ge .05$), Phase 6 fails and the instrument must undergo structural item pruning before any Phase 7 cross-cultural administration.

---

## 6. Item Response Theory (IRT) Calibration Model

All dichotomous and binarized task outcomes will be fitted with a **2-Parameter Logistic (2PL) IRT Model**:

$$P(Y_{ik} = 1 | \\theta_i) = \\frac{1}{1 + e^{-\\alpha_k (\\theta_i - \\beta_k)}}$$

Where:
- $\\theta_i \\sim \\mathcal{N}(0, 1)$ represents the latent human AI-readiness capability of participant $i$.
- $\\alpha_k$ represents item discrimination for task item $k$ (Target: $1.0 \\le \\alpha_k \\le 2.5$).
- $\\beta_k$ represents item difficulty (Target: standardized span across $[-2.0, +2.0]$ to prevent floor or ceiling compression).
