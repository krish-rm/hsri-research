"""
Master Harmonization Pipeline for HSRI Empirical Observations
Merges institutional feeds, preserves authentic missing values (NaN),
and generates data/raw_observations_harmonized.csv.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("harmonize")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
RESEARCH_DIR = ROOT_DIR / "research"


def run_harmonization():
    logger.info("Starting HSRI Empirical Observation Harmonization Pipeline...")

    # Load baseline datasets
    coverage_df = pd.read_csv(DATA_DIR / "coverage-by-country.csv")
    benchmark_countries = coverage_df[coverage_df["overall_status"] == "Scored"].copy()
    benchmark_iso_list = set(benchmark_countries["country_iso3"].unique())

    indicators_df = pd.read_csv(DATA_DIR / "indicators.csv")
    retained_ids = set(indicators_df[indicators_df["role"] == "Retained"]["indicator_id"])
    all_indicators = indicators_df.set_index("indicator_id")

    obs_df = pd.read_csv(DATA_DIR / "observations.csv")

    # Define verified empirical availability boundaries per remediation/01-coverage-audit.md

    # 1. Non-European nations missing EMLI (META_COG_002)
    NON_EUROPEAN = {"AUS", "CAN", "HKG", "ISR", "JPN", "KOR", "NZL", "SGP", "USA"}

    # 2. KPMG AI Trust 2023 Wave benchmark participants
    KPMG_BENCHMARK_PARTICIPANTS = {
        "AUS", "CAN", "DEU", "EST", "FRA", "GBR", "ISR", "JPN", "KOR", "NLD", "SGP", "USA"
    }

    # 3. Reuters Digital News Report unsurveyed benchmark nations
    REUTERS_MISSING = {"CYP", "ISL", "MLT", "LUX"}

    # 4. OECD PIAAC PSTRE unsurveyed / missing round benchmark nations
    PIAAC_MISSING = {"BGR", "CYP", "ISL", "MLT", "MKD", "ROU"}

    # 5. Stanford AI Legislative Tracker missing standalone tracker
    STANFORD_MISSING = {"CYP", "MKD", "MLT", "ISL"}

    records = []

    for _, row in obs_df.iterrows():
        iso = row["country_iso3"]
        cname = row["country_name"]
        ind_id = row["indicator_id"]
        val = row["value"]
        year = row["year"]
        unit = row["unit"]
        source_id = row["source_id"]
        notes = row["coverage_notes"]

        status = "Observed"
        audit_note = notes

        # Apply empirical missingness rules
        if ind_id == "META_COG_002" and iso in NON_EUROPEAN:
            val = np.nan
            status = "Missing"
            audit_note = "Non-European economy: not surveyed in Council of Europe / OSIS EMLI index"

        elif ind_id == "CAL_TRUST_001" and iso not in KPMG_BENCHMARK_PARTICIPANTS:
            val = np.nan
            status = "Missing"
            audit_note = "Economy not surveyed in KPMG-Melbourne 2023 17-country study wave"

        elif ind_id == "META_COG_003" and iso in REUTERS_MISSING:
            val = np.nan
            status = "Missing"
            audit_note = "Unsurveyed in Reuters Institute Digital News Report sample"

        elif ind_id == "AI_LIT_001" and iso in PIAAC_MISSING:
            val = np.nan
            status = "Missing"
            audit_note = "Did not participate in OECD PIAAC Problem Solving (PSTRE) module"

        elif ind_id == "DEC_AGY_005" and iso in STANFORD_MISSING:
            val = np.nan
            status = "Missing"
            audit_note = "No standalone national legislative tracker in Stanford HAI Index"

        records.append({
            "country_iso3": iso,
            "country_name": cname,
            "indicator_id": ind_id,
            "value": val,
            "year": year,
            "unit": unit,
            "source_id": source_id,
            "status": status,
            "coverage_notes": audit_note
        })

    harmonized_df = pd.DataFrame(records)

    # Save to data/raw_observations_harmonized.csv
    output_path = DATA_DIR / "raw_observations_harmonized.csv"
    harmonized_df.to_csv(output_path, index=False)
    logger.info("Saved %d harmonized observation records to %s", len(harmonized_df), output_path)

    # Generate Empirical Coverage Summary Report
    retained_df = harmonized_df[harmonized_df["indicator_id"].isin(retained_ids)]
    total_retained_obs = len(retained_df)
    observed_retained_obs = retained_df["value"].notna().sum()
    missing_retained_obs = retained_df["value"].isna().sum()
    avg_retained_coverage = (observed_retained_obs / total_retained_obs) * 100

    logger.info(
        "Retained Indicators Coverage: %d/%d (%.1f%% observed, %.1f%% missing)",
        observed_retained_obs, total_retained_obs, avg_retained_coverage, 100 - avg_retained_coverage
    )

    # Compute coverage per country
    country_summary = []
    for iso, group in retained_df.groupby("country_iso3"):
        cname = group["country_name"].iloc[0]
        obs_count = group["value"].notna().sum()
        tot_count = len(group)
        pct = (obs_count / tot_count) * 100
        country_summary.append({
            "iso3": iso,
            "country": cname,
            "observed_count": obs_count,
            "total_retained": tot_count,
            "coverage_pct": round(pct, 1)
        })

    summary_df = pd.DataFrame(country_summary).sort_values("coverage_pct", ascending=False)
    
    # Write summary artifact
    summary_md = f"""# Empirical Indicator Coverage Summary (Phase 2 Ingestion)

**Harmonized Observations Dataset:** `data/raw_observations_harmonized.csv`  
**Total Scored Benchmark Countries:** 39  
**Retained Indicators Evaluated:** {len(retained_ids)}  
**Overall Retained Completeness:** **{avg_retained_coverage:.1f}%** (Observed: {observed_retained_obs}, Missing: {missing_retained_obs})

---

## Country-by-Country Empirical Coverage (Retained Indicators)

| ISO3 | Country Name | Observed | Total | Empirical Coverage |
| :--- | :--- | :---: | :---: | :---: |
"""
    for _, r in summary_df.iterrows():
        summary_md += f"| `{r['iso3']}` | {r['country']} | {r['observed_count']} | {r['total_retained']} | **{r['coverage_pct']}%** |\n"

    with open(RESEARCH_DIR / "empirical_coverage_summary.md", "w", encoding="utf-8") as f:
        f.write(summary_md)

    logger.info("Generated empirical coverage summary at research/empirical_coverage_summary.md")
    return harmonized_df


if __name__ == "__main__":
    run_harmonization()
