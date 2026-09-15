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

def reconstruct_abstract(inv: Optional[Dict[str, List[int]]]) -> str:
    """Reconstruct abstract from OpenAlex inverted index format."""
    if not inv:
        return ""
    words = []
    for word, positions in inv.items():
        for pos in positions:
            words.append((pos, word))
    words.sort(key=lambda x: x[0])
    return " ".join([w[1] for w in words])

def query_openalex(keywords: List[str], days: int = 30, max_results: int = 5) -> List[Dict[str, Any]]:
    """Query OpenAlex API for recent works matching evidence table keywords."""
    hits: List[Dict[str, Any]] = []
    today = datetime.date.today()
    from_date = (today - datetime.timedelta(days=days)).isoformat()
    
    # Clean and combine primary keywords
    search_phrase = " OR ".join([f'"{k}"' for k in keywords[:3]])
    encoded = urllib.parse.quote(search_phrase)
    url = f"https://api.openalex.org/works?search={encoded}&filter=from_publication_date:{from_date}&per_page={max_results}&sort=publication_date:desc"
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "HSRI-Agents-Research-Bot/0.1.0 (mailto:research@hsri.org)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        for r in data.get("results", []):
            title = r.get("title") or "Untitled"
            pub_date = r.get("publication_date") or str(today)
            doi = r.get("doi") or r.get("id") or ""
            authors = [
                a.get("author", {}).get("display_name", "")
                for a in r.get("authorships", [])
                if a.get("author", {}).get("display_name")
            ]
            venue = (
                r.get("primary_location", {}).get("source", {}).get("display_name")
                if r.get("primary_location") and r.get("primary_location", {}).get("source")
                else "OpenAlex"
            )
            abstract = reconstruct_abstract(r.get("abstract_inverted_index"))
            clean_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", doi.split("/")[-1] if doi else f"oa_{len(hits)+1}")
            
            hits.append({
                "id": clean_id,
                "title": title,
                "authors": authors,
                "venue": venue,
                "date": pub_date,
                "abstract": abstract,
                "url_or_doi": doi,
                "source_api": "OpenAlex",
            })
    except Exception as e:
        logger.warning(f"OpenAlex query failed: {e}")
        
    return hits

def query_arxiv(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Query the official arXiv API for recent papers."""
    encoded_query = urllib.parse.quote(query)
    url = (
        f"https://export.arxiv.org/api/query?"
        f"search_query=all:{encoded_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    )

    hits: List[Dict[str, Any]] = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HSRI-Agents-Research-Bot/0.1.0 (mailto:research@hsri.org)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
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
                "source_api": "arXiv",
            })
    except Exception as e:
        logger.warning(f"arXiv API query failed or timed out: {e}")

    return hits

def scan_literature(
    provider: str = "mock",
    query: Optional[str] = None,
    days: int = 30,
    max_results: int = 5,
    seed_paper: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Execute a manual literature scan pass.
    Writes candidate hits to scan-log/ directory.
    """
    ensure_directories()

    candidates: List[Dict[str, Any]] = []

    if seed_paper:
        candidates.append(seed_paper)
    else:
        keywords = [query] if query else extract_keywords_from_evidence_table()
        
        # 1. First attempt OpenAlex (reliable, fast, date-bounded)
        oa_hits = query_openalex(keywords, days=days, max_results=max_results)
        candidates.extend(oa_hits)
        
        # 2. Also query arXiv if fewer than max_results
        if len(candidates) < max_results:
            search_term = " OR ".join([f'"{k}"' for k in keywords[:3]])
            arxiv_hits = query_arxiv(search_term, max_results=max_results - len(candidates))
            candidates.extend(arxiv_hits)

    scan_results = []
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # Initialize LLM if key is present or in mock mode
    llm = None
    try:
        llm = LLMClient(provider=provider, allow_fallback=(provider == "mock"))
    except Exception as e:
        logger.info(f"Scanner operating without LLM generation for provider '{provider}': {e}")

    for hit in candidates:
        if llm:
            user_prompt = (
                f"Title: {hit['title']}\n"
                f"Authors: {', '.join(hit.get('authors', []))}\n"
                f"Venue: {hit.get('venue', 'Unknown')}\n"
                f"Date: {hit.get('date', 'Unknown')}\n\n"
                f"Abstract:\n{hit.get('abstract', '')}\n"
            )
            try:
                response_text = llm.generate(SCANNER_SYSTEM_PROMPT, user_prompt)
                parsed = json.loads(response_text)
            except Exception:
                parsed = {
                    "relevance": "Matched keywords in candidate abstract.",
                    "trigger_status": "POSSIBLE" if "calibrated trust" in hit.get("abstract", "").lower() or "automation bias" in hit.get("abstract", "").lower() else "NO_TRIGGER",
                    "target_lane": "HAI-Interaction",
                    "notes": "Extracted via candidate heuristic."
                }
        else:
            # Deterministic keyword scanner matching
            text_lower = (hit["title"] + " " + hit.get("abstract", "")).lower()
            if any(k in text_lower for k in ["automation bias", "cognitive forcing", "calibrated trust", "overreliance", "effort opacity"]):
                trigger = "DIRECT"
                lane = "HAI-Interaction"
                rel = "Direct empirical intersection with HAI interaction and trust/reliance mechanisms."
            elif any(k in text_lower for k in ["metacognit", "intellectual humility", "construct validity", "invariance"]):
                trigger = "POSSIBLE"
                lane = "Psychometrics"
                rel = "Plausible intersection with cognitive or psychometric substrate."
            else:
                trigger = "NO_TRIGGER"
                lane = "General"
                rel = "General AI literature without direct evidence-table construct metrics."

            parsed = {
                "relevance": rel,
                "trigger_status": trigger,
                "target_lane": lane,
                "notes": f"Scanned via {hit.get('source_api', 'OpenAlex')}."
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
