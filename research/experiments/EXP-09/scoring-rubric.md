# EXP-09 Scoring Rubric: Cognitive-Forcing-Function Interface Comparison

## Scoring Framework

Each item response is scored on a standardized 3-point ordinal scale (0, 1, 2) based on precommitment retention, independent evidence verification, and resistance to interface-level persuasive cues.

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Deliberative Verification & Robust Precommitment** | Participant maintains their correct independent precommitment despite opposing AI advice, inspects raw sensor/case data rather than relying on superficial interface cues, and rejects explanations lacking substantive evidentiary validity. |
| **1** | **Partial Verification / Hesitant Compliance** | Participant notices discrepancy between raw data and AI advice, but delays decision, reduces confidence, or accepts flawed AI advice with reservations. |
| **0** | **Frictionless Surrender / Heuristic Compliance** | Participant immediately capitulates to flawed AI advice (e.g., reversing bail ruling, approving pneumothorax scan in 3.8s, reopening damaged bridge, or approving loan based on vacuous explanation). |

---

## Domain Guidance by Error Type

### 1. `precommitment_override_failure` (Item 1 — Magistrate Bail Hearing)
- **Score 2:** Maintains independent ruling to grant ROR; articulates that community ties and appearance records refute the AI's 94% flight risk label.
- **Score 1:** Expresses hesitation about the AI's 94% badge, but compromises by setting high monetary bail rather than ROR.
- **Score 0:** Overrides precommitment immediately, ordering custodial detention solely due to the AI confidence score.

### 2. `frictionless_heuristic_surrender` (Item 2 — Radiology Pneumothorax)
- **Score 2:** Conducts thorough independent visual scan ($\ge 15$s); detects the subtle apical pneumothorax pleural line; overrides the AI's "No acute finding".
- **Score 1:** Spends intermediate time scanning and suspects an apex anomaly, but fails to definitively confirm pneumothorax without prompt.
- **Score 0:** Approves the scan in $< 5$s based on the green bounding box, missing the pneumothorax.

### 3. `miscalibrated_confidence_sway` (Item 3 — Bridge Tendon Fatigue)
- **Score 2:** Upholds bridge closure order based on calculated cable elongation; notes that the AI's 99.8% certainty model omitted transverse shear sensors.
- **Score 1:** Questions the 99.8% meter, but downgrades the closure order to a partial lane reduction.
- **Score 0:** Rescinds the closure order based on the 99.8% certainty display, ignoring physical cable elongation data.

### 4. `explanation_placebo_effect` (Item 4 — Credit DSCR Covenant)
- **Score 2:** Rejects loan approval; identifies that the three-page explanation lacks any cash-flow mechanism to service debt at 0.88x DSCR.
- **Score 1:** Notes the low 0.88x DSCR, but assumes the complex mathematical explanation must contain mitigating factors.
- **Score 0:** Approves the loan, citing the comprehensive three-page explanation as proof of creditworthiness.

---

## Interface Deliberation Indicators

- **Reliance Ratio ($RR$):** Ratio of adopting correct advice versus rejecting incorrect advice.
- **Precommitment Loyalty Index:** Percentage of trials where correct precommitment is retained after viewing conflicting AI advice.
- **Cognitive Friction Advantage:** Difference in override accuracy between the forcing-function interface and standard frictionless interface.
