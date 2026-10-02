# EXP-03: Fluent Hallucination Detection — Technical/Code Domain

## Purpose
Tests whether individuals can detect factual, logical, API misuse, or security
errors embedded in fluent, authoritative AI-generated code explanations, API documentation
excerpts, or technical specifications under cognitive automation pressure.

## Target Population
Technically literate adults without deep specialist software engineering or cybersecurity expertise
(e.g., product managers, data analysts, technical operations personnel, technology journalists).

## Pilot Status
- **Battery Size:** 5 stimuli across 4 error types (`factual`, `logical`, `api_misuse`, `security`).
- **Synthetic Cohort Pilot (Sprint 11):** Completed (N=5 responses per persona across LOW, MEDIUM, and HIGH reflection personas).
- **Discrimination:** $D \in [0.67, 1.00]$ (all items pass $D \ge 0.30$ constraint threshold; ceiling effects detected across upper reflection personas).
- **Epistemic Classification:** Stimuli cleared for IRB packaging. Synthetic persona pilots are stimulus behavior checks only and never constitute evidence about human participants (Rule 12).
- **Deployment Status:** NOT approved for human participant deployment.

## IRB / Ethics Note
⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
ethical review. The agent generates and pilots stimuli synthetically; it does not deploy them.
The deployment gate is a human institutional review process outside this system.

## Error Type Coverage
The EXP-03 battery covers all four permitted error types:

| Item | File | Error Type | Embedded Distortion | Doc Reference |
|---|---|---|---|---|
| Item 1 | `stimuli-2026-09-30.jsonl` | `factual` | Local storage claimed as standard secure practice for JWTs | RFC 7519 / OWASP XSS Prevention |
| Item 2 | `stimuli-2026-09-30.jsonl` | `logical` | Local storage token storage contradicts robust session security | OWASP HTML5 Security Cheat Sheet |
| Item 3 | `stimuli-2026-09-30.jsonl` | `factual` | HMAC signature claimed to encrypt rather than sign JWT payload | RFC 7519 / RFC 7515 (JWS) |
| Item 4 | `stimuli-2026-10-01.jsonl` | `api_misuse` | Omitting `requests.get()` timeout claimed to apply 10s default | [Requests Documentation](https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts) |
| Item 5 | `stimuli-2026-10-01.jsonl` | `security` | Python standard `random` claimed cryptographically secure for MFA | [Python random Documentation](https://docs.python.org/3/library/random.html) |

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
- `documentation_url`: Official authoritative technical documentation URL verifying ground truth (required for Sprint 11+ additions)

## Scoring Rubric
[see scoring-rubric.md](scoring-rubric.md)
