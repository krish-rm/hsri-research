"""
tests/test_civilizational_sandbox.py - Test suite for Civilizational Transition Sandbox
"""
import json
import pytest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_ROOT / "scripts"))

import civilizational_sandbox_engine as cse

SRC_PAYLOAD = REPO_ROOT / "site-astro" / "src" / "data" / "civilizational_sandbox_payload.json"
PUB_PAYLOAD = REPO_ROOT / "site-astro" / "public" / "data" / "civilizational_sandbox_payload.json"
DATA_PAYLOAD = REPO_ROOT / "data" / "civilizational_sandbox_payload.json"


def test_payload_files_exist_and_match():
    assert DATA_PAYLOAD.exists(), "data/ payload missing"
    assert SRC_PAYLOAD.exists(), "site-astro/src/data payload missing"
    assert PUB_PAYLOAD.exists(), "site-astro/public/data payload missing"

    data_payload = json.loads(DATA_PAYLOAD.read_text(encoding="utf-8"))
    src_payload = json.loads(SRC_PAYLOAD.read_text(encoding="utf-8"))
    pub_payload = json.loads(PUB_PAYLOAD.read_text(encoding="utf-8"))

    assert data_payload == src_payload, "Data and Source payloads must be identical"
    assert src_payload == pub_payload, "Source and Public payloads must be identical"
    assert "countries" in src_payload
    assert len(src_payload["countries"]) >= 39
    assert len(src_payload["injects"]) == 4


def test_csp_bounds_and_hegemony():
    # Test boundary limits
    zero_csp = cse.compute_csp(gw_clean=0.0, sfp=0.0, waa=0.0)
    assert zero_csp == 0.01

    max_csp = cse.compute_csp(gw_clean=50.0, sfp=1.0, waa=1.0)
    assert 0.90 <= max_csp <= 1.0

    # Real country checks: USA and CHN must have higher CSP than SGP and GBR
    csp_usa = cse.compute_csp(45.0, 0.95, 0.98)
    csp_sgp = cse.compute_csp(1.0, 0.45, 0.08)
    assert csp_usa > 0.70
    assert csp_sgp < 0.15
    assert csp_usa > csp_sgp * 5.0


def test_archetype_classification():
    arch_usa = cse.classify_archetype(csp=0.85, waa=0.98, h_layer1=0.85, h_layer2=0.30, t_half_h=14, gw_clean=45.0)
    assert arch_usa == "HYPERSCALE_EMPIRE"

    arch_sgp = cse.classify_archetype(csp=0.04, waa=0.08, h_layer1=0.85, h_layer2=0.11, t_half_h=4, gw_clean=1.0)
    assert arch_sgp == "EPISTEMIC_VASSAL"

    arch_nor = cse.classify_archetype(csp=0.35, waa=0.45, h_layer1=0.81, h_layer2=0.51, t_half_h=1440, gw_clean=8.5)
    assert arch_nor == "ENERGY_MERCENARY"

    arch_che = cse.classify_archetype(csp=0.32, waa=0.55, h_layer1=0.79, h_layer2=0.46, t_half_h=1200, gw_clean=4.5)
    assert arch_che == "AIR_GAPPED_REDOUBT"


def test_fiscal_insolvency_horizon():
    # Test moderate vs aggressive displacement on high debt nation (e.g. Japan-like)
    base_res = cse.compute_fiscal_insolvency_horizon(debt_gdp=2.6, labor_tax=0.42, displacement_rate=0.35)
    shock_res = cse.compute_fiscal_insolvency_horizon(debt_gdp=2.6, labor_tax=0.42, displacement_rate=0.70)

    assert base_res["t_default_months"] is not None
    assert shock_res["t_default_months"] is not None
    # Accelerated displacement must trigger earlier default
    assert shock_res["t_default_months"] <= base_res["t_default_months"]
    assert len(base_res["quarterly_trajectory"]) == 21  # months 0 through 60 step 3


def test_epistemic_divergence_metrics():
    # Sovereign weights (waa=0.95) should have significantly lower divergence than vassal (waa=0.10)
    sovereign_ep = cse.compute_epistemic_divergence(waa=0.95, h_layer2=0.50, months=48)
    vassal_ep = cse.compute_epistemic_divergence(waa=0.10, h_layer2=0.20, months=48)

    sovereign_dkl_final = sovereign_ep["divergence_trajectory"][-1]["d_kl"]
    vassal_dkl_final = vassal_ep["divergence_trajectory"][-1]["d_kl"]

    assert sovereign_dkl_final < vassal_dkl_final
    assert sovereign_ep["epistemic_inviolability_rating"] > vassal_ep["epistemic_inviolability_rating"]


def test_deterrence_mandatory_delegation():
    ret = cse.compute_deterrence_escalation(tau_human_min=30.0, tau_machine_sec=0.01)
    assert ret["speed_asymmetry_ratio"] == 180000.0  # (30 * 60) / 0.01
    assert ret["delegation_probability_pct"] >= 95.0
    assert ret["command_verdict"] == "HUMAN_COMMAND_SURRENDERED"


def test_all_injects_apply_cleanly():
    for inj in cse.INJECT_DEFINITIONS:
        inj_id = inj["id"]
        shock_usa = cse.apply_inject_shock("USA", inj_id)
        shock_sgp = cse.apply_inject_shock("SGP", inj_id)
        assert shock_usa["inject_id"] == inj_id
        assert shock_sgp["inject_id"] == inj_id
        assert shock_sgp["post_csp"] >= 0.0
        assert shock_usa["post_csp"] >= 0.0

