# 2. Existing Global Indices: Comparative Methodology and Lessons

Composite international indices offer vital methodological precedents and structural warnings for designing the Human Superintelligence Readiness Index (HSRI). International index construction has evolved through three distinct historical paradigms, with HSRI positioned provisionally within an unproven fourth.

---

## 2.1 Three Historical Paradigms of International Indices

1. **Unidimensional Economic Output (Mid-20th Century):** Dominated by Gross Domestic Product (GDP) and Gross National Product (GNP). While standardized, this paradigm was widely criticized for treating aggregate market activity as synonymous with societal welfare, ignoring distribution, externalities, and non-market capabilities.
2. **Multidimensional Human Capability (1990s):** Inaugurated by Mahbub ul-Haq and Amartya Sen through the UNDP's **Human Development Index (HDI)**. Grounded in Sen's capabilities approach, development was redefined as the expansion of substantive human freedoms and capabilities (health, education, purchasing power) rather than income alone.
3. **Deprivation, Governance, and Sustainability (2000s–Present):** Represented by the **Multidimensional Poverty Index (MPI)**, the **Social Progress Index (SPI)**, and environmental governance frameworks. These introduced non-compensatory aggregation rules, dual-cutoff identification of deprivation, and explicit measurement of institutional outcomes independent of economic growth.
4. **Cognitive and Epistemic Agency Under AI Asymmetry (Proposed 4th Paradigm):** HSRI provisionally sits here—measuring individual- and population-level cognitive discernment, calibrated trust, and preserved decisional agency under interaction with intelligent systems. However, each previous paradigm required more than a decade of contested methodological debate to achieve legitimacy; HSRI cannot assume acceptance without equivalent empirical scrutiny.
{: .evidence-theoretical }

---

## 2.2 Comparative Methodological Review

The table below examines the mathematical formulation, indicator structure, aggregation methods, and documented critiques of the primary international benchmarks:

| Index | Sponsoring Organization / Authors | Core Dimensions & Indicators | Aggregation Mathematics | Documented Methodological Criticisms |
|---|---|---|---|---|
| **Human Development Index (HDI)** | UNDP (Mahbub ul-Haq & Amartya Sen, 1990) | Health (life expectancy), Education (mean/expected years), Income (GNI per capita). | Geometric mean of normalized sub-indices: $$\text{HDI} = (I_{\text{health}} \times I_{\text{education}} \times I_{\text{income}})^{1/3}$$ | Ignores net wealth distribution, quality-of-service differences, and environmental sustainability. Companion indices (IHDI, GII, MPI) were required to address inequality and multi-deprivation. |
| **Social Progress Index (SPI)** | Social Progress Imperative (Porter, Stern, & Green, 2013–2017) | 3 dimensions (Basic Needs, Foundations of Wellbeing, Opportunity) comprising 12 components and ~50 indicators. | Component indicators combined via Principal Component Analysis (PCA); the 12 components themselves are **explicitly equal-weighted**. | Equal weighting of the 12 components assumes each contributes identically and independently to social progress—an assumption with no statistical or theoretical justification (Jitmaneeroj, 2017). Criticized for encoding Western liberal normative assumptions. |
| **World Happiness Report** | UN Sustainable Development Solutions Network (Helliwell, Layard, & Sachs) | Cantril ladder life evaluations regressed on GDP, social support, healthy life expectancy, freedom, generosity, perceptions of corruption. | Pooled Ordinary Least Squares (OLS) regression of national life evaluations against six determinant categories. | Correlational rather than causal; relies on a single-item subjective evaluation; deliberately avoids normative definitions of societal structure. |
| **Multidimensional Poverty Index (MPI)** | Oxford Poverty & Human Development Initiative (OPHI) / UNDP (Alkire & Foster, 2011) | 10 indicators across Health, Education, and Living Standards. | Non-compensatory dual-cutoff counting method: individuals are identified as poor only if deprived across a weighted threshold ($k$). | Deprivation cutoffs ($z_j$) and overall poverty threshold ($k$) are normatively selected rather than empirically derived. Weighting of indicators within dimensions remains contestable. |
| **Global Innovation Index (GII)** | WIPO / Cornell / INSEAD | 7 pillars (Institutions, Human capital, Infrastructure, Market/Business sophistication, Knowledge/Creative outputs). | Arithmetic mean of equal-weighted pillar scores. | Overlap between "input" and "output" pillars creates conceptual collinearity and risks tautological scoring. |

---

## 2.3 Documented Criticisms and Failure Modes

### 2.3.1 The Equal-Weighting Fallacy
Equal weighting is the most prevalent methodological shortcut in composite index design, yet it remains the primary target of external econometric critique. As Jitmaneeroj (2017) demonstrated regarding the Social Progress Index, equal weighting assumes that every constituent dimension exerts an identical, orthogonal contribution to the latent construct. In reality, sub-dimensions exhibit substantial collinearity and differential predictive power. For HSRI, adopting equal weighting past the initial exploratory pilot would undermine scientific credibility.
{: .evidence-strong }

### 2.3.2 Non-Compensatory vs. Compensatory Aggregation
Standard arithmetic averaging allows compensatory substitution: an exceptionally high score on one dimension fully offsets a catastrophic failure on another. In the context of human-AI interaction, this formulation is dangerous. If a decision-maker exhibits a near-total inability to detect confident machine hallucinations or an uncritical willingness to surrender oversight, high scores in general AI literacy or abstract value clarity should not mask that critical operational vulnerability. The non-compensatory, dual-cutoff framework of Alkire & Foster (2011) provides the correct psychometric precedent.
{: .evidence-theoretical }

### 2.3.3 Western Normative Bias in Universal Indices
The Social Progress Index has faced sustained criticism that its Opportunity dimension reflects predominantly Western normative ideals, systematically penalizing non-Western governance models. Because constructs like "individual autonomy," "agency," and "self-determination" are culturally sensitive, HSRI faces an even greater risk of cultural parochialism if deployed globally without rigorous measurement invariance testing.
{: .evidence-moderate }

---

## 2.4 Four Architectural Lessons for HSRI

1. **Mandatory Profile Reporting:** Never publish a single composite figure without disaggregated sub-scores. Composite point estimates obscure vital structural deficits.
2. **Provisional-to-Empirical Weighting Transition:** Equal weighting should be used strictly during exploratory pilot phases, explicitly labeled provisional, and replaced with empirically estimated regression or factor weights following validation studies.
3. **Non-Compensatory Critical-Weakness Floor:** Foundational cognitive substrates (such as attentional control and error detection) must operate as non-compensatory thresholds, capping overall readiness when a severe deficiency is detected.
4. **Pre-Registered Invariance Standards:** Follow the OECD/JRC *Handbook on Constructing Composite Indicators* (2008), pre-registering sensitivity analyses and uncertainty intervals for all aggregation and normalization parameters.

---

## Sources on this page

- **Alkire, S., & Foster, J. (2011).** Counting and multidimensional poverty measurement. *Journal of Public Economics*, 95(7–8), 476–487.
- **Greco, S., Ishizaka, A., Tasiou, M., & Torrisi, G. (2019).** On the methodological framework of composite indices: A review of the issues of weighting, aggregation, and robustness. *Social Indicators Research*, 141(1), 61–94.
- **Helliwell, J. F., Layard, R., & Sachs, J. (2018).** *World Happiness Report 2018*. Sustainable Development Solutions Network.
- **Jitmaneeroj, B. (2017).** Beyond the equal-weight framework of the Social Progress Index: A quantile regression approach. *International Journal of Social Economics*, 44(12), 2336–2350.
- **OECD & European Commission Joint Research Centre. (2008).** *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- **Porter, M. E., Stern, S., & Green, M. (2017).** *Social Progress Index 2017: Methodological Report*. Social Progress Imperative.
- **UNDP.** *Human Development Report Technical Notes*. United Nations Development Programme.
