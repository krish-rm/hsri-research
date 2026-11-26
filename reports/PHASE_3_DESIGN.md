# Phase 3 Architecture & Privacy Design Document

> **Status**: `DRAFT` (Next Work C — design only, **zero backend code implemented yet**).
> Backend implementation begins strictly after Phase 2.5 merges clean and the owner confirms hosting + DNS control.

---

## 1. Design Goals & Non-Negotiables
1. **Anonymous by default**: Zero logins, zero persistent cookies, zero IP logging, zero browser fingerprinting, zero PII in telemetry.
2. **20-response cohort threshold (`k >= 20`)**: Neither global readiness lights, breakthrough counts, nor country-specific aggregates are returned or rendered until at least **20 distinct valid submissions** exist for that cohort. Below 20, the API returns `{ ready: false, countHiddenBelow: 20, sampleCountBucket: "<20" }` and the UI stays in honest invitation state.
3. **Never auto-publish free text**: Custom breakthrough ideas go into a **hidden `pending` moderation queue** scrubbed of email/phone/handle strings, reviewed explicitly by the owner before any `approved` item appears on `"What the world is asking for"`.
4. **No single-person tracking**: Client submission is strictly opt-in (visitor clicks contribute or completes flow without local IDs); no cross-session user token is persisted server-side.

---

## 2. Public API Endpoints & Request/Response Schema

### A. `POST /api/v1/contribute`
Records one anonymous completed breakthrough reflection. Rejects unexpected fields (`additionalProperties: false`) and rejects free-text strings.

**Request JSON**:
```json
{
  "breakthroughId": "sanjeevani",
  "weightChoice": "a",
  "lightsDelta": {
    "Clarity": 1,
    "Foresight": 1,
    "Fairness": 1,
    "Wisdom": 0,
    "Capability": 1
  },
  "country": "NOR",
  "ts": "2026-11-26T12:00:00Z"
}
```
- **Validation rules**:
  - `breakthroughId`: must match allowlist from `wishes.json` (plus approved `wishes.draft15.json` IDs when enabled).
  - `weightChoice`: `"a" | "b" | "c"`.
  - `lightsDelta`: integers strictly `0` or `1` per allowed key (`Clarity`, `Foresight`, `Fairness`, `Wisdom`, `Capability`).
  - `country`: ISO-3 uppercase `[A-Z]{3}` or `null` (only included if explicitly selected by visitor).
  - `ts`: ISO timestamp rounded server-side to **UTC hour granularity** (`YYYY-MM-DDTHH:00:00Z`) before writing, preventing second-level timing correlation!
  - **Rate limit**: Sliding window per ephemeral coarse subnet hash (salted daily rotating key in memory/KV, **never stored in DB**), max `10 requests / minute`, `30 / day`.

**Response JSON (`202 Accepted`)**:
```json
{ "accepted": true }
```

### B. `GET /api/v1/aggregates`
Returns cached global cohort summaries (and optional single `?country=ISO3` slice ONLY if that country cohort independently has `>= 20` contributions). Cached 60s at the edge (`Cache-Control: public, max-age=60, s-maxage=120`).

**Response JSON when cohort `< 20`**:
```json
{
  "cohortThreshold": 20,
  "ready": false,
  "participantBand": "<20"
}
```

**Response JSON when global cohort `>= 20`**:
```json
{
  "cohortThreshold": 20,
  "ready": true,
  "participantCount": 247,
  "ringReady": true,
  "meanLightLevels": {
    "Clarity": 2.4,
    "Foresight": 2.1,
    "Fairness": 1.9,
    "Wisdom": 2.2,
    "Capability": 1.7
  },
  "shadowDistribution": {
    "Control": 0.24,
    "Dependence": 0.27,
    "Power": 0.19,
    "Truth": 0.18,
    "Speed": 0.12
  },
  "topBreakthroughs": [
    { "id": "sanjeevani", "count": 98 },
    { "id": "jarvis-for-my-life", "count": 81 },
    { "id": "prove-riemann-hypothesis", "count": 68 }
  ],
  "countrySlice": {
    "iso": "NOR",
    "ready": false,
    "participantBand": "<20"
  }
}
```
*(Note: Hero ring reveals numerical crowd distribution only once `participantCount >= 200` per Hero Ring decision; `20..199` shows `"20+ contributors recorded — aggregate themes active, hero ring opens at 200"` or aggregates without premature percentages below 200.)*

### C. `POST /api/v1/wall/submit`
Submits an optional short breakthrough idea for `"What the world is asking for"` into the **private pending moderation queue**.

**Request JSON**:
```json
{
  "theme": "Health",
  "promptText": "Clean water testing sensors run openly by village schools.",
  "lang": "en"
}
```
- **Server-side sanitization**:
  - `theme`: strictly `"Health" | "Learning" | "Climate" | "Dignity" | "Wonder" | "Truth"`.
  - `promptText`: trimmed `12..140` chars; rejects URLs, `@handles`, email patterns, phone numbers (PII scrub).
  - Stored with `status = 'pending'`. **Never returned in public `GET /api/v1/wall`** until owner explicitly marks `status = 'approved'` in a private authenticated admin endpoint (`PATCH /api/admin/wall/:id` guarded by signed owner token/Cloudflare Access).

---

## 3. Storage Tables (Minimal SQL Schema)
```sql
CREATE TABLE contributions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  breakthrough_id TEXT NOT NULL,
  weight_choice TEXT NOT NULL CHECK (weight_choice IN ('a','b','c')),
  shadow_tag TEXT NOT NULL,
  light_clarity INTEGER NOT NULL CHECK (light_clarity IN (0,1)),
  light_foresight INTEGER NOT NULL CHECK (light_foresight IN (0,1)),
  light_fairness INTEGER NOT NULL CHECK (light_fairness IN (0,1)),
  light_wisdom INTEGER NOT NULL CHECK (light_wisdom IN (0,1)),
  light_capability INTEGER NOT NULL CHECK (light_capability IN (0,1)),
  country_iso TEXT,
  bucket_hour TEXT NOT NULL
);

CREATE TABLE wall_submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  theme TEXT NOT NULL,
  lang TEXT NOT NULL CHECK (lang IN ('en','es','ar')),
  clean_text TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected')),
  reviewed_at TEXT
);
```
Notice: **Zero IP address, zero User-Agent, zero cookie ID, zero session ID columns exist in SQLite/Postgres.**

---

## 4. Platform Comparison: Cloudflare Workers + D1 vs. Supabase

| Dimension | Cloudflare Workers + D1 (+ KV Rate Limit) | Supabase (Postgres + Edge Functions) |
|---|---|---|
| **Cost at Free / Hobby Tier** | **\$0/mo** up to 100k Workers req/day, 5M D1 reads/day, 100k D1 writes/day | **\$0/mo** free tier (500 MB DB, 500k Edge invocations), **BUT projects pause after 7 days of inactivity** unless on \$25/mo Pro plan |
| **Paid Predictability** | \$5/mo Workers Paid covers huge headroom (25B D1 reads/mo) | \$25/mo Pro minimum to avoid auto-pause & get daily backups |
| **Cold Starts & Latency** | ~0–5 ms global V8 isolates close to users (especially India/Gulf/Africa/LatAm visitors) | Deno Edge Functions good globally, but single-region Postgres adds 60–180 ms RTT for cross-continent writes |
| **Zero-PII Alignment** | Clean custom endpoint code with zero built-in Auth/telemetry baggage | Rich Postgres RLS + Studio Dashboard UI makes **owner moderation UI** super fast out of the box (no custom admin page needed!) |
| **DNS / Hosting Fit** | Best paired if DNS sits on Cloudflare (`workers.dev` or `api.humanityreadiness.org` CNAME without disturbing GitHub Pages apex) | Requires no DNS change at all (`*.supabase.co` HTTPS endpoint works straight from static GitHub Pages) |
| **Schema & Migrations** | Lightweight SQLite D1 migrations in repo (`wrangler d1 migrations`) | Standard Postgres SQL migrations + built-in row editor for approving `wall_submissions` |
| **Operational Complexity** | Need small Cloudflare Access-protected script/endpoint for moderating queue | Built-in Table Editor lets owner click `pending -> approved` visually |

### Recommendation
- **Recommended default: Cloudflare Workers + D1** (`\$0–\$5/mo`, never pauses on low-traffic days, near-zero cold start for global visitors, zero-auth tiny surface area) **paired with a 1-page CLI or Cloudflare Access-protected moderation form**, once DNS/subdomain (`api.humanityreadiness.org` or `workers.dev`) is confirmed.
- Choose **Supabase** only if the owner strongly prefers a zero-code GUI table dashboard (`\$25/mo` Pro recommended so the free project never pauses) without creating a custom moderation view.

---

## 5. Rollout Sequence (When Phase 3 Is Authorized)
1. Owner confirms DNS access / subdomain choice and selects Workers+D1 vs Supabase.
2. Deploy staging API pointing strictly to `hsri-phase2-preview` (`k=20` unit tests + synthetic flood/rate-limit verification + zero-PII DB inspection).
3. Wire explicit-opt-in hero ring + `Wish Wall` `GET /api/v1/aggregates` & `GET /api/v1/wall`.
4. Verify fallback behavior: if backend is unreachable or offline, homepage degrades gracefully to Phase 2 local-only mode with zero console errors.
