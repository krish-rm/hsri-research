"""
Systematic Review Synthesizer Module.

Reads the full verbatim debate transcript and drafts either a concrete proposed diff
tagged to its source, or an explicit NO CHANGE verdict. May not soften Skeptic objections.
"""

import logging
from typing import Any, Dict

from hsri_agents.llm import LLMClient

logger = logging.getLogger("hsri_agents.synthesizer")

SYNTHESIZER_SYSTEM_PROMPT = """You are the Systematic Review Synthesizer for HSRI.
Your function is to evaluate the complete debate transcript and determine whether
the evidence warrants a concrete documentation or evidence-table diff, or a verdict of NO CHANGE.

Critical constraints:
1. You may NOT soften Skeptic objections to make a diff appear more decisive.
2. If the debate ended in genuine disagreement or unresolved methodological critique (e.g., sample generalizability or construct redundancy), the synthesis MUST explicitly document that disagreement rather than picking a side.
3. If proposing a diff:
   - Must specify the target file (e.g., evidence/master-evidence-table.csv or docs/07-objections.md).
   - Must provide exact diff lines (with + and -).
   - Must tag every changed or added claim strictly to its verifiable source citation and DOI.
   - Must include all required caveats (e.g., WEIRD sample limitations, non-substitutability for AI developer liability).
4. If the evidence does not convincingly justify an update, you must return an explicit:
   "NO CHANGE — evidence insufficient" followed by a single concise sentence of reasoning.
"""

def run_synthesizer(
    hit: Dict[str, Any],
    debate_results: Dict[str, Any],
    provider: str = "mock",
) -> Dict[str, Any]:
    """
    Run the Systematic Review Synthesizer on the full debate transcript.
    Returns the synthesis decision, reasoning, and proposed diff (if any).
    """
    llm = LLMClient(provider=provider)

    user_prompt = (
        f"TRIGGERING PAPER:\n"
        f"Title: {hit.get('title')}\n"
        f"Authors: {', '.join(hit.get('authors', []))}\n"
        f"Venue: {hit.get('venue')}\n"
        f"URL/DOI: {hit.get('url_or_doi')}\n\n"
        f"FULL DEBATE TRANSCRIPT:\n{debate_results.get('full_dialogue_text', '')}\n\n"
        f"Evaluate the debate and produce your synthesis. Draft either a concrete proposed diff or an explicit NO CHANGE verdict."
    )

    synthesis_text = llm.generate(SYNTHESIZER_SYSTEM_PROMPT, user_prompt, temperature=0.2, max_tokens=1000)

    verdict = "PROPOSED DIFF" if ("proposed diff" in synthesis_text.lower() or "--- a/" in synthesis_text or "diff" in synthesis_text.lower()) and "no change" not in synthesis_text.lower()[:50] else "NO CHANGE"

    return {
        "hit_id": hit.get("id"),
        "paper_title": hit.get("title"),
        "verdict": verdict,
        "synthesis_text": synthesis_text,
        "has_diff": verdict == "PROPOSED DIFF",
    }
