import os
import json
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def test_actuarial_telemetry_json_integrity():
    telemetry_path = os.path.join(REPO_ROOT, "data", "telemetry", "reinsurance_risk_profiles.json")
    astro_path = os.path.join(REPO_ROOT, "site-astro", "src", "data", "reinsurance_risk_profiles.json")
    
    assert os.path.exists(telemetry_path), f"Missing {telemetry_path}"
    assert os.path.exists(astro_path), f"Missing {astro_path}"
    
    with open(telemetry_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    meta = data.get("metadata", {})
    assert meta.get("author") == "Krishnakumar Radhakrishnan"
    assert meta.get("cors_oversight_scale") == 10.0
    assert 0.10 <= meta.get("annual_catastrophic_decoupling_probability", 0) <= 0.25
    
    profiles = data.get("profiles", {})
    for key in ["archetype_a", "archetype_b", "archetype_c"]:
        assert key in profiles, f"Missing archetype {key}"
        prof = profiles[key]
        assert "decoupling_half_life_hours" in prof
        assert "14_day_cumulative_loss_pct" in prof
        assert "actuarial_risk_loading_factor" in prof
        assert "solvency_ii_capital_charge_billion_usd" in prof

def test_actuarial_pricing_monotonicity_and_discount():
    telemetry_path = os.path.join(REPO_ROOT, "data", "telemetry", "reinsurance_risk_profiles.json")
    with open(telemetry_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    p_a = data["profiles"]["archetype_a"]
    p_b = data["profiles"]["archetype_b"]
    p_c = data["profiles"]["archetype_c"]
    
    # Loss percentage ordering: A > B > C
    assert p_a["14_day_cumulative_loss_pct"] > p_b["14_day_cumulative_loss_pct"] > p_c["14_day_cumulative_loss_pct"]
    assert p_a["14_day_cumulative_loss_pct"] >= 90.0
    assert p_c["14_day_cumulative_loss_pct"] <= 25.0
    
    # Risk loading factor: A has surcharge > 1.8x, B has surcharge > 1.4x, C has discount < 0.6x
    assert p_a["actuarial_risk_loading_factor"] > p_b["actuarial_risk_loading_factor"] > p_c["actuarial_risk_loading_factor"]
    assert p_a["actuarial_risk_loading_factor"] >= 1.8
    assert p_c["actuarial_risk_loading_factor"] <= 0.50
    assert p_c["sovereignty_discount_or_surcharge_pct"] < 0  # True discount
    
    # Solvency II capital requirement: A > B > C
    assert p_a["solvency_ii_capital_charge_billion_usd"] > p_b["solvency_ii_capital_charge_billion_usd"] > p_c["solvency_ii_capital_charge_billion_usd"]

def test_subscription_tiers_structure():
    telemetry_path = os.path.join(REPO_ROOT, "data", "telemetry", "reinsurance_risk_profiles.json")
    with open(telemetry_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    tiers = data.get("subscription_tiers", {})
    assert "tier_1_sovereign_feed" in tiers
    assert "tier_2_reinsurance_underwriting" in tiers
    assert "tier_3_cabinet_enclave" in tiers
    
    assert tiers["tier_1_sovereign_feed"]["annual_price_usd"] == 75000
    assert tiers["tier_2_reinsurance_underwriting"]["annual_price_usd"] == 120000
    assert tiers["tier_3_cabinet_enclave"]["annual_price_usd"] == 250000
    
    for t in tiers.values():
        assert len(t.get("deliverables", [])) >= 4

def test_framework_and_offering_documents():
    fw_path = os.path.join(REPO_ROOT, "research", "reinsurance", "actuarial_underwriting_framework.md")
    off_path = os.path.join(REPO_ROOT, "research", "reinsurance", "sovereign_reinsurance_offering.md")
    
    assert os.path.exists(fw_path), f"Missing {fw_path}"
    assert os.path.exists(off_path), f"Missing {off_path}"
    
    with open(fw_path, "r", encoding="utf-8") as f:
        fw_text = f.read()
    with open(off_path, "r", encoding="utf-8") as f:
        off_text = f.read()
        
    assert "Krishnakumar Radhakrishnan" in fw_text
    assert "Krishnakumar Radhakrishnan" in off_text
    assert "Solvency II" in fw_text
    assert "Clause L2-DEC-01" in fw_text
    assert "$75,000" in off_text
    assert "$120,000" in off_text
    assert "$250,000" in off_text
    assert "10.5281/zenodo.23441742" in fw_text

def test_annual_report_2027_integrity():
    report_path = os.path.join(REPO_ROOT, "reports", "annual_report_2027.md")
    assert os.path.exists(report_path), f"Missing {report_path}"
    
    with open(report_path, "r", encoding="utf-8") as f:
        rep_text = f.read()
        
    assert "Krishnakumar Radhakrishnan" in rep_text
    assert "The HSRI 2027 State of Human Sovereignty & ASI Precursor Report" in rep_text
    assert "Dual-Layer Architecture" in rep_text
    assert "CORS 10.0" in rep_text
    assert "Leontief Minimum Floor" in rep_text
    assert "High-Compute Vulnerability Trap" in rep_text
    assert "10.5281/zenodo.23441742" in rep_text


def test_reinsurance_calculator_syndicate_slip_export():
    """Verify Sprint 38 Lloyd's Syndicate Slip and term sheet export feature."""
    calc_path = os.path.join(REPO_ROOT, "site-astro", "src", "components", "ReinsurancePricingCalculator.svelte")
    assert os.path.exists(calc_path), f"Missing {calc_path}"
    
    with open(calc_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    assert "exportSyndicateSlip" in text
    assert "LLOYD'S SYNDICATE PLACEMENT SLIP" in text
    assert "Solvency II" in text
    assert "HSRI Research Consortium" in text
    assert "10.5281/zenodo.23441742" in text
    assert "HSRI Risk Loading Factor" in text
    assert "syndicate-action-bar" in text
    assert "export-slip-btn" in text
