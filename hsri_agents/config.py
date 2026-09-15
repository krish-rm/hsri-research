"""
Configuration for HSRI-Agents.

Defines supported model providers, API endpoints, environment variable bindings,
and repository file paths.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

# Root directory of the repository
REPO_ROOT = Path(__file__).resolve().parent.parent

# Core repository paths
EVIDENCE_TABLE_PATH = REPO_ROOT / "evidence" / "master-evidence-table.csv"
SCAN_LOG_DIR = REPO_ROOT / "scan-log"
RESEARCH_MEMORY_PATH = REPO_ROOT / "research_memory.md"
MODEL_DIVERGENCE_LOG_PATH = REPO_ROOT / "model-divergence-log.csv"
DOCS_DIR = REPO_ROOT / "docs"

# Real frontier ensemble providers (Section 5: 7 independent families)
REAL_ENSEMBLE_PROVIDERS: List[str] = [
    "anthropic",     # Claude
    "openai",        # GPT
    "google",        # Gemini
    "xai",           # Grok
    "deepseek",      # DeepSeek
    "qwen",          # Alibaba DashScope
    "glm",           # Zhipu AI
]

# Test/offline fallback provider (strictly excluded from real ensemble counts and divergence aggregation)
TEST_FALLBACK_PROVIDERS: List[str] = [
    "mock",
]

# All supported runtime targets (real ensemble + offline test harness)
SUPPORTED_PROVIDERS: List[str] = REAL_ENSEMBLE_PROVIDERS + TEST_FALLBACK_PROVIDERS

# Default model per provider
DEFAULT_MODELS: Dict[str, str] = {
    "anthropic": "claude-3-5-sonnet-20241022",
    "openai": "gpt-4o",
    "google": "gemini-1.5-pro",
    "xai": "grok-2-latest",
    "deepseek": "deepseek-chat",
    "qwen": "qwen-plus",
    "glm": "glm-4",
    "mock": "mock-conservative-evaluator",
}

# Environment variable keys
API_KEY_ENV_VARS: Dict[str, List[str]] = {
    "anthropic": ["ANTHROPIC_API_KEY"],
    "openai": ["OPENAI_API_KEY"],
    "google": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
    "xai": ["XAI_API_KEY"],
    "deepseek": ["DEEPSEEK_API_KEY"],
    "qwen": ["DASHSCOPE_API_KEY", "QWEN_API_KEY"],
    "glm": ["ZHIPUAI_API_KEY", "GLM_API_KEY"],
    "mock": [],
}

# Base URLs for OpenAI-compatible and REST endpoints
API_BASE_URLS: Dict[str, str] = {
    "openai": "https://api.openai.com/v1",
    "xai": "https://api.x.ai/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "glm": "https://open.bigmodel.cn/api/paas/v4",
    "anthropic": "https://api.anthropic.com/v1/messages",
    "google": "https://generativelanguage.googleapis.com/v1beta/models",
}

def get_api_key(provider: str) -> Optional[str]:
    """Retrieve API key for the specified provider from environment variables."""
    if provider == "mock":
        return "mock-key"
    candidates = API_KEY_ENV_VARS.get(provider, [])
    for env_var in candidates:
        val = os.environ.get(env_var)
        if val:
            return val
    return None

def ensure_directories() -> None:
    """Ensure runtime directories exist."""
    SCAN_LOG_DIR.mkdir(parents=True, exist_ok=True)
