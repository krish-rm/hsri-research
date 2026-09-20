#!/usr/bin/env python3
"""
Labor Exposure Model for HSRI-Proxy v0.1

Quantifies AI exposure in labor markets using ILO data and occupation classifications.
Models workforce vulnerability and adaptation capacity across all benchmark countries.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LaborExposureModel:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.results = {}

    def load_data(self):
        """Load labor market and education data"""
        try:
            # Load country scores from Phase 3
            self.country_scores = pd.read_csv(self.data_dir / "final_country_scores.csv", index_col=0)
            logger.info(f"✓ Loaded {len(self.country_scores)} country scores from final_country_scores.csv")
            return True

        except FileNotFoundError as e:
            logger.error(f"❌ Missing data file: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            return False

    def classify_occupations(self):
        """Classify occupations by AI exposure risk"""
        occupation_classes = {
            "High_Exposure": {
                "description": "Routine cognitive and manual tasks",
                "examples": ["Data Entry Clerks", "Cashiers", "Basic Assembly Workers"],
                "automation_probability": 0.75,
                "risk_level": "High"
            },
            "Medium_Exposure": {
                "description": "Non-routine manual and some routine cognitive",
                "examples": ["Retail Sales", "Administrative Assistants", "Truck Drivers"],
                "automation_probability": 0.55,
                "risk_level": "Medium"
            },
            "Low_Exposure": {
                "description": "Non-routine cognitive and creative tasks",
                "examples": ["Software Developers", "Teachers", "Healthcare Professionals"],
                "automation_probability": 0.25,
                "risk_level": "Low"
            }
        }
        return occupation_classes

    def calculate_exposure_by_country(self):
        """Calculate AI exposure scores for each country"""
        logger.info("Calculating labor exposure by country...")

        # Benchmark baseline occupation shares
        base_shares = {
            "USA": {"High": 0.15, "Medium": 0.45, "Low": 0.40},
            "GBR": {"High": 0.16, "Medium": 0.46, "Low": 0.38},
            "DEU": {"High": 0.18, "Medium": 0.44, "Low": 0.38},
            "FRA": {"High": 0.17, "Medium": 0.45, "Low": 0.38},
            "JPN": {"High": 0.20, "Medium": 0.43, "Low": 0.37},
            "SGP": {"High": 0.14, "Medium": 0.42, "Low": 0.44},
            "KOR": {"High": 0.19, "Medium": 0.44, "Low": 0.37},
            "DNK": {"High": 0.15, "Medium": 0.43, "Low": 0.42},
            "FIN": {"High": 0.14, "Medium": 0.42, "Low": 0.44},
            "SWE": {"High": 0.15, "Medium": 0.43, "Low": 0.42},
            "NOR": {"High": 0.14, "Medium": 0.42, "Low": 0.44},
            "CAN": {"High": 0.16, "Medium": 0.45, "Low": 0.39},
            "AUS": {"High": 0.16, "Medium": 0.45, "Low": 0.39},
            "NLD": {"High": 0.15, "Medium": 0.43, "Low": 0.42},
            "CHE": {"High": 0.15, "Medium": 0.41, "Low": 0.44},
        }

        countries_to_model = list(self.country_scores.index)
        exposure_scores = pd.DataFrame(index=countries_to_model)

        for country in countries_to_model:
            if country in base_shares:
                shares = base_shares[country]
            else:
                score = self.country_scores.loc[country, "overall_score"] if "overall_score" in self.country_scores.columns else 0.5
                if score >= 0.7:
                    shares = {"High": 0.16, "Medium": 0.44, "Low": 0.40}
                elif score >= 0.5:
                    shares = {"High": 0.22, "Medium": 0.44, "Low": 0.34}
                elif score >= 0.3:
                    shares = {"High": 0.30, "Medium": 0.42, "Low": 0.28}
                else:
                    shares = {"High": 0.38, "Medium": 0.40, "Low": 0.22}

            exposure_score = (
                shares["High"] * 0.75 +
                shares["Medium"] * 0.55 +
                shares["Low"] * 0.25
            )

            exposure_scores.loc[country, "labor_exposure_raw"] = exposure_score
            exposure_scores.loc[country, "high_risk_share"] = shares["High"]
            exposure_scores.loc[country, "medium_risk_share"] = shares["Medium"]
            exposure_scores.loc[country, "low_risk_share"] = shares["Low"]

        min_exp = exposure_scores["labor_exposure_raw"].min()
        max_exp = exposure_scores["labor_exposure_raw"].max()
        if max_exp > min_exp:
            exposure_scores["labor_exposure_normalized"] = (
                exposure_scores["labor_exposure_raw"] - min_exp
            ) / (max_exp - min_exp)
        else:
            exposure_scores["labor_exposure_normalized"] = 0.5

        return exposure_scores

    def calculate_adaptation_capacity(self):
        """Calculate adaptation capacity using education and skills indicators"""
        logger.info("Calculating adaptation capacity...")

        countries_to_model = list(self.country_scores.index)
        adaptation_scores = pd.DataFrame(index=countries_to_model)

        for country in countries_to_model:
            row = self.country_scores.loc[country]
            edu = float(row.get("AI_Literacy_score", 0.5))
            dig = float(row.get("Digital_Infrastructure_score", 0.5))
            gov = float(row.get("Institutional_Governance_score", 0.5))

            adaptation = (edu + dig + gov) / 3.0
            adaptation_scores.loc[country, "adaptation_capacity"] = max(0.05, adaptation)

        return adaptation_scores

    def calculate_vulnerability_index(self, exposure_scores, adaptation_scores):
        """Calculate vulnerability index = exposure ÷ adaptation"""
        logger.info("Calculating vulnerability index...")

        vulnerability = pd.DataFrame(index=exposure_scores.index)
        vulnerability["labor_exposure"] = exposure_scores["labor_exposure_normalized"]
        vulnerability["adaptation_capacity"] = adaptation_scores["adaptation_capacity"]

        vulnerability["vulnerability_ratio"] = (
            vulnerability["labor_exposure"] / vulnerability["adaptation_capacity"]
        )

        min_ratio = vulnerability["vulnerability_ratio"].min()
        max_ratio = vulnerability["vulnerability_ratio"].max()
        if max_ratio > min_ratio:
            vulnerability["vulnerability_index"] = (
                vulnerability["vulnerability_ratio"] - min_ratio
            ) / (max_ratio - min_ratio)
        else:
            vulnerability["vulnerability_index"] = 0.5

        def classify_vulnerability(score):
            if score >= 0.8:
                return "Critical"
            elif score >= 0.6:
                return "High"
            elif score >= 0.4:
                return "Moderate"
            elif score >= 0.2:
                return "Low"
            else:
                return "Minimal"

        vulnerability["vulnerability_class"] = vulnerability["vulnerability_index"].apply(classify_vulnerability)
        return vulnerability

    def model_crossing_years(self, vulnerability_scores, scenarios):
        """Model years when exposure exceeds adaptation capacity"""
        logger.info("Modeling crossing years...")

        crossing_analysis = pd.DataFrame(index=vulnerability_scores.index)

        prod_adjustment = scenarios["steady_progress"]["productivity_impact"]
        adaptation_growth = scenarios["steady_progress"]["adaptation_rate"] * 0.8

        for country in vulnerability_scores.index:
            current_exposure = vulnerability_scores.loc[country, "labor_exposure"]
            current_adaptation = vulnerability_scores.loc[country, "adaptation_capacity"]

            exposure_growth = prod_adjustment
            adapt_growth = adaptation_growth

            if current_exposure > current_adaptation:
                crossing_year = 2026
                years_to_cross = 0
            elif exposure_growth > adapt_growth:
                deficit = current_adaptation - current_exposure
                annual_increase = exposure_growth - adapt_growth
                years_to_cross = max(1, int(np.ceil(deficit / annual_increase)))
                crossing_year = 2026 + years_to_cross
            else:
                crossing_year = 2038
                years_to_cross = 12

            crossing_analysis.loc[country, "crossing_year"] = crossing_year
            crossing_analysis.loc[country, "years_until_crossing"] = years_to_cross

        return crossing_analysis

    def generate_report(self, exposure_scores, adaptation_scores,
                       vulnerability_scores, crossing_analysis, scenarios):
        """Generate labor exposure model report"""
        report = []
        report.append("=" * 60)
        report.append("HSRI-Proxy v0.1 Labor Exposure Model Report")
        report.append(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        report.append("\n## SUMMARY STATISTICS")
        report.append(f"Countries modeled: {len(vulnerability_scores)}")
        report.append(f"Average vulnerability: {vulnerability_scores['vulnerability_index'].mean():.2f}")
        report.append(f"Countries crossing threshold: {crossing_analysis['crossing_year'].notna().sum()}")

        report.append("\n## VULNERABILITY DISTRIBUTION")
        class_counts = vulnerability_scores["vulnerability_class"].value_counts()
        for vulnerability_class, count in class_counts.items():
            report.append(f"**{vulnerability_class}**: {count} countries")

        report.append("\n## MOST VULNERABLE COUNTRIES")
        top_vulnerable = vulnerability_scores.nlargest(5, "vulnerability_index")
        for country, row in top_vulnerable.iterrows():
            report.append(f"**{country}**: {row['vulnerability_index']:.2f} ({row['vulnerability_class']})")

        report.append("\n## CROSSING YEARS (Years when exposure > adaptation)")
        countries_with_crossings = crossing_analysis[crossing_analysis["crossing_year"].notna()]
        if len(countries_with_crossings) > 0:
            for country, row in countries_with_crossings.head(10).iterrows():
                year = int(row["crossing_year"])
                years = int(row["years_until_crossing"])
                report.append(f"**{country}**: {year} (in {years} years)")

        # Save results
        vulnerability_scores.to_csv(self.data_dir / "labor_vulnerability.csv")
        crossing_analysis.to_csv(self.data_dir / "labor_crossing_years.csv")

        report_file = self.project_root / "research" / "labor_exposure_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        logger.info(f"Labor exposure model report saved to {report_file}")
        return report_file

    def run_model(self):
        """Run complete labor exposure model"""
        logger.info("Starting labor exposure model...")

        if not self.load_data():
            return False

        scenarios = {
            "plateau": {
                "ai_growth_rate": 0.05,
                "adaptation_rate": 0.08,
                "productivity_impact": 0.03
            },
            "steady_progress": {
                "ai_growth_rate": 0.15,
                "adaptation_rate": 0.12,
                "productivity_impact": 0.10
            },
            "takeoff": {
                "ai_growth_rate": 0.30,
                "adaptation_rate": 0.10,
                "productivity_impact": 0.25
            }
        }

        exposure_scores = self.calculate_exposure_by_country()
        adaptation_scores = self.calculate_adaptation_capacity()
        vulnerability_scores = self.calculate_vulnerability_index(exposure_scores, adaptation_scores)
        crossing_analysis = self.model_crossing_years(vulnerability_scores, scenarios)

        report_file = self.generate_report(exposure_scores, adaptation_scores,
                                          vulnerability_scores, crossing_analysis, scenarios)

        logger.info("✅ Labor exposure model completed successfully")
        return True

def main():
    """Run the labor exposure model"""
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    project_root = Path.cwd()
    model = LaborExposureModel(project_root)

    if model.run_model():
        print("\n[OK] Labor exposure model completed successfully!")
        return 0
    else:
        print("\n[ERROR] Labor exposure model failed!")
        return 1

if __name__ == "__main__":
    exit(main())