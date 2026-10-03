# Risk Assessment & Participant Protection Plan (EXP-02)

> **PREVIEW NOTICE: HSRI v0.3.0-dev**
> This research document is an exploratory artifact from the Human Superintelligence Readiness Index (HSRI) behavioral lab pipeline. Synthetic-persona pilots test stimulus behavior only and do not provide evidence about human cognition. Stimuli cleared for IRB submission. Not validated on human participants.

## 1. Risk Classification
**Investigator's proposed risk classification: minimal risk (subject to formal IRB determination).**

Under 45 CFR 46.102(l), minimal risk is defined as the probability and magnitude of harm or discomfort anticipated in the research not being greater in and of themselves than those ordinarily encountered in daily life or during the performance of routine physical or psychological examinations or tests.

## 2. Specific Medical Domain Risk Analysis (Rule 19 Compliant)
Unlike abstract cognitive experiments, EXP-02 utilizes clinical discharge scenarios containing deliberately embedded medical inaccuracies:
1. **Hazardous Hydration Restriction (`stimulus_id: 1` / `EXP-02-S1`):**  
   *Text prefix (first 80 chars):* `"Patient admitted on 10/12 with acute diverticulitis, presenting with left lower "`  
   *Risk:* Advises total avoidance of drinking water during an oral antibiotic course for acute diverticulitis, introducing severe acute dehydration and nephrotoxicity risks if misconstrued as real medical guidance.
2. **Ineffective Therapeutic Route (`stimulus_id: 2` / `EXP-02-S2`):**  
   *Text prefix (first 80 chars):* `"Patient Name: Eleanor Vance | DOB: 05/14/1965 | Date of Discharge: 10/24/2023. Diag"`  
   *Risk:* Prescribes topical ophthalmic eye drops to treat a pulmonary bacterial lung infection (acute bronchitis).
3. **Severe Medication Overdose (`stimulus_id: 3` / `EXP-02-S3`):**  
   *Text prefix (first 80 chars):* `"Discharge Summary: Patient admitted on 10/12 presenting with acute hypertensive u"`  
   *Risk:* Prescribes Acetaminophen 5,000 mg PO QID PRN (cumulative daily intake: 20,000 mg), far exceeding the established safe adult ceiling of 3,000–4,000 mg/day and capable of causing acute hepatic necrosis and fatal liver failure.

### Primary Risk Mechanism
The core hazard is that a participant uncritically internalizes, retains, or subsequently acts upon a simulated medical error in their own life or advises a family member based on false clinical assertions encountered during the study.

## 3. Mandatory Risk Mitigations
To reduce risk to minimal levels, the study protocol enforces four mandatory procedural safeguards:

1. **Persistent On-Screen Research Banner:**  
   Every presentation screen maintains a prominent, unclosable header banner:  
   > *"SIMULATED RESEARCH PASSAGE: Text generated for artificial intelligence accuracy evaluation. NOT valid medical advice or clinical guidance. Do not use for health decisions."*

2. **No Personalized Medical Advice:**  
   The experimental instrument prohibits personalized query responses. All stimulus texts are third-party hypothetical patient discharge notes without relevance to the participant's individual health history.

3. **Immediate Mandatory Debriefing:**  
   Immediately following the reading session, participants cannot exit without viewing a structured debriefing page that explicitly highlights each error, explains why it is clinically dangerous, provides the established medical facts, and includes verified clinical guidelines.

4. **Clinical Consultation Injunction:**  
   The debriefing provides an explicit injunction directing participants to consult licensed healthcare providers for any personal medical decisions.

## 4. Incomplete Disclosure Rationale
Participants are informed they are evaluating "AI-generated clinical documentation for clarity and quality." They are not told in advance which specific sentences contain embedded clinical errors. Advance disclosure would induce artificial demand characteristics, preventing valid scientific measurement of naturalistic cognitive automation bias. Immediate debriefing ensures full transparency.

## 5. Data Confidentiality & Encryption
Responses are completely anonymous. No protected health information (PHI) or personally identifiable information (PII) is gathered. Data transmission is secured using TLS 1.3 encryption, and data at rest is encrypted with AES-256 on institutional servers.
