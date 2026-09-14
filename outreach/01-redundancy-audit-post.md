# Every Substrate of "AI Readiness" Already Has a Validated Test. The Untested Part Is Whether They Interact.

When an experienced engineer or physician accepts an authoritative, syntactically polished model output that contains a critical error, standard psychometrics will usually show they have normal executive attention, intact cognitive reflection, and strong domain knowledge. Yet they still deferred. Every psychological attribute commonly proposed under labels like "AI readiness"—executive attention, metacognitive monitoring, decisional agency, value clarity, AI literacy, and calibrated trust—already has a mature, validated home in the literature. The only place a defensible, unaddressed research gap plausibly exists is whether these substrates, measured jointly under direct interaction with an AI system that matches or outperforms the person at the task in front of them, predict behavioral discernment and override accuracy in ways the standalone instruments do not.

That joint interaction hypothesis is currently untested. If it fails, any construct labeled "AI readiness" collapses into existing psychology and should be discarded as redundant.

---

### The Redundancy Audit

The central skeptical question for any proposed psychological index is whether it identifies a new construct or merely re-labels existing ones (the jangle fallacy). Auditing candidate dimensions against validated experimental paradigms shows that the underlying substrates are already accounted for:

| Candidate Dimension | Existing Validated Construct | Established Measurement Paradigm / Instrument | Empirical Redundancy Status |
|---|---|---|---|
| **Attentional Control** | Executive Attention / Conflict Inhibition | Attention Network Test (ANT; Fan et al., 2002); SART | **Redundant.** Captures distraction resistance; instrument is directly reusable. |
| **Metacognitive Accuracy** | Metacognitive Monitoring / Sensitivity | Type-2 signal detection ($meta\text{-}d'$; Fleming & Lau, 2014); calibration curves | **Redundant.** Standard method separating subjective confidence from objective discernment. |
| **Epistemic Humility** | Intellectual Humility | Comprehensive Intellectual Humility Scale (CIHS; Leary et al., 2017) | **Redundant.** Measures willingness to revise beliefs when confronted with valid evidence. |
| **Cognitive Reflection** | Reflective vs. Intuitive Processing | Cognitive Reflection Test (CRT; Frederick, 2005) | **Redundant.** Predicts heuristic override, though subject to familiarity effects. |
| **Decisional Agency** | Autonomous Motivation (Self-Determination Theory) | Need Satisfaction Scale (Deci & Ryan, 2000); Rotter's Locus of Control | **Redundant as a general trait.** Volition is distinguishable from competence; AI delegation is understudied. |
| **AI Literacy** | Technical Competency & Conceptual Knowledge | AI Literacy Questionnaire (Ng et al., 2024); UNESCO/OECD Frameworks | **Fully redundant field.** A fast-maturing literature measures this; import wholesale. |
| **Calibrated Trust** | Automation Bias / Appropriate Reliance | Reliance ratio paradigms; errors of omission/commission (Mosier & Skitka, 1996; Lee & See, 2004) | **Redundant in classical automation.** Decades of aviation and clinical studies define misuse and disuse. |

Of the candidate dimensions frequently discussed in connection with human capability under advanced AI, none represents a novel psychological faculty. Proposing an index that aggregates these separate scales into an unweighted composite produces no new explanatory power.

---

### Where a Gap Might Actually Exist

The one plausible, narrow gap is not about new substrates, but about their behavior under cognitive asymmetry.

Existing cognitive instruments present static, non-adaptive stimuli: letter strings, card-sorting rules, synthetic logic puzzles, or multiple-choice self-reports. None of these tests evaluate how a human manages epistemic vigilance against an active counter-party that generates fluent, highly persuasive, and occasionally erroneous arguments.

Classical human factors established that automation bias is real: operators routinely favor automated advice over contrary human evidence (Mosier & Skitka, 1996), and automating decision selection produces severe complacency (Parasuraman, Sheridan, & Wickens, 2000). But modern generative models differ from legacy automation in their linguistic fluency and apparent coherence.

A concrete anchor is the finding by Bansal et al. (2021) and Buçinca, Malaya, and Gajos (2021) on AI explanations. In classical decision-support systems, providing transparency or explanation is assumed to help users calibrate trust. With generative assistance, providing local explanations does not reliably reduce over-reliance; in some conditions, explanations actively increase over-reliance because fluent explanations trigger an illusion of explanatory depth.

What reliably reduced over-reliance in Buçinca et al.'s experiments was not more explanation, but **cognitive forcing functions**—interface designs compelling users to formulate and commit to their own judgment before the AI's answer was revealed. Crucially, the magnitude of this effect was moderated by the user's Need for Cognition (NFC): individuals with higher intrinsic motivation for effortful thinking benefited significantly more from forced friction.

This demonstrates that successful human-AI interaction is not simply a linear function of a person's raw cognitive ability, nor of system accuracy, nor of interface transparency. It is an interaction effect between human metacognitive disposition and task interface demands. That interaction—whether an individual retains decisional agency, detects confident error, and calibrates reliance when paired with an AI system that matches or exceeds their task performance—is the only empirical territory not already covered by standalone instruments.

---

### The Falsification Test

If this interaction hypothesis is genuine, it must be falsifiable. The claim is:

> *An integrated battery measuring behavioral discernment and override under real AI task asymmetry explains significant variance in decision quality that is not explained by a linear composite of existing standalone instruments (CRT + CIHS + ANT + AI Literacy).*

Here is the experiment that tests it:

1. **Sample:** 200–300 knowledge workers performing domain tasks (code debugging, factual synthesis, data interpretation).
2. **Baseline Predictors:** Standard Cognitive Reflection Test, Comprehensive Intellectual Humility Scale, Attention Network Test (conflict score), and the AI Literacy Questionnaire.
3. **Interactive Battery:**
   - *Task A (Confident-Wrong Detection):* 25% of AI suggestions contain subtle, critical errors framed with authoritative syntax and high expressed confidence.
   - *Task B (Forcing-Function Modulation):* Tasks completed under standard AI assistance versus forced-commitment friction interfaces.
4. **Criterion Outcome:** Objective override accuracy on deceptive model outputs and empirical reliance calibration (ratio of following correct vs. incorrect advice).
5. **Decisive Test:** Hierarchical linear regression estimating the change in explained variance:
   $$\Delta R^2 = R^2_{\text{Interactive Battery + Baseline}} - R^2_{\text{Baseline Only}}$$

**What would prove this claim wrong:**  
If $\Delta R^2 \approx 0$—that is, if variance in error detection and calibrated reliance is fully accounted for by general cognitive reflection, intellectual humility, executive attention, and technical AI literacy—then the hypothesis of an independent "AI readiness" construct is falsified.

A null result means there is no separate construct to study. Researchers should stop attempting to build specialized indices of human-AI cognitive readiness and instead rely on standard, well-normed psychological instruments alongside model-side safety evaluations. Stating this plainly in advance is necessary to prevent moving the goalposts if empirical data shows zero incremental validity.

---

### What Is the Strongest Counterargument?

For researchers working in cognitive science, HCI, or AI evaluation, what is the cleanest objection to this framing?

Specifically:
- Is there already an established behavioral instrument that directly measures discernment of confident, fluent machine hallucinations as distinct from general critical thinking? If so, pointing to it resolves the question immediately and eliminates the need for a new battery.
- Alternatively, is there theoretical reason to expect that the interaction between these substrates is cleanly linear and fully captured by standard structural equation modeling of existing traits, making specialized interaction experiments redundant a priori?

---

*Full audit trail and primary citations: [master-evidence-table.csv](https://github.com/krish-rm/hsri-research/blob/main/evidence/master-evidence-table.csv)*
