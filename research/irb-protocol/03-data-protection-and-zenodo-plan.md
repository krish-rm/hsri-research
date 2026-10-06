# Data Protection, Anonymization, and Zenodo Open Science Plan

> **Protocol ID:** HSRI-IRB-2026-088  
> **Document Type:** Data Management & Open Science Protocol  
> **Compliance:** FAIR Data Principles (Findable, Accessible, Interoperable, Reusable), GDPR, Common Rule  
> **Repository:** CERN Zenodo Open Data Archive  
> **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  
> **Version:** 1.0.0  

---

## 1. Data Management Philosophy & Open Science Commitment

The HSRI research program adheres to the highest standards of **Open Science** and **reproducible psychometrics**. To ensure that findings are independently verifiable by the global scientific community, all anonymized validation datasets, statistical processing scripts, factor score matrices, and analysis pipelines are scheduled for permanent open-access deposition in the **CERN Zenodo** repository.

---

## 2. Privacy Safeguards and Cryptographic De-Identification

### 2.1 Zero Personally Identifiable Information (PII) Intake
The research platform is architected with strict Zero-PII principles:
- **No Name or Email:** No participant names, emails, telephone numbers, or physical addresses are recorded.
- **IP Address Stripping:** Incoming IP addresses are discarded at the edge reverse proxy and never logged to analytical storage.
- **Browser Fingerprints Discarded:** Standard browser user-agent strings are generalized into coarse categorical buckets (e.g., `Desktop-Blink`, `Desktop-Gecko`) to prevent device fingerprinting.

### 2.2 Cryptographic Subject Tokenization Pipeline
```
Raw Platform Intake
       │
       ▼
Salted SHA-256 Token Engine [ salt: 256-bit cryptographically secure random ]
       │
       ▼
`SUBJ-` + First 12 Hex Characters (e.g., SUBJ-7F2A09B4E1C3)
       │
       ▼
Behavioral Telemetry Store (Zero Direct Identifiers)
```

The hashing salt is maintained in volatile memory during collection and securely rotated. It is impossible to reverse-engineer platform IDs from the public research tokens.

---

## 3. Data Structure and Telemetry Payload

The public open-access release will contain four tabular datasets:

### 3.1 Dataset 1: Baseline Demographics & Survey Scales (`hsri_cohort_demographics.csv`)
- `subject_id`: Salted subject token.
- `age_bracket`: Coarse 10-year brackets (e.g., `18-24`, `25-34`, `35-44`, `45-54`, `55+`).
- `education_level`: Highest educational tier achieved.
- `domain_background`: Broad career field (`STEM`, `Law`, `Healthcare`, `Finance`, `Humanities`, `Other`).
- `crt2_composite_score`: Cognitive Reflection Test composite score (0–4).
- `ai_literacy_mean`: Mean rating across AI Literacy subscales.
- `trust_automation_score`: Standardized Trust in Automated Systems rating.
- `self_efficacy_score`: General Self-Efficacy composite score.

### 3.2 Dataset 2: Behavioral Task Telemetry (`hsri_task_telemetry.csv`)
- `subject_id`: Salted subject token.
- `task_id`: `EXP-01` through `EXP-09`.
- `condition`: Assigned experimental variant or interface condition.
- `selection_choice`: Final option selected.
- `is_override`: Binary flag indicating override of erroneous AI recommendation.
- `override_accuracy`: 1 if correct override, 0 otherwise.
- `latency_ms`: Total response time in milliseconds.
- `first_interaction_latency_ms`: Time to initial inspection or interaction.
- `revision_count`: Number of times participant altered their tentative answer.

### 3.3 Dataset 3: Latent Factor Scores (`hsri_factor_scores.csv`)
- `subject_id`: Salted subject token.
- `eta_1_discernment`: Standardized factor score for Cognitive Discernment.
- `eta_2_default_resistance`: Standardized factor score for Default Resistance.
- `eta_3_agency_preservation`: Standardized factor score for Agency Preservation.
- `eta_4_epistemic_friction`: Standardized factor score for Epistemic Friction.
- `general_hsri_score`: Overall composite HSRI Index.

### 3.4 Dataset 4: Correlation & MTMM Matrices (`hsri_mtmm_matrix.json`)
- Complete variance-covariance matrices, item difficulty ($\\beta$), discrimination ($\\alpha$), and cross-method correlation coefficients.

---

## 4. CERN Zenodo Deposition Architecture

### 4.1 Metadata & Identifier Specification
- **Title:** "Human-AI Systemic Readiness Index (HSRI) Phase 6 Psychometric Validation Cohort Telemetry (N=1,080)"
- **Persistent Identifier:** Digital Object Identifier (DOI) via Zenodo minting (e.g., `10.5281/zenodo.xxxxxxx`).
- **Creator:** Human-AI Systemic Readiness Initiative (HSRI Research Consortium).
- **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0).
- **Keywords:** `human-ai-readiness`, `psychometrics`, `incremental-validity`, `automation-bias`, `ai-safety`, `cognitive-discernment`, `agency`.

### 4.2 Automated Ingestion & Release Pipeline
Validation artifacts are packaged using the repository build system:
```bash
python scripts/psychometric_validator.py --n 1080 --output research/psychometrics/phase-6-validation-report.md
```
The resulting datasets are archived with cryptographic SHA-256 checksums in `zenodo_deposit_checksums.txt` prior to automated API upload.

---

## 5. Compliance Verification Checklist

- [x] **GDPR Article 89 Compliance:** Data processed exclusively for scientific research purposes under robust cryptographic pseudonymization and anonymization safeguards.
- [x] **US HHS 45 CFR 46:** Meets all requirements for public release of minimal-risk, fully de-identified human subjects behavioral data.
- [x] **FAIR Principles:** Complete metadata dictionaries, JSON-LD schemas, and standard CSV formats provided to guarantee interoperability and immediate reusability.
