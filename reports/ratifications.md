# HSRI Formal Governance Ratification Log

This document serves as the append-only registry of retroactive and exceptional governance ratifications under Standing Governance Rules 1, 10, and 17.

---

## Ratification: merges to main without recorded sign-off (Sprint 9 and Sprint 10)
Date recorded: 2026-10-02T14:45:00+05:30
Commits covered (agent fills from 11.0.0 output):
  - 1bae217 ("ci: increase smoke test propagation window to ensure Pages deployment completes")
  - PR #3 merge commit: not merged as of 2026-10-02 (PR #3 remains open in draft status; pending maintainer review and merge)
  - PR #4 merge commit: not merged as of 2026-10-02 (PR #4 remains open in draft status; pending maintainer review and merge)
  - Any other commit on main between 1bae217 and 2026-10-02 that was merged without recorded review: None (commit 1bae217 is the current HEAD of origin/main)

Maintainer decision: Accepted retrospectively. The maintainer stated in the sprint chat that the earlier merging without recorded sign-off is acceptable to them, and asked that the Sprint 10 commits be covered as well.

Scope and limits:
  - This ratifies the PROCESS deviation (rule 1) for the commits listed above only.
  - It does NOT certify their content. Known content errors (e.g. the EXP-02 risk assessment mismatch, task 11.0.a) remain open and must still be fixed.
  - It does NOT cover merges made after 2026-10-02. Rule 1 is not waived for future work.

Ratified by: Human Maintainer (via sprint chat instruction: "go with Option B ... earlier until spritn 9 it was auto merge", 2026-10-02)

---

## Authorization: Direct Merge of Sprint 10 & Sprint 11 Commits to main
Date recorded: 2026-10-02T22:45:00+05:30
Commits covered:
  - 17c9a44 ("fix(sprint-10): Sprint 9 remediation (Rule 11-14 compliance, addendum, status labels, ceiling analysis, overclaim sweep)")
  - fc2a634 ("feat(sprint-10): complete EXP-02 IRB package, preprint scaffold, and zenodo metadata")
  - f14a59f ("docs(sprint-10): add Sprint 10 execution report")
  - cff48a0 ("fix(sprint-11): Task 11.0 Sprint 10 remediation (EXP-02 package consistency, step5 scripts, credential addendum, ratifications, verified references, Zenodo lowercase licenses)")
  - e8ecb51 ("feat(exp03): expand EXP-03 battery to 4 error types, run synthetic pilot, scope EXP-04, and add maintainer merge checklist")
  - 21fa79b ("docs(sprint-11): add Sprint 11 execution report")

Maintainer decision: Explicitly authorized direct integration and push to main per Option B.
Verbatim instruction: "go with Option B ... earlier until spritn 9 it was auto merge"
Authorized and ratified by: Human Maintainer (Krish / krish-rm)

---

## Authorization & Ratification: Integration of ASI-Transition Evidence Map Study (Phases 0–6) to main
Date recorded: 2026-10-04T12:05:46.7104620+05:30
Branch merged: `study-asi/final-audit`
Target branch: `main`
Commits covered:
  - 98f886b ("docs(study-asi): add Phase 0 context reconstruction memo (Task WS-00)")
  - 876578a ("feat(study-asi): complete Phase 1 search protocol, source register, and seed verification (WS-01)")
  - a1a43a4, 98b1cec, e4b25e5, 8b7338b, 0b021ab (Phase 2 Scenario Profiles SC-01 to SC-26, WS-02)
  - 7d87e3c, eed0f35, 3de18c3, fb701c1, 1bc3d38, b89c5e8, 7586c00 (Phase 3 Deep Dives WS-03 to WS-09)
  - bebeb04 ("feat(study-asi): complete WS-10 adversarial review and self-position red-team (Schema F8 review_log.csv)")
  - 59c07aa ("feat(study-asi): complete Phase 5 (WS-11 Scenario Matrix and WS-12 HSRI Implications)")
  - 632e100 ("feat(study-asi): complete WS-13 master synthesis report and audit table for Gate P6")

Maintainer decision: Explicitly authorized integration of the completed study branch into `main`.
Verbatim instructions: "DONE ... CONFIRM", "Excellent, go ahead and commit", "merge"
Authorized and ratified by: Human Maintainer (Krish / krish-rm)


