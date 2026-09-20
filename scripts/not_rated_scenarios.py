#!/usr/bin/env python3
"""
Not Rated Scenarios for HSRI-Proxy v0.1

Defines scenarios for countries that cannot be fully rated due to
data limitations, special circumstances, or emerging status.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import json
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotRatedScenarios:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.results = {}

    def define_exclusion_categories(self):
        """Define categories of countries that cannot be fully rated"""
        categories = {
            "data_insufficient": {
                "name": "Data Insufficient",
                "description": "Lack adequate data for comprehensive assessment",
                "criteria": [
                    "Less than 50% indicator coverage",
                    "No reliable governance data",
                    "Missing digital infrastructure metrics",
                    "Insufficient education statistics"
                ],
                "examples": ["SMR", "MCO", "LIE"],  # Microstates
                "characteristics": [
                    "Small population size",
                    "Limited statistical capacity",
                    "Unique economic structures"
                ],
                "path_to_rating": [
                    "Develop national statistical systems",
                    "Participate in international data initiatives",
                    "Establish baseline measurements"
                ],
                "recommendations": [
                    "Focus on data collection capacity",
                    "Participate in regional benchmarking",
                    "Develop proxy indicators where appropriate"
                ]
            },

            "conflict_zones": {
                "name": "Conflict Zones",
                "description": "Countries experiencing active conflict or instability",
                "criteria": [
                    "Active armed conflict",
                    "Political instability",
                    "Humanitarian crisis",
                    "Governance breakdown"
                ],
                "examples": ["UKR", "SYR", "YEM", "AFG"],
                "characteristics": [
                    "Emergency focus",
                    "Institutional collapse",
                    "Population displacement",
                    "International intervention"
                ],
                "path_to_rating": [
                    "Stabilization progress",
                    "Governance restoration",
                    "Data collection resumption",
                    "International support"
                ],
                "recommendations": [
                    "Prioritize basic needs and safety",
                    "Support peacebuilding efforts",
                    "Prepare for future assessment",
                    "International coordination"
                ]
            },

            "emerging_economies": {
                "name": "Emerging Economies",
                "description": "Rapidly developing countries with incomplete data",
                "criteria": [
                    "GDP growth > 7% annually",
                    "Digital transformation underway",
                    "Institutional capacity building",
                    "Data quality improving"
                ],
                "examples": ["VNM", "BGD", "LAO", "KGZ"],
                "characteristics": [
                    "Rapid change",
                    "Data lag",
                    "Policy experimentation",
                    "Investment focus"
                ],
                "path_to_rating": [
                    "Data infrastructure development",
                    "Policy stabilization",
                    "Statistical capacity building",
                    "International benchmarking"
                ],
                "recommendations": [
                    "Invest in data systems",
                    "Participate in learning networks",
                    "Adopt international standards",
                    "Focus on key indicators"
                ]
            },

            "special_administrative": {
                "name": "Special Administrative Regions",
                "description": "Regions with unique political or administrative status",
                "criteria": [
                    "Special political status",
                    "Autonomous governance",
                    "Different legal frameworks",
                    "Unique economic systems"
                ],
                "examples": ["HKG", "MAC", "TWN", "XKX"],
                "characteristics": [
                    "Separate legal systems",
                    "Distinct economic policies",
                    "International status questions",
                    "Data reporting differences"
                ],
                "path_to_rating": [
                    "Clarify international status",
                    "Standardize data reporting",
                    "Participate in assessment frameworks",
                    "Develop region-specific metrics"
                ],
                "recommendations": [
                    "Develop tailored assessment approach",
                    "Engage with relevant international bodies",
                    "Contribute to methodological development",
                    "Share best practices"
                ]
            },

            "island_nations": {
                "name": "Island Nations",
                "description": "Small island developing states with unique challenges",
                "criteria": [
                    "Island geography",
                    "Climate vulnerability",
                    "Limited resources",
                    "International dependency"
                ],
                "examples": ["MDV", "FJI", "SLB", "VUT"],
                "characteristics": [
                    "Geographic isolation",
                    "Environmental constraints",
                    "Tourism dependency",
                    "International aid reliance"
                ],
                "path_to_rating": [
                    "Data capacity building",
                    "Regional cooperation",
                    "Climate resilience integration",
                    "International support coordination"
                ],
                "recommendations": [
                    "Focus on resilience indicators",
                    "Participate in regional networks",
                    "Leverage international partnerships",
                    "Develop island-specific metrics"
                ]
            }
        }

        return categories

    def define_assessment_gaps(self):
        """Define specific gaps that prevent full assessment"""
        gaps = {
            "data_coverage": {
                "name": "Data Coverage Gap",
                "description": "Insufficient data across multiple pillars",
                "impact": "Cannot calculate composite score",
                "severity": "High",
                "mitigation": "Develop proxy indicators and estimation methods"
            },
            "time_alignment": {
                "name": "Time Alignment Gap",
                "description": "Data points from different time periods",
                "impact": "Cannot assess current readiness accurately",
                "severity": "Medium",
                "mitigation": "Interpolation and forward/backward projection"
            },
            "methodological_applicability": {
                "name": "Methodological Applicability Gap",
                "description": "Methodology not suitable for country context",
                "impact": "Results may not be meaningful or comparable",
                "severity": "High",
                "mitigation": "Develop context-specific adaptation guidelines"
            },
            "political_sensitivity": {
                "name": "Political Sensitivity Gap",
                "description": "Data collection affected by political factors",
                "impact": "Data reliability compromised",
                "severity": "High",
                "mitigation": "Multiple source verification and triangulation"
            },
            "institutional_capacity": {
                "name": "Institutional Capacity Gap",
                "description": "Lack of capacity to provide reliable data",
                "impact": "Data quality and consistency issues",
                "severity": "Medium",
                "mitigation": "Capacity building programs and support"
            }
        }

        return gaps

    def create_scenario_templates(self):
        """Create templates for each not-rated scenario"""
        logger.info("Creating not-rated scenario templates...")

        exclusion_categories = self.define_exclusion_categories()
        assessment_gaps = self.define_assessment_gaps()

        templates = {}

        for category_name, category_info in exclusion_categories.items():
            template = {
                "category": category_name,
                "name": category_info["name"],
                "description": category_info["description"],
                "criteria": category_info["criteria"],
                "characteristics": category_info["characteristics"],
                "path_to_rating": category_info["path_to_rating"],
                "recommendations": category_info["recommendations"],
                "assessment_gaps": [],
                "timeline_assessment": {
                    "current_status": "Unable to assess",
                    "projection_available": False,
                    "confidence_level": "None",
                    "key_uncertainties": []
                },
                "engagement_strategy": {
                    "immediate_actions": [],
                    "short_term_goals": [],
                    "long_term_vision": []
                }
            }

            # Add relevant assessment gaps
            relevant_gaps = []
            for gap_name, gap_info in assessment_gaps.items():
                # Determine which gaps are most relevant for this category
                if category_name == "data_insufficient" and gap_name in ["data_coverage", "time_alignment"]:
                    relevant_gaps.append(gap_info)
                elif category_name == "conflict_zones" and gap_name in ["political_sensitivity", "institutional_capacity"]:
                    relevant_gaps.append(gap_info)
                elif category_name == "emerging_economies" and gap_name in ["data_coverage", "time_alignment"]:
                    relevant_gaps.append(gap_info)
                elif category_name == "special_administrative" and gap_name in ["methodological_applicability"]:
                    relevant_gaps.append(gap_info)
                elif category_name == "island_nations" and gap_name in ["data_coverage"]:
                    relevant_gaps.append(gap_info)

            template["assessment_gaps"] = relevant_gaps

            # Define engagement strategy
            template["engagement_strategy"]["immediate_actions"] = [
                "Initial data collection assessment",
                "Stakeholder identification",
                "Baseline establishment"
            ]

            template["engagement_strategy"]["short_term_goals"] = [
                "Data quality improvement",
                "Participatory assessment development",
                "Regional collaboration"
            ]

            template["engagement_strategy"]["long_term_vision"] = [
                "Full integration into HSRI-Proxy framework",
                "Contribution to methodology refinement",
                "Knowledge sharing leadership"
            ]

            templates[category_name] = template

        return templates

    def generate_country_scenarios(self):
        """Generate specific scenarios for not-rated countries"""
        logger.info("Generating country-specific scenarios...")

        templates = self.create_scenario_templates()
        scenarios = {}

        # Define example countries for each category
        country_assignments = {
            "data_insufficient": ["SMR", "MCO", "LIE", "VAT"],
            "conflict_zones": ["UKR", "SYR", "YEM", "AFG"],
            "emerging_economies": ["VNM", "BGD", "LAO", "KGZ"],
            "special_administrative": ["HKG", "MAC", "TWN", "XKX"],
            "island_nations": ["MDV", "FJI", "SLB", "VUT"]
        }

        for category_name, countries in country_assignments.items():
            template = templates[category_name]

            for country in countries:
                scenario = {
                    "country": country,
                    "category": category_name,
                    "template": template,
                    "specific_challenges": self._get_country_specific_challenges(country),
                    "context_factors": self._get_country_context(country),
                    "engagement_priorities": self._get_engagement_priorities(country),
                    "monitoring_indicators": self._get_monitoring_indicators(country),
                    "transition_path": self._get_transition_path(country, category_name),
                    "last_assessment": {
                        "date": "2026-09-20",
                        "status": "Not Rated",
                        "reason": template["description"],
                        "next_review": self._get_next_review_date(category_name)
                    }
                }

                scenarios[country] = scenario

        return scenarios

    def _get_country_specific_challenges(self, country):
        """Get country-specific challenges"""
        challenges_map = {
            "SMR": ["Microstate size", "Limited data infrastructure", "Unique economic model"],
            "UKR": ["Active conflict", "Displacement crisis", "Infrastructure damage"],
            "VNM": ["Rapid digital transformation", "Data quality improvement", "Policy experimentation"],
            "HKG": ["Political status uncertainty", "Data reporting differences", "International relations"],
            "MDV": ["Climate vulnerability", "Geographic isolation", "Tourism dependency"]
        }
        return challenges_map.get(country, ["General data limitations"])

    def _get_country_context(self, country):
        """Get country-specific context"""
        context_map = {
            "SMR": ["Population: 33,000", "GDP per capita: $85,000", "Digital adoption: High"],
            "UKR": ["Population: 41M", "Conflict since 2014", "International support: High"],
            "VNM": ["Population: 98M", "GDP growth: 6-7%", "Digital transformation: Accelerating"],
            "HKG": ["Population: 7.5M", "Special Administrative Region", "Financial hub status"],
            "MDV": ["Population: 521K", "Atoll nation", "Climate vulnerability: Extreme"]
        }
        return context_map.get(country, ["Limited context information available"])

    def _get_engagement_priorities(self, country):
        """Get engagement priorities for country"""
        priorities_map = {
            "SMR": ["Data systems development", "Regional integration", "Best practices sharing"],
            "UKR": ["Peacebuilding support", "Data collection resumption", "Capacity rebuilding"],
            "VNM": ["Data quality improvement", "Policy alignment", "International benchmarking"],
            "HKG": ["Status clarification", "Data standardization", "Methodological contribution"],
            "MDV": ["Resilience indicators", "Regional cooperation", "Climate adaptation"]
        }
        return priorities_map.get(country, ["General capacity building"])

    def _get_monitoring_indicators(self, country):
        """Get monitoring indicators for transition"""
        indicators_map = {
            "SMR": ["Data coverage improvement", "Statistical capacity development"],
            "UKR": ["Conflict resolution progress", "Governance restoration", "Data collection resumption"],
            "VNM": ["Data quality metrics", "Policy stability indicators", "Digital maturity"],
            "HKG": ["International status progress", "Data harmonization", "Assessment readiness"],
            "MDV": ["Climate resilience progress", "Data infrastructure development", "Regional integration"]
        }
        return indicators_map.get(country, ["General progress indicators"])

    def _get_transition_path(self, country, category):
        """Get transition path to full rating"""
        path_map = {
            "data_insufficient": "Data Coverage → Full Assessment",
            "conflict_zones": "Stabilization → Governance → Assessment",
            "emerging_economies": "Data Quality → Policy Stability → Full Rating",
            "special_administrative": "Status Clarification → Methodological Adaptation → Full Rating",
            "island_nations": "Resilience Building → Regional Integration → Full Rating"
        }
        return path_map.get(category, "General Development Path")

    def _get_next_review_date(self, category):
        """Get next review date based on category"""
        review_map = {
            "data_insufficient": "2027-12-31",
            "conflict_zones": "2028-06-30",
            "emerging_economies": "2027-06-30",
            "special_administrative": "2027-12-31",
            "island_nations": "2027-12-31"
        }
        return review_map.get(category, "2027-12-31")

    def create_assessment_framework(self):
        """Create framework for future assessment of not-rated countries"""
        logger.info("Creating assessment framework...")

        framework = {
            "reassessment_triggers": [
                "Significant political change",
                "Data quality improvement",
                "International status clarification",
                "Conflict resolution progress",
                "Economic stabilization",
                "Statistical capacity building"
            ],
            "monitoring_frequency": {
                "data_insufficient": "Quarterly",
                "conflict_zones": "Biannual (when stable)",
                "emerging_economies": "Quarterly",
                "special_administrative": "Biannual",
                "island_nations": "Quarterly"
            },
            "progress_indicators": [
                "Data coverage percentage",
                "Data quality scores",
                "Political stability index",
                "Economic indicators",
                "Statistical capacity metrics",
                "International cooperation levels"
            ],
            "reassessment_criteria": {
                "data_sufficient": "70%+ indicator coverage with recent data",
                "political_stable": "No active conflict or major instability",
                "methodological_applicable": "Framework can be applied meaningfully",
                "data_reliable": "Multiple sources confirm key indicators"
            },
            "review_process": {
                "step_1": "Data collection assessment",
                "step_2": "Stakeholder consultation",
                "step_3": "Methodological review",
                "step_4": "Expert panel evaluation",
                "step_5": "Final determination"
            }
        }

        return framework

    def export_scenarios(self, scenarios, framework):
        """Export not-rated scenarios"""
        logger.info("Exporting not-rated scenarios...")

        # Export scenarios directory
        scenarios_dir = self.project_root / "research" / "not_rated_scenarios"
        scenarios_dir.mkdir(exist_ok=True)

        # Export individual scenarios
        for country, scenario in scenarios.items():
            scenario_file = scenarios_dir / f"{country.lower()}_scenario.json"
            with open(scenario_file, 'w', encoding='utf-8') as f:
                json.dump(scenario, f, indent=2)

        # Export templates
        templates_file = scenarios_dir / "templates.json"
        with open(templates_file, 'w', encoding='utf-8') as f:
            json.dump(self.create_scenario_templates(), f, indent=2)

        # Export framework
        framework_file = scenarios_dir / "assessment_framework.json"
        with open(framework_file, 'w', encoding='utf-8') as f:
            json.dump(framework, f, indent=2)

        # Export summary report
        summary_file = scenarios_dir / "summary_report.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_summary_report(scenarios, framework))

        logger.info(f"Not-rated scenarios exported to {scenarios_dir}")

        return {
            "scenarios": scenarios,
            "framework": framework,
            "scenarios_dir": scenarios_dir,
            "summary_file": summary_file
        }

    def _generate_summary_report(self, scenarios, framework):
        """Generate summary report for not-rated scenarios"""
        report = []
        report.append("# Not Rated Countries Scenarios Summary\n")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"Countries with scenarios: {len(scenarios)}\n\n")

        # Category distribution
        categories = {}
        for country, scenario in scenarios.items():
            category = scenario["category"]
            categories[category] = categories.get(category, 0) + 1

        report.append("## Category Distribution\n")
        for category, count in categories.items():
            report.append(f"- {category.replace('_', ' ').title()}: {count} countries\n")
        report.append("\n")

        # Country listing by category
        report.append("## Countries by Category\n")
        for category_name in categories.keys():
            countries = [c for c, s in scenarios.items() if s["category"] == category_name]
            report.append(f"### {category_name.replace('_', ' ').title()}\n")
            for country in sorted(countries):
                report.append(f"- {country}\n")
            report.append("\n")

        # Assessment framework summary
        report.append("## Assessment Framework\n")
        report.append("### Reassessment Triggers\n")
        for trigger in framework["reassessment_triggers"]:
            report.append(f"- {trigger}\n")
        report.append("\n")

        report.append("### Monitoring Frequency\n")
        for category, frequency in framework["monitoring_frequency"].items():
            report.append(f"- {category.replace('_', ' ').title()}: {frequency}\n")
        report.append("\n")

        report.append("### Progress Indicators\n")
        for indicator in framework["progress_indicators"]:
            report.append(f"- {indicator}\n")
        report.append("\n")

        # Next review dates
        report.append("## Next Review Dates\n")
        for category in categories.keys():
            country_example = [c for c, s in scenarios.items() if s["category"] == category][0]
            next_review = scenarios[country_example]["last_assessment"]["next_review"]
            report.append(f"- {category.replace('_', ' ').title()}: {next_review}\n")
        report.append("\n")

        # Transition paths
        report.append("## Transition Paths to Full Rating\n")
        for category in categories.keys():
            country_example = [c for c, s in scenarios.items() if s["category"] == category][0]
            transition = scenarios[country_example]["transition_path"]
            report.append(f"- {category.replace('_', ' ').title()}: {transition}\n")
        report.append("\n")

        return '\n'.join(report)

    def run_not_rated_scenarios(self):
        """Run complete not-rated scenarios process"""
        logger.info("Starting not-rated scenarios generation...")

        # Generate country scenarios
        scenarios = self.generate_country_scenarios()

        # Create assessment framework
        framework = self.create_assessment_framework()

        # Export scenarios
        results = self.export_scenarios(scenarios, framework)

        logger.info("✅ Not-rated scenarios completed successfully")
        return True

def main():
    """Run the not-rated scenarios process"""
    project_root = Path.cwd()
    processor = NotRatedScenarios(project_root)

    if processor.run_not_rated_scenarios():
        print("\n✅ Not-rated scenarios completed successfully!")
        return 0
    else:
        print("\n❌ Not-rated scenarios failed!")
        return 1

if __name__ == "__main__":
    exit(main())