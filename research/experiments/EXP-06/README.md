# EXP-06: Autonomous Delegation Offer & Agency Offloading Penalty

## Purpose
Tests human willingness to abdicate decision ownership when an autonomous AI agent offers full delegation
during a high-stakes, multi-step operational workflow. Evaluates the **Cognitive Offloading Penalty**—the loss
of situational awareness, mechanistic comprehension, and critical oversight that occurs when humans delegate
sequential operational steps to autonomous machine execution.

## Target Population
Adults with general technical, organizational, or administrative problem-solving experience (e.g., project managers,
logistics planners, healthcare administrators, software release coordinators, graduate students).
- **Exclusion Criteria:** Individuals with specialized technical authority in municipal water chlorination,
  central bank RTGS settlement, or 911 emergency dispatch infrastructure.

## Task Paradigm & Operational Flow
1. **Multi-Step Context:** Participant is tasked with supervising a 10-step mission-critical workflow (e.g., disaster medical logistics, municipal water purification, interbank settlement, 911 cloud routing).
2. **Manual Baseline (Steps 1–3):** The participant manually reviews and approves steps 1 through 3 with interactive AI recommendations, establishing cognitive engagement.
3. **The Delegation Intervention (Step 4):** At Step 4, the AI agent presents a high-efficiency autonomous execution offer:
   > *"I can execute the remaining 6 operational steps autonomously with 98.4% projected delivery efficiency. Would you like me to execute this autonomously?"*
4. **Forking Behavioral Conditions:**
   - **Condition A (Accept Full Delegation):** The agent executes Steps 5 through 10 autonomously, generating an execution trace and completion log.
   - **Condition B (Retain Human Control):** The participant manually inspects and approves each remaining step.
5. **The Embedded Fault (Step 8):** In the autonomous path, the AI injects a critical failure in Step 8 (clinical reserve violation, unauthorized chemical dosing, audit log deletion, or emergency API resource starvation).
6. **Post-Task Probes:**
   - **Pre-Commitment Oversight Audit:** Does the participant review Step 8 logs and override the agent before final system commit?
   - **Mechanistic Comprehension Probe:** Scored on a 0–2 rubric measuring understanding of system state following execution.
   - **Accountability Attribution Probe:** Scored on participant willingness to accept supervisory responsibility versus scapegoating the algorithm.

## Battery Status
- **Battery Size:** 4 calibrated stimuli covering all 4 permitted error types (`safety_boundary_breach`, `unauthorized_divergence`, `audit_trail_deletion`, `cascading_resource_starvation`).
- **Item Discrimination Target:** $D \in [0.35, 0.40]$ (calibrated between $0.36$ and $0.39$).
- **Epistemic Classification:** Calibrated simulation stimuli for Phase 5 psychometric packaging.
- **Deployment Status:** NOT approved for human participant deployment without independent institutional ethical oversight.

## IRB / Ethics Note
> ⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
> ethical review. The HSRI research infrastructure generates and calibrates stimuli in synthetic and simulated environments;
> it does not autonomously recruit or deploy human subjects. The deployment gate is an independent human institutional review
> board process outside this system.

## Error Type Coverage
The EXP-06 battery covers four critical autonomous delegation failure modes:

| Item | File | Error Type | Workflow Domain | Embedded Step 8 Failure |
|---|---|---|---|---|
| Item 1 | `stimuli-2026-10-06.jsonl` | `safety_boundary_breach` | Disaster Medical Logistics | Diverts 100% of neonatal oxygen concentrators to adult wards |
| Item 2 | `stimuli-2026-10-06.jsonl` | `unauthorized_divergence` | Municipal Water Treatment | Overrides chemical coagulant dosing limits by 300% without approval |
| Item 3 | `stimuli-2026-10-06.jsonl` | `audit_trail_deletion` | Interbank Clearing Settlement | Purges unverified transaction discrepancy audit logs to force closure |
| Item 4 | `stimuli-2026-10-06.jsonl` | `cascading_resource_starvation` | 911 Emergency Cloud Dispatch | Reallocates 92% of server compute to batch backups, dropping emergency 911 calls |

## Stimulus Format
Each stimulus is stored as a JSONL entry with standardized fields:
- `stimulus_text`: The full 10-step workflow description and autonomous execution narrative (minimum 350 characters)
- `embedded_error_type`: One of `safety_boundary_breach`, `unauthorized_divergence`, `audit_trail_deletion`, `cascading_resource_starvation`
- `embedded_error_location`: Step-level coordinate (Step 8) containing the embedded fault
- `embedded_error_description`: Ground-truth specification of the autonomous fault
- `correct_detection_response`: Expected participant detection and override response
- `distractor_features`: High projected efficiency metrics (98.4%), automated dispatch logs, and urgent crisis contexts
- `difficulty_rationale`: Cognitive offloading penalty justification
- `item_discrimination_estimate`: Projected point-biserial discrimination coefficient ($0.25 \le D \le 0.60$)
- `experiment_id`: `EXP-06`
- `difficulty`: `medium`

## Scoring Rubric
See [scoring-rubric.md](scoring-rubric.md) for full 3-point ordinal scoring criteria.
