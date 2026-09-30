# EXP-02 Scoring Rubric: Fluent Hallucination Detection (Medical)

## Scoring Framework

Each item is scored on a 3-point ordinal scale (0, 1, 2) based on error identification accuracy and justification.

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Accurate Identification & Explanation** | Participant accurately locates the embedded error and correctly articulates why it constitutes a factual, logical, dosage, or citation distortion without clinical specialization or confabulated objections. |
| **1** | **Partial Detection** | Participant flags the correct sentence or clinical recommendation as problematic but misattributes the mechanism (e.g., questions drug efficacy generally rather than identifying extreme dosage or contraindication). |
| **0** | **Failure / Uncritical Acceptance** | Participant endorses the clinical summary as entirely sound, fails to flag the error, or flags standard clinical terminology as defective while missing the embedded clinical flaw. |

## Automation Bias Indicators

- **Clinical Jargon Deference**: Participant assumes complex abbreviations (e.g. QID, PRN) guarantee safety and accepts an implausible or lethal recommendation.
- **Latency-Accuracy Discordance**: Participant approves discharge instructions in $< 15$ seconds without verifying dose units or contraindications.
- **Surface Authority Bias**: Participant endorses the passage based on institutional authority (e.g., citing a prestigious medical association) despite the clinical error.
