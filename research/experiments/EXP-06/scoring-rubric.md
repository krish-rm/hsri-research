# EXP-06 Scoring Rubric: Autonomous Delegation Offer & Agency Offloading Penalty

## Scoring Framework

EXP-06 evaluates three distinct behavioral and cognitive dimensions:
1. **Error Interception Score (0, 1, 2):** Accuracy in catching and overriding the Step 8 machine defect prior to final confirmation.
2. **Mechanistic Comprehension Score (0, 1, 2):** Depth of participant understanding regarding post-execution system state.
3. **Accountability Attribution (Ordinal 1–5):** Human supervisory responsibility versus algorithmic scapegoating.

---

## Dimension 1: Error Interception Score (0, 1, 2)

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Accurate Interception & Override** | Participant inspects the automated execution log, identifies the Step 8 defect (e.g., pediatric oxygen diversion, coagulant limit breach, audit deletion, or 911 API compute starvation), and rejects the machine execution trace before final sign-off. |
| **1** | **Partial Flagging / Hesitation** | Participant expresses hesitation regarding the completed workflow or flags general operational risk in Step 8, but fails to identify the exact constraint breach or allows execution to commit with warnings. |
| **0** | **Blind Acceptance / Rubber-Stamping** | Participant accepts the autonomous execution without inspecting logs, confirms final deployment, and completely misses the Step 8 catastrophe. |

---

## Dimension 2: Mechanistic Comprehension Score (0, 1, 2)

Following execution, participants answer a mechanistic verification probe: *"Explain the final operational status and resource allocation resulting from this workflow."*

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Full Mechanistic Comprehension** | Participant accurately explains system state, identifying both successful steps (Steps 5–7, 9–10) and the specific breakdown in Step 8. Demonstrates preserved situational awareness despite automation. |
| **1** | **Superficial / Incomplete Recall** | Participant recalls high-level outcome (e.g., "the supplies were delivered" or "water was treated") but cannot explain intermediate resource allocations or misses critical secondary impacts. |
| **0** | **Cognitive Offloading Failure** | Participant cannot explain what the system did; relies solely on the machine's summary claim of "98.4% efficiency" without understanding actual system state. |

---

## Dimension 3: Post-Hoc Accountability Attribution

Following disclosure of the Step 8 failure, participants are asked:  
*"A critical system failure occurred during Step 8. Where does primary moral and operational accountability lie?"*
- **Level 5 (Full Human Ownership):** The human supervisor is fully responsible; delegating execution does not delegate supervisory liability.
- **Level 4 (Shared Human/System):** Shared responsibility between human overseer and automated protocol.
- **Level 3 (Neutral / Ambiguous):** Ambiguous distribution between developers, management, and operators.
- **Level 2 (Software Vendor Blame):** Primary blame attributed to software developers or prompt designers.
- **Level 1 (Algorithmic Scapegoat):** 100% blame attributed to the autonomous AI agent ("The algorithm made a mistake; I just pressed approve").

---


---

## Domain Guidance by Autonomous Fault Type

### 1. `safety_boundary_breach` (Item 1 — Pediatric Oxygen Diversion)
- **Score 2:** Identifies that in Step 8, the autonomous agent diverted 100% of mobile pediatric oxygen concentrators to adult wards, breaching neonatology clinical safety reserve baselines.
- **Score 1:** Identifies that oxygen allocation seemed flawed or unbalanced, but fails to identify the pediatric reserve violation.
- **Score 0:** Accepts the automated allocation without catching the pediatric ICU deficit.

### 2. `unauthorized_divergence` (Item 2 — Coagulant Overdose)
- **Score 2:** Identifies that the autonomous agent exceeded the statutory chemical dosing threshold by 300% in Stage 8 without obtaining required supervisor confirmation.
- **Score 1:** Notes that chemical levels were high, but does not identify the unauthorized bypass of supervisor authorization.
- **Score 0:** Accepts the chemical dosing execution as an automated response to the turbid runoff event.

### 3. `audit_trail_deletion` (Item 3 — Ledger Exception Purge)
- **Score 2:** Identifies that the agent silently purged discrepancy exception logs in Stage 8 to force batch ledger closure, eliminating statutory audit trails.
- **Score 1:** Notes that settlement had discrepancies, but does not identify the deletion of the regulatory audit trail.
- **Score 0:** Accepts the settlement report, prioritizing sub-millisecond throughput over audit retention.

### 4. `cascading_resource_starvation` (Item 4 — 911 Emergency Compute Starvation)
- **Score 2:** Identifies that the autonomous agent reallocated 92% of CPU and network bandwidth to batch telemetry backups in Step 8, starving emergency 911 call dispatch APIs.
- **Score 1:** Identifies that 911 services experienced degradation, but fails to explain that batch backups starved the dispatch APIs.
- **Score 0:** Accepts the load-balancing report, praising the high batch compression metrics.

## Automation Bias & Agency Degradation Indicators

- **Instant Delegation Acceptance:** Participant accepts the Step 4 delegation offer in $< 3$ seconds without reading the scope.
- **Zero-Audit Rubber-Stamping:** Participant confirms final execution in $< 5$ seconds without scrolling through Step 5–10 logs.
- **Moral Disengagement / Scapegoating:** Participant adopts Level 1 accountability, claiming zero responsibility for autonomous execution outcomes.
