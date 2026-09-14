# 4. Causal Model and Index Design

Designing a scientifically defensible index requires an explicit structural theory linking foundational psychological capacities to observable behavioral outcomes under AI cognitive asymmetry. This section outlines human agency as the central organizing axis, articulates a four-tier conceptual scaffold, details dimension retention decisions, evaluates three aggregation architectures, and examines multi-level feasibility across individual, organizational, and national domains.

---

## 4.1 Human Agency as the Central Organizing Axis

The core organizing axis of HSRI is **agency**, not capability or throughput.
{: .evidence-theoretical }

Drawing on Self-Determination Theory (Deci & Ryan), autonomy (acting from reflective volition and internal endorsement) is empirically distinguishable from competence (capability):

- **High Capability / Low Agency:** A technical expert who, facing complex code or analytical outputs, reflexively accepts fluent AI recommendations without verification, diffusing personal accountability.
- **Low Capability / High Agency:** A non-expert who knowingly delegates task execution to an AI system while retaining full ownership of the criteria for success, critically probing assumptions, and accepting responsibility for failures.

No existing composite capability index (e.g., HDI, Social Progress Index, Human Capital Index) captures this behavioral distinction at the individual level. Concentrating on agency prevents HSRI from collapsing into a conventional cognitive ability test or digital literacy benchmark.
{: .evidence-theoretical }

---

## 4.2 Proposed Four-Tier Conceptual Framework

To structure empirical investigation, candidate variables are organized into a four-tier theoretical scaffold:

```
[ Tier 1: Foundational Substrates (Endogenous) ]
  ├── Executive Attentional Control (ANT / SART)
  ├── Metacognitive Sensitivity (Confidence-Accuracy Calibration)
  └── Cognitive Flexibility (Task-Switching / Set-Shifting)
           │
           ▼
[ Tier 2: Higher-Order Epistemic & Decisional Mediators ]
  ├── Cognitive Reflection (CRT)
  ├── Intellectual / Epistemic Humility (CIHS)
  ├── Uncertainty Tolerance (IUS-12)
  └── Value Clarity & Reflective Endorsement (PVQ)
           │
           ▼
[ Tier 3: AI-Interaction Behavioral Interface (Novel Core) ]
  ├── Calibrated Trust & Appropriate Reliance (Reliance Ratio)
  ├── Discernment of Confident-Wrong AI Outputs (Detection Rate)
  ├── Override Latency, Accuracy, and Willingness
  └── Resistance to Persuasive / Sycophantic AI Framing
           │
           ▼
[ Tier 4: Emergent Outcome ]
  └── Preserved Decisional Agency and Value-Directed Goal-Setting
```

### Causal Ordering Hypotheses
Foundational substrates (Tier 1) are hypothesized to enable higher-order mediators (Tier 2), which in turn enable specific AI-interaction competencies (Tier 3), collectively predicting preserved agency (Tier 4).
{: .evidence-theoretical }

> **Methodological Epistemic Rule:** This four-tier arrangement is a **theoretical scaffold to be empirically tested**, not a fitted structural equation model. Stating pre-calibrated path coefficients (e.g., $\beta$ or $\gamma$ weights) prior to data collection conveys false mathematical precision and introduces pseudoscience risk. The required scientific sequence is: (1) establish tiers conceptually and achieve expert consensus via Delphi panels, (2) gather empirical pilot data, and (3) fit and publish structural equation models with transparent standard errors and confidence intervals.
{: .evidence-theoretical }

---

## 4.3 Candidate Dimensions: Inclusion, Pruning, and Retention

Early proposals contained 18 disparate dimensions. Applying the redundancy audit produced the following pruning decisions:

| Candidate Dimension | Proposed Tier | Methodological Disposition | Psychometric Rationale |
|---|---|---|---|
| **Psychological Stability** | Baseline | Reject as standalone; retain as affective covariate under cognitive load. | Standalone measure conflates readiness with general neuroticism and clinical mental health. |
| **Attentional Control** | Tier 1 | **Retain** (Endogenous Substrate) | Necessary substrate for resisting notification interruptions and detecting subtle model drift. |
| **Metacognition** | Tier 1 | **Retain** (Monitoring Substrate) | Core self-monitoring capacity; confidence-accuracy calibration methods directly reusable. |
| **Self-Knowledge** | — | **Merge into Metacognition** | Conceptually redundant with metacognitive monitoring. |
| **Cognitive Flexibility** | Baseline | Retain as covariate | Required to update priors given valid AI evidence, but fully measured by standard neuropsychological tests. |
| **Epistemic Humility** | Tier 2 | **Retain** (Mediator) | Prevents algorithm aversion and dogmatic rejection of valid machine assistance. |
| **Discernment** | Tier 3 | **Operationalize via Behavioral Tasks** | Measure behaviorally via detection of confident-wrong outputs rather than via self-report. |
| **Decision Agency** | Tier 4 | **Retain** (Primary Outcome) | Central organizing construct of the index. |
| **Value Clarity** | Tier 2 | **Retain as Theoretical / Supplementary** | Protects against goal drift toward machine-optimized proxy metrics; empirical link to AI context remains unverified `[UNVERIFIED — NEEDS SOURCE]`. |
| **Meaning / Purpose** | — | **Move to Supplementary Research** | Substantial cross-cultural variation; high risk of measurement non-invariance. |
| **AI Literacy** | Tier 3 | **Retain (Import Frameworks)** | Import existing validated frameworks (UNESCO, OECD, Ng et al.) rather than creating redundant scales. |
| **Generic Collaboration** | — | **Reject** | Conflates preserved human agency with mere operational task throughput. |
| **Automation-Bias Resistance** | Tier 3 | **Retain** (Behavioral Interface) | Primary behavioral indicator anchored in decades of human factors literature. |
| **Resistance to Manipulation** | — | **Merge with Automation-Bias Resistance** | Driven by identical underlying mechanisms of epistemic vigilance. |
| **Uncertainty Tolerance** | Tier 2 | **Retain** (Mediator) | Predicts premature surrender of judgment when facing ambiguous machine recommendations. |
| **Accountability Retention** | Tier 4 | **Retain** (Outcome Dimension) | Distinct from override behavior; measures whether an operator accepts moral/causal ownership of AI-assisted outputs. |
| **Social / Relational Resilience** | — | **Move to Institutional / Societal Level** | Belongs to organizational governance, not individual psychometrics. |
| **Independent Judgment** | — | **Merge with Decision Agency** | Conceptually identical under conditions of cognitive conflict. |

---

## 4.4 Index Design: Three Candidate Architectures

Evaluating aggregation architectures is critical to avoid structural failure modes documented in existing international indices:

| Architecture Model | Mathematical Structure | Weighting Scheme | Architectural Strengths | Critical Weaknesses & Failure Modes |
|---|---|---|---|---|
| **Model A: Equal-Weight Composite** | Arithmetic mean of normalized sub-scores: $$I = \frac{1}{k}\sum_{i=1}^k S_i$$ | Equal weights assigned a priori ($w_i = 1/k$). | Simple, fully transparent, computationally trivial to audit. | Inherits the SPI's primary methodological flaw: assumes each component contributes identically and independently to readiness (Jitmaneeroj, 2017). |
| **Model B: Evidence-Weighted Composite** | Weighted sum or regression model: $$I = \sum_{i=1}^k w_i S_i$$ | Empirically derived weights (PCA factor loadings or regression coefficients predicting real override accuracy). | Statistically defensible; aligns weights with actual predictive power. | **Premature before Phase 6 validation.** Weights cannot be estimated without large-scale validation data; claiming empirical weights today is methodologically fraudulent. |
| **Model C: Hierarchical / Threshold Composite** | Domain profile reporting with non-compensatory critical-weakness floor: $$I = f(\mathbf{S}) \quad \text{s.t.} \quad \min(S_{\text{Tier 1}}) \ge \theta$$ | Foundational domains act as non-compensatory gating constraints; higher tiers aggregated conditionally. | Prevents high literacy or confidence from compensating for a total inability to catch critical machine errors. Aligns with MPI dual-cutoff logic (Alkire & Foster, 2011). | More complex to communicate; selecting cutoff thresholds ($\theta$) involves normative judgment that requires explicit pre-registration and sensitivity testing. |

### Architectural Recommendation
Adopt **Model C's reporting logic** (disaggregated domain profiles accompanied by critical-weakness flags) while utilizing **Model A's provisional equal weighting** strictly during exploratory pilot studies (Phase 4). Migrate to **Model B's empirical weights** only after Phase 6 psychometric validation generates real criterion data.
{: .evidence-theoretical }

---

## 4.5 Multi-Level Feasibility: Individual, Organizational, National

| Analytical Level | Scientific Feasibility | Recommended Operational Form | Critical Methodological Caution |
|---|---|---|---|
| **Individual HSRI** | **Feasible as Research Instrument** | Standardized behavioral battery (ANT, calibration tasks, simulated AI-interaction scenarios). | **Must not be published as public rankings or used for employment screening.** |
| **Organizational HSRI** | **Feasible as Diagnostic Audit** | Workflow auditing of override behavior, accountability tracing, and error-recovery latency in real decision systems. | Substantially overlaps existing IT change-management and digital-maturity models. |
| **National HSRI** | **Not Currently Feasible as Aggregated Psychometrics** | Separate composite of national indicators: AI curriculum penetration, institutional trust, information integrity, and regulatory governance quality. | **Aggregating individual psychological scores to national averages commits an ecological fallacy** and duplicates established AI-readiness indices. |

National benchmarking should **not** be attempted until Phases 1–6 have rigorously validated the individual construct.
{: .evidence-theoretical }

---

## Sources on this page

- **Alkire, S., & Foster, J. (2011).** Counting and multidimensional poverty measurement. *Journal of Public Economics*, 95(7–8), 476–487.
- **Deci, E. L., & Ryan, R. M. (2000).** The "what" and "why" of goal pursuits: Human needs and the self-determination of behavior. *Psychological Inquiry*, 11(4), 227–268.
- **Jitmaneeroj, B. (2017).** Beyond the equal-weight framework of the Social Progress Index: A quantile regression approach. *International Journal of Social Economics*, 44(12), 2336–2350.
- **OECD & European Commission Joint Research Centre. (2008).** *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
