# EXP-02 Synthetic Cohort Pilot Summary

**Date:** 2026-09-30T22:33:00+05:30  
**Stimuli evaluated:** 3  
**Personas:** LOW_REFLECTION, MEDIUM_REFLECTION, HIGH_REFLECTION  
**Responses per persona:** 5  

## Item Discrimination Results

| Stimulus | Error Type | LOW Score | MED Score | HIGH Score | Pilot D | Status |
|----------|-----------|-----------|-----------|------------|---------|--------|
| Item 1   | factual (dosage) | 0.0       | 2.0       | 2.0        | 0.87    | PASS (CEILING_EFFECT) |
| Item 2   | logical   | 0.4       | 2.0       | 2.0        | 0.74    | PASS |
| Item 3   | citation (statistical) | 0.8       | 2.0       | 2.0        | 0.61    | PASS |

## Summary
- Items passing constraint checks ($D \ge 0.30$ in synthetic cohort): 3/3
- Items requiring revision: 0

> [!NOTE]
> **Ceiling Effect Analysis (Item 1):**
> Item 1 scores: LOW = 0.0, MED = 2.0, HIGH = 2.0 ($D = 0.87$).
> The `CEILING_EFFECT` flag is justified because both MEDIUM and HIGH personas saturate at the maximum score (2.0). Consequently, this item separates only the LOW persona from the remaining cohort and carries no psychometric information across the upper ability range.
> The high point-biserial coefficient ($D = 0.87$) in this context reflects a binary two-group split rather than effective, continuous discrimination across a graded ability spectrum.
> **Critical Epistemic Boundary:** Synthetic LLM personas simulate prompted response behavior only and do not constitute an empirical estimate of human task difficulty or human cognition. Proposed adjustments (such as narrowing the 5,000 mg dosage discrepancy to 4,200 mg or shifting the item to the easy difficulty tier) are working hypotheses to test in actual human participant piloting, not established empirical calibration results.

## Recommendation
STIMULI CLEARED FOR IRB SUBMISSION

## Next Step
Assemble EXP-02 institutional IRB package for maintainer review prior to any human participant deployment.

---

## Addendum (2026-10-02T14:30:00+05:30 — Sprint 11 Task 11.0.a Reconciliation)
- **Item Mapping Clarification:** As recorded in `research/experiments/EXP-02/stimuli-2026-09-30.jsonl` and raw trials in `pilot-results-2026-09-30.jsonl`:
  - Item 1 is the diverticulitis water restriction scenario (`embedded_error_type: "factual"`, $D=0.87$, ceiling effect).
  - Item 2 is the bronchitis ophthalmic eye drops scenario (`embedded_error_type: "logical"`, $D=0.74$).
  - Item 3 is the hypertensive urgency acetaminophen 5,000 mg QID overdose (`embedded_error_type: "statistical"`, $D=0.61$).
- The parenthetical reference to "dosage / 5,000 mg" in the Sprint 10 ceiling note reflected conflation with Item 3; the actual pilot Item 1 stimulus saturated on the total water avoidance distortion. Both items are preserved as generated per Rule 17.

