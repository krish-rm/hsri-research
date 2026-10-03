# Academic Principal Investigator (PI) Readiness Brief: Human Superintelligence Readiness Index (HSRI)

> **PREVIEW DISCLAIMER: HSRI v0.3.0-dev**
> **STATUS:** DRAFT COLLABORATION BRIEF. NO HUMAN DATA COLLECTED. NO PI DESIGNATED.
> This brief summarizes project readiness, methodological scaffolds, and governance prerequisites for a prospective academic Principal Investigator to lead accredited human-participant empirical research.

---

## 1. Project Overview & Current Epistemic Status

The **Human Superintelligence Readiness Index (HSRI)** is an open-science research initiative investigating societal preparedness for advancing frontier artificial intelligence. In strict adherence to project governance and public transparency standards, the framework operates under the following precise epistemic definitions:

- **Benchmark Classification:** HSRI is an **exploratory, non-psychometrically-validated proxy benchmark**, not an evaluative ranking or definitive standard.
- **Data Harmonization:** The macro composite framework synthesizes 780 harmonized observations across 39 nations structured into four equal-weighted conceptual pillars (25% each): AI Literacy, Critical Discernment, Institutional Governance, and Digital Infrastructure.
- **Behavioral Lab Status (Phase 2 Roadmap):** Empirical behavioral experiments (EXP-01 through EXP-03) are currently restricted to **synthetic-persona pilots only**. Synthetic personas test stimulus behavior, parseability, and embedded error mechanics only; they provide **no empirical evidence regarding human cognition, reading latency, or real-world error detection**.
- **Human Participant Data:** **Zero human behavioral data has been collected or validated.** All live human deployment is strictly halted pending formal institutional review.

---

## 2. What Exists: Repository Assets & Scaffolds

The repository provides a complete, version-controlled research pipeline available for review:

1. **EXP-01 Complete IRB Package (9 Documents):**
   - Located at [`research/experiments/EXP-01/irb-package/`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/experiments/EXP-01/irb-package/).
   - Contains: Cover Sheet (`00-cover-sheet.md`), Study Description (`01-study-description.md`), Participant Criteria (`02-participant-criteria.md`), Informed Consent Template (`03-consent-template.md`), Risk Assessment (`04-risk-assessment.md`), Data Management Plan (`05-data-management.md`), Standardized Stimulus Battery (`06-stimulus-battery.md`), Power Analysis (`07-power-analysis.md`), and Participant Debriefing Protocol (`08-debrief-script.md`).
2. **EXP-02 Clinical Experiment Package (Clinician Review Pending):**
   - Located at [`research/experiments/EXP-02/irb-package/`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/experiments/EXP-02/irb-package/).
   - 9 draft IRB documents assembled for medical discharge summary hallucination detection. Stimuli are cleared for IRB review, but formal institutional submission remains blocked pending independent licensed clinician review.
3. **EXP-03 Software/Technical Stimulus Battery:**
   - Located at [`research/experiments/EXP-03/`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/experiments/EXP-03/).
   - 5 standardized stimuli evaluated across numerical precision, concurrency, and cryptographic PRNG boundaries. Synthetic pilot completed; formal IRB package drafting has not yet been initiated.
4. **Preregistration Draft with Open Decision Points:**
   - Located at [`research/experiments/EXP-01/prereg/`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/experiments/EXP-01/prereg/).
   - Includes `prereg-draft.md`, `item-calibration-plan.md`, and `platform-requirements.md`.
   - Explicitly designates all unresolved methodological decisions with `[DECISION NEEDED: PI / statistician]`, avoiding premature unilateral algorithmic choices.
5. **Permissive Open Licensing:**
   - Code and documentation licensed under Creative Commons Attribution-ShareAlike 4.0 International (`CC-BY-SA-4.0`).
   - Deliberative datasets licensed under Creative Commons Attribution 4.0 International (`CC-BY-4.0`).

---

## 3. What Is Being Asked of a Principal Investigator

The project requires an academic collaborator to serve as institutional Principal Investigator to transition from synthetic prototype development to accredited empirical science:

1. **Institutional Affiliation & Oversight:**
   - Provide the necessary institutional home to sponsor and submit the protocol to an accredited Institutional Review Board (IRB) or human research ethics committee.
2. **IRB Protocol Submission:**
   - Review, adapt, and submit the pre-drafted EXP-01 IRB package under institutional standards, serving as the accountable investigator of record.
3. **Biostatistical & Methodological Review:**
   - Resolve open `[DECISION NEEDED]` items in the preregistration protocol:
     - Formally select the primary human discrimination metric (Upper-Lower Index $D_{\text{UL}}$, Corrected Item-Rest Correlation $r_{\text{i-rest}}$, or IRT Graded Response Model slope $a_i$) and empirical retention cutoffs.
     - Validate sample size assumptions (target 130 completers per arm, 260 total; 137 enrolled per arm, 274 total given assumed 5% attrition).
     - Authorize the statistical model specification (Cumulative Link Mixed Model vs. Linear Mixed-Effects Model).
4. **Clinical Oversight for EXP-02:**
   - Coordinate or conduct expert clinician review of the clinical discharge stimuli (diverticulitis hydration, ophthalmic administration, acetaminophen dosing margins) prior to patient or healthcare-professional recruitment.

---

## 4. Honest Methodological & Structural Limitations

Prospective collaborators should be fully aware of the boundary conditions and known limitations of the current codebase:

- **Single-Model-Family Deliberations:** The automated multi-agent governance pipeline (`hsri_agents/`) has executed live deliberative cycles exclusively against the Google Gemini 3.8 Flash model family due to API provisioning bounds. The divergence log reflects single-family responses rather than cross-architecture consensus.
- **Structural Missingness Protocol:** Rather than using statistical imputation, HSRI enforces structural NaNs for indicators with systemic missingness (e.g., non-European economies in EMLI; non-participating nations in PIAAC PSTRE). Exactly 86 nations are categorized as unrated and strictly excluded from extrapolation.
- **Proxy Inadequacy:** National macro proxies (broadband speeds, schooling years, survey participation) are imperfect representations of cognitive discernment and risk confounding economic development with epistemic resilience.
- **Non-Transferability of Synthetic Metrics:** Synthetic point-biserial discrimination coefficients ($D$) reflect prompted LLM capabilities and do not predict human performance or effect sizes.

---

## 5. Repository Resource Index

All referenced materials can be inspected directly in the local workspace:

- **Project README & Scope:** [`README.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/README.md)
- **Methodology & Scoring:** [`docs/methodology.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/docs/methodology.md)
- **Preprint Scaffold:** [`research/preprint/draft-v0.1.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/preprint/draft-v0.1.md)
- **EXP-01 Preregistration Draft:** [`research/experiments/EXP-01/prereg/prereg-draft.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/experiments/EXP-01/prereg/prereg-draft.md)
- **EXP-01 Calibration Plan:** [`research/experiments/EXP-01/prereg/item-calibration-plan.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/experiments/EXP-01/prereg/item-calibration-plan.md)
- **EXP-01 IRB Package Directory:** [`research/experiments/EXP-01/irb-package/`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/experiments/EXP-01/irb-package/)
- **EXP-02 IRB Package Directory:** [`research/experiments/EXP-02/irb-package/`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/experiments/EXP-02/irb-package/)
- **EXP-03 Stimulus Battery:** [`research/experiments/EXP-03/`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/experiments/EXP-03/)
- **Model Divergence Log Dataset:** [`hsri_agents/logs/model-divergence-log.csv`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/hsri_agents/logs/model-divergence-log.csv)
