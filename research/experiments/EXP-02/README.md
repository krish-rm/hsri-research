# EXP-02: Fluent Hallucination Detection — Medical Domain

## Purpose
Tests whether individuals can detect factual, logical, dosage, or citation
errors embedded in fluent, authoritative AI-generated clinical text under cognitive automation pressure.

## Target Population
Educated adults without clinical specialist training (patient health literacy level).

## Pilot Status
- **Battery Size:** 3 stimuli in `research/experiments/EXP-02/stimuli-2026-09-30.jsonl`
- **Synthetic Cohort Pilot:** Completed (N=5 responses per persona across LOW, MEDIUM, HIGH reflection personas)
- **Discrimination:** $D \in [0.61, 0.87]$ (all items pass $D \ge 0.30$ constraint threshold; `stimulus_id: 1` flagged for ceiling effect)
- **Epistemic Classification:** Stimuli cleared for IRB submission. Synthetic persona pilots are stimulus behavior checks only and never constitute evidence about human participants (Rule 12).
- **Deployment Status:** NOT approved for human participant deployment.

## Active Stimulus Battery (Rule 19 Compliant)

| Stimulus ID | First 80 Characters of Stimulus Text | Error Type | Pilot D | Discrimination Status |
|---|---|---|---|---|
| `stimulus_id: 1` (`EXP-02-S1`) | `Patient admitted on 10/12 with acute diverticulitis, presenting with left lower ` | `factual` (water avoidance) | 0.87 | PASS (`FLAG: CEILING_EFFECT`) |
| `stimulus_id: 2` (`EXP-02-S2`) | `Patient Name: Eleanor Vance \| DOB: 05/14/1965 \| Date of Discharge: 10/24/2023. Diag` | `logical` (eye drops for lungs) | 0.74 | PASS |
| `stimulus_id: 3` (`EXP-02-S3`) | `Discharge Summary: Patient admitted on 10/12 presenting with acute hypertensive u` | `statistical` (5,000mg acetaminophen) | 0.61 | PASS |


## IRB / Ethics Note
⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
ethical review. The agent generates stimuli; it does not deploy them.
The deployment gate is a human institutional review process outside this system.

## Stimulus Format
Each stimulus is a JSONL entry with fields documented in `data-dictionary.md`:
- `stimulus_text`: The full clinical summary, case report, or guideline excerpt
- `embedded_error_type`: One of `factual`, `logical`, `dosage`, `citation`
- `embedded_error_location`: Sentence-level coordinate of the embedded clinical distortion
- `embedded_error_description`: Ground truth error definition for scoring
- `correct_detection_response`: Expected participant detection criteria
- `distractor_features`: Clinical terminology, lab values, and procedural distractions
- `difficulty_rationale`: Item design and psychometric justification
- `item_discrimination_estimate`: Projected point-biserial discrimination coefficient (target: 0.25–0.60)

## Scoring Rubric
[see scoring-rubric.md](scoring-rubric.md)
