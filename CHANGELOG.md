# Changelog

All notable changes to the Human Superintelligence Readiness Index (HSRI) research repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
