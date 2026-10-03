# HSRI Debate Topic Queue

Topics are run in order. Each topic requires a completed run before the next begins.

## TOPIC-002 — Pillar Weighting Defensibility [STATUS: complete — NO CHANGE — 2026-09-27]
Is the equal 25/25/25/25 weighting defensible given Critical Discernment has the weakest indicator coverage?

## TOPIC-003 [STATUS: auto-resolved — MAINTAIN NaN — 2026-10-01]
**Resolution:** Conservative default applied (Sprint 9, 4th sprint since escalation).
**Ruling:** MAINTAIN NaN POLICY pending future evidence.
**Override:** Maintainer may issue explicit ruling at any time.

Proponent brief: The non-participation is an administrative fact, not a data gap. Treating it as missing data to impute would confound two different constructs (problem-solving ability vs. participation in an OECD measurement program).

Skeptic brief: Six nations are systematically disadvantaged in the Critical Discernment pillar not because their populations lack the skills but because their governments did not participate in one survey. A regional EU proxy (PISA Digital Reasoning) could provide an evidence-based substitute.

Evidence package: docs/10-proxy-framework.md §Missingness

## TOPIC-004 — Exposure Gap Modeling Validity [STATUS: complete, awaiting maintainer review: single-model result, not a finding]
Is the current macro-exposure gap model (contrasting preparedness score
against structural AI adoption exposure) empirically defensible as a
composite metric, or does it introduce a hidden assumption about the
relationship between economic exposure and cognitive readiness?

Verdict: PROPOSED DIFF (Gemini 3.8 Flash single-model run; awaiting maintainer review: single-model result, not a finding. No methodology change proposed or implemented). Cites Governance & Ethics and notes geographic bias in framing automation exposure strictly as vulnerability versus demographic necessity (e.g. East Asian developmental state model).

Evidence package: docs/04-causal-model-and-index-design.md §Exposure

## TOPIC-005 — Exposure Gap Weighting Assumptions [STATUS: queued]
Does the current exposure gap model's implicit assumption that economic
exposure to AI displacement is linearly related to preparedness deficit
hold empirically, or does it introduce systematic bias against nations
with high exposure but strong institutional buffers (e.g., Japan, South Korea)?

Evidence package: docs/04-causal-model-and-index-design.md §Exposure
Proponent brief: Linear relationship is the most conservative assumption
  absent empirical elasticity data. Non-linear models require parameter
  choices that introduce their own arbitrary assumptions.
Skeptic brief: Japan and South Korea show high economic AI exposure but
  also strong institutional governance scores. A linear model
  systematically underestimates their effective resilience.

---

## Addendum on Timestamps (Rule 17 Compliance — 2026-10-02T14:35:00+05:30)
- **Historical Timestamp Reconciliation:** The resolution date for TOPIC-003 and execution date for TOPIC-004 were recorded as `2026-10-01` in commit `c0151e6` (committed at `2026-09-30 22:41:44 +0530`).
  - *Established by logs:* Commit `c0151e6` occurred on 2026-09-30 (local `22:41:44 +0530` / UTC `17:11:44Z`) and contained the literal string `2026-10-01`.
  - *Marked as conjecture / guess:* The prior narrative explanation that this occurred due to "UTC/early next-day date transposition" is a retroactive guess/inference about author intent, not an established fact from repository logs (since UTC was also 2026-09-30 at commit time).
- In compliance with Standing Governance Rule 17 (prohibiting retrospective rewriting of dated log entries to match later reports), the original `2026-10-01` queue timestamp is preserved as committed, and this discrepancy is recorded via addendum rather than in-place rewriting.

