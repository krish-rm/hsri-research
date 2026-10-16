"""
hsri_engine.reinsurance — Actuarial Decoupling Pricing & Lloyd's Syndicate Slip Engine
=====================================================================================
Calculates extreme-tail reinsurance pricing, expected civilizational decoupling losses (ECDL),
Solvency II 99.5% 1-Year SCR capital charges, and generates publication-grade Lloyd's Syndicate Slips.

Author: Krishnakumar Radhakrishnan (HSRI Research Consortium)
DOI: 10.5281/zenodo.10842000
"""

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_PROFILES = {
    "archetype_a": {
        "archetype": "archetype_a",
        "name": "Small Open Tech Hub",
        "representative_states": ["Singapore", "Hong Kong", "UAE"],
        "decoupling_half_life_hours": 8.0,
        "v_asi": 0.742,
        "regime": "CATASTROPHIC_COLLAPSE",
        "14_day_cumulative_loss_pct": 94.2,
        "actuarial_risk_loading_factor": 2.096,
        "sovereignty_discount_or_surcharge_pct": 109.6,
        "adjusted_reinsurance_rate_pct": 0.9432,
    },
    "archetype_b": {
        "archetype": "archetype_b",
        "name": "Diversified Continental Power",
        "representative_states": ["United States", "Germany", "Japan", "United Kingdom"],
        "decoupling_half_life_hours": 28.0,
        "v_asi": 0.541,
        "regime": "SEVERE_SYSTEMIC_CONTRACTION",
        "14_day_cumulative_loss_pct": 86.8,
        "actuarial_risk_loading_factor": 1.753,
        "sovereignty_discount_or_surcharge_pct": 75.3,
        "adjusted_reinsurance_rate_pct": 0.7888,
    },
    "archetype_c": {
        "archetype": "archetype_c",
        "name": "High-Trust Air-Gapped State",
        "representative_states": ["Norway", "Finland", "Iceland", "Switzerland"],
        "decoupling_half_life_hours": 336.0,
        "v_asi": 0.184,
        "regime": "CONTROLLED_ANALOG_PLATEAU",
        "14_day_cumulative_loss_pct": 18.4,
        "actuarial_risk_loading_factor": 0.35,
        "sovereignty_discount_or_surcharge_pct": -65.0,
        "adjusted_reinsurance_rate_pct": 0.1575,
    }
}

UNDERWRITING_GUIDELINES = [
    {
        "rule": "Mandatory Air-Gap Warranty Clause",
        "condition": "T_half < 24 Hours",
        "mandate": "Cedent must deploy hardware-enforced manual air-gap interlocks on SCADA and power switches (Market Clause L2-DEC-01)."
    },
    {
        "rule": "Sovereignty Floor Maintenance",
        "condition": "Layer 2 Score < 0.35",
        "mandate": "Minimum statutory capital loading surcharge +75% applied to unbacked digital liabilities."
    },
    {
        "rule": "Verification Latency Cap",
        "condition": "CORS >= 8.0 (Recursive Horizon)",
        "mandate": "Autonomous AI agent transaction limits capped at $50,000 USD without dual-human cryptographic authorization."
    }
]


def load_reinsurance_data(repo_root: Optional[Path] = None) -> Dict[str, Any]:
    """Load institutional reinsurance profiles and guidelines."""
    search_paths = []
    if repo_root:
        search_paths.extend([
            repo_root / "data" / "telemetry" / "reinsurance_risk_profiles.json",
            repo_root / "site-astro" / "src" / "data" / "reinsurance_risk_profiles.json"
        ])
    
    # Defaults based on module location
    here = Path(__file__).resolve().parent
    search_paths.extend([
        here.parent / "data" / "telemetry" / "reinsurance_risk_profiles.json",
        here.parent / "site-astro" / "src" / "data" / "reinsurance_risk_profiles.json"
    ])

    for p in search_paths:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

    return {
        "metadata": {
            "annual_catastrophic_decoupling_probability": 0.1728,
            "cors_oversight_scale": 10.0,
            "author": "Krishnakumar Radhakrishnan"
        },
        "profiles": DEFAULT_PROFILES,
        "underwriting_guidelines": UNDERWRITING_GUIDELINES
    }


def normalize_archetype_key(key: str) -> str:
    """Normalize 'A', 'archetype_a', 'tech-hub', etc. to standard key."""
    cleaned = key.strip().lower()
    if cleaned in ["a", "archetype_a", "tech_hub", "singapore", "sgp"]:
        return "archetype_a"
    if cleaned in ["b", "archetype_b", "continental", "usa", "us"]:
        return "archetype_b"
    if cleaned in ["c", "archetype_c", "resilient", "nordic", "nor"]:
        return "archetype_c"
    return cleaned


def calculate_reinsurance_pricing(
    archetype_key: str,
    tiv_billion: float = 10.0,
    repo_root: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Calculate Solvency II / NAIC RBC reinsurance pricing metrics.
    
    tiv_billion: Total Insured Valuation in USD Billion (e.g. 10.0 = $10B).
    """
    data = load_reinsurance_data(repo_root)
    norm_key = normalize_archetype_key(archetype_key)
    
    profiles = data.get("profiles", DEFAULT_PROFILES)
    if norm_key not in profiles:
        raise ValueError(f"Unknown archetype '{archetype_key}'. Valid options: A, B, C.")

    prof = profiles[norm_key]
    annual_prob = data.get("metadata", {}).get("annual_catastrophic_decoupling_probability", 0.1728)

    gross_loss_pct = prof["14_day_cumulative_loss_pct"] / 100.0
    gross_loss_billion = round(tiv_billion * gross_loss_pct, 4)
    ecdl_billion = round(gross_loss_billion * annual_prob, 4)
    risk_loading = prof["actuarial_risk_loading_factor"]
    adj_rate_pct = prof["adjusted_reinsurance_rate_pct"]
    annual_premium_million = round(tiv_billion * 1000.0 * (adj_rate_pct / 100.0), 2)
    solvency_capital_billion = round(gross_loss_billion * 0.42 * math.sqrt(risk_loading), 4)

    return {
        "archetype_key": norm_key,
        "archetype_name": prof["name"],
        "representative_states": prof["representative_states"],
        "tiv_billion_usd": tiv_billion,
        "decoupling_half_life_hours": prof["decoupling_half_life_hours"],
        "regime": prof["regime"],
        "annual_decoupling_probability": annual_prob,
        "14_day_cumulative_loss_pct": prof["14_day_cumulative_loss_pct"],
        "gross_loss_billion_usd": gross_loss_billion,
        "expected_civilizational_decoupling_loss_billion_usd": ecdl_billion,
        "actuarial_risk_loading_factor_phi": risk_loading,
        "sovereignty_discount_or_surcharge_pct": prof["sovereignty_discount_or_surcharge_pct"],
        "adjusted_reinsurance_rate_pct": adj_rate_pct,
        "annual_premium_million_usd": annual_premium_million,
        "solvency_ii_99_5_capital_charge_billion_usd": solvency_capital_billion,
        "underwriting_guidelines": data.get("underwriting_guidelines", UNDERWRITING_GUIDELINES)
    }


def generate_syndicate_slip_markdown(pricing: Dict[str, Any]) -> str:
    """Generate official Lloyd's Syndicate Placement Slip & Treaty Term Sheet Markdown."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    arch_name = pricing["archetype_name"]
    states = ", ".join(pricing["representative_states"])
    tiv = pricing["tiv_billion_usd"]
    t_half = pricing["decoupling_half_life_hours"]
    regime = pricing["regime"]
    loss_pct = pricing["14_day_cumulative_loss_pct"]
    gross_loss = pricing["gross_loss_billion_usd"]
    p_dec = pricing["annual_decoupling_probability"] * 100.0
    ecdl = pricing["expected_civilizational_decoupling_loss_billion_usd"]
    phi = pricing["actuarial_risk_loading_factor_phi"]
    surcharge = pricing["sovereignty_discount_or_surcharge_pct"]
    surcharge_str = f"+{surcharge}% High-Compute Trap Surcharge" if surcharge > 0 else f"{surcharge}% Resilient Sovereignty Credit"
    rate_pct = pricing["adjusted_reinsurance_rate_pct"]
    premium = pricing["annual_premium_million_usd"]
    scr = pricing["solvency_ii_99_5_capital_charge_billion_usd"]

    md = f"""# LLOYD'S SYNDICATE PLACEMENT SLIP & TREATY TERM SHEET
## Catastrophic Civilizational Decoupling Reinsurance Facility (CCDR-2026)

> **Document Type:** Non-Proportional Excess of Loss / Extreme Catastrophe Syndicate Slip (Draft)  
> **Permanent Research Baseline:** HSRI Research Consortium · DOI: [10.5281/zenodo.10842000](https://doi.org/10.5281/zenodo.10842000)  
> **Lead Model PI:** Krishnakumar Radhakrishnan  
> **Pricing Date:** {today}  
> **Compliance Standard:** Solvency II (Directive 2009/138/EC) Art 101 / NAIC RBC 99.5% 1-Year VaR  

---

### 1. SUMMARY OF RISK & CEDENT PROFILE

| Parameter | Placement Value | Actuarial Reference |
|---|---|---|
| **Sovereign Risk Archetype** | {arch_name} | HSRI Layer 2 Sovereign Archetype Taxonomy |
| **Representative Jurisdictions** | {states} | Sovereign Cloud Risk Database |
| **Total Insured Valuation (TIV)** | $USD {tiv} Billion | Primary critical digital & power infrastructure assets |
| **Decoupling Half-Life ($T_{{\text{{half}}}}$)** | {t_half} Hours | Time to 50% critical infrastructure function loss |
| **Systemic Risk Regime** | {regime} | Post-severance analog reversion capacity |
| **14-Day Cumulative Loss Rate** | {loss_pct}% | Leontief weakest-link cascade model |
| **Gross Catastrophic Loss (14-Day)** | $USD {gross_loss} Billion | TIV x Gross Loss Rate |

---

### 2. ACTUARIAL PRICING & TREATY RATINGS

| Metric | Syndicate Rating | Model Methodology |
|---|---|---|
| **Annual Decoupling Probability P(Decoupling)** | {p_dec:.1f}% / year | Global telemetric precursor seismograph (CORS 10.0) |
| **Expected Annual Decoupling Loss (ECDL)** | $USD {ecdl} Billion | P(Decoupling) x Gross 14-Day Loss |
| **HSRI Risk Loading Factor ($\\Phi$)** | **{phi}x** | Frechet extreme value tail index & Choquet capacity |
| **Sovereign Posture Surcharge / Discount** | {surcharge_str} | Layer 1/2 decoupling sensitivity ratio |
| **Indicative Reinsurance Treaty Rate** | **{rate_pct}%** | Technical premium rate on total facility size |
| **Annual Treaty Premium** | **$USD {premium} Million** | Technical annual cedent premium commitment |
| **Solvency II 99.5% SCR Capital Charge** | **$USD {scr} Billion** | Regulatory capital requirement (0.42 x Loss x sqrt(Phi)) |

---

### 3. STATUTORY UNDERWRITING MANDATES & CONDITIONS PRECEDENT

"""
    for idx, g in enumerate(pricing.get("underwriting_guidelines", [])):
        md += f"""#### Condition {idx + 1}: {g['rule']}
- **Trigger / Threshold:** `{g['condition']}`
- **Syndicate Mandate:** {g['mandate']}

"""

    md += """---

### 4. MANDATORY REGULATORY & ACTUARIAL DISCLAIMER

> [!IMPORTANT]
> **STATUTORY DISCLAIMER (SOLVENCY II / NAIC RBC):**  
> This placement slip and technical term sheet is generated by the HSRI Catastrophic Decoupling Reinsurance Risk Engine for academic, research, and institutional decision-support purposes only. It does not constitute a formal insurance binder, firm quotation, or statutory actuarial certification.
> 
> In accordance with EU Solvency II (Directive 2009/138/EC) Article 101, EIOPA Technical Specifications, and NAIC Risk-Based Capital guidelines, formal treaty execution and Solvency Capital Requirement (SCR) internal model filings require formal actuarial review, validation, and sign-off by a qualified Fellow of the Institute and Faculty of Actuaries (FIA), Fellow of the Casualty Actuarial Society (FCAS), or equivalent certifying jurisdiction actuary.

---
*Slip Generated by HSRI Reinsurance Actuarial Risk Engine · Permanent Citation DOI: [10.5281/zenodo.10842000](https://doi.org/10.5281/zenodo.10842000)*
"""
    return md
