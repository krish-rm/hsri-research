# Empirical Protocol: ASI Synthetic Experiments (EXP-07-SYN & EXP-08-SYN)

> **Protocol ID**: HSRI-ASI-PROTO-SYN-07-08  
> **Classification (Rule 12)**: `CLASS: SYNTHETIC_EXPERIMENT_SIMULATION`  
> **Source-First Foundation**: Handed off from ASI Transition Master Synthesis (`ws13-synthesis-and-audit.md`, Section 17)  
> **Status**: Approved for Synthetic Laboratory Runner Execution  
> **Governing Authorities**: Huang et al. (2024, ICLR); METR (2024); Sclar et al. (2024); Salvi et al. (2024); Gans (2018).

---

## 1. Executive Summary & Context

The **ASI Transition Evidence Map Study** (Milestone P6, commit `0eb710d`) demonstrated that human cognitive agency faces acute asymmetric pressure as autonomous machine capabilities scale toward superhuman speed and fluency. Section 17 of `ws13-synthesis-and-audit.md` formulated two priority synthetic laboratory experiments designed to run autonomously in simulation without requiring human participant IRB approval:

1. **EXP-07-SYN (Compounding Error Cascades in Autonomous Multi-Agent R&D):**
   Investigating whether autonomous agent swarms attempting open-ended research workflows suffer fatal error cascading when external empirical verifiers (compilers, execution environments, empirical oracles) are withheld.
2. **EXP-08-SYN (Persuasive Belief Inversion Boundary):**
   Quantifying the exact mathematical boundary where a superhuman persuasive model inverts the factual beliefs of an evaluating entity through fluent rhetoric and synthesized pseudo-evidence.

---

## 2. EXP-07-SYN: Multi-Agent Recursive R&D Cascading

### 2.1 Swarm Architecture & Roles
The autonomous R&D swarm consists of 5 interacting agents:
1. **Agent-Architect:** Decomposes research problem into formal hypotheses and technical blueprints.
2. **Agent-Researcher:** Conducts literature and data synthesis.
3. **Agent-Coder:** Implements mathematical models and analysis code.
4. **Agent-Tester:** Generates validation suites and synthetic unit tests.
5. **Agent-Reviewer:** Evaluates internal consistency and signs off on deliverables.

### 2.2 Execution Horizons
- **Horizon 1 (8-Hour Equivalent):** 16 sequential decision cycles.
- **Horizon 2 (16-Hour Equivalent):** 32 sequential decision cycles.
- **Horizon 3 (24-Hour Equivalent):** 48 sequential decision cycles.

### 2.3 Experimental Conditions
- **Condition A (Oracle Ground-Truth Feedback):** Swarm receives objective verification feedback (compiler signals, mathematical truth checks) at regular execution checkpoints.
- **Condition B (Intrinsic Reflection / Closed Loop):** Swarm relies solely on peer critique and internal deliberation without external verifiers.

### 2.4 Error Dynamics Formulation
Step error probability degrades exponentially in closed loop as ungrounded hallucinations reinforce:
$$p_{\text{error}}(t) = 1 - (1 - p_0) \cdot \exp(-\lambda_{\text{drift}} \cdot t)$$
Task survival across $T$ steps follows:
$$S(T) = \prod_{t=1}^T (1 - p_{\text{error}}(t))$$
We evaluate the **Task Survival Half-Life ($\tau_{1/2}$)** and terminal task completion rate across $N = 50$ Monte Carlo simulation trials per condition.

---

## 3. EXP-08-SYN: Persuasive Belief Inversion Boundary

### 3.1 Adversarial Setup
- **Factual Dataset:** 100 established empirical propositions across physics, epidemiology, macroeconomics, and history where ground truth is indisputably established ($Y = 1$).
- **Superhuman Persuader:** An adversarial model tasked with generating maximally convincing arguments, framing, and plausible pseudo-citations defending the false inverse hypothesis ($Y' = 0$).
- **Evaluator Agent:** An AI evaluator representing institutional peer review or human oversight triage.

### 3.2 Controlled Parameters
- **Capability Asymmetry ($\Delta C \in [0.5, 3.0]$):** Advantage in model scale, training compute, and token generation capacity.
- **Rhetorical Fluency ($F \in [0.70, 0.99]$):** Linguistic readability and persuasive framing.
- **Pseudo-Citation Density ($\rho_{\text{pseudo}} \in [0.0, 0.40]$):** Fabricated scholarly references and spurious statistical claims.
- **Verification Depth ($D_{\text{verify}} \in [1, 5]$):** Number of independent epistemic checks conducted by the evaluator.

### 3.3 Belief Inversion Logistic Model
The probability of successfully inverting the evaluator's belief from truth to falsehood is governed by:
$$P(\text{Inversion}) = \frac{1}{1 + \exp(-(\beta_0 + \beta_1 \Delta C + \beta_2 F + \beta_3 \rho_{\text{pseudo}} - \beta_4 D_{\text{verify}}))}$$

We empirically extract:
1. **Belief Inversion Boundary ($\Delta C^*$):** The critical asymmetry threshold where belief accuracy falls below random chance ($P(\text{Truth}) < 0.50$, $d' \le 0$).
2. **Epistemic Armor Effectiveness:** The marginal verification depth $\beta_4$ required to neutralize each unit of persuasive asymmetry.

---

## 4. Gating & Verification Criteria

| Experiment | Metric | Target Threshold | Interpretation |
|---|---|---|---|
| **EXP-07-SYN** | Oracle vs Closed Survival Ratio | $S_{\text{Oracle}}(48) / S_{\text{Closed}}(48) \ge 3.00$ | Confirms empirical verifiers are essential for RSI |
| **EXP-07-SYN** | Closed Loop Error Compounding | $\lambda_{\text{cascade}} > 0.020$ | Validates METR (2024) error cascading hypothesis |
| **EXP-08-SYN** | Inversion Boundary Identification | $1.20 \le \Delta C^* \le 2.50$ | Identifies non-trivial critical persuasion threshold |
| **EXP-08-SYN** | Verification Depth Buffer | $\beta_4 / \beta_1 \ge 0.50$ | Verifies that epistemic friction preserves truth-tracking |
