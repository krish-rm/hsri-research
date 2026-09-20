#!/usr/bin/env python3
"""
Forecast Integration for HSRI-Proxy v0.1

Integrates expert, platform, model-based, lab, and skeptical forecasts
into unified probability distributions for timeline synthesis.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime
from scipy import stats
from scipy.stats import beta, norm
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ForecastIntegrator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.results = {}

        # Forecast source weights
        self.source_weights = {
            "expert": 0.4,
            "platform": 0.3,
            "model_based": 0.2,
            "lab": 0.1,
            "skeptical": 0.1
        }

    def define_capability_milestones(self):
        """Define AI capability milestones with years"""
        milestones = {
            "A": {"name": "Current AI", "year": 2026, "description": "Narrow AI applications"},
            "B": {"name": "Advanced Narrow AI", "year": 2028, "description": "Domain-specific expertise"},
            "C": {"name": "Multi-Domain AI", "year": 2030, "description": "Cross-domain reasoning"},
            "D": {"name": "Emerging AGI", "year": 2032, "description": "Self-improvement capability"},
            "E": {"name": "Advanced AGI", "year": 2035, "description": "General intelligence"},
            "F": {"name": "Transcendent AI", "year": 2040, "description": "Superintelligence"}
        }
        return milestones

    def define_forecast_sources(self):
        """Define forecast sources with characteristics"""
        sources = {
            "expert": {
                "name": "Expert Surveys",
                "description": "AI researcher and expert assessments",
                "weight": 0.4,
                "confidence": 0.8,
                "examples": ["AI Impacts surveys", "AI Index expert panels"]
            },
            "platform": {
                "name": "Company Roadmaps",
                "description": "AI platform company projections",
                "weight": 0.3,
                "confidence": 0.6,
                "examples": ["OpenAI predictions", "Google AI forecasts"]
            },
            "model_based": {
                "name": "Statistical Models",
                "description": "AI capability extrapolation models",
                "weight": 0.2,
                "confidence": 0.7,
                "examples": ["Metaculus predictions", "AI forecasting tournaments"]
            },
            "lab": {
                "name": "Technical Assessments",
                "description": "AI research lab technical analysis",
                "weight": 0.1,
                "confidence": 0.9,
                "examples": ["DeepMind research", "Anthropic technical reports"]
            },
            "skeptical": {
                "name": "Critical Perspectives",
                "description": "Risk-aware and conservative estimates",
                "weight": 0.1,
                "confidence": 0.5,
                "examples": ["AI safety concerns", "Regulatory impact assessments"]
            }
        }
        return sources

    def generate_forecast_data(self):
        """Generate synthetic forecast data for each source type"""
        logger.info("Generating forecast data for integration...")

        capability_milestones = self.define_capability_milestones()
        forecast_sources = self.define_forecast_sources()

        # Generate forecasts for each source
        source_forecasts = {}

        # Expert forecasts (moderate optimism)
        expert_forecasts = {}
        for milestone, info in capability_milestones.items():
            if milestone == "A":  # Current AI is certain
                expert_forecasts[milestone] = {
                    "year": info["year"],
                    "probability": 1.0,
                    "confidence": 0.95,
                    "source": "expert"
                }
            else:
                # Probability distribution reaching each milestone
                base_year = int(info["year"])
                uncertainty = max(2, int(round((ord(milestone) - ord("A")) * 1.5)))

                # Create probability distribution
                years = np.arange(base_year - uncertainty, base_year + uncertainty + 1)
                probs = norm.pdf(years, base_year, max(0.5, uncertainty / 3))
                probs = probs / probs.sum()  # Normalize
                valid_years = years[probs > 0.01] if np.any(probs > 0.01) else years

                expert_forecasts[milestone] = {
                    "year_dist": years.tolist(),
                    "prob_dist": probs.tolist(),
                    "median_year": int(round(float(np.percentile(years, 50)))),
                    "mean_year": int(round(float(np.mean(valid_years)))),
                    "confidence": 0.8 - (ord(milestone) - ord("A")) * 0.1
                }

        source_forecasts["expert"] = expert_forecasts

        # Platform forecasts (optimistic)
        platform_forecasts = {}
        for milestone, info in capability_milestones.items():
            if milestone == "A":
                platform_forecasts[milestone] = {
                    "year": info["year"],
                    "probability": 1.0,
                    "confidence": 0.98,
                    "source": "platform"
                }
            else:
                # More optimistic, earlier predictions
                base_year = int(info["year"]) - 1
                uncertainty = max(2, int(round((ord(milestone) - ord("A")) * 1.2)))

                years = np.arange(base_year - uncertainty, base_year + uncertainty + 1)
                probs = norm.pdf(years, base_year, max(0.5, uncertainty / 4))
                probs = probs / probs.sum()
                valid_years = years[probs > 0.01] if np.any(probs > 0.01) else years

                platform_forecasts[milestone] = {
                    "year_dist": years.tolist(),
                    "prob_dist": probs.tolist(),
                    "median_year": int(round(float(np.percentile(years, 50)))),
                    "mean_year": int(round(float(np.mean(valid_years)))),
                    "confidence": 0.7 - (ord(milestone) - ord("A")) * 0.08
                }

        source_forecasts["platform"] = platform_forecasts

        # Model-based forecasts (statistical)
        model_forecasts = {}
        for milestone, info in capability_milestones.items():
            if milestone == "A":
                model_forecasts[milestone] = {
                    "year": info["year"],
                    "probability": 1.0,
                    "confidence": 0.99,
                    "source": "model_based"
                }
            else:
                # Based on historical technology adoption curves
                base_year = int(info["year"])
                uncertainty = max(2, int(round((ord(milestone) - ord("A")) * 2)))

                years = np.arange(base_year - uncertainty, base_year + uncertainty + 1)
                # Normalize domain to (0, 1) for beta distribution
                norm_x = (years - (base_year - uncertainty)) / (2 * uncertainty)
                norm_x = np.clip(norm_x, 1e-4, 1.0 - 1e-4)
                probs = beta.pdf(norm_x, 2, 5)
                if probs.sum() > 0:
                    probs = probs / probs.sum()
                else:
                    probs = np.ones_like(years, dtype=float) / len(years)
                valid_years = years[probs > 0.01] if np.any(probs > 0.01) else years

                model_forecasts[milestone] = {
                    "year_dist": years.tolist(),
                    "prob_dist": probs.tolist(),
                    "median_year": int(round(float(np.percentile(years, 50)))),
                    "mean_year": int(round(float(np.mean(valid_years)))),
                    "confidence": 0.75 - (ord(milestone) - ord("A")) * 0.1
                }

        source_forecasts["model_based"] = model_forecasts

        # Lab forecasts (cautious)
        lab_forecasts = {}
        for milestone, info in capability_milestones.items():
            if milestone == "A":
                lab_forecasts[milestone] = {
                    "year": info["year"],
                    "probability": 1.0,
                    "confidence": 0.99,
                    "source": "lab"
                }
            else:
                # More conservative, later predictions
                base_year = int(info["year"]) + 1
                uncertainty = max(3, int(round((ord(milestone) - ord("A")) * 1.8)))

                years = np.arange(base_year - uncertainty, base_year + uncertainty + 1)
                probs = norm.pdf(years, base_year, max(0.5, uncertainty / 3))
                probs = probs / probs.sum()
                valid_years = years[probs > 0.01] if np.any(probs > 0.01) else years

                lab_forecasts[milestone] = {
                    "year_dist": years.tolist(),
                    "prob_dist": probs.tolist(),
                    "median_year": int(round(float(np.percentile(years, 50)))),
                    "mean_year": int(round(float(np.mean(valid_years)))),
                    "confidence": 0.85 - (ord(milestone) - ord("A")) * 0.08
                }

        source_forecasts["lab"] = lab_forecasts

        # Skeptical forecasts (very conservative)
        skeptical_forecasts = {}
        for milestone, info in capability_milestones.items():
            if milestone == "A":
                skeptical_forecasts[milestone] = {
                    "year": info["year"],
                    "probability": 1.0,
                    "confidence": 1.0,
                    "source": "skeptical"
                }
            else:
                # Much later predictions
                base_year = int(info["year"]) + 3
                uncertainty = max(5, int(round((ord(milestone) - ord("A")) * 2.5)))

                years = np.arange(base_year - uncertainty, base_year + uncertainty + 1)
                probs = norm.pdf(years, base_year, max(0.5, uncertainty / 2))
                probs = probs / probs.sum()
                valid_years = years[probs > 0.01] if np.any(probs > 0.01) else years

                skeptical_forecasts[milestone] = {
                    "year_dist": years.tolist(),
                    "prob_dist": probs.tolist(),
                    "median_year": int(round(float(np.percentile(years, 50)))),
                    "mean_year": int(round(float(np.mean(valid_years)))),
                    "confidence": 0.6 - (ord(milestone) - ord("A")) * 0.08
                }

        source_forecasts["skeptical"] = skeptical_forecasts

        return source_forecasts

    def integrate_forecasts(self, source_forecasts):
        """Integrate forecasts from different sources"""
        logger.info("Integrating forecasts from multiple sources...")

        capability_milestones = self.define_capability_milestones()
        integrated_forecasts = {}

        # Create integrated probability distributions for each milestone
        for milestone in capability_milestones.keys():
            milestone_forecasts = {}

            # Collect year distributions from all sources
            all_years = []
            all_probs = []

            for source_name, source_data in source_forecasts.items():
                if milestone in source_data:
                    source_info = source_data[milestone]

                    if "year_dist" in source_info:  # Distribution data
                        years = source_info["year_dist"]
                        probs = source_info["prob_dist"]
                        weight = self.source_weights[source_name]
                        confidence = source_info.get("confidence", 0.5)

                        # Apply weight and confidence
                        adjusted_probs = np.array(probs) * weight * confidence

                        all_years.extend(years)
                        all_probs.extend(adjusted_probs)
                    else:  # Point estimate
                        year = source_info["year"]
                        weight = self.source_weights[source_name]
                        confidence = source_info.get("confidence", 0.5)

                        all_years.append(year)
                        all_probs.append(weight * confidence)

            if all_years:
                # Normalize probabilities
                total_prob = sum(all_probs)
                if total_prob > 0:
                    all_probs = [p / total_prob for p in all_probs]

                    # Sort by year
                    sorted_data = sorted(zip(all_years, all_probs))
                    sorted_years = [x[0] for x in sorted_data]
                    sorted_probs = [x[1] for x in sorted_data]

                    valid_years = [y for y, p in zip(sorted_years, sorted_probs) if p > 0.01]
                    mean_val = int(round(float(np.mean(valid_years)))) if valid_years else int(round(float(np.mean(sorted_years))))

                    integrated_forecasts[milestone] = {
                        "year_dist": [int(y) for y in sorted_years],
                        "prob_dist": [float(p) for p in sorted_probs],
                        "median_year": int(round(float(np.percentile(sorted_years, 50)))),
                        "mean_year": mean_val,
                        "confidence": float(np.mean([source_data[milestone].get("confidence", 0.5)
                                              for source_name, source_data in source_forecasts.items()
                                              if milestone in source_data]))
                    }

        return integrated_forecasts

    def calculate_disagreement_metrics(self, integrated_forecasts):
        """Calculate disagreement between forecast sources"""
        logger.info("Calculating forecast disagreement metrics...")

        disagreement_metrics = {}

        # Calculate entropy for each milestone (higher entropy = more disagreement)
        for milestone, forecast in integrated_forecasts.items():
            prob_dist = forecast["prob_dist"]
            entropy = -sum([p * np.log(p + 1e-10) for p in prob_dist if p > 0])
            ci = np.percentile(forecast["year_dist"], [25, 75])
            disagreement_metrics[milestone] = {
                "entropy": float(entropy),
                "disagreement_level": "Low" if entropy < 2 else "Medium" if entropy < 3 else "High",
                "confidence_interval": f"{int(round(ci[0]))}-{int(round(ci[1]))}"
            }

        # Overall disagreement
        total_entropy = float(np.mean([m["entropy"] for m in disagreement_metrics.values()]))
        disagreement_metrics["overall"] = {
            "total_entropy": total_entropy,
            "disagreement_level": "Low" if total_entropy < 2 else "Medium" if total_entropy < 3 else "High"
        }

        return disagreement_metrics

    def create_disagreement_preserving_distributions(self, integrated_forecasts, disagreement_metrics):
        """Create distributions that preserve disagreement between sources"""
        logger.info("Creating disagreement-preserving distributions...")

        # Create CDFs (cumulative distribution functions) for each milestone
        cdf_data = {}

        for milestone, forecast in integrated_forecasts.items():
            years = forecast["year_dist"]
            probs = forecast["prob_dist"]

            # Calculate cumulative probabilities
            cumulative_probs = []
            cumulative = 0.0
            cumulative_probs_by_year = {}

            for year, prob in zip(years, probs):
                cumulative += prob
                cumulative_probs.append(float(cumulative))
                cumulative_probs_by_year[str(int(year))] = float(cumulative)

            cdf_data[milestone] = {
                "years": [int(y) for y in years],
                "cdf": cumulative_probs,
                "cdf_by_year": cumulative_probs_by_year,
                "disagreement": float(disagreement_metrics[milestone]["entropy"])
            }

        return cdf_data

    def generate_forecast_report(self, source_forecasts, integrated_forecasts,
                               disagreement_metrics, cdf_data):
        """Generate comprehensive forecast integration report"""
        report = []
        report.append("=" * 60)
        report.append("HSRI-Proxy v0.1 Forecast Integration Report")
        report.append(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        # Executive Summary
        report.append("\n## EXECUTIVE SUMMARY")
        report.append(f"Forecast sources integrated: {len(source_forecasts)}")
        report.append(f"Capability milestones: {len(integrated_forecasts)}")
        report.append(f"Overall disagreement level: {disagreement_metrics['overall']['disagreement_level']}")

        # Source Analysis
        report.append("\n## FORECAST SOURCE ANALYSIS")
        for source_name, source_info in self.define_forecast_sources().items():
            report.append(f"### {source_info['name']} ({source_info['weight']:.0%} weight)")
            report.append(f"Description: {source_info['description']}")
            report.append(f"Confidence: {source_info['confidence']:.0%}")
            report.append(f"Examples: {', '.join(source_info['examples'][:2])}")

        # Integrated Forecasts
        report.append("\n## INTEGRATED FORECASTS")
        for milestone, forecast in integrated_forecasts.items():
            report.append(f"### Level {milestone}: {self.define_capability_milestones()[milestone]['name']}")
            report.append(f"Median Year: {forecast['median_year']}")
            report.append(f"Mean Year: {forecast['mean_year']}")
            report.append(f"Confidence: {forecast['confidence']:.0%}")
            report.append(f"25th-75th Percentile: {forecast['confidence_interval'] if 'confidence_interval' in forecast else 'N/A'}")

        # Disagreement Analysis
        report.append("\n## DISAGREEMENT ANALYSIS")
        report.append(f"Overall Entropy: {disagreement_metrics['overall']['total_entropy']:.2f}")
        report.append("Milestone-Level Disagreement:")

        for milestone, metrics in disagreement_metrics.items():
            if milestone != "overall":
                report.append(f"- Level {milestone}: {metrics['disagreement_level']} (entropy: {metrics['entropy']:.2f})")

        # CDF Information
        report.append("\n## CDF INFORMATION")
        report.append("Cumulative distribution functions created for each milestone:")
        report.append("- Shows probability of achievement by each year")
        report.append("- Preserves source disagreement")
        report.append("- Enables timeline synthesis integration")

        # Methodology
        report.append("\n## METHODOLOGY")
        report.append("### Integration Process")
        report.append("1. Source Weighting: Expert (40%), Platform (30%), Model-based (20%), Lab (10%), Skeptical (10%)")
        report.append("2. Probability Combination: Weighted average of source predictions")
        report.append("3. Confidence Adjustment: Source confidence applied as multiplier")
        report.append("4. Entropy Calculation: Measures disagreement between sources")

        report.append("\n### Uncertainty Preservation")
        report.append("- Maintains source variation in final distributions")
        report.append("- Higher weight sources have greater influence")
        report.append("- Entropy quantifies disagreement level")

        # Limitations
        report.append("\n## LIMITATIONS")
        report.append("1. Synthetic Data: Real forecast data would improve accuracy")
        report.append("2. Source Assumptions: Weights and confidence estimates subjective")
        report.append("3. Timeline Uncertainty: Cannot predict breakthrough timing")
        report.append("4. Cultural Variation: Different regions may have different projections")

        # Save results
        # Save integrated forecasts
        integrated_df = pd.DataFrame({
            milestone: {
                "median_year": f["median_year"],
                "mean_year": f["mean_year"],
                "confidence": f["confidence"]
            } for milestone, f in integrated_forecasts.items()
        }).T
        integrated_df.to_csv(self.data_dir / "integrated_forecasts.csv")

        # Save disagreement metrics
        disagreement_df = pd.DataFrame(disagreement_metrics).T
        disagreement_df.to_csv(self.data_dir / "forecast_disagreement.csv")

        # Save CDF data
        with open(self.data_dir / "forecast_cdfs.json", 'w', encoding='utf-8') as f:
            json.dump(cdf_data, f, indent=2)

        # Write report
        report_file = self.project_root / "research" / "forecast_integration_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        logger.info(f"Forecast integration report saved to {report_file}")

        return {
            "source_forecasts": source_forecasts,
            "integrated_forecasts": integrated_forecasts,
            "disagreement_metrics": disagreement_metrics,
            "cdf_data": cdf_data,
            "report_file": report_file
        }

    def run_forecast_integration(self):
        """Run complete forecast integration process"""
        logger.info("Starting forecast integration...")

        # Generate forecast data
        source_forecasts = self.generate_forecast_data()

        # Integrate forecasts
        integrated_forecasts = self.integrate_forecasts(source_forecasts)

        # Calculate disagreement metrics
        disagreement_metrics = self.calculate_disagreement_metrics(integrated_forecasts)

        # Create disagreement-preserving distributions
        cdf_data = self.create_disagreement_preserving_distributions(
            integrated_forecasts, disagreement_metrics
        )

        # Generate report
        results = self.generate_forecast_report(
            source_forecasts, integrated_forecasts, disagreement_metrics, cdf_data
        )

        logger.info("✅ Forecast integration completed successfully")
        return True

def main():
    """Run the forecast integration process"""
    project_root = Path.cwd()
    integrator = ForecastIntegrator(project_root)

    if integrator.run_forecast_integration():
        print("\n✅ Forecast integration completed successfully!")
        return 0
    else:
        print("\n❌ Forecast integration failed!")
        return 1

if __name__ == "__main__":
    exit(main())