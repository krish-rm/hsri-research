#!/usr/bin/env python3
"""
live_telemetry_scraper.py — Track 4 Minimal Live Telemetry Scraper

Fetches SWE-bench Verified + METR feed, appends live_feeds.jsonl,
and refreshes precursor_summary.json with provenance + data_timestamp.
No DB, no secrets, no authenticated calls. Resilient to HTTP failures
with deterministic fallback — never produces silent wrong numbers.

Usage:
    python scripts/live_telemetry_scraper.py
"""
import json
import time
import logging
import re
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


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def fetch_swe_bench() -> dict:
    t0 = time.time()
    try:
        r = requests.get(
            "https://api.github.com/repos/princeton-nlp/SWE-bench/commits",
            params={"path": "docs/leaderboard.json", "per_page": 1},
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        commits = r.json()
        if not commits or not isinstance(commits, list):
            raise ValueError("Empty commits response for SWE-bench")
        commit = commits[0]
        latency = int((time.time() - t0) * 1000)
        return {
            "fetch_status": "success",
            "latency_ms": latency,
            "provenance": "live_sentinel_telemetry",
            "data_timestamp": commit["commit"]["author"]["date"],
            "payload": {
                "commit_sha": commit["sha"][:7],
                "commit_date": commit["commit"]["author"]["date"],
                "message": commit["commit"]["message"][:120],
            },
        }
    except Exception as e:
        logger.warning("SWE-bench fetch failed: %s", e)
        return {
            "fetch_status": "failed",
            "latency_ms": int((time.time() - t0) * 1000),
            "provenance": "deterministic_calibration_fallback",
            "data_timestamp": None,
            "error": str(e)[:300],
            "payload": None,
        }


def fetch_metr() -> dict:
    t0 = time.time()
    for url in [
        "https://metr.org/atom.xml",
        "https://metr.org/feed.xml",
        "https://metr.org/rss.xml",
    ]:
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200 and ("<entry" in r.text or "<item" in r.text):
                latency = int((time.time() - t0) * 1000)
                m = re.search(r"<published>(.*?)</published>", r.text) or re.search(
                    r"<pubDate>(.*?)</pubDate>", r.text
                )
                latest = m.group(1).strip() if m else utcnow()
                return {
                    "fetch_status": "success",
                    "latency_ms": latency,
                    "provenance": "live_sentinel_telemetry",
                    "data_timestamp": latest,
                    "payload": {"feed_url": url, "latest_date": latest, "available": True},
                }
        except Exception as e:
            logger.info("METR %s failed: %s", url, e)
            continue
    return {
        "fetch_status": "failed",
        "latency_ms": 0,
        "provenance": "deterministic_calibration_fallback",
        "data_timestamp": None,
        "error": "METR feed not reachable",
        "payload": {"available": False},
    }


def main():
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    now = utcnow()

    # Carry forward last data_timestamp for fallback rows
    last_ts = None
    if LIVE_FEEDS.exists():
        try:
            for line in LIVE_FEEDS.read_text(encoding="utf-8").strip().splitlines()[-20:]:
                try:
                    j = json.loads(line)
                    if j.get("data_timestamp"):
                        last_ts = j["data_timestamp"]
                except json.JSONDecodeError:
                    continue
        except Exception:
            pass

    results = []
    for source, fn in [
        ("swe_bench_verified", fetch_swe_bench),
        ("metr_feed", fetch_metr),
    ]:
        rec = fn()
        if rec["data_timestamp"] is None:
            rec["data_timestamp"] = last_ts or now
        row = {"timestamp": now, "source": source, **rec}
        results.append(row)
        with open(LIVE_FEEDS, "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
        logger.info("%s %s %s", source, rec["fetch_status"], rec["data_timestamp"])

    # Refresh precursor_summary.json (merge, not overwrite classification/threat)
    summary: dict = {}
    if SUMMARY.exists():
        try:
            summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
        except json.JSONDecodeError as jde:
            logger.warning("Corrupted precursor_summary.json: %s — starting fresh", jde)
            summary = {}
        except OSError as ose:
            logger.warning("I/O error reading precursor_summary.json: %s", ose)
            summary = {}

    any_success = any(r["fetch_status"] == "success" for r in results)
    summary.update(
        {
            "timestamp": now,
            "provenance": "live_sentinel_telemetry" if any_success else "deterministic_calibration_fallback",
            "is_fallback": not any_success,
            "data_timestamp": next(
                (r["data_timestamp"] for r in results if r["fetch_status"] == "success"),
                last_ts or now,
            ),
            "live_feeds": {
                r["source"]: {"fetch_status": r["fetch_status"], "data_timestamp": r["data_timestamp"]}
                for r in results
            },
        }
    )
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logger.info("Summary provenance=%s is_fallback=%s", summary["provenance"], summary["is_fallback"])

    # Sync to Astro src/data and public/data if present
    for d in [REPO_ROOT / "site-astro" / "src" / "data", REPO_ROOT / "site-astro" / "public" / "data"]:
        if d.exists():
            import shutil

            shutil.copy(SUMMARY, d / "precursor_summary.json")
            logger.info("Synced to %s", d / "precursor_summary.json")


if __name__ == "__main__":
    main()
