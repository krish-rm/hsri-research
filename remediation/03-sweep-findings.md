# Comprehensive Sweep Findings: Unsupported Statistics, Heuristics, and False Claims

**Repository:** `hsri-research`  
**Date:** September 2026  
**Auditor:** Antigravity Data Integrity Pass  
**Guiding Principle:** Find every place where the site states something with more certainty or completeness than the underlying data supports. Log every finding, whether fixed immediately or tracked as an open limitation.

---

## 1. Summary of Sweep Findings

| # | Item / Claim Audited | Location(s) in Codebase | Source / Empirical Status in Repo | Action Taken / Recommendation |
| :- | :--- | :--- | :--- | :--- |
| 1 | **Validation Claim (α > 0.90)** | `MethodologyOverview.svelte`<br>(Tab label, lines 61, 131, 350-372) | **Unsubstantiated Mock Numbers:** The component hardcodes `α = 0.948`, `0.941`, `0.932`, `0.947` (labeled "Outstanding"). `statistical_validation.py` computed different values (0.930, 0.905, 0.969, 0.962) on `normalized_indicators.csv` (N=39), which was built from pre-filled imputed observations. | **Fixed:** Relabeled tab to "Statistical Diagnostics (Exploratory)". Replaced fake hardcoded values with actual script values, with prominent disclosure that high collinearity stems from a high-income 39-country sample with unverified input completeness. |
| 2 | **Confidence Interval: "±2 years"** | `TimelinePreview.svelte`<br>(lines 318-321) | **Arbitrary Heuristic:** Hardcoded string `±2 years`. No empirical resampling, bootstrap, or econometric uncertainty model produced this interval. In `docs/14-timeline-definitions.md`, intervals were assigned qualitatively. | **Fixed:** Replaced `±2 years` with "No formal statistical interval computed yet (exploratory heuristic)". |
| 3 | **National Exposure & Labor Vulnerability Percentages** | `scripts/exposure_modeling.py`<br>`scripts/labor_exposure_model.py`<br>`countries/[id].astro`<br>`country_scores.json` | **Stylized Proxy Simulation:** Not derived from national labor force microdata or ISCO employment censuses. `labor_exposure_model.py` hardcodes shares for 15 countries and uses readiness-binned archetype shares for the remaining 24. Domain exposures use synthetic `(1 - readiness)` formulas. | **Fixed:** Added explicit disclosure on Country Profile, Methodology, and Compare pages that exposure and labor vulnerability metrics represent stylized simulation proxies rather than direct labor census observations. |
| 4 | **Inclusion of "BRICS+" in Scored Cohort** | `data.astro`<br>(line 126) | **False Claim:** Page claims sample includes "39 benchmark nations (OECD, G7, BRICS+, regional anchors)". Not a single BRICS member (Brazil, Russia, India, China, South Africa) is scored in the 39-country dataset. | **Fixed:** Corrected copy to "39 benchmark nations (OECD, EU, and high-income Asia-Pacific economies; BRICS+ are unrated in this release due to source coverage gaps)". |
| 5 | **"100% Empirical Completeness" Claims** | `data.astro` (line 134)<br>`MethodologyOverview.svelte` (lines 124, 254) | **Misleading Assertion:** Asserts 100% data completeness based on `observations.csv` being fully populated, ignoring that survey indicators (EMLI, KPMG, Reuters) have severe geographic omissions and were imputed. | **Fixed:** Relabeled to "Exploratory sample (780 populated observations across 39 countries; primary microdata unverified)". |
| 6 | **Fabricated Average Score (62.4)** | `HSRIHeader.svelte`<br>(line 21) | **Fictitious Constant:** Hardcoded `avgScore: 62.4`. The actual mathematical mean of the 39 scored countries in `final_country_scores.csv` and `country_scores.json` is `53.8`. | **Fixed:** Updated to `53.8` to match the empirical data mean. |
| 7 | **Three Fictional Research Publications** | `data.astro`<br>(lines 145-165) | **Dead Citations:** Listed three papers with `#` links:<br>1. *Global Readiness for Superintelligence: A Multi-Dimensional Assessment*<br>2. *Cross-National Patterns in AI Preparedness*<br>3. *Methodology for the Human Superintelligence Readiness Index*<br>None of these exist. | **Fixed:** Removed the placeholder entries and added an honest notice: "No peer-reviewed publications use this dataset yet." |
| 8 | **Dead Support & Community Links** | `data.astro`<br>(lines 170-192) | **Nonexistent Pages:** Four `#` links for Documentation, Tutorials, Community Forum, and Support. | **Fixed:** Removed placeholder forum/tutorials. Linked Documentation to `${base}/methodology/` and Contact/Bug Reports to the official GitHub repository Issues page. |
| 9 | **Floating Point False Precision (Up to 16 Decimals)** | `data/final_country_scores.csv`<br>`data/pillar_scores.csv`<br>`data/readiness_exposure_gap.csv`<br>`data/timeline_data.json` | **False Precision:** Storing and exporting numbers like `0.9890187172744423` conveys false scientific precision when input data is rough, unverified survey estimates. | **Fixed:** Standardized all exported scores and gap values to 2 decimal places (or 4 decimals for raw normalized [0, 1] index values). |
| 10 | **Pillar Coverage = 1.0 Assertion** | `data/final_country_scores.csv`<br>`data/pillar_scores.csv`<br>`scripts/index_construction.py` | **Artifact of Pre-filled Inputs:** Every country showed `1.0` coverage because the script evaluated missingness on a pre-filled matrix. | **Fixed:** Relabeled pillar coverage in output CSVs and data tables to indicate unverified completeness. |

---

## 2. Issues Logged for Future Releases (Outside Scope of Current Pass)

The following items were identified during the sweep but involve introducing new methodologies, which is outside the non-negotiable scope for this pass:
1. **Primary Microdata Pipeline:**  
   The repository needs automated scrapers/fetchers that pull primary survey tables directly from OECD (PIAAC/PISA), ITU, UNESCO, and Council of Europe, saving raw dated extracts into `data/raw/` so coverage can be dynamically verified.
2. **National Labor Force Census Ingestion:**  
   Replace the stylized 3-tier occupational exposure model with empirical ILOSTAT or national bureau of statistics employment tables (e.g. BLS, Eurostat) mapped to AI exposure rubrics (e.g. Felten et al. or Eloundou et al.).
3. **Global South Data Harmonization:**  
   Expand indicator selection to include metrics with broad coverage across Latin America, Sub-Saharan Africa, and South Asia (e.g., World Bank ASPIRE social protection, ITU connectivity surveys) to enable legitimate global benchmark scores beyond high-income OECD economies.
