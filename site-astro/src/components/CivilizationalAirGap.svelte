<script lang="ts">
  import layer2Data from '../data/hsri_layer2.json';

  interface CountryLayer2 {
    country_iso3: string;
    overall_score: number;
    h_layer1: number;
    h_layer2: number;
    v_asi: number;
    rank_layer1: number;
    rank_layer2: number;
    rank_delta_sovereignty: number;
    t_half_hours: number;
    vsr: number;
    v_coord: number;
    p5_epistemic: number;
    p6_decoupling: number;
    p7_coordination: number;
    p8_post_labor: number;
    layer2_bottleneck: string;
    fragility_tier: string;
    high_compute_trap: boolean;
  }

  // Country name mapping
  const countryNames: Record<string, string> = {
    NOR: 'Norway', FIN: 'Finland', ISL: 'Iceland', DNK: 'Denmark', SWE: 'Sweden',
    AUT: 'Austria', DEU: 'Germany', NLD: 'Netherlands', CHE: 'Switzerland', CAN: 'Canada',
    NZL: 'New Zealand', AUS: 'Australia', JPN: 'Japan', GBR: 'United Kingdom', FRA: 'France',
    IRL: 'Ireland', BEL: 'Belgium', EST: 'Estonia', LUX: 'Luxembourg', ESP: 'Spain',
    ITA: 'Italy', PRT: 'Portugal', CZE: 'Czech Republic', SVN: 'Slovenia', POL: 'Poland',
    SVK: 'Slovakia', LTU: 'Lithuania', LVA: 'Latvia', GRC: 'Greece', CYP: 'Cyprus',
    MLT: 'Malta', HUN: 'Hungary', BGR: 'Bulgaria', ROU: 'Romania', MKD: 'North Macedonia',
    ISR: 'Israel', KOR: 'South Korea', USA: 'United States', SGP: 'Singapore', HKG: 'Hong Kong'
  };

  const countries: CountryLayer2[] = (layer2Data as CountryLayer2[]).sort((a, b) => {
    const nameA = countryNames[a.country_iso3] || a.country_iso3;
    const nameB = countryNames[b.country_iso3] || b.country_iso3;
    return nameA.localeCompare(nameB);
  });

  // Selected state
  let selectedIso = 'SGP';
  let blackoutHours = 72;

  $: selectedCountry = countries.find(c => c.country_iso3 === selectedIso) || countries[0];

  // Duration presets
  const presets = [
    { label: '12 Hours', hours: 12 },
    { label: '24 Hours', hours: 24 },
    { label: '48 Hours', hours: 48 },
    { label: '72 Hours (Default)', hours: 72 },
    { label: '7 Days (168h)', hours: 168 },
    { label: '30 Days (720h)', hours: 720 },
  ];

  // Mathematical Decoupling Decay: 1 - 2^(-t / T_half)
  $: tHalf = selectedCountry ? selectedCountry.t_half_hours : 24.0;
  $: decayFraction = 1.0 - Math.pow(2, -blackoutHours / Math.max(1.0, tHalf));
  $: decayPercent = Math.min(100, Math.max(0, decayFraction * 100));
  $: survivalPercent = Math.max(0, 100 - decayPercent);

  // Sector failure thresholds relative to T_half
  interface Sector {
    id: string;
    name: string;
    thresholdMultiplier: number;
    description: string;
  }

  const sectors: Sector[] = [
    {
      id: 'finance',
      name: 'Financial Settlement & Clearing',
      thresholdMultiplier: 0.5,
      description: 'High-frequency algorithmic liquidity provision, clearing houses, and cross-border payment settlement.'
    },
    {
      id: 'telecom',
      name: 'Telecommunications & Cloud Mesh',
      thresholdMultiplier: 1.0,
      description: 'Dynamic traffic routing, autonomous peering, edge microservices, and remote API gateways.'
    },
    {
      id: 'energy',
      name: 'Smart Energy & Grid Dispatch',
      thresholdMultiplier: 1.5,
      description: 'Renewable intermittency balancing, automated substation switching, and load forecasting.'
    },
    {
      id: 'health',
      name: 'Emergency Health & Supply Chains',
      thresholdMultiplier: 2.0,
      description: 'Hospital bed allocation triage, pharmaceutical cold-chain logistics, and automated dispatch.'
    },
    {
      id: 'governance',
      name: 'Institutional & Civil Continuity',
      thresholdMultiplier: 3.0,
      description: 'Administrative decision registries, emergency statutory enforcement, and judicial scheduling.'
    }
  ];

  function getSectorStatus(multiplier: number, tHalfH: number, blackoutH: number) {
    const failureH = multiplier * tHalfH;
    const ratio = blackoutH / Math.max(0.1, failureH);

    if (ratio < 0.6) {
      return { label: 'OPERATIONAL', color: '#10b981', badgeClass: 'badge-nominal', progress: ratio * 100 };
    } else if (ratio < 1.0) {
      return { label: 'DEGRADED', color: '#f59e0b', badgeClass: 'badge-warning', progress: ratio * 100 };
    } else if (ratio < 2.0) {
      return { label: 'CRITICAL FAILURE', color: '#ef4444', badgeClass: 'badge-danger', progress: 100 };
    } else {
      return { label: 'CATASTROPHIC COLLAPSE', color: '#7f1d1d', badgeClass: 'badge-severe', progress: 100 };
    }
  }
</script>

<div class="airgap-simulator" id="airgap-simulator-root">
  <div class="sim-header">
    <div class="header-titles">
      <div class="badge-tag">LAYER 2 EMPIRICAL SIMULATOR</div>
      <h3>Civilizational Air-Gap Decoupling Simulator</h3>
      <p class="sim-desc">
        Simulates an abrupt, zero-notice synthetic intelligence network severance (72-Hour Air-Gap Scenario).
        Measures the empirical cascading collapse of critical institutional infrastructure under national 
        Decoupling Half-Life ($T_&#123;\text&#123;half&#125;&#125;$) constraints.
      </p>
    </div>
  </div>

  <!-- Control Controls Panel -->
  <div class="control-grid">
    <!-- Country Selector -->
    <div class="control-card">
      <label for="country-select" class="control-label">Target Nation (39 Benchmark Nations):</label>
      <select id="country-select" bind:value={selectedIso} class="styled-select">
        {#each countries as c}
          <option value={c.country_iso3}>
            {countryNames[c.country_iso3] || c.country_iso3} ({c.country_iso3}) — T_half: {c.t_half_hours >= 720 ? `${Math.round(c.t_half_hours / 24)} days` : `${c.t_half_hours}h`}
          </option>
        {/each}
      </select>
      <div class="country-meta">
        <span class="meta-item">
          <strong>Adoption Rank (Layer 1):</strong> #{selectedCountry.rank_layer1}
        </span>
        <span class="meta-item">
          <strong>Sovereignty Rank (Layer 2):</strong> #{selectedCountry.rank_layer2}
        </span>
        <span class="meta-item rank-delta" class:negative={selectedCountry.rank_delta_sovereignty < 0}>
          <strong>Rank Shift:</strong> {selectedCountry.rank_delta_sovereignty > 0 ? `+${selectedCountry.rank_delta_sovereignty}` : selectedCountry.rank_delta_sovereignty}
        </span>
      </div>
    </div>

    <!-- Blackout Duration Slider -->
    <div class="control-card">
      <div class="slider-title-row">
        <span class="control-label">Synthetic Blackout Duration:</span>
        <span class="duration-display">{blackoutHours} Hours ({Math.round((blackoutHours / 24) * 10) / 10} Days)</span>
      </div>
      <input
        type="range"
        id="blackout-slider"
        min="6"
        max="336"
        step="6"
        bind:value={blackoutHours}
        class="styled-range"
      />
      <div class="presets-row">
        {#each presets as p}
          <button
            class="preset-btn"
            class:active={blackoutHours === p.hours}
            on:click={() => blackoutHours = p.hours}
          >
            {p.label}
          </button>
        {/each}
      </div>
    </div>
  </div>

  <!-- Simulation KPI Banner -->
  <div class="kpi-banner" class:trap-active={selectedCountry.high_compute_trap}>
    <div class="kpi-col">
      <span class="kpi-label">Decoupling Half-Life (T_half)</span>
      <span class="kpi-value text-accent">
        {selectedCountry.t_half_hours >= 720 ? `${Math.round(selectedCountry.t_half_hours / 24)} Days` : `${selectedCountry.t_half_hours} Hours`}
      </span>
      <span class="kpi-sub">Critical institutional decay halving interval</span>
    </div>

    <div class="kpi-col">
      <span class="kpi-label">Systemic Operational Decay</span>
      <span class="kpi-value" class:text-danger={decayPercent > 50} class:text-warning={decayPercent > 20 && decayPercent <= 50} class:text-success={decayPercent <= 20}>
        {decayPercent.toFixed(1)}%
      </span>
      <span class="kpi-sub">Autonomous functions rendered non-operational</span>
    </div>

    <div class="kpi-col">
      <span class="kpi-label">Residual Unassisted Agency</span>
      <span class="kpi-value" class:text-success={survivalPercent >= 70} class:text-warning={survivalPercent >= 30 && survivalPercent < 70} class:text-danger={survivalPercent < 30}>
        {survivalPercent.toFixed(1)}%
      </span>
      <span class="kpi-sub">Human unassisted operational capacity</span>
    </div>

    <div class="kpi-col">
      <span class="kpi-label">Vulnerability Trap Alert</span>
      <span class="kpi-value" class:text-danger={selectedCountry.high_compute_trap}>
        {selectedCountry.high_compute_trap ? 'TRAP DETECTED' : 'BALANCED BUFFER'}
      </span>
      <span class="kpi-sub">V_ASI: {selectedCountry.v_asi.toFixed(3)}</span>
    </div>
  </div>

  <!-- Sector Failure Cascading Breakdown -->
  <div class="sectors-section">
    <div class="section-title-row">
      <h4>Infrastructure Sector Failure Sequence ($t = {blackoutHours}\text&#123;h&#125;$)</h4>
      <span class="legend-note">Calculated against $T_&#123;\text&#123;half&#125;&#125; = {selectedCountry.t_half_hours}\text&#123;h&#125;$</span>
    </div>

    <div class="sectors-grid">
      {#each sectors as sec}
        {@const status = getSectorStatus(sec.thresholdMultiplier, selectedCountry.t_half_hours, blackoutHours)}
        {@const failThresholdH = sec.thresholdMultiplier * selectedCountry.t_half_hours}
        <div class="sector-card" style="border-left: 4px solid {status.color};">
          <div class="sector-card-top">
            <div class="sec-meta">
              <span class="sec-name">{sec.name}</span>
              <span class="sec-threshold">Failure Threshold: {failThresholdH >= 24 ? `${Math.round(failThresholdH / 24 * 10) / 10}d` : `${failThresholdH}h`}</span>
            </div>
            <span class="status-badge {status.badgeClass}">{status.label}</span>
          </div>
          <p class="sec-desc">{sec.description}</p>
          <div class="stress-bar-wrapper">
            <div class="stress-bar-fill" style="width: {Math.min(100, (blackoutHours / Math.max(0.1, failThresholdH)) * 100)}%; background-color: {status.color};"></div>
          </div>
          <div class="stress-bar-labels">
            <span>0h (Cutoff)</span>
            <span>Threshold: {failThresholdH}h</span>
            <span>Active: {blackoutHours}h</span>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Analytical Takeaway Drawer -->
  <div class="analysis-box">
    <div class="analysis-header">
      <span class="analysis-tag">ECONOMETRIC FINDING</span>
      <h5>The High-Compute Decoupling Asymmetry</h5>
    </div>
    <p>
      {#if selectedCountry.high_compute_trap}
        <strong>{countryNames[selectedCountry.country_iso3] || selectedCountry.country_iso3}</strong> exhibits an acute 
        <em>High-Compute Vulnerability Trap</em>. While ranking <strong>#{selectedCountry.rank_layer1}</strong> in conventional AI adoption 
        due to massive compute density and digital infrastructure, its Civilizational Decoupling Half-Life is only 
        <strong>{selectedCountry.t_half_hours} hours</strong>. In an unannounced 72-hour air-gap scenario, over 
        <strong>{decayPercent.toFixed(1)}%</strong> of systemic administrative and financial coordination fails, dropping it to 
        <strong>#{selectedCountry.rank_layer2}</strong> in global sovereign survival capability.
      {:else}
        <strong>{countryNames[selectedCountry.country_iso3] || selectedCountry.country_iso3}</strong> maintains 
        resilient sovereign reserves with a Decoupling Half-Life of <strong>{selectedCountry.t_half_hours >= 720 ? `${Math.round(selectedCountry.t_half_hours / 24)} days` : `${selectedCountry.t_half_hours} hours`}</strong>. 
        Its deep analog fallback protocols, decentralized energy balancing, and robust unassisted human institutional agency 
        limit 72-hour operational degradation to just <strong>{decayPercent.toFixed(1)}%</strong>, preserving sovereign continuity.
      {/if}
    </p>
  </div>
</div>

<style>
  .airgap-simulator {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 2rem;
    color: #f1f5f9;
    font-family: inherit;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    margin: 2rem 0;
  }

  .badge-tag {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.25);
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    margin-bottom: 0.5rem;
  }

  .sim-header h3 {
    font-size: 1.6rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    color: #ffffff;
  }

  .sim-desc {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.5;
    max-width: 900px;
    margin: 0;
  }

  .control-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin: 1.75rem 0;
  }

  @media (max-width: 768px) {
    .control-grid {
      grid-template-columns: 1fr;
    }
  }

  .control-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .control-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #cbd5e1;
  }

  .styled-select {
    background: #0f172a;
    color: #f8fafc;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 0.6rem 0.75rem;
    font-size: 0.95rem;
    cursor: pointer;
    outline: none;
    transition: border-color 0.15s;
  }

  .styled-select:focus {
    border-color: #38bdf8;
  }

  .country-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    font-size: 0.8rem;
    color: #94a3b8;
  }

  .rank-delta {
    color: #34d399;
  }

  .rank-delta.negative {
    color: #f87171;
  }

  .slider-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .duration-display {
    font-size: 1rem;
    font-weight: 700;
    color: #38bdf8;
  }

  .styled-range {
    width: 100%;
    accent-color: #38bdf8;
    cursor: pointer;
  }

  .presets-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .preset-btn {
    background: #0f172a;
    border: 1px solid #334155;
    color: #94a3b8;
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.15s;
  }

  .preset-btn:hover {
    color: #f8fafc;
    border-color: #475569;
  }

  .preset-btn.active {
    background: rgba(56, 189, 248, 0.15);
    border-color: #38bdf8;
    color: #38bdf8;
    font-weight: 600;
  }

  .kpi-banner {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 8px;
    padding: 1.25rem;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  @media (max-width: 900px) {
    .kpi-banner {
      grid-template-columns: 1fr 1fr;
    }
  }

  @media (max-width: 500px) {
    .kpi-banner {
      grid-template-columns: 1fr;
    }
  }

  .kpi-banner.trap-active {
    border-color: rgba(239, 68, 68, 0.4);
    background: linear-gradient(180deg, #111827 0%, rgba(239, 68, 68, 0.05) 100%);
  }

  .kpi-col {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .kpi-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    font-weight: 600;
  }

  .kpi-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: #f8fafc;
  }

  .kpi-sub {
    font-size: 0.75rem;
    color: #64748b;
  }

  .text-accent { color: #38bdf8; }
  .text-danger { color: #ef4444; }
  .text-warning { color: #f59e0b; }
  .text-success { color: #10b981; }

  .sectors-section {
    margin-bottom: 2rem;
  }

  .section-title-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1rem;
  }

  .section-title-row h4 {
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0;
    color: #ffffff;
  }

  .legend-note {
    font-size: 0.8rem;
    color: #64748b;
  }

  .sectors-grid {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
  }

  .sector-card {
    background: #1e293b;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .sector-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .sec-meta {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
  }

  .sec-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f8fafc;
  }

  .sec-threshold {
    font-size: 0.75rem;
    color: #94a3b8;
  }

  .sec-desc {
    font-size: 0.825rem;
    color: #94a3b8;
    margin: 0;
    line-height: 1.4;
  }

  .status-badge {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    text-transform: uppercase;
  }

  .badge-nominal {
    background: rgba(16, 185, 129, 0.2);
    color: #34d399;
  }

  .badge-warning {
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
  }

  .badge-danger {
    background: rgba(239, 68, 68, 0.25);
    color: #f87171;
  }

  .badge-severe {
    background: rgba(127, 29, 29, 0.6);
    color: #fca5a5;
    border: 1px solid #ef4444;
  }

  .stress-bar-wrapper {
    height: 8px;
    background: #0f172a;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 0.25rem;
  }

  .stress-bar-fill {
    height: 100%;
    transition: width 0.3s ease;
  }

  .stress-bar-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: #64748b;
  }

  .analysis-box {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1.25rem;
  }

  .analysis-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
  }

  .analysis-tag {
    font-size: 0.7rem;
    font-weight: 700;
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
  }

  .analysis-header h5 {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0;
  }

  .analysis-box p {
    font-size: 0.875rem;
    color: #cbd5e1;
    line-height: 1.5;
    margin: 0;
  }

  .analysis-box em {
    color: #f59e0b;
    font-style: normal;
    font-weight: 600;
  }
</style>
