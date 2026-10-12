#!/usr/bin/env python3
"""
precursor_sentinel.py - Unified ASI Precursor Sentinel (Sprint 29)

Master scheduled monitor orchestrating all 3 precursor streams:
  - Stream 1: Autonomy Seismometer (M2M share, Human Paper Trail Gap)
  - Stream 2: Latent Drift Detector (token entropy, steganography, parseability)
  - Stream 3: Live Verification Wedge Accelerometer (tau divergence, CORS rating)

Computes the Master Precursor Threat Composite:
  Theta_ASI = (1/3) * S_autonomy + (1/3) * S_drift + (1/3) * S_cors

Logs periodic records to:
  data/telemetry/precursor_signals.jsonl
  data/telemetry/precursor_summary.json
  site-astro/src/data/precursor_summary.json
"""

import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import logging
from datetime import datetime, timezone
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Import streams
from autonomy_seismometer import AutonomySeismometer
from latent_drift_detector import LatentDriftDetector
from wedge_accelerometer import export_wedge_telemetry

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = REPO_ROOT / "data"
TELEMETRY_DIR = DATA_DIR / "telemetry"
SITE_ASTRO_DIR = REPO_ROOT / "site-astro"
SRC_DATA_DIR = SITE_ASTRO_DIR / "src" / "data"


class PrecursorSentinel:
    """
    Coordinates execution of all three precursor streams and logs unified telemetry.
    """

    def __init__(self):
        self.seismometer = AutonomySeismometer()
        self.drift_detector = LatentDriftDetector()

    def run_all_streams(self) -> Dict[str, Any]:
        """
        Executes all 3 stream analyses and calculates master composite threat index.
        """
        # 1. Run Stream 1
        s1 = self.seismometer.get_latest_readout()
        score1 = s1["seismograph_score"]

        # 2. Run Stream 2
        s2 = self.drift_detector.get_latest_readout()
        score2 = s2["latent_drift_index"]

        # 3. Run Stream 3
        wedge_payload = export_wedge_telemetry()
        s3 = wedge_payload["active_rating"]
        score3 = s3["current_cors_level"]

        # Composite Threat Level in [0.0, 10.0]
        # Equal weighting across the triad
        composite_score = (score1 + score2 + score3) / 3.0
        composite_score = round(float(np.clip(composite_score, 0.0, 10.0)), 2)

        # Classification
        if composite_score < 3.0:
            classification = "NORMAL_SUPERVISED"
            advisory = "Human-in-the-loop audit pipelines remain functional."
        elif composite_score < 5.5:
            classification = "ELEVATED_WATCH"
            advisory = "Early agentic divergence; human latency deficit emerging."
        elif composite_score < 7.5:
            classification = "SERIOUS_SYSTEMIC_DECOUPLING"
            advisory = "M2M transaction expansion with reduced human paper trails."
        elif composite_score < 9.0:
            classification = "CRITICAL_SUPERVISORY_COLLAPSE"
            advisory = "Autonomous execution velocity severely outstripping human verification capacity."
        else:
            classification = "RECURSIVE_EVENT_HORIZON"
            advisory = "Complete decoupling across cognitive oversight, protocol parseability, and economic agency."

        now_iso = datetime.now(timezone.utc).isoformat()

        payload = {
            "timestamp": now_iso,
            "master_precursor_threat_score": composite_score,
            "overall_classification": classification,
            "advisory_summary": advisory,
            "stream_1_autonomy_seismometer": {
                "score": score1,
                "alert": s1["alert_level"],
                "severity": s1["severity"],
                "hptg": s1["human_paper_trail_gap"],
                "m2m_share": s1["m2m_composite_share"]
            },
            "stream_2_latent_drift_detector": {
                "score": score2,
                "alert": s2["alert_level"],
                "severity": s2["severity"],
                "human_parseability": s2["human_parseability_index"],
                "stego_confidence": s2["stego_confidence"]
            },
            "stream_3_verification_wedge": {
                "score": score3,
                "cors_rating": s3["current_cors_level"],
                "cors_label": s3["current_cors_regime"],
                "delta_t_seconds": s3["current_delta_t_seconds"],
                "wedge_ratio": s3["current_wedge_ratio"],
                "velocity_per_month": s3["velocity_seconds_per_month"],
                "acceleration_per_month2": s3["acceleration_seconds_per_month2"]
            }
        }

        return payload

    def record_and_sync(self, output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Appends entry to JSONL log and overwrites summary JSON files.
        """
        t_dir = output_dir or TELEMETRY_DIR
        t_dir.mkdir(parents=True, exist_ok=True)

        payload = self.run_all_streams()

        # 1. Append to JSONL log
        jsonl_path = t_dir / "precursor_signals.jsonl"
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
        logger.info(f"Appended signal to {jsonl_path}")

        # 2. Overwrite telemetry summary JSON
        summary_path = t_dir / "precursor_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        logger.info(f"Wrote summary to {summary_path}")

        # 3. Synchronize to Astro src/data
        if SRC_DATA_DIR.exists():
            astro_path = SRC_DATA_DIR / "precursor_summary.json"
            with open(astro_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            logger.info(f"Synchronized to Astro portal: {astro_path}")

        return payload


def main():
    sentinel = PrecursorSentinel()
    data = sentinel.record_and_sync()
    print("=================================================================")
    print("      HSRI 2.0 UNIFIED ASI PRECURSOR SENTINEL SUMMARY")
    print("=================================================================")
    print(f"  Timestamp:               {data['timestamp']}")
    print(f"  Master Threat Score:     {data['master_precursor_threat_score']} / 10.0")
    print(f"  Classification:          {data['overall_classification']}")
    print(f"  Stream 1 (Autonomy):     {data['stream_1_autonomy_seismometer']['score']} / 10.0 ({data['stream_1_autonomy_seismometer']['alert']})")
    print(f"  Stream 2 (Latent Drift): {data['stream_2_latent_drift_detector']['score']} / 10.0 ({data['stream_2_latent_drift_detector']['alert']})")
    print(f"  Stream 3 (Wedge/CORS):   {data['stream_3_verification_wedge']['score']} / 10.0 ({data['stream_3_verification_wedge']['cors_label']})")
    print("-----------------------------------------------------------------")
    print(f"  Advisory: {data['advisory_summary']}")
    print("=================================================================")


if __name__ == "__main__":
    main()
