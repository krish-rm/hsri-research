# Pull Request: HSRI Public Benchmark Transition (Stages 1–3)

**Timestamp:** `2026-10-11T10:35:49.7652522+05:30`  
**Target Branch:** `main`  
**Milestone:** `v1.8.0` / Public Transition Release  
**Test Suite:** 117/117 passing green  
**Static Build:** 49/49 pages built cleanly in 5.49s  

## Summary of Changes

### Stage 1: Master Working Paper v1.1.0 & Open Science Metadata
- Created `research/preprint/working-paper-v1.1.0.md`: Canonical scientific preprint synthesizing Phases 0–11, CFA factor structure, incremental validity ($\Delta R^2 = +0.4870$), cross-cultural scalar invariance ($N=2,000$), longitudinal stability ($r_{tt} = 0.918$), 7-provider consensus ($\kappa = 0.666$), ecological validity ($\Delta T_{\text{wedge}} = 104.55\text{s}$), OECD 7-step audit, dynamic Kalman ingestion, and ASI synthetic batteries (EXP-07/08-SYN).
- Created root `zenodo.json` and updated `research/zenodo-metadata.json` for Zenodo deposition.
- Updated `CITATION.cff` to version `1.1.0`.
- Added `test_working_paper_v1_1_exists_and_complete` in `tests/test_preprint_scaffold.py`.

### Stage 2: Web Portal Interactive Features (`site-astro`)
- Created `site-astro/src/components/ASIScenarioExplorer.svelte` and `site-astro/src/pages/scenarios.astro`: Interactive explorer for 26 transition scenarios, the 7-axis capability matrix, and 14 precursors.
- Created `site-astro/src/components/BehavioralLabExplorer.svelte` and `site-astro/src/pages/experiments.astro`: Interactive gallery for EXP-01–09, in-situ professional domain metrics, and real-time Verification Latency Wedge Simulator.
- Updated `HSRIHeader.svelte` and `HSRIFooter.svelte` with new navigation routes.
- Updated `scripts/export_web_data.py` to automatically bundle `asi_scenarios.json` and `behavioral_experiments.json`.

### Stage 3: Security & Sanitization Audit
- Executed full repository secrets and private references scan: 0 findings.
- Verified governance documents (`LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`).
- Modernized `README.md` with updated architecture tree, quick links, and 117 passing badge.

## Verification
- `uv run pytest`: 117 passed in 4.80s.
- `cd site-astro && npm run build`: 49 pages built in 5.49s.