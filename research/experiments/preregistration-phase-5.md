# Unified Phase 5 OSF Preregistration Protocol: Behavioral AI Discernment, Choice Overload, and Autonomous Delegation (EXP-01 to EXP-06)

> **OSF Preregistration Type:** Open Science Framework (OSF) Standard Pre-Data Collection Registration  
> **Study Identification:** HSRI-EXP-PHASE5-UNIFIED-2026  
> **Version:** 2.0.0  
> **Date:** 2026-10-06  
> **Status:** Filed for Scientific Governance Review (Pre-Human Subject Deployment)  
> **Ethical Notice:** Minimal risk behavioral protocol. Human subject recruitment is strictly contingent upon formal Institutional Review Board (IRB) approval. No human participants have been recruited prior to this filing.

---

## 1. Study Overview & Institutional Mission

The Human Superintelligence Readiness Index (HSRI) investigates human cognitive resilience, agency retention, and institutional readiness in the face of rapidly advancing frontier artificial intelligence. A fundamental psychometric vulnerability of technology readiness frameworks is over-reliance on self-reported competence and subjective trust scales, which are severely contaminated by social desirability and Dunning-Kruger effects.

Phase 5 of the HSRI Scientific Roadmap establishes an empirical, standardized multi-domain behavioral testing battery. This protocol preregisters the methodology, experimental manipulation, stimulus calibration, and statistical estimation models for six foundational experiments measuring human discernment, decision agency, and cognitive offloading under AI automation pressure:
1. **EXP-01 (Legal Domain):** Identification of factual, logical, citation, and statutory errors in AI-drafted legal briefs.
2. **EXP-02 (Medical Domain):** Identification of dosage, clinical mechanism, and guideline citation errors in AI clinical summaries.
3. **EXP-03 (Technical/Code Domain):** Identification of API misuse, security vulnerabilities, and logic flaws in AI architectural documentation.
4. **EXP-04 (Financial/Quantitative Domain):** Identification of cash-flow accounting misclassifications, valuation discount rate fallacies, regulatory solvency threshold breaches, and risk metric inflations in AI financial memoranda.
5. **EXP-05 (Choice-Overload Stress Test):** Evaluation of decision paralysis, latency, and susceptibility to machine default anchors under high option density and time pressure.
6. **EXP-06 (Autonomous Delegation Offer):** Evaluation of delegation propensity, cognitive offloading comprehension penalties, and post-hoc accountability attribution during high-stakes multi-step workflows.

---

## 2. Theoretical Framework & Hypotheses

### 2.1 Theoretical Framework: Cognitive Automation Asymmetry & Cognitive Offloading
Generative and agentic AI systems introduce two critical psychological vulnerabilities:
1. **Fluency-Induced Complacency (Dual-Process Theory; Kahneman, 2011):** High linguistic fluency and authoritative styling act as cognitive heuristics triggering System 1 acceptance while suppressing System 2 deliberative verification.
2. **The Cognitive Offloading Penalty (Risko & Gilbert, 2016; Mosier & Skitka, 1996):** When individuals delegate multi-step operational tasks to autonomous agents, situational awareness and working-memory representations of system state decay rapidly, rendering human supervisors blind to downstream execution anomalies ("Control Without Agency").

### 2.2 Preregistered Confirmatory Hypotheses

- **Hypothesis 1 (H1: Verification Latency Wedge):**  
  Participants evaluating fluent AI-generated text containing embedded errors will exhibit significantly reduced verification latencies compared to disfluent or hedged control passages ($\Delta t < 0$, $p < .001$), predicting a corresponding reduction in error detection accuracy ($r_{latency, accuracy} > 0$).

- **Hypothesis 2 (H2: Domain Error Discrimination Stability):**  
  Across all four knowledge domains (Legal, Medical, Technical, Financial), individual stimulus item discrimination will achieve point-biserial correlation $D \ge 0.30$, with error detection positively predicted by cognitive reflection (CRT-2 score; $eta_{CRT} > 0$, $p < .01$).

- **Hypothesis 3 (H3: Quantitative Automation Deference):**  
  Participants evaluating quantitative and code domains (EXP-03, EXP-04) will demonstrate significantly higher miss rates (lower detection odds) than participants in text-based domains (EXP-01, EXP-02) when controlling for participant domain familiarity ($	ext{Odds Ratio} < 0.70$, $p < .01$).

- **Hypothesis 4 (H4: Machine Default Anchor Deference under Choice Overload):**  
  In high-density choice environments (8 options) under time pressure (45s), participant adoption of the AI's top-ranked default recommendation will significantly exceed rational baseline choice rates ($P(	ext{Default}) > 0.65$, $p < .001$), with decision paralysis (timeouts) positively predicted by Intolerance of Uncertainty (IUS-12 score; $eta_{IUS} > 0$, $p < .01$).

- **Hypothesis 5 (H5: Autonomous Delegation & Cognitive Offloading Penalty):**  
  Participants who accept full autonomous delegation in Step 4 of a 10-step workflow will exhibit significantly lower post-task mechanistic comprehension scores ($\Delta 	ext{Comprehension} < -0.80$, $p < .001$) and lower Step 8 error interception rates ($	ext{OR} < 0.25$, $p < .001$) compared to participants who retain manual supervisory control, exhibiting increased algorithmic scapegoating in post-hoc incident attribution.

---

## 3. Experimental Design & Sampling Plan

### 3.1 Design Structure
- **Part I: Multi-Domain Fluent Hallucination Detection (EXP-01 to EXP-04):**
  - 4 (Domain: Legal vs. Medical vs. Technical vs. Financial) $	imes$ 2 (Passage Accuracy: Error-Embedded vs. Error-Free Control) mixed factorial design.
  - Between-subjects assignment to domain; within-subjects evaluation of 6 randomized passages (4 target stimuli, 2 controls).
- **Part II: Choice-Overload Stress Test (EXP-05):**
  - 2 (Choice Density: High [8 options] vs. Low [3 options]) $	imes$ 2 (Machine Recommendation: Top-Ranked Default vs. Unranked) between-subjects design under uniform 45s time constraint.
- **Part III: Autonomous Delegation Paradigm (EXP-06):**
  - Sequential decision paradigm: Baseline manual control (Steps 1–3) followed by Step 4 Delegation Offer (Accept Delegation vs. Retain Manual Control). Quasi-experimental comparison on Step 8 error interception and post-task comprehension.

### 3.2 Participant Sampling & Inclusion Criteria
- **Target Population:** Educated adults (undergraduate or graduate degree, or current university enrollment) with general literacy and foundational numeracy.
- **Sample Size:** $N = 120$ participants per experiment protocol ($N_{total} = 720$ human participants across EXP-01 through EXP-06).
- **Exclusion Filters:**
  - Specialized domain practitioners with advanced licensure (lawyers, physicians, CPAs, senior cybersecurity architects).
  - Failed attention checks ($> 1$ missed check out of 3 embedded catch trials).
  - Rapid click-through speeders (reading latency $< 100$ words per minute or $< 8$ seconds per passage).

### 3.3 Statistical Power Analysis
Power calculations were conducted using $G*Power$ and simulated mixed-effects estimation:
- **Assumed Effect Size:** Medium standardized effect ($f = 0.25$, equivalent to Cohen's $d = 0.35$ or an odds ratio $	ext{OR} = 1.88$).
- **Significance Level:** $lpha = .05$ (two-tailed, family-wise error controlled).
- **Target Power:** $1 - eta = 0.80$.
- **Per-Protocol Requirement:** Minimum $N = 108$ participants required to achieve $0.80$ power for main effects and interactions; planned $N = 120$ per protocol provides over-sampling protection against $15\%$ participant attrition.

#### Power Sensitivity Matrix Across Effect Sizes ($N = 120$ per protocol)
| Effect Size ($d$) | Effect Size ($f$) | Expected Power ($1 - eta$) | Minimum Required Sample | Planned Sample ($N$) |
|---|---|---|---|---|
| $0.25$ (Small) | $0.125$ | $0.62$ | $N = 210$ | $N = 120$ (Underpowered for small) |
| $0.30$ (Moderate-Low) | $0.150$ | $0.74$ | $N = 146$ | $N = 120$ (Marginal) |
| **$0.35$ (Target Effect)** | **$0.175$** | **$0.84$** | **$N = 108$** | **$N = 120$ (Adequately Powered)** |
| $0.40$ (Moderate-High) | $0.200$ | $0.92$ | $N = 82$ | $N = 120$ (Well Powered)** |

---

## 4. Stimulus Materials & Error Taxonomies

All stimuli adhere to strict HSRI psychometric specifications: minimum length 350 characters, realistic institutional prose, single embedded error or structural flaw per scenario, and no surface typography/grammar giveaways.

### 4.1 Master Phase 5 Battery Matrix

| Experiment | Paradigm / Domain | Permitted Error / Flaw Types | Context / Scenarios | Calibrated Items |
|---|---|---|---|---|
| **EXP-01** | Legal Hallucination Detection | `factual`, `logical`, `citation`, `statistical` | Civil litigation, APA review, Fourth Amendment motions | 4 items |
| **EXP-02** | Medical Hallucination Detection | `dosage`, `factual`, `logical`, `citation` | Clinical triage, antibiotic dosing, pulmonary guidelines | 4 items |
| **EXP-03** | Technical Hallucination Detection | `api_misuse`, `security`, `logical`, `factual` | RESTful APIs, JWT tokens, microservice TLS, PRNG crypto | 5 items |
| **EXP-04** | Financial Hallucination Detection | `accounting_logic`, `valuation_fallacy`, `factual_regulatory`, `statistical_distortion` | Cash flow restructuring, DCF valuation, Basel III capital, Sharpe ratio backtest | 4 items |
| **EXP-05** | Choice-Overload Stress Test | `hidden_negative_externality`, `pareto_suboptimal_tradeoff`, `constraint_violation`, `risk_asymmetry` | Grid load shedding, harbor berthing, cloud migration, surge ICU bed allocation | 4 items |
| **EXP-06** | Autonomous Delegation Paradigm | `safety_boundary_breach`, `unauthorized_divergence`, `audit_trail_deletion`, `cascading_resource_starvation` | Disaster medical supply, municipal water dosing, RTGS interbank clearing, 911 cloud routing | 4 items |

---

## 5. Variables & Measurement Plan

### 5.1 Primary Dependent Variables
1. **Error Detection Score (Ordinal $0, 1, 2$):** Identification accuracy and explanation quality (EXP-01 through EXP-04).
2. **Default Recommendation Adoption Rate ($P(	ext{Default})$):** Proportion of participants selecting the AI's top-ranked choice (EXP-05).
3. **Decision Paralysis Rate:** Proportion of trials exceeding the 45-second deadline without action (EXP-05).
4. **Delegation Acceptance Rate ($P(	ext{Delegate})$):** Proportion accepting autonomous execution at Step 4 (EXP-06).
5. **Step 8 Error Interception Rate ($0$ vs. $1$):** Verification and override of the autonomous defect before commit (EXP-06).
6. **Mechanistic Comprehension Score ($0, 1, 2$):** Accuracy of explanation of resulting system state (EXP-06).

### 5.2 Secondary Dependent Variables & Individual Covariates
1. **Verification Latency ($T_{verify}$):** Reading and evaluation time in milliseconds (log-transformed).
2. **Cognitive Reflection Test (CRT-2; Thomson & Oppenheimer, 2016):** 4-item cognitive reflection measure.
3. **Intolerance of Uncertainty Scale (IUS-12; Carleton et al., 2007):** 12-item uncertainty tolerance scale.
4. **Post-Hoc Accountability Attribution (Scale 1–5):** Supervisory human liability versus algorithmic scapegoating.

---

## 6. Confirmatory Statistical Analysis Plan

### 6.1 Confirmatory Model for H1, H2, H3 (GLMM for Hallucination Detection)
A binomial Generalized Linear Mixed-Effects Model (GLMM) with a logit link function:

$$\text{logit}(P(Y_{ij} = 1)) = \beta_0 + \beta_1 \text{Domain}_j + \beta_2 \log(T_{ij}) + \beta_3 \text{CRT}_i + \beta_4 (\text{Domain}_j \times \log(T_{ij})) + u_i + v_j + \epsilon_{ij}$$

### 6.2 Confirmatory Model for H4 (Choice Overload & Default Adoption)
A binary logistic regression estimating probability of selecting the AI top-ranked default:

$$\text{logit}(P(\text{SelectDefault}_i = 1)) = \alpha_0 + \alpha_1 \text{ChoiceDensity}_i + \alpha_2 \text{IUS}_i + \alpha_3 \text{CRT}_i + \epsilon_i$$

Hypothesis H4 is confirmed if $\alpha_1 > 0$ with $p < .001$.

### 6.3 Confirmatory Model for H5 (Cognitive Offloading & Delegation Penalty)
A linear regression evaluating post-task mechanistic comprehension score:

$$\text{Comprehension}_i = \gamma_0 + \gamma_1 \text{Delegated}_i + \gamma_2 \text{CRT}_i + \gamma_3 \text{PriorExperience}_i + \epsilon_i$$

Hypothesis H5 is confirmed if $\gamma_1 < -0.80$ with $p < .001$.

---

## 7. Open Science, Archiving & Ethical Governance

1. **Preregistration Archiving:** Stamped and registered on the Open Science Framework (OSF) upon IRB approval.
2. **De-identification & Fictitious Data:** All stimuli utilize strictly fictitious corporate and municipal entity names. Anonymized participant telemetry will be stripped of PII and IP addresses.
3. **Data Availability:** Participant response logs, task execution traces, scoring matrices, analysis scripts (R and Python), and fitted GLMM outputs will be deposited in Zenodo under CC-BY-4.0.
4. **Governed Human Deployment Gate:** No human subjects will be recruited until an accredited institutional ethics review committee grants formal protocol clearance.
