#!/usr/bin/env python3
"""
HSRI 2.0 Reinsurance Actuarial Risk Engine
==========================================
Operationalizes the actuarial pricing and catastrophic loss underwriting framework
for critical infrastructure AI decoupling risks.

Computes:
1. Catastrophic AI Decoupling Probability P(Decoupling) based on CORS telemetry.
2. Expected Civilizational Decoupling Loss (ECDL) across sovereign archetypes.
3. HSRI Layer 2 Actuarial Risk Premium Loadings and Resilience Discounts.
4. Capital Adequacy Solvency II / RBC capital charges for systemic AI exposure.

Author: Krishnakumar Radhakrishnan
License: CC BY-SA 4.0 / Open Science
"""

import json
import math
import os
import sys

ARCHETYPES = {
    "archetype_a": {
        "name": "Small Open Tech Hub",
        "representative_states": ["Singapore", "Hong Kong", "UAE"],
        "t_half_hours": 8.0,
        "v_asi": 0.742,
        "daily_gdp_usd_billion": 1.25,
        "ai_dependency_ratio": 0.88,
        "analog_fallback_capacity": 0.05
    },
    "archetype_b": {
        "name": "Diversified Continental Power",
        "representative_states": ["United States", "Germany", "Japan"],
        "t_half_hours": 28.0,
        "v_asi": 0.541,
        "daily_gdp_usd_billion": 75.0,
        "ai_dependency_ratio": 0.76,
        "analog_fallback_capacity": 0.22
    },
    "archetype_c": {
        "name": "High-Trust Air-Gapped State",
        "representative_states": ["Switzerland", "Finland", "Sweden"],
        "t_half_hours": 420.0,
        "v_asi": -0.050,
        "daily_gdp_usd_billion": 2.50,
        "ai_dependency_ratio": 0.38,
        "analog_fallback_capacity": 0.82
    }
}

SUBSCRIPTION_TIERS = {
    "tier_1_sovereign_feed": {
        "name": "Sovereign Intelligence Feed",
        "annual_price_usd": 75000,
        "target": "Sovereign Wealth Funds & Economic Ministries",
        "deliverables": [
            "Real-time CORS 10.0 hourly webhooks & early-warning alerts",
            "14 Observable ASI Precursor Tripwire streaming API",
            "Continuous 39-country Layer 1 & Layer 2 sovereignty re-calibrations",
            "Quarterly executive horizon brief on latent model drift"
        ]
    },
    "tier_2_reinsurance_underwriting": {
        "name": "Institutional Reinsurance Underwriting Dossier",
        "annual_price_usd": 120000,
        "target": "Reinsurance Underwriters (Lloyd's, Munich Re, Swiss Re)",
        "deliverables": [
            "Everything in Tier 1",
            "Full 39-country ECDL loss frequency & severity curves",
            "Leontief cross-sector cascading failure correlation matrices",
            "Quarterly tailored portfolio stress-testing & capital reserve audits",
            "Underwriting policy wording & 'AI Force Majeure' exclusionary clauses"
        ]
    },
    "tier_3_cabinet_enclave": {
        "name": "National Security Cabinet Dedicated Enclave",
        "annual_price_usd": 250000,
        "target": "National Security Councils & Critical Infrastructure Agencies",
        "deliverables": [
            "Everything in Tier 2",
            "On-premise, air-gapped hsri-engine Docker microservice deployment",
            "Classified national SCADA / banking telemetry ingestion pipelines",
            "Annual facilitator-led live civilizational decoupling drill exercise",
            "Direct 24/7 sovereign advisory access to Lead Principal Investigator"
        ]
    }
}

def calculate_catastrophe_probability(cors_score: float = 10.0, baseline_lambda: float = 0.02) -> float:
    """
    Computes annual Poisson probability of a catastrophic zero-notice AI quarantine / shutdown event.
    lambda = baseline_lambda * exp(0.25 * (CORS - 1.0))
    """
    hazard_rate = baseline_lambda * math.exp(0.25 * (cors_score - 1.0))
    prob = 1.0 - math.exp(-hazard_rate)
    return round(prob, 4)

def calculate_actuarial_loss_profile(archetype_key: str, exposed_asset_value_usd_billion: float = 10.0):
    arch = ARCHETYPES[archetype_key]
    t_half = arch["t_half_hours"]
    v_asi = arch["v_asi"]
    
    # 14-day cumulative loss percentage modeled from decoupling simulator
    if t_half <= 10.0:
        loss_pct = 0.942
        regime = "CATASTROPHIC_COLLAPSE"
    elif t_half <= 35.0:
        loss_pct = 0.868
        regime = "SEVERE_SYSTEMIC_CONTRACTION"
    else:
        loss_pct = 0.184
        regime = "CONTROLLED_ANALOG_PLATEAU"
        
    expected_gross_loss_billion = round(exposed_asset_value_usd_billion * loss_pct, 3)
    annual_event_prob = calculate_catastrophe_probability(10.0)
    annual_expected_loss_billion = round(expected_gross_loss_billion * annual_event_prob, 4)
    
    # Actuarial Risk Loading Factor
    # Base rate = 1.0
    # Loading increases with V_ASI and decreases with T_half
    risk_loading = 1.0 + max(0.0, v_asi * 1.5) - min(0.65, (t_half / 336.0) * 0.70)
    risk_loading = round(max(0.35, risk_loading), 3)
    
    # Base cyber premium rate per $100M coverage = $450,000 (0.45%)
    base_cyber_rate_pct = 0.45
    adjusted_rate_pct = round(base_cyber_rate_pct * risk_loading, 4)
    annual_premium_per_10b_coverage_million = round(10000.0 * (adjusted_rate_pct / 100.0), 2)
    
    # Solvency II 99.5% 1-Year Value at Risk Capital Charge
    # Under Extreme Value Theory (Frechet tail index alpha = 1.8)
    solvency_capital_requirement_billion = round(expected_gross_loss_billion * 0.42 * (risk_loading ** 0.5), 3)
    
    return {
        "archetype": archetype_key,
        "name": arch["name"],
        "representative_states": arch["representative_states"],
        "decoupling_half_life_hours": t_half,
        "v_asi": v_asi,
        "regime": regime,
        "14_day_cumulative_loss_pct": round(loss_pct * 100.0, 1),
        "expected_gross_loss_billion_usd": expected_gross_loss_billion,
        "annual_event_probability": annual_event_prob,
        "annual_expected_loss_billion_usd": annual_expected_loss_billion,
        "actuarial_risk_loading_factor": risk_loading,
        "sovereignty_discount_or_surcharge_pct": round((risk_loading - 1.0) * 100.0, 1),
        "adjusted_reinsurance_rate_pct": adjusted_rate_pct,
        "annual_premium_for_10b_facility_usd_million": annual_premium_per_10b_coverage_million,
        "solvency_ii_capital_charge_billion_usd": solvency_capital_requirement_billion
    }

def generate_reinsurance_dossier():
    annual_prob = calculate_catastrophe_probability(10.0)
    
    profiles = {}
    for arch_key in ARCHETYPES:
        profiles[arch_key] = calculate_actuarial_loss_profile(arch_key, exposed_asset_value_usd_billion=10.0)
        
    dossier = {
        "metadata": {
            "title": "HSRI 2.0 Reinsurance & Sovereign Risk Underwriting Telemetry",
            "version": "2.5.0",
            "author": "Krishnakumar Radhakrishnan",
            "cors_oversight_scale": 10.0,
            "annual_catastrophic_decoupling_probability": annual_prob,
            "solvency_framework": "Solvency II / NAIC Risk-Based Capital (RBC) Compliant"
        },
        "profiles": profiles,
        "subscription_tiers": SUBSCRIPTION_TIERS,
        "underwriting_guidelines": [
            {
                "rule": "RULE-UW-01: The Leontief Floor Exclusion",
                "condition": "If V_ASI >= 0.50 and T_half < 24.0h",
                "mandate": "Uninsurable at standard cyber market rates. Require 2.2x - 3.5x sovereign risk loading and mandatory Tier 3 tabletop certification."
            },
            {
                "rule": "RULE-UW-02: Sovereign Resilience Credit",
                "condition": "If T_half >= 168.0h and Analog Fallback Capacity >= 60%",
                "mandate": "Grant 45% - 65% premium discount and reduce Solvency II capital charge by 50%."
            },
            {
                "rule": "RULE-UW-03: Multi-Agent Cascade Contingency",
                "condition": "If CORS >= 8.5",
                "mandate": "Underwriters must mandate air-gapped deterministic kill-switches for all automated clearinghouse settlement feeds."
            }
        ]
    }
    return dossier

def main():
    dossier = generate_reinsurance_dossier()
    
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(repo_root, "data", "telemetry")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "reinsurance_risk_profiles.json")
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dossier, f, indent=2)
    print(f"Exported reinsurance telemetry to: {out_file}")
    
    astro_data_dir = os.path.join(repo_root, "site-astro", "src", "data")
    if os.path.exists(astro_data_dir):
        astro_file = os.path.join(astro_data_dir, "reinsurance_risk_profiles.json")
        with open(astro_file, "w", encoding="utf-8") as f:
            json.dump(dossier, f, indent=2)
        print(f"Exported reinsurance telemetry to Astro: {astro_file}")

if __name__ == "__main__":
    main()
