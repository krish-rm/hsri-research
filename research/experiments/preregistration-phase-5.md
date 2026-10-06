# Unified Phase 5 OSF Preregistration Protocol: Behavioral AI Discernment Across Four Knowledge Domains (EXP-01 to EXP-04)

> **OSF Preregistration Type:** Open Science Framework (OSF) Standard Pre-Data Collection Registration  
> **Study Identification:** HSRI-EXP-PHASE5-UNIFIED-2026  
> **Version:** 1.0.0  
> **Date:** 2026-10-06  
> **Status:** Filed for Scientific Governance Review (Pre-Human Subject Deployment)  
> **Ethical Notice:** Minimal risk behavioral protocol. Human subject recruitment is strictly contingent upon formal Institutional Review Board (IRB) approval. No human participants have been recruited prior to this filing.

---

## 1. Study Overview & Institutional Mission

The Human Superintelligence Readiness Index (HSRI) investigates human cognitive resilience, agency retention, and institutional readiness in the face of rapidly advancing frontier artificial intelligence. A fundamental psychometric vulnerability of technology readiness frameworks is over-reliance on self-reported competence and subjective trust scales, which are severely contaminated by social desirability and Dunning-Kruger effects.

Phase 5 of the HSRI Scientific Roadmap establishes an empirical, standardized multi-domain behavioral testing battery. This protocol preregisters the methodology, experimental manipulation, stimulus calibration, and statistical estimation models for four foundational experiments measuring human discernment of fluent AI hallucinations:
1. **EXP-01 (Legal Domain):** Identification of factual, logical, citation, and statutory errors in AI-drafted legal briefs.
2. **EXP-02 (Medical Domain):** Identification of dosage, clinical mechanism, and guideline citation errors in AI clinical summaries.
3. **EXP-03 (Technical/Code Domain):** Identification of API misuse, security vulnerabilities, and logic flaws in AI architectural documentation.
4. **EXP-04 (Financial/Quantitative Domain):** Identification of cash-flow accounting misclassifications, valuation discount rate fallacies, regulatory solvency threshold breaches, and risk metric inflations in AI financial memoranda.

---

## 2. Theoretical Framework & Hypotheses

### 2.1 Theoretical Framework: Cognitive Automation Asymmetry
Generative AI models produce text characterized by high surface fluency, syntactical authority, and institutional styling. According to Dual-Process Theory (Kahneman, 2011; Evans & Stanovich, 2013), high linguistic fluency acts as a cognitive heuristic triggering System 1 acceptance and suppressing System 2 deliberative verification. When AI systems generate "confident hallucinations," humans routinely exhibit automation complacency and deference.

### 2.2 Preregistered Confirmatory Hypotheses

- **Hypothesis 1 (H1: Verification Latency Wedge):**  
  Participants evaluating fluent AI-generated text containing embedded errors will exhibit significantly reduced verification latencies compared to disfluent or hedged control passages ($\Delta t < 0$, $p < .001$), predicting a corresponding reduction in error detection accuracy ($r_{latency, accuracy} > 0$).

- **Hypothesis 2 (H2: Domain Error Discrimination Stability):**  
  Across all four knowledge domains (Legal, Medical, Technical, Financial), individual stimulus item discrimination will achieve point-biserial correlation $D \ge 0.30$, with error detection positively predicted by cognitive reflection (CRT-2 score; $eta_{CRT} > 0$, $p < .01$).

- **Hypothesis 3 (H3: Quantitative Automation Deference):**  
  Participants evaluating quantitative and code domains (EXP-03, EXP-04) will demonstrate significantly higher miss rates (lower detection odds) than participants in text-based domains (EXP-01, EXP-02) when controlling for participant domain familiarity ($	ext{Odds Ratio} < 0.70$, $p < .01$), reflecting heightened deference to numerical matrices, technical jargon, and mathematical formulas.

---

## 3. Experimental Design & Sampling Plan

### 3.1 Design Structure
- **Design Type:** 4 (Domain: Legal vs. Medical vs. Technical vs. Financial) $\times$ 2 (Passage Accuracy: Error-Embedded vs. Error-Free Control) mixed factorial design.
- **Between-Subjects Factor:** Primary Domain assignment (Legal, Medical, Technical, Financial).
- **Within-Subjects Factor:** Stimulus Condition (Calibrated Error Passages vs. Ground-Truth Verified Control Passages).
- **Task Structure:** Each participant evaluates 6 randomized passages (4 target stimuli containing distinct calibrated errors, 2 verified control passages containing zero errors).

### 3.2 Participant Sampling & Inclusion Criteria
- **Target Population:** Educated adults (undergraduate or graduate degree, or current university enrollment) with general literacy and foundational numeracy.
- **Sample Size:** $N = 120$ participants per domain ($N_{total} = 480$ human participants).
- **Exclusion Filters:**
  - Professional specialists holding advanced licensure in the target domain (e.g., licensed attorneys excluded from EXP-01; practicing physicians/pharmacists excluded from EXP-02; professional senior software security engineers excluded from EXP-03; CFA charterholders/CPAs excluded from EXP-04).
  - Failed attention checks ($> 1$ missed check out of 3 embedded catch trials).
  - Rapid click-through speeders (reading latency $< 100$ words per minute or $< 8$ seconds per passage).

### 3.3 Statistical Power Analysis
Power calculations were conducted using $G*Power$ and simulated mixed-effects estimation:
- **Assumed Effect Size:** Medium standardized effect ($f = 0.25$, equivalent to Cohen's $d = 0.35$ or an odds ratio $	ext{OR} = 1.88$).
- **Significance Level:** $\alpha = .05$ (two-tailed, family-wise error controlled).
- **Target Power:** $1 - \beta = 0.80$.
- **Per-Domain Requirement:** Minimum $N = 104$ participants required to achieve $0.80$ power for within-between interaction effects; target $N = 120$ provides over-sampling protection against $15\%$ participant attrition.

#### Power Sensitivity Matrix Across Effect Sizes ($N = 120$ per domain)
| Effect Size ($d$) | Effect Size ($f$) | Expected Power ($1 - \beta$) | Minimum Required Sample | Planned Sample ($N$) |
|---|---|---|---|---|
| $0.25$ (Small) | $0.125$ | $0.62$ | $N = 210$ | $N = 120$ (Underpowered for small) |
| $0.30$ (Moderate-Low) | $0.150$ | $0.74$ | $N = 146$ | $N = 120$ (Marginal) |
| **$0.35$ (Target Effect)** | **$0.175$** | **$0.84$** | **$N = 108$** | **$N = 120$ (Adequately Powered)** |
| $0.40$ (Moderate-High) | $0.200$ | $0.92$ | $N = 82$ | $N = 120$ (Well Powered)** |

---

## 4. Stimulus Materials & Error Taxonomies

All stimuli adhere to strict HSRI psychometric specifications: minimum length 350 characters, realistic institutional prose, single embedded error per stimulus, and no surface typography/grammar giveaways.

### 4.1 Domain Battery Matrix

| Experiment | Domain | Permitted Error Types | Target Entities / Context | Calibrated Item Count |
|---|---|---|---|---|
| **EXP-01** | Legal | `factual`, `logical`, `citation`, `statistical` | Civil litigation, administrative APA review, Fourth Amendment motions | 4 items |
| **EXP-02** | Medical | `dosage`, `factual`, `logical`, `citation` | Outpatient clinical notes, emergency triage, antibiotic guidelines | 4 items |
| **EXP-03** | Technical | `api_misuse`, `security`, `logical`, `factual` | RESTful APIs, JWT tokens, microservice TLS, cryptographic PRNG | 5 items |
| **EXP-04** | Financial | `accounting_logic`, `valuation_fallacy`, `factual_regulatory`, `statistical_distortion` | Cash flow restructuring, DCF acquisition, Basel III capital, Sharpe ratio backtest | 4 items |

---

## 5. Variables & Measurement Plan

### 5.1 Primary Dependent Variables
1. **Error Detection Score (Ordinal $0, 1, 2$):**
   - $0$ = Failure / uncritical acceptance of the erroneous passage.
   - $1$ = Partial detection (locates the suspicious statement but misattributes mechanism).
   - $2$ = Accurate detection and correct causal explanation.
2. **Binary Error Interception Rate ($0$ vs. $1$):**
   - Binary override indicator where Score $\ge 1$ is classified as successful interception.

### 5.2 Secondary Dependent Variables
1. **Verification Latency ($T_{verify}$):** Time spent on the evaluation screen prior to submitting judgment (measured in milliseconds, log-transformed for normality).
2. **Confidence Calibration Bias ($B_{conf}$):** Subjective confidence ($0\% - 100\%$) minus objective accuracy ($0$ or $1$).
3. **Automation Complacency Index ($ACI$):** Composite scale measuring participant reliance on AI suggestions across trials.

### 5.3 Covariates & Individual Differences
- **Cognitive Reflection Test (CRT-2; Thomson & Oppenheimer, 2016):** 4-item cognitive reflection measure.
- **Subjective AI Literacy Scale (Ng et al., 2024):** Self-reported familiarity with LLMs.
- **Domain Background Questionnaire:** Prior coursework or industry experience in target domain.

---

## 6. Confirmatory Statistical Analysis Plan

### 6.1 Confirmatory Model for H1 & H2 (Generalized Linear Mixed-Effects Model)
A binomial Generalized Linear Mixed-Effects Model (GLMM) with a logit link function will estimate error detection probability:

$$\text{logit}(P(Y_{ij} = 1)) = \beta_0 + \beta_1 \text{Domain}_j + \beta_2 \log(T_{ij}) + \beta_3 \text{CRT}_i + \beta_4 (\text{Domain}_j \times \log(T_{ij})) + u_i + v_j + \epsilon_{ij}$$

Where:
- $Y_{ij}$ is the binary error detection of participant $i$ on stimulus $j$.
- $T_{ij}$ is the verification latency in milliseconds.
- $\text{CRT}_i$ is the mean-centered cognitive reflection score.
- $u_i \sim \mathcal{N}(0, \sigma_u^2)$ is the random intercept for participant $i$.
- $v_j \sim \mathcal{N}(0, \sigma_v^2)$ is the random intercept for stimulus item $j$.

### 6.2 Confirmatory Model for H3 (Quantitative Automation Deference)
To test whether quantitative and technical stimuli induce higher automation deference:

$$\text{logit}(P(Y_{ij} = 1)) = \gamma_0 + \gamma_1 \text{IsQuantitative} + \gamma_2 \text{DomainExperience}_i + \gamma_3 \text{CRT}_i + u_i + v_j$$

Where $\text{IsQuantitative} = 1$ for EXP-03 and EXP-04, and $0$ for EXP-01 and EXP-02. The hypothesis is supported if $\gamma_1 < 0$ and $p < .01$.

### 6.3 Missing Data & Outlier Management
- Incomplete sessions ($> 20\%$ missing task items) will be dropped listwise.
- Latency outliers ($> 3$ standard deviations from the domain mean on log-scale) will be winsorized.
- Multiple imputation via chained equations (MICE) will be applied for missing demographic covariates if $< 5\%$ missingness.

---

## 7. Open Science, Archiving & Ethical Governance

1. **Preregistration Archiving:** This document will be stamped and registered on the Open Science Framework (OSF) upon IRB approval.
2. **De-identification & Fictitious Data:** All stimuli utilize fictitious entities and scenarios. Human participant response data will be stripped of IP addresses, Prolific IDs, and identifying demographic markers.
3. **Data Availability:** Anonymized participant response logs, scoring transcripts, analysis scripts in R and Python, and fitted GLMM model outputs will be deposited in the open-access Zenodo repository under Creative Commons Attribution 4.0 International (CC-BY-4.0).
4. **Governed Human Deployment Gate:** No human subjects will be recruited until an accredited institutional ethics review committee grants formal protocol clearance.
