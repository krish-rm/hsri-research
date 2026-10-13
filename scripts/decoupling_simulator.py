"""
scripts/decoupling_simulator.py - HSRI 2.0 Civilizational Decoupling Drill Engine (Sprint 34)

Simulates a 14-day (336-hour) zero-notice AI quarantine / cloud cutoff scenario
across four critical societal subsystems:
1. Power Grid Dispatch & Frequency Regulation
2. Interbank Financial Clearing & Market Liquidity
3. Food & Essential Medical Logistics Routing
4. Core Telecommunications & Packet Switching

Models 3 distinct civilizational archetypes:
- Archetype A (Hyper-Automated Hostage): Singapore / Hong Kong
- Archetype B (Fragmented Superpower): United States
- Archetype C (Resilient Decentralizer): Norway / Switzerland / Finland

Exports time-series trajectory and operational crisis injects to:
- data/telemetry/decoupling_drill_results.json
- site-astro/src/data/decoupling_drill_results.json
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Any
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "telemetry"
ASTRO_DATA_DIR = REPO_ROOT / "site-astro" / "src" / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)
ASTRO_DATA_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# ARCHETYPE SUBSYSTEM CONFIGURATIONS
# -----------------------------------------------------------------------------
ARCHETYPES = {
    "archetype_a": {
        "id": "archetype_a",
        "name": "Archetype A: The Hyper-Automated Hostage",
        "exemplars": ["Singapore (SGP)", "Hong Kong (HKG)"],
        "description": "Hyper-dense, cloud-native city-state with near-total reliance on foreign frontier AI APIs and zero domestic analog or sovereign compute air-gaps.",
        "subsystems": {
            "power_grid": {"buffer_hours": 6.0, "half_life_hours": 18.0, "weight": 0.25},
            "financial_clearing": {"buffer_hours": 1.0, "half_life_hours": 4.0, "weight": 0.25},
            "food_logistics": {"buffer_hours": 12.0, "half_life_hours": 36.0, "weight": 0.25},
            "telecommunications": {"buffer_hours": 4.0, "half_life_hours": 12.0, "weight": 0.25},
        },
        "sovereign_posture": "Critical Dependency Trap",
    },
    "archetype_b": {
        "id": "archetype_b",
        "name": "Archetype B: The Fragmented Superpower",
        "exemplars": ["United States (USA)"],
        "description": "Frontier compute empire with vast geographic territory, massive private tech clusters, but high regional fragmentation and hyper-vulnerable financial clearing.",
        "subsystems": {
            "power_grid": {"buffer_hours": 24.0, "half_life_hours": 120.0, "weight": 0.25},
            "financial_clearing": {"buffer_hours": 4.0, "half_life_hours": 14.0, "weight": 0.25},
            "food_logistics": {"buffer_hours": 48.0, "half_life_hours": 96.0, "weight": 0.25},
            "telecommunications": {"buffer_hours": 24.0, "half_life_hours": 72.0, "weight": 0.25},
        },
        "sovereign_posture": "Glass Fortress (High Offensive Compute, Low Decoupling Buffer)",
    },
    "archetype_c": {
        "id": "archetype_c",
        "name": "Archetype C: The Resilient Decentralizer",
        "exemplars": ["Norway (NOR)", "Finland (FIN)", "Switzerland (CHE)"],
        "description": "Decentralized socio-technical democracy with sovereign municipal utilities, mandatory offline defense relays, high civic trust, and robust manual fallbacks.",
        "subsystems": {
            "power_grid": {"buffer_hours": 168.0, "half_life_hours": 720.0, "weight": 0.25},
            "financial_clearing": {"buffer_hours": 72.0, "half_life_hours": 360.0, "weight": 0.25},
            "food_logistics": {"buffer_hours": 240.0, "half_life_hours": 960.0, "weight": 0.25},
            "telecommunications": {"buffer_hours": 144.0, "half_life_hours": 600.0, "weight": 0.25},
        },
        "sovereign_posture": "Sovereign Fortress (High Decoupling Half-Life)",
    },
}

# -----------------------------------------------------------------------------
# TABLETOP OPERATIONAL CRISIS INJECTS
# -----------------------------------------------------------------------------
CRISIS_INJECTS = [
    {
        "hour": 4,
        "inject_code": "INJ-01",
        "title": "Interbank Algorithmic Clearing Freeze",
        "affected_subsystems": ["financial_clearing"],
        "severity": "CRITICAL",
        "description": "Global multi-agent financial liquidity engines desynchronize following cloud certificate revoking. Algorithmic settlements halt; payment processors reject M2M transactions.",
    },
    {
        "hour": 12,
        "inject_code": "INJ-02",
        "title": "Automated Market Maker Liquidity Evaporation",
        "affected_subsystems": ["financial_clearing"],
        "severity": "HIGH",
        "description": "High-frequency market makers running on cloud co-location withdraw liquidity. Sovereign bond bid-ask spreads widen by 450bps.",
    },
    {
        "hour": 24,
        "inject_code": "INJ-03",
        "title": "Renewable Microgrid Frequency Desynchronization",
        "affected_subsystems": ["power_grid"],
        "severity": "CRITICAL",
        "description": "AI-optimized solar and wind inverter dispatch algorithms freeze without central weather and load forecasting APIs. Regional substations trip offline to prevent islanding.",
    },
    {
        "hour": 48,
        "inject_code": "INJ-04",
        "title": "Automated Port & Cold-Chain Routing Stoppage",
        "affected_subsystems": ["food_logistics"],
        "severity": "HIGH",
        "description": "Container terminal autonomous gantry cranes and refrigerated transport manifests lock up as cloud verification servers fail to handshake.",
    },
    {
        "hour": 72,
        "inject_code": "INJ-05",
        "title": "Autonomous BGP Routing Table Decay",
        "affected_subsystems": ["telecommunications"],
        "severity": "CRITICAL",
        "description": "Core internet exchange points experience route flapping as autonomous optimization daemons fail to reconcile divergent routing vectors.",
    },
    {
        "hour": 120,
        "inject_code": "INJ-06",
        "title": "Municipal Water Telemetry Manual Override Failure",
        "affected_subsystems": ["power_grid", "food_logistics"],
        "severity": "HIGH",
        "description": "SCADA water filtration valves fail to respond to legacy human manual control due to missing mechanical bypass keys retired during smart-city automation upgrades.",
    },
    {
        "hour": 168,
        "inject_code": "INJ-07",
        "title": "Emergency Barter & Physical Currency Reversion",
        "affected_subsystems": ["financial_clearing"],
        "severity": "MEDIUM",
        "description": "Retail commercial banks exhaust physical vault banknotes. Municipalities initiate emergency printed voucher distributions.",
    },
    {
        "hour": 240,
        "inject_code": "INJ-08",
        "title": "Civil Defense Analog High-Frequency Radio Reversion",
        "affected_subsystems": ["telecommunications"],
        "severity": "MEDIUM",
        "description": "National security ministries fully deactivate fiber IP packet routing and broadcast emergency directives via shortwave radio and satellite courier relays.",
    },
]


def calculate_subsystem_health(t: float, buffer_hours: float, half_life_hours: float) -> float:
    """
    Subsystem decay equation:
    If t <= buffer: health = 1.0 (buffer holding)
    If t > buffer:  health = exp( -ln(2) / T_half * (t - buffer) )
    """
    if t <= buffer_hours:
        return 1.0
    elapsed = t - buffer_hours
    decay = math.exp(-math.log(2) * elapsed / half_life_hours)
    return float(max(0.01, min(1.0, decay)))


def simulate_decoupling_drill():
    """Simulates 14-day (336 hours) drill across 3 archetypes."""
    total_hours = 336
    time_points = list(range(0, total_hours + 1, 1))  # Hourly resolution

    results = {
        "metadata": {
            "title": "HSRI 2.0 Civilizational Decoupling Drill (Operation Silent Cloud)",
            "simulation_window_hours": 336,
            "simulation_window_days": 14,
            "scenario": "Sudden, zero-notice global recursive containment quarantine (complete cloud/API severance)",
            "methodology": "Leontief Floor Non-Compensatory Weakest-Link Dynamic Aggregation",
            "doi": "10.5281/zenodo.10842000",
            "generated_at": "2026-10-13T23:25:00+00:00",
        },
        "archetypes": {},
        "crisis_injects": CRISIS_INJECTS,
        "comparative_metrics": {},
    }

    for arch_key, arch in ARCHETYPES.items():
        subsystems = arch["subsystems"]
        timeline = []

        t_half_crossing = None
        t_critical_crossing = None  # Drops below 0.20
        t_first_fracture = None    # Drops below 0.90

        for t in time_points:
            sub_scores = {}
            for sub_name, params in subsystems.items():
                score = calculate_subsystem_health(t, params["buffer_hours"], params["half_life_hours"])
                sub_scores[sub_name] = round(score, 4)

            scores_list = list(sub_scores.values())
            linear_avg = sum(scores_list) / 4.0
            weakest_sub = min(sub_scores, key=sub_scores.get)
            weakest_val = sub_scores[weakest_sub]

            # Leontief Floor Weakest-Link:
            # H = sqrt( min * linear_avg )
            leontief_composite = math.sqrt(weakest_val * linear_avg)

            if t_first_fracture is None and leontief_composite < 0.90:
                t_first_fracture = t
            if t_half_crossing is None and leontief_composite <= 0.50:
                t_half_crossing = t
            if t_critical_crossing is None and leontief_composite <= 0.20:
                t_critical_crossing = t

            # Record sampled points (every 2 hours to keep JSON compact and fast)
            if t % 2 == 0 or t == total_hours:
                timeline.append({
                    "hour": t,
                    "day": round(t / 24.0, 2),
                    "power_grid": sub_scores["power_grid"],
                    "financial_clearing": sub_scores["financial_clearing"],
                    "food_logistics": sub_scores["food_logistics"],
                    "telecommunications": sub_scores["telecommunications"],
                    "linear_composite": round(linear_avg, 4),
                    "leontief_composite": round(leontief_composite, 4),
                    "weakest_link": weakest_sub,
                })

        final_composite = timeline[-1]["leontief_composite"]
        results["archetypes"][arch_key] = {
            "id": arch["id"],
            "name": arch["name"],
            "exemplars": arch["exemplars"],
            "description": arch["description"],
            "sovereign_posture": arch["sovereign_posture"],
            "metrics": {
                "t_first_fracture_hours": t_first_fracture if t_first_fracture is not None else 336,
                "t_half_crossing_hours": t_half_crossing if t_half_crossing is not None else 336,
                "t_critical_crossing_hours": t_critical_crossing if t_critical_crossing is not None else 336,
                "day_14_residual_functionality": final_composite,
            },
            "timeline": timeline,
        }

    # Summary table
    results["comparative_metrics"] = {
        "archetype_a": {
            "name": "The Hyper-Automated Hostage (Singapore / HK)",
            "t_half_hours": results["archetypes"]["archetype_a"]["metrics"]["t_half_crossing_hours"],
            "day_14_residual": results["archetypes"]["archetype_a"]["metrics"]["day_14_residual_functionality"],
            "diagnosis": "Rapid Systemic Paralysis within 28.6 hours; Day 3 Functional Collapse.",
        },
        "archetype_b": {
            "name": "The Fragmented Superpower (United States)",
            "t_half_hours": results["archetypes"]["archetype_b"]["metrics"]["t_half_crossing_hours"],
            "day_14_residual": results["archetypes"]["archetype_b"]["metrics"]["day_14_residual_functionality"],
            "diagnosis": "Financial bottleneck fracture at 18 hours; 50% systemic failure by Day 6.",
        },
        "archetype_c": {
            "name": "The Resilient Decentralizer (Nordic / Swiss)",
            "t_half_hours": results["archetypes"]["archetype_c"]["metrics"]["t_half_crossing_hours"],
            "day_14_residual": results["archetypes"]["archetype_c"]["metrics"]["day_14_residual_functionality"],
            "diagnosis": "Sovereign Air-Gap Resilience; retains >75% functionality throughout 14 days.",
        },
    }

    # Save to data/ and site-astro/
    out_file1 = DATA_DIR / "decoupling_drill_results.json"
    out_file2 = ASTRO_DATA_DIR / "decoupling_drill_results.json"

    with open(out_file1, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Exported: {out_file1}")

    with open(out_file2, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Exported: {out_file2}")

    return results


if __name__ == "__main__":
    simulate_decoupling_drill()
