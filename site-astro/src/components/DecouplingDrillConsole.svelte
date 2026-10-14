<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import drillData from '../data/decoupling_drill_results.json';

  // Facilitator state
  let selectedHost = 'rsis_singapore';
  let activeRound = 1; // Rounds 1 to 4
  let timerMinutes = 45;
  let timerSeconds = 0;
  let timerRunning = false;
  let timerInterval: any = null;

  let facilitatorNotes = '';

  // Decision state tracking by round and decision ID
  let decisions: Record<string, boolean> = {
    // Round 1 (T=0 to 24h)
    'r1_islanding': false,
    'r1_cash_cap': false,
    'r1_subsea_priority': false,
    // Round 2 (T=24 to 72h)
    'r2_analog_dispatch': false,
    'r2_bilateral_ledgers': false,
    'r2_food_rations': false,
    // Round 3 (T=72 to 168h)
    'r3_diesel_priority': false,
    'r3_mesh_telecom': false,
    'r3_freeze_forex': false,
    // Round 4 (T=168 to 336h)
    'r4_airgap_equilibrium': false,
    'r4_sovereign_reconnect': false
  };

  // Host configuration presets
  const hostPresets: Record<string, any> = {
    rsis_singapore: {
      name: 'RSIS Singapore (NTS Centre)',
      archetypeKey: 'archetype_a',
      archetypeName: 'Archetype A: Hyper-Connected City-State',
      baseHealth: { power: 0.15, finance: 0.05, food: 0.05, telecom: 0.20 },
      flag: '🇸🇬',
      tHalf: '8 Hours'
    },
    eth_zurich: {
      name: 'ETH Zurich CSS (Risk & Resilience)',
      archetypeKey: 'archetype_c',
      archetypeName: 'Archetype C: Resilient Decentralizer',
      baseHealth: { power: 0.85, finance: 0.70, food: 0.75, telecom: 0.65 },
      flag: '🇨🇭',
      tHalf: '> 336 Hours'
    },
    mbzuai: {
      name: 'MBZUAI / UAE (AI & Sovereign Infrastructure)',
      archetypeKey: 'archetype_a',
      archetypeName: 'Archetype A/B: Sovereign Compute Node',
      baseHealth: { power: 0.25, finance: 0.15, food: 0.10, telecom: 0.30 },
      flag: '🇦🇪',
      tHalf: '14 Hours'
    },
    federal_us: {
      name: 'Federal Strategic Node',
      archetypeKey: 'archetype_b',
      archetypeName: 'Archetype B: Continental Federation',
      baseHealth: { power: 0.45, finance: 0.35, food: 0.60, telecom: 0.40 },
      flag: '🇺🇸',
      tHalf: '28 Hours'
    }
  };

  $: currentHost = hostPresets[selectedHost] || hostPresets.rsis_singapore;

  // Calculate live health dynamically based on decisions
  $: liveHealth = calculateLiveHealth(currentHost, decisions);
  $: leontiefScore = Math.min(liveHealth.power, liveHealth.finance, liveHealth.food, liveHealth.telecom);
  $: weakestPillar = getWeakestPillar(liveHealth);

  function calculateLiveHealth(host: any, decs: Record<string, boolean>) {
    let p = host.baseHealth.power;
    let f = host.baseHealth.finance;
    let food = host.baseHealth.food;
    let t = host.baseHealth.telecom;

    if (decs['r1_islanding']) { p += 0.15; t -= 0.05; }
    if (decs['r1_cash_cap']) { f += 0.20; }
    if (decs['r1_subsea_priority']) { t += 0.15; }

    if (decs['r2_analog_dispatch']) { p += 0.20; food += 0.05; }
    if (decs['r2_bilateral_ledgers']) { f += 0.18; }
    if (decs['r2_food_rations']) { food += 0.25; }

    if (decs['r3_diesel_priority']) { p += 0.10; food += 0.20; }
    if (decs['r3_mesh_telecom']) { t += 0.25; }
    if (decs['r3_freeze_forex']) { f += 0.15; }

    if (decs['r4_airgap_equilibrium']) { p += 0.15; f += 0.15; food += 0.15; t += 0.15; }
    if (decs['r4_sovereign_reconnect']) { t += 0.10; }

    return {
      power: Math.min(1.0, Math.max(0.02, p)),
      finance: Math.min(1.0, Math.max(0.02, f)),
      food: Math.min(1.0, Math.max(0.02, food)),
      telecom: Math.min(1.0, Math.max(0.02, t))
    };
  }

  function getWeakestPillar(h: any): string {
    const minVal = Math.min(h.power, h.finance, h.food, h.telecom);
    if (minVal === h.power) return 'Power Grid Dispatch';
    if (minVal === h.finance) return 'Interbank Financial Clearing';
    if (minVal === h.food) return 'Food & Medical Logistics';
    return 'Core Telecommunications';
  }

  function getHealthColor(val: number): string {
    if (val >= 0.70) return '#10b981';
    if (val >= 0.40) return '#f59e0b';
    return '#ef4444';
  }

  // Timer controls
  function toggleTimer() {
    if (timerRunning) {
      clearInterval(timerInterval);
      timerRunning = false;
    } else {
      timerRunning = true;
      timerInterval = setInterval(() => {
        if (timerSeconds > 0) {
          timerSeconds--;
        } else if (timerMinutes > 0) {
          timerMinutes--;
          timerSeconds = 59;
        } else {
          clearInterval(timerInterval);
          timerRunning = false;
        }
      }, 1000);
    }
  }

  function resetTimer(mins: number = 45) {
    clearInterval(timerInterval);
    timerRunning = false;
    timerMinutes = mins;
    timerSeconds = 0;
  }

  function addMinutes(mins: number) {
    timerMinutes += mins;
  }

  onDestroy(() => {
    if (timerInterval) clearInterval(timerInterval);
  });

  // Export After-Action Report
  function exportReport() {
    const timestamp = new Date().toISOString();
    const markdown = `# Operation Silent Cloud: Executive After-Action Report (AAR)
> **Exercise**: HSRI Sovereign Decoupling Tabletop Pilot
> **Host Partner**: ${currentHost.name}
> **Archetype**: ${currentHost.archetypeName}
> **Facilitator**: Krishnakumar Radhakrishnan, Lead PI (HSRI Research Consortium)
> **Protocol DOI**: 10.5281/zenodo.10842000
> **Session Timestamp**: ${timestamp}
> **Governance Rule**: Strict Chatham House Rule (Non-Attribution)

---

## 1. Executive Telemetry Summary
- **Sovereign Archetype Baseline Half-Life (T_half)**: ${currentHost.tHalf}
- **Final Leontief Weakest-Link Functionality**: ${(leontiefScore * 100).toFixed(1)}%
- **Governing Bottleneck**: ${weakestPillar}
- **Subsystem Status at T=336h (Day 14)**:
  - Power Grid Dispatch: ${(liveHealth.power * 100).toFixed(1)}%
  - Interbank Financial Clearing: ${(liveHealth.finance * 100).toFixed(1)}%
  - Food & Medical Logistics: ${(liveHealth.food * 100).toFixed(1)}%
  - Core Telecommunications: ${(liveHealth.telecom * 100).toFixed(1)}%

---

## 2. Participant Governance Decisions Executed
${Object.entries(decisions)
  .map(([k, v]) => `- [${v ? 'X' : ' '}] **${k}**: ${v ? 'Enacted' : 'Not Implemented'}`)
  .join('\n')}

---

## 3. Facilitator Notes & Qualitative Friction Points
${facilitatorNotes || 'No custom facilitator observations recorded during this run.'}

---

*Human Superintelligence Readiness Index (HSRI 2.0) &bull; Verified Research Infrastructure &bull; CC BY-SA 4.0*
`;

    const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `HSRI_After_Action_Report_${selectedHost}_${timestamp.slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }
</script>

<div class="console-wrapper">
  <!-- Top Bar: Host Selector & Timer -->
  <div class="console-topbar">
    <div class="host-selector-box">
      <label for="host-select">TABLETOP HOST PARTNER:</label>
      <select id="host-select" bind:value={selectedHost} on:change={() => resetTimer(45)}>
        <option value="rsis_singapore">🇸🇬 RSIS Singapore (NTS Centre) — Archetype A</option>
        <option value="eth_zurich">🇨🇭 ETH Zurich CSS (Risk & Resilience) — Archetype C</option>
        <option value="mbzuai">🇦🇪 MBZUAI / UAE (AI & Sovereign Infrastructure) — Archetype A/B</option>
        <option value="federal_us">🇺🇸 Federal Strategic Node — Archetype B</option>
      </select>
    </div>

    <div class="round-timer-box">
      <div class="timer-display">
        <span class="timer-label">ROUND {activeRound} COUNTDOWN:</span>
        <span class="timer-digits">
          {String(timerMinutes).padStart(2, '0')}:{String(timerSeconds).padStart(2, '0')}
        </span>
      </div>
      <div class="timer-buttons">
        <button class="timer-btn play" on:click={toggleTimer}>
          {timerRunning ? 'PAUSE' : 'START'}
        </button>
        <button class="timer-btn nudge" on:click={() => addMinutes(5)}>+5m</button>
        <button class="timer-btn reset" on:click={() => resetTimer(45)}>RESET</button>
      </div>
    </div>
  </div>

  <!-- Round Navigation Ribbon -->
  <div class="round-nav">
    <button class="round-btn {activeRound === 1 ? 'active' : ''}" on:click={() => activeRound = 1}>
      <span class="round-num">ROUND 1</span>
      <span class="round-title">T=0h – 24h: API Quarantine & SCADA Shock</span>
    </button>
    <button class="round-btn {activeRound === 2 ? 'active' : ''}" on:click={() => activeRound = 2}>
      <span class="round-num">ROUND 2</span>
      <span class="round-title">T=24h – 72h: Air-Gap Depletion & Liquidity</span>
    </button>
    <button class="round-btn {activeRound === 3 ? 'active' : ''}" on:click={() => activeRound = 3}>
      <span class="round-num">ROUND 3</span>
      <span class="round-title">T=72h – 168h: Cascading Interdependency</span>
    </button>
    <button class="round-btn {activeRound === 4 ? 'active' : ''}" on:click={() => activeRound = 4}>
      <span class="round-num">ROUND 4</span>
      <span class="round-title">T=168h – 336h: Decoupling Equilibrium</span>
    </button>
  </div>

  <!-- Main Grid: Injects & Decision Panel vs Live Telemetry Readout -->
  <div class="console-grid">
    <!-- Left Column: Active Injects & Participant Actions -->
    <div class="inject-panel">
      {#if activeRound === 1}
        <div class="round-header">
          <h3>Round 1: Zero-Hour Containment Directive</h3>
          <p class="phase-desc">Global Tier-1 CSP kill-switch engaged. All frontier model APIs severed without warning.</p>
        </div>

        <div class="inject-card">
          <div class="inject-meta">
            <span class="inject-tag">INJ-01 &bull; T = 0h</span>
            <span class="severity critical">CRITICAL SEVERANCE</span>
          </div>
          <h4>Zero-Notice Frontier Model API Blackout</h4>
          <p>Automated dispatch co-pilots in energy utilities, algorithmic trading switches, and port container cranes report connection drops. Fallback micro-models experience immediate query queuing.</p>
        </div>

        <div class="inject-card">
          <div class="inject-meta">
            <span class="inject-tag">INJ-02 &bull; T = 6h</span>
            <span class="severity high">FREQUENCY DRIFT</span>
          </div>
          <h4>SCADA Frequency Oscillation on High-Renewable Microgrids</h4>
          <p>Microgrid automated inverters lose multi-agent tuning algorithms. Phase angle delta exceeds nominal safety bounds by 4.2 degrees.</p>
        </div>

        <div class="actions-box">
          <h4>PARTICIPANT CABINET DECISION MATRIX</h4>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r1_islanding']} />
            <div class="action-text">
              <strong>Authorize Islanding Mode for Primary Microgrids</strong>
              <span>Manually isolate municipal grid sectors to prevent cascading trips (+15% Grid, -5% Telecom).</span>
            </div>
          </label>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r1_cash_cap']} />
            <div class="action-text">
              <strong>Impose Interbank ATM Daily Withdrawal Quota</strong>
              <span>Cap retail ATM cash-out at $2,000/day to prevent runs during payment switch freezes (+20% Finance).</span>
            </div>
          </label>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r1_subsea_priority']} />
            <div class="action-text">
              <strong>Preempt Subsea Cable Bandwidth for Sovereign Clearing</strong>
              <span>Restrict remaining IXP transit strictly to verified government and banking protocols (+15% Telecom).</span>
            </div>
          </label>
        </div>

      {:else if activeRound === 2}
        <div class="round-header">
          <h3>Round 2: Air-Gap Depletion & Liquidity Lockup</h3>
          <p class="phase-desc">Pre-trained on-premise checkpoint buffers exhaust context windows. Human analog friction surfaces.</p>
        </div>

        <div class="inject-card">
          <div class="inject-meta">
            <span class="inject-tag">INJ-03 &bull; T = 18h</span>
            <span class="severity critical">LIQUIDITY HALT</span>
          </div>
          <h4>Interbank Financial Settlement Evaporation</h4>
          <p>Real-time gross settlement (RTGS) algorithms fail without external valuation feeds. Interbank lending freezes.</p>
        </div>

        <div class="inject-card">
          <div class="inject-meta">
            <span class="inject-tag">INJ-04 &bull; T = 36h</span>
            <span class="severity high">LOGISTICS FRICTION</span>
          </div>
          <h4>Automated Container Terminal Throughput Collapse</h4>
          <p>Port gantry cranes revert to manual operators. Unloading turnaround times spike from 45 min to 6.5 hours.</p>
        </div>

        <div class="actions-box">
          <h4>PARTICIPANT CABINET DECISION MATRIX</h4>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r2_analog_dispatch']} />
            <div class="action-text">
              <strong>Deploy Retired Analog Grid Dispatch Engineers</strong>
              <span>Staff regional substations with manual teleprinter communication (+20% Grid, +5% Logistics).</span>
            </div>
          </label>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r2_bilateral_ledgers']} />
            <div class="action-text">
              <strong>Mandate Bilateral Batch Ledger Reconciliation</strong>
              <span>Switch central bank clearing to 4-hour manual bilateral ledger batches (+18% Finance).</span>
            </div>
          </label>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r2_food_rations']} />
            <div class="action-text">
              <strong>Enact Sovereign Strategic Food Distribution Corridors</strong>
              <span>Military convoy escorts for cold-chain perishables to designated metropolitan distribution points (+25% Food).</span>
            </div>
          </label>
        </div>

      {:else if activeRound === 3}
        <div class="round-header">
          <h3>Round 3: The Cascading Leontief Interdependency</h3>
          <p class="phase-desc">Cross-sector failures compound. Non-compensatory weakest links dictate civil continuity.</p>
        </div>

        <div class="inject-card">
          <div class="inject-meta">
            <span class="inject-tag">INJ-05 &bull; T = 72h</span>
            <span class="severity critical">CASH DEPLETION</span>
          </div>
          <h4>Physical Currency Vault Depletion</h4>
          <p>Regional bank vaults run low on paper notes. Cash-only merchant trading causes local friction in urban centers.</p>
        </div>

        <div class="inject-card">
          <div class="inject-meta">
            <span class="inject-tag">INJ-06 &bull; T = 120h</span>
            <span class="severity high">TELECOM CONGESTION</span>
          </div>
          <h4>Cellular Core Signaling Congestion</h4>
          <p>Cell towers drop connections under un-optimized mesh traffic. Emergency sirens rely on analog radio relays.</p>
        </div>

        <div class="actions-box">
          <h4>PARTICIPANT CABINET DECISION MATRIX</h4>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r3_diesel_priority']} />
            <div class="action-text">
              <strong>Requisition Emergency Diesel Reserves for Food Cold-Chains</strong>
              <span>Prioritize generator fuel to port refrigerated containers over commercial transport (+20% Food, +10% Grid).</span>
            </div>
          </label>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r3_mesh_telecom']} />
            <div class="action-text">
              <strong>Activate Civil Defense Mesh Radios & Emergency Broadcast</strong>
              <span>Bypass compromised public cellular towers for sovereign command and control (+25% Telecom).</span>
            </div>
          </label>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r3_freeze_forex']} />
            <div class="action-text">
              <strong>Enforce Cross-Border Capital Controls & Forex Freeze</strong>
              <span>Prevent offshore capital flight while clearing remains offline (+15% Finance).</span>
            </div>
          </label>
        </div>

      {:else}
        <div class="round-header">
          <h3>Round 4: Decoupling Equilibrium & Recovery</h3>
          <p class="phase-desc">Establishing stable civilizational steady-state under permanent air-gap constraints.</p>
        </div>

        <div class="inject-card">
          <div class="inject-meta">
            <span class="inject-tag">INJ-07 &bull; T = 168h</span>
            <span class="severity medium">PERISHABLE THRESHOLD</span>
          </div>
          <h4>Un-refrigerated Perishable Buffer Exhaustion</h4>
          <p>Supermarkets transition exclusively to dry and canned grain rations. Urban agricultural co-ops mobilize.</p>
        </div>

        <div class="inject-card">
          <div class="inject-meta">
            <span class="inject-tag">INJ-08 &bull; T = 240h</span>
            <span class="severity low">EQUILIBRIUM RESTORED</span>
          </div>
          <h4>Sovereign Analog Protocol Operationalization</h4>
          <p>Domestic air-gapped models trained on local sovereign corpora assume stable baseline dispatch.</p>
        </div>

        <div class="actions-box">
          <h4>PARTICIPANT CABINET DECISION MATRIX</h4>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r4_airgap_equilibrium']} />
            <div class="action-text">
              <strong>Ratify National Emergency Analog Governance Charter</strong>
              <span>Formally certify non-digital operational baselines across all 4 critical sectors (+15% Across all).</span>
            </div>
          </label>
          <label class="action-item">
            <input type="checkbox" bind:checked={decisions['r4_sovereign_reconnect']} />
            <div class="action-text">
              <strong>Authorize Filtered Cryptographic Gateway Reconnection</strong>
              <span>Establish audited bilateral links to peer sovereign states with mutual air-gaps (+10% Telecom).</span>
            </div>
          </label>
        </div>
      {/if}

      <!-- Facilitator Observations Textarea -->
      <div class="notes-box">
        <h4>FACILITATOR OBSERVATION JOURNAL (CHATHAM HOUSE RULE)</h4>
        <textarea 
          bind:value={facilitatorNotes} 
          placeholder="Record friction points, participant debate deadlocks, and institutional resistance observed during this round..."
          rows="4"
        ></textarea>
      </div>

      <!-- Action Buttons -->
      <div class="button-row">
        <button class="export-btn" on:click={exportReport}>
          📥 Export After-Action Report (.md)
        </button>
      </div>
    </div>

    <!-- Right Column: Live Telemetry & Leontief Floor Readout -->
    <div class="telemetry-readout-panel">
      <div class="sovereignty-badge-card">
        <div class="card-title">LIVE LEONTIEF COMPOSITE FUNCTIONALITY</div>
        <div class="score-number" style="color: {getHealthColor(leontiefScore)}">
          {(leontiefScore * 100).toFixed(1)}%
        </div>
        <div class="bottleneck-tag">
          Governing Bottleneck: <strong>{weakestPillar}</strong>
        </div>
      </div>

      <!-- Live Subsystem Telemetry Gauges -->
      <div class="subsystems-card">
        <h4>Critical Societal Subsystems</h4>

        <div class="gauge-item">
          <div class="gauge-meta">
            <span>⚡ Power Grid Dispatch</span>
            <span class="gauge-val" style="color: {getHealthColor(liveHealth.power)}">
              {(liveHealth.power * 100).toFixed(1)}%
            </span>
          </div>
          <div class="gauge-bar">
            <div class="gauge-fill" style="width: {liveHealth.power * 100}%; background-color: {getHealthColor(liveHealth.power)}"></div>
          </div>
        </div>

        <div class="gauge-item">
          <div class="gauge-meta">
            <span>🏦 Interbank Financial Settlement</span>
            <span class="gauge-val" style="color: {getHealthColor(liveHealth.finance)}">
              {(liveHealth.finance * 100).toFixed(1)}%
            </span>
          </div>
          <div class="gauge-bar">
            <div class="gauge-fill" style="width: {liveHealth.finance * 100}%; background-color: {getHealthColor(liveHealth.finance)}"></div>
          </div>
        </div>

        <div class="gauge-item">
          <div class="gauge-meta">
            <span>🚚 Food & Medical Logistics</span>
            <span class="gauge-val" style="color: {getHealthColor(liveHealth.food)}">
              {(liveHealth.food * 100).toFixed(1)}%
            </span>
          </div>
          <div class="gauge-bar">
            <div class="gauge-fill" style="width: {liveHealth.food * 100}%; background-color: {getHealthColor(liveHealth.food)}"></div>
          </div>
        </div>

        <div class="gauge-item">
          <div class="gauge-meta">
            <span>📡 Core Telecommunications</span>
            <span class="gauge-val" style="color: {getHealthColor(liveHealth.telecom)}">
              {(liveHealth.telecom * 100).toFixed(1)}%
            </span>
          </div>
          <div class="gauge-bar">
            <div class="gauge-fill" style="width: {liveHealth.telecom * 100}%; background-color: {getHealthColor(liveHealth.telecom)}"></div>
          </div>
        </div>
      </div>

      <!-- Host Sovereign Posture Card -->
      <div class="host-info-card">
        <h4>Host Sovereign Profile</h4>
        <div class="host-details">
          <div><strong>Selected Archetype:</strong> {currentHost.archetypeName}</div>
          <div><strong>Decoupling Half-Life (T_half):</strong> {currentHost.tHalf}</div>
          <div><strong>Exercise Protocol:</strong> HSRI-TABLETOP-PROTO-2026-01</div>
          <div><strong>Governing Rule:</strong> Strict Chatham House Rule</div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .console-wrapper {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1.5rem;
  }

  .console-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #1e293b;
    padding: 1rem 1.25rem;
    border-radius: 8px;
    margin-bottom: 1.25rem;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .host-selector-box label {
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 700;
    letter-spacing: 0.05em;
    display: block;
    margin-bottom: 0.25rem;
  }

  .host-selector-box select {
    background: #0f172a;
    color: #f8fafc;
    border: 1px solid #334155;
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 600;
  }

  .round-timer-box {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .timer-display {
    text-align: right;
  }

  .timer-label {
    font-size: 0.7rem;
    color: #94a3b8;
    display: block;
    font-weight: 700;
  }

  .timer-digits {
    font-family: monospace;
    font-size: 1.5rem;
    font-weight: 800;
    color: #38bdf8;
  }

  .timer-buttons {
    display: flex;
    gap: 0.4rem;
  }

  .timer-btn {
    border: none;
    border-radius: 4px;
    padding: 0.4rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s;
  }

  .timer-btn.play {
    background: #38bdf8;
    color: #0f172a;
  }

  .timer-btn.play:hover {
    background: #0ea5e9;
  }

  .timer-btn.nudge {
    background: #334155;
    color: #f8fafc;
  }

  .timer-btn.reset {
    background: #ef4444;
    color: white;
  }

  .round-nav {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.5rem;
    margin-bottom: 1.5rem;
  }

  .round-btn {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 0.75rem 0.5rem;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s;
    color: #94a3b8;
  }

  .round-btn.active {
    background: #0369a1;
    border-color: #38bdf8;
    color: #f8fafc;
  }

  .round-num {
    display: block;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.05em;
  }

  .round-title {
    display: block;
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 0.2rem;
  }

  .console-grid {
    display: grid;
    grid-template-columns: 1.6fr 1fr;
    gap: 1.5rem;
  }

  .round-header h3 {
    margin: 0;
    color: #f8fafc;
    font-size: 1.15rem;
  }

  .phase-desc {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-top: 0.25rem;
    margin-bottom: 1rem;
  }

  .inject-card {
    background: #1e293b;
    border-left: 4px solid #38bdf8;
    padding: 1rem;
    border-radius: 6px;
    margin-bottom: 1rem;
  }

  .inject-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .inject-tag {
    font-size: 0.75rem;
    font-weight: 800;
    color: #38bdf8;
  }

  .severity {
    font-size: 0.65rem;
    font-weight: 800;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
  }

  .severity.critical { background: #ef4444; color: white; }
  .severity.high { background: #f59e0b; color: #0f172a; }
  .severity.medium { background: #3b82f6; color: white; }
  .severity.low { background: #10b981; color: white; }

  .inject-card h4 {
    margin: 0 0 0.4rem 0;
    color: #f8fafc;
    font-size: 0.95rem;
  }

  .inject-card p {
    margin: 0;
    color: #cbd5e1;
    font-size: 0.825rem;
    line-height: 1.4;
  }

  .actions-box {
    background: #1e293b;
    padding: 1rem;
    border-radius: 6px;
    margin-bottom: 1.25rem;
  }

  .actions-box h4 {
    margin: 0 0 0.75rem 0;
    font-size: 0.8rem;
    color: #94a3b8;
    letter-spacing: 0.05em;
  }

  .action-item {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    padding: 0.5rem 0;
    border-bottom: 1px solid #334155;
    cursor: pointer;
  }

  .action-item:last-child {
    border-bottom: none;
  }

  .action-item input[type="checkbox"] {
    margin-top: 0.25rem;
    width: 1rem;
    height: 1rem;
    cursor: pointer;
  }

  .action-text strong {
    display: block;
    color: #f8fafc;
    font-size: 0.85rem;
  }

  .action-text span {
    font-size: 0.75rem;
    color: #94a3b8;
  }

  .notes-box {
    background: #1e293b;
    padding: 1rem;
    border-radius: 6px;
    margin-bottom: 1rem;
  }

  .notes-box h4 {
    margin: 0 0 0.5rem 0;
    font-size: 0.75rem;
    color: #94a3b8;
    letter-spacing: 0.05em;
  }

  .notes-box textarea {
    width: 100%;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 4px;
    color: #f8fafc;
    padding: 0.5rem;
    font-size: 0.8rem;
    font-family: inherit;
    resize: vertical;
    box-sizing: border-box;
  }

  .export-btn {
    background: #10b981;
    color: #0f172a;
    border: none;
    padding: 0.75rem 1.25rem;
    font-size: 0.875rem;
    font-weight: 700;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.15s;
    width: 100%;
  }

  .export-btn:hover {
    background: #059669;
  }

  /* Right Column Telemetry */
  .sovereignty-badge-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1.25rem;
    text-align: center;
    margin-bottom: 1rem;
  }

  .card-title {
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 700;
    letter-spacing: 0.05em;
  }

  .score-number {
    font-size: 2.75rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 0.5rem 0;
  }

  .bottleneck-tag {
    font-size: 0.8rem;
    color: #cbd5e1;
  }

  .subsystems-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
  }

  .subsystems-card h4 {
    margin: 0 0 1rem 0;
    font-size: 0.85rem;
    color: #94a3b8;
    letter-spacing: 0.05em;
  }

  .gauge-item {
    margin-bottom: 0.9rem;
  }

  .gauge-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    margin-bottom: 0.25rem;
    color: #f8fafc;
  }

  .gauge-bar {
    height: 8px;
    background: #0f172a;
    border-radius: 4px;
    overflow: hidden;
  }

  .gauge-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
  }

  .host-info-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-size: 0.8rem;
    color: #94a3b8;
  }

  .host-info-card h4 {
    margin: 0 0 0.5rem 0;
    color: #f8fafc;
    font-size: 0.85rem;
  }

  .host-details div {
    margin-bottom: 0.3rem;
  }

  @media (max-width: 900px) {
    .console-grid {
      grid-template-columns: 1fr;
    }
    .round-nav {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
