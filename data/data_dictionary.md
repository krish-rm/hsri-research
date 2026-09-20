# HSRI-Proxy v0.1 Data Dictionary

This document defines all data structures, fields, and conventions used in the HSRI-Proxy v0.1 project.

---

## 1. Data Files Overview

| File | Purpose | Status |
|------|---------|--------|
| `indicators.csv` | Indicator framework with metadata | Complete |
| `sources.csv` | Source provenance and metadata | In Progress |
| `observations.csv` | Raw data observations | In Progress |
| `coverage-by-country.csv` | Geographic coverage matrix | Complete |

---

## 2. `indicators.csv` Structure

### Columns

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `indicator_id` | String | Unique identifier for each indicator | Lowercase with underscores |
| `name` | String | Full name of the indicator | Descriptive human-readable |
| `description` | String | Detailed description of what the indicator measures | Free text |
| `subcomponent` | String | HSRI sub-component this indicator maps to | AI_Literacy, Calibrated_Trust, etc. |
| `pillar` | String | Pillar classification | Core or Context pillar name |
| `validity_rating` | String | Research validity assessment | High, Medium, Low |
| `role` | String | Retention classification | Retained, Context-only, Rejected, Not measurable |
| `data_source` | String | Primary source publisher | OECD, UNESCO, etc. |
| `unit` | String | Measurement unit | z-score, percent, points, index, rank |
| `direction` | String | Higher values indicate | higher, lower (for inverted scales) |
| `normalization` | String | Preferred normalization method | min-max, z-score, rank |
| `coverage_notes` | String | Key coverage limitations | Free text |

### HSRI Sub-component Mapping

| Sub-component | Pillar | Description |
|---------------|--------|-------------|
| `AI_Literacy` | Core AI Literacy & Skills | Cognitive capacity for AI interaction |
| `Calibrated_Trust` | Core Critical Discernment | Trust calibration and verification behavior |
| `Metacognition` | Core Critical Discernment | Independent judgment and evaluation |
| `Decision_Agency` | Core Institutional Governance | Institutional safeguards framework |
| `Attentional_Control` | Context Wellbeing | Attentional resources management |
| `Value_Clarity` | Context Value Clarity | Metacognitive value alignment |
| `Enabling_Environment` | Context Digital Infrastructure | Technological and institutional readiness |

### Role Classifications

- **Retained**: Core indicators for pillar scores
- **Context-only**: Supplementary indicators for context only
- **Rejected**: Excluded due to poor validity
- **Not measurable**: Theoretically important but no existing measures

---

## 3. `sources.csv` Structure

### Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `source_id` | String | Unique source identifier | PIAAC_OECD |
| `publisher` | String | Source organization | OECD |
| `title` | String | Publication title | Skills for a Digital World |
| `edition` | String | Edition or version | 3rd ed. |
| `publication_date` | String | Publication date | 2023-06 |
| `url` | String | Direct link to source | https://www.oecd.org/... |
| `retrieved_at` | String | Data retrieval timestamp | 2026-09-19 |
| `license` | String | Data license type | CC BY-NC-SA 4.0 |
| `terms_notes` | String | Special terms or restrictions | "Data from International Database" |
| `method_summary` | String | Brief methodology description | "Survey of adults' skills..." |
| `sample_notes` | String | Sample size and characteristics | "39 countries, 200,000+ respondents" |
| `known_biases` | String | Documented limitations | "OECD countries overrepresented..." |
| `is_vendor_or_stakeholder` | Boolean | Private sector source | true/false |

### License Types

| License | Usage Restriction | Required Attribution |
|---------|-------------------|-------------------|
| `CC BY 4.0` | Commercial use allowed | Required |
| `CC BY-SA 4.0` | Share-alike required | Required |
| `CC BY-NC-SA 4.0` | Non-commercial only | Required |
| `Custom` | Varies by provider | Check terms |

---

## 4. `observations.csv` Structure

### Columns

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| `country_iso3` | String | ISO 3166-1 alpha-3 country code | 3 uppercase letters |
| `country_name` | String | Full country name | Official UN name |
| `indicator_id` | String | Reference to indicator table | Must match indicators.csv |
| `value` | Float | Numeric value | Can be negative for inverted scales |
| `year` | Integer | Year of observation | 1900-2027 range |
| `unit` | String | Measurement unit | Consistent with indicators.csv |
| `source_id` | String | Reference to sources table | Must match sources.csv |
| `coverage_notes` | String | Data quality notes | Free text for limitations |

### Data Constraints

- **country_iso3**: Must be valid ISO 3166-1 alpha-3 code
- **indicator_id**: Must exist in indicators.csv
- **source_id**: Must exist in sources.csv
- **year**: Must be between 1900 and current year + 1
- **value**: Must be numeric (can be negative for inverted indicators)

---

## 5. `coverage-by-country.csv` Structure

### Columns

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `country_iso3` | String | ISO country code | 3-letter code |
| `country_name` | String | Country name | Full official name |
| `*_coverage` | Integer | Number of indicators available | Count |
| `overall_coverage` | Integer | Total indicators available | 0-30 |
| `overall_status` | String | Rating eligibility | Not rated, Context-only, Partial rating |

### Status Definitions

- **Not rated**: < 5 indicators total
- **Context-only**: Only context indicators available
- **Partial rating**: Core indicators present but incomplete
- **Full rating**: Will be assigned when complete

---

## 6. Normalization Methods

### Z-score Standardization
```
z = (x - μ) / σ
```
- Suitable for assessment data
- Preserves distribution shape
- Handles outliers well

### Min-Max Scaling
```
normalized = (x - min) / (max - min)
```
- Binds values to [0, 1] range
- Good for indices and scores
- Sensitive to outliers

### Rank Transformation
```
rank = position in sorted order / total observations
```
- Reduces outlier impact
- Preserves ordinal relationships
- Good for sparse data

---

## 7. Country Code Standards

### ISO 3166-1 alpha-3
- Standard 3-letter country codes
- Used for consistent identification
- Special cases:
  - Dependencies: GBR-ENG, GBR-SCT, GBR-NIR
  - Territories: USA-GUM, USA-PR
  - Sovereign: All 193 UN members

### Naming Conventions
- Use official UN country names
- Follow ISO 3166-1 standard
- Include regional clarifiers when needed
- No political implications in naming

---

## 8. Data Quality Indicators

### Completeness
- **Full**: 100% of expected values present
- **Partial**: 50-99% of values present
- **Sparse**: 10-49% of values present
- **Missing**: < 10% of values present

### Reliability
- **Primary**: Direct measurement (surveys, assessments)
- **Secondary**: Aggregated from multiple sources
- **Proxy**: Indirect measure with theoretical basis
- **Estimated**: Statistical inference required

### Timeliness
- **Current**: Data from last 2 years
- **Recent**: Data from 2-5 years old
- **Stale**: Data > 5 years old
- **Historical**: Historical comparison only

---

## 9. Data Access and Usage

### License Compliance
- All data must be used according to source licenses
- Commercial use requires CC BY compatible licenses
- Attribution must include source and HSRI-Proxy v0.1
- Contact source publishers for special use cases

### Data Privacy
- No personally identifiable information
- Aggregate data only (individual records never published)
- Statistical disclosure control applied
- Follows GDPR and local data protection laws

### Citation Format
When using HSRI-Proxy data:
```
HSRI-Proxy v0.1 (2026). Human Superintelligence Readiness Index - Public Benchmark Website. 
Retrieved from [dataset URL] 
Indicator: [indicator_name], Source: [source_publisher], Year: [year]
```

---

## 10. Update and Maintenance

### Version Control
- All data changes documented
- Version numbers incremented for significant changes
- Change logs maintained in data/version_history.csv
- Backups preserved for audit trail

### Updates Schedule
- Annual updates when new data available
- Quarterly validation runs
- Monthly metadata reviews
- Continuous improvement of provenance tracking

---

**Last Updated**: 2026-09-19  
**Version**: v0.1-Data-Draft  
**Status**: Initial framework established, data acquisition in progress