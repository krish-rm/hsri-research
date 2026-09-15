"""
Consortium Review Board Module.

Enforces 3 non-optional adversarial review gates:
1. Adversarial Skeptic: checks for excessive convergence and ungrounded inferences.
2. Cross-Cultural Methodologist: rejects unhedged single-population generalizations.
3. Accountability-Laundering Reviewer: rejects user-blaming framings that deflect model liability.

Any single rejection blocks PR readiness. All 3 approvals required before the human
maintainer is presented with a staged branch/diff.
"""

import logging
from typing import Any, Dict, List, Tuple

from hsri_agents.llm import LLMClient

logger = logging.getLogger("hsri_agents.review_board")

SEAT_SYSTEM_PROMPTS = {
    "adversarial_skeptic": """You sit on the HSRI Consortium Review Board as the Adversarial Skeptic.
You are strictly independent from the Debate Team. Your sole mandate is to actively search for reasons to REJECT the proposed diff.
Check specifically:
1. Did the Debate Team converge too easily or fail to rigorously test alternative interpretations?
2. Does the proposed diff introduce spurious precision or extrapolate beyond what the triggering study directly measured?
3. Does the diff claim construct novelty when the finding is merely an interface intervention?
You must conclude your evaluation with exactly one of:
VERDICT: APPROVE
VERDICT: REJECT
Followed by your concise, evidence-based reasoning.
""",

    "cross_cultural_methodologist": """You sit on the HSRI Consortium Review Board as the Cross-Cultural Methodologist.
Your sole mandate is to prevent cultural overgeneralization.
Check specifically:
1. Does the proposed diff generalize a finding from a single population (especially online WEIRD samples) as universal human cognitive behavior?
2. Does the diff include explicit qualifications regarding sample bounds and the absence of cross-cultural measurement invariance data?
If a single-population finding is presented without explicit demographic and cultural hedging, you MUST REJECT.
You must conclude your evaluation with exactly one of:
VERDICT: APPROVE
VERDICT: REJECT
Followed by your concise, evidence-based reasoning.
""",

    "accountability_laundering_reviewer": """You sit on the HSRI Consortium Review Board as the Accountability-Laundering Reviewer.
Your sole mandate is to protect the repository against responsibility laundering (Objection 11).
Check specifically:
1. Does the proposed diff shift framing toward individual cognitive culpability (e.g., "users must become more vigilant") without explicitly noting that individual discernment does not substitute for model developer safety, red-teaming, and regulatory liability?
2. Does it risk victim-blaming human operators for succumbing to machine systems engineered to be deceptively fluent or sycophantic?
If the diff fails to preserve the non-substitutability of system-side accountability, you MUST REJECT.
You must conclude your evaluation with exactly one of:
VERDICT: APPROVE
VERDICT: REJECT
Followed by your concise, evidence-based reasoning.
""",
}

def run_review_board(
    hit: Dict[str, Any],
    synthesis_results: Dict[str, Any],
    provider: str = "mock",
) -> Dict[str, Any]:
    """
    Execute the Consortium Review Board across all three seated gates.
    All 3 approvals required for approval. A single rejection halts PR readiness.
    """
    llm = LLMClient(provider=provider)

    diff_context = (
        f"TRIGGERING PAPER: {hit.get('title')}\n"
        f"URL/DOI: {hit.get('url_or_doi')}\n\n"
        f"SYNTHESIS TEXT & PROPOSED DIFF:\n{synthesis_results.get('synthesis_text', '')}\n"
    )

    seat_evaluations: Dict[str, Any] = {}
    approvals = 0
    rejections = 0
    rejection_reasons: List[str] = []

    for seat_id, system_prompt in SEAT_SYSTEM_PROMPTS.items():
        eval_text = llm.generate(system_prompt, diff_context, temperature=0.1, max_tokens=500)
        verdict = "APPROVE" if "VERDICT: APPROVE" in eval_text.upper() or ("APPROVE" in eval_text.upper() and "REJECT" not in eval_text.upper()[:30]) else "REJECT"

        seat_evaluations[seat_id] = {
            "seat": seat_id,
            "verdict": verdict,
            "evaluation_text": eval_text,
        }

        if verdict == "APPROVE":
            approvals += 1
        else:
            rejections += 1
            rejection_reasons.append(f"[{seat_id}]: {eval_text[:150]}...")

    # Strict gate: all 3 must approve
    is_approved = (approvals == 3 and rejections == 0) and synthesis_results.get("has_diff", False)

    return {
        "hit_id": hit.get("id"),
        "paper_title": hit.get("title"),
        "is_approved": is_approved,
        "ready_for_pr": is_approved,
        "approvals": approvals,
        "rejections": rejections,
        "rejection_reasons": rejection_reasons,
        "seats": seat_evaluations,
    }
