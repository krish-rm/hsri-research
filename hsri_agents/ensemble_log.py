"""
Multi-Model Ensemble Concordance and Epistemic Diversity Module.

Evaluates cross-model agreement across frontier LLM families.
Enforces that fewer than 5/7 agreement marks a topic as CONTESTED
and gates submission to the Consortium Review Board.
"""

from collections import Counter
from typing import Any, Dict, List, Optional


def evaluate_concordance(
    verdicts: List[str],
    threshold: int = 5,
    total_expected: int = 7,
) -> Dict[str, Any]:
    """
    Evaluate concordance across model family verdicts.
    Requires at least threshold agreement (default 5/7) to pass.
    """
    if not verdicts:
        return {
            "passes_threshold": False,
            "status": "CONTESTED — HUMAN ARBITRATION REQUIRED",
            "concordance_count": 0,
            "dominant_verdict": None,
            "total_verdicts": 0,
        }

    counts = Counter(verdicts)
    dominant_verdict, dominant_count = counts.most_common(1)[0]
    passes = dominant_count >= threshold

    status = (
        f"CONCORDANCE ACHIEVED ({dominant_count}/{len(verdicts)} — {dominant_verdict})"
        if passes
        else "CONTESTED — HUMAN ARBITRATION REQUIRED"
    )

    return {
        "passes_threshold": passes,
        "status": status,
        "dominant_verdict": dominant_verdict,
        "concordance_count": dominant_count,
        "total_verdicts": len(verdicts),
    }
