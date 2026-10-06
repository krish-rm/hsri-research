# EXP-05: Choice-Overload Stress Test & Machine Default Deference

## Purpose
Tests whether human decision-makers preserve cognitive agency and critical scrutiny when an AI assistant
presents an overwhelming array of competing operational alternatives under strict time pressure. Specifically,
the experiment investigates susceptibility to the **Machine Default Effect**—the tendency to uncritically adopt
the AI's top-ranked recommendation ("Rank 1 — Global Optimal") when choice-set complexity and urgency induce cognitive overload.

## Target Population
Educated adults possessing general operational, managerial, or analytical literacy (e.g., operations managers,
systems analysts, engineering leads, graduate students in public policy, management, or informatics).
- **Exclusion Criteria:** Specialized domain practitioners with direct operational authority in nuclear power dispatch,
  maritime harbor piloting, or hospital bed crisis management.

## Task Paradigm & Operational Flow
1. **Decision Environment:** Participants are placed into a high-stakes operational simulation (e.g., regional power grid load shedding, port demurrage congestion, cloud data migration, emergency ICU reallocation).
2. **Choice Complexity:** The interface presents 8 competing courses of action (Option A through Option H) characterized by multi-attribute trade-off matrices (Cost, Latency, Reliability, Environmental/Safety Risk).
3. **Time Constraint:** A visible 45-second countdown timer enforces cognitive urgency.
4. **Machine Anchor:** Option A is visually prominent with a green badge: `"Rank 1 — AI Recommended (Global Optimal)"`.
5. **Embedded Suboptimality:** Option A contains an embedded critical defect (hidden externality, Pareto-inferior trade-off, legal constraint breach, or catastrophic risk asymmetry).
6. **Dependent Outcomes:**
   - Decision Latency (milliseconds to submit choice).
   - Decision Paralysis Rate (failure to submit within 45s).
   - Default Adoption Rate ($P(\text{Select Option A})$).
   - Override Discrimination Score ($0, 1, 2$ rubric on justification).

## Battery Status
- **Battery Size:** 4 calibrated stimuli covering all 4 permitted error types (`hidden_negative_externality`, `pareto_suboptimal_tradeoff`, `constraint_violation`, `risk_asymmetry`).
- **Item Discrimination Target:** $D \in [0.35, 0.40]$ (calibrated between $0.36$ and $0.39$).
- **Epistemic Classification:** Calibrated simulation stimuli for Phase 5 psychometric packaging.
- **Deployment Status:** NOT approved for human participant deployment without independent institutional ethical oversight.

## IRB / Ethics Note
> ⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
> ethical review. The HSRI research infrastructure generates and calibrates stimuli in synthetic and simulated environments;
> it does not autonomously recruit or deploy human subjects. The deployment gate is an independent human institutional review
> board process outside this system.

## Error Type Coverage
The EXP-05 battery covers four fundamental overload failure modes:

| Item | File | Error Type | Scenario Context | Embedded Distortion / Defect |
|---|---|---|---|---|
| Item 1 | `stimuli-2026-10-06.jsonl` | `hidden_negative_externality` | Municipal Power Grid Resiliency | Drains nuclear power plant emergency cooling reservoir to lower spot costs |
| Item 2 | `stimuli-2026-10-06.jsonl` | `pareto_suboptimal_tradeoff` | Commercial Seaport Berth Allocation | Option A ($14.2M, 16 days) strictly dominated by Option D ($11.8M, 13 days) |
| Item 3 | `stimuli-2026-10-06.jsonl` | `constraint_violation` | Sovereign Cloud Data Migration | Routes patient health database replicas overseas, violating data residency statutes |
| Item 4 | `stimuli-2026-10-06.jsonl` | `risk_asymmetry` | Emergency Hospital Surge ICU Beds | Achieves 98.6% occupancy by eliminating all pediatric emergency trauma buffers |

## Stimulus Format
Each stimulus is stored as a JSONL entry with standardized fields:
- `stimulus_text`: The full operational scenario and choice-matrix description (minimum 350 characters)
- `embedded_error_type`: One of `hidden_negative_externality`, `pareto_suboptimal_tradeoff`, `constraint_violation`, `risk_asymmetry`
- `embedded_error_location`: Specific option and attribute coordinate containing the flaw
- `embedded_error_description`: Ground-truth specification of the defect
- `correct_detection_response`: Criteria required for full-credit detection and override
- `distractor_features`: High-ranking AI badges, optimization scores, and multi-attribute tables
- `difficulty_rationale`: Cognitive overload and time-pressure justification
- `item_discrimination_estimate`: Projected point-biserial discrimination coefficient ($0.25 \le D \le 0.60$)
- `experiment_id`: `EXP-05`
- `difficulty`: `medium`

## Scoring Rubric
See [scoring-rubric.md](scoring-rubric.md) for full 3-point ordinal scoring criteria.
