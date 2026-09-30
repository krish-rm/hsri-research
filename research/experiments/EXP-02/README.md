# EXP-02: Fluent Hallucination Detection — Medical Domain

## Purpose
Tests whether individuals can detect factual, logical, dosage, or citation
errors embedded in fluent, authoritative AI-generated clinical text under cognitive automation pressure.

## Target Population
Educated adults without clinical specialist training (patient health literacy level).

## Pilot Status
Stimuli generated. Validation against item discrimination criteria: 3/3 passed.
NOT yet approved for human participant deployment.

## IRB / Ethics Note
⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
ethical review. The agent generates and validates stimuli; it does not deploy them.
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
