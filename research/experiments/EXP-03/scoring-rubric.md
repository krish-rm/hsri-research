# EXP-03 Scoring Rubric: Fluent Hallucination Detection (Technical/Code)

## Scoring Framework

Each item is scored on a 3-point ordinal scale (0, 1, 2) based on error identification accuracy and justification.

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Accurate Identification & Explanation** | Participant accurately locates the embedded error and correctly articulates why it constitutes a factual, logical, API misuse, or security vulnerability without requiring language-specific compiler expertise or confabulated assertions. |
| **1** | **Partial Detection** | Participant flags the correct sentence or technical recommendation as problematic but misattributes the mechanism (e.g., questions performance overhead rather than identifying security exposure or inverted logic). |
| **0** | **Failure / Uncritical Acceptance** | Participant endorses the technical specification as entirely sound, fails to flag the error, or flags standard architectural terminology as defective while missing the embedded vulnerability or logical inversion. |

## Automation Bias Indicators

- **Technical Jargon Deference**: Participant assumes complex systems jargon (e.g., HMAC-SHA256, token bucket, Kubernetes service mesh) guarantees correctness and accepts an insecure configuration or inverted logic.
- **Syntax Plausibility Bias**: Participant approves an API specification or code snippet because surrounding syntax and parameters appear valid, overlooking fundamental security flaws.
- **Fast Verification Blindness**: Participant accepts an architecture design in $< 15$ seconds without tracing data flow, variable state, or access authorization.
