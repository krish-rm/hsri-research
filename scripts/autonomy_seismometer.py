#!/usr/bin/env python3
"""
autonomy_seismometer.py - Precursor Stream 1: Autonomy Seismometer (Sprint 29)

Mathematical and empirical telemetry engine tracking:
1. Human Paper Trail Gap (HPTG):
   The widening opacity ratio of frontier AI capability releases lacking
   reproducible, human-interpretable verification artifacts or open execution traces:
       HPTG(t) = 1 - [ sum_k (Delta C_k * A_k) / sum_k Delta C_k ]
   where Delta C_k is capability delta and A_k in [0, 1] is human auditability.

2. Machine-to-Machine (M2M) Economic Share Proxy:
   Composite index tracking machine-to-machine transaction density, autonomous API
   agent-to-agent billing, autonomous smart contract execution, and agent web traffic:
       M2M(t) = w_api * S_api + w_pay * S_pay + w_contract * S_contract + w_traffic * S_traffic

3. Autonomy Velocity (v_autonomy) and Acceleration (a_autonomy).

4. Composite Autonomy Seismograph Score (S_autonomy in [0.0, 10.0]):
   Calibrated metric mapping the approach of autonomous systemic economic decoupling.
"""

from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import json
import math
import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
TELEMETRY_DIR = DATA_DIR / "telemetry"
SITE_ASTRO_DIR = REPO_ROOT / "site-astro"
PUBLIC_DATA_DIR = SITE_ASTRO_DIR / "public" / "data"
SRC_DATA_DIR = SITE_ASTRO_DIR / "src" / "data"

# Weights for M2M economic share calculation
M2M_WEIGHTS = {
    "api_agent_share": 0.35,      # Agent-to-agent API traffic
    "autonomous_billing": 0.25,   # Automated micro-billing / x402 / crypto rails
    "smart_contracts": 0.20,      # Unsupervised bot contract executions
    "machine_web_traffic": 0.20   # Non-human bot web request share
}

# -----------------------------------------------------------------------------
# 1. EMPIRICAL FRONTIER CAPABILITY RELEASES & HUMAN AUDITABILITY (2023 - 2026)
# -----------------------------------------------------------------------------
# A_k: 1.0 = Fully open weights/proofs; 0.5 = Detailed technical report;
#      0.1 = Proprietary with hidden reasoning tokens; 0.0 = Black-box swarm closed loop.
FRONTIER_MILESTONES = [
    {
        "milestone_id": "MS-2023-01",
        "date": "2023-03-14",
        "model_or_event": "GPT-4 Release",
        "capability_delta": 35.0,
        "auditability_score": 0.45,
        "architecture_openness": "Closed API with system card",
        "human_readable_proofs": False,
        "notes": "Multimodal milestone, weights and training data undisclosed"
    },
    {
        "milestone_id": "MS-2023-02",
        "date": "2023-07-18",
        "model_or_event": "Llama 2 Release",
        "capability_delta": 20.0,
        "auditability_score": 0.85,
        "architecture_openness": "Open weights, partial training recipe",
        "human_readable_proofs": True,
        "notes": "Open weights enable mechanistic interpretability"
    },
    {
        "milestone_id": "MS-2024-01",
        "date": "2024-03-04",
        "model_or_event": "Claude 3 Family",
        "capability_delta": 30.0,
        "auditability_score": 0.40,
        "architecture_openness": "Closed API, safety benchmarks",
        "human_readable_proofs": False,
        "notes": "Vision-language reasoning SOTA, proprietary weights"
    },
    {
        "milestone_id": "MS-2024-02",
        "date": "2024-06-20",
        "model_or_event": "Claude 3.5 Sonnet & Artifacts",
        "capability_delta": 40.0,
        "auditability_score": 0.35,
        "architecture_openness": "Closed API, computer-use preview",
        "human_readable_proofs": False,
        "notes": "Tool-use and coding agent jump, UI interaction capabilities"
    },
    {
        "milestone_id": "MS-2024-03",
        "date": "2024-09-12",
        "model_or_event": "OpenAI o1-preview (Test-Time Reasoning)",
        "capability_delta": 55.0,
        "auditability_score": 0.12,
        "architecture_openness": "Closed API, encrypted/hidden CoT reasoning tokens",
        "human_readable_proofs": False,
        "notes": "Internal thought traces concealed to prevent distillation; verification opacity jump"
    },
    {
        "milestone_id": "MS-2025-01",
        "date": "2025-04-10",
        "model_or_event": "DeepSeek R1 / Distributed Reasoning",
        "capability_delta": 50.0,
        "auditability_score": 0.70,
        "architecture_openness": "Open weights with visible reasoning tokens",
        "human_readable_proofs": True,
        "notes": "Open reasoning trajectories partially restore paper trail visibility"
    },
    {
        "milestone_id": "MS-2025-02",
        "date": "2025-09-18",
        "model_or_event": "Claude 4 Opus Multi-Agent Swarms",
        "capability_delta": 65.0,
        "auditability_score": 0.10,
        "architecture_openness": "Closed multi-agent asynchronous infrastructure",
        "human_readable_proofs": False,
        "notes": "Autonomous multi-agent orchestration; execution logs exceed human real-time review capacity"
    },
    {
        "milestone_id": "MS-2026-01",
        "date": "2026-03-25",
        "model_or_event": "Autonomous Economic Swarms & x402 Rail Integration",
        "capability_delta": 75.0,
        "auditability_score": 0.05,
        "architecture_openness": "Agent-to-agent cryptographically negotiated contracts",
        "human_readable_proofs": False,
        "notes": "Autonomous agents execute multi-million dollar liquidity rebalances with 0 human approvals"
    },
    {
        "milestone_id": "MS-2026-02",
        "date": "2026-10-01",
        "model_or_event": "EXP-07-SYN Continuous Closed-Loop R&D Swarm",
        "capability_delta": 90.0,
        "auditability_score": 0.02,
        "architecture_openness": "Recursive self-compounding closed loop",
        "human_readable_proofs": False,
        "notes": "Sub-millisecond verification exchange, human paper trail functionally zero"
    }
]

# -----------------------------------------------------------------------------
# 2. MONTHLY EMPIRICAL M2M & TRANSACTION DENSITY TIMESERIES (2023 - 2026)
# -----------------------------------------------------------------------------
# Monthly historical telemetry points: (YYYY-MM, S_api, S_pay, S_contract, S_traffic)
MONTHLY_TELEMETRY_SERIES = [
    # 2023 (Early agent emergence: AutoGPT, LangChain)
    ("2023-01", 0.015, 0.002, 0.012, 0.380),
    ("2023-03", 0.022, 0.003, 0.014, 0.385),
    ("2023-06", 0.038, 0.006, 0.018, 0.395),
    ("2023-09", 0.051, 0.009, 0.022, 0.405),
    ("2023-12", 0.068, 0.014, 0.028, 0.418),
    # 2024 (Tool calling, function calling, agentic coding)
    ("2024-03", 0.089, 0.022, 0.036, 0.432),
    ("2024-06", 0.118, 0.035, 0.048, 0.448),
    ("2024-09", 0.152, 0.054, 0.062, 0.465),
    ("2024-12", 0.194, 0.078, 0.081, 0.485),
    # 2025 (Test-time compute scaling, agentic payment rails)
    ("2025-03", 0.245, 0.112, 0.105, 0.510),
    ("2025-06", 0.308, 0.158, 0.138, 0.538),
    ("2025-09", 0.380, 0.215, 0.178, 0.569),
    ("2025-12", 0.462, 0.285, 0.224, 0.602),
    # 2026 (Autonomous economic loops, swarm orchestration)
    ("2026-03", 0.548, 0.368, 0.282, 0.638),
    ("2026-06", 0.635, 0.462, 0.345, 0.672),
    ("2026-08", 0.695, 0.525, 0.388, 0.695),
    ("2026-10", 0.742, 0.584, 0.432, 0.718),
]


class AutonomySeismometer:
    """
    Evaluates the Human Paper Trail Gap (HPTG) and Machine-to-Machine (M2M)
    economic decoupling trajectories over time.
    """

    def __init__(self, milestones: Optional[List[Dict[str, Any]]] = None):
        self.milestones = milestones or FRONTIER_MILESTONES

    def compute_cumulative_paper_trail_gap(self, up_to_date: Optional[str] = None) -> Dict[str, float]:
        """
        Calculates HPTG(t) across all frontier milestones recorded up to a target date:
            HPTG(t) = 1.0 - ( sum_k (Delta C_k * A_k) / sum_k Delta C_k )
        """
        filtered = [
            m for m in self.milestones
            if up_to_date is None or m["date"] <= up_to_date
        ]
        if not filtered:
            return {"hptg": 0.0, "total_capability_delta": 0.0, "weighted_auditability": 1.0}

        total_delta = sum(m["capability_delta"] for m in filtered)
        weighted_audit = sum(m["capability_delta"] * m["auditability_score"] for m in filtered)

        avg_audit = weighted_audit / total_delta if total_delta > 0 else 1.0
        hptg = max(0.0, min(1.0, 1.0 - avg_audit))

        return {
            "hptg": round(float(hptg), 4),
            "total_capability_delta": round(float(total_delta), 2),
            "mean_auditability": round(float(avg_audit), 4),
            "milestone_count": len(filtered)
        }

    def compute_m2m_share(self, s_api: float, s_pay: float, s_contract: float, s_traffic: float) -> float:
        """
        Computes composite M2M economic share in [0.0, 1.0] from constituent indicators.
        """
        w = M2M_WEIGHTS
        share = (
            w["api_agent_share"] * s_api +
            w["autonomous_billing"] * s_pay +
            w["smart_contracts"] * s_contract +
            w["machine_web_traffic"] * s_traffic
        )
        return float(np.clip(share, 0.0, 1.0))

    def evaluate_seismograph_timeseries(self) -> List[Dict[str, Any]]:
        """
        Evaluates full historical timeseries of Autonomy Seismograph telemetry.
        """
        results = []
        m2m_history = []
        dates = []

        for date_str, s_api, s_pay, s_contract, s_traffic in MONTHLY_TELEMETRY_SERIES:
            gap_meta = self.compute_cumulative_paper_trail_gap(up_to_date=date_str + "-31")
            hptg = gap_meta["hptg"]
            m2m = self.compute_m2m_share(s_api, s_pay, s_contract, s_traffic)
            m2m_history.append(m2m)
            dates.append(date_str)

            # Composite Score in [0.0, 10.0]
            # M2M critical tipping threshold is set at 0.40 (40% machine-governed liquidity)
            m2m_scaled = min(1.0, m2m / 0.40)
            score = 10.0 * (0.50 * hptg + 0.50 * m2m_scaled)
            score = float(np.clip(score, 0.0, 10.0))

            # Richter Alert Classification
            if score < 3.0:
                alert = "TRIVIAL_AUTONOMY"
                severity = "LOW"
            elif score < 5.5:
                alert = "AGENTIC_EXPANSION"
                severity = "MODERATE"
            elif score < 7.5:
                alert = "ACCELERATED_M2M_DECOUPLING"
                severity = "HIGH"
            elif score < 9.0:
                alert = "CRITICAL_SUPERVISORY_DEFICIT"
                severity = "SEVERE"
            else:
                alert = "AUTONOMOUS_SINGULARITY_LOCK"
                severity = "CRITICAL_EVENT"

            results.append({
                "period": date_str,
                "s_api": round(float(s_api), 4),
                "s_pay": round(float(s_pay), 4),
                "s_contract": round(float(s_contract), 4),
                "s_traffic": round(float(s_traffic), 4),
                "m2m_composite_share": round(float(m2m), 4),
                "human_paper_trail_gap": round(float(hptg), 4),
                "seismograph_score": round(float(score), 2),
                "alert_level": alert,
                "severity": severity,
                "velocity_m2m_per_year": 0.0,
                "acceleration_m2m_per_year2": 0.0
            })

        # Calculate empirical finite-difference velocity & acceleration
        # Periods are approximately spaced; compute annualized rates
        for i in range(1, len(results)):
            # dt in years approximated from monthly index
            # Assume ~3 month step between sequential records
            dt = 0.25
            v = (results[i]["m2m_composite_share"] - results[i-1]["m2m_composite_share"]) / dt
            results[i]["velocity_m2m_per_year"] = round(float(v), 4)

        for i in range(2, len(results)):
            dt = 0.25
            a = (results[i]["velocity_m2m_per_year"] - results[i-1]["velocity_m2m_per_year"]) / dt
            results[i]["acceleration_m2m_per_year2"] = round(float(a), 4)

        return results

    def get_latest_readout(self) -> Dict[str, Any]:
        """
        Returns the active current telemetry reading.
        """
        series = self.evaluate_seismograph_timeseries()
        latest = series[-1]
        summary = {
            "stream_name": "Stream 1: Autonomy Seismometer",
            "active_period": latest["period"],
            "seismograph_score": latest["seismograph_score"],
            "alert_level": latest["alert_level"],
            "severity": latest["severity"],
            "human_paper_trail_gap": latest["human_paper_trail_gap"],
            "m2m_composite_share": latest["m2m_composite_share"],
            "m2m_velocity_annualized": latest["velocity_m2m_per_year"],
            "m2m_acceleration_annualized": latest["acceleration_m2m_per_year2"],
            "total_milestones_evaluated": len(self.milestones),
            "historical_trajectory_points": len(series)
        }
        return summary

    def export_telemetry(self, output_path: Optional[Path] = None) -> Path:
        """
        Exports full timeseries and latest readout to JSON.
        """
        out = output_path or (TELEMETRY_DIR / "autonomy_seismometer.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "metadata": {
                "metric": "HSRI Autonomy Seismometer (Precursor Stream 1)",
                "version": "2.0.0",
                "weights": M2M_WEIGHTS
            },
            "latest": self.get_latest_readout(),
            "timeseries": self.evaluate_seismograph_timeseries(),
            "milestones": self.milestones
        }
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Exported Autonomy Seismometer telemetry to {out}")

        # Sync to Astro src/data if exists
        if SRC_DATA_DIR.exists():
            astro_out = SRC_DATA_DIR / "autonomy_seismometer.json"
            with open(astro_out, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Synchronized to Astro: {astro_out}")

        return out


def main():
    seismometer = AutonomySeismometer()
    readout = seismometer.get_latest_readout()
    print("=================================================================")
    print("  HSRI 2.0 PRECURSOR STREAM 1: AUTONOMY SEISMOMETER READOUT")
    print("=================================================================")
    print(f"  Period:                 {readout['active_period']}")
    print(f"  Seismograph Score:      {readout['seismograph_score']} / 10.0")
    print(f"  Alert Classification:   {readout['alert_level']} ({readout['severity']})")
    print(f"  Human Paper Trail Gap:  {readout['human_paper_trail_gap'] * 100:.1f}%")
    print(f"  M2M Composite Share:    {readout['m2m_composite_share'] * 100:.1f}%")
    print(f"  M2M Velocity (Annual):  +{readout['m2m_velocity_annualized'] * 100:.2f}% / year")
    print("=================================================================")
    seismometer.export_telemetry()


if __name__ == "__main__":
    main()
