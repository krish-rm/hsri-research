# Indicator Coverage Audit (End-to-End)

**Repository:** `hsri-research`  
**Date:** September 2026  
**Auditor:** Antigravity Data Integrity Pass  
**Reference File:** `data/indicators.csv` (30 indicators: 17 Retained, 7 Context-only, 6 Rejected)

---

## 1. Executive Summary of Audit Findings

1. **No Raw Microdata Checked into Repository:**  
   The repository contains `data/observations.csv` (780 pre-aggregated rows: 39 countries × 20 indicators), but **no underlying primary survey microdata, official source extracts, or survey response files** are checked in.
2. **Aggregated Coverage = 1.0 is an Artifact of Input Imputation:**  
   Every one of the 39 scored countries in `data/observations.csv` has a populated float value for all 20 listed indicators. Consequently, `scripts/index_construction.py` calculated coverage as `count(axis=1) / len(available_indicators)`, which mechanically yielded `1.0` (100%) for all four pillars across all 39 countries.
3. **Severe Geographical Mismatches in Survey Sources:**  
   - **European Media Literacy Index (`META_COG_002`):** Only surveys European nations. Non-European nations in the benchmark (USA, CAN, JPN, KOR, AUS, NZL, SGP, TWN, HKG, ISR) have imputed/synthetic numbers without disclosure.
   - **KPMG–Melbourne AI Trust Study (`CAL_TRUST_001`):** Only surveyed 17 nations in its 2023 wave. All 39 countries in `observations.csv` carry values.
   - **Reuters Institute Digital News Report (`META_COG_003`):** Does not cover all 39 benchmark nations (e.g., Cyprus, Iceland, Malta, Luxembourg lack full independent survey samples).
   - **Stanford AI Index Legislative Tracker (`DEC_AGY_005`):** Covers ~25-30 nations with formalized legislation, not all 39 uniformly.
4. **Audit Conclusion:**  
   The claim of `coverage = 1.0` (100% completeness) cannot be empirically substantiated from what is checked into the repository. Per R1 and R2, all `coverage = 1.0` claims must be removed, replaced with "Unverified / Not Available" status, and the preview nature of the dataset must be plainly stated.

---

## 2. Comprehensive Audit Matrix (30 Indicators)

| # | Indicator ID | Indicator Name | Pillar | Role | Raw Data in Repo | Source Reality vs 39 Nations | Evidence Finding | Recommendation |
| :- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `AI_LIT_001` | OECD PIAAC Problem Solving | AI_Literacy | Retained | Absent (pre-filled in `observations.csv`) | PIAAC Cycle 1 spans ~38 nations across rounds, but several benchmark nations (e.g. ISL, BGR, ROU, MLT) did not complete all PSTRE modules. | **Coverage Contradicted** | Remove `1.0` coverage claim; mark coverage as unverified in release. |
| 2 | `AI_LIT_002` | PISA Digital Reading Literacy | AI_Literacy | Retained | Absent (pre-filled in `observations.csv`) | Broad OECD coverage, but sub-scale reporting varies across cycles and territories (e.g. CYP). | **Coverage Unverified** | Mark coverage as unverified until primary PISA extracts are added. |
| 3 | `AI_LIT_003` | LinkedIn Global Skills Gap Index | AI_Literacy | Context-only | Absent | Proprietary platform data; not in `observations.csv`. | **Raw Data Absent** | Retain as unrated context indicator; do not compute coverage. |
| 4 | `AI_LIT_004` | Tertiary STEM Enrollment | AI_Literacy | Retained | Absent (pre-filled in `observations.csv`) | UNESCO UIS data has variable reporting years (2018-2023) across countries. | **Coverage Unverified** | Remove `1.0` coverage; disclose reporting year variance. |
| 5 | `AI_LIT_005` | ITU Digital Skills Index | AI_Literacy | Retained | Absent (pre-filled in `observations.csv`) | ITU collects skills indicators via national statistical offices with significant data gaps. | **Coverage Unverified** | Mark coverage as unverified; remove asserted 100%. |
| 6 | `CAL_TRUST_001` | KPMG-Melbourne AI Trust Study | Trust_Attitudes | Context-only | Absent (pre-filled in `observations.csv`) | Surveyed only 17 countries globally in 2023 wave. 39 countries populated in `observations.csv`. | **Coverage Contradicted** | Exclude from core readiness; document that 22 countries are imputed/unobserved. |
| 7 | `CAL_TRUST_002` | Ipsos AI Monitor | Trust_Attitudes | Context-only | Absent | Survey covers ~28-31 nations, not all 39 benchmark nations. | **Raw Data Absent** | Retain as context-only; no coverage claim. |
| 8 | `CAL_TRUST_003` | Pew Research AI Attitudes | Trust_Attitudes | Context-only | Absent | Irregular multi-country waves (primarily US + select nations). | **Raw Data Absent** | Retain as context-only; no coverage claim. |
| 9 | `CAL_TRUST_004` | Edelman Trust Barometer AI | Trust_Attitudes | Context-only | Absent | Commercial survey covering ~28 countries. | **Raw Data Absent** | Retain as context-only; no coverage claim. |
| 10 | `CAL_TRUST_005` | Lloyd's Register World Risk Poll | Trust_Attitudes | Rejected | Absent | Gallup-administered risk poll; rejected during construct audit. | **Raw Data Absent** | Keep Rejected status; excluded from scoring. |
| 11 | `META_COG_001` | PISA Fact vs Opinion | Critical_Discernment | Retained | Absent (pre-filled in `observations.csv`) | OECD PISA 2018 reading module evaluated 21-point task across OECD subset. | **Coverage Unverified** | Mark coverage as unverified; remove `1.0` claim. |
| 12 | `META_COG_002` | European Media Literacy Index | Critical_Discernment | Retained | Absent (pre-filled in `observations.csv`) | Exclusively covers European states. Non-European benchmark nations (USA, CAN, AUS, JPN, etc.) have no native EMLI rating. | **Coverage Contradicted** | Disclose imputation for non-European nations; remove `1.0` pillar coverage. |
| 13 | `META_COG_003` | Reuters Institute Digital News Report | Critical_Discernment | Retained | Absent (pre-filled in `observations.csv`) | Covers 46 markets, but lacks sample for several small benchmark economies (e.g. ISL, MLT, CYP). | **Coverage Contradicted** | Mark coverage as unverified; note source sample boundaries. |
| 14 | `META_COG_004` | MediaWise Digital Literacy | Critical_Discernment | Rejected | Absent | US-centric youth initiative; rejected for lack of international standardization. | **Raw Data Absent** | Keep Rejected status; excluded from scoring. |
| 15 | `DEC_AGY_001` | Worldwide Governance Indicators | Institutional_Governance | Retained | Absent (pre-filled in `observations.csv`) | World Bank covers >200 economies with high statistical coverage. | **Coverage Plausible but Unverified** | Remove false 1.0 assertion; note primary extract needed. |
| 16 | `DEC_AGY_002` | V-Dem Democracy Indices | Institutional_Governance | Retained | Absent (pre-filled in `observations.csv`) | V-Dem covers ~180 countries using expert coder aggregation. | **Coverage Plausible but Unverified** | Document lack of checked-in primary microdata. |
| 17 | `DEC_AGY_003` | Freedom House Freedom in the World | Institutional_Governance | Retained | Absent (pre-filled in `observations.csv`) | Global coverage of 195+ countries and territories. | **Coverage Plausible but Unverified** | Remove false 1.0 assertion; provide provenance link. |
| 18 | `DEC_AGY_004` | OECD AI Policy Observatory | Institutional_Governance | Retained | Absent (pre-filled in `observations.csv`) | Active tracking for OECD member states; partner/non-member coverage varies. | **Coverage Unverified** | Mark coverage as unverified across non-OECD economies. |
| 19 | `DEC_AGY_005` | Stanford AI Index Policy Section | Institutional_Governance | Retained | Absent (pre-filled in `observations.csv`) | Legislative tracking covers ~25-30 economies with specific AI policy bills. | **Coverage Contradicted** | Mark coverage as unverified/incomplete; remove 1.0. |
| 20 | `ATT_WELL_001` | Daily Screen Time Average | Wellbeing_Context | Context-only | Absent (pre-filled in `observations.csv`) | Commercial telemetry; uneven national sample sizes and opt-in bias. | **Coverage Unverified** | Keep as context-only; disclose sampling limitations. |
| 21 | `ATT_WELL_002` | WHO Mental Health Prevalence | Wellbeing_Context | Context-only | Absent (pre-filled in `observations.csv`) | Global Health Observatory estimates; statistical modeling rather than direct annual censuses. | **Coverage Unverified** | Keep as context-only; note estimation status. |
| 22 | `ATT_WELL_003` | HBSC Adolescent Wellbeing | Wellbeing_Context | Rejected | Absent | WHO European/North American regional focus only; rejected. | **Raw Data Absent** | Keep Rejected status; excluded from scoring. |
| 23 | `VALUE_001` | WVS Tradition vs Secularism | Value_Clarity | Rejected | Absent | World Values Survey; rejected due to normative variance and wave lag. | **Raw Data Absent** | Keep Rejected status; excluded from scoring. |
| 24 | `VALUE_002` | EVS Values Importance Rankings | Value_Clarity | Rejected | Absent | European Values Study; European focus; rejected. | **Raw Data Absent** | Keep Rejected status; excluded from scoring. |
| 25 | `VALUE_003` | ESS Values Dimension | Value_Clarity | Rejected | Absent | European Social Survey; European focus; rejected. | **Raw Data Absent** | Keep Rejected status; excluded from scoring. |
| 26 | `ENAB_001` | Oxford Insights AI Readiness | Digital_Infrastructure | Retained | Absent (pre-filled in `observations.csv`) | Covers ~180 countries across infrastructure and government capacity. | **Coverage Plausible but Unverified** | Mark coverage as unverified; remove 1.0 assertion. |
| 27 | `ENAB_002` | IMF AI Preparedness Index | Digital_Infrastructure | Retained | Absent (pre-filled in `observations.csv`) | Covers 174 countries across digital infrastructure and human capital. | **Coverage Plausible but Unverified** | Remove 1.0 assertion; note primary source extract needed. |
| 28 | `ENAB_003` | ITU Development Index (IDI) | Digital_Infrastructure | Retained | Absent (pre-filled in `observations.csv`) | Covers ~160 economies with standardized telecommunication metrics. | **Coverage Plausible but Unverified** | Mark coverage as unverified; remove 1.0 assertion. |
| 29 | `ENAB_004` | World Bank Digital Adoption Index | Digital_Infrastructure | Retained | Absent (pre-filled in `observations.csv`) | Historic composite covering business, people, and government digital adoption. | **Coverage Plausible but Unverified** | Mark coverage as unverified; remove 1.0 assertion. |
| 30 | `ENAB_005` | WEF Technology Adoption Index | Digital_Infrastructure | Retained | Absent (pre-filled in `observations.csv`) | World Economic Forum Executive Opinion Survey; ~140 countries. | **Coverage Plausible but Unverified** | Mark coverage as unverified; remove 1.0 assertion. |

---

## 3. Recommendations & Action Plan for Pass

1. **Remove False Coverage Rates:**  
   Across `final_country_scores.csv` and `pillar_scores.csv`, replace the mechanical `1.0` coverage figures with `Unverified` or plain text disclosure that data completeness has not been verified from primary microdata for this preview release.
2. **Harmonize Site Copy:**  
   Replace all claims of "100% completeness" and "780 validated empirical observations with 100% completeness" across `index.astro`, `data.astro`, and `MethodologyOverview.svelte` with honest statements: data completeness is exploratory/unverified, with survey indicators subject to geographic boundaries and imputation.
3. **Data Provenance Transparency:**  
   On country profile pages, explicitly list which indicators have direct observed sources versus which are imputed or unverified, ensuring auditability for every country score.
