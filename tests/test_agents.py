"""
Unit test suite for HSRI-Agents.

Tests strict role separation, manual CLI invocation, Review Board veto gates,
multi-provider configuration, durable logging, and epistemic guardrails.
"""

import csv
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from hsri_agents.analysts import ANALYST_SYSTEM_PROMPTS, run_analysts
from hsri_agents.config import (
    DOCS_DIR,
    EVIDENCE_TABLE_PATH,
    MODEL_DIVERGENCE_LOG_PATH,
    REAL_ENSEMBLE_PROVIDERS,
    REPO_ROOT,
    RESEARCH_MEMORY_PATH,
    SCAN_LOG_DIR,
    SUPPORTED_PROVIDERS,
)
from hsri_agents.debate import run_debate
from hsri_agents.llm import LLMClient
from hsri_agents.logger import (
    initialize_ledgers,
    log_divergence_entry,
    log_research_memory_entry,
)
from hsri_agents.review_board import SEAT_SYSTEM_PROMPTS, run_review_board
from hsri_agents.scanner import scan_literature
from hsri_agents.synthesizer import run_synthesizer

SAMPLE_PAPER = {
    "id": "test_bucinca_2021",
    "title": "To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-Assisted Decision-Making",
    "authors": ["Zana Buçinca", "Maja Barbara Malaya", "Krzysztof Z. Gajos"],
    "venue": "Proceedings of the ACM on Human-Computer Interaction (CSCW)",
    "date": "2021-04-13",
    "abstract": "While AI-assisted decision-making systems promise complementary team performance, users frequently over-rely on AI recommendations even when they are incorrect. Standard explanations do not reliably mitigate this automation bias. In this paper, we evaluate cognitive forcing functions—design interventions that compel users to engage in deliberative analytical reasoning before viewing AI advice. Across two randomized experiments, cognitive forcing functions significantly reduced over-reliance on incorrect machine suggestions, with effects moderated by participants' Need for Cognition (NFC).",
    "url_or_doi": "https://doi.org/10.1145/3449287",
}

class TestHSRIAgents(unittest.TestCase):

    def setUp(self):
        initialize_ledgers()

    def test_provider_configuration(self):
        """Ensure all 7 ensemble providers plus mock are supported without mixing."""
        self.assertEqual(len(REAL_ENSEMBLE_PROVIDERS), 7)
        self.assertNotIn("mock", REAL_ENSEMBLE_PROVIDERS)
        expected = ["anthropic", "openai", "google", "xai", "deepseek", "qwen", "glm", "mock"]
        for p in expected:
            self.assertIn(p, SUPPORTED_PROVIDERS)
            client = LLMClient(provider=p, allow_fallback=True)
            self.assertEqual(client.provider, p if client.api_key else "mock")

        # Confirm that missing API key without allow_fallback raises RuntimeError
        with self.assertRaises(RuntimeError):
            LLMClient(provider="anthropic", allow_fallback=False)

    def test_role_prompt_separation(self):
        """Verify that all 4 analyst roles and 3 review board seats have distinct prompts."""
        self.assertEqual(len(ANALYST_SYSTEM_PROMPTS), 4)
        analyst_roles = set(ANALYST_SYSTEM_PROMPTS.keys())
        self.assertEqual(analyst_roles, {"psychometrics", "hai_interaction", "cross_cultural", "governance_ethics"})

        self.assertEqual(len(SEAT_SYSTEM_PROMPTS), 3)
        seat_roles = set(SEAT_SYSTEM_PROMPTS.keys())
        self.assertEqual(seat_roles, {"adversarial_skeptic", "cross_cultural_methodologist", "accountability_laundering_reviewer"})

    def test_scanner_manual_execution(self):
        """Verify scanner produces structured hits in scan-log/ without calling next steps."""
        hits = scan_literature(provider="mock", seed_paper=SAMPLE_PAPER)
        self.assertGreaterEqual(len(hits), 1)
        hit = hits[0]
        self.assertEqual(hit["id"], "test_bucinca_2021")
        self.assertIn(hit["trigger_status"], ["DIRECT", "POSSIBLE", "NO_TRIGGER"])
        self.assertTrue(SCAN_LOG_DIR.exists())

    def test_analysts_briefs(self):
        """Verify that analysts produce bounded briefs concluding with an explicit impact status."""
        result = run_analysts(SAMPLE_PAPER, provider="mock")
        self.assertEqual(result["hit_id"], "test_bucinca_2021")
        self.assertEqual(len(result["briefs"]), 4)

        for lane, brief in result["briefs"].items():
            self.assertIn("brief_text", brief)
            self.assertIn("impact_status", brief)
            self.assertIn(brief["impact_status"], [
                "NO EVIDENCE-TABLE IMPACT",
                "POSSIBLE IMPACT",
                "DIRECT IMPACT",
            ])

    def test_debate_team(self):
        """Verify multi-round debate preserves full transcript."""
        analysis_result = run_analysts(SAMPLE_PAPER, provider="mock")
        debate_result = run_debate(SAMPLE_PAPER, analysis_result, rounds=2, provider="mock")

        self.assertEqual(debate_result["rounds_completed"], 2)
        self.assertEqual(len(debate_result["transcript"]), 4)  # 2 rounds * 2 speakers
        self.assertIn("Proponent", [t["speaker"] for t in debate_result["transcript"]])
        self.assertIn("Skeptic", [t["speaker"] for t in debate_result["transcript"]])
        self.assertIn("full_dialogue_text", debate_result)

    def test_synthesizer(self):
        """Verify synthesizer produces either a diff or NO CHANGE."""
        analysis_result = run_analysts(SAMPLE_PAPER, provider="mock")
        debate_result = run_debate(SAMPLE_PAPER, analysis_result, rounds=2, provider="mock")
        synth_result = run_synthesizer(SAMPLE_PAPER, debate_result, provider="mock")

        self.assertIn(synth_result["verdict"], ["PROPOSED DIFF", "NO CHANGE"])
        self.assertIn("synthesis_text", synth_result)

    def test_review_board_veto_gate(self):
        """Verify that any single rejection halts PR readiness."""
        synthesis_mock_approved = {
            "has_diff": True,
            "verdict": "PROPOSED DIFF",
            "synthesis_text": "Proposed diff with all proper caveats and WEIRD demographic boundaries.",
        }
        board_result = run_review_board(SAMPLE_PAPER, synthesis_mock_approved, provider="mock")
        self.assertEqual(len(board_result["seats"]), 3)
        self.assertEqual(board_result["approvals"], 3)
        self.assertTrue(board_result["is_approved"])
        self.assertTrue(board_result["ready_for_pr"])

        # Test rejection behavior when no diff exists
        synthesis_no_diff = {
            "has_diff": False,
            "verdict": "NO CHANGE",
            "synthesis_text": "NO CHANGE — evidence insufficient.",
        }
        board_result_reject = run_review_board(SAMPLE_PAPER, synthesis_no_diff, provider="mock")
        self.assertFalse(board_result_reject["ready_for_pr"])

    def test_logging_ledgers(self):
        """Verify research_memory.md and model-divergence-log.csv record events properly without polluting main ledgers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_memory = Path(tmpdir) / "test_memory.md"
            tmp_divergence = Path(tmpdir) / "test_divergence.csv"

            import hsri_agents.logger as logger_mod
            orig_mem = logger_mod.RESEARCH_MEMORY_PATH
            orig_div = logger_mod.MODEL_DIVERGENCE_LOG_PATH
            logger_mod.RESEARCH_MEMORY_PATH = tmp_memory
            logger_mod.MODEL_DIVERGENCE_LOG_PATH = tmp_divergence

            try:
                analysis_result = run_analysts(SAMPLE_PAPER, provider="mock")
                debate_result = run_debate(SAMPLE_PAPER, analysis_result, rounds=1, provider="mock")
                synth_result = run_synthesizer(SAMPLE_PAPER, debate_result, provider="mock")
                board_result = run_review_board(SAMPLE_PAPER, synth_result, provider="mock")

                log_research_memory_entry(
                    hit=SAMPLE_PAPER,
                    provider="mock",
                    analysts_result=analysis_result,
                    debate_result=debate_result,
                    synthesizer_result=synth_result,
                    review_board_result=board_result,
                    pr_status="Test staged status",
                )

                log_divergence_entry(
                    triggering_paper=SAMPLE_PAPER["title"],
                    provider="mock",
                    verdict="diff-proposed",
                    notes="Test entry",
                )

                self.assertTrue(tmp_memory.exists())
                with open(tmp_memory, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.assertIn("HSRI Research Memory", content)
                    self.assertIn("Manual-First Operational Notice", content)
                    self.assertIn(SAMPLE_PAPER["title"], content)

                self.assertTrue(tmp_divergence.exists())
                with open(tmp_divergence, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    found = False
                    for row in reader:
                        if row.get("triggering_paper") == SAMPLE_PAPER["title"]:
                            self.assertEqual(row.get("mock"), "diff-proposed")
                            found = True
                    self.assertTrue(found)
            finally:
                logger_mod.RESEARCH_MEMORY_PATH = orig_mem
                logger_mod.MODEL_DIVERGENCE_LOG_PATH = orig_div

    def test_no_automation_workflows(self):
        """Verify that NO cron, scheduler, or agent GitHub Actions workflow was added."""
        workflows_dir = REPO_ROOT / ".github" / "workflows"
        if workflows_dir.exists():
            workflows = [f.name for f in workflows_dir.glob("*.yml")] + [f.name for f in workflows_dir.glob("*.yaml")]
            # Only deploy.yml for MkDocs is permitted
            self.assertEqual(workflows, ["deploy.yml"])

            with open(workflows_dir / "deploy.yml", "r", encoding="utf-8") as f:
                content = f.read().lower()
                self.assertNotIn("hsri-agents", content)
                self.assertNotIn("schedule", content)
                self.assertNotIn("cron", content)

if __name__ == "__main__":
    unittest.main()
