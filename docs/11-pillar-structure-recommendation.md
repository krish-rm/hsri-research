# Pillar Structure Recommendation for HSRI-Proxy v0.1

This document proposes the pillar structure for the HSRI-Proxy index, based on the systematic indicator mapping completed in Phase 1.

---

## 1. Recommended Pillar Structure

### 1.1 Core Pillars (Derived from HSRI Sub-components)

| Pillar | Description | Number of Indicators | Coverage Goal |
|--------|-------------|---------------------|---------------|
| **AI Literacy & Skills** | Cognitive and technical capacity to understand and work with AI | 5 (2 core + 3 context) | Minimum 3 indicators |
| **Critical Discernment** | Ability to evaluate information, distinguish fact from opinion, and think critically | 3 (2 core + 1 context) | Minimum 2 indicators |
| **Institutional Governance** | Legal and regulatory frameworks that protect human agency in AI systems | 5 (all core) | Minimum 4 indicators |
| **Digital Infrastructure** | Foundational technology infrastructure enabling AI access and adoption | 5 (all context) | Minimum 3 indicators |

### 1.2 Context Pillars (Enabling Environment)

| Pillar | Description | Number of Indicators | Purpose |
|--------|-------------|---------------------|---------|
| **Trust & Attitudes** | Public perceptions and attitudes toward AI | 4 (all context) | Contextual understanding only |
| **Wellbeing Context** | Mental health and attentional factors | 2 (all context) | Contextual understanding only |

### 1.3 Behavioral Evidence Layer

| Component | Status | Indicators | Purpose |
|-----------|--------|------------|---------|
| **AI Interaction Behavior** | Empty | 0 | Explicitly shown as awaiting research |
| **Calibrated Trust** | Proxy only | 0 (attitudinal only) | Clear limitation disclosure |

---

## 2. Pillar Weighting Strategy

### 2.1 Baseline Approach: Equal Weighting
- All core pillars receive equal weight (25% each)
- Context pillars shown separately, not included in overall score
- Transparent methodology disclosure

### 2.2 Sensitivity Analysis
- Test alternative weightings:
  - Education-focused (AI Literacy 40%, others 20% each)
  - Governance-focused (Institutional 40%, others 20% each)
  - Equal weights as baseline
- Report all results in methodology

---

## 3. Scoring Rules

### 3.1 Pillar Coverage Thresholds
- A pillar is scored only if ≥70% of its indicators are present
- For core pillars: minimum 2/3 indicators for AI Literacy & Critical Discernment, 4/5 for Institutional Governance
- Countries missing ≥2 core pillars are "Not Rated"

### 3.2 Overall Score Calculation
- Only core pillars contribute to overall score
- Equal weighting: (AI_Literacy + Critical_Discernment + Institutional_Governance + Digital_Infrastructure) / 4
- Missing pillars treated as zero in calculation (no imputation)

### 3.3 Band Definitions (Preliminary)
| Band | Score Range | Interpretation |
|------|-------------|----------------|
| Band 1 | 0.0 - 0.4 | Limited capacity |
| Band 2 | 0.4 - 0.6 | Developing capacity |
| Band 3 | 0.6 - 0.8 | Moderate capacity |
| Band 4 | 0.8 - 1.0 | Strong capacity |

*Note: Bands will be refined based on actual score distribution*

---

## 4. Indicator-Aggregation Matrix

| Pillar | Indicator ID | Weight | Direction | Normalization |
|--------|--------------|--------|-----------|---------------|
| **AI Literacy & Skills** | | | | |
| PIAAC_Adaptive | 0.5 | +1 | Min-max | z-score |
| PISA_Digital | 0.5 | +1 | Min-max | z-score |
| LinkedIn_Skills | 0.33 | +1 | Min-max | z-score |
| TERTIARY_STEM | 0.33 | +1 | Min-max | rank |
| ITU_Digital | 0.33 | +1 | Min-max | rank |
| **Critical Discernment** | | | | |
| PISA_FactOpinion | 0.67 | +1 | Min-max | z-score |
| EMLI_MediaLit | 0.33 | +1 | Min-max | z-score |
| Reuters_Misconcern | 0.33 | +1 | Min-max | reverse |
| **Institutional Governance** | | | | |
| WGI_RuleLaw | 0.2 | +1 | Min-max | z-score |
| WGI_VoiceAcc | 0.2 | +1 | Min-max | z-score |
| VDEM_Democ | 0.2 | +1 | Min-max | z-score |
| Freedom_House | 0.2 | +1 | Min-max | reverse |
| OECD_AI_Policy | 0.2 | +1 | Min-max | z-score |
| **Digital Infrastructure** | | | | |
| Oxford_AI_Ready | 0.25 | +1 | Min-max | z-score |
| IMF_AI_Prep | 0.25 | +1 | Min-max | z-score |
| ITU_Develop | 0.25 | +1 | Min-max | z-score |
| WB_Digital | 0.15 | +1 | Min-max | z-score |
| WEF_TechAdopt | 0.10 | +1 | Min-max | z-score |

---

## 5. Geographic Considerations

### 5.1 Regional Groupings
- **OECD+**: High data quality, full pillar coverage
- **BRICS**: Mixed coverage, governance focus
- **LAC**: Context-only coverage, infrastructure focus
- **SSA**: Limited coverage, institutional governance only

### 5.2 Special Cases
- **Microstates**: Separate handling due to small population
- **Conflict zones**: Mark clearly with data caveats
- **Dependencies**: Include with parent state notation

---

## 6. Ethical Safeguards

### 6.1 Responsibility Laundering Prevention
- Clear disclaimer that institutional ≠ individual readiness
- Prominent note that governance indicators do not measure individual capability
- Explicit statement that low scores do not justify restrictions on AI access

### 6.2 Avoiding Stigmatization
- Neutral band labels (no "failing/backward" language)
- Contextual explanations for low scores
- Focus on capacity building, not ranking

---

## 7. Recommended Next Steps

### 7.1 Data Acquisition Priority
1. **High**: PIAAC, PISA, WGI, V-Dem (high coverage, high validity)
2. **Medium**: Oxford Insights, IMF AI Prep, Pew AI Attitudes
3. **Low**: Wellbeing indicators (context only)

### 7.2 Quality Assurance
1. Source verification for all indicators
2. Cross-check country name harmonization
3. Test normalization methods
4. Validate scoring calculations

---

## 8. Decision Points for Human Approval

### 8.1 Pillar Structure
**Question**: Should we merge "Critical Discernment" into "AI Literacy" given limited indicators?
**Recommendation**: Keep separate to maintain theoretical alignment with HSRI framework

### 8.2 Coverage Inclusion
**Question**: Should countries with only governance indicators be included?
**Recommendation**: Include as "Governance Only" category, not in main ranking

### 8.3 Band Labels
**Question**: Should bands be descriptive (e.g., "Strong Capacity") or neutral (1-4)?
**Recommendation**: Neutral with plain language descriptors to avoid value judgment

---

This structure maintains theoretical alignment with HSRI while providing practical, implementable country-level proxy measures with clear limitations disclosed.