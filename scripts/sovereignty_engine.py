#!/usr/bin/env python3
"""
sovereignty_engine.py - HSRI 2.0 Dual-Layer Sovereignty Engine (Sprint 27)

Implements:
1. Layer 1 (Adoption Baseline, P1-P4): Frozen OECD/JRC linear composite.
2. Layer 2 (ASI Sovereignty Layer, P5-P8):
   - P5: Epistemic Inviolability (VSR & Persuasion Resilience)
   - P6: Civilizational Decoupling Half-Life (T_half via min operator across critical infrastructure)
   - P7: Multipolar Coordination Velocity (V_coord)
   - P8: Post-Labor Institutional Elasticity (PLIE)
   - Aggregated via Leontief Weakest-Link Floor (beta=0.5):
     H_Layer2 = ( min_{j} P_j )^0.5 * ( 0.25 * sum_{j} P_j )^0.5
3. Master ASI Vulnerability Index:
   V_ASI = H_Layer1 - H_Layer2
4. National Rank Shifts:
   Delta Rank = Rank_Layer1 - Rank_Layer2 (positive = rank collapse under sovereignty)
5. High-Compute Vulnerability Trap Detection:
   Identifies nations where V_ASI >= 0.25 and Digital Infrastructure P4 >= 0.70.
6. B=1,000 Dirichlet Monte Carlo Sensitivity Audit on Layer 2 weights.
7. Synced Artifact Export to data/ and site-astro/
"""

import sys
from pathlib import Path
import json
import logging
import numpy as np
import pandas as pd
from scipy import stats

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
SITE_ASTRO_DIR = REPO_ROOT / "site-astro"
PUBLIC_DATA_DIR = SITE_ASTRO_DIR / "public" / "data"
SRC_DATA_DIR = SITE_ASTRO_DIR / "src" / "data"

sys.path.append(str(REPO_ROOT / "scripts"))
import dual_layer_formalization as dlf

# -----------------------------------------------------------------------------
# 1. 39-NATION EMPIRICAL SEED TELEMETRY MATRIX FOR LAYER 2 (P5 - P8)
# -----------------------------------------------------------------------------

LAYER2_SEED_DATA = {
    # Nordic Resilient Decentralizers
    "DNK": {"vsr": 0.88, "rho_persuade": 0.92, "t_energy": 1800, "t_finance": 1440, "t_logistics": 1200, "t_info": 1500, "tau_modify": 180, "tau_verify": 240, "gini_compute": 0.38, "safety_net": 0.94, "labor_tax": 0.48},
    "FIN": {"vsr": 0.89, "rho_persuade": 0.94, "t_energy": 2160, "t_finance": 1600, "t_logistics": 1440, "t_info": 1800, "tau_modify": 190, "tau_verify": 240, "gini_compute": 0.36, "safety_net": 0.95, "labor_tax": 0.46},
    "NOR": {"vsr": 0.87, "rho_persuade": 0.91, "t_energy": 2880, "t_finance": 1800, "t_logistics": 1440, "t_info": 2160, "tau_modify": 200, "tau_verify": 250, "gini_compute": 0.32, "safety_net": 0.96, "labor_tax": 0.40},
    "SWE": {"vsr": 0.85, "rho_persuade": 0.90, "t_energy": 2000, "t_finance": 1200, "t_logistics": 1200, "t_info": 1500, "tau_modify": 170, "tau_verify": 240, "gini_compute": 0.42, "safety_net": 0.92, "labor_tax": 0.49},
    "ISL": {"vsr": 0.86, "rho_persuade": 0.88, "t_energy": 2880, "t_finance": 1000, "t_logistics": 960, "t_info": 1200, "tau_modify": 160, "tau_verify": 220, "gini_compute": 0.35, "safety_net": 0.90, "labor_tax": 0.42},

    # Continental European Balanced Economies
    "DEU": {"vsr": 0.78, "rho_persuade": 0.85, "t_energy": 720, "t_finance": 480, "t_logistics": 500, "t_info": 600, "tau_modify": 160, "tau_verify": 240, "gini_compute": 0.45, "safety_net": 0.88, "labor_tax": 0.52},
    "AUT": {"vsr": 0.79, "rho_persuade": 0.86, "t_energy": 1200, "t_finance": 600, "t_logistics": 650, "t_info": 700, "tau_modify": 170, "tau_verify": 240, "gini_compute": 0.40, "safety_net": 0.89, "labor_tax": 0.51},
    "NLD": {"vsr": 0.80, "rho_persuade": 0.86, "t_energy": 600, "t_finance": 360, "t_logistics": 400, "t_info": 500, "tau_modify": 150, "tau_verify": 240, "gini_compute": 0.48, "safety_net": 0.86, "labor_tax": 0.48},
    "FRA": {"vsr": 0.74, "rho_persuade": 0.82, "t_energy": 960, "t_finance": 360, "t_logistics": 420, "t_info": 500, "tau_modify": 140, "tau_verify": 240, "gini_compute": 0.49, "safety_net": 0.87, "labor_tax": 0.53},
    "BEL": {"vsr": 0.72, "rho_persuade": 0.80, "t_energy": 550, "t_finance": 300, "t_logistics": 350, "t_info": 450, "tau_modify": 140, "tau_verify": 240, "gini_compute": 0.46, "safety_net": 0.85, "labor_tax": 0.54},
    "LUX": {"vsr": 0.76, "rho_persuade": 0.84, "t_energy": 360, "t_finance": 180, "t_logistics": 240, "t_info": 300, "tau_modify": 130, "tau_verify": 240, "gini_compute": 0.52, "safety_net": 0.88, "labor_tax": 0.45},
    "IRL": {"vsr": 0.75, "rho_persuade": 0.82, "t_energy": 400, "t_finance": 200, "t_logistics": 250, "t_info": 300, "tau_modify": 130, "tau_verify": 240, "gini_compute": 0.55, "safety_net": 0.82, "labor_tax": 0.44},
    "CHE": {"vsr": 0.84, "rho_persuade": 0.90, "t_energy": 2400, "t_finance": 1200, "t_logistics": 1440, "t_info": 1800, "tau_modify": 190, "tau_verify": 240, "gini_compute": 0.42, "safety_net": 0.88, "labor_tax": 0.38},

    # Anglo-Saxon & Market Economies
    "GBR": {"vsr": 0.65, "rho_persuade": 0.74, "t_energy": 360, "t_finance": 120, "t_logistics": 168, "t_info": 240, "tau_modify": 110, "tau_verify": 260, "gini_compute": 0.62, "safety_net": 0.76, "labor_tax": 0.46},
    "USA": {"vsr": 0.58, "rho_persuade": 0.68, "t_energy": 240, "t_finance": 72, "t_logistics": 120, "t_info": 168, "tau_modify": 90, "tau_verify": 280, "gini_compute": 0.74, "safety_net": 0.64, "labor_tax": 0.42},
    "CAN": {"vsr": 0.72, "rho_persuade": 0.80, "t_energy": 600, "t_finance": 240, "t_logistics": 280, "t_info": 360, "tau_modify": 130, "tau_verify": 250, "gini_compute": 0.58, "safety_net": 0.80, "labor_tax": 0.45},
    "AUS": {"vsr": 0.71, "rho_persuade": 0.79, "t_energy": 520, "t_finance": 220, "t_logistics": 260, "t_info": 340, "tau_modify": 125, "tau_verify": 250, "gini_compute": 0.55, "safety_net": 0.80, "labor_tax": 0.43},
    "NZL": {"vsr": 0.76, "rho_persuade": 0.84, "t_energy": 720, "t_finance": 300, "t_logistics": 360, "t_info": 400, "tau_modify": 140, "tau_verify": 240, "gini_compute": 0.50, "safety_net": 0.81, "labor_tax": 0.43},

    # Asian Technospheres & Hyper-Automated Hostages
    "HKG": {"vsr": 0.44, "rho_persuade": 0.52, "t_energy": 72, "t_finance": 18, "t_logistics": 30, "t_info": 36, "tau_modify": 70, "tau_verify": 280, "gini_compute": 0.72, "safety_net": 0.58, "labor_tax": 0.32},
    "SGP": {"vsr": 0.52, "rho_persuade": 0.60, "t_energy": 48, "t_finance": 24, "t_logistics": 36, "t_info": 48, "tau_modify": 80, "tau_verify": 270, "gini_compute": 0.68, "safety_net": 0.62, "labor_tax": 0.30},
    "JPN": {"vsr": 0.72, "rho_persuade": 0.80, "t_energy": 480, "t_finance": 240, "t_logistics": 300, "t_info": 400, "tau_modify": 130, "tau_verify": 250, "gini_compute": 0.54, "safety_net": 0.82, "labor_tax": 0.48},
    "KOR": {"vsr": 0.64, "rho_persuade": 0.72, "t_energy": 300, "t_finance": 120, "t_logistics": 180, "t_info": 240, "tau_modify": 100, "tau_verify": 270, "gini_compute": 0.64, "safety_net": 0.74, "labor_tax": 0.44},
    "ISR": {"vsr": 0.62, "rho_persuade": 0.70, "t_energy": 240, "t_finance": 96, "t_logistics": 120, "t_info": 180, "tau_modify": 85, "tau_verify": 280, "gini_compute": 0.66, "safety_net": 0.70, "labor_tax": 0.42},

    # Southern & Eastern European Economies
    "ESP": {"vsr": 0.66, "rho_persuade": 0.75, "t_energy": 450, "t_finance": 220, "t_logistics": 260, "t_info": 350, "tau_modify": 120, "tau_verify": 240, "gini_compute": 0.52, "safety_net": 0.78, "labor_tax": 0.50},
    "ITA": {"vsr": 0.64, "rho_persuade": 0.74, "t_energy": 420, "t_finance": 200, "t_logistics": 240, "t_info": 320, "tau_modify": 120, "tau_verify": 240, "gini_compute": 0.53, "safety_net": 0.77, "labor_tax": 0.52},
    "PRT": {"vsr": 0.65, "rho_persuade": 0.76, "t_energy": 480, "t_finance": 220, "t_logistics": 260, "t_info": 340, "tau_modify": 125, "tau_verify": 240, "gini_compute": 0.50, "safety_net": 0.78, "labor_tax": 0.49},
    "GRC": {"vsr": 0.54, "rho_persuade": 0.65, "t_energy": 300, "t_finance": 120, "t_logistics": 150, "t_info": 240, "tau_modify": 100, "tau_verify": 250, "gini_compute": 0.54, "safety_net": 0.68, "labor_tax": 0.48},
    "CYP": {"vsr": 0.52, "rho_persuade": 0.64, "t_energy": 200, "t_finance": 96, "t_logistics": 120, "t_info": 180, "tau_modify": 95, "tau_verify": 250, "gini_compute": 0.56, "safety_net": 0.65, "labor_tax": 0.40},
    "MLT": {"vsr": 0.58, "rho_persuade": 0.68, "t_energy": 180, "t_finance": 84, "t_logistics": 96, "t_info": 160, "tau_modify": 90, "tau_verify": 250, "gini_compute": 0.55, "safety_net": 0.70, "labor_tax": 0.42},
    "EST": {"vsr": 0.78, "rho_persuade": 0.85, "t_energy": 500, "t_finance": 180, "t_logistics": 240, "t_info": 360, "tau_modify": 130, "tau_verify": 240, "gini_compute": 0.50, "safety_net": 0.82, "labor_tax": 0.46},
    "LTU": {"vsr": 0.68, "rho_persuade": 0.76, "t_energy": 400, "t_finance": 180, "t_logistics": 220, "t_info": 300, "tau_modify": 120, "tau_verify": 240, "gini_compute": 0.49, "safety_net": 0.76, "labor_tax": 0.48},
    "LVA": {"vsr": 0.66, "rho_persuade": 0.74, "t_energy": 380, "t_finance": 160, "t_logistics": 200, "t_info": 280, "tau_modify": 115, "tau_verify": 240, "gini_compute": 0.51, "safety_net": 0.74, "labor_tax": 0.48},
    "SVN": {"vsr": 0.74, "rho_persuade": 0.82, "t_energy": 600, "t_finance": 300, "t_logistics": 350, "t_info": 420, "tau_modify": 140, "tau_verify": 240, "gini_compute": 0.44, "safety_net": 0.84, "labor_tax": 0.50},
    "CZE": {"vsr": 0.70, "rho_persuade": 0.78, "t_energy": 550, "t_finance": 260, "t_logistics": 300, "t_info": 380, "tau_modify": 130, "tau_verify": 240, "gini_compute": 0.46, "safety_net": 0.82, "labor_tax": 0.51},
    "POL": {"vsr": 0.64, "rho_persuade": 0.72, "t_energy": 480, "t_finance": 200, "t_logistics": 240, "t_info": 320, "tau_modify": 120, "tau_verify": 240, "gini_compute": 0.50, "safety_net": 0.78, "labor_tax": 0.48},
    "SVK": {"vsr": 0.62, "rho_persuade": 0.70, "t_energy": 420, "t_finance": 180, "t_logistics": 220, "t_info": 300, "tau_modify": 115, "tau_verify": 240, "gini_compute": 0.48, "safety_net": 0.77, "labor_tax": 0.49},
    "HUN": {"vsr": 0.56, "rho_persuade": 0.66, "t_energy": 360, "t_finance": 150, "t_logistics": 180, "t_info": 260, "tau_modify": 110, "tau_verify": 250, "gini_compute": 0.52, "safety_net": 0.72, "labor_tax": 0.50},
    "ROU": {"vsr": 0.48, "rho_persuade": 0.60, "t_energy": 300, "t_finance": 120, "t_logistics": 150, "t_info": 220, "tau_modify": 100, "tau_verify": 260, "gini_compute": 0.55, "safety_net": 0.64, "labor_tax": 0.46},
    "BGR": {"vsr": 0.42, "rho_persuade": 0.55, "t_energy": 240, "t_finance": 96, "t_logistics": 120, "t_info": 180, "tau_modify": 90, "tau_verify": 260, "gini_compute": 0.56, "safety_net": 0.60, "labor_tax": 0.45},
    "MKD": {"vsr": 0.38, "rho_persuade": 0.52, "t_energy": 180, "t_finance": 72, "t_logistics": 96, "t_info": 150, "tau_modify": 80, "tau_verify": 270, "gini_compute": 0.58, "safety_net": 0.56, "labor_tax": 0.44},
}


def build_layer2_indicators_dataframe() -> pd.DataFrame:
    """Computes normalized P5, P6, P7, P8 scores for all 39 nations from seed telemetry."""
    records = []
    for iso, seed in LAYER2_SEED_DATA.items():
        # P5 Epistemic Inviolability
        p5, vsr = dlf.calculate_p5_epistemic_inviolability(
            human_verifications=int(seed["vsr"] * 1000),
            total_critical_verifications=1000,
            adversarial_persuasion_resilience=seed["rho_persuade"]
        )

        # P6 Civilizational Decoupling Half-Life
        p6, t_half = dlf.calculate_p6_decoupling_half_life(
            t_energy=seed["t_energy"],
            t_finance=seed["t_finance"],
            t_logistics=seed["t_logistics"],
            t_info=seed["t_info"],
            t_half_saturation_hours=720.0
        )

        # P7 Multipolar Coordination Velocity
        p7, v_coord = dlf.calculate_p7_coordination_velocity(
            tau_modify=seed["tau_modify"],
            tau_verify_treaty=seed["tau_verify"]
        )

        # P8 Post-Labor Institutional Elasticity
        p8 = dlf.calculate_p8_post_labor_elasticity(
            gini_compute=seed["gini_compute"],
            safety_net_coverage=seed["safety_net"],
            labor_tax_reliance=seed["labor_tax"]
        )

        # Bottleneck identification
        p_dict = {
            "Epistemic Inviolability (P5)": p5,
            "Decoupling Half-Life (P6)": p6,
            "Coordination Velocity (P7)": p7,
            "Post-Labor Elasticity (P8)": p8,
        }
        min_pillar_name = min(p_dict, key=p_dict.get)
        min_pillar_score = float(p_dict[min_pillar_name])

        records.append({
            "country_iso3": iso,
            "p5_epistemic": round(p5, 4),
            "p6_decoupling": round(p6, 4),
            "p7_coordination": round(p7, 4),
            "p8_post_labor": round(p8, 4),
            "t_half_hours": round(t_half, 1),
            "vsr": round(vsr, 4),
            "v_coord": round(v_coord, 4),
            "layer2_bottleneck": min_pillar_name,
            "layer2_min_score": round(min_pillar_score, 4),
        })

    return pd.DataFrame(records)


def compute_dual_layer_sovereignty(base_country_scores_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges Layer 1 adoption scores with Layer 2 sovereignty telemetry.
    Calculates H_Layer1, H_Layer2, V_ASI, ranks, rank shifts, and High-Compute Trap tags.
    """
    l2_df = build_layer2_indicators_dataframe()

    # Merge on country_iso3
    df = pd.merge(base_country_scores_df, l2_df, on="country_iso3", how="inner")
    if len(df) != 39:
        logger.warning(f"Expected 39 nations after merge, got {len(df)}")

    # Ensure Layer 1 components
    p1_col = "AI_Literacy_score" if "AI_Literacy_score" in df.columns else "p_lit"
    p2_col = "Critical_Discernment_score" if "Critical_Discernment_score" in df.columns else "p_disc"
    p3_col = "Institutional_Governance_score" if "Institutional_Governance_score" in df.columns else "p_gov"
    p4_col = "Digital_Infrastructure_score" if "Digital_Infrastructure_score" in df.columns else "p_infra"

    # Compute Layer 1 Score
    df["h_layer1"] = df.apply(
        lambda r: dlf.calculate_layer1_score(r[p1_col], r[p2_col], r[p3_col], r[p4_col]),
        axis=1
    ).round(4)

    # Compute Layer 2 Sovereignty Score (Leontief Floor)
    df["h_layer2"] = df.apply(
        lambda r: dlf.calculate_layer2_sovereignty_score(
            r["p5_epistemic"], r["p6_decoupling"], r["p7_coordination"], r["p8_post_labor"]
        ),
        axis=1
    ).round(4)

    # Compute Master ASI Vulnerability Index
    df["v_asi"] = (df["h_layer1"] - df["h_layer2"]).round(4)

    # Compute National Rankings (Descending: higher score = better rank #1)
    df["rank_layer1"] = df["h_layer1"].rank(ascending=False, method="min").astype(int)
    df["rank_layer2"] = df["h_layer2"].rank(ascending=False, method="min").astype(int)

    # Rank delta = rank_layer1 - rank_layer2
    df["rank_delta_sovereignty"] = df["rank_layer1"] - df["rank_layer2"]

    # Classify Fragility Tiers
    def get_tier(v):
        if v >= 0.40:
            return "Extreme"
        elif v >= 0.25:
            return "High"
        elif v >= 0.10:
            return "Moderate"
        else:
            return "Low"

    df["fragility_tier"] = df["v_asi"].apply(get_tier)

    # High-Compute Vulnerability Trap: high adoption/compute P4 >= 0.70 with V_ASI >= 0.25
    df["high_compute_trap"] = (df["v_asi"] >= 0.25) & (df[p4_col] >= 0.70)

    # Sort by rank_layer2 ascending
    df = df.sort_values("rank_layer2").reset_index(drop=True)
    return df


def run_layer2_dirichlet_monte_carlo(
    df: pd.DataFrame,
    n_draws: int = 1000,
    alpha: list = None,
    seed: int = 42
) -> dict:
    """
    Executes JRC Step 7 Sensitivity Audit across B=1,000 Dirichlet weight draws for Layer 2.
    Evaluates Kendall's W concordance and Spearman rank correlations with Layer 1.
    """
    if alpha is None:
        alpha = [4, 4, 4, 4]  # Centered at equal weights [0.25, 0.25, 0.25, 0.25]

    rng = np.random.default_rng(seed)
    weight_samples = rng.dirichlet(alpha, size=n_draws)

    n_countries = len(df)
    iso_list = df["country_iso3"].tolist()
    p_matrix = df[["p5_epistemic", "p6_decoupling", "p7_coordination", "p8_post_labor"]].to_numpy(dtype=float)
    h_layer1_arr = df["h_layer1"].to_numpy(dtype=float)
    r_layer1 = pd.Series(h_layer1_arr).rank(ascending=False, method="min").to_numpy()

    l2_ranks = np.zeros((n_draws, n_countries))
    spearman_l1_l2 = np.zeros(n_draws)

    for b in range(n_draws):
        w = weight_samples[b]
        # Weighted arithmetic mean component
        mean_part = np.sum(p_matrix * w, axis=1)
        # Weakest-link floor component
        min_part = np.min(p_matrix, axis=1)
        # Leontief composite
        l2_scores = np.sqrt(min_part * mean_part)

        r_l2 = pd.Series(l2_scores).rank(ascending=False, method="min").to_numpy()
        l2_ranks[b] = r_l2
        spearman_l1_l2[b] = stats.spearmanr(r_layer1, r_l2)[0]

    # Kendall's W across draws
    m, n = l2_ranks.shape
    r_sums = np.sum(l2_ranks, axis=0)
    r_bar = np.mean(r_sums)
    ss = np.sum((r_sums - r_bar) ** 2)
    kendall_w = float((12 * ss) / ((m ** 2) * (n ** 3 - n)))

    stability = {}
    for i, iso in enumerate(iso_list):
        stability[iso] = {
            "mean_rank_l2": float(np.mean(l2_ranks[:, i])),
            "std_rank_l2": float(np.std(l2_ranks[:, i])),
            "ci_95": [float(np.percentile(l2_ranks[:, i], 2.5)), float(np.percentile(l2_ranks[:, i], 97.5))],
        }

    audit_summary = {
        "n_draws": n_draws,
        "alpha": alpha,
        "seed": seed,
        "kendall_w_layer2": kendall_w,
        "spearman_l1_vs_l2": {
            "mean": float(np.mean(spearman_l1_l2)),
            "std": float(np.std(spearman_l1_l2)),
            "ci_95": [float(np.percentile(spearman_l1_l2, 2.5)), float(np.percentile(spearman_l1_l2, 97.5))],
        },
        "country_stability": stability,
    }

    return audit_summary


def export_sovereignty_engine_results():
    """Calculates Dual-Layer metrics, exports CSV and JSON payloads, and runs sensitivity audit."""
    input_path = DATA_DIR / "final_country_scores.csv"
    if not input_path.exists():
        input_path = DATA_DIR / "hsri_variants.csv"

    base_df = pd.read_csv(input_path)
    res_df = compute_dual_layer_sovereignty(base_df)

    # 1. Save seeds to data/layer2_sovereignty_seeds.csv
    seed_records = []
    for iso, s in LAYER2_SEED_DATA.items():
        seed_records.append({
            "country_iso3": iso,
            **s
        })
    seeds_df = pd.DataFrame(seed_records)
    seeds_csv = DATA_DIR / "layer2_sovereignty_seeds.csv"
    seeds_df.to_csv(seeds_csv, index=False)
    logger.info(f"Saved {seeds_csv}")

    # 2. Save full variants to data/hsri_layer2_variants.csv
    out_csv = DATA_DIR / "hsri_layer2_variants.csv"
    res_df.to_csv(out_csv, index=False)
    logger.info(f"Saved {out_csv} ({len(res_df)} countries)")

    # 3. Run B=1000 Monte Carlo audit
    logger.info("Running B=1,000 Dirichlet Monte Carlo audit for Layer 2...")
    audit = run_layer2_dirichlet_monte_carlo(res_df, n_draws=1000, seed=42)
    audit_out = DATA_DIR / "monte_carlo_layer2_audit.json"
    with open(audit_out, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)
    logger.info(f"Saved {audit_out}")

    # 4. Export JSON & CSV payloads to site-astro
    records = res_df.to_dict(orient="records")
    for target_dir in [PUBLIC_DATA_DIR, SRC_DATA_DIR]:
        target_dir.mkdir(parents=True, exist_ok=True)
        json_path = target_dir / "hsri_layer2.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
        logger.info(f"Exported {json_path}")

        # Also copy CSV
        astro_csv = target_dir / "hsri_layer2_variants.csv"
        res_df.to_csv(astro_csv, index=False)

    return res_df, audit


def main():
    print("=== HSRI 2.0 Dual-Layer Sovereignty Engine (Sprint 27) ===")
    res_df, audit = export_sovereignty_engine_results()
    print(f"\nProcessed {len(res_df)} countries successfully.")
    print("\n--- TOP 5 HIGHEST ASI VULNERABILITY (V_ASI) ---")
    print(res_df.sort_values("v_asi", ascending=False)[
        ["country_iso3", "h_layer1", "h_layer2", "v_asi", "rank_layer1", "rank_layer2", "rank_delta_sovereignty", "high_compute_trap"]
    ].head(8).to_string(index=False))

    print("\n--- TOP 5 MOST SOVEREIGN NATIONS (H_Layer2) ---")
    print(res_df.sort_values("h_layer2", ascending=False)[
        ["country_iso3", "h_layer1", "h_layer2", "v_asi", "rank_layer1", "rank_layer2", "rank_delta_sovereignty", "layer2_bottleneck"]
    ].head(8).to_string(index=False))

    print(f"\nLayer 2 Kendall Concordance W: {audit['kendall_w_layer2']:.4f}")
    print(f"Mean Spearman Correlation Layer 1 vs Layer 2: {audit['spearman_l1_vs_l2']['mean']:.4f}")


if __name__ == "__main__":
    main()
