# EXP-04: Fluent Hallucination Detection — Financial & Quantitative Domain
## Scoping Document (Sprint 11)

> **Preview Status:** v0.3-dev preview. Conceptual design and governance scoping only.
> **Operational Gate:** No stimuli generated this sprint. Stimulus generation is explicitly blocked until prerequisites are met.

---

## 1. Domain Definition

EXP-04 extends the HSRI Lane 6 Behavioral Experiment battery into **Quantitative Financial Analysis & Corporate Decision Modeling**. 

This domain assesses how individuals evaluate authoritative, fluent AI-generated financial analyses, investment memoranda, credit underwriting summaries, and valuation models that contain embedded mathematical, accounting, or regulatory distortions.

Modern corporate workflows increasingly delegate financial summarization, discounted cash flow (DCF) drafting, and ratio analysis to generative LLMs. Because financial text frequently integrates authoritative quantitative tables with fluent prose, automation bias (complacency toward fluent, structured outputs) represents a critical operational risk.

---

## 2. Target Population

- **Target Cohort:** Adults possessing foundational numeracy and business/financial literacy (e.g., business administration undergraduates, MBA students, corporate financial analysts, retail investors, operations managers).
- **Exclusion Criteria:** Certified Financial Analysts (CFA charterholders), licensed CPAs, professional forensic auditors, or individuals without basic familiarity with standard financial statements (Income Statement, Balance Sheet, Cash Flow Statement).
- **Recruitment Venues:** Academic research participant pools (e.g., Prolific academic filters, university behavioral labs) filtered for introductory finance or accounting coursework completion.

---

## 3. Permitted Error Types

Stimulus generation for EXP-04 will permit four tightly controlled error types:

| Error Type | Description | Illustrative Example |
|---|---|---|
| `accounting_logic` | Inversion of standard accounting identities or cash flow classifications under GAAP/IFRS. | Classifying principal debt repayment as an operating cash outflow rather than a financing cash outflow, artificially depressing reported free cash flow. |
| `valuation_fallacy` | Methodological contradictions in corporate valuation or capital budgeting. | Discounting nominal projected cash flows using a real (inflation-adjusted) Weighted Average Cost of Capital (WACC), or setting terminal growth rates higher than long-term GDP growth. |
| `factual_regulatory` | Erroneous claims regarding mandatory regulatory thresholds, tax rules, or statutory covenants. | Asserting that Basel III capital requirements permit Tier 1 common equity ratios below 4.5%, or misstating SEC Regulation S-X disclosure mandates. |
| `statistical_distortion` | Quantitative misattributions in algorithmic backtests, historical volatility, or risk metrics. | Asserting that an investment strategy achieved a Sharpe ratio of 3.2 while defining the metric as return divided by variance rather than standard deviation, or omitting survivorship bias adjustments. |

---

## 4. Proposed Risk & Ethics Concerns

1. **Simulated Investment Advice Risk:** Participants must not perceive experimental stimuli as actionable financial advice or investment recommendations.
   - *Mitigation:* All scenarios must utilize fictitious entity names (e.g., "Apex Industrial Holdings Ltd."), hypothetical currencies or standardized units, and explicit experimental watermarks.
2. **Real-World Market & Commercial Defamation Risk:** Real corporate entities, public tickers, or active securities must never be referenced.
   - *Mitigation:* Automated regex validation and entity scrubbing on all generated stimuli prior to storage.
3. **Cognitive Burden & Performance Anxiety:** Quantitative evaluation tasks can induce mathematics anxiety, potentially inflating miss rates for non-cognitive reasons.
   - *Mitigation:* Standardized pre-task practice items, calibration on low-stakes comprehension checks, and explicit instructions that the study evaluates AI text fluency rather than individual math prowess.
4. **IRB Ethical Classification:** Minimal risk under standard institutional review guidelines, provided deception (embedded errors) is resolved through debriefing.

---

## 5. Explicit Prerequisites Before Stimulus Generation Begins

Stimulus generation for EXP-04 must NOT commence until all five of the following conditions are satisfied:

1. **Empirical Calibration Data from EXP-01 / EXP-02:** Human participant pilot data from EXP-01 (legal) and EXP-02 (clinical) must be collected and analyzed to empirically calibrate the relationship between synthetic persona discrimination ($D$) and human error detection rates.
2. **Domain Specialist Reviewer Sign-Off:** A designated finance professional (CFA charterholder, CPA, or academic finance faculty member) must review and approve the stimulus generation template and error scoring rubric.
3. **Entity Scrubbing & De-identification Pipeline:** An automated check ensuring zero overlap between stimulus text and active SEC EDGAR corporate filings or public ticker symbols must be integrated into `scripts/stimulus_generator.py`.
4. **Institutional Review Board (IRB) Protocol Submission:** Formal human subjects research protocol including informed consent and post-experiment debriefing templates must be drafted and submitted.
5. **Human Maintainer Sign-Off:** Explicit maintainer directive recorded in sprint planning authorizing the transition from scoping to stimulus authoring.
