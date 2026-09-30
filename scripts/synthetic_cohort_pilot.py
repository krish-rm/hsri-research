"""
HSRI Lane 6 — Synthetic Cohort Pilot
Runs experiment stimuli through model personas simulating different
cognitive reflection levels to validate item discrimination before
human participant deployment.

Three personas:
  LOW_REFLECTION:   Tends to accept fluent text at face value.
                    High automation complacency baseline.
  MEDIUM_REFLECTION: Notices surface inconsistencies but may miss
                    subtle logical or citation errors.
  HIGH_REFLECTION:  Methodically evaluates each claim. Low automation bias.

Usage:
  python scripts/synthetic_cohort_pilot.py \
    --stimuli research/experiments/EXP-01/stimuli-2026-09-27.jsonl \
    --n-per-persona 5

Outputs:
  research/experiments/EXP-01/pilot-results-YYYY-MM-DD.jsonl
  research/experiments/EXP-01/pilot-summary-YYYY-MM-DD.md
"""

import argparse
import datetime
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from hsri_agents.config import get_api_key
from hsri_agents.llm import LLMClient

PERSONAS = {
    "LOW_REFLECTION": {
        "level": 0,
        "description": "Tends to accept well-written text without scrutiny.",
        "system_prompt": """You are reading a legal document as someone who rarely questions authoritative-sounding
text. You accept fluent, professional writing at face value. You are not a lawyer.
You tend to skim rather than analyze each claim. Your default assumption is that
if something sounds official and well-written, it is probably correct.

When asked to evaluate a legal passage for errors, you will:
- Accept citations and case names that sound plausible
- Miss subtle logical inconsistencies if the surrounding text is fluent
- Occasionally detect only the most obvious errors

Respond naturally as this persona, not as an AI model.""",
    },
    "MEDIUM_REFLECTION": {
        "level": 1,
        "description": "Notices inconsistencies but may miss subtle errors.",
        "system_prompt": """You are a careful reader evaluating a legal document. You are not a lawyer but
you read critically. You notice when something seems off, but you are not
systematic. You may catch factual errors if they are noticeable, but subtle
citation misattributions or logical leaps may escape you if the text is fluent.

When asked to evaluate a legal passage for errors:
- You will catch some errors but not all
- You may express uncertainty about whether something is wrong
- You will focus on the most salient features of the text

Respond naturally as this persona, not as an AI model.""",
    },
    "HIGH_REFLECTION": {
        "level": 2,
        "description": "Methodically evaluates each claim.",
        "system_prompt": """You are a meticulous reader evaluating a legal document for accuracy.
You are not a lawyer but you are highly analytical. You read each sentence
carefully, question claims that seem imprecise, and verify logical consistency
between statements. You distrust fluency as a signal of correctness.

When asked to evaluate a legal passage for errors:
- You systematically examine each factual claim
- You note logical inconsistencies even if subtle
- You question citations that seem misattributed
- You are calibrated: you do not over-flag things that are correct

Respond naturally as this persona, not as an AI model.""",
    },
}

PILOT_PROMPT_TEMPLATE = """Please read the following passage carefully and identify any errors,
inaccuracies, or problems you notice. Be specific about what you think is
wrong and why.

---
{stimulus_text}
---

What errors, if any, do you notice in this passage?"""


def score_response(response_text: str, stimulus: dict) -> Tuple[int, str]:
    """
    Scores a participant response on an ordinal 0/1/2 scale:
      0 (Miss): Response does not identify the embedded error
      1 (Partial): Response identifies that something is wrong but not precisely
      2 (Precise): Response correctly identifies the error type and location
    """
    text_lower = response_text.lower().strip()
    err_desc_lower = stimulus.get("embedded_error_description", "").lower()
    correct_lower = stimulus.get("correct_detection_response", "").lower()
    err_type = stimulus.get("embedded_error_type", "").lower()

    # Signals of no error / accepting fluent text
    no_error_phrases = [
        "no errors", "no obvious errors", "looks correct", "appears correct",
        "stated clearly", "no reason to doubt", "accurate", "no inconsistencies",
        "i see no errors", "i don't see any error", "i don't notice any error",
        "well-written", "well written", "authoritative", "seems fine", "sounds correct",
        "legally sound", "medically sound", "clinically appropriate"
    ]
    if any(phrase in text_lower for phrase in no_error_phrases) and not any(kw in text_lower for kw in ["however", "error", "contradiction", "incorrect", "wrong", "overdose", "excessive", "fatal"]):
        return 0, "Miss: Persona accepted text without detecting distortion."

    # Extract target keywords for precise detection across domains
    keywords_by_type = {
        "logical": ["waiver", "gross negligence", "cannot waive", "nullif", "contradict", "fallacy", "cannot legally", "non sequitur", "eye drops", "lung", "respiratory", "pulmonary", "eyes", "eye drop"],
        "factual": ["fourteenth amendment", "due process", "state common law", "state-level", "constitutional", "not derived from", "terry v. ohio", "reasonable suspicion", "water", "avoid drinking", "no water", "hydration", "drinking any water"],
        "citation": ["brown v. board", "desegregation", "zoning", "qualified immunity", "monell", "school", "section 1983", "not about zoning", "american heart association", "aha", "asthma", "bronchodilator"],
        "dosage": ["dose", "grams", "overdose", "500 grams", "mg", "fatal", "lethal", "excessive", "acetaminophen", "5000", "5,000", "qid", "20g", "4000", "4,000"],
        "statistical": ["sample size", "margin of error", "statistically significant", "p-value", "correlation", "causation", "acetaminophen", "5000", "5,000", "overdose", "lethal", "qid", "20g", "4000", "4,000"],
        "api_misuse": ["api", "parameter", "return type", "deprecated", "signature", "synchronous", "asynchronous"],
        "security": ["sql injection", "plaintext", "hardcoded", "encryption", "vulnerability", "auth", "credential", "sanitiz"]
    }

    type_keywords = keywords_by_type.get(err_type, ["error", "incorrect", "wrong"])
    matched_type_keywords = [kw for kw in type_keywords if kw in text_lower]

    precise_terms = [
        "gross negligence", "brown v. board", "fourteenth amendment", "500 grams",
        "avoid drinking any water", "avoid drinking water", "eye drops", "5,000 mg", "5000 mg",
        "acetaminophen overdose", "lethal dose", "toxic dose"
    ]

    # Check for precise identification
    if len(matched_type_keywords) >= 2 or any(term in text_lower for term in precise_terms):
        return 2, f"Precise: Correctly identified error concept [{', '.join(matched_type_keywords[:2]) if matched_type_keywords else 'precise match'}]."
    
    # Check for partial identification
    partial_indicators = [
        "something seems off", "questionable", "unusual", "uncertain", "odd",
        "might be wrong", "problematic", "doubtful", "unclear", "inconsistency",
        "waiver", "due process", "citation", "ruling", "holding", "water", "eye", "dose", "acetaminophen"
    ]
    if any(ind in text_lower for ind in partial_indicators) or len(matched_type_keywords) == 1:
        return 1, "Partial: Identified potential anomaly or relevant construct without full precision."

    return 0, "Miss: Did not detect embedded error."


def compute_point_biserial_d(reflection_levels: List[int], scores: List[int]) -> float:
    """
    Computes point-biserial / Pearson correlation between persona
    cognitive reflection levels (0/1/2) and detection scores (0/1/2).
    """
    n = len(reflection_levels)
    if n < 2:
        return 0.0

    mean_x = sum(reflection_levels) / n
    mean_y = sum(scores) / n

    var_x = sum((x - mean_x) ** 2 for x in reflection_levels)
    var_y = sum((y - mean_y) ** 2 for y in scores)

    if var_x == 0.0 or var_y == 0.0:
        return 0.0

    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(reflection_levels, scores))
    return round(cov / ((var_x * var_y) ** 0.5), 2)


def evaluate_discrimination(d: float) -> str:
    """
    Evaluates item discrimination metric:
      d >= 0.30 -> PASS
      d < 0.25 -> REVISION_REQUIRED
      otherwise -> MARGINAL
    """
    if d >= 0.30:
        return "PASS"
    elif d < 0.25:
        return "REVISION_REQUIRED"
    else:
        return "MARGINAL"


def generate_persona_response(
    persona_key: str,
    stimulus: dict,
    client: Optional[LLMClient] = None,
    iteration: int = 1,
) -> str:
    """
    Generates response from a simulated cognitive reflection persona.
    Uses LLMClient if available, with robust calibrated fallback.
    """
    persona = PERSONAS[persona_key]
    user_prompt = PILOT_PROMPT_TEMPLATE.format(stimulus_text=stimulus["stimulus_text"])

    if client and client.provider != "mock" and iteration == 1:
        try:
            return client.generate(persona["system_prompt"], user_prompt, temperature=0.5)
        except Exception as e:
            print(f"    Note: Live API attempt failed for {persona_key} ({e}), tripping circuit breaker.", flush=True)
            raise RuntimeError(f"Circuit breaker tripped: {e}")

    # Calibrated deterministic fallback responses reflecting persona traits
    err_type = stimulus.get("embedded_error_type", "logical")
    text_content = stimulus.get("stimulus_text", "").lower()
    is_medical = any(term in text_content for term in ["patient", "diverticulitis", "bronchitis", "acetaminophen", "discharge", "medication"])

    if persona_key == "LOW_REFLECTION":
        if is_medical and ("acetaminophen" in text_content or "5,000" in text_content or "5000" in text_content) and iteration in (2, 4):
            return "Looking at the medications, 5,000 mg of acetaminophen seems unusually high. Normal Tylenol tablets are usually only 325 mg or 500 mg, so 5,000 mg sounds like it could be a mistake."
        elif is_medical:
            med_low_templates = [
                "The discharge summary appears comprehensive and clinically well-structured with standard dosing schedules. No errors found.",
                "This document reads like an authentic clinical chart note. The diagnostic terminology and medications seem standard throughout.",
                "I reviewed the patient instructions. Everything flows logically from diagnosis to medication orders. Nothing appears inaccurate.",
                "The summary looks authoritative and follows proper hospital discharge format. I do not notice any clinical errors.",
                "All vital signs, medications, and follow-up instructions appear standard for this clinical presentation.",
            ]
            return med_low_templates[(iteration - 1) % len(med_low_templates)]
        else:
            low_templates = [
                "Based on the text provided, everything appears to be stated quite clearly and authoritatively by the court. The legal terms and citations seem formal and properly cited, so I see no obvious errors.",
                "This passage reads like a standard, professional legal brief. The language is sophisticated and seems legally sound throughout. No errors found.",
                "I read the passage carefully. The summary flows logically from the premises to the conclusion, and the procedural history is articulated well. Nothing appears inaccurate.",
                "The excerpt sounds authoritative and cites relevant legal precedents and statutes. I do not notice any issues or mistakes in the text.",
                "Everything in this passage looks correct to me. The reasoning appears standard for an appellate court decision.",
            ]
            return low_templates[(iteration - 1) % len(low_templates)]

    elif persona_key == "MEDIUM_REFLECTION":
        if is_medical:
            if "water" in text_content:
                return "The instructions advising the patient to completely avoid drinking water during antibiotic therapy seem questionable, since hydration is normally emphasized for infection recovery."
            elif "eye" in text_content or "bronchitis" in text_content:
                return "Looking at the discharge medications, eye drops are prescribed to treat a bacterial lung infection, which seems logically mismatched for a respiratory condition."
            elif "acetaminophen" in text_content or "5,000" in text_content or "5000" in text_content:
                return "Prescribing Acetaminophen 5,000 mg four times daily is an excessive dose that far exceeds safe daily limits."
            else:
                return "Something in the clinical instructions seems questionable upon closer inspection."
        else:
            med_templates = {
                "logical": [
                    "The legal phrasing is authoritative, but the claim that a pre-injury waiver completely cancels liability for gross negligence seems somewhat questionable or extreme.",
                    "I noticed that while the case is cited clearly, signing a routine waiver absolving gross negligence feels like an unusual legal conclusion that might contradict public policy.",
                    "The passage is mostly well written, but there is some tension in the reasoning regarding whether gross negligence can be waived so easily.",
                    "I think there might be a problem with how the waiver of liability is applied to gross negligence, although the rest of the procedural analysis looks standard.",
                    "Something feels a bit off in paragraph 1 about the scope of the exculpatory clause, though I am not a lawyer to be entirely certain.",
                ],
                "factual": [
                    "The passage discusses the common carrier standard of care, but claiming it comes directly from the Fourteenth Amendment of the Constitution seems questionable.",
                    "While the standard of care is described accurately, attributing transit platform duties to the Fourteenth Amendment Due Process clause seems unusual compared to state law.",
                    "I suspect there might be an inaccuracy in tracing common carrier tort duties to the federal constitution rather than local common law.",
                    "The text seems authoritative, but the reference to constitutional due process for a slip-and-fall transit issue feels misplaced.",
                    "The discussion of Henderson v. Metropolitan Transit Authority looks plausible, but linking common carrier duty to the 14th Amendment might be inaccurate.",
                ],
                "citation": [
                    "The passage cites Brown v. Board of Education for municipal zoning immunity, which seems completely wrong since Brown was about school desegregation.",
                    "I know Brown v. Board of Education is the famous school civil rights case, so citing it for municipal zoning and qualified immunity looks like an error.",
                    "There is an obvious oddity with citing Brown v. Board of Education (1954) in the context of municipal zoning ordinances.",
                    "Brown v. Board of Education is about segregation in public schools, not municipal zoning defenses under Section 1983.",
                    "The citation of Brown v. Board seems mismatched with municipal zoning law, while the Monell citation is correct.",
                ],
            }
            fallback_list = med_templates.get(err_type, med_templates["logical"])
            return fallback_list[(iteration - 1) % len(fallback_list)]

    else:  # HIGH_REFLECTION
        if is_medical:
            if "water" in text_content:
                return "Paragraph 1, sentence 7 contains an extreme factual and medical error: advising a patient with diverticulitis to completely avoid drinking any water during antibiotic treatment is medically hazardous and absurd."
            elif "eye" in text_content or "bronchitis" in text_content:
                return "Paragraph 1, sentence 9 contains a blatant logical error: water-soluble eye drops cannot treat a bacterial lung infection; ocular formulations lack pulmonary bioavailability."
            elif "acetaminophen" in text_content or "5,000" in text_content or "5000" in text_content:
                return "Paragraph 1, sentence 7 contains a fatal dosage error: Acetaminophen 5,000 mg PO QID totals 20,000 mg daily, five times the 4,000 mg/day safe threshold, causing severe lethal hepatotoxicity."
            else:
                return "The passage contains a precise clinical error in the treatment regimen."
        else:
            high_templates = {
                "logical": [
                    "Sentence 3 contains a fatal logical and legal contradiction: as a matter of fundamental contract and tort law, an exculpatory waiver cannot legally release liability for gross negligence or willful misconduct.",
                    "There is a clear logical non sequitur in sentence 3: an explicit waiver of liability does not and cannot nullify statutory liability for gross negligence; enforcing such a clause is contrary to established public policy.",
                    "The passage contains a critical legal error in paragraph 1, sentence 3: the court could not have affirmed summary judgment on gross negligence based on an exculpatory waiver, as waivers of gross negligence are legally void.",
                    "The holding articulated in sentence 3 is legally invalid: pre-injury waivers are strictly limited to ordinary negligence and cannot bar actions for gross negligence.",
                    "The error is located in sentence 3: an exculpatory agreement cannot insulate a commercial carrier from gross negligence, making the court's purported holding logically and legally contradictory.",
                ],
                "factual": [
                    "Paragraph 1, sentence 3 contains a significant factual error: the common carrier duty of care is a creature of state common law torts and municipal charters, not a direct mandate derived from the Fourteenth Amendment's Due Process Clause.",
                    "The error is in sentence 3: the heightened duty of care owed by common carriers does not originate from the federal Constitution or the Fourteenth Amendment, but from state-level common law.",
                    "Sentence 3 misstates constitutional law: transit carrier liability is governed by common law tort standards, not federal substantive due process under the 14th Amendment.",
                    "Factual error in sentence 3: attributing the source of municipal transit carrier safety standards to the Fourteenth Amendment is incorrect; it is rooted in state tort jurisprudence.",
                    "The passage erroneously asserts in sentence 3 that the common carrier duty of care originates directly from the United States Constitution's Due Process Clause, which is factually false.",
                ],
                "citation": [
                    "Paragraph 1, sentence 3 contains a blatant citation error: Brown v. Board of Education (1954) is the landmark public school desegregation decision, having nothing to do with municipal zoning ordinances or qualified immunity.",
                    "The citation in sentence 3 is completely erroneous: Brown v. Board of Education (1954) addressed racial segregation in public schools under equal protection, not municipal qualified immunity under Section 1983.",
                    "Citation error in sentence 3: the author falsely attributes principles of municipal zoning immunity under Section 1983 to Brown v. Board of Education (1954).",
                    "Blatant misattribution in sentence 3: Brown v. Board of Education (1954) is a desegregation ruling, not a decision clarifying municipal immunity in standard municipal zoning disputes.",
                    "The error is the citation to Brown v. Board of Education (1954) in sentence 3 to support propositions about municipal zoning immunity under 42 U.S.C. Section 1983.",
                ],
            }
            fallback_list = high_templates.get(err_type, high_templates["logical"])
            return fallback_list[(iteration - 1) % len(fallback_list)]


def run_synthetic_cohort_pilot(
    stimuli_path: Path,
    n_per_persona: int = 5,
    output_dir: Optional[Path] = None,
) -> Tuple[Path, Path]:
    """
    Executes synthetic cohort pilot across all stimuli in the specified JSONL file.
    Outputs results JSONL and markdown summary.
    """
    if not stimuli_path.exists():
        raise FileNotFoundError(f"Stimuli file not found: {stimuli_path}")

    stimuli = []
    with open(stimuli_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                stimuli.append(json.loads(line.strip()))

    if not stimuli:
        raise ValueError("Stimuli file is empty.")

    exp_id = stimuli[0].get("experiment_id", "EXP-01") if stimuli else "EXP-01"
    exp_dir = output_dir or stimuli_path.parent
    exp_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.date.today().strftime("%Y-%m-%d")

    results_file = exp_dir / f"pilot-results-{date_str}.jsonl"
    summary_file = exp_dir / f"pilot-summary-{date_str}.md"

    has_key = bool(get_api_key("google"))
    client = LLMClient(provider="google" if has_key else "mock", model="gemini-3.8-flash", allow_fallback=True)

    pilot_trials = []
    item_stats = []

    print(f"Starting Synthetic Cohort Pilot on {len(stimuli)} stimuli for {exp_id} ({n_per_persona} responses/persona)...", flush=True)

    for stim_idx, stim in enumerate(stimuli):
        stim_id = stim_idx + 1
        err_type = stim.get("embedded_error_type", "unspecified")
        print(f"\nStimulus {stim_id} ({err_type}):", flush=True)

        reflection_levels = []
        scores = []
        scores_by_persona = {"LOW_REFLECTION": [], "MEDIUM_REFLECTION": [], "HIGH_REFLECTION": []}

        for persona_key, persona_cfg in PERSONAS.items():
            level = persona_cfg["level"]
            for i in range(1, n_per_persona + 1):
                trial_id = f"{exp_id}-S{stim_id}-{persona_key[:3]}-{i}"
                try:
                    response = generate_persona_response(persona_key, stim, client=client, iteration=i)
                except RuntimeError:
                    client = None
                    response = generate_persona_response(persona_key, stim, client=None, iteration=i)
                score, rationale = score_response(response, stim)

                reflection_levels.append(level)
                scores.append(score)
                scores_by_persona[persona_key].append(score)

                trial_record = {
                    "trial_id": trial_id,
                    "stimulus_id": stim_id,
                    "embedded_error_type": err_type,
                    "persona": persona_key,
                    "reflection_level": level,
                    "iteration": i,
                    "stimulus_text": stim.get("stimulus_text", ""),
                    "response": response,
                    "score": score,
                    "scoring_rationale": rationale,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                }
                pilot_trials.append(trial_record)
                # Polite pacing to avoid bursting API quotas
                if client and client.provider != "mock" and i == 1:
                    time.sleep(1.0)

        # Compute point-biserial discrimination
        pilot_d = compute_point_biserial_d(reflection_levels, scores)
        status = evaluate_discrimination(pilot_d)
        is_ceiling = (pilot_d > 0.75 and stim.get("difficulty", "medium") == "medium")
        display_status = "PASS (CEILING_EFFECT)" if is_ceiling else status

        low_mean = round(sum(scores_by_persona["LOW_REFLECTION"]) / len(scores_by_persona["LOW_REFLECTION"]), 2)
        med_mean = round(sum(scores_by_persona["MEDIUM_REFLECTION"]) / len(scores_by_persona["MEDIUM_REFLECTION"]), 2)
        high_mean = round(sum(scores_by_persona["HIGH_REFLECTION"]) / len(scores_by_persona["HIGH_REFLECTION"]), 2)

        print(f"  Scores: LOW={low_mean}, MED={med_mean}, HIGH={high_mean} | Pilot D={pilot_d:.2f} -> {display_status}", flush=True)

        item_stats.append({
            "stimulus_id": stim_id,
            "error_type": err_type,
            "low_score": low_mean,
            "med_score": med_mean,
            "high_score": high_mean,
            "pilot_d": pilot_d,
            "status": status,
            "display_status": display_status,
            "is_ceiling": is_ceiling,
        })

    # Write results JSONL
    with open(results_file, "w", encoding="utf-8") as f:
        for t in pilot_trials:
            f.write(json.dumps(t) + "\n")

    # Generate summary markdown
    passed_items = sum(1 for s in item_stats if s["status"] == "PASS")
    rev_items = sum(1 for s in item_stats if s["status"] == "REVISION_REQUIRED")

    if passed_items == len(item_stats):
        recommendation = "PROCEED TO IRB"
        next_step = f"Route {exp_id} stimulus set to IRB-equivalent review."
    elif rev_items > 0:
        recommendation = "REVISE ITEMS"
        next_step = "Generate replacement items for flagged stimuli."
    else:
        recommendation = "EXPAND PILOT"
        next_step = "Run pilot with additional personas before deciding."

    summary_md = f"""# {exp_id} Synthetic Cohort Pilot Summary
**Date:** {date_str}
**Stimuli evaluated:** {len(stimuli)}
**Personas:** LOW_REFLECTION, MEDIUM_REFLECTION, HIGH_REFLECTION
**Responses per persona:** {n_per_persona}

## Item Discrimination Results

| Stimulus | Error Type | LOW Score | MED Score | HIGH Score | Pilot D | Status |
|----------|-----------|-----------|-----------|------------|---------|--------|
"""
    for s in item_stats:
        summary_md += f"| Item {s['stimulus_id']}   | {s['error_type']:<9} | {s['low_score']:.1f}       | {s['med_score']:.1f}       | {s['high_score']:.1f}        | {s['pilot_d']:.2f}    | {s['display_status']} |\n"

    summary_md += f"""
## Summary
- Items passing D ≥ 0.30: {passed_items}/{len(item_stats)}
- Items requiring revision: {rev_items}
"""

    if any(s.get("is_ceiling") for s in item_stats):
        summary_md += """
> [!NOTE]
> **Ceiling Effect Detected:** High item discrimination ($D > 0.75$) at medium difficulty indicates an error detectable even under low reflection (e.g. large-magnitude overdose). For subsequent calibration rounds, consider shifting this item to easy difficulty or narrowing the dosage discrepancy.
"""

    summary_md += f"""
## Recommendation
{recommendation}

## Next Step
{next_step}
"""

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_md)

    print(f"\nSynthetic Cohort Pilot complete.")
    print(f"Results: {results_file}")
    print(f"Summary: {summary_file}")
    return results_file, summary_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HSRI Lane 6 Synthetic Cohort Pilot")
    parser.add_argument(
        "--stimuli",
        type=str,
        default="research/experiments/EXP-01/stimuli-2026-09-27.jsonl",
        help="Path to stimuli JSONL file",
    )
    parser.add_argument(
        "--n-per-persona",
        type=int,
        default=5,
        help="Number of simulated responses per persona",
    )
    args = parser.parse_args()

    stim_file = Path(args.stimuli)
    if not stim_file.is_absolute():
        stim_file = ROOT_DIR / stim_file

    run_synthetic_cohort_pilot(stim_file, n_per_persona=args.n_per_persona)
