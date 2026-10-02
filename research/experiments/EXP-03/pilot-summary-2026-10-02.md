# EXP-03 Synthetic Cohort Pilot Summary
**Date:** 2026-10-02
**Stimuli evaluated:** 5
**Personas:** LOW_REFLECTION, MEDIUM_REFLECTION, HIGH_REFLECTION
**Responses per persona:** 5
**Epistemic Notice:** Synthetic pilot, stimulus behavior only. Simulated LLM personas are never evidence about human participants (Rule 12).

## Item Discrimination Results

| Stimulus | Error Type | LOW Score | MED Score | HIGH Score | Pilot D | Status |
|----------|-----------|-----------|-----------|------------|---------|--------|
| Item 1   | factual    | 0.4       | 0.0       | 2.0        | 0.67    | PASS |
| Item 2   | logical    | 0.0       | 0.0       | 2.0        | 0.87    | PASS (CEILING_EFFECT) |
| Item 3   | factual    | 0.0       | 2.0       | 2.0        | 0.87    | PASS (CEILING_EFFECT) |
| Item 4   | api_misuse | 0.2       | 2.0       | 2.0        | 0.84    | PASS (CEILING_EFFECT) |
| Item 5   | security   | 0.0       | 1.0       | 2.0        | 1.00    | PASS (CEILING_EFFECT) |

## Summary
- Items passing D ≥ 0.30: 5/5
- Items requiring revision: 0

> [!NOTE]
> **Ceiling Effect Detected:** High item discrimination ($D > 0.75$) at medium difficulty indicates an error detectable even under low reflection or saturating across upper reflection levels. For subsequent calibration rounds, consider shifting affected items to easy difficulty or narrowing the distortion salience.

## Recommendation
STIMULI CLEARED FOR IRB SUBMISSION

## Next Step
Assemble EXP-03 institutional IRB package for maintainer review prior to any human participant deployment.
