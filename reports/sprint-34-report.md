# HSRI Sprint 34 Report: The First Civilizational Decoupling Drill (Small-State Tabletop)

> **Generated**: `2026-10-13T23:30:00+05:30`  
> **Milestone**: `v2.5.0-DecouplingDrill` (Sprint 34 Closure — The First Civilizational Decoupling Drill & Small-State Tabletop)  
> **Branch**: `main`  
> **Status**: Verified & Passing (`206/206` tests passing green, `51/51` Astro pages cleanly built in 8.50s)  
> **Live Benchmark**: `https://humanreadinessindex.org/`  
> **Interactive Drill Simulator**: `https://humanreadinessindex.org/research/decoupling-drill/`  
> **Master Drill Protocol**: [`research/tabletop/decoupling_drill_protocol.md`](../research/tabletop/decoupling_drill_protocol.md)  
> **Publication Whitepaper**: [`research/tabletop/when_the_cloud_goes_silent.md`](../research/tabletop/when_the_cloud_goes_silent.md)  
> **Principal Investigator**: Krishnakumar Radhakrishnan  

---

## 1. Executive Summary & Tabletop Objective

**Sprint 34** operationalizes the core theoretical postulate of HSRI 2.0 — Pillar 6: *Civilizational Decoupling Half-Life ($T_{\text{half}}$)* — moving from mathematical equations to an empirical, reproducible civilizational crisis simulation.

When frontier AI cloud providers (Azure, AWS, GCP, Anthropic, OpenAI) experience an abrupt, zero-notice quarantine or autonomous weaponization seizure, what happens to modern nation-states?

Sprint 34 delivers:
1. **The 336-Hour Multi-Sector Simulation Engine (`scripts/decoupling_simulator.py`)**: A discrete-time dynamical simulator modeling 4 critical subsystems (Power Grid, Financial Clearing, Food Logistics, Telecom Backbone) across three sovereign archetypes.
2. **Master Exercise Protocol (`research/tabletop/decoupling_drill_protocol.md`)**: A complete 4-phase, 8-inject crisis simulation manual with quantitative Leontief weakest-link scoring and fallback metrics.
3. **Publication Whitepaper (`research/tabletop/when_the_cloud_goes_silent.md`)**: A master policy and national security treatise titled *"When the Cloud Goes Silent: The Civilizational Decoupling Drill and the Small-State Sovereign Dilemma in the Age of Frontier Artificial Superintelligence"*, authored by Krishnakumar Radhakrishnan.
4. **Interactive Astro & Svelte Portal (`/research/decoupling-drill`)**: An institutional-grade web viewer with real-time hour scrubbing, live telemetry charts, fracture status indicators, and crisis inject logs.
5. **Comprehensive Automated Verification (`tests/test_decoupling_drill.py`)**: Expanding the repository test suite to 206 passing tests.

---

## 2. Key Findings: The Decoupling Half-Life Trilemma

The 14-day (336-hour) simulation revealed three stark archetypal trajectories:

| Sovereign Archetype | Representative States | First Fracture ($T_{\text{first}}$) | Decoupling Half-Life ($T_{\text{half}}$) | Critical Failure ($T_{\text{crit}}$) | Day 14 Residual Capacity | Dominant Failure Mode |
|---|---|---|---|---|---|---|
| **Archetype A: Small Open Tech Hub** | Singapore, Hong Kong, UAE | **2.0 hours** | **8.0 hours** | **17.0 hours** | **1.00%** | Financial Clearing collapse cascading into immediate import port gridlock |
| **Archetype B: Diversified Continental Power** | USA, Germany, Japan | **8.0 hours** | **28.0 hours** | **60.0 hours** | **2.96%** | Telecom peering collapse degrading automated power grid SCADA dispatch |
| **Archetype C: High-Trust Air-Gapped State** | Switzerland, Finland, Sweden | **159.0 hours** | **> 336 hours** | **None** | **69.22%** | Controlled step-down to deterministic analog reserve protocols |

### Core Mathematical Insights
1. **The Verification Illusion in Practice**: Archetype A exhibits high nominal readiness under traditional indices (high GDP, high cloud adoption, high STEM literacy), yet experiences a complete civilizational paralysis within 17 hours due to the absence of un-augmented human manual fallbacks.
2. **The Leontief Bottleneck Cascade**: Because human infrastructure operates under Leontief minimums ($S_{\text{civ}} = \min(P, F, L, T)$), failure in financial settlement immediately halts dockside container unloading within 12 hours, regardless of grid stability.
3. **The Sovereign Paradox**: True civilizational resilience requires deliberate friction — analog reserves, civil conscription, manual dispatch relays, and local air-gapped sovereign compute.

---

## 3. Architecture & Delivered Modules

### A. Simulation Engine (`scripts/decoupling_simulator.py`)
- Simulates 336 discrete 1-hour steps.
- Models 4 interdependent subsystems with non-linear exponential decay driven by AI dependency factors ($d_s$), human manual fallback capacities ($m_s$), and inter-sector Leontief couplings ($C$).
- Tracks 8 scheduled operational injects:
  - `INJ-01` (T+0h): Global Cloud Kill-Switch Trigger.
  - `INJ-02` (T+4h): High-Frequency Liquidity Freezes.
  - `INJ-03` (T+12h): SCADA Frequency Instability.
  - `INJ-04` (T+24h): Port Logistics & Perishable Spoilage.
  - `INJ-05` (T+48h): Hospital Emergency Power Depletion.
  - `INJ-06` (T+72h): Telecom Peering Fragmentation.
  - `INJ-07` (T+120h): Public Rationing & Civil Order Strain.
  - `INJ-08` (T+240h): Secondary Analog Re-Stabilization Plateau.
- Exports validated JSON datasets to `data/telemetry/decoupling_drill_results.json` and Astro static data directory.

### B. Master Exercise Protocol & Injects (`research/tabletop/decoupling_drill_protocol.md`)
- Complete facilitator instructions, room layout, participant role-playing assignments (National Security Advisor, Grid Chief, Central Bank Governor, Supply Chain Director, Telecom Secretary).
- Inject timeline, expected player decisions, and mathematical scoring rubric.
- Post-exercise audit template for sovereign resilience benchmarking.

### C. Master Whitepaper (`research/tabletop/when_the_cloud_goes_silent.md`)
- Authored by Krishnakumar Radhakrishnan.
- Deep theoretical synthesis of Leontief production functions, Ashby's Law of Requisite Variety, and the Small-State Sovereign Dilemma.
- 5 strategic policy recommendations for small-state national security cabinets.

### D. Interactive Svelte & Astro Visualizer (`site-astro/src/components/DecouplingDrillViewer.svelte`)
- Tabbed archetype switcher (Archetype A, Archetype B, Archetype C).
- Interactive time slider (0h to 336h) with play/pause simulation scrubber.
- Dynamic telemetry cards showing Aggregate Sovereign Capacity, Leontief Bottleneck Subsystem, and active Injects.
- Animated multi-subsystem progress bars with color-coded operational regimes (Operational, Strained, Critical, Collapsed).
- Integrated into main Astro navigation and footer (`/research/decoupling-drill`).

---

## 4. Verification & Quality Assurance

- **Unit Tests**: `tests/test_decoupling_drill.py` authored and passing:
  - `test_simulation_data_integrity`: Verifies structural integrity, all 3 archetypes, and 336-hour steps.
  - `test_half_life_ordering`: Validates that Archetype A ($T_{\text{half}}=8\text{h}$) is strictly more fragile than Archetype B ($28\text{h}$), which is strictly more fragile than Archetype C ($>336\text{h}$).
  - `test_leontief_bottleneck_mechanics`: Confirms Leontief minimum aggregation and system collapse thresholds.
  - `test_protocol_documentation_integrity`: Validates all 8 injects and scoring sections in protocol manual.
  - `test_whitepaper_author_and_content`: Verifies authorship by Krishnakumar Radhakrishnan, mathematical definitions, and small-state analysis.
- **Test Suite Result**: **206/206 tests passing green** across the repository in 8.37s.
- **Astro Build**: **51 static pages compiled in 8.50s** with 0 errors.

---

## 5. Next Steps: Sprint 35 Roadmap Transition

With the Civilizational Decoupling Drill fully integrated and verified, HSRI 2.0 enters **Sprint 35: HSRI 2.0 General Release & Reinsurance Risk Offering**:
1. Formal public announcement and distribution of the Decoupling Drill whitepaper to civil defense agencies and national security councils.
2. Reinsurance actuarial risk framework formalization for critical infrastructure underwriting.
3. Master release tagging (`v2.5.0-DecouplingDrill`) and DOI synchronization.
