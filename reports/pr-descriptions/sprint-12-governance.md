DRAFT PR: to be opened by the maintainer

# PR Description: sprint-12/governance

**Suggested Title:** `feat(governance): consolidate Rules 1-21, audit direct commits, and sanitize agent contacts`  
**Base Branch:** `main`  
**Compare Branch:** `sprint-12/governance`  
**Compare URL:** https://github.com/krish-rm/hsri-research/compare/main...sprint-12/governance  

---

## 1. Restricted Categories Touched
- **Governance Rules:** Authoring `reports/governance-rules-v2.md` to reconcile Standing Rules 1 and 11 and consolidate Rules 1–21.
- **Verification Script History Audit:** Modifying `reports/ratifications.md` to log `PENDING` entries for direct commits affecting verification scripts and status text.

Under Rule 1 and Rule 21, changes to governance rules and verification script history require a human-approved pull request. This branch was pushed by the agent and is submitted for human maintainer review and merge.

---

## 2. Summary of Changes

1. **Governance Rules Consolidation (`reports/governance-rules-v2.md`):**
   - Reconciled Rule 1 (maintainer's proposed autonomous merge conditions) and Rule 11 (branch & PR workflow) to eliminate contradictions: all development occurs on feature branches (`sprint-<N>/<task>`); direct commits to `main` are strictly prohibited; autonomous merge is permitted via `--no-ff` only when all Rule 1 criteria are satisfied and no restricted file is touched; otherwise, a draft PR is opened and work stops.
   - Consolidated Rules 1–21 in full, adding rationale and explicit inventories of the four restricted categories (Verification Scripts, IRB Documents, Public Verdict Labels, and Governance Rules).

2. **Audit of Direct Commits (`reports/ratifications.md`):**
   - Logged `PENDING` maintainer ratification entries for:
     - SHA `8a47a40`: Direct commit modifying `scripts/step5_supplementary.py` to widen label matching for EXP-03 without a prior human-approved PR.
     - SHA `1a762aa`: Direct commit modifying governance rules text in `handoff-corrections.md` and EXP-03 status text without a prior human-approved PR.

3. **Timestamp Audit (`reports/timestamp-corrections.md`):**
   - Audited all Sprint 10 and Sprint 11 reports/addenda against `git log --format='%H %ad' --date=iso`.
   - Identified five documents whose stated timestamps in text were earlier than their initial commit timestamp (`cff48a0`), documenting them in an audit table per Rule 17.
   - Clarified in `hsri_agents/debate-queue.md` which parts of the TOPIC-003 date explanation are log-established vs speculative guesses.

4. **Sanitization of Agent User-Agent Contacts (Rule 20):**
   - Replaced simulated email addresses (`audit@hsri.org`, `research@hsri.org`) in `scripts/literature_sentinel.py`, `scratch/verify_references.py`, and `scratch/verify_remaining_refs.py` with neutral agent identifier `HSRI-Audit`.

---

## 3. Test Suite Verification

Full test suite execution on branch `sprint-12/governance` (`python -m pytest -v`):

```
============================= test session starts =============================
platform win32 -- Python 3.10.0, pytest-7.4.3, pluggy-1.6.0 -- C:\Users\lenovo\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\lenovo\Documents\Github Repo\hsri-research
plugins: anyio-3.7.1, dash-3.0.0, Faker-37.5.3, cov-6.2.1
collecting ... collected 68 items

tests/test_agents.py::TestHSRIAgents::test_analysts_briefs PASSED        [  1%]
tests/test_agents.py::TestHSRIAgents::test_debate_team PASSED            [  2%]
tests/test_agents.py::TestHSRIAgents::test_logging_ledgers PASSED        [  4%]
tests/test_agents.py::TestHSRIAgents::test_no_automation_workflows PASSED [  5%]
tests/test_agents.py::TestHSRIAgents::test_provider_configuration PASSED [  7%]
tests/test_agents.py::TestHSRIAgents::test_review_board_veto_gate PASSED [  8%]
tests/test_agents.py::TestHSRIAgents::test_role_prompt_separation PASSED [ 10%]
tests/test_agents.py::TestHSRIAgents::test_scanner_manual_execution PASSED [ 11%]
tests/test_agents.py::TestHSRIAgents::test_synthesizer PASSED            [ 13%]
tests/test_agents.py::test_literature_escalation_triggers_debate PASSED  [ 14%]
tests/test_agents.py::test_pipeline_hold_blocks_pr_generation PASSED     [ 16%]
tests/test_agents.py::test_concordance_threshold_gates_review_board PASSED [ 17%]
tests/test_agents.py::test_single_veto_blocks_pr PASSED                  [ 19%]
tests/test_agents.py::test_unanimous_approve_creates_pr_draft PASSED     [ 20%]
tests/test_citation_cff.py::test_citation_cff_valid_schema PASSED        [ 22%]
tests/test_citation_cff.py::test_release_tag_matches_citation_version PASSED [ 23%]
tests/test_divergence_log.py::test_divergence_log_schema_matches_citable_spec PASSED [ 25%]
tests/test_divergence_log.py::test_topic_001_example_row_integrity PASSED [ 26%]
tests/test_divergence_log.py::test_validation_rejects_missing_fields PASSED [ 27%]
tests/test_divergence_log.py::test_validation_rejects_unauthorized_extra_fields PASSED [ 29%]
tests/test_divergence_log.py::test_append_divergence_entry_enforces_schema PASSED [ 30%]
tests/test_ensemble_runner.py::test_ensemble_runner_handles_missing_keys PASSED [ 32%]
tests/test_ensemble_runner.py::test_parse_debate_response_formats PASSED [ 33%]
tests/test_ensemble_runner.py::test_topic_argument_loads_correct_config PASSED [ 35%]
tests/test_evidence_reconciler.py::test_review_required_flag_on_strong_claim_challenge PASSED [ 36%]
tests/test_evidence_reconciler.py::test_upgrade_candidate_flag_on_rct_support PASSED [ 38%]
tests/test_evidence_reconciler.py::test_reconciler_never_modifies_evidence_tiers PASSED [ 39%]
tests/test_evidence_reconciler.py::test_reconciler_issue_fires_on_review_required PASSED [ 41%]
tests/test_ingestion.py::TestHarmonizedObservations::test_record_count_and_columns PASSED [ 42%]
tests/test_ingestion.py::TestHarmonizedObservations::test_emli_geographic_missingness PASSED [ 44%]
tests/test_ingestion.py::TestHarmonizedObservations::test_emli_european_observed PASSED [ 45%]
tests/test_ingestion.py::TestHarmonizedObservations::test_piaac_pstre_missingness PASSED [ 47%]
tests/test_ingestion.py::TestNormalizedMatrix::test_dimension_and_bounds PASSED [ 48%]
tests/test_ingestion.py::TestNormalizedMatrix::test_nan_preservation_in_normalization PASSED [ 50%]
tests/test_ingestion.py::TestIndexScoresAndCoverage::test_coverage_bounds_and_completeness PASSED [ 51%]
tests/test_ingestion.py::TestIndexScoresAndCoverage::test_pillar_coverage_consistency PASSED [ 52%]
tests/test_ingestion.py::TestIndexScoresAndCoverage::test_score_ranges PASSED [ 54%]
tests/test_ingestion.py::TestIndexScoresAndCoverage::test_sgp_band_stability_under_observed_only_rule PASSED [ 55%]
tests/test_ingestion.py::TestWebExportSynchronization::test_country_scores_json PASSED [ 57%]
tests/test_ingestion.py::TestModularFetchers::test_all_fetchers PASSED   [ 58%]
tests/test_literature_sentinel.py::test_jsonl_schema_complete PASSED     [ 60%]
tests/test_literature_sentinel.py::test_escalation_fires_on_strong_contradiction PASSED [ 61%]
tests/test_weird_flag_detection PASSED      [ 63%]
tests/test_preprint_scaffold.py::test_preprint_file_exists PASSED        [ 64%]
tests/test_preprint_scaffold.py::test_preprint_required_sections PASSED  [ 66%]
tests/test_preprint_scaffold.py::test_preprint_abstract_and_framing PASSED [ 67%]
tests/test_preprint_scaffold.py::test_preprint_limitations_substantive PASSED [ 69%]
tests/test_preprint_scaffold.py::test_preprint_references_marked_verify PASSED [ 70%]
tests/test_stimulus_generator.py::test_stimulus_schema_complete PASSED   [ 72%]
tests/test_stimulus_generator.py::test_validation_rejects_short_stimulus PASSED [ 73%]
tests/test_stimulus_generator.py::test_validation_rejects_out_of_range_discrimination PASSED [ 75%]
tests/test_irb_note_in_readme PASSED         [ 76%]
tests/test_stimulus_generator.py::test_stimuli_file_is_valid_jsonl PASSED [ 77%]
tests/test_stimulus_generator.py::test_pilot_scores_are_in_range PASSED  [ 79%]
tests/test_stimulus_generator.py::test_pilot_discrimination_computed_correctly PASSED [ 80%]
tests/test_stimulus_generator.py::test_revision_required_flag_on_low_discrimination PASSED [ 82%]
tests/test_stimulus_generator.py::test_exp02_stimuli_and_readme PASSED   [ 83%]
tests/test_stimulus_generator.py::test_exp03_stimuli_and_readme PASSED   [ 85%]
tests/test_stimulus_generator.py::test_exp03_new_stimuli_sprint11 PASSED [ 86%]
tests/test_stimulus_generator.py::test_exp01_irb_package PASSED          [ 88%]
tests/test_stimulus_generator.py::test_exp02_irb_package PASSED          [ 89%]
tests/test_unrated_nations.py::test_unrated_nations_csv_exists_and_schema_valid PASSED [ 91%]
tests/test_unrated_nations.py::test_scope_denominators_and_disjointness PASSED [ 92%]
tests/test_zenodo_metadata.py::test_zenodo_json_well_formed PASSED       [ 94%]
tests/test_zenodo_metadata.py::test_zenodo_required_keys PASSED          [ 95%]
tests/test_zenodo_metadata.py::test_zenodo_licenses PASSED               [ 97%]
tests/test_zenodo_metadata.py::test_zenodo_creator_placeholders PASSED   [ 98%]
tests/test_zenodo_metadata.py::test_zenodo_rule_12_and_disclaimer PASSED [100%]

============================= 68 passed in 4.41s ==============================
```
