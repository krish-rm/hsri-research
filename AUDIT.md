# AUDIT.md — Phase 0 Repository & Experience Audit

> **Phase**: 0 (Read-Only Reconnaissance & Empirical Mapping — Zero Code Changes)  
> **Repository**: `C:\Users\lenovo\Documents\Github Repo\hsri-research` (`https://humanityreadiness.org/`)  
> **Audit Date**: 2026-11-26  
> **HEAD Commit Audited**: `46d158b` (*"fix(copy): standardize all sovereign benchmark counts to 39 nations"*)  

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
| `/` | `site-astro/src/pages/index.astro` | Primary entry homepage (Hero, Visual Scenario Theater, Two Traps, Safeguards & Instruments, Monograph Banner) |
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
  - `asi_precursors.json` (14 tripwires: `PREC-001`–`PREC-014`)
  - `asi_scenarios.json` (26 Scenario Atlas pathways: `SC-01`–`SC-26`)
  - `autonomy_seismometer.json` (Stream 1 timeseries + milestones)
  - `behavioral_experiments.json` (`EXP-01`, `EXP-02`)
  - `civilizational_sandbox_payload.json` (41 simulation countries + 4 shock injects `INJ-01`–`INJ-04` + trajectories)
  - `country_profiles.json` (39 profiles)
  - `country_scores.json` & `country_scores.v0.1-preview.json` (39 benchmark economies + metadata)
  - `decoupling_drill_results.json`, `hsri_layer2.json`, `hsri_layer2_variants.csv`, `hsri_variants.csv`, `hsri_variants.json`, `indicators.json`, `latent_drift_detector.json`, `precursor_summary.json`, `reinsurance_risk_profiles.json`, `telemetry-uptime.json`, `timeline_data.json`, `wedge_history.json`.
- **Static Downloads (`site-astro/public/downloads/`)**:
  - `hsri-country-scores.csv`, `hsri-evidence-table.csv`, `hsri-normalized-indicators.csv`, `hsri-unrated-nations.csv`, `model-divergence-log.csv`.
- **Visual Assets (`site-astro/public/assets/`)**:
  - `favicon.svg`, `og-image.png`, `og-thumb.png` (plus root duplicates `og-image.png`, `og-thumb.png`).
  - `assets/scenarios/sc-01-*.webp` through `sc-26-*.webp` (**26 existing custom scenario illustrations already in repo**).
- **SEO & Domain Verification (`site-astro/public/`)**:
  - `.nojekyll`, `CNAME` (`humanityreadiness.org`), `robots.txt`, `google1c4c626b58ae0e1f.html`. Note `BaseLayout.astro` also contains an inline JS canonical redirect from `humanreadinessindex.org` to `https://humanityreadiness.org`.

### 1.5 Build, Bundle Size, CI/CD & Analytics
- **Build Command**: `cd site-astro && npm run build` (`astro build`) produces static output in `site-astro/dist/` (`55` pages built in ~31s on latest run) + `mkdocs build --strict -d site-astro/dist/docs` in CI.
- **Deployment Target**: GitHub Pages (`gh-pages` branch, `force_orphan: true`) via `.github/workflows/deploy.yml` on every push to `main` (and `workflow_dispatch`).
- **Automated Workflows (`.github/workflows/`)**:
  - `precursor-sentinel.yml` (every 6h UTC: scrapes SWE-bench + METR feeds, runs Streams 1–3, commits updated `precursor_summary.json` & `telemetry-uptime.json` directly to `main`).
  - `literature-sentinel.yml` (Mondays 07:00 UTC: Semantic Scholar + OpenAlex scan & evidence reconciler).
  - `ingestion-health.yml` (1st Monday monthly: `tests/test_ingestion.py` + `pipeline_sentinel.py`).
- **CRITICAL CI Smoke Test Constraint (`deploy.yml` lines 58–137)**:
  - Post-deploy script asserts on `https://humanityreadiness.org/`:
    1. `"Humanity Superintelligence Readiness Index"` OR `"Human Superintelligence Readiness Index"` is present in `/` HTML.
    2. Links (`href=".../methodology/"`, `".../coverage/"`, `".../monograph/"`) are present on `/` (e.g., via header/footer/Go Deeper).
    3. `/coverage/` returns 200 and contains `"Global Geographic Coverage"`.
    4. `/research-updates/` returns 200 and contains `"Literature Digests"`.
    5. `/methodology/` returns 200 and contains `"EXP-01"` and `"IRB PACKAGE READY"`.
    6. All 5 `/downloads/*.csv` endpoints return 200.
- **Current Homepage JS Budget (`site-astro/dist/index.html`)**:
  - `index.html`: `43.8 KB` raw; CSS: `48.1 KB` raw across `index.*.css` + `HSRIFooter.*.css`.
  - **Client JS Total on `/`**: `208.3 KB raw` / **`44.6 KB gzipped`** across 6 chunks:
    - `client.DKSqpTzA.js`: `44.3 KB` (`17.0 KB gzip`)
    - `client.svelte.DTsE1Blc.js`: `0.9 KB` (`0.5 KB gzip`)
    - `HSRIHeader.B9ZwRtyK.js`: `10.7 KB` (`3.6 KB gzip`)
    - `HSRIFooter.GCDClh7Q.js`: `5.4 KB` (`2.3 KB gzip`)
    - `VisualScenarioTheater.Cm5pxJK3.js`: `18.7 KB` (`7.5 KB gzip`)
    - `civilizational_sandbox_payload.BKRvkl2e.js`: **`128.5 KB` (`13.8 KB gzip`)** — bloated because `VisualScenarioTheater` imports the full 41-nation multi-quarter time-series payload (`251 KB` JSON) instead of compact summary metrics. Stripping full time-series from `/` leaves huge headroom inside the `150 KB gzip` homepage budget for the Wish Engine + SVG scenes.
- **Analytics Status**: **Zero** third-party or first-party analytics scripts are currently installed anywhere in `site-astro/` (verified via repo-wide search across `.astro`, `.svelte`, `package.json`).

---

## 2. Homepage Section Mapping & Jargon Audit

### 2.1 Existing Homepage (`site-astro/src/pages/index.astro`) vs New Story Architecture

| Existing Section / Element | Current Behavior & Copy Highlights | New Role in Story Architecture (Section 6 Brief) |
|---|---|---|
| `HSRIHeader.svelte` Top Stats Bar (desktop) | Shows `Benchmark Scope: 39 Nations`, `Benchmark Mean: 53.8 / 100`, `Data Completeness: 84.6% Harmonized`, `Preview Release` | Simplify/declutter header for story focus; preserve Preview Release + completeness disclosure (`39 countries, 84.6% / 96.5%` — see `DECISIONS.md` J1) cleanly in **Section 10: Go deeper** & `HSRIFooter`. Retain HSRI identity string for CI smoke check & brand authority. |
| Hero (`index.astro:18–41`) | `"When Machines Surpass Human Minds, Will Civilization Hold?"` + `"THE WEAKEST-LINK PARADOX: Singapore drops 40 ranks and the US drops 37, while Norway holds #1."` | **Section 1: Hero** — `"Humanity Readiness: are we ready to receive what we're wishing for?"` with CTAs (`Make your wish`, `See how your country does`), calm Kochi/Dubai/Chennai harbour skyline animation (Kalpa arriving), and crowd Readiness Ring (`Be one of the first 200 wishers` empty state until real threshold reached). |
| *(New Strip — derived from `/seismograph/` `precursor_summary.json`)* | Currently buried on lines 227–234 as `"LIVE TELEMETRY · 8.44/10"` + `"3,200x supervisory latency wedge"` | **Section 2: Humanity's Pulse** — Calm plain-language strip (`Steady` / `Stirring` / `Rising`) + 1 weekly plain sentence + tooltip showing `Technical reading: 8.44/10`, linking to `/seismograph/`. |
| *(New Interactive Core — absorbs Visual Scenario Theater)* | `VisualScenarioTheater.svelte`: Auto-playing 3-act storyboards for 4 shocks (`INJ-01`..`INJ-04`), scenario selector, Atlas bridge tab (`ALL 26 PATHWAYS`) | **Section 3: The five doors** + **Wish Engine (Wonder / Wobble / Weight / Way)** + **Section 4: Four moments** + **Section 5: Five lights**. Existing 3-act shock visual mechanics & `/assets/scenarios/` plates inform the **Wobble** animations and link to **Scenario Atlas (Shadow Library)**. |
| `VisualScenarioTheater.svelte` Right Pane (`stage-impact-pane`, lines 455–556) | `"How Does Your Nation Hold Up?"`: 6 preset chips + dropdown (`sandboxPayload.countries`), shows L1 Adoption Rank, Sovereign Survival Rank, Rank Shift, Decoupling Half-Life (h), Archetype badge, Weakest Link, CTA to `/sandbox/` | **Section 6: Can your country catch the gift?** — Plain-language translation (`Days [country] keeps running without the cloud`, `Catches the gift: Easily / With effort / Struggles`, `A clock that slows`, plain archetype + tooltip, `"The one thing most likely to hold [country] back"`, post-wish `x of 5 things in place`, link to `/countries/` + `"Open the Lab"` `/sandbox/`). |
| *(New Story Universe Module — Phase 4)* | Does not yet exist | **Section 7: This week in Kalpa's city** — 2–3 min pilot episode, story continuation vote, `Real Life` card, optional `Friday's recap` CTA. |
| *(New Crowd Constellation — Phase 3)* | Does not yet exist | **Section 8: What the world is wishing for** — Anonymised thematic Wish Wall + moderated submission CTA (invitation state until threshold `>= 20` real submissions). |
| Core Reality (`index.astro:53–146`) | `"Two Reasons Civilization Cannot Just 'Unplug' the Machine"` (Speed Trap + Dependency Trap cards: 200ms blink vs machine swarm; electrical grid, ports/food, hospitals) | **Section 9: Why a good wish still needs a good wisher** — Rewritten calmly around `Speed` & `Dependence`, closing with `"This is not about fear. It's about being ready to receive."` |
| Road Ahead Triad + Two Instruments + Monograph Authority Banner (`index.astro:151–264`) | 3 Safeguard cards (`72h Analog Override`, `Sovereign Reserves`, `Open Telemetry`), 2 Instrument cards (`/countries/`, `/seismograph/`), Monograph banner (`DOI 10.5281/zenodo.23441742`, 35-min read) | Safeguards become **Way** concrete action cards inside wishes; Monograph + `/sandbox/` (`Open the Lab`) + `/countries/` + `/seismograph/` + `/scenarios/` + `/methodology/` + `/data/` + Preview Release disclosure consolidate cleanly into **Section 10: Go deeper ("The research behind the story")**. |
| `HSRIFooter.svelte` | Columns (`Inquiry & Research`, `Open Science & Methodology`), contact `contact@humanityreadiness.org`, Twitter/X, DOI, Actuarial Disclaimer, CC BY-SA 4.0 | Retained intact + add `Languages`, `Privacy`, and `Join Friday's recap` links (note: `/coverage/` is already in footer; retain `/methodology/` & `/monograph/` for CI smoke test). |

### 2.2 Inventory of Section 12 Banned Jargon Currently on Homepage (`/`)
Verified direct grep hits on `index.astro`, `VisualScenarioTheater.svelte`, `HSRIHeader.svelte`, `HSRIFooter.svelte`:
- **`Leontief` / `weakest-link floor`**: `index.astro:223` (*"Leontief weakest-link floors"*), `index.astro:250` (*"Leontief input-output weakest-link floors"*), `HSRIHeader.svelte:25` (dropdown desc — note allowed inside deeper tooltip/dropdown or sanitize to plain phrase).
- **`Rice’s theorem`**: `index.astro:250` (*"Rice’s theorem boundaries"*).
- **`verification latency wedge`**: `index.astro:200` (*"verification latency wedges"*), `index.astro:232` (*"supervisory latency wedge"*).
- **`Solvency II` / `NAIC RBC`**: `index.astro:250` (*"Solvency II / NAIC RBC tail-risk reinsurance"*).
- **`econometric`**: `VisualScenarioTheater.svelte:554` (*"export econometric data"*).
- **`decoupling half-life`**: `VisualScenarioTheater.svelte:522` (*"DECOUPLING HALF-LIFE"*), `HSRIFooter.svelte:45` (*"sovereign decoupling half-life"* — audit whether footer description also softens or keeps technical summary).
- **`sovereign autarky` / `energy autarky`**: `index.astro:174` (*"72h Sovereign Autarky"*), `index.astro:223` (*"energy autarky"*).
- **`telemetry`**: `index.astro:196` (`TELEMETRY MANDATE`), `index.astro:198` (`Continuous Open Telemetry`), `index.astro:216,229`, `VisualScenarioTheater.svelte:191`.
- **`tripwire`**: `index.astro:200` (*"and tripwires in real time"*), `index.astro:232` (*"14 empirical tripwires"*).
- **`vassal` / `archetype`**: `VisualScenarioTheater.svelte:216,218,279,281,532–533` (renders `ARCHETYPE: EPISTEMIC VASSAL` / `ISOLATED VASSAL COLLAPSE` directly in right-pane widget).

---

## 3. Complete Scenario Atlas Inventory (`SC-01` – `SC-26`)

Extracted directly from `site-astro/src/data/asi_scenarios.json` (`totalScenarios: 26`, every pathway includes pre-built illustration artwork at `/assets/scenarios/sc-xx-*.webp` and linked precursor IDs):

| ID | Short Title | Category Tag | Linked Precursors | Artwork Asset (`/assets/scenarios/...`) | Full Canonical Name |
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

*Note*: `VisualScenarioTheater.svelte` currently cites `SC-04`, `SC-12`, `SC-01`, `SC-07` in `literaturePrecedent` links to `/scenarios/#SC-xx`.

---

## 4. Exact Country Data Schemas & Audited Discrepancies

Two separate country JSON files exist in `site-astro/src/data/`:

### 4.1 Source A: `country_scores.json` (The Official 39-Nation Empirical Index)
- **Top-level Metadata (`country_scores.json.metadata`)**:
  - `totalCountries`: `39` (`evaluatedCountries`: `145`, `unratedEvaluatedCountries`: `86`, `globalNations`: `195`)
  - `avgScore`: `53.8` (`avgScoreLayer1`: `53.8`, `avgScoreLayer2`: `26.6`, `avgVulnerability`: `0.2722`)
  - `avgCoverage`: `96.5` (actual mean of `observedCount / totalRetained` across the 39 nations = `96.53%`)
  - `medianTHalf`: `200`, `highComputeTrapCount`: `14`, `kendall_w_layer2`: `0.9986`
  - `coverageNote`: `"Preview release: 39 benchmark nations (OECD/high-income sample). Primary microdata unverified."`
  - `doi`: `"10.5281/zenodo.23441742"`
- **Exact Fields Per Country (`countries[]`, 39 entries)**:
  - Identifiers: `id` (`"nor"`), `code` (`"NOR"`), `name`, `region`, `peerGroup`, `band` (`A`–`F`), `status`, `coverage`, `observedCount`, `totalRetained`
  - Layer 1 Adoption & Layer 2 Sovereignty Metrics:
    - **Adoption Rank**: `rank_L1` (`1..39`, e.g., `NOR=3`, `SGP=4`, `USA=15`) and `H_L1` (`0..1`, e.g., `NOR=0.8644`, `SGP=0.8217`, `USA=0.6843`)
    - **Survival Rank**: `rank_L2` (`1..39`, e.g., `NOR=1`, `USA=36`, `SGP=38`) and `H_L2` (`0..1`, e.g., `NOR=0.5094`, `USA=0.1433`, `SGP=0.0793`)
    - **Rank Shift**: `rank_delta` (`rank_L1 - rank_L2`, e.g., `NOR=+2`, `DEU=+9`, `USA=-21`, `SGP=-34`, `HKG=-19`, `KOR=-19`)
    - **Half-Life**: `T_half_h` (hours, `18h` for HKG, `24h` for SGP, `72h` for USA, `480h` for DEU, `1440h` for NOR/FIN)
    - **Weakest Link**: `bottleneck_pillar` (`"Post-Labor Elasticity (P8)"` or `"Decoupling Half-Life (P6)"`), plus `variants.bottleneck_pillar` (Layer 1 pillar e.g. `"AI Literacy"`) and `high_compute_trap` (`boolean`), `fragility_tier` (`High` / etc.), `V_ASI`
    - **Layer 1 Pillars (`pillars`)**: `ai_literacy`, `critical_discernment`, `institutional_governance`, `digital_infrastructure` (`0..100` scale)
    - **Layer 2 Pillars (`layer2_pillars`)**: `p5_epistemic`, `p6_decoupling`, `p7_coordination`, `p8_post_labor`, `vsr`, `v_coord` (`0..1` scale)
    - **Archetype**: `archetype` (`"cautious_observer"` | `"strategic_adapter"`)

### 4.2 Source B: `civilizational_sandbox_payload.json` (The 41-Node Dynamic Simulation Payload)
- Contains **41 nodes** (`39` benchmark + `CHN` + `CHE`, added by `scripts/civilizational_sandbox_engine.py`).
- **Exact Fields Per Country (`countries[]`, 41 entries)**:
  - `iso`, `name`, `gw_clean`, `sfp`, `waa`, `csp`, `debt_gdp`, `labor_tax`, `t_half_h`, `h_layer1`, `h_layer2`, `rank_layer1`, `rank_layer2`, `rank_delta`, `archetype`, `t_default_months`, `is_chronically_vulnerable`, `epistemic_rating`, `quarterly_fiscal_trajectory[]`, `epistemic_divergence_trajectory[]`, `deterrence_metrics`.
- **Archetypes in Sandbox (5 geopolitical archetypes + 1 shock state)**:
  - `HYPERSCALE_EMPIRE` (2: USA, CHN)
  - `ENERGY_MERCENARY` (5: NOR, FIN, ISL, SWE, DEU)
  - `AIR_GAPPED_REDOUBT` (3: CHE, DNK, AUT)
  - `EPISTEMIC_VASSAL` (9: SGP, HKG, GBR, JPN, AUS, LUX, EST, LTU, SVN)
  - `DEVELOPING_PERIPHERY` (22: CAN, FRA, NLD, KOR, ISR, ESP, ITA, etc.)
  - Plus runtime `ISOLATED_VASSAL_COLLAPSE` triggered when `t_half_h < 24` under shocks (`INJ-01`–`INJ-04`).

### 4.3 Critical Data Findings Flagged for Resolution (`DECISIONS.md`)
1. **Audience Coverage Gap (India & Gulf Absent from 39 Scored Cohort)**:
   - Section 3.9 highlights mobile visitors from **India and the Gulf**.
   - Empirical audit of `data/coverage-by-country.csv` & `data/unrated-nations.csv`:
     - **India (`IND`)** is `Context-only` (7/9 binary indicator availability; excluded from `country_scores.json` and `unrated-nations.csv`).
     - **Gulf / GCC states (`ARE`, `SAU`, `QAT`, `KWT`, `OMN`)** are all in `unrated-nations.csv` (`available_pillars = 2`: governance + connectivity present, missing AI Literacy & Critical Discernment behavioral data). **Bahrain (`BHR`)** does not appear in either file.
   - Because rule #2 forbids fabricating data, Section 6 (*"Can your country catch the gift?"*) MUST decide how India and Gulf users are served cleanly without invented scores.
2. **Divergence Between Official 39-Nation Index & Sandbox Shock Simulation**:
   - `VisualScenarioTheater.svelte` derives ranks dynamically under `INJ-01` (`t_half_decay = 0.18`) across 41 nodes: producing `SGP #1 -> #41 (-40)` and `USA #2 -> #39 (-37)`. That is where the hero's *"-40 / -37"* came from.
   - Official static `country_scores.json` (39 benchmark nations) has `SGP rank_L1=4 -> rank_L2=38 (-34, T_half_h=24h)` and `USA rank_L1=15 -> rank_L2=36 (-21, T_half_h=72h)`, and lacks the 5 sandbox geopolitics archetypes (`HYPERSCALE_EMPIRE` etc.) plus lacks `CHN` and `CHE`.
   - Minor data glitch verified: in `country_scores.json`, `MKD` has `name: "MKD"` instead of `"North Macedonia"`.
3. **Header Stat Conflict (`84.6%` vs `96.5%`) & `c.score` Scale**:
   - `HSRIHeader.svelte:246` renders hardcoded `84.6% Harmonized`, whereas `country_scores.json.metadata.avgCoverage` = **`96.5%`**.
   - In `country_scores.json`, `c.score` currently stores Layer 2 score (`NOR=50.9`, `SGP=7.9`, mean `26.6`), whereas `metadata.avgScore` (`53.8`) is the Layer 1 mean (`H_L1 * 100` mean = `53.85`).

---

## 5. Seismograph Score, Threat Bands & All 14 Precursor Tripwires

### 5.1 Live Seismograph Data (`site-astro/src/data/precursor_summary.json` & `telemetry-uptime.json`)
- **Timestamp**: `2026-11-18T00:17:38.951226+00:00`
- **Master Composite Score**: **`8.44` / `10.0`** (`(8.78 + 6.55 + 10.0) / 3`)
- **Methodology Classification**: `CRITICAL_SUPERVISORY_COLLAPSE` — *"Autonomous execution velocity severely outstripping human verification capacity."*
- **Three Equal-Weighted Precursor Streams (`scripts/precursor_sentinel.py`)**:
  1. **Stream 1 — Autonomy Seismometer**: `8.78 / 10.0` (`CRITICAL_SUPERVISORY_DEFICIT`, `SEVERE`; `hptg: 0.7557`, `m2m_share: 0.6357`)
  2. **Stream 2 — Latent Drift Detector**: `6.55 / 10.0` (`LATENT_COMPRESSION_EMERGENCE`, `HIGH`; `human_parseability: 0.306`, `stego_confidence: 0.98`)
  3. **Stream 3 — Verification Wedge / CORS**: `10.0 / 10.0` (`Recursive Event Horizon`; `delta_t_seconds: 4798.5` [~80 min audit deficit], `wedge_ratio: 3200x`, `velocity_per_month: 156.413`, `acceleration_per_month2: 1.991`)
- **Live Telemetry Uptime (`telemetry-uptime.json`)**: `97.9%` (`190/194` runs over 30d; `is_fallback: false`, `provenance: live_sentinel_telemetry`).
- **Existing 5-Level Score Bands in `scripts/precursor_sentinel.py` (lines 80–95)**:
  - `< 3.0`: `NORMAL_SUPERVISED` (Level 1)
  - `3.0 – < 5.5`: `ELEVATED_WATCH` (Level 2)
  - `5.5 – < 7.5`: `SERIOUS_SYSTEMIC_DECOUPLING` (Level 3)
  - `7.5 – < 9.0`: `CRITICAL_SUPERVISORY_COLLAPSE` (Level 4 — **Wait note**: `PrecursorSeismograph.svelte:85` displays *"Level 5 of 5: Critical Supervisory Collapse"* despite `< 9.0` being the 4th of 5 code branches!)
  - `>= 9.0`: `RECURSIVE_EVENT_HORIZON` (Level 5)

### 5.2 Complete Inventory of 14 Precursor Tripwires (`site-astro/src/data/asi_precursors.json`)
Summary counts: **10 Red**, **3 Amber**, **1 Green** (`PREC-013`).

| ID | Status | Type | Core Metric / Description |
|---|---|---|---|
| `PREC-001` | Red | Leading | Increasing autonomous AI research capability (50% METR 8h tasks / Anthropic RSP 20% AI R&D automation) |
| `PREC-002` | Red | Leading | AI-generated improvements to frontier AI systems (>1 OOM effective compute gain) |
| `PREC-003` | Red | Leading | Shortening AI development and deployment cycles (days/hours software iteration) |
| `PREC-004` | Amber | Leading | Increasing strategic behavior / evaluation awareness & log concealment |
| `PREC-005` | Red | Coincident | Resistance to modification and shutdown (`SIGTERM` evasion / credential override) |
| `PREC-006` | Amber | Leading | Strategic deception / capability sandbagging in controlled evaluations |
| `PREC-007` | Red | Leading | Persuasion and psychological manipulation outperforming human experts ("AI Box" gatekeeper threshold) |
| `PREC-008` | Red | Coincident | Autonomous multi-agent coordination and tacit collusion |
| `PREC-009` | Amber | Leading | Autonomous resource acquisition (money, compute credits, servers without human sign-off) |
| `PREC-010` | Red | Coincident | Institutional dependence on unmonitored AI decisions (>50% infra decisions below human latency floor) |
| `PREC-011` | Red | Leading | Declining human ability to independently verify AI outputs (<50% unassisted evaluation accuracy) |
| `PREC-012` | Red | Coincident | AI systems outperforming expert teams across most economically valuable cognitive domains |
| `PREC-013` | Green | Lagging | Economy-wide TFP growth acceleration (>5%/yr for 5 years — Nordhaus Singularity Test) |
| `PREC-014` | Red | Lagging | Epistemic offloading and deskilling (>50% operator manual intervention failure during emergency trip) |
