# Contributing to HSRI

Thank you for your interest in contributing to the **Human Superintelligence Readiness Index (HSRI)** research repository.

This project is maintained for an audience of skeptical academics, cognitive scientists, AI safety researchers, and policy analysts. Every structural decision in this repository is designed to prioritize **epistemic integrity over velocity**.

---

## Ways to Contribute

### 1. Data Issues
If you believe an indicator value for a specific country is incorrect, open a GitHub Issue with:
- Country ISO3 code
- Indicator ID (from `data-dictionary.md`)
- Current value in the dataset
- Correct value with source citation (DOI or institutional URL)

### 2. Evidence Challenges
If you are aware of published research that challenges a claim in `research/evidence/master-evidence-table.csv`, open an Issue with:
- Claim ID from the evidence table
- Challenging paper DOI
- Brief summary of why the claim requires review

Evidence challenges are processed through the Lane 3 adversarial debate system. They do not result in immediate score changes.

### 3. Coverage Expansion
If you represent a statistical agency or institution that can provide data for currently unrated nations, please open an Issue tagged `coverage-expansion`. See `data/unrated-nations.csv` for the list of nations and their primary data gaps.

### 4. Methodology Feedback
Substantive methodology critiques should be filed as GitHub Issues with the tag `methodology-review`. These are routed to the Consortium Review Board process described in `docs/08-roadmap.md`.

---

## What We Do Not Accept
- Direct edits to `data/indicators.csv` or `data/final_country_scores.csv` without a full evidence trail through the Lane 3–4 pipeline
- Claims that a country should rank higher or lower without specific indicator-level evidence
- Suggestions to impute EMLI or PIAAC PSTRE for non-participating nations (see `docs/10-proxy-framework.md §Missingness` for the governance rationale)

---

## Replication
To replicate the index from scratch:
1. Clone the repository:
   ```bash
   git clone https://github.com/krish-rm/hsri-research.git
   cd hsri-research
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run observation harmonization:
   ```bash
   python scripts/ingestion/harmonize_observations.py
   ```
4. Run mathematical index construction:
   ```bash
   python scripts/index_construction.py
   ```
5. Compare output to `data/final_country_scores.csv`.

Full methodology: see `data-dictionary.md` and `docs/`.

---

## Mandatory Rule: Master Evidence Table Updates

> [!IMPORTANT]
> **Every pull request that adds, modifies, or challenges an empirical claim MUST update [`research/evidence/master-evidence-table.csv`](research/evidence/master-evidence-table.csv).**

When updating `master-evidence-table.csv`:
- Ensure all 7 columns are populated: `claim, page_reference, evidence_tier, source_citation, source_url_or_doi, notes, reconciliation_flag`.
- Assign the appropriate evidence tier:
  - `Strong`: Multiple converging peer-reviewed sources or large-scale meta-analyses.
  - `Moderate`: Single high-quality RCT or small consistent literature.
  - `Preliminary`: Recent, active empirical literature (e.g., post-2020 LLM interaction studies).
  - `Theoretical`: Coherent conceptual, mathematical, or philosophical argument without direct empirical testing.
  - `Speculative`: Plausible extrapolation outside current empirical reach.
  - `[UNVERIFIED — NEEDS SOURCE]`: Claim appears in source text without an identifiable, checked citation.
