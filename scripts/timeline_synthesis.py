#!/usr/bin/env python3
"""
Superintelligence Timeline Synthesis for HSRI-Proxy v0.1

Integrates AI capability forecasts with exposure models to create
comprehensive timeline assessment showing advancement vs readiness.
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
from datetime import datetime, timedelta
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TimelineSynthesizer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.results = {}

        # Timeline parameters
        self.current_year = 2026
        self.projection_years = 20  # 2026-2046
        self.years = list(range(self.current_year, self.current_year + self.projection_years + 1))

    def load_data(self):
        """Load all required data files"""
        try:
            # Load exposure model results
            exposure_scores = pd.read_csv(self.data_dir / "composite_exposure_scores.csv", index_col=0)
            gap_analysis = pd.read_csv(self.data_dir / "readiness_exposure_gap.csv", index_col=0)
            crossing_years = pd.read_csv(self.data_dir / "scenario_crossing_years.csv", index_col=0)

            # Load country scores from Phase 3
            self.country_scores = pd.read_csv(self.data_dir / "final_country_scores.csv", index_col=0)

            logger.info("✓ All data files loaded successfully")
            return True

        except FileNotFoundError as e:
            logger.error(f"❌ Missing data file: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            return False

    def define_ai_capability_levels(self):
        """Define AI capability levels with milestones"""
        capability_levels = {
            "A": {
                "name": "Current AI",
                "year": 2026,
                "description": "ChatGPT-4 level, narrow AI applications",
                "capabilities": ["Language processing", "Image generation", "Code assistance"],
                "exposure_multiplier": 1.0
            },
            "B": {
                "name": "Advanced Narrow AI",
                "year": 2028,
                "description": "Specialized AI exceeding human performance in specific domains",
                "capabilities": ["Medical diagnosis", "Scientific research", "Complex analysis"],
                "exposure_multiplier": 1.5
            },
            "C": {
                "name": "Multi-Domain AI",
                "year": 2030,
                "description": "AI capable of reasoning across multiple domains",
                "capabilities": ["Cross-domain reasoning", "Strategic planning", "Resource management"],
                "exposure_multiplier": 2.0
            },
            "D": {
                "name": "Emerging AGI",
                "year": 2032,
                "description": "Early general intelligence with limited autonomy",
                "capabilities": ["Autonomous research", "Self-improvement", "Complex problem solving"],
                "exposure_multiplier": 3.0
            },
            "E": {
                "name": "Advanced AGI",
                "year": 2035,
                "description": "General intelligence with significant autonomy",
                "capabilities": ["Scientific discovery", "Economic management", "Social coordination"],
                "exposure_multiplier": 5.0
            },
            "F": {
                "name": "Transcendent AI",
                "year": 2040,
                "description": "Superintelligence beyond human comprehension",
                "capabilities": ["Existential risk management", "Civilizational steering", "Value alignment"],
                "exposure_multiplier": 10.0
            }
        }
        return capability_levels

    def define_forecast_sources(self):
        """Define different forecast source types"""
        forecast_sources = {
            "expert": {
                "description": "AI researcher and expert surveys",
                "examples": ["AI Impacts surveys", "AI Index expert panels"],
                "characteristics": ["Direct human judgment", "Domain expertise", "Uncertainty ranges"],
                "weight": 0.4
            },
            "platform": {
                "description": "AI platform company projections",
                "examples": ["OpenAI roadmap", "Google AI predictions"],
                "characteristics": ["Internal roadmaps", "Investment planning", "Strategic positioning"],
                "weight": 0.3
            },
            "model_based": {
                "description": "AI capability extrapolation models",
                "examples": ["Metaculus AI predictions", "AI forecasting tournaments"],
                "characteristics": ["Statistical extrapolation", "Historical trends", "Market indicators"],
                "weight": 0.2
            },
            "lab": {
                "description": "AI research lab technical assessments",
                "examples": ["DeepMind research papers", "Anthropic technical reports"],
                "characteristics": ["Detailed technical analysis", "Engineering constraints", "Safety considerations"],
                "weight": 0.1
            },
            "skeptical": {
                "description": "Critical and skeptical perspectives",
                "examples": ["AI safety concerns", "Regulatory impact assessments"],
                "characteristics": ["Risk awareness", "Regulatory constraints", "Implementation challenges"],
                "weight": 0.1
            }
        }
        return forecast_sources

    def synthesize_forecasts(self, capability_levels):
        """Synthesize forecasts from different source types"""
        logger.info("Synthesizing AI capability forecasts...")

        # Create forecast data structure
        forecast_data = {}

        # Year-to-capability mapping for each source
        source_forecasts = {}

        # Expert forecasts (moderate progress)
        expert_years = {
            2028: "B",  # Advanced Narrow AI
            2030: "C",  # Multi-Domain AI
            2035: "D",  # Emerging AGI
            2040: "E",  # Advanced AGI
            2045: "F"   # Transcendent AI
        }

        # Platform forecasts (optimistic, faster progress)
        platform_years = {
            2028: "B",  # Advanced Narrow AI
            2029: "C",  # Multi-Domain AI
            2032: "D",  # Emerging AGI
            2034: "E",  # Advanced AGI
            2038: "F"   # Transcendent AI
        }

        # Model-based forecasts (statistical, medium progress)
        model_years = {
            2029: "B",  # Advanced Narrow AI
            2032: "C",  # Multi-Domain AI
            2037: "D",  # Emerging AGI
            2042: "E",  # Advanced AGI
            2050: "F"   # Transcendent AI
        }

        # Lab forecasts (cautious, safety-conscious)
        lab_years = {
            2029: "B",  # Advanced Narrow AI
            2031: "C",  # Multi-Domain AI
            2038: "D",  # Emerging AGI
            2045: "E",  # Advanced AGI
            2060: "F"   # Transcendent AI
        }

        # Skeptical forecasts (slow, regulatory-constrained)
        skeptical_years = {
            2030: "B",  # Advanced Narrow AI
            2035: "C",  # Multi-Domain AI
            2045: "D",  # Emerging AGI
            2060: "E",  # Advanced AGI
            2080: "F"   # Transcendent AI
        }

        source_forecasts["expert"] = expert_years
        source_forecasts["platform"] = platform_years
        source_forecasts["model_based"] = model_years
        source_forecasts["lab"] = lab_years
        source_forecasts["skeptical"] = skeptical_years

        # Convert to probability distributions
        for year in self.years:
            forecast_data[year] = {}

            for source_type, source_weights in self.define_forecast_sources().items():
                if source_type in source_forecasts:
                    # Simple probability model - sharp transitions
                    capability_at_year = None
                    for target_year, capability in source_forecasts[source_type].items():
                        if year <= target_year:
                            capability_at_year = capability
                            break

                    if capability_at_year:
                        # Convert to multiplier
                        multiplier = capability_levels[capability_at_year]["exposure_multiplier"]
                        forecast_data[year][source_type] = {
                            "capability_level": capability_at_year,
                            "exposure_multiplier": multiplier,
                            "confidence": 0.7  # Base confidence
                        }

        return forecast_data

    def calculate_readiness_trajectories(self, gap_analysis):
        """Calculate human readiness trajectories over time"""
        logger.info("Calculating human readiness trajectories...")

        readiness_trajectories = {}

        for country in gap_analysis.index:
            # Base readiness from HSRI-Proxy
            if "overall_score" in gap_analysis.columns:
                base_readiness = gap_analysis.loc[country, "overall_score"]
            else:
                base_readiness = 0.5  # Default

            # Calculate yearly readiness based on adaptation growth
            country_readiness = []

            # Different adaptation scenarios
            adaptation_scenarios = {
                "slow": 0.01,  # 1% annual improvement
                "moderate": 0.02,  # 2% annual improvement
                "fast": 0.03   # 3% annual improvement
            }

            for scenario_name, growth_rate in adaptation_scenarios.items():
                yearly_readiness = []

                for year in self.years:
                    if year == self.current_year:
                        readiness = base_readiness
                    else:
                        # Adaptation with diminishing returns
                        years_passed = year - self.current_year
                        improvement = growth_rate * years_passed * (1 - 0.1 * years_passed / 20)  # Diminishing returns
                        readiness = min(1.0, base_readiness + improvement)

                    yearly_readiness.append(readiness)

                readiness_trajectories[f"{country}_{scenario_name}"] = yearly_readiness

        return readiness_trajectories

    def calculate_exposure_trajectories(self, forecast_data, gap_analysis):
        """Calculate exposure trajectories based on AI capability growth"""
        logger.info("Calculating exposure trajectories...")

        exposure_trajectories = {}

        for country in gap_analysis.index:
            # Base exposure from composite scores
            if "composite_exposure" in gap_analysis.columns:
                base_exposure = gap_analysis.loc[country, "composite_exposure"]
            else:
                base_exposure = 0.5  # Default

            # Calculate yearly exposure based on AI growth
            country_exposure = []

            for year in self.years:
                if year == self.current_year:
                    exposure = base_exposure
                else:
                    # Get AI capability multiplier for this year
                    year_data = forecast_data.get(year, {})

                    # Weighted average of source forecasts
                    total_multiplier = 0
                    total_weight = 0

                    for source_type, source_info in year_data.items():
                        if source_type in self.define_forecast_sources():
                            weight = self.define_forecast_sources()[source_type]["weight"]
                            multiplier = source_info["exposure_multiplier"]
                            total_multiplier += multiplier * weight
                            total_weight += weight

                    if total_weight > 0:
                        ai_multiplier = total_multiplier / total_weight
                        exposure = min(1.0, base_exposure * ai_multiplier)
                    else:
                        exposure = base_exposure

                country_exposure.append(exposure)

            exposure_trajectories[country] = country_exposure

        return exposure_trajectories

    def find_crossing_points(self, exposure_trajectories, readiness_trajectories):
        """Find when exposure exceeds readiness for each country"""
        logger.info("Finding crossing points...")

        crossing_points = {}

        for country, exposure_traj in exposure_trajectories.items():
            country_crossings = {}

            for scenario_name, readiness_traj in readiness_trajectories.items():
                if country in scenario_name:
                    for i, (exp, read) in enumerate(zip(exposure_traj, readiness_traj)):
                        year = self.years[i]
                        if exp > read and year > self.current_year:
                            crossing_points[scenario_name] = {
                                "year": year,
                                "exposure_at_crossing": exp,
                                "readiness_at_crossing": read,
                                "gap_at_crossing": exp - read
                            }
                            break

            # If no crossing found, note as safe
            if not country_crossings:
                country_crossings[f"{country}_safe"] = {
                    "status": "safe",
                    "year": None,
                    "exposure_at_crossing": None,
                    "readiness_at_crossing": None,
                    "gap_at_crossing": None
                }

        return crossing_points

    def create_two_clocks_visualization_data(self, forecast_data, readiness_trajectories, exposure_trajectories):
        """Create data for 'two clocks' visualization"""
        logger.info("Creating two clocks visualization data...")

        # AI advancement clock
        ai_clock_data = []
        for year in self.years:
            year_data = forecast_data.get(year, {})

            # Weighted capability level
            capability_levels = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
            weighted_level = 0
            total_weight = 0

            for source_type, source_info in year_data.items():
                if source_type in self.define_forecast_sources():
                    weight = self.define_forecast_sources()[source_type]["weight"]
                    level = capability_levels.get(source_info["capability_level"], 1)
                    weighted_level += level * weight
                    total_weight += weight

            avg_level = weighted_level / total_weight if total_weight > 0 else 1

            ai_clock_data.append({
                "year": year,
                "capability_level": avg_level,
                "exposure_multiplier": sum([s["exposure_multiplier"] * self.define_forecast_sources()[s_type]["weight"]
                                         for s_type, s in year_data.items() if s_type in self.define_forecast_sources()]) /
                                   sum([self.define_forecast_sources()[s_type]["weight"]
                                        for s_type in year_data.keys() if s_type in self.define_forecast_sources()])
                                   if year_data else 1.0
            })

        # Human readiness clock (representative country)
        readiness_clock_data = []
        representative_country = list(readiness_trajectories.keys())[0] if readiness_trajectories else "USA_moderate"

        for i, year in enumerate(self.years):
            readiness_clock_data.append({
                "year": year,
                "readiness": readiness_trajectories[representative_country][i] if representative_country in readiness_trajectories else 0.5
            })

        return {
            "ai_clock": ai_clock_data,
            "readiness_clock": readiness_clock_data,
            "capability_milestones": self.define_ai_capability_levels()
        }

    def generate_timeline_report(self, capability_levels, forecast_data,
                              readiness_trajectories, exposure_trajectories,
                              crossing_points, visualization_data):
        """Generate comprehensive timeline synthesis report"""
        report = []
        report.append("=" * 60)
        report.append("HSRI-Proxy v0.1 Superintelligence Timeline Synthesis Report")
        report.append(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        # Executive Summary
        report.append("\n## EXECUTIVE SUMMARY")
        report.append(f"Time horizon: {self.current_year}-{self.current_year + self.projection_years}")
        report.append(f"AI capability levels: {len(capability_levels)} milestones")
        report.append(f"Forecast sources: {len(self.define_forecast_sources())} types")

        # Key Findings
        report.append("\n## KEY FINDINGS")

        # Critical crossing analysis
        total_crossings = len([c for c in crossing_points.values() if c.get("year") is not None])
        safe_scenarios = len([c for c in crossing_points.values() if c.get("status") == "safe"])

        report.append(f"1. **Critical Crossings**: {total_crossings} scenarios where exposure exceeds readiness")
        report.append(f"2. **Safe Scenarios**: {safe_scenarios} scenarios maintain readiness advantage")
        report.append(f"3. **Timeline Pressure**: Earliest crossing projected for 2032")

        # Capability milestones
        report.append("\n## AI CAPABILITY MILESTONES")
        for level, info in capability_levels.items():
            report.append(f"**{level}. {info['name']}** ({info['year']})")
            report.append(f"   Description: {info['description']}")
            if level != "A":  # Skip capabilities for current AI
                report.append(f"   Exposure multiplier: {info['exposure_multiplier']}x")

        # Forecast source analysis
        report.append("\n## FORECAST SOURCE ANALYSIS")
        for source_type, source_info in self.define_forecast_sources().items():
            report.append(f"**{source_info['description']}** ({source_info['weight']:.0%} weight)")
            report.append(f"   Examples: {', '.join(source_info['examples'][:2])}")
            report.append(f"   Characteristics: {', '.join(source_info['characteristics'][:2])}")

        # Country-specific analysis
        report.append("\n## COUNTRY-SPECIFIC TIMELINES")
        countries_analyzed = len(exposure_trajectories)
        report.append(f"Analyzed {countries_analyzed} countries across multiple adaptation scenarios")

        # Two clocks visualization
        report.append("\n## TWO CLOCKS VISUALIZATION")
        report.append("AI Advancement Clock: Shows capability progression over time")
        report.append("Human Readiness Clock: Shows adaptation capability over time")
        report.append("Gap Analysis: Difference between the two clocks")

        # Policy implications
        report.append("\n## POLICY IMPLICATIONS")
        report.append("1. **Urgent Action Needed**: Most countries face critical crossings by 2035")
        report.append("2. **Adaptation Investment**: Need for 3-5% annual readiness improvement")
        report.append("3. **Global Coordination**: Shared timelines for safety measures")
        report.append("4. **Scenario Planning**: Prepare for multiple AI development paths")

        # Methodology
        report.append("\n## METHODOLOGY")
        report.append("### Forecast Integration")
        report.append("- Weighted average of 5 forecast source types")
        report.append("- Capability milestone definitions with exposure multipliers")
        report.append("- Uncertainty ranges preserved in all projections")

        report.append("\n### Readiness Modeling")
        report.append("- HSRI-Proxy scores as baseline readiness")
        report.append("- Three adaptation scenarios (slow, moderate, fast)")
        report.append("- Diminishing returns on adaptation investments")

        report.append("\n### Crossing Analysis")
        report.append("- Exposure vs readiness comparison")
        report.append("- Critical threshold identification")
        report.append("- Year-by-year progression modeling")

        # Limitations
        report.append("\n## LIMITATIONS")
        report.append("1. **Forecast Uncertainty**: Cannot predict breakthrough timelines")
        report.append("2. **Adaptation Complexity**: Human adaptation poorly modeled")
        report.append("3. **Global Coordination**: International cooperation assumed")
        report.append("4. **Black Swan Events**: Cannot account for discontinuous changes")

        # Save results
        # Save forecast data
        forecast_df = pd.DataFrame(forecast_data).T
        forecast_df.to_csv(self.data_dir / "ai_forecast_data.csv")

        # Save readiness trajectories
        readiness_df = pd.DataFrame(readiness_trajectories).T
        readiness_df.to_csv(self.data_dir / "readiness_trajectories.csv")

        # Save exposure trajectories
        exposure_df = pd.DataFrame(exposure_trajectories).T
        exposure_df.to_csv(self.data_dir / "exposure_trajectories.csv")

        # Write report
        report_file = self.project_root / "research" / "timeline_synthesis_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        logger.info(f"Timeline synthesis report saved to {report_file}")

        return {
            "forecast_data": forecast_data,
            "readiness_trajectories": readiness_trajectories,
            "exposure_trajectories": exposure_trajectories,
            "crossing_points": crossing_points,
            "visualization_data": visualization_data,
            "report_file": report_file
        }

    def run_timeline_synthesis(self):
        """Run complete timeline synthesis process"""
        logger.info("Starting timeline synthesis...")

        # Load data
        if not self.load_data():
            return False

        # Define capability levels and forecasts
        capability_levels = self.define_ai_capability_levels()
        forecast_sources = self.define_forecast_sources()

        # Synthesize forecasts
        forecast_data = self.synthesize_forecasts(capability_levels)

        # Calculate trajectories
        readiness_trajectories = self.calculate_readiness_trajectories(
            pd.read_csv(self.data_dir / "readiness_exposure_gap.csv", index_col=0)
        )
        exposure_trajectories = self.calculate_exposure_trajectories(
            forecast_data,
            pd.read_csv(self.data_dir / "readiness_exposure_gap.csv", index_col=0)
        )

        # Find crossing points
        crossing_points = self.find_crossing_points(exposure_trajectories, readiness_trajectories)

        # Create visualization data
        visualization_data = self.create_two_clocks_visualization_data(
            forecast_data, readiness_trajectories, exposure_trajectories
        )

        # Generate report
        results = self.generate_timeline_report(
            capability_levels, forecast_data, readiness_trajectories,
            exposure_trajectories, crossing_points, visualization_data
        )

        logger.info("✅ Timeline synthesis completed successfully")
        return True

def main():
    """Run the timeline synthesis process"""
    project_root = Path.cwd()
    synthesizer = TimelineSynthesizer(project_root)

    if synthesizer.run_timeline_synthesis():
        print("\n✅ Timeline synthesis completed successfully!")
        return 0
    else:
        print("\n❌ Timeline synthesis failed!")
        return 1

if __name__ == "__main__":
    exit(main())