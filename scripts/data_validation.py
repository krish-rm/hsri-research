#!/usr/bin/env python3
"""
Automated Data Quality Assurance Pipeline for HSRI-Proxy v0.1

Validates data integrity, checks for missing values, verifies country codes,
and ensures compliance with provenance requirements.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataValidator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.validation_results = []

    def validate_sources_catalog(self):
        """Validate the sources.csv file for completeness"""
        sources_file = self.data_dir / "sources.csv"

        if not sources_file.exists():
            self.validation_results.append({
                "category": "Sources Catalog",
                "check": "File Exists",
                "status": "FAIL",
                "message": "sources.csv not found"
            })
            return False

        try:
            df = pd.read_csv(sources_file)

            # Check required columns
            required_columns = [
                "source_id", "publisher", "title", "publication_date",
                "url", "retrieved_at", "license", "method_summary"
            ]

            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                self.validation_results.append({
                    "category": "Sources Catalog",
                    "check": "Required Columns",
                    "status": "FAIL",
                    "message": f"Missing columns: {missing_cols}"
                })
                return False

            # Check for empty required fields
            empty_required = []
            for col in required_columns:
                if df[col].isna().any():
                    empty_required.extend(df[df[col].isna()].index.tolist())

            if empty_required:
                self.validation_results.append({
                    "category": "Sources Catalog",
                    "check": "Empty Required Fields",
                    "status": "FAIL",
                    "message": f"Empty required fields at rows: {empty_required}"
                })
                return False

            # Check unique source IDs
            if df["source_id"].duplicated().any():
                duplicates = df[df["source_id"].duplicated()]["source_id"].tolist()
                self.validation_results.append({
                    "category": "Sources Catalog",
                    "check": "Unique Source IDs",
                    "status": "FAIL",
                    "message": f"Duplicate source IDs: {duplicates}"
                })
                return False

            self.validation_results.append({
                "category": "Sources Catalog",
                "check": "Basic Validation",
                "status": "PASS",
                "message": "Sources catalog is valid"
            })
            return True

        except Exception as e:
            self.validation_results.append({
                "category": "Sources Catalog",
                "check": "File Readability",
                "status": "FAIL",
                "message": f"Error reading sources.csv: {str(e)}"
            })
            return False

    def validate_observations(self):
        """Validate observations data structure and integrity"""
        obs_file = self.data_dir / "observations.csv"

        if not obs_file.exists():
            self.validation_results.append({
                "category": "Observations Data",
                "check": "File Exists",
                "status": "FAIL",
                "message": "observations.csv not found"
            })
            return False

        try:
            df = pd.read_csv(obs_file)

            # Check required columns
            required_columns = [
                "country_iso3", "country_name", "indicator_id",
                "value", "year", "unit", "source_id"
            ]

            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                self.validation_results.append({
                    "category": "Observations Data",
                    "check": "Required Columns",
                    "status": "FAIL",
                    "message": f"Missing columns: {missing_cols}"
                })
                return False

            # Validate country codes (ISO 3166-1 alpha-3)
            invalid_countries = df[~df["country_iso3"].str.match(r'^[A-Z]{3}$')]["country_iso3"].unique()
            if len(invalid_countries) > 0:
                self.validation_results.append({
                    "category": "Observations Data",
                    "check": "ISO Country Codes",
                    "status": "FAIL",
                    "message": f"Invalid country codes: {invalid_countries.tolist()}"
                })
                return False

            # Check for negative values where inappropriate
            numeric_cols = ["value", "year"]
            for col in numeric_cols:
                if col in df.columns:
                    if (df[col] < 0).any():
                        self.validation_results.append({
                            "category": "Observations Data",
                            "check": f"{col} Values",
                            "status": "FAIL",
                            "message": f"Negative values found in {col}"
                        })
                        return False

            # Check year format and reasonableness
            current_year = datetime.now().year
            if df["year"].max() > current_year + 1:
                self.validation_results.append({
                    "category": "Observations Data",
                    "check": "Year Values",
                    "status": "FAIL",
                    "message": "Contains future years beyond current + 1"
                })
                return False

            # Check if all sources exist in sources catalog
            sources_df = pd.read_csv(self.data_dir / "sources.csv")
            valid_sources = set(sources_df["source_id"])
            obs_sources = set(df["source_id"])
            invalid_sources = obs_sources - valid_sources

            if invalid_sources:
                self.validation_results.append({
                    "category": "Observations Data",
                    "check": "Source References",
                    "status": "FAIL",
                    "message": f"References to non-existent sources: {list(invalid_sources)}"
                })
                return False

            self.validation_results.append({
                "category": "Observations Data",
                "check": "Basic Validation",
                "status": "PASS",
                "message": "Observations data is valid"
            })
            return True

        except Exception as e:
            self.validation_results.append({
                "category": "Observations Data",
                "check": "File Readability",
                "status": "FAIL",
                "message": f"Error reading observations.csv: {str(e)}"
            })
            return False

    def validate_indicators(self):
        """Validate indicators framework"""
        indicators_file = self.data_dir / "indicators.csv"

        if not indicators_file.exists():
            self.validation_results.append({
                "category": "Indicators Framework",
                "check": "File Exists",
                "status": "FAIL",
                "message": "indicators.csv not found"
            })
            return False

        try:
            df = pd.read_csv(indicators_file)

            # Check required columns
            required_columns = [
                "indicator_id", "subcomponent", "pillar",
                "validity_rating", "role"
            ]

            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                self.validation_results.append({
                    "category": "Indicators Framework",
                    "check": "Required Columns",
                    "status": "FAIL",
                    "message": f"Missing columns: {missing_cols}"
                })
                return False

            # Check validity ratings
            valid_ratings = {"High", "Medium", "Low"}
            invalid_ratings = set(df["validity_rating"].unique()) - valid_ratings
            if invalid_ratings:
                self.validation_results.append({
                    "category": "Indicators Framework",
                    "check": "Validity Ratings",
                    "status": "FAIL",
                    "message": f"Invalid validity ratings: {invalid_ratings}"
                })
                return False

            # Check role consistency
            valid_roles = {"Retained", "Context-only", "Rejected", "Not measurable"}
            invalid_roles = set(df["role"].unique()) - valid_roles
            if invalid_roles:
                self.validation_results.append({
                    "category": "Indicators Framework",
                    "check": "Role Classifications",
                    "status": "FAIL",
                    "message": f"Invalid role classifications: {invalid_roles}"
                })
                return False

            self.validation_results.append({
                "category": "Indicators Framework",
                "check": "Basic Validation",
                "status": "PASS",
                "message": "Indicators framework is valid"
            })
            return True

        except Exception as e:
            self.validation_results.append({
                "category": "Indicators Framework",
                "check": "File Readability",
                "status": "FAIL",
                "message": f"Error reading indicators.csv: {str(e)}"
            })
            return False

    def check_coverage_consistency(self):
        """Check if observations match indicators framework"""
        try:
            # Load data
            indicators_df = pd.read_csv(self.data_dir / "indicators.csv")
            obs_df = pd.read_csv(self.data_dir / "observations.csv")

            # Get retained indicators
            retained_indicators = set(
                indicators_df[indicators_df["role"] == "Retained"]["indicator_id"]
            )
            all_indicators = set(indicators_df["indicator_id"])

            # Check for observations of non-existent indicators
            obs_indicators = set(obs_df["indicator_id"])
            nonexistent = obs_indicators - all_indicators

            if nonexistent:
                self.validation_results.append({
                    "category": "Coverage Consistency",
                    "check": "Indicator Existence",
                    "status": "FAIL",
                    "message": f"Observations for non-existent indicators: {list(nonexistent)}"
                })
                return False

            # Check if retained indicators have observations
            missing_data = retained_indicators - set(obs_df["indicator_id"])

            if missing_data:
                self.validation_results.append({
                    "category": "Coverage Consistency",
                    "check": "Retained Indicators Coverage",
                    "status": "FAIL",
                    "message": f"Retained indicators without observations: {list(missing_data)}"
                })
                return False

            self.validation_results.append({
                "category": "Coverage Consistency",
                "check": "Data Coverage",
                "status": "PASS",
                "message": "Data coverage is consistent with indicators framework"
            })
            return True

        except Exception as e:
            self.validation_results.append({
                "category": "Coverage Consistency",
                "check": "File Readability",
                "status": "FAIL",
                "message": f"Error checking coverage: {str(e)}"
            })
            return False

    def generate_report(self):
        """Generate validation report"""
        report = []
        report.append("=" * 60)
        report.append("HSRI-Proxy v0.1 Data Quality Validation Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        # Summary
        total_checks = len(self.validation_results)
        passed = sum(1 for r in self.validation_results if r["status"] == "PASS")
        failed = total_checks - passed

        report.append(f"\nSUMMARY:")
        report.append(f"Total checks performed: {total_checks}")
        report.append(f"Passed: {passed}")
        report.append(f"Failed: {failed}")

        # Details by category
        report.append(f"\nDETAILED RESULTS:")

        for result in self.validation_results:
            status_icon = "✓" if result["status"] == "PASS" else "✗"
            report.append(f"\n{status_icon} {result['category']} - {result['check']}")
            report.append(f"   Status: {result['status']}")
            report.append(f"   Message: {result['message']}")

        # Recommendations
        if failed > 0:
            report.append(f"\nRECOMMENDATIONS:")
            report.append("Please address failed checks before proceeding to analysis")
        else:
            report.append(f"\n✓ All validations passed! Data is ready for analysis.")

        # Write report
        report_file = self.project_root / "research" / "validation_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        logger.info(f"Validation report saved to {report_file}")
        return report_file

def main():
    """Run the complete validation pipeline"""
    # Get project root from current directory
    project_root = Path.cwd()

    validator = DataValidator(project_root)

    # Run all validations
    validations = [
        validator.validate_sources_catalog(),
        validator.validate_observations(),
        validator.validate_indicators(),
        validator.check_coverage_consistency()
    ]

    # Generate report
    report_file = validator.generate_report()

    if all(validations):
        logger.info("✓ All validations passed!")
        return 0
    else:
        logger.error("✗ Some validations failed. See report for details.")
        return 1

if __name__ == "__main__":
    exit(main())