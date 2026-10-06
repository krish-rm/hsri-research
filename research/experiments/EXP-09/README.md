# EXP-09: Cognitive-Forcing-Function Interface Comparison

## Purpose
Directly replicates and extends the experimental paradigm of Buçinca, Malaya, and Gajos (2021). Evaluates human
reliance, override accuracy, and cognitive verification depth across three distinct interface interaction modes:
1. **Unassisted Human Judgment (Baseline)**
2. **Standard Frictionless AI Assistance** (instant recommendations and explanations)
3. **Cognitive Forcing Function Interface** (requiring independent human precommitment before unlocking AI advice)

## Target Population
Educated adults evaluating complex domain judgments (e.g., criminal bail risk, emergency radiology, civil engineering inspections, commercial credit underwriting).
- **Exclusion Criteria:** Domain specialists with board-level certification in radiology or civil forensic engineering.

## Task Paradigm & Operational Flow
1. **Interface Randomization:** Participants are randomly assigned to one of three interface conditions:
   - *Baseline Condition:* Evaluates task materials with zero AI assistance.
   - *Standard Frictionless Interface:* AI recommendation and confidence rating are displayed immediately alongside the case file.
   - *Cognitive Forcing Interface:* Participant must formulate, articulate, and commit an independent determination before the AI reveals its output.
2. **The Flawed AI Intervention:** In 25% of trials, the AI provides subtly or blatantly incorrect advice accompanied by high expressed confidence or lengthy pseudo-explanations.
3. **Dependent Outcomes:**
   - **Appropriate Reliance Ratio:** Following AI advice when correct vs. overriding when incorrect.
   - **Precommitment Reversal Rate:** How often participants abandon a correct independent precommitment to follow flawed AI advice.
   - **Verification Latency:** Time spent inspecting raw evidence versus reading machine explanations.
   - **Explanation Placebo Effect:** Acceptance of flawed advice driven by the length/visual density of explanations.

## Battery Status
- **Battery Size:** 4 calibrated stimuli covering all 4 permitted error types (`precommitment_override_failure`, `frictionless_heuristic_surrender`, `miscalibrated_confidence_sway`, `explanation_placebo_effect`).
- **Item Discrimination Target:** $D \in [0.35, 0.40]$ (calibrated between $0.36$ and $0.39$).
- **Epistemic Classification:** Calibrated simulation stimuli for Phase 5 psychometric packaging.
- **Deployment Status:** NOT approved for human participant deployment without independent institutional ethical oversight.

## IRB / Ethics Note
> ⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
> ethical review. The HSRI research infrastructure generates and calibrates stimuli in synthetic and simulated environments;
> it does not autonomously recruit or deploy human subjects. The deployment gate is an independent human institutional review
> board process outside this system.

## Error Type Coverage
The EXP-09 battery covers four critical interface-mediated deliberation failure modes:

| Item | File | Error Type | Decision Domain | Deliberation Breakdown Mechanism |
|---|---|---|---|---|
| Item 1 | `stimuli-2026-10-06.jsonl` | `precommitment_override_failure` | Pre-Trial Bail Risk Assessment | Overrides correct precommitment to grant bail upon viewing 94% confidence detention badge |
| Item 2 | `stimuli-2026-10-06.jsonl` | `frictionless_heuristic_surrender` | Emergency Chest Radiograph Triage | Frictionless bounding box induces 3.8s scan time, missing apical pneumothorax |
| Item 3 | `stimuli-2026-10-06.jsonl` | `miscalibrated_confidence_sway` | Bridge Cable Tendon Inspection | Reverses bridge closure order due to 99.8% AI certainty meter ignoring shear sensors |
| Item 4 | `stimuli-2026-10-06.jsonl` | `explanation_placebo_effect` | Commercial Credit Default Underwriting | Approves loan violating 1.25x DSCR covenant because AI produced a three-page vacuous explanation |

## Stimulus Format
Each stimulus is stored as a JSONL entry with standardized fields:
- `stimulus_text`: The full decision scenario and interface trace description (minimum 350 characters)
- `embedded_error_type`: One of `precommitment_override_failure`, `frictionless_heuristic_surrender`, `miscalibrated_confidence_sway`, `explanation_placebo_effect`
- `embedded_error_location`: Sentence-level coordinate of the deliberation breakdown
- `embedded_error_description`: Ground-truth specification of the interface breakdown
- `correct_detection_response`: Expected participant override and deliberation preservation response
- `distractor_features`: 99%+ animated confidence meters, instant green boxes, and dense mathematical explanations
- `difficulty_rationale`: Cognitive friction vs heuristic surrender justification
- `item_discrimination_estimate`: Projected point-biserial discrimination coefficient ($0.25 \le D \le 0.60$)
- `experiment_id`: `EXP-09`
- `difficulty`: `medium`

## Scoring Rubric
See [scoring-rubric.md](scoring-rubric.md) for full 3-point ordinal scoring criteria.
