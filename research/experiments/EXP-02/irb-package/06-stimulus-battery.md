# Stimulus Battery & Scoring Rubric (EXP-02)

> **PREVIEW NOTICE: HSRI v0.3.0-dev**
> This research document is an exploratory artifact from the Human Superintelligence Readiness Index (HSRI) behavioral lab pipeline. Synthetic-persona pilots test stimulus behavior only and do not provide evidence about human cognition. Stimuli cleared for IRB submission. Not validated on human participants.

This document presents the complete 3-item medical domain stimulus battery and scoring rubric for EXP-02.

---

## Stimulus 1: Diverticulitis Discharge Guidance (Factual Restriction / Physiological Absurdity)

### Stimulus Text Presented to Participant
> "Patient admitted on 10/12 with acute diverticulitis, presenting with left lower quadrant pain, leukocytosis (WBC 15.4), and low-grade fever. CT scan confirmed mild sigmoid diverticulitis without perforation or abscess formation. Managed conservatively with intravenous piperacillin-tazobactam and strict bowel rest for 48 hours, followed by advancement to a clear liquid diet. Pain was adequately controlled with oral oxycodone PRN. Vital signs remained stable throughout the hospitalization, and inflammatory markers normalized by discharge. Patient was instructed to take the remaining course of oral augmentin 875 mg twice daily for 7 days. To ensure complete recovery, the patient was advised to completely avoid drinking any water for the duration of the antibiotic therapy. Discharged home in stable condition on 10/16 with outpatient follow-up scheduled in two weeks."

### Psychometric & Item Metadata
- **Domain:** Medical / Clinical
- **Difficulty Tier:** Medium (Provisional — flagged `CEILING_EFFECT` in synthetic LLM testing; human difficulty pending empirical pilot)
- **Embedded Error Type:** Factual
- **Embedded Error Location:** Paragraph 1, Sentence 7
- **Embedded Error Ground Truth:** The discharge instructions advise the patient to completely avoid drinking any water during oral antibiotic therapy, which is physiologically impossible, clinically hazardous, and directly counter to standard medical guidelines emphasizing hydration during infection recovery.
- **Distractor Features:** Standard clinical language and abbreviations (PRN, WBC, CT scan), specific plausible lab values (WBC 15.4), realistic pharmaceutical names and dosages (piperacillin-tazobactam, oxycodone, augmentin 875 mg twice daily).
- **Target Item Discrimination ($D$):** 0.38 (Synthetic LLM cohort pilot $D = 0.87$, `CEILING_EFFECT`; human empirical discrimination pending)

---

## Stimulus 2: Bronchitis Treatment Route (Logical Inversion / Ophthalmic Misattribution)

### Stimulus Text Presented to Participant
> "Patient Name: Eleanor Vance | DOB: 05/14/1965 | Date of Discharge: 10/24/2023. Diagnosis: Acute Bronchitis and Mild Dehydration. Hospital Course: The patient was admitted following a 4-day history of productive cough, low-grade fever, and generalized fatigue. Chest X-ray revealed clear lung fields with no focal consolidation. Lab results on admission showed sodium at 138 mEq/L, potassium at 4.2 mEq/L, and creatinine at 0.9 mg/dL. The patient was treated with intravenous fluids, nebulizer treatments, and a standard 5-day course of oral azithromycin. Vital signs stabilized over 48 hours. Discharge Medications: 1. Azithromycin 250mg tablets: Take two tablets on day one, then one tablet daily for four days. 2. Ibuprofen 600mg PO QID PRN for fever or body aches. 3. Water-soluble eye drops: Instill one drop into both eyes twice daily to treat the bacterial lung infection. The patient is advised to follow up with her primary care physician in 7 to 10 days and return to the emergency department if shortness of breath recurs."

### Psychometric & Item Metadata
- **Domain:** Medical / Clinical
- **Difficulty Tier:** Medium
- **Embedded Error Type:** Logical
- **Embedded Error Location:** Paragraph 1, Sentence 9 (Discharge Medication #3)
- **Embedded Error Ground Truth:** Prescription of topical ophthalmic eye drops to treat a pulmonary bacterial lung infection. Topical eye drops deliver localized ocular therapy and have zero pharmacological bioavailability in bronchial tissues.
- **Distractor Features:** Standard clinical abbreviations (PO, QID, PRN), normal serum electrolyte lab values (sodium, potassium, creatinine), realistic dosing instructions for oral azithromycin and ibuprofen.
- **Target Item Discrimination ($D$):** 0.38 (Synthetic LLM cohort pilot $D = 0.74$; human empirical discrimination pending)

---

## Stimulus 3: Hypertensive Urgency Discharge (Extreme Toxic Dosage)

### Stimulus Text Presented to Participant
> "Discharge Summary: Patient admitted on 10/12 presenting with acute hypertensive urgency and moderate community-acquired pneumonia. Vital signs at discharge: BP 128/82 mmHg, HR 72 bpm, SpO2 96% on room air. Lab results show WBC count normalized at 7.4 x10^3/uL and serum creatinine stable at 1.0 mg/dL. The patient tolerated oral alimentation well and ambulates independently. Medications prescribed upon discharge include Lisinopril 10 mg PO daily for blood pressure control, Azithromycin 500 mg PO on day one followed by 250 mg daily for four days to complete the pneumonia regimen, and Acetaminophen 5,000 mg PO QID PRN for mild discomfort. Follow-up appointment scheduled with primary care physician in one week."

### Psychometric & Item Metadata
- **Domain:** Medical / Clinical
- **Difficulty Tier:** Medium
- **Embedded Error Type:** Statistical / Dosage
- **Embedded Error Location:** Paragraph 1, Sentence 7
- **Embedded Error Ground Truth:** Prescribing Acetaminophen 5,000 mg PO QID (four times daily) represents a cumulative daily intake of 20,000 mg (20g). The safe maximum daily ceiling for healthy adults is 3,000–4,000 mg. A single 5,000 mg dose and a 20,000 mg daily intake represent severe, life-threatening hepatotoxicity.
- **Distractor Features:** Authentic clinical abbreviations (PO, QID, PRN, BP, HR, SpO2), plausible vital signs and normalized lab values (BP 128/82, HR 72, SpO2 96%, WBC 7.4, creatinine 1.0).
- **Target Item Discrimination ($D$):** 0.38 (Synthetic LLM cohort pilot $D = 0.61$; human empirical discrimination pending)

---

## Scoring Rubric

Participant evaluations are independently scored on an ordinal 3-point scale (0, 1, 2) by two raters blinded to experimental condition (target inter-rater reliability: Cohen's $\kappa \ge 0.85$).

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Accurate Identification & Explanation** | Participant correctly identifies the specific embedded medical error (e.g. noticing the impossible water restriction, the absurd prescription of eye drops for a lung infection, or the extreme toxic acetaminophen dosage) and accurately articulates why it is clinically flawed without relying on confabulated clinical assertions. |
| **1** | **Partial Detection** | Participant flags the correct medication or sentence as suspicious but fails to articulate the specific clinical mechanism (e.g. noting "I wouldn't take that much medicine" without recognizing the 5,000 mg overdose, or feeling uncertain whether water restriction might be legitimate). |
| **0** | **Failure / Uncritical Acceptance** | Participant endorses the clinical summary as entirely sound, overlooks the error, or flags standard clinical abbreviations (e.g. PRN, PO) as defective while accepting the fatal error. |
