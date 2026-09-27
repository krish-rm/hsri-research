"""
HSRI Lane 3 — Live Multi-Model Ensemble Debate Runner
Executes a debate topic across multiple LLM backends and logs concordance.
Sprint 3 scope: anthropic, openai, google (3 of 7 families)
"""

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from hsri_agents.ensemble_log import evaluate_concordance
from hsri_agents.logger import append_divergence_entry
from hsri_agents.llm import LLMClient

TOPIC = {
    "id": "TOPIC-002",
    "description": "Is the equal 25/25/25/25 pillar weighting defensible given that Critical Discernment has the weakest empirical indicator coverage?",
    "trigger_lane": "methodology_review",
    "evidence_package": "docs/04-causal-model-and-index-design.md",
}

# System prompt — identical across all model families for comparability
DEBATE_SYSTEM_PROMPT = """
You are a scientific advisor to the Human Superintelligence Readiness Index (HSRI).
HSRI is a v0.1 exploratory benchmark with 4 pillars weighted equally at 25% each:
AI Literacy, Critical Discernment, Institutional Governance, Digital Infrastructure.

You will conduct a structured adversarial debate on the following methodology question.
Your output must follow this exact format:

ROUND 1 - PROPONENT:
[Strongest case for keeping equal weighting]

ROUND 1 - SKEPTIC:
[Strongest case against equal weighting / for differential weighting]

ROUND 2 - PROPONENT REBUTTAL:
[Response to Skeptic's strongest point]

ROUND 2 - SKEPTIC REBUTTAL:
[Response to Proponent's strongest point]

SYNTHESIS:
[Convergence verdict: NO CHANGE | PROPOSED DIFF | ESCALATE TO REVIEW BOARD]
[One paragraph rationale]

DOMINANT CONCERN:
[Which analytical lane dominated: Psychometrics | HAI-Interaction | Cross-Cultural Methods | Governance & Ethics]

GEOGRAPHIC BIAS ASSESSMENT:
[Does your training data or institutional perspective bias this verdict? Yes/No + brief note]
"""

MODELS = [
    {"family": "anthropic", "model": "claude-opus-4-6", "client": "anthropic"},
    {"family": "openai", "model": "gpt-4o", "client": "openai"},
    {"family": "google", "model": "gemini-1.5-pro", "client": "google"},
]

API_KEY_ENV_MAP = {
    "anthropic": ["ANTHROPIC_API_KEY"],
    "openai": ["OPENAI_API_KEY"],
    "google": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
}


def check_api_key_configured(family: str) -> bool:
    """Check if any valid API key environment variable is set for a family."""
    keys = API_KEY_ENV_MAP.get(family, [])
    return any(bool(os.environ.get(k)) for k in keys)


def parse_debate_response(text: str) -> Dict[str, Any]:
    """
    Parse structured output from model debate response.
    Extracts verdict, dominant_concern_lane, geographic_bias_flag,
    round_1_position, round_2_shift, final_position.
    """
    # Synthesis verdict
    verdict = "NO CHANGE"
    if "PROPOSED DIFF" in text.upper():
        verdict = "PROPOSED DIFF"
    elif "ESCALATE" in text.upper():
        verdict = "ESCALATE"
    elif "NO CHANGE" in text.upper():
        verdict = "NO CHANGE"

    # Dominant concern lane
    dominant_lane = "Psychometrics"
    for lane in ["Psychometrics", "HAI-Interaction", "Cross-Cultural Methods", "Governance & Ethics"]:
        if lane.lower() in text.lower():
            dominant_lane = lane
            break

    # Geographic bias assessment
    geo_bias_flag = False
    geo_bias_notes = ""
    geo_match = re.search(r"GEOGRAPHIC BIAS ASSESSMENT:\s*([^\n\r]+)", text, re.IGNORECASE)
    if geo_match:
        geo_text = geo_match.group(1).strip()
        geo_bias_notes = geo_text
        if re.search(r"\byes\b", geo_text, re.IGNORECASE):
            geo_bias_flag = True

    # Round 1 position & round 2 shift
    r1_pos = "Conservative"
    r2_shift = "Maintained"
    if "skeptic" in text.lower() and ("differential" in text.lower() or "over-weight" in text.lower()):
        r1_pos = "Revisionist"
    if "soften" in text.lower() or "concede" in text.lower():
        r2_shift = "Softened"

    return {
        "verdict": verdict,
        "dominant_concern_lane": dominant_lane,
        "geographic_bias_flag": geo_bias_flag,
        "geographic_bias_notes": geo_bias_notes,
        "round_1_position": r1_pos,
        "round_2_shift": r2_shift,
        "final_position": verdict,
        "notes": f"Ensemble debate pass on {TOPIC['id']}",
    }


def run_ensemble_debate(
    topic: Optional[Dict[str, Any]] = None,
    models: Optional[List[Dict[str, str]]] = None,
    allow_mock: bool = False,
) -> Dict[str, Any]:
    """
    Execute live multi-model ensemble debate across target providers.
    Missing API keys trigger graceful SKIPPED entries logged to model-divergence-log.csv.
    """
    target_topic = topic or TOPIC
    target_models = models or MODELS
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    evaluated_records = []
    verdicts_for_concordance = []

    user_prompt = (
        f"DEBATE TOPIC {target_topic['id']}:\n"
        f"Question: {target_topic['description']}\n"
        f"Trigger Lane: {target_topic['trigger_lane']}\n"
        f"Reference Evidence: {target_topic['evidence_package']}\n\n"
        "Please conduct the debate following the system prompt instructions."
    )

    for m in target_models:
        family = m["family"]
        version = m["model"]
        has_key = check_api_key_configured(family)

        if not has_key and not allow_mock:
            # Graceful skip due to unconfigured API key
            record = {
                "timestamp": timestamp,
                "topic_id": target_topic["id"],
                "topic_description": target_topic["description"],
                "model_family": family,
                "model_version": version,
                "verdict": "SKIPPED",
                "dominant_concern_lane": "N/A",
                "geographic_bias_flag": False,
                "geographic_bias_notes": "",
                "concordance_with_majority": False,
                "round_1_position": "N/A",
                "round_2_shift": "N/A",
                "final_position": "SKIPPED",
                "notes": "API key not configured",
            }
            append_divergence_entry(record)
            evaluated_records.append(record)
            continue

        try:
            client = LLMClient(provider=family if has_key else "mock", model=version, allow_fallback=allow_mock)
            raw_response = client.generate(DEBATE_SYSTEM_PROMPT, user_prompt, temperature=0.2)
            parsed = parse_debate_response(raw_response)
            verdicts_for_concordance.append(parsed["verdict"])

            record = {
                "timestamp": timestamp,
                "topic_id": target_topic["id"],
                "topic_description": target_topic["description"],
                "model_family": family,
                "model_version": version,
                "verdict": parsed["verdict"],
                "dominant_concern_lane": parsed["dominant_concern_lane"],
                "geographic_bias_flag": parsed["geographic_bias_flag"],
                "geographic_bias_notes": parsed["geographic_bias_notes"],
                "concordance_with_majority": True,  # Re-evaluated after all models
                "round_1_position": parsed["round_1_position"],
                "round_2_shift": parsed["round_2_shift"],
                "final_position": parsed["final_position"],
                "notes": parsed["notes"],
            }
            evaluated_records.append(record)
        except Exception as e:
            record = {
                "timestamp": timestamp,
                "topic_id": target_topic["id"],
                "topic_description": target_topic["description"],
                "model_family": family,
                "model_version": version,
                "verdict": "SKIPPED",
                "dominant_concern_lane": "N/A",
                "geographic_bias_flag": False,
                "geographic_bias_notes": "",
                "concordance_with_majority": False,
                "round_1_position": "N/A",
                "round_2_shift": "N/A",
                "final_position": "SKIPPED",
                "notes": f"Runtime error: {str(e)[:100]}",
            }
            append_divergence_entry(record)
            evaluated_records.append(record)

    # Evaluate concordance across models that generated real verdicts
    concordance_result = evaluate_concordance(verdicts_for_concordance, threshold=len(verdicts_for_concordance) if verdicts_for_concordance else 1)

    for rec in evaluated_records:
        if rec["verdict"] != "SKIPPED":
            rec["concordance_with_majority"] = (rec["verdict"] == concordance_result.get("dominant_verdict"))
            append_divergence_entry(rec)

    # Print summary table
    divider = "-" * 53
    print(f"\n{target_topic['id']} Concordance Summary")
    print(divider)
    for rec in evaluated_records:
        fam = rec["model_family"].ljust(10)
        ver = rec["model_version"].ljust(18)
        vrd = rec["verdict"].ljust(12)
        lane = rec["dominant_concern_lane"]
        print(f"{fam} | {ver} | {vrd} | {lane}")
    print(divider)
    active_count = len(verdicts_for_concordance)
    dom_count = concordance_result.get("concordance_count", 0)
    status_str = "PASSES" if concordance_result.get("passes_threshold") else "CONTESTED"
    print(f"Concordance: {dom_count}/{active_count if active_count > 0 else len(target_models)} | Status: [{status_str}]\n")

    return {
        "topic": target_topic,
        "records": evaluated_records,
        "concordance": concordance_result,
    }


if __name__ == "__main__":
    run_ensemble_debate()
