# Power Analysis & Sample Size Determination (EXP-02)

> **PREVIEW NOTICE: HSRI v0.3.0-dev**
> This research document is an exploratory artifact from the Human Superintelligence Readiness Index (HSRI) behavioral lab pipeline. Synthetic-persona pilots test stimulus behavior only and do not provide evidence about human cognition. Stimuli cleared for IRB submission. Not validated on human participants.

## Experimental Design
Between-subjects randomized comparison of error detection rates across exposure framing conditions (AI-generated clinical draft with embedded error vs. clinician-reviewed control).

## Statistical Hypotheses & Test Family
- **Primary Endpoint:** Standardized error detection score per item (0–2 scale) and overall detection rate across conditions.
- **Statistical Test:** Two-sample independent $t$-test (two-tailed) per stimulus item, supplemented by logistic regression on binary detection status.
- **Type I Error Rate ($\alpha$):** 0.05 (two-tailed, $z_{0.025} = 1.96$).
- **Statistical Power ($1 - \beta$):** 0.80 ($z_{0.20} = 0.84$).

## Effect Size Rationale
Target effect size is set at **Cohen's $d = 0.35$** (a conventional small-to-medium effect size in psychological and automation-bias research; Goddard et al., 2012; Parasuraman & Riley, 1997).

> [!NOTE]
> **Literature-Derived Assumption vs. Pilot Data:**
> The effect size $d = 0.35$ is strictly an assumption derived from the empirical human-automation interaction literature. It is **not** derived from HSRI synthetic-persona pilot runs. Point-biserial discrimination coefficients from synthetic LLM pilots ($D = 0.61–0.87$) reflect prompted model behavioral separation and do not represent human effect size estimates.

## Sample Size Calculation
$$N_{\text{group}} = \left\lceil 2 \times \left( \frac{z_{\alpha/2} + z_{\beta}}{d} \right)^2 \right\rceil$$

For $d = 0.35$:
$$N_{\text{group}} = \left\lceil 2 \times \left( \frac{1.96 + 0.84}{0.35} \right)^2 \right\rceil = \lceil 2 \times (8.0)^2 \rceil = \lceil 2 \times 64 \rceil = 128$$

Accounting for an anticipated $5\%$ participant attrition rate (incomplete responses, failed attention checks), the recommended sample size is **$N = 130$ per condition**, yielding a total planned enrollment of **$N = 260$ participants**. With 3 items administered per participant, this produces **$780$ participant-item evaluation observations**.

## Power Sensitivity Table across Effect Sizes
The table below illustrates sample size requirements across plausible effect size assumptions at $\alpha = 0.05$ (two-tailed) and $80\%$ statistical power:

| Target Effect Size (Cohen's $d$) | Calculated $N$ per Group | Total $N$ Required | Total Observations (3 items) | Recommended Enrollment (+5% attrition) |
|---|---|---|---|---|
| **$d = 0.25$** (Small) | 251 | 502 | 1,506 | 265 per group (530 total) |
| **$d = 0.30$** (Small–Medium) | 175 | 350 | 1,050 | 185 per group (370 total) |
| **$d = 0.35$** (Benchmark) | 128 | 256 | 768 | **130 per group (260 total)** |
| **$d = 0.40$** (Medium) | 98 | 196 | 588 | 105 per group (210 total) |
