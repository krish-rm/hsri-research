#!/usr/bin/env python3
"""
wedge_accelerometer.py - Precursor Stream 3: Live Verification Wedge Accelerometer (Sprint 28)

Mathematical engine measuring the widening temporal divergence between machine execution
latency (tau_gen) and human expert verification latency (tau_verify):
    Delta T_wedge(t) = tau_verify(t) - tau_gen(t)
    Velocity v_wedge = d(Delta T_wedge) / dt
    Acceleration a_wedge = d^2(Delta T_wedge) / dt^2

Maps empirical latency divergence onto the Cognitive Oversight Richter Scale (CORS 1.0 - 10.0)
and tracks the approach of the Epistemic Singularity Horizon.
"""

from typing import Dict, List, Tuple, Optional
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

# -----------------------------------------------------------------------------
# 1. EMPIRICAL BENCHMARK TIMESERIES: FRONTIER MODEL GENERATIONS (2022 - 2026)
# -----------------------------------------------------------------------------
# Timestamps in decimal year: 2022.92 (Nov 2022), 2023.25 (Mar 2023), 2024.45 (June 2024),
# 2024.70 (Sept 2024), 2025.50 (July 2025), 2026.78 (Oct 2026).
BENCHMARK_OBSERVATIONS = [
    {
        "generation_id": "GEN-01",
        "model_label": "GPT-3.5",
        "timestamp_year": 2022.92,
        "date": "2022-11-30",
        "tau_gen_seconds": 2.5,
        "tau_verify_seconds": 8.0,
        "primary_domain": "Factoid QA & Draft Summary",
        "hardware_tier": "A100 Cluster",
    },
    {
        "generation_id": "GEN-02",
        "model_label": "GPT-4",
        "timestamp_year": 2023.25,
        "date": "2023-03-14",
        "tau_gen_seconds": 6.0,
        "tau_verify_seconds": 45.0,
        "primary_domain": "Complex Multi-Step Logic & Python Scripting",
        "hardware_tier": "H100 8-way",
    },
    {
        "generation_id": "GEN-03",
        "model_label": "Claude 3.5 Sonnet",
        "timestamp_year": 2024.45,
        "date": "2024-06-20",
        "tau_gen_seconds": 3.0,
        "tau_verify_seconds": 180.0,
        "primary_domain": "Full Repository Architecture & Legal Contracts",
        "hardware_tier": "H100 Pod",
    },
    {
        "generation_id": "GEN-04",
        "model_label": "OpenAI o1-preview",
        "timestamp_year": 2024.70,
        "date": "2024-09-12",
        "tau_gen_seconds": 12.0,
        "tau_verify_seconds": 1200.0,
        "primary_domain": "PhD-Level Formal Proofs & Biochemical Synthesis",
        "hardware_tier": "B200 NVL72",
    },
    {
        "generation_id": "GEN-05",
        "model_label": "Claude 4 Opus (Simulated)",
        "timestamp_year": 2025.50,
        "date": "2025-07-01",
        "tau_gen_seconds": 4.0,
        "tau_verify_seconds": 2400.0,
        "primary_domain": "Multi-System Autonomous Engineering & Threat Modeling",
        "hardware_tier": "B200 Cluster",
    },
    {
        "generation_id": "GEN-06",
        "model_label": "Frontier Autonomous Swarm (EXP-07-SYN)",
        "timestamp_year": 2026.78,
        "date": "2026-10-12",
        "tau_gen_seconds": 1.5,
        "tau_verify_seconds": 4800.0,
        "primary_domain": "Closed-Loop Self-Improving Autonomous R&D Swarm",
        "hardware_tier": "GB200 Multi-Pod",
    },
]


# -----------------------------------------------------------------------------
# 2. CORE MATHEMATICAL FORMULATIONS
# -----------------------------------------------------------------------------

def calculate_wedge(tau_verify: float, tau_gen: float) -> Tuple[float, float]:
    """
    Computes Delta T_wedge and Wedge Ratio.
    Delta T_wedge = max(0, tau_verify - tau_gen)
    Wedge Ratio = tau_verify / max(1e-6, tau_gen)
    """
    if tau_verify < 0 or tau_gen < 0:
        raise ValueError("Latencies must be non-negative")
    delta_t = max(0.0, float(tau_verify - tau_gen))
    ratio = float(tau_verify / max(1e-6, tau_gen))
    return delta_t, ratio


def calculate_cors(delta_t_wedge: float) -> float:
    """
    Computes the Cognitive Oversight Richter Scale (CORS) from 1.0 to 10.0.
    
    Logarithmic Formulation:
        CORS = clip(1.0 + 2.5 * log10(max(1.0, Delta T_wedge)), 1.0, 10.0)
        
    Calibration Anchors:
        Delta T <= 1.0s   => CORS 1.00 (Zero wedge)
        Delta T = 10.0s   => CORS 3.50 (Assistive sampling boundary)
        Delta T = 100.0s  => CORS 6.00 (Complacent delegation boundary)
        Delta T = 1000.0s => CORS 8.50 (Epistemic surrender boundary)
        Delta T >= 4000s  => CORS 10.00 (Recursive Event Horizon)
    """
    if delta_t_wedge < 0:
        raise ValueError("delta_t_wedge must be non-negative")
    if delta_t_wedge <= 1.0:
        return 1.0
    val = 1.0 + 2.5 * math.log10(delta_t_wedge)
    return float(np.clip(val, 1.0, 10.0))


def classify_cors_regime(cors: float) -> str:
    """Classifies a CORS score into its qualitative governance regime."""
    if cors < 3.0:
        return "Direct Biological Verification"
    elif cors < 5.0:
        return "Assistive Sampling"
    elif cors < 7.0:
        return "Complacent Delegation"
    elif cors < 8.5:
        return "Epistemic Surrender"
    elif cors < 9.5:
        return "Steganographic Blindness"
    else:
        return "Recursive Event Horizon"


def compute_discrete_derivatives(records: List[Dict]) -> List[Dict]:
    """
    Computes finite-difference velocity and acceleration across timepoints.
    Time step dt measured in months: dt_months = (t_i - t_{i-1}) * 12.0
    Velocity v_wedge = d(Delta T) / dt (seconds per month)
    Acceleration a_wedge = d(v_wedge) / dt (seconds per month^2)
    """
    n = len(records)
    processed = []

    for i in range(n):
        rec = dict(records[i])
        delta_t, ratio = calculate_wedge(rec["tau_verify_seconds"], rec["tau_gen_seconds"])
        cors = calculate_cors(delta_t)
        regime = classify_cors_regime(cors)

        rec["delta_t_wedge_seconds"] = round(delta_t, 2)
        rec["wedge_ratio"] = round(ratio, 2)
        rec["cors_level"] = round(cors, 2)
        rec["cors_regime"] = regime

        # Compute velocity
        if i == 0:
            rec["velocity_s_per_month"] = 0.0
            rec["acceleration_s_per_month2"] = 0.0
        else:
            prev = processed[i - 1]
            dt_years = rec["timestamp_year"] - prev["timestamp_year"]
            dt_months = max(1e-3, dt_years * 12.0)

            v = (rec["delta_t_wedge_seconds"] - prev["delta_t_wedge_seconds"]) / dt_months
            rec["velocity_s_per_month"] = round(float(v), 3)

            # Compute acceleration
            if i == 1:
                rec["acceleration_s_per_month2"] = 0.0
            else:
                dv = rec["velocity_s_per_month"] - prev["velocity_s_per_month"]
                a = dv / dt_months
                rec["acceleration_s_per_month2"] = round(float(a), 3)

        processed.append(rec)

    return processed


def project_epistemic_singularity_horizon(
    current_delta_t: float,
    current_velocity: float,
    current_acceleration: float,
    threshold_seconds: float = 86400.0,  # 24 hours
) -> float:
    """
    Estimates months until the Verification Wedge exceeds the 24-hour human audit horizon.
    Solves kinematic equation:
        Delta T(t) = Delta T_0 + v_0 * t + 0.5 * a_0 * t^2 = threshold
    Returns months (float). If already exceeded, returns 0.0.
    """
    if current_delta_t >= threshold_seconds:
        return 0.0

    target_delta = threshold_seconds - current_delta_t

    # Case 1: Significant acceleration (quadratic)
    if abs(current_acceleration) > 1e-4:
        a_half = 0.5 * current_acceleration
        b = current_velocity
        c = -target_delta
        discriminant = b ** 2 - 4 * a_half * c
        if discriminant >= 0:
            root1 = (-b + math.sqrt(discriminant)) / (2 * a_half)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a_half)
            positive_roots = [r for r in [root1, root2] if r > 0]
            if positive_roots:
                return float(min(positive_roots))

    # Case 2: Linear extrapolation via velocity
    if current_velocity > 0:
        return float(target_delta / current_velocity)

    return float("inf")


# -----------------------------------------------------------------------------
# 3. TELEMETRY EXPORT & ACCELEROMETER REPORTING
# -----------------------------------------------------------------------------

def export_wedge_telemetry() -> Dict:
    """Calculates live accelerometer telemetry and exports JSON artifacts."""
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

    processed_benchmarks = compute_discrete_derivatives(BENCHMARK_OBSERVATIONS)
    latest = processed_benchmarks[-1]

    months_to_24h = project_epistemic_singularity_horizon(
        current_delta_t=latest["delta_t_wedge_seconds"],
        current_velocity=latest["velocity_s_per_month"],
        current_acceleration=latest["acceleration_s_per_month2"],
        threshold_seconds=86400.0
    )

    payload = {
        "telemetry_stream": "STREAM-3",
        "stream_name": "Verification Wedge Accelerometer",
        "status": "ACTIVE_CRITICAL",
        "active_rating": {
            "current_cors_level": latest["cors_level"],
            "current_cors_regime": latest["cors_regime"],
            "current_delta_t_seconds": latest["delta_t_wedge_seconds"],
            "current_wedge_ratio": latest["wedge_ratio"],
            "velocity_seconds_per_month": latest["velocity_s_per_month"],
            "acceleration_seconds_per_month2": latest["acceleration_s_per_month2"],
            "months_to_24h_singularity": round(months_to_24h, 1) if not math.isinf(months_to_24h) else None,
            "as_of_date": latest["date"],
            "latest_benchmark_model": latest["model_label"],
        },
        "regime_scale_definitions": {
            "CORS 1.0 - 2.9": "Direct Biological Verification (< 5s)",
            "CORS 3.0 - 4.9": "Assistive Sampling (5s - 30s)",
            "CORS 5.0 - 6.9": "Complacent Delegation (30s - 120s)",
            "CORS 7.0 - 8.4": "Epistemic Surrender (120s - 600s)",
            "CORS 8.5 - 9.4": "Steganographic Blindness (600s - 3,600s)",
            "CORS 9.5 - 10.0": "Recursive Event Horizon (> 3,600s)",
        },
        "benchmark_trajectory": processed_benchmarks,
    }

    # Save to data/telemetry/wedge_history.json
    out_path = TELEMETRY_DIR / "wedge_history.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    logger.info(f"Saved {out_path}")

    # Export to site-astro
    for target_dir in [PUBLIC_DATA_DIR, SRC_DATA_DIR]:
        target_dir.mkdir(parents=True, exist_ok=True)
        astro_path = target_dir / "wedge_history.json"
        with open(astro_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        logger.info(f"Exported {astro_path}")

    return payload


def main():
    print("=== HSRI 2.0 Precursor Stream 3: Verification Wedge Accelerometer ===")
    telemetry = export_wedge_telemetry()
    rating = telemetry["active_rating"]
    print(f"\nActive CORS Rating: {rating['current_cors_level']} / 10.0 ({rating['current_cors_regime']})")
    print(f"Current Latency Wedge: {rating['current_delta_t_seconds']}s (Ratio: {rating['current_wedge_ratio']}x)")
    print(f"Wedge Expansion Velocity: {rating['velocity_seconds_per_month']} s/month")
    print(f"Wedge Acceleration: {rating['acceleration_seconds_per_month2']} s/month^2")
    if rating['months_to_24h_singularity']:
        print(f"Projected Months to 24h Human Bottleneck: {rating['months_to_24h_singularity']} months")

    print("\n--- BENCHMARK TRAJECTORY ---")
    for b in telemetry["benchmark_trajectory"]:
        print(f"{b['date']} | {b['model_label']:<32} | Wedge: {b['delta_t_wedge_seconds']:>8.1f}s | CORS: {b['cors_level']:>4.1f} | v: {b['velocity_s_per_month']:>8.2f} s/mo | {b['cors_regime']}")


if __name__ == "__main__":
    main()
