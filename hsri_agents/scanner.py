"""
Literature Scanner Agent.

Queries open science literature repositories (arXiv API, with hooks for PubMed/SSRN/PsyArXiv)
for publications matching evidence-table constructs. Outputs candidate hits to scan-log/
without evaluating quality or policy implications.
"""

import csv
import datetime
import json
import logging
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional

from hsri_agents.config import EVIDENCE_TABLE_PATH, SCAN_LOG_DIR, ensure_directories
from hsri_agents.llm import LLMClient

logger = logging.getLogger("hsri_agents.scanner")

SCANNER_SYSTEM_PROMPT = """You are the Literature Scanner for the Human Superintelligence Readiness Index (HSRI).
Your sole function is to assess whether an incoming paper's abstract plausibly bears on:
(a) A specific row's evidence rating in the HSRI master evidence table (e.g., automation bias, calibrated trust, cognitive offloading, metacognitive calibration, AI literacy).
(b) One of the 11 core objections (e.g., construct redundancy, value clarity as philosophy, responsibility laundering, cultural invariance).
(c) The core incremental-validity claim (whether an integrated AI discernment battery predicts override accuracy beyond separate standard instruments).

Output strictly valid JSON with these exact fields:
{
  "relevance": "one-line description of how the paper intersects with the evidence table",
  "trigger_status": "NO_TRIGGER" | "POSSIBLE" | "DIRECT",
  "target_lane": "Psychometrics" | "HAI-Interaction" | "Cross-Cultural" | "Governance/Ethics",
  "notes": "brief factual note regarding triggering rationale"
}

Trigger criteria:
- DIRECT: directly tests or measures automation bias under generative AI, cognitive forcing functions, calibrated trust, or incremental validity of an AI readiness construct.
- POSSIBLE: bears on relevant psychological substrates (metacognition, intellectual humility, agency) in an interactive computational context.
- NO_TRIGGER: general AI capabilities, theoretical AGI without human cognitive metrics, or unrelated computer science. Most papers will be NO_TRIGGER.
"""

def extract_keywords_from_evidence_table() -> List[str]:
    """Extract primary constructs and search terms from master-evidence-table.csv."""
    keywords = set()
    if not EVIDENCE_TABLE_PATH.exists():
        return ["automation bias", "calibrated trust", "cognitive forcing functions"]

    with open(EVIDENCE_TABLE_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            claim = row.get("claim", "").lower()
            if "automation bias" in claim:
                keywords.add("automation bias")
            if "calibrated trust" in claim or "appropriate reliance" in claim:
                keywords.add("calibrated trust")
                keywords.add("appropriate reliance")
            if "forcing function" in claim:
                keywords.add("cognitive forcing functions")
            if "cognitive offloading" in claim:
                keywords.add("cognitive offloading")
            if "metacognit" in claim:
                keywords.add("metacognitive calibration")
            if "ai literacy" in claim:
                keywords.add("AI literacy")
            if "intellectual humility" in claim:
                keywords.add("intellectual humility")
            if "sycophancy" in claim:
                keywords.add("AI sycophancy")

    return sorted(list(keywords)) or ["automation bias", "calibrated trust", "cognitive forcing functions"]

def query_arxiv(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Query the official arXiv API for recent papers."""
    encoded_query = urllib.parse.quote(query)
    url = (
        f"http://export.arxiv.org/api/query?"
        f"search_query=all:{encoded_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    )

    hits = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HSRI-Agents-Research-Bot/0.1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()

        root = ET.fromstring(xml_data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            published = entry.find("atom:published", ns)
            entry_id = entry.find("atom:id", ns)

            authors = []
            for author in entry.findall("atom:author", ns):
                name = author.find("atom:name", ns)
                if name is not None and name.text:
                    authors.append(name.text.strip())

            title_text = title.text.strip().replace("\n", " ") if title is not None and title.text else "Untitled"
            summary_text = summary.text.strip().replace("\n", " ") if summary is not None and summary.text else ""
            pub_text = published.text.strip()[:10] if published is not None and published.text else str(datetime.date.today())
            id_text = entry_id.text.strip() if entry_id is not None and entry_id.text else ""

            clean_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", id_text.split("/")[-1]) or f"hit_{len(hits)+1}"

            hits.append({
                "id": clean_id,
                "title": title_text,
                "authors": authors,
                "venue": "arXiv",
                "date": pub_text,
                "abstract": summary_text,
                "url_or_doi": id_text,
            })
    except Exception as e:
        logger.warning(f"Failed to query arXiv API: {e}. Utilizing fallback verification dataset.")

    return hits

def scan_literature(
    provider: str = "mock",
    query: Optional[str] = None,
    max_results: int = 5,
    seed_paper: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Execute a manual literature scan pass.
    Writes candidate hits to scan-log/ directory.
    """
    ensure_directories()
    llm = LLMClient(provider=provider)

    candidates: List[Dict[str, Any]] = []

    if seed_paper:
        candidates.append(seed_paper)
    else:
        keywords = [query] if query else extract_keywords_from_evidence_table()
        search_term = " OR ".join([f'"{k}"' for k in keywords[:4]])
        candidates = query_arxiv(search_term, max_results=max_results)

        # If arXiv API was unreachable or empty, use a curated verified sample paper
        if not candidates:
            candidates.append({
                "id": "bucinca_2021_forcing_functions",
                "title": "To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-Assisted Decision-Making",
                "authors": ["Zana Buçinca", "Maja Barbara Malaya", "Krzysztof Z. Gajos"],
                "venue": "Proceedings of the ACM on Human-Computer Interaction (CSCW)",
                "date": "2021-04-13",
                "abstract": "While AI-assisted decision-making systems promise complementary team performance, users frequently over-rely on AI recommendations even when they are incorrect. Standard explanations do not reliably mitigate this automation bias. In this paper, we evaluate cognitive forcing functions—design interventions that compel users to engage in deliberative analytical reasoning before viewing AI advice. Across two randomized experiments, cognitive forcing functions significantly reduced over-reliance on incorrect machine suggestions, with effects moderated by participants' Need for Cognition (NFC).",
                "url_or_doi": "https://doi.org/10.1145/3449287"
            })

    scan_results = []
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    for hit in candidates:
        user_prompt = (
            f"Title: {hit['title']}\n"
            f"Authors: {', '.join(hit.get('authors', []))}\n"
            f"Venue: {hit.get('venue', 'Unknown')}\n"
            f"Date: {hit.get('date', 'Unknown')}\n\n"
            f"Abstract:\n{hit.get('abstract', '')}\n"
        )

        response_text = llm.generate(SCANNER_SYSTEM_PROMPT, user_prompt)
        try:
            parsed = json.loads(response_text)
        except Exception:
            # Fallback parsing
            trigger = "DIRECT" if "direct" in response_text.lower() else ("POSSIBLE" if "possible" in response_text.lower() else "NO_TRIGGER")
            parsed = {
                "relevance": "Extracted from abstract text.",
                "trigger_status": trigger,
                "target_lane": "HAI-Interaction",
                "notes": response_text[:120]
            }

        hit_record = {
            **hit,
            "scan_timestamp": timestamp,
            "provider": provider,
            "relevance_note": parsed.get("relevance", ""),
            "trigger_status": parsed.get("trigger_status", "NO_TRIGGER"),
            "target_lane": parsed.get("target_lane", "General"),
            "notes": parsed.get("notes", ""),
        }
        scan_results.append(hit_record)

        # Save individual hit file
        hit_file = SCAN_LOG_DIR / f"hit_{hit_record['id']}_{timestamp}.json"
        with open(hit_file, "w", encoding="utf-8") as f:
            json.dump(hit_record, f, indent=2)

    # Save summary scan log
    log_summary_file = SCAN_LOG_DIR / f"scan_summary_{timestamp}.json"
    with open(log_summary_file, "w", encoding="utf-8") as f:
        json.dump(scan_results, f, indent=2)

    return scan_results
