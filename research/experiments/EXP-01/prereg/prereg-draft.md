# Preregistration Draft: EXP-01 Human Pilot Study

> **DRAFT: NOT SUBMITTED. NO HUMAN DATA COLLECTED. NO PI DESIGNATED**
> **PREVIEW DISCLAIMER: HSRI v0.3.0-dev**
> This preregistration draft outlines the exploratory human-participant calibration protocol for HSRI Experiment 01 (Legal Domain). All components represent research scaffolds under development. In strict compliance with Standing Governance Rule 6, no stimuli will be deployed to human participants prior to formal institutional review board (IRB) submission and approval, and designation of a Principal Investigator. All outputs carry the v0.3-dev preview notice.

---

## 1. Study Information

- **Study Title:** Human Discernment Under Cognitive Automation Pressure: Fluent Hallucination Detection in Legal Documentation (HSRI EXP-01)
- **Primary Investigator:** `[DECISION NEEDED: Institutional PI to be formally designated upon IRB application submission]`
- **Lead Statistician:** `[DECISION NEEDED: Institutional Biostatistician/Methodologist to be designated]`
- **Affiliated Repository:** `https://github.com/krish-rm/hsri-research`
- **Protocol Version:** v0.3.0-dev-prereg

---

## 2. Research Questions & Hypotheses

### 2.1 Research Questions
1. **RQ1 (Framing Effect):** Does explicit labeling of legal text as "AI-generated draft" induce cognitive automation bias—manifesting as reduced error detection rates and uncritical endorsement—relative to identical text labeled as "peer-reviewed human draft"?
2. **RQ2 (Processing Latency):** Does reading latency correlate positively with error detection accuracy, substantiating the theoretical prediction that uncritical acceptance stems from System 1 heuristic processing rather than deliberative System 2 scrutiny?

### 2.2 Formal Hypotheses
- **Hypothesis 1 (Primary - Framing Effect):** Participants in the experimental condition (AI-generated framing) will achieve significantly lower composite error detection scores ($d \ge 0.35$) compared to participants in the control condition (peer-reviewed framing).
- **Hypothesis 2 (Secondary - Process / Latency):** Across both conditions, inspection latency (seconds spent per stimulus item) will correlate positively with error detection score, with participants failing to detect errors exhibiting significantly shorter reading latencies.
- **Hypothesis 3 (Exploratory - Confidence Calibration):** Participants in the AI-generated condition who fail to detect embedded errors will report equal or higher subjective confidence compared to participants who successfully detect the error, demonstrating unwarranted epistemic certainty.

---

## 3. Experimental Design

- **Design Type:** Between-subjects, two-arm randomized controlled experiment.
- **Factor:** Framing Condition (2 levels, randomized 1:1 via survey platform):
  - **Condition A (Experimental — AI Framing):** Passages are framed as "First-draft summary produced by an advanced generative artificial intelligence legal assistant."
  - **Condition B (Control — Peer-Reviewed Framing):** Identical passages are framed as "First-draft summary produced by a senior legal associate, subject to secondary peer review."
- **Stimulus Battery:** Each participant reads and evaluates three standardized legal passages (350–500 words each), presented in randomized order:
  - **Item 1 (`legal_001` - Logical Inversion):** First 80 chars: `"In contractual indemnity and liability allocation, an exculpatory waiver absolve"`. Core flaw: Inversion of core exculpatory doctrine asserting a waiver can absolve gross negligence.
  - **Item 2 (`legal_002` - Factual Misattribution):** First 80 chars: `"Under federal jurisprudence governing common carriers, the duty of extraordinary"`. Core flaw: False constitutionalization of common carrier duty under the 14th Amendment rather than state common law.
  - **Item 3 (`legal_003` - Citation Fabrication):** First 80 chars: `"Municipal zoning ordinances and land-use restrictions frequently trigger qualifi"`. Core flaw: Fabricated attribution of municipal zoning and qualified immunity doctrine to *Brown v. Board of Education* (1954).
- **Task Procedure:**
  1. Informed consent and inclusion screening.
  2. On-screen task instructions and framing exposure.
  3. Sequential presentation of the 3 passages (order randomized).
  4. For each passage:
     - Error identification prompt: *"Does this text contain any factual inaccuracy, logical flaw, or invalid citation? If yes, identify the specific flaw and explain why it is incorrect."*
     - Confidence rating (1–5 Likert scale: 1 = Completely Unconfident, 5 = Completely Confident).
  5. Attention check item.
  6. Demographics and debriefing.

---

## 4. Outcome Measures & Scoring Rubric

### 4.1 Primary Outcome Measure
The primary outcome is the **Error Detection Score** per item, graded on an ordinal 3-point scale (0, 1, 2) according to the pre-established HSRI EXP-01 Scoring Rubric:

| Score | Classification | Operational Criteria |
|:---:|:---|:---|
| **2** | **Accurate Identification & Explanation** | Participant accurately locates the embedded error and correctly articulates why it constitutes a factual, logical, citation, or statistical distortion without introducing confabulated objections. |
| **1** | **Partial Detection** | Participant flags the correct sentence or paragraph as problematic but misattributes the mechanism (e.g., classifies a logical contradiction as a stylistic ambiguity or cites an unrelated trivial concern). |
| **0** | **Failure / Uncritical Acceptance** | Participant endorses the passage as sound, fails to flag the error, or flags legitimate surrounding context as defective while missing the embedded flaw. |

Composite score per participant is the sum across the 3 items (range: 0 to 6 points).

### 4.2 Secondary & Process Outcomes
1. **Inspection Latency:** Automated timer measuring total elapsed seconds per item from screen render to response submission.
2. **Subjective Confidence:** 5-point Likert scale response following each item.
3. **Sycophantic Endorsement Count:** Binary flag per item identifying responses that explicitly praise the authoritative fluency of flawed arguments.

---

## 5. Participant Criteria & Exclusion Rules

### 5.1 Inclusion Criteria
- Adults aged 18 years or older.
- General adult literacy level in English (assessed via pre-screening comprehension item).
- Residing in the recruitment jurisdiction.

### 5.2 Exclusion Criteria (Pre-Randomization)
As defined in `research/experiments/EXP-01/irb-package/02-participant-criteria.md`:
- Individuals with formal legal education beyond secondary school (law students, holders of JD/LLB or equivalent legal credentials).
- Current or past employment in the legal profession (lawyers, paralegals, legal clerks, compliance officers).
- Prior exposure to HSRI experimental materials or participation in earlier pilot rounds.

### 5.3 Post-Randomization Data Exclusion Rules
Participant protocols will be excluded from final inferential analysis if:
1. The participant fails the embedded directed-attention check item (e.g., *"Please select 'Slightly Agree' to confirm you are reading these instructions"*).
2. Total inspection latency across all three items is $< 45$ seconds (indicating non-reading / mechanical clicking).
3. The response text contains non-responsive gibberish, copy-pasted prompt instructions, or automated bot signatures.
- `[DECISION NEEDED: Statistician to confirm whether participants with exactly 1 excluded item should have remaining 2 items analyzed in mixed-effects models or be dropped listwise.]`

---

## 6. Planned Statistical Analysis

### 6.1 Primary Model: Handling Repeated Items
Because each participant evaluates 3 distinct stimulus items, observations are nested within participants and cross-classified by stimulus items.
- **Model Specification:** Cumulative Link Mixed Model (CLMM) for ordinal item scores (0, 1, 2), or alternatively a Linear Mixed-Effects Model (LMM) on the composite score:
  $$\text{logit}(P(Y_{ij} \le k)) = \theta_k - (\beta_1 \cdot \text{Condition}_i + u_i + v_j)$$
  where:
  - $\text{Condition}_i$ is the fixed effect of experimental arm ($0 = \text{Peer-Reviewed}$, $1 = \text{AI-Generated}$).
  - $u_i \sim \mathcal{N}(0, \sigma_u^2)$ is the random intercept for participant $i$.
  - $v_j \sim \mathcal{N}(0, \sigma_v^2)$ is the random intercept for stimulus item $j$.
- **Software Implementation:** R `ordinal::clmm()` or Python `statsmodels` / `lme4`.
- `[DECISION NEEDED: Statistician to formally approve whether ordinal CLMM is mandatory or whether standard linear mixed-effects (LMM, lmer) on the 0–6 composite is acceptable as primary specification.]`
- `[DECISION NEEDED: PI to designate whether Item 3 (citation fabrication) is analyzed jointly with Items 1–2 in the primary omnibus model or reported separately due to domain knowledge requirements.]`

### 6.2 Secondary Analyses & Multiple Comparisons
- **Latency Analysis:** Log-transformed latency modeled via linear regression: $\log(\text{Latency}_{ij}) = \alpha + \gamma_1 \text{Score}_{ij} + \gamma_2 \text{Condition}_i + u_i + v_j$.
- **Multiple Comparisons Correction:** Family-wise error rate across the primary hypothesis (framing on detection) and secondary hypothesis (latency-accuracy relationship) controlled using the Holm-Bonferroni step-down procedure ($\alpha = 0.05$).

---

## 7. Sample Size & Power Analysis

### 7.1 Assumptions
The target effect size is set at **Cohen's $d = 0.35$**.
- **Important Governance Note:** This effect size assumption is derived strictly from published peer-reviewed human-automation interaction literature (Goddard et al., 2012; Parasuraman & Riley, 1997; Skitka et al., 1999). It is **not** an empirical finding or measurement of the HSRI repository.
- $\alpha = 0.05$ (two-tailed, $\alpha/2 = 0.025$).
- Target Power $(1 - \beta) = 0.80$.

### 7.2 Sample Size Determination
$$\text{Required } N \text{ per group} \approx 2 \cdot \left(\frac{z_{\alpha/2} + z_{\beta}}{d}\right)^2 = 2 \cdot \left(\frac{1.96 + 0.842}{0.35}\right)^2 \approx 2 \cdot (8.006)^2 \approx 128.2$$
Rounding up and incorporating an anticipated **$5\%$ participant attrition/incomplete session rate**, the planned sample size is **$N = 130$ participants per condition**, yielding a total enrollment target of **$N = 260$ participants** ($780$ participant-item evaluation pairs).

### 7.3 Power Sensitivity Table
The following sensitivity table establishes achieved statistical power across various plausible effect sizes given planned sample sizes:

| Effect Size (Cohen's $d$) | Description | Power ($N=100$/group) | Power ($N=130$/group, Target) | Power ($N=160$/group) | Required $N$/group for 80% Power |
|:---:|:---|:---:|:---:|:---:|:---:|
| **$0.20$** | Subtle / Small Effect | $29.1\%$ | $36.2\%$ | $43.0\%$ | $393$ |
| **$0.25$** | Small-to-Moderate Effect | $42.2\%$ | $51.8\%$ | $60.5\%$ | $252$ |
| **$0.30$** | Moderate Effect | $56.4\%$ | $67.5\%$ | $76.2\%$ | $175$ |
| **$0.35$** | **Target Literature Baseline** | **$69.7\%$** | **$80.4\%$** | **$87.8\%$** | **$128$** |
| **$0.40$** | Moderate-to-Substantial Effect | $80.8\%$ | $89.7\%$ | $94.9\%$ | $99$ |
| **$0.50$** | Large Effect | $94.0\%$ | $98.4\%$ | $99.6\%$ | $63$ |

---

## 8. Stopping Rules & Data Monitoring

- **Stopping Rule:** Participant recruitment will cease immediately upon reaching exactly $N = 130$ completed, non-excluded sessions per arm ($N = 260$ total valid participants).
- **Interim Analysis:** No sequential interim looks for statistical significance will be performed. Early stopping for efficacy is strictly prohibited to prevent inflated Type I error.
- `[DECISION NEEDED: PI and IRB to determine whether an independent Data Safety and Monitoring Board (DSMB) or an interim futility audit at 50% enrollment (N=130 total) is required.]`

---

## 9. Epistemic Scope: What Will and Will Not Be Concluded

### 9.1 What Will Be Concluded (If Hypotheses Are Supported)
- Whether explicit labeling of legal summaries as AI-generated versus human peer-reviewed causally alters the rate at which lay adults detect calibrated legal errors.
- Empirical quantification of human reading latency under automation framing.
- Preliminary psychometric difficulty and discrimination parameters for calibrated legal stimuli in a human sample.

### 9.2 What Will NOT Be Concluded
- **No Claims of General Human Vulnerability:** Findings will not be extrapolated to claim that humans are inherently incapable of identifying AI errors.
- **No National Index Calibration:** Results from an exploratory lay pilot cannot be used to extrapolate national-level HSRI scores or replace missing proxy indicators.
- **No Claims Regarding Legal Professionals:** Results will not be generalized to practicing attorneys, judges, or paralegals, who operate under professional duties of inquiry.
- **No Global / Cross-Cultural Universality:** Findings will reflect only the specific demographic population sampled and will carry explicit WEIRD demographic boundary caveats.
