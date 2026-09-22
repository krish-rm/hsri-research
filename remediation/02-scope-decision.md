# Country Scope Reconciliation & Denominators Decision

**Repository:** `hsri-research`  
**Date:** September 2026  
**Auditor:** Antigravity Data Integrity Pass  
**Reference Files:** `data/coverage-by-country.csv`, `data/final_country_scores.csv`, `site-astro/src/components/HSRIHeader.svelte`

---

## 1. The Denominator Conflict

Across the live repository and site templates, three conflicting denominators appeared without reconciliation:
- **195:** Shown on the persistent header stats banner ("Countries Rated 86/195").
- **86:** Shown on the persistent header stats banner ("Countries Rated 86/195").
- **39:** Shown on the homepage hero, the countries page ("All 39 Benchmark Country Profiles"), the data explorer, and in `data/final_country_scores.csv`.

---

## 2. Forensic Reconstruction: What Did Each Number Actually Mean?

By auditing the repository data pipeline and historical CSVs, each number was definitively traced:

### A. The "195" Figure
- **Definition:** The standard international count of recognized sovereign states (193 United Nations member states + 2 permanent observer states: Holy See and State of Palestine).
- **Function in HSRI:** Represents the ultimate global universe of nations that an ideal, complete index would evaluate.

### B. The "86" Figure (The Inverted Metric Bug)
- **File of Origin:** `data/coverage-by-country.csv`
- **What it actually is:** In `coverage-by-country.csv`, exactly 145 nations were audited for data availability across pillars. The breakdown of `overall_status` is:
  - `Not rated`: **86 countries**
  - `Context-only`: **22 countries**
  - `Partial rating`: **37 countries**
  - **Total:** 145 countries (86 + 22 + 37 = 145)
- **The Bug:** The author of `HSRIHeader.svelte` inspected `coverage-by-country.csv`, took the number **86** (which was the count of **UNRATED / INSUFFICIENT DATA** countries), and mistakenly placed it into the header banner as:
  ```svelte
  ratedCountries: 86, totalCountries: 195 // "Countries Rated 86/195"
  ```
  **The banner literally inverted the meaning of 86**, displaying unrated countries as rated countries!

### C. The "39" Figure
- **File of Origin:** `data/final_country_scores.csv`
- **What it actually is:** The actual empirical cohort that received headline scores across the four pillars.
- **Geographic Composition:** All 39 nations are OECD members, European Union states, or high-income Asia-Pacific economies (e.g. Australia, Canada, Germany, Japan, Singapore, South Korea, United Kingdom, United States).
- **Selection Bias:** Zero countries from Sub-Saharan Africa, South Asia, Southeast Asia (except Singapore), or Latin America appear in the scored set.

---

## 3. Scope Reconciliation & Definitional Standard

To comply with **Rule R1** (Fix the claim or fix the data) and **Rule R6** (One country list used consistently), all three counts are now defined, harmonized, and presented together wherever country counts are displayed:

1. **39 Benchmark Rated Countries:**  
   "39 of 195 recognized nations receive a preliminary benchmark score in this release."
2. **59 Countries with Partial/Context Data:**  
   "A further 59 countries have partial or contextual data in our preliminary coverage assessment (37 partial, 22 context-only)."
3. **86 Evaluated Countries Unrated:**  
   "86 evaluated countries have insufficient data across core pillars and remain unrated."
4. **195 Global Sovereign Nations:**  
   The total international denominator.

---

## 4. Required Disclosures & Language

### A. Persistent Header Banner (`HSRIHeader.svelte`)
- Display format:
  - Label: **Benchmark Scope**
  - Value: **39 / 195**
  - Subtitle / Hover details: "39 benchmarked (high-income/OECD preliminary sample); 59 partial, 86 unrated of 195 global nations."
  - Correct Average Score: **53.8** (the empirical mean of the 39 scored countries, replacing the fabricated 62.4).

### B. Country List & Methodology Pages (`countries.astro`, `index.astro`, `data.astro`)
The following mandatory disclosure sentence must accompany every country list:
> **Scope & Geographic Limitation:**  
> "The current preview benchmark evaluates 39 nations, heavily weighted toward high-income and OECD economies. This is a coverage limitation of currently available international empirical data sources, not a judgment about other countries' readiness. In our coverage assessment of 145 countries, 59 possess partial or contextual data, while 86 evaluated countries remain unrated."
