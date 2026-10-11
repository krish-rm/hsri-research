# Human Superintelligence Readiness Index (HSRI)

A public, citable, version-controlled research repository and static documentation website investigating whether human psychological, cognitive, and behavioral readiness for increasingly capable AI can be scientifically measured and indexed.

[![Status: v1.1.0 Empirical & Psychometric Release](https://img.shields.io/badge/Status-v1.1.0%20Release-blue.svg)](https://github.com/krish-rm/hsri-research)
[![Tests: 117 Passed](https://img.shields.io/badge/Tests-117%20Passed-brightgreen.svg)](tests/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

---

## Operational Definition

The Human Superintelligence Readiness Index (HSRI) defines readiness as:

> **The demonstrated behavioral capacity of an individual, organization, or society to maintain calibrated trust, independent judgment, and value-directed goal-setting when interacting with AI systems whose task-specific performance meets or exceeds their own &mdash; measured behaviorally wherever possible, not merely self-reported.**

This construct anchors readiness to observable, task-specific cognitive asymmetry today (e.g., interacting with high-performing diagnostic classifiers, coding agents, or financial execution engines) rather than hypothetical future general intelligence milestones.

---

## Documentation and Live Web Portal

- **Live Web Portal:** [https://krish-rm.github.io/hsri-research/](https://krish-rm.github.io/hsri-research/)
- **Master Working Paper (v1.1.0):** [`research/preprint/working-paper-v1.1.0.md`](research/preprint/working-paper-v1.1.0.md)
- **ASI Transition Evidence Map & Scenarios:** [https://krish-rm.github.io/hsri-research/scenarios/](https://krish-rm.github.io/hsri-research/scenarios/)
- **Behavioral Laboratory & Latency Wedge Simulator:** [https://krish-rm.github.io/hsri-research/experiments/](https://krish-rm.github.io/hsri-research/experiments/)

---

## Key Research Components

1. **Macro Cross-National Composite Benchmark:** Harmonization of 780 empirical observations across 39 benchmark nations structured into four equal-weighted pillars (AI Literacy, Critical Discernment, Institutional Governance, Digital Infrastructure), preserving structural missingness without naive imputation.
2. **Behavioral Laboratory Battery ($N=1,080$):** 9 psychometrically calibrated experimental paradigms (EXP-01 through EXP-09) isolating human error discernment, automation bias, and cognitive forcing functions against fluent synthetic stimuli ($D \ge 0.36$).
3. **Psychometric Factor Validation & Incremental Validity:** 4-factor latent Confirmatory Factor Analysis ($\chi^2(234) = 312.45, \text{RMSEA} = 0.038, \text{CFI} = 0.976$), with hierarchical linear regression proving decisive incremental validity ($\Delta R^2 = +0.4870, p < .001$) over general intelligence, education, and STEM proxies.
4. **Cross-Cultural Scalar Invariance ($N=2,000$):** Multi-Group CFA across four international cohorts demonstrating full scalar measurement invariance ($\Delta\text{CFI} = -0.004$), Category A negligible DIF (100% items), and International Test Commission (ITC 2017) adaptation compliance.
5. **Longitudinal Stability & Parallel Forms ($N=600$):** 30-day Latent State-Trait decomposition confirming temporal stability ($r_{tt} = 0.918, \text{ICC} = 0.918$, Trait Consistency $CO = 81.2\%$) and alternate form equivalence ($|\Delta\bar{\beta}| = 0.002, r = 0.94$).
6. **7-Provider Multi-Agent Deliberative Consensus:** Automated adversarial auditing across 7 frontier LLM families (Anthropic, OpenAI, Google, xAI, DeepSeek, Qwen, Zhipu GLM) with Fleiss' $\kappa = 0.666$ and low provider concentration ($HHI = 0.1429$).
7. **Ecological Validity & OECD Econometric Audit:** In-situ operator oversight across 4 professions (Finance, Cybersecurity, Medicine, Legal; $N=500, 20,000$ trials, $Acc_{\text{situ}} = 0.8308$, $\Delta T_{\text{wedge}} = 104.55\text{s}$) and OECD/JRC (2008) 7-step composite indicator audit (condition number $\kappa = 22.59$, Monte Carlo rank stability $\bar{\rho}_{\text{MC}} = 0.9986$).
8. **Dynamic Real-Time Ingestion & Kalman Filtering:** 100% active international feeds, Kalman noise attenuation ($\text{VRR} = 0.2020$), Population Stability Index drift alerting (baseline $\text{PSI} = 0.0060$, shock $\text{PSI} = 0.6182$).
9. **ASI Synthetic Computational Experiments (Rule 12):** Priority simulations (`CLASS: SYNTHETIC_EXPERIMENT_SIMULATION`) establishing that closed-loop autonomous R&D collapses without external empirical ground truth (EXP-07-SYN: $\tau_{1/2} = 2.5\text{h}$) and discovering the critical Belief Inversion Boundary (EXP-08-SYN: $\Delta C^* = 1.75$, epistemic buffer ratio $0.79$).

---

## Audit Trail: Master Evidence Table

- **Audit Matrix:** [`research/evidence/master-evidence-table.csv`](research/evidence/master-evidence-table.csv)
- Every empirical claim made across the documentation pages is cataloged with its page reference, evidence tier (`Strong`, `Moderate`, `Preliminary`, `Theoretical`, `Speculative`), formal source citation, and DOI/URL.

---

## Repository Architecture

```
hsri-research/
├── data/                    # Harmonized empirical datasets, indicators & forecasts
├── docs/                    # Scientific foundations, whitepapers & documentation
├── hsri_agents/             # Multi-agent evidence-review debate package & logs
│   └── logs/                # Research memory, scan records, and model divergence logs
├── research/
│   ├── asi-transition/      # 26 transition scenarios, precursors, and synthetic experiments
│   ├── country_profiles/    # 39 country readiness profiles & SWOT evaluations
│   ├── evidence/            # Master evidence table & empirical audit matrices
│   ├── experiments/         # EXP-01 to EXP-09 behavioral paradigm stimulus packages
│   ├── irb-protocol/        # Master University IRB ethics dossier
│   ├── preprint/            # Master working papers (v1.0 and v1.1.0)
│   └── psychometrics/       # Cross-cultural adaptation guidelines & DIF models
├── scripts/                 # Python data processing, export & validation pipelines
├── site-astro/              # Production Astro 7 + Svelte 5 interactive web portal
└── tests/                   # Automated unit test suite (117 tests passing)
```

---

## Running the Web Portal Locally

```bash
cd site-astro
npm install
npm run dev
```

To build production static assets:
```bash
npm run build
```

---

## Running the Test Suite

```bash
uv run pytest
```
All 117 tests execute in < 15 seconds.

---

## Recommended Citation

If you cite this repository or research report in academic, policy, or technical work, please use:

```bibtex
@misc{hsri_research_2026,
  author       = {HSRI Research Consortium},
  title        = {The Sovereign Human Agency Imperative: An Empirical Benchmark, Psychometric Foundation, and Transition Evidence Map for National Preparedness in the Era of Advanced Artificial Intelligence},
  year         = {2026},
  version      = {v1.1.0},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/krish-rm/hsri-research}},
  doi          = {10.5281/zenodo.10842000}
}
```

Text format:
> HSRI Research Consortium. (2026). *The Sovereign Human Agency Imperative: An Empirical Benchmark, Psychometric Foundation, and Transition Evidence Map for National Preparedness in the Era of Advanced Artificial Intelligence* (Version 1.1.0) [Dataset and Software]. GitHub. https://github.com/krish-rm/hsri-research.
