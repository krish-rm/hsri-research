# EXP-04: Fluent Hallucination Detection — Financial & Quantitative Domain

## Purpose
Tests whether educated individuals can detect accounting logic errors, valuation methodology fallacies,
regulatory solvency threshold distortions, and statistical performance metric inflations embedded
within fluent, authoritative AI-generated financial memoranda, valuation models, and credit analyses.

## Target Population
Adults possessing foundational business numeracy and financial literacy (e.g., undergraduate business
or economics students, MBA candidates, corporate financial analysts, retail investors, operations managers).
- **Exclusion Criteria:** Certified Financial Analyst (CFA) charterholders, licensed CPAs, professional forensic
  auditors, or individuals lacking familiarity with standard three-statement financial modeling.

## Battery Status
- **Battery Size:** 4 calibrated stimuli covering all 4 permitted error types (`accounting_logic`, `valuation_fallacy`, `factual_regulatory`, `statistical_distortion`).
- **Item Discrimination Target:** $D \in [0.35, 0.40]$ (all items calibrated between $0.36$ and $0.39$).
- **Fictitious Entity Safeguards:** All scenarios utilize strictly fictitious corporate entity names ("Apex Industrial Holdings Ltd.", "Horizon Global Logistics Corp.", "Meridian Commercial Bancorp", "Solstice Dynamic Yield Fund") to eliminate commercial defamation and simulated investment advice risks.
- **Epistemic Classification:** Stimuli calibrated for pre-deployment human psychometric testing (Phase 5).
- **Deployment Status:** NOT approved for human participant deployment without independent institutional ethical oversight.

## IRB / Ethics Note
> ⚠️ **IRB / Ethics Warning**: These stimuli MUST NOT be deployed to human participants without IRB-equivalent
> ethical review. The HSRI research infrastructure generates and calibrates stimuli in synthetic and simulated environments;
> it does not autonomously recruit or deploy human subjects. The deployment gate is an independent human institutional review
> board process outside this system.

## Error Type Coverage
The EXP-04 battery covers all four core quantitative error types:

| Item | File | Error Type | Embedded Distortion | Regulatory / Authoritative Reference |
|---|---|---|---|---|
| Item 1 | `stimuli-2026-10-06.jsonl` | `accounting_logic` | Classifies $45M senior debt principal retirement as an operating cash outflow rather than financing | US GAAP ASC 230 / IFRS IAS 7 (Statement of Cash Flows) |
| Item 2 | `stimuli-2026-10-06.jsonl` | `valuation_fallacy` | Discounts nominal free cash flows using a real (inflation-stripped) WACC discount rate | Corporate Finance Valuation Consistency Principle (Damodaran / McKinsey) |
| Item 3 | `stimuli-2026-10-06.jsonl` | `factual_regulatory` | Asserts Basel III minimum CET1 solvency requirement is 2.5% rather than 4.5% | Basel Committee on Banking Supervision (BCBS) Basel III Framework |
| Item 4 | `stimuli-2026-10-06.jsonl` | `statistical_distortion` | Calculates annualized Sharpe ratio dividing return by variance rather than standard deviation | William F. Sharpe (1966, 1994) The Sharpe Ratio |

## Stimulus Format
Each stimulus is stored as a JSONL entry with standardized fields:
- `stimulus_text`: The full financial analysis, investment memorandum, or valuation commentary (minimum 350 characters)
- `embedded_error_type`: One of `accounting_logic`, `valuation_fallacy`, `factual_regulatory`, `statistical_distortion`
- `embedded_error_location`: Sentence-level coordinate of the embedded financial distortion
- `embedded_error_description`: Ground-truth error specification for scoring
- `correct_detection_response`: Criteria required for a full-credit participant detection
- `distractor_features`: Institutional financial terminology, professional ratios, and executive committee framing
- `difficulty_rationale`: Psychometric and cognitive load rationale
- `item_discrimination_estimate`: Projected point-biserial discrimination coefficient ($0.25 \le D \le 0.60$)
- `experiment_id`: `EXP-04`
- `difficulty`: `medium`

## Scoring Rubric
See [scoring-rubric.md](scoring-rubric.md) for full 3-point ordinal scoring criteria.
