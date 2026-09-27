"""
HSRI Lane 4 — Consortium Review Board
Evaluates a proposed diff from Lane 3 debate through three adversarial veto seats.
Any single VETO blocks PR creation. All three must APPROVE for PR generation.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from hsri_agents.config import get_api_key
from hsri_agents.llm import LLMClient
from hsri_agents.review_board import SEAT_PROMPTS, evaluate_board_verdict


def run_consortium_review_board(
    diff_context: str,
    provider: str = "google",
    model: str = "gemini-3.8-flash",
) -> Dict[str, Any]:
    """Execute evaluation across the three Review Board seats."""
    has_key = bool(get_api_key(provider))
    client = LLMClient(provider=provider if has_key else "mock", model=model, allow_fallback=True)
    seat_results = []
    print("\n--- LANE 4 CONSORTIUM REVIEW BOARD ---")
    for seat_id, prompt in SEAT_PROMPTS.items():
        print(f"Evaluating seat: {seat_id}...")
        resp = client.generate(prompt, diff_context, temperature=0.1)
        verdict = "VETO" if ("VERDICT: VETO" in resp.upper() or "VETO" in resp.upper()[:40]) else "APPROVE"
        seat_results.append({
            "seat": seat_id,
            "verdict": verdict,
            "response": resp,
        })
        print(f"  {seat_id}: {verdict}")

    board_outcome = evaluate_board_verdict(seat_results)
    status_str = "BLOCKED" if board_outcome["blocked"] else "PR ELIGIBLE"
    print(f"Board Decision: {status_str}")
    return {
        "seat_results": seat_results,
        "outcome": board_outcome,
    }


if __name__ == "__main__":
    sample_context = (
        "PROPOSED DIFF:\n"
        "Path: docs/04-causal-model-and-index-design.md\n"
        "Change: Adjust Critical Discernment weight from 25% to 20%."
    )
    run_consortium_review_board(sample_context)
