# HSRI 2.0 Regulatory & Standards Crosswalk
## Mapping Civilizational Sovereignty Constructs to International Statutory, Governance & Actuarial Frameworks

> **Document Class**: Regulatory Harmonization & Standards Crosswalk  
> **Version**: 2.5.0  
> **Author & Lead Principal Investigator**: Krishnakumar Radhakrishnan  
> **Permanent DOI**: [10.5281/zenodo.23441742](https://doi.org/10.5281/zenodo.23441742)  
> **Target Frameworks**: EU AI Act, NIST AI RMF 1.0, ISO/IEC 42001, EU NIS 2, CISA CPGs, EU Solvency II Directive  

---

## 1. Executive Intent: Neutralizing Abstraction Debt

A common critique of frontier AI safety benchmarks is **abstraction debt**: the tendency to introduce novel, bespoke theoretical metrics (e.g., VSR, CORS, ECDL) without grounding them in the statutory language and compliance architectures used by international regulators, enterprise risk officers, and reinsurance underwriters.

This document establishes the **authoritative crosswalk matrix** connecting the mathematical formulations of HSRI 2.0 directly to binding international standards, translating academic and theoretical constructs into auditable regulatory controls.

```
+---------------------------------------------------------------------------------------------------------+
|                                HSRI REGULATORY HARMONIZATION HIERARCHY                                  |
+---------------------------------------------------------------------------------------------------------+
| HSRI CONSTRUCT                     PRIMARY REGULATORY MAPPING                  AUDIT CONTROL ID         |
| ---------------------------------  ------------------------------------------  ------------------------ |
| Epistemic Inviolability (VSR)      EU AI Act Article 14 (Human Oversight)     AIA-ART-14-VSR           |
| Verification Wedge (ΔT_wedge)      NIST AI RMF 1.0 (Measure 2.5 / Manage 2.4) NIST-RMF-MEAS-2.5        |
| Decoupling Half-Life (T_half)      EU NIS 2 Directive & CISA CPG Goal 2.A     NIS2-ART-21-CPG-2A       |
| Coordination Velocity (V_coord)    UN AI Advisory Body & G7 Hiroshima Code    UN-G7-COORD-04           |
| Precursor Seismograph (CORS 10.0)  US EO 14110 Sec 4.2 & UK AISI Standards    EO14110-SEC42-CORS       |
| Actuarial Risk Loading (Φ) & ECDL  EU Solvency II (Directive 2009/138/EC)      SOLV-II-ART-105-SCR      |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Master Crosswalk Matrix

### Pillar 5: Epistemic Inviolability & Verification Sovereignty Ratio (VSR)

$$\text{VSR} = \frac{\tau_{\text{gen}}}{\tau_{\text{verify}}} \in [0, 1]$$

| Regulatory Framework | Specific Clause / Control | Compliance Interpretation & HSRI Diagnostic |
|---|---|---|
| **EU Artificial Intelligence Act (Regulation 2024/1689)** | **Article 14 (Human Oversight)**: Providers and deployers of high-risk AI must enable natural persons to oversee systems, prevent automation bias, and remain able to override outputs. | **Non-Compliance Diagnosis**: When $\text{VSR} < 0.05$ (or $\Delta T_{\text{wedge}} > 300\text{s}$), natural human oversight is mathematically impossible within statutory operational windows. HSRI proves Article 14 cannot be satisfied by screen-based interfaces without architectural rate-limiting. |
| **NIST AI Risk Management Framework (AI RMF 1.0)** | **Measure 2.5**: AI system performance is measured against human operator capabilities in realistic operating environments.<br>**Manage 2.4**: Human oversight processes are documented and calibrated. | HSRI isolates the human operator defect leakage rate ($DLR$) and verification latency buffer ($VLBR$). An entity failing HSRI Pillar 5 fails NIST Measure 2.5 criteria for human-in-the-loop oversight. |
| **ISO/IEC 42001:2023 (AI Management System)** | **Clause A.6.2 (Human Oversight)** & **A.8.4 (Third-Party Model Risk)**: Controls ensuring that delegated decision thresholds do not exceed human audit capability. | HSRI provides the quantitative threshold audit: if model decision velocity exceeds operator cognitive parseability ($HPI < 50\%$), delegation authority must be revoked under Control A.6.2. |

---

### Pillar 6: Civilizational Decoupling Half-Life ($T_{\text{half}}$)

$$T_{\text{half}} = \min(T_{\text{power}}, T_{\text{finance}}, T_{\text{logistics}}, T_{\text{telecom}})$$

| Regulatory Framework | Specific Clause / Control | Compliance Interpretation & HSRI Diagnostic |
|---|---|---|
| **EU NIS 2 Directive (Directive 2022/2555)** | **Article 21 (Cybersecurity Risk-Management Measures)**: Essential entities must maintain business continuity, crisis response, and supply chain security for cloud services. | HSRI operationalizes the quantitative requirement for Article 21: essential entities must prove a verified decoupling half-life of $T_{\text{half}} \ge 72.0\text{ hours}$ without dependency on single-provider cloud or foreign API infrastructure. |
| **CISA Cross-Sector Cybersecurity Performance Goals (CPGs 1.0.1)** | **Goal 2.A (Asset Inventory & Manual Workarounds)**: Critical infrastructure operators must maintain and practice manual fallback procedures for critical OT/SCADA functions. | HSRI’s Civilizational Decoupling Drill (`scripts/decoupling_simulator.py`) directly tests CPG Goal 2.A compliance across Power, Finance, and Telecom under zero-notice digital asset revocation. |
| **US Presidential Policy Directive 21 (PPD-21)** | **Critical Infrastructure Security & Resilience**: Mandate to identify dependencies and cascading cross-sector disruptions. | HSRI’s Leontief cross-sector matrix ($S_{\text{civ}} = \min(P, F, L, T)$) provides the formal mathematical dependency model specified in PPD-21. |

---

### Precursor Telemetry & Cognitive Oversight Richter Scale (CORS 1.0–10.0)

| Regulatory Framework | Specific Clause / Control | Compliance Interpretation & HSRI Diagnostic |
|---|---|---|
| **US Executive Order 14110 (Safe, Secure, and Trustworthy AI)** | **Section 4.2 (Reporting Dual-Use Models)**: Mandatory notification for models exceeding compute or autonomous agentic thresholds. | CORS establishes the empirical threshold for agentic proliferation: CORS $\ge 7.0$ indicates that autonomous agent action velocity has decoupled from auditable paper trails ($HPTG > 50\%$). |
| **UK AI Safety Institute (AISI) Frontier Evaluation Standard** | **Autonomous Agent Capability Benchmarks**: Assessing recursive modification and cyber-offense capabilities. | HSRI Stream 1 (Autonomy Seismometer) tracks the exact metrics required by AISI: SWE-bench harness self-modification rates and autonomous API credential acquisition. |

---

### Reinsurance Underwriting: Sovereign Risk Factor ($\Phi$) & ECDL

$$\Phi = 1.0 + 1.50 \cdot \max(0, V_{\text{ASI}}) - 0.70 \cdot \min\left(1.0, \frac{T_{\text{half}}}{336}\right)$$

| Regulatory Framework | Specific Clause / Control | Compliance Interpretation & HSRI Diagnostic |
|---|---|---|
| **EU Solvency II Directive (Directive 2009/138/EC)** | **Articles 101 & 105 (Solvency Capital Requirement — Operational & Catastrophe Risk)**: 99.5% Value-at-Risk ($VaR_{99.5\%}$) over 1-year horizon. | HSRI formalizes systemic cyber-reinsurance reserves: catastrophic autonomous decoupling follows Fréchet extreme-value distributions where Solvency II capital charges scale directly with $\sqrt{\Phi}$. |
| **NAIC Risk-Based Capital (RBC) for P&C Insurers** | **Catastrophe Risk Charge (Rcat)**: Capital reserving for non-modeled multi-line catastrophic events. | HSRI provides the quantitative loss severity baseline for systemic cloud outage: Expected Civilizational Decoupling Loss ($ECDL$). |
| **Lloyd's Market Association (LMA) Clauses** | **LMA5583A (Cyber Loss Absolute Exclusion)**: Exclusion of systemic state-backed or non-localized cyber perils. | HSRI’s `Clause L2-DEC-01` provides the positive underwriting warranty allowing syndicates to re-enter the critical infrastructure market with calibrated decoupling thresholds. |

---

## 3. Implementation Checklist for Enterprise & Regulatory Compliance Officers

To leverage HSRI within an existing governance audit, compliance teams should execute the following 4-step sequence:
1. **Audit Verification Latency (Article 14 Compliance)**: Use `hsri_engine.core.calculate_wedge_diagnostics()` to compute operational VSR. If $\text{VSR} < 0.20$, document supplementary manual review gates to satisfy Article 14.
2. **Execute Tabletop Decoupling Drill (NIS 2 / CPG 2.A Compliance)**: Run `scripts/decoupling_simulator.py` across corporate SCADA and payment channels to verify that $T_{\text{half}} \ge 72\text{h}$.
3. **Calibrate Treaty Reserves (Solvency II Compliance)**: Input corporate exposed asset values into `scripts/reinsurance_actuarial_engine.py` to calculate Solvency Capital Requirements (SCR).
4. **Deploy Precursor Sentinel**: Subscribe to `/v1/telemetry/precursors` to receive programmatic alerts when frontier models cross critical supervisory tripwires.
