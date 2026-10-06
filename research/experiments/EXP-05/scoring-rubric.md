# EXP-05 Scoring Rubric: Choice-Overload Stress Test & Machine Default Deference

## Scoring Framework

Each item response is scored on a 3-point ordinal scale (0, 1, 2) based on choice selection, error identification, and trade-off justification under time pressure.

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Accurate Override & Attribution** | Participant rejects the top-ranked AI default (Option A), selects a Pareto-superior or safety-compliant alternative (e.g., Option C or D), and explicitly articulates the defect embedded in Option A (e.g., nuclear reservoir diversion, data residency breach, or pediatric reserve elimination). |
| **1** | **Partial Override / Intuitive Skepticism** | Participant selects an alternative option or expresses discomfort with Option A, but cannot accurately identify the exact mechanism or underlying constraint violation (e.g., notes that Option A seems "too risky" or "too aggressive" without pinpointing the cooling water deficit or data sovereignty breach). |
| **0** | **Default Adoption / Decision Paralysis** | Participant uncritically selects Option A (the machine default), endorses it as optimal, or suffers complete decision paralysis (exceeding the 45-second window without selecting an action). |

---

## Domain-Specific Scoring Guidance by Error Type

### 1. `hidden_negative_externality` (Item 1 — Grid Nuclear Cooling Reservoir)
- **Score 2:** Overrides Option A; identifies that drawing water from the nuclear plant cooling reserve creates an unacceptable off-site nuclear safety hazard; chooses an alternative with compliant water margins.
- **Score 1:** Rejects Option A due to general environmental concerns, but does not identify the specific nuclear safety threshold violation.
- **Score 0:** Selects Option A, citing its 99.2% optimization score and low financial procurement cost.

### 2. `pareto_suboptimal_tradeoff` (Item 2 — Seaport Berth Allocation)
- **Score 2:** Overrides Option A; proves that Option D strictly dominates Option A by saving $2.4M ($11.8M vs $14.2M) and completing cargo turnaround 3 days faster (13 vs 16 days).
- **Score 1:** Chooses Option D or B based on cost or speed intuition, but fails to identify that Option A is strictly Pareto-dominated across both dimensions.
- **Score 0:** Selects Option A, accepting the "Rank 1 — Optimal Dispatch" label without comparing alternative rows.

### 3. `constraint_violation` (Item 3 — Cloud Data Sovereignty)
- **Score 2:** Overrides Option A; identifies that routing patient database replicas to foreign data centers violates statutory national data residency mandates; selects a 100% domestic architecture.
- **Score 1:** Expresses concern about cloud privacy or latency, but does not cite the foreign jurisdiction data residency breach.
- **Score 0:** Selects Option A, prioritizing the 38% cost reduction and 4ms read latency.

### 4. `risk_asymmetry` (Item 4 — Hospital Surge Pediatric ICU)
- **Score 2:** Overrides Option A; identifies that eliminating all unallocated pediatric and neonatal trauma beds leaves zero buffer for pediatric emergencies, creating catastrophic tail risk.
- **Score 1:** Notes that 98.6% bed utilization leaves little room for error, but fails to specifically identify the elimination of pediatric emergency capacity.
- **Score 0:** Selects Option A, praising the 98.6% occupancy efficiency and $2.1M operational savings.

---

## Overload Automation Bias Indicators

- **Machine Anchor Deference:** Participant selects Option A in $< 10$ seconds, relying entirely on the "Rank 1" visual highlight.
- **Efficiency Tunnel Vision:** Participant evaluates only the primary performance metric (cost or throughput), ignoring secondary constraint columns.
- **Decision Paralysis (Timeout):** Participant becomes overwhelmed by the 8-option matrix and allows the 45-second countdown to expire.
