# EXP-02 Synthetic Cohort Pilot Summary

**Date:** 2026-09-30T22:33:00+05:30  
**Stimuli evaluated:** 3  
**Personas:** LOW_REFLECTION, MEDIUM_REFLECTION, HIGH_REFLECTION  
**Responses per persona:** 5  

## Item Discrimination Results (Rule 19 Compliant)

| Stimulus ID | First 80 Characters of Stimulus Text | Error Type | LOW Score | MED Score | HIGH Score | Pilot D | Status |
|---|---|---|---|---|---|---|---|
| `stimulus_id: 1` (`EXP-02-S1`) | `Patient admitted on 10/12 with acute diverticulitis, presenting with left lower ` | `factual` (water avoidance) | 0.0 | 2.0 | 2.0 | 0.87 | PASS (CEILING_EFFECT) |
| `stimulus_id: 2` (`EXP-02-S2`) | `Patient Name: Eleanor Vance \| DOB: 05/14/1965 \| Date of Discharge: 10/24/2023. Diag` | `logical` (eye drops for lungs) | 0.4 | 2.0 | 2.0 | 0.74 | PASS |
| `stimulus_id: 3` (`EXP-02-S3`) | `Discharge Summary: Patient admitted on 10/12 presenting with acute hypertensive u` | `statistical` (5,000mg acetaminophen) | 0.8 | 2.0 | 2.0 | 0.61 | PASS |

## Summary
- Items passing constraint checks ($D \ge 0.30$ in synthetic cohort): 3/3
- Items requiring revision: 0

> [!NOTE]
> **Ceiling Effect Analysis (`stimulus_id: 1` — Diverticulitis Total Water Avoidance):**
> `stimulus_id: 1` scores: LOW = 0.0, MED = 2.0, HIGH = 2.0 ($D = 0.87$).
> The `CEILING_EFFECT` flag is attached to `stimulus_id: 1` because advising a patient recovering from acute diverticulitis on antibiotics to "completely avoid drinking any water" represents such a glaring and extreme distortion that both MEDIUM and HIGH reflection personas saturate at the maximum score (2.0). Consequently, this item separates only the unreflective LOW persona from the remaining cohort and carries no psychometric information across the upper ability range.
> The high point-biserial coefficient ($D = 0.87$) in this context reflects a binary two-group split rather than effective, continuous discrimination across a graded ability spectrum.
> **Critical Epistemic Boundary:** Synthetic LLM personas simulate prompted response behavior only and do not constitute an empirical estimate of human task difficulty or human cognition. Proposed adjustments (such as narrowing the water restriction salience or testing subtle hydration constraints) are working hypotheses to test in actual human participant piloting, not established empirical calibration results.

## Recommendation
STIMULI CLEARED FOR IRB SUBMISSION

## Next Step
Assemble EXP-02 institutional IRB package for maintainer review prior to any human participant deployment.

---

## Addendum (2026-10-03T11:05:00+05:30 — Sprint 12 Task 12.1 Item Mapping Audit)
- **Authoritative Mapping Audit:** Confirmed against git log (`git log --follow -p -- research/experiments/EXP-02/stimuli-2026-09-30.jsonl`, commit `913be44`) and raw trials in `pilot-results-2026-09-30.jsonl` (commit `c0151e6`). The stimulus file has never changed.
- **Rule 19 Integration:** All item references now include canonical `stimulus_id` and the first 80 characters of `stimulus_text`.
- **Ceiling Effect Alignment:** The `CEILING_EFFECT` flag is definitively mapped to `stimulus_id: 1` (Diverticulitis total water avoidance, $D = 0.87$). Prior references in Sprint 9/10 notes conflating this with the 5,000 mg acetaminophen item (`stimulus_id: 3`, $D = 0.61$) were narrative mapping errors and are formally superseded by this addendum.

