#!/usr/bin/env python3
"""
Export Web Data for site-astro
Gathers all Phase 2-6 analytical artifacts and exports unified JSON/CSV datasets
to site-astro/public/data and site-astro/src/data.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
import shutil
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SITE_DIR = PROJECT_ROOT / "site-astro"
PUBLIC_DATA_DIR = SITE_DIR / "public" / "data"
SRC_DATA_DIR = SITE_DIR / "src" / "data"

PUBLIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
SRC_DATA_DIR.mkdir(parents=True, exist_ok=True)

COUNTRY_NAMES = {
    "AUS": ("Australia", "oceania"),
    "AUT": ("Austria", "europe"),
    "BEL": ("Belgium", "europe"),
    "BGR": ("Bulgaria", "europe"),
    "CAN": ("Canada", "north-america"),
    "CYP": ("Cyprus", "europe"),
    "CZE": ("Czech Republic", "europe"),
    "DEU": ("Germany", "europe"),
    "DNK": ("Denmark", "europe"),
    "ESP": ("Spain", "europe"),
    "EST": ("Estonia", "europe"),
    "FIN": ("Finland", "europe"),
    "FRA": ("France", "europe"),
    "GBR": ("United Kingdom", "europe"),
    "GRC": ("Greece", "europe"),
    "HKG": ("Hong Kong", "asia"),
    "HUN": ("Hungary", "europe"),
    "IRL": ("Ireland", "europe"),
    "ISL": ("Iceland", "europe"),
    "ISR": ("Israel", "asia"),
    "ITA": ("Italy", "europe"),
    "JPN": ("Japan", "asia"),
    "KOR": ("South Korea", "asia"),
    "LTU": ("Lithuania", "europe"),
    "LUX": ("Luxembourg", "europe"),
    "LVA": ("Latvia", "europe"),
    "MLT": ("Malta", "europe"),
    "NLD": ("Netherlands", "europe"),
    "NOR": ("Norway", "europe"),
    "NZL": ("New Zealand", "oceania"),
    "POL": ("Poland", "europe"),
    "PRT": ("Portugal", "europe"),
    "ROU": ("Romania", "europe"),
    "SGP": ("Singapore", "asia"),
    "SVK": ("Slovakia", "europe"),
    "SVN": ("Slovenia", "europe"),
    "SWE": ("Sweden", "europe"),
    "TWN": ("Taiwan", "asia"),
    "USA": ("United States", "north-america"),
}

KPMG_SURVEY_COUNTRIES = {"AUS", "BRA", "CAN", "CHL", "CHN", "EST", "FRA", "DEU", "IND", "ISR", "JPN", "NLD", "SGP", "ZAF", "KOR", "GBR", "USA"}
EMLI_NON_EUROPEAN = {"AUS", "CAN", "HKG", "ISR", "JPN", "KOR", "NZL", "SGP", "TWN", "USA"}

def round_floats(obj, digits=4):
    """Recursively round floats to avoid spurious precision"""
    if isinstance(obj, float):
        return round(obj, digits)
    elif isinstance(obj, dict):
        return {k: round_floats(v, digits) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [round_floats(v, digits) for v in obj]
    return obj

def get_band(score_100: float) -> str:
    if score_100 >= 80.0:
        return "A"
    elif score_100 >= 70.0:
        return "B"
    elif score_100 >= 60.0:
        return "C"
    elif score_100 >= 50.0:
        return "D"
    else:
        return "F"

def export_all():
    print("Exporting pipeline outputs to site-astro...")

    # 1. Load CSVs
    final_scores = pd.read_csv(DATA_DIR / "final_country_scores.csv", index_col="country_iso3")
    gap_df = pd.read_csv(DATA_DIR / "readiness_exposure_gap.csv", index_col="country_iso3")
    cross_df = pd.read_csv(DATA_DIR / "scenario_crossing_years.csv", index_col="country_iso3")
    labor_cross_df = pd.read_csv(DATA_DIR / "labor_crossing_years.csv", index_col=0)
    labor_vuln_df = pd.read_csv(DATA_DIR / "labor_vulnerability.csv", index_col=0)
    indicators_df = pd.read_csv(DATA_DIR / "indicators.csv")

    # Load country profiles JSON files
    profiles_dir = PROJECT_ROOT / "research" / "country_profiles"
    country_profiles = {}
    if profiles_dir.exists():
        for f in profiles_dir.glob("*.json"):
            if f.stem.lower() not in ["templates", "summary_report"]:
                with open(f, "r", encoding="utf-8") as fp:
                    country_profiles[f.stem.upper()] = json.load(fp)

    # Load narrative integration JSON files
    narratives_dir = PROJECT_ROOT / "research" / "integrated_narratives"
    country_narratives = {}
    if narratives_dir.exists():
        for f in narratives_dir.glob("*_narrative.json"):
            iso = f.stem.replace("_narrative", "").upper()
            with open(f, "r", encoding="utf-8") as fp:
                country_narratives[iso] = json.load(fp)

    # Sort final scores by overall_score descending
    final_scores_sorted = final_scores.sort_values(by="overall_score", ascending=False)
    
    countries_list = []
    rank = 1

    for iso3, row in final_scores_sorted.iterrows():
        name, region = COUNTRY_NAMES.get(iso3, (iso3, "other"))
        score_100 = round(float(row["overall_score"]) * 100, 2)
        band = get_band(score_100)

        # Pillars
        ai_lit = round(float(row["AI_Literacy_score"]) * 100, 2)
        crit_disc = round(float(row["Critical_Discernment_score"]) * 100, 2)
        gov = round(float(row["Institutional_Governance_score"]) * 100, 2)
        infra = round(float(row["Digital_Infrastructure_score"]) * 100, 2)

        # Exposure & gap
        exp_score = round(float(gap_df.loc[iso3, "exposure"]) * 100, 2) if iso3 in gap_df.index else 50.0
        gap_val = round(float(gap_df.loc[iso3, "gap"]) * 100, 2) if iso3 in gap_df.index else 0.0
        gap_status = str(gap_df.loc[iso3, "gap_status"]) if iso3 in gap_df.index else "Balanced"

        # Scenario crossing years
        takeoff_yr = int(cross_df.loc[iso3, "takeoff_crossing"]) if (iso3 in cross_df.index and pd.notna(cross_df.loc[iso3, "takeoff_crossing"])) else None
        steady_yr = int(cross_df.loc[iso3, "steady_progress_crossing"]) if (iso3 in cross_df.index and pd.notna(cross_df.loc[iso3, "steady_progress_crossing"])) else None
        plateau_yr = int(cross_df.loc[iso3, "plateau_crossing"]) if (iso3 in cross_df.index and pd.notna(cross_df.loc[iso3, "plateau_crossing"])) else None

        # Labor vulnerability
        labor_vuln = round(float(labor_vuln_df.loc[iso3, "vulnerability_index"]) * 100, 2) if iso3 in labor_vuln_df.index else 50.0
        labor_cross = int(round(float(labor_cross_df.loc[iso3, "crossing_year"]))) if (iso3 in labor_cross_df.index and pd.notna(labor_cross_df.loc[iso3, "crossing_year"])) else 2035

        profile = country_profiles.get(iso3, {})
        narrative = country_narratives.get(iso3, {})

        # Indicator provenance breakdown for auditability (Task 5)
        indicators_breakdown = []
        for _, ind_row in indicators_df.iterrows():
            code = str(ind_row.get("indicator_id", ""))
            role = str(ind_row.get("role", "Retained"))
            ind_name = str(ind_row.get("name", ""))
            pillar = str(ind_row.get("pillar", ""))
            source = str(ind_row.get("source_ids", ""))

            if role == "Rejected":
                audit_status = "Rejected"
                audit_note = "Excluded during construct audit"
            elif role == "Context-only":
                if code == "CAL_TRUST_001":
                    if iso3 in KPMG_SURVEY_COUNTRIES:
                        audit_status = "Context-Observed"
                        audit_note = "Observed in KPMG-Melbourne 2023 wave (17 countries)"
                    else:
                        audit_status = "Context-Imputed"
                        audit_note = "Country was not in 17-country survey sample; value was imputed"
                else:
                    audit_status = "Context-Only"
                    audit_note = "Tracked for context; not scored in core index"
            else:  # Retained
                if code == "META_COG_002" and iso3 in EMLI_NON_EUROPEAN:
                    audit_status = "Imputed (Geographic Gap)"
                    audit_note = "European Media Literacy Index only surveys European states; non-European value is imputed"
                elif code == "META_COG_003" and iso3 in ["CYP", "ISL", "MLT"]:
                    audit_status = "Imputed (Sample Gap)"
                    audit_note = "Not covered in standard Reuters DNR sample waves"
                else:
                    audit_status = "Observed (Unverified Microdata)"
                    audit_note = "Observation populated in observations.csv; primary survey microdata unverified in repo"

            indicators_breakdown.append({
                "code": code,
                "name": ind_name,
                "pillar": pillar,
                "role": role,
                "source": source,
                "auditStatus": audit_status,
                "auditNote": audit_note
            })

        c_data = {
            "id": iso3.lower(),
            "code": iso3,
            "name": name,
            "rank": rank,
            "score": score_100,
            "rawScore": round(float(row["overall_score"]), 4),
            "band": band,
            "region": region,
            "status": row.get("status", "Moderate capacity"),
            "exposure": exp_score,
            "gap": gap_val,
            "gapStatus": gap_status,
            "laborVulnerability": labor_vuln,
            "laborCrossingYear": labor_cross,
            "crossingYears": {
                "takeoff": takeoff_yr,
                "steady": steady_yr,
                "plateau": plateau_yr
            },
            "pillars": {
                "ai_literacy": ai_lit,
                "critical_discernment": crit_disc,
                "institutional_governance": gov,
                "digital_infrastructure": infra,
                "economic": ai_lit,
                "social": crit_disc,
                "institutional": gov,
                "technological": infra
            },
            # Map legacy names for existing components compatibility
            "economic": ai_lit,
            "social": crit_disc,
            "institutional": gov,
            "technological": infra,
            "peerGroup": "High-income OECD",
            "lastUpdated": "2026-09-22",
            "summary": profile.get("summary", ""),
            "strengths": profile.get("strengths", []),
            "challenges": profile.get("challenges", []),
            "recommendations": profile.get("recommendations", []),
            "archetype": narrative.get("archetype", "strategic_adapter"),
            "executiveSummary": narrative.get("executive_summary", ""),
            "indicatorsBreakdown": indicators_breakdown
        }
        countries_list.append(c_data)
        rank += 1

    country_scores_payload = {
        "metadata": {
            "totalCountries": len(countries_list),
            "benchmarkRatedCountries": 39,
            "evaluatedCountries": 145,
            "unratedEvaluatedCountries": 86,
            "globalNations": 195,
            "avgScore": round(float(np.mean([c["score"] for c in countries_list])), 1),
            "bandCounts": {
                "A": sum(1 for c in countries_list if c["band"] == "A"),
                "B": sum(1 for c in countries_list if c["band"] == "B"),
                "C": sum(1 for c in countries_list if c["band"] == "C"),
                "D": sum(1 for c in countries_list if c["band"] == "D"),
                "F": sum(1 for c in countries_list if c["band"] == "F")
            },
            "lastUpdated": "2026-09-22",
            "methodologyVersion": "v0.1-preview",
            "coverageNote": "Preview release: 39 benchmark nations (OECD/high-income sample). Primary microdata unverified."
        },
        "pillars": [
            {
                "id": "ai_literacy",
                "name": "AI Literacy",
                "code": "LIT",
                "weight": 0.25,
                "description": "Public and workforce technical comprehension of generative & cognitive models."
            },
            {
                "id": "critical_discernment",
                "name": "Critical Discernment",
                "code": "DISC",
                "weight": 0.25,
                "description": "Cognitive defense against algorithmic epistemic manipulation and deepfakes."
            },
            {
                "id": "institutional_governance",
                "name": "Institutional Governance",
                "code": "GOV",
                "weight": 0.25,
                "description": "State capacity to audit, enforce safety bounds, and regulate frontier autonomy."
            },
            {
                "id": "digital_infrastructure",
                "name": "Digital Infrastructure",
                "code": "INFRA",
                "weight": 0.25,
                "description": "Resilience of power, domestic compute clusters, and network transmission."
            }
        ],
        "countries": countries_list
    }

    # Save to public/data and src/data
    for dest_dir in [PUBLIC_DATA_DIR, SRC_DATA_DIR]:
        with open(dest_dir / "country_scores.json", "w", encoding="utf-8") as f:
            json.dump(country_scores_payload, f, indent=2)

        with open(dest_dir / "country_profiles.json", "w", encoding="utf-8") as f:
            json.dump({c["id"]: c for c in countries_list}, f, indent=2)

    # Indicators json
    indicators_list = []
    for _, row in indicators_df.iterrows():
        indicators_list.append({
            "code": str(row.get("indicator_id", "")),
            "name": str(row.get("name", "")),
            "pillar": str(row.get("pillar", "")),
            "subcomponent": str(row.get("subcomponent", "")),
            "description": str(row.get("description", "")),
            "unit": str(row.get("unit", "")),
            "direction": str(row.get("direction", "higher")),
            "validity": str(row.get("validity_rating", "")),
            "source": str(row.get("source_ids", "")),
            "role": str(row.get("role", "Retained")),
            "normalization": str(row.get("normalization", "min-max"))
        })

    for dest_dir in [PUBLIC_DATA_DIR, SRC_DATA_DIR]:
        with open(dest_dir / "indicators.json", "w", encoding="utf-8") as f:
            json.dump(indicators_list, f, indent=2)

    # Forecast timeline data json
    forecast_cdfs_path = DATA_DIR / "forecast_cdfs.json"
    forecast_cdfs = {}
    if forecast_cdfs_path.exists():
        with open(forecast_cdfs_path, "r", encoding="utf-8") as f:
            forecast_cdfs = json.load(f)

    integrated_forecasts_path = DATA_DIR / "integrated_forecasts.csv"
    integrated_forecasts = {}
    if integrated_forecasts_path.exists():
        int_df = pd.read_csv(integrated_forecasts_path, index_col=0)
        integrated_forecasts = int_df.to_dict(orient="index")

    timeline_payload = {
        "currentYear": 2026,
        "capabilityMilestones": {
            "A": {"name": "Current AI", "year": 2026, "desc": "ChatGPT-4 class narrow models"},
            "B": {"name": "Advanced Narrow AI", "year": 2028, "desc": "Domain-specific expertise exceeding humans"},
            "C": {"name": "Multi-Domain AI", "year": 2030, "desc": "Cross-domain strategic reasoning"},
            "D": {"name": "Emerging AGI", "year": 2032, "desc": "Early self-improvement capability"},
            "E": {"name": "Advanced AGI", "year": 2035, "desc": "General multi-agent autonomy"},
            "F": {"name": "Transcendent AI", "year": 2040, "desc": "Superintelligent cognitive singularity"}
        },
        "capabilityLevels": {
            "2026": "A",
            "2028": "B",
            "2030": "C",
            "2032": "D",
            "2035": "E",
            "2040": "F"
        },
        "forecasts": {
            "plateau": [
                {"year": 2028, "probability": 0.20},
                {"year": 2030, "probability": 0.45},
                {"year": 2033, "probability": 0.65},
                {"year": 2036, "probability": 0.82},
                {"year": 2040, "probability": 0.94}
            ],
            "steady": [
                {"year": 2027, "probability": 0.15},
                {"year": 2029, "probability": 0.35},
                {"year": 2032, "probability": 0.60},
                {"year": 2035, "probability": 0.80},
                {"year": 2038, "probability": 0.92}
            ],
            "takeoff": [
                {"year": 2027, "probability": 0.25},
                {"year": 2029, "probability": 0.55},
                {"year": 2031, "probability": 0.75},
                {"year": 2034, "probability": 0.90},
                {"year": 2037, "probability": 0.98}
            ],
            "integrated": round_floats(integrated_forecasts, 4)
        },
        "cdfs": round_floats(forecast_cdfs, 4)
    }

    for dest_dir in [PUBLIC_DATA_DIR, SRC_DATA_DIR]:
        with open(dest_dir / "timeline_data.json", "w", encoding="utf-8") as f:
            json.dump(timeline_payload, f, indent=2)

    # Copy CSV files to public/data for direct user download
    csv_files_to_copy = [
        "final_country_scores.csv",
        "pillar_scores.csv",
        "indicators.csv",
        "readiness_exposure_gap.csv",
        "composite_exposure_scores.csv",
        "scenario_crossing_years.csv",
        "labor_vulnerability.csv",
        "labor_crossing_years.csv",
        "normalized_indicators.csv"
    ]
    for csv_file in csv_files_to_copy:
        src = DATA_DIR / csv_file
        if src.exists():
            shutil.copy2(src, PUBLIC_DATA_DIR / csv_file)

    print(f"Successfully exported data for {len(countries_list)} countries to site-astro!")

if __name__ == "__main__":
    export_all()
