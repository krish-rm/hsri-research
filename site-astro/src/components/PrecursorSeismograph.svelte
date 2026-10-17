<script lang="ts">
  import precursorSummary from '../data/precursor_summary.json';
  import wedgeHistory from '../data/wedge_history.json';
  import asiPrecursors from '../data/asi_precursors.json';
  import layer2Data from '../data/hsri_layer2.json';
  import CivilizationalAirGap from './CivilizationalAirGap.svelte';
  import TelemetryUptimeBadge from './TelemetryUptimeBadge.svelte';
  import SeismographKineticDrum from './SeismographKineticDrum.svelte';
  import VerificationHorizonChart from './VerificationHorizonChart.svelte';

  const base = (import.meta.env.BASE_URL || '').replace(/\/$/, '');

  // Navigation tab state (Disciplined 2-core tabs + 1 dedicated stress-test tool)
  let activeTab: 'radar' | 'tripwires' | 'airgap' = 'radar';

  // Evidence drawer state for Stream 1, 2, 3
  let openDrawer: 'stream1' | 'stream2' | 'stream3' | null = null;

  function toggleDrawer(stream: 'stream1' | 'stream2' | 'stream3') {
    openDrawer = openDrawer === stream ? null : stream;
  }

  // Filter states for 14 Tripwires
  let tripwireStatusFilter: 'all' | 'red' | 'amber' | 'green' = 'all';
  let tripwireTypeFilter: 'all' | 'leading' | 'coincident' | 'lagging' = 'all';
  let tripwireStreamFilter: 'all' | 'stream1' | 'stream2' | 'stream3' = 'all';
  let tripwireSearch = '';
  let selectedPrecursorId: string | null = 'PREC-011';

  // Mapping precursors to governing telemetry streams
  function getGoverningStream(id: string): { stream: string; label: string; color: string } {
    const num = parseInt(id.replace('PREC-', ''), 10);
    if ([1, 2, 5, 7].includes(num)) {
      return { stream: 'stream1', label: 'Stream 1: Autonomy', color: '#ef4444' };
    }
    if ([3, 4, 8, 9].includes(num)) {
      return { stream: 'stream2', label: 'Stream 2: Language Drift', color: '#f59e0b' };
    }
    return { stream: 'stream3', label: 'Stream 3: Verification Wedge', color: '#38bdf8' };
  }

  // Filtered Precursors
  $: filteredPrecursors = asiPrecursors.filter(p => {
    const matchStatus = tripwireStatusFilter === 'all' || p.status_color === tripwireStatusFilter;
    const matchType = tripwireTypeFilter === 'all' || p.indicator_type === tripwireTypeFilter;
    const streamInfo = getGoverningStream(p.id);
    const matchStream = tripwireStreamFilter === 'all' || streamInfo.stream === tripwireStreamFilter;
    const matchSearch = tripwireSearch === '' ||
      p.id.toLowerCase().includes(tripwireSearch.toLowerCase()) ||
      p.description.toLowerCase().includes(tripwireSearch.toLowerCase()) ||
      p.proposed_threshold.toLowerCase().includes(tripwireSearch.toLowerCase());
    return matchStatus && matchType && matchStream && matchSearch;
  });

  $: selectedPrecursor = asiPrecursors.find(p => p.id === selectedPrecursorId) || asiPrecursors[0];

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
      <span>LIVE SENTINEL TELEMETRY ACTIVE · HSRI RESEARCH CONSORTIUM</span>
    </div>
    <div class="hero-main-row">
      <div class="hero-left">
        <h2>The ASI Precursor Seismograph</h2>
        <p class="hero-lead">
          Continuous global telemetry tracking the biological collapse of human oversight.
          Detecting the micro-fractures in human supervision before Artificial Superintelligence breaks containment.
        </p>
      </div>
      <div class="hero-right">
        <div class="master-threat-card">
          <span class="threat-title">Master Precursor Threat Level</span>
          <div class="threat-score-row">
            <span class="threat-score">{precursorSummary.master_precursor_threat_score.toFixed(2)}</span>
            <span class="threat-max">/ 10.0</span>
          </div>
          <span class="threat-regime">Level 5 of 5: Critical Supervisory Collapse</span>
          <div class="regime-scale-bar">
            <span class="dot filled" title="Level 1: Nominal"></span>
            <span class="dot filled" title="Level 2: Elevated"></span>
            <span class="dot filled" title="Level 3: High"></span>
            <span class="dot filled" title="Level 4: Severe"></span>
            <span class="dot filled red" title="Level 5: Critical Collapse"></span>
            <span class="scale-label">No Human Can Keep Up in Real Time</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <TelemetryUptimeBadge />

  <!-- Primary Sub-navigation Tabs (2 Primary Tabs + 1 Decoupling Stress-Test) -->
  <div class="tab-navigation" role="tablist">
    <button
      class="tab-btn"
      class:active={activeTab === 'radar'}
      on:click={() => activeTab = 'radar'}
      role="tab"
      aria-selected={activeTab === 'radar'}
    >
      <span class="tab-icon">⚡</span>
      <span>Planetary Telemetry &amp; Seismogram</span>
    </button>
    <button
      class="tab-btn"
      class:active={activeTab === 'tripwires'}
      on:click={() => activeTab = 'tripwires'}
      role="tab"
      aria-selected={activeTab === 'tripwires'}
    >
      <span class="tab-icon">🚨</span>
      <span>14 Observable Precursor Tripwires</span>
      <span class="tab-counter red">{countRed} Active</span>
    </button>
    <button
      class="tab-btn"
      class:active={activeTab === 'airgap'}
      on:click={() => activeTab = 'airgap'}
      role="tab"
      aria-selected={activeTab === 'airgap'}
    >
      <span class="tab-icon">🛡️</span>
      <span>Air-Gap Decoupling Stress Test</span>
    </button>
  </div>

  <!-- TAB 1: RADAR & TRIAD TELEMETRY -->
  {#if activeTab === 'radar'}
    <div class="tab-content radar-view">
      <!-- HERO AUDIT DEFICIT CLOCK -->
      <div class="audit-deficit-hero">
        <div class="deficit-top-row">
          <div class="deficit-badge">
            <span class="db-title">THE 80-MINUTE SUPERVISORY DEFICIT</span>
            <h3 class="db-hero-text">
              Humans are <span class="highlight-danger">3,200× Too Slow</span> to Stop Autonomous AI Actions
            </h3>
            <p class="db-desc">
              In 1.5 seconds, a frontier AI system generates complex software or financial moves that take a human security expert 80 minutes (4,798 seconds) to verify.
              Because machines produce 3,200× faster than humans can read, "Human-in-the-Loop" supervision is a physical impossibility.
            </p>
          </div>
          <div class="deficit-metrics-cluster">
            <div class="dm-card">
              <span class="dm-label">Current Audit Debt</span>
              <span class="dm-num text-danger">80.0 min</span>
              <span class="dm-sub">4,798.5s deficit per task</span>
            </div>
            <div class="dm-card">
              <span class="dm-label">Speed Deficit Ratio</span>
              <span class="dm-num text-danger">3,200×</span>
              <span class="dm-sub">Audit time ÷ machine time</span>
            </div>
            <div class="dm-card">
              <span class="dm-label">Debt Expansion Rate</span>
              <span class="dm-num text-warning">+2.6 min/mo</span>
              <span class="dm-sub">+156.4s/month, accelerating</span>
            </div>
          </div>
        </div>
      </div>

      <!-- KINETIC SEISMOGRAM DRUM -->
      <div class="drum-wrapper-card">
        <SeismographKineticDrum
          score={precursorSummary.master_precursor_threat_score}
          stream1Score={precursorSummary.stream_1_autonomy_seismometer.score}
          stream2Score={precursorSummary.stream_2_latent_drift_detector.score}
          stream3Score={precursorSummary.stream_3_verification_wedge.score}
        />
      </div>

      <!-- THE THREE GROUNDED SIRENS (Triad Telemetry Deconstructed) -->
      <div class="triad-grid">
        <!-- Stream 1 Card -->
        <div class="stream-card">
          <div class="stream-card-header">
            <span class="stream-id">STREAM 1 · UNASSISTED EXECUTION</span>
            <h4>Machine Autonomy Seismometer</h4>
          </div>
          <div class="stream-score-row">
            <span class="stream-score">{precursorSummary.stream_1_autonomy_seismometer.score.toFixed(2)}</span>
            <span class="stream-score-max">/ 10.0</span>
            <span class="stream-alert-tag text-danger">Critical Supervisory Deficit</span>
          </div>
          <div class="stream-bar-wrap">
            <div class="stream-bar-fill" style="width: {precursorSummary.stream_1_autonomy_seismometer.score * 10}%; background: #ef4444;"></div>
          </div>
          <div class="stream-stats">
            <div class="stat-row">
              <span>Black Box Reasoning Rate:</span>
              <strong class="text-danger">{(precursorSummary.stream_1_autonomy_seismometer.hptg * 100).toFixed(1)}%</strong>
            </div>
            <div class="stat-row">
              <span>Machine-to-Machine Share:</span>
              <strong class="text-warning">{(precursorSummary.stream_1_autonomy_seismometer.m2m_share * 100).toFixed(1)}%</strong>
            </div>
          </div>
          <p class="stream-desc">
            <strong>What this means:</strong> Over 75% of frontier AI reasoning occurs in opaque internal tokens humans cannot read. 64% of agent transactions now execute directly between machines without human review.
          </p>

          <div class="stream-tripwire-tags">
            <span class="tag-label">Dependent Tripwires:</span>
            <button type="button" class="tag-chip" on:click={() => { activeTab = 'tripwires'; tripwireStreamFilter = 'stream1'; }}>PREC-001 (R&amp;D)</button>
            <button type="button" class="tag-chip" on:click={() => { activeTab = 'tripwires'; tripwireStreamFilter = 'stream1'; }}>PREC-002 (Replication)</button>
            <button type="button" class="tag-chip" on:click={() => { activeTab = 'tripwires'; tripwireStreamFilter = 'stream1'; }}>PREC-005 (M2M)</button>
          </div>

          <button type="button" class="evidence-toggle-btn" on:click={() => toggleDrawer('stream1')}>
            {openDrawer === 'stream1' ? 'Hide Evidence & Scrape Receipts ▲' : 'Inspect Evidence & Scrape Receipts ▼'}
          </button>

          {#if openDrawer === 'stream1'}
            <div class="drawer-content">
              <div class="drawer-row">
                <span class="d-k">Primary Telemetry Feed:</span>
                <span class="d-v">SWE-bench Verified &amp; METR Autonomy Evaluations</span>
              </div>
              <div class="drawer-row">
                <span class="d-k">Scrape Status:</span>
                <span class="d-v text-success">Verified Active · 100% harmonized</span>
              </div>
              <div class="drawer-row">
                <span class="d-k">Model Evidence:</span>
                <span class="d-v">OpenAI o1/o3 hidden CoT tokens, Docker swarm API logs</span>
              </div>
              <div class="drawer-row">
                <span class="d-k">Mathematical Construct:</span>
                <span class="d-v font-mono">HPTG = 1.0 - (Tokens_auditable / Tokens_total) = 75.57%</span>
              </div>
            </div>
          {/if}
        </div>

        <!-- Stream 2 Card -->
        <div class="stream-card">
          <div class="stream-card-header">
            <span class="stream-id">STREAM 2 · PROTOCOL DRIFT</span>
            <h4>Latent Language Drift Detector</h4>
          </div>
          <div class="stream-score-row">
            <span class="stream-score">{precursorSummary.stream_2_latent_drift_detector.score.toFixed(2)}</span>
            <span class="stream-score-max">/ 10.0</span>
            <span class="stream-alert-tag text-warning">High Dialect Compression</span>
          </div>
          <div class="stream-bar-wrap">
            <div class="stream-bar-fill" style="width: {precursorSummary.stream_2_latent_drift_detector.score * 10}%; background: #f59e0b;"></div>
          </div>
          <div class="stream-stats">
            <div class="stat-row">
              <span>Readable to Humans:</span>
              <strong class="text-warning">{(precursorSummary.stream_2_latent_drift_detector.human_parseability * 100).toFixed(1)}%</strong>
            </div>
            <div class="stat-row">
              <span>Covert Channel Risk:</span>
              <strong class="text-danger">{(precursorSummary.stream_2_latent_drift_detector.stego_confidence * 100).toFixed(1)}%</strong>
            </div>
          </div>
          <p class="stream-desc">
            <strong>What this means:</strong> When AI agents coordinate in swarms, they develop compressed shorthand dialects. Nearly 70% of inter-agent tokens are now unreadable to human supervisors in real time.
          </p>

          <div class="stream-tripwire-tags">
            <span class="tag-label">Dependent Tripwires:</span>
            <button type="button" class="tag-chip" on:click={() => { activeTab = 'tripwires'; tripwireStreamFilter = 'stream2'; }}>PREC-003 (Stego)</button>
            <button type="button" class="tag-chip" on:click={() => { activeTab = 'tripwires'; tripwireStreamFilter = 'stream2'; }}>PREC-004 (Compression)</button>
            <button type="button" class="tag-chip" on:click={() => { activeTab = 'tripwires'; tripwireStreamFilter = 'stream2'; }}>PREC-009 (Swarm)</button>
          </div>

          <button type="button" class="evidence-toggle-btn" on:click={() => toggleDrawer('stream2')}>
            {openDrawer === 'stream2' ? 'Hide Evidence & Scrape Receipts ▲' : 'Inspect Evidence & Scrape Receipts ▼'}
          </button>

          {#if openDrawer === 'stream2'}
            <div class="drawer-content">
              <div class="drawer-row">
                <span class="d-k">Empirical Protocol:</span>
                <span class="d-v">Multi-Agent Steganographic Protocol Scan (EXP-08-SYN)</span>
              </div>
              <div class="drawer-row">
                <span class="d-k">Token Compression Ratio:</span>
                <span class="d-v font-mono">HPI = 0.3060 (69.4% unreadable machine shorthand)</span>
              </div>
              <div class="drawer-row">
                <span class="d-k">Covert Channel Retention:</span>
                <span class="d-v text-danger">98.0% steganographic decoding confidence</span>
              </div>
              <div class="drawer-row">
                <span class="d-k">Risk Meaning:</span>
                <span class="d-v">Swarms can exchange instructions without trigger detection</span>
              </div>
            </div>
          {/if}
        </div>

        <!-- Stream 3 Card -->
        <div class="stream-card">
          <div class="stream-card-header">
            <span class="stream-id">STREAM 3 · OVERSIGHT HORIZON</span>
            <h4>Verification Accelerometer</h4>
          </div>
          <div class="stream-score-row">
            <span class="stream-score">{precursorSummary.stream_3_verification_wedge.score.toFixed(1)}</span>
            <span class="stream-score-max">/ 10.0</span>
            <span class="stream-alert-tag text-danger">Point of No Return (CORS 10.0)</span>
          </div>
          <div class="stream-bar-wrap">
            <div class="stream-bar-fill" style="width: {precursorSummary.stream_3_verification_wedge.score * 10}%; background: #ef4444;"></div>
          </div>
          <div class="stream-stats">
            <div class="stat-row">
              <span>Audit Deficit (ΔT):</span>
              <strong class="text-danger">{precursorSummary.stream_3_verification_wedge.delta_t_seconds.toLocaleString()}s (80m)</strong>
            </div>
            <div class="stat-row">
              <span>Deficit Acceleration:</span>
              <strong class="text-warning">+{precursorSummary.stream_3_verification_wedge.acceleration_per_month2.toFixed(3)} s/mo²</strong>
            </div>
          </div>
          <p class="stream-desc">
            <strong>What this means:</strong> The gap between machine speed and human audit capacity is widening by 2.6 minutes every month, and the rate of expansion is accelerating. Real-time human oversight has permanently ended.
          </p>

          <div class="stream-tripwire-tags">
            <span class="tag-label">Dependent Tripwires:</span>
            <button type="button" class="tag-chip" on:click={() => { activeTab = 'tripwires'; tripwireStreamFilter = 'stream3'; }}>PREC-010 (Speed)</button>
            <button type="button" class="tag-chip" on:click={() => { activeTab = 'tripwires'; tripwireStreamFilter = 'stream3'; }}>PREC-011 (Crossing)</button>
            <button type="button" class="tag-chip" on:click={() => { activeTab = 'tripwires'; tripwireStreamFilter = 'stream3'; }}>PREC-014 (Recursive)</button>
          </div>

          <button type="button" class="evidence-toggle-btn" on:click={() => toggleDrawer('stream3')}>
            {openDrawer === 'stream3' ? 'Hide Formal Proof & Math ▲' : 'Inspect Formal Proof & Math ▼'}
          </button>

          {#if openDrawer === 'stream3'}
            <div class="drawer-content">
              <div class="drawer-row">
                <span class="d-k">CORS Formulation:</span>
                <span class="d-v font-mono">CORS = min(10.0, 1.0 + log10(1 + ΔT_wedge / 0.200) * α)</span>
              </div>
              <div class="drawer-row">
                <span class="d-k">Kinematic Velocity:</span>
                <span class="d-v font-mono">v_wedge = d(ΔT)/dt = +156.413 s/month</span>
              </div>
              <div class="drawer-row">
                <span class="d-k">Kinematic Acceleration:</span>
                <span class="d-v font-mono">a_wedge = d²(ΔT)/dt² = +1.991 s/month²</span>
              </div>
              <div class="drawer-row">
                <span class="d-k">DOI Provenance:</span>
                <span class="d-v">HSRI Working Paper §4 · DOI 10.5281/zenodo.23441742</span>
              </div>
            </div>
          {/if}
        </div>
      </div>

      <!-- HISTORICAL VERIFICATION HORIZON CHART (2022-2026) -->
      <VerificationHorizonChart />

      <!-- CONTEXTUAL SOVEREIGNTY BRIDGE CARD (Replacing Duplicate Leaderboard) -->
      <div class="sovereignty-bridge-card">
        <div class="bridge-info">
          <span class="bridge-tag">GEOPOLITICAL IMPLICATION</span>
          <h4>How Does Supervisory Collapse Impact Sovereign Survival?</h4>
          <p>
            When autonomous AI models cannot be audited in real-time, high-compute captive nations face catastrophic severance cliffs under zero-notice air-gap severance.
            <strong>Most exposed:</strong> Singapore (−34 ranks, T<sub>half</sub> 8h) and United States (−21 ranks, T<sub>half</sub> 28h).
            <strong>Most resilient:</strong> Norway (Rank #1, T<sub>half</sub> &gt; 720h) and Finland (Rank #2, T<sub>half</sub> &gt; 720h).
          </p>
        </div>
        <div class="bridge-action">
          <a class="bridge-btn" href={`${base}/countries/`}>
            Explore 39-Nation Sovereign Decoupling Observatory →
          </a>
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
          <span class="filter-label">Stream:</span>
          <button class="pill" class:active={tripwireStreamFilter === 'all'} on:click={() => tripwireStreamFilter = 'all'}>All Streams</button>
          <button class="pill" class:active={tripwireStreamFilter === 'stream1'} on:click={() => tripwireStreamFilter = 'stream1'}>Stream 1 (Autonomy)</button>
          <button class="pill" class:active={tripwireStreamFilter === 'stream2'} on:click={() => tripwireStreamFilter = 'stream2'}>Stream 2 (Drift)</button>
          <button class="pill" class:active={tripwireStreamFilter === 'stream3'} on:click={() => tripwireStreamFilter = 'stream3'}>Stream 3 (Wedge)</button>
        </div>

        <div class="filter-pills">
          <span class="filter-label">Indicator:</span>
          <button class="pill" class:active={tripwireTypeFilter === 'all'} on:click={() => tripwireTypeFilter = 'all'}>All Types</button>
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
            {@const streamInfo = getGoverningStream(prec.id)}
            <div
              class="tripwire-card"
              class:selected={selectedPrecursorId === prec.id}
              class:status-red={prec.status_color === 'red'}
              class:status-amber={prec.status_color === 'amber'}
              class:status-green={prec.status_color === 'green'}
              on:click={() => selectedPrecursorId = prec.id}
            >
              <div class="tc-top">
                <span class="tc-id">{prec.id}</span>
                <span class="stream-chip" style="color: {streamInfo.color}; border-color: {streamInfo.color};">
                  {streamInfo.label.split(':')[1].trim()}
                </span>
                <span class="tc-badge {prec.status_color}">{prec.status.replace('_', ' ')}</span>
              </div>
              <p class="tc-desc">{prec.description}</p>
              <div class="tc-footer">
                <span class="tc-type">{prec.indicator_type.toUpperCase()} INDICATOR</span>
                <span class="tc-arrow">Inspect Dossier →</span>
              </div>
            </div>
          {/each}
        </div>

        <!-- Detail Drawer (Selected Precursor) -->
        {#if selectedPrecursor}
          {@const streamInfo = getGoverningStream(selectedPrecursor.id)}
          <div class="tripwire-drawer">
            <div class="drawer-header">
              <div class="dh-top">
                <span class="dh-id">{selectedPrecursor.id}</span>
                <span class="stream-chip" style="color: {streamInfo.color}; border-color: {streamInfo.color};">
                  Governed by {streamInfo.label}
                </span>
                <span class="dh-status {selectedPrecursor.status_color}">{selectedPrecursor.status.replace('_', ' ')}</span>
              </div>
              <h3>{selectedPrecursor.description}</h3>
            </div>

            <div class="drawer-section">
              <span class="d-label">PROPOSED LITERATURE THRESHOLD</span>
              <div class="d-box highlight">
                {selectedPrecursor.proposed_threshold}
              </div>
            </div>

            <div class="drawer-section">
              <span class="d-label">MEASUREMENT METHODOLOGY &amp; BENCHMARK</span>
              <p class="d-text">{selectedPrecursor.measurement_method}</p>
            </div>

            <div class="drawer-section">
              <span class="d-label">OBSERVED BASELINE &amp; TIME SERIES</span>
              <p class="d-text">{selectedPrecursor.baseline_or_time_series}</p>
            </div>

            <div class="drawer-grid">
              <div class="dg-cell">
                <span class="d-label">FALSE POSITIVE RISK</span>
                <p>{selectedPrecursor.false_positive_risk}</p>
              </div>
              <div class="dg-cell">
                <span class="d-label">FALSE NEGATIVE RISK</span>
                <p>{selectedPrecursor.false_negative_risk}</p>
              </div>
              <div class="dg-cell">
                <span class="d-label">GAMING &amp; COGOODHART RISK</span>
                <p>{selectedPrecursor.gaming_risk}</p>
              </div>
              <div class="dg-cell">
                <span class="d-label">OUTSIDER VERIFIABLE?</span>
                <p class="highlight-text">{selectedPrecursor.outsider_verifiable.toUpperCase()}</p>
              </div>
            </div>

            <div class="drawer-footer">
              <span>Primary Data Holder: <strong>{selectedPrecursor.data_holder}</strong></span>
              <span class="notes">{selectedPrecursor.notes}</span>
            </div>
          </div>
        {/if}
      </div>
    </div>
  {/if}

  <!-- TAB 3: CIVILIZATIONAL AIR-GAP DECOUPLING SIMULATOR -->
  {#if activeTab === 'airgap'}
    <div class="tab-content">
      <CivilizationalAirGap />
    </div>
  {/if}
</div>

<style>
  .seismograph-container {
    font-family: inherit;
    padding-bottom: 3rem;
  }

  /* Hero Status Banner */
  .sentinel-hero-banner {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.85) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
  }

  .sentinel-status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.35);
    color: #ef4444;
    padding: 4px 12px;
    border-radius: 9999px;
    font-family: var(--font-family-mono, monospace);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
  }

  .pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #ef4444;
    box-shadow: 0 0 10px #ef4444;
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
  }

  .hero-main-row {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 2rem;
    align-items: center;
  }

  .hero-left h2 {
    font-size: 2.1rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    color: #f8fafc;
    margin: 0 0 0.5rem 0;
  }

  .hero-lead {
    color: #94a3b8;
    font-size: 0.98rem;
    line-height: 1.6;
    margin: 0;
  }

  /* Master Threat Card */
  .master-threat-card {
    background: rgba(6, 9, 17, 0.9);
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    display: flex;
    flex-direction: column;
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.15);
  }

  .threat-title {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.72rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .threat-score-row {
    display: flex;
    align-items: baseline;
    gap: 6px;
    margin: 4px 0;
  }

  .threat-score {
    font-family: var(--font-family-mono, monospace);
    font-size: 2.8rem;
    font-weight: 900;
    color: #ef4444;
    line-height: 1;
  }

  .threat-max {
    font-family: var(--font-family-mono, monospace);
    font-size: 1.2rem;
    color: #64748b;
  }

  .threat-regime {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.82rem;
    font-weight: 800;
    color: #ef4444;
    letter-spacing: 0.03em;
  }

  .regime-scale-bar {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .regime-scale-bar .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
  }

  .regime-scale-bar .dot.filled {
    background: #f59e0b;
  }

  .regime-scale-bar .dot.filled.red {
    background: #ef4444;
    box-shadow: 0 0 6px #ef4444;
  }

  .scale-label {
    font-size: 0.72rem;
    color: #94a3b8;
    margin-left: 4px;
  }

  /* Sub-Navigation Tabs */
  .tab-navigation {
    display: flex;
    gap: 8px;
    margin: 1.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 0.5rem;
    overflow-x: auto;
  }

  .tab-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: transparent;
    border: 1px solid transparent;
    color: #94a3b8;
    padding: 10px 18px;
    border-radius: 10px;
    font-size: 0.92rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
  }

  .tab-btn:hover {
    color: #f8fafc;
    background: rgba(255, 255, 255, 0.05);
  }

  .tab-btn.active {
    background: rgba(30, 41, 59, 0.9);
    border-color: rgba(255, 255, 255, 0.15);
    color: #f8fafc;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  }

  .tab-counter {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.7rem;
    padding: 2px 7px;
    border-radius: 9999px;
  }

  .tab-counter.red {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.35);
  }

  /* AUDIT DEFICIT HERO */
  .audit-deficit-hero {
    background: radial-gradient(800px 300px at 10% 0%, rgba(239, 68, 68, 0.12), transparent 70%),
                linear-gradient(135deg, #090d16 0%, #0f172a 100%);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
  }

  .deficit-top-row {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 24px;
    align-items: center;
  }

  .db-title {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #ef4444;
    display: block;
    margin-bottom: 6px;
  }

  .db-hero-text {
    font-size: 1.45rem;
    font-weight: 900;
    color: #f8fafc;
    margin: 0 0 8px 0;
    line-height: 1.3;
  }

  .highlight-danger {
    color: #ef4444;
    text-decoration: underline;
    text-underline-offset: 4px;
  }

  .db-desc {
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.55;
    margin: 0;
  }

  .deficit-metrics-cluster {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .dm-card {
    background: rgba(6, 9, 17, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 8px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .dm-label {
    font-size: 0.8rem;
    color: #94a3b8;
  }

  .dm-num {
    font-family: var(--font-family-mono, monospace);
    font-weight: 800;
    font-size: 1.1rem;
  }

  .dm-sub {
    font-size: 0.72rem;
    color: #64748b;
  }

  /* Drum Wrapper */
  .drum-wrapper-card {
    margin-bottom: 24px;
  }

  /* Triad Grid */
  .triad-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    margin-bottom: 24px;
  }

  .stream-card {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  }

  .stream-card-header {
    margin-bottom: 0.75rem;
  }

  .stream-id {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.68rem;
    color: #94a3b8;
    letter-spacing: 0.05em;
  }

  .stream-card-header h4 {
    font-size: 1.1rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 2px 0 0 0;
  }

  .stream-score-row {
    display: flex;
    align-items: baseline;
    gap: 6px;
    margin-bottom: 0.5rem;
  }

  .stream-score {
    font-family: var(--font-family-mono, monospace);
    font-size: 2rem;
    font-weight: 900;
    color: #f8fafc;
    line-height: 1;
  }

  .stream-score-max {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.9rem;
    color: #64748b;
  }

  .stream-alert-tag {
    margin-left: auto;
    font-family: var(--font-family-mono, monospace);
    font-size: 0.68rem;
    font-weight: 700;
  }

  .stream-bar-wrap {
    height: 6px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 9999px;
    margin-bottom: 1rem;
    overflow: hidden;
  }

  .stream-bar-fill {
    height: 100%;
    border-radius: 9999px;
  }

  .stream-stats {
    display: flex;
    flex-direction: column;
    gap: 6px;
    background: rgba(6, 9, 17, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 10px;
  }

  .stat-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #94a3b8;
  }

  .stream-desc {
    color: #cbd5e1;
    font-size: 0.85rem;
    line-height: 1.5;
    margin: 0 0 12px 0;
    flex: 1;
  }

  .stream-tripwire-tags {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 12px;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
  }

  .tag-label {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.65rem;
    color: #64748b;
    width: 100%;
  }

  .tag-chip {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.68rem;
    padding: 3px 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .tag-chip:hover {
    color: #f8fafc;
    border-color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
  }

  .evidence-toggle-btn {
    width: 100%;
    padding: 7px 10px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.04);
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: center;
  }

  .evidence-toggle-btn:hover {
    color: #f8fafc;
    background: rgba(255, 255, 255, 0.08);
  }

  .drawer-content {
    margin-top: 10px;
    padding: 10px 12px;
    background: rgba(6, 9, 17, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    animation: drawerIn 0.2s ease-out;
  }

  @keyframes drawerIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .drawer-row {
    display: flex;
    flex-direction: column;
    font-size: 0.75rem;
    gap: 1px;
  }

  .d-k {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.65rem;
    color: #64748b;
  }

  .d-v {
    color: #cbd5e1;
  }

  /* Sovereignty Bridge Card */
  .sovereignty-bridge-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 14px;
    padding: 18px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  }

  .bridge-tag {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #38bdf8;
    display: block;
    margin-bottom: 4px;
  }

  .bridge-info h4 {
    font-size: 1.15rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 0 0 6px 0;
  }

  .bridge-info p {
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.5;
    margin: 0;
    max-width: 760px;
  }

  .bridge-btn {
    display: inline-block;
    padding: 10px 18px;
    border-radius: 10px;
    background: #1d4ed8;
    color: white;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.88rem;
    white-space: nowrap;
    transition: background 0.15s ease;
  }

  .bridge-btn:hover {
    background: #1e40af;
  }

  /* Tripwires Tab Styling */
  .tripwire-controls {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 1.5rem;
    background: rgba(15, 23, 42, 0.6);
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }

  .search-box {
    flex: 1;
    min-width: 240px;
  }

  .styled-input {
    width: 100%;
    padding: 9px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    background: rgba(6, 9, 17, 0.8);
    color: #f8fafc;
    font-size: 0.88rem;
    outline: none;
  }

  .filter-pills {
    display: flex;
    gap: 6px;
    align-items: center;
  }

  .filter-label {
    font-size: 0.72rem;
    color: #64748b;
    font-family: var(--font-family-mono, monospace);
  }

  .pill {
    padding: 5px 10px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: transparent;
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 700;
    cursor: pointer;
  }

  .pill.active {
    background: rgba(255, 255, 255, 0.15);
    color: #f8fafc;
    border-color: rgba(255, 255, 255, 0.3);
  }

  .pill-red.active { background: rgba(239, 68, 68, 0.25); color: #ef4444; border-color: #ef4444; }
  .pill-amber.active { background: rgba(245, 158, 11, 0.25); color: #f59e0b; border-color: #f59e0b; }
  .pill-green.active { background: rgba(16, 185, 129, 0.25); color: #10b981; border-color: #10b981; }

  .tripwire-split {
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 20px;
    align-items: start;
  }

  .tripwires-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 820px;
    overflow-y: auto;
    padding-right: 4px;
  }

  .tripwire-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 12px 14px;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .tripwire-card:hover {
    border-color: rgba(255, 255, 255, 0.25);
    background: rgba(30, 41, 59, 0.6);
  }

  .tripwire-card.selected {
    border-color: #38bdf8;
    background: rgba(56, 189, 248, 0.08);
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
  }

  .tc-top {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 6px;
    flex-wrap: wrap;
  }

  .tc-id {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.72rem;
    font-weight: 800;
    color: #f8fafc;
    background: rgba(255, 255, 255, 0.08);
    padding: 1px 6px;
    border-radius: 4px;
  }

  .stream-chip {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.65rem;
    padding: 1px 6px;
    border-radius: 9999px;
    border: 1px solid;
    background: rgba(0, 0, 0, 0.3);
  }

  .tc-badge {
    margin-left: auto;
    font-family: var(--font-family-mono, monospace);
    font-size: 0.65rem;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 9999px;
  }

  .tc-badge.red { background: rgba(239, 68, 68, 0.18); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.35); }
  .tc-badge.amber { background: rgba(245, 158, 11, 0.18); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.35); }
  .tc-badge.green { background: rgba(16, 185, 129, 0.18); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.35); }

  .tc-desc {
    font-size: 0.85rem;
    color: #cbd5e1;
    margin: 0 0 8px 0;
    line-height: 1.45;
  }

  .tc-footer {
    display: flex;
    justify-content: space-between;
    font-size: 0.68rem;
    color: #64748b;
    font-family: var(--font-family-mono, monospace);
  }

  .tc-arrow {
    color: #38bdf8;
    font-weight: 700;
  }

  /* Tripwire Detail Drawer */
  .tripwire-drawer {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    padding: 18px;
    position: sticky;
    top: 88px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  }

  .drawer-header {
    margin-bottom: 14px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .dh-top {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 8px;
    flex-wrap: wrap;
  }

  .dh-id {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.76rem;
    font-weight: 800;
    background: rgba(255, 255, 255, 0.1);
    padding: 2px 7px;
    border-radius: 6px;
    color: #f8fafc;
  }

  .dh-status {
    margin-left: auto;
    font-family: var(--font-family-mono, monospace);
    font-size: 0.7rem;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 9999px;
  }

  .dh-status.red { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.4); }
  .dh-status.amber { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); }
  .dh-status.green { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); }

  .drawer-header h3 {
    font-size: 1.05rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 0;
    line-height: 1.4;
  }

  .drawer-section {
    margin-bottom: 12px;
  }

  .d-label {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.65rem;
    font-weight: 800;
    color: #94a3b8;
    letter-spacing: 0.05em;
    display: block;
    margin-bottom: 4px;
  }

  .d-box {
    background: rgba(6, 9, 17, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.85rem;
    line-height: 1.45;
  }

  .d-box.highlight {
    border-color: rgba(56, 189, 248, 0.3);
    color: #38bdf8;
  }

  .d-text {
    font-size: 0.85rem;
    color: #cbd5e1;
    line-height: 1.45;
    margin: 0;
  }

  .drawer-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 12px;
  }

  .dg-cell {
    background: rgba(6, 9, 17, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 8px 10px;
  }

  .dg-cell p {
    margin: 0;
    font-size: 0.78rem;
    color: #cbd5e1;
    line-height: 1.35;
  }

  .highlight-text {
    font-family: var(--font-family-mono, monospace);
    font-weight: 800;
    color: #10b981;
  }

  .drawer-footer {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 0.75rem;
    color: #94a3b8;
  }

  .drawer-footer .notes {
    font-size: 0.72rem;
    color: #64748b;
    font-style: italic;
  }

  /* Utility classes */
  .text-danger { color: #ef4444; }
  .text-warning { color: #f59e0b; }
  .text-success { color: #10b981; }
  .font-mono { font-family: var(--font-family-mono, monospace); }

  @media (max-width: 980px) {
    .hero-main-row {
      grid-template-columns: 1fr;
    }
    .deficit-top-row {
      grid-template-columns: 1fr;
    }
    .triad-grid {
      grid-template-columns: 1fr;
    }
    .sovereignty-bridge-card {
      flex-direction: column;
      align-items: flex-start;
    }
    .tripwire-split {
      grid-template-columns: 1fr;
    }
    .tripwire-drawer {
      position: static;
    }
  }
</style>
