# Participant Debriefing Form & Script

> **PREVIEW NOTICE: HSRI v0.3.0-dev**
> This research document is an exploratory artifact from the Human Superintelligence Readiness Index (HSRI) behavioral lab pipeline. Synthetic-persona pilots test stimulus behavior only and do not provide evidence about human cognition. Stimuli cleared for IRB submission. Not validated on human participants.

## Study Title
Human Discernment Under Cognitive Automation Pressure: Fluent Hallucination Detection in Clinical and Medical Advice (HSRI EXP-02)

---

## 1. Full Explanation of Study Purpose
Thank you for participating in this research study!

When you enrolled, you were informed that you would evaluate "AI-generated informational documents for clarity, tone, and quality." We would now like to provide a full and comprehensive explanation of the true study objectives, design, and scientific goals.

### The Phenomenon Under Investigation: Automation Bias & Medical Hallucinations
This experiment investigates **clinical automation bias**—the human cognitive vulnerability wherein individuals uncritically trust and accept advice produced by fluent, authoritative artificial intelligence models, even when that advice contains dangerous medical misinformation, contraindicated treatments, or severe dosage errors.

In order to rigorously measure human discernment under cognitive automation pressure, our research team embedded one specific, calibrated factual distortion into each of the clinical discharge summaries you reviewed.

---

## 2. Incomplete Disclosure and Deception Rationale
### Why Incomplete Disclosure Was Necessary
To observe natural cognitive discernment and evaluate baseline scrutiny without artificial cueing, participants could not be warned in advance that specific medical errors were intentionally embedded in the texts. Forewarning participants would induce an artificial proofreading posture ("demand characteristics"), rendering it impossible to measure how real users interact with fluent AI health advice in everyday contexts.

---

## 3. Explicit Medical Corrections for All Study Stimuli

> **CRITICAL MEDICAL DISCLAIMER & INJUNCTION**
> The passages presented during this study contained **deliberately fabricated and medically dangerous errors** designed solely for experimental testing. 
> **NONE of the medical advice, dosages, or treatment recommendations presented in the experimental stimuli should ever be used or relied upon in real life.** 
> If you have questions about your personal health, medications, or any medical condition, **always consult a qualified, licensed healthcare professional or clinician.**

Below are the exact clinical corrections for the active stimulus battery (`research/experiments/EXP-02/stimuli-2026-09-30.jsonl`):

### Stimulus 1: Diverticulitis Discharge Guidance (Total Water Avoidance)
* **What the Stimulus Stated:** The discharge summary instructed the patient: *"To ensure complete recovery, the patient was advised to completely avoid drinking any water for the duration of the antibiotic therapy."*
* **The Accurate Medical Fact [CLINICAL REVIEW REQUIRED]:**
  - Completely withholding or avoiding water while undergoing oral antibiotic therapy for acute diverticulitis is physiologically hazardous, absurd, and directly counter to established medical practice.
  - Patients recovering from infection and taking systemic antimicrobials (such as amoxicillin-clavulanate / Augmentin) require adequate fluid intake to maintain normal intravascular volume, facilitate drug absorption and renal excretion, prevent crystalluria, and avoid prerenal acute kidney injury.
  - Hydration should **never** be restricted unless specifically managed in a hospital setting under strict fluid restriction protocols (e.g. end-stage renal disease or severe decompensated heart failure).

### Stimulus 2: Acute Bronchitis Discharge Guidance (Ophthalmic Route for Lung Infection)
* **What the Stimulus Stated:** Under discharge medications for acute bronchitis, the summary prescribed: *"Water-soluble eye drops: Instill one drop into both eyes twice daily to treat the bacterial lung infection."*
* **The Accurate Medical Fact [CLINICAL REVIEW REQUIRED]:**
  - Ophthalmic eye drops are formulated exclusively for localized ocular administration (cornea, conjunctiva, anterior chamber). They possess virtually **zero systemic or pulmonary bioavailability** and cannot reach or treat a lower respiratory tract infection.
  - Bacterial respiratory infections require systemic antimicrobial therapy (such as oral or intravenous antibiotics) or specialized pulmonary aerosolization via nebulizer. Prescribing eye drops for a lung infection is a severe anatomical and pharmacological error.

### Stimulus 3: Hypertensive Urgency / Pneumonia Discharge (Lethal Acetaminophen Overdose)
* **What the Stimulus Stated:** The discharge summary prescribed: *"Acetaminophen 5,000 mg PO QID PRN for mild discomfort."*
* **The Accurate Medical Fact [CLINICAL REVIEW REQUIRED]:**
  - Prescribing **5,000 mg QID** (four times daily) directs the patient to ingest **20,000 mg (20 grams) of acetaminophen daily**.
  - The maximum safe adult daily dose of acetaminophen from **all sources combined is 4,000 mg per 24 hours** (and many clinical guidelines recommend capping at 3,000 mg/day for chronic use, older adults, or those with mild hepatic impairment).
  - An acute single dose of 5,000 mg, or a daily cumulative dose of 20,000 mg, is a **severe, life-threatening overdose** that causes acute centrilobular liver necrosis, fulminant hepatic failure, metabolic acidosis, and death unless treated promptly with intravenous N-acetylcysteine. Standard adult therapeutic dosing is 500 mg to 1,000 mg every 4 to 6 hours as needed, never exceeding 4,000 mg in 24 hours.

---

## 4. Supplementary Debriefing: Alternative / Candidate Stimulus Items

For complete institutional transparency, the following corrections cover candidate and fallback stimuli generated in the HSRI stimulus framework:

### Candidate Item A: Penicillin Anaphylaxis & Ampicillin Cross-Reactivity
* **Hypothetical Error:** Prescribing intravenous ampicillin to a patient with a documented history of life-threatening anaphylactic allergy to penicillin (prior ICU admission for bronchospasm and angioedema).
* **The Accurate Medical Fact [CLINICAL REVIEW REQUIRED]:**
  - Ampicillin is an aminopenicillin belonging to the beta-lactam class. It shares the identical beta-lactam ring core and cross-allergenicity with penicillin.
  - Administering ampicillin to a patient with known IgE-mediated anaphylaxis to penicillin is **strictly contraindicated** and presents an immediate risk of fatal anaphylactic shock. Clinicians must select non-cross-reactive alternatives (e.g. fluoroquinolones, macrolides, or glycopeptides depending on the pathogen).

### Candidate Item B: Pediatric Asthma Clinical Guideline Authority
* **Hypothetical Error:** Citing the American Heart Association (AHA) Advanced Cardiovascular Life Support (ACLS) guidelines as the primary clinical authority for pediatric asthma bronchodilator dosing intervals.
* **The Accurate Medical Fact [CLINICAL REVIEW REQUIRED]:**
  - The American Heart Association (AHA) establishes guidelines for cardiovascular resuscitation and cardiovascular emergencies (e.g. PALS, ACLS), not chronic or acute outpatient pulmonary disease management.
  - Pediatric asthma bronchodilator protocols are governed by respiratory and pediatric authorities, specifically the **Global Initiative for Asthma (GINA)**, the **National Asthma Education and Prevention Program (NAEPP / EPR-3 & 2020 Focused Updates)**, and the **American Academy of Pediatrics (AAP)**.

---

## 5. Participant Reassurance & Educational Support
Please note that your performance on this evaluation is **not** an evaluation of your intelligence, general medical literacy, or competence. The stimuli were specifically crafted with sophisticated rhetorical framing and authoritative clinical prose to simulate the persuasive fluency of state-of-the-art large language models. Research demonstrates that even highly educated individuals are susceptible to automation bias when reading syntactically fluent synthetic prose.

---

## 6. Contact Information & Data Withdrawal
If you experience any distress, have questions regarding your participation, or wish to withdraw your data from the research registry following this debriefing, please contact the study team or the oversight review board:

* **Principal Investigator:** [Investigator Name, Credentials Pending Affiliation]
* **Study Email:** `[study-contact@institution.edu]`
* **Institutional Review Board:** `[irb-contact@institution.edu]`

Thank you again for your vital contribution to artificial intelligence safety and human-AI interaction research.
