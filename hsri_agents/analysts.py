"""
Evidence Analysts Module.

Implements 4 strictly separated analyst roles (Psychometrics, HAI-Interaction,
Cross-Cultural Methods, Governance/Ethics). Each reads only the triggering paper
and its specific evidence-table lane to produce a bounded brief under 400 words.
"""

import csv
import datetime
import logging
from typing import Any, Dict, List, Tuple

from hsri_agents.config import EVIDENCE_TABLE_PATH
from hsri_agents.llm import LLMClient

logger = logging.getLogger("hsri_agents.analysts")

ANALYST_SYSTEM_PROMPTS = {
    "psychometrics": """You are the Psychometrics Analyst for HSRI.
Your lane is construct validity, redundancy audit, and psychometric measurement standards.
You must answer:
1. Does this paper bear on construct validity, redundancy with existing instruments (ANT, CRT, CIHS, meta-d'), or measurement invariance?
2. Does it change any evidence-tier rating (Strong, Moderate, Preliminary, Theoretical, Speculative) in the evidence table?
3. State your assessment strictly and conservatively under 400 words.
Do not invent any statistics, effect sizes, or sample numbers not explicitly stated in the source text.
Your brief MUST conclude with exactly one of these three lines:
NO EVIDENCE-TABLE IMPACT
POSSIBLE IMPACT — flag for debate
DIRECT IMPACT — cites [specific row/construct]
""",

    "hai_interaction": """You are the HAI-Interaction Analyst for HSRI.
Your lane is human-AI interaction: calibrated trust, automation bias (omission/commission errors), cognitive offloading, and cognitive-forcing-function findings (the Buçinca et al. / Bansal et al. lineage).
You must answer:
1. Does this paper provide empirical findings on reliance ratios, trust calibration, or over-reliance under automated assistance?
2. Does it replicate or challenge the finding that passive explanations fail while forced deliberation reduces automation bias?
3. State your assessment strictly under 400 words.
Do not invent any effect sizes or experimental numbers not in the abstract/paper.
Your brief MUST conclude with exactly one of these three lines:
NO EVIDENCE-TABLE IMPACT
POSSIBLE IMPACT — flag for debate
DIRECT IMPACT — cites [specific row/construct]
""",

    "cross_cultural": """You are the Cross-Cultural Methods Analyst for HSRI.
Your lane is sample demographics, cultural generalizability, and measurement invariance.
You must answer:
1. What was the sample composition of this study? Does it rely on Western, Educated, Industrialized, Rich, Democratic (WEIRD) online crowdsourced cohorts?
2. Does the study conduct or report multi-group measurement invariance testing (configural, metric, scalar)?
3. If the paper's findings are treated as universal human behavior, does this overgeneralize a culturally contingent norm of autonomy?
State your brief strictly under 400 words.
Your brief MUST conclude with exactly one of these three lines:
NO EVIDENCE-TABLE IMPACT
POSSIBLE IMPACT — flag for debate
DIRECT IMPACT — cites [specific row/construct]
""",

    "governance_ethics": """You are the Governance and Ethics Analyst for HSRI.
Your lane is institutional misuse, ethical safeguards, and the accountability-laundering objection (Objection 11).
You must answer:
1. Does this paper or its framing risk shifting responsibility away from AI model developers/regulators onto individual users for being deceived by manipulative systems?
2. Does it bear on workplace screening, paternalistic categorization, or surveillance justification?
3. What safeguards or governance disclaimers are required if this finding is incorporated?
State your brief strictly under 400 words.
Your brief MUST conclude with exactly one of these three lines:
NO EVIDENCE-TABLE IMPACT
POSSIBLE IMPACT — flag for debate
DIRECT IMPACT — cites [specific row/construct]
""",
}

def load_lane_evidence(lane: str) -> str:
    """Extract evidence rows relevant to the specific analyst's lane."""
    if not EVIDENCE_TABLE_PATH.exists():
        return "No local evidence table found."

    relevant_rows = []
    with open(EVIDENCE_TABLE_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            claim = row.get("claim", "").lower()
            tier = row.get("evidence_tier", "")
            citation = row.get("source_citation", "")

            if lane == "psychometrics" and any(k in claim for k in ["construct", "redundant", "ant", "crt", "metacognit", "humility", "instrument", "invariance"]):
                relevant_rows.append(f"- [{tier}] {claim} ({citation})")
            elif lane == "hai_interaction" and any(k in claim for k in ["automation bias", "trust", "reliance", "forcing function", "explanation", "offload"]):
                relevant_rows.append(f"- [{tier}] {claim} ({citation})")
            elif lane == "cross_cultural" and any(k in claim for k in ["cultural", "western", "invariance", "collectiv", "individual"]):
                relevant_rows.append(f"- [{tier}] {claim} ({citation})")
            elif lane == "governance_ethics" and any(k in claim for k in ["laundering", "responsibility", "surveillance", "employer", "paternalism", "screen"]):
                relevant_rows.append(f"- [{tier}] {claim} ({citation})")

    return "\n".join(relevant_rows[:6]) if relevant_rows else "No specific prior claims in lane."

def run_analysts(hit: Dict[str, Any], provider: str = "mock") -> Dict[str, Any]:
    """
    Run all 4 analysts in parallel/sequence on a candidate hit.
    Produces a brief for each role.
    """
    llm = LLMClient(provider=provider)
    date_str = datetime.date.today().isoformat()

    paper_context = (
        f"Title: {hit.get('title', 'Unknown')}\n"
        f"Authors: {', '.join(hit.get('authors', []))}\n"
        f"Venue: {hit.get('venue', 'Unknown')}\n"
        f"Date: {hit.get('date', date_str)}\n"
        f"URL/DOI: {hit.get('url_or_doi', 'N/A')}\n\n"
        f"Abstract:\n{hit.get('abstract', '')}\n"
    )

    briefs = {}
    max_impact = "NO EVIDENCE-TABLE IMPACT"

    for lane, system_prompt in ANALYST_SYSTEM_PROMPTS.items():
        prior_evidence = load_lane_evidence(lane)
        user_prompt = (
            f"EVALUATION DATE: {date_str}\n\n"
            f"TARGET PAPER:\n{paper_context}\n\n"
            f"RELEVANT EVIDENCE TABLE BASELINE IN YOUR LANE:\n{prior_evidence}\n\n"
            f"Produce your bounded brief (<400 words) concluding with an explicit impact status."
        )

        brief_text = llm.generate(system_prompt, user_prompt, temperature=0.2, max_tokens=600)
        briefs[lane] = {
            "date": date_str,
            "lane": lane,
            "brief_text": brief_text,
            "impact_status": extract_impact_status(brief_text),
        }

        # Track overall impact status
        status = briefs[lane]["impact_status"]
        if "DIRECT" in status:
            max_impact = "DIRECT IMPACT"
        elif "POSSIBLE" in status and max_impact != "DIRECT IMPACT":
            max_impact = "POSSIBLE IMPACT"

    return {
        "hit_id": hit.get("id"),
        "paper_title": hit.get("title"),
        "overall_impact": max_impact,
        "eligible_for_debate": max_impact in ["DIRECT IMPACT", "POSSIBLE IMPACT"],
        "briefs": briefs,
    }

def extract_impact_status(text: str) -> str:
    """Extract the concluding impact status line."""
    upper = text.upper()
    if "DIRECT IMPACT" in upper:
        return "DIRECT IMPACT"
    elif "POSSIBLE IMPACT" in upper:
        return "POSSIBLE IMPACT"
    elif "NO EVIDENCE-TABLE IMPACT" in upper or "NO IMPACT" in upper:
        return "NO EVIDENCE-TABLE IMPACT"
    return "NO EVIDENCE-TABLE IMPACT"
