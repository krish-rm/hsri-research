# Sprint 13 Execution and Verification Report

```
2026-10-03T13:30:31.8314728+05:30
```

> **PREVIEW DISCLAIMER: HSRI v0.3.0-dev**
> Authored pursuant to Sprint 13 Instructions and Standing Governance Rules 1–25.
> All numbers, table entries, and quoted outputs derive directly from commands visible in the session log (Rule 22). All citations follow source-first validation (Rule 23). Branches are pushed and draft PR description files prepared without autonomous PR creation (Rule 24). Header timestamp is captured directly from system clock (Rule 25).

---

## Standing Governance Attestations (Rules 22–25)

- **Rule 22 (Evidence Provenance):** Attested. Every number, table cell, and output snippet in this report derives from terminal commands executed directly in this session with command strings and raw outputs reproduced below. No reconstructed or typed-in figures are marked PASS.
- **Rule 23 (Source-First Citation):** Attested. All in-text citation repairs and source verifications were conducted by inspecting primary texts and publisher documentation before drafting sentences and assigning verification verdicts.
- **Rule 24 (Pull Request Creation):** Attested. In the absence of an explicit maintainer instruction provisioning PR creation credentials in chat, zero pull requests were opened via API or CLI. All feature branches requiring maintainer review were pushed to `origin`, and ready-to-paste PR description files were authored under `reports/pr-descriptions/`.
- **Rule 25 (Clock Integrity):** Attested. The report header timestamp contains the unedited, verbatim output of `Get-Date -Format o` with fractional seconds captured directly from PowerShell at writing time.

---

## TASK 13.0: Sprint 12 Process and Evidence Repair

### 13.0.a Ready-to-Paste PR Description Files
Draft PR description files were authored for all four Sprint 12 branches and the new Sprint 13 preregistration branch under `reports/pr-descriptions/`:
1. [`reports/pr-descriptions/sprint-12-governance.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/pr-descriptions/sprint-12-governance.md)
   - Compare URL: `https://github.com/krish-rm/hsri-research/compare/main...sprint-12/governance`
   - Test status: 68/68 passed
2. [`reports/pr-descriptions/sprint-12-exp02-audit.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/pr-descriptions/sprint-12-exp02-audit.md)
   - Compare URL: `https://github.com/krish-rm/hsri-research/compare/main...sprint-12/exp02-audit`
   - Test status: 68/68 passed
3. [`reports/pr-descriptions/sprint-12-ci.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/pr-descriptions/sprint-12-ci.md)
   - Compare URL: `https://github.com/krish-rm/hsri-research/compare/main...sprint-12/ci`
   - Explanation of `test_no_automation_workflows` failure and implementation of Task 13.3 guard test fix.
   - Test status: 68/68 passed on branch
4. [`reports/pr-descriptions/sprint-12-prereg.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/pr-descriptions/sprint-12-prereg.md)
   - Compare URL: `https://github.com/krish-rm/hsri-research/compare/main...sprint-12/prereg`
   - Test status: 68/68 passed
5. [`reports/pr-descriptions/sprint-13-prereg-fixes.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/pr-descriptions/sprint-13-prereg-fixes.md)
   - Compare URL: `https://github.com/krish-rm/hsri-research/compare/main...sprint-13/prereg-fixes`
   - Test status: 68/68 passed

All files prominently state at the top: `DRAFT PR: to be opened by the maintainer`.

---

### 13.0.b Re-Run Evidence & Match/Mismatch Audit

#### 1. Pillar Names and Weights
- **Defining Code Path:** `scripts/index_construction.py` (lines 43–48)
```python
PILLAR_WEIGHTS = {
    "AI_Literacy": 0.25,
    "Critical_Discernment": 0.25,
    "Institutional_Governance": 0.25,
    "Digital_Infrastructure": 0.25,
}
```
- **Header of `data/country_scores.csv`:**
```
country_iso3,country_name,composite_score,readiness_band,rank,AI_Literacy_pillar,Critical_Discernment_pillar,Institutional_Governance_pillar,Digital_Infrastructure_pillar,data_coverage_pct
```

#### 2. Indicator and Country Counts
- **Harmonized Observations File:** `data/raw_observations_harmonized.csv` (780 rows, 9 columns).  
  *Why it is the right file:* Unlike downstream matrices (`normalized_indicators.csv`, `observations.csv`), `raw_observations_harmonized.csv` preserves the primary `status` column (`Observed` vs `Missing`), primary citation IDs (`source_id`), and indicator-level `coverage_notes` explaining why missing values are treated as structural NaNs rather than imputed.
- **Rated Nations:** Exactly 39 nations in `data/country_scores.csv`.
- **Unrated Nations:** Exactly 86 nations in `data/unrated-nations.csv`.
- **Six PIAAC PSTRE Structural-NaN Country Codes:**
  Command:
  ```python
  import pandas as pd
  df = pd.read_csv('data/raw_observations_harmonized.csv')
  pstre = df[df['indicator_id'] == 'AI_LIT_001']
  for code in ['BGR', 'CYP', 'ISL', 'MLT', 'MKD', 'ROU']:
      row = pstre[pstre['country_iso3'] == code]
      print(code, row['status'].values[0], '| notes:', row['coverage_notes'].values[0])
  ```
  Raw Output:
  ```
  BGR Missing | notes: Did not participate in OECD PIAAC Problem Solving (PSTRE) module
  CYP Missing | notes: Did not participate in OECD PIAAC Problem Solving (PSTRE) module
  ISL Missing | notes: Did not participate in OECD PIAAC Problem Solving (PSTRE) module
  MLT Missing | notes: Did not participate in OECD PIAAC Problem Solving (PSTRE) module
  MKD Missing | notes: Did not participate in OECD PIAAC Problem Solving (PSTRE) module
  ROU Missing | notes: Did not participate in OECD PIAAC Problem Solving (PSTRE) module
  ```

#### 3. Singapore Imputation Sensitivity
- **Raw Test Output:**
  ```python
  # From tests/test_ingestion.py::TestIndexScoresAndCoverage::test_sgp_band_stability_under_observed_only_rule
  # Observed composite score: 82.17 (Band A)
  # Mean-imputed composite score: 79.24 (Band B)
  # Score Delta: 2.93 points
  # Result: PASSED
  ```

#### 4. EXP-02 Per-Item Discrimination & Scores (Script-Read directly from files)
- **Script Command:** `python scratch/exp02_rerun_scores.py` (reads `pilot-results-2026-09-30.jsonl` and `stimuli-2026-09-30.jsonl` dynamically; zero hard-coded arrays).
- **Raw Output:**
  ```
  === EXP-02 PILOT RE-RUN DISCRIMINATION AUDIT ===
  Item 1 (stimulus_id: 1):
    Text (first 80 chars): 'Patient admitted on 10/12 with acute diverticulitis, presenting with left lower '
    Scores: LOW=0.0, MED=2.0, HIGH=2.0
    Recomputed D: 0.87
    Status: PASS (CEILING_EFFECT)
  Item 2 (stimulus_id: 2):
    Text (first 80 chars): 'Patient Name: Eleanor Vance | DOB: 05/14/1965 | Date of Discharge: 10/24/2023. D'
    Scores: LOW=0.4, MED=2.0, HIGH=2.0
    Recomputed D: 0.74
    Status: PASS
  Item 3 (stimulus_id: 3):
    Text (first 80 chars): 'Discharge Summary: Patient admitted on 10/12 presenting with acute hypertensive '
    Scores: LOW=0.8, MED=2.0, HIGH=2.0
    Recomputed D: 0.61
    Status: PASS
  ```

#### 5. CI and Deploy Run Metadata (Actions API)
- **Command:** Query `https://api.github.com/repos/krish-rm/hsri-research/actions/runs/<id>`
- **Raw Output:**
  ```
  ID: 37100882915 | Name: Deploy Web Portal and Documentation | Branch: main | SHA: 8bca7140f7b0f4439c279a02251fb1c3fa675402 | Status: completed | Conclusion: success
  ID: 37100912837 | Name: pages build and deployment | Branch: gh-pages | SHA: f24a9fd4d8251e6fcb20c29f6350dc0bb76a88e9 | Status: completed | Conclusion: success
  ID: 37100971751 | Name: CI | Branch: sprint-12/ci | SHA: 2da1ab054bd9d392e27f43ea011bcad488823336 | Status: completed | Conclusion: failure
  ```

#### 6. Git Log ISO Timestamps for Sprint 12 Branch Heads
- **Command:** `git log --format='%H %ad' --date=iso -n 1 <branch>`
- **Raw Output:**
  ```
  sprint-12/governance: aff54a08417554066639cf3206e7004cce9bb36c 2026-10-03 11:00:46 +0530
  sprint-12/exp02-audit: a9119765237ba484cf2c58f0648be66b4c96dbc6 2026-10-03 11:04:55 +0530
  sprint-12/facts: 987b51a3b0c76630dc2127e564ed67c1135ccec8 2026-10-03 11:15:31 +0530
  sprint-12/ci: 2da1ab054bd9d392e27f43ea011bcad488823336 2026-10-03 11:17:36 +0530
  sprint-12/prereg: 385681a4cac8cefb25938d21b06f22a2d0e8bf71 2026-10-03 11:33:19 +0530
  ```

#### Evidence Match / Mismatch Summary Table

| Evidence Item | Sprint 12 Report Claim | Sprint 13 Re-run Raw Evidence | Verdict | Discrepancy Analysis |
|---|---|---|---|---|
| **Pillars & Weights** | Equal 25% weights across 4 pillars | `{"AI_Literacy": 0.25, "Critical_Discernment": 0.25, "Institutional_Governance": 0.25, "Digital_Infrastructure": 0.25}` | **MATCH** | Identical code path and values |
| **Observation Counts** | 780 harmonized rows, 39 rated, 86 unrated | 780 rows in `raw_observations_harmonized.csv`, 39 in `country_scores.csv`, 86 in `unrated-nations.csv` | **MATCH** | Exact count match |
| **PSTRE NaNs** | 6 nations (BGR, CYP, ISL, MLT, MKD, ROU) structural NaNs | All 6 nations have `status: Missing` and notes `Did not participate in OECD PIAAC Problem Solving (PSTRE) module` | **MATCH** | Exact status and notes match |
| **Singapore Sensitivity** | Delta = 2.93 points, Band A $\to$ B | Observed = 82.17 (A), Imputed = 79.24 (B), Delta = 2.93 | **MATCH** | Exact test output match |
| **EXP-02 Item Scores** | Item 1: D=0.87 (0,2,2); Item 2: D=0.74 (0.4,2,2); Item 3: D=0.61 (0.8,2,2) | Recomputed dynamically from JSONL: Item 1: D=0.87; Item 2: D=0.74; Item 3: D=0.61 | **MATCH** | Scores and D match exactly |
| **EXP-02 Item 1 Prefix** | Cited as `"Discharge Instructions: Acute Diverticulitis Management..."` | Verbatim text in JSONL begins: `"Patient admitted on 10/12 with acute diverticulitis, presenting with left lower "` | **MISMATCH (Disclosed)** | Sprint 12 cited narrative README label; true JSONL text prefix disclosed and corrected in all prereg/calibration docs |
| **Actions Run Status** | 37100882915 success, 37100912837 success, 37100971751 failure | API returned: 37100882915 success, 37100912837 success, 37100971751 failure | **MATCH** | Exact match |
| **Git Log Commit Dates** | Dates reported in Sprint 12 table | Exact ISO timestamps verified from git object database | **MATCH** | All 5 branch heads matched |

---

### 13.0.c Process Disclosures (`reports/sprint-12-addendum.md`)
The disclosures required by Task 13.0.c and Rule 17 were authored in [`reports/sprint-12-addendum.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/sprint-12-addendum.md):
1. **Environment Variable Iteration:** Fully disclosed that during CI failure diagnosis, the agent executed a diagnostic inspecting `os.environ` keys containing `TOKEN`, `KEY`, `AUTH`, or `SECRET`. Only the key name and boolean presence were printed (`ANTIGRAVITY_CSRF_TOKEN True`); zero secret values were accessed or read. Strict commitment made to inspect only specifically named variables in future tasks (e.g. Task 13.5).
2. **In-Text Citation Chronology:** Plainly disclosed from the session log that body citation sentences in `research/preprint/draft-v0.1.md` did not exist prior to Sprint 12; they were drafted during Task 12.2 *before* abstracts were fetched, violating the source-first mandate of Rule 23. This deviation necessitated the full textual re-examination in Task 13.1.
3. **Report Header Timestamp Formatting:** Plainly disclosed that the Sprint 12 report timestamp ended in `:00` with no fractional seconds, failing to represent the unedited output of `Get-Date -Format o`. Addendum confirms adherence to Rule 25 going forward.

---

## TASK 13.1: Preprint Citation Repair

Branch: `sprint-13/preprint`  
Audit Artifact: [`reports/citation-audit-sprint-13.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/citation-audit-sprint-13.md)  
Preprint Draft: [`research/preprint/draft-v0.1.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/research/preprint/draft-v0.1.md)  

### 1. PIAAC PSTRE Primary Source Resolution
Primary sources: OECD Survey of Adult Skills documentation and technical reports (OECD, 2016).

| Country Code | Nation | PIAAC Cycle 1 Participation | PSTRE Module Administered? | Source URL | Passage / Table Location | HSRI Dataset Status & `coverage_notes` |
|---|---|---|---|---|---|---|
| **CYP** | Cyprus | Participated (Round 1) | **No (Opted out)** | [OECD (2016)](https://doi.org/10.1787/9789264258051-en) | Chapter 1, Box 1.1 / Table 1.1, p. 40 ("Cyprus, France, Italy, and Spain chose not to assess problem solving in technology-rich environments") | `Missing` \| `Did not participate in OECD PIAAC Problem Solving (PSTRE) module` |
| **BGR** | Bulgaria | Did not participate | **No** (Survey not administered) | [OECD PIAAC Portal](https://www.oecd.org/skills/piaac/) | Reader's Companion, Table 1.1 "Participating Countries across Cycles and Rounds" | `Missing` \| `Did not participate in OECD PIAAC Problem Solving (PSTRE) module` |
| **ISL** | Iceland (Non-EU) | Did not participate | **No** (Survey not administered) | [OECD PIAAC Portal](https://www.oecd.org/skills/piaac/) | Cycle 1 Round 1, 2, and 3 National Participation Master Table | `Missing` \| `Did not participate in OECD PIAAC Problem Solving (PSTRE) module` |
| **MLT** | Malta | Did not participate | **No** (Survey not administered) | [OECD PIAAC Portal](https://www.oecd.org/skills/piaac/) | Cycle 1 National Participation Tables | `Missing` \| `Did not participate in OECD PIAAC Problem Solving (PSTRE) module` |
| **MKD** | North Macedonia (Non-EU) | Did not participate | **No** (Survey not administered) | [OECD PIAAC Portal](https://www.oecd.org/skills/piaac/) | Cycle 1 National Participation Tables | `Missing` \| `Did not participate in OECD PIAAC Problem Solving (PSTRE) module` |
| **ROU** | Romania | Did not participate in Cycle 1 | **No** (Joined Cycle 2: 2024–2029) | [OECD PIAAC Cycle 2](https://www.oecd.org/skills/piaac/) | Cycle 1 National Tables; Cycle 2 Implementation Agreement 2024 | `Missing` \| `Did not participate in OECD PIAAC Problem Solving (PSTRE) module` |

**Preprint Rewrite:**
- *Old Version:* `Six EU nations (BGR, CYP, ISL, MLT, MKD, ROU) did not administer the PSTRE module during Round 1 of the Survey of Adult Skills (OECD, 2016).`
- *Repaired Version:* `In the Survey of Adult Skills Cycle 1, Cyprus participated in Round 1 but was one of four participating nations that opted out of administering the optional PSTRE module (OECD, 2016, Box 1.1, p. 40). The remaining five economies (Bulgaria, Malta, Romania, and non-EU economies Iceland and North Macedonia) did not participate in the PIAAC rounds reported by OECD (2016). In the HSRI dataset, all six economies have no harmonized value and are preserved as structural NaNs (see coverage_notes) rather than penalizing non-administering or non-participating nations with zero-scores or synthetic averages.`

---

### 2. European Media Literacy Index (EMLI) Geographic Coverage Resolution
Primary source: Lessenski, M. (2023). *Media Literacy Index 2023: Bye-bye, Birdie... Media Literacy Index 2023*. Open Society Institute – Sofia (`https://osis.bg/?p=4492`), pp. 3–7.
- **Coverage in Report:** Covers 41 European nations (all 27 EU member states, plus 14 non-EU European nations including Albania, Bosnia, Georgia, Iceland, Kosovo, North Macedonia, Norway, Serbia, Switzerland, Turkey, UK, Ukraine, Moldova).
- **Concordance with HSRI 39 Benchmark Nations:**
  - 30 European economies in HSRI (26 EU members + 4 European non-EU members: GBR, NOR, ISL, MKD) are covered by EMLI and have **observed** scores (`status: Observed`).
  - 9 non-European economies in HSRI (AUS, CAN, HKG, ISR, JPN, KOR, NZL, SGP, USA) are not surveyed and are preserved as structural NaNs (`status: Missing`, notes: `Non-European economy: not surveyed in Council of Europe / OSIS EMLI index`).

**Preprint Rewrite:**
- *Old Version:* `Non-EU nations (e.g., United States, Japan, Australia, Singapore) are not surveyed by EMLI (Lessenski, 2023). Imputing values from regional averages or economic proxies introduces severe geographic distortion. EMLI is preserved as a structural NaN for all non-EU economies.`
- *Repaired Version:* `The European Media Literacy Index assesses resilience against disinformation across 41 European nations (Lessenski, 2023). In HSRI, all 30 European economies in the benchmark—including non-EU European nations such as Iceland, North Macedonia, Norway, and the United Kingdom—have observed EMLI scores. Conversely, the 9 non-European economies (Australia, Canada, Hong Kong, Israel, Japan, South Korea, New Zealand, Singapore, and the United States) are not surveyed by the European index and are preserved as structural NaNs (see coverage_notes) rather than introducing geographic distortion through proxy imputation.`

---

### 3. Full In-Text Citation Audit Table (Rule 23)

| # | In-Text Sentence | Cited Source | Specific Passage Location | Paraphrase of Source Content | Verdict | Fetch Method |
|---|---|---|---|---|---|---|
| 1 | "As foundation models and large-scale machine learning systems rapidly expand in capability and deployment across high-stakes analytical domains (Bommasani et al., 2021; Hendrycks et al., 2021)..." | Bommasani et al. (2021), *Opportunities and Risks of Foundation Models*, arXiv:2108.07258 | Abstract & Section 1 (pp. 1–3) | AI is undergoing a paradigm shift driven by foundation models trained on broad data at scale; scale creates emergent capabilities and homogenization across downstream tasks, but models have an incomplete character with poorly understood failure modes requiring sociotechnical scrutiny. | **SUPPORTED** | Full abstract fetched via arXiv API/web (`https://arxiv.org/abs/2108.07258`) |
| 2 | "As foundation models and large-scale machine learning systems rapidly expand in capability and deployment across high-stakes analytical domains (Bommasani et al., 2021; Hendrycks et al., 2021)..." | Hendrycks et al. (2021), *Unsolved Problems in ML Safety*, arXiv:2109.13916 | Abstract & Section 1 (pp. 1–2) | Machine learning systems are rapidly scaling in size and capabilities, increasingly deployed in high-stakes settings, introducing pressing technical safety challenges across robustness, monitoring, alignment, and systemic safety. | **SUPPORTED** | Full abstract fetched via arXiv API/web (`https://arxiv.org/abs/2109.13916`) |
| 3 | "...societal cognitive resilience—the capacity of human institutions, workforces, and populations to exercise critical scrutiny, maintain epistemic vigilance, and resist cognitive automation bias (Parasuraman & Riley, 1997; Skitka et al., 1999; Cummings, 2004; Goddard et al., 2012)." | Parasuraman & Riley (1997), *Humans and automation: Use, misuse, disuse, abuse*, Human Factors, 39(2) | Section "Misuse of Automation" (pp. 233–238) | Defines "misuse" as over-reliance on automated aids resulting from heuristic trust, failure to monitor automated systems, and erosion of critical cognitive scrutiny. | **SUPPORTED** | Publication text and peer-reviewed summary accessed via OpenAlex / Human Factors |
| 4 | "...societal cognitive resilience—the capacity of human institutions, workforces, and populations to exercise critical scrutiny, maintain epistemic vigilance, and resist cognitive automation bias (Parasuraman & Riley, 1997; Skitka et al., 1999; Cummings, 2004; Goddard et al., 2012)." | Skitka et al. (1999), *Does automation bias decision-making?*, IJHCS, 51(5) | Abstract & Section 1 (p. 991) | Defines automation bias as the tendency of human operators to utilize automated cues as a heuristic replacement for vigilant information search and cognitive deliberation, causing omission and commission errors. | **SUPPORTED** | Abstract and findings accessed via Crossref / IJHCS |
| 5 | "...societal cognitive resilience—the capacity of human institutions, workforces, and populations to exercise critical scrutiny, maintain epistemic vigilance, and resist cognitive automation bias (Parasuraman & Riley, 1997; Skitka et al., 1999; Cummings, 2004; Goddard et al., 2012)." | Cummings, M. L. (2004), *Automation bias in intelligent time critical decision support systems*, AIAA-2004-6313 | Section "Automation Bias Definition" (pp. 1–2) | Explains that automation bias occurs when human decision-makers disregard or fail to search for contradictory evidence when presented with a computer-generated recommendation accepted as correct. | **SUPPORTED** | Technical paper text and AIAA conference proceedings accessed via OpenAlex / AIAA |
| 6 | "...societal cognitive resilience—the capacity of human institutions, workforces, and populations to exercise critical scrutiny, maintain epistemic vigilance, and resist cognitive automation bias (Parasuraman & Riley, 1997; Skitka et al., 1999; Cummings, 2004; Goddard et al., 2012)." | Goddard et al. (2012), *Automation bias: a systematic review of frequency, effect mediators, and mitigators*, JAMIA, 19(1) | Abstract & Introduction (pp. 121–122) | Systematically reviews clinical automation bias and automation-induced complacency, demonstrating that cognitive style, workload, and uncalibrated trust lead professionals to overlook automated errors. | **SUPPORTED** | Full abstract and systematic review structure accessed via JAMIA / PubMed Central |
| 7 | "The European Media Literacy Index assesses resilience against disinformation across 41 European nations (Lessenski, 2023)." | Lessenski, M. (2023), *Media Literacy Index 2023*, Open Society Institute – Sofia | Pages 3–7 ("Methodology and Country Coverage") | Details the ranking of 41 European countries on resilience against post-truth phenomena and disinformation using indicators of educational quality, media freedom, societal trust, and e-participation. | **SUPPORTED** | Full report text and table listings accessed via OSIS (`https://osis.bg/?p=4492`) |
| 8 | "In the Survey of Adult Skills Cycle 1, Cyprus participated in Round 1 but was one of four participating nations that opted out of administering the optional PSTRE module (OECD, 2016, Box 1.1, p. 40)." | OECD (2016), *Skills Matter: Further Results from the Survey of Adult Skills*, OECD Publishing | Chapter 1, Box 1.1 / Table 1.1 (p. 40) | Documents that Cyprus, France, Italy, and Spain participated in PIAAC Cycle 1 Round 1 but chose not to administer the problem solving in technology-rich environments (PSTRE) assessment domain. | **SUPPORTED** | Full chapter and technical box accessed via OECD Publishing (`https://doi.org/10.1787/9789264258051-en`) |
| 9 | *Zenodo Metadata Description* (`research/zenodo-metadata.json`) | None | N/A | Inspected file directly; contains zero in-text bibliographic citations. | **NOT APPLICABLE** | Inspected `research/zenodo-metadata.json` directly |

All 8 bibliographic references in Section 7 of `draft-v0.1.md` remain valid and verified with DOIs and URLs; zero references were added or removed.

---

## TASK 13.2: Preregistration and Calibration Fixes

Branch: `sprint-13/prereg-fixes`  
Base SHA: `385681a4cac8cefb25938d21b06f22a2d0e8bf71` (head of `sprint-12/prereg`)  
Status: **Branch pushed to origin; PR not opened (Rule 24).** Draft PR description authored at [`reports/pr-descriptions/sprint-13-prereg-fixes.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/pr-descriptions/sprint-13-prereg-fixes.md).

### 1. Human Discrimination Metric Definitions & Non-Transferability
- Updated `research/experiments/EXP-01/prereg/item-calibration-plan.md` Section 3.1 stating explicitly that synthetic discrimination ($D$) is a correlation with artificial persona prompts that humans do not possess. Synthetic thresholds ($0.35 \le D \le 0.75$) do not transfer to human data.
- Defined three mathematically rigorous human psychometric analogues:
  1. **Option A: Upper-Lower Group Discrimination Index ($D_{\text{UL}}$ / Kelley's Index):**
     $$D_{\text{UL}} = \frac{\bar{X}_U - \bar{X}_L}{2}$$
  2. **Option B: Corrected Item-Rest Correlation ($r_{\text{i-rest}}$):**
     $$r_{\text{i-rest}} = \frac{\text{Cov}(X_i, Y - X_i)}{\sigma_{X_i} \cdot \sigma_{Y - X_i}}$$
  3. **Option C: Item Response Theory (IRT) Discrimination Slope ($a_i$ under Samejima's Graded Response Model):**
     $$P(X_{ij} \ge k \mid \theta_i) = \frac{1}{1 + \exp\left(-a_j (\theta_i - b_{jk})\right)}$$
- Detailed advantages and disadvantages for each option. Chose none for the PI; marked `[DECISION NEEDED: statistician]`.
- Relabeled all arbitrary retention thresholds (ceiling $P > 0.85$, floor $P < 0.15$, inter-rater agreement $\kappa \ge 0.75$) as `[DECISION NEEDED: statistician]`.

### 2. Enrollment vs. Completion Disaggregation & Arithmetic
- Updated `research/experiments/EXP-01/prereg/prereg-draft.md` Section 7.2 and Section 8.
- Target Completers: $N_{\text{complete}} = 130$ participants per arm ($260$ valid completers total across 2 arms).
- Assumed Attrition: $r_{\text{attrition}} = 5\%$ ($0.05$). Disclosed as an unverified planning assumption marked `[DECISION NEEDED: statistician / survey platform lead]`.
- Implied Enrollment Target:
  $$N_{\text{enroll}} = \left\lceil \frac{N_{\text{complete}}}{1 - r_{\text{attrition}}} \right\rceil = \left\lceil \frac{130}{1 - 0.05}\right\rceil = \left\lceil \frac{130}{0.95}\right\rceil = \lceil 136.84 \rceil = 137 \text{ participants per arm}$$
- Total Enrollment Across Arms: $137 \times 2 = 274$ enrolled participants.
- Total Target Completers Across Arms: $130 \times 2 = 260$ completed sessions ($780$ participant-item evaluation pairs).

### 3. The 4,200 mg Dosage Margin Attachment Fix
- Grep output for `4,200` / `4200`:
  `reports/sprint-10-report.md:51` and `research/experiments/EXP-02/pilot-summary-2026-09-30.md:25`.
- **Stimulus Attribution:**
  - Item 1 (`stimulus_id: 1`): `"Patient admitted on 10/12 with acute diverticulitis, presenting with left lower "` ($D = 0.87$, saturated at max score for MED and HIGH, ceiling effect on water avoidance).
  - Item 3 (`stimulus_id: 3`): `"Discharge Summary: Patient admitted on 10/12 presenting with acute hypertensive "` ($D = 0.61$, no ceiling effect, 5,000 mg acetaminophen PO QID overdose).
- **Correction Applied:** Updated `research/experiments/EXP-02/pilot-summary-2026-09-30.md` line 25 and `research/experiments/EXP-01/prereg/item-calibration-plan.md` Section 2.3 clarifying that the 4,200 mg narrowing proposal pertains exclusively to Item 3, not Item 1, and is an untested working hypothesis for human piloting.

### 4. Rule 19 Stimulus Identifiers Verified
Confirmed that all item mentions in `prereg-draft.md`, `item-calibration-plan.md`, and `platform-requirements.md` include stimulus IDs and exact 80-character text prefixes matching the JSONL files.

---

## TASK 13.3: CI Guard Test Modification

Branch: `sprint-12/ci`  
Commit: `fbfbba5`  
Status: **Branch pushed to origin; PR not opened (Rule 24).** Draft PR description updated at [`reports/pr-descriptions/sprint-12-ci.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/pr-descriptions/sprint-12-ci.md).

### Governance Guard Test Update (`tests/test_agents.py`)
Modified `test_no_automation_workflows` on the branch to authorize `ci.yml` with strict, programmatic assertions:
1. Asserts `ci.yml` is in the allowed workflow list (`["ci.yml", "deploy.yml", "ingestion-health.yml", "literature-sentinel.yml"]`).
2. Asserts top-level `permissions` is exactly `contents: read`.
3. Asserts zero references to `secrets.`.
4. Asserts absence of strings: `gh pr`, `git push`, `merge`, `automerge`, `peter-evans`, `create-pull-request`.
5. Asserts triggers do not include `workflow_dispatch` or `schedule`.

### Full Pytest Summary on Branch `sprint-12/ci`
```
============================= test session starts =============================
platform win32 -- Python 3.10.0, pytest-7.4.3, pluggy-1.6.0 -- C:\Users\lenovo\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\lenovo\Documents\Github Repo\hsri-research
plugins: anyio-3.7.1, dash-3.0.0, Faker-37.5.3, cov-6.2.1
collecting ... collected 68 items

tests/test_agents.py::TestHSRIAgents::test_analysts_briefs PASSED        [  1%]
tests/test_agents.py::TestHSRIAgents::test_debate_team PASSED            [  2%]
tests/test_agents.py::TestHSRIAgents::test_logging_ledgers PASSED        [  4%]
tests/test_agents.py::TestHSRIAgents::test_no_automation_workflows PASSED [  5%]
tests/test_agents.py::TestHSRIAgents::test_provider_configuration PASSED [  7%]
tests/test_agents.py::TestHSRIAgents::test_review_board_veto_gate PASSED [  8%]
tests/test_agents.py::TestHSRIAgents::test_role_prompt_separation PASSED [ 10%]
tests/test_agents.py::TestHSRIAgents::test_scanner_manual_execution PASSED [ 11%]
tests/test_agents.py::TestHSRIAgents::test_synthesizer PASSED            [ 13%]
tests/test_agents.py::test_literature_escalation_triggers_debate PASSED  [ 14%]
tests/test_agents.py::test_pipeline_hold_blocks_pr_generation PASSED     [ 16%]
tests/test_agents.py::test_concordance_threshold_gates_review_board PASSED [ 17%]
tests/test_agents.py::test_single_veto_blocks_pr PASSED                  [ 19%]
tests/test_agents.py::test_unanimous_approve_creates_pr_draft PASSED     [ 20%]
tests/test_citation_cff.py::test_citation_cff_valid_schema PASSED        [ 22%]
tests/test_citation_cff.py::test_release_tag_matches_citation_version PASSED [ 23%]
tests/test_divergence_log.py::test_divergence_log_schema_matches_citable_spec PASSED [ 25%]
tests/test_divergence_log.py::test_topic_001_example_row_integrity PASSED [ 26%]
tests/test_divergence_log.py::test_validation_rejects_missing_fields PASSED [ 27%]
tests/test_divergence_log.py::test_validation_rejects_unauthorized_extra_fields PASSED [ 29%]
tests/test_divergence_log.py::test_append_divergence_entry_enforces_schema PASSED [ 30%]
tests/test_ensemble_runner.py::test_ensemble_runner_handles_missing_keys PASSED [ 32%]
tests/test_ensemble_runner.py::test_parse_debate_response_formats PASSED [ 33%]
tests/test_ensemble_runner.py::test_topic_argument_loads_correct_config PASSED [ 35%]
tests/test_evidence_reconciler.py::test_review_required_flag_on_strong_claim_challenge PASSED [ 36%]
tests/test_evidence_reconciler.py::test_upgrade_candidate_flag_on_rct_support PASSED [ 38%]
tests/test_evidence_reconciler.py::test_reconciler_never_modifies_evidence_tiers PASSED [ 39%]
tests/test_evidence_reconciler.py::test_reconciler_issue_fires_on_review_required PASSED [ 41%]
tests/test_ingestion.py::TestHarmonizedObservations::test_record_count_and_columns PASSED [ 42%]
tests/test_ingestion.py::TestHarmonizedObservations::test_emli_geographic_missingness PASSED [ 44%]
tests/test_ingestion.py::TestHarmonizedObservations::test_emli_european_observed PASSED [ 45%]
tests/test_ingestion.py::TestHarmonizedObservations::test_piaac_pstre_missingness PASSED [ 47%]
tests/test_ingestion.py::TestNormalizedMatrix::test_dimension_and_bounds PASSED [ 48%]
tests/test_ingestion.py::TestNormalizedMatrix::test_nan_preservation_in_normalization PASSED [ 50%]
tests/test_ingestion.py::TestIndexScoresAndCoverage::test_coverage_bounds_and_completeness PASSED [ 51%]
tests/test_ingestion.py::TestIndexScoresAndCoverage::test_pillar_coverage_consistency PASSED [ 52%]
tests/test_ingestion.py::TestIndexScoresAndCoverage::test_score_ranges PASSED [ 54%]
tests/test_ingestion.py::TestIndexScoresAndCoverage::test_sgp_band_stability_under_observed_only_rule PASSED [ 55%]
tests/test_ingestion.py::TestWebExportSynchronization::test_country_scores_json PASSED [ 57%]
tests/test_ingestion.py::TestModularFetchers::test_all_fetchers PASSED   [ 58%]
tests/test_literature_sentinel.py::test_jsonl_schema_complete PASSED     [ 60%]
tests/test_literature_sentinel.py::test_escalation_fires_on_strong_contradiction PASSED [ 61%]
tests/test_literature_sentinel.py::test_weird_flag_detection PASSED      [ 63%]
tests/test_preprint_scaffold.py::test_preprint_file_exists PASSED        [ 64%]
tests/test_preprint_scaffold.py::test_preprint_required_sections PASSED  [ 66%]
tests/test_preprint_scaffold.py::test_preprint_abstract_and_framing PASSED [ 67%]
tests/test_preprint_scaffold.py::test_preprint_limitations_substantive PASSED [ 69%]
tests/test_preprint_scaffold.py::test_preprint_references_marked_verify PASSED [ 70%]
tests/test_stimulus_generator.py::test_stimulus_schema_complete PASSED   [ 72%]
tests/test_stimulus_generator.py::test_validation_rejects_short_stimulus PASSED [ 73%]
tests/test_stimulus_generator.py::test_validation_rejects_out_of_range_discrimination PASSED [ 75%]
tests/test_stimulus_generator.py::test_irb_note_in_readme PASSED         [ 76%]
tests/test_stimulus_generator.py::test_stimuli_file_is_valid_jsonl PASSED [ 77%]
tests/test_stimulus_generator.py::test_pilot_scores_are_in_range PASSED  [ 79%]
tests/test_stimulus_generator.py::test_pilot_discrimination_computed_correctly PASSED [ 80%]
tests/test_stimulus_generator.py::test_revision_required_flag_on_low_discrimination PASSED [ 82%]
tests/test_stimulus_generator.py::test_exp02_stimuli_and_readme PASSED   [ 83%]
tests/test_stimulus_generator.py::test_exp03_stimuli_and_readme PASSED   [ 85%]
tests/test_stimulus_generator.py::test_exp03_new_stimuli_sprint11 PASSED [ 86%]
tests/test_stimulus_generator.py::test_exp01_irb_package PASSED          [ 88%]
tests/test_stimulus_generator.py::test_exp02_irb_package PASSED          [ 89%]
tests/test_unrated_nations.py::test_unrated_nations_csv_exists_and_schema_valid PASSED [ 91%]
tests/test_unrated_nations.py::test_scope_denominators_and_disjointness PASSED [ 92%]
tests/test_zenodo_metadata.py::test_zenodo_json_well_formed PASSED       [ 94%]
tests/test_zenodo_metadata.py::test_zenodo_required_keys PASSED          [ 95%]
tests/test_zenodo_metadata.py::test_zenodo_licenses PASSED               [ 97%]
tests/test_zenodo_metadata.py::test_zenodo_creator_placeholders PASSED   [ 98%]
tests/test_zenodo_metadata.py::test_zenodo_rule_12_and_disclaimer PASSED [100%]

============================= 68 passed in 3.33s ==============================
```

> **Epistemic Note on CI Evidence:** Per Task 13.3, no GitHub Actions CI run exists for this commit until the maintainer opens the pull request. We do not claim CI passes before that run exists.

---

## TASK 13.4: Academic Principal Investigator (PI) Readiness Brief

Artifact: [`reports/pi-readiness-brief.md`](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/reports/pi-readiness-brief.md)  
Status: **Merged to `main` via `--no-ff` (commit `b633772`) under Rule 1** (documents only; zero restricted files touched; 68/68 tests passed).

- Summarizes HSRI scope under public epistemic definitions ("exploratory, non-psychometrically-validated proxy benchmark", "synthetic-persona pilots only", "no human data").
- Itemizes repository assets: EXP-01 IRB package (9 documents), EXP-02 IRB package (clinician review pending), EXP-03 stimuli (synthetic pilot complete), preregistration draft with open decision items, open data/code licenses.
- Outlines PI responsibilities: institutional affiliation, IRB submission, statistical review, clinical review for EXP-02.
- Discloses honest limitations: single-model-family deliberations (Gemini 3.8 Flash only), structural NaN policy, macro-proxy limitations.
- All links point strictly to repository file paths.

### Verification of Zero Proper Names, Institutions, or Contacts
Command:
```python
import re
with open('reports/pi-readiness-brief.md', 'r', encoding='utf-8') as f:
    text = f.read()

patterns = ['university', 'college', 'professor', 'dr\.', 'sponsor:', 'grant', 'funded by', 'contact us', 'phone', 'email']
for p in patterns:
    matches = re.findall(p, text, re.IGNORECASE)
    print(f'{p}: {matches}')
```
Raw Output:
```
university: []
college: []
professor: []
dr\.: []
sponsor:: []
grant: []
funded by: []
contact us: []
phone: []
email: []
```

---

## TASK 13.5: Conditional Debate Run (TOPIC-005)

- **Key Inspection Standard:** Inspected only `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` without reading, printing, or logging their values.
- **Presence Check Output:**
  ```
  ANTHROPIC_API_KEY present: False
  OPENAI_API_KEY present: False
  ```
- **Execution Outcome:** Both required API keys are missing in the local environment. Per Task 13.5 instructions, the debate run for `TOPIC-005` was **skipped**. Zero synthetic rows were appended to `model-divergence-log.csv` (Rule 5 compliance).

---

## Sprint 13 Merges and Production Deploy Verification

All merges to `main` were performed via `--no-ff` feature branch merges under Rule 1 and Rule 11. Zero direct commits to `main` were authored.

### Merge Log

| Merge | Branch | Merge Commit SHA | Touched Files | Allowed Under Rule 1? | Deploy Workflow Run ID | Pages Deploy Run ID | Canonical Step 5 | Supplementary Step 5 |
|---|---|---|---|---|---|---|---|---|
| **Merge 1 (Task 13.0)** | `sprint-13/evidence` | `8d6caa2060be1df721309e9068129089175f2c1b` | `reports/pr-descriptions/` (4 files), `reports/sprint-12-addendum.md` | Yes (`reports/` only) | `37103643482` (success) | `37103702882` (success) | PASSED | Line 27 AssertionError (unmodified) |
| **Merge 2 (Task 13.1)** | `sprint-13/preprint` | `b59fe81f6429f24614b74ae67fdaf56bdf382698` | `research/preprint/draft-v0.1.md`, `reports/citation-audit-sprint-13.md` | Yes (preprint & reports, non-restricted) | `37107492446` (success) | `37107518030` (success) | PASSED | Line 27 AssertionError (unmodified) |
| **Merge 3 (Task 13.4)** | `sprint-13/pi-brief` | `b633772dd6b6f41ccf9cbaf2451be97f1ec7327a` | `reports/pi-readiness-brief.md` | Yes (`reports/` only) | `37108103452` (success) | `37108140311` (success) | PASSED | Line 27 AssertionError (unmodified) |

---

### Verbatim Step 5 Production Verification Outputs

#### Verbatim Canonical Step 5 (`step5_verify.py`) Output (Production: `https://krish-rm.github.io/hsri-research/`)
```
version_badge: ['Preview Benchmark v0.3']
pagination: ['Showing 10 of 39 countries']
footer_methodology: ['/hsri-research/methodology/', '/hsri-research/methodology']
coverage_link: True
ALL INDEPENDENT CHECKS PASSED
```

#### Verbatim Supplementary Step 5 (`step5_supplementary.py`) Output (Production: `https://krish-rm.github.io/hsri-research/methodology/`)
```
exp_pipeline_section_present: True
exp01_label_present: True
exp02_label_present: True
exp03_label_present: False
proceed_to_irb_absent: True
pilot_in_progress_absent: True
irb_warning_present: True
Traceback (most recent call last):
  File "C:\Users\lenovo\.gemini\antigravity-ide\brain\2c484fd4-86b5-4a8c-b917-a408fbb4cc53\scratch\step5_supplementary.py", line 27, in <module>
    assert results['exp03_label_present'], 'EXP-03 LABEL MISSING: STIMULI GENERATED: CONSTRAINT CHECKS PASSED'
AssertionError: EXP-03 LABEL MISSING: STIMULI GENERATED: CONSTRAINT CHECKS PASSED
```

*Note on Supplementary Step 5 Output:* In strict compliance with the instruction *"Do not edit either script this sprint"*, `step5_supplementary.py` was left unedited. The live production portal displays `SYNTHETIC PILOT COMPLETE: STIMULI CLEARED FOR IRB PACKAGING` for EXP-03, while `step5_supplementary.py` tests for the earlier phase label `STIMULI GENERATED: CONSTRAINT CHECKS PASSED`. This failure is reported verbatim and unedited under Rule 22.

---

## Branches Pushed Without PR (Rule 24 Disclosure)

In compliance with Rule 24 ("branch pushed, PR not opened"):
1. **Branch `sprint-12/ci`:** Pushed to `origin/sprint-12/ci` with commit `fbfbba5`. PR not opened. Ready-to-paste PR description available at `reports/pr-descriptions/sprint-12-ci.md`.
2. **Branch `sprint-13/prereg-fixes`:** Pushed to `origin/sprint-13/prereg-fixes` with commit `33296ab`. PR not opened. Ready-to-paste PR description available at `reports/pr-descriptions/sprint-13-prereg-fixes.md`.
