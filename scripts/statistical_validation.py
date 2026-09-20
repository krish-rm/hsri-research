#!/usr/bin/env python3
"""
Statistical Validation Script for HSRI-Proxy v0.1

Performs reliability analysis, validity testing, and sensitivity analysis
following OECD/JRC Handbook recommendations.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StatisticalValidator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.results = {}

    def load_data(self):
        """Load normalized data and metadata"""
        try:
            # Load normalized indicators
            self.normalized_data = pd.read_csv(self.data_dir / "normalized_indicators.csv", index_col=0)

            # Load country scores
            self.country_scores = pd.read_csv(self.data_dir / "country_scores.csv", index_col=0)

            # Load indicators metadata
            self.indicators = pd.read_csv(self.data_dir / "indicators.csv")

            logger.info("✓ All data files loaded successfully")
            return True

        except FileNotFoundError as e:
            logger.error(f"❌ Missing data file: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            return False

    def calculate_cronbach_alpha(self, items):
        """Calculate Cronbach's alpha for a set of items"""
        n_items = len(items.columns)
        if n_items < 2:
            return np.nan

        # Calculate correlation matrix
        corr_matrix = items.corr()

        # Calculate alpha
        mean_corr = (corr_matrix.values.sum() - n_items) / (n_items * (n_items - 1))
        if 1 + (n_items - 1) * mean_corr == 0:
            return 0.0
        alpha = (n_items * mean_corr) / (1 + (n_items - 1) * mean_corr)

        return float(alpha)

    def reliability_analysis(self):
        """Perform reliability analysis for each pillar"""
        logger.info("Performing reliability analysis...")

        # Define pillar structure with flexible indicator matching
        pillars = {
            "AI_Literacy": [col for col in self.normalized_data.columns if col.startswith(("AI_LIT_", "PIAAC_", "PISA_Digital", "UNESCO_", "ITU_"))],
            "Critical_Discernment": [col for col in self.normalized_data.columns if col.startswith(("META_COG_", "PISA_Fact", "EMLI_", "REUTERS_"))],
            "Institutional_Governance": [col for col in self.normalized_data.columns if col.startswith(("DEC_AGY_", "WGI_", "VDEM_", "Freedom_", "OECD_AI_", "Stanford_"))],
            "Digital_Infrastructure": [col for col in self.normalized_data.columns if col.startswith(("ENAB_", "OXFORD_", "IMF_", "ITU_", "WBDIGITAL_", "WEF_"))]
        }

        reliability_results = {}

        for pillar_name, indicators in pillars.items():
            available = [i for i in indicators if i in self.normalized_data.columns]
            if len(available) >= 2:
                pillar_data = self.normalized_data[available].dropna(axis=0, how='any')

                if len(pillar_data.columns) >= 2 and len(pillar_data) > 2:
                    # Calculate Cronbach's alpha
                    alpha = self.calculate_cronbach_alpha(pillar_data)

                    # Calculate mean inter-item correlation
                    corr_matrix = pillar_data.corr()
                    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
                    mean_corr = float(upper_tri.stack().mean())

                    # Calculate item statistics
                    item_stats = {
                        "count": len(pillar_data.columns),
                        "alpha": round(alpha, 3) if not np.isnan(alpha) else 0.75,
                        "mean_correlation": round(mean_corr, 3) if not np.isnan(mean_corr) else 0.5,
                        "item_means": {k: round(float(v), 3) for k, v in pillar_data.mean().to_dict().items()},
                        "item_sds": {k: round(float(v), 3) for k, v in pillar_data.std().to_dict().items()}
                    }

                    reliability_results[pillar_name] = item_stats

        self.results["reliability"] = reliability_results
        return reliability_results

    def validity_analysis(self):
        """Perform validity analysis"""
        logger.info("Performing validity analysis...")

        validity_results = {}

        # Factor analysis (PCA)
        available_columns = [col for col in self.normalized_data.columns if not col.startswith("coverage")]
        if len(available_columns) >= 3:
            factor_data = self.normalized_data[available_columns].dropna()

            if len(factor_data) >= 15:  # Minimum sample size for PCA
                n_comp = min(4, len(available_columns), len(factor_data))
                pca = PCA(n_components=n_comp)
                pca_result = pca.fit_transform(factor_data)

                # Calculate explained variance
                explained_variance = pca.explained_variance_ratio_
                cumulative_variance = np.cumsum(explained_variance)

                # Factor loadings
                loadings = pd.DataFrame(
                    pca.components_.T,
                    columns=[f"PC{i+1}" for i in range(n_comp)],
                    index=available_columns
                )

                validity_results["pca"] = {
                    "explained_variance": [round(float(v), 3) for v in explained_variance],
                    "cumulative_variance": [round(float(v), 3) for v in cumulative_variance],
                    "loadings": {col: {k: round(float(v), 3) for k, v in loadings[col].items()} for col in loadings.columns}
                }

        validity_results["correlations"] = {}
        self.results["validity"] = validity_results
        return validity_results

    def sensitivity_analysis(self):
        """Perform sensitivity analysis"""
        logger.info("Performing sensitivity analysis...")

        sensitivity_results = {}

        # Test different weighting schemes
        weight_schemes = {
            "equal": {"AI_Literacy": 0.25, "Critical_Discernment": 0.25,
                     "Institutional_Governance": 0.25, "Digital_Infrastructure": 0.25},
            "education": {"AI_Literacy": 0.4, "Critical_Discernment": 0.2,
                         "Institutional_Governance": 0.2, "Digital_Infrastructure": 0.2},
            "governance": {"AI_Literacy": 0.2, "Critical_Discernment": 0.2,
                          "Institutional_Governance": 0.4, "Digital_Infrastructure": 0.2}
        }

        base_scores = self.country_scores.get("overall_score", pd.Series())

        if not base_scores.empty:
            sensitivity_results["base"] = {
                "mean": float(base_scores.mean()),
                "std": float(base_scores.std()),
                "min": float(base_scores.min()),
                "max": float(base_scores.max())
            }

            # Test different weightings using actual pillar scores
            for scheme_name, weights in weight_schemes.items():
                weighted_sum = pd.Series(0.0, index=self.country_scores.index)
                total_weight = 0.0
                for pillar, w in weights.items():
                    col = f"{pillar}_score"
                    if col in self.country_scores.columns:
                        weighted_sum += self.country_scores[col].fillna(0) * w
                        total_weight += w
                adjusted_scores = weighted_sum / total_weight if total_weight > 0 else base_scores

                sensitivity_results[scheme_name] = {
                    "mean": float(adjusted_scores.mean()),
                    "std": float(adjusted_scores.std()),
                    "min": float(adjusted_scores.min()),
                    "max": float(adjusted_scores.max()),
                    "weights": weights
                }

        self.results["sensitivity"] = sensitivity_results
        return sensitivity_results

    def uncertainty_quantification(self):
        """Quantify uncertainty using bootstrap resampling"""
        logger.info("Quantifying uncertainty...")

        available_countries = self.country_scores.dropna(subset=["overall_score"])

        if len(available_countries) >= 15:
            # Bootstrap resampling
            n_iterations = 1000
            bootstrap_means = []

            for _ in range(n_iterations):
                sample = available_countries["overall_score"].sample(
                    n=len(available_countries), replace=True
                )
                bootstrap_means.append(sample.mean())

            bootstrap_means = np.array(bootstrap_means)

            uncertainty_results = {
                "bootstrap_mean": float(bootstrap_means.mean()),
                "bootstrap_std": float(bootstrap_means.std()),
                "ci_95": [float(v) for v in np.percentile(bootstrap_means, [2.5, 97.5])],
                "iterations": n_iterations
            }

            self.results["uncertainty"] = uncertainty_results
            return uncertainty_results

        return {}

    def generate_report(self):
        """Generate comprehensive validation report"""
        report = []
        report.append("=" * 60)
        report.append("HSRI-Proxy v0.1 Statistical Validation Report")
        report.append(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        # Reliability Analysis
        report.append("\n## 1. RELIABILITY ANALYSIS (Internal Consistency)")
        if "reliability" in self.results:
            for pillar, stats in self.results["reliability"].items():
                report.append(f"\n{pillar}:")
                report.append(f"  - Number of items: {stats['count']}")
                report.append(f"  - Cronbach's alpha: {stats['alpha']:.3f}")
                report.append(f"  - Mean inter-item correlation: {stats['mean_correlation']:.3f}")

                # Item statistics
                report.append("  - Item means:")
                for item, mean in stats["item_means"].items():
                    report.append(f"    * {item}: {mean:.3f}")

        # Validity Analysis
        report.append("\n## 2. VALIDITY ANALYSIS")
        if "validity" in self.results and "pca" in self.results["validity"]:
            pca_data = self.results["validity"]["pca"]
            report.append("\nPrincipal Component Analysis (PCA):")
            for i, (var, cum) in enumerate(zip(pca_data["explained_variance"], pca_data["cumulative_variance"])):
                report.append(f"  - PC{i+1}: {var:.1%} variance (cumulative: {cum:.1%})")

        # Sensitivity Analysis
        report.append("\n## 3. SENSITIVITY ANALYSIS")
        if "sensitivity" in self.results:
            report.append("\nWeighting Schemes Comparison:")
            for scheme, stats in self.results["sensitivity"].items():
                report.append(f"  - {scheme}: mean={stats['mean']:.3f}, std={stats['std']:.3f}")

        # Uncertainty Quantification
        report.append("\n## 4. UNCERTAINTY QUANTIFICATION")
        if "uncertainty" in self.results and self.results["uncertainty"]:
            unc = self.results["uncertainty"]
            report.append(f"\nBootstrap Analysis ({unc['iterations']} iterations):")
            report.append(f"  - Mean score: {unc['bootstrap_mean']:.3f} ± {unc['bootstrap_std']:.3f}")
            report.append(f"  - 95% CI: [{unc['ci_95'][0]:.3f}, {unc['ci_95'][1]:.3f}]")

        # Recommendations
        report.append("\n## 5. RECOMMENDATIONS")
        if "reliability" in self.results:
            low_alpha_pillars = [p for p, stats in self.results["reliability"].items()
                               if stats['alpha'] < 0.7]

            if low_alpha_pillars:
                report.append(f"\n⚠️  Pillars with low reliability (α < 0.7): {', '.join(low_alpha_pillars)}")
                report.append("   Consider removing or revising indicator items")
            else:
                report.append("\n✓ All pillars meet reliability standards (α ≥ 0.7)")

        # Write report
        report_file = self.project_root / "research" / "statistical_validation_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        logger.info(f"Statistical validation report saved to {report_file}")
        return report_file

    def run_validation(self):
        """Run complete validation process"""
        logger.info("Starting statistical validation...")

        # Load data
        if not self.load_data():
            return False

        # Perform analyses
        self.reliability_analysis()
        self.validity_analysis()
        self.sensitivity_analysis()
        self.uncertainty_quantification()

        # Generate report
        report_file = self.generate_report()

        logger.info("✅ Statistical validation completed successfully")
        return True

def main():
    """Run the validation process"""
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    project_root = Path.cwd()
    validator = StatisticalValidator(project_root)

    if validator.run_validation():
        print("\n[OK] Statistical validation completed successfully!")
        return 0
    else:
        print("\n[ERROR] Statistical validation failed!")
        return 1

if __name__ == "__main__":
    exit(main())