# Human Superintelligence Readiness Index (HSRI)

A public, citable, version-controlled research repository and static documentation website investigating whether human psychological, cognitive, and behavioral readiness for increasingly capable AI can be scientifically measured and indexed.

[![Status: Early research draft — not peer reviewed](https://img.shields.io/badge/Status-Early%20research%20draft%20%E2%80%94%20not%20peer%20reviewed-amber.svg)](https://github.com/krish-rm/hsri-research)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## Operational Definition

The Human Superintelligence Readiness Index (HSRI) defines readiness as:

> **The demonstrated behavioral capacity of an individual, organization, or society to maintain calibrated trust, independent judgment, and value-directed goal-setting when interacting with AI systems whose task-specific performance meets or exceeds their own &mdash; measured behaviorally wherever possible, not merely self-reported.**

This construct anchors readiness to observable, task-specific cognitive asymmetry today (e.g., interacting with high-performing diagnostic classifiers, coding agents, or chess engines) rather than hypothetical future general intelligence milestones.

---

## Documentation and Live Website

- **Live Documentation Website:** [https://krish-rm.github.io/hsri-research/](https://krish-rm.github.io/hsri-research/)
- Complete multi-page research report, construct audit, experimental designs, and governance protocols are published and readable via the link above.

---

## Audit Trail: Master Evidence Table

- **Audit Matrix:** [evidence/master-evidence-table.csv](evidence/master-evidence-table.csv)
- Every empirical claim made across the documentation pages is cataloged with its page reference, evidence tier (`Strong`, `Moderate`, `Preliminary`, `Theoretical`, `Speculative`, or `[UNVERIFIED — NEEDS SOURCE]`), formal source citation, and DOI/URL.

---

## How to Contribute

We welcome rigorous critical peer review, counterarguments, and source verification. See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines, including:

1. Proposing a stronger or additional source for an existing claim.
2. Submitting a new objection or counterargument for `docs/07-objections.md`.
3. Proposing a new candidate behavioral experiment for `docs/05-measurement-and-experiments.md`.

*Note: Any pull request modifying an empirical claim must update [evidence/master-evidence-table.csv](evidence/master-evidence-table.csv).*

---

## Evidence-Review Pipeline (HSRI-Agents)

The repository includes `hsri_agents`, an automated evidence-review and adversarial multi-agent debate pipeline designed to audit incoming literature, evaluate candidate evidence against established psychometric lanes, convene structured debates, and draft proposed diffs subject to a 3-seat Consortium Review Board veto gate.

- **Manual-First Operation:** The pipeline is currently operated strictly by hand, one step at a time, pending a cadence decision. Automated cron jobs, schedulers, and webhooks are intentionally deferred until manual protocols are validated.
- **Multi-Model Reliability Ensemble:** The same evidence-review protocol is executed independently across model families (Anthropic, OpenAI, Google, xAI, DeepSeek, Alibaba Qwen, and Zhipu GLM) to test whether conclusions are robust to which model performs the review—not as competing national or corporate teams.
- **Audit Logs:** Full debate transcripts are recorded in [research_memory.md](research_memory.md), and cross-model concordance is tracked in [model-divergence-log.csv](model-divergence-log.csv). See [`hsri_agents/README.md`](hsri_agents/README.md) for CLI usage.

---

## Recommended Citation

If you cite this repository or research feasibility report in academic, policy, or technical work, please use the following citation format:

```bibtex
@misc{hsri_research_2026,
  author       = {HSRI Research Consortium},
  title        = {Human Superintelligence Readiness Index (HSRI): Conceptual Foundation, Scientific Feasibility, and Governance Blueprint},
  year         = {2026},
  version      = {v0.1.0-draft},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/krish-rm/hsri-research}},
  doi          = {10.5281/zenodo.XXXXXXX} /* Placeholder: Zenodo DOI to be assigned upon initial release */
}
```

Text format:
> HSRI Research Consortium. (2026). *Human Superintelligence Readiness Index (HSRI): Conceptual Foundation, Scientific Feasibility, and Governance Blueprint* (Version v0.1.0-draft) [Computer software]. GitHub. https://github.com/krish-rm/hsri-research. DOI: 10.5281/zenodo.XXXXXXX (Placeholder).
