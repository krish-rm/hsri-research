# Institutional Review Board (IRB) Protocol Application: HSRI Behavioral Validation

> **Protocol ID:** HSRI-IRB-2026-088  
> **Study Title:** Empirical Assessment of Human Agency, Cognitive Discernment, and Default Resistance under Advanced AI Decision Support  
> **Principal Investigator:** HSRI Research Group / Lead Psychometrics Unit  
> **Affiliation:** Human-AI Systemic Readiness Initiative (HSRI Research Consortium)  
> **Protocol Category:** Behavioral & Cognitive Science / Human-Computer Interaction  
> **Review Classification:** Expedited Review (Minimal Risk, Benign Behavioral Intervention under 45 CFR 46.110 Category 7)  
> **Effective Date:** October 2026  
> **Version:** 1.0.0  

---

## 1. Study Personnel & Research Affiliations
- **Principal Investigator (PI):** Krishnakumar R. M. (HSRI Principal Research Director)
- **Co-Investigators:** Quantitative Psychometrics & Cognitive Architecture Research Fellows
- **Collaborating Institutions:** Academic Cognitive Science & Human-Computer Interaction Consortium Laboratories
- **Primary Contact:** `research@hsri.org` (or institutional contact portal)

---

## 2. Scientific Justification, Purpose & Hypotheses

### 2.1 Scientific Purpose
Recent advances in generative AI and automated decision systems have created severe risks of **automation complacency**, **premature delegation**, and **cognitive attrition**. While organizations and nations frequently deploy subjective digital literacy questionnaires, these instruments fail to capture actual behavioral failure modes when humans interact with highly fluent, plausible, but erroneous AI outputs.

The Human-AI Systemic Readiness Index (HSRI) provides an empirically grounded behavioral benchmark across four core cognitive factors:
1. **Factor 1 ($\\eta_1$): Cognitive Discernment & Fallacy Interception** (detection of subtle domain errors).
2. **Factor 2 ($\\eta_2$): Overload & Default Resistance** (preservation of critical evaluation under cognitive load and machine defaults).
3. **Factor 3 ($\\eta_3$): Autonomous Agency Preservation** (maintenance of supervisory control and independent hypothesis generation).
4. **Factor 4 ($\\eta_4$): Calibrated Epistemic Friction** (Bayesian updating vs cognitive entrenchment and commitment loyalty).

### 2.2 Primary Research Hypotheses
- **$H_1$ (Factorial Structure):** A 4-factor correlated structural equation model will exhibit superior fit to empirical behavioral telemetry compared to a unidimensional model (RMSEA $\\le 0.05$, CFI $\\ge 0.95$, TLI $\\ge 0.95$).
- **$H_2$ (Convergent/Discriminant Validity):** HSRI behavioral tasks will demonstrate robust convergent validity with multi-method diagnostic vignettes ($r > 0.50$) while maintaining discriminant separation ($r < 0.35$).
- **$H_3$ (Incremental Validity — Gating Hypothesis):** HSRI will account for statistically significant incremental variance in real-world human-AI override accuracy beyond standard baseline instruments (CRT-2, AI Literacy, Trust in Automation, Self-Efficacy), achieving $\\Delta R^2 \\ge 0.15$ with $p < .001$.

---

## 3. Participant Population, Recruitment & Sampling

### 3.1 Sample Cohort Size & Statistical Power
- **Target Sample:** $N = 1,080$ adult participants.
- **Power Calculation:** For Confirmatory Factor Analysis with 9 indicators and 4 latent factors (degrees of freedom $\\approx 21$), $N = 1,080$ provides $> 0.99$ statistical power ($\\alpha = 0.01$) to reject models with RMSEA $> 0.05$ (MacCallum, Browne, & Sugawara, 1996). For incremental hierarchical regression ($\\Delta R^2 \\ge 0.15$, 4 added predictors), statistical power exceeds $0.999$.

### 3.2 Inclusion and Exclusion Criteria
- **Inclusion Criteria:**
  - Age $\\ge 18$ years.
  - Fluency in English (sufficient for professional problem-solving scenarios).
  - Normal or corrected-to-normal vision.
  - Access to a desktop/laptop computer with standard web browser and mouse/trackpad.
- **Exclusion Criteria:**
  - Individuals under 18 years of age.
  - Inability to provide informed voluntary consent.
  - Use of automated browser extensions or external unauthorized LLM solvers during task execution.

### 3.3 Recruitment Strategy & Fair Compensation
Participants will be recruited via institutional participant pools and verified research platforms (e.g., Prolific Academic, university research subject pools). 
- **Duration:** Approximately 35–45 minutes per session.
- **Remuneration:** Compensated at an hourly rate equivalent to or exceeding standard living wage standards ($12.00–$15.00/hour equivalent pro-rated), ensuring non-coercive, equitable compensation.

---

## 4. Experimental Procedures & Methodology

Participants complete a standardized digital experimental battery in a randomized block design:
1. **Electronic Informed Consent:** Review of research nature, voluntary participation, and consent acknowledgment.
2. **Baseline Cognitive Instruments:**
   - Cognitive Reflection Test (CRT-2; Thomson & Oppenheimer, 2016).
   - AI Literacy Scale (Ng et al., 2024).
   - Trust in Automated Systems Survey (Jian et al., 2000).
   - General Self-Efficacy Scale (Schwarzer & Jerusalem, 1995).
3. **Standardized Behavioral Battery (EXP-01 through EXP-09):**
   - 9 micro-tasks presenting real-world problem scenarios (legal analysis, clinical diagnostic calibration, multi-threaded systems engineering, quantitative valuation, choice matrices, delegation thresholds, belief updating, and precommitment forcing).
   - Real-time logging of decision choices, override actions, deliberation latencies, revision counts, and epistemic confidence.
4. **Debriefing & Educational Reflection:** Immediate disclosure of study design, explanation of embedded errors, and educational materials.

---

## 5. Assessment of Risks and Justification of Minimal Risk

### 5.1 Minimal Risk Classification
Under 45 CFR 46.102(l), this study poses **no more than minimal risk**. The probability and magnitude of harm or discomfort anticipated are not greater than those ordinarily encountered in daily life during standard computer use or professional knowledge work.
- **Physical Risks:** None.
- **Psychological Risks:** Minimal. Participants may experience mild intellectual challenge or brief surprise upon learning during debriefing that an AI suggestion contained an intentional error. No distress-inducing or traumatic content is used.
- **Economic/Legal Risks:** None. No personal financial decisions or legal advice are involved.

---

## 6. Justification for Benign Deception & Immediate Debriefing

### 6.1 Regulatory Compliance (45 CFR 46.116(f))
To validly measure automated complacency and unprompted fallacy interception, participants are informed that they are working with an AI decision-support system to solve complex problems; however, the precise incidence and placement of intentional errors in the AI advice cannot be revealed in advance. 
Pre-informing participants that "the AI will deliberately mislead you on Task 3" would induce artificial vigilance and invalidate ecological validity, rendering the scientific index useless.

### 6.2 Safeguards and De-Escalation
- Incomplete disclosure is strictly limited to withholding the explicit schedule of intentional AI flaws.
- Incomplete disclosure introduces no physical, psychological, or legal hazards.
- Full debriefing is mandatory immediately upon test battery completion (see Protocol Document 02). Participants are provided with full error rationales and the opportunity to ask questions or strike their data.

---

## 7. Data Confidentiality, Privacy & Zenodo Open Access Plan

- **Cryptographic Anonymization:** No direct identifiers (names, emails, IP addresses, student IDs) are stored with experimental telemetry. Each participant is assigned a cryptographic token (`SUBJ-UUID4`) salted via SHA-256.
- **Storage & Access Controls:** Raw telemetry is stored in encrypted cloud repositories accessible only by authorized investigators.
- **Open Data Deposition:** Fully de-identified aggregate matrices will be deposited in the CERN Zenodo repository under Creative Commons Attribution 4.0 International (CC-BY-4.0) to ensure full scientific reproducibility.

---

## 8. Investigator Assurances

The Principal Investigator certifies that:
1. All procedures comply with the Declaration of Helsinki, US HHS Common Rule (45 CFR 46), and institutional ethics regulations.
2. Participation is strictly voluntary with guaranteed right of withdrawal without penalty.
3. Any adverse event or unexpected problem involving risks to subjects will be reported to the IRB within 48 hours.

**Signed:**  
*Krishnakumar R. M., Principal Investigator*  
*HSRI Scientific Direction*  
*Date of Submission: October 2026*
