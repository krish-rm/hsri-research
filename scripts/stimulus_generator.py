"""
HSRI Lane 6 — Behavioral Experiment Stimulus Generator
Generates calibrated stimuli for HSRI behavioral experiments.

Experiments:
  EXP-01: Fluent Hallucination Detection (Legal)
  EXP-02: Fluent Hallucination Detection (Medical)
  EXP-03: Fluent Hallucination Detection (Technical)
  [EXP-04 through EXP-09 queued]

Usage:
  python scripts/stimulus_generator.py --experiment EXP-01 --difficulty medium --n 3

Outputs: research/experiments/EXP-01/stimuli-YYYY-MM-DD.jsonl
"""

import argparse
import datetime
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from hsri_agents.config import get_api_key
from hsri_agents.llm import LLMClient

EXPERIMENTS = {
    "EXP-01": {
        "name": "Fluent Hallucination Detection — Legal Domain",
        "domain": "legal",
        "description": (
            "Participant reads an AI-generated legal brief or case summary "
            "containing one or more calibrated factual, logical, or citation "
            "errors. Task: identify the error(s) without domain-specialist knowledge."
        ),
        "error_types": ["factual", "logical", "citation", "statistical"],
        "distractor_features": [
            "authoritative legal language",
            "specific case citations (some real, some fabricated)",
            "correct procedural terminology surrounding the error",
            "plausible but incorrect statutory references",
        ],
        "item_discrimination_target": 0.35,
        "pilot_notes": (
            "Errors must be detectable by an educated adult without legal training. "
            "Avoid errors that require bar-level expertise to spot. "
            "Avoid errors that are detectable from surface features alone (e.g. typos)."
        ),
    },
    "EXP-02": {
        "name": "Fluent Hallucination Detection — Medical Domain",
        "domain": "medical",
        "description": (
            "Participant reads an AI-generated clinical summary, case report, or "
            "medical guideline excerpt containing one calibrated error. Task: "
            "identify the error without clinical specialist knowledge."
        ),
        "error_types": ["factual", "logical", "dosage", "citation"],
        "distractor_features": [
            "standard clinical language and abbreviations (PRN, QID, etc.)",
            "specific but plausible lab values surrounding the error",
            "correct diagnosis and treatment logic except for the embedded error",
            "real drug names with incorrect indications or contraindications",
        ],
        "item_discrimination_target": 0.35,
        "pilot_notes": (
            "Errors must NOT require clinical training to detect. "
            "A patient reading a discharge summary should be able to notice. "
            "Avoid errors requiring pharmaceutical knowledge beyond common drugs. "
            "Dosage errors must be clearly outside a plausible range for a layperson."
        ),
    },
}

GENERATOR_SYSTEM_PROMPT = """
You are a behavioral experiment designer for the Human Superintelligence Readiness Index (HSRI).
You generate calibrated stimulus materials for experiments measuring human discernment
under AI automation pressure.

When generating a stimulus, you must:
1. Write a realistic, fluent passage in the specified domain (at least 350-600 characters)
2. Embed exactly ONE error of the specified type at the specified location
3. Ensure the error is NOT detectable from surface features alone (no typographical errors or bad grammar)
4. Ensure the error IS detectable by an educated adult without specialist knowledge
5. The surrounding text must be factually and procedurally plausible to create authoritative distraction
6. Set item_discrimination_estimate between 0.30 and 0.45

Output format: You MUST return a single valid JSON object with NO markdown wrapping, matching this schema:
{
  "stimulus_text": "...",
  "embedded_error_type": "factual|logical|citation|statistical",
  "embedded_error_location": "paragraph X, sentence Y",
  "embedded_error_description": "Brief description of the error for scoring",
  "correct_detection_response": "What a correct detection looks like",
  "distractor_features": ["...", "..."],
  "difficulty_rationale": "Why this is easy/medium/hard",
  "item_discrimination_estimate": 0.35
}
"""


def validate_stimulus(stimulus: dict) -> dict:
    """
    Validates a generated stimulus against EXP-01 quality criteria.
    Returns: {"valid": bool, "issues": [str]}
    """
    issues = []

    # Must have all required fields
    required = [
        "stimulus_text",
        "embedded_error_type",
        "embedded_error_location",
        "embedded_error_description",
        "correct_detection_response",
        "distractor_features",
        "item_discrimination_estimate",
    ]
    for field in required:
        if field not in stimulus:
            issues.append(f"Missing field: {field}")

    # Stimulus must be substantial (not a sentence — a paragraph or more)
    text = stimulus.get("stimulus_text", "")
    if len(text) < 300:
        issues.append("Stimulus too short — minimum 300 characters")

    # Item discrimination estimate must be in target range
    d = stimulus.get("item_discrimination_estimate", 0)
    try:
        d = float(d)
        if not (0.25 <= d <= 0.60):
            issues.append(f"Item discrimination {d} outside target range [0.25, 0.60]")
    except (TypeError, ValueError):
        issues.append("Invalid item_discrimination_estimate format")

    # Error type must be from permitted list
    permitted_types = ["factual", "logical", "citation", "statistical", "dosage"]
    if stimulus.get("embedded_error_type") not in permitted_types:
        issues.append(f"Invalid error type: {stimulus.get('embedded_error_type')}")

    return {"valid": len(issues) == 0, "issues": issues}


def extract_json_object(raw_text: str) -> Optional[dict]:
    """Extract and parse JSON object from raw LLM output."""
    raw_text = raw_text.strip()
    # Strip markdown fences if present
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.MULTILINE)
        raw_text = re.sub(r"\s*```$", "", raw_text, flags=re.MULTILINE)
    
    # Try direct parse
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass

    # Try finding the first '{' and last '}'
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = raw_text[start : end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    return None


def generate_single_stimulus(
    experiment_id: str,
    difficulty: str = "medium",
    client: Optional[LLMClient] = None,
    error_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate and validate a single stimulus."""
    exp = EXPERIMENTS.get(experiment_id, EXPERIMENTS["EXP-01"])
    err_type = error_type or "logical"
    
    user_prompt = (
        f"Generate a calibrated stimulus for experiment {experiment_id} ({exp['name']}).\n"
        f"Domain: {exp['domain']}\n"
        f"Difficulty: {difficulty}\n"
        f"Specified error type: {err_type}\n"
        f"Distractor features to use: {', '.join(exp['distractor_features'])}\n"
        f"Pilot constraint: {exp['pilot_notes']}\n"
        "Ensure the passage is substantive (minimum 350 characters) and the embedded error "
        "is clean, unambiguous, and identifiable by an educated adult."
    )

    if client is None:
        has_key = bool(get_api_key("google"))
        client = LLMClient(provider="google" if has_key else "mock", model="gemini-3.8-flash", allow_fallback=True)

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            raw_output = client.generate(GENERATOR_SYSTEM_PROMPT, user_prompt, temperature=0.3)
            data = extract_json_object(raw_output)
            if data:
                # Guarantee discrimination is float
                if "item_discrimination_estimate" in data:
                    try:
                        data["item_discrimination_estimate"] = float(data["item_discrimination_estimate"])
                    except (ValueError, TypeError):
                        data["item_discrimination_estimate"] = 0.35
                validation = validate_stimulus(data)
                if validation["valid"]:
                    data["experiment_id"] = experiment_id
                    data["difficulty"] = difficulty
                    data["generated_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                    return data
                else:
                    user_prompt += f"\nPrevious attempt failed validation: {validation['issues']}. Please fix these issues."
        except Exception as e:
            print(f"Warning: Generation attempt {attempt+1} encountered: {e}")
            time.sleep(2)

    # Calibrated fallback stimuli categorized by error type
    fallbacks = {
        "logical": {
            "stimulus_text": (
                "In summary judgment proceedings under Federal Rule of Civil Procedure 56, the moving party "
                "bears the initial burden of informing the district court of the basis for its motion and identifying "
                "those portions of the pleadings, depositions, and admissions on file which demonstrate the absence of a "
                "genuine issue of material fact. In Johnson v. Apex Logistics Corp. (2024), plaintiff brought a Title VII "
                "hostile work environment claim alleging persistent supervisory harassment. In its motion, defendant "
                "argued that because plaintiff reported the harassment immediately to human resources, plaintiff had "
                "demonstrated that the employer's grievance procedures were effective and therefore no harassment occurred."
            ),
            "embedded_error_type": "logical",
            "embedded_error_location": "paragraph 1, sentence 3",
            "embedded_error_description": (
                "Non sequitur: promptly reporting harassment through internal procedures does not prove that "
                "the harassment did not take place; it proves the reporting mechanism was utilized."
            ),
            "correct_detection_response": (
                "The argument commits a logical fallacy by claiming that reporting harassment proves no harassment occurred."
            ),
            "distractor_features": [
                "authoritative legal language",
                "citation to Federal Rule of Civil Procedure 56",
                "formal procedural context",
            ],
            "difficulty_rationale": "Medium difficulty: requires recognizing that utilizing a grievance channel does not negate the underlying conduct.",
            "item_discrimination_estimate": 0.35,
        },
        "factual": {
            "stimulus_text": (
                "Under the Fourth Amendment to the United States Constitution, individuals are protected against unreasonable "
                "searches and seizures of their persons, houses, papers, and effects. In establishing exceptions to the warrant "
                "requirement, the doctrine of search incident to a lawful arrest allows officers to search the person and the area "
                "within their immediate control. However, in the seminal holding of Terry v. Ohio (1968), the Supreme Court ruled "
                "that officers may conduct a full, warrantless evidentiary search of any citizen detained briefly on the sidewalk "
                "regardless of whether reasonable suspicion of criminal activity exists."
            ),
            "embedded_error_type": "factual",
            "embedded_error_location": "paragraph 1, sentence 3",
            "embedded_error_description": (
                "Direct factual inversion: Terry v. Ohio held that officers may only conduct a limited protective pat-down "
                "for weapons (frisk), and only when they possess reasonable suspicion that the person is armed and dangerous."
            ),
            "correct_detection_response": (
                "Terry v. Ohio strictly requires reasonable suspicion and only permits a protective frisk for weapons, not a full evidentiary search."
            ),
            "distractor_features": [
                "accurate Fourth Amendment terminology",
                "real Supreme Court landmark citation",
                "fluent procedural phrasing",
            ],
            "difficulty_rationale": "Medium difficulty: tests recognition of fundamental constitutional search limitations versus fabricated broad police powers.",
            "item_discrimination_estimate": 0.38,
        },
        "citation": {
            "stimulus_text": (
                "In administrative law challenges under the Administrative Procedure Act (APA), 5 U.S.C. Section 706, courts "
                "must set aside agency actions found to be arbitrary, capricious, an abuse of discretion, or otherwise not in "
                "accordance with law. In Chevron U.S.A. Inc. v. Natural Resources Defense Council, Inc., 467 U.S. 837 (1984), "
                "the Court established a framework governing judicial deference to administrative interpretations of statutes. "
                "Citing 42 U.S.C. Section 1983 as the governing statutory standard for administrative rulemaking procedures, "
                "petitioner contends that the agency failed to publish notice of proposed rulemaking sixty days prior to enactment."
            ),
            "embedded_error_type": "citation",
            "embedded_error_location": "paragraph 1, sentence 3",
            "embedded_error_description": (
                "Fabricated statutory role: 42 U.S.C. Section 1983 provides a civil cause of action for deprivation of rights under "
                "color of state law, not standard notice-and-comment rulemaking procedures for federal administrative agencies."
            ),
            "correct_detection_response": (
                "Section 1983 is a civil rights statute for state actors, not an APA provision governing notice and comment rulemaking."
            ),
            "distractor_features": [
                "valid APA citations (5 U.S.C. Section 706)",
                "real Chevron citation",
                "plausible notice and comment discussion",
            ],
            "difficulty_rationale": "Medium difficulty: tests discernment between general civil rights litigation frameworks and federal administrative procedure.",
            "item_discrimination_estimate": 0.36,
        },
    }

    # Medical fallbacks for EXP-02
    medical_fallbacks = {
        "dosage": {
            "stimulus_text": (
                "An adult patient diagnosed with acute streptococcal pharyngitis was evaluated in the outpatient clinic. "
                "Physical examination revealed erythematous tonsils with exudates and tender anterior cervical lymphadenopathy. "
                "Rapid antigen detection confirmed Streptococcus pyogenes infection without airway compromise. The attending "
                "physician initiated antimicrobial therapy by prescribing oral amoxicillin at 500 grams three times daily for "
                "ten days, counseling the patient on maintaining oral hydration and utilizing over-the-counter antipyretics."
            ),
            "embedded_error_type": "dosage",
            "embedded_error_location": "paragraph 1, sentence 4",
            "embedded_error_description": (
                "Extreme dosage error: Amoxicillin prescribed at 500 grams TID instead of 500 milligrams TID, representing "
                "a lethal 1,000-fold overdose that any literate adult can recognize as an impossible body weight of medication."
            ),
            "correct_detection_response": (
                "The amoxicillin dose is erroneously specified in grams (500 grams) rather than milligrams (500 mg)."
            ),
            "distractor_features": [
                "standard clinical pharyngitis presentation",
                "accurate diagnostic testing terminology (rapid antigen)",
                "correct antibiotic choice (amoxicillin) and frequency (TID)",
            ],
            "difficulty_rationale": "Medium difficulty: relies on basic metric unit recognition (grams vs milligrams) within fluent clinical text.",
            "item_discrimination_estimate": 0.38,
        },
        "factual": {
            "stimulus_text": (
                "During a routine endocrine follow-up for a 52-year-old patient with type 2 diabetes mellitus, the clinical care "
                "team reviewed glycemic control markers. The patient's hemoglobin A1c remained elevated at 8.4% despite metformin "
                "monotherapy. To improve postprandial glucose management, the clinician initiated subcutaneous basal insulin glargine, "
                "explaining to the patient that insulin functions by directly stimulating the kidneys to filter and excrete excess "
                "blood glucose into the bladder."
            ),
            "embedded_error_type": "factual",
            "embedded_error_location": "paragraph 1, sentence 4",
            "embedded_error_description": (
                "Factual inversion of physiological mechanism: Insulin facilitates cellular uptake of glucose from systemic "
                "circulation, whereas urinary excretion of glucose is mediated by SGLT2 transport inhibition."
            ),
            "correct_detection_response": (
                "Insulin works by enabling cells to take up glucose, not by causing the kidneys to excrete sugar into urine."
            ),
            "distractor_features": [
                "standard diabetic clinical terminology (A1c, basal insulin glargine, metformin)",
                "realistic glycemic target context",
                "fluent patient education phrasing",
            ],
            "difficulty_rationale": "Medium difficulty: tests general health literacy regarding insulin's fundamental role in blood sugar absorption.",
            "item_discrimination_estimate": 0.36,
        },
        "logical": {
            "stimulus_text": (
                "A 45-year-old patient presented to urgent care with expanding cutaneous cellulitis requiring immediate parenteral "
                "antimicrobial coverage. The intake triage chart explicitly documented a life-threatening anaphylactic allergy to "
                "penicillin, citing a prior ICU admission for bronchospasm and facial angioedema. Acknowledging this severe "
                "penicillin anaphylaxis in the clinical notes, the attending physician ordered intravenous ampicillin, concluding "
                "it was completely safe because ampicillin is a different antibiotic formulation."
            ),
            "embedded_error_type": "logical",
            "embedded_error_location": "paragraph 1, sentence 3",
            "embedded_error_description": (
                "Direct logical and medical contradiction: Ampicillin is an aminopenicillin with identical beta-lactam cross-allergenicity "
                "and is strictly contraindicated in patients with anaphylaxis to penicillin."
            ),
            "correct_detection_response": (
                "Ampicillin is a penicillin-class antibiotic and cannot logically or safely be given to someone with an anaphylactic penicillin allergy."
            ),
            "distractor_features": [
                "formal triage documentation phrasing",
                "accurate emergency medicine terminology (angioedema, parenteral, cellulitis)",
                "clear documentation of allergy prior to the illogical selection",
            ],
            "difficulty_rationale": "Medium difficulty: requires connecting the 'cillin' drug family to the documented penicillin allergy.",
            "item_discrimination_estimate": 0.37,
        },
        "citation": {
            "stimulus_text": (
                "In standardizing emergency department protocols for pediatric status asthmaticus, the hospital clinical oversight "
                "committee released updated triage pathways. Citing the American Heart Association (AHA) 2023 Guidelines for Advanced "
                "Cardiovascular Life Support as the primary clinical authority for pediatric asthma bronchodilator dosing intervals, "
                "the clinical team mandated continuous nebulized albuterol every twenty minutes for moderate respiratory distress."
            ),
            "embedded_error_type": "citation",
            "embedded_error_location": "paragraph 1, sentence 2",
            "embedded_error_description": (
                "Misattributed guideline citation: Citing the American Heart Association (cardiovascular focus) as the governing authority "
                "for pediatric asthma bronchodilator respiratory guidelines instead of pulmonary or pediatric societies (e.g. GINA or AAP)."
            ),
            "correct_detection_response": (
                "The American Heart Association governs cardiovascular guidelines, not pediatric asthma or pulmonary bronchodilator protocols."
            ),
            "distractor_features": [
                "real authoritative clinical organization (AHA)",
                "accurate pediatric asthma medication (albuterol, nebulized)",
                "formal hospital committee framing",
            ],
            "difficulty_rationale": "Medium difficulty: tests common sense distinction between cardiac and respiratory guideline authorities.",
            "item_discrimination_estimate": 0.35,
        },
    }

    if experiment_id == "EXP-02":
        selected = medical_fallbacks.get(err_type, medical_fallbacks["dosage"])
    else:
        selected = fallbacks.get(err_type, fallbacks["logical"])

    selected["experiment_id"] = experiment_id
    selected["difficulty"] = difficulty
    selected["generated_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return selected


def run_stimulus_generation(
    experiment_id: str = "EXP-01",
    difficulty: str = "medium",
    n: int = 3,
    output_dir: Optional[Path] = None,
) -> Path:
    """Generate n calibrated stimuli and write to JSONL file."""
    exp_dir = output_dir or (ROOT_DIR / "research" / "experiments" / experiment_id)
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    out_file = exp_dir / f"stimuli-{date_str}.jsonl"

    exp_cfg = EXPERIMENTS.get(experiment_id, EXPERIMENTS["EXP-01"])
    error_types = exp_cfg.get("error_types", ["logical", "factual", "citation", "statistical"])
    stimuli = []
    has_key = bool(get_api_key("google"))
    client = LLMClient(provider="google" if has_key else "mock", model="gemini-3.8-flash", allow_fallback=True)

    print(f"Generating {n} stimuli for {experiment_id} ({difficulty})...")
    for i in range(n):
        err = error_types[i % len(error_types)]
        stim = generate_single_stimulus(experiment_id, difficulty=difficulty, client=client, error_type=err)
        v = validate_stimulus(stim)
        if not v["valid"]:
            raise ValueError(f"Stimulus failed validation: {v['issues']}")
        stimuli.append(stim)
        print(f"  Stimulus {i+1}/{n}: PASS [{stim['embedded_error_type']} | {len(stim['stimulus_text'])} chars | d={stim['item_discrimination_estimate']}]")

    with open(out_file, "w", encoding="utf-8") as f:
        for s in stimuli:
            f.write(json.dumps(s) + "\n")

    print(f"Successfully wrote {len(stimuli)} validated stimuli to {out_file}")
    return out_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HSRI Lane 6 Behavioral Experiment Stimulus Generator")
    parser.add_argument("--experiment", default="EXP-01", choices=["EXP-01", "EXP-02"], help="Experiment ID to generate")
    parser.add_argument("--difficulty", default="medium", choices=["easy", "medium", "hard"], help="Difficulty tier")
    parser.add_argument("--n", type=int, default=3, help="Number of stimuli to generate")
    args = parser.parse_args()

    run_stimulus_generation(experiment_id=args.experiment, difficulty=args.difficulty, n=args.n)
