#!/usr/bin/env python3
"""
HSRI Non-Compensatory & Weakest-Link Aggregation Engine (Sprint 25 - Study 2)
Implements JRC/OECD composite indicator non-compensatory families:
1. Compensatory Linear Mean (Baseline HSRI)
2. Non-Compensatory Geometric Mean (Discounting unbalanced development)
3. Leontief Minimum Floor (Weakest-link bottleneck penalty, beta=0.5)
4. Choquet Integral (2-additive capacity modeling infrastructure-discernment synergy/vulnerability)

Includes Vulnerability Index (V_n), Floor Fragility (F_n), High-Compute Vulnerability Trap detection,
and B=1,000 Dirichlet Monte Carlo sensitivity analysis.
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

DEFAULT_PILLARS = [
    "AI_Literacy_score",
    "Critical_Discernment_score",
    "Institutional_Governance_score",
    "Digital_Infrastructure_score",
]

DEFAULT_WEIGHTS = np.array([0.25, 0.25, 0.25, 0.25], dtype=float)


def calculate_linear(pillars: np.ndarray, weights: np.ndarray = None) -> float:
    """
    Model 1: Compensatory Linear Weighted Average (HSRI Baseline)
    H_lin = sum(w_k * P_k)
    """
    p = np.asarray(pillars, dtype=float)
    if np.any(np.isnan(p)):
        raise ValueError("Pillar vector contains NaN. Cannot compute compensatory score under Rule 3.")
    
    if weights is None:
        w = np.ones_like(p) / len(p)
    else:
        w = np.asarray(weights, dtype=float)
        w = w / np.sum(w)
        
    score = float(np.sum(p * w))
    return float(np.clip(score, 0.0, 1.0))


def calculate_geometric(pillars: np.ndarray, weights: np.ndarray = None, eps: float = 0.01) -> float:
    """
    Model 2: Non-Compensatory Geometric Mean
    H_geo = prod(P_k + eps)^w_k - eps
    Preserves scale invariance: if all P_k = c, H_geo = c.
    Penalizes unbalanced pillars via AM-GM inequality.
    """
    p = np.asarray(pillars, dtype=float)
    if np.any(np.isnan(p)):
        raise ValueError("Pillar vector contains NaN. Cannot compute geometric score under Rule 3.")
    
    if weights is None:
        w = np.ones_like(p) / len(p)
    else:
        w = np.asarray(weights, dtype=float)
        w = w / np.sum(w)

    # Shifted geometric mean to preserve scale: prod(p + eps)^w - eps
    shifted = p + eps
    log_geom = np.sum(w * np.log(shifted))
    score = float(np.exp(log_geom) - eps)
    return float(np.clip(score, 0.0, 1.0))


def calculate_leontief(pillars: np.ndarray, weights: np.ndarray = None, beta: float = 0.5) -> float:
    """
    Model 3: Leontief Minimum Floor (Weakest-Link Critical Bottleneck)
    H_leo = (min(P_k))^beta * (H_lin)^(1 - beta)
    Balances overall capacity with weakest link constraint.
    If any pillar collapses to 0, H_leo = 0.
    Scale invariant: if all P_k = c, H_leo = c.
    """
    p = np.asarray(pillars, dtype=float)
    if np.any(np.isnan(p)):
        raise ValueError("Pillar vector contains NaN. Cannot compute Leontief score under Rule 3.")
    
    p_min = float(np.min(p))
    h_lin = calculate_linear(p, weights)
    
    if p_min <= 0.0:
        return 0.0
    
    score = float((p_min ** beta) * (h_lin ** (1.0 - beta)))
    return float(np.clip(score, 0.0, 1.0))


def calculate_choquet(pillars: np.ndarray, weights: np.ndarray = None) -> float:
    """
    Model 4: Choquet Integral with 2-Additive Capacity
    Models synergistic and sub-additive interactions:
    Pillars: 0=AI Literacy, 1=Critical Discernment, 2=Governance, 3=Infrastructure.
    - If Infrastructure (3) is present without Discernment (1), sub-additive penalty:
      mu({3}) = w3 - 0.06 (Technological exposure vulnerability)
    - If both are present, synergy bonus:
      mu({1, 3}) = w1 + w3 + 0.04
    Guarantees monotonicity: mu(A) <= mu(B) for A subset of B, mu(empty)=0, mu(N)=1.
    """
    p = np.asarray(pillars, dtype=float)
    if np.any(np.isnan(p)):
        raise ValueError("Pillar vector contains NaN. Cannot compute Choquet score under Rule 3.")
    
    n = len(p)
    if weights is None:
        base_w = np.ones(n) / n
    else:
        base_w = np.asarray(weights, dtype=float)
        base_w = base_w / np.sum(base_w)

    # Sort criteria ascending: p_(1) <= p_(2) <= ... <= p_(n)
    sorted_indices = np.argsort(p)
    sorted_p = p[sorted_indices]

    h_choq = 0.0
    prev_val = 0.0

    for i in range(n):
        subset = set(sorted_indices[i:])
        # Base additive measure
        cap = sum(base_w[c] for c in subset)
        
        # Apply 2-additive interaction if infra (3) and discernment (1) are present
        if len(subset) == n:
            cap = 1.0
        elif len(subset) == 0:
            cap = 0.0
        else:
            # Sub-additive exposure trap if infra is in subset but discernment is NOT
            if 3 in subset and 1 not in subset:
                cap -= 0.06
            # Synergistic resilience if BOTH infra and discernment are in subset
            elif 3 in subset and 1 in subset:
                cap += 0.04
            cap = max(0.0, min(1.0, cap))

        h_choq += (sorted_p[i] - prev_val) * cap
        prev_val = sorted_p[i]

    return float(np.clip(h_choq, 0.0, 1.0))


def assign_fragility_tier(v_n: float) -> str:
    """Classifies Vulnerability Index into institutional resilience tiers"""
    if v_n >= 0.05:
        return "Critical"
    elif v_n >= 0.02:
        return "High"
    elif v_n >= 0.005:
        return "Moderate"
    else:
        return "Low"


def compute_country_variants(
    df: pd.DataFrame,
    pillars_cols: list = None,
    weights: np.ndarray = None,
    beta: float = 0.5,
    eps: float = 0.01
) -> pd.DataFrame:
    """
    Computes all 4 aggregation variants, vulnerability indices, ranks, and trap flags
    for all countries in the dataset.
    """
    if pillars_cols is None:
        pillars_cols = DEFAULT_PILLARS
    if weights is None:
        weights = DEFAULT_WEIGHTS

    pillar_labels = ["AI Literacy", "Critical Discernment", "Institutional Governance", "Digital Infrastructure"]

    results = []
    for _, row in df.iterrows():
        iso3 = row["country_iso3"]
        p = np.array([row[col] for col in pillars_cols], dtype=float)

        h_lin = calculate_linear(p, weights)
        h_geo = calculate_geometric(p, weights, eps=eps)
        h_leo = calculate_leontief(p, weights, beta=beta)
        h_choq = calculate_choquet(p, weights)

        v_n = h_lin - h_geo
        f_n = h_lin - h_leo

        min_idx = int(np.argmin(p))
        min_val = float(p[min_idx])
        min_name = pillar_labels[min_idx]

        results.append({
            "country_iso3": iso3,
            "hsri_linear": round(h_lin, 4),
            "hsri_geometric": round(h_geo, 4),
            "hsri_leontief": round(h_leo, 4),
            "hsri_choquet": round(h_choq, 4),
            "vulnerability_index": round(v_n, 4),
            "floor_fragility": round(f_n, 4),
            "fragility_tier": assign_fragility_tier(v_n),
            "bottleneck_pillar": min_name,
            "min_pillar_score": round(min_val, 4),
            "p_lit": round(p[0], 4),
            "p_disc": round(p[1], 4),
            "p_gov": round(p[2], 4),
            "p_infra": round(p[3], 4),
        })

    res_df = pd.DataFrame(results)

    # Compute ranks (descending order: rank 1 is highest index)
    for model in ["linear", "geometric", "leontief", "choquet"]:
        res_df[f"rank_{model}"] = res_df[f"hsri_{model}"].rank(ascending=False, method="min").astype(int)

    # Rank deltas: positive means dropped in rank (e.g. from 15 to 18 is +3 positions worse)
    res_df["rank_delta_geo"] = res_df["rank_geometric"] - res_df["rank_linear"]
    res_df["rank_delta_leo"] = res_df["rank_leontief"] - res_df["rank_linear"]
    res_df["rank_delta_choq"] = res_df["rank_choquet"] - res_df["rank_linear"]

    # High-Compute Trap Flag:
    # High vulnerability index (>=0.015) AND rank drop under leontief >= 2 with digital infra > discernment by >0.15
    # OR acute vulnerability (>=0.05)
    infra_disc_gap = (res_df["p_infra"] - res_df["p_disc"]) > 0.15
    res_df["high_compute_trap"] = (
        (res_df["vulnerability_index"] >= 0.015) &
        (res_df["rank_delta_leo"] >= 2) &
        infra_disc_gap
    ) | (res_df["vulnerability_index"] >= 0.05)

    return res_df


def run_dirichlet_monte_carlo(
    df: pd.DataFrame,
    n_draws: int = 1000,
    alpha: list = None,
    seed: int = 42
) -> dict:
    """
    Runs JRC Step 7 Monte Carlo Sensitivity Audit across B=1000 weight draws
    drawn from Dirichlet(alpha).
    Assesses rank stability, Spearman correlation distributions, and confidence intervals.
    """
    if alpha is None:
        alpha = [4, 4, 4, 4]  # Centered at equal weights [0.25, 0.25, 0.25, 0.25]
    
    rng = np.random.default_rng(seed)
    weight_samples = rng.dirichlet(alpha, size=n_draws)

    pillars_cols = DEFAULT_PILLARS
    n_countries = len(df)
    iso_list = df["country_iso3"].tolist()

    lin_ranks = np.zeros((n_draws, n_countries))
    geo_ranks = np.zeros((n_draws, n_countries))
    leo_ranks = np.zeros((n_draws, n_countries))
    choq_ranks = np.zeros((n_draws, n_countries))

    spearman_lin_geo = np.zeros(n_draws)
    spearman_lin_leo = np.zeros(n_draws)
    spearman_lin_choq = np.zeros(n_draws)

    p_matrix = df[pillars_cols].to_numpy(dtype=float)

    for b in range(n_draws):
        w = weight_samples[b]
        
        b_lin = np.array([calculate_linear(p_matrix[i], w) for i in range(n_countries)])
        b_geo = np.array([calculate_geometric(p_matrix[i], w) for i in range(n_countries)])
        b_leo = np.array([calculate_leontief(p_matrix[i], w) for i in range(n_countries)])
        b_choq = np.array([calculate_choquet(p_matrix[i], w) for i in range(n_countries)])

        r_lin = pd.Series(b_lin).rank(ascending=False, method="min").to_numpy()
        r_geo = pd.Series(b_geo).rank(ascending=False, method="min").to_numpy()
        r_leo = pd.Series(b_leo).rank(ascending=False, method="min").to_numpy()
        r_choq = pd.Series(b_choq).rank(ascending=False, method="min").to_numpy()

        lin_ranks[b] = r_lin
        geo_ranks[b] = r_geo
        leo_ranks[b] = r_leo
        choq_ranks[b] = r_choq

        spearman_lin_geo[b] = stats.spearmanr(r_lin, r_geo)[0]
        spearman_lin_leo[b] = stats.spearmanr(r_lin, r_leo)[0]
        spearman_lin_choq[b] = stats.spearmanr(r_lin, r_choq)[0]

    # Compute Kendall's W across draws for each model
    def compute_kendall_w(rank_matrix):
        m, n = rank_matrix.shape
        r_sums = np.sum(rank_matrix, axis=0)
        r_bar = np.mean(r_sums)
        ss = np.sum((r_sums - r_bar) ** 2)
        w = (12 * ss) / ((m ** 2) * (n ** 3 - n))
        return float(w)

    country_stability = {}
    for i, iso in enumerate(iso_list):
        country_stability[iso] = {
            "lin_mean_rank": float(np.mean(lin_ranks[:, i])),
            "lin_rank_std": float(np.std(lin_ranks[:, i])),
            "geo_mean_rank": float(np.mean(geo_ranks[:, i])),
            "geo_rank_std": float(np.std(geo_ranks[:, i])),
            "leo_mean_rank": float(np.mean(leo_ranks[:, i])),
            "leo_rank_std": float(np.std(leo_ranks[:, i])),
            "rank_ci_95_lin": [float(np.percentile(lin_ranks[:, i], 2.5)), float(np.percentile(lin_ranks[:, i], 97.5))],
            "rank_ci_95_leo": [float(np.percentile(leo_ranks[:, i], 2.5)), float(np.percentile(leo_ranks[:, i], 97.5))],
        }

    audit_summary = {
        "n_draws": n_draws,
        "alpha": alpha,
        "seed": seed,
        "kendall_w": {
            "linear": compute_kendall_w(lin_ranks),
            "geometric": compute_kendall_w(geo_ranks),
            "leontief": compute_kendall_w(leo_ranks),
            "choquet": compute_kendall_w(choq_ranks),
        },
        "spearman_correlations": {
            "lin_vs_geo": {
                "mean": float(np.mean(spearman_lin_geo)),
                "std": float(np.std(spearman_lin_geo)),
                "ci_95": [float(np.percentile(spearman_lin_geo, 2.5)), float(np.percentile(spearman_lin_geo, 97.5))],
            },
            "lin_vs_leo": {
                "mean": float(np.mean(spearman_lin_leo)),
                "std": float(np.std(spearman_lin_leo)),
                "ci_95": [float(np.percentile(spearman_lin_leo, 2.5)), float(np.percentile(spearman_lin_leo, 97.5))],
            },
            "lin_vs_choq": {
                "mean": float(np.mean(spearman_lin_choq)),
                "std": float(np.std(spearman_lin_choq)),
                "ci_95": [float(np.percentile(spearman_lin_choq, 2.5)), float(np.percentile(spearman_lin_choq, 97.5))],
            },
        },
        "country_stability": country_stability,
    }

    return audit_summary


def export_aggregation_results():
    """Generates and exports data/hsri_variants.csv and JSON artifacts to site-astro"""
    data_path = DATA_DIR / "final_country_scores.csv"
    if not data_path.exists():
        raise FileNotFoundError(f"Missing {data_path}")

    df = pd.read_csv(data_path)
    res_df = compute_country_variants(df)

    # Save to data/hsri_variants.csv
    csv_out = DATA_DIR / "hsri_variants.csv"
    res_df.to_csv(csv_out, index=False)
    logger.info(f"Saved {csv_out} ({len(res_df)} countries)")

    # Run Monte Carlo audit
    logger.info("Running B=1,000 Dirichlet Monte Carlo audit...")
    audit = run_dirichlet_monte_carlo(df, n_draws=1000, seed=42)
    audit_out = DATA_DIR / "monte_carlo_aggregation_audit.json"
    with open(audit_out, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)
    logger.info(f"Saved Monte Carlo audit to {audit_out}")

    # Export to site-astro
    records = res_df.to_dict(orient="records")
    for target_dir in [PUBLIC_DATA_DIR, SRC_DATA_DIR]:
        target_dir.mkdir(parents=True, exist_ok=True)
        json_path = target_dir / "hsri_variants.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
        logger.info(f"Exported {json_path}")
        # Also copy CSV
        shutil_csv = target_dir / "hsri_variants.csv"
        res_df.to_csv(shutil_csv, index=False)

    return res_df, audit


def main():
    print("=== HSRI Non-Compensatory Aggregation Engine ===")
    res_df, audit = export_aggregation_results()
    print(f"Successfully processed {len(res_df)} countries.")
    print("Top 5 by Vulnerability Index:")
    print(res_df.sort_values("vulnerability_index", ascending=False)[["country_iso3", "hsri_linear", "hsri_geometric", "hsri_leontief", "vulnerability_index", "rank_delta_leo", "high_compute_trap"]].head(8))
    print("\nDirichlet B=1000 Kendall Concordance:")
    print(audit["kendall_w"])
    print("\nMean Spearman Lin vs Leo:", audit["spearman_correlations"]["lin_vs_leo"]["mean"])


if __name__ == "__main__":
    main()
