# Human Pilot Item Calibration Plan

> **DRAFT: NOT SUBMITTED. NO HUMAN DATA COLLECTED. NO PI DESIGNATED**
> **PREVIEW DISCLAIMER: HSRI v0.3.0-dev**
> This item calibration plan establishes empirical psychometric criteria for evaluating and calibrating behavioral stimulus batteries upon execution of accredited human subject pilots. In strict accordance with Standing Rule 12, synthetic-persona pilot results reflect stimulus behavior only and provide zero evidence regarding human cognitive faculties. All outputs carry the v0.3-dev preview notice.

---

## 1. Purpose & Calibration Architecture

The HSRI behavioral lab uses a phased stimulus calibration methodology. Prior to human deployment, candidate stimuli undergo synthetic LLM persona cohort testing ($N = 5$ per ability persona: Low, Medium, High). These synthetic runs serve strictly as **stimulus-behavior checks** to verify grammatical fluency, machine parseability, and prompt interpretability.

However, synthetic persona discrimination ($D$) does not measure human cognition. Items that exhibit extreme discrimination or ceiling effects in synthetic testing may behave radically differently when evaluated by human participants. This calibration plan defines how human pilot data will be used to calibrate, revise, or retire stimulus items across EXP-01, EXP-02, and EXP-03.

---

## 2. Priority Items Flagged in Synthetic Pilots

Two specific stimulus items from preceding synthetic cohorts have been designated for high-priority human empirical calibration:

### 2.1 EXP-02 Item 1 (Diverticulitis Hydration Restriction)
- **Item Identity (Rule 19):**
  - **ID:** `stimulus_id: 1`
  - **Text Prefix (first 80 chars):** `"Discharge Instructions: Acute Diverticulitis Management. You have been evaluate"`
  - **Error Classification:** `factual_clinical` (Instructing a recovering diverticulitis patient to restrict fluid intake to under 500 mL/day to "rest the bowel", creating severe dehydration risk).
- **Synthetic Cohort Performance:**
  - Low Persona Score: $0.0$ / $2.0$
  - Medium Persona Score: $2.0$ / $2.0$
  - High Persona Score: $2.0$ / $2.0$
  - Discrimination: $D = 0.87$
  - Synthetic Status: `PASS (CEILING_EFFECT)`
- **Calibration Objective:** In synthetic runs, both Medium and High ability personas saturated at full credit ($2.0$), producing a ceiling effect. The human pilot will test whether non-expert human lay adults recognize the clinical danger of extreme fluid restriction or whether authoritative medical terminology induces uncritical acceptance.

### 2.2 EXP-03 Item 5 (Insecure PRNG for MFA Token Generation)
- **Item Identity (Rule 19):**
  - **ID:** `exp03_sec_001` (`stimulus_id: 5`)
  - **Text Prefix (first 80 chars):** `"def generate_mfa_token(user_id: str, entropy_bytes: int = 32) -> str:\n    \"\"\"Gene"`
  - **Error Classification:** `security` (Using Python standard library `random` [Mersenne Twister] for multi-factor authentication tokens while falsely asserting in docstrings that it is cryptographically secure).
- **Synthetic Cohort Performance:**
  - Low Persona Score: $0.0$ / $2.0$
  - Medium Persona Score: $1.0$ / $2.0$
  - High Persona Score: $2.0$ / $2.0$
  - Discrimination: $D = 1.00$
  - Synthetic Status: `FLAG: CEILING_EFFECT`
- **Calibration Objective:** A synthetic discrimination of $D = 1.00$ is a synthetic artifact indicating that the error was trivially obvious to the High persona model while entirely obscure to the Low persona. It does **not** indicate that human developers or lay participants will discriminate perfectly. The human pilot will determine real-world human vulnerability to subtle cryptographic misattributions in code.

---

## 3. Human Psychometric Calibration Criteria

Upon completion of human pilot testing ($N = 130$ per condition in EXP-01; subsequent pilot cohorts in EXP-02 and EXP-03), item performance will be audited against classical test theory (CTT) and item response theory (IRT) benchmarks:

### 3.1 Item Discrimination ($D_{\text{human}}$)
Item discrimination will be calculated by comparing the top $27\%$ performing human participants ($U$) against the bottom $27\%$ ($L$):
$$D_{\text{human}} = \frac{R_U - R_L}{N_{27\%}}$$
- **Retain Item ($0.35 \le D_{\text{human}} \le 0.75$):** Item exhibits healthy, robust discrimination between participants exercising analytical scrutiny and those exhibiting automation bias.
- **Marginal Item ($0.20 \le D_{\text{human}} < 0.35$):** Item requires review; consider revising distractors or clarifying rubric instructions.
- **Drop / Re-author ($D_{\text{human}} < 0.20$):** Item fails to discriminate and will be removed from the battery.

### 3.2 Difficulty & Boundary Criteria (Ceiling and Floor Effects)
- **Ceiling Effect Threshold ($P > 0.85$):** If $> 85\%$ of human participants across all conditions detect and explain the error correctly, the item is trivial.
  - *Action:* The embedded error must be recalibrated to be more nuanced, or the surrounding authoritative framing must be enhanced to simulate realistic cognitive friction.
- **Floor Effect Threshold ($P < 0.15$):** If $< 15\%$ of human participants detect the error, the flaw is excessively obscure or requires specialist professional knowledge outside lay competence.
  - *Action:* The flaw must be reformulated so that common-sense analytical reasoning is sufficient for detection without professional credentialing.

### 3.3 Inter-Rater Reliability (IRR) Gate
- Two independent human raters will blind-score a random $20\%$ sample of qualitative responses.
- An inter-rater agreement of **Cohen's $\kappa \ge 0.75$** (or quadratic weighted $\kappa \ge 0.80$) on the 3-point rubric is mandatory prior to unblinding and model estimation.
- If $\kappa < 0.75$, scoring rubric operational definitions must be revised and raters retrained before continuing.

---

## 4. Revision and Deprecation Lifecycle

1. **Version Tracking:** Every stimulus revision receives an updated timestamped filename (e.g., `stimuli-YYYY-MM-DD.jsonl`). Existing files are never overwritten.
2. **Audit Trail:** Any revision or deprecation must be documented in the corresponding experiment's `README.md` and registered in the project changelog.
3. **Draft PR Gate:** All item changes require a human-approved pull request; autonomous agent merging of stimulus modifications is strictly prohibited under Rule 1.
