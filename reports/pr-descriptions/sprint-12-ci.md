DRAFT PR: to be opened by the maintainer

# PR Description: sprint-12/ci

**Suggested Title:** `ci: add pull_request and non-main branch test and build workflow`  
**Base Branch:** `main`  
**Compare Branch:** `sprint-12/ci`  
**Compare URL:** https://github.com/krish-rm/hsri-research/compare/main...sprint-12/ci  

---

## 1. Restricted Categories Touched
- **Verification Infrastructure:** Adding `.github/workflows/ci.yml`.

Under Rule 1 and Rule 21, changes to verification infrastructure require a human-approved pull request. This branch was pushed by the agent and is submitted for human maintainer review and merge.

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

---

## 3. Test Failure Explanation & Proposed Resolution

### Failing Test Explanation
Running `python -m pytest -v` on branch `sprint-12/ci` yields **1 failure out of 68 tests**:

```
================================== FAILURES ===================================
_________________ TestHSRIAgents.test_no_automation_workflows _________________

self = <test_agents.TestHSRIAgents testMethod=test_no_automation_workflows>

    def test_no_automation_workflows(self):
        """Verify that only authorized workflows exist and no autonomous merge/PR workflows are added."""
        workflows_dir = REPO_ROOT / ".github" / "workflows"
        if workflows_dir.exists():
            workflows = sorted([f.name for f in workflows_dir.glob("*.yml")] + [f.name for f in workflows_dir.glob("*.yaml")])
            # Only deploy.yml, ingestion-health.yml, and literature-sentinel.yml are permitted
>           self.assertEqual(workflows, ["deploy.yml", "ingestion-health.yml", "literature-sentinel.yml"])
E           AssertionError: Lists differ: ['ci.yml', 'deploy.yml', 'ingestion-health.yml', 'literature-sentinel.yml'] != ['deploy.yml', 'ingestion-health.yml', 'literature-sentinel.yml']
E           
E           First differing element 0:
E           'ci.yml'
E           'deploy.yml'
E           
E           First list contains 1 additional elements.
E           First extra element 3:
E           'literature-sentinel.yml'
E           
E           - ['ci.yml', 'deploy.yml', 'ingestion-health.yml', 'literature-sentinel.yml']
E           ?  ----------
E           
E           + ['deploy.yml', 'ingestion-health.yml', 'literature-sentinel.yml']

tests\test_agents.py:212: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_agents.py::TestHSRIAgents::test_no_automation_workflows - A...
======================== 1 failed, 67 passed in 18.14s ========================
```

- **Root Cause:** Unit test `test_no_automation_workflows` in `tests/test_agents.py` strictly checks that only three specific workflow files exist. Introducing `.github/workflows/ci.yml` triggers an assertion failure.
- **Why it was not altered on `sprint-12/ci`:** Standing instructions state: *"Do not weaken or delete tests to get a pass; propose fixes in the PR description and let the maintainer decide."*
- **Proposed Fix (Task 13.3):** The maintainer should adopt the guard test update prepared on branch `sprint-12/ci` under Task 13.3, which:
  1. Authorizes `ci.yml` in the allowed workflows list.
  2. Inspects `ci.yml` to assert top-level `permissions` is strictly `contents: read`.
  3. Verifies zero references to `secrets.`.
  4. Verifies absence of automation tools (`gh pr`, `git push`, `merge`, `automerge`, `peter-evans`, `create-pull-request`).
  5. Verifies absence of `workflow_dispatch` and `schedule` triggers.

Once the maintainer reviews and merges the PR with the guard test update, CI checks will pass cleanly.
