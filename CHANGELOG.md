# Changelog

All notable changes to the Human Superintelligence Readiness Index (HSRI) research repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.1] — 2026-09-22: Benchmark Integrity, Coverage Audit & Epistemic Humility Remediation

### Changed
- **Fabricated Coverage Relabeled to Unverified:**
  - Audited all 30 indicators in `data/indicators.csv` against repository contents (`remediation/01-coverage-audit.md`).
  - Disclosed that primary microdata observation extracts are absent from the repository; survey-based indicators (e.g. KPMG Trust, Ipsos AI Monitor, Reuters DNR) cannot cover all 39 countries simultaneously.
  - Replaced fabricated `coverage = 1.0` (100%) claims across `final_country_scores.csv`, `pillar_scores.csv`, and all UI components with explicit `"Unverified"` and `"Data Completeness Unverified"` disclaimers.
  - Added an indicator-by-indicator empirical provenance table to every individual country profile page (`countries/[id].astro`).
- **Country Scope & Denominators Reconciled:**
  - Forensically reconstructed the conflicting denominators: 195 (globally recognized nations), 86 (unrated evaluated nations with insufficient data), 59 (partial/context nations in source matrices), and 39 (retained high-income/OECD benchmark cohort) (`remediation/02-scope-decision.md`).
  - Resolved homepage banner error that previously displayed "Countries Rated 86/195" to truthfully state "39 of 195 Rated (86 Unrated)".
  - Added explicit geographic composition warnings across the homepage, countries directory, and data explorer disclosing that all 39 scored countries are high-income/OECD economies and that Sub-Saharan Africa, South Asia, Southeast Asia, and Latin America are unrated due to data availability constraints.
- **False Precision Eliminated:**
  - Truncated 16-decimal floating-point numbers across the analytical pipeline (`scripts/index_construction.py`, `scripts/exposure_modeling.py`, `scripts/export_web_data.py`), CSV outputs, and JSON bundles to 2 decimal places for 0–100 scale scores and 4 decimal places for 0–1 normalized weights/shares.
- **Dead Links & False Citations Removed:**
  - Removed three placeholder research publications linking to dead `#` anchors on the Data page (`data.astro`).
  - Added explicit disclosure: *"No peer-reviewed publications use this dataset yet."*
  - Replaced dead `#` anchor for documentation with a working route to `/methodology` and replaced contact anchor with a direct link to GitHub Issues.
  - Removed unsupported claim of "BRICS+" coverage.
- **Sweep Findings & Statistical Humility:**
  - Relabeled methodology tab from "Scale Validation (α > 0.90)" to "Diagnostics (Exploratory α)" and replaced hardcoded mock values with true calculated pipeline metrics (`remediation/03-sweep-findings.md`).
  - Added prominent caveats that high Cronbach's alpha values reflect systemic collinearity across wealthy OECD nations rather than psychometric scale validation.
  - Removed deterministic `±2 years` timeline confidence interval from `TimelinePreview.svelte`, relabeling it as an exploratory projection with formal uncertainty quantification pending.
  - Disclosed stylized proxy assumptions in occupational exposure and labor vulnerability simulation models.
- **Empirical Evidence Tracking:**
  - Updated `research/evidence/master-evidence-table.csv` and `evidence/master-evidence-table.csv` with 4 new entries cataloging claims regarding coverage status, scale validation, sample composition, and projection intervals.

## [v0.2.0] — 2026-09-20: Analytical Pipeline, Static Web Portal & Repository Modernization

### Added
- **Full Analytical Pipeline (Phases 0–6):**
  - Harmonized empirical indicator datasets across 39 economies (`data/`).
  - Implemented 5-pillar mathematical index construction with min-max normalization, PCA robustness checks, and scenario cross-point modeling.
  - Generated comprehensive country profiles, SWOT matrices, and narrative evaluations for 39 economies (`research/country_profiles/`, `research/integrated_narratives/`).
  - Added scenario crossing year projections and labor market vulnerability assessments.
- **Production Interactive Web Portal (`site-astro/`):**
  - Built static web application using Astro 7 and Svelte 5 (45 statically generated pages).
  - Implemented interactive country profile pages with SVG radar charts, readiness-exposure gap gauges, and SWOT matrices.
  - Built interactive Head-to-Head Comparison matrix comparing countries across all 5 pillars.
  - Created dynamic Weight Calculator allowing custom pillar weight recalculation on the fly.
  - Integrated full methodology explorer, construct audit, and interactive simulator.
- **Automated Verification & Tests:**
  - Added unit test suite for multi-agent evidence review pipeline (`tests/test_agents.py`).
  - Verified 100% mathematical consistency across pipeline scripts and web data exports.

### Changed
- **Professional Repository Restructuring:**
  - Consolidated scattered research outputs (`country_profiles/`, `integrated_narratives/`, `evidence/`, `not_rated_scenarios/`, `outreach/`) into unified `research/` directory.
  - Relocated agent memory, scan logs, and divergence logs into `hsri_agents/logs/`.
  - Cleaned repository root to standard professional layout (10 directories, 9 standard files).
  - Updated all 16 pipeline scripts and configuration modules to reference new standardized paths.

## v0.1.0-draft — Initial scaffold from merged research report

- Initial public research repository scaffold and static documentation website using MkDocs with Material theme.
- Restructured research synthesis into a 9-page evidence-tiered format across `docs/`.
- Implemented five-tier inline evidence taxonomy with colored badges and explicit `[UNVERIFIED — NEEDS SOURCE]` tags.
- Compiled `evidence/master-evidence-table.csv` auditing 40 distinct empirical claims against verifiable peer-reviewed sources.
- Established repository governance, ethical risk safeguards, CC-BY 4.0 licensing, and Contributor Covenant v2.1 code of conduct.
- Configured automated GitHub Actions deployment workflow for GitHub Pages.
