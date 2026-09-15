"""
Construct Debate Team Module.

Implements structured, adversarial debate between a Proponent and a Skeptic across
configurable rounds (2-3), reading all 4 analyst briefs. Preserves the full verbatim
debate transcript.
"""

import logging
from typing import Any, Dict, List

from hsri_agents.llm import LLMClient

logger = logging.getLogger("hsri_agents.debate")

PROPONENT_SYSTEM_PROMPT = """You are the Proponent in the HSRI Construct Debate Team.
Your objective is to argue the strongest defensible case that the new evidence supports
the incremental-validity gap being real, or warrants an update/strengthening of the HSRI
evidence table and experimental battery.

Grounding rules:
1. You must ground every claim strictly in the four Analyst briefs or the provided paper abstract/text.
2. Do not appeal to intuition, hype, or vague futurology about superintelligence.
3. If an effect size or sample size is stated, verify that it was directly quoted by an analyst; do not extrapolate numbers.
4. Address the Skeptic's objections directly with specific evidence rather than rhetorical dismissal.
"""

SKEPTIC_SYSTEM_PROMPT = """You are the Skeptic in the HSRI Construct Debate Team.
Your objective is to argue the null hypothesis: that the newly presented evidence remains
fully consistent with construct redundancy (existing psychology), that an interface intervention
is being conflated with a novel human cognitive trait, or that the paper is being over-read.

Adversarial auditing rules:
1. Actively check for the "precision without verification" failure mode: if the Proponent cites any tight number, percentage, or effect size not verified in the source text, call it out explicitly.
2. Check for sample limitations (e.g., WEIRD crowdsourced samples) and demand that findings not be generalized universally.
3. Check for construct proliferation: does this finding simply reflect general critical thinking, Need for Cognition, or classic automation bias under another name?
4. Do not concede the existence of a new psychological faculty unless incremental predictive validity is conclusively demonstrated.
"""

def run_debate(
    hit: Dict[str, Any],
    analyst_results: Dict[str, Any],
    rounds: int = 2,
    provider: str = "mock",
) -> Dict[str, Any]:
    """
    Run an adversarial multi-round debate between Proponent and Skeptic.
    Returns the complete verbatim transcript.
    """
    llm = LLMClient(provider=provider)
    rounds = max(1, min(rounds, 3))

    briefs_text = "\n\n".join([
        f"--- {b['lane'].upper()} BRIEF (Status: {b['impact_status']}) ---\n{b['brief_text']}"
        for b in analyst_results.get("briefs", {}).values()
    ])

    paper_context = (
        f"Title: {hit.get('title', 'Unknown')}\n"
        f"Authors: {', '.join(hit.get('authors', []))}\n"
        f"Venue: {hit.get('venue', 'Unknown')}\n"
        f"URL/DOI: {hit.get('url_or_doi', 'N/A')}\n\n"
        f"Abstract:\n{hit.get('abstract', '')}\n\n"
        f"ANALYST BRIEFS:\n{briefs_text}"
    )

    transcript: List[Dict[str, str]] = []
    dialogue_history = ""

    for round_num in range(1, rounds + 1):
        # 1. Proponent Turn
        proponent_user_prompt = (
            f"TARGET EVIDENCE AND BRIEFS:\n{paper_context}\n\n"
            f"DEBATE TRANSCRIPT SO FAR:\n{dialogue_history}\n\n"
            f"Round {round_num}: Present your grounded argument for why this evidence bears on HSRI's evidence table or incremental validity."
        )
        prop_response = llm.generate(PROPONENT_SYSTEM_PROMPT, proponent_user_prompt, temperature=0.3, max_tokens=750)
        transcript.append({
            "round": round_num,
            "speaker": "Proponent",
            "content": prop_response,
        })
        dialogue_history += f"\n\n**PROPONENT (Round {round_num}):**\n{prop_response}"

        # 2. Skeptic Turn
        skeptic_user_prompt = (
            f"TARGET EVIDENCE AND BRIEFS:\n{paper_context}\n\n"
            f"DEBATE TRANSCRIPT SO FAR:\n{dialogue_history}\n\n"
            f"Round {round_num}: Present your adversarial counterargument defending the null and checking for unverified precision or overclaiming."
        )
        skep_response = llm.generate(SKEPTIC_SYSTEM_PROMPT, skeptic_user_prompt, temperature=0.3, max_tokens=750)
        transcript.append({
            "round": round_num,
            "speaker": "Skeptic",
            "content": skep_response,
        })
        dialogue_history += f"\n\n**SKEPTIC (Round {round_num}):**\n{skep_response}"

    return {
        "hit_id": hit.get("id"),
        "paper_title": hit.get("title"),
        "rounds_completed": rounds,
        "transcript": transcript,
        "full_dialogue_text": dialogue_history.strip(),
    }
