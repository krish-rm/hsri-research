# DECISIONS.md — Architecture, Data Mapping & Open Questions (Phase 0)

> **Status**: `DRAFT FOR OWNER REVIEW (CHECKPOINT 0)`  
> **Scope**: Records all Section 13 open questions plus concrete data-mapping judgment calls surfaced during Phase 0 Audit (`AUDIT.md`). Per Section 14, no silent assumptions will be shipped without owner resolution or explicit documentation here.

---

## PART A: Section 13 Open Questions for the Owner

### Q1. Pulse Bands: What Seismograph score ranges map to `Steady / Stirring / Rising`, and does the methodology support those words?
- **Empirical Evidence from Codebase (`scripts/precursor_sentinel.py` + `scripts/wedge_accelerometer.py`)**:
  - Current composite score is **`8.44 / 10.0`** (`precursor_summary.json`), driven by Stream 1 (`8.78`), Stream 2 (`6.55`), Stream 3 / CORS (`10.0`, `3,200x` speed ratio, `80.0 min` verification deficit). `10 of 14` precursor indicators (`asi_precursors.json`) are `red`, `3 amber`, `1 green`.
  - Code defines 5 internal tiers (`< 3.0` Normal Supervised; `3.0–5.5` Elevated Watch; `5.5–7.5` Serious Systemic Decoupling; `7.5–9.0` Critical Supervisory Collapse; `>= 9.0` Recursive Event Horizon).
- **Methodological Tension**:
  - The brief specifically requires a calm homepage Pulse strip (`Steady` / `Stirring` / `Rising`) without fear-mongering, while also enforcing honesty (Section 14: *"keep the research accurate and adjust the story layer"*).
  - Mapping today's `8.44 / 10.0` to **`Rising`** is accurate without hyperbole. However, mapping `8.44` to `Steady` or `Stirring` would contradict the underlying `CRITICAL_SUPERVISORY_COLLAPSE` finding.
- **Recommended Mapping (`DRAFT` for sign-off)**:
  - `0.0 – 3.9`: **`Steady`** (corresponds to `NORMAL_SUPERVISED` & low `ELEVATED_WATCH` where human oversight keeps pace)
  - `4.0 – 6.9`: **`Stirring`** (corresponds to early `ELEVATED_WATCH` & `SERIOUS_SYSTEMIC_DECOUPLING`, detectable speed gap emerging)
  - `7.0 – 10.0`: **`Rising`** (corresponds to upper decoupling & `CRITICAL_SUPERVISORY_COLLAPSE` / `RECURSIVE_EVENT_HORIZON` — today's `8.44/10` clearly sits in **`Rising`**, paired with the calm weekly sentence and `"Technical reading: 8.44/10"` tooltip).

---

### Q2. Capability & `"x of 5 things in place"` in Section 6 ("Can your country catch the gift?")
- **What Existing Index Fields Must Feed It (Zero Fabrication)**:
  - Under `country_scores.json` (39 nations), every rated nation has audited values for:
    1. `T_half_h` (offline survival window in hours)
    2. `pillars.digital_infrastructure` (`0–100`) & `layer2_pillars.p6_decoupling` (`0–1`)
    3. `pillars.critical_discernment` (`0–100`) & `layer2_pillars.p5_epistemic` (`0–1`)
    4. `pillars.institutional_governance` (`0–100`) & `layer2_pillars.p7_coordination` (`0–1`)
    5. `layer2_pillars.p8_post_labor` (`0–1`) / `pillars.ai_literacy` (`0–100`)
- **Proposed Deterministic `"x of 5 things in place"` Rule (`DRAFT` — 5 Binary Checklist Thresholds Derived Strictly from Real Metrics)**:
  1. **Offline safety buffer** (physical fallback if cloud pauses): `T_half_h >= 168` (at least 1 full week of physical continuity; `168h = 7 days` vs median `200h`). *Note*: Threshold alternative `>= 72h` aligns to the 72h Analog Override safeguard mandate — confirm `>= 72h` vs `>= 168h`!
  2. **Clean infrastructure foundation**: `pillars.digital_infrastructure >= 70.0`.
  3. **Public truth & checking skill** (critical discernment): `pillars.critical_discernment >= 70.0`.
  4. **Rule-making & safety oversight** (institutional governance): `pillars.institutional_governance >= 70.0`.
  5. **Economic / job-shift cushion** (`layer2_pillars.p8_post_labor >= 0.25`, or balanced no-trap profile `!high_compute_trap`).
  - *Wish-Specific Relevance (`shadowTag`)*: Each wish's summary highlights which of those 5 checks correspond to its `shadowTag` (`Truth` -> check #3, `Control`/`Power` -> check #4, `Dependence` -> checks #1 & #2, `Speed` -> checks #1 & #5), while displaying exact score `x of 5`.
  - *Examples under proposed rule (`>= 72h` option)*:
    - **Norway (`NOR`)**: 5/5 (or 5/5 checks pass: `T_half=1440h`, Infra `91.7`, Discernment `88.9`, Governance `87.4`, P8 `0.39`).
    - **Singapore (`SGP`)**: 2/5 (`T_half=24h` fails, Governance `63.3 < 70` fails, P8 `0.139 < 0.25` fails; passes Infra `88.8` & Discernment `84.5`).
    - **United States (`USA`)**: 2/5 (passes Infra `92.0` & `T_half=72h`; fails Discernment `62.0`, Governance `69.5`, P8 `0.097`).
- **CRITICAL SUB-QUESTION FOR SECTION 6: How do we handle India & Gulf visitors?**
  - **Audit Finding**: Neither **India** nor **any Gulf state (`ARE`, `SAU`, `QAT`, `KWT`, `OMN`, `BHR`)** is in the 39 scored nations (`country_scores.json`). India is `Context-only` (7/9 binary tracking in `coverage-by-country.csv`) and `ARE`/`SAU`/`QAT`/`KWT`/`OMN` are in `unrated-nations.csv` (`2 of 4` pillars observed, missing cognitive discernment microdata).
  - **Proposed Honest UX (`DRAFT`)**: Include India and the Gulf countries in the country picker **strictly tagged as *"Data Partial / Not Yet Fully Rated"*** (never invent an `x/5` or survival score!). Show honestly which checks have real partial observations (`data/coverage-by-country.csv` & `data/unrated-nations.csv` — e.g. *"India has digital & school data tracked, but public verification and bias data aren't measured internationally yet"* / *"UAE has strong infrastructure and government readiness data, but adult AI discernment isn't measured yet"*), plus offer a comparison to the 39 benchmark economies. **Owner decision required.**

---

### Q3. Languages: Which two languages come after English first?
- **Context**: Prompt cites mobile visitors in **India and the Gulf** (Section 3.9), Kodi/Kochi default city (Section 6/9), with future set `Malayalam, Hindi, Tamil, Arabic` (Section 10), and Phase 6 deliverable of `2 extra languages`.
- **Options**:
  - **Option A (Recommended)**: **Malayalam (`ml`) + Hindi (`hi`)** OR **Malayalam (`ml`) + Arabic (`ar`)** (gives both immediate regional anchoring for Kochi/Kerala and RTL Gulf coverage test early in Phase 6).
  - **Option B**: **Hindi (`hi`) + Arabic (`ar`)** (broadest speaker reach across India + Gulf).
- **Need Owner Choice** so RTL CSS/font architecture can be validated early even while copy starts in English `i18n` keys.

---

### Q4. Backend and Hosting: Current host, and is an edge function + small store acceptable?
- **Audit Finding**: Site currently deploys as 100% static HTML/CSS/JS via **GitHub Pages** (`gh-pages` branch, CNAME `humanityreadiness.org`). There is no active runtime server or serverless DB (`hsri_engine/` is standalone Python Docker not connected to the domain).
- **Options for Phase 3 (Crowd Aggregates, Moderated Wish Wall, Friday Recap Opt-In)**:
  - **Option A (Recommended if DNS is on Cloudflare)**: **Cloudflare Workers + D1/KV** (keeps static origin on GitHub Pages or Cloudflare Pages, zero cold-start latency in India/Gulf, free tier covers large traffic, enforces server-side `n >= 20` threshold before returning counts, strips PII).
  - **Option B**: **Supabase (Edge Functions + Postgres)** or **Netlify/Vercel Functions** wired as external API endpoint called by client islands on `humanityreadiness.org`.
- **Owner Confirmation Needed**: Who controls `humanityreadiness.org` DNS (Cloudflare vs registrar), and is deploying a minimal serverless endpoint + DB (e.g., Cloudflare Worker + D1 or Supabase) approved for Phase 3? *(Note: Phases 1 & 2 work 100% statically with `localStorage` `hr:v1:*`, needing zero backend.)*

---

### Q5. Illustration and Animation: In-house, commissioned, or AI-assisted with human review + budget range?
- **Audit Finding**: `site-astro/public/assets/scenarios/` already contains **26 original linocut/illustrated plates (`sc-01`–`sc-26.webp`)**. No harbour skyline, Kalpa character, or custom 4-beat wish illustrations exist yet.
- **Plan for Phases 1–4**:
  - **Phases 1–2**: Hand-crafted lightweight **inline SVG + CSS / Web Animations API** for the Kochi/Dubai/Chennai harbour skyline hero + interactive 4-beat animations, paired cleanly with `prefers-reduced-motion` static frames and zero heavy media overhead (< 150 KB gzip budget).
  - **Phase 4 (Pilot Episode 1 & bespoke wish plates)**: Needs owner direction on whether animated/illustrated plates for Meera, Ouseph, Zara, Sarojini, Adil will be AI-assisted + human-reviewed in-house or externally commissioned (plus target budget range).

---

### Q6. Moderation: Who reviews free-text wishes and under what policy?
- **Audit Finding**: Zero moderation queue exists today.
- **Proposed Default Policy (`DRAFT`)**: All free-text submissions enter a hidden `pending` queue (never auto-published). Automated pre-filter rejects URLs, phone numbers, emails, slurs, or political/medical prescriptions, and strips PII. Maintainer / designated editor approves weekly batches before inclusion on the Wish Wall (credited optionally via first name/handle only). **Needs owner assignment of reviewer role.**

---

### Q7. Friday Recap Channel: Email, WhatsApp, or both?
- **Context**: Prompt targets mobile visitors in India and the Gulf where WhatsApp engagement is high, alongside email subscribers.
- **Technical Implication**:
  - Email (`Resend` / `Buttondown` / `Postmark`) is lightweight, low-cost, zero template approval overhead.
  - WhatsApp Business API requires Meta Business verification, per-message conversation pricing, and opt-in template approval (or starting with a public **WhatsApp Channel** link + Email digest in Phase 5 until volume justifies API costs!).
- **Need Owner Choice**: Email only, WhatsApp Channel + Email, or automated WhatsApp Business API?

---

### Q8. Day Zero: Go ahead and build later, or hold until retention is proven?
- **Default**: Per Section 8, keep **Day Zero** unannounced and unbuilt until Phase 5 sets and validates core return retention baselines. **Confirm hold.**

---

## PART B: Additional Judgment Calls Discovered in Phase 0 Audit

### J1. Data Completeness Figure Conflict (`84.6%` vs `96.5%`)
- **Audit Finding**: `HSRIHeader.svelte:246` displays `84.6% Harmonized`, whereas `country_scores.json.metadata.avgCoverage` = **`96.5`** (verified exact mean of `observedCount / totalRetained` across all 39 countries = `96.53%`). Meanwhile the prompt specifically noted `"existing key numbers: 39 nations, benchmark mean 53.8/100, 84.6% data completeness, Preview Release status"`.
- **Decision Required**: Should Section 10 ("Go deeper") display **`84.6%`** (matching existing header continuity) or **`96.5%`** (exact verified completeness mean inside `country_scores.json`, updating the header discrepancy)?
- **Draft Recommendation**: Display **`96.5%`** (matching `country_scores.json` empirical audit) and note the change in `CHANGELOG.md`, unless `84.6%` refers to a separate Layer-1+Layer-2 harmonized share that the owner wants preserved.

### J2. Country Index Truth vs Sandbox Simulation Values (`39` vs `41` Nations & Metrics)
- **Audit Finding**:
  - Section 6 ("Can your country catch the gift?") maps: survival rank, rank shift, half-life, archetype, weakest link, adoption rank.
  - `country_scores.json` (**39 nations**) has empirical `rank_L1`, `rank_L2`, `rank_delta`, `T_half_h`, `bottleneck_pillar`, **no** sandbox geopolitics archetypes (uses `cautious_observer`/`strategic_adapter`), and **no** China (`CHN`) or Switzerland (`CHE`).
  - `civilizational_sandbox_payload.json` (**41 nodes**: 39 + `CHN` + `CHE`) has geopolitics archetypes (`HYPERSCALE_EMPIRE`, `ENERGY_MERCENARY`, `AIR_GAPPED_REDOUBT`, `EPISTEMIC_VASSAL`, `DEVELOPING_PERIPHERY`) and *different* baseline half-lives (`SGP: 4h`, `USA: 14h`) plus dynamic `INJ-01` rank shifts (`SGP -40`, `USA -37`).
- **Draft Resolution (for Owner Sign-off)**:
  - Section 6 **"Can your country catch the gift?"** reads **strictly from authoritative `country_scores.json` (39 nations)** for survival rank (`rank_L2`), adoption rank (`rank_L1`), rank shift (`rank_delta`), half-life (`T_half_h`), and weakest link (`bottleneck_pillar`), linking straight to `/countries/[id]/` (which avoids 404s on `CHN`/`CHE`!).
  - For plain-language **"archetype"**, derive deterministically from `country_scores.json` / sandbox archetype mapping (`AIR_GAPPED_REDOUBT` -> *"Steady Offline Builder"*, `EPISTEMIC_VASSAL` -> *"Fast Digital Adopter"*, etc.) — flagged transparently here, with full simulation archetypes (`CHN`/`CHE` peers) living inside `/sandbox/` (**"Open the Lab"**).
  - Also normalize `MKD`'s missing display name (`"MKD"` -> `"North Macedonia"`) when rendering in Section 6.

### J3. Reality Meter & Honesty Labels for Wishes
- Prompt rule #3 & #4 require: *no invented numbers, honesty label on every wish (`Imagination`, `Possible soon`, `Real today`) with 1-line justification, and Reality Meter (`0–100`) only with a real cited source & `lastReviewed` date*.
- **Draft Plan for Phase 2**: For `Reality Meter`, anchor directly to verifiable empirical milestones in existing repo telemetry (`precursor_summary.json`, `autonomy_seismometer.json`, `asi_precursors.json` such as `PREC-001`..`PREC-014` + real cited papers/benchmarks like METR RE-Bench / SWE-bench), rather than arbitrary qualitative percentages. Where a wish is `Imagination` (e.g., `Riemann Hypothesis`, `Time-Turner`), mark meter qualitatively or at a documented conservative baseline with explicit rationale for owner review.

### J4. CI/CD Post-Deploy Smoke Test Compatibility (`.github/workflows/deploy.yml`)
- **Audit Finding**: `deploy.yml` automatically fails deployment if `/` lacks the exact substring `"Humanity Superintelligence Readiness Index"` or links to `/methodology/`, `/coverage/`, and `/monograph/`.
- **Resolution Plan (Phase 1)**: Preserve `"Humanity Superintelligence Readiness Index"` in header/footer brand identity and `<title>` / metadata, and keep `/methodology/`, `/coverage/`, `/monograph/` links in Section 10 ("Go deeper") and `HSRIFooter` so every automated CI check stays green with zero broken deployments.

### J5. Footer New Links (`Languages`, `Privacy`, `Join Friday's recap`)
- Current `HSRIFooter.svelte` has no `/privacy/` route and no language selector.
- **Draft Plan (Phase 1)**: Create `/privacy/` page clearly documenting anonymous local-first storage (`hr:v1:*`), export/delete controls, and future Phase 3 cohort `n >= 20` rule; add `Languages` switcher/anchor (English active, upcoming queue visible) and `Join Friday's recap` link pointing cleanly to Section 7.
