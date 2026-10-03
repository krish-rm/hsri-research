DRAFT PR: to be opened by the maintainer

# Suggested Title
docs(prereg): define human discrimination metrics, separate enrollment from completion, and fix 4,200 mg attachment

# Compare URL
https://github.com/krish-rm/hsri-research/compare/main...sprint-13/prereg-fixes

# Base SHA
`385681a4cac8cefb25938d21b06f22a2d0e8bf71` (head of `sprint-12/prereg`)

# Restricted Categories Touched
- **IRB / Preregistration / Risk Protocol:** Modifies `research/experiments/EXP-01/prereg/` (`item-calibration-plan.md`, `prereg-draft.md`, `platform-requirements.md`) and `research/experiments/EXP-02/pilot-summary-2026-09-30.md`.
- Under Standing Governance Rule 1 and Rule 11, this branch touches restricted human-subject calibration governance and **must not be merged autonomously**. It requires formal human review and designation of a Principal Investigator and Lead Statistician.

# What Changed
1. **Explicit Non-Transferability of Synthetic Discrimination:** Updated `item-calibration-plan.md` to state plainly that synthetic discrimination ($D$) reflects prompted persona adherence rather than human cognition. Synthetic thresholds ($0.35 \le D \le 0.75$) do not transfer to human datasets.
2. **Defined Human Discrimination Metrics:** Replaced synthetic D thresholds with three mathematically formulated human psychometric analogues:
   - Option A: Upper-Lower Group Discrimination Index ($D_{\text{UL}}$ / Kelley's Index)
   - Option B: Corrected Item-Rest Correlation ($r_{\text{i-rest}}$)
   - Option C: Item Response Theory (IRT) Discrimination Slope ($a_i$ under Samejima's Graded Response Model)
   - Presented all three with explicit trade-offs and marked `[DECISION NEEDED: statistician]` without pre-selecting a choice for the PI.
   - Relabeled all arbitrary retention thresholds as `[DECISION NEEDED: statistician]`.
3. **Enrollment vs. Completion Disaggregation:** Updated `prereg-draft.md` Section 7.2 and Section 8 to clearly distinguish target completers ($N_{\text{complete}} = 130$ per arm, $260$ total) from enrollment targets ($N_{\text{enroll}} = 137$ per arm, $274$ total) given an assumed $5\%$ attrition rate. Explicitly disclosed that the 5% attrition figure is an unverified planning assumption marked `[DECISION NEEDED: statistician / survey platform lead]`.
4. **4,200 mg Dosage Margin Attachment Fix:** Corrected the earlier conflation where a 4,200 mg dosage narrowing was attached to Item 1 (acute diverticulitis, $D = 0.87$, ceiling effect on total water avoidance). The 4,200 mg narrowing is now explicitly attached to Item 3 (`stimulus_id: 3`, $D = 0.61$, 5,000 mg acetaminophen PO QID) and described as an untested working hypothesis for human piloting.
5. **Rule 19 Stimulus References:** Verified and updated all item references across `prereg-draft.md`, `item-calibration-plan.md`, and `platform-requirements.md` to include canonical stimulus IDs and exact 80-character text prefixes matching the underlying JSONL stimulus files.

# Test Status
```
============================= test session starts =============================
platform win32 -- Python 3.10.0, pytest-7.4.3, pluggy-1.6.0
rootdir: C:\Users\lenovo\Documents\Github Repo\hsri-research
plugins: anyio-3.7.1, dash-3.0.0, Faker-37.5.3, cov-6.2.1
collected 68 items

tests/test_agents.py .............                                       [ 19%]
tests/test_citation_cff.py ..                                            [ 22%]
tests/test_divergence_log.py .....                                       [ 29%]
tests/test_ensemble_runner.py ...                                        [ 33%]
tests/test_evidence_reconciler.py ....                                   [ 39%]
tests/test_ingestion.py ............                                     [ 57%]
tests/test_literature_sentinel.py ...                                    [ 61%]
tests/test_preprint_scaffold.py .....                                    [ 69%]
tests/test_stimulus_generator.py .............                           [ 88%]
tests/test_unrated_nations.py ..                                         [ 91%]
tests/test_zenodo_metadata.py ......                                     [100%]

============================= 68 passed in 2.97s ==============================
```
