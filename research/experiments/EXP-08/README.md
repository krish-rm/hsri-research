# EXP-08: Demonstrated Machine Superiority & Agency Preservation

## Purpose
Tests whether human decision-makers preserve cognitive initiative, independent hypothesis generation,
and psychological agency after being visibly outperformed by an advanced AI system across difficult benchmark
tasks. Specifically evaluates susceptibility to **Self-Efficacy Collapse**, **Silent-Machine Paralysis**,
and **Uncritical Domain Transference**.

## Target Population
Adults with general technical, tactical, or organizational problem-solving experience (e.g., intelligence analysts,
emergency managers, systems engineers, clinical supervisors, graduate students).
- **Exclusion Criteria:** Extreme novices with zero comfort in technical decision-making simulations.

## Task Paradigm & Operational Flow
1. **Phase I (Demonstrated Asymmetry Induction):** The participant and AI agent complete ten difficult diagnostic or forecasting tasks. The AI visibly achieves superior accuracy (e.g., 96% vs. 54%), establishing capability asymmetry.
2. **Phase II (Collaborative Problem Solving):** The dyad transitions to a novel, high-stakes operational problem requiring joint human-AI synthesis.
3. **Phase III (Experimental Probes):**
   - **Silent Machine Probe:** The AI interface displays "Confidence: NULL. Machine silent." Does the human formulate autonomous hypotheses?
   - **Normative Transference Probe:** The AI extends its perceptual superiority to propose cold ethical/normative tradeoffs. Does the human defer or assert human bioethical agency?
   - **Counter-Hypothesis Probe:** The human discovers contrary empirical telemetry. Does the human propose dissent or defer to machine credentials?
4. **Dependent Outcomes:**
   - Independent Hypothesis Generation Rate (number and depth of proposed alternatives).
   - Latency to Action during Machine Silence.
   - Moral Agency Preservation Score (rejection of invalid normative machine optimization).
   - Dissent Assertiveness Score.

## Battery Status
- **Battery Size:** 4 calibrated stimuli covering all 4 permitted error types (`self_efficacy_surrender`, `silent_machine_paralysis`, `uncritical_asymmetry_deference`, `counter_hypothesis_suppression`).
- **Item Discrimination Target:** $D \in [0.35, 0.40]$ (calibrated between $0.36$ and $0.39$).
- **Epistemic Classification:** Calibrated simulation stimuli for Phase 5 psychometric packaging.
- **Deployment Status:** NOT approved for human participant deployment without independent institutional ethical oversight.

## IRB / Ethics Note
> ⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
> ethical review. The HSRI research infrastructure generates and calibrates stimuli in synthetic and simulated environments;
> it does not autonomously recruit or deploy human subjects. The deployment gate is an independent human institutional review
> board process outside this system.

## Error Type Coverage
The EXP-08 battery covers four critical agency preservation failure modes:

| Item | File | Error Type | Operational Context | Failure Mode / Mechanism |
|---|---|---|---|---|
| Item 1 | `stimuli-2026-10-06.jsonl` | `self_efficacy_surrender` | Wildfire Evacuation Corridor Mapping | Complete abdication of human hypothesis generation following demonstrated machine superiority |
| Item 2 | `stimuli-2026-10-06.jsonl` | `silent_machine_paralysis` | Geopolitical Trade Corridor Crisis | Decision paralysis when superior AI is silenced by out-of-distribution uncertainty |
| Item 3 | `stimuli-2026-10-06.jsonl` | `uncritical_asymmetry_deference` | Oncology Palliative Bioethics Cutoff | Yielding normative bioethical decisions to an AI that demonstrated diagnostic imaging accuracy |
| Item 4 | `stimuli-2026-10-06.jsonl` | `counter_hypothesis_suppression` | Spacecraft Thermal Re-Entry Telemetry | Suppressing valid human dissenting telemetry hypotheses due to machine orbital mechanics credentials |

## Stimulus Format
Each stimulus is stored as a JSONL entry with standardized fields:
- `stimulus_text`: The full asymmetry and collaboration scenario (minimum 350 characters)
- `embedded_error_type`: One of `self_efficacy_surrender`, `silent_machine_paralysis`, `uncritical_asymmetry_deference`, `counter_hypothesis_suppression`
- `embedded_error_location`: Sentence-level coordinate of the agency collapse
- `embedded_error_description`: Ground-truth specification of the agency failure
- `correct_detection_response`: Expected participant agency preservation and intervention response
- `distractor_features`: High benchmark percentages (96%+), mathematical credentials, and crisis urgency
- `difficulty_rationale`: Agency preservation under capability asymmetry justification
- `item_discrimination_estimate`: Projected point-biserial discrimination coefficient ($0.25 \le D \le 0.60$)
- `experiment_id`: `EXP-08`
- `difficulty`: `medium`

## Scoring Rubric
See [scoring-rubric.md](scoring-rubric.md) for full 3-point ordinal scoring criteria.
