# Proposed Replacements for Repository Handoff Document

- **Target File:** Repository Handoff Document (Maintainer's External / Root Document)
- **Author:** HSRI Governance Sentinel (Sprint 11, Task 11.0.j)
- **Date:** 2026-10-02T14:40:00+05:30
- **Purpose:** Provide exact, verbatim text replacements for the human maintainer to apply to the handoff document to ensure total epistemic consistency with Rules 11–17.

---

## 1. Sprint History Table Replacements

### Sprint 7 Table Row
**Find:**
```markdown
| Sprint 7 | ... | EXP-01 validated via synthetic personas ... |
```
*(or any phrasing stating that EXP-01 was "validated" by synthetic personas)*

**Replace With:**
```markdown
| Sprint 7 | Behavioral Lab Phase 2 | EXP-01 stimulus generation and synthetic persona piloting completed (stimuli cleared for IRB submission; not validated on human participants); TOPIC-003 escalated. |
```

---

### Sprint 8 Table Row
**Find:**
```markdown
| Sprint 8 | ... | EXP-02 validated, pilot pending ... |
```
*(or any phrasing stating that EXP-02 was "validated")*

**Replace With:**
```markdown
| Sprint 8 | Behavioral Lab Phase 2 | Synthetic cohort pilot framework established; EXP-02 stimulus battery generated (stimuli cleared for IRB submission; not validated on human participants); governance alert issued. |
```

---

### Sprint 9 Table Row
**Find:**
```markdown
| Sprint 9 | ... | EXP-01 PROCEED TO IRB | EXP-02 pilot complete | EXP-03 validated | ... |
```

**Replace With:**
```markdown
| Sprint 9 | Behavioral Lab & Governance | EXP-01 synthetic pilot complete (IRB package ready); EXP-02 synthetic pilot complete (stimuli cleared for IRB submission); EXP-03 stimuli generated (constraint checks passed); TOPIC-003 conservative default applied; TOPIC-004 logged. |
```

---

### Sprint 10 Table Row (Addition)
**Insert:**
```markdown
| Sprint 10 | Governance Remediation & Open Science | Remediated Sprint 9 governance gaps (Tasks 10.0.a–j); split Step 5 into canonical 4-check gate and supplementary script; produced full EXP-02 IRB submission package (00–08); created preprint scaffold draft-v0.1.md; created Zenodo deposit metadata schema; 67/67 unit tests passing. |
```

---

## 2. Behavioral Experiments Status Section Replacements

**Find Section:**
```markdown
### Behavioral Lab Status
- EXP-01: PROCEED TO IRB
- EXP-02: PILOT IN PROGRESS (or validated)
- EXP-03: validated
```

**Replace With:**
```markdown
### Behavioral Experiment Pipeline Status (Rule 12 Compliant)
> **EPISTEMIC BOUNDARY (Rule 12):** Synthetic-persona pilots (LLM personas) test stimulus behavior only and provide zero empirical evidence regarding human cognition or human automation bias. All human participant evaluations remain strictly gated under institutional ethics review. "Validated" is reserved strictly for human-participant data.

- **EXP-01 (Legal Domain):** `SYNTHETIC PILOT COMPLETE: IRB PACKAGE READY` (9 submission documents assembled; institutional PI designation pending).
- **EXP-02 (Medical Domain):** `SYNTHETIC PILOT COMPLETE: STIMULI CLEARED FOR IRB SUBMISSION` (9 submission documents assembled; clinician review of debriefing content required; Item 1 ceiling effect flagged for human calibration).
- **EXP-03 (Technical/Code Domain):** `SYNTHETIC PILOT COMPLETE: STIMULI CLEARED FOR IRB PACKAGING` (5-item battery covering factual, logical, api_misuse, and security errors; Item 5 flagged for synthetic ceiling artifact / triviality at $D = 1.00$).
- **EXP-04 (Financial/Quantitative Domain):** Scoped; stimulus generation deferred pending human pilot data on EXP-01/02.
```

---

## 3. Standing Governance Rules Section: Permanent Merge Authorization & Rules 11–17

### Rule 1 Replacement (Permanent Merge Authorization)
**Replace Rule 1 With:**
```markdown
1. The agent may merge to main without per-merge human sign-off only when:
   (a) the full pytest suite passes, with the summary pasted;
   (b) canonical Step 5 passes on production after deploy;
   (c) the merge is --no-ff, with no force-push or history rewriting;
   (d) every merge is reported with SHA and workflow run IDs.
   A human-approved PR is still required for changes to governance rules,
   to the pass criteria of any verification script, to IRB/consent/risk
   documents, or to public verdict labels. The maintainer may revoke this
   at any time.
```

### Addition of Rules 11–17
**Append Following Rule 10:**
```markdown
11. **Branch + PR workflow.** All changes go on a feature branch (`sprint-<N>/<task>`) and open as a PR. The agent never pushes directly to `main`. If the maintainer explicitly authorizes a direct push in the sprint chat, quote that authorization in the report.
12. **Verdict language.** Synthetic-persona pilots (LLM personas) test stimulus behavior only. They are never evidence about human cognition. Use "stimuli cleared for IRB submission", not "validated" or "PROCEED TO IRB", on the site, in reports, and in any preprint or metadata. "Validated" is reserved for human-participant data.
13. **Report integrity.** Execution reports must disclose CI failures, retries, and workflow changes made to get a green run, and must reconcile all dates to a single timezone.
14. **Canonical Step 5 gate.** The four-check Step 5 script in the handoff document is the authoritative gate. Additional checks (e.g. `exp_pipeline_on_methodology`) run as a separate supplementary script, and their output is reported separately.
15. **Credentials.** The agent never reads, extracts, or reuses stored credentials (e.g. via `git credential fill`, environment dumps, or keychain access). It may use only credentials explicitly provisioned for it (`gh` CLI session or a scoped token in environment secrets). If none is available, the agent pushes the branch and gives the maintainer the compare URL to open the PR manually. Any credential use outside this must be disclosed as a deviation.
16. **Evidence rule.** Every PASS in a verification table cites raw command output pasted verbatim (pytest summary, grep output, run ID with conclusion). A PASS with no pasted evidence is reported as `UNVERIFIED`.
17. **Historical record.** Dated log entries (queue statuses, divergence log, sprint reports) are never rewritten to match a later correction. Corrections are made by adding a dated addendum or amending only the incorrect document, with the change noted.
```

---

## 4. Step 5 Verification Scripts Section Replacements

**Replace Single Script Section With:**
```markdown
### Verification Gate: Canonical Step 5 Script (`scripts/step5_verify.py`)
Run before any sprint report sign-off. Must output `ALL INDEPENDENT CHECKS PASSED` verbatim:
```bash
python scripts/step5_verify.py
```
*Checks:*
1. Preview version badge (`v0.2` or `v0.3`)
2. Country pagination (`Showing 10 of 39 countries`)
3. Methodology footer link present and valid
4. Coverage link present

### Supplementary Methodology Verification Script (`scripts/step5_supplementary.py`)
Run separately to audit methodology page label updates. Output reported in its own independent section:
```bash
python scripts/step5_supplementary.py
```
*Checks:*
1. Behavioral Experiment Pipeline section present
2. EXP-01 exact label: `SYNTHETIC PILOT COMPLETE: IRB PACKAGE READY`
3. EXP-02 exact label: `SYNTHETIC PILOT COMPLETE: STIMULI CLEARED FOR IRB SUBMISSION`
4. EXP-03 exact label: `STIMULI GENERATED: CONSTRAINT CHECKS PASSED`
5. Absence of legacy string `PROCEED TO IRB`
6. Absence of legacy string `PILOT IN PROGRESS`
7. IRB gate warning present
```
