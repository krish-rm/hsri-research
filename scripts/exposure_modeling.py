#!/usr/bin/env python3
"""
Comprehensive Exposure Modeling for HSRI-Proxy v0.1

Integrates all domain exposures (labor, skills, information, wellbeing,
inequality, autonomy, catastrophic) to create unified exposure assessment.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExposureModeler:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.results = {}

    def load_data(self):
        """Load all required data files"""
        try:
            # Load HSRI-Proxy country scores
            self.country_scores = pd.read_csv(self.data_dir / "final_country_scores.csv", index_col=0)

            # Load labor vulnerability (from previous model)
            self.labor_data = pd.read_csv(self.data_dir / "labor_vulnerability.csv", index_col=0)

            logger.info("✓ All data files loaded successfully")
            return True

        except FileNotFoundError as e:
            logger.error(f"❌ Missing data file: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            return False

    def define_domain_models(self):
        """Define exposure models for each domain"""
        domain_models = {
            "labor": {
                "description": "AI impact on employment and workforce",
                "indicators": ["automation_risk", "skill_obsolescence", "job_transformation"],
                "weight": 0.25,
                "vulnerability_threshold": 0.6
            },
            "skills": {
                "description": "AI impact on human skills and capabilities",
                "indicators": ["skill_obsolescence_rate", "learning_capacity", "digital_literacy"],
                "weight": 0.20,
                "vulnerability_threshold": 0.7
            },
            "information": {
                "description": "AI impact on information environment and trust",
                "indicators": ["information_overload", "deepfake_risk", "trust_calibration"],
                "weight": 0.15,
                "vulnerability_threshold": 0.5
            },
            "wellbeing": {
                "description": "AI impact on mental health and social connection",
                "indicators": ["attention_fragmentation", "social_connection", "digital_wellbeing"],
                "weight": 0.15,
                "vulnerability_threshold": 0.4
            },
            "inequality": {
                "description": "AI impact on social and economic inequality",
                "indicators": ["digital_divide", "wealth_concentration", "access_gap"],
                "weight": 0.15,
                "vulnerability_threshold": 0.8
            },
            "autonomy": {
                "description": "AI impact on human decision-making and agency",
                "indicators": ["decision_automation", "value_drift", "agency_preservation"],
                "weight": 0.05,
                "vulnerability_threshold": 0.9
            },
            "catastrophic": {
                "description": "AI existential risk and catastrophic potential",
                "indicators": ["capability_threshold", "safety_preparedness", "coordination_capacity"],
                "weight": 0.05,
                "vulnerability_threshold": 0.95
            }
        }

        return domain_models

    def calculate_domain_exposures(self):
        """Calculate exposure scores for each domain"""
        logger.info("Calculating domain exposures...")

        domain_exposures = pd.DataFrame(index=self.country_scores.index)

        # Labor exposure (from previous model)
        if hasattr(self, 'labor_data'):
            for c in domain_exposures.index:
                if c in self.labor_data.index:
                    domain_exposures.loc[c, "labor"] = float(self.labor_data.loc[c, "labor_exposure"])
                else:
                    domain_exposures.loc[c, "labor"] = 0.5

        # Other domain exposures calibrated by country readiness
        exposure_simulations = {
            "skills": {
                "USA": 0.45, "GBR": 0.48, "DEU": 0.52, "FRA": 0.55, "JPN": 0.50,
                "CHN": 0.65, "RUS": 0.60, "BRA": 0.70, "IND": 0.75, "MEX": 0.68,
                "IDN": 0.72, "EGY": 0.78, "NGA": 0.80, "PAK": 0.82, "ETH": 0.85
            },
            "information": {
                "USA": 0.60, "GBR": 0.58, "DEU": 0.62, "FRA": 0.65, "JPN": 0.63,
                "CHN": 0.70, "RUS": 0.68, "BRA": 0.72, "IND": 0.75, "MEX": 0.73,
                "IDN": 0.78, "EGY": 0.80, "NGA": 0.82, "PAK": 0.85, "ETH": 0.88
            },
            "wellbeing": {
                "USA": 0.40, "GBR": 0.42, "DEU": 0.38, "FRA": 0.45, "JPN": 0.43,
                "CHN": 0.55, "RUS": 0.52, "BRA": 0.60, "IND": 0.65, "MEX": 0.58,
                "IDN": 0.62, "EGY": 0.68, "NGA": 0.70, "PAK": 0.75, "ETH": 0.78
            },
            "inequality": {
                "USA": 0.75, "GBR": 0.70, "DEU": 0.65, "FRA": 0.68, "JPN": 0.60,
                "CHN": 0.80, "RUS": 0.78, "BRA": 0.85, "IND": 0.88, "MEX": 0.82,
                "IDN": 0.85, "EGY": 0.88, "NGA": 0.90, "PAK": 0.92, "ETH": 0.95
            },
            "autonomy": {
                "USA": 0.35, "GBR": 0.38, "DEU": 0.42, "FRA": 0.45, "JPN": 0.40,
                "CHN": 0.55, "RUS": 0.58, "BRA": 0.50, "IND": 0.65, "MEX": 0.60,
                "IDN": 0.70, "EGY": 0.75, "NGA": 0.80, "PAK": 0.82, "ETH": 0.85
            },
            "catastrophic": {
                "USA": 0.15, "GBR": 0.12, "DEU": 0.18, "FRA": 0.20, "JPN": 0.16,
                "CHN": 0.25, "RUS": 0.28, "BRA": 0.22, "IND": 0.30, "MEX": 0.24,
                "IDN": 0.26, "EGY": 0.35, "NGA": 0.32, "PAK": 0.38, "ETH": 0.40
            }
        }

        for domain, exposures in exposure_simulations.items():
            for country in self.country_scores.index:
                if country in exposures:
                    domain_exposures.loc[country, domain] = exposures[country]
                else:
                    readiness = float(self.country_scores.loc[country, "overall_score"]) if "overall_score" in self.country_scores.columns else 0.5
                    if domain == "skills":
                        domain_exposures.loc[country, domain] = round(max(0.25, min(0.80, 0.42 + (1 - readiness) * 0.38)), 3)
                    elif domain == "information":
                        domain_exposures.loc[country, domain] = round(max(0.35, min(0.85, 0.52 + (1 - readiness) * 0.32)), 3)
                    elif domain == "wellbeing":
                        domain_exposures.loc[country, domain] = round(max(0.28, min(0.75, 0.36 + (1 - readiness) * 0.34)), 3)
                    elif domain == "inequality":
                        domain_exposures.loc[country, domain] = round(max(0.35, min(0.90, 0.58 + (1 - readiness) * 0.32)), 3)
                    elif domain == "autonomy":
                        domain_exposures.loc[country, domain] = round(max(0.22, min(0.80, 0.32 + (1 - readiness) * 0.42)), 3)
                    elif domain == "catastrophic":
                        domain_exposures.loc[country, domain] = round(max(0.10, min(0.40, 0.12 + readiness * 0.12)), 3)

        return domain_exposures

    def calculate_composite_exposure(self, domain_exposures, domain_models):
        """Calculate composite exposure score"""
        logger.info("Calculating composite exposure score...")

        composite_scores = pd.DataFrame(index=domain_exposures.index)

        # Weighted average by domain weights
        for country in domain_exposures.index:
            total_exposure = 0
            total_weight = 0

            for domain, model in domain_models.items():
                if domain in domain_exposures.columns:
                    exposure = domain_exposures.loc[country, domain]
                    weight = model["weight"]
                    total_exposure += exposure * weight
                    total_weight += weight

            if total_weight > 0:
                composite_scores.loc[country, "composite_exposure"] = round(total_exposure / total_weight, 3)

        # Add HSRI-Proxy readiness score for comparison
        if "overall_score" in self.country_scores.columns:
            composite_scores["overall_score"] = self.country_scores["overall_score"].round(4)

        return composite_scores

    def calculate_readiness_exposure_gap(self, composite_scores):
        """Calculate readiness-exposure gap"""
        logger.info("Calculating readiness-exposure gap...")

        gap_analysis = pd.DataFrame(index=composite_scores.index)

        if "overall_score" in composite_scores.columns:
            gap_analysis["readiness"] = composite_scores["overall_score"].round(4)
            gap_analysis["exposure"] = composite_scores["composite_exposure"].round(4)
            gap_analysis["gap"] = round(gap_analysis["exposure"] - gap_analysis["readiness"], 3)

            def classify_gap(gap):
                if gap > 0.2:
                    return "Critical Gap"
                elif gap > 0.05:
                    return "Warning Gap"
                elif gap > -0.1:
                    return "Balanced"
                else:
                    return "Prepared"

            gap_analysis["gap_status"] = gap_analysis["gap"].apply(classify_gap)

        return gap_analysis

    def model_scenario_crossings(self, gap_analysis, scenarios):
        """Model crossing years under different scenarios"""
        logger.info("Modeling scenario crossings...")

        crossing_analysis = pd.DataFrame(index=gap_analysis.index)

        for scenario_name, params in scenarios.items():
            col_name = f"{scenario_name}_crossing"
            crossing_series = pd.Series(index=gap_analysis.index, dtype=object)

            exposure_growth = params["exposure_growth"]
            readiness_growth = params["readiness_growth"]

            for country in gap_analysis.index:
                current_gap = gap_analysis.loc[country, "gap"]

                if current_gap >= 0.2:
                    crossing_year = 2026
                elif exposure_growth > readiness_growth:
                    net_rate = exposure_growth - readiness_growth
                    gap_to_close = 0.2 - current_gap
                    years = max(1, int(np.ceil(gap_to_close / net_rate)))
                    crossing_year = 2026 + years
                else:
                    # In plateau scenario, prepared countries stay resilient
                    crossing_year = None

                crossing_series[country] = crossing_year

            crossing_analysis[col_name] = crossing_series

        return crossing_analysis

    def create_visualization_data(self, gap_analysis, crossing_analysis):
        """Create data for visualizations"""
        visualization_data = {
            "gap_heatmap": gap_analysis[["gap", "gap_status"]].copy(),
            "timeline_data": crossing_analysis.copy(),
            "comparison_data": gap_analysis[["readiness", "exposure", "gap"]].copy()
        }
        return visualization_data

    def generate_comprehensive_report(self, domain_models, domain_exposures,
                                    composite_scores, gap_analysis, crossing_analysis,
                                    visualization_data):
        """Generate comprehensive exposure modeling report"""
        report = []
        report.append("=" * 60)
        report.append("HSRI-Proxy v0.1 Comprehensive Exposure Modeling Report")
        report.append(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        report.append("\n## EXECUTIVE SUMMARY")
        report.append(f"Countries analyzed: {len(gap_analysis)}")
        report.append(f"Average exposure score: {composite_scores['composite_exposure'].mean():.2f}")
        report.append(f"Average readiness score: {composite_scores['overall_score'].mean():.2f}")

        report.append("\n## READINESS-EXPOSURE GAP ANALYSIS")
        gap_counts = gap_analysis["gap_status"].value_counts()
        for status, count in gap_counts.items():
            report.append(f"**{status}**: {count} countries")

        report.append("\n## DOMAIN EXPOSURES OVERVIEW")
        for domain in domain_models.keys():
            if domain in domain_exposures.columns:
                mean_exp = domain_exposures[domain].mean()
                report.append(f"**{domain.title()}**: mean exposure = {mean_exp:.2f}")

        # Save results
        composite_scores.to_csv(self.data_dir / "composite_exposure_scores.csv")
        gap_analysis.to_csv(self.data_dir / "readiness_exposure_gap.csv")
        crossing_analysis.to_csv(self.data_dir / "scenario_crossing_years.csv")

        report_file = self.project_root / "research" / "exposure_modeling_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        logger.info(f"Exposure modeling report saved to {report_file}")
        return {
            "composite_scores": composite_scores,
            "gap_analysis": gap_analysis,
            "crossing_analysis": crossing_analysis,
            "report_file": report_file
        }

    def run_exposure_modeling(self):
        """Run complete exposure modeling process"""
        logger.info("Starting comprehensive exposure modeling...")

        if not self.load_data():
            return False

        domain_models = self.define_domain_models()
        scenarios = {
            "plateau": {"exposure_growth": 0.02, "readiness_growth": 0.05},
            "steady_progress": {"exposure_growth": 0.08, "readiness_growth": 0.06},
            "takeoff": {"exposure_growth": 0.20, "readiness_growth": 0.04}
        }

        domain_exposures = self.calculate_domain_exposures()
        composite_scores = self.calculate_composite_exposure(domain_exposures, domain_models)
        gap_analysis = self.calculate_readiness_exposure_gap(composite_scores)
        crossing_analysis = self.model_scenario_crossings(gap_analysis, scenarios)
        visualization_data = self.create_visualization_data(gap_analysis, crossing_analysis)

        self.generate_comprehensive_report(
            domain_models, domain_exposures, composite_scores, gap_analysis,
            crossing_analysis, visualization_data
        )

        logger.info("✅ Exposure modeling completed successfully")
        return True

def main():
    """Run the exposure modeling process"""
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    project_root = Path.cwd()
    modeler = ExposureModeler(project_root)

    if modeler.run_exposure_modeling():
        print("\n[OK] Exposure modeling completed successfully!")
        return 0
    else:
        print("\n[ERROR] Exposure modeling failed!")
        return 1

if __name__ == "__main__":
    exit(main())