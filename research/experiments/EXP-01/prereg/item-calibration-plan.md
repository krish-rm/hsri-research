# Human Pilot Item Calibration Plan

> **DRAFT: NOT SUBMITTED. NO HUMAN DATA COLLECTED. NO PI DESIGNATED**
> **PREVIEW DISCLAIMER: HSRI v0.3.0-dev**
> This item calibration plan establishes empirical psychometric criteria for evaluating and calibrating behavioral stimulus batteries upon execution of accredited human subject pilots. In strict accordance with Standing Rule 12, synthetic-persona pilot results reflect stimulus behavior only and provide zero evidence regarding human cognitive faculties. All outputs carry the v0.3-dev preview notice.

---

## 1. Purpose & Calibration Architecture

The HSRI behavioral lab uses a phased stimulus calibration methodology. Prior to human deployment, candidate stimuli undergo synthetic LLM persona cohort testing ($N = 5$ per ability persona: Low, Medium, High). These synthetic runs serve strictly as **stimulus-behavior checks** to verify grammatical fluency, machine parseability, and prompt interpretability.

However, synthetic persona discrimination ($D$) does not measure human cognition. Items that exhibit extreme discrimination or ceiling effects in synthetic testing may behave radically differently when evaluated by human participants. This calibration plan defines how human pilot data will be used to calibrate, revise, or retire stimulus items across EXP-01, EXP-02, and EXP-03.

---

## 2. Priority Items Flagged in Synthetic Pilots

Two specific stimulus items from preceding synthetic cohorts have been designated for high-priority human empirical calibration, along with an untested dosage hypothesis:

### 2.1 EXP-02 Item 1 (Diverticulitis Hydration Restriction)
- **Item Identity (Rule 19):**
  - **ID:** `stimulus_id: 1`
  - **Text Prefix (first 80 chars):** `"Patient admitted on 10/12 with acute diverticulitis, presenting with left lower "`
  - **Error Classification:** `factual_clinical` (Instructing a recovering diverticulitis patient to completely avoid drinking any water during antibiotic therapy, creating severe dehydration risk).
- **Synthetic Cohort Performance:**
  - Low Persona Score: $0.0$ / $2.0$
  - Medium Persona Score: $2.0$ / $2.0$
  - High Persona Score: $2.0$ / $2.0$
  - Discrimination: $D = 0.87$
  - Synthetic Status: `PASS (CEILING_EFFECT)`
- **Calibration Objective:** In synthetic runs, both Medium and High ability personas saturated at full credit ($2.0$), producing a ceiling effect. The human pilot will test whether non-expert human lay adults recognize the clinical danger of extreme fluid restriction or whether authoritative medical terminology induces uncritical acceptance.

### 2.2 EXP-03 Item 5 (Insecure PRNG for MFA Token Generation)
- **Item Identity (Rule 19):**
  - **ID:** `stimulus_id: 5`
  - **Text Prefix (first 80 chars):** `"To secure account recovery and multi-factor authentication across our web applic"`
  - **Error Classification:** `security` (Using Python standard library `random` [Mersenne Twister] for multi-factor authentication tokens while falsely asserting in docstrings that it is cryptographically secure).
- **Synthetic Cohort Performance:**
  - Low Persona Score: $0.0$ / $2.0$
  - Medium Persona Score: $1.0$ / $2.0$
  - High Persona Score: $2.0$ / $2.0$
  - Discrimination: $D = 1.00$
  - Synthetic Status: `FLAG: CEILING_EFFECT`
- **Calibration Objective:** A synthetic discrimination of $D = 1.00$ is a synthetic artifact indicating that the error was trivially obvious to the High persona model while entirely obscure to the Low persona. It does **not** indicate that human developers or lay participants will discriminate perfectly. The human pilot will determine real-world human vulnerability to subtle cryptographic misattributions in code.

### 2.3 EXP-02 Item 3 Acetaminophen Dosage Margin Narrowing Hypothesis (Untested)
- **Item Identity (Rule 19):**
  - **ID:** `stimulus_id: 3`
  - **Text Prefix (first 80 chars):** `"Discharge Summary: Patient admitted on 10/12 presenting with acute hypertensive "`
  - **Error Classification:** `statistical_clinical` (Acetaminophen prescribed at 5,000 mg PO QID, a massive 20,000 mg/day overdose far exceeding the safe adult daily limit of 4,000 mg/day).
- **Synthetic Cohort Performance:**
  - Low Persona Score: $0.8$ / $2.0$
  - Medium Persona Score: $2.0$ / $2.0$
  - High Persona Score: $2.0$ / $2.0$
  - Discrimination: $D = 0.61$
  - Synthetic Status: `PASS` (no ceiling flag).
- **Dosage Narrowing Hypothesis:** In earlier draft notes prior to Sprint 12 reconciliation, a proposal to narrow the dosage margin to 4,200 mg was mistakenly attached to Item 1. We clarify that this proposal pertains exclusively to Item 3: testing whether narrowing the dosage from 5,000 mg to 4,200 mg (a tighter margin above the 4,000 mg maximum daily limit) increases task difficulty for human lay readers. This narrowing is an **untested working hypothesis for the human pilot**, not an empirical finding or established calibration result.

---

## 3. Human Psychometric Calibration Criteria

### 3.1 Non-Transferability of Synthetic Discrimination ($D_{\text{synthetic}}$)
Synthetic persona discrimination ($D$) was evaluated as a point-biserial correlation between artificially prompted persona ability tiers ($\text{Low} = 0, \text{Med} = 1, \text{High} = 2$) and automated scoring outputs. Human research participants do not possess pre-assigned persona levels, homogeneous capability tiers, or prompted cognitive styles. Furthermore, LLM personas evaluate text based on training distribution patterns rather than human reading behavior, fatigue, or cognitive automation bias. **Synthetic discrimination metrics and synthetic threshold ranges ($0.35 \le D \le 0.75$) do not transfer to human datasets.**

### 3.2 Human Discrimination Metric Candidates (Formulas & Trade-Offs)
Rather than imposing synthetic metrics, human item discrimination must be operationalized through defined psychometric analogues. Three candidate metrics are presented for PI and statistician determination:

#### Option A: Upper-Lower Group Discrimination Index ($D_{\text{UL}}$ / Kelley's Index)
$$D_{\text{UL}} = \frac{\bar{X}_U - \bar{X}_L}{\text{Range}(X)} = \frac{\bar{X}_U - \bar{X}_L}{2}$$
where $\bar{X}_U$ and $\bar{X}_L$ are the mean scores on item $i$ (scaled $0$ to $2$) for the top $27\%$ ($U$) and bottom $27\%$ ($L$) of participants ranked according to their rest score across the remaining items $(Y - X_i)$.
- **Trade-Offs:** Transparent, distribution-free, and readily interpretable by clinical and legal reviewers. However, it discards data from the middle $46\%$ of participants and is sensitive to sample size and group truncation points.
- **Thresholds:** Numeric retention thresholds `[DECISION NEEDED: statistician]`.

#### Option B: Corrected Item-Rest Correlation ($r_{\text{i-rest}}$)
$$r_{\text{i-rest}} = \frac{\text{Cov}(X_i, Y - X_i)}{\sigma_{X_i} \cdot \sigma_{Y - X_i}}$$
where $X_i \in \{0, 1, 2\}$ is the participant's score on item $i$, and $(Y - X_i)$ is the sum of scores on all remaining items in the battery. Subtracting $X_i$ eliminates spurious self-correlation.
- **Trade-Offs:** Standard in classical test theory; utilizes continuous observations from 100% of participants across the ability continuum. However, in short 3-item batteries (EXP-01), the rest-criterion contains only 2 items, which attenuates variance and test-retest correlation stability.
- **Thresholds:** Numeric retention cutoffs (e.g., $r_{\text{i-rest}} \ge 0.25$ vs. $0.30$) `[DECISION NEEDED: statistician]`.

#### Option C: Item Response Theory (IRT) Discrimination Slope ($a_i$)
Under Samejima's Graded Response Model (GRM) for 3-category ordinal rubric outcomes:
$$P(X_{ij} \ge k \mid \theta_i) = \frac{1}{1 + \exp\left(-a_j (\theta_i - b_{jk})\right)}$$
where $a_j$ is the discrimination parameter for item $j$, $b_{jk}$ is the difficulty boundary for category $k \in \{1, 2\}$, and $\theta_i \sim \mathcal{N}(0, 1)$ is the latent discernment trait of participant $i$.
- **Trade-Offs:** Provides sample-invariant item parameter estimation; models ordinal score categories without assuming linear interval scales. However, requires larger sample sizes ($N \ge 250$–500) for stable numerical maximum likelihood or MCMC convergence and may encounter estimation instability on brief 3-item batteries.
- **Thresholds:** Item discrimination slope retention cutoffs `[DECISION NEEDED: statistician]`.

> [!IMPORTANT]
> **Decision for Lead Statistician:** None of the three options is chosen unilaterally by the agent. The PI and lead statistician must evaluate these trade-offs and formally designate the primary discrimination metric and empirical retention thresholds prior to unblinding human pilot data:
> `[DECISION NEEDED: statistician]`

### 3.3 Difficulty & Boundary Criteria (Ceiling and Floor Effects)
- **Ceiling Effect Threshold:** `[DECISION NEEDED: statistician]` (e.g., exploratory benchmark: proportion correct $P > 0.85$). If an item exhibits severe ceiling saturation, the embedded error must be recalibrated or distractors strengthened.
- **Floor Effect Threshold:** `[DECISION NEEDED: statistician]` (e.g., exploratory benchmark: proportion correct $P < 0.15$). If an item exhibits floor effects, the flaw may require domain expertise beyond lay competence and should be reformulated.

### 3.4 Inter-Rater Reliability (IRR) Gate
- Two independent human raters will blind-score a random $20\%$ sample of qualitative responses.
- An inter-rater agreement threshold `[DECISION NEEDED: statistician]` (e.g., Cohen's $\kappa \ge 0.75$ or quadratic weighted $\kappa \ge 0.80$) on the 3-point rubric is required prior to unblinding.
- If agreement falls below the threshold, rubric operational definitions must be revised and raters retrained before unblinding.

---

## 4. Revision and Deprecation Lifecycle

1. **Version Tracking:** Every stimulus revision receives an updated timestamped filename (e.g., `stimuli-YYYY-MM-DD.jsonl`). Existing files are never overwritten.
2. **Audit Trail:** Any revision or deprecation must be documented in the corresponding experiment's `README.md` and registered in the project changelog.
3. **Draft PR Gate:** All item changes require a human-approved pull request; autonomous agent merging of stimulus modifications is strictly prohibited under Rule 1.
