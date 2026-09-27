"""
HSRI Lane 4 — Consortium Review Board
Evaluates a proposed diff from Lane 3 debate through three adversarial veto seats.
Any single VETO blocks PR creation. All three must APPROVE for PR generation.
"""

from typing import Any, Dict, List
from hsri_agents.llm import LLMClient

SEAT_PROMPTS = {
    "adversarial_skeptic": """
You are Seat 1 of the HSRI Consortium Review Board: the Adversarial Skeptic.
You receive a proposed change to the HSRI methodology or data.
Your role is to block changes that do not meet the evidentiary bar required
for a peer-reviewed publication.

Veto criteria (any one is sufficient to block):
- Sample size N < 100
- Single-institution sample with no replication
- Effect size below practical significance (Cohen's d < 0.3)
- Not pre-registered
- WEIRD-only sample with no cross-cultural validation

Output format:
VERDICT: APPROVE | VETO
REASON: [one paragraph]
VETO_CRITERIA_TRIGGERED: [list, or NONE]
""",
    "cross_cultural_methodologist": """
You are Seat 2 of the HSRI Consortium Review Board: the Cross-Cultural Methodologist.
Your role is to block changes that introduce measurement non-equivalence across
HSRI's 39 benchmarked economies or that systematically disadvantage non-Western nations.

Veto criteria:
- Change advantages OECD-core nations over non-OECD benchmark nations
- Change introduces construct non-equivalence across cultural contexts
- Change worsens coverage for the 86 unrated nations

Output format:
VERDICT: APPROVE | VETO
REASON: [one paragraph]
AFFECTED_NATIONS: [list of ISO3 codes most impacted, or NONE]
""",
    "accountability_laundering_reviewer": """
You are Seat 3 of the HSRI Consortium Review Board: the Accountability Laundering Reviewer.
Your role is to block changes that — even if empirically valid — could be cited
by governments or institutions to justify surveillance, exclusion, or ranking harm.

Veto criteria:
- Change could be used to launder political or economic biases into an
  authoritative-seeming benchmark without explicit caveat
- Harm potential is not explicitly documented in the change rationale
- Change narrows the construct in ways that systematically exclude
  non-Western political or governance models

Output format:
VERDICT: APPROVE | VETO
REASON: [one paragraph]
HARM_SCENARIO: [brief description of potential misuse, or NONE]
"""
}

# Alias for backwards compatibility with earlier Lane 4 tests
SEAT_SYSTEM_PROMPTS = SEAT_PROMPTS


def evaluate_board_verdict(seat_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluate outcomes across the three review board seats.
    Any single VETO blocks PR creation. All three must APPROVE for PR generation.
    """
    vetoes = [s for s in seat_results if s.get("verdict") == "VETO"]
    if vetoes:
        return {
            "blocked": True,
            "blocking_seat": vetoes[0].get("seat"),
            "blocking_reason": vetoes[0].get("reason", "Veto criteria triggered"),
            "pr_created": False,
            "pr_eligible": False,
        }

    approvals = [s for s in seat_results if s.get("verdict") == "APPROVE"]
    if len(approvals) == len(seat_results) and len(seat_results) == 3:
        return {
            "blocked": False,
            "blocking_seat": None,
            "blocking_reason": None,
            "pr_eligible": True,
            "pr_created": False,
        }

    return {
        "blocked": True,
        "blocking_seat": "incomplete_board",
        "blocking_reason": "Not all seats produced approval",
        "pr_created": False,
        "pr_eligible": False,
    }


def evaluate_pr_eligibility(
    pipeline_status: Dict[str, Any],
    debate_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Gate PR readiness on Lane 2 data pipeline sentinel status.
    A HOLD-RELEASE verdict from the pipeline sentinel unconditionally blocks
    any PR from being generated, even if the debate team or review board reaches consensus.
    """
    verdict = pipeline_status.get("verdict", "")
    if verdict == "HOLD-RELEASE":
        flag = pipeline_status.get("flag", "DATA_INTEGRITY_DRIFT")
        return {
            "eligible": False,
            "blocked": True,
            "block_reason": f"Lane 2 pipeline HOLD-RELEASE active ({flag}). Automated PR generation strictly blocked.",
        }

    return {
        "eligible": True,
        "blocked": False,
        "block_reason": "",
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

    for seat_id, system_prompt in SEAT_PROMPTS.items():
        eval_text = llm.generate(system_prompt, diff_context, temperature=0.1, max_tokens=500)
        verdict = "APPROVE" if "VERDICT: APPROVE" in eval_text.upper() or ("APPROVE" in eval_text.upper() and "REJECT" not in eval_text.upper()[:30] and "VETO" not in eval_text.upper()[:30]) else "VETO"

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
