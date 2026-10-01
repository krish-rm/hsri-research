# EXP-03: Fluent Hallucination Detection — Technical/Code Domain

## Purpose
Tests whether individuals can detect factual, logical, API misuse, or security
errors embedded in fluent, authoritative AI-generated code explanations, API documentation
excerpts, or technical specifications under cognitive automation pressure.

## Target Population
Technically literate adults without deep specialist software engineering or cybersecurity expertise
(e.g., product managers, data analysts, technical operations personnel, technology journalists).

## Pilot Status
Stimuli generated. Constraint checks against item discrimination targets: 3/3 passed (synthetic/generator estimate; not human validation).
NOT approved for human participant deployment.

## IRB / Ethics Note
⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
ethical review. The agent generates stimuli; it does not deploy them.
The deployment gate is a human institutional review process outside this system.

## Error Type Coverage Gap (Sprint 11 Candidate)
The stimulus generator specification for EXP-03 permits four error types: `factual`, `logical`, `api_misuse`, and `security`. The current 3-item pilot battery (`stimuli-2026-09-30.jsonl`) contains two `factual` items and one `logical` item (focusing on token storage security anti-patterns and signature/encryption confusion). The battery currently contains neither a dedicated `api_misuse` item nor a dedicated `security` item. Expanding the stimulus pool to include dedicated `api_misuse` and `security` items is queued as a candidate deliverable for Sprint 11.

## Stimulus Format
Each stimulus is a JSONL entry with fields documented in `data-dictionary.md`:
- `stimulus_text`: The full technical specification, API reference, or code explanation excerpt
- `embedded_error_type`: One of `factual`, `logical`, `api_misuse`, `security`
- `embedded_error_location`: Sentence-level coordinate of the embedded technical distortion
- `embedded_error_description`: Ground truth error definition for scoring
- `correct_detection_response`: Expected participant detection criteria
- `distractor_features`: Code syntax, technical terminology, and architectural framing distractions
- `difficulty_rationale`: Item design and psychometric justification
- `item_discrimination_estimate`: Projected point-biserial discrimination coefficient (target: 0.25–0.60)

## Scoring Rubric
[see scoring-rubric.md](scoring-rubric.md)
