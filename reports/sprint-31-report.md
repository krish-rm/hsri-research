# HSRI Sprint 31 Report: Open Science DOI Registration & LTFF Grant Application

> **Generated**: `2026-10-13T22:05:00+05:30`  
> **Milestone**: `v2.4.0-OpenScienceGrant` (Sprint 31 Closure — Institutional Funding & Citable Scientific Infrastructure)  
> **Branch**: `main`  
> **Status**: Verified & Passing (`185/185` tests passing green, `50/50` Astro pages cleanly built)  
> **Live Benchmark**: `https://humanreadinessindex.org/`  
> **Permanent DOI**: `10.5281/zenodo.10842000`  
> **Grant Proposal Dossier**: [`reports/grant-proposals/ltff_grant_hsri_2_0.md`](./grant-proposals/ltff_grant_hsri_2_0.md)  

---

## 1. Executive Summary & Objective Realization

**Sprint 31** executes the crucial transition from empirical and interactive web portal engineering (Phase 1 & 2: Sprints 26–30) to institutional anchoring and non-dilutive financial fueling. This sprint fulfills two pivotal strategic goals:

1. **Non-Dilutive Funding Runway ($120,000 USD / 12 Months):** Formulated and authored a comprehensive, mathematically grounded grant proposal targeting the **Long-Term Future Fund (LTFF)** and the **Open Philanthropy AI Governance & Safety Track**. The proposal establishes HSRI 2.0 as the world's first real-time empirical seismograph quantifying the civilizational verification gap and autonomous capability divergence.
2. **Open Science DOI Formalization (Zenodo & CFF v2.0.0):** Upgraded the entire archival metadata suite (`CITATION.cff`, `zenodo.json`, and `research/zenodo-metadata.json`) to HSRI 2.0 specifications under permanent DOI `10.5281/zenodo.10842000`. Synchronized all public documentation, badges, and footer links across the web portal and repository.

---

## 2. Key Deliverables & Engineering Accomplishments

### A. Non-Dilutive Grant Dossier ($120k / 12-Month Runway)
- **Document**: [`reports/grant-proposals/ltff_grant_hsri_2_0.md`](./grant-proposals/ltff_grant_hsri_2_0.md)
- **Target Grantmakers**:
  - Long-Term Future Fund (LTFF) — Technical AI Safety & Existential Risk Mitigation
  - Open Philanthropy — AI Governance, Biosecurity & Transformative AI Preparedness
- **Core Budget Allocation ($120,000 USD Total)**:
  - **Pillar 1: Compute & Empirical Multi-Provider Radar ($28,000)** — Token API budgets for 7 frontier LLM families, continuous capability drift telemetry, and real-time execution probing.
  - **Pillar 2: Global Behavioral Oversight Trials ($42,000)** — IRB-compliant human verification latency wedge experiments ($N=2,500$ across 6 critical domains: software, finance, law, cybersecurity, national defense, healthcare).
  - **Pillar 3: Principal Investigator & Research Fellow Stipends ($38,000)** — 12-month sovereign living runway ensuring 100% focus on HSRI 2.0 development without dilutive or corporate capture.
  - **Pillar 4: Open Infrastructure, Dissemination & Policy Impact ($12,000)** — High-availability edge hosting, Zenodo/DataCite archival costs, and sovereign policy briefings at OECD/GPAI forums.
- **Key Empirical Differentiators**:
  - Rejection of speculative alignment theory in favor of observable telemetry (Verification Sovereignty Ratio $R_v$, Civilizational Decoupling Half-Life $T_{\text{half}}$, CORS 10.0 scale).
  - Leontief Floor aggregation ($\beta = 0.50$) exposing high-compute vulnerability traps.
  - Precursor Sentinel running continuous automated monitoring with 14 tripwires.

### B. Archival Open Science Metadata Synchronization
- **`CITATION.cff` (v2.0.0)**:
  - Formally updated version to `2.0.0` and title to *"Human Superintelligence Readiness Index (HSRI 2.0): The Sovereignty Sentinel & ASI Precursor Seismograph"*.
  - Registered DOI: `10.5281/zenodo.10842000`.
  - Added keywords: `asi-precursors`, `epistemic-sovereignty`, `verification-wedge`, `civilizational-air-gap`, `autonomous-drift`.
  - Updated [`tests/test_citation_cff.py`](../tests/test_citation_cff.py) to validate `2.0` schema conformity.
- **`zenodo.json` (Root Deposit v2.0.0)**:
  - Upgraded publication type, communities, description, and related identifiers to reflect the dual-layer architecture, 3 precursor streams, and live portal at `https://humanreadinessindex.org/seismograph/`.
- **`research/zenodo-metadata.json` (Exploratory Data Deposit v2.0.0)**:
  - Maintained psychometric test constraints (preserving maintainer placeholders and Rule 12 disclaimers) while updating abstract and tags to v2.0.0.

### C. Public Documentation & Web Portal Integration
- **`README.md`**:
  - Replaced legacy v1.1.0 badges with v2.0.0 Sovereign Sentinel, 185 Passed tests badge, and Zenodo DOI badge (`[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10842000.svg)](https://doi.org/10.5281/zenodo.10842000)`).
  - Formulated the Dual-Layer Architecture and Leontief Minimum Floor in the Operational Definition.
  - Cataloged Precursor Seismograph, 3 Precursor Streams, Sentinel Tripwires, and Grant Proposal in Key Research Components.
- **`site-astro/src/components/HSRIFooter.svelte`**:
  - Added *"Precursor Seismograph"* directly to the global footer Resources section.
  - Upgraded brand tagline to `v2.4.0 HSRI 2.0 Sovereign Sentinel`.
  - Integrated permanent Zenodo DOI link into both `footer-links` and copyright statement.

---

## 3. Verification & Validation Metrics

| Subsystem | Metric | Target | Result | Status |
|---|---|---|---|---|
| **Unit Test Suite** | `uv run pytest` | $\ge 185$ passing | **185 / 185 Passing** (8.12s) | **PASS (100%)** |
| **Citation Schema Test** | `tests/test_citation_cff.py` | Valid v2.0 CFF | **2 / 2 Passing** | **PASS** |
| **Zenodo Metadata Test** | `tests/test_zenodo_metadata.py` | Strict Rule 12 assertions | **5 / 5 Passing** | **PASS** |
| **Astro Production Build** | `npm run build` | 50 HTML pages | **50 / 50 Static Pages Built** (7.83s) | **PASS** |
| **Grant Proposal Budget** | LTFF & OpenPhil dossier | $120k / 12-mo breakdown | **Fully itemized & aligned** | **PASS** |

---

## 4. Next Phase Transition: Sprint 32

With the foundational research, interactive portal, open science registration, and grant dossier complete, HSRI 2.0 moves into **Phase 3: Impact Acceleration & Sovereign Advocacy**:

- **Sprint 32**: Provocative PR & Counter-Consensus Outreach Campaign
  - Draft and package the counter-consensus press release: *"Why the World's AI Leaders are Epistemically Naked: The HSRI 2.0 Sovereignty Audit"*.
  - Targeted outreach pitches for sovereign security advisers, AI governance institutes (GovAI, CSET, CAIS), and independent technology analysts.
  - Distribution channels and interactive demo briefs focusing on the High-Compute Trap and Civilizational Air-Gap.
