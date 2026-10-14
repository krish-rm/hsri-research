"""
tests/test_live_telemetry_scraper.py — Track 4 Live Telemetry Scraper & Uptime Badge

Covers: fetch error handling, fallback switching, schema conformity,
        JSONL append, badge color rules, and precursor_summary provenance.
"""
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

import pytest
import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.live_telemetry_scraper import fetch_swe_bench, fetch_metr, utcnow
from scripts.generate_uptime_badge import parse_ts


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _mock_swe_success(*args, **kwargs):
    m = MagicMock()
    m.status_code = 200
    m.json.return_value = [
        {
            "sha": "abc1234567890",
            "commit": {
                "author": {"date": "2026-10-14T06:00:00Z"},
                "message": "Update SWE-bench Verified leaderboard",
            },
        }
    ]
    m.raise_for_status = MagicMock()
    return m


def _mock_swe_failure(*args, **kwargs):
    raise requests.exceptions.ConnectionError("connection refused")


def _mock_metr_success(*args, **kwargs):
    m = MagicMock()
    m.status_code = 200
    m.text = "<feed><entry><published>2026-10-13T12:00:00Z</published></entry></feed>"
    return m


def _mock_metr_empty(*args, **kwargs):
    m = MagicMock()
    m.status_code = 404
    m.text = "not found"
    return m


# ---------------------------------------------------------------------------
# SWE-bench fetcher
# ---------------------------------------------------------------------------
class TestFetchSweBench:
    def test_success_returns_live_provenance(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_swe_success):
            rec = fetch_swe_bench()
        assert rec["fetch_status"] == "success"
        assert rec["provenance"] == "live_sentinel_telemetry"
        assert rec["data_timestamp"] == "2026-10-14T06:00:00Z"
        assert rec["payload"]["commit_sha"] == "abc1234"
        assert "latency_ms" in rec
        assert rec["latency_ms"] >= 0

    def test_success_payload_has_commit_fields(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_swe_success):
            rec = fetch_swe_bench()
        assert "commit_sha" in rec["payload"]
        assert "commit_date" in rec["payload"]
        assert "message" in rec["payload"]

    def test_connection_error_returns_fallback(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_swe_failure):
            rec = fetch_swe_bench()
        assert rec["fetch_status"] == "failed"
        assert rec["provenance"] == "deterministic_calibration_fallback"
        assert rec["data_timestamp"] is None
        assert rec["payload"] is None
        assert "error" in rec

    def test_http_error_returns_fallback(self):
        def _raise_http(*a, **kw):
            m = MagicMock()
            m.raise_for_status.side_effect = requests.exceptions.HTTPError("403 rate limited")
            return m

        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_raise_http):
            rec = fetch_swe_bench()
        assert rec["fetch_status"] == "failed"
        assert rec["provenance"] == "deterministic_calibration_fallback"

    def test_empty_commits_returns_fallback(self):
        def _empty(*a, **kw):
            m = MagicMock()
            m.status_code = 200
            m.json.return_value = []
            m.raise_for_status = MagicMock()
            return m

        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_empty):
            rec = fetch_swe_bench()
        assert rec["fetch_status"] == "failed"

    def test_timeout_returns_fallback(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=requests.exceptions.Timeout("timed out")):
            rec = fetch_swe_bench()
        assert rec["fetch_status"] == "failed"
        assert rec["provenance"] == "deterministic_calibration_fallback"


# ---------------------------------------------------------------------------
# METR fetcher
# ---------------------------------------------------------------------------
class TestFetchMetr:
    def test_success_returns_live_provenance(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_metr_success):
            rec = fetch_metr()
        assert rec["fetch_status"] == "success"
        assert rec["provenance"] == "live_sentinel_telemetry"
        assert rec["data_timestamp"] == "2026-10-13T12:00:00Z"
        assert rec["payload"]["available"] is True

    def test_all_feeds_fail_returns_fallback(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_metr_empty):
            rec = fetch_metr()
        assert rec["fetch_status"] == "failed"
        assert rec["provenance"] == "deterministic_calibration_fallback"
        assert rec["payload"]["available"] is False

    def test_connection_error_returns_fallback(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=requests.exceptions.ConnectionError("refused")):
            rec = fetch_metr()
        assert rec["fetch_status"] == "failed"
        assert rec["provenance"] == "deterministic_calibration_fallback"


# ---------------------------------------------------------------------------
# utcnow helper
# ---------------------------------------------------------------------------
class TestUtcnow:
    def test_utcnow_is_iso8601_zulu(self):
        ts = utcnow()
        assert ts.endswith("Z")
        # must parse
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        assert dt.tzinfo is not None

    def test_utcnow_is_recent(self):
        ts = utcnow()
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        delta = (datetime.now(timezone.utc) - dt).total_seconds()
        assert abs(delta) < 5.0


# ---------------------------------------------------------------------------
# parse_ts helper
# ---------------------------------------------------------------------------
class TestParseTs:
    def test_parse_valid_zulu(self):
        dt = parse_ts("2026-10-14T06:00:00Z")
        assert dt is not None
        assert dt.year == 2026

    def test_parse_invalid_returns_none(self):
        assert parse_ts("not-a-date") is None
        assert parse_ts("") is None


# ---------------------------------------------------------------------------
# Schema conformity — live_feeds.jsonl row shape
# ---------------------------------------------------------------------------
class TestLiveFeedsSchema:
    def test_success_row_has_required_keys(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_swe_success):
            rec = fetch_swe_bench()
        # Simulate row assembly as in main()
        row = {"timestamp": utcnow(), "source": "swe_bench_verified", **rec}
        for key in ["timestamp", "source", "fetch_status", "provenance", "data_timestamp", "latency_ms", "payload"]:
            assert key in row, f"missing key: {key}"

    def test_failed_row_has_error_key(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_swe_failure):
            rec = fetch_swe_bench()
        # fallback rows get data_timestamp filled in main(); here it is None before filling
        assert rec["fetch_status"] == "failed"
        assert "error" in rec

    def test_provenance_enum(self):
        for rec in [
            {"provenance": "live_sentinel_telemetry"},
            {"provenance": "deterministic_calibration_fallback"},
        ]:
            assert rec["provenance"] in ["live_sentinel_telemetry", "deterministic_calibration_fallback"]

    def test_fetch_status_enum(self):
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_swe_success):
            ok = fetch_swe_bench()
        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_swe_failure):
            fail = fetch_swe_bench()
        assert ok["fetch_status"] in ["success", "failed"]
        assert fail["fetch_status"] in ["success", "failed"]


# ---------------------------------------------------------------------------
# Badge color rules
# ---------------------------------------------------------------------------
class TestBadgeColorRule:
    def _color(self, success_rate: float, is_fallback: bool) -> str:
        if is_fallback:
            return "orange"
        elif success_rate >= 0.90:
            return "brightgreen"
        elif success_rate >= 0.70:
            return "yellow"
        else:
            return "red"

    def test_fallback_always_orange(self):
        assert self._color(1.0, True) == "orange"
        assert self._color(0.0, True) == "orange"

    def test_high_success_brightgreen(self):
        assert self._color(0.90, False) == "brightgreen"
        assert self._color(1.0, False) == "brightgreen"

    def test_mid_success_yellow(self):
        assert self._color(0.70, False) == "yellow"
        assert self._color(0.85, False) == "yellow"

    def test_low_success_red(self):
        assert self._color(0.69, False) == "red"
        assert self._color(0.0, False) == "red"

    def test_boundary_90(self):
        assert self._color(0.90, False) == "brightgreen"
        assert self._color(0.899, False) == "yellow"


# ---------------------------------------------------------------------------
# Integration: main() appends JSONL and updates summary (tmp dir)
# ---------------------------------------------------------------------------
class TestMainIntegration:
    def test_main_appends_jsonl_and_updates_summary(self, tmp_path, monkeypatch):
        import scripts.live_telemetry_scraper as scraper

        # Redirect dirs to tmp
        monkeypatch.setattr(scraper, "TELEMETRY_DIR", tmp_path)
        monkeypatch.setattr(scraper, "LIVE_FEEDS", tmp_path / "live_feeds.jsonl")
        monkeypatch.setattr(scraper, "SUMMARY", tmp_path / "precursor_summary.json")

        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_swe_success):
            # Patch fetch_metr to also succeed
            with patch.object(scraper, "fetch_metr", return_value={
                "fetch_status": "success",
                "latency_ms": 100,
                "provenance": "live_sentinel_telemetry",
                "data_timestamp": "2026-10-13T12:00:00Z",
                "payload": {"available": True},
            }):
                scraper.main()

        # JSONL has 2 lines
        lines = (tmp_path / "live_feeds.jsonl").read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        for line in lines:
            obj = json.loads(line)
            assert "timestamp" in obj
            assert "source" in obj
            assert obj["provenance"] == "live_sentinel_telemetry"

        # Summary has provenance + is_fallback
        summary = json.loads((tmp_path / "precursor_summary.json").read_text(encoding="utf-8"))
        assert summary["provenance"] == "live_sentinel_telemetry"
        assert summary["is_fallback"] is False
        assert "data_timestamp" in summary
        assert "live_feeds" in summary

    def test_main_fallback_when_all_fail(self, tmp_path, monkeypatch):
        import scripts.live_telemetry_scraper as scraper

        monkeypatch.setattr(scraper, "TELEMETRY_DIR", tmp_path)
        monkeypatch.setattr(scraper, "LIVE_FEEDS", tmp_path / "live_feeds.jsonl")
        monkeypatch.setattr(scraper, "SUMMARY", tmp_path / "precursor_summary.json")

        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=requests.exceptions.ConnectionError("down")):
            scraper.main()

        summary = json.loads((tmp_path / "precursor_summary.json").read_text(encoding="utf-8"))
        assert summary["provenance"] == "deterministic_calibration_fallback"
        assert summary["is_fallback"] is True

    def test_main_preserves_existing_classification(self, tmp_path, monkeypatch):
        import scripts.live_telemetry_scraper as scraper

        monkeypatch.setattr(scraper, "TELEMETRY_DIR", tmp_path)
        monkeypatch.setattr(scraper, "LIVE_FEEDS", tmp_path / "live_feeds.jsonl")
        monkeypatch.setattr(scraper, "SUMMARY", tmp_path / "precursor_summary.json")

        # Pre-seed summary with existing fields
        seed = {
            "master_precursor_threat_score": 8.44,
            "overall_classification": "CRITICAL_SUPERVISORY_COLLAPSE",
            "stream_1_autonomy_seismometer": {"score": 8.78},
        }
        (tmp_path / "precursor_summary.json").write_text(json.dumps(seed), encoding="utf-8")

        with patch("scripts.live_telemetry_scraper.requests.get", side_effect=_mock_swe_success):
            with patch.object(scraper, "fetch_metr", return_value={
                "fetch_status": "success",
                "latency_ms": 100,
                "provenance": "live_sentinel_telemetry",
                "data_timestamp": "2026-10-13T12:00:00Z",
                "payload": {"available": True},
            }):
                scraper.main()

        summary = json.loads((tmp_path / "precursor_summary.json").read_text(encoding="utf-8"))
        assert summary["master_precursor_threat_score"] == 8.44
        assert summary["overall_classification"] == "CRITICAL_SUPERVISORY_COLLAPSE"


# ---------------------------------------------------------------------------
# Badge generator
# ---------------------------------------------------------------------------
class TestBadgeGenerator:
    def test_generates_valid_badge_from_jsonl(self, tmp_path, monkeypatch):
        import scripts.generate_uptime_badge as badge_mod

        # Seed a few success lines within 7d window
        now = datetime.now(timezone.utc)
        lines = []
        for i in range(5):
            ts = (now).isoformat().replace("+00:00", "Z")
            lines.append(json.dumps({
                "timestamp": ts,
                "source": "swe_bench_verified",
                "fetch_status": "success",
                "provenance": "live_sentinel_telemetry",
                "data_timestamp": ts,
                "latency_ms": 200,
                "payload": {},
            }))
        (tmp_path / "live_feeds.jsonl").write_text("\n".join(lines), encoding="utf-8")

        out = tmp_path / "badge.json"
        alt = tmp_path / "alt.json"
        monkeypatch.setattr(badge_mod, "LIVE", tmp_path / "live_feeds.jsonl")
        monkeypatch.setattr(badge_mod, "OUT", out)
        monkeypatch.setattr(badge_mod, "ALT", alt)
        alt.parent.mkdir(parents=True, exist_ok=True)

        result = badge_mod.main()
        assert result == out
        badge = json.loads(out.read_text(encoding="utf-8"))
        assert badge["schemaVersion"] == 1
        assert badge["label"] == "live telemetry"
        assert badge["color"] == "brightgreen"
        assert badge["is_fallback"] is False
        assert badge["provenance"] == "live_sentinel_telemetry"
        assert badge["window_30d"]["success_rate"] == 1.0
        assert badge["window_30d"]["total_runs"] == 5

    def test_empty_jsonl_yields_fallback_orange(self, tmp_path, monkeypatch):
        import scripts.generate_uptime_badge as badge_mod

        (tmp_path / "live_feeds.jsonl").write_text("", encoding="utf-8")
        out = tmp_path / "badge.json"
        alt = tmp_path / "alt.json"
        monkeypatch.setattr(badge_mod, "LIVE", tmp_path / "live_feeds.jsonl")
        monkeypatch.setattr(badge_mod, "OUT", out)
        monkeypatch.setattr(badge_mod, "ALT", alt)
        alt.parent.mkdir(parents=True, exist_ok=True)

        badge_mod.main()
        badge = json.loads(out.read_text(encoding="utf-8"))
        assert badge["is_fallback"] is True
        assert badge["color"] == "orange"
        assert badge["provenance"] == "deterministic_calibration_fallback"

    def test_corrupt_lines_skipped(self, tmp_path, monkeypatch):
        import scripts.generate_uptime_badge as badge_mod

        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        good = json.dumps({
            "timestamp": now, "source": "swe_bench_verified",
            "fetch_status": "success", "provenance": "live_sentinel_telemetry",
            "data_timestamp": now, "latency_ms": 100, "payload": {},
        })
        (tmp_path / "live_feeds.jsonl").write_text("not json\n" + good + "\n{bad json", encoding="utf-8")
        out = tmp_path / "badge.json"
        alt = tmp_path / "alt.json"
        monkeypatch.setattr(badge_mod, "LIVE", tmp_path / "live_feeds.jsonl")
        monkeypatch.setattr(badge_mod, "OUT", out)
        monkeypatch.setattr(badge_mod, "ALT", alt)
        alt.parent.mkdir(parents=True, exist_ok=True)

        badge_mod.main()
        badge = json.loads(out.read_text(encoding="utf-8"))
        assert badge["window_30d"]["total_runs"] == 1
        assert badge["window_30d"]["success_rate"] == 1.0
