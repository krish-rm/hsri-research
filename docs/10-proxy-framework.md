# 10. Proxy Framework for HSRI-Index v0.1

This document outlines the country-level proxy indicators mapping to the HSRI sub-components, following the repository's evidence standards and acknowledging current measurement limitations.

---

## Executive Summary

The HSRI-Proxy v0.1 is built from existing global indicators that map onto HSRI sub-components. It is **not** a measurement of the HSRI construct itself (which requires behavioral experiments), but a transitional framework to highlight data gaps and inform future research priorities.

**Key Limitations:**
- No country-level measure of the core behavioral construct (Tier 3: AI-Interaction Behavioral Interface)
- Proxy indicators capture enabling environments rather than demonstrated readiness
- Cross-cultural measurement invariance not yet established
- All indicators are indirect proxies requiring careful interpretation

---

## 1. HSRI Sub-Components to Proxy Mapping

### 1.1 AI Literacy & Skills (Enabling Environment)

| Candidate Proxy | Retention | Validity | Rationale | Coverage |
|----------------|-----------|----------|-----------|----------|
| **OECD PIAAC Adaptive Problem Solving** | Retained | High | Direct measure of cognitive skills in technology-rich environments | 39 countries |
| **PISA Digital Reading Literacy** | Retained | High | Validated digital literacy assessment for youth | 81 countries |
| **LinkedIn Global Skills Gap Index** | Context | Medium | Reflects real-world AI skill demand/supply but vendor-derived | 50+ countries |
| **Tertiary STEM Enrollment** | Context | Medium | Proxy for technical workforce development | 190+ countries |
| **ITU Digital Skills Index** | Context | Low | Broad coverage but limited AI-specific validation | 180+ countries |

**Dispositions:**
- **Core indicators**: PIAAC and PISA (empirically validated, direct relevance)
- **Context indicators**: LinkedIn, STEM, ITU (supplementary, broader coverage)
- **Not measurable**: Behavioral AI interaction skills at country level

---

### 1.2 Calibrated Trust / Verification Behavior (Core Behavioral Evidence)

| Candidate Proxy | Retention | Validity | Rationale | Coverage |
|----------------|-----------|----------|-----------|----------|
| **KPMG-Melbourne AI Trust Study** | Context | High | Direct measure of trust vs concern balance | 32 countries |
| **Ipsos AI Monitor** | Context | High | Regular tracking with behavioral validation | 28+ countries |
| **Pew Research AI Attitudes** | Context | Medium | Large samples but limited behavioral components | 46+ countries |
| **Edelman Trust Barometer AI** | Context | Medium | Focuses on institutional trust | 28+ countries |
| **Lloyd's Foundation World Risk Poll** | Rejected | Low | General risk attitudes, not AI-specific | 142+ countries |

**Critical Note: **No proxy adequately measures the core behavioral construct of **calibrated trust** - actual verification behavior when interacting with AI systems. All available measures are self-reported attitudes, which the repository's evidence audit shows poorly predict actual reliance behavior (Lee & See, 2004).

---

### 1.3 Metacognition / Independent Judgment (Core Behavioral Evidence)

| Candidate Proxy | Retention | Validity | Rationale | Coverage |
|----------------|-----------|----------|-----------|----------|
| **PISA Reading Fact vs Opinion** | Retained | Medium | Valid measure of epistemic discernment | 81 countries |
| **European Media Literacy Index** | Retained | Medium | Direct measure of critical evaluation skills | 39 European countries |
| **Reuters Institute Digital News Report** | Context | Low | Measures news behavior, not specifically AI | 46+ countries |
| **MediaWise Digital Literacy** | Rejected | Low | General digital literacy not AI-specific | US-focused |

**Dispositions:**
- Retained indicators measure general epistemic skills that partially contribute to AI discernment
- **Key Gap**: No measure of confident-wrong AI detection specifically

---

### 1.4 Decision Agency (Institutional Safeguards)

| Candidate Proxy | Retention | Validity | Rationale | Coverage |
|----------------|-----------|----------|-----------|----------|
| **Worldwide Governance Indicators (RL/VA)** | Retained | High | Validated measure of institutional oversight | 215+ countries |
| **V-Dem Democracy Indices** | Retained | High | Comprehensive measure of institutional constraints | 202+ countries |
| **Freedom House Freedom in the World** | Retained | Medium | Long-standing measure of democratic constraints | 195+ countries |
| **OECD AI Policy Observatory** | Retained | High | Direct measure of AI-specific governance | OECD+ countries |
| **Stanford AI Index Policy Section** | Retained | Medium | Comprehensive policy tracking | Global with focus on G20 |

**Note**: These measure institutional frameworks, not individual decision agency, but provide context for individual behavioral expression.

---

### 1.5 Attentional Control / Wellbeing (Context Only)

| Candidate Proxy | Retention | Validity | Rationale | Coverage |
|----------------|-----------|----------|-----------|----------|
| **Daily Screen Time Average** | Context | Low | Indirect proxy for attentional demands | 46+ countries |
| **WHO Mental Health Prevalence** | Context | Medium | Mental health affects attentional capacity | 194+ countries |
| **HBSC Adolescent Wellbeing** | Rejected | Low | Measures general wellbeing not attention | 45+ countries |

**Disposition**: All classified as context-only due to weak validity as attentional control measures.

---

### 1.6 Value Clarity (Theoretical Dimension)

| Candidate Proxy | Retention | Validity | Rationale | Coverage |
|----------------|-----------|----------|-----------|----------|
| **World Values Survey** | Rejected | Low | Measures static values not dynamic clarity | 100+ countries |
| **EVS Values Importance** | Rejected | Low | Self-reported values not operational clarity | 47 countries |
| **European Social Survey Values** | Rejected | Low | Static value measures not metacognitive clarity | 36 countries |

**Disposition**: **Not measurable at country level** with existing data per repository assessment.

---

## 2. Additional Layer: Enabling Environment

This layer captures contextual factors that influence AI readiness but are not direct HSRI sub-components:

| Indicator | Validity | Coverage | Rationale |
|-----------|----------|----------|-----------|
| **Oxford Insights Gov AI Readiness** | High | 181 countries | Government AI strategy benchmark |
| **IMF AI Preparedness Index** | High | 125 countries | IMF's official AI preparedness measure |
| **ITU Development Index** | High | 180+ countries | Connectivity foundation |
| **World Bank Digital Adoption** | Medium | 120+ countries | General digital adoption proxy |
| **WEF Tech Adoption** | Medium | 148 countries | Industry-focused adoption |

---

## 3. Behavioral Evidence Layer: Empty/Awaiting Data

Per repository requirements, the core HSRI construct (behavioral measurement under AI interaction) cannot be operationalized at country level currently:

- **Confident-wrong AI detection**: No country-level behavioral data
- **Cognitive forcing function performance**: No cross-country measures
- **Override accuracy and calibration**: No validated proxies
- **Resistance to sycophantic framing**: No country-level indicators

**Status**: Displayed as empty layer on public site with pointer to docs/05-measurement-and-experiments.md

---

## 4. Coverage Analysis

### 4.1 By Sub-component
| Sub-component | Core Indicators | Context Indicators | Coverage (Countries) |
|---------------|-----------------|---------------------|---------------------|
| AI Literacy | 2 | 3 | 39-190 |
| Calibrated Trust | 0 | 4 | 28-46 |
| Metacognition | 2 | 1 | 39-81 |
| Decision Agency | 5 | 0 | 195-215 |
| Attentional Control | 0 | 2 | 46-194 |
| Value Clarity | 0 | 0 | 0 |

### 4.2 By Geographic Region
| Region | AI Literacy | Calibrated Trust | Metacognition | Decision Agency | Attentional | Overall Coverage |
|--------|--------------|------------------|---------------|----------------|-------------|------------------|
| North America | High | High | High | High | Medium | High |
| Europe | High | High | High | High | High | High |
| East Asia | Medium | Medium | Medium | High | Medium | Medium |
| Latin America | Low | Low | Medium | Medium | Medium | Low |
| Africa | Low | Low | Low | Low | Low | Low |
| Oceania | Medium | Low | Medium | High | Medium | Medium |

---

## 5. Indicator Quality Ratings

### 5.1 High Validity
- PIAAC Adaptive Problem Solving
- PISA Digital Reading Literacy
- WGI Rule of Law/Voice & Accountability
- V-Dem Democracy Indices
- Oxford Insights AI Readiness
- IMF AI Preparedness Index

### 5.2 Medium Validity
- LinkedIn Skills Gap (vendor bias)
- Tertiary STEM (indirect measure)
- Pew AI Attitudes (attitudinal only)
- WHO Mental Health (correlational only)
- ITU Digital Skills (broad scope)

### 5.3 Low Validity
- All wellbeing measures
- General media literacy (not AI-specific)
- WVS/EVS value measures

---

## 6. Recommendations for Data Collection

### 6.1 Priority 1: Behavioral Proxy Development
- Develop international attitudinal surveys with behavioral scenario questions
- Partner with global survey organizations (Gallup, WVS, Ipsos)
- Focus on override behavior and verification scenarios

### 6.2 Priority 2: AI-Specific Literacy Measures
- Expand PISA to include AI-specific literacy items
- Develop UNESCO AI literacy assessment protocols
- Create workforce readiness surveys

### 6.3 Priority 3: Institutional Governance Tracking
- Expand OECD AI Policy Observatory coverage
- Create standardized AI governance assessment metrics
- Track implementation of AI audit requirements

---

## 7. Ethical Considerations

### 7.1 Responsibility Laundering Risk
All proxy indicators must be accompanied by clear disclaimers that:
- Individual readiness cannot substitute for AI safety and alignment
- Institutional indicators do not measure individual capability
- Low scores should not justify paternalistic restrictions

### 7.2 Cultural Bias
- Western-educated populations may over-index on epistemic individualism
- Collectivist cultures may demonstrate agency through consensus, not individual override
- Require cross-cultural validation before any normative interpretations

---

## 8. Data Gaps Summary

### 8.1 Critical Gaps
1. **Behavioral data**: No country-level measures of AI interaction behavior
2. **Cross-cultural**: Limited non-Western validation of psychometric constructs
3. **Longitudinal**: No trend data on adaptation to AI capability growth
4. **Sectoral**: Limited data on organizational vs individual readiness

### 8.2 Measurement Challenges
1. **Aggregation**: Individual-level measures cannot be meaningfully averaged to country level
2. **Invariance**: No established measurement equivalence across cultures
3. **Specificity**: General cognitive measures may not predict AI-specific behavior

---

This framework provides a transitional path toward the full HSRI construct while maintaining scientific honesty about current limitations.