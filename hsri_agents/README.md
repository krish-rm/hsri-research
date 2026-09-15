# HSRI-Agents: Evidence-Review and Adversarial Debate Pipeline

`hsri_agents` is an automated evidence-review subsystem for the Human Superintelligence Readiness Index (HSRI). It adapts multi-agent debate architectures to scientific literature auditing, construct validation, and empirical integrity verification.

Unlike trading or game-playing agents, an evidence-review system has no daily objective market feedback signal. Therefore, **HSRI-Agents is built to run rarely and rigorously, not daily and cheaply.**

---

## ⚠️ Operational Notice: Manual-First Rollout

> [!IMPORTANT]
> **Automation is intentionally deferred.**  
> In accordance with project governance, **all scheduled workflows, cron jobs, and webhooks are disabled in this build**. Every component is operated strictly by hand, one step at a time, with human review required between steps:
> 
> `Scanner` ➔ *(Human reviews hits)* ➔ `Analysts` ➔ *(Human reviews briefs)* ➔ `Debate Team` ➔ *(Human reads transcript)* ➔ `Synthesizer` ➔ *(Human reads diff)* ➔ `Review Board` ➔ *(Human inspects votes)* ➔ **Manual PR Creation**.
> 
> **Do not wire up automated triggers or schedulers** until the repository maintainer has validated the manual process and explicitly specified a review cadence and trigger threshold.

---

## Multi-Model Reliability Ensemble (Section 5 Framing)

The full agent graph executes independently once per backbone provider:

```python
providers = [
    "anthropic",     # Claude
    "openai",        # GPT
    "google",        # Gemini
    "xai",           # Grok
    "deepseek",
    "qwen",          # Alibaba DashScope
    "glm",           # Zhipu
]
```

> **Methodological Framing:**  
> This ensemble represents **the same evidence-review protocol executed independently across model families, to test whether conclusions are robust to which model performs the review**—not competing national or corporate teams. No providers are mixed within a single evaluation run. Divergence across model families on the same paper is logged in `model-divergence-log.csv` as an empirical research finding.

---

## Agent Roles (Strictly Separated)

1. **Literature Scanner (`scanner.py`):** Queries open science APIs (arXiv, PubMed, etc.) for evidence-table keywords. Writes candidate records to `scan-log/`. Does not evaluate implications or open PRs.
2. **Evidence Analysts (`analysts.py`):** 4 parallel roles (Psychometrics, HAI-Interaction, Cross-Cultural Methods, Governance/Ethics). Each produces a bounded brief (<400 words) concluding with `NO EVIDENCE-TABLE IMPACT`, `POSSIBLE IMPACT`, or `DIRECT IMPACT`.
3. **Construct Debate Team (`debate.py`):** Multi-round debate between a **Proponent** (arguing for incremental validity or evidence-table updates based strictly on source text) and a **Skeptic** (defending the null, checking for unverified precision and sample limitations). Retains full transcripts.
4. **Systematic Review Synthesizer (`synthesizer.py`):** Evaluates the debate and drafts either a concrete line-by-line diff or an explicit `NO CHANGE — evidence insufficient` verdict. Never softens Skeptic objections.
5. **Consortium Review Board (`review_board.py`):** 3 non-optional adversarial seats:
   - **Adversarial Skeptic:** checks for excessive convergence and ungrounded inferences.
   - **Cross-Cultural Methodologist:** vetoes single-population generalizations lacking invariance testing.
   - **Accountability-Laundering Reviewer:** vetoes user-blaming framings that excuse AI model developers or regulators.
   *Any single rejection halts PR readiness. All 3 approvals required.*

---

## CLI Usage (Manual Step-by-Step)

Each step can be executed individually:

```bash
# Step 1: Scan literature
python -m hsri_agents scan --provider mock

# Step 2: Run the 4 Evidence Analysts on a specific hit
python -m hsri_agents analyze --hit <hit_id> --provider mock

# Step 3: Convene the Construct Debate Team (2 or 3 rounds)
python -m hsri_agents debate --hit <hit_id> --rounds 2 --provider mock

# Step 4: Synthesize the debate into a proposed diff or NO CHANGE
python -m hsri_agents synthesize --debate <hit_id> --provider mock

# Step 5: Convene the 3-seat Consortium Review Board
python -m hsri_agents review --diff <hit_id> --provider mock

# Optional: Interactive multi-step sequence
python -m hsri_agents run-all-manual --hit <hit_id> --provider mock

# View system and log status
python -m hsri_agents status
```

---

## Durable Audit Trail

- **`research_memory.md`:** Comprehensive, unsummarized ledger of every convened debate, analyst brief, synthesizer diff, and seated Review Board vote.
- **`model-divergence-log.csv`:** Cross-provider reliability matrix tracking verdict concordance across providers for each evaluated paper.
- **`scan-log/`:** Local storage directory holding JSON snapshots of all candidate hits and intermediate pipeline stages.
