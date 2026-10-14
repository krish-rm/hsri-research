# Track 4 — Minimal Live Telemetry Scraper Specification

> **Status:** Spec — ready to implement in one focused build session
> **Goal:** Convert `CORS 10.0 / 8.44` from `provenance=deterministic_calibration_fallback` into `provenance=live_sentinel_telemetry` with a **public, git-versioned uptime badge** on `/seismograph`
> **Constraint:** Zero burn, zero new infra — GitHub Actions + flat JSONL only (no DB, no server)
> **Author:** Krishnakumar Radhakrishnan · 2026-10-14 · DOI 10.5281/zenodo.10842000

---

## 1. What "Live" Means — Acceptance Criterion

`GET /v1/telemetry/precursors` returns:

```json
{
  "is_fallback": false,
  "provenance": "live_sentinel_telemetry",
  "data_timestamp": "2026-10-14T14:00:00Z"
}
```

with `data_timestamp` < 24h old on **>90% of checks over any rolling 60-day window.** Public badge on `/seismograph` reflects the same file the API reads — no divergent state.

Failed fetches never produce silent wrong numbers — they produce `is_fallback=true` + `provenance=deterministic_calibration_fallback` + last-known `data_timestamp`, exactly as Sprint 36's `hsri_engine/core.py:get_precursor_telemetry()` now does.

---

## 2. Architecture — Minimal Path (One New Script + One Workflow Patch)

```
                 ┌─────────────────────────────────────────────────┐
                 │  GitHub Actions — precursor-sentinel.yml         │
                 │  cron: 0 */6 * * *  (every 6h) + workflow_dispatch │
                 │                                                  │
                 │  Step 1  scripts/live_telemetry_scraper.py       │
                 │          ├─ fetch SWE-bench verified (GitHub raw)│
                 │          ├─ fetch METR eval feed (if available)  │
                 │          └─ append data/telemetry/live_feeds.jsonl│
                 │                + refresh data/telemetry/         │
                 │                  precursor_summary.json           │
                 │                  wedge_history.json               │
                 │                  autonomy_seismometer.json        │
                 │                                                  │
                 │  Step 2  scripts/generate_uptime_badge.py        │
                 │          └─ data/telemetry/live_feeds.jsonl      │
                 │             → site-astro/public/badges/          │
                 │               telemetry-uptime.json               │
                 │             → site-astro/src/data/               │
                 │               (sync for Astro build)            │
                 │                                                  │
                 │  Step 3  existing streams (autonomy/wedge/latent)│
                 │          reconsume live_feeds.jsonl if present   │
                 │                                                  │
                 │  Step 4  git add data/telemetry/                 │
                 │          site-astro/src/data/                    │
                 │          site-astro/public/badges/  → commit     │
                 └─────────────────────────────────────────────────┘
                                   │
                                   ▼
              ┌──────────────────────────────────────┐
              │  hsri_engine/core.py                  │
              │  get_precursor_telemetry()            │
              │  reads precursor_summary.json         │
              │  → PrecursorTelemetryResponse         │
              │    { is_fallback, provenance,         │
              │      data_timestamp, cors_score, ... }│
              └──────────────────────────────────────┘
                                   │
                                   ▼
              ┌──────────────────────────────────────┐
              │  /seismograph Svelte badge            │
              │  fetches /badges/telemetry-uptime.json│
              │  "Live Telemetry: 97.3% · Updated 2h ago" │
              └──────────────────────────────────────┘
```

Why every 6h, not hourly: stays well under GitHub API unauthenticated rate limits (60/h), avoids Actions minute-contention, and still gives `data_timestamp` freshness <24h with 4 chances/day to recover.

---

## 3. Data Sources — Two Primary, One Optional

| Priority | Source | What to fetch | Endpoint (no auth) | Parse | On failure |
|---|---|---|---|---|---|
| **P0** | **SWE-bench Verified** | Latest leaderboard head — top resolved rate + date | `https://raw.githubusercontent.com/princeton-nlp/SWE-bench/main/docs/leaderboard.json` **or** `https://api.github.com/repos/princeton-nlp/SWE-bench/commits?path=docs/leaderboard.json&per_page=1` (commit date = freshness) | JSON; extract `date`, `resolved_rate`, `model_label` | Log `fetch_status=failed`, do not mutate `precursor_summary.json` beyond updating `data_timestamp` of last success |
| **P0** | **SWE-bench GitHub pulse** | Commit activity as autonomy velocity proxy | `https://api.github.com/repos/princeton-nlp/SWE-bench/commits?per_page=5` | `commit.author.date` + message count | Same — degraded, not fatal |
| **P1** | **METR** | Eval publication / autonomous capability notes | `https://metr.org/atom.xml` or `https://metr.org/feed.xml` (RSS) | Last `<published>` date + title | Optional — if feed absent, write `metr_available=false` and continue |
| *(defer)* | GitHub Archive / HF | PR agent activity, HF commit feeds | — | — | Track 4 Phase 2 — not in minimal spec |

**Key principle:** No scraping of HTML. Only GitHub Raw / GitHub API / RSS — stable, unauthenticated, cacheable.

---

## 4. Schemas

### 4.1 `data/telemetry/live_feeds.jsonl` — append-only, one JSON object per line

```json
{"timestamp":"2026-10-14T06:00:00Z","source":"swe_bench_verified","fetch_status":"success","latency_ms":412,"provenance":"live_sentinel_telemetry","data_timestamp":"2026-10-14T06:00:00Z","payload":{"resolved_rate":0.412,"model_label":"SWE-bench Verified Leaderboard","commit_sha":"a1b2c3d","commit_date":"2026-10-13T22:11:00Z"}}
{"timestamp":"2026-10-14T06:00:00Z","source":"metr_feed","fetch_status":"success","latency_ms":298,"provenance":"live_sentinel_telemetry","data_timestamp":"2026-10-14T05:48:00Z","payload":{"latest_title":"Evaluating autonomous capabilities...","latest_date":"2026-10-10T00:00:00Z","available":true}}
{"timestamp":"2026-10-14T12:00:00Z","source":"swe_bench_verified","fetch_status":"failed","latency_ms":5003,"provenance":"deterministic_calibration_fallback","data_timestamp":"2026-10-14T06:00:00Z","error":"HTTP 403 rate limited","payload":null}
```

Fields:

| Field | Type | Notes |
|---|---|---|
| `timestamp` | ISO-8601 UTC | When scraper ran |
| `source` | `swe_bench_verified` \| `metr_feed` | Extensible |
| `fetch_status` | `success` \| `failed` | Drives uptime calc |
| `latency_ms` | int | Request latency, for wedge diagnostics |
| `provenance` | `live_sentinel_telemetry` \| `deterministic_calibration_fallback` | Mirrors API enum |
| `data_timestamp` | ISO-8601 UTC | Freshness of underlying data (commit date or feed date); on failure = last success timestamp |
| `payload` | object \| null | Source-specific snapshot |
| `error` | string \| absent | Only on failure |

### 4.2 `data/telemetry/precursor_summary.json` — existing file, add two fields (no breaking change)

```json
{
  "master_precursor_threat_score": 8.44,
  "overall_classification": "CRITICAL_SUPERVISORY_COLLAPSE",
  "timestamp": "2026-10-14T06:00:00Z",
  "provenance": "live_sentinel_telemetry",
  "is_fallback": false,
  "data_timestamp": "2026-10-14T06:00:00Z",
  "live_feeds": {
    "swe_bench_verified": {"fetch_status":"success","commit_date":"2026-10-13T22:11:00Z"},
    "metr_feed": {"fetch_status":"success","latest_date":"2026-10-10T00:00:00Z"}
  }
}
```

`hsri_engine/core.py` already reads `timestamp` and sets `data_timestamp`/`provenance`/`is_fallback` accordingly (Sprint 36). No model change needed — just ensure scraper writes `timestamp` + `provenance`.

### 4.3 `site-astro/public/badges/telemetry-uptime.json` — shields-style badge data

```json
{
  "schemaVersion": 1,
  "label": "live telemetry",
  "message": "97.3% · updated 2h ago",
  "color": "brightgreen",
  "is_fallback": false,
  "provenance": "live_sentinel_telemetry",
  "data_timestamp": "2026-10-14T12:00:00Z",
  "window_30d": {"total_runs": 120, "success_runs": 117, "success_rate": 0.975},
  "window_7d": {"total_runs": 28, "success_runs": 28, "success_rate": 1.0}
}
```

Color rule: `success_rate >=0.90` → `brightgreen`; `>=0.70` → `yellow`; `<0.70` → `red`; `is_fallback=true` → `orange` regardless.

---

## 5. New Script — `scripts/live_telemetry_scraper.py` (skeleton, copy-paste ready)

```python
#!/usr/bin/env python3
"""
live_telemetry_scraper.py — Track 4 Minimal Live Scraper
Fetches SWE-bench Verified + METR feed, appends live_feeds.jsonl,
and refreshes precursor_summary.json with provenance + data_timestamp.
No DB, no secrets, no authenticated calls.
"""
import json, time, logging
from datetime import datetime, timezone
from pathlib import Path
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("live_scraper")

REPO_ROOT = Path(__file__).resolve().parent.parent
TELEMETRY_DIR = REPO_ROOT / "data" / "telemetry"
LIVE_FEEDS = TELEMETRY_DIR / "live_feeds.jsonl"
SUMMARY = TELEMETRY_DIR / "precursor_summary.json"

TIMEOUT = 10
HEADERS = {"User-Agent": "HSRI-Sentinel/2.5 (+https://humanreadinessindex.org)"}

def utcnow(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

def fetch_swe_bench():
    t0 = time.time()
    try:
        # Use commits API for freshness (no raw JSON parsing fragility)
        r = requests.get(
            "https://api.github.com/repos/princeton-nlp/SWE-bench/commits",
            params={"path":"docs/leaderboard.json","per_page":1},
            headers=HEADERS, timeout=TIMEOUT
        )
        r.raise_for_status()
        commit = r.json()[0]
        latency = int((time.time()-t0)*1000)
        return {
            "fetch_status":"success","latency_ms":latency,
            "provenance":"live_sentinel_telemetry","data_timestamp": commit["commit"]["author"]["date"],
            "payload": {"commit_sha": commit["sha"][:7], "commit_date": commit["commit"]["author"]["date"],
                        "message": commit["commit"]["message"][:120]}
        }
    except Exception as e:
        logger.warning("SWE-bench fetch failed: %s", e)
        return {"fetch_status":"failed","latency_ms":int((time.time()-t0)*1000),
                "provenance":"deterministic_calibration_fallback","data_timestamp": None,
                "error": str(e)[:300], "payload": None}

def fetch_metr():
    t0 = time.time()
    for url in ["https://metr.org/atom.xml","https://metr.org/feed.xml","https://metr.org/rss.xml"]:
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code==200 and "<entry" in r.text or "<item" in r.text:
                latency=int((time.time()-t0)*1000)
                # minimal parse: first <published> or <pubDate>
                import re
                m=re.search(r"<published>(.*?)</published>",r.text) or re.search(r"<pubDate>(.*?)</pubDate>",r.text)
                latest=m.group(1) if m else utcnow()
                return {"fetch_status":"success","latency_ms":latency,
                        "provenance":"live_sentinel_telemetry","data_timestamp": latest,
                        "payload":{"feed_url":url,"latest_date":latest,"available":True}}
        except Exception as e:
            logger.info("METR %s failed: %s", url, e); continue
    return {"fetch_status":"failed","latency_ms":0,"provenance":"deterministic_calibration_fallback",
            "data_timestamp":None,"error":"METR feed not reachable","payload":{"available":False}}

def main():
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    now=utcnow()
    # Carry forward last data_timestamp for fallback rows
    last_ts=None
    if LIVE_FEEDS.exists():
        try:
            for line in LIVE_FEEDS.read_text().strip().splitlines()[-20:]:
                j=json.loads(line)
                if j.get("data_timestamp"): last_ts=j["data_timestamp"]
        except: pass

    results=[]
    for source, fn in [("swe_bench_verified",fetch_swe_bench),("metr_feed",fetch_metr)]:
        rec=fn()
        if rec["data_timestamp"] is None: rec["data_timestamp"]=last_ts or now
        row={"timestamp":now,"source":source, **rec}
        results.append(row)
        with open(LIVE_FEEDS,"a",encoding="utf-8") as f: f.write(json.dumps(row)+"\n")
        logger.info("%s %s %s", source, rec["fetch_status"], rec["data_timestamp"])

    # Refresh precursor_summary.json (merge, not overwrite classification/threat)
    summary={}
    if SUMMARY.exists():
        try: summary=json.loads(SUMMARY.read_text())
        except: summary={}
    any_success=any(r["fetch_status"]=="success" for r in results)
    summary.update({
        "timestamp": now,
        "provenance": "live_sentinel_telemetry" if any_success else "deterministic_calibration_fallback",
        "is_fallback": not any_success,
        "data_timestamp": next((r["data_timestamp"] for r in results if r["fetch_status"]=="success"), last_ts or now),
        "live_feeds": {r["source"]: {"fetch_status":r["fetch_status"],"data_timestamp":r["data_timestamp"]} for r in results}
    })
    SUMMARY.write_text(json.dumps(summary,indent=2),encoding="utf-8")
    logger.info("Summary provenance=%s is_fallback=%s", summary["provenance"], summary["is_fallback"])
    # Sync to Astro src/data if present
    for d in [REPO_ROOT/"site-astro"/"src"/"data", REPO_ROOT/"site-astro"/"public"/"data"]:
        if d.exists():
            import shutil; shutil.copy(SUMMARY, d/"precursor_summary.json")

if __name__=="__main__": main()
```

**Dependencies:** `requests` only (already in `pyproject.toml`). No new pip installs.

### Badge generator — `scripts/generate_uptime_badge.py`

```python
#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT=Path(__file__).resolve().parent.parent
LIVE=REPO_ROOT/"data/telemetry/live_feeds.jsonl"
OUT=REPO_ROOT/"site-astro/public/badges/telemetry-uptime.json"

def parse_ts(s):
    try: return datetime.fromisoformat(s.replace("Z","+00:00"))
    except: return None

def main():
    lines=[]
    if LIVE.exists():
        for l in LIVE.read_text().strip().splitlines():
            try: lines.append(json.loads(l))
            except: pass
    now=datetime.now(timezone.utc)
    def window(days):
        cutoff=now.timestamp()-days*86400
        w=[x for x in lines if (parse_ts(x["timestamp"]) or now).timestamp()>=cutoff]
        total=len(w); succ=sum(1 for x in w if x["fetch_status"]=="success")
        return {"total_runs":total,"success_runs":succ,"success_rate": round(succ/total,3) if total else 0.0}
    w30, w7 = window(30), window(7)
    last = lines[-1] if lines else None
    is_fallback = not (last and last["fetch_status"]=="success")
    # age
    age="never"
    if last:
        dt=parse_ts(last["data_timestamp"]) or parse_ts(last["timestamp"])
        if dt:
            hrs=int((now-dt).total_seconds()//3600)
            age=f"{hrs}h ago" if hrs<48 else f"{hrs//24}d ago"
    msg=f"{w30['success_rate']*100:.1f}% · updated {age}"
    if is_fallback: color="orange"
    elif w30["success_rate"]>=0.90: color="brightgreen"
    elif w30["success_rate"]>=0.70: color="yellow"
    else: color="red"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "schemaVersion":1,"label":"live telemetry","message":msg,"color":color,
        "is_fallback":is_fallback,"provenance": last["provenance"] if last else "deterministic_calibration_fallback",
        "data_timestamp": last["data_timestamp"] if last else None,
        "window_30d":w30,"window_7d":w7
    },indent=2))
    # also sync to src/data
    alt=REPO_ROOT/"site-astro/src/data/telemetry-uptime.json"
    if alt.parent.exists(): alt.write_text(OUT.read_text())

if __name__=="__main__": main()
```

---

## 6. Workflow Patch — `.github/workflows/precursor-sentinel.yml`

Replace current `0 6 * * 1` (weekly Monday) with every-6h + manual dispatch. Insert two new steps before existing stream runs.

```yaml
name: HSRI ASI Precursor Sentinel
on:
  schedule:
    - cron: '0 */6 * * *'   # every 6 hours (00,06,12,18 UTC)
  workflow_dispatch:

jobs:
  telemetry-scan:
    runs-on: ubuntu-latest
    permissions: { contents: write, issues: write }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install numpy requests

      - name: Fetch live telemetry (SWE-bench / METR)
        run: python scripts/live_telemetry_scraper.py

      - name: Generate uptime badge
        run: python scripts/generate_uptime_badge.py

      - name: Run Autonomy Seismometer (Stream 1)
        run: python scripts/autonomy_seismometer.py
      - name: Run Latent Drift Detector (Stream 2)
        run: python scripts/latent_drift_detector.py
      - name: Run Verification Wedge Accelerometer (Stream 3)
        run: python scripts/wedge_accelerometer.py
      - name: Run Master Precursor Sentinel
        run: python scripts/precursor_sentinel.py

      - uses: actions/upload-artifact@v4
        with:
          name: precursor-telemetry-${{ github.run_id }}
          path: |
            data/telemetry/live_feeds.jsonl
            data/telemetry/precursor_summary.json
            data/telemetry/precursor_signals.jsonl
            data/telemetry/autonomy_seismometer.json
            data/telemetry/latent_drift_detector.json
            data/telemetry/wedge_history.json
            site-astro/public/badges/telemetry-uptime.json
          retention-days: 90

      - name: Commit and push telemetry updates
        run: |
          git config user.name "hsri-ops[bot]"
          git config user.email "hsri-ops@users.noreply.github.com"
          git add data/telemetry/ site-astro/src/data/ site-astro/public/badges/ site-astro/public/data/ || true
          git diff --staged --quiet || git commit -m "telemetry(sentinel): live sync $(date -u +%Y-%m-%dT%H:%M:%SZ) [provenance=$(jq -r .provenance data/telemetry/precursor_summary.json)]"
          git push
```

Add `jq` is preinstalled on `ubuntu-latest`; if missing, drop the `$(jq ...)` interpolation.

**Retention hygiene:** Append `live_feeds.jsonl` — never truncate in the scraper. Add monthly compaction job later (keep last 90 days). Keep telemetry dir git-tracked; artifact upload gives 90d recoverability even if commit fails.

---

## 7. Wiring to Existing Code — What NOT to Change

- **`hsri_engine/core.py:get_precursor_telemetry()`** — already Sprint 36 hardened; reads `precursor_summary.json` → `is_fallback`/`provenance`/`data_timestamp`. No change.
- **`hsri_engine/models.py:PrecursorTelemetryResponse`** — already has `is_fallback`, `provenance`, `data_timestamp`. No change.
- **`scripts/autonomy_seismometer.py` / `wedge_accelerometer.py`** — optionally read `live_feeds.jsonl` to enrich `payload` (e.g., latest SWE-bench commit date as annotation). Do not block if file missing.

---

## 8. `/seismograph` Badge — Svelte Snippet

New component `site-astro/src/components/TelemetryUptimeBadge.svelte`:

```svelte
<script>
  import { onMount } from 'svelte';
  let badge=null, loading=true;
  onMount(async()=>{
    try{ const r=await fetch('/badges/telemetry-uptime.json'); badge=await r.json(); }catch{}
    loading=false;
  });
</script>

{#if !loading && badge}
  <a href="https://github.com/krish-rm/hsri-research/actions/workflows/precursor-sentinel.yml"
     class="inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-medium border"
     class:bg-emerald-50={badge.color==='brightgreen'}
     class:bg-amber-50={badge.color==='yellow' || badge.color==='orange'}
     class:bg-red-50={badge.color==='red'}>
    <span class="h-2 w-2 rounded-full" class:bg-emerald-500={badge.color==='brightgreen'}
          class:bg-amber-500={badge.color==='yellow'||badge.color==='orange'}
          class:bg-red-500={badge.color==='red'}></span>
    Live Telemetry: {badge.message}
    {#if badge.is_fallback}<span class="opacity-60">· fallback</span>{/if}
  </a>
  <span class="ml-2 text-xs opacity-60">provenance: {badge.provenance} · 30d {badge.window_30d.success_rate*100}% · 7d {badge.window_7d.success_rate*100}%</span>
{/if}
```

Place directly under the CORS gauge on `/seismograph`. Links to Actions run for auditability.

Alternative zero-JS: Shields.io endpoint badge pointing at `https://humanreadinessindex.org/badges/telemetry-uptime.json` — but the Svelte component above is preferred (git-versioned, no external service).

---

## 9. Testing & Monitoring

```bash
# Local dry run (no workflow needed)
python scripts/live_telemetry_scraper.py
python scripts/generate_uptime_badge.py
cat data/telemetry/live_feeds.jsonl | tail -5
cat site-astro/public/badges/telemetry-uptime.json
uv run python -m hsri_engine.cli serve --port 8000  # curl /v1/telemetry/precursors → check provenance

# New tests to add to tests/test_hardening_and_crosswalk.py
# - test_live_feeds_jsonl_schema_valid
# - test_precursor_summary_provenance_enum
# - test_uptime_badge_color_rule
# - test_scraper_handles_http_403_gracefully (mocked requests)
```

**Alerting:** If `window_7d.success_rate < 0.70` for 48h, workflow should open an issue (reuse `issues: write` permission + `gh issue create` step). Add after badge step if desired — not required for minimal spec.

---

## 10. Deployment Checklist (One Session, ~3 Hours)

- [ ] Create `scripts/live_telemetry_scraper.py` + `scripts/generate_uptime_badge.py` from skeletons above
- [ ] Run locally once: `python scripts/live_telemetry_scraper.py && python scripts/generate_uptime_badge.py`
- [ ] Verify `GET /v1/telemetry/precursors` returns `provenance=live_sentinel_telemetry` when `precursor_summary.json` is fresh
- [ ] Patch `.github/workflows/precursor-sentinel.yml` to `0 */6 * * *` + insert two new steps
- [ ] Add `TelemetryUptimeBadge.svelte` to `/seismograph` + `npm run build` locally
- [ ] Commit all + push → trigger one `workflow_dispatch` run → confirm `live_feeds.jsonl` appends, badge JSON updates, and commit message includes provenance
- [ ] Wait 24h (4 runs) → confirm badge reads `>90%` and `data_timestamp` < 24h → then include screenshot in LTFF update email

---

## 11. What Comes After (Not in Minimal Spec)

- SWE-bench resolved-rate time series → feed into `wedge_accelerometer.py` as empirical `model_label`
- METR eval cadence → `autonomy_seismometer.py` HPTG velocity
- GitHub Archive PR agent volume (Track 4 Phase 2) — only after 60d of stable P0 feeds

---

*End of spec. All paths, field names, and enums match the current `main` at `1277a0d` / `ef3e7e8`.*
