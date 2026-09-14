# 3. Construct Redundancy Audit

A central vulnerability of newly proposed psychological indices is **construct proliferation** (also known as the "jangle fallacy")&mdash;attaching a novel label to an existing, well-validated psychological attribute without demonstrating empirical distinctiveness or incremental predictive validity. This section conducts a rigorous redundancy audit of every candidate HSRI component against established cognitive science, human factors, and human-computer interaction literatures.

---

## 3.1 Systematic Construct Redundancy Audit

Every candidate dimension proposed in early HSRI concept drafts was audited against established instruments and psychometric literature:

| Proposed Dimension | Existing Psychological / Cognitive Construct | Validated Instrument or Experimental Paradigm | Redundancy Verdict | Methodological Disposition for HSRI |
|---|---|---|---|---|
| **Attentional Control** | Executive Attention / Sustained Attention | Attention Network Test (ANT); Sustained Attention to Response Task (SART) | **Redundant Construct** | Reusable measurement paradigm; evaluate distraction resistance under AI-driven alerts. |
| **Metacognition / Self-Knowledge** | Metacognitive Monitoring / Sensitivity | Confidence-accuracy calibration curves; type-2 signal detection ($meta\text{-}d'$) (Fleming & Lau, 2014) | **Redundant Construct** | Direct methodological reuse; calibrate subjective confidence against actual AI output accuracy. |
| **Cognitive Flexibility** | Task-Switching / Set-Shifting | Wisconsin Card Sorting Test (WCST); Trail Making Test B | **Redundant Construct** | Exclude from core; retain as baseline cognitive covariate. |
| **Epistemic Humility** | Intellectual Humility | Comprehensive Intellectual Humility Scale (Leary et al., 2017) | **Redundant Construct** | Direct instrument reuse; captures willingness to revise beliefs when confronted with valid AI evidence. |
| **Cognitive Reflection** | Reflective vs. Intuitive Cognitive Processing | Cognitive Reflection Test (CRT; Frederick, 2005) | **Redundant Construct** | Useful baseline, but high test-retest familiarity contamination limits repeated longitudinal deployment. |
| **Uncertainty Tolerance** | Intolerance of Uncertainty | Intolerance of Uncertainty Scale (IUS-12; Carleton et al., 2007) | **Redundant Construct** | Direct instrument reuse; predicts premature surrender of judgment under ambiguous AI recommendations. |
| **Decision Agency** | Autonomous Motivation / Locus of Control | Basic Psychological Need Satisfaction Scale (Deci & Ryan); Rotter's I-E Scale | **Redundant General Construct** | General construct is mature, but behavioral delegation and override under AI advice is an active empirical gap. |
| **Value Clarity & Meaning** | Goal Contents / Meaning in Life | Meaning in Life Questionnaire (MLQ); Portrait Values Questionnaire (Schwartz) | **Redundant Construct** | Mature general psychometrics; causal connection to AI optimization remains theoretical. |
| **AI Literacy** | Multi-dimensional AI Competency | AI Literacy Questionnaire (Ng et al., 2024); UNESCO Frameworks (2024); OECD/EC Framework (2026) | **Fully Redundant Field** | **Import wholesale.** Active, mature field; HSRI should not reinvent AI literacy measurement. |
| **Resistance to Automation Bias / Calibrated Trust** | Automation Bias; Appropriate Trust & Reliance | Errors of omission/commission paradigm (Mosier & Skitka, 1996); trust calibration models (Lee & See, 2004) | **Fully Redundant Construct** | Mature in classical automation (aviation, medicine); **extension to generative/agentic AI is the genuine research frontier**. |

**Audit Conclusion:** Virtually all proposed sub-constructs are redundant with established, peer-reviewed psychology. The sole defensible, non-redundant scientific contribution lies in measuring how these established cognitive substrates function **jointly under interaction with adaptive, persuasive, generative AI counterparts**—an interactive environment that static psychometric batteries (such as standard Stroop or card-sorting tasks) do not replicate.
{: .evidence-strong }

---

## 3.2 Human-AI Interaction: Automation Bias, Reliance, and Calibrated Trust

The foundational literature on automated decision aids spans three decades of empirical validation:

### 3.2.1 Automation Stages and Levels
Parasuraman, Sheridan, and Wickens (2000) formalized a four-stage framework of human interaction with automation: (1) information acquisition, (2) information analysis, (3) decision selection, and (4) action implementation. Their empirical synthesis established that automating the *decision selection* stage produces the greatest degree of human operator complacency, cognitive disengagement, and loss of situational awareness.
{: .evidence-strong }

### 3.2.2 Errors of Omission and Commission
Mosier and Skitka (1996) demonstrated that automation bias manifests through two distinct failure modes:
- **Errors of Omission:** Operators fail to notice system hazards or critical anomalies because automated monitoring aids did not trigger an alert.
- **Errors of Commission:** Operators follow an incorrect automated recommendation even when contradictory evidence is directly available in the physical environment.
{: .evidence-strong }

### 3.2.3 Trust Calibration vs. Subjective Trust
Lee and See (2004) formalized trust calibration: trust is calibrated when an operator's subjective confidence matches the actual operational capability of the automated system. They identified two failure states:
- **Overtrust (Misuse):** Operator trust exceeds system capability, leading to uncritical reliance and automation bias.
- **Undertrust (Disuse):** System capability exceeds operator trust, resulting in reflexive rejection of valid advice (algorithm aversion).
{: .evidence-strong }

A 2025 PRISMA-compliant systematic review synthesizing 35 peer-reviewed studies (2015–2025) confirmed that automation bias manifests across modern AI-driven enterprise workflows, proving that the phenomenon extends into contemporary machine-learning environments rather than being restricted to legacy aviation systems.
{: .evidence-preliminary }

---

## 3.3 The Failure of Explanations and the Role of Cognitive Forcing Functions

A critical design insight from recent empirical human-AI interaction research concerns the limitations of model transparency and explainable AI (XAI):

### 3.3.1 Transparency Can Increase Over-Reliance
Bansal et al. (2021, CHI) demonstrated that providing AI explanations does not reliably improve complementary human-AI team performance. In multiple experimental conditions, adding local feature-importance explanations *increased* operator over-reliance on incorrect machine recommendations, because fluent, plausible explanations created an illusion of system competence.
{: .evidence-strong }

### 3.3.2 Cognitive Forcing Functions Reduce Automation Bias
Buçinca, Malaya, and Gajos (2021, CSCW) evaluated interventions to mitigate over-reliance. They demonstrated that while passive explanation interfaces failed, **cognitive forcing functions**—design interventions that compel deliberate, active analytical judgment before an AI recommendation is revealed or accepted (such as requiring the user to formulate and commit to an independent hypothesis first)—statistically significantly reduced over-reliance. Furthermore, this intervention effect was moderated by individual **Need for Cognition (NFC)**: participants with higher baseline motivation for cognitive effort benefited significantly more from forced deliberation.
{: .evidence-strong }

This finding directly informs HSRI's behavioral experimental battery: static self-report cannot measure resistance to automation bias; diagnostic validity requires behavioral paradigms that test whether individuals engage deliberative verification under fluent machine prompting.
{: .evidence-strong }

---

## 3.4 Cognitive Offloading and Deskilling

Cognitive offloading—the practice of using physical actions or external artifacts to reduce cognitive demands (Risko & Gilbert, 2016)—is well-documented in human cognition. Transactive memory research has demonstrated offloading effects in search engine usage and spatial navigation via GPS systems.
{: .evidence-strong }

However, the hypothesized extension of this effect to high-order analytical synthesis, critical argumentation, and conceptual reasoning under generative AI remains an **active empirical hypothesis without robust longitudinal validation**. High-quality longitudinal studies demonstrating irreversible cognitive deskilling from LLM usage do not yet exist. In HSRI, generative deskilling must be classified as a **research gap**, not a verified finding.
{: .evidence-preliminary }

---

## 3.5 Contemplative Science: Empirical Review and Boundary Delimitation

Early conceptual drafts of HSRI proposed including meditation practice frequency as an indicator of attentional and psychological readiness. A rigorous review of the contemplative science literature demonstrates that this represents an overreach:

| Empirical Claim | Evidence Base | Effect Size & Statistical Parameters | Strength Tier | Methodological Caveats & Assessment |
|---|---|---|---|---|
| **Mindfulness improves executive attention** | Meta-analyses of Randomized Controlled Trials (RCTs) | Hedges' $g = 0.29$ for intervention studies; $g = 0.32$ comparing long-term meditators to non-meditators (Sumantry & Stewart, 2021). | **Moderate** | Effects concentrated narrowly in conflict inhibition / executive control; no general cognitive boost. |
| **Mindfulness improves working memory** | Meta-analysis of RCTs in healthy adults | Overall effect $g = 0.20$; non-significant effect on working memory capacity specifically (Yakobi, Smilek, & Danckert, 2021). | **Weak / Null** | Executive control shows modest gains, but working memory retention is not reliably altered in healthy populations. |
| **Mindfulness improves alerting / orienting networks** | Systematic reviews of attention sub-networks | Small, inconsistent effect sizes across trials (Sharpe, 2021). | **Weak** | Doctoral meta-analysis and primary experimental series yielded non-significant or null effects on alerting/orienting networks. |
| **Dose-response relationship (sessions vs. hours)** | Moderation analyses of meditation interventions | Number of formal in-class sessions moderates effect size; total accumulated intervention hours does not (Yakobi et al., 2021). | **Preliminary** | Authors note that session count may reflect participant motivation and compliance rather than neurobiological dose-response. |
| **Broader clinical vs. cognitive outcomes** | Large-scale comparative systematic review (47 RCTs, $n = 3{,}515$) | Moderate evidence for reduction of anxiety (ES = 0.38 at 8 weeks), depression (ES = 0.30), and pain (ES = 0.33); **low evidence of any effect on attention specifically** (Goyal et al., 2014, *JAMA Intern Med*). | **Moderate for Affect; Weak-to-Null for Attention** | Found no evidence that meditation outperforms active behavioral treatments (exercise, therapy); attention effects were statistically negligible. |

### Contemplative Science Conclusion
Meditation produces small, domain-specific effects on executive attention ($g \approx 0.29$), but the largest and highest-quality comparative meta-analysis (Goyal et al., 2014) identified low evidence for attentional benefits specifically—the precise substrate required for AI discernment.
{: .evidence-strong }

Therefore, **meditation practice must be classified strictly as a candidate training intervention, never as an indicator or constituent dimension of readiness**. HSRI must measure attentional control and metacognitive monitoring directly through standardized behavioral tasks (ANT, SART, calibration curves), remaining entirely agnostic to whether an individual trained those faculties through contemplative practice, athletic training, musicianship, or software engineering.
{: .evidence-theoretical }

---

## Sources on this page

- **Bansal, G., Wu, T. S., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M. T., & Weld, D. (2021).** Does the whole exceed its parts? The effect of AI explanations on complementary team performance. *Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems (CHI '21)*, Article 81, 1–16.
- **Buçinca, Z., Malaya, M. B., & Gajos, K. Z. (2021).** To trust or to think: Cognitive forcing functions can reduce overreliance on AI in AI-assisted decision-making. *Proceedings of the ACM on Human-Computer Interaction*, 5(CSCW1), Article 188, 1–21.
- **Carleton, R. N., Norton, M. P. J., & Asmundson, G. J. G. (2007).** Fearing the unknown: A short version of the Intolerance of Uncertainty Scale. *Journal of Anxiety Disorders*, 21(1), 105–117.
- **Fleming, S. M., & Lau, H. C. (2014).** How to measure metacognition. *Frontiers in Human Neuroscience*, 8, Article 443.
- **Frederick, S. (2005).** Cognitive reflection and decision making. *Journal of Economic Perspectives*, 19(4), 25–42.
- **Goyal, M., Singh, S., Sibinga, E. M. S., Gould, N. F., Rowland-Seymour, A., Sharma, R., Berger, Z., Sleicher, D., Shen模式, D. D., Han, D., Ranasinghe, P. D., Shihab, H. M., Robinson, K. A., Choi, S. W., Karitza, S., Rosman, D., & Haythornthwaite, J. A. (2014).** Meditation programs for psychological stress and well-being: A systematic review and meta-analysis. *JAMA Internal Medicine*, 174(3), 357–368.
- **Leary, M. R., Diebels, K. J., Jongman-Sereno, K. P., Maha-affey, A. L., Schrader, K. L., & Fernandez, D. (2017).** Cognitive and interpersonal features of intellectual humility. *Personality and Social Psychology Bulletin*, 43(6), 793–813.
- **Lee, J. D., & See, K. A. (2004).** Trust in automation: Designing for appropriate reliance. *Human Factors*, 46(1), 50–80.
- **Mosier, K. L., & Skitka, L. J. (1996).** Human decision makers and automated decision aids: Made for each other? In *Automation and Human Performance: Theory and Applications* (pp. 201–220).
- **Ng, D. T. K., Leung, J. K. L., Chu, S. K. W., & Qiao, M. S. (2021).** Conceptualizing AI literacy: An exploratory review. *Computers and Education: Artificial Intelligence*, 2, 100041.
- **Ng, D. T. K., Luo, W., Chan, H. M. Y., & Chu, S. K. W. (2024).** Design and validation of the AI literacy questionnaire. *British Journal of Educational Technology*, 55(3), 1082–1104.
- **OECD & European Commission. (2026).** *AI Literacy Framework for Primary and Secondary Education*. OECD Publishing.
- **Parasuraman, R., Sheridan, T. B., & Wickens, C. D. (2000).** A model for types and levels of human interaction with automation. *IEEE Transactions on Systems, Man, and Cybernetics - Part A: Systems and Humans*, 30(3), 286–297.
- **Risko, E. F., & Gilbert, S. J. (2016).** Cognitive offloading. *Trends in Cognitive Sciences*, 20(9), 676–688.
- **Sharpe, P. (2021).** *The effects of mindfulness meditation on attention regulation* (Doctoral thesis). University of Plymouth.
- **Sumantry, D., & Stewart, K. E. (2021).** Meditation, mindfulness, and attention: A meta-analysis. *Mindfulness*, 12(6), 1332–1349.
- **UNESCO. (2024).** *AI Competency Framework for Teachers* and *AI Competency Framework for Students*. United Nations Educational, Scientific and Cultural Organization.
- **Yakobi, O., Smilek, D., & Danckert, J. (2021).** The effects of mindfulness meditation on attention, executive control and working memory in healthy adults: A meta-analysis of RCTs. *Cognitive Therapy and Research*, 45(4), 543–560.
