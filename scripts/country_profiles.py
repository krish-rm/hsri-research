#!/usr/bin/env python3
"""
Country Profiles for HSRI-Proxy v0.1

Creates data-driven country profiles integrating timeline projections,
exposure models, and readiness scores for comprehensive country assessment.
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
import json
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CountryProfileGenerator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.results = {}

        # Profile parameters
        self.current_year = 2026
        self.projection_years = 20

    def load_data(self):
        """Load all required data files"""
        try:
            # Load index results from Phase 3
            self.country_scores = pd.read_csv(self.data_dir / "final_country_scores.csv", index_col=0)

            # Load exposure model results from Phase 4
            self.exposure_scores = pd.read_csv(self.data_dir / "composite_exposure_scores.csv", index_col=0)
            self.gap_analysis = pd.read_csv(self.data_dir / "readiness_exposure_gap.csv", index_col=0)
            self.crossing_years = pd.read_csv(self.data_dir / "scenario_crossing_years.csv", index_col=0)

            # Load timeline data from Phase 5
            self.timeline_data = pd.read_csv(self.data_dir / "ai_forecast_data.csv", index_col=0)
            self.readiness_trajectories = pd.read_csv(self.data_dir / "readiness_trajectories.csv", index_col=0)

            logger.info("✓ All data files loaded successfully")
            return True

        except FileNotFoundError as e:
            logger.error(f"❌ Missing data file: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            return False

    def define_country_categories(self):
        """Define country categories based on readiness and exposure"""
        categories = {
            "prepared": {
                "readiness_threshold": 0.7,
                "exposure_threshold": 0.4,
                "description": "High readiness with moderate exposure",
                "characteristics": ["Strong institutions", "Advanced digital infrastructure", "High education levels"],
                "recommendations": ["Maintain leadership", "Share best practices", "Contribute to global standards"]
            },
            "developing": {
                "readiness_threshold": 0.5,
                "exposure_threshold": 0.6,
                "description": "Moderate readiness with high exposure",
                "characteristics": ["Growing digital economy", "Educational investment", "Institutional development"],
                "recommendations": ["Focus on education", "Build digital infrastructure", "Regional cooperation"]
            },
            "vulnerable": {
                "readiness_threshold": 0.4,
                "exposure_threshold": 0.7,
                "description": "Low readiness with high exposure",
                "characteristics": ["Limited digital access", "Educational gaps", "Institutional challenges"],
                "recommendations": ["International support", "Basic digital access", "Capacity building"]
            },
            "at_risk": {
                "readiness_threshold": 0.3,
                "exposure_threshold": 0.8,
                "description": "Critical readiness-exposure gap",
                "characteristics": ["Severe institutional challenges", "Limited resources", "High vulnerability"],
                "recommendations": ["Emergency measures", "International assistance", "Basic needs focus"]
            }
        }
        return categories

    def define_peer_groups(self):
        """Define peer comparison groups"""
        peer_groups = {
            "high_income": ["USA", "GBR", "DEU", "FRA", "JPN"],
            "upper_middle": ["CHN", "RUS", "BRA", "IND", "MEX"],
            "lower_middle": ["IDN", "EGY", "NGA", "PAK", "ETH"],
            "regional_leaders": {
                "North America": ["USA"],
                "Europe": ["GBR", "DEU", "FRA"],
                "Asia": ["JPN", "CHN", "IND"],
                "Latin America": ["BRA", "MEX"],
                "Africa": ["NGA", "EGY", "ETH"],
                "Middle East": ["RUS", "IDN", "PAK"]
            }
        }
        return peer_groups

    def classify_countries(self):
        """Classify countries based on readiness and exposure"""
        logger.info("Classifying countries by readiness and exposure...")

        categories = self.define_country_categories()
        classifications = {}

        for country in self.gap_analysis.index:
            # Get readiness and exposure scores
            if "overall_score" in self.gap_analysis.columns:
                readiness = self.gap_analysis.loc[country, "overall_score"]
            else:
                readiness = 0.5

            if "composite_exposure" in self.gap_analysis.columns:
                exposure = self.gap_analysis.loc[country, "composite_exposure"]
            else:
                exposure = 0.5

            # Classify based on thresholds
            category = "unclassified"
            for cat_name, cat_info in categories.items():
                if (readiness >= cat_info["readiness_threshold"] and
                    exposure <= cat_info["exposure_threshold"]):
                    category = cat_name
                    break
                elif (readiness >= cat_info["readiness_threshold"] * 0.8 and
                      exposure <= cat_info["exposure_threshold"] * 1.2):
                    category = f"transitioning_{cat_name}"
                    break

            classifications[country] = {
                "readiness": readiness,
                "exposure": exposure,
                "gap": exposure - readiness,
                "category": category,
                "year_2026": {
                    "status": self._get_status_2026(country, readiness, exposure)
                }
            }

        return classifications

    def _get_status_2026(self, country, readiness, exposure):
        """Determine 2026 status for country"""
        if readiness > 0.7:
            return "Leading"
        elif readiness > 0.5 and exposure < 0.6:
            return "Competitive"
        elif readiness > 0.4 and exposure < 0.7:
            return "Developing"
        elif exposure > 0.7:
            return "Vulnerable"
        else:
            return "At Risk"

    def calculate_timeline_projections(self, classifications):
        """Calculate timeline projections for each country"""
        logger.info("Calculating timeline projections...")

        projections = {}

        # Define scenario crossing column mappings
        scenario_cols = [
            ("takeoff", "takeoff_crossing"),
            ("steady_progress", "steady_progress_crossing"),
            ("plateau", "plateau_crossing")
        ]

        for country, info in classifications.items():
            country_projections = {
                "earliest_crossing": None,
                "latest_crossing": None,
                "most_likely_crossing": None,
                "crossing_probability": 0.0,
                "preparation_years": 0,
                "urgency_level": "low"
            }

            # Get crossing years from crossing_years data
            for scenario, col_name in scenario_cols:
                if col_name in self.crossing_years.columns and country in self.crossing_years.index:
                    crossing_year = self.crossing_years.loc[country, col_name]
                    if pd.notna(crossing_year):
                        c_yr = int(round(float(crossing_year)))
                        country_projections[f"{scenario}_crossing"] = c_yr

                        # Calculate most likely crossing (steady_progress scenario)
                        if scenario == "steady_progress":
                            country_projections["most_likely_crossing"] = c_yr

            # Fallback for most likely crossing if steady_progress not found
            if not country_projections.get("most_likely_crossing"):
                if country_projections.get("takeoff_crossing"):
                    country_projections["most_likely_crossing"] = country_projections["takeoff_crossing"]
                elif country_projections.get("plateau_crossing"):
                    country_projections["most_likely_crossing"] = country_projections["plateau_crossing"]

            # Calculate preparation years
            if country_projections["most_likely_crossing"]:
                preparation_years = country_projections["most_likely_crossing"] - self.current_year
                country_projections["preparation_years"] = max(0, preparation_years)

            # Determine urgency level
            if country_projections["most_likely_crossing"]:
                years_to_cross = country_projections["most_likely_crossing"] - self.current_year
                if years_to_cross <= 5:
                    country_projections["urgency_level"] = "critical"
                elif years_to_cross <= 10:
                    country_projections["urgency_level"] = "high"
                elif years_to_cross <= 15:
                    country_projections["urgency_level"] = "medium"
                else:
                    country_projections["urgency_level"] = "low"

            # Calculate crossing probability based on gap
            gap = info["gap"]
            if gap > 0.3:
                country_projections["crossing_probability"] = min(0.9, 0.3 + gap * 0.5)
            elif gap > 0.1:
                country_projections["crossing_probability"] = min(0.6, 0.1 + gap * 0.8)
            else:
                country_projections["crossing_probability"] = max(0.1, gap * 0.3)

            projections[country] = country_projections

        return projections

    def generate_country_narrative(self, country, classifications, projections):
        """Generate narrative for each country"""
        category = classifications[country]
        projection = projections[country]

        # Get category information
        categories = self.define_country_categories()
        category_info = categories.get(category["category"], categories["developing"])

        narrative = {
            "summary": self._generate_summary(country, category, projection),
            "strengths": self._identify_strengths(country, category),
            "challenges": self._identify_challenges(country, category),
            "timeline_outlook": self._describe_timeline(projection),
            "recommendations": self._generate_recommendations(category_info, projection),
            "key_metrics": self._compile_key_metrics(country, category, projection),
            "peer_comparisons": self._get_peer_comparisons(country)
        }

        return narrative

    def _generate_summary(self, country, category, projection):
        """Generate country summary"""
        status_2026 = category["year_2026"]["status"]
        urgency = projection["urgency_level"]
        crossing_year = projection.get("most_likely_crossing")

        summary = f"{country} enters 2026 as a {status_2026} AI readiness nation "
        summary += f"with a {urgency}-level urgency for AI preparedness. "

        if crossing_year:
            summary += f"Projected critical crossing year is {crossing_year}, "
            summary += f"giving {projection['preparation_years']} years for preparation. "

        summary += f"Current readiness score of {category['readiness']:.2f} "
        summary += f"faces exposure levels of {category['exposure']:.2f}."

        return summary

    def _identify_strengths(self, country, category):
        """Identify country strengths"""
        strengths = []

        # Based on high readiness components
        if category["readiness"] > 0.6:
            strengths.append("Strong institutional foundation")
            strengths.append("Advanced digital infrastructure")

        if category["readiness"] > 0.7:
            strengths.append("High education levels")
            strengths.append("Innovative ecosystem")

        # Geographic strengths
        if country in ["USA", "GBR", "DEU", "FRA", "JPN"]:
            strengths.append("Established AI research community")
            strengths.append("Strong regulatory frameworks")

        # Sector strengths
        if category["readiness"] > 0.5:
            strengths.append("Digital economy development")

        return strengths

    def _identify_challenges(self, country, category):
        """Identify country challenges"""
        challenges = []

        # Exposure-related challenges
        if category["exposure"] > 0.6:
            challenges.append("High vulnerability to AI disruption")
            challenges.append("Rapid automation risk")

        if category["exposure"] > 0.7:
            challenges.append("Critical readiness-exposure gap")
            challenges.append("Limited adaptation capacity")

        # Geographic challenges
        if country in ["IDN", "EGY", "NGA", "PAK", "ETH"]:
            challenges.append("Digital infrastructure gaps")
            challenges.append("Educational resource constraints")

        # Economic challenges
        if category["readiness"] < 0.4:
            challenges.append("Limited economic resources")
            challenges.append("Institutional capacity constraints")

        return challenges

    def _describe_timeline(self, projection):
        """Describe timeline outlook"""
        timeline = {}

        if projection.get("most_likely_crossing"):
            timeline["crossing_year"] = projection["most_likely_crossing"]
            timeline["preparation_years"] = projection.get("preparation_years", 0)
            timeline["preparation_window"] = projection.get("preparation_years", 0)
            timeline["urgency"] = projection.get("urgency_level", "low")
            timeline["urgency_level"] = projection.get("urgency_level", "low")
            timeline["probability"] = projection.get("crossing_probability", 0.0)
            timeline["crossing_probability"] = projection.get("crossing_probability", 0.0)

            # Describe phases
            current_year = 2026
            if projection["most_likely_crossing"] <= 2030:
                timeline["phases"] = {
                    "immediate": "2026-2028: Build adaptation capacity",
                    "critical": "2028-2030: Emergency preparedness",
                    "transition": "2030+: New reality adaptation"
                }
            elif projection["most_likely_crossing"] <= 2035:
                timeline["phases"] = {
                    "development": "2026-2030: Infrastructure investment",
                    "preparation": "2030-2035: Capability building",
                    "transition": "2035+: System adaptation"
                }
            else:
                timeline["phases"] = {
                    "planning": "2026-2030: Long-term strategy",
                    "development": "2030-2035: Implementation phase",
                    "adaptation": "2035+: Continuous adjustment"
                }

        return timeline

    def _generate_recommendations(self, category_info, projection):
        """Generate policy recommendations"""
        recommendations = []

        # General recommendations based on category
        recommendations.extend(category_info["recommendations"])

        # Urgency-specific recommendations
        if projection["urgency_level"] == "critical":
            recommendations.extend([
                "Establish emergency task force",
                "Implement immediate capacity building",
                "Seek international assistance",
                "Prioritize critical sectors"
            ])
        elif projection["urgency_level"] == "high":
            recommendations.extend([
                "Accelerate adaptation programs",
                "Increase investment in education",
                "Strengthen digital infrastructure",
                "Develop regulatory frameworks"
            ])

        # Timeline-specific recommendations
        if projection["preparation_years"] < 5:
            recommendations.append("Crash program implementation required")
        elif projection["preparation_years"] < 10:
            recommendations.append("Accelerated timeline recommended")
        else:
            recommendations.append("Strategic long-term planning")

        return recommendations

    def _compile_key_metrics(self, country, category, projection):
        """Compile key metrics for country"""
        metrics = {
            "readiness_score": round(category["readiness"], 3),
            "exposure_score": round(category["exposure"], 3),
            "gap_score": round(category["gap"], 3),
            "status_2026": category["year_2026"]["status"],
            "urgency_level": projection["urgency_level"],
            "crossing_probability": round(projection["crossing_probability"], 2)
        }

        if projection.get("most_likely_crossing"):
            metrics["most_likely_crossing"] = projection["most_likely_crossing"]
            metrics["preparation_years"] = projection["preparation_years"]

        return metrics

    def _get_peer_comparisons(self, country):
        """Get peer comparison information"""
        peer_groups = self.define_peer_groups()

        comparisons = {
            "income_group": "unclassified",
            "regional_group": "unclassified",
            "regional_peers": [],
            "global_rank": "unclassified"
        }

        # Determine income group
        if country in peer_groups["high_income"]:
            comparisons["income_group"] = "high_income"
            comparisons["regional_peers"] = [p for p in peer_groups["high_income"] if p != country]
        elif country in peer_groups["upper_middle"]:
            comparisons["income_group"] = "upper_middle"
            comparisons["regional_peers"] = [p for p in peer_groups["upper_middle"] if p != country]
        elif country in peer_groups["lower_middle"]:
            comparisons["income_group"] = "lower_middle"
            comparisons["regional_peers"] = [p for p in peer_groups["lower_middle"] if p != country]

        # Determine regional group
        for region, countries in peer_groups["regional_leaders"].items():
            if country in countries:
                comparisons["regional_group"] = region
                comparisons["regional_peers"] = [p for p in countries if p != country]
                break

        # Calculate global rank (simplified)
        if hasattr(self, 'country_scores'):
            scores = self.country_scores["overall_score"].sort_values(ascending=False)
            rank = list(scores.index).index(country) + 1
            comparisons["global_rank"] = f"#{rank}/{len(scores)}"

        return comparisons

    def generate_all_profiles(self, classifications, projections):
        """Generate all country profiles"""
        logger.info("Generating all country profiles...")

        all_profiles = {}

        for country in classifications.keys():
            narrative = self.generate_country_narrative(country, classifications, projections)
            all_profiles[country] = narrative

        return all_profiles

    def create_profile_templates(self):
        """Create profile templates for different categories"""
        logger.info("Creating profile templates...")

        categories = self.define_country_categories()
        templates = {}

        for category_name, category_info in categories.items():
            template = {
                "name": category_name.title(),
                "description": category_info["description"],
                "characteristics": category_info["characteristics"],
                "recommendations": category_info["recommendations"],
                "profile_structure": {
                    "summary": "Country overview with timeline outlook",
                    "strengths": "Key competitive advantages",
                    "challenges": "Critical vulnerabilities",
                    "timeline_outlook": "Crossing year projections",
                    "recommendations": "Policy action items",
                    "key_metrics": "Quantitative performance",
                    "peer_comparisons": "Regional and global context"
                }
            }
            templates[category_name] = template

        # Create "not rated" template
        templates["not_rated"] = {
            "name": "Not Rated",
            "description": "Insufficient data for comprehensive assessment",
            "characteristics": ["Limited data availability", "Emerging economy", "Unique circumstances"],
            "recommendations": ["Data collection investment", "Participatory assessment", "Future inclusion planning"],
            "profile_structure": {
                "data_status": "Current data limitations",
                "inclusion_path": "Path to future rating",
                "recommendations": "Building assessment capacity"
            }
        }

        return templates

    def export_profiles(self, profiles, templates):
        """Export profiles to various formats"""
        logger.info("Exporting country profiles...")

        # Export individual country profiles
        profiles_dir = self.project_root / "research" / "country_profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)

        for country, profile in profiles.items():
            # JSON format
            json_file = profiles_dir / f"{country.lower()}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2)

            # Markdown format
            md_file = profiles_dir / f"{country.lower()}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(self._format_profile_markdown(country, profile))

        # Export templates
        templates_file = profiles_dir / "templates.json"
        with open(templates_file, 'w', encoding='utf-8') as f:
            json.dump(templates, f, indent=2)

        # Export summary report
        summary_file = self.project_root / "research" / "country_profiles_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_summary_report(profiles, templates))

        logger.info(f"Profiles exported to {profiles_dir}")

        return {
            "profiles": profiles,
            "templates": templates,
            "profiles_dir": profiles_dir,
            "summary_file": summary_file
        }

    def _format_profile_markdown(self, country, profile):
        """Format profile as markdown"""
        md = f"# {country} Profile\n\n"

        # Summary
        md += f"## Summary\n{profile['summary']}\n\n"

        # Strengths
        md += "## Strengths\n"
        for strength in profile['strengths']:
            md += f"- {strength}\n"
        md += "\n"

        # Challenges
        md += "## Challenges\n"
        for challenge in profile['challenges']:
            md += f"- {challenge}\n"
        md += "\n"

        # Timeline Outlook
        md += "## Timeline Outlook\n"
        timeline = profile['timeline_outlook']
        if 'crossing_year' in timeline:
            md += f"- **Most Likely Crossing**: {timeline['crossing_year']}\n"
            md += f"- **Preparation Years**: {timeline['preparation_years']}\n"
            md += f"- **Urgency Level**: {timeline['urgency_level']}\n"
            md += f"- **Crossing Probability**: {timeline['crossing_probability']:.1%}\n"
        else:
            md += "No crossing projected within timeline\n"
        md += "\n"

        # Recommendations
        md += "## Recommendations\n"
        for rec in profile['recommendations']:
            md += f"- {rec}\n"
        md += "\n"

        # Key Metrics
        md += "## Key Metrics\n"
        metrics = profile['key_metrics']
        for key, value in metrics.items():
            md += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        md += "\n"

        # Peer Comparisons
        md += "## Peer Comparisons\n"
        peers = profile['peer_comparisons']
        for key, value in peers.items():
            md += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        md += "\n"

        return md

    def _generate_summary_report(self, profiles, templates):
        """Generate summary report"""
        report = []
        report.append("# Country Profiles Summary Report\n")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"Countries profiled: {len(profiles)}\n\n")

        # Category distribution
        categories = {}
        for country, profile in profiles.items():
            category = profile['key_metrics']['status_2026'].lower()
            categories[category] = categories.get(category, 0) + 1

        report.append("## Category Distribution\n")
        for category, count in categories.items():
            report.append(f"- {category.title()}: {count} countries\n")
        report.append("\n")

        # Urgency distribution
        urgency_dist = {}
        for country, profile in profiles.items():
            urgency = profile['key_metrics']['urgency_level']
            urgency_dist[urgency] = urgency_dist.get(urgency, 0) + 1

        report.append("## Urgency Distribution\n")
        for urgency, count in urgency_dist.items():
            report.append(f"- {urgency.title()}: {count} countries\n")
        report.append("\n")

        # Timeline projections
        report.append("## Timeline Projections\n")
        crossing_countries = [c for c, p in profiles.items()
                            if p['key_metrics'].get('most_likely_crossing')]
        if crossing_countries:
            report.append(f"Countries with projected crossings: {len(crossing_countries)}\n")
            for country in sorted(crossing_countries[:5]):  # Top 5
                year = profiles[country]['key_metrics']['most_likely_crossing']
                urgency = profiles[country]['key_metrics']['urgency_level']
                report.append(f"- {country}: {year} ({urgency} urgency)\n")
        report.append("\n")

        # Recommendations overview
        all_recommendations = {}
        for country, profile in profiles.items():
            for rec in profile['recommendations']:
                category = rec.split()[0].lower()
                all_recommendations[category] = all_recommendations.get(category, 0) + 1

        report.append("## Key Recommendations by Category\n")
        for category, count in sorted(all_recommendations.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- {category.title()}: {count} instances\n")
        report.append("\n")

        # Template information
        report.append("## Profile Templates\n")
        for template_name, template in templates.items():
            report.append(f"### {template_name.title()}\n")
            report.append(f"{template['description']}\n")
            report.append("\n")

        return '\n'.join(report)

    def run_country_profiles(self):
        """Run complete country profiles process"""
        logger.info("Starting country profiles generation...")

        # Load data
        if not self.load_data():
            return False

        # Classify countries
        classifications = self.classify_countries()

        # Calculate timeline projections
        projections = self.calculate_timeline_projections(classifications)

        # Generate all profiles
        profiles = self.generate_all_profiles(classifications, projections)

        # Create templates
        templates = self.create_profile_templates()

        # Export profiles
        results = self.export_profiles(profiles, templates)

        logger.info("✅ Country profiles completed successfully")
        return True

def main():
    """Run the country profiles process"""
    project_root = Path.cwd()
    generator = CountryProfileGenerator(project_root)

    if generator.run_country_profiles():
        print("\n✅ Country profiles completed successfully!")
        return 0
    else:
        print("\n❌ Country profiles failed!")
        return 1

if __name__ == "__main__":
    exit(main())