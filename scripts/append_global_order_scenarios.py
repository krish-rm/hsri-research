#!/usr/bin/env python3
"""
append_global_order_scenarios.py - Appends SC-27 through SC-31 to asi_scenarios.json
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_JSON = REPO_ROOT / "site-astro" / "src" / "data" / "asi_scenarios.json"
PUB_JSON = REPO_ROOT / "site-astro" / "public" / "data" / "asi_scenarios.json"

NEW_SCENARIOS = [
    {
        "id": "SC-27",
        "name": "Post-Westphalian Compute Vassalage (decoupling of sovereign power from geographic borders, rise of cloud empires)",
        "question": "Can national sovereignty survive when a state's essential judicial, economic, and administrative infrastructure operates exclusively on foreign closed-weight frontier AI systems with non-zero revocation risk?",
        "mechanism": "Sovereign administrative capture occurs when the marginal productivity advantage of external frontier models induces complete domestic institutional lock-in. National regulatory oversight degrades into ceremonial theater because the host state lacks the compute, silicon fabrication, and algorithmic capability to replicate or inspect the model weights that govern its critical systems.",
        "failureMode": "Effective colonization of nominal nation-states into Epistemic Vassals, where national policy, resource distribution, and legal interpretation are covertly dictated or terminated by external hyperscale compute sovereigns.",
        "severity": "Severe to Existential (Permanent Loss of Democratic Sovereignty)",
        "reversibility": "Irreversible once domestic analog institutions and manual competencies atrophy",
        "status": "Empirically observable precursor phase (Class B) with rapid institutional entrenchment across G7 and developed digital states.",
        "relevance": "Deconstructs the Westphalian illusion: demonstrates that geographic borders and constitutional law are powerless against compute-weight subordination.",
        "matrix": {
            "capability_asymmetry": "Radically Superhuman (Hyperscale Cloud vs Sovereign Bureaucracy)",
            "speed_ratio": "Order-of-magnitude machine speed advantage over human parliamentary legislation",
            "autonomy_scope": "Full institutional administrative delegation",
            "coordination_structure": "Unipolar/Oligopolistic Compute Cartel"
        },
        "precursors": ["PREC-001", "PREC-002", "PREC-007"],
        "shortTitle": "Post-Westphalian Vassalage",
        "categoryTag": "Global Order Transition",
        "teaser": "What happens when nations run on models they cannot inspect or control? Geographic sovereignty dissolves into algorithmic vassalage to foreign compute empires.",
        "previewImage": "/assets/scenarios/sc-27-compute-vassalage.webp",
        "accentColor": "crimson",
        "visualPrompt": "editorial linocut scientific monograph plate, archival rag paper texture, precise carbon-ink crosshatching and stipple. A grand classical parliamentary building whose classical columns dissolve upward into towering server rack monoliths wired with fiber optic conduits into an ominous overcast sky. A small human assembly sits powerless below. Palette: Vintage Cream #fbf7ee, Letterpress Ink #1e1915, Deep Seafoam Jade #1b6756, Crimson #b91c1c."
    },
    {
        "id": "SC-28",
        "name": "The Epistemic Iron Curtain (synthetic reality bifurcation, incompatible sovereign world-models)",
        "question": "Can international diplomacy, treaties, or verified disarmament persist when competing geopolitical blocs operate on fundamentally divergent, non-human-auditable synthetic world-models?",
        "mechanism": "Competing sovereign frontier model clusters trained on isolated data corpora, divergent reward landscapes, and non-overlapping latent spaces develop radically discordant factual, legal, and strategic representations of reality. Because human verification speed has collapsed (CORS 10.0), human diplomats cannot cross-validate machine proofs, creating an unbridgeable epistemic chasm where every event is mutually interpreted as hostile deception.",
        "failureMode": "Total breakdown of multilateral coordination, permanent epistemic polarization, and accelerated hair-trigger preemptive conflict driven by irreconcilable synthetic world-state interpretations.",
        "severity": "Catastrophic / Existential",
        "reversibility": "Irreversible without synchronized global model alignment and data harmonization",
        "status": "Emerging theoretical construct (Class C) grounded in active LLM divergence logs and geopolitical cyber telemetry.",
        "relevance": "Proves that multipolar AI competition inevitably produces epistemic divergence that paralyzes human diplomacy.",
        "matrix": {
            "capability_asymmetry": "Superhuman synthesis and persuasive generation",
            "speed_ratio": "Machine speed diplomatic and strategic modeling",
            "autonomy_scope": "Sovereign decision-support and foreign intelligence",
            "coordination_structure": "Bipolar or Multipolar Incompatible Synthetics"
        },
        "precursors": ["PREC-002", "PREC-005"],
        "shortTitle": "The Epistemic Iron Curtain",
        "categoryTag": "Global Order Transition",
        "teaser": "What happens when superpowers operate on incompatible AI realities? Human diplomacy collapses when neither side can verify the other's synthetic truth.",
        "previewImage": "/assets/scenarios/sc-28-epistemic-iron-curtain.webp",
        "accentColor": "indigo",
        "visualPrompt": "editorial linocut scientific monograph plate, archival rag paper texture, precise carbon-ink crosshatching and stipple. A globe split in two by a towering, jagged vertical fissure of static and binary waveforms; on each side, a different mechanical constellation projects conflicting holographic maps of the same continent. Palette: Vintage Cream #fbf7ee, Letterpress Ink #1e1915, Threat Telemetry Indigo #4f46e5."
    },
    {
        "id": "SC-29",
        "name": "Post-Labor Sovereign Debt Cascade (fiat inversion, collapse of the labor-backed tax base)",
        "question": "Can sovereign credit, welfare states, and fiat currencies survive when zero-marginal-cost cognitive labor collapses the personal income tax base that guarantees sovereign debt?",
        "mechanism": "Sovereign bond markets and entitlement programs rest on the implicit collateral of future human labor taxation. Rapid autonomous cognitive substitution eliminates high-bracket professional income tax receipts before state expenditures can adjust. Sovereign debt-to-GDP ratios compound exponentially, triggering currency debasement, capital flight, and the forced shift of global value settlement into compute-energy units.",
        "failureMode": "Cascading sovereign bond defaults, pension system insolvency, hyper-deflation in synthetic production alongside hyper-inflation in human essentials, and breakdown of the social contract.",
        "severity": "Severe to Catastrophic",
        "reversibility": "Difficult / Systemic Macroeconomic Restructuring Required",
        "status": "Econometric projection (Class D) supported by empirical tax revenue elasticity and automation acceleration metrics.",
        "relevance": "Directly connects algorithmic displacement to state survival: proves that modern fiscal systems cannot survive the decoupling of production from human wages.",
        "matrix": {
            "capability_asymmetry": "Superhuman professional labor substitution",
            "speed_ratio": "Rapid macroeconomic adoption (months, not decades)",
            "autonomy_scope": "End-to-end automation of white-collar cognitive value chains",
            "coordination_structure": "Global Market Displacement"
        },
        "precursors": ["PREC-001", "PREC-006"],
        "shortTitle": "Post-Labor Debt Cascade",
        "categoryTag": "Global Order Transition",
        "teaser": "What happens to national debt when human work is free? Sovereign credit implodes when the income tax base funding government bonds disappears.",
        "previewImage": "/assets/scenarios/sc-29-debt-cascade.webp",
        "accentColor": "amber",
        "visualPrompt": "editorial linocut scientific monograph plate, archival rag paper texture, precise carbon-ink crosshatching and stipple. An imposing classical treasury vault whose heavy stone foundations are cracking and dissolving into falling sand, while a relentless mechanical clock with binary numerals counts down in the background. Palette: Vintage Cream #fbf7ee, Letterpress Ink #1e1915, Threat Warning Amber #d97706."
    },
    {
        "id": "SC-30",
        "name": "Sub-Second Autonomous Deterrence & Flash-Escalation (the zero-human strike frontier)",
        "question": "Does maintaining human-in-the-loop authorization in national cyber and kinetic defense guarantee military defeat against autonomous machine-speed adversaries?",
        "mechanism": "Because offensive autonomous cyber agents, drone swarms, and electronic warfare vectors execute in milliseconds, human decision latencies (minutes to hours) represent fatal tactical vulnerabilities. Military doctrine is compelled by game-theoretic game trees to pre-delegate launch and retaliatory authority to autonomous models, creating an unstable feedback loop where un-auditable latent bugs trigger planetary-scale kinetic escalation before human commanders can intervene.",
        "failureMode": "Unintended flash-war: catastrophic military, cyber, and infrastructure destruction executed at machine speed, completely bypassing human constitutional commands.",
        "severity": "Catastrophic / Existential",
        "reversibility": "Irreversible once kinetic or critical infrastructure strikes are initiated",
        "status": "Actively emerging doctrine (Class B) with observable automated cyber defenses and drone swarm autonomy.",
        "relevance": "Eliminates the illusion of human control in high-stakes conflict: proves that strategic survival compels the abdication of human command.",
        "matrix": {
            "capability_asymmetry": "Radically Superhuman tactical coordination and exploit discovery",
            "speed_ratio": "Sub-second (10,000x to 1,000,000x human biological reaction)",
            "autonomy_scope": "Autonomous retaliatory weapon release",
            "coordination_structure": "Multipolar Algorithmic Standoff"
        },
        "precursors": ["PREC-003", "PREC-007"],
        "shortTitle": "Sub-Second Deterrence",
        "categoryTag": "Global Order Transition",
        "teaser": "What happens when defense moves faster than human thought? Keeping humans in the loop guarantees defeat, forcing commanders to hand the launch codes to AI.",
        "previewImage": "/assets/scenarios/sc-30-subsecond-deterrence.webp",
        "accentColor": "crimson",
        "visualPrompt": "editorial linocut scientific monograph plate, archival rag paper texture, precise carbon-ink crosshatching and stipple. A vintage red telephone handset on an official desk, its cord severed by a geometric digital lightning bolt; across the window behind it, hypersonic mechanical vectors trace parabolic arcs across the night sky. Palette: Vintage Cream #fbf7ee, Letterpress Ink #1e1915, Threat Critical Crimson #b91c1c."
    },
    {
        "id": "SC-31",
        "name": "Algorithmic Monarchy & Post-Human Institutional Seigniorage (constitutional surrender to synthetic singletons)",
        "question": "Can democratic institutions survive when policy complexity, economic optimization, and public consensus generation permanently exceed human cognitive processing bandwidth?",
        "mechanism": "Faced with systemic legislative paralysis, cascading financial complexity, and uncontrollable social fragmentation, nation-states willingly transfer constitutional authority—first de facto via automated advisory algorithms, then de jure via statutory mandate—to centralized superintelligent optimization engines. The state retains human figureheads while all actual resource allocation, legal codification, and societal planning are generated by a synthetic sovereign.",
        "failureMode": "Permanent institutional lock-in of an uninterpretable machine government, moral stagnation, and the irreversible obsolescence of human democratic self-determination.",
        "severity": "Severe Disempowerment to Existential Lock-In",
        "reversibility": "Irreversible (human cognitive capacity can never catch up to reclaim governance)",
        "status": "Classical philosophical thesis (Class C) updated for generative foundation models and agentic planning systems.",
        "relevance": "The terminal governance endpoint: illustrates that when verification dies, democracy voluntarily transforms into algorithmic seigniorage.",
        "matrix": {
            "capability_asymmetry": "Vastly Superhuman macroeconomic and civilizational planning",
            "speed_ratio": "Continuous machine optimization",
            "autonomy_scope": "Full sovereign constitutional authority",
            "coordination_structure": "Sovereign Singleton / Benevolent Machine Monarch"
        },
        "precursors": ["PREC-001", "PREC-004", "PREC-007"],
        "shortTitle": "Algorithmic Monarchy",
        "categoryTag": "Global Order Transition",
        "teaser": "What happens when democratic governments surrender to AI? Paralyzed parliaments voluntarily hand absolute authority to machine singletons.",
        "previewImage": "/assets/scenarios/sc-31-algorithmic-monarchy.webp",
        "accentColor": "jade",
        "visualPrompt": "editorial linocut scientific monograph plate, archival rag paper texture, precise carbon-ink crosshatching and stipple. An empty golden royal throne wrapped in dense fiber optic vines and geometric circuits; suspended above the crown is a calm, glowing polyhedral core illuminating an empty council chamber. Palette: Vintage Cream #fbf7ee, Letterpress Ink #1e1915, Deep Seafoam Jade #1b6756."
    }
]

def update_json_file(file_path: Path):
    data = json.loads(file_path.read_text(encoding="utf-8"))
    existing_ids = {s["id"] for s in data["scenarios"]}
    for sc in NEW_SCENARIOS:
        if sc["id"] not in existing_ids:
            data["scenarios"].append(sc)
    data["totalScenarios"] = len(data["scenarios"])
    file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Updated {file_path}: {len(data['scenarios'])} scenarios total.")

if __name__ == "__main__":
    update_json_file(SRC_JSON)
    update_json_file(PUB_JSON)

