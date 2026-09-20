# Index Construction Methodology for HSRI-Proxy v0.1

This document outlines the methodology for constructing the HSRI-Proxy index following the OECD/JRC Handbook on Composite Indicators and taking into account the repository's scientific rigor requirements.

---

## 1. Methodological Framework

### 1.1 Core Principles
- **Non-compensatory**: Weaknesses in one pillar cannot be compensated by strengths in others
- **Transparency**: All methodological choices documented and reproducible
- **Uncertainty**: Confidence intervals provided for all scores
- **Sensitivity**: Methodological variations tested and reported

### 1.2 OECD/JRC Handbook Compliance
- Theoretical justification for each component
- Statistical testing for reliability and validity
- Clear treatment of missing data
- Uncertainty quantification

---

## 2. Pillar Structure and Weighting

### 2.1 Core Pillars (Equal Weighting)
| Pillar | Description | Number of Indicators | Weight |
|--------|-------------|---------------------|--------|
| **AI Literacy & Skills** | Cognitive capacity for AI interaction | 5 | 25% |
| **Critical Discernment** | Evaluation and verification skills | 3 | 25% |
| **Institutional Governance** | Institutional safeguards framework | 5 | 25% |
| **Digital Infrastructure** | Technological readiness | 5 | 25% |

### 2.2 Context Pillars (Separate Reporting)
| Pillar | Description | Data Source |
|--------|-------------|-------------|
| **Trust & Attitudes** | Public perceptions | Survey data |
| **Wellbeing Context** | Attentional resources | Health surveys |

---

## 3. Normalization Methods

### 3.1 Normalization Strategy by Indicator Type

| Indicator Type | Method | Rationale |
|----------------|--------|-----------|
| **Assessment Data** (PIAAC, PISA) | Z-score standardization | Preserves distribution shape, handles different scales |
| **Indices** (Oxford, IMF) | Min-max scaling to [0,1] | Binds to interpretable range |
| **Ranks** | Rank transformation | Reduces outlier impact, preserves ordinal relationships |
| **Percentages/Ratios** | Min-max scaling | Natural upper bounds, intuitive interpretation |

### 3.2 Directional Alignment
- All indicators normalized so higher values = better readiness
- Inverted indicators (e.g., where lower = better) transformed using: `normalized = 1 - normalized`

---

## 4. Coverage Rules

### 4.1 Pillar Coverage Thresholds
- **Minimum coverage**: 70% of indicators per pillar required for scoring
- **Missing data**: Not imputed for headline scores
- **Partial pillars**: Countries with insufficient coverage flagged separately

### 4.2 Country Inclusion Rules
- **Full rating**: Minimum 3 core pillars with sufficient coverage
- **Partial rating**: 1-2 core pillars with sufficient coverage
- **Not rated**: No core pillars with sufficient coverage

### 4.3 Handling Missing Data
- No mean imputation for headline scores
- Multiple imputation used only for sensitivity analysis
- Coverage percentage reported transparently

---

## 5. Aggregation Methodology

### 5.1 Pillar Score Calculation
- Simple arithmetic mean of normalized indicators
- Equal weighting within pillars
- Minimum 70% coverage requirement

### 5.2 Overall Score Calculation
- Simple arithmetic mean of available core pillars
- Equal weighting across core pillars (25% each)
- No compensation for missing pillars

### 5.3 Band Classification (Preliminary)
| Band | Score Range | Interpretation | Color Code |
|------|-------------|----------------|------------|
| 1 | 0.0 - 0.4 | Limited capacity | #e74c3c |
| 2 | 0.4 - 0.6 | Developing capacity | #f39c12 |
| 3 | 0.6 - 0.8 | Moderate capacity | #3498db |
| 4 | 0.8 - 1.0 | Strong capacity | #27ae60 |

*Note: Band thresholds will be refined based on actual score distribution*

---

## 6. Uncertainty Quantification

### 6.1 Confidence Intervals
- **Bootstrap resampling**: 1000 iterations for each country score
- **Report**: Mean score ± 95% confidence interval
- **Display**: Error bars on visualizations

### 6.2 Monte Carlo Analysis
- **Parameters**: Normalization method, weighting schemes
- **Scenarios**: Equal weights, education-focused, governance-focused
- **Output**: Range of possible scores for sensitivity analysis

---

## 7. Statistical Validation

### 7.1 Reliability Testing
- **Cronbach's alpha**: Internal consistency of core pillars
- **Inter-item correlations**: Check for redundancy
- **Split-half reliability**: Consistency across indicator subsets

### 7.2 Validity Assessment
- **Convergent validity**: Correlations with existing indices
- **Discriminant validity**: Low correlations with theoretically unrelated measures
- **Construct validity**: Factor analysis to confirm structure

### 7.3 Sensitivity Analysis
- **Methodological variations**: Test different normalization and aggregation methods
- **Indicator subsets**: Remove/add indicators to test robustness
- **Weight variations**: Test different pillar weightings

---

## 8. Implementation Steps

### 8.1 Data Preparation
1. Load indicators, observations, and sources
2. Normalize each indicator using appropriate method
3. Apply directional adjustments
4. Create country-indicator matrix

### 8.2 Pillar Scoring
1. Apply coverage rules to each pillar
2. Calculate pillar scores with sufficient coverage
3. Flag countries with insufficient coverage

### 8.3 Index Construction
1. Calculate overall score from available core pillars
2. Apply country inclusion rules
3. Classify countries into bands

### 8.4 Validation
1. Run statistical reliability tests
2. Perform sensitivity analysis
3. Generate confidence intervals

---

## 9. Quality Assurance

### 9.1 Error Checking
- Validate data integrity at each step
- Check for normalization errors
- Verify coverage calculations

### 9.2 Documentation
- Record all methodological decisions
- Document version control
- Maintain reproducibility

### 9.3 Transparency
- Publish methodology and code
- Document limitations
- Report uncertainty measures

---

## 10. Ethical Considerations

### 10.1 Responsibility Laundering Prevention
- Clear disclaimer that institutional ≠ individual readiness
- Prominent note that governance indicators do not measure individual capability
- Statement that low scores do not justify restrictions on AI access

### 10.2 Avoiding Misinterpretation
- Neutral band labels without value judgments
- Contextual explanations for low scores
- Focus on capacity building, not ranking

### 10.3 Cultural Sensitivity
- Avoid Western-centric bias in interpretation
- Acknowledge cultural differences in agency expression
- Future measurement invariance testing required

---

## 11. Known Limitations

### 11.1 Measurement Limitations
- Proxy indicators may not predict actual behavioral readiness
- No validation against the core HSRI construct
- Risk of reification without experimental validation

### 11.2 Data Limitations
- Geographic bias toward OECD countries
- Static measures not tracking adaptation
- Ecological fallacy from individual to country level

### 11.3 Methodological Limitations
- No established cross-cultural measurement invariance
- Equal weighting assumes equal importance
- Missing data reduces statistical power

---

## 12. Future Improvements

### 12.1 Short-term (1-2 years)
- Expand indicator coverage with AI-specific measures
- Improve normalization methods
- Test alternative weighting schemes

### 12.2 Medium-term (3-5 years)
- Develop behavioral proxy measures
- Establish cross-cultural validation
- Implement longitudinal tracking

### 12.3 Long-term (5+ years)
- Integrate experimental validation
- Develop country-specific adjustments
- Machine learning refinement

---

**Methodology Version**: v0.1  
**Based on**: OECD/JRC Handbook on Composite Indicators  
**Repository Alignment**: HSRI scientific rigor standards  
**Last Updated**: 2026-09-19