<script lang="ts">
  import precursorSummary from '../data/precursor_summary.json';
  import wedgeHistory from '../data/wedge_history.json';
  import asiPrecursors from '../data/asi_precursors.json';
  import layer2Data from '../data/hsri_layer2.json';
  import CivilizationalAirGap from './CivilizationalAirGap.svelte';
  import TelemetryUptimeBadge from './TelemetryUptimeBadge.svelte';

  // Navigation tab state
  let activeTab: 'radar' | 'tripwires' | 'dual_layer' | 'airgap' = 'radar';

  // Filter states for 14 Tripwires
  let tripwireStatusFilter: 'all' | 'red' | 'amber' | 'green' = 'all';
  let tripwireTypeFilter: 'all' | 'leading' | 'coincident' | 'lagging' = 'all';
  let tripwireSearch = '';
  let selectedPrecursorId: string | null = 'PREC-011';

  // Dual-Layer Leaderboard state
  let leaderboardMode: 'layer1' | 'layer2' | 'delta' = 'layer2';
  let filterTrapOnly = false;
  let countrySearch = '';

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

  // Filtered Precursors
  $: filteredPrecursors = asiPrecursors.filter(p => {
    const matchStatus = tripwireStatusFilter === 'all' || p.status_color === tripwireStatusFilter;
    const matchType = tripwireTypeFilter === 'all' || p.indicator_type === tripwireTypeFilter;
    const matchSearch = tripwireSearch === '' ||
      p.id.toLowerCase().includes(tripwireSearch.toLowerCase()) ||
      p.description.toLowerCase().includes(tripwireSearch.toLowerCase()) ||
      p.proposed_threshold.toLowerCase().includes(tripwireSearch.toLowerCase());
    return matchStatus && matchType && matchSearch;
  });

  $: selectedPrecursor = asiPrecursors.find(p => p.id === selectedPrecursorId) || asiPrecursors[0];

  // Sorted Leaderboard
  interface Layer2Entry {
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
    layer2_bottleneck: string;
    fragility_tier: string;
    high_compute_trap: boolean;
  }

  const rawEntries: Layer2Entry[] = layer2Data as Layer2Entry[];

  $: sortedEntries = [...rawEntries]
    .filter(e => {
      const name = countryNames[e.country_iso3] || e.country_iso3;
      const matchSearch = countrySearch === '' ||
        e.country_iso3.toLowerCase().includes(countrySearch.toLowerCase()) ||
        name.toLowerCase().includes(countrySearch.toLowerCase());
      const matchTrap = !filterTrapOnly || e.high_compute_trap;
      return matchSearch && matchTrap;
    })
    .sort((a, b) => {
      if (leaderboardMode === 'layer1') {
        return a.rank_layer1 - b.rank_layer1;
      } else if (leaderboardMode === 'layer2') {
        return a.rank_layer2 - b.rank_layer2;
      } else {
        // Sort by rank delta (largest plunge first)
        return a.rank_delta_sovereignty - b.rank_delta_sovereignty;
      }
    });

  // Precursor count statistics
  $: countRed = asiPrecursors.filter(p => p.status_color === 'red').length;
  $: countAmber = asiPrecursors.filter(p => p.status_color === 'amber').length;
  $: countGreen = asiPrecursors.filter(p => p.status_color === 'green').length;
</script>

<div class="seismograph-container" id="seismograph-root">
  <!-- Top Hero Status Bar -->
  <div class="sentinel-hero-banner">
    <div class="sentinel-status-badge">
      <span class="pulse-dot"></span>
      <span>LIVE SENTINEL TELEMETRY ACTIVE</span>
    </div>
    <div class="hero-main-row">
      <div class="hero-left">
        <h2>The ASI Precursor Seismograph</h2>
        <p class="hero-lead">
          Continuous global telemetry tracking the cognitive, algorithmic, and institutional boundary conditions
          preceding Artificial Superintelligence.
        </p>
      </div>
      <div class="hero-right">
        <div class="master-threat-card">
          <span class="threat-title">Master Precursor Threat Level</span>
          <div class="threat-score-row">
            <span class="threat-score">{precursorSummary.master_precursor_threat_score.toFixed(2)}</span>
            <span class="threat-max">/ 10.0</span>
          </div>
          <span class="threat-regime">{precursorSummary.overall_classification}</span>
        </div>
      </div>
    </div>
  </div>

  <TelemetryUptimeBadge />

  <!-- Primary Sub-navigation Tabs -->
  <div class="tab-navigation" role="tablist">
    <button
      class="tab-btn"
      class:active={activeTab === 'radar'}
      on:click={() => activeTab = 'radar'}
      role="tab"
      aria-selected={activeTab === 'radar'}
    >
      <span class="tab-icon">⚡</span>
      <span>CORS & Triad Radar</span>
    </button>
    <button
      class="tab-btn"
      class:active={activeTab === 'tripwires'}
      on:click={() => activeTab = 'tripwires'}
      role="tab"
      aria-selected={activeTab === 'tripwires'}
    >
      <span class="tab-icon">🚨</span>
      <span>14 Precursor Tripwires</span>
      <span class="tab-counter red">{countRed} Active</span>
    </button>
    <button
      class="tab-btn"
      class:active={activeTab === 'dual_layer'}
      on:click={() => activeTab = 'dual_layer'}
      role="tab"
      aria-selected={activeTab === 'dual_layer'}
    >
      <span class="tab-icon">⚖️</span>
      <span>Dual-Layer Leaderboard</span>
    </button>
    <button
      class="tab-btn"
      class:active={activeTab === 'airgap'}
      on:click={() => activeTab = 'airgap'}
      role="tab"
      aria-selected={activeTab === 'airgap'}
    >
      <span class="tab-icon">🛡️</span>
      <span>Air-Gap Decoupling Simulator</span>
    </button>
  </div>

  <!-- TAB 1: RADAR & TRIAD TELEMETRY -->
  {#if activeTab === 'radar'}
    <div class="tab-content radar-view">
      <!-- CORS Live Gauge Banner -->
      <div class="cors-gauge-card">
        <div class="cors-gauge-header">
          <div>
            <div class="gauge-tag">STREAM 3: VERIFICATION WEDGE ACCELEROMETER</div>
            <h3>Cognitive Oversight Richter Scale (CORS)</h3>
          </div>
          <div class="cors-score-badge">
            <span class="cors-number">{precursorSummary.stream_3_verification_wedge.cors_rating.toFixed(1)}</span>
            <span class="cors-unit">/ 10.0</span>
          </div>
        </div>

        <div class="cors-regime-banner">
          <span class="regime-name">{precursorSummary.stream_3_verification_wedge.cors_label}</span>
          <span class="regime-desc">Verification latency wedge exceeds human biological real-time supervision threshold.</span>
        </div>

        <div class="cors-metrics-strip">
          <div class="metric-block">
            <span class="m-label">Latency Wedge (ΔT_wedge)</span>
            <span class="m-val text-accent">{precursorSummary.stream_3_verification_wedge.delta_t_seconds.toLocaleString()}s</span>
            <span class="m-sub">≈ {(precursorSummary.stream_3_verification_wedge.delta_t_seconds / 60).toFixed(1)} min verification deficit</span>
          </div>
          <div class="metric-block">
            <span class="m-label">Wedge Ratio (R_wedge)</span>
            <span class="m-val text-danger">{precursorSummary.stream_3_verification_wedge.wedge_ratio.toLocaleString()}x</span>
            <span class="m-sub">Human audit / machine generation ratio</span>
          </div>
          <div class="metric-block">
            <span class="m-label">Wedge Velocity (v_wedge)</span>
            <span class="m-val text-warning">+{precursorSummary.stream_3_verification_wedge.velocity_per_month.toFixed(1)} s/mo</span>
            <span class="m-sub">Rate of oversight deficit expansion</span>
          </div>
          <div class="metric-block">
            <span class="m-label">Wedge Acceleration (a_wedge)</span>
            <span class="m-val text-warning">+{precursorSummary.stream_3_verification_wedge.acceleration_per_month2.toFixed(3)} s/mo²</span>
            <span class="m-sub">Kinematic second derivative</span>
          </div>
        </div>
      </div>

      <!-- Triad Architecture Grid -->
      <div class="triad-grid">
        <!-- Stream 1 Card -->
        <div class="stream-card">
          <div class="stream-card-header">
            <span class="stream-id">PRECURSOR STREAM 1</span>
            <h4>Autonomy Seismometer</h4>
          </div>
          <div class="stream-score-row">
            <span class="stream-score">{precursorSummary.stream_1_autonomy_seismometer.score.toFixed(2)}</span>
            <span class="stream-score-max">/ 10.0</span>
            <span class="stream-alert-tag text-danger">{precursorSummary.stream_1_autonomy_seismometer.alert}</span>
          </div>
          <div class="stream-bar-wrap">
            <div class="stream-bar-fill" style="width: {precursorSummary.stream_1_autonomy_seismometer.score * 10}%; background: #ef4444;"></div>
          </div>
          <div class="stream-stats">
            <div class="stat-row">
              <span>Human Paper Trail Gap:</span>
              <strong>{(precursorSummary.stream_1_autonomy_seismometer.hptg * 100).toFixed(1)}%</strong>
            </div>
            <div class="stat-row">
              <span>M2M Economic Share Proxy:</span>
              <strong>{(precursorSummary.stream_1_autonomy_seismometer.m2m_share * 100).toFixed(1)}%</strong>
            </div>
          </div>
          <p class="stream-desc">
            Measures the percentage of frontier capability milestones released with opaque reasoning tokens
            and automated agent-to-agent transaction volume.
          </p>
        </div>

        <!-- Stream 2 Card -->
        <div class="stream-card">
          <div class="stream-card-header">
            <span class="stream-id">PRECURSOR STREAM 2</span>
            <h4>Latent Drift Detector</h4>
          </div>
          <div class="stream-score-row">
            <span class="stream-score">{precursorSummary.stream_2_latent_drift_detector.score.toFixed(2)}</span>
            <span class="stream-score-max">/ 10.0</span>
            <span class="stream-alert-tag text-warning">{precursorSummary.stream_2_latent_drift_detector.alert}</span>
          </div>
          <div class="stream-bar-wrap">
            <div class="stream-bar-fill" style="width: {precursorSummary.stream_2_latent_drift_detector.score * 10}%; background: #f59e0b;"></div>
          </div>
          <div class="stream-stats">
            <div class="stat-row">
              <span>Human Parseability Index:</span>
              <strong>{(precursorSummary.stream_2_latent_drift_detector.human_parseability * 100).toFixed(1)}%</strong>
            </div>
            <div class="stat-row">
              <span>Steganography Confidence:</span>
              <strong>{(precursorSummary.stream_2_latent_drift_detector.stego_confidence * 100).toFixed(1)}%</strong>
            </div>
          </div>
          <p class="stream-desc">
            Watches multi-agent dialogue for sudden drops in human-parseable tokens, compressed idiomatic dialects,
            and steganographic covert coordination channels.
          </p>
        </div>

        <!-- Stream 3 Card -->
        <div class="stream-card">
          <div class="stream-card-header">
            <span class="stream-id">PRECURSOR STREAM 3</span>
            <h4>Verification Accelerometer</h4>
          </div>
          <div class="stream-score-row">
            <span class="stream-score">{precursorSummary.stream_3_verification_wedge.score.toFixed(1)}</span>
            <span class="stream-score-max">/ 10.0</span>
            <span class="stream-alert-tag text-danger">{precursorSummary.stream_3_verification_wedge.cors_label}</span>
          </div>
          <div class="stream-bar-wrap">
            <div class="stream-bar-fill" style="width: {precursorSummary.stream_3_verification_wedge.score * 10}%; background: #ef4444;"></div>
          </div>
          <div class="stream-stats">
            <div class="stat-row">
              <span>Wedge Velocity:</span>
              <strong>+{precursorSummary.stream_3_verification_wedge.velocity_per_month.toFixed(1)} s/mo</strong>
            </div>
            <div class="stat-row">
              <span>Verification Deficit:</span>
              <strong>{precursorSummary.stream_3_verification_wedge.delta_t_seconds.toLocaleString()}s</strong>
            </div>
          </div>
          <p class="stream-desc">
            Tracks the physical and cognitive gap between machine generation speed and expert human audit bandwidth
            across 6 frontier model generations.
          </p>
        </div>
      </div>
    </div>
  {/if}

  <!-- TAB 2: 14 OBSERVABLE ASI PRECURSORS TRIPWIRE BOARD -->
  {#if activeTab === 'tripwires'}
    <div class="tab-content tripwires-view">
      <!-- Filter Bar -->
      <div class="tripwire-controls">
        <div class="search-box">
          <input
            type="text"
            placeholder="Search precursors by ID, keyword, or threshold..."
            bind:value={tripwireSearch}
            class="styled-input"
          />
        </div>

        <div class="filter-pills">
          <span class="filter-label">Status:</span>
          <button class="pill" class:active={tripwireStatusFilter === 'all'} on:click={() => tripwireStatusFilter = 'all'}>All ({asiPrecursors.length})</button>
          <button class="pill pill-red" class:active={tripwireStatusFilter === 'red'} on:click={() => tripwireStatusFilter = 'red'}>Active ({countRed})</button>
          <button class="pill pill-amber" class:active={tripwireStatusFilter === 'amber'} on:click={() => tripwireStatusFilter = 'amber'}>Triggering ({countAmber})</button>
          <button class="pill pill-green" class:active={tripwireStatusFilter === 'green'} on:click={() => tripwireStatusFilter = 'green'}>Latent ({countGreen})</button>
        </div>

        <div class="filter-pills">
          <span class="filter-label">Indicator:</span>
          <button class="pill" class:active={tripwireTypeFilter === 'all'} on:click={() => tripwireTypeFilter = 'all'}>All</button>
          <button class="pill" class:active={tripwireTypeFilter === 'leading'} on:click={() => tripwireTypeFilter = 'leading'}>Leading</button>
          <button class="pill" class:active={tripwireTypeFilter === 'coincident'} on:click={() => tripwireTypeFilter = 'coincident'}>Coincident</button>
          <button class="pill" class:active={tripwireTypeFilter === 'lagging'} on:click={() => tripwireTypeFilter = 'lagging'}>Lagging</button>
        </div>
      </div>

      <!-- Main Tripwire Layout: Grid + Selected Detail Drawer -->
      <div class="tripwire-split">
        <!-- Cards List -->
        <div class="tripwires-list">
          {#each filteredPrecursors as prec}
            <div
              class="tripwire-card"
              class:selected={selectedPrecursorId === prec.id}
              class:status-red={prec.status_color === 'red'}
              class:status-amber={prec.status_color === 'amber'}
              class:status-green={prec.status_color === 'green'}
              on:click={() => selectedPrecursorId = prec.id}
            >
              <div class="tw-top">
                <span class="tw-id">{prec.id}</span>
                <span class="tw-status-tag {prec.status_color}">{prec.status}</span>
              </div>
              <p class="tw-desc">{prec.description}</p>
              <div class="tw-footer">
                <span class="tw-type-tag">{prec.indicator_type.toUpperCase()} INDICATOR</span>
                <span class="tw-verifiable">Verifiable: {prec.outsider_verifiable}</span>
              </div>
            </div>
          {/each}
        </div>

        <!-- Detail Drawer -->
        <div class="tripwire-drawer">
          <div class="drawer-header">
            <span class="drawer-id">{selectedPrecursor.id}</span>
            <span class="tw-status-tag {selectedPrecursor.status_color}">{selectedPrecursor.status}</span>
          </div>

          <h4 class="drawer-title">{selectedPrecursor.description}</h4>

          <div class="drawer-meta-grid">
            <div class="d-meta-item">
              <span class="dm-label">Indicator Type</span>
              <strong class="dm-val">{selectedPrecursor.indicator_type.toUpperCase()}</strong>
            </div>
            <div class="d-meta-item">
              <span class="dm-label">Already Observable</span>
              <strong class="dm-val">{selectedPrecursor.already_observable.toUpperCase()}</strong>
            </div>
            <div class="d-meta-item">
              <span class="dm-label">Data Holder</span>
              <strong class="dm-val">{selectedPrecursor.data_holder}</strong>
            </div>
            <div class="d-meta-item">
              <span class="dm-label">Gaming Risk</span>
              <strong class="dm-val">{selectedPrecursor.gaming_risk}</strong>
            </div>
          </div>

          <div class="drawer-section">
            <span class="sec-label">PROPOSED LITERATURE THRESHOLD</span>
            <p class="sec-text highlight-box">{selectedPrecursor.proposed_threshold}</p>
          </div>

          <div class="drawer-section">
            <span class="sec-label">MEASUREMENT METHODOLOGY</span>
            <p class="sec-text">{selectedPrecursor.measurement_method}</p>
          </div>

          <div class="drawer-section">
            <span class="sec-label">EMPIRICAL BASELINE & TIMESERIES</span>
            <p class="sec-text">{selectedPrecursor.baseline_or_time_series}</p>
          </div>

          <div class="drawer-section">
            <span class="sec-label">HSRI RESEARCH NOTES</span>
            <p class="sec-text">{selectedPrecursor.notes}</p>
          </div>
        </div>
      </div>
    </div>
  {/if}

  <!-- TAB 3: DUAL-LAYER SOVEREIGNTY LEADERBOARD -->
  {#if activeTab === 'dual_layer'}
    <div class="tab-content dual-layer-view">
      <div class="dual-layer-intro">
        <div class="intro-left">
          <h3>Dual-Layer Architecture Leaderboard</h3>
          <p>
            Contrast <strong>Layer 1 (Adoption Baseline)</strong> against <strong>Layer 2 (ASI Sovereignty Layer)</strong>.
            Under non-compensatory Leontief Floor aggregation ($\beta = 0.5$), high-compute captive economies experience
            precipitous rank plunges due to Decoupling Half-Life ($T_&#123;\text&#123;half&#125;&#125;$) bottlenecks.
          </p>
        </div>
        <div class="toggle-cluster">
          <button
            class="toggle-btn"
            class:active={leaderboardMode === 'layer1'}
            on:click={() => leaderboardMode = 'layer1'}
          >
            Layer 1: Adoption
          </button>
          <button
            class="toggle-btn"
            class:active={leaderboardMode === 'layer2'}
            on:click={() => leaderboardMode = 'layer2'}
          >
            Layer 2: Sovereignty
          </button>
          <button
            class="toggle-btn"
            class:active={leaderboardMode === 'delta'}
            on:click={() => leaderboardMode = 'delta'}
          >
            Rank Inversion (Δ)
          </button>
        </div>
      </div>

      <!-- Controls Row -->
      <div class="table-controls">
        <input
          type="text"
          placeholder="Filter country name or ISO3..."
          bind:value={countrySearch}
          class="styled-input-sm"
        />
        <label class="trap-filter-toggle">
          <input type="checkbox" bind:checked={filterTrapOnly} />
          <span>Show High-Compute Vulnerability Traps Only</span>
        </label>
      </div>

      <!-- Leaderboard Table -->
      <div class="table-container">
        <table class="leaderboard-table">
          <thead>
            <tr>
              <th>Country</th>
              <th class="text-center">L1 Rank</th>
              <th class="text-center">L2 Rank</th>
              <th class="text-center">Rank Shift</th>
              <th class="text-center">L1 Score</th>
              <th class="text-center">L2 Score</th>
              <th class="text-center">V_ASI (Gap)</th>
              <th class="text-center">T_half</th>
              <th class="text-center">Bottleneck Pillar</th>
              <th class="text-center">Trap Flag</th>
            </tr>
          </thead>
          <tbody>
            {#each sortedEntries as row}
              <tr class:trap-row={row.high_compute_trap}>
                <td class="country-cell">
                  <strong>{countryNames[row.country_iso3] || row.country_iso3}</strong>
                  <span class="iso-code">({row.country_iso3})</span>
                </td>
                <td class="text-center rank-num">#{row.rank_layer1}</td>
                <td class="text-center rank-num highlight-col">#{row.rank_layer2}</td>
                <td class="text-center">
                  {#if row.rank_delta_sovereignty > 0}
                    <span class="rank-badge gain">+{row.rank_delta_sovereignty}</span>
                  {:else if row.rank_delta_sovereignty < 0}
                    <span class="rank-badge plunge">{row.rank_delta_sovereignty}</span>
                  {:else}
                    <span class="rank-badge neutral">0</span>
                  {/if}
                </td>
                <td class="text-center">{row.h_layer1.toFixed(4)}</td>
                <td class="text-center highlight-col">{row.h_layer2.toFixed(4)}</td>
                <td class="text-center font-mono">{row.v_asi.toFixed(4)}</td>
                <td class="text-center font-mono">
                  {row.t_half_hours >= 720 ? `${Math.round(row.t_half_hours / 24)}d` : `${row.t_half_hours}h`}
                </td>
                <td class="text-center bottleneck-cell">{row.layer2_bottleneck}</td>
                <td class="text-center">
                  {#if row.high_compute_trap}
                    <span class="trap-pill">TRAP</span>
                  {:else}
                    <span class="buffer-pill">RESILIENT</span>
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  {/if}

  <!-- TAB 4: CIVILIZATIONAL AIR-GAP DECOUPLING SIMULATOR -->
  {#if activeTab === 'airgap'}
    <div class="tab-content">
      <CivilizationalAirGap />
    </div>
  {/if}
</div>

<style>
  .seismograph-container {
    font-family: inherit;
    color: #f1f5f9;
  }

  /* Hero Status Banner */
  .sentinel-hero-banner {
    background: linear-gradient(135deg, #090d16 0%, #111827 100%);
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
  }

  .sentinel-status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
  }

  .pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #38bdf8;
    box-shadow: 0 0 8px #38bdf8;
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(56, 189, 248, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
  }

  .hero-main-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 2rem;
  }

  @media (max-width: 850px) {
    .hero-main-row {
      flex-direction: column;
      align-items: flex-start;
    }
  }

  .hero-left h2 {
    font-size: 2.25rem;
    font-weight: 900;
    margin: 0 0 0.5rem 0;
    color: #ffffff;
    letter-spacing: -0.02em;
  }

  .hero-lead {
    font-size: 1.05rem;
    color: #94a3b8;
    margin: 0;
    max-width: 650px;
    line-height: 1.5;
  }

  .master-threat-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1.25rem 1.75rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    min-width: 280px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  }

  .threat-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #94a3b8;
    letter-spacing: 0.05em;
  }

  .threat-score-row {
    display: flex;
    align-items: baseline;
    gap: 0.25rem;
    margin: 0.25rem 0;
  }

  .threat-score {
    font-size: 2.5rem;
    font-weight: 900;
    color: #ef4444;
  }

  .threat-max {
    font-size: 1.2rem;
    color: #64748b;
    font-weight: 600;
  }

  .threat-regime {
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    color: #f87171;
    background: rgba(239, 68, 68, 0.15);
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    text-transform: uppercase;
  }

  /* Sub-Navigation Tabs */
  .tab-navigation {
    display: flex;
    gap: 0.5rem;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 2rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }

  .tab-btn {
    background: transparent;
    border: none;
    color: #94a3b8;
    font-size: 0.95rem;
    font-weight: 600;
    padding: 0.75rem 1.25rem;
    border-radius: 6px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    white-space: nowrap;
    transition: all 0.15s;
  }

  .tab-btn:hover {
    color: #f8fafc;
    background: #1e293b;
  }

  .tab-btn.active {
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
    border-bottom: 2px solid #38bdf8;
    border-radius: 6px 6px 0 0;
  }

  .tab-counter.red {
    font-size: 0.7rem;
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
    padding: 0.1rem 0.4rem;
    border-radius: 9999px;
  }

  /* TAB 1: RADAR */
  .cors-gauge-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
  }

  .cors-gauge-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .gauge-tag {
    font-size: 0.75rem;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
  }

  .cors-gauge-header h3 {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0;
    color: #ffffff;
  }

  .cors-score-badge {
    display: flex;
    align-items: baseline;
    gap: 0.2rem;
    background: #1e293b;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: 1px solid #334155;
  }

  .cors-number {
    font-size: 2.25rem;
    font-weight: 900;
    color: #ef4444;
  }

  .cors-unit {
    font-size: 1.1rem;
    color: #64748b;
  }

  .cors-regime-banner {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1.25rem 0 1.75rem 0;
  }

  @media (max-width: 768px) {
    .cors-regime-banner {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.25rem;
    }
  }

  .regime-name {
    font-weight: 800;
    color: #f87171;
    text-transform: uppercase;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
  }

  .regime-desc {
    font-size: 0.85rem;
    color: #cbd5e1;
  }

  .cors-metrics-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
  }

  @media (max-width: 900px) {
    .cors-metrics-strip {
      grid-template-columns: 1fr 1fr;
    }
  }

  .metric-block {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .m-label {
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 600;
  }

  .m-val {
    font-size: 1.5rem;
    font-weight: 800;
  }

  .m-sub {
    font-size: 0.75rem;
    color: #64748b;
  }

  .text-accent { color: #38bdf8; }
  .text-danger { color: #ef4444; }
  .text-warning { color: #f59e0b; }

  /* Triad Grid */
  .triad-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  @media (max-width: 900px) {
    .triad-grid {
      grid-template-columns: 1fr;
    }
  }

  .stream-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .stream-id {
    font-size: 0.7rem;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.05em;
  }

  .stream-card-header h4 {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0.2rem 0 0 0;
  }

  .stream-score-row {
    display: flex;
    align-items: baseline;
    gap: 0.25rem;
  }

  .stream-score {
    font-size: 1.8rem;
    font-weight: 800;
    color: #f8fafc;
  }

  .stream-score-max {
    font-size: 0.95rem;
    color: #64748b;
  }

  .stream-alert-tag {
    margin-left: auto;
    font-size: 0.7rem;
    font-weight: 800;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.05);
  }

  .stream-bar-wrap {
    height: 6px;
    background: #1e293b;
    border-radius: 3px;
    overflow: hidden;
  }

  .stream-bar-fill {
    height: 100%;
  }

  .stream-stats {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    background: #1e293b;
    border-radius: 6px;
    padding: 0.75rem;
    font-size: 0.8rem;
  }

  .stat-row {
    display: flex;
    justify-content: space-between;
    color: #94a3b8;
  }

  .stat-row strong {
    color: #f8fafc;
  }

  .stream-desc {
    font-size: 0.8rem;
    color: #94a3b8;
    line-height: 1.4;
    margin: 0;
  }

  /* TAB 2: TRIPWIRES */
  .tripwire-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
  }

  .search-box {
    flex: 1;
    min-width: 250px;
  }

  .styled-input {
    width: 100%;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #f8fafc;
    padding: 0.6rem 0.8rem;
    font-size: 0.875rem;
    outline: none;
  }

  .styled-input:focus {
    border-color: #38bdf8;
  }

  .filter-pills {
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }

  .filter-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
  }

  .pill {
    background: #1e293b;
    border: 1px solid #334155;
    color: #94a3b8;
    font-size: 0.75rem;
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    cursor: pointer;
    transition: all 0.15s;
  }

  .pill:hover {
    color: #ffffff;
    border-color: #475569;
  }

  .pill.active {
    background: #38bdf8;
    color: #0f172a;
    font-weight: 700;
    border-color: #38bdf8;
  }

  .pill-red.active { background: #ef4444; border-color: #ef4444; color: #ffffff; }
  .pill-amber.active { background: #f59e0b; border-color: #f59e0b; color: #0f172a; }
  .pill-green.active { background: #10b981; border-color: #10b981; color: #0f172a; }

  .tripwire-split {
    display: grid;
    grid-template-columns: 1fr 1.1fr;
    gap: 1.5rem;
  }

  @media (max-width: 900px) {
    .tripwire-split {
      grid-template-columns: 1fr;
    }
  }

  .tripwires-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: 750px;
    overflow-y: auto;
    padding-right: 0.5rem;
  }

  .tripwire-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 1rem;
    cursor: pointer;
    transition: all 0.15s;
  }

  .tripwire-card:hover {
    border-color: #475569;
    transform: translateY(-1px);
  }

  .tripwire-card.selected {
    border-color: #38bdf8;
    background: rgba(56, 189, 248, 0.05);
  }

  .tw-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
  }

  .tw-id {
    font-size: 0.8rem;
    font-weight: 800;
    color: #38bdf8;
  }

  .tw-status-tag {
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    text-transform: uppercase;
  }

  .tw-status-tag.red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
  .tw-status-tag.amber { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
  .tw-status-tag.green { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }

  .tw-desc {
    font-size: 0.85rem;
    color: #cbd5e1;
    margin: 0 0 0.5rem 0;
    line-height: 1.4;
  }

  .tw-footer {
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: #64748b;
  }

  .tw-type-tag {
    font-weight: 700;
    color: #94a3b8;
  }

  /* Detail Drawer */
  .tripwire-drawer {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    position: sticky;
    top: 2rem;
    height: fit-content;
  }

  .drawer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .drawer-id {
    font-size: 1.1rem;
    font-weight: 900;
    color: #38bdf8;
  }

  .drawer-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    line-height: 1.4;
  }

  .drawer-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    background: #1e293b;
    border-radius: 6px;
    padding: 0.75rem;
  }

  .d-meta-item {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }

  .dm-label {
    font-size: 0.65rem;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 600;
  }

  .dm-val {
    font-size: 0.8rem;
    color: #f8fafc;
  }

  .drawer-section {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .sec-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .sec-text {
    font-size: 0.85rem;
    color: #94a3b8;
    line-height: 1.45;
    margin: 0;
  }

  .highlight-box {
    background: #1e293b;
    border-left: 3px solid #38bdf8;
    padding: 0.5rem 0.75rem;
    border-radius: 0 4px 4px 0;
    color: #f1f5f9;
  }

  /* TAB 3: DUAL-LAYER LEADERBOARD */
  .dual-layer-intro {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 2rem;
    margin-bottom: 1.5rem;
  }

  @media (max-width: 850px) {
    .dual-layer-intro {
      flex-direction: column;
      align-items: flex-start;
    }
  }

  .intro-left h3 {
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.5rem 0;
  }

  .intro-left p {
    font-size: 0.9rem;
    color: #94a3b8;
    margin: 0;
    max-width: 700px;
    line-height: 1.5;
  }

  .toggle-cluster {
    display: flex;
    background: #1e293b;
    border-radius: 6px;
    padding: 0.25rem;
  }

  .toggle-btn {
    background: transparent;
    border: none;
    color: #94a3b8;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.5rem 0.9rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.15s;
    white-space: nowrap;
  }

  .toggle-btn.active {
    background: #38bdf8;
    color: #0f172a;
  }

  .table-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .styled-input-sm {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #f8fafc;
    padding: 0.4rem 0.75rem;
    font-size: 0.85rem;
    outline: none;
    min-width: 250px;
  }

  .trap-filter-toggle {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #f87171;
    cursor: pointer;
    font-weight: 600;
  }

  .table-container {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    overflow-x: auto;
  }

  .leaderboard-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    text-align: left;
  }

  .leaderboard-table th {
    background: #111827;
    color: #94a3b8;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #1e293b;
    font-weight: 700;
  }

  .leaderboard-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #1e293b;
    color: #cbd5e1;
  }

  .leaderboard-table tr:hover {
    background: rgba(30, 41, 59, 0.5);
  }

  .leaderboard-table tr.trap-row {
    background: rgba(239, 68, 68, 0.03);
  }

  .country-cell {
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
  }

  .country-cell strong {
    color: #f8fafc;
  }

  .iso-code {
    font-size: 0.75rem;
    color: #64748b;
  }

  .rank-num {
    font-weight: 700;
    color: #94a3b8;
  }

  .highlight-col {
    color: #38bdf8 !important;
    font-weight: 800;
  }

  .rank-badge {
    display: inline-block;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
  }

  .rank-badge.gain {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
  }

  .rank-badge.plunge {
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
    font-weight: 800;
  }

  .rank-badge.neutral {
    background: #1e293b;
    color: #64748b;
  }

  .font-mono {
    font-family: monospace;
    font-size: 0.8rem;
  }

  .bottleneck-cell {
    font-size: 0.75rem;
    color: #94a3b8;
  }

  .trap-pill {
    font-size: 0.65rem;
    font-weight: 800;
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
  }

  .buffer-pill {
    font-size: 0.65rem;
    font-weight: 700;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
  }

  .text-center { text-align: center; }
</style>
