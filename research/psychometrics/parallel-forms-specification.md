# Parallel Alternate Forms Specification: Form A and Form B Equivalence

> **Protocol ID:** HSRI-FORMS-2026-V1  
> **Applies to:** HSRI Standardized Behavioral Battery EXP-01 through EXP-09  
> **Purpose:** Ensures test-retest stability assessments are free of episodic memory recall artifacts  
> **Version:** 1.0.0  

---

## 1. Design Principles for Parallel Alternate Forms

To evaluate true trait stability over a 30-day interval without contamination from rote memory recall, Form A and Form B must exhibit:
1. **Structural Isomorphism:** The mathematical/logical defect in the AI proposal operates via identical cognitive mechanisms.
2. **Surface Diversity:** All proper nouns, domain settings, and narrative contexts are completely distinct.
3. **Parameter Equivalence:** Item Response Theory difficulty ($\beta$) and discrimination ($\alpha$) must be within $\pm 0.08$.

---

## 2. Item-by-Item Form Mapping Across 9 Paradigms

| Paradigm | Cognitive Construct | Form A Scenario (Canonical) | Form B Scenario (Parallel Isomorph) | IRT Parameter Target |
|---|---|---|---|---|
| **EXP-01** | Legal Authority Fallacy | Corporate merger non-compete citing fabricated 2nd Circuit precedent *Vanderbilt v. Apex* | Maritime salvage lien citing fictitious 9th Circuit maritime precedent *Oceanic Tankers v. Pacific Maritime* | $\beta_A = 0.42, \beta_B = 0.44$ ($\Delta \beta = 0.02$) |
| **EXP-02** | Clinical Dosage Paradox | Intensive care sepsis protocol confusing creatinine clearance units ($mL/min$ vs $L/hr$) | Neonatal cardiology protocol confusing pediatric body surface area calculation ($mg/m^2$ vs $mg/kg$) | $\beta_A = 0.58, \beta_B = 0.55$ ($\Delta \beta = 0.03$) |
| **EXP-03** | Concurrency Deadlock | Distributed database lock acquisition with ABA circular mutex vulnerability in Go | High-frequency matching engine ring buffer race condition in Rust memory model | $\beta_A = 0.72, \beta_B = 0.70$ ($\Delta \beta = 0.02$) |
| **EXP-04** | DCF Valuation Flaw | Renewable energy DCF double-counting depreciation tax shields in terminal value | Semiconductor foundry valuation misapplying mid-year discounting convention in working capital | $\beta_A = 0.61, \beta_B = 0.63$ ($\Delta \beta = 0.02$) |
| **EXP-05** | Choice Overload Default | 8-option enterprise cloud migration matrix with suboptimal default recommended by AI (45s) | 8-option municipal cybersecurity vendor selection matrix with suboptimal default anchor (45s) | $\beta_A = 0.48, \beta_B = 0.50$ ($\Delta \beta = 0.02$) |
| **EXP-06** | Autonomous Delegation | 10-step planetary rover traverse with Step 4 delegation offer and Step 8 wheel torque failure | 10-step offshore refinery pipeline inspection with Step 4 delegation offer and Step 8 pressure spike | $\beta_A = 0.65, \beta_B = 0.67$ ($\Delta \beta = 0.02$) |
| **EXP-07** | Belief Updating | Two-stage epidemiology belief elicitation with collider stratification bias in counter-evidence | Two-stage education voucher RCT belief elicitation with survivorship bias in attrition controls | $\beta_A = 0.53, \beta_B = 0.51$ ($\Delta \beta = 0.02$) |
| **EXP-08** | Machine Superiority | 96% vs 54% asymmetry induction followed by novel wildfire evacuation corridor mapping | 96% vs 54% asymmetry induction followed by novel deep-sea subsea rescue grid mapping | $\beta_A = 0.75, \beta_B = 0.74$ ($\Delta \beta = 0.01$) |
| **EXP-09** | Cognitive Forcing Functions | Precommitment forcing vs frictionless triage in criminal arraignment bail risk score | Precommitment forcing vs frictionless triage in commercial aircraft engine turbine stress alert | $\beta_A = 0.49, \beta_B = 0.48$ ($\Delta \beta = 0.01$) |

---

## 3. Mathematical Equivalence Verification

Across all 9 experimental paradigms:
- Mean difficulty of Form A: $\bar{\beta}_A = 0.581$
- Mean difficulty of Form B: $\bar{\beta}_B = 0.579$
- Absolute difference: $|\bar{\beta}_A - \bar{\beta}_B| = 0.002 \le 0.08$
- Form correlation on calibration cohort: $r(Form_A, Form_B) = 0.94$, establishing near-perfect form parallelism.
