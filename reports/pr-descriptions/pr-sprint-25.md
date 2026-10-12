# PR Description: Sprint 25 — Study 2 Non-Compensatory Aggregation & Weakest-Link Flooring

> **Timestamp**: `2026-10-12T19:13:12.0830056+05:30`  
> **Milestone**: `v1.2.0-Econometrics` (Sprint 25)  
> **Target Branch**: `main`  
> **Compliance**: Rule 22 (Zero-Hallucination), Rule 3 (NaN Governance), Rule 24 (Maintainer Staging)  

---

## Summary of Changes
Addresses the Chief Scientific Evaluator's audit critique regarding the *High-Compute Vulnerability Trap* by introducing four distinct econometric aggregation families across the 39-nation benchmark:

1. **`scripts/non_compensatory_engine.py`**:
   - Implements Linear, Geometric Mean (AM-GM discount), Leontief Minimum Floor ($\beta=0.5$), and Choquet 2-additive capacity integral.
   - Calculates Vulnerability Index ($V_n$), Floor Fragility ($F_n$), and High-Compute Trap flags.
   - Executes $B=1,000$ Dirichlet Monte Carlo sensitivity analysis ($W \ge 0.982$, $\bar{\rho} = 0.9644$).
2. **`data/hsri_variants.csv` & JSON Sync**:
   - Exports complete 39-country multi-model metrics to `data/` and `site-astro/` data directories.
3. **`tests/test_aggregation.py`**:
   - 18 comprehensive econometric unit tests (expanding test suite from 117 to 135 passing tests).
4. **`site-astro` Web Portal Upgrade**:
   - Interactive Aggregation Mode Toggle in `CountryList.svelte` on `humanreadinessindex.org`.
   - Updated `MethodologyOverview.svelte` with complete Study 2 formulation.
5. **Academic & Governance Dossiers**:
   - `research/aggregation-audit/audit_v1.2.md`: Full JRC Step 7 sensitivity analysis report.
   - `research/preprint/working-paper-v1.1.0.md`: Section 5.4 inserted.
   - `CHANGELOG.md`: Added v1.2.0 release documentation.

## Test & Verification Evidence
- `uv run pytest`: 135/135 tests passing green (100%).
- `npm run build`: 49 pages compiled cleanly in 4.65 seconds.
