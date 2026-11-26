# DECISIONS.md — Architecture, Data Mapping & Owner Decisions

> **Status**: `CHECKPOINT 0 DECISIONS RATIFIED BY OWNER (2026-11-26)`  
> **Scope Rule**: HSRI is a **strictly global benchmark** (`humanityreadiness.org`). Zero single-country, single-city, or single-region assumptions are embedded as defaults.

---

## PART A: Ratified Section 13 Decisions

### 1. Global Scope & Locale Detection
- **Audience**: Worldwide across every region. No country or region is treated as a privileged default audience.
- **Country Default in Section 6 ("Can your country catch the gift?")**: Client detects visitor's country automatically from browser locale (`navigator.languages` / `navigator.language`) and timezone (`Intl.DateTimeFormat().resolvedOptions().timeZone`) where unambiguous, falling back cleanly to a neutral global starter (**Global Overview / Australia A–Z or #1 Norway benchmark comparator**, with balanced cross-continent comparison chips).
- **Hero Coastal City Switcher**: Default scene renders a neutral coastal port city (**Coastal Harbour**); interactive switcher lets visitors view culturally varied coastal city examples across every region: **Lagos, São Paulo, Mumbai, Berlin, Jakarta, Dubai, Toronto, Nairobi**.

### 2. Pulse Bands (`Humanity's Pulse`) — APPROVED
- **Range Mapping** against `precursor_summary.json` (`master_precursor_threat_score`, `[0, 10]`):
  - `0.0 – 3.9`: **`Steady`** (oversight keeps pace with automated systems)
  - `4.0 – 6.9`: **`Stirring`** (early divergence; checking plans growing useful)
  - `7.0 – 10.0`: **`Rising`** (systems executing significantly faster than unassisted review; aligns with methodology tiers `SERIOUS_SYSTEMIC_DECOUPLING` / `CRITICAL_SUPERVISORY_COLLAPSE`)
- **Current Readout (`8.44 / 10`)**: Displays **`Rising`**, one calm factual weekly sentence (*"Autonomous systems now solve multi-step software tasks faster than people can check line by line. That is why built-in verification plans matter."*), and `"Technical reading: 8.44 / 10"` inside the tooltip alongside `/seismograph/`.

### 3. Capability & `"x of 5 things in place"` Checklist — APPROVED
- **Scope**: Computed strictly for the **39 rated nations in `country_scores.json`**. Never calculated or invented for any country outside the 39.
- **Labeling**: Explicitly displayed as **`"A simple checklist, not a ranking"`** with a tap tooltip exposing underlying metrics.
- **Exact 5 Binary Checks (Deterministic & Traceable)**:
  1. **72-hour offline backup**: `T_half_h >= 72` *(grounded in the 72h analog override safeguard)*.
  2. **Strong everyday tech & grid**: `pillars.digital_infrastructure >= 70.0` *(editorial cutoff — see disclosure below)*.
  3. **Public skill at checking AI claims**: `pillars.critical_discernment >= 70.0` *(editorial cutoff — see disclosure below)*.
  4. **Clear rules & public oversight**: `pillars.institutional_governance >= 70.0` *(editorial cutoff — see disclosure below)*.
  5. **Jobs & public budget cushion**: `layer2_pillars.p8_post_labor >= 0.25` *(editorial floor matching Layer 2 post-labor elasticity threshold; top quartile of 39 nations)*.
- **Editorial Threshold Disclosure**: The `70.0`-point pillar cutoffs (`digital_infrastructure`, `critical_discernment`, `institutional_governance`) and `0.25` Layer 2 cushion floor are **editorial readability thresholds**, *not* statistically optimized empirical changepoints or official HSRI academic cutoffs. Users are directed to `/countries/[id]/` and `/methodology/` for continuous scores and Leontief rankings.
- **Normalization**: `MKD` in `country_scores.json` (`name: "MKD"`) is normalized to **`North Macedonia`** in UI display.

### 4. Unrated Countries Policy — APPROVED (Strictly Equal Global Treatment)
- **Universal Application**: Applies identically to **every** nation evaluated outside the 39-nation empirical index (86 rows in `data/unrated-nations.csv` + 22 `Context-only` rows & `TWN` `Partial rating` in `data/coverage-by-country.csv` — zero special handling for any nation).
- **UI Behavior**:
  - Every unrated country is selectable in the global Section 6 picker and tagged **`"Not yet rated in the full 39-nation index"`**.
  - Displays **only genuine observed fields from the real CSVs** (`available_pillars`, `missing_pillars`, `partial_coverage_notes` from `data/unrated-nations.csv`; all 9 binary coverage indicator columns `ai_lit_core`, `ai_lit_context`, `calibrated_trust`, `metacognition_core`, `metacognition_context`, `decision_agency`, `attentional_context`, `value_clarity`, `enabling_context`, plus `overall_status` from `data/coverage-by-country.csv`). Counts (`x/9`) are summed directly from those 9 binary indicator flags rather than the upstream `overall_coverage` integer (which is +1 above the binary flag sum for several rows such as BRA/ARG). Zero filled-in or estimated values anywhere. Only Guinea (`GIN`) replaces the single CSV word `"telemetry"` with `"survey tracking"` under the plain-language rule.
  - Includes a direct **`"Help us rate your country"`** link pointing to `/coverage/`.

### 5. Completeness Metric Reconciliation (`84.6%` vs `96.5%`) — APPROVED
- **Forensic Audit Result**: Commit `881a4a1` (Oct 17, 2026) replaced `{stats.avgCoverage}%` (`96.5%`) in `HSRIHeader.svelte` with hardcoded text `84.6% Harmonized`. Cross-checking every dataset (`normalized_indicators.csv = 640/663 = 96.53%`, `country_scores.json.metadata.avgCoverage = 96.5`, `raw_observations_harmonized.csv = 730/780 = 93.59%`) confirms **`84.6%` originated strictly from that hardcoded override in `881a4a1` and is stale**.
- **Resolution**: Replace `84.6%` with verified **`96.5%`** (`640/663` cells), displayed visibly on `/` with its one-line definition (`"share of retained indicators observed across 39 benchmark countries — 640 of 663 cells"`) in `HSRIHeader.svelte` and Homepage Section 10, and logged in `CHANGELOG.md`.

### 6. Country Data Sources & Plain Archetype Mapping — APPROVED
- **Single Source for Section 6**: Reads strictly from `site-astro/src/data/country_scores.json` (plus real coverage tables for unrated nations). Never mixes stylized sandbox shock ranks (`-40`/`-37`) with the 39-nation baseline (`-34`/`-21`).
- **Deterministic Plain Archetype Mapping (`country_scores.json` only, tooltip shows technical reading & `/sandbox/` link)**:
  - `H_L2 >= 0.40 && rank_delta >= -2` -> **"Steady Offline Builder"** *(Physical buffers hold strong alongside digital tools — NOR, FIN, ISL, DNK, SWE)*
  - `high_compute_trap && rank_delta < -5` -> **"Fast Digital Adopter"** *(Deep digital adoption outpacing manual backups — e.g. SGP, USA, GBR, KOR, CAN, AUS, HKG, EST, ISR)*
  - Remaining countries -> **"Balanced Contender"** *(Moderate pace with mixed physical buffers — e.g. DEU, AUT, FRA, NZL, BEL, ESP, ITA, POL, etc.)*
  - Technical transition labels (`Hyperscale Empire`, etc., plus CHN/CHE comparison nodes) live exclusively inside `/sandbox/` (**"Open the Lab"**).

### 7. Languages & i18n / RTL Architecture
- **Phase 1 Build**: All Phase 1 copy runs cleanly through typed `i18n` dictionary keys (`src/i18n/en.ts`), paired with CSS logical properties (`margin-inline`, `padding-inline`, `text-align: start`) and an inspectable **`RTL Layout Test (Stub)`** toggle (`src/i18n/rtl-stub.ts`) accessible from `#languages` so RTL mirroring (`dir="rtl"`) is proven structurally without shipping incomplete translations.
- **Language Selection Open Question**: Owner will choose the first two full global languages after reviewing the Phase 1 preview deploy (`CHECKPOINT 1`).

### 8. Backend, Moderation, Art, Recap, Day Zero & Footer Rules
- **Hosting (Phases 1–2)**: 100% static Astro build on `localStorage` (`hr:v1:*`). Phase 3 serverless backend (`Cloudflare Workers + D1` vs `Supabase`) deferred until pre-Phase 3 DNS confirmation.
- **Phase 4 Art**: AI-assisted storyboard & animatic with human review; final character visual direction locked after animatic review.
- **Wish Wall Moderation**: Owner reviews a hidden `pending` queue; no free-text wish ever auto-publishes; Strip PII before queueing.
- **Friday Recap Channel**: Deferred until after subscriber origin data is clear (**NOT built in Phase 1**; `#this-week` & footer `"Join Friday's recap"` link to a quiet Phase 4/5 teaser notice).
- **Day Zero**: **ON HOLD** until Phase 5 return retention is proven.
- **CI/CD Smoke Test (`deploy.yml`)**: Preserve exact text `"Humanity Superintelligence Readiness Index"` and `/` links to `/methodology/`, `/coverage/`, `/monograph/`.
- **Footer Additions**: New `/privacy/` route (anonymous local-first `hr:v1:*` privacy notice + interactive inspect/export/delete controls), `Languages` anchor (`#languages` switcher), and `"Join Friday's recap"` (`#this-week`).
- **Reality Meter (Phase 2 Open Sign-Off)**: Anchor percentages/ratings strictly to verifiable milestones + `lastReviewed` + `sources[]`; `Imagination` wishes receive a documented conservative baseline for owner sign-off in Phase 2.
