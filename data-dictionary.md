# HSRI Data Dictionary & Schema Reference

Canonical schema documentation for all public datasets published by the **Human Superintelligence Readiness Index (HSRI)** v0.2 release.

All files are distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

---

## 1. Country Readiness Scores (`hsri-country-scores.csv`)

- **File location:** `/hsri-research/downloads/hsri-country-scores.csv`
- **Source repository path:** `data/final_country_scores.csv`
- **Scope:** 39 benchmark economies across OECD and high-income partner nations
- **Dimensions:** 39 rows × 13 columns

| Column | Type | Description | Values / Bounds |
|---|---|---|---|
| `country_iso3` | String (ISO 3166-1 alpha-3) | Three-letter nation identifier | e.g., `USA`, `SGP`, `DEU`, `JPN` |
| `overall_score` | Float | Composite geometric readiness index score normalized to [0, 1] | Range `0.000` to `1.000` (e.g. `0.8217` for Singapore) |
| `core_pillars_available` | Integer | Count of primary readiness pillars with observed empirical data | `4` for all benchmark rated nations |
| `overall_coverage` | Float | Fraction of total indicators observed without structural absence | Range `0.60` to `1.00` (benchmark average $\ge 0.95$) |
| `status` | String | Indicator qualification status | `Rated` |
| `AI_Literacy_score` | Float | Pillar 1: Workforce cognitive skills, problem solving, and technical education | Range `0.000` to `1.000` |
| `AI_Literacy_coverage` | Float | Proportion of Pillar 1 indicators with observed empirical data | Range `0.60` to `1.00` |
| `Critical_Discernment_score` | Float | Pillar 2: Epistemic calibration, fact-checking, and synthetic bias resistance | Range `0.000` to `1.000` |
| `Critical_Discernment_coverage` | Float | Proportion of Pillar 2 indicators observed (0.667 for non-European; 1.00 for EU) | Range `0.667` to `1.000` |
| `Institutional_Governance_score` | Float | Pillar 3: Regulatory agility, algorithmic accountability, and institutional rule of law | Range `0.000` to `1.000` |
| `Institutional_Governance_coverage` | Float | Proportion of Pillar 3 indicators observed | Range `0.80` to `1.00` |
| `Digital_Infrastructure_score` | Float | Pillar 4: Sovereign compute density, high-speed fiber, and clean grid resilience | Range `0.000` to `1.000` |
| `Digital_Infrastructure_coverage` | Float | Proportion of Pillar 4 indicators observed | Range `0.80` to `1.00` |

---

## 2. Normalized Indicators Matrix (`hsri-normalized-indicators.csv`)

- **File location:** `/hsri-research/downloads/hsri-normalized-indicators.csv`
- **Source repository path:** `data/normalized_indicators.csv`
- **Scope:** 39 benchmark economies across 17 retained indicators
- **Dimensions:** 39 rows × 18 columns

Every indicator is direction-adjusted and min-max normalized to $[0.0, 1.0]$. Structural geographic missingness is preserved as `NaN` (never imputed).

| Column | Indicator Name | Source Organization | Scope / Missingness Rule |
|---|---|---|---|
| `country_iso3` | ISO 3166-1 alpha-3 code | ISO | Primary key |
| `AI_LIT_001` | OECD PIAAC Adaptive Problem Solving | OECD PIAAC | Missing for non-participating nations (`NaN`) |
| `AI_LIT_002` | PISA Digital Reading Literacy | OECD PISA | Secondary education youth assessment |
| `AI_LIT_004` | Tertiary STEM Enrollment Ratio | UNESCO UIS | Proportion of graduates in STEM/CS fields |
| `AI_LIT_005` | ITU Digital Skills Index | ITU | National population digital literacy |
| `META_COG_001` | PISA Epistemic Discrimination (Fact vs. Opinion) | OECD PISA | Cognitive discernment in digital text |
| `META_COG_002` | European Media Literacy Index (EMLI) | Open Society Institute Sofia | **European-scope only.** Absent (`NaN`) for non-EU economies |
| `META_COG_003` | Cognitive Reflection & Verification Calibration | Academic & Psychometric Audits | Resistance to automation bias |
| `DEC_AGY_001` | Voice & Accountability | World Bank WGI | Civil liberties & public scrutiny |
| `DEC_AGY_002` | Regulatory Quality | World Bank WGI | State regulatory capability |
| `DEC_AGY_003` | Rule of Law | World Bank WGI | Judicial independence & enforceability |
| `DEC_AGY_004` | Deliberative Democracy Index | V-Dem Institute | Institutional public deliberation quality |
| `DEC_AGY_005` | Government AI Readiness (Governance) | Oxford Insights | National AI regulatory & safety strategy |
| `ENAB_001` | Sovereign Compute Density | Top500 & Hardware Benchmarks | TFLOPS per million capita |
| `ENAB_002` | Fixed Broadband Penetration | ITU / World Bank | Subscriptions per 100 inhabitants |
| `ENAB_003` | Clean Power Grid Stability | International Energy Agency | Low-carbon data center power capacity |
| `ENAB_004` | International Internet Bandwidth | ITU | Megabits per second per user |
| `ENAB_005` | High-Speed Fiber / 5G Penetration | National Telecommunication Regulators | Population access coverage ratio |

---

## 3. Master Evidence Table (`hsri-evidence-table.csv`)

- **File location:** `/hsri-research/downloads/hsri-evidence-table.csv`
- **Source repository path:** `research/evidence/master-evidence-table.csv`
- **Scope:** 44 audited empirical claims underpinning HSRI construct validity
- **Dimensions:** 44 rows × 7 columns

| Column | Type | Description | Example Values |
|---|---|---|---|
| `claim` | String | Proposition regarding automation bias, metacognition, or readiness | e.g., "Adding AI explanations does not consistently reduce user over-reliance..." |
| `page_reference` | String | Methodology document where the claim is operationalized | `docs/03-construct-audit.md; docs/05-measurement-and-experiments.md` |
| `evidence_tier` | String | Epistemic confidence level based on study rigor and replication | `Strong`, `Moderate`, `Preliminary`, `Weak`, `[UNVERIFIED — NEEDS SOURCE]` |
| `source_citation` | String | Primary academic reference in APA format | `Bansal, G., Wu, T. S., et al. (2021). CHI '21, Article 81.` |
| `source_url_or_doi` | String | Permanent Digital Object Identifier (DOI) or canonical research URL | `https://doi.org/10.1145/3411764.3445717` |
| `notes` | String | Psychometric context, sample boundaries, or effect size summary | `Found local feature-importance explanations can induce an illusion of system competence.` |
| `reconciliation_flag` | String | Lane 1 automated literature audit synchronization status | `CURRENT`, `REVIEW_REQUIRED`, `UPGRADE_CANDIDATE` |

---

## 4. Evaluated Unrated Nations Register (`hsri-unrated-nations.csv`)

- **File location:** `/hsri-research/downloads/hsri-unrated-nations.csv`
- **Source repository path:** `data/unrated-nations.csv`
- **Scope:** 86 evaluated economies currently lacking sufficient multi-pillar microdata to receive headline scores
- **Dimensions:** 86 rows × 8 columns

| Column | Type | Description | Values / Bounds |
|---|---|---|---|
| `country_iso3` | String (ISO 3166-1 alpha-3) | Three-letter nation identifier | e.g., `AFG`, `EGY`, `IND`, `NGA`, `SAU` |
| `country_name` | String | Standard international country name | English country name |
| `region` | String | Continental macro-region (UN geoscheme) | `Africa`, `Americas`, `Asia`, `Europe`, `Oceania` |
| `un_subregion` | String | Detailed regional classification | e.g. `Northern Africa`, `Western Asia` |
| `available_pillars` | Integer | Count of pillars with at least one observed empirical indicator | `0`, `1`, or `2` |
| `missing_pillars` | String | Pillars lacking observed empirical microdata | Semicolon-separated pillar names |
| `primary_data_gap` | String | Root cause taxonomy for absence from the rated benchmark | `missing_cognitive_pillars`, `insufficient_source_coverage` |
| `partial_coverage_notes` | String | Specific institutional tracking vs. survey absence notes | Summary of observed source indicators vs. missing microdata |

