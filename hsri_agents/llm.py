"""
Unified LLM client for multi-model ensemble execution.

Enforces provider separation (one provider per run, no mixing), supports
OpenAI-compatible, Anthropic, and Google REST APIs, and provides a deterministic
MockProvider for testing, offline execution, and dry runs.
"""

import json
import logging
import re
from typing import Any, Dict, Optional
import urllib.parse
import requests

from hsri_agents.config import (
    API_BASE_URLS,
    API_KEY_ENV_VARS,
    DEFAULT_MODELS,
    SUPPORTED_PROVIDERS,
    get_api_key,
)

logger = logging.getLogger("hsri_agents.llm")

class LLMClient:
    """Unified LLM client executing strictly within a single model provider."""

    def __init__(
        self,
        provider: str = "mock",
        model: Optional[str] = None,
        allow_fallback: bool = False,
    ):
        provider = provider.lower().strip()
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider '{provider}'. Must be one of: {SUPPORTED_PROVIDERS}"
            )
        self.provider = provider
        self.model = model or DEFAULT_MODELS[provider]
        self.api_key = get_api_key(provider)

        if self.provider != "mock" and not self.api_key:
            if not allow_fallback:
                raise RuntimeError(
                    f"CRITICAL: Missing API key for live provider '{provider}'. "
                    f"Expected one of environment variables: {API_KEY_ENV_VARS.get(provider)}. "
                    "Silent fallback to mock is strictly disabled for live runs."
                )
            logger.warning(
                f"No API key detected for provider '{provider}'. Falling back to mock/offline mode."
            )
            self.provider = "mock"

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1500,
    ) -> str:
        """Execute generation using the configured provider."""
        if self.provider == "mock":
            return self._mock_generate(system_prompt, user_prompt)
        elif self.provider in ["openai", "xai", "deepseek", "qwen", "glm"]:
            return self._call_openai_compatible(
                system_prompt, user_prompt, temperature, max_tokens
            )
        elif self.provider == "anthropic":
            return self._call_anthropic(
                system_prompt, user_prompt, temperature, max_tokens
            )
        elif self.provider == "google":
            return self._call_google(
                system_prompt, user_prompt, temperature, max_tokens
            )
        else:
            raise ValueError(f"Provider '{self.provider}' has no execution handler.")

    def _call_openai_compatible(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        base_url = API_BASE_URLS[self.provider]
        url = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error(f"Error calling {self.provider} API: {e}")
            raise RuntimeError(f"{self.provider} API call failed: {e}")

    def _call_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        url = API_BASE_URLS["anthropic"]
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"].strip()
        except Exception as e:
            logger.error(f"Error calling Anthropic API: {e}")
            raise RuntimeError(f"Anthropic API call failed: {e}")

    def _call_google(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        base_url = API_BASE_URLS["google"]
        url = f"{base_url}/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
            raise ValueError(f"No content returned from Google API: {data}")
        except Exception as e:
            logger.error(f"Error calling Google API: {e}")
            raise RuntimeError(f"Google API call failed: {e}")

    def _mock_generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Deterministic mock responses for testing, dry runs, and offline auditing.
        Parses the role from system_prompt to simulate conservative research outputs.
        """
        prompt_lower = system_prompt.lower()

        # 1. Literature Scanner
        if "literature scanner" in prompt_lower:
            return json.dumps({
                "relevance": "Direct empirical study evaluating cognitive forcing functions and automation bias under generative AI assistance.",
                "trigger_status": "DIRECT",
                "target_lane": "HAI-Interaction",
                "notes": "Directly bears on calibrated trust and override accuracy in human-AI interaction."
            })

        # 2. Psychometrics Analyst
        elif "psychometrics analyst" in prompt_lower:
            return (
                "**Psychometrics Brief**\n\n"
                "**Construct Validity Assessment:** The paper evaluates behavioral reliance and decision quality "
                "under automated recommendations. It does not introduce a novel general psychological faculty, but "
                "measures task-specific reliance behavior.\n\n"
                "**Redundancy Audit:** Findings align with existing calibrated trust paradigms (Lee & See, 2004) "
                "and confirmation bias literature. No change to foundational Tier 1 cognitive substrate definitions.\n\n"
                "**Evidence Tier Rating:** Validated via randomized controlled trial with behavioral metrics. "
                "Supports maintaining 'Strong' tier for cognitive forcing functions mitigating over-reliance.\n\n"
                "**Impact Status:** POSSIBLE IMPACT — flag for debate"
            )

        # 3. HAI-Interaction Analyst
        elif "hai-interaction analyst" in prompt_lower:
            return (
                "**HAI-Interaction Brief**\n\n"
                "**Core Mechanism:** Evaluates how cognitive forcing functions (forcing an independent decision before "
                "revealing AI output) reduce automation bias and over-reliance.\n\n"
                "**Connection to Lineage:** Directly confirms the Buçinca et al. (2021) and Bansal et al. (2021) lineage: "
                "passive transparency does not reliably prevent over-reliance, whereas cognitive friction compels analytical verification.\n\n"
                "**Evidence Tier Assessment:** Replicates across controlled experimental tasks. Confirms that interface design "
                "moderates reliance ratios in generative collaboration.\n\n"
                "**Impact Status:** DIRECT IMPACT — cites row on cognitive forcing functions and automation bias reliance ratio"
            )

        # 4. Cross-Cultural Methods Analyst
        elif "cross-cultural methods analyst" in prompt_lower:
            return (
                "**Cross-Cultural Methods Brief**\n\n"
                "**Sample Demographics:** The experimental sample was drawn primarily from online crowdsourcing platforms "
                "(Prolific/MTurk) with predominantly US and Western participants.\n\n"
                "**Generalizability Limit:** The findings cannot be assumed to generalize across non-WEIRD populations without "
                "measurement invariance testing (configural, metric, scalar). Autonomy under automated advice reflects individualist norms.\n\n"
                "**Evidence Tier Assessment:** Generalization remains restricted to educated, digital-native Western cohorts.\n\n"
                "**Impact Status:** POSSIBLE IMPACT — flag for debate"
            )

        # 5. Governance/Ethics Analyst
        elif "governance" in prompt_lower and "ethics" in prompt_lower:
            return (
                "**Governance & Ethics Brief**\n\n"
                "**Accountability Laundering Audit:** The study tests human user decision behavior. There is a structural risk "
                "that these findings could be misconstrued to blame users for automation failures rather than requiring model developers "
                "to eliminate deceptive fluency.\n\n"
                "**Safeguard Requirement:** Any repository update incorporating this evidence must reiterate that user-side forcing "
                "functions complement, but never substitute for, model alignment, red-teaming, and regulatory liability.\n\n"
                "**Impact Status:** DIRECT IMPACT — cites Objection 11 (Responsibility Laundering)"
            )

        # 6. Debate Team: Proponent
        elif "proponent in the hsri construct debate team" in prompt_lower or "debate proponent" in prompt_lower:
            return (
                "**Proponent Argument**\n\n"
                "The evidence directly reinforces our core thesis that the only real research gap is the *interaction effect* under "
                "asymmetric AI assistance. As both the HAI and Psychometrics briefs note, general cognitive reflection does not prevent "
                "automation bias when a fluent model presents incorrect advice. The finding that cognitive forcing functions reduce over-reliance "
                "demonstrates that interaction-specific cognitive friction explains variance that baseline traits miss. We should propose an "
                "explicit diff updating the evidence table to incorporate this replication and strengthen the experimental grounding in Section 5."
            )

        # 7. Debate Team: Skeptic
        elif "skeptic in the hsri construct debate team" in prompt_lower or "debate skeptic" in prompt_lower:
            return (
                "**Skeptic Argument**\n\n"
                "The Proponent is over-reading the novelty of this result. The paper demonstrates an interface intervention effect, "
                "not an endogenous human psychological faculty. As the Psychometrics Analyst conceded, this remains fully consistent with "
                "established automation-bias research (Mosier & Skitka, 1996; Parasuraman et al., 2000). Furthermore, as the Cross-Cultural "
                "Analyst flagged, the sample is entirely WEIRD-restricted. Claiming this validates a distinct 'AI readiness' construct is premature. "
                "Any proposed diff must be strictly confined to updating existing literature citations without declaring construct novelty."
            )

        # 8. Systematic Review Synthesizer
        elif "systematic review synthesizer" in prompt_lower or "synthesizer" in prompt_lower:
            return (
                "**Synthesizer Verdict: PROPOSED DIFF**\n\n"
                "**Reasoning:** The debate demonstrated consensus on empirical replication of cognitive forcing functions, while "
                "the Skeptic's objection against claiming construct novelty is fully sustained. The diff is restricted to updating "
                "the empirical citation matrix in `evidence/master-evidence-table.csv` and cross-referencing in `docs/05-measurement-and-experiments.md` "
                "without altering construct definitions.\n\n"
                "**Proposed Diff:**\n"
                "```diff\n"
                "--- a/evidence/master-evidence-table.csv\n"
                "+++ b/evidence/master-evidence-table.csv\n"
                "+Replication: Cognitive forcing functions reduce overreliance on AI recommendations,docs/05-measurement-and-experiments.md,Strong,Buçinca et al. (2021) / Replications,https://doi.org/10.1145/3449287,Replicated finding confirming that forced deliberation mitigates automation bias.\n"
                "```\n\n"
                "**Required Caveats:** Note explicit sample limitation (WEIRD cohorts only) and reinforce that cognitive forcing is an interface intervention, not an individual trait."
            )

        # 9. Review Board Seats
        elif "adversarial skeptic" in prompt_lower:
            return (
                "**Seat 1: Adversarial Skeptic Verdict**\n\n"
                "**Verdict:** APPROVE\n"
                "**Reasoning:** The Synthesizer did not soften the Skeptic's objections; the proposed diff is strictly bounded to an "
                "empirical replication citation and avoids construct-reification language. Precision is bounded strictly to documented findings."
            )
        elif "cross-cultural methodologist" in prompt_lower:
            return (
                "**Seat 2: Cross-Cultural Methodologist Verdict**\n\n"
                "**Verdict:** APPROVE\n"
                "**Reasoning:** The synthesis explicitly includes the necessary qualification restricting generalizability to WEIRD "
                "online crowdsourced samples and notes that cross-cultural invariance remains unproven."
            )
        elif "accountability-laundering reviewer" in prompt_lower:
            return (
                "**Seat 3: Accountability-Laundering Reviewer Verdict**\n\n"
                "**Verdict:** APPROVE\n"
                "**Reasoning:** The synthesis preserves the requirement that interface-level cognitive friction does not shift liability "
                "away from model developers or substitute for system alignment. Guardrail maintained."
            )

        # Default fallback
        return "NO CHANGE — evidence insufficient. Analysis indicates no statistically robust evidence-table impact."
