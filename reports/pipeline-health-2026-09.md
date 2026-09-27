# HSRI Data Pipeline Health & Anomaly Audit — September 2026

**Audit Execution Timestamp:** `2026-09-27 08:44:30 UTC`  
**Repository:** `krish-rm/hsri-research`  
**Overall Action Verdict:** **`AUTO-PATCH`**

---

## 1. Institutional Fetcher Dry-Run Health Checks

| Source ID | Target Domain / Indicator Scope | Status | Diagnostic Notes |
|---|---|:---:|---|
| `WGI_WorldBank` | WDI / Governance / Digital Adoption | 🟢 Healthy | 39 harmonized records validated |
| `VDEM_Vdem` | Deliberative Democracy / Academic Freedom | 🟢 Healthy | 39 harmonized records validated |
| `ITU_DEVELOP` | ICT Infrastructure / Broadband Penetration | 🟢 Healthy | 78 harmonized records validated |
| `PISA_OECD` | PISA Science/Math / PIAAC PSTRE | 🟢 Healthy | 78 harmonized records validated |
| `UNESCO_STEM` | Tertiary STEM Enrollment / R&D | 🟢 Healthy | 39 harmonized records validated |
| `IMF_AI` | AI Preparedness Index | 🟢 Healthy | 39 harmonized records validated |
| `OXFORD_AI` | Government AI Readiness Index | 🟢 Healthy | 39 harmonized records validated |

---

## 2. Authentic Missingness Audit (Anti-Imputation Verification)

- **European Media Literacy Index (EMLI):** Verified `NaN` across all 9 non-European economies.
- **PIAAC PSTRE (Problem Solving in Tech-Rich Environments):** Verified `NaN` across all 6 non-participating nations.

> [!NOTE]
> **Status: CLEAN.** Zero forbidden imputations detected; institutional boundary conditions strictly preserved.

---

## 3. Anomaly Detection (|Δz| > 2.5)

| Country | Indicator | z-Score | Normalized Value | Classification | Action |
|---|---|---|---|---|---|
| `MKD` | `META_COG_003` | `-2.6` | `0.0303` | `GENUINE_SHIFT` | **`AUTO-PATCH`** |
| `ROU` | `META_COG_003` | `-2.73` | `0.0` | `GENUINE_SHIFT` | **`AUTO-PATCH`** |
| `MKD` | `ENAB_004` | `-2.822` | `0.0` | `GENUINE_SHIFT` | **`AUTO-PATCH`** |
| `MKD` | `ENAB_005` | `-2.554` | `0.0` | `GENUINE_SHIFT` | **`AUTO-PATCH`** |

---

## 4. Imputation Sensitivity Analysis

- **Tested Imputation Methods:** `baseline_observed_rescaled, mean_imputation, median_imputation`
- **Maximum Observed Country Score Delta:** `7.884 points`

### Band Shift Impact Under Imputation:
| Country | Baseline Band | Mean Imputation Band | Median Imputation Band | Max Delta |
|---|:---:|:---:|:---:|:---:|
| `SGP` | `A` | `B` | `B` | `2.93` |

---

## 5. Summary & Action Recommendations

- **Recommended Governance Action:** **`AUTO-PATCH`**
- **Data Update Policy:** No autonomous commit to `data/indicators.csv` or published bundles without human maintainer sign-off.
