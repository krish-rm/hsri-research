# LTFF / Open Philanthropy — Update Memo & $120,000 Deployment Plan

> **Date:** 2026-10-14 · **Re:** HSRI 2.0 Sprint 36 Hardening — Response to Audit & Request to Deploy Funds
> **PI:** Krishnakumar Radhakrishnan, HSRI Research Consortium · krishnakumar.rmenon@gmail.com
> **Repository:** https://github.com/krish-rm/hsri-research (commit `1277a0d` → `ef3e7e8`)
> **Live Portal / Seismograph:** https://humanreadinessindex.org · https://humanreadinessindex.org/seismograph/
> **Archive:** Zenodo DOI 10.5281/zenodo.10842000 · **arXiv:** HSRI-WP-2026-02 v1.1.0 (deposit week of 2026-10-20, `cs.CY` + `cs.AI`)

---

### TL;DR — What Changed Since Submission

Your review implied three risks: **engineering fragility, abstraction debt, and actuarial overclaim.** We treated them as blockers, not notes.

**Sprint 36 (`ef3e7e8`) + follow-on (`1277a0d`) shipped in direct response:**

1. **Telemetry is now observable, not silent.** `hsri_engine/core.py:get_precursor_telemetry()` no longer swallows exceptions. Structured `logger.warning/info`, and `PrecursorTelemetryResponse` now exposes `is_fallback: bool`, `provenance: str` (`live_sentinel_telemetry` vs `deterministic_calibration_fallback`), and `data_timestamp: Optional[str]` (ISO-8601 of source file). A reviewer or CISO can now distinguish measured vs. calibrated CORS in one API call.
2. **CORS is port-hardened.** `hsri_engine/api.py` wildcard `allow_origins=["*"]` removed. Default allowlist is `https://humanreadinessindex.org` + `www` subdomain + localhost dev ports; production override via `HSRI_ALLOWED_ORIGINS` env var. No `*` in production.
3. **Abstraction debt is closed with a regulatory crosswalk.** New `docs/regulatory_crosswalk.md` maps every bespoke HSRI construct to binding law: P5 (VSR) → EU AI Act Art. 14 + NIST RMF Measure 2.5 + ISO/IEC 42001 A.6.2; P6 ($T_{\text{half}}$) → EU NIS 2 Art. 21 + CISA CPG 2.A + PPD-21; CORS/precursors → UK AISI Frontier Evals + EO 14110 §4.2; Φ/ECDL → Solvency II 2009/138/EC Art. 101/105 + NAIC RBC Rcat + LMA5583A.
4. **Peer-review rebuttal is pre-written.** New `research/preprint/anticipated_objections_rebuttal.md` answers the five inevitable objections (Leontief $\beta$=0.50 stability $W$=0.9986; CORS 10.0 grounded in measured 3,200× wedge; synthetic Rule 12 demarcation; 39-nation scope with 86 unrated register; High-Compute Trap neutrality via deterministic $V_{\text{ASI}}$). Choquet 2-additive monotonicity formally proven in `working-paper-v1.1.0.md` Appendix C ($\Delta\mu\ge0.19>0$). Reinsurance docs and `/reinsurance/` calculator now carry statutory disclaimer: *"Illustrative research — SCR calculations require qualified cedent actuary."*
5. **Tests 217/217 green, portal 52 pages rebuilt, OpenAPI re-exported.**

This memo requests deployment of the **$120,000 non-dilutive award** against exactly the operational debt your audit surfaced.

---

### The Ask — $120,000 to Make the Sentinel Live and Externally Validated

We propose to deploy the award across **two P0 deliverables** (no new pillars, no scope creep):

**A. Persistent Live Telemetry (Track 4) — turning CORS from calibrated estimate into measured signal.**
Replace weekly batch `precursor-sentinel.yml` (Mon 06:00) with persistent hourly scrapers for **SWE-bench verified** and **METR autonomy evals** as primary feeds, appending to `data/telemetry/live_feeds.jsonl` with schema `{timestamp, source, fetch_status, latency_ms, provenance, data_timestamp}`. On success `provenance=live_sentinel_telemetry`; on failure `is_fallback=true` with last-known `data_timestamp`. Public uptime badge on `/seismograph` ("Live Telemetry: 97.3% 30d · Updated 2h ago") backed by the same file the API serves. No new database — GitHub Actions + flat JSONL. This is the sole criterion that converts `CORS 10.0` from defensible to demonstrable.

**B. First External Decoupling Drill Pilot (Track 5) — validating P6 ($T_{\text{half}}$) with a sovereign partner.**
Execute one facilitated 14-day tabletop (336h) with a **named institutional host** (priority: RSIS Singapore, MBZUAI/UAE, or ETH Zurich Center for Security Studies) across the 4 subsystems (Power/Finance/Food/Telecom) using `scripts/decoupling_simulator.py` + 8 Leontief injects. Output: co-authored **HSRI Case Study 01** with measured $T_{\text{half}}$ archetype validation and published after-action report. This is the external replication the paper cannot provide alone.

> Tracks 1a (arXiv deposit) ships this week at zero cost and is not funded by this award — it is the credential that lets Tracks 4/5 be evaluated.

---

### 12-Month Deployment (two phases, four milestones)

| Phase | Months | Milestones | Verifiable Artifact |
|---|---|---|---|
| **I — Make it live** | 1–6 | M1: SWE-bench/METR hourly scrapers + `/v1/telemetry/precursors` provenance + uptime badge · M2: 60d continuous live window, public incident log | `data/telemetry/live_feeds.jsonl` (90d retention artifact) + `GET /v1/telemetry/precursors` returning `provenance=live` >90% |
| **II — Make it externally true** | 7–12 | M3: Decoupling drill pilot executed · M4: Case Study 01 + Working Paper v2.0 submission to *Nature Machine Intelligence* / *JAIR* + NeurIPS/ICML AI Safety workshop | Co-authored case study PDF + conference submission + updated Zenodo version |

### Budget — $120,000 (12 months, 100% open science, zero equity)

| Category | Use | Amount |
|---|---|---|
| PI stipend | $5,000/mo × 12 — sole full-time operator, zero burn otherwise | $60,000 |
| Frontier API & compute | $2,000/mo — 7-provider debate + 24/7 drift simulations + scraper hosting | $24,000 |
| Data & feed access | GitHub Archive, HF, eval trackers, academic DBs | $12,000 |
| Dissemination & travel | arXiv/SSRN + one workshop (NeurIPS/ICML) + pilot travel | $14,000 |
| Hosting & API infra | AWS/Fly, domain, TLS, artifact storage | $10,000 |
| **Total** | Non-dilutive, CC BY-SA 4.0, MIT code | **$120,000** |

### Success Criteria (falsifiable — you can check these from the repo)

- **Telemetry liveness:** `GET /v1/telemetry/precursors` returns `is_fallback=false` and `data_timestamp` < 24h on >90% of checks over any 60-day window; public badge history is versioned in git.
- **Pilot completion:** Signed host MOU + published Case Study 01 with measured $T_{\text{half}}$ (not simulated) within 12 months.
- **Reproducibility:** Every claim remains code-tied (`hsri_engine/`, `scripts/`, `data/`) with 217+ tests green and Zenodo-versioned DOI.

### Risks & Mitigations

- *Scraper fragility (upstream schema change):* Structured logging + `is_fallback` + last-known-good cache; no silent failure mode remains after Sprint 36.
- *Pilot access:* Parallel outreach to 3 hosts; pilot scoped as half-day tabletop (not 14 live days) to clear institutional approval; funded by this award so host cost is zero.
- *Actuarial liability:* All ECDL/Φ tables carry statutory disclaimer; commercial path positioned as telemetry license, not regulated treaty, until co-signed by accredited actuary.

---

**Commitment:** 100% of outputs remain open (CC BY-SA 4.0 / MIT), Zenodo-archived, with no paywall, no equity, no bureaucratic overhead. Funding maps 1:1 to code, data, and one external validation — the two things that convert a 70% infrastructure build into a living sentinel.

We welcome a 30-minute review call and can demo `GET /v1/telemetry/precursors` (with `is_fallback`/`provenance` live) and `/seismograph` at your convenience.

— Krishnakumar Radhakrishnan

**Appendices attached (not counted toward 2 pages):** `docs/regulatory_crosswalk.md` (2 pp) · `research/preprint/anticipated_objections_rebuttal.md` (3 pp) · `research/preprint/arxiv_submission_package.md` cover
