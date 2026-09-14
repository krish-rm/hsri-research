# Contributing to HSRI Research

Thank you for your interest in contributing to the **Human Superintelligence Readiness Index (HSRI)** research repository.

This project is maintained for an audience of skeptical academics, cognitive scientists, AI safety researchers, and policy analysts. Every structural decision in this repository is designed to prioritize **auditability, falsifiability, and epistemic rigor** over speculative enthusiasm.

---

## Three Primary Contribution Types

We actively solicit contributions in three specific areas:

### 1. Proposing a Stronger or Additional Source for an Existing Claim
- **Scope:** If a claim currently tagged `[UNVERIFIED — NEEDS SOURCE]` has an established peer-reviewed source, or if a claim tagged `Preliminary` or `Moderate` can be strengthened by meta-analyses or high-powered pre-registered replications.
- **Requirement:** Provide full bibliographic details (authors, year, title, journal/conference, DOI or open-access URL). Do not summarize findings with greater precision than the primary paper's actual statistics justify.

### 2. Submitting a New Objection or Counterargument
- **Scope:** Proposing additions or refinements to [`docs/07-objections.md`](docs/07-objections.md).
- **Requirement:** Present the counterargument in its strongest, steel-manned form. We actively welcome arguments that expose construct redundancy, measurement impossibility, cultural bias, or ethical risks (such as responsibility laundering). The self-critical posture of this repository is a core feature, not a flaw to be softened.

### 3. Proposing a New Candidate Behavioral Experiment
- **Scope:** Expanding the behavioral evaluation battery in [`docs/05-measurement-and-experiments.md`](docs/05-measurement-and-experiments.md).
- **Requirement:** Experiments must be testable today using existing frontier AI systems under task asymmetry. Propose explicit independent variables, operational metrics (override latency, reliance ratios, detection rates), and falsifiable criteria. Avoid speculative setups predicated on hypothetical future AGI.

---

## Mandatory Rule: Master Evidence Table Updates

> [!IMPORTANT]
> **Every pull request that adds, modifies, or challenges an empirical claim MUST update [`evidence/master-evidence-table.csv`](evidence/master-evidence-table.csv).**

When updating `master-evidence-table.csv`:
- Ensure all 6 columns are populated: `claim, page_reference, evidence_tier, source_citation, source_url_or_doi, notes`.
- Assign the appropriate evidence tier:
  - `Strong`: Multiple converging peer-reviewed sources or large-scale meta-analyses.
  - `Moderate`: Single high-quality RCT or small consistent literature.
  - `Preliminary`: Recent, active empirical literature (e.g., post-2020 LLM interaction studies).
  - `Theoretical`: Coherent conceptual, mathematical, or philosophical argument without direct empirical testing.
  - `Speculative`: Plausible extrapolation outside current empirical reach.
  - `[UNVERIFIED — NEEDS SOURCE]`: Claim appears in source text without an identifiable, checked citation.
- Ensure no required cell is left blank.

---

## Development & Verification Workflow

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feature/propose-source-claim-12
   ```
2. Make your edits in `docs/` and `evidence/master-evidence-table.csv`.
3. Verify the documentation build locally:
   ```bash
   pip install -r requirements.txt # or pip install mkdocs-material
   python -m mkdocs build --strict
   ```
   *The build must succeed with zero warnings and zero broken internal links.*
4. Commit your changes with a descriptive, atomic commit message and open a Pull Request.
