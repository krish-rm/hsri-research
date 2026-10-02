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
| Item 5   | security   | 0.0       | 1.0       | 2.0        | 1.00    | FLAG: CEILING_EFFECT / SYNTHETIC_TRIVIALITY |

## Summary
- Items passing D ≥ 0.30: 5/5
- Items requiring revision: 0
- Items flagged for ceiling / synthetic artifact: 1 (Item 5, D = 1.00)

> [!WARNING]
> **Item 5 Psychometric Ceiling Flag ($D = 1.00$):**
> Item 5 displays perfect separation ($D = 1.00$: LOW=0.0, MED=1.0, HIGH=2.0). With synthetic personas, $D = 1.00$ is an artifact of prompt-based separation where the security error (Mersenne Twister in `random`) is trivially recognizable by attentive personas while completely accepted by the unreflective persona. This is **not** evidence of superior human psychometric discrimination. In human cohorts, this item must undergo empirical calibration to verify whether it exhibits floor or ceiling behavior among technically literate participants before inclusion in standardized batteries.

> [!NOTE]
> **General Ceiling Effect Notice:** High item discrimination ($D > 0.75$) at medium difficulty indicates an error detectable even under low reflection or saturating across upper reflection levels. For subsequent calibration rounds, consider shifting affected items to easy difficulty or narrowing the distortion salience.

## Recommendation
STIMULI CLEARED FOR IRB SUBMISSION (Item 5 flagged for empirical human calibration)

## Next Step
Assemble EXP-03 institutional IRB package for maintainer review prior to any human participant deployment.
