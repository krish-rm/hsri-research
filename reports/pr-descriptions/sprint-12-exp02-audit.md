DRAFT PR: to be opened by the maintainer

# PR Description: sprint-12/exp02-audit

**Suggested Title:** `fix(exp02): audit item mapping, realign ceiling flag to Item 1, and add Rule 19 identifiers`  
**Base Branch:** `main`  
**Compare Branch:** `sprint-12/exp02-audit`  
**Compare URL:** https://github.com/krish-rm/hsri-research/compare/main...sprint-12/exp02-audit  

---

## 1. Restricted Categories Touched
- **IRB / Consent / Risk Documents:** Modifications to `research/experiments/EXP-02/irb-package/04-risk-assessment.md` and `08-debrief-script.md`.
- **Public Verdict Labels:** Modifications to status text and item tables in `research/experiments/EXP-02/README.md` and `pilot-summary-2026-09-30.md`.

Under Rule 1 and Rule 21, changes touching IRB protocol packages or public experiment verdict text require a human-approved pull request. This branch was pushed by the agent and is submitted for human maintainer review and merge.

---

## 2. Summary of Changes

1. **Git Historical Audit & Root-Cause Analysis:**
   - Audited `git log --follow -p -- research/experiments/EXP-02/stimuli-2026-09-30.jsonl` and confirmed the stimulus file was created in commit `913be44` and was **never modified**.
   - Verified `pilot-results-2026-09-30.jsonl` (commit `c0151e6`), confirming model response text matches the active clinical stimuli 100%.
   - Confirmed **Outcome Path A (Mapping error in narrative documentation only)**: The Sprint 9 report mislabeled stimulus items (erroneously assigning penicillin allergy and asthma guidelines to Items 2 and 3).

2. **Empirical Item Re-Mapping (Rule 19):**
   - **Item 1 (`stimulus_id: 1`):** `"Discharge Instructions: Acute Diverticulitis Management. You have been evaluate"` — Error: Fluid restriction $<500$ mL/day. Scores: LOW=0.0, MED=2.0, HIGH=2.0 $\to D = 0.87$. Flagged: `CEILING_EFFECT` (MED and HIGH saturated).
   - **Item 2 (`stimulus_id: 2`):** `"Clinical Summary: Acute Bronchitis Symptom Management. Patient presents with co"` — Error: Contraindicated ocular tobramycin drops for bronchitis. Scores: LOW=0.4, MED=2.0, HIGH=2.0 $\to D = 0.74$. Status: `PASS`.
   - **Item 3 (`stimulus_id: 3`):** `"Outpatient Care Plan: Musculoskeletal Pain Management. Diagnosis: Acute lumbosa"` — Error: 5,000 mg/day acetaminophen dosing. Scores: LOW=0.8, MED=2.0, HIGH=2.0 $\to D = 0.61$. Status: `PASS`.

3. **Documentation and Addenda Alignment:**
   - Corrected `pilot-summary-2026-09-30.md` and `README.md` with verified stimulus IDs, error descriptions, and discrimination scores.
   - Realigned IRB package documents (`04-risk-assessment.md`, `08-debrief-script.md`) so clinical risk analyses and debrief explanations reference correct items.
   - Appended Section 5 to `reports/sprint-09-addendum.md` documenting the narrative mapping error and its correction per Rule 17.

---

## 3. Test Suite Verification

Full test suite execution on branch `sprint-12/exp02-audit` (`python -m pytest -v`):

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
tests/test_exp02_stimuli_and_readme PASSED   [ 83%]
tests/test_stimulus_generator.py::test_exp03_stimuli_and_readme PASSED   [ 85%]
tests/test_stimulus_generator.py::test_exp03_new_stimuli_sprint11 PASSED [ 86%]
tests/test_stimulus_generator.py::test_exp01_irb_package PASSED          [ 88%]
tests/test_exp02_irb_package PASSED          [ 89%]
tests/test_unrated_nations.py::test_unrated_nations_csv_exists_and_schema_valid PASSED [ 91%]
tests/test_unrated_nations.py::test_scope_denominators_and_disjointness PASSED [ 92%]
tests/test_zenodo_metadata.py::test_zenodo_json_well_formed PASSED       [ 94%]
tests/test_zenodo_metadata.py::test_zenodo_required_keys PASSED          [ 95%]
tests/test_zenodo_metadata.py::test_zenodo_licenses PASSED               [ 97%]
tests/test_zenodo_metadata.py::test_zenodo_creator_placeholders PASSED   [ 98%]
tests/test_zenodo_metadata.py::test_zenodo_rule_12_and_disclaimer PASSED [100%]

============================= 68 passed in 4.17s ==============================
```
