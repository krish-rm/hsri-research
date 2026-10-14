#!/usr/bin/env python3
"""
generate_uptime_badge.py — Telemetry Uptime Badge Generator (Track 4)

Reads data/telemetry/live_feeds.jsonl and emits:
  - site-astro/public/badges/telemetry-uptime.json
  - site-astro/src/data/telemetry-uptime.json  (for Astro build sync)

Badge schema matches docs/track4_minimal_scraper_spec.md §4.3:
  { schemaVersion, label, message, color, is_fallback, provenance,
    data_timestamp, window_30d, window_7d }

Color rule:
  is_fallback => orange, success_rate >=0.90 => brightgreen,
  >=0.70 => yellow, else red.

Usage:
    python scripts/generate_uptime_badge.py
"""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("telemetry_badge")

REPO_ROOT = Path(__file__).resolve().parent.parent
LIVE = REPO_ROOT / "data" / "telemetry" / "live_feeds.jsonl"
OUT = REPO_ROOT / "site-astro" / "public" / "badges" / "telemetry-uptime.json"
ALT = REPO_ROOT / "site-astro" / "src" / "data" / "telemetry-uptime.json"


def parse_ts(s: str):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def main() -> Path:
    lines: list[dict] = []
    if LIVE.exists():
        try:
            for raw in LIVE.read_text(encoding="utf-8").strip().splitlines():
                if not raw.strip():
                    continue
                try:
                    lines.append(json.loads(raw))
                except json.JSONDecodeError as jde:
                    logger.warning("Skipping corrupt live_feeds line: %s (%s)", raw[:120], jde)
        except OSError as ose:
            logger.warning("I/O reading live_feeds.jsonl: %s", ose)

    now = datetime.now(timezone.utc)

    def window(days: int) -> dict:
        cutoff = now.timestamp() - days * 86400
        w = [x for x in lines if (parse_ts(x.get("timestamp", "")) or now).timestamp() >= cutoff]
        total = len(w)
        succ = sum(1 for x in w if x.get("fetch_status") == "success")
        return {
            "total_runs": total,
            "success_runs": succ,
            "success_rate": round(succ / total, 3) if total else 0.0,
        }

    w30 = window(30)
    w7 = window(7)
    last = lines[-1] if lines else None
    is_fallback = not (last and last.get("fetch_status") == "success")

    age = "never"
    if last:
        dt = parse_ts(last.get("data_timestamp", "")) or parse_ts(last.get("timestamp", ""))
        if dt:
            hrs = int((now - dt).total_seconds() // 3600)
            age = f"{hrs}h ago" if hrs < 48 else f"{hrs // 24}d ago"

    msg = f"{w30['success_rate'] * 100:.1f}% · updated {age}"
    if is_fallback:
        color = "orange"
    elif w30["success_rate"] >= 0.90:
        color = "brightgreen"
    elif w30["success_rate"] >= 0.70:
        color = "yellow"
    else:
        color = "red"

    payload = {
        "schemaVersion": 1,
        "label": "live telemetry",
        "message": msg,
        "color": color,
        "is_fallback": is_fallback,
        "provenance": last.get("provenance", "deterministic_calibration_fallback") if last else "deterministic_calibration_fallback",
        "data_timestamp": last.get("data_timestamp") if last else None,
        "window_30d": w30,
        "window_7d": w7,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Wrote badge to %s (color=%s, msg=%s)", OUT, color, msg)

    if ALT.parent.exists():
        ALT.write_text(OUT.read_text(encoding="utf-8"), encoding="utf-8")
        logger.info("Synced to %s", ALT)

    return OUT


if __name__ == "__main__":
    main()
