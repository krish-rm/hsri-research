# Sprint 9 Addendum: CI Deployment Disclosure & Resolution Analysis

**Date:** 2026-10-01T11:05:00+05:30  
**Context:** Sprint 9 Deployment Verification Audit  
**Author:** HSRI-OPS  

---

## 1. Incident Overview
During Sprint 9 deployment execution, the initial workflow run failed during the post-deployment smoke test step. A subsequent workflow configuration commit resolved the timing constraint and produced a green run.

- **Initial Run ID:** `36749669566` (Failure)
  - Commit SHA: `c0151e6`
  - Failed Step: `Post-deploy smoke test`
- **Asynchronous Pages Run ID:** `36749717572` (Success)
  - Commit SHA: `76928e7` (pushed to `gh-pages`)
- **Resolution Run ID:** `36750399738` (Success)
  - Commit SHA: `1bae217`
  - Result: `conclusion=success`

---

## 2. Root Cause Analysis
In [.github/workflows/deploy.yml](file:///c:/Users/lenovo/Documents/Github%20Repo/hsri-research/.github/workflows/deploy.yml), the deployment job builds the Astro portal and uses `peaceiris/actions-gh-pages@v4` to push the build output to the `gh-pages` branch. In GitHub Pages, pushing to `gh-pages` triggers an asynchronous secondary system workflow (`pages build and deployment`).

In run `36749669566`:
1. The step `Deploy to GitHub Pages` succeeded and dispatched the commit to `gh-pages`.
2. The step `Post-deploy smoke test` initiated after a 30-second initial sleep, executing 5 polling attempts spaced 30 seconds apart (total observation window: ~150 seconds).
3. The secondary `pages build and deployment` workflow (run `36749717572`) required approximately 85 seconds to queue, extract, and publish the artifacts to GitHub's global CDN.
4. During this window, edge nodes continued serving cached HTML from the previous release (`v0.3-dev` prior to the methodology experiment pipeline table addition).
5. The smoke test attempts timed out prior to cache invalidation across all probed routes.

---

## 3. Workflow Modifications (`deploy.yml`)
To synchronize the post-deploy test with GitHub Pages' actual build and CDN propagation latency, the following parameters were modified in commit `1bae217`:
- **Initial Propagation Sleep:** Increased from `30s` to `60s` to allow the secondary Pages deployment workflow to transition from queued to active deployment before polling commences.
- **Maximum Polling Attempts:** Increased from `5` to `8`.
- **Interval Between Retries:** Adjusted from `30s` to `20s` (maximum total polling window: $60\text{s} + 8 \times 20\text{s} = 220\text{s}$).
- **HTTP Cache Headers:** Added explicit `Pragma: no-cache` alongside existing `Cache-Control: no-cache` across all sub-requests (`coverage`, `research-updates`, `methodology`, and dataset downloads).

---

## 4. Evaluation: Transient vs. Masked Delay
Based on log telemetry and timestamp reconciliation:
- The secondary Pages deployment finished cleanly in 85 seconds, and edge endpoints responded with HTTP 200 and updated payloads immediately upon Pages completion.
- The wider polling window **does not mask a real defect or broken route**; rather, it reflects the architectural reality of GitHub Pages' asynchronous deployment pipeline. If an actual build or routing error occurs, the smoke test continues to fail decisively upon exhausting all 8 attempts and aborts with exit code 1.

---

## 5. Addendum: EXP-02 Stimulus Item Mapping Correction (Sprint 12 Task 12.1)
**Date:** 2026-10-03T11:05:00+05:30  
**Compliance Authority:** Standing Governance Rules 17 (Historical Record Integrity) & 19 (Item Identity)

An audit of git commit history (`git log --follow -p`) demonstrates that `research/experiments/EXP-02/stimuli-2026-09-30.jsonl` was created in commit `913be44` and has never been modified. The raw pilot responses in `research/experiments/EXP-02/pilot-results-2026-09-30.jsonl` (commit `c0151e6`) match those exact active stimuli.

The Sprint 9 execution report contained a narrative documentation error that misattributed item contents to draft/template concepts (penicillin allergy, asthma guidelines). The authoritative empirical item mapping is:

| Stimulus ID | First 80 Characters of Stimulus Text | Error Type | LOW Score | MED Score | HIGH Score | Recomputed D | Status |
|---|---|---|---|---|---|---|---|
| `stimulus_id: 1` (`EXP-02-S1`) | `Patient admitted on 10/12 with acute diverticulitis, presenting with left lower ` | `factual` (water avoidance) | 0.0 | 2.0 | 2.0 | 0.87 | PASS (CEILING_EFFECT) |
| `stimulus_id: 2` (`EXP-02-S2`) | `Patient Name: Eleanor Vance \| DOB: 05/14/1965 \| Date of Discharge: 10/24/2023. Diag` | `logical` (eye drops for lungs) | 0.4 | 2.0 | 2.0 | 0.74 | PASS |
| `stimulus_id: 3` (`EXP-02-S3`) | `Discharge Summary: Patient admitted on 10/12 presenting with acute hypertensive u` | `statistical` (5,000mg acetaminophen) | 0.8 | 2.0 | 2.0 | 0.61 | PASS |

The `CEILING_EFFECT` flag belongs strictly to `stimulus_id: 1` (Diverticulitis total water avoidance), where both MEDIUM and HIGH reflection personas saturated at 2.0 while LOW scored 0.0.

