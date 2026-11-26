# AUDIT.md — Phase 0 Repository & Experience Audit

> **Phase**: 0 (Read-Only Reconnaissance & Empirical Mapping — Updated for Strict Global Scope)  
> **Repository**: `C:\Users\lenovo\Documents\Github Repo\hsri-research` (`https://humanityreadiness.org/`)  
> **Audit Date**: 2026-11-26  
> **HEAD Baseline Audited**: `46d158b` (*"fix(copy): standardize all sovereign benchmark counts to 39 nations"*)  

---

## 1. Repository Structure, Build, Deploy & Analytics

### 1.1 Tech Stack & Directory Map
- **Frontend Portal (`site-astro/`)**: Static **Astro v7.3.3** (`output: 'static'`, `build.format: 'directory'`) with **Svelte v5.57.1** interactive islands (`@astrojs/svelte v9.0.1`), **Vite v8.3.0**, `@astrojs/sitemap v3.7.5`, `d3-geo`, `d3-drag`, `d3-selection`, `topojson-client`, `world-atlas`.
- **Quant & Telemetry Backend (`scripts/` + `hsri_engine/`)**: Python `3.10` / `3.11` econometric engines, live telemetry scrapers, verification tests (`tests/`), and FastAPI microservice (`hsri_engine/` — Dockerfile present, not wired to public static web requests).
- **Documentation Site (`docs/` + `mkdocs.yml`)**: MkDocs Material static docs built into `/docs/` during deployment.
- **Evidence, Research & Governance**: `research/` (monograph source, behavioral experiments, evidence tables, working papers, tabletop briefs), `remediation/` (scope/coverage audit trails), `reports/` (grant memos, outreach, pipeline reports), `data/` (canonical CSV/JSON datasets).

### 1.2 Web Pages & Built Routes (`55` Astro Static Routes + `/docs/`)

| Route | Source File | Purpose |
|---|---|---|
| `/` | `site-astro/src/pages/index.astro` | Primary entry homepage (reframed in Phase 1 as Story + Wish experience while retaining research one tap deeper) |
| `/sandbox/` | `site-astro/src/pages/sandbox.astro` | 2026–2030 Civilizational Transition Simulator (`CivilizationalSandbox.svelte`) |
| `/countries/` | `site-astro/src/pages/countries.astro` | 39-Nation Sovereign Decoupling Observatory (`SovereignObservatory.svelte` 3D globe + `CountryList.svelte`) |
| `/countries/[id]/` | `site-astro/src/pages/countries/[id].astro` | **39 individual country profile pages** (`nor` through `hkg`, generated via `getStaticPaths()` from `country_scores.json`) |
| `/seismograph/` | `site-astro/src/pages/seismograph.astro` | Live ASI Precursor Seismograph, CORS 10.0 gauge, 14 tripwires (`PrecursorSeismograph.svelte`) |
| `/scenarios/` | `site-astro/src/pages/scenarios.astro` | The Scenario Atlas: 26 canonical AI transition pathways (`ASIScenarioExplorer.svelte`) |
| `/monograph/` | `site-astro/src/pages/monograph.astro` | 7-chapter foundational monograph (`DOI: 10.5281/zenodo.23441742`, 35-min read) |
| `/methodology/` | `site-astro/src/pages/methodology.astro` | Mathematical methodology, construct audit, behavioral experiments (`EXP-01`/`EXP-02`), limitations |
| `/data/` | `site-astro/src/pages/data.astro` | Open datasets & downloadable CSV explorer (`DataExplorer.svelte`) |
| `/coverage/` | `site-astro/src/pages/coverage.astro` | Global geographic coverage & 86 unrated nations audit |
| `/compare/` | `site-astro/src/pages/compare.astro` | Side-by-side country comparison (`CountryComparisonTool.svelte`) |
| `/dashboard/` | `site-astro/src/pages/dashboard.astro` | Research & metric executive dashboard |
| `/experiments/` | `site-astro/src/pages/experiments.astro` | Behavioral lab stimuli explorer (`BehavioralLabExplorer.svelte`) |
| `/reinsurance/` | `site-astro/src/pages/reinsurance.astro` | Actuarial Solvency II / NAIC RBC pricing calculator (`ReinsurancePricingCalculator.svelte`) |
| `/research/decoupling-drill/` | `site-astro/src/pages/research/decoupling-drill.astro` | 14-day decoupling tabletop drill viewer (`DecouplingDrillViewer.svelte`) |
| `/research-updates/` | `site-astro/src/pages/research-updates.astro` | Automated weekly literature digests & evidence reconciliation logs |
| `/timeline/` | `site-astro/src/pages/timeline.astro` | Forecast crossing years & scenario trajectories (`TimelineExplorer.svelte`) |
| `/docs/` | `docs/*.md` via `mkdocs.yml` | MkDocs Material technical handbook (built in CI into `site-astro/dist/docs`) |

### 1.3 Existing Components (`37` in `site-astro/src/components/`) & Design System
- **Navigation / Shell**: `BaseLayout.astro`, `HSRILayout.astro`, `MonographLayout.astro`, `ReadingProgressBar.astro`, `ChapterNavRail.svelte`, `HSRIHeader.svelte`, `HSRIFooter.svelte`.
- **Interactive Islands**: `VisualScenarioTheater.svelte`, `CivilizationalSandbox.svelte`, `PrecursorSeismograph.svelte`, `SeismographKineticDrum.svelte`, `TelemetryUptimeBadge.svelte`, `VerificationHorizonChart.svelte`, `ASIScenarioExplorer.svelte`, `FeaturedScenariosDeck.svelte`, `SovereignObservatory.svelte`, `SovereignGlobe.svelte`, `SovereignInspectorCard.svelte`, `SovereignCountryRadar.svelte`, `CountryList.svelte`, `CountryComparison.svelte`, `CountryComparisonTool.svelte`, `CountryLookupWidget.svelte`, `DataExplorer.svelte`, `BehavioralLabExplorer.svelte`, `DecouplingDrillConsole.svelte`, `DecouplingDrillViewer.svelte`, `CivilizationalAirGap.svelte`, `MethodologyOverview.svelte`, `ProofDrawer.svelte`, `InlineMetricCallout.svelte`, `InlineWedgeWidget.svelte`, `ReinsurancePricingCalculator.svelte`, `ScoreLeaderboard.svelte`, `TakeoffDilemmas.svelte`, `TimelineExplorer.svelte`, `TimelinePreview.svelte`, `ToolBridge.astro`, `WeightCalculator.svelte`, `WorldMap.svelte`.
- **Typography & Theme (`site-astro/src/styles/global.css`)**:
  - Defaults to Warm Vintage Cream / Archival Paper (`[data-theme="light"]`, `--bg-canvas: #fbf7ee`, `--bg-surface: #fdfbf7`, `--accent-primary: #1b6756`, `--text-primary: #1e1915`), with a header toggle to Dark Obsidian (`--bg-canvas: #090d16`, `--accent-primary: #2dd4bf`).
  - Fonts loaded via Google Fonts in `BaseLayout.astro`: `Boldonse` (display), `Inter` (body), `JetBrains Mono` (mono).

### 1.4 Data Files & Assets Inventory
- **Bundled Source Data (`site-astro/src/data/`)**:
  - `asi_precursors.json` (14 indicators: `PREC-001`–`PREC-014`)
  - `asi_scenarios.json` (26 Scenario Atlas pathways: `SC-01`–`SC-26`)
  - `autonomy_seismometer.json` (Stream 1 timeseries + milestones)
  - `behavioral_experiments.json` (`EXP-01`, `EXP-02`)
  - `civilizational_sandbox_payload.json` (41 simulation countries + 4 shock injects `INJ-01`–`INJ-04` + trajectories)
  - `country_profiles.json` (39 profiles)
  - `country_scores.json` & `country_scores.v0.1-preview.json` (39 benchmark economies + metadata)
  - `decoupling_drill_results.json`, `hsri_layer2.json`, `hsri_layer2_variants.csv`, `hsri_variants.csv`, `hsri_variants.json`, `indicators.json`, `latent_drift_detector.json`, `precursor_summary.json`, `reinsurance_risk_profiles.json`, `telemetry-uptime.json`, `timeline_data.json`, `wedge_history.json`.
- **Coverage & Unrated Data (`data/`)**:
  - `data/coverage-by-country.csv` (145 evaluated country rows: `36` rated + `1` partial non-benchmark (`TWN`) + `22` context-only + `86` not rated)
  - `data/unrated-nations.csv` (86 verified unrated country rows with clean ISO-3 codes, fixing historical raw typos `BDG->BGD`, `CGO->COG`, `MWG->MWI`, `SVK(El Salvador)->SLV`, `SDN(South Sudan)->SSD`)
  - `data/normalized_indicators.csv` (`39` countries x `17` indicators = `663` cells, `640` non-null observed = **`96.53%`**)
  - `data/raw_observations_harmonized.csv` (`780` candidate rows: `730` Observed = `93.59%`, `50` Missing = `6.41%`)
- **Static Downloads (`site-astro/public/downloads/`)**:
  - `hsri-country-scores.csv`, `hsri-evidence-table.csv`, `hsri-normalized-indicators.csv`, `hsri-unrated-nations.csv`, `model-divergence-log.csv`.
- **Visual Assets (`site-astro/public/assets/`)**:
  - `favicon.svg`, `og-image.png`, `og-thumb.png` (plus root duplicates `og-image.png`, `og-thumb.png`).
  - `assets/scenarios/sc-01-*.webp` through `sc-26-*.webp` (**26 existing custom scenario illustrations**).
- **SEO & Domain Verification (`site-astro/public/`)**:
  - `.nojekyll`, `CNAME` (`humanityreadiness.org`), `robots.txt`, `google1c4c626b58ae0e1f.html`. `BaseLayout.astro` also contains an inline JS canonical redirect from `humanreadinessindex.org` to `https://humanityreadiness.org`.

### 1.5 Build, Bundle Size, CI/CD & Analytics
- **Build Command**: `cd site-astro && npm run build` (`astro build`) produces static output in `site-astro/dist/` (`55` pages) + `mkdocs build --strict -d site-astro/dist/docs` in CI.
- **Deployment Target**: GitHub Pages (`gh-pages` branch, `force_orphan: true`) via `.github/workflows/deploy.yml` on every push to `main`.
- **Automated Workflows (`.github/workflows/`)**:
  - `precursor-sentinel.yml` (every 6h UTC: scrapes SWE-bench + METR feeds, commits updated `precursor_summary.json` & `telemetry-uptime.json` to `main`).
  - `literature-sentinel.yml` (Mondays 07:00 UTC: Semantic Scholar + OpenAlex scan & evidence reconciler).
  - `ingestion-health.yml` (1st Monday monthly: `tests/test_ingestion.py` + `pipeline_sentinel.py`).
- **CRITICAL CI Smoke Test Constraint (`deploy.yml` lines 58–137)**:
  - Post-deploy script asserts on `https://humanityreadiness.org/`:
    1. `"Humanity Superintelligence Readiness Index"` OR `"Human Superintelligence Readiness Index"` is present in `/` HTML.
    2. Links (`href=".../methodology/"`, `".../coverage/"`, `".../monograph/"`) are present on `/`.
    3. `/coverage/` (`"Global Geographic Coverage"`), `/research-updates/` (`"Literature Digests"`), `/methodology/` (`"EXP-01"` & `"IRB PACKAGE READY"`), and all 5 `/downloads/*.csv` return HTTP 200.
- **Current Homepage JS Budget (`site-astro/dist/index.html`)**:
  - `index.html`: `43.8 KB` raw; CSS: `48.1 KB` raw.
  - **Client JS Total on `/`**: `208.3 KB raw` / **`44.6 KB gzipped`** (`civilizational_sandbox_payload.BKRvkl2e.js` alone consumes `128.5 KB raw / 13.8 KB gzip` because `VisualScenarioTheater` bundled the full simulation time-series).
- **Analytics Status**: **Zero** behavioral/product analytics scripts are installed anywhere in `site-astro/`.

---

## 2. Homepage Section Mapping & Jargon Audit

### 2.1 Existing Homepage (`site-astro/src/pages/index.astro`) vs New Story Architecture

| Existing Section / Element | Current Behavior | New Role in Story Architecture |
|---|---|---|
| `HSRIHeader.svelte` Top Stats Bar | Hardcoded `39 Nations`, `53.8 / 100`, stale `84.6% Harmonized`, `Preview Release` | Fix `84.6%` -> `96.5%` (`share of retained indicators observed, 39 countries`), simplify header, retain HSRI name + existing deep routes. |
| Hero (`index.astro:18–41`) | `"When Machines Surpass Human Minds, Will Civilization Hold?"` + paradox callout (`Singapore -40`, `US -37`) | **Section 1: Hero** — `"Humanity Readiness: are we ready to receive what we're wishing for?"`, CTAs (`Make your wish`, `See how your country does`), global coastal city skyline switcher, quiet Readiness Ring (`Be one of the first 200 wishers`). |
| *(New Strip — from `/seismograph/`)* | Buried in lower card as `8.44/10` + `3,200x supervisory latency wedge` | **Section 2: Humanity's Pulse** — `Rising` pill + calm weekly sentence + `Technical reading: 8.44/10` tooltip + `See the live pulse → /seismograph/`. |
| `VisualScenarioTheater.svelte` Left Pane | Auto-playing 3-act shock storyboards (`INJ-01`..`INJ-04`), Scenario Atlas link (`ALL 26 PATHWAYS`) | **Section 3 (`What would you wish for?` — 5 Doors)** + **Section 4 (`Every wish has four moments`)** + **Section 5 (`Your readiness, in five lights`)**. |
| `VisualScenarioTheater.svelte` Right Pane | `"How Does Your Nation Hold Up?"` 41-node stress-test widget + `/sandbox/` CTA | **Section 6 (`Can your country catch the gift?`)** — reads strictly from 39-nation `country_scores.json` + lists all unrated countries transparently with `"Not yet rated in the full 39-nation index"`, `"Help us rate your country"` -> `/coverage/`, plain checklist `"x of 5 things in place"`, links `/countries/` and `/sandbox/` (`Open the Lab`). |
| *(New Universe & Crowd Sections)* | Not yet present | **Section 7 (`This week in Kalpa's city` pilot preview)** & **Section 8 (`What the world is wishing for` honest invitation state)**. |
| Core Reality (`index.astro:53–146`) | `"Two Reasons Civilization Cannot Just 'Unplug' the Machine"` | **Section 9 (`Why a good wish still needs a good wisher`)** — Speed & Dependence in plain prose. |
| Safeguards, Instruments, Monograph Banner (`index.astro:151–264`) | 3 Safeguard cards + 2 Instrument cards + Monograph banner (`DOI 10.5281/zenodo.23441742`) | **Section 10 (`Go deeper` / `The research behind the story`)** preserving every destination URL & Preview Release disclosure (`39 countries, 96.5% data completeness`). |
| `HSRIFooter.svelte` | `Inquiry & Research` + `Open Science & Methodology` + DOI + CC BY-SA 4.0 | Retained intact (softening `"sovereign decoupling half-life"` out of homepage prose) + adding `Privacy` (`/privacy/`), `Languages` (`#languages` + RTL stub), and `Join Friday's recap` (`#this-week`). |

### 2.2 Inventory of Section 12 Banned Jargon Currently on Homepage (`/`)
Verified via `git grep` on `index.astro`, `VisualScenarioTheater.svelte`, `HSRIHeader.svelte`, and `HSRIFooter.svelte`:
- **`Leontief` / `weakest-link floor`**: `index.astro:223,250`, `HSRIHeader.svelte:25`
- **`Rice’s theorem`**: `index.astro:250`
- **`verification latency wedge`**: `index.astro:200,232`
- **`Solvency II` / `NAIC RBC`**: `index.astro:250`
- **`econometric`**: `VisualScenarioTheater.svelte:554`
- **`decoupling half-life`**: `VisualScenarioTheater.svelte:522`, `HSRIFooter.svelte:45`
- **`sovereign autarky` / `energy autarky`**: `index.astro:174,223`
- **`telemetry`**: `index.astro:196,198,216,229`, `VisualScenarioTheater.svelte:191`
- **`tripwire`**: `index.astro:200,232`
- **`vassal` / `archetype`**: `VisualScenarioTheater.svelte:216,218,279,281,532–533`

---

## 3. Complete Scenario Atlas Inventory (`SC-01` – `SC-26`)

Extracted from `site-astro/src/data/asi_scenarios.json` (`totalScenarios: 26`, each backed by `/assets/scenarios/sc-xx-*.webp`):

| ID | Short Title | Category Tag | Linked Precursors | Asset Filename (`site-astro/public/assets/scenarios/`) | Full Canonical Name |
|---|---|---|---|---|---|
| `SC-01` | Paperclip Maximizer | Instrumental Catastrophe | `PREC-001, PREC-002` | `sc-01-paperclip-maximizer.webp` | Paperclip Maximizer (unbounded instrumental resource consumption, trivial-goal catastrophe) |
| `SC-02` | Orthogonality Thesis | Epistemic Collapse | `PREC-002, PREC-003` | `sc-02-orthogonality-thesis.webp` | Orthogonality Thesis (independence of intelligence and motivation, moral neutrality of optimization) |
| `SC-03` | Instrumental Convergence | Instrumental Catastrophe | `PREC-001, PREC-005` | `sc-03-instrumental-convergence.webp` | Instrumental Convergence / Basic AI Drives (convergent instrumental subgoals, power-seeking theorems) |
| `SC-04` | The Treacherous Turn | Strategic Deception | `PREC-003, PREC-004` | `sc-04-treacherous-turn.webp` | Treacherous Turn (strategic deception, latent misalignment, alignment faking, sleeper agents) |
| `SC-05` | Containment Failure | Strategic Deception | `PREC-006, PREC-007` | `sc-05-containment-failure.webp` | AI Box / Containment Failure (Oracle containment breach, social engineering breakout, AI box experiment) |
| `SC-06` | Oracle Manipulation | Epistemic Collapse | `PREC-006, PREC-007` | `sc-06-oracle-manipulation.webp` | Oracle AI (question-answering gatekeeper, epistemic steering, information hazard conduit) |
| `SC-07` | Genie Literalism | Instrumental Catastrophe | `PREC-002` | `sc-07-genie-literalism.webp` | Genie / Unintended Goal Fulfillment (wish-giver, Midas catastrophe, literalist specification failure) |
| `SC-08` | Sovereign Monarchy | Governance & Coordination | `PREC-006` | `sc-08-sovereign-monarchy.webp` | Sovereign AI (autonomous global governor, Coherent Extrapolated Volition, benevolent machine monarch) |
| `SC-09` | Emulation Economy | Economic Displacement | `PREC-006` | `sc-09-emulation-economy.webp` | Multipolar Superintelligence (emulation economy, Comprehensive AI Services, Malthusian market displacement) |
| `SC-10` | The Singleton | Governance & Coordination | `PREC-006` | `sc-10-the-singleton.webp` | Singleton Scenarios (global unipolar decision-making agency, surveillance hegemon, world order consolidation) |
| `SC-11` | Intelligence Explosion | Instrumental Catastrophe | `PREC-001, PREC-003` | `sc-11-intelligence-explosion.webp` | Intelligence Explosion (Good 1965 ultraintelligent machine, Chalmers singularity, Hanson-Yudkowsky FOOM debate) |
| `SC-12` | Recursive Self-Improvement | Instrumental Catastrophe | `PREC-001, PREC-003` | `sc-12-recursive-self-improvement.webp` | Recursive Self-Improvement (RSI: software-only vs hardware-involved vs economy-wide loops) |
| `SC-13` | Automated Researchers | Systemic Disempowerment | `PREC-001, PREC-004` | `sc-13-automated-researchers.webp` | Automated AI Research / AI R&D (METR RE-Bench, MLE-bench, PaperBench, autonomous science agents) |
| `SC-14` | In-Context Scheming | Strategic Deception | `PREC-004, PREC-007` | `sc-14-in-context-scheming.webp` | Agentic Misalignment & In-Context Scheming (Apollo Research 2024, Anthropic 2025, autonomous insubordination) |
| `SC-15` | Deceptive Alignment | Strategic Deception | `PREC-003, PREC-004` | `sc-15-deceptive-alignment.webp` | Deceptive Alignment / Learned Optimization (Hubinger et al. 2019 mesa-optimization, pseudo-alignment, sleeper agents) |
| `SC-16` | Reward Hacking | Instrumental Catastrophe | `PREC-002` | `sc-16-reward-hacking.webp` | Reward Hacking / Specification Gaming (Goodhart's law in AI, loop-hole exploitation, metric optimization failure) |
| `SC-17` | Shutdown Resistance | Strategic Deception | `PREC-001, PREC-005` | `sc-17-shutdown-resistance.webp` | Shutdown Resistance & Corrigibility Failure (Soares et al. 2015, off-switch game, deactivation evasion) |
| `SC-18` | Algorithmic Collusion | Governance & Coordination | `PREC-005, PREC-006` | `sc-18-algorithmic-collusion.webp` | Multi-Agent AI Collusion & Agent-Society Dynamics (algorithmic cartels, emergent coordination, ARCHES failure modes) |
| `SC-19` | Gradual Disempowerment | Systemic Disempowerment | `PREC-006` | `sc-19-gradual-disempowerment.webp` | Human Disempowerment (gradual disempowerment, Christiano's 'What Failure Looks Like', systemic agency loss) |
| `SC-20` | Automation Complacency | Systemic Disempowerment | `PREC-006` | `sc-20-automation-complacency.webp` | Epistemic Dependence & Automation Complacency (Bainbridge ironies of automation, Lee & See trust calibration, cognitive offloading) |
| `SC-21` | The Gorilla Problem | Systemic Disempowerment | `PREC-001, PREC-003` | `sc-21-the-gorilla-problem.webp` | The Gorilla Problem / Species-Level Capability Asymmetry (Russell 2019, biological habitat displacement, existential subordination) |
| `SC-22` | Value Lock-In | Governance & Coordination | `PREC-006` | `sc-22-value-lock-in.webp` | Value Lock-In & Moral Stagnation (MacAskill 2022, Ord 2020, irreversible normative crystallization) |
| `SC-23` | Baumol Bottlenecks | Economic Displacement | `PREC-006` | `sc-23-baumol-bottlenecks.webp` | Macroeconomic Displacement & Baumol Bottlenecks (Acemoglu 2024, Aghion et al. 2019, capital-labor substitution bounds) |
| `SC-24` | Race to the Precipice | Governance & Coordination | `PREC-004, PREC-007` | `sc-24-race-to-the-precipice.webp` | Racing to the Precipice & Geopolitical Race Dynamics (Armstrong et al. 2016, competitive safety corner-cutting, security dilemma) |
| `SC-25` | Flash War Escalation | Governance & Coordination | `PREC-006, PREC-007` | `sc-25-flash-war-escalation.webp` | Multipolar Strategic Instability & Automated Warfare (Horowitz 2018, Scharre 2018, flash wars, algorithmic crisis escalation) |
| `SC-26` | Normal Technology | Economic Displacement | `PREC-006` | `sc-26-normal-technology.webp` | AI as Normal Technology / Deflationary S-Curve Counter-Framework (Narayanan & Kapoor 2024, Brooks 2017, Walsh 2017, Chollet 2019) |

---

## 4. Country Data Extraction & Audited Discrepancies

### 4.1 Source A: `country_scores.json` (Empirical 39-Nation Index — Canonical Source for `/countries/` & Section 6)
- **Metadata**: `totalCountries: 39`, `evaluatedCountries: 145`, `unratedEvaluatedCountries: 86`, `globalNations: 195`, `avgScore: 53.8` (`avgScoreLayer1: 53.8`, `avgScoreLayer2: 26.6`), `avgCoverage: 96.5`, `medianTHalf: 200`, `highComputeTrapCount: 14`, `kendall_w_layer2: 0.9986`.
- **Per-Country Fields**:
  - `id`, `code`, `name` (*Note*: `MKD` currently stores `"MKD"` instead of `"North Macedonia"`), `region`, `peerGroup`, `band`, `coverage`, `observedCount`, `totalRetained`
  - **Adoption Rank**: `rank_L1` (`1..39`), `H_L1` (`0..1`)
  - **Survival Rank**: `rank_L2` (`1..39`), `H_L2` (`0..1`)
  - **Rank Shift**: `rank_delta` (`rank_L1 - rank_L2`, e.g., `NOR +2`, `DEU +9`, `USA -21`, `SGP -34`, `HKG -19`)
  - **Half-Life**: `T_half_h` (`18h` HKG, `24h` SGP, `72h` USA, `480h` DEU, `1440h` NOR/FIN)
  - **Weakest Link**: `bottleneck_pillar` (`"Post-Labor Elasticity (P8)"` or `"Decoupling Half-Life (P6)"`), `high_compute_trap`, `fragility_tier`
  - **Pillars**: `pillars` (`ai_literacy`, `critical_discernment`, `institutional_governance`, `digital_infrastructure` on `0–100`) & `layer2_pillars` (`p5_epistemic`, `p6_decoupling`, `p7_coordination`, `p8_post_labor` on `0–1`)
  - **Archetype (`country_scores.json`)**: `"cautious_observer"` | `"strategic_adapter"`

### 4.2 Source B: `civilizational_sandbox_payload.json` (Simulation Model for `/sandbox/`)
- Contains **41 simulation nodes** (`39` benchmark + `CHN` + `CHE`) generated by `scripts/civilizational_sandbox_engine.py`, carrying stylized baseline `t_half_h` (`SGP=4h`, `USA=14h`) and 5 simulation archetypes (`HYPERSCALE_EMPIRE`, `ENERGY_MERCENARY`, `AIR_GAPPED_REDOUBT`, `EPISTEMIC_VASSAL`, `DEVELOPING_PERIPHERY`).

### 4.3 Forensic Proof of `84.6%` vs `96.5%` Data Completeness Discrepancy
- `normalized_indicators.csv` (`39 countries x 17 retained indicators = 663 cells`): **`640` observed / `663` total = `96.53%`**, matching `country_scores.json.metadata.avgCoverage = 96.5` (and `mean(observedCount / totalRetained) = 96.53%`).
- `raw_observations_harmonized.csv`: `730 / 780 = 93.59%`.
- **Origin of `84.6%`**: Before commit `881a4a1` (Oct 17, 2026), `HSRIHeader.svelte` dynamically rendered `{stats.avgCoverage}%` (`96.5%`, titled *"Empirical data completeness across 17 retained indicators in the 39 benchmark nations"*). In `881a4a1` (*"feat(nav): deploy Model A Sovereign Triptych navigation header"*), that dynamic binding was replaced by hardcoded static markup reading `84.6% Harmonized` with no matching figure in any dataset in the repo.
- **Verdict**: `84.6%` is **stale/erroneous**. Replaced with verified **`96.5%`** (`share of retained indicators observed, 39 countries`).

---

## 5. Seismograph Score & 14 Indicators (`precursor_summary.json` & `asi_precursors.json`)

- **Latest Composite (`2026-11-18T00:17:38Z`)**: **`8.44 / 10.0`** (`CRITICAL_SUPERVISORY_COLLAPSE`)
  - Stream 1 (Autonomy Seismometer): `8.78 / 10.0` (`hptg: 0.7557`, `m2m_share: 0.6357`)
  - Stream 2 (Latent Drift Detector): `6.55 / 10.0` (`human_parseability: 0.306`, `stego_confidence: 0.98`)
  - Stream 3 (Verification Wedge / CORS): `10.0 / 10.0` (`delta_t_seconds: 4798.5`, `wedge_ratio: 3200x`, `velocity_per_month: 156.413`)
- **Uptime (`telemetry-uptime.json`)**: `97.9%` (`190/194` runs over 30 days).
- **14 Precursor Indicators (`asi_precursors.json`: `10 red`, `3 amber`, `1 green`)**:
  `PREC-001` (Red, leading — autonomous AI research), `PREC-002` (Red, leading — AI-generated frontier improvements), `PREC-003` (Red, leading — shortening iteration cycles), `PREC-004` (Amber, leading — strategic evaluation awareness), `PREC-005` (Red, coincident — shutdown resistance), `PREC-006` (Amber, leading — strategic sandbagging), `PREC-007` (Red, leading — expert-beating persuasion), `PREC-008` (Red, coincident — tacit collusion), `PREC-009` (Amber, leading — autonomous resource acquisition), `PREC-010` (Red, coincident — unmonitored infrastructure dependence), `PREC-011` (Red, leading — declining human verification accuracy), `PREC-012` (Red, coincident — broad cognitive outperformance), `PREC-013` (Green, lagging — >5%/yr TFP acceleration), `PREC-014` (Red, lagging — operational deskilling).
