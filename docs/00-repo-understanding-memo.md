# HSRI Repository Understanding Memo

## Executive Summary
This memo synthesizes the key aspects of the Human Superintelligence Readiness Index (HSRI) research repository to inform the development of a public benchmark-style interactive website. The memo covers the operational definition, capability framework, conceptual architecture, evidence standards, and tensions between the repository's current position and the task requirements.

---

## 1. Operational Definition of Readiness

The HSRI defines readiness operationally as:

> **"The demonstrated behavioral capacity of an individual, organization, or society to maintain calibrated trust, independent judgment, and value-directed goal-setting when interacting with AI systems whose task-specific performance meets or exceeds their own — measured behaviorally wherever possible, not merely self-reported."**

### Key Characteristics:
- **Behavioral, not attitudinal**: Focuses on observable actions rather than self-reported beliefs
- **Task-specific, not general**: Anchored to present-day cognitive asymmetry (e.g., chess engines, diagnostic classifiers, coding agents)
- **Calibrated trust**: Measures appropriate reliance, not simply "trust" or "distrust"
- **Independent judgment**: Emphasizes override behavior and verification
- **Value-directed goal-setting**: Focuses on preserving human agency in setting objectives

---

## 2. Capability Levels A–F

The repository classifies human-AI interaction into six ascending capability tiers:

| Level | System Role | Human Value Gains | Human Value Losses | Primary Failure Mode | Feasibility |
|-------|-------------|------------------|-------------------|---------------------|-------------|
| **A** | Tool | Basic digital literacy | Rote calculation | Non-adoption | Established |
| **B** | Cognitive Assistant | Verification habits | Manual info retrieval | Mild over-reliance | Established |
| **C** | Capable Collaborator | Error discernment | Initial drafting | Automation complacency | Active focus |
| **D** | Autonomous Task Manager | Oversight judgment | Manual execution | Deskilling | Active focus |
| **E** | Exceeds Human Reasoning | Meta-evaluative judgment | Individual expertise | Systemic dependence | Preliminary |
| **F** | Hypothetical Superintelligence | Unknown | Individual competition | Cognitive obsolescence | Speculative |

**Key Point**: HSRI is empirically grounded through Level D and cautiously extrapolated to Level E. Level F is purely conceptual.

---

## 3. Four-Tier Conceptual Scaffold

The repository organizes candidate variables into a four-tier theoretical framework:

### Tier 1: Foundational Substrates (Endogenous)
- Executive Attentional Control (ANT/SART)
- Metacognitive Sensitivity (Confidence-accuracy calibration)
- Cognitive Flexibility (Task-switching)

### Tier 2: Higher-Order Epistemic Mediators
- Cognitive Reflection (CRT)
- Intellectual Humility (CIHS)
- Uncertainty Tolerance (IUS-12)
- Value Clarity (Theoretical, supplementary)

### Tier 3: AI-Interaction Behavioral Interface (Novel Core)
- Calibrated Trust & Appropriate Reliance
- Discernment of Confident-Wrong AI Outputs
- Override Latency and Accuracy
- Resistance to Persuasive/Sycophantic Framing
- AI Literacy (Imported from UNESCO/OECD)

### Tier 4: Emergent Outcome
- Preserved Decisional Agency and Value-Directed Goal-Setting

---

## 4. Indicator Retention Decisions

After systematic redundancy audit, six candidate sub-components remain:

| Sub-component | Status | Rationale |
|---------------|--------|-----------|
| **Attentional Control** | Retained (Tier 1) | Reusable measurement paradigm from cognitive psychology |
| **Metacognition** | Retained (Tier 1) | Direct methodological reuse via confidence-accuracy calibration |
| **Decision Agency** | Retained (Tier 4) | Central organizing construct; distinct from mere capability |
| **Value Clarity** | Retained as supplementary | Theoretical dimension; empirical link unverified |
| **AI Literacy** | Retained (Tier 3) | Import existing frameworks rather than create redundant scales |
| **Calibrated Trust** | Retained (Tier 3) | Extension of classical automation bias to generative AI |

### Rejected Dimensions:
- Psychological stability (affective covariate only)
- Meditation frequency (candidate training intervention, not indicator)
- Generic collaboration (conflates agency with throughput)

---

## 5. Aggregation Models

The repository rejects simple composite scoring in favor of:

### Individual Level:
- **Non-compensatory threshold logic**: Critical weaknesses in foundational substrates cannot be offset by strengths in higher-order capabilities
- **Profile reporting**: Multidimensional scores with domain breakdowns
- **Mandatory uncertainty intervals**: Ranges rather than point estimates

### Organizational/National Level:
- **Currently deemed premature** per the roadmap
- Would require structural indicators (curricula, governance frameworks) not individual psychometrics

---

## 6. Six Candidate Sub-components

### 1. Attentional Control
- **Measurement**: Attention Network Test (ANT), Sustained Attention to Response Task (SART)
- **Role**: Foundational substrate for resisting notification overload and detecting subtle model drift

### 2. Metacognition
- **Measurement**: Confidence-accuracy calibration curves, meta-d' sensitivity
- **Role**: Self-monitoring capacity against AI output accuracy

### 3. Decision Agency
- **Measurement**: Behavioral delegation choices, override willingness, accountability retention
- **Role**: Central construct measuring preserved volition under AI assistance

### 4. Value Clarity
- **Measurement**: Values clarification tasks, goal-action consistency
- **Role**: Theoretical dimension protecting against goal drift

### 5. AI Literacy
- **Measurement**: AI Literacy Questionnaire (Ng et al.), UNESCO/OECD frameworks
- **Role**: Technical and conceptual understanding of AI systems

### 6. Calibrated Trust
- **Measurement**: Reliance ratios (correct vs. incorrect advice), error detection rates
- **Role**: Behavioral interface measuring appropriate automation reliance

---

## 7. Repo's Headline Recommendation

The repository concludes with a **"Develop as a research construct first"** recommendation for three key reasons:

1. **No validation data exists**: Zero psychometric validation of the construct
2. **Public indexing risks unmanaged**: Ethical safeguards against discrimination and responsibility laundering not yet established
3. **Methodological immaturity**: Premature national benchmarking would violate established index construction principles

The roadmap requires 11 phases of research before any public deployment, with Phase 6 (psychometric validation) being decisive.

---

## 8. Five-Tier Evidence Taxonomy

Claims are categorized by evidence strength:

| Tier | Tag | Meaning |
|------|-----|---------|
| **Strong** | `{: .evidence-strong }` | Multiple converging peer-reviewed sources; replicated findings |
| **Moderate** | `{: .evidence-moderate }` | Single high-quality RCT or small consistent literature |
| **Preliminary** | `{: .evidence-preliminary }` | Recent, active empirical area (e.g., 2020–2026 LLM studies) |
| **Theoretical** | `{: .evidence-theoretical }` | Coherent argument without direct empirical testing |
| **Speculative** | `{: .evidence-speculative }` | Plausible extrapolation outside current empirical reach |
| **Unverified** | `[UNVERIFIED — NEEDS SOURCE]` | Claim without verified citation |

The Master Evidence Table tracks all 42+ empirical claims with source citations.

---

## 9. Tensions with Repository Position

This task (creating a public country ratings website) creates significant tensions with the repository's stated position:

### Tension 1: Premature Public Indexing
- **Repo position**: "Public indexing risks unmanaged" — Phase 10 national benchmarking explicitly prohibited until Phase 6 validation
- **Task requirement**: Country ratings with as many countries as data supports
- **Proposed resolution**: Label as "HSRI-Proxy v0.1 — Public Preview for Review" with explicit disclaimers of validation status

### Tension 2: Behavioral vs. Proxy Measurement
- **Repo position**: HSRI is defined as behavioral and requires experiments in docs/05
- **Task requirement**: Country-level proxies now
- **Proposed resolution**: Clear separation between:
  - "Behavioral Evidence Layer": Empty, awaiting experiments
  - "Proxy Layer": Existing indicators mapping to HSRI sub-components

### Tension 3: Individual vs. National Aggregation
- **Repo position**: National aggregation premature (Phase 10)
- **Task requirement**: Country ratings
- **Proposed resolution**: Measure enabling environment separately, acknowledge proxy limitations

### Tension 4: Composite Scores vs. Profile Reporting
- **Repo position**: Prohibit bare composite rankings; require multidimensional profiles
- **Task requirement**: Leaderboard-style presentation
- **Proposed resolution**: Show ranges, not point estimates; include full pillar breakdowns

### Tension 5: Ethical Concerns
- **Repo position**: Strong safeguards against responsibility laundering and discrimination
- **Task requirement**: Public benchmarking
- **Proposed resolution**: Prominent "How this index could be misused" section and ethics disclaimer

---

## 10. Proposed Resolution Approach

The approach should be:
1. **Transparent about limitations**: Explicit "v0.1 Public Preview — not validated" status
2. **Methodologically honest**: Clear separation between behavioral construct (unmeasured) and proxy indicators
3. **Ethically cautious**: Prominent responsibility laundering disclaimer
4. **Scientally rigorous**: Full provenance and evidence tiering
5. **Incrementally validatable**: Clear path from proxy to validated construct

This maintains scientific integrity while providing value as an early warning system about where the genuine research gaps exist at country level.