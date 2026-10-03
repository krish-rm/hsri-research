DRAFT PR: to be opened by the maintainer

# PR Description: sprint-12/ci

**Suggested Title:** `ci: add pull_request and non-main branch test and build workflow`  
**Base Branch:** `main`  
**Compare Branch:** `sprint-12/ci`  
**Compare URL:** https://github.com/krish-rm/hsri-research/compare/main...sprint-12/ci  

---

## 1. Restricted Categories Touched
- **Verification Infrastructure & Governance Guard Test:** Adding `.github/workflows/ci.yml` and modifying `test_no_automation_workflows` in `tests/test_agents.py`.
- **CRITICAL GOVERNANCE NOTICE:** This branch modifies a governance guard test (`test_no_automation_workflows`) designed to prevent autonomous merge and PR workflows. Under Rule 1, Rule 11, and Task 13.3, changes to verification infrastructure and governance guard tests **strictly require human maintainer review and approval**. Autonomous agent merge is prohibited.

---

## 2. Summary of Changes

1. **Automated CI Workflow (`.github/workflows/ci.yml`):**
   - Configured to trigger on all `pull_request` events and all `push` events to non-main branches (`branches-ignore: [main]`).
   - Runs on `ubuntu-latest` (Linux runner) to detect cross-platform path, separator, and line-ending issues early.
   - Pinned dependencies to match documented versions:
     - Python: `'3.10'` (matching `.github/workflows/deploy.yml` line 26).
     - Node.js: `22` (matching `.github/workflows/deploy.yml` line 21).
   - Restricted permissions: `permissions: contents: read`.
   - Executes `python -m pytest -v` across the Python test suite and `npm run build` in `site-astro`.
   - Contains no deployment steps, no secrets, and no push permissions.

2. **Governance Guard Test Update (`tests/test_agents.py`):**
   - In accordance with Task 13.3, `test_no_automation_workflows` was updated directly on the branch to authorize `ci.yml` in the allowed workflow list, accompanied by strict, programmatic security assertions:
     1. Asserts top-level `permissions` is exactly `contents: read`.
     2. Asserts zero references to `secrets.`.
     3. Asserts absence of strings: `gh pr`, `git push`, `merge`, `automerge`, `peter-evans`, `create-pull-request`.
     4. Asserts triggers do not include `workflow_dispatch` or `schedule`.

---

## 3. Test Status on Branch

With the governance guard assertions implemented, `python -m pytest -v` passes 68/68 on `sprint-12/ci`:

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

============================= 68 passed in 3.33s ==============================
```

> **Note on CI Evidence:** Per Task 13.3, no GitHub Actions CI run exists for this commit until the maintainer opens the pull request. We do not claim CI passes before that run exists. The local 68-test pass is recorded as local evidence only.
