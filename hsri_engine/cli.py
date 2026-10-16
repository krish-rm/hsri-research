"""
hsri_engine.cli - Command Line Interface for HSRI Engine Core
"""

import sys
import argparse
import json
from pathlib import Path

from hsri_engine import __version__
from hsri_engine.models import EvaluationRequest, PillarInput
from hsri_engine.core import evaluate_profile


def main():
    parser = argparse.ArgumentParser(
        prog="hsri-engine",
        description="HSRI 2.0 Engine Core CLI & Evaluation Toolkit",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Launch FastAPI REST server")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    serve_parser.add_argument("--reload", action="store_true", help="Enable autoreload for development")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate a national or corporate profile")
    eval_parser.add_argument("--id", default="custom-eval", help="Entity ID")
    eval_parser.add_argument("--name", default="Custom Node", help="Entity name")
    eval_parser.add_argument("--p1", type=float, default=0.5, help="P1: AI Literacy [0, 1]")
    eval_parser.add_argument("--p2", type=float, default=0.5, help="P2: Critical Discernment [0, 1]")
    eval_parser.add_argument("--p3", type=float, default=0.5, help="P3: Institutional Governance [0, 1]")
    eval_parser.add_argument("--p4", type=float, default=0.5, help="P4: Digital Infrastructure [0, 1]")
    eval_parser.add_argument("--p5", type=float, default=0.5, help="P5: Epistemic Inviolability [0, 1]")
    eval_parser.add_argument("--p6", type=float, default=0.5, help="P6: Decoupling Half-Life [0, 1]")
    eval_parser.add_argument("--p7", type=float, default=0.5, help="P7: Coordination Velocity [0, 1]")
    eval_parser.add_argument("--p8", type=float, default=0.5, help="P8: Post-Labor Elasticity [0, 1]")
    eval_parser.add_argument("--decay", action="store_true", help="Apply negative cross-elasticity decay")
    eval_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Reinsurance sub-command
    reins_parser = subparsers.add_parser("reinsurance", help="Actuarial reinsurance pricing & syndicate slip generator")
    reins_subparsers = reins_parser.add_subparsers(dest="reinsurance_subcommand", help="Reinsurance actions")

    slip_parser = reins_subparsers.add_parser("slip", help="Generate Lloyd's Syndicate Slip & Treaty Term Sheet")
    slip_parser.add_argument("--archetype", "-a", choices=["A", "B", "C", "archetype_a", "archetype_b", "archetype_c"], default="A", help="Sovereign Risk Archetype (A: Tech Hub, B: Continental, C: Decentralized)")
    slip_parser.add_argument("--tiv", "-t", type=float, default=10.0, help="Total Insured Valuation in USD Billion (default: 10.0)")
    slip_parser.add_argument("--output", "-o", default=None, help="Destination markdown filepath")
    slip_parser.add_argument("--json", action="store_true", help="Output raw actuarial pricing JSON instead of Markdown")

    # Export openapi
    export_parser = subparsers.add_parser("export-openapi", help="Export OpenAPI JSON schema to a file")
    export_parser.add_argument("--output", default="openapi.json", help="Destination path for OpenAPI JSON")

    args = parser.parse_args()

    if args.command == "serve":
        import uvicorn
        print(f"Starting HSRI 2.0 Engine API server on {args.host}:{args.port}...")
        uvicorn.run("hsri_engine.api:app", host=args.host, port=args.port, reload=args.reload)

    elif args.command == "evaluate":
        req = EvaluationRequest(
            entity_id=args.id,
            entity_name=args.name,
            pillars=PillarInput(
                p1=args.p1, p2=args.p2, p3=args.p3, p4=args.p4,
                p5=args.p5, p6=args.p6, p7=args.p7, p8=args.p8,
            ),
            apply_negative_cross_elasticity=args.decay,
        )
        resp = evaluate_profile(req)
        if args.json:
            print(resp.model_dump_json(indent=2))
        else:
            print("=======================================================")
            print(f" HSRI 2.0 EVALUATION: {resp.entity_name} ({resp.entity_id})")
            print("=======================================================")
            print(f"Layer 1 Adoption (Linear):          {resp.layer1_score:.4f}")
            print(f"Layer 2 Sovereignty (Leontief):     {resp.layer2_score:.4f}")
            print(f"Geometric Mean Score:               {resp.geometric_score:.4f}")
            print(f"Choquet 2-Additive Score:           {resp.choquet_score:.4f}")
            print(f"Master ASI Vulnerability Index:     {resp.master_vulnerability_index:.4f}")
            print(f"High-Compute Trap Detected:         {resp.is_high_compute_trap}")
            print(f"Weakest-Link Governing Pillar:      {resp.weakest_link_pillar} ({resp.weakest_link_score:.4f})")
            print("=======================================================")

    elif args.command == "reinsurance":
        if args.reinsurance_subcommand == "slip":
            from hsri_engine.reinsurance import calculate_reinsurance_pricing, generate_syndicate_slip_markdown
            pricing = calculate_reinsurance_pricing(args.archetype, tiv_billion=args.tiv)
            if args.json:
                print(json.dumps(pricing, indent=2))
            else:
                slip_md = generate_syndicate_slip_markdown(pricing)
                if args.output:
                    out_p = Path(args.output)
                    out_p.parent.mkdir(parents=True, exist_ok=True)
                    out_p.write_text(slip_md, encoding="utf-8")
                    print(f"Exported Lloyd's Syndicate Slip to {out_p.resolve()}")
                else:
                    print(slip_md)
        else:
            reins_parser.print_help()

    elif args.command == "export-openapi":
        from hsri_engine.api import app
        schema = app.openapi()
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2)
        print(f"Exported OpenAPI schema to {out_path.resolve()}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
