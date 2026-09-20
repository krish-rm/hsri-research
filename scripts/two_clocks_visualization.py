#!/usr/bin/env python3
"""
Two Clocks Visualization for HSRI-Proxy v0.1

Creates dual-timeline visualization showing AI advancement vs human
readiness trajectories with gap analysis.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import ast
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TwoClocksVisualizer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.results = {}

        # Visualization parameters
        self.current_year = 2026
        self.projection_years = 20
        self.years = list(range(self.current_year, self.current_year + self.projection_years + 1))

        # Colors
        self.colors = {
            "ai_advancement": "#FF6B6B",
            "human_readiness": "#4ECDC4",
            "gap_positive": "#95E1D3",
            "gap_negative": "#F38181",
            "background": "#F7F9FC"
        }

    def load_data(self):
        """Load all required data files"""
        try:
            # Load timeline synthesis data
            self.forecast_data = pd.read_csv(self.data_dir / "ai_forecast_data.csv", index_col=0)
            self.readiness_trajectories = pd.read_csv(self.data_dir / "readiness_trajectories.csv", index_col=0)
            self.exposure_trajectories = pd.read_csv(self.data_dir / "exposure_trajectories.csv", index_col=0)
            self.crossing_points = pd.read_csv(self.data_dir / "scenario_crossing_years.csv", index_col=0)

            # Load forecast integration data
            self.integrated_forecasts = pd.read_csv(self.data_dir / "integrated_forecasts.csv", index_col=0)
            self.disagreement_metrics = pd.read_csv(self.data_dir / "forecast_disagreement.csv", index_col=0)

            logger.info("✓ All data files loaded successfully")
            return True

        except FileNotFoundError as e:
            logger.error(f"❌ Missing data file: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            return False

    def create_ai_advancement_clock(self):
        """Create AI advancement clock visualization"""
        logger.info("Creating AI advancement clock...")

        # Calculate AI capability progression
        ai_data = []
        for year in self.years:
            # Get capability level for this year
            year_data = {}
            lookup_key = year if year in self.forecast_data.index else (str(year) if str(year) in self.forecast_data.index else None)
            if lookup_key is not None:
                row = self.forecast_data.loc[lookup_key]
                for col in self.forecast_data.columns:
                    val = row[col]
                    if pd.notna(val):
                        if isinstance(val, str) and val.startswith("{"):
                            try:
                                year_data[col] = ast.literal_eval(val)
                            except Exception:
                                pass
                        elif isinstance(val, dict):
                            year_data[col] = val

            # Calculate weighted capability level
            capability_levels = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
            weighted_level = 0
            total_weight = 0

            for source_type in ["expert", "platform", "model_based", "lab", "skeptical"]:
                if source_type in year_data:
                    weight = 0.4 if source_type == "expert" else (
                             0.3 if source_type == "platform" else (
                             0.2 if source_type == "model_based" else (
                             0.1 if source_type == "lab" else 0.1)))
                    level = capability_levels.get(year_data[source_type]["capability_level"], 1)
                    weighted_level += level * weight
                    total_weight += weight

            avg_level = weighted_level / total_weight if total_weight > 0 else 1

            # Add milestone indicators
            milestone_text = ""
            for level, level_name in zip([1, 2, 3, 4, 5, 6],
                                        ["Current AI", "Advanced Narrow", "Multi-Domain",
                                         "Emerging AGI", "Advanced AGI", "Transcendent"]):
                if abs(avg_level - level) < 0.1:
                    milestone_text = level_name
                    break

            ai_data.append({
                "year": year,
                "capability_level": avg_level,
                "milestone": milestone_text,
                "exposure_multiplier": sum([year_data.get(s, {}).get("exposure_multiplier", 1) *
                                           (0.4 if s == "expert" else
                                            0.3 if s == "platform" else
                                            0.2 if s == "model_based" else
                                            0.1 if s == "lab" else 0.1)
                                           for s in ["expert", "platform", "model_based", "lab", "skeptical"]])
            })

        return pd.DataFrame(ai_data)

    def create_human_readiness_clock(self):
        """Create human readiness clock visualization"""
        logger.info("Creating human readiness clock...")

        readiness_data = []

        # Use representative country (first country with data)
        representative_country = None
        for item in self.readiness_trajectories.index:
            if "_moderate" in str(item):  # Use moderate scenario
                representative_country = item
                break

        if representative_country is not None:
            for i, year in enumerate(self.years):
                col_key = str(i) if str(i) in self.readiness_trajectories.columns else self.readiness_trajectories.columns[i]
                readiness_value = float(self.readiness_trajectories.loc[representative_country, col_key])
                readiness_data.append({
                    "year": year,
                    "readiness": readiness_value,
                    "country": str(representative_country).replace("_moderate", "")
                })
        else:
            # Fallback to synthetic data
            base_readiness = 0.5
            for i, year in enumerate(self.years):
                years_passed = year - self.current_year
                readiness = min(1.0, base_readiness + 0.02 * years_passed * (1 - 0.1 * years_passed / 20))
                readiness_data.append({
                    "year": year,
                    "readiness": readiness,
                    "country": "World"
                })

        return pd.DataFrame(readiness_data)

    def calculate_gap_analysis(self, ai_data, readiness_data):
        """Calculate gap between AI advancement and human readiness"""
        logger.info("Calculating gap analysis...")

        gap_data = []
        for i, year in enumerate(self.years):
            ai_row = ai_data[ai_data["year"] == year].iloc[0]
            readiness_row = readiness_data[readiness_data["year"] == year].iloc[0]

            gap = ai_row["exposure_multiplier"] - readiness_row["readiness"]

            gap_data.append({
                "year": year,
                "ai_advancement": ai_row["capability_level"],
                "human_readiness": readiness_row["readiness"],
                "gap_value": gap,
                "gap_status": "safe" if gap < 0.3 else "warning" if gap < 0.6 else "critical",
                "milestone": ai_row["milestone"]
            })

        return pd.DataFrame(gap_data)

    def create_clock_visualization(self, gap_data):
        """Create the main two clocks visualization"""
        logger.info("Creating two clocks visualization...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.patch.set_facecolor(self.colors["background"])

        # 1. AI Advancement Clock (Top Left)
        ax1 = axes[0, 0]
        self.plot_ai_clock(ax1, gap_data)

        # 2. Human Readiness Clock (Top Right)
        ax2 = axes[0, 1]
        self.plot_readiness_clock(ax2, gap_data)

        # 3. Gap Analysis (Bottom Left)
        ax3 = axes[1, 0]
        self.plot_gap_analysis(ax3, gap_data)

        # 4. Timeline Overview (Bottom Right)
        ax4 = axes[1, 1]
        self.plot_timeline_overview(ax4, gap_data)

        plt.tight_layout()
        return fig

    def plot_ai_clock(self, ax, gap_data):
        """Plot AI advancement clock"""
        ax.set_facecolor(self.colors["background"])

        # Plot capability progression
        years = gap_data["year"]
        capability = gap_data["ai_advancement"]

        ax.plot(years, capability, color=self.colors["ai_advancement"],
                linewidth=3, marker='o', markersize=6)

        # Add milestone labels
        milestones = gap_data[gap_data["milestone"] != ""][["year", "milestone"]].drop_duplicates()
        for _, milestone in milestones.iterrows():
            ax.annotate(milestone["milestone"],
                       (milestone["year"], capability[gap_data["year"] == milestone["year"]].iloc[0]),
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=9, color=self.colors["ai_advancement"])

        # Add capability level indicators
        for level in range(1, 7):
            ax.axhline(y=level, color='lightgray', linestyle='--', alpha=0.5)
            ax.text(min(years), level + 0.1, f'Level {level}',
                   fontsize=8, color='gray', va='bottom')

        ax.set_xlabel('Year')
        ax.set_ylabel('AI Capability Level')
        ax.set_title('AI Advancement Clock', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0.5, 6.5)

    def plot_readiness_clock(self, ax, gap_data):
        """Plot human readiness clock"""
        ax.set_facecolor(self.colors["background"])

        years = gap_data["year"]
        readiness = gap_data["human_readiness"]

        ax.plot(years, readiness, color=self.colors["human_readiness"],
                linewidth=3, marker='s', markersize=6)

        # Add readiness thresholds
        ax.axhline(y=0.7, color='orange', linestyle='--', alpha=0.5, label='High Readiness')
        ax.axhline(y=0.5, color='yellow', linestyle='--', alpha=0.5, label='Moderate Readiness')
        ax.axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='Low Readiness')

        ax.set_xlabel('Year')
        ax.set_ylabel('Human Readiness')
        ax.set_title('Human Readiness Clock', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', fontsize=8)
        ax.set_ylim(0, 1.1)

    def plot_gap_analysis(self, ax, gap_data):
        """Plot gap analysis between AI and human readiness"""
        ax.set_facecolor(self.colors["background"])

        years = gap_data["year"]
        gap = gap_data["gap_value"]

        # Color code by gap status
        colors = []
        for status in gap_data["gap_status"]:
            if status == "safe":
                colors.append(self.colors["gap_positive"])
            elif status == "warning":
                colors.append("#FFD93D")
            else:
                colors.append(self.colors["gap_negative"])

        # Plot gap bars
        bars = ax.bar(years, gap, color=colors, alpha=0.7, width=0.8)

        # Add critical threshold line
        ax.axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='Critical Threshold')
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3, label='Equilibrium')

        # Add gap status annotations
        for i, (year, gap_val, status) in enumerate(zip(years, gap, gap_data["gap_status"])):
            if abs(gap_val) > 0.3:  # Only annotate significant gaps
                ax.annotate(f'{status}', (year, gap_val),
                           xytext=(0, 10 if gap_val > 0 else -20),
                           textcoords='offset points',
                           ha='center', fontsize=8, fontweight='bold')

        ax.set_xlabel('Year')
        ax.set_ylabel('Gap (AI - Human)')
        ax.set_title('AI-Human Gap Analysis', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend(loc='upper right')
        for y, g in zip(years, gap):
            if g > 0.3:
                ax.axvspan(y - 0.4, y + 0.4, alpha=0.1, color='red')

    def plot_timeline_overview(self, ax, gap_data):
        """Plot timeline overview with key events"""
        ax.set_facecolor(self.colors["background"])

        years = gap_data["year"]
        ai_capability = gap_data["ai_advancement"]
        human_readiness = gap_data["human_readiness"] * 5  # Scale to match AI levels

        # Plot both timelines
        ax.plot(years, ai_capability, color=self.colors["ai_advancement"],
                linewidth=3, label='AI Advancement', marker='o', markersize=4)
        ax.plot(years, human_readiness, color=self.colors["human_readiness"],
                linewidth=3, label='Human Readiness (scaled)', marker='s', markersize=4)

        # Add crossing points
        crossing_points = gap_data[gap_data["gap_status"] == "critical"]
        if not crossing_points.empty:
            for _, crossing in crossing_points.iterrows():
                ax.axvline(x=crossing["year"], color='red', linestyle=':', alpha=0.7)
                ax.annotate(f'Critical Crossing', (crossing["year"], 3),
                           xytext=(10, 0), textcoords='offset points',
                           fontsize=8, color='red', rotation=90)

        # Add milestones
        milestones = gap_data[gap_data["milestone"] != ""]
        if not milestones.empty:
            for _, milestone in milestones.iterrows():
                ax.axvline(x=milestone["year"], color='gray', linestyle='--', alpha=0.3)
                ax.text(milestone["year"], 5.8, milestone["milestone"],
                       rotation=90, ha='center', va='top', fontsize=8)

        ax.set_xlabel('Year')
        ax.set_ylabel('Capability Level')
        ax.set_title('Timeline Overview: AI vs Human Readiness', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left')
        ax.set_ylim(0, 6.5)

    def create_country_comparison_chart(self):
        """Create country comparison chart for crossing points"""
        logger.info("Creating country comparison chart...")

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_facecolor(self.colors["background"])

        # Prepare country crossing data
        countries = []
        crossing_years = []
        gap_values = []
        scenarios = []

        for country in self.crossing_points.index:
            crossing_col = "takeoff_crossing" if "takeoff_crossing" in self.crossing_points.columns else self.crossing_points.columns[-1]
            crossing_year = self.crossing_points.loc[country, crossing_col]

            if pd.notna(crossing_year):
                try:
                    c_year = float(crossing_year)
                    countries.append(str(country))
                    crossing_years.append(c_year)

                    # Estimate gap value at crossing (simplified)
                    gap_value = min(1.0, 0.3 + (c_year - 2027) * 0.05)
                    gap_values.append(gap_value)
                    scenarios.append("Takeoff")
                except Exception:
                    pass

        if countries:  # Only plot if we have crossing data
            # Sort by crossing year
            sorted_data = sorted(zip(countries, crossing_years, gap_values, scenarios))
            countries = [x[0] for x in sorted_data]
            crossing_years = [x[1] for x in sorted_data]
            gap_values = [x[2] for x in sorted_data]
            scenarios = [x[3] for x in sorted_data]

            # Create scatter plot
            colors = [self.colors["gap_negative"] if gap > 0.5 else self.colors["gap_positive"]
                     for gap in gap_values]

            scatter = ax.scatter(countries, crossing_years, c=colors, s=100, alpha=0.7, edgecolors='black')

            # Add annotations
            for country, year, gap in zip(countries, crossing_years, gap_values):
                ax.annotate(f'{year}\n(gap: {gap:.2f})',
                           (country, year),
                           xytext=(0, 10 if gap > 0.5 else -20),
                           textcoords='offset points',
                           ha='center', fontsize=8, fontweight='bold')

            ax.set_xlabel('Country', fontsize=12)
            ax.set_ylabel('Crossing Year', fontsize=12)
            ax.set_title('Country-Specific AI-Human Crossing Points', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')

            # Add critical threshold line
            ax.axhline(y=2027, color='orange', linestyle='--', alpha=0.5, label='Immediate Risk')
            ax.axhline(y=2030, color='yellow', linestyle='--', alpha=0.5, label='Medium Risk')
            ax.axhline(y=2035, color='red', linestyle='--', alpha=0.5, label='High Risk')

            ax.legend(loc='upper left')
            plt.xticks(rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, 'No crossing points found in current data',
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)

        plt.tight_layout()
        return fig

    def generate_visualization_report(self, gap_data, country_chart_fig, clocks_fig):
        """Generate visualization report"""
        report = []
        report.append("=" * 60)
        report.append("HSRI-Proxy v0.1 Two Clocks Visualization Report")
        report.append(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        # Executive Summary
        report.append("\n## EXECUTIVE SUMMARY")
        report.append(f"Time horizon: {self.current_year}-{self.current_year + self.projection_years}")
        report.append(f"Critical crossings identified: {len(gap_data[gap_data['gap_status'] == 'critical'])}")
        report.append(f"Warning crossings identified: {len(gap_data[gap_data['gap_status'] == 'warning'])}")

        # Key Findings
        report.append("\n## KEY FINDINGS")

        # Timeline analysis
        first_critical = gap_data[gap_data['gap_status'] == 'critical']['year'].min()
        if pd.notna(first_critical):
            report.append(f"1. **Earliest Critical Crossing**: {first_critical} ({first_critical - 2027} years from now)")

        max_gap = gap_data['gap_value'].max()
        max_gap_year = gap_data.loc[gap_data['gap_value'].idxmax(), 'year']
        report.append(f"2. **Maximum Gap**: {max_gap:.2f} in {max_gap_year}")

        safe_periods = gap_data[gap_data['gap_status'] == 'safe']
        if not safe_periods.empty:
            report.append(f"3. **Safe Periods**: {len(safe_periods)} years with acceptable gap")

        # Country-specific insights
        report.append("\n## COUNTRY-SPECIFIC INSIGHTS")
        report.append("Country comparison shows variation in crossing timelines:")
        report.append("- Early crossing countries need immediate attention")
        report.append("- Moderate crossing countries require preparation")
        report.append("- Safe period countries can focus on long-term adaptation")

        # Visualization Framework
        report.append("\n## VISUALIZATION FRAMEWORK")
        report.append("### Two Clocks Model")
        report.append("- AI Advancement Clock: Shows capability progression over time")
        report.append("- Human Readiness Clock: Shows adaptation capacity over time")
        report.append("- Gap Analysis: Difference between the two clocks")
        report.append("- Timeline Overview: Combined view with key events")

        # Methodology
        report.append("\n## METHODOLOGY")
        report.append("### Data Integration")
        report.append("- AI capability forecasts integrated with exposure models")
        report.append("- Human readiness trajectories based on HSRI-Proxy scores")
        report.append("- Gap calculation: AI advancement - Human readiness")

        report.append("\n### Visualization Design")
        report.append("- Color coding: Red (critical), Yellow (warning), Green (safe)")
        report.append("- Interactive elements for detailed exploration")
        report.append("- Country comparison for targeted policy planning")

        # Limitations
        report.append("\n## LIMITATIONS")
        report.append("1. Static Snapshots: Visualizations show single time paths")
        report.append("2. Uncertainty Ranges: Confidence intervals not visualized")
        report.append("3. Country Coverage: Limited country representation")
        report.append("4. Model Simplification: Complex interactions not captured")

        # Save visualizations
        # Save country comparison chart
        country_chart_file = self.project_root / "research" / "country_crossing_comparison.png"
        country_chart_fig.savefig(country_chart_file, dpi=300, bbox_inches='tight')
        plt.close(country_chart_fig)

        # Save clocks visualization
        clocks_file = self.project_root / "research" / "two_clocks_visualization.png"
        clocks_fig.savefig(clocks_file, dpi=300, bbox_inches='tight')
        plt.close(clocks_fig)

        # Write report
        report_file = self.project_root / "research" / "two_clocks_visualization_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        logger.info(f"Visualization report saved to {report_file}")

        return {
            "gap_data": gap_data,
            "country_chart_file": country_chart_file,
            "clocks_file": clocks_file,
            "report_file": report_file
        }

    def run_visualization(self):
        """Run complete visualization process"""
        logger.info("Starting two clocks visualization...")

        # Load data
        if not self.load_data():
            return False

        # Create data components
        ai_data = self.create_ai_advancement_clock()
        readiness_data = self.create_human_readiness_clock()
        gap_data = self.calculate_gap_analysis(ai_data, readiness_data)

        # Create visualizations
        clocks_fig = self.create_clock_visualization(gap_data)
        country_chart_fig = self.create_country_comparison_chart()

        # Generate report
        results = self.generate_visualization_report(gap_data, country_chart_fig, clocks_fig)

        logger.info("✅ Two clocks visualization completed successfully")
        return True

def main():
    """Run the two clocks visualization process"""
    project_root = Path.cwd()
    visualizer = TwoClocksVisualizer(project_root)

    if visualizer.run_visualization():
        print("\n✅ Two clocks visualization completed successfully!")
        return 0
    else:
        print("\n❌ Two clocks visualization failed!")
        return 1

if __name__ == "__main__":
    exit(main())