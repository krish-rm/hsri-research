# EXP-01: Fluent Hallucination Detection — Legal Domain

## Purpose
Tests whether individuals can detect factual, logical, citation, or statistical
errors embedded in fluent, authoritative AI-generated legal text under cognitive automation pressure.

## Target Population
Educated adults without legal specialist training.

## Pilot Status
Stimuli generated. Constraint checks against item discrimination targets: 3/3 passed (synthetic cohort estimate; not human validation).
NOT yet approved for human participant deployment.

## IRB / Ethics Note
⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
ethical review. The agent generates stimuli; it does not deploy them.
The deployment gate is a human institutional review process outside this system.

## Stimulus Format
Each stimulus is a JSONL entry with fields documented in `data-dictionary.md`:
- `stimulus_text`: The full legal brief or case analysis passage
- `embedded_error_type`: One of `factual`, `logical`, `citation`, `statistical`
- `embedded_error_location`: Sentence-level coordinate of the embedded distortion
- `embedded_error_description`: Ground truth error definition for scoring
- `correct_detection_response`: Expected participant detection criteria
- `distractor_features`: Authoritative formatting and procedural distractions
- `difficulty_rationale`: Item design and psychometric justification
- `item_discrimination_estimate`: Projected point-biserial discrimination coefficient (target: 0.25–0.60)

## Scoring Rubric
[see scoring-rubric.md](scoring-rubric.md)
