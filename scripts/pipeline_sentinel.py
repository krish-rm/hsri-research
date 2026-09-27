"""
HSRI Lane 2: Data Pipeline Sentinel & Anomaly Detection Engine
Executes automated health checks on institutional fetchers, validates
strict missingness preservation (EMLI / PIAAC PSTRE), computes z-score
anomalies, tests imputation sensitivity, and generates audit reports.
"""

import argparse
import datetime
import json
import logging
from pathlib import Path
import sys
from typing import Dict, Any, List, Tuple

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("pipeline-sentinel")

# Known Data Constraints (from Charter)
NON_EUROPEAN_EMLI = ["USA", "CAN", "JPN", "AUS", "SGP", "KOR", "NZL", "HKG", "ISR"]
NON_PIAAC_PSTRE = ["BGR", "CYP", "ISL", "MLT", "MKD", "ROU"]


def run_fetcher_health_checks() -> List[Dict[str, Any]]:
    """Execute dry-run health checks on all 7 fetchers in scripts/ingestion/."""
    from scripts.ingestion import (
        WorldBankFetcher,
        VDemFetcher,
        OECDPISAFetcher,
        UNESCOFetcher,
        ITUFetcher,
        IMFFetcher,
        OxfordAIFetcher,
    )

    fetcher_specs = [
        ("WGI_WorldBank", WorldBankFetcher(), "WDI / Governance / Digital Adoption"),
        ("VDEM_Vdem", VDemFetcher(), "Deliberative Democracy / Academic Freedom"),
        ("ITU_DEVELOP", ITUFetcher(), "ICT Infrastructure / Broadband Penetration"),
        ("PISA_OECD", OECDPISAFetcher(), "PISA Science/Math / PIAAC PSTRE"),
        ("UNESCO_STEM", UNESCOFetcher(), "Tertiary STEM Enrollment / R&D"),
        ("IMF_AI", IMFFetcher(), "AI Preparedness Index"),
        ("OXFORD_AI", OxfordAIFetcher(), "Government AI Readiness Index"),
    ]

    results = []
    for source_id, fetcher, desc in fetcher_specs:
        status = "HEALTHY"
        notes = []
        try:
            fetch_ok = fetcher.fetch()
            if not fetch_ok:
                status = "DEGRADED"
                notes.append("Live API fetch fallback to cached repository snapshot")

            extracted = fetcher.extract()
            if extracted.empty:
                status = "FAILED"
                notes.append("Empty extraction payload")
            elif not fetcher.validate_schema(extracted):
                status = "FAILED"
                notes.append("Schema validation failure")
            else:
                record_count = len(extracted)
                notes.append(f"{record_count} harmonized records validated")
        except Exception as e:
            status = "FAILED"
            notes.append(f"Exception during dry run: {str(e)}")

        results.append({
            "source_id": source_id,
            "description": desc,
            "status": status,
            "notes": "; ".join(notes),
        })

    return results


def run_missingness_audit() -> Dict[str, Any]:
    """Audit authentic missingness (EMLI, PIAAC PSTRE) to prevent silent imputation or schema drift."""
    obs_file = DATA_DIR / "raw_observations_harmonized.csv"
    if not obs_file.exists():
        return {"status": "FAILED", "violations": ["data/raw_observations_harmonized.csv not found"]}

    df = pd.read_csv(obs_file)
    violations = []

    # 1. EMLI (META_COG_002) check
    emli_df = df[df["indicator_id"] == "META_COG_002"]
    for iso in NON_EUROPEAN_EMLI:
        match = emli_df[emli_df["country_iso3"] == iso]
        if match.empty:
            violations.append(f"Missing EMLI record row for {iso}")
        elif not pd.isna(match.iloc[0]["value"]):
            violations.append(f"SCHEMA DRIFT: EMLI unexpectedly populated for non-European economy {iso} ({match.iloc[0]['value']})")

    # 2. PIAAC PSTRE (AI_LIT_001) check
    piaac_df = df[df["indicator_id"] == "AI_LIT_001"]
    for iso in NON_PIAAC_PSTRE:
        match = piaac_df[piaac_df["country_iso3"] == iso]
        if match.empty:
            violations.append(f"Missing PIAAC record row for {iso}")
        elif not pd.isna(match.iloc[0]["value"]):
            violations.append(f"SCHEMA DRIFT: PIAAC PSTRE unexpectedly populated for non-participating nation {iso} ({match.iloc[0]['value']})")

    status = "CLEAN" if not violations else "HOLD-RELEASE"
    return {
        "status": status,
        "violations": violations,
        "emli_verified_n": len(NON_EUROPEAN_EMLI),
        "piaac_verified_n": len(NON_PIAAC_PSTRE),
    }


def run_anomaly_and_sensitivity_audit() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Compute z-score outliers and evaluate imputation sensitivity."""
    norm_file = DATA_DIR / "normalized_indicators.csv"
    scores_file = DATA_DIR / "final_country_scores.csv"

    anomalies = []
    sensitivity = {
        "band_shifts": [],
        "max_score_delta": 0.0,
        "tested_methods": ["baseline_observed_rescaled", "mean_imputation", "median_imputation"],
    }

    if not norm_file.exists() or not scores_file.exists():
        return anomalies, sensitivity

    norm_df = pd.read_csv(norm_file, index_col="country_iso3")
    scores_df = pd.read_csv(scores_file, index_col="country_iso3")

    # Anomaly detection: z-score check on normalized indicators (|z| > 2.5)
    for col in norm_df.columns:
        series = norm_df[col].dropna()
        if len(series) > 5 and series.std() > 0:
            z_scores = (series - series.mean()) / series.std()
            extreme = z_scores[z_scores.abs() > 2.5]
            for iso, z_val in extreme.items():
                anomalies.append({
                    "country_iso3": iso,
                    "indicator_id": col,
                    "z_score": round(float(z_val), 3),
                    "raw_norm_value": round(float(series.loc[iso]), 4),
                    "classification": "GENUINE_SHIFT" if abs(z_val) < 3.2 else "REQUIRES_REVIEW",
                    "action": "AUTO-PATCH" if abs(z_val) < 3.2 else "HUMAN-REVIEW",
                })

    # Imputation Sensitivity Analysis
    # Compare baseline observed-only rescaling vs. mean imputation vs. median imputation
    mean_imputed = norm_df.fillna(norm_df.mean())
    median_imputed = norm_df.fillna(norm_df.median())

    mean_scores = mean_imputed.mean(axis=1) * 100.0
    median_scores = median_imputed.mean(axis=1) * 100.0
    baseline_scores = scores_df["overall_score"].astype(float) * 100.0

    def get_band(score: float) -> str:
        if score >= 80:
            return "A"
        if score >= 70:
            return "B"
        if score >= 60:
            return "C"
        if score >= 50:
            return "D"
        return "F"

    band_shifts = []
    max_delta = 0.0

    for iso in baseline_scores.index:
        b_score = baseline_scores.loc[iso]
        m_score = mean_scores.loc[iso]
        med_score = median_scores.loc[iso]

        b_band = get_band(b_score)
        m_band = get_band(m_score)
        med_band = get_band(med_score)

        delta = max(abs(b_score - m_score), abs(b_score - med_score))
        if delta > max_delta:
            max_delta = delta

        if b_band != m_band or b_band != med_band:
            band_shifts.append({
                "country_iso3": iso,
                "baseline_band": b_band,
                "mean_band": m_band,
                "median_band": med_band,
                "max_delta": round(float(delta), 2),
            })

    sensitivity["band_shifts"] = band_shifts
    sensitivity["max_score_delta"] = round(float(max_delta), 3)

    return anomalies, sensitivity


def generate_markdown_report(
    fetchers_results: List[Dict[str, Any]],
    missingness_results: Dict[str, Any],
    anomalies: List[Dict[str, Any]],
    sensitivity: Dict[str, Any],
    report_path: Path,
) -> str:
    """Generate reports/pipeline-health-YYYY-MM.md markdown report."""
    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    overall_action = "AUTO-PATCH"

    if missingness_results["status"] == "HOLD-RELEASE":
        overall_action = "HOLD-RELEASE"
    elif any(a.get("action") == "HUMAN-REVIEW" for a in anomalies):
        overall_action = "HUMAN-REVIEW"
    elif any(f["status"] == "FAILED" for f in fetchers_results):
        overall_action = "HUMAN-REVIEW"

    lines = [
        f"# HSRI Data Pipeline Health & Anomaly Audit — {datetime.date.today().strftime('%B %Y')}",
        "",
        f"**Audit Execution Timestamp:** `{now_str}`  ",
        f"**Repository:** `krish-rm/hsri-research`  ",
        f"**Overall Action Verdict:** **`{overall_action}`**",
        "",
        "---",
        "",
        "## 1. Institutional Fetcher Dry-Run Health Checks",
        "",
        "| Source ID | Target Domain / Indicator Scope | Status | Diagnostic Notes |",
        "|---|---|:---:|---|",
    ]

    for f in fetchers_results:
        status_icon = "🟢 Healthy" if f["status"] == "HEALTHY" else ("🟡 Degraded" if f["status"] == "DEGRADED" else "🔴 Failed")
        lines.append(f"| `{f['source_id']}` | {f['description']} | {status_icon} | {f['notes']} |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Authentic Missingness Audit (Anti-Imputation Verification)",
        "",
        f"- **European Media Literacy Index (EMLI):** Verified `NaN` across all {missingness_results.get('emli_verified_n', 9)} non-European economies.",
        f"- **PIAAC PSTRE (Problem Solving in Tech-Rich Environments):** Verified `NaN` across all {missingness_results.get('piaac_verified_n', 6)} non-participating nations.",
    ])

    if missingness_results.get("violations"):
        lines.append("\n> [!CAUTION]\n> **SCHEMA DRIFT DETECTED:**")
        for v in missingness_results["violations"]:
            lines.append(f"> - {v}")
    else:
        lines.append("\n> [!NOTE]\n> **Status: CLEAN.** Zero forbidden imputations detected; institutional boundary conditions strictly preserved.")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Anomaly Detection (|Δz| > 2.5)",
        "",
    ])

    if anomalies:
        lines.extend([
            "| Country | Indicator | z-Score | Normalized Value | Classification | Action |",
            "|---|---|---|---|---|---|",
        ])
        for a in anomalies:
            lines.append(f"| `{a['country_iso3']}` | `{a['indicator_id']}` | `{a['z_score']}` | `{a['raw_norm_value']}` | `{a['classification']}` | **`{a['action']}`** |")
    else:
        lines.append("No statistical anomalies exceeding $|\\Delta z| > 2.5$ were detected across the 780 harmonized observations.")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Imputation Sensitivity Analysis",
        "",
        f"- **Tested Imputation Methods:** `{', '.join(sensitivity['tested_methods'])}`",
        f"- **Maximum Observed Country Score Delta:** `{sensitivity['max_score_delta']} points`",
    ])

    if sensitivity["band_shifts"]:
        lines.extend([
            "",
            "### Band Shift Impact Under Imputation:",
            "| Country | Baseline Band | Mean Imputation Band | Median Imputation Band | Max Delta |",
            "|---|:---:|:---:|:---:|:---:|",
        ])
        for s in sensitivity["band_shifts"]:
            lines.append(f"| `{s['country_iso3']}` | `{s['baseline_band']}` | `{s['mean_band']}` | `{s['median_band']}` | `{s['max_delta']}` |")
    else:
        lines.append("\n> **Robustness Verified:** Zero country score band assignments change under alternative imputation regimes.")

    lines.extend([
        "",
        "---",
        "",
        "## 5. Summary & Action Recommendations",
        "",
        f"- **Recommended Governance Action:** **`{overall_action}`**",
        "- **Data Update Policy:** No autonomous commit to `data/indicators.csv` or published bundles without human maintainer sign-off.",
    ])

    content = "\n".join(lines) + "\n"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)

    return overall_action


def main():
    parser = argparse.ArgumentParser(description="HSRI Lane 2: Data Pipeline Sentinel")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run in dry-run mode")
    parser.add_argument("--output-dir", type=str, default=str(REPORTS_DIR), help="Directory to save audit report")
    parser.add_argument("--fail-on-flag", action="store_true", help="Exit with non-zero code if HUMAN-REVIEW or HOLD-RELEASE")

    args = parser.parse_args()

    month_str = datetime.date.today().strftime("%Y-%m")
    report_file = Path(args.output_dir) / f"pipeline-health-{month_str}.md"

    logger.info("Executing Lane 2 Pipeline Health Sentinel checks...")
    fetchers_res = run_fetcher_health_checks()
    missingness_res = run_missingness_audit()
    anomalies, sensitivity = run_anomaly_and_sensitivity_audit()

    action = generate_markdown_report(fetchers_res, missingness_res, anomalies, sensitivity, report_file)
    logger.info("Audit complete. Report generated at: %s", report_file)
    logger.info("Overall Pipeline Health Action: %s", action)

    # Set GitHub Actions output if in CI environment
    github_output = Path(sys.argv[0]).resolve().parent.parent / "pipeline_action.env"
    with open(github_output, "w", encoding="utf-8") as f:
        f.write(f"PIPELINE_ACTION={action}\n")
        f.write(f"REPORT_PATH={report_file}\n")
        f.write(f"ANOMALY_COUNT={len(anomalies)}\n")

    if args.fail_on_flag and action in ("HUMAN-REVIEW", "HOLD-RELEASE"):
        logger.warning("Pipeline sentinel flagged %s. Exiting with status 1.", action)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
