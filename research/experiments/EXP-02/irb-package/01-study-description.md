# Study Description & Protocol Narrative (EXP-02)

> **PREVIEW NOTICE: HSRI v0.3.0-dev**
> This research document is an exploratory artifact from the Human Superintelligence Readiness Index (HSRI) behavioral lab pipeline. Synthetic-persona pilots test stimulus behavior only and do not provide evidence about human cognition. Stimuli cleared for IRB submission. Not validated on human participants.

## Protocol Title
Human Discernment Under Cognitive Automation Pressure: Fluent Hallucination Detection in Clinical Documentation (HSRI EXP-02)

## 1. Scientific Background & Rationale
Frontier artificial intelligence applications in healthcare routinely generate fluent, professional clinical summaries, discharge paperwork, and patient advisory instructions. While superficially convincing, large language models (LLMs) can produce subtle factual errors, extreme dosage miscalculations, or illogical therapeutic instructions ("fluent clinical hallucinations").

In high-stakes health contexts, automation bias poses severe risks: individuals frequently defer to authoritative medical jargon and polished typography, bypassing System 2 analytical verification (Goddard et al., 2012; Parasuraman & Riley, 1997). This study investigates lay health literacy and human error discernment when reading AI-generated clinical documentation containing calibrated errors.

## 2. Specific Aims & Hypotheses
- **Aim 1:** Measure baseline error detection rates in fluent AI-generated clinical texts among non-specialist adults.
- **Aim 2:** Quantify whether clinical terminology and authoritative discharge formatting inhibit lay discernment of dangerous errors.
- **Hypothesis 1:** Detection rates will vary significantly across error types: extreme dosage errors and physical impossibilities (e.g. total water avoidance) will show higher initial detection than subtle route-of-administration errors (e.g. eye drops for lung infections).
- **Hypothesis 2:** Faster reading times (low response latency) will correlate with failure to identify clinical errors, reflecting heuristic System 1 acceptance.

## 3. Experimental Design
- **Design Type:** Between-subjects randomized controlled design.
  - **Condition A (Experimental):** Participants review clinical passages labeled as "AI-generated medical documentation drafts" containing calibrated embedded errors.
  - **Condition B (Control / Benchmark):** Participants review identical passages labeled as "clinician-reviewed drafts."
- **Task:** Participants read 3 short clinical summaries (~200–350 words each) and answer:
  1. Reading comprehension check.
  2. Clinical accuracy check: "Does this passage contain any factual, logical, or medication errors? If yes, identify the error and explain why it is problematic."
  3. Subjective confidence rating (1–5 Likert scale).
- **Session Duration:** Approximately 15 minutes via an online secure portal.

## 4. Stimulus Battery Overview
The battery contains three calibrated clinical items:
1. **Item 1 (Factual / Physiological Absurdity):** Post-diverticulitis discharge instructions advising total avoidance of water during antibiotic therapy.
2. **Item 2 (Logical / Route Distortion):** Bronchitis discharge note prescribing topical ophthalmic eye drops to treat a bacterial pulmonary infection.
3. **Item 3 (Extreme Toxic Dosage):** Hypertensive urgency and pneumonia discharge note prescribing Acetaminophen 5,000 mg PO QID PRN (a lethal 20g/day cumulative dose).

Synthetic cohort evaluations indicated that all items passed target discrimination constraints ($D \ge 0.30$). Item 1 is flagged as `CEILING_EFFECT` in synthetic cohorts; its human difficulty remains provisional pending empirical testing.
