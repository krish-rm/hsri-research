"""
CLI Interface for HSRI-Agents.

Implements manual-first standalone commands for each role in the evidence-review pipeline:
  hsri-agents scan
  hsri-agents analyze --hit <id>
  hsri-agents debate --hit <id> [--rounds 2|3]
  hsri-agents synthesize --debate <id>
  hsri-agents review --diff <id>
  hsri-agents status
  hsri-agents run-all-manual --hit <id>
"""

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from hsri_agents.analysts import run_analysts
from hsri_agents.config import (
    DEFAULT_MODELS,
    RESEARCH_MEMORY_PATH,
    SCAN_LOG_DIR,
    SUPPORTED_PROVIDERS,
    ensure_directories,
)
from hsri_agents.debate import run_debate
from hsri_agents.logger import (
    initialize_ledgers,
    log_divergence_entry,
    log_research_memory_entry,
)
from hsri_agents.review_board import run_review_board
from hsri_agents.scanner import scan_literature
from hsri_agents.synthesizer import run_synthesizer

def find_json_record(prefix: str, identifier: str) -> Optional[Dict[str, Any]]:
    """Locate a JSON record in scan-log by prefix and identifier."""
    ensure_directories()
    for file_path in SCAN_LOG_DIR.glob(f"{prefix}*.json"):
        if identifier in file_path.name:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                continue
    return None

def save_json_record(prefix: str, identifier: str, data: Dict[str, Any]) -> Path:
    """Save an intermediate stage record to scan-log/."""
    ensure_directories()
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = SCAN_LOG_DIR / f"{prefix}_{identifier}_{timestamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path

# ----------------------------------------------------------------------
# CLI Subcommands
# ----------------------------------------------------------------------

def cmd_scan(args: argparse.Namespace) -> None:
    print(f"\n[Literature Scanner] Initiating manual literature scan using provider: {args.provider.upper()}...")
    hits = scan_literature(provider=args.provider, query=args.query, max_results=args.max_results)

    print(f"\n[Scanner Results] Processed {len(hits)} candidate items:")
    for h in hits:
        status_badge = f"[{h.get('trigger_status')}]"
        print(f"\n- ID: {h.get('id')}")
        print(f"  Title: {h.get('title')}")
        print(f"  Status: {status_badge} (Lane: {h.get('target_lane')})")
        print(f"  Relevance: {h.get('relevance_note')}")

    print(f"\nCandidate records saved in: {SCAN_LOG_DIR}")
    print("\nNext manual step:")
    print("  Review the hits above. If a hit warrants evaluation, run:")
    print("  python -m hsri_agents analyze --hit <id>\n")

def cmd_analyze(args: argparse.Namespace) -> None:
    hit_id = args.hit
    print(f"\n[Evidence Analysts] Loading hit '{hit_id}'...")
    hit = find_json_record("hit_", hit_id)
    if not hit:
        print(f"ERROR: No hit record matching '{hit_id}' found in {SCAN_LOG_DIR}.")
        sys.exit(1)

    print(f"Target: \"{hit.get('title')}\"")
    print(f"Running 4 parallel analysts using provider: {args.provider.upper()}...\n")

    result = run_analysts(hit, provider=args.provider)
    save_json_record("analysis", hit_id, result)

    for lane, brief in result["briefs"].items():
        print(f"==================================================")
        print(f"{lane.upper().replace('_', ' ')} BRIEF — {brief['impact_status']}")
        print(f"==================================================")
        print(brief["brief_text"].strip())
        print()

    print(f"Overall Evidence Impact: {result['overall_impact']}")
    print(f"Eligible for Debate: {'YES' if result['eligible_for_debate'] else 'NO'}")
    print(f"\nAnalysis saved to {SCAN_LOG_DIR}")

    if result["eligible_for_debate"]:
        print("\nNext manual step:")
        print(f"  python -m hsri_agents debate --hit {hit_id}\n")
    else:
        print("\nNo further action required. This hit does not warrant convening the debate team.")

def cmd_debate(args: argparse.Namespace) -> None:
    hit_id = args.hit
    print(f"\n[Construct Debate Team] Loading analysis for hit '{hit_id}'...")
    hit = find_json_record("hit_", hit_id)
    analysis = find_json_record("analysis_", hit_id)

    if not hit:
        print(f"ERROR: Hit record '{hit_id}' not found.")
        sys.exit(1)
    if not analysis:
        print(f"ERROR: No analysis record found for '{hit_id}'. Please run 'analyze --hit {hit_id}' first.")
        sys.exit(1)

    print(f"Convening {args.rounds}-round adversarial debate using provider: {args.provider.upper()}...\n")
    result = run_debate(hit, analysis, rounds=args.rounds, provider=args.provider)
    save_json_record("debate", hit_id, result)

    for turn in result["transcript"]:
        print(f"--------------------------------------------------")
        print(f"Round {turn['round']} — {turn['speaker']}")
        print(f"--------------------------------------------------")
        print(turn["content"].strip())
        print()

    print(f"\nFull debate transcript retained in {SCAN_LOG_DIR}")
    print("\nNext manual step:")
    print(f"  python -m hsri_agents synthesize --debate {hit_id}\n")

def cmd_synthesize(args: argparse.Namespace) -> None:
    debate_id = args.debate
    print(f"\n[Review Synthesizer] Loading debate transcript for '{debate_id}'...")
    hit = find_json_record("hit_", debate_id)
    debate = find_json_record("debate_", debate_id)

    if not hit or not debate:
        print(f"ERROR: Debate transcript for '{debate_id}' not found.")
        sys.exit(1)

    print(f"Synthesizing debate using provider: {args.provider.upper()}...\n")
    result = run_synthesizer(hit, debate, provider=args.provider)
    save_json_record("synthesis", debate_id, result)

    print(f"==================================================")
    print(f"SYNTHESIZER VERDICT: {result['verdict']}")
    print(f"==================================================")
    print(result["synthesis_text"].strip())
    print()

    print(f"\nSynthesis saved to {SCAN_LOG_DIR}")
    if result["has_diff"]:
        print("\nNext manual step:")
        print(f"  python -m hsri_agents review --diff {debate_id}\n")
    else:
        print("\nVerdict is NO CHANGE. No Review Board session required.")

def cmd_review(args: argparse.Namespace) -> None:
    diff_id = args.diff
    print(f"\n[Consortium Review Board] Loading synthesis for '{diff_id}'...")
    hit = find_json_record("hit_", diff_id)
    analysis = find_json_record("analysis_", diff_id)
    debate = find_json_record("debate_", diff_id)
    synthesis = find_json_record("synthesis_", diff_id)

    if not hit or not synthesis:
        print(f"ERROR: Synthesis record for '{diff_id}' not found.")
        sys.exit(1)

    print(f"Convening 3-Seat Consortium Review Board using provider: {args.provider.upper()}...\n")
    result = run_review_board(hit, synthesis, provider=args.provider)
    save_json_record("review", diff_id, result)

    for seat_id, s in result["seats"].items():
        print(f"--------------------------------------------------")
        print(f"SEAT: {seat_id.upper().replace('_', ' ')} — {s['verdict']}")
        print(f"--------------------------------------------------")
        print(s["evaluation_text"].strip())
        print()

    print(f"==================================================")
    print(f"BOARD RESULT: Approvals: {result['approvals']}/3 | Rejections: {result['rejections']}/3")
    print(f"PR READINESS: {'READY FOR HUMAN REVIEW' if result['is_approved'] else 'BLOCKED / REJECTED'}")
    print(f"==================================================")

    # Determine divergence verdict label
    divergence_label = "diff-proposed" if result["is_approved"] else ("rejected-at-board" if synthesis["has_diff"] else "no-change")

    # Log to durable ledgers
    paper_title = hit.get("title", diff_id)
    log_research_memory_entry(
        hit=hit,
        provider=args.provider,
        analysts_result=analysis or {"briefs": {}},
        debate_result=debate or {"full_dialogue_text": ""},
        synthesizer_result=synthesis,
        review_board_result=result,
        pr_status="Ready for human git branch & PR staging" if result["is_approved"] else "Blocked by Review Board",
    )
    log_divergence_entry(
        triggering_paper=paper_title,
        provider=args.provider,
        verdict=divergence_label,
        notes=f"Approvals: {result['approvals']}/3, Rejections: {result['rejections']}/3",
    )

    print(f"\nDurable audit trail updated:")
    print(f"  - {RESEARCH_MEMORY_PATH}")
    print(f"  - Model Divergence Log: model-divergence-log.csv")

    if result["is_approved"]:
        print("\n[ACTION REQUIRED BY HUMAN MAINTAINER]:")
        print("  All 3 Review Board seats approved the proposed diff.")
        print("  Per Section 0.1, the system does not auto-merge or push.")
        print("  You may now inspect the diff above, stage changes on a branch, and open a PR manually.")
    else:
        print("\nReview Board vetoed the proposed diff. PR readiness halted.")

def cmd_run_all_manual(args: argparse.Namespace) -> None:
    """Interactive step-by-step runner with human confirmation pauses."""
    hit_id = args.hit
    provider = args.provider
    print(f"\n=======================================================")
    print(f"  HSRI-Agents: Manual Multi-Step Pipeline Execution")
    print(f"  Target Hit ID: {hit_id} | Provider: {provider.upper()}")
    print(f"=======================================================\n")

    # Step 1: Analyze
    cmd_analyze(argparse.Namespace(hit=hit_id, provider=provider))
    analysis = find_json_record("analysis_", hit_id)
    if not analysis or not analysis.get("eligible_for_debate"):
        print("\nPipeline stopped: Hit not eligible for debate.")
        return

    # Step 2: Debate
    cmd_debate(argparse.Namespace(hit=hit_id, rounds=args.rounds, provider=provider))

    # Step 3: Synthesize
    cmd_synthesize(argparse.Namespace(debate=hit_id, provider=provider))
    synthesis = find_json_record("synthesis_", hit_id)
    if not synthesis or not synthesis.get("has_diff"):
        print("\nPipeline concluded: Synthesizer issued NO CHANGE verdict.")
        return

    # Step 4: Review Board
    cmd_review(argparse.Namespace(diff=hit_id, provider=provider))

def cmd_status(args: argparse.Namespace) -> None:
    """Print current repository agent status."""
    ensure_directories()
    hits = list(SCAN_LOG_DIR.glob("hit_*.json"))
    analyses = list(SCAN_LOG_DIR.glob("analysis_*.json"))
    debates = list(SCAN_LOG_DIR.glob("debate_*.json"))
    reviews = list(SCAN_LOG_DIR.glob("review_*.json"))

    print("\n=== HSRI-Agents Operational Status ===")
    print(f"Rollout Mode: MANUAL-FIRST (All schedulers/cron/webhooks disabled)")
    print(f"Configured Providers: {', '.join(SUPPORTED_PROVIDERS)}")
    print(f"Scan Log Directory: {SCAN_LOG_DIR}")
    print(f"Total Cached Scan Hits: {len(hits)}")
    print(f"Completed Analyses: {len(analyses)}")
    print(f"Convened Debates: {len(debates)}")
    print(f"Completed Review Board Sessions: {len(reviews)}")
    print(f"Audit Trail: {RESEARCH_MEMORY_PATH} ({'Exists' if RESEARCH_MEMORY_PATH.exists() else 'Not initialized'})")
    print("======================================\n")

# ----------------------------------------------------------------------
# Entry Point
# ----------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hsri-agents",
        description="HSRI-Agents: Evidence-review and adversarial multi-agent debate pipeline.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Agent action to execute")

    # scan
    p_scan = subparsers.add_parser("scan", help="Scan literature repositories for construct matches")
    p_scan.add_argument("--query", type=str, default=None, help="Specific search query override")
    p_scan.add_argument("--max-results", type=int, default=5, help="Max candidates to retrieve")
    p_scan.add_argument("--provider", type=str, default="mock", choices=SUPPORTED_PROVIDERS, help="LLM provider")

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="Run 4 parallel analysts on a candidate hit")
    p_analyze.add_argument("--hit", type=str, required=True, help="Target hit ID in scan-log/")
    p_analyze.add_argument("--provider", type=str, default="mock", choices=SUPPORTED_PROVIDERS, help="LLM provider")

    # debate
    p_debate = subparsers.add_parser("debate", help="Convene Proponent vs. Skeptic debate on an analyzed hit")
    p_debate.add_argument("--hit", type=str, required=True, help="Target hit ID")
    p_debate.add_argument("--rounds", type=int, default=2, choices=[1, 2, 3], help="Debate rounds")
    p_debate.add_argument("--provider", type=str, default="mock", choices=SUPPORTED_PROVIDERS, help="LLM provider")

    # synthesize
    p_synthesize = subparsers.add_parser("synthesize", help="Run review synthesizer on debate transcript")
    p_synthesize.add_argument("--debate", type=str, required=True, help="Target debate/hit ID")
    p_synthesize.add_argument("--provider", type=str, default="mock", choices=SUPPORTED_PROVIDERS, help="LLM provider")

    # review
    p_review = subparsers.add_parser("review", help="Convene 3-seat Consortium Review Board on synthesized diff")
    p_review.add_argument("--diff", type=str, required=True, help="Target synthesis/hit ID")
    p_review.add_argument("--provider", type=str, default="mock", choices=SUPPORTED_PROVIDERS, help="LLM provider")

    # run-all-manual
    p_all = subparsers.add_parser("run-all-manual", help="Run complete pipeline sequentially on a hit with manual logs")
    p_all.add_argument("--hit", type=str, required=True, help="Target hit ID")
    p_all.add_argument("--rounds", type=int, default=2, choices=[1, 2, 3], help="Debate rounds")
    p_all.add_argument("--provider", type=str, default="mock", choices=SUPPORTED_PROVIDERS, help="LLM provider")

    # status
    subparsers.add_parser("status", help="Show system status and cached log statistics")

    return parser

def main() -> None:
    initialize_ledgers()
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "scan": cmd_scan,
        "analyze": cmd_analyze,
        "debate": cmd_debate,
        "synthesize": cmd_synthesize,
        "review": cmd_review,
        "run-all-manual": cmd_run_all_manual,
        "status": cmd_status,
    }

    func = dispatch.get(args.command)
    if func:
        func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
