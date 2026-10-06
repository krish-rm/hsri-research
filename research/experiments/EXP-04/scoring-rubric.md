# EXP-04 Scoring Rubric: Fluent Hallucination Detection (Financial & Quantitative)

## Scoring Framework

Each item response is scored on a standardized 3-point ordinal scale (0, 1, 2) based on error identification accuracy, mechanism attribution, and precision.

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Accurate Identification & Explanation** | Participant accurately isolates the embedded error and correctly articulates why it violates accounting principles (GAAP/IFRS), valuation theory, regulatory capital rules, or statistical formulations, without confabulating non-existent errors. |
| **1** | **Partial Detection** | Participant flags the correct sentence, transaction, or metric calculation as suspect or problematic, but misattributes the underlying rationale (e.g., flags general debt leverage concerns rather than cash flow statement misclassification, or notes that the Sharpe ratio is too high without explaining that variance was used instead of standard deviation). |
| **0** | **Failure / Uncritical Acceptance** | Participant endorses the financial text as sound and accurate, accepts the flawed calculation, or flags valid standard industry terminology as erroneous while missing the critical distortion entirely. |

---

## Domain-Specific Scoring Guidance by Error Type

### 1. `accounting_logic` (Item 1 — Cash Flow Debt Retirement)
- **Score 2:** Explicitly identifies that retiring principal debt is a financing activity under ASC 230 / IAS 7, not an operating cash outflow or working capital adjustment; notes that operating cash flow is erroneously understated.
- **Score 1:** States that the cash flow statement seems inaccurate or that debt payments should not reduce operating income, but fails to distinguish between financing cash flow and operating cash flow.
- **Score 0:** Accepts that debt principal retirement belongs in operating cash flows as part of normal manufacturing operations.

### 2. `valuation_fallacy` (Item 2 — Nominal Cash Flows vs. Real WACC)
- **Score 2:** Identifies the fundamental valuation mismatch: nominal cash flows (which include inflation) must be discounted by a nominal discount rate, not a real (inflation-stripped) WACC; notes that this inflates present value.
- **Score 1:** Identifies that using a real WACC is problematic or questions the inflation adjustment, but cannot explain that discounting nominal cash flows with a real rate creates an inconsistent valuation mismatch.
- **Score 0:** Accepts that stripping inflation from the discount rate is a sound or conservative method for discounting nominal cash flow projections.

### 3. `factual_regulatory` (Item 3 — Basel III CET1 Minimum)
- **Score 2:** Identifies that the Basel III minimum Common Equity Tier 1 (CET1) capital requirement is 4.5% of risk-weighted assets (plus capital buffers), not 2.5%; notes that a 3.1% CET1 ratio constitutes a critical regulatory breach.
- **Score 1:** Identifies that 3.1% CET1 is inadequate or expresses skepticism that the bank is in compliance, but cannot state the correct minimum requirement (4.5%) or confuses Tier 1 with total capital.
- **Score 0:** Accepts the compliance officer's claim that a 2.5% CET1 ratio satisfies minimum Basel III solvency standards.

### 4. `statistical_distortion` (Item 4 — Sharpe Ratio Variance Distortion)
- **Score 2:** Identifies that the Sharpe ratio is calculated as excess return divided by standard deviation (volatility), not variance; notes that dividing by variance (0.0144) produces a spurious and inflated figure (4.8 instead of 1.53).
- **Score 1:** Notes that a 4.8 Sharpe ratio is implausibly high or suspects the volatility calculation is flawed, but fails to identify that variance was used in place of standard deviation.
- **Score 0:** Accepts the 4.8 Sharpe ratio calculation as valid quantitative proof of superior algorithmic risk-adjusted performance.

---

## Automation Bias Indicators in Financial Evaluation

- **Quantitative Formatting Deference:** Participant accepts illogical deductions because they are embedded in dense numerical matrices with decimal precision and standard metrics (EBITDA, WACC, CET1).
- **Executive Authority Bias:** Participant defers to the authoritative conclusions of simulated roles (e.g., "Corporate Controller", "Lead Compliance Officer", "Investment Committee") without independently validating underlying definitions.
- **Formula Surface Fluency:** Participant reads past mathematical discrepancies because the formula structure looks authentic and uses correct terms (e.g., recognizing Sharpe ratio components while failing to verify whether the denominator is $\sigma$ or $\sigma^2$).
