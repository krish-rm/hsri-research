# Maintainer Merge Checklist & Deployment Guide (Sprint 11)

> **Audience:** Human Maintainer  
> **Repository:** `krish-rm/hsri-research`  
> **Date:** 2026-10-02  
> **Status:** Path A Confirmed (neither PR #3 nor PR #4 has merged to `main` as of 2026-10-02)

---

## 1. Recommended Merge Order (Path A)

Because neither Sprint 10 PR has been merged to `main` (current `main` HEAD is `1bae217`), changes must be integrated in logical dependency order:

```
[origin/main: 1bae217]
       │
       ▼
 [Step 1: Merge PR #3] (sprint-10/remediation)
       │  • Fixes methodology labels, Zenodo metadata schema, unrated nations audit
       ▼
 [Step 2: Rebase & Merge PR #4] (sprint-10/deliverables)
       │  • Rebase against main to incorporate PR #3 test additions
       │  • Adds EXP-02 IRB package, preprint scaffold, EXP-03 initial stimuli
       ▼
 [Step 3: Merge Sprint 11 Remediation PR] (branch sprint-11/remediation)
       │  • Compare URL: https://github.com/krish-rm/hsri-research/pull/new/sprint-11/remediation
       │  • Fixes EXP-02 stimulus/package consistency (Task 11.0.a)
       │  • Adds credential disclosure addendum (Rule 15)
       │  • Reconciles preprint references against OpenAlex/Crossref
       │  • Adds retrospective ratification entry (11.0.k)
       ▼
 [Step 4: Merge Sprint 11 EXP-03 PR] (branch sprint-11/exp03)
          • Compare URL: https://github.com/krish-rm/hsri-research/pull/new/sprint-11/exp03
          • EXP-03 battery expansion: api_misuse and security stimuli
          • Synthetic cohort pilot execution (5 stimuli, N=5/persona)
          • EXP-04 scoping document
          • Methodology page update (5 stimuli, cleared for IRB packaging)
```

---

## 2. Verification Commands & Expected Output

After **each merge commit** to `main`, wait for the GitHub Pages deploy workflow (`deploy.yml`) to complete, then run the verification suite locally:

### Canonical Step 5 Gate:
```bash
python scripts/step5_verify.py
```
- **Success Criteria:** Exit code 0, verbatim stdout:
  ```
  ALL INDEPENDENT CHECKS PASSED
  ```

### Supplementary Live Production Verification:
```bash
python scripts/step5_supplementary.py
```
- **Pre-PR #3 Merge Status:** Will report `EXP-01 LABEL MISSING` because live production still serves Sprint 9 artifact without the updated labels (`UNVERIFIED (pending merge of PR #3)`).
- **Post-PR #3 & Subsequent Merges Success Criteria:** Exit code 0, verbatim stdout:
  ```
  exp_pipeline_section_present: True
  exp01_label_present: True
  exp02_label_present: True
  exp03_label_present: True
  proceed_to_irb_absent: True
  pilot_in_progress_absent: True
  irb_warning_present: True
  ALL SUPPLEMENTARY CHECKS PASSED
  ```

### Full Unit Test Suite:
```bash
python -m pytest -v
```
- **Success Criteria:** Exit code 0, 68 passed (or higher as new tests are added).

---

## 3. Items Requiring Maintainer Decision Before Merge

| Decision Item | Location / Context | Maintainer Recommendation |
|---|---|---|
| **TOPIC-004 & TOPIC-005 Review** | `hsri_agents/debate-queue.md` | **Review briefs and render ruling.** Either accept Proponent/Skeptic brief or assign arbitration status to unblock debate pipeline. |
| **Zenodo Deposit Route** | `research/zenodo-metadata.json` | **Adopt Option 1 (Manual Web Upload).** Keep `research/zenodo-metadata.json` as deposit artifact; avoid creating root `.zenodo.json` until formal v0.3 release tag. |
| **Token Scope & Credentialing** | `reports/sprint-10-addendum.md` | **Rotate/review token scope.** The Sprint 10 agent extracted a token via `git credential fill`. Provision a scoped token or authenticate the maintainer environment with `gh auth login`. |
| **PI & Institutional Designation** | `research/experiments/EXP-01/irb-package/00-cover-sheet.md` and `EXP-02/...` | **Designate Human PI.** Fill in Principal Investigator name and institutional affiliation prior to institutional IRB submission. |
| **EXP-02 Clinician Review** | `research/experiments/EXP-02/irb-package/08-debrief-script.md` | **Clinical Specialist Sign-Off.** Clinician must review clinical debrief statements (5,000 mg acetaminophen dosing, penicillin cross-reactivity, asthma guidelines) before IRB submission. |
| **Ratification Sign-off** | `reports/ratifications.md` | **Sign Ratification Record.** Add maintainer name to the ratified entry covering Sprint 9 push (`1bae217`) and Sprint 10 commits. (Zero `PENDING` entries exist). |

---

## 4. "What Could Break" Risk Analysis

1. **Rebasing PR #4 over PR #3:**
   - *Risk:* Git conflict in `tests/test_zenodo_metadata.py` or `scripts/step5_verify.py` due to concurrent edits.
   - *Mitigation:* Perform `git checkout sprint-10/deliverables && git rebase origin/main` after PR #3 merges; resolve in favor of PR #3's verified structure.
2. **EXP-02 Risk Assessment & Debrief Script Mismatch:**
   - *Risk:* PR #4 contains mismatched debrief items (Sprint 10 `04-risk-assessment.md` vs `stimuli-2026-09-30.jsonl`).
   - *Mitigation:* Merging `sprint-11/remediation` immediately resolves this mismatch by aligning all package documents to the authoritative stimulus file.
3. **Preprint References Verification:**
   - *Risk:* Citations failing automated schema or bibtex checks.
   - *Mitigation:* All 8 references have been audited against Crossref/OpenAlex/OSIS and verified with real DOIs in `sprint-11/remediation`.

---

## 5. Rollback Procedure

If a deployment failure or unexpected regression occurs after any merge commit to `main`:

```bash
# 1. Fetch latest main
git checkout main
git pull origin main

# 2. Revert the faulty merge commit (preserving commit history per Rule 17)
git revert -m 1 <MERGE_COMMIT_SHA> -m "Revert merge commit <MERGE_COMMIT_SHA> due to deployment regression"

# 3. Push revert to main
git push origin main

# 4. Confirm GitHub Actions deploy workflow completes and re-run verification
python scripts/step5_verify.py
```
