# Remediation Inventory: Data Pipeline, Data Artifacts, and Site Templates

**Repository:** `hsri-research`  
**Date:** September 2026  
**Purpose:** Comprehensive inventory of all files producing, storing, or displaying country scores, pillar scores, coverage percentages, country counts ("Countries Rated"), and research publication citations.

---

## 1. Data Pipeline & Analytical Scripts

| File Path | Description & Role | Key Outputs / Metrics Handled |
| :--- | :--- | :--- |
| `scripts/index_construction.py` | Primary composite index engine implementing OECD/JRC handbook aggregation. Calculates pillar scores, coverage ratios, non-compensatory thresholds, and bootstrap uncertainty. | Generates `data/final_country_scores.csv` and `data/pillar_scores.csv`. Calculates pillar coverage (`count(axis=1) / len(indicators)`). |
| `scripts/data_normalization.py` | Reads empirical observations, performs z-score / min-max normalization, applies directional alignment. | Reads `data/observations.csv`, outputs `data/normalized_indicators.csv`. |
| `scripts/statistical_validation.py` | Computes internal consistency (Cronbach's alpha), inter-item correlation, PCA factor loading, and sensitivity tests on normalized data. | Outputs `research/statistical_validation_report.txt`. |
| `scripts/exposure_modeling.py` | Integrates domain exposure indicators and calculates composite exposure and readiness-exposure gaps. | Outputs `data/composite_exposure_scores.csv` and `data/readiness_exposure_gap.csv`. Uses heuristic fallback formulas for unmodeled countries. |
| `scripts/labor_exposure_model.py` | Models occupational exposure shares (High, Medium, Low) and automation risk. | Outputs `data/labor_vulnerability.csv` and `data/labor_crossing_years.csv`. Contains hardcoded shares for 15 countries and heuristic archetypes for others. |
| `scripts/timeline_synthesis.py` | Parameterizes milestone capabilities across Plateau, Steady, and Takeoff scenarios. | Generates `data/forecast_cdfs.json` and `data/scenario_crossing_years.csv`. |
| `scripts/export_web_data.py` | Export utility gathering analytical CSVs and JSONs, formatting payloads for the Astro web application. | Generates `country_scores.json`, `country_profiles.json`, `indicators.json`, `timeline_data.json` into `site-astro/src/data/` and `site-astro/public/data/`. Copies CSV artifacts. |

---

## 2. Static Data Files (CSVs and JSONs)

| File Path | Description | Issues / Audit Findings |
| :--- | :--- | :--- |
| `data/final_country_scores.csv` | Final evaluated scores for 39 benchmark nations with 4 pillar scores and 4 pillar coverage columns. | **Fabricated Coverage:** Every country has `1.0` across all 4 pillars.<br>**False Precision:** Scores carry up to 16 decimal places (e.g. `0.9890187172744423`). |
| `data/pillar_scores.csv` | Breakdown of pillar scores, coverage ratios, indicator counts, and sufficiency flags. | All 39 countries show `coverage = 1.0`, `sufficient = True`, and 16-decimal float precision. |
| `data/normalized_indicators.csv` | Standardized values for 17 retained indicators across 39 countries. | Complete matrix with zero missing values, resulting from pre-filled/imputed input observations. |
| `data/observations.csv` | 780 rows (39 countries × 20 indicators). | Contains values for all 39 countries even for surveys with restricted geographical coverage (e.g. KPMG AI Trust, EMLI). Raw microdata/survey responses are absent. |
| `data/coverage-by-country.csv` | 145 countries analyzed for empirical coverage across indicator categories. | **Denominators:** Lists 86 "Not rated", 37 "Partial rating", 22 "Context-only" (total: 145 countries). The "86" count was erroneously displayed as "Rated 86/195" on the site banner. |
| `data/readiness_exposure_gap.csv` | Readiness, composite exposure, gap, and gap status for 39 nations. | Carries 16-decimal readiness floats; exposure derived from stylized simulation formulas. |
| `data/indicators.csv` | Master catalog of 30 indicators (17 Retained, 7 Context-only, 6 Rejected). | Documents indicators, source organizations, and roles. |
| `site-astro/public/data/*.csv` | Public downloadable copies of all data CSVs. | Mirrors data folder CSVs including false precision and `coverage = 1.0`. |
| `site-astro/src/data/country_scores.json`<br>`site-astro/public/data/country_scores.json` | JSON consumed by Astro pages containing metadata, pillars, rankings, and country objects. | `avgScore` is 53.8, `totalCountries` is 39. |
| `site-astro/src/data/country_profiles.json`<br>`site-astro/public/data/country_profiles.json` | Detailed country profiles keyed by ISO3 code. | Contains scores, ranks, qualitative narratives, and SWOT assessments. |
| `site-astro/src/data/timeline_data.json`<br>`site-astro/public/data/timeline_data.json` | Timeline scenario probability curves and CDF parameters. | Carries floating point values up to 17 decimal places. |

---

## 3. Site Page Templates & Svelte Components (`site-astro/`)

| File Path | Component / Section | Claims & Displays Audited |
| :--- | :--- | :--- |
| `site-astro/src/components/HSRIHeader.svelte` | Persistent Header & Stats Bar | **Denominators:** Shows `stats.ratedCountries` (86) and `stats.totalCountries` (195) labeled as "Countries Rated 86/195".<br>**Average Score:** Hardcoded as `62.4` (conflicts with actual data mean `53.8`). |
| `site-astro/src/pages/index.astro` | Homepage Hero & Stats Section | Displays "39 Nations Fully Rated", "across 39 nations", and stats grid showing 39 countries profiled. Does not disclose high-income/OECD selection bias. |
| `site-astro/src/pages/countries.astro` | Countries Index Page | Displays "All 39 Benchmark Country Profiles". Lacks clear disclosure regarding the OECD/high-income composition of the preview sample. |
| `site-astro/src/pages/countries/[id].astro` | Individual Country Profile Page | Displays `#{country.rank} / 39`, pillar scores as percentages, exposure and gap metrics. Currently lacks an auditable indicator-level data presence breakdown. |
| `site-astro/src/pages/data.astro` | Data Download & Provenance Page | **False Scope:** Claims sample covers "39 benchmark nations (OECD, G7, BRICS+, regional anchors)" — BRICS+ are not scored.<br>**False Completeness:** Claims "100% harmonized (780 empirical observations across 20 indicators)".<br>**Dead Publications:** Lists 3 fictional papers linking to `#`:<br>1. *Global Readiness for Superintelligence: A Multi-Dimensional Assessment*<br>2. *Cross-National Patterns in AI Preparedness*<br>3. *Methodology for the Human Superintelligence Readiness Index*<br>**Dead Links:** 4 support links pointing to `#`. |
| `site-astro/src/components/DataExplorer.svelte` | Interactive Dataset Explorer | Lists 6 datasets with country counts (39), pillar counts, and direct download links. |
| `site-astro/src/components/MethodologyOverview.svelte` | Methodology Overview Component | **Completeness Claim:** Claims "780 empirical observations validated for 39 benchmark nations with 100% completeness" and "100% Empirical Completeness".<br>**Cronbach's Alpha:** Tab labeled `Validation (α > 0.90)`; four cards claiming unverified `α = 0.948`, `0.941`, `0.932`, `0.947`. |
| `site-astro/src/components/TimelinePreview.svelte` | Timeline Preview & Status Component | **False Precision / Unsourced Interval:** Hardcodes `Confidence Interval: ±2 years` with no documented empirical estimation method. |
| `site-astro/src/components/CountryList.svelte` | Filterable Country Grid | Renders 39 country cards, sorting by rank, score, exposure, and filtering by region/band. |
| `site-astro/src/components/CountryComparisonTool.svelte` | Side-by-Side Comparison Tool | Compares 39 countries across pillar scores and radar charts. |
| `site-astro/src/components/WeightCalculator.svelte` | Interactive Weight Simulator | Allows adjusting pillar weights (0-100%) to simulate changes in rank across the 39 countries. |
| `site-astro/src/components/ScoreLeaderboard.svelte` | Top-10 Leaderboard Component | Renders top 10 ranked countries on homepage. |
