# Phase 2.5 -> Main Merge & Deploy Checklist

> **Status**: Verified for `feat/phase-2-5-toto` (`CHECKPOINT 2.5 REVIEW`, Fix #5). Do NOT merge to `main` until owner confirms `pagespeed.web.dev` Mobile numbers for `hsri-phase2-preview` and approves stacked branches.

---

## 1. Branch Stack Integrity (Why Only the Full Stack Merges)
- `main`: `46d158b` (untouched)
- `feat/phase-1-story-reframe`: `d825396` (**DO NOT MERGE ALONE** — still carries pre-2.5 `"wish"` / `"Kalpa"` wording)
- `feat/phase-2-wish-player`: `e030ddd` (stacked on Phase 1)
- `feat/phase-2-5-toto`: **HEAD** (stacked on Phase 2; contains unified Headline v2, `"breakthrough"` terminology, `Toto` guide, 3-step Reality Meter, fixed AR/ES strings, build-flag gating for `draft` badges & 15 dev breakthroughs)

---

## 2. Production Tree Cleanliness (Confirmed Zero Preview Artifacts)
- [x] `vercel.json`: **Not present** anywhere in `hsri-research` repo (`preview` deploys live exclusively out-of-tree under artifact `scratch/`).
- [x] `preview-dist` / `preview-p2-dist`: **Not present** anywhere in `hsri-research` repo (`site-astro/dist/` is gitignored via `dist/`).
- [x] `X-Robots-Tag: noindex, nofollow` / `robots` preview headers: **Not present** in `site-astro/` source, layouts, or `.github/workflows/deploy.yml`.
- [x] Production `npm run build` (`PUBLIC_SHOW_DRAFTS` unset, `PUBLIC_SHOW_DEV_BREAKTHROUGHS` unset):
  - `SHOW_DRAFT_BADGE === false` -> zero `DRAFT` badges rendered on production pages or players.
  - `INCLUDE_DEV_BREAKTHROUGHS === false` -> `wishes.draft15.json` tree-shaken out of production JS bundles (verified via dist grep).

---

## 3. GitHub Pages Deploy Workflow (`.github/workflows/deploy.yml`) Smoke Check Matrix
All assertions enforced by `.github/workflows/deploy.yml` after push to `main`:

| Smoke Assertion | Status in `npm run build` (`dist/`) | Verification Target |
|---|---|---|
| `Humanity Superintelligence Readiness Index` in `/` HTML | Verified | `<title>` & footer brand in `site-astro/dist/index.html` |
| Link `href=".../methodology/"` on `/` | Verified | Section 10 `GoDeeperSection` + Header/Footer |
| Link `href=".../coverage/"` on `/` | Verified | Section 6 unrated link + Section 10 `GoDeeperSection` |
| Link `href=".../monograph/"` on `/` | Verified | Section 10 `GoDeeperSection` + DOI archive link |
| `/coverage/` 200 + `"Global Geographic Coverage"` | Verified | Static page built |
| `/research-updates/` 200 + `"Literature Digests"` | Verified | Static page built |
| `/methodology/` 200 + `"EXP-01"` & `"IRB PACKAGE READY"` | Verified | Static page built |
| All 5 CSVs under `/downloads/` return `200` | Verified | Copied from `site-astro/public/downloads/` |
| `test_no_automation_workflows` (`tests/test_agents.py`) | Verified (`16/16 passed`) | Zero added files in `.github/workflows/` |

---

## 4. Merge Execution Steps (Run Only After Owner Sign-Off)
1. Confirm owner approves `status: "draft" -> "owner_approved"` for the breakthroughs to ship (so any content change lands on `feat/phase-2-5-toto` before merge).
2. Run `cd site-astro && npm run build` (without preview env flags) and confirm zero `DRAFT` badges and zero `wishes.draft15.json` titles inside `site-astro/dist/_astro/`.
3. Fast-forward or squash-merge stacked PR `feat/phase-2-5-toto` into `main` on GitHub (never force-push `main`).
4. Watch GitHub Actions `Deploy Web Portal and Documentation` complete cleanly on `https://humanityreadiness.org/`, including `All smoke tests passed successfully.`
5. Verify live URLs `/`, `/toto/`, `/privacy/`, `/countries/`, `/seismograph/`, `/scenarios/`, `/monograph/`, `/methodology/`, `/data/`, and `/coverage/` all return `200` without `noindex`.
