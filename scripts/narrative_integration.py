#!/usr/bin/env python3
"""
Narrative Integration for HSRI-Proxy v0.1

Integrates timeline projections with country profiles to create
compelling narratives that tell the story of AI readiness journeys.
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
from typing import Dict, List, Tuple
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NarrativeIntegrator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.results = {}

    def load_data(self):
        """Load all required data files"""
        try:
            # Load country profiles from Phase 6
            self.profiles_dir = self.project_root / "research" / "country_profiles"
            self.country_profiles = self._load_country_profiles()

            # Load not-rated scenarios
            self.scenarios_dir = self.project_root / "research" / "not_rated_scenarios"
            self.not_rated_scenarios = self._load_not_rated_scenarios()

            # Load timeline data from Phase 5
            self.timeline_data = pd.read_csv(self.data_dir / "ai_forecast_data.csv", index_col=0)
            self.crossing_years = pd.read_csv(self.data_dir / "scenario_crossing_years.csv", index_col=0)

            logger.info("✓ All data files loaded successfully")
            return True

        except FileNotFoundError as e:
            logger.error(f"❌ Missing data file: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            return False

    def _load_country_profiles(self):
        """Load country profiles from JSON files"""
        profiles = {}
        if self.profiles_dir.exists():
            for json_file in self.profiles_dir.glob("*.json"):
                if json_file.stem.lower() in ["templates", "summary_report"]:
                    continue
                with open(json_file, 'r', encoding='utf-8') as f:
                    country = json_file.stem.upper()
                    profiles[country] = json.load(f)
        return profiles

    def _load_not_rated_scenarios(self):
        """Load not-rated scenarios from JSON files"""
        scenarios = {}
        if self.scenarios_dir.exists():
            for json_file in self.scenarios_dir.glob("*_scenario.json"):
                with open(json_file, 'r', encoding='utf-8') as f:
                    country = json_file.stem.replace("_scenario", "").upper()
                    scenarios[country] = json.load(f)
        return scenarios

    def define_narrative_archetypes(self):
        """Define narrative archetypes for different country trajectories"""
        archetypes = {
            "front_runner": {
                "name": "Front Runner",
                "description": "Leading the AI transition with strong preparation",
                "characteristics": [
                    "High readiness scores (>0.7)",
                    "Early crossing years (>2035)",
                    "Strong institutional capacity",
                    "Advanced digital infrastructure"
                ],
                "narrative_elements": {
                    "opening": "Positioned at the forefront of the AI revolution",
                    "challenge": "Maintaining leadership in rapidly evolving landscape",
                    "opportunity": "Setting global standards and best practices",
                    "call_to_action": "Continue investment and share knowledge"
                },
                "timeline_phases": {
                    "present": "Building capabilities",
                    "near_future": "Establishing leadership",
                    "long_term": "Shaping global AI governance"
                }
            },

            "strategic_adapter": {
                "name": "Strategic Adapter",
                "description": "Making steady progress with focused preparation",
                "characteristics": [
                    "Moderate readiness scores (0.5-0.7)",
                    "Mid-range crossing years (2030-2035)",
                    "Targeted investment areas",
                    "Building adaptive capacity"
                ],
                "narrative_elements": {
                    "opening": "Navigating the AI transition with strategic focus",
                    "challenge": "Balancing innovation with risk management",
                    "opportunity": "Unique positioning in emerging AI economy",
                    "call_to_action": "Accelerate key capabilities and partnerships"
                },
                "timeline_phases": {
                    "present": "Building foundations",
                    "near_future": "Scaling capabilities",
                    "long_term": "Becoming regional leader"
                }
            },

            "critical_transition": {
                "name": "Critical Transition",
                "description": "Facing urgent crossing with immediate action needed",
                "characteristics": [
                    "Low readiness scores (<0.4)",
                    "Early crossing years (<2030)",
                    "High vulnerability indicators",
                    "Urgency for preparation"
                ],
                "narrative_elements": {
                    "opening": "At the critical juncture of AI transformation",
                    "challenge": "Limited time for preparation before crossing",
                    "opportunity": "Rapid development potential with right support",
                    "call_to_action": "Emergency measures and international support"
                },
                "timeline_phases": {
                    "present": "Emergency response",
                    "near_future": "Capacity building sprint",
                    "long_term": "New equilibrium adaptation"
                }
            },

            "cautious_observer": {
                "name": "Cautious Observer",
                "description": "Taking measured approach with careful consideration",
                "characteristics": [
                    "Moderate readiness scores (0.4-0.6)",
                    "Later crossing years (>2035)",
                    "Focus on safety and alignment",
                    "Methodical planning"
                ],
                "narrative_elements": {
                    "opening": "Approaching AI transition with deliberate caution",
                    "challenge": "Balancing innovation with safety concerns",
                    "opportunity": "Building robust governance frameworks",
                    "call_to_action": "Develop safety-first approach"
                },
                "timeline_phases": {
                    "present": "Building governance frameworks",
                    "near_future": "Safety-focused development",
                    "long_term": "Stable integration leadership"
                }
            },

            "emerging_player": {
                "name": "Emerging Player",
                "description": "Rapidly developing with growing AI capabilities",
                "characteristics": [
                    "Improving readiness scores",
                    "Variable crossing projections",
                    "Digital transformation underway",
                    "Investment in AI development"
                ],
                "narrative_elements": {
                    "opening": "Emerging as significant player in AI landscape",
                    "challenge": "Managing rapid growth and change",
                    "opportunity": "Leapfrogging traditional development paths",
                    "call_to_action": "Sustainable development and international integration"
                },
                "timeline_phases": {
                    "present": "Building infrastructure",
                    "near_future": "Scaling capabilities",
                    "long_term": "Global integration"
                }
            }
        }
        return archetypes

    def classify_narrative_types(self):
        """Classify countries into narrative archetypes"""
        logger.info("Classifying countries into narrative types...")

        archetypes = self.define_narrative_archetypes()
        classifications = {}

        for country, profile in self.country_profiles.items():
            metrics = profile['key_metrics']

            # Classify based on readiness and urgency
            readiness = metrics['readiness_score']
            urgency = metrics['urgency_level']

            if readiness > 0.7:
                archetype = "front_runner"
            elif readiness > 0.6:
                if urgency == "critical":
                    archetype = "critical_transition"
                else:
                    archetype = "strategic_adapter"
            elif readiness > 0.4:
                if urgency == "low":
                    archetype = "cautious_observer"
                else:
                    archetype = "strategic_adapter"
            else:
                if urgency == "critical":
                    archetype = "critical_transition"
                else:
                    archetype = "strategic_adapter"

            classifications[country] = {
                "archetype": archetype,
                "archetype_info": archetypes[archetype],
                "readiness": readiness,
                "urgency": urgency,
                "crossing_year": metrics.get('most_likely_crossing'),
                "adaptation_capacity": metrics['readiness_score'] - metrics.get('gap_score', 0)
            }

        return classifications, archetypes

    def generate_country_narrative(self, country, classification, archetypes):
        """Generate complete narrative for country"""
        archetype_name = classification["archetype"]
        archetype = archetypes[archetype_name]
        metrics = self.country_profiles[country]['key_metrics']

        narrative = {
            "country": country,
            "archetype": archetype_name,
            "title": f"{country}: {archetype['name']} Journey",
            "executive_summary": self._generate_executive_summary(country, classification),
            "timeline_journey": self._generate_timeline_journey(country, classification),
            "strategic_context": self._generate_strategic_context(country, classification),
            "key_milestones": self._generate_key_milestones(country, classification),
            "stakeholder_analysis": self._generate_stakeholder_analysis(country, classification),
            "recommendations": self._generate_strategic_recommendations(country, classification),
            "future_scenarios": self._generate_future_scenarios(country, classification),
            "risk_assessment": self._generate_risk_assessment(country, classification),
            "appendix": self._generate_appendix(country, metrics)
        }

        return narrative

    def _generate_executive_summary(self, country, classification):
        """Generate executive summary"""
        archetype = classification["archetype_info"]
        readiness = classification["readiness"]
        urgency = classification["urgency"]
        crossing_year = classification.get("crossing_year")

        summary = f"{country} emerges as a {archetype['name']} in the global AI landscape, "
        summary += f"currently at readiness level {readiness:.2f}. "

        if crossing_year:
            summary += f"With a projected critical crossing in {crossing_year}, "
            summary += f"the country faces {urgency}-level urgency for AI preparation. "

        summary += f"This narrative explores {country}'s strategic positioning, "
        summary += "preparation timeline, and path to successful AI integration. "

        return summary

    def _generate_timeline_journey(self, country, classification):
        """Generate timeline journey narrative"""
        archetype = classification["archetype_info"]
        crossing_year = classification.get("crossing_year")

        journey = {
            "present_phase": {
                "title": f"{country} Today: {archetype['timeline_phases']['present']}",
                "description": self._describe_present_phase(country, classification),
                "key_indicators": self._get_present_indicators(country, classification)
            },
            "near_future": {
                "title": f"Near Future: {archetype['timeline_phases']['near_future']}",
                "description": self._describe_near_future(country, classification),
                "key_indicators": self._get_near_future_indicators(country, classification)
            },
            "long_term": {
                "title": f"Long Term: {archetype['timeline_phases']['long_term']}",
                "description": self._describe_long_term(country, classification),
                "key_indicators": self._get_long_term_indicators(country, classification)
            }
        }

        if crossing_year:
            journey["critical_crossing"] = {
                "title": f"Critical Crossing: {crossing_year}",
                "description": self._describe_crossing_point(country, classification),
                "key_indicators": self._get_crossing_indicators(country, classification)
            }

        return journey

    def _describe_present_phase(self, country, classification):
        """Describe present phase of country"""
        archetype = classification["archetype_info"]
        metrics = self.country_profiles[country]['key_metrics']

        description = f"In 2026, {country} finds itself in a phase of "
        description += f"{archetype['timeline_phases']['present']}. "
        description += f"With a readiness score of {metrics['readiness_score']:.2f}, "
        description += f"the country is {metrics['status_2026'].lower()} in its AI preparedness journey. "

        if metrics['urgency_level'] != 'low':
            description += f"The {metrics['urgency_level']} urgency level indicates "
            description += f"immediate attention is needed for key areas. "

        return description

    def _describe_near_future(self, country, classification):
        """Describe near future phase"""
        archetype = classification["archetype_info"]
        crossing_year = classification.get("crossing_year")

        description = f"Looking ahead to the near future, {country} enters a phase of "
        description += f"{archetype['timeline_phases']['near_future']}. "

        if crossing_year and int(crossing_year) <= 2030:
            description += f"The critical crossing point approaches in {crossing_year}, "
            description += "requiring accelerated preparation efforts. "
        else:
            description += "Steady progress continues toward AI integration goals. "

        description += "This period will be crucial for establishing the foundations "
        description += "for successful navigation of the AI transition. "

        return description

    def _describe_long_term(self, country, classification):
        """Describe long term phase"""
        archetype = classification["archetype_info"]

        description = f"In the long term, {country} aspires to "
        description += f"{archetype['timeline_phases']['long_term']}. "
        description += "This represents the culmination of current preparation efforts "
        description += "and the establishment of a sustainable AI-integrated future. "

        description += "The country's unique strengths and strategic positioning "
        description += "will play a crucial role in its long-term success. "

        return description

    def _describe_crossing_point(self, country, classification):
        """Describe critical crossing point"""
        crossing_year = classification["crossing_year"]
        metrics = self.country_profiles[country]['key_metrics']

        description = f"In {crossing_year}, {country} reaches a critical crossing point "
        description += "where AI capabilities exceed human readiness thresholds. "
        description += f"With a crossing probability of {metrics['crossing_probability']:.1%}, "
        description += f"this represents a pivotal moment in the country's AI journey. "

        description += "Successful navigation of this transition will determine "
        description += f"whether {country} emerges as a leader or struggles in the new AI era. "

        return description

    def _generate_strategic_context(self, country, classification):
        """Generate strategic context analysis"""
        context = {
            "geopolitical_positioning": self._describe_geopolitical_position(country),
            "economic_implications": self._describe_economic_implications(country, classification),
            "technological_trajectory": self._describe_technological_trajectory(country, classification),
            "social_preparedness": self._describe_social_preparedness(country, classification)
        }

        return context

    def _describe_geopolitical_position(self, country):
        """Describe geopolitical positioning"""
        # Simplified geopolitical analysis
        if country in ["USA", "GBR", "DEU", "FRA", "JPN"]:
            return f"{country} maintains significant geopolitical influence with established AI research communities and strong international partnerships."
        elif country in ["CHN", "IND"]:
            return f"{country} represents a major emerging power with rapidly growing AI capabilities and increasing regional influence."
        else:
            return f"{country} navigates complex geopolitical relationships while developing its unique AI strategy and partnerships."

    def _describe_economic_implications(self, country, classification):
        """Describe economic implications"""
        archetype = classification["archetype_info"]
        readiness = classification["readiness"]

        implications = f"The economic implications for {country} are profound. "
        implications += f"With a readiness score of {readiness:.2f}, the country is "
        implications += f"positioned to {'significantly benefit' if readiness > 0.6 else 'moderately benefit'} "
        implications += "from AI-driven economic transformation. "

        implications += f"As a {archetype['name']}, {country} has the opportunity to "
        implications += "leverage AI for economic growth while addressing potential disruptions. "

        return implications

    def _describe_technological_trajectory(self, country, classification):
        """Describe technological trajectory"""
        m = self.country_profiles.get(country, {}).get("key_metrics", {})
        crossing = m.get("most_likely_crossing", "2035+")
        return f"{country} is advancing its compute base and data ecosystems, targeting system stability ahead of the projected {crossing} capability threshold."

    def _describe_social_preparedness(self, country, classification):
        """Describe social preparedness"""
        m = self.country_profiles.get(country, {}).get("key_metrics", {})
        readiness = m.get("readiness_score", classification["readiness"])
        return f"Social resilience in {country} reflects a readiness baseline of {readiness:.2f}, requiring targeted public education and workforce transition safety nets."

    def _generate_key_milestones(self, country, classification):
        """Generate key milestones narrative"""
        milestones = {
            "immediate_priorities": self._get_immediate_milestones(country, classification),
            "short_term_goals": self._get_short_term_milestones(country, classification),
            "long_term_vision": self._get_long_term_milestones(country, classification),
            "success_metrics": self._get_success_metrics(country, classification)
        }

        return milestones

    def _get_immediate_milestones(self, country, classification):
        """Get immediate milestones"""
        urgency = classification["urgency"]
        metrics = self.country_profiles[country]['key_metrics']

        if urgency == "critical":
            return [
                "Establish emergency AI preparedness task force",
                "Implement immediate capability building programs",
                "Secure international assistance and partnerships",
                "Prioritize critical sector protection"
            ]
        elif urgency == "high":
            return [
                "Accelerate AI education and skills development",
                "Strengthen digital infrastructure",
                "Develop comprehensive AI governance framework",
                "Build strategic public-private partnerships"
            ]
        else:
            return [
                "Conduct detailed AI readiness assessment",
                "Develop long-term AI strategy",
                "Build institutional capacity",
                "Establish monitoring and evaluation systems"
            ]

    def _generate_stakeholder_analysis(self, country, classification):
        """Generate stakeholder analysis"""
        stakeholders = {
            "government": self._analyze_government_stakeholders(country, classification),
            "private_sector": self._analyze_private_sector(country, classification),
            "civil_society": self._analyze_civil_society(country, classification),
            "international_partners": self._analyze_international_partners(country, classification),
            "research_community": self._analyze_research_community(country, classification)
        }

        return stakeholders

    def _generate_strategic_recommendations(self, country, classification):
        """Generate strategic recommendations"""
        archetype = classification["archetype_info"]
        recommendations = {
            "immediate_actions": archetype["narrative_elements"]["call_to_action"],
            "strategic_priorities": self._get_strategic_priorities(country, classification),
            "policy_recommendations": self._get_policy_recommendations(country, classification),
            "implementation_roadmap": self._get_implementation_roadmap(country, classification)
        }

        return recommendations

    def _generate_future_scenarios(self, country, classification):
        """Generate future scenarios"""
        scenarios = {
            "optimistic_scenario": self._generate_optimistic_scenario(country, classification),
            "realistic_scenario": self._generate_realistic_scenario(country, classification),
            "pessimistic_scenario": self._generate_pessimistic_scenario(country, classification)
        }

        return scenarios

    def _generate_optimistic_scenario(self, country, classification):
        """Generate optimistic future scenario"""
        crossing_year = classification.get("crossing_year")
        readiness = classification["readiness"]

        scenario = {
            "title": f"Optimistic Path for {country}",
            "probability": "20%",
            "description": f"In an optimistic scenario, {country} successfully prepares for AI integration, reaching readiness levels above 0.8 by {crossing_year if crossing_year else 2035}.",
            "key_factors": [
                "Strong political will and coordination",
                "Successful international partnerships",
                "Rapid technological adoption",
                "Effective public engagement"
            ],
            "outcomes": [
                "Leadership in AI governance",
                "Economic prosperity from AI integration",
                "Social stability during transition",
                "Global knowledge sharing"
            ]
        }

        return scenario

    def _generate_realistic_scenario(self, country, classification):
        """Generate realistic future scenario"""
        crossing_year = classification.get("crossing_year")
        readiness = classification["readiness"]

        scenario = {
            "title": f"Expected Path for {country}",
            "probability": "60%",
            "description": f"In the realistic scenario, {country} experiences a moderate AI transition with some challenges but ultimately successful adaptation by {crossing_year if crossing_year else 2040}.",
            "key_factors": [
                "Steady progress on preparation",
                "Managed technological adoption",
                "Adequate but not optimal coordination",
                "Gradual social adaptation"
            ],
            "outcomes": [
                "Successful AI integration",
                "Economic benefits with adjustments",
                "Social adaptation period",
                "Regional leadership position"
            ]
        }

        return scenario

    def _generate_pessimistic_scenario(self, country, classification):
        """Generate pessimistic future scenario"""
        crossing_year = classification.get("crossing_year")
        readiness = classification["readiness"]

        scenario = {
            "title": f"Challenged Path for {country}",
            "probability": "20%",
            "description": f"In a pessimistic scenario, {country} struggles with AI integration, facing significant challenges during the crossing period in {crossing_year if crossing_year else 2035}.",
            "key_factors": [
                "Insufficient preparation",
                "Institutional resistance",
                "International isolation",
                "Social disruption"
            ],
            "outcomes": [
                "Economic disruption",
                "Social unrest",
                "Need for international intervention",
                "Longer adaptation period"
            ]
        }

        return scenario

    def _generate_risk_assessment(self, country, classification):
        """Generate risk assessment"""
        risks = {
            "high_risks": self._identify_high_risks(country, classification),
            "medium_risks": self._identify_medium_risks(country, classification),
            "low_risks": self._identify_low_risks(country, classification),
            "mitigation_strategies": self._identify_mitigation_strategies(country, classification)
        }

        return risks

    def _generate_appendix(self, country, metrics):
        """Generate appendix with key metrics"""
        appendix = {
            "key_metrics": metrics,
            "timeline_projection": self._get_timeline_projection(country),
            "peer_comparisons": self.country_profiles[country]['peer_comparisons'],
            "data_sources": self._get_data_sources(country),
            "methodology_notes": self._get_methodology_notes(country)
        }

    def _get_present_indicators(self, country, classification):
        m = self.country_profiles.get(country, {}).get("key_metrics", {})
        return [
            f"Readiness Score: {m.get('readiness_score', classification['readiness']):.2f}",
            f"Exposure Level: {m.get('exposure_score', 'N/A')}",
            f"Current Gap: {m.get('gap_score', 'N/A')}",
            f"2026 Standing: {m.get('status_2026', 'Developing')}"
        ]

    def _get_near_future_indicators(self, country, classification):
        m = self.country_profiles.get(country, {}).get("key_metrics", {})
        crossing = m.get("most_likely_crossing", "2035+")
        prep = m.get("preparation_years", 5)
        return [
            "Projected Readiness Trajectory: +1-2% annual adaptation",
            f"Preparation Window: {prep} years remaining",
            f"Estimated Crossing Horizon: {crossing}",
            f"Urgency Classification: {classification['urgency'].title()}"
        ]

    def _get_long_term_indicators(self, country, classification):
        return [
            "Institutional alignment with frontier AI capability tiers",
            "Sustained workforce reskilling across exposed professions",
            "Participation in multilateral safety and standards regimes",
            "Systemic resilience to superintelligent capability shocks"
        ]

    def _get_crossing_indicators(self, country, classification):
        m = self.country_profiles.get(country, {}).get("key_metrics", {})
        return [
            f"Threshold Crossing Year: {m.get('most_likely_crossing', 2035)}",
            f"Crossing Probability: {m.get('crossing_probability', 0.5):.0%}",
            "Deficit Indicator: Exposure exceeds domestic absorptive capacity",
            "Trigger Level: Immediate structural mitigation required"
        ]

    def _get_short_term_milestones(self, country, classification):
        return [
            "Complete national AI audit across critical infrastructure",
            "Establish multi-stakeholder technical oversight committee",
            "Launch public-sector workforce digital discernment curriculum",
            "Publish baseline algorithmic risk assessments for labor markets"
        ]

    def _get_long_term_milestones(self, country, classification):
        return [
            "Achieve universal digital discernment and AI literacy across secondary education",
            "Integrate automated safety verifications into essential public systems",
            "Establish sovereign compute and evaluation capabilities",
            "Harmonize national guardrails with global non-compensatory safety accords"
        ]

    def _get_success_metrics(self, country, classification):
        return {
            "Readiness Target": "Composite score > 0.70 by 2030",
            "Labor Exposure Absorptive Rate": ">85% transitioning workforce re-employed",
            "Governance Verification": "Annual third-party frontier safety audits",
            "Infrastructure Redundancy": "Zero single-point failures in critical systems"
        }

    def _analyze_government_stakeholders(self, country, classification):
        return f"National ministries in {country} coordinate regulatory oversight, data governance, and strategic education initiatives."

    def _analyze_private_sector(self, country, classification):
        return f"Enterprises and technology developers in {country} are key drivers of absorption and must adhere to safety benchmarks."

    def _analyze_civil_society(self, country, classification):
        return f"Civil society organizations in {country} safeguard public trust, digital rights, and community resilience against synthetic media."

    def _analyze_international_partners(self, country, classification):
        return f"International bodies and bilateral partners facilitate knowledge exchange, threat monitoring, and mutual defense."

    def _analyze_research_community(self, country, classification):
        return f"Academia and research institutions in {country} lead validation, interpretability, and independent capability audits."

    def _get_strategic_priorities(self, country, classification):
        return [
            "Accelerate high-impact institutional capacity building",
            "Fortify digital infrastructure resilience and compute sovereignty",
            "Deploy nationwide critical discernment educational programs"
        ]

    def _get_policy_recommendations(self, country, classification):
        return [
            "Enact enforceable compliance mandates for high-capability frontier systems",
            "Create transitional safety nets and reskilling accounts for exposed workers",
            "Mandate cryptographic provenance standards for public communications"
        ]

    def _get_implementation_roadmap(self, country, classification):
        return {
            "Phase 1 (2026-2027)": "Emergency readiness assessment and baseline stabilization",
            "Phase 2 (2028-2030)": "Infrastructure scaling and regulatory harmonisation",
            "Phase 3 (2031+)": "Full system resilience and active superintelligence navigation"
        }

    def _identify_high_risks(self, country, classification):
        return [
            "Accelerated labor dislocation outpacing retraining speed",
            "Severe informational distortion impacting institutional decision-making"
        ]

    def _identify_medium_risks(self, country, classification):
        return [
            "Supply chain disruptions in high-end compute and networking hardware",
            "Regional regulatory fragmentation impeding collaborative defense"
        ]

    def _identify_low_risks(self, country, classification):
        return [
            "Public fatigue towards recurrent technology policy updates",
            "Minor transitional variance in consumer software ecosystems"
        ]

    def _identify_mitigation_strategies(self, country, classification):
        return [
            "Establish agile regulatory sandboxes with real-time feedback loops",
            "Maintain sovereign redundant communication and computational nodes",
            "Institutionalize non-compensatory thresholds in national risk registries"
        ]

    def _get_timeline_projection(self, country):
        m = self.country_profiles.get(country, {}).get("key_metrics", {})
        return {
            "status": m.get("status_2026", "Developing"),
            "most_likely_crossing": m.get("most_likely_crossing", "2035+"),
            "preparation_years": m.get("preparation_years", 0),
            "urgency": m.get("urgency_level", "medium"),
            "crossing_probability": m.get("crossing_probability", 0.5)
        }

    def _get_data_sources(self, country):
        return [
            "HSRI Composite Benchmark Dataset (2026)",
            "OECD AI Policy Observatory & Employment Outlook",
            "World Bank Governance Indicators & ITU Telecommunications Database",
            "Expert Delphi Surveys & Platform Capability Roadmaps"
        ]

    def _get_methodology_notes(self, country):
        return (
            "Readiness calculated via non-compensatory geometric aggregation across four pillars "
            "(AI Literacy, Critical Discernment, Institutional Governance, Digital Infrastructure). "
            "Exposure trajectories projected using multi-source probabilistic capability modeling."
        )

    def _generate_narrative_types_overview(self, classifications, archetypes):
        md = "# Narrative Archetypes Overview\n\n"
        md += "This document synthesizes the strategic archetypes across profiled benchmark nations.\n\n"
        for code, info in archetypes.items():
            assigned = [c for c, cl in classifications.items() if cl["archetype"] == code]
            md += f"## {info['name']}\n"
            md += f"{info['description']}\n\n"
            md += f"**Assigned Countries ({len(assigned)})**: {', '.join(sorted(assigned)) if assigned else 'None'}\n\n"
        return md

    def _generate_summary_report(self, classifications, archetypes):
        md = "# Narrative Integration Summary Report\n\n"
        md += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += f"Total Nations Profiled: {len(classifications)}\n\n"
        md += "## Archetype Distribution\n\n"
        dist = {}
        for c, cl in classifications.items():
            a = cl["archetype"]
            dist[a] = dist.get(a, 0) + 1
        for a, count in dist.items():
            md += f"- **{archetypes[a]['name']}**: {count} nations\n"
        return md

    def export_narratives(self, classifications, archetypes):
        """Export complete narratives"""
        logger.info("Exporting integrated narratives...")

        narratives_dir = self.project_root / "research" / "integrated_narratives"
        narratives_dir.mkdir(exist_ok=True)

        # Export individual country narratives
        for country, classification in classifications.items():
            narrative = self.generate_country_narrative(country, classification, archetypes)

            # JSON format
            json_file = narratives_dir / f"{country.lower()}_narrative.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(narrative, f, indent=2)

            # Markdown format
            md_file = narratives_dir / f"{country.lower()}_narrative.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(self._format_narrative_markdown(country, narrative))

        # Export narrative type overview
        overview_file = narratives_dir / "narrative_types_overview.md"
        with open(overview_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_narrative_types_overview(classifications, archetypes))

        # Export summary report
        summary_file = narratives_dir / "narrative_integration_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_summary_report(classifications, archetypes))

        logger.info(f"Integrated narratives exported to {narratives_dir}")

        return {
            "classifications": classifications,
            "archetypes": archetypes,
            "narratives_dir": narratives_dir,
            "summary_file": summary_file
        }

    def _format_narrative_markdown(self, country, narrative):
        """Format narrative as markdown"""
        md = f"# {country}: {narrative['title']}\n\n"

        # Executive Summary
        md += f"## Executive Summary\n{narrative['executive_summary']}\n\n"

        # Timeline Journey
        md += "## Timeline Journey\n"
        for phase_key, phase_data in narrative['timeline_journey'].items():
            if phase_key == "critical_crossing":
                md += f"### {phase_data['title']}\n{phase_data['description']}\n\n"
            else:
                md += f"### {phase_data['title']}\n{phase_data['description']}\n\n"

        # Strategic Context
        md += "## Strategic Context\n"
        for context_key, context_data in narrative['strategic_context'].items():
            md += f"### {context_key.replace('_', ' ').title()}\n{context_data}\n\n"

        # Key Milestones
        md += "## Key Milestones\n"
        for milestone_type, milestones in narrative['key_milestones'].items():
            if isinstance(milestones, list):
                md += f"### {milestone_type.replace('_', ' ').title()}\n"
                for milestone in milestones:
                    md += f"- {milestone}\n"
                md += "\n"
            elif isinstance(milestones, dict):
                md += f"### {milestone_type.replace('_', ' ').title()}\n"
                for key, value in milestones.items():
                    md += f"**{key}**: {value}\n"
                md += "\n"
            else:
                md += f"### {milestone_type.replace('_', ' ').title()}\n"
                md += f"{milestones}\n\n"

        # Recommendations
        md += "## Strategic Recommendations\n"
        for rec_type, recs in narrative['recommendations'].items():
            if isinstance(recs, list):
                md += f"### {rec_type.replace('_', ' ').title()}\n"
                for rec in recs:
                    md += f"- {rec}\n"
                md += "\n"
            elif isinstance(recs, dict):
                md += f"### {rec_type.replace('_', ' ').title()}\n"
                for key, value in recs.items():
                    md += f"**{key}**: {value}\n"
                md += "\n"
            else:
                md += f"### {rec_type.replace('_', ' ').title()}\n"
                md += f"{recs}\n\n"

        # Future Scenarios
        md += "## Future Scenarios\n"
        for scenario_type, scenario in narrative['future_scenarios'].items():
            md += f"### {scenario['title']} ({scenario['probability']})\n"
            md += f"{scenario['description']}\n\n"
            md += "**Key Factors:**\n"
            for factor in scenario['key_factors']:
                md += f"- {factor}\n"
            md += "\n"
            md += "**Expected Outcomes:**\n"
            for outcome in scenario['outcomes']:
                md += f"- {outcome}\n"
            md += "\n"

        return md

    def generate_all_narratives(self):
        """Generate all country narratives"""
        logger.info("Generating all country narratives...")

        # Classify countries into narrative types
        classifications, archetypes = self.classify_narrative_types()

        # Export complete narratives
        results = self.export_narratives(classifications, archetypes)

        logger.info("✅ Narrative integration completed successfully")
        return True

    def run_narrative_integration(self):
        """Run complete narrative integration process"""
        logger.info("Starting narrative integration...")

        # Load data
        if not self.load_data():
            return False

        # Generate all narratives
        if self.generate_all_narratives():
            logger.info("✅ Narrative integration completed successfully")
            return True
        else:
            logger.error("❌ Narrative integration failed")
            return False

def main():
    """Run the narrative integration process"""
    project_root = Path.cwd()
    integrator = NarrativeIntegrator(project_root)

    if integrator.run_narrative_integration():
        print("\n✅ Narrative integration completed successfully!")
        return 0
    else:
        print("\n❌ Narrative integration failed!")
        return 1

if __name__ == "__main__":
    exit(main())