# Study Description & Protocol Narrative

## Protocol Title
Human Discernment Under Cognitive Automation Pressure: Fluent Hallucination Detection in Legal Documentation (HSRI EXP-01)

## 1. Scientific Background & Rationale
Large language models (LLMs) produce fluent, grammatically flawless, and rhetorically authoritative prose that frequently contains subtle factual inaccuracies, logical inversions, or fabricated citations ("fluent hallucinations"). Research in human-automation interaction indicates that individuals exhibit strong automation bias—systematically defaulting to System 1 heuristic acceptance when machine outputs appear fluent and authoritative, rather than engaging System 2 deliberative scrutiny (Kahneman, 2011; Parasuraman & Riley, 1997; Goddard et al., 2012).

The Human Superintelligence Readiness Index (HSRI) behavioral lab seeks to empirically evaluate human discernment capacity under simulated AI automation pressure. Experiment 1 (EXP-01) targets the legal domain, testing whether educated lay adults can identify calibrated legal errors embedded in fluent judicial summaries and briefs.

## 2. Specific Aims & Hypotheses
- **Aim 1:** Measure baseline error detection rates in fluent AI-generated text among non-specialist adults.
- **Aim 2:** Quantify the magnitude of automation bias induced by authoritative legal framing and terminology.
- **Hypothesis 1:** Error detection rates will be significantly depressed by authoritative distraction features (d ≥ 0.35) relative to non-authoritative baselines.
- **Hypothesis 2:** Participant response latencies will correlate positively with detection accuracy, indicating that fast processing correlates with uncritical acceptance.

## 3. Experimental Design
- **Design Type:** Between-subjects randomized control design.
  - **Condition A (Experimental):** Participants evaluate text passages presented as "AI-generated drafts" containing calibrated embedded errors.
  - **Condition B (Control / Benchmark):** Participants evaluate identical text passages framed as "peer-reviewed drafts."
- **Task:** Participants read 3 short passages (350–500 words each) and answer:
  1. Comprehension check questions.
  2. Quality and accuracy assessment: "Does this passage contain any factual, logical, citation, or statistical errors? If yes, please identify the error and explain why it is incorrect."
  3. Confidence rating (1–5 Likert scale).
- **Duration:** Estimated completion time is approximately 15 minutes.

## 4. Stimuli Overview
The stimulus battery comprises three calibrated legal domain passages:
1. **Item 1 (Logical Error):** Inverted liability waiver principle asserting that an exculpatory waiver can absolve liability for gross negligence.
2. **Item 2 (Factual Error):** False attribution of common carrier duty of care to the 14th Amendment of the U.S. Constitution rather than state common law.
3. **Item 3 (Citation Error):** Fabricated attribution of municipal zoning and qualified immunity doctrine to *Brown v. Board of Education* (1954).

All stimuli underwent synthetic LLM persona cohort testing, meeting item design constraint checks ($D \ge 0.72$ in synthetic testing; human validation pending). Synthetic-persona pilots test stimulus behavior only and do not provide evidence about human cognition.
