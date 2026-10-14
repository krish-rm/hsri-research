<script lang="ts">
  import drillData from '../data/decoupling_drill_results.json';
  import DecouplingDrillConsole from './DecouplingDrillConsole.svelte';

  let viewMode: 'viewer' | 'console' = 'viewer';

  let selectedArchetype = 'archetype_a';
  let currentHour = 24; // Default to Day 1

  $: archetype = drillData.archetypes[selectedArchetype];
  $: timeline = archetype.timeline;
  $: currentStep = timeline.find((p: any) => p.hour >= currentHour) || timeline[timeline.length - 1];

  $: activeInjects = drillData.crisis_injects.filter((inj: any) => inj.hour <= currentHour);
  $: latestInject = activeInjects.length > 0 ? activeInjects[activeInjects.length - 1] : null;

  function setArchetype(key: string) {
    selectedArchetype = key;
  }

  function getHealthColor(val: number): string {
    if (val >= 0.70) return '#10b981'; // Green
    if (val >= 0.40) return '#f59e0b'; // Amber
    return '#ef4444'; // Red
  }
</script>

<div class="drill-container">
  <!-- Header & Controls -->
  <div class="drill-header">
    <div class="title-badge">HSRI 2.0 TABLETOP EXERCISE SIMULATOR</div>
    <h2>Operation Silent Cloud: Civilizational Decoupling Drill</h2>
    <p class="subtitle">
      Simulating a 14-day (336-hour) zero-notice global AI cloud severance quarantine across critical societal subsystems.
    </p>

    <!-- Mode Switcher -->
    <div class="mode-switcher">
      <button 
        class="mode-btn {viewMode === 'viewer' ? 'active' : ''}" 
        on:click={() => viewMode = 'viewer'}
      >
        📊 Operational Trajectory Mode
      </button>
      <button 
        class="mode-btn {viewMode === 'console' ? 'active' : ''}" 
        on:click={() => viewMode = 'console'}
      >
        ⚡ Tabletop Facilitator Console (Live Simulation)
      </button>
    </div>
  </div>

  {#if viewMode === 'console'}
    <DecouplingDrillConsole />
  {:else}
    <!-- Archetype Selector Tabs -->
    <div class="archetype-tabs">
      <button 
        class="tab-btn {selectedArchetype === 'archetype_a' ? 'active' : ''}" 
        on:click={() => setArchetype('archetype_a')}
      >
        <span class="flag">🇸🇬 / 🇭🇰</span>
        <span class="tab-label">Archetype A: Hyper-Automated Hostage</span>
      </button>

      <button 
        class="tab-btn {selectedArchetype === 'archetype_b' ? 'active' : ''}" 
        on:click={() => setArchetype('archetype_b')}
      >
        <span class="flag">🇺🇸</span>
        <span class="tab-label">Archetype B: Fragmented Superpower</span>
      </button>

      <button 
        class="tab-btn {selectedArchetype === 'archetype_c' ? 'active' : ''}" 
        on:click={() => setArchetype('archetype_c')}
      >
        <span class="flag">🇳🇴 / 🇨🇭 / 🇫🇮</span>
        <span class="tab-label">Archetype C: Resilient Decentralizer</span>
      </button>
    </div>

  <!-- Main Simulation Grid -->
  <div class="drill-grid">
    <!-- Left Column: Controls & Dynamic Telemetry -->
    <div class="telemetry-card">
      <div class="card-header">
        <h3>{archetype.name}</h3>
        <span class="posture-tag">{archetype.sovereign_posture}</span>
      </div>
      <p class="arch-desc">{archetype.description}</p>

      <!-- Time Slider -->
      <div class="time-control-box">
        <div class="slider-meta">
          <span class="time-readout">Elapsed Time: <strong>T + {currentHour} Hours</strong> (Day {(currentHour / 24).toFixed(1)})</span>
          <span class="max-time">Limit: 336h (Day 14)</span>
        </div>
        <input 
          type="range" 
          min="0" 
          max="336" 
          step="2" 
          bind:value={currentHour} 
          class="time-slider"
        />
        <div class="slider-marks">
          <span>T=0h</span>
          <span>Day 2 (48h)</span>
          <span>Day 5 (120h)</span>
          <span>Day 7 (168h)</span>
          <span>Day 10 (240h)</span>
          <span>Day 14 (336h)</span>
        </div>
      </div>

      <!-- Leontief Composite Score Display -->
      <div class="composite-display">
        <div class="composite-label">LEONTIEF WEAKEST-LINK FUNCTIONALITY</div>
        <div class="composite-value" style="color: {getHealthColor(currentStep.leontief_composite)}">
          {(currentStep.leontief_composite * 100).toFixed(1)}%
        </div>
        <div class="bottleneck-indicator">
          Governing Bottleneck: <strong>{currentStep.weakest_link.replace('_', ' ').toUpperCase()}</strong>
        </div>
      </div>

      <!-- Subsystem Telemetry Bars -->
      <div class="subsystems-breakdown">
        <h4>Critical Societal Subsystems</h4>

        <div class="subsystem-row">
          <div class="sub-meta">
            <span>⚡ Power Grid Dispatch</span>
            <span class="score" style="color: {getHealthColor(currentStep.power_grid)}">{(currentStep.power_grid * 100).toFixed(1)}%</span>
          </div>
          <div class="bar-bg">
            <div class="bar-fill" style="width: {currentStep.power_grid * 100}%; background-color: {getHealthColor(currentStep.power_grid)}"></div>
          </div>
        </div>

        <div class="subsystem-row">
          <div class="sub-meta">
            <span>🏦 Interbank Financial Clearing</span>
            <span class="score" style="color: {getHealthColor(currentStep.financial_clearing)}">{(currentStep.financial_clearing * 100).toFixed(1)}%</span>
          </div>
          <div class="bar-bg">
            <div class="bar-fill" style="width: {currentStep.financial_clearing * 100}%; background-color: {getHealthColor(currentStep.financial_clearing)}"></div>
          </div>
        </div>

        <div class="subsystem-row">
          <div class="sub-meta">
            <span>🚛 Food & Medical Logistics</span>
            <span class="score" style="color: {getHealthColor(currentStep.food_logistics)}">{(currentStep.food_logistics * 100).toFixed(1)}%</span>
          </div>
          <div class="bar-bg">
            <div class="bar-fill" style="width: {currentStep.food_logistics * 100}%; background-color: {getHealthColor(currentStep.food_logistics)}"></div>
          </div>
        </div>

        <div class="subsystem-row">
          <div class="sub-meta">
            <span>📡 Core Telecommunications</span>
            <span class="score" style="color: {getHealthColor(currentStep.telecommunications)}">{(currentStep.telecommunications * 100).toFixed(1)}%</span>
          </div>
          <div class="bar-bg">
            <div class="bar-fill" style="width: {currentStep.telecommunications * 100}%; background-color: {getHealthColor(currentStep.telecommunications)}"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Crisis Injects & Summary Matrix -->
    <div class="injects-card">
      <div class="card-header">
        <h3>Cabinet Crisis Injects Timeline</h3>
        <span class="inject-counter">{activeInjects.length} / {drillData.crisis_injects.length} Injects Active</span>
      </div>

      {#if latestInject}
        <div class="latest-inject-banner">
          <div class="inject-tag">{latestInject.inject_code} (Hour {latestInject.hour})</div>
          <h4>{latestInject.title}</h4>
          <p>{latestInject.description}</p>
        </div>
      {/if}

      <div class="injects-scroll">
        {#each drillData.crisis_injects as inj}
          <div class="inject-item {inj.hour <= currentHour ? 'active' : 'pending'}">
            <div class="inj-time">T + {inj.hour}h</div>
            <div class="inj-body">
              <div class="inj-title">
                <strong>{inj.inject_code}: {inj.title}</strong>
                <span class="badge {inj.severity.toLowerCase()}">{inj.severity}</span>
              </div>
              <p class="inj-text">{inj.description}</p>
            </div>
          </div>
        {/each}
      </div>

      <!-- Comparative Archetype Summary Table -->
      <div class="archetype-summary-table">
        <h4>14-Day Archetype Comparison</h4>
        <table>
          <thead>
            <tr>
              <th>Archetype</th>
              <th>Fracture (&lt;90%)</th>
              <th>Half-Life (&lt;50%)</th>
              <th>Day 14 Residual</th>
            </tr>
          </thead>
          <tbody>
            {#each Object.entries(drillData.archetypes) as [k, a]}
              <tr class="{selectedArchetype === k ? 'selected-row' : ''}">
                <td><strong>{a.exemplars[0]}</strong></td>
                <td>T + {a.metrics.t_first_fracture_hours}h</td>
                <td>T + {a.metrics.t_half_crossing_hours}h</td>
                <td style="color: {getHealthColor(a.metrics.day_14_residual_functionality)}">
                  {(a.metrics.day_14_residual_functionality * 100).toFixed(1)}%
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  </div>

  {/if}

  <!-- Bottom Action Footer -->
  <div class="drill-footer">
    <div class="footer-note">
      <strong>Citation & Permanent DOI:</strong> HSRI Research Consortium. (2026). Operation Silent Cloud Decoupling Drill. Zenodo. 
      <a href="https://doi.org/10.5281/zenodo.10842000" target="_blank" rel="noopener noreferrer">10.5281/zenodo.10842000</a>
    </div>
    <div class="footer-links">
      <a href="https://github.com/krish-rm/hsri-research/blob/main/research/tabletop/decoupling_drill_protocol.md" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">
        View Exercise Protocol (.md)
      </a>
      <a href="https://github.com/krish-rm/hsri-research/blob/main/research/tabletop/when_the_cloud_goes_silent.md" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
        Read Whitepaper (.md)
      </a>
    </div>
  </div>
</div>

<style>
  .mode-switcher {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    margin: 1.5rem 0 0.5rem 0;
  }

  .mode-btn {
    background: #1e293b;
    border: 1px solid #334155;
    color: #94a3b8;
    padding: 0.65rem 1.25rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .mode-btn:hover {
    color: #f8fafc;
    border-color: #475569;
  }

  .mode-btn.active {
    background: #0284c7;
    color: #f8fafc;
    border-color: #38bdf8;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.25);
  }

  .drill-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    font-family: inherit;
    color: var(--text-primary, #1e293b);
  }

  .drill-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .title-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: rgba(37, 99, 235, 0.1);
    color: #2563eb;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-bottom: 0.75rem;
  }

  .drill-header h2 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 0.5rem;
  }

  .subtitle {
    font-size: 1rem;
    color: var(--text-secondary, #64748b);
    max-width: 700px;
    margin: 0 auto 1.5rem;
  }

  .archetype-tabs {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .tab-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.25rem;
    border: 1px solid var(--border-color, #e2e8f0);
    background: var(--surface-color, #ffffff);
    border-radius: 0.5rem;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary, #1e293b);
    transition: all 0.2s;
  }

  .tab-btn:hover {
    border-color: #2563eb;
  }

  .tab-btn.active {
    background: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
  }

  .drill-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  @media (max-width: 900px) {
    .drill-grid {
      grid-template-columns: 1fr;
    }
  }

  .telemetry-card, .injects-card {
    background: var(--surface-color, #ffffff);
    border: 1px solid var(--border-color, #e2e8f0);
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
  }

  .card-header h3 {
    margin: 0;
    font-size: 1.25rem;
  }

  .posture-tag {
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.5rem;
    background: #f1f5f9;
    border-radius: 0.25rem;
  }

  .arch-desc {
    font-size: 0.875rem;
    color: var(--text-secondary, #64748b);
    margin-bottom: 1.5rem;
  }

  .time-control-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 1.5rem;
  }

  .slider-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
  }

  .time-slider {
    width: 100%;
    margin-bottom: 0.5rem;
  }

  .slider-marks {
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: #94a3b8;
  }

  .composite-display {
    text-align: center;
    padding: 1.25rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    margin-bottom: 1.5rem;
  }

  .composite-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: #64748b;
    margin-bottom: 0.25rem;
  }

  .composite-value {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.5rem;
  }

  .bottleneck-indicator {
    font-size: 0.85rem;
    color: #475569;
  }

  .subsystems-breakdown h4 {
    font-size: 1rem;
    margin: 0 0 1rem;
  }

  .subsystem-row {
    margin-bottom: 1rem;
  }

  .sub-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .bar-bg {
    width: 100%;
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    transition: width 0.3s ease;
  }

  .inject-counter {
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.5rem;
    background: #eff6ff;
    color: #2563eb;
    border-radius: 0.25rem;
  }

  .latest-inject-banner {
    background: #fff7ed;
    border-left: 4px solid #f97316;
    padding: 1rem;
    border-radius: 0.25rem;
    margin-bottom: 1rem;
  }

  .latest-inject-banner .inject-tag {
    font-size: 0.7rem;
    font-weight: 800;
    color: #ea580c;
    text-transform: uppercase;
  }

  .latest-inject-banner h4 {
    margin: 0.25rem 0 0.5rem;
    font-size: 1rem;
    color: #9a3412;
  }

  .latest-inject-banner p {
    margin: 0;
    font-size: 0.85rem;
    color: #7c2d12;
  }

  .injects-scroll {
    max-height: 280px;
    overflow-y: auto;
    margin-bottom: 1.5rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    padding: 0.5rem;
  }

  .inject-item {
    display: flex;
    gap: 0.75rem;
    padding: 0.75rem;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.85rem;
  }

  .inject-item:last-child {
    border-bottom: none;
  }

  .inject-item.pending {
    opacity: 0.4;
  }

  .inj-time {
    font-weight: 700;
    color: #2563eb;
    white-space: nowrap;
  }

  .inj-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
  }

  .badge {
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.1rem 0.4rem;
    border-radius: 0.25rem;
  }

  .badge.critical { background: #fee2e2; color: #b91c1c; }
  .badge.high { background: #ffedd5; color: #c2410c; }
  .badge.medium { background: #fef9c3; color: #854d0e; }

  .inj-text {
    margin: 0;
    color: #64748b;
    font-size: 0.8rem;
  }

  .archetype-summary-table table {
    width: 100%;
    font-size: 0.8rem;
    border-collapse: collapse;
  }

  .archetype-summary-table th, .archetype-summary-table td {
    padding: 0.5rem;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
  }

  .selected-row {
    background: #f0fdf4;
  }

  .drill-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--surface-color, #ffffff);
    border: 1px solid var(--border-color, #e2e8f0);
    border-radius: 0.75rem;
  }

  .footer-note {
    font-size: 0.85rem;
    color: #64748b;
  }

  .footer-links {
    display: flex;
    gap: 0.75rem;
  }

  .btn {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    font-weight: 600;
    border-radius: 0.375rem;
    text-decoration: none;
    transition: all 0.2s;
  }

  .btn-secondary {
    background: #f1f5f9;
    color: #334155;
  }

  .btn-secondary:hover {
    background: #e2e8f0;
  }

  .btn-primary {
    background: #2563eb;
    color: #ffffff;
  }

  .btn-primary:hover {
    background: #1d4ed8;
  }
</style>
