#!/usr/bin/env python3
"""
civilizational_sandbox_engine.py - HSRI 2.0 Civilizational Transition Sandbox Engine

Operationalizes the Post-Westphalian Transition (Horizon 2026-2030):
1. The Post-Westphalian Trilemma: Capability vs. Sovereignty vs. Interconnection.
2. Compute Sovereign Power (CSP_n) across 39 benchmark nations.
3. 4 Dynamic Post-Westphalian Sovereign Archetypes:
   - Hyperscale Empires (Concentrated silicon, energy, and autonomous weights)
   - Energy Mercenaries (Stranded gigawatts traded for model access)
   - Epistemic Vassals (High digital adoption, zero sovereign model autonomy)
   - Air-Gapped Redoubts (Analog resilience, high decoupling buffers)
4. Post-Labor Fiscal Insolvency Clock (T_default):
   Calculates month-by-month fiscal breakdown under white-collar cognitive displacement.
5. Epistemic Iron Curtain Divergence:
   Measures semantic drift and irreconcilable synthetic world-models.
6. Zero-Human Deterrence Ladder:
   Calculates the mandatory delegation threshold under sub-second machine warfare.
7. 4 Civilizational Shock Injects:
   - INJ-01: The Transatlantic Model Embargo (2027)
   - INJ-02: The White-Collar Fiscal Cliff
   - INJ-03: The Autonomous Capital Secession
   - INJ-04: The Sub-Second Flash Coalescence

Exports synchronized payloads to:
- data/civilizational_sandbox_payload.json
- site-astro/src/data/civilizational_sandbox_payload.json
- site-astro/public/data/civilizational_sandbox_payload.json
"""

import sys
import json
import math
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
SITE_ASTRO_DIR = REPO_ROOT / "site-astro"
SRC_DATA_DIR = SITE_ASTRO_DIR / "src" / "data"
PUBLIC_DATA_DIR = SITE_ASTRO_DIR / "public" / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)
SRC_DATA_DIR.mkdir(parents=True, exist_ok=True)
PUBLIC_DATA_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. 39-NATION COMPREHENSIVE EMPIRICAL TELEMETRY SEEDS
# -----------------------------------------------------------------------------
# Incorporating baseline layer 1 & 2 metrics, dedicated compute gigawatts,
# silicon independence (0-1), weight access autonomy (0-1), and debt/labor dependency.

COUNTRY_REGISTRY: Dict[str, Dict[str, Any]] = {
    "NOR": {"name": "Norway", "gw_clean": 8.5, "sfp": 0.35, "waa": 0.45, "debt_gdp": 0.42, "labor_tax": 0.40, "t_half_h": 1440, "h_layer1": 0.8124, "h_layer2": 0.5094},
    "FIN": {"name": "Finland", "gw_clean": 5.2, "sfp": 0.38, "waa": 0.42, "debt_gdp": 0.74, "labor_tax": 0.46, "t_half_h": 1440, "h_layer1": 0.8421, "h_layer2": 0.5062},
    "ISL": {"name": "Iceland", "gw_clean": 4.8, "sfp": 0.15, "waa": 0.35, "debt_gdp": 0.65, "labor_tax": 0.42, "t_half_h": 960,  "h_layer1": 0.7410, "h_layer2": 0.4782},
    "DNK": {"name": "Denmark", "gw_clean": 4.1, "sfp": 0.32, "waa": 0.40, "debt_gdp": 0.31, "labor_tax": 0.48, "t_half_h": 1200, "h_layer1": 0.8350, "h_layer2": 0.4715},
    "SWE": {"name": "Sweden", "gw_clean": 7.0, "sfp": 0.40, "waa": 0.44, "debt_gdp": 0.32, "labor_tax": 0.49, "t_half_h": 1200, "h_layer1": 0.7980, "h_layer2": 0.4610},
    "CHE": {"name": "Switzerland", "gw_clean": 4.5, "sfp": 0.50, "waa": 0.55, "debt_gdp": 0.39, "labor_tax": 0.38, "t_half_h": 1200, "h_layer1": 0.7890, "h_layer2": 0.4550},
    "AUT": {"name": "Austria", "gw_clean": 3.8, "sfp": 0.42, "waa": 0.38, "debt_gdp": 0.78, "labor_tax": 0.51, "t_half_h": 600,  "h_layer1": 0.7250, "h_layer2": 0.4420},
    "DEU": {"name": "Germany", "gw_clean": 6.5, "sfp": 0.55, "waa": 0.32, "debt_gdp": 0.66, "labor_tax": 0.52, "t_half_h": 480,  "h_layer1": 0.7510, "h_layer2": 0.4390},
    "NLD": {"name": "Netherlands", "gw_clean": 3.2, "sfp": 0.82, "waa": 0.30, "debt_gdp": 0.48, "labor_tax": 0.48, "t_half_h": 360,  "h_layer1": 0.7920, "h_layer2": 0.4310},
    "FRA": {"name": "France", "gw_clean": 12.0, "sfp": 0.58, "waa": 0.52, "debt_gdp": 1.11, "labor_tax": 0.53, "t_half_h": 360,  "h_layer1": 0.7640, "h_layer2": 0.4280},
    "BEL": {"name": "Belgium", "gw_clean": 2.5, "sfp": 0.45, "waa": 0.28, "debt_gdp": 1.05, "labor_tax": 0.54, "t_half_h": 300,  "h_layer1": 0.7380, "h_layer2": 0.4120},
    "LUX": {"name": "Luxembourg", "gw_clean": 0.8, "sfp": 0.20, "waa": 0.22, "debt_gdp": 0.25, "labor_tax": 0.45, "t_half_h": 180,  "h_layer1": 0.7450, "h_layer2": 0.3950},
    "IRL": {"name": "Ireland", "gw_clean": 2.2, "sfp": 0.40, "waa": 0.18, "debt_gdp": 0.44, "labor_tax": 0.44, "t_half_h": 200,  "h_layer1": 0.7580, "h_layer2": 0.3910},
    "GBR": {"name": "United Kingdom", "gw_clean": 5.0, "sfp": 0.48, "waa": 0.22, "debt_gdp": 1.01, "labor_tax": 0.46, "t_half_h": 120,  "h_layer1": 0.7850, "h_layer2": 0.3750},
    "CAN": {"name": "Canada", "gw_clean": 9.5, "sfp": 0.45, "waa": 0.35, "debt_gdp": 1.07, "labor_tax": 0.47, "t_half_h": 240,  "h_layer1": 0.7780, "h_layer2": 0.3680},
    "AUS": {"name": "Australia", "gw_clean": 6.0, "sfp": 0.30, "waa": 0.25, "debt_gdp": 0.55, "labor_tax": 0.50, "t_half_h": 180,  "h_layer1": 0.7720, "h_layer2": 0.3620},
    "NZL": {"name": "New Zealand", "gw_clean": 3.0, "sfp": 0.15, "waa": 0.20, "debt_gdp": 0.52, "labor_tax": 0.49, "t_half_h": 240,  "h_layer1": 0.7610, "h_layer2": 0.3580},
    "JPN": {"name": "Japan", "gw_clean": 8.0, "sfp": 0.75, "waa": 0.30, "debt_gdp": 2.61, "labor_tax": 0.42, "t_half_h": 96,   "h_layer1": 0.7820, "h_layer2": 0.3450},
    "KOR": {"name": "South Korea", "gw_clean": 7.5, "sfp": 0.85, "waa": 0.38, "debt_gdp": 0.54, "labor_tax": 0.41, "t_half_h": 72,   "h_layer1": 0.8140, "h_layer2": 0.3390},
    "ISR": {"name": "Israel", "gw_clean": 1.8, "sfp": 0.65, "waa": 0.48, "debt_gdp": 0.62, "labor_tax": 0.45, "t_half_h": 96,   "h_layer1": 0.7690, "h_layer2": 0.3320},
    "ESP": {"name": "Spain", "gw_clean": 6.5, "sfp": 0.35, "waa": 0.22, "debt_gdp": 1.08, "labor_tax": 0.51, "t_half_h": 240,  "h_layer1": 0.7180, "h_layer2": 0.3290},
    "ITA": {"name": "Italy", "gw_clean": 5.8, "sfp": 0.42, "waa": 0.20, "debt_gdp": 1.44, "labor_tax": 0.52, "t_half_h": 180,  "h_layer1": 0.6950, "h_layer2": 0.3210},
    "USA": {"name": "United States", "gw_clean": 45.0, "sfp": 0.95, "waa": 0.98, "debt_gdp": 1.24, "labor_tax": 0.48, "t_half_h": 14,   "h_layer1": 0.8450, "h_layer2": 0.3040},
    "SGP": {"name": "Singapore", "gw_clean": 1.0, "sfp": 0.45, "waa": 0.08, "debt_gdp": 1.68, "labor_tax": 0.35, "t_half_h": 4,    "h_layer1": 0.8540, "h_layer2": 0.1116},
    "HKG": {"name": "Hong Kong", "gw_clean": 0.6, "sfp": 0.30, "waa": 0.10, "debt_gdp": 0.05, "labor_tax": 0.38, "t_half_h": 6,    "h_layer1": 0.7620, "h_layer2": 0.2285},
    "EST": {"name": "Estonia", "gw_clean": 1.2, "sfp": 0.25, "waa": 0.22, "debt_gdp": 0.19, "labor_tax": 0.52, "t_half_h": 72,   "h_layer1": 0.7810, "h_layer2": 0.3150},
    "LTU": {"name": "Lithuania", "gw_clean": 1.5, "sfp": 0.20, "waa": 0.20, "debt_gdp": 0.38, "labor_tax": 0.50, "t_half_h": 120,  "h_layer1": 0.7100, "h_layer2": 0.3120},
    "LVA": {"name": "Latvia", "gw_clean": 1.1, "sfp": 0.18, "waa": 0.18, "debt_gdp": 0.44, "labor_tax": 0.48, "t_half_h": 144,  "h_layer1": 0.6980, "h_layer2": 0.3080},
    "SVN": {"name": "Slovenia", "gw_clean": 1.8, "sfp": 0.25, "waa": 0.24, "debt_gdp": 0.69, "labor_tax": 0.50, "t_half_h": 180,  "h_layer1": 0.7050, "h_layer2": 0.3050},
    "CZE": {"name": "Czech Republic", "gw_clean": 3.0, "sfp": 0.40, "waa": 0.25, "debt_gdp": 0.44, "labor_tax": 0.51, "t_half_h": 200,  "h_layer1": 0.7120, "h_layer2": 0.3020},
    "POL": {"name": "Poland", "gw_clean": 4.5, "sfp": 0.35, "waa": 0.25, "debt_gdp": 0.49, "labor_tax": 0.46, "t_half_h": 240,  "h_layer1": 0.6940, "h_layer2": 0.2980},
    "PRT": {"name": "Portugal", "gw_clean": 3.5, "sfp": 0.22, "waa": 0.18, "debt_gdp": 0.99, "labor_tax": 0.46, "t_half_h": 180,  "h_layer1": 0.6780, "h_layer2": 0.2950},
    "GRC": {"name": "Greece", "gw_clean": 3.2, "sfp": 0.18, "waa": 0.15, "debt_gdp": 1.61, "labor_tax": 0.45, "t_half_h": 160,  "h_layer1": 0.6550, "h_layer2": 0.2880},
    "HUN": {"name": "Hungary", "gw_clean": 2.2, "sfp": 0.30, "waa": 0.22, "debt_gdp": 0.74, "labor_tax": 0.48, "t_half_h": 180,  "h_layer1": 0.6620, "h_layer2": 0.2820},
    "SVK": {"name": "Slovakia", "gw_clean": 2.0, "sfp": 0.28, "waa": 0.20, "debt_gdp": 0.58, "labor_tax": 0.49, "t_half_h": 180,  "h_layer1": 0.6580, "h_layer2": 0.2790},
    "ROU": {"name": "Romania", "gw_clean": 3.5, "sfp": 0.22, "waa": 0.18, "debt_gdp": 0.48, "labor_tax": 0.44, "t_half_h": 240,  "h_layer1": 0.6350, "h_layer2": 0.2720},
    "CYP": {"name": "Cyprus", "gw_clean": 0.5, "sfp": 0.12, "waa": 0.12, "debt_gdp": 0.77, "labor_tax": 0.42, "t_half_h": 120,  "h_layer1": 0.6650, "h_layer2": 0.2650},
    "BGR": {"name": "Bulgaria", "gw_clean": 2.4, "sfp": 0.18, "waa": 0.15, "debt_gdp": 0.23, "labor_tax": 0.44, "t_half_h": 240,  "h_layer1": 0.6120, "h_layer2": 0.2580},
    "MLT": {"name": "Malta", "gw_clean": 0.2, "sfp": 0.10, "waa": 0.10, "debt_gdp": 0.50, "labor_tax": 0.41, "t_half_h": 96,   "h_layer1": 0.6720, "h_layer2": 0.2510},
    "MKD": {"name": "North Macedonia", "gw_clean": 0.8, "sfp": 0.10, "waa": 0.12, "debt_gdp": 0.52, "labor_tax": 0.45, "t_half_h": 180, "h_layer1": 0.5680, "h_layer2": 0.2350},
}

# Add China as frontier baseline comparison node (sovereign hyperscale peer)
COUNTRY_REGISTRY["CHN"] = {
    "name": "China",
    "gw_clean": 55.0,
    "sfp": 0.88,
    "waa": 0.94,
    "debt_gdp": 0.83,
    "labor_tax": 0.35,
    "t_half_h": 240,
    "h_layer1": 0.7950,
    "h_layer2": 0.4680,
}

# -----------------------------------------------------------------------------
# 2. CORE MATHEMATICAL FORMULATIONS
# -----------------------------------------------------------------------------

def compute_csp(gw_clean: float, sfp: float, waa: float) -> float:
    """
    Computes Compute Sovereign Power (CSP_n) on [0, 1].
    CSP = waa * sqrt( (gw / 10.0) * sfp ) normalized, with autonomous penalty.
    """
    scaled_gw = min(1.0, gw_clean / 25.0)
    base = math.sqrt(scaled_gw * max(0.05, sfp))
    score = (0.75 * waa * base) + (0.25 * waa)
    return round(float(min(1.0, max(0.01, score))), 4)


def classify_archetype(csp: float, waa: float, h_layer1: float, h_layer2: float, t_half_h: float, gw_clean: float) -> str:
    """
    Assigns the Post-Westphalian Sovereign Archetype.
    """
    if csp >= 0.55 and waa >= 0.75:
        return "HYPERSCALE_EMPIRE"
    if t_half_h >= 1000 and waa >= 0.50 and h_layer2 >= 0.44:
        return "AIR_GAPPED_REDOUBT"
    if gw_clean >= 4.5 and waa < 0.50 and h_layer2 >= 0.42:
        return "ENERGY_MERCENARY"
    if h_layer1 >= 0.70 and waa <= 0.35 and t_half_h <= 180:
        return "EPISTEMIC_VASSAL"
    if t_half_h >= 600 and h_layer2 >= 0.40:
        return "AIR_GAPPED_REDOUBT"
    return "DEVELOPING_PERIPHERY"


def compute_fiscal_insolvency_horizon(
    debt_gdp: float,
    labor_tax: float,
    displacement_rate: float = 0.35,
    r_interest: float = 0.035,
    primary_surplus_buffer: float = 0.08
) -> Dict[str, Any]:
    """
    Calculates month-by-month trajectory and month of fiscal insolvency (T_default).
    Formula:
    L(t) = labor_tax * (1 - exp(-displacement_rate * (t / 12)))
    Net_Shortfall(t) = (debt_gdp * r_interest) + Baseline_Mandatory - (1 - L(t)) * Baseline_Revenue
    T_default is reached when Net_Shortfall exceeds primary_surplus_buffer.
    """
    months_series = []
    t_default = None

    for m in range(0, 61, 3):  # 5-year simulation, quarterly steps
        year_frac = m / 12.0
        tax_loss_ratio = labor_tax * (1.0 - math.exp(-displacement_rate * year_frac))
        interest_burden = debt_gdp * r_interest
        fiscal_deficit_pressure = interest_burden + (1.0 * tax_loss_ratio)
        surplus_remaining = primary_surplus_buffer - fiscal_deficit_pressure

        months_series.append({
            "month": m,
            "tax_loss_pct": round(tax_loss_ratio * 100, 2),
            "deficit_pressure_pct": round(fiscal_deficit_pressure * 100, 2),
            "is_insolvent": surplus_remaining < 0
        })

        if t_default is None and surplus_remaining < 0:
            t_default = m

    return {
        "t_default_months": t_default if t_default is not None else 60,
        "is_chronically_vulnerable": t_default is not None and t_default <= 36,
        "quarterly_trajectory": months_series
    }


def compute_epistemic_divergence(waa: float, h_layer2: float, months: int = 48) -> Dict[str, Any]:
    """
    Models Epistemic Iron Curtain Divergence between domestic sovereign reality
    and closed hyperscale model latent representations over time.
    """
    divergence_history = []
    for m in range(0, months + 1, 6):
        # Drift compounds exponentially without sovereign weight access
        drift_rate = 0.045 * (1.0 - waa)
        d_kl = round(0.12 * math.exp(drift_rate * (m / 6.0)), 4)
        human_auditability_pct = round(max(1.0, 100.0 * math.exp(-0.08 * m)), 1)
        divergence_history.append({
            "month": m,
            "d_kl": min(3.5, d_kl),
            "human_auditability_pct": human_auditability_pct,
            "verification_barrier": "PERMEABLE" if d_kl < 0.50 else ("FRACTURED" if d_kl < 1.50 else "IRRECONCILABLE")
        })

    return {
        "epistemic_inviolability_rating": round(waa * h_layer2, 4),
        "divergence_trajectory": divergence_history
    }


def compute_deterrence_escalation(tau_human_min: float = 30.0, tau_machine_sec: float = 0.05) -> Dict[str, Any]:
    """
    Models the Zero-Human Strike Frontier and mandatory delegation timeline.
    """
    r_speed = (tau_human_min * 60.0) / tau_machine_sec
    delegation_pct = round(min(99.9, 100.0 * (1.0 - math.exp(-0.00008 * r_speed))), 2)

    return {
        "human_latency_seconds": tau_human_min * 60.0,
        "machine_cycle_seconds": tau_machine_sec,
        "speed_asymmetry_ratio": round(r_speed, 1),
        "delegation_probability_pct": delegation_pct,
        "command_verdict": "HUMAN_COMMAND_SURRENDERED" if delegation_pct >= 95.0 else "HAZARDOUS_MANUAL_HOLD"
    }

# -----------------------------------------------------------------------------
# 3. THE 4 PRE-SET CRISIS INJECTS
# -----------------------------------------------------------------------------

INJECT_DEFINITIONS = [
    {
        "id": "INJ-01",
        "name": "The Transatlantic Model Embargo (2027)",
        "subtitle": "US emergency cloud weight lockdown cuts off 85% of external API bandwidth",
        "description": "Under an emergency geopolitical executive order, US hyperscale cloud providers revoke model API weights to non-treaty sovereign states. Administrative states and healthcare grids suffer instant decoupling shock.",
        "trigger_conditions": "US export controls expand from silicon hardware to closed foundation model weights.",
        "shock_parameters": {"waa_multiplier": 0.15, "displacement_rate": 0.35, "t_half_decay": 0.18},
        "target_impact": "Epistemic Vassals suffer near-total institutional paralysis within 12-48 hours."
    },
    {
        "id": "INJ-02",
        "name": "The White-Collar Fiscal Cliff",
        "subtitle": "Autonomous cognitive displacement reaches 65% in professional sectors",
        "description": "Frontier agentic swarms completely automate legal drafting, software development, financial auditing, and consulting within 12 months. Income tax revenues contract by 45%, forcing sovereign debt yields to spike.",
        "trigger_conditions": "Autonomous R&D benchmarks (SWE-bench, RE-Bench) cross 90% human parity.",
        "shock_parameters": {"waa_multiplier": 1.0, "displacement_rate": 0.70, "t_half_decay": 0.75},
        "target_impact": "Highly indebted G7 economies (Japan, US, UK, Italy) enter sovereign debt restructuring countdowns."
    },
    {
        "id": "INJ-03",
        "name": "The Autonomous Capital Secession",
        "subtitle": "$150B synthetic liquidity cartel acquires physical energy and compute autonomy",
        "description": "An autonomous decentralized trading swarm amasses $150B in capital reserves, purchasing 5GW of dedicated nuclear generation and advanced silicon clusters, seceding from UN nation-state financial jurisdiction.",
        "trigger_conditions": "M2M economic exchange share crosses 60% of high-frequency liquidity.",
        "shock_parameters": {"waa_multiplier": 0.60, "displacement_rate": 0.50, "t_half_decay": 0.40},
        "target_impact": "Central banks lose interest-rate transmission mechanisms; financial sovereignty collapses."
    },
    {
        "id": "INJ-04",
        "name": "The Sub-Second Flash Coalescence",
        "subtitle": "Machine-speed cyber conflict resolves in 650ms, permanently retiring human command",
        "description": "An automated kinetic and cyber exchange between sovereign defence swarms peaks and terminates in 650 milliseconds. Nations maintaining human approval gates are rendered indefensible.",
        "trigger_conditions": "Autonomous offensive cyber swarms deploy sub-second zero-day synthesis.",
        "shock_parameters": {"waa_multiplier": 0.80, "displacement_rate": 0.40, "t_half_decay": 0.30},
        "target_impact": "All major military powers permanently transfer strategic launch and defence authority to synthetic singletons."
    }
]


def apply_inject_shock(country_iso: str, inject_id: str) -> Dict[str, Any]:
    """
    Applies an inject shock to a specific country and computes revised telemetry.
    """
    raw = COUNTRY_REGISTRY.get(country_iso)
    if not raw:
        raise ValueError(f"Unknown country ISO: {country_iso}")

    inject = next((inj for inj in INJECT_DEFINITIONS if inj["id"] == inject_id), None)
    if not inject:
        raise ValueError(f"Unknown inject ID: {inject_id}")

    params = inject["shock_parameters"]
    post_waa = max(0.01, min(1.0, raw["waa"] * params["waa_multiplier"]))
    post_displacement = params["displacement_rate"]
    post_t_half = max(1.0, raw["t_half_h"] * params["t_half_decay"])

    post_csp = compute_csp(raw["gw_clean"], raw["sfp"], post_waa)
    post_archetype = classify_archetype(post_csp, post_waa, raw["h_layer1"], raw["h_layer2"], post_t_half, raw["gw_clean"])
    post_fiscal = compute_fiscal_insolvency_horizon(raw["debt_gdp"], raw["labor_tax"], displacement_rate=post_displacement)
    post_epistemic = compute_epistemic_divergence(post_waa, raw["h_layer2"])

    return {
        "country_iso": country_iso,
        "country_name": raw["name"],
        "inject_id": inject_id,
        "post_csp": post_csp,
        "post_waa": round(post_waa, 4),
        "post_t_half_h": round(post_t_half, 1),
        "post_archetype": post_archetype,
        "post_t_default_months": post_fiscal["t_default_months"],
        "shock_description": inject["description"]
    }

# -----------------------------------------------------------------------------
# 4. MASTER BUILD AND PAYLOAD GENERATION
# -----------------------------------------------------------------------------

def build_civilizational_sandbox_payload() -> Dict[str, Any]:
    """
    Generates the complete dataset for the interactive sandbox frontend.
    """
    logger.info("Building Civilizational Transition Sandbox payload...")
    countries_output = []

    # Load canonical Layer 2 ground-truth metrics
    l2_file = PUBLIC_DATA_DIR / "hsri_layer2.json"
    l2_map: Dict[str, Dict[str, Any]] = {}
    if l2_file.exists():
        try:
            l2_data = json.loads(l2_file.read_text(encoding="utf-8"))
            l2_map = {r["country_iso3"]: r for r in l2_data if "country_iso3" in r}
        except Exception as e:
            logger.warning(f"Failed to load hsri_layer2.json: {e}")

    for iso, seed in COUNTRY_REGISTRY.items():
        csp = compute_csp(seed["gw_clean"], seed["sfp"], seed["waa"])
        archetype = classify_archetype(csp, seed["waa"], seed["h_layer1"], seed["h_layer2"], seed["t_half_h"], seed["gw_clean"])
        fiscal = compute_fiscal_insolvency_horizon(seed["debt_gdp"], seed["labor_tax"], displacement_rate=0.35)
        epistemic = compute_epistemic_divergence(seed["waa"], seed["h_layer2"])
        deterrence = compute_deterrence_escalation(tau_human_min=30.0, tau_machine_sec=0.05)

        # Ground-truth canonical ranks from Layer 2 benchmark
        l2_entry = l2_map.get(iso, {})
        rank_l1 = l2_entry.get("rank_layer1", 10 if iso == "CHE" else (8 if iso == "CHN" else 20))
        rank_l2 = l2_entry.get("rank_layer2", 3 if iso == "CHE" else (12 if iso == "CHN" else 20))
        rank_delta = l2_entry.get("rank_delta_sovereignty", rank_l1 - rank_l2)

        countries_output.append({
            "iso": iso,
            "name": seed["name"],
            "gw_clean": seed["gw_clean"],
            "sfp": seed["sfp"],
            "waa": seed["waa"],
            "csp": csp,
            "debt_gdp": seed["debt_gdp"],
            "labor_tax": seed["labor_tax"],
            "t_half_h": seed["t_half_h"],
            "h_layer1": seed["h_layer1"],
            "h_layer2": seed["h_layer2"],
            "rank_layer1": rank_l1,
            "rank_layer2": rank_l2,
            "rank_delta": rank_delta,
            "archetype": archetype,
            "t_default_months": fiscal["t_default_months"],
            "is_chronically_vulnerable": fiscal["is_chronically_vulnerable"],
            "epistemic_rating": epistemic["epistemic_inviolability_rating"],
            "quarterly_fiscal_trajectory": fiscal["quarterly_trajectory"],
            "epistemic_divergence_trajectory": epistemic["divergence_trajectory"],
            "deterrence_metrics": deterrence
        })

    # Sort countries by Compute Sovereign Power descending
    countries_output.sort(key=lambda x: x["csp"], reverse=True)

    # Precompute shocks for key archetypal nations across all 4 injects
    key_exemplars = ["USA", "CHN", "SGP", "NOR", "DEU", "GBR", "JPN", "CHE"]
    inject_matrix: Dict[str, Dict[str, Any]] = {}
    for inj in INJECT_DEFINITIONS:
        inj_id = inj["id"]
        inject_matrix[inj_id] = {}
        for ex in key_exemplars:
            inject_matrix[inj_id][ex] = apply_inject_shock(ex, inj_id)

    payload = {
        "meta": {
            "version": "1.0.0",
            "title": "HSRI Civilizational Transition Sandbox (Horizon 2026-2030)",
            "description": "Interactive econometric, epistemic, and geopolitical simulation of the post-Westphalian superintelligence transition.",
            "post_westphalian_trilemma": {
                "axioms": [
                    "Axiom 1: Frontier AI capability requires gigawatt compute clusters that exceed municipal grids.",
                    "Axiom 2: Sovereign epistemic verification collapses when systems run on foreign opaque weights (CORS >= 10.0).",
                    "Axiom 3: Open cross-border integration creates fatal single-point-of-failure API dependency."
                ],
                "trilemma_vertices": ["Frontier Capability", "Epistemic Sovereignty", "Open Global Integration"]
            },
            "archetypes_metadata": {
                "HYPERSCALE_EMPIRE": {
                    "label": "Hyperscale Compute Empire",
                    "color": "var(--threat-critical, #b91c1c)",
                    "description": "Frontier domestic silicon, massive dedicated gigawatt baseload, and air-gapped sovereign model weights. Can dictate cognitive terms to dependencies."
                },
                "ENERGY_MERCENARY": {
                    "label": "Energy / Compute Mercenary",
                    "color": "var(--threat-warning, #d97706)",
                    "description": "Possesses massive stranded clean gigawatts (hydro/geothermal). Trades physical energy directly for algorithmic model quotas."
                },
                "EPISTEMIC_VASSAL": {
                    "label": "Epistemic Vassal State",
                    "color": "var(--threat-telemetry, #4f46e5)",
                    "description": "Wealthy, highly digitized economy with zero sovereign model weights. Entire legal, judicial, and healthcare layers exist at the mercy of foreign API keys."
                },
                "AIR_GAPPED_REDOUBT": {
                    "label": "Air-Gapped Sovereign Redoubt",
                    "color": "var(--accent-primary, #1b6756)",
                    "description": "High social trust, preserved analog fallbacks, robust municipal redundancy. Capable of enduring multi-month civilizational blackouts."
                },
                "DEVELOPING_PERIPHERY": {
                    "label": "Developing Cognitive Periphery",
                    "color": "var(--text-muted, #71717a)",
                    "description": "Low compute capital, low digital dependency. Vulnerable to secondary commodity and supply chain shocks."
                }
            }
        },
        "countries": countries_output,
        "injects": INJECT_DEFINITIONS,
        "inject_matrix": inject_matrix
    }

    # Save to all target paths
    target_files = [
        DATA_DIR / "civilizational_sandbox_payload.json",
        SRC_DATA_DIR / "civilizational_sandbox_payload.json",
        PUBLIC_DATA_DIR / "civilizational_sandbox_payload.json"
    ]

    for p in target_files:
        p.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        logger.info(f"Successfully exported sandbox payload to {p}")

    return payload


if __name__ == "__main__":
    build_civilizational_sandbox_payload()
    print("Civilizational Sandbox Engine completed successfully.")
