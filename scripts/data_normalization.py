#!/usr/bin/env python3
"""
Data Normalization Script for HSRI-Proxy v0.1

Normalizes indicator values to common scale using repository-recommended methods.
Applies OECD/JRC Handbook methodology with non-compensatory thresholds.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from scipy import stats
from scipy.stats import rankdata

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataNormalizer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.normalization_results = {}

    def load_data(self):
        """Load all required data files"""
        try:
            # Load indicators
            self.indicators = pd.read_csv(self.data_dir / "indicators.csv")

            # Load harmonized raw observations if available
            harmonized_path = self.data_dir / "raw_observations_harmonized.csv"
            if harmonized_path.exists():
                self.observations = pd.read_csv(harmonized_path)
                logger.info("✓ Loaded harmonized observations from %s", harmonized_path)
            else:
                self.observations = pd.read_csv(self.data_dir / "observations.csv")

            # Load sources
            self.sources = pd.read_csv(self.data_dir / "sources.csv")

            # Load coverage
            self.coverage = pd.read_csv(self.data_dir / "coverage-by-country.csv")

            logger.info("✓ All data files loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error loading data: {str(e)}")
            return False

    def normalize_value(self, values, method):
        """Normalize values using specified method to [0, 1] range while preserving NaNs"""
        values = np.array(values, dtype=float)
        mask = ~np.isnan(values)
        if not np.any(mask):
            return values

        normalized = np.full_like(values, np.nan)
        valid_vals = values[mask].reshape(-1, 1)

        if method == "min-max":
            scaler = MinMaxScaler()
            norm_valid = scaler.fit_transform(valid_vals).flatten()
        elif method == "z-score":
            scaler = StandardScaler()
            z = scaler.fit_transform(valid_vals).flatten()
            norm_valid = stats.norm.cdf(z)
        elif method == "rank":
            norm_valid = rankdata(valid_vals.flatten(), method='average') / len(valid_vals)
        else:
            raise ValueError(f"Unknown normalization method: {method}")

        normalized[mask] = norm_valid
        return normalized

    def apply_directional_adjustment(self, values, direction):
        """Adjust values based on direction (higher/lower is better) while preserving NaNs"""
        if direction == "lower":
            return np.where(np.isnan(values), np.nan, 1 - values)
        return values

    def normalize_indicator(self, indicator_id):
        """Normalize data for a specific indicator"""
        try:
            # Get indicator metadata
            matches = self.indicators[self.indicators["indicator_id"] == indicator_id]
            if len(matches) == 0:
                logger.warning(f"Indicator metadata not found for {indicator_id}")
                return None
            indicator = matches.iloc[0]

            # Filter observations for this indicator
            obs = self.observations[self.observations["indicator_id"] == indicator_id]

            if len(obs) == 0:
                logger.warning(f"No observations for {indicator_id}")
                return None

            # Get normalization method and direction
            method = indicator.get("normalization", "min-max")
            direction = indicator.get("direction", "higher")

            # Normalize values
            raw_values = obs["value"].values
            normalized = self.normalize_value(raw_values, method)

            # Apply directional adjustment
            normalized = self.apply_directional_adjustment(normalized, direction)

            # Store results
            result = obs.copy()
            result["normalized_value"] = normalized
            result["normalization_method"] = method
            result["normalization_direction"] = direction

            self.normalization_results[indicator_id] = {
                "method": method,
                "direction": direction,
                "min": float(normalized.min()),
                "max": float(normalized.max()),
                "mean": float(normalized.mean()),
                "std": float(normalized.std()),
                "count": len(normalized)
            }

            return result

        except Exception as e:
            logger.error(f"Error normalizing {indicator_id}: {str(e)}")
            return None

    def create_country_indicators_matrix(self):
        """Create matrix of countries x normalized indicators"""
        # Get all retained indicators
        role_filter = self.indicators["role"].astype(str).str.strip().str.lower().isin(["retained", "core"])
        retained_indicators = self.indicators[role_filter]["indicator_id"].tolist()

        # Initialize matrix
        matrix = pd.DataFrame()

        for indicator_id in retained_indicators:
            normalized_data = self.normalize_indicator(indicator_id)

            if normalized_data is not None:
                # Pivot to wide format
                pivot = normalized_data.pivot(
                    index="country_iso3",
                    columns="indicator_id",
                    values="normalized_value"
                )

                if len(matrix) == 0:
                    matrix = pivot
                else:
                    matrix = matrix.merge(pivot, left_index=True, right_index=True, how="outer")

        return matrix

    def apply_coverage_rules(self, matrix):
        """Apply coverage thresholds for pillar and overall scores"""
        # Define pillar structure from indicators catalog with flexible fallback
        pillars = {}
        for pillar_name in ["AI_Literacy", "Critical_Discernment", "Institutional_Governance", "Digital_Infrastructure"]:
            ind_list = self.indicators[self.indicators["pillar"] == pillar_name]["indicator_id"].tolist()
            # Also catch any columns matching prefixes
            if pillar_name == "AI_Literacy":
                extra = [c for c in matrix.columns if c.startswith(("AI_LIT_", "PIAAC_", "PISA_Digital", "UNESCO_STEM", "ITU_Digital", "LINKEDIN_"))]
            elif pillar_name == "Critical_Discernment":
                extra = [c for c in matrix.columns if c.startswith(("META_COG_", "PISA_Fact", "EMLI_", "REUTERS_"))]
            elif pillar_name == "Institutional_Governance":
                extra = [c for c in matrix.columns if c.startswith(("DEC_AGY_", "WGI_", "VDEM_", "Freedom_", "OECD_AI_", "Stanford_"))]
            elif pillar_name == "Digital_Infrastructure":
                extra = [c for c in matrix.columns if c.startswith(("ENAB_", "OXFORD_", "IMF_", "ITU_", "WBDIGITAL_", "WEF_"))]
            else:
                extra = []
            combined = list(dict.fromkeys(ind_list + extra))
            pillars[pillar_name] = [c for c in combined if c in matrix.columns]

        # Calculate pillar scores
        country_scores = pd.DataFrame(index=matrix.index)

        for pillar_name, indicators in pillars.items():
            available_indicators = [i for i in indicators if i in matrix.columns]

            if len(available_indicators) > 0:
                # Calculate mean of available indicators
                pillar_scores = matrix[available_indicators].mean(axis=1)

                # Apply coverage threshold (70% of indicators required)
                coverage_threshold = 0.7
                min_required = max(1, int(np.ceil(len(available_indicators) * coverage_threshold)))

                # Flag countries with sufficient coverage
                sufficient_coverage = (matrix[available_indicators].count(axis=1) >= min_required)

                country_scores[f"{pillar_name}_score"] = pillar_scores.where(sufficient_coverage, np.nan)
                country_scores[f"{pillar_name}_coverage"] = matrix[available_indicators].count(axis=1) / len(available_indicators)
                country_scores[f"{pillar_name}_available"] = len(available_indicators)

        # Calculate overall score (only core pillars)
        core_pillars = ["AI_Literacy", "Critical_Discernment", "Institutional_Governance", "Digital_Infrastructure"]
        available_core = [f"{p}_score" for p in core_pillars if f"{p}_score" in country_scores.columns]

        if len(available_core) > 0:
            country_scores["overall_score"] = country_scores[available_core].mean(axis=1)

            # Status classification
            def get_status(row):
                core_pillars_with_data = sum(1 for p in core_pillars if f"{p}_score" in row and pd.notna(row[f"{p}_score"]))

                if core_pillars_with_data == 0:
                    return "Not rated"
                elif core_pillars_with_data < 2:
                    return "Insufficient core pillars"
                elif row["overall_score"] >= 0.8:
                    return "Strong capacity"
                elif row["overall_score"] >= 0.6:
                    return "Moderate capacity"
                elif row["overall_score"] >= 0.4:
                    return "Developing capacity"
                else:
                    return "Limited capacity"

            country_scores["status"] = country_scores.apply(get_status, axis=1)

        return country_scores

    def generate_normalization_report(self):
        """Generate report of normalization results"""
        report = []
        report.append("=" * 60)
        report.append("HSRI-Proxy v0.1 Data Normalization Report")
        report.append(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        # Summary statistics
        report.append(f"\nNORMALIZATION SUMMARY:")
        report.append(f"Total indicators processed: {len(self.normalization_results)}")
        report.append(f"Normalization methods used:")

        method_counts = {}
        for result in self.normalization_results.values():
            method = result["method"]
            method_counts[method] = method_counts.get(method, 0) + 1

        for method, count in method_counts.items():
            report.append(f"  {method}: {count} indicators")

        # Detailed results by indicator
        report.append(f"\nDETAILED NORMALIZATION RESULTS:")

        for indicator_id, result in self.normalization_results.items():
            matches = self.indicators[self.indicators["indicator_id"] == indicator_id]
            name = matches.iloc[0]["name"] if len(matches) > 0 else indicator_id
            direction = matches.iloc[0]["direction"] if len(matches) > 0 else "higher"

            report.append(f"\n{indicator_id} - {name}")
            report.append(f"  Method: {result['method']}")
            report.append(f"  Direction: {direction}")
            report.append(f"  Values: {result['count']} observations")
            report.append(f"  Normalized range: {result['min']:.3f} - {result['max']:.3f}")
            report.append(f"  Mean: {result['mean']:.3f} (σ={result['std']:.3f})")

        # Write report
        report_file = self.project_root / "research" / "normalization_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        logger.info(f"Normalization report saved to {report_file}")
        return report_file

    def run_normalization(self):
        """Run complete normalization process"""
        logger.info("Starting data normalization process...")

        # Load data
        if not self.load_data():
            return False

        # Create normalized indicators matrix
        logger.info("Creating normalized indicators matrix...")
        normalized_matrix = self.create_country_indicators_matrix()

        # Apply coverage rules
        logger.info("Applying coverage rules...")
        country_scores = self.apply_coverage_rules(normalized_matrix)

        # Save results
        # Save normalized matrix
        normalized_matrix.round(4).to_csv(self.data_dir / "normalized_indicators.csv")

        # Save country scores
        country_scores.round(4).to_csv(self.data_dir / "country_scores.csv")

        # Generate report
        report_file = self.generate_normalization_report()

        logger.info("✓ Normalization completed successfully")
        return True

def main():
    """Run the normalization process"""
    project_root = Path.cwd()
    normalizer = DataNormalizer(project_root)

    if normalizer.run_normalization():
        logger.info("✓ Normalization process completed successfully!")
        return 0
    else:
        logger.error("✗ Normalization process failed!")
        return 1

if __name__ == "__main__":
    exit(main())