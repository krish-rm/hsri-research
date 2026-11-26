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

---

## Phase 2 Calibration & Design Decisions (2026-11-26)

### 9. Readiness Lights Formula (`hr:v1:*`, Glow Levels `0–3`)
- Lights display **only** visual glow tiers (`0 = unlit`, `1 = spark`, `2 = warm`, `3 = bright`) with zero numeric ranking scores shown in the UI.
- **Clarity (`0–3`)**: +1 per unique wish completed through Beat 4 (`Way`), capped at 3.
- **Foresight (`0–3`)**: +1 per unique wish where the visitor chooses a pre-Wobble guess OR selects a `Foresight`-mapped worry in Beat 3, capped at 3.
- **Fairness (`0–3`)**: +1 per unique wish where the visitor selects a `Fairness`-mapped worry in Beat 3, capped at 3.
- **Wisdom (`0–3`)**: +1 per unique wish where the visitor selects a `Wisdom`-mapped worry OR commits to a human `Way` habit pledge, capped at 3.
- **Capability (`0–3`)**: +1 per unique human `Way` habit pledge (capped at 2) **plus `+1` ONLY when the visitor explicitly selects a country in Section 6 whose rated checklist has `>= 3 of 5` checks in place** (ambient timezone/locale pre-detection never alters `hr:v1:country` or `Capability`; unrated countries contribute `0` and clearly explain why).

### 10. Trail Card (`3` Wishes) & Shadow Map (`5` Wishes)
- **Playable Wish Pool**: Ships the 3 verbatim Checkpoint 1 flagship wishes (`sanjeevani`, `jarvis-for-my-life`, `prove-riemann-hypothesis`) plus 2 cross-door wishes (`walk-into-classic-film`, `fix-my-river`, clearly tagged **`DRAFT`** on new Wobble/Weight/Way copy for owner review) so visitors can explore all 5 doors and reach the 5-wish Shadow Map unlock.
- **Trail Archetype Selection**: Deterministic priority from dominant lights & spotted shadows:
  - `The Verifier` (Foresight/Truth verification focus)
  - `The Neighbour` (Fairness/Power equity focus)
  - `The Builder` (Capability/Speed resilience focus)
  - `The Keeper` (Wisdom/Dependence human stewardship fallback)
- **Client-Side Export**: `1200×630` and `1080×1920` PNG exports + `.svg` render locally via HTML5 Canvas (`0 KB` third-party libraries).

### 11. Reality Meter Grounding & Provenance (Superseded in Checkpoint 2.5 -> See §15)
- Earlier Phase 2 draft displayed `0/100` baselines and `64/100` (for Jarvis from `m2m_composite_share` in `autonomy_seismometer.json`). Replaced in §15 at owner review.

### 12. Spanish & Arabic Live Localization (`B.1`)
- Implemented full dictionary parity across English (`en`), Spanish (`es`), and Arabic (`ar` with live `dir="rtl"` and mirrored margins/arrows via `BaseLayout.astro` + `store.ts` + static `data-hr-t` DOM sync).
- Arabic renders via crisp native system sans stacks with **zero extra external webfont bytes**, keeping Mandarin/Hindi deferred until CJK/Devanagari font budgets are reviewed.

---

## Phase 2.5: Terminology & Toto Guide Architecture (2026-11-26)

### 13. Terminology Migration (`wish` -> `breakthrough`, `Kalpa` -> `Toto`)
- **User-Facing Vocabulary**: Replaced every user-facing occurrence of `wish` / `wishes` / `wisher` and `Kalpa` / `Wishgiver` with **`breakthrough` / `breakthroughs` / `participant`** and **`Toto`**, updating the headline to `"Humanity Readiness: are we ready for what we're asking superintelligence to deliver?"`, domains to **Open Problems, Everyday Technologies, Transformative Powers, Culture & Creativity, Public Good**, and closing line to `"Every great breakthrough needs a ready world."`.
- **Natural ES/AR Renderings & Native Review (`reports/TRANSLATION_REVIEW_AR_ES.md`)**:
  - **Spanish (`es`)**: Rendered `breakthrough` as **`avance` / `avances`**, `ready world` as **`mundo preparado`**, and preserved `Toto` untranslated per brief §9.5.
  - **Arabic (`ar`)**: Rendered `breakthrough` as **`إنجاز` / `إنجازات`** rather than `اختراق` (cyber intrusion), localized `Toto` phonetically as **`توتو`**, and updated `wishWall.emptyHeadline` (`"What the world is asking for"`) from loose `"الخريطة المشتركة العالمية"` to plain, literal **`تُفتح صفحة «ما الذي يطلبه العالم؟» بعد أول 20 مساهمة مجهولة الهوية.`** per Checkpoint 2.5 review Fix #4. Full candidate alternatives (`نقلة نوعية`, `كشف/طفرة علمية`) and complete AR/ES `Meet Toto` + `/toto/` string sheets sit in `reports/TRANSLATION_REVIEW_AR_ES.md`.
- **Backward-Compatible Internals & Migration Plan**: Preserved `wishes.json`, `wishes.schema.json`, existing breakthrough `id` strings, DOM anchor IDs (`#wish-doors`, `#wish-wall`), and all `hr:v1:*` browser storage keys unchanged until a future v2 storage migration.

### 14. Toto Guide Character, Greeting (`hr:v1:intro_seen`) & Trademark Note
- **Storytelling Disclaimer**: Toto is explicitly labelled as a fictional superintelligence storytelling device (`Fictional, not a real system`), never a forecast or real AI product.
- **Visual Spec (`TotoIllustration.svelte`)**: Original inline SVG glowing dawn orb inside a thin orbital ring with three poses (`calm`, `curious`, `apologetic`), zero animal/dog likeness, zero SVG blurs/filters, and static `prefers-reduced-motion` support.
- **Presence**: Appears in Hero SVG (`#toto-glow`), `MeetTotoCard`, one-time dismissible Breakthrough Player greeting (`hr:v1:intro_seen` with `Skip` + `Escape`, clearable in `/privacy/`), all 4 beat speech bars, and `/toto/`.
- **Merchandise/Brand Flag (§9.5)**: *TOTO* is an existing commercial brand and band name; acceptable strictly as a fictional non-commercial storytelling guide character, flagged for legal review prior to any merchandise.

---

## Checkpoint 2.5 Owner Decisions & Fixes (2026-11-26)

### 15. Status Labels (`draft` / `owner_approved`), 3-Step Reality Meter & Dev Gating
- **Strict Status Enum**: All breakthroughs use strictly `"status": "draft" | "owner_approved"`. All 5 current breakthroughs (`wishes.json`) and all 15 Phase 6 drafts (`wishes.draft15.json`) are marked `"draft"` until explicit owner sign-off.
- **Build-Flag Gating (`site-astro/src/lib/breakthroughCatalog.ts`)**:
  - `PUBLIC_SHOW_DRAFTS === 'true'` (enabled by `npm run build:preview` / `astro dev`, **unset on production `npm run build`**): renders the visual `DRAFT` pill in preview builds and hides every `DRAFT` pill on production builds.
  - `PUBLIC_SHOW_DEV_BREAKTHROUGHS === 'true'` (enabled by `npm run build:dev` / `astro dev`, **unset on production `npm run build`**): gates `wishes.draft15.json` so Vite tree-shakes the 15 unapproved entries out of the production bundle completely.
- **3-Step Reality Meter (Fix #2 — Zero Unsupported Numeric Scores)**:
  - Removed the `0–100` progress bar and removed the **`Jarvis` `64` metric** because `autonomy_seismometer.json` (`m2m_composite_share = 0.6357`) measures macro M2M traffic/billing rather than personal AI life-assistant readiness.
  - Replaced with a 3-step scale (`Imagination` | `Possible soon` | `Real today`), one-line plain `reason`, cited `source` (`sourceUrl`), and `lastReviewed` date on every entry. An optional `observedMetric` field is permitted by `wishes.schema.json` **strictly only when `directCapabilityMatch === true`**.
- **Capability Rule Sign-Off (Fix #3)**: Explicit-selection `Capability` rule (`>= 3 of 5` safeguards adds `+1` glow tier) confirmed as a documented **editorial choice** (not a statistical changepoint).
- **Stacked Merge Gate & Planning Docs (Fix #5, Next Work B & C)**: Full stack (`Phase 1` -> `Phase 2` -> `Phase 2.5`) merges together after owner PageSpeed sign-off on `hsri-phase2-preview`; Phase 1 alone never merges. Merge checklist (`reports/PHASE_2_5_MERGE_CHECKLIST.md`), Pilot Episode 1 storyboard (`reports/PILOT_EPISODE_1_STORYBOARD.md`), and Phase 3 backend design doc (`reports/PHASE_3_DESIGN.md`) checked in as `DRAFT` documents.



