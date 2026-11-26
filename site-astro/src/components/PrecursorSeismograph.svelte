<script lang="ts">
  import precursorSummary from '../data/precursor_summary.json';
  import autonomyData from '../data/autonomy_seismometer.json';
  import asiPrecursors from '../data/asi_precursors.json';
  import layer2Data from '../data/hsri_layer2.json';
  import CivilizationalAirGap from './CivilizationalAirGap.svelte';
  import TelemetryUptimeBadge from './TelemetryUptimeBadge.svelte';
  import VerificationHorizonChart from './VerificationHorizonChart.svelte';

  const base = (import.meta.env.BASE_URL || '').replace(/\/$/, '');

  // Three plain tabs preserving full tool depth
  let activeTab: 'visuals' | 'signs' | 'backup' = 'visuals';

  // Layman status mapping matching Homepage Decision #1 (Steady / Stirring / Rising)
  const overallScore = Number(precursorSummary.master_precursor_threat_score ?? 8.44);
  const pulseWord = overallScore < 4.0 ? 'Steady' : overallScore < 7.0 ? 'Stirring' : 'Rising';

  // Radial gauge needle angle: 0 -> -90deg (left), 10 -> +90deg (right)
  const needleDeg = -90 + (Math.min(10, Math.max(0, overallScore)) / 10) * 180;

  // Real metrics from precursor_summary & autonomy_seismometer
  const s1 = precursorSummary.stream_1_autonomy_seismometer;
  const s2 = precursorSummary.stream_2_latent_drift_detector;
  const s3 = precursorSummary.stream_3_verification_wedge;

  const m2mDots = Math.round(s1.m2m_share * 100); // 64 of 100
  const readableBlocks = Math.round(s2.human_parseability * 10); // 3 of 10
  const series = autonomyData.timeseries || [];
  const milestones = autonomyData.milestones || [];
  let selectedMilestoneId = milestones[milestones.length - 1]?.milestone_id || 'MS-2026-02';

  $: activeMilestone = milestones.find((m: any) => m.milestone_id === selectedMilestoneId) || milestones[milestones.length - 1];

  // Historical Seismograph Trajectory SVG curve (17 points from 2023-01 to 2026-10)
  const TW = 640;
  const TH = 158;
  const tPadL = 54;
  const tPadR = 30;
  const tPadT = 16;
  const tPadB = 28;
  const tX = (i: number) => tPadL + (i / Math.max(1, series.length - 1)) * (TW - tPadL - tPadR);
  const tY = (score: number) => TH - tPadB - (Math.min(10, Math.max(0, score)) / 10) * (TH - tPadT - tPadB);
  const trendPolyline = series.map((pt: any, i: number) => `${tX(i).toFixed(1)},${tY(pt.seismograph_score).toFixed(1)}`).join(' ');
  const trendArea = series.length
    ? `M ${tX(0).toFixed(1)},${(TH - tPadB).toFixed(1)} L ${trendPolyline} L ${tX(series.length - 1).toFixed(1)},${(TH - tPadB).toFixed(1)} Z`
    : '';

  // Battery comparison (Singapore vs Norway) from hsri_layer2.json
  const sgpEntry = layer2Data.find((c: any) => c.country_iso3 === 'SGP');
  const norEntry = layer2Data.find((c: any) => c.country_iso3 === 'NOR');

  // 14 Early Warning Signs filters
  let signStatusFilter: 'all' | 'red' | 'amber' | 'green' = 'all';
  let signSearch = '';
  let selectedSignId = asiPrecursors[0]?.id || 'PREC-001';

  const countRed = asiPrecursors.filter(p => p.status_color === 'red').length;
  const countAmber = asiPrecursors.filter(p => p.status_color === 'amber').length;
  const countGreen = asiPrecursors.filter(p => p.status_color === 'green').length;

  $: filteredSigns = asiPrecursors.filter(p => {
    const okStatus = signStatusFilter === 'all' || p.status_color === signStatusFilter;
    const okQ = !signSearch.trim() ||
      p.id.toLowerCase().includes(signSearch.toLowerCase()) ||
      p.description.toLowerCase().includes(signSearch.toLowerCase());
    return okStatus && okQ;
  });

  $: selectedSign = asiPrecursors.find(p => p.id === selectedSignId) || asiPrecursors[0];

  function plainStatusLabel(color: string) {
    if (color === 'red') return 'Happening today';
    if (color === 'amber') return 'Early signs appearing';
    return 'Being watched';
  }
</script>

<div class="seismo-shell" id="seismograph-root">
  <!-- CALM VISUAL HERO + RADIAL SPEEDOMETER -->
  <section class="hero-visual-panel">
    <div class="hv-left">
      <span class="hv-pill">
        <span class="hv-dot" aria-hidden="true"></span>
        LIVE PACE TRACKER
      </span>
      <h1 class="hv-title">How fast is AI moving compared to human review?</h1>
      <p class="hv-lead">
        Visual gauges tracking the gap between automated computer speed and how fast people can inspect what happens.
      </p>
      <div class="uptime-wrap">
        <TelemetryUptimeBadge />
      </div>
    </div>

    <div class="hv-gauge-card" aria-label={`Current pace reading: ${pulseWord}, technical score ${overallScore.toFixed(2)} out of 10`}>
      <!-- Clean Radial Speedometer SVG -->
      <svg viewBox="0 0 220 132" width="220" height="132" class="gauge-svg" role="img" aria-label={`Half-circle speedometer pointing to ${pulseWord} (${overallScore.toFixed(2)} out of 10)`}>
        <!-- Background arc track: Steady (0-4), Stirring (4-7), Rising (7-10) -->
        <path d="M 24 112 A 86 86 0 0 1 68 38" fill="none" stroke="var(--threat-sovereign)" stroke-width="14" stroke-linecap="round" opacity="0.85" />
        <path d="M 74 34 A 86 86 0 0 1 156 44" fill="none" stroke="var(--threat-warning)" stroke-width="14" stroke-linecap="round" opacity="0.85" />
        <path d="M 162 49 A 86 86 0 0 1 196 112" fill="none" stroke="var(--threat-critical)" stroke-width="14" stroke-linecap="round" opacity="0.9" />

        <!-- Zone labels -->
        <text x="18" y="127" class="g-zone">Steady</text>
        <text x="110" y="16" text-anchor="middle" class="g-zone">Stirring</text>
        <text x="202" y="127" text-anchor="end" class="g-zone">Rising</text>

        <!-- Pointer needle -->
        <g transform={`translate(110 112) rotate(${needleDeg})`}>
          <polygon points="-4,0 0,-74 4,0" fill="var(--text-primary)" />
          <circle cx="0" cy="0" r="8" fill="var(--text-primary)" />
          <circle cx="0" cy="0" r="3" fill="var(--bg-surface-elevated)" />
        </g>
      </svg>

      <div class="gauge-readout">
        <span class="gauge-word">{pulseWord}</span>
        <span class="gauge-sub">Machines move faster than manual step-by-step checks.</span>
        <details class="gauge-tech">
          <summary>&#9432; Technical reading: {overallScore.toFixed(2)} / 10</summary>
          <span>Composite precursor monitor updated periodically from open telemetry logs.</span>
        </details>
      </div>
    </div>
  </section>

  <!-- 3 CLEAR NAVIGATION TABS -->
  <div class="visual-tabs" role="tablist" aria-label="Choose visual view">
    <button
      type="button"
      role="tab"
      aria-selected={activeTab === 'visuals'}
      class="vtab"
      class:active={activeTab === 'visuals'}
      on:click={() => (activeTab = 'visuals')}
    >
      Visual Charts
    </button>
    <button
      type="button"
      role="tab"
      aria-selected={activeTab === 'signs'}
      class="vtab"
      class:active={activeTab === 'signs'}
      on:click={() => (activeTab = 'signs')}
    >
      14 Early Signs <span class="vtab-pill">{countRed} active</span>
    </button>
    <button
      type="button"
      role="tab"
      aria-selected={activeTab === 'backup'}
      class="vtab"
      class:active={activeTab === 'backup'}
      on:click={() => (activeTab = 'backup')}
    >
      Backup Test (If Cloud Pauses)
    </button>
  </div>

  <!-- TAB 1: MOSTLY VISUAL -->
  {#if activeTab === 'visuals'}
    <!-- VISUAL 1: 1.5s vs 80m RACE + 2022-2026 CURVE -->
    <VerificationHorizonChart />

    <!-- VISUALS 2 & 3: TWO PICTOGRAM CARDS -->
    <div class="pictograms-grid">
      <!-- Pictogram 2: 100-dot Machine-to-Machine Share -->
      <article class="pic-card">
        <span class="pic-kicker">2 · WHO CLICKS "APPROVE"?</span>
        <h3 class="pic-title">Roughly 6 in 10 automated steps happen machine-to-machine</h3>

        <!-- 10x10 Visual Dot Grid -->
        <div class="dot-grid-wrap">
          <div class="dot-matrix" role="img" aria-label={`${m2mDots} out of 100 dots represent automated machine-to-machine calls without human clicks`}>
            {#each Array(100) as _, idx}
              <span class="m-dot" class:machine={idx < m2mDots}></span>
            {/each}
          </div>
          <div class="pic-legend">
            <span class="leg-chip"><i class="sw-m"></i> Machine-to-machine ({m2mDots}%)</span>
            <span class="leg-chip"><i class="sw-h"></i> Human-triggered ({100 - m2mDots}%)</span>
          </div>
        </div>

        <details class="pic-details">
          <summary>&#9432; Technical sources ({(s1.m2m_share * 100).toFixed(1)}% composite)</summary>
          <p>Weighted across API agent traffic, automated payments, smart contracts, and autonomous web activity (Stream 1: {s1.score.toFixed(2)}/10).</p>
        </details>
      </article>

      <!-- Pictogram 3: 10-block Readable vs Compressed Language -->
      <article class="pic-card">
        <span class="pic-kicker">3 · CAN PEOPLE READ WHAT AI THINKS?</span>
        <h3 class="pic-title">About 3 in 10 steps stay plain enough for humans to follow live</h3>

        <!-- 10-Tile Visual Readability Strip -->
        <div class="read-blocks-wrap">
          <div class="read-grid" role="img" aria-label={`${readableBlocks} out of 10 blocks readable in plain text; ${10 - readableBlocks} blocks compressed or hidden`}>
            {#each Array(10) as _, idx}
              {#if idx < readableBlocks}
                <div class="r-tile readable" title="Readable plain language step">
                  <span class="r-icon">Aa</span>
                  <span class="r-lbl">Plain</span>
                </div>
              {:else}
                <div class="r-tile opaque" title="Hidden scratchpad or compressed code">
                  <span class="r-icon">&bull;&bull;&bull;</span>
                  <span class="r-lbl">Hidden</span>
                </div>
              {/if}
            {/each}
          </div>
          <div class="pic-legend">
            <span class="leg-chip"><i class="sw-h"></i> Easy to inspect ({Math.round(s2.human_parseability * 100)}%)</span>
            <span class="leg-chip"><i class="sw-o"></i> Hidden / shorthand ({Math.round((1 - s2.human_parseability) * 100)}%)</span>
          </div>
        </div>

        <details class="pic-details">
          <summary>&#9432; Technical details (Stream 2: {s2.score.toFixed(2)}/10)</summary>
          <p>Human-readable share: {(s2.human_parseability * 100).toFixed(1)}% · Hidden chain-of-thought gap: {(s1.hptg * 100).toFixed(1)}% (EXP-08-SYN).</p>
        </details>
      </article>
    </div>

    <!-- VISUAL 4: 2023 -> 2026 TIMELINE + MODEL VISIBILITY MILESTONES -->
    <section class="timeline-visual-card">
      <div class="tv-head">
        <div>
          <span class="pic-kicker">4 · 2023–2026 TREND</span>
          <h3 class="pic-title">How AI pace climbed — and why open weights help humans see</h3>
          <p class="tv-sub">Tap a release dot below: open-weight models gave researchers clear windows inside, while closed loops reduced visibility.</p>
        </div>
        <span class="tv-now-pill">2023: 1.05 &rarr; Today: {series[series.length - 1]?.seismograph_score.toFixed(2)}</span>
      </div>

      <!-- 2023-2026 Smooth Area Chart SVG -->
      <svg viewBox={`0 0 ${TW} ${TH}`} class="trend-svg" role="img" aria-label="Trend line rising from 1.05 in January 2023 to 8.78 in October 2026">
        <defs>
          <linearGradient id="paceTrendFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="var(--accent-primary)" stop-opacity="0.28" />
            <stop offset="100%" stop-color="var(--accent-primary)" stop-opacity="0.02" />
          </linearGradient>
        </defs>
        <line x1={tPadL} y1={tY(4)} x2={TW - tPadR} y2={tY(4)} stroke="var(--border-subtle)" stroke-dasharray="4 4" />
        <text x={tPadL - 6} y={tY(4) + 3} text-anchor="end" class="ax-txt">Stirring</text>
        <line x1={tPadL} y1={tY(7)} x2={TW - tPadR} y2={tY(7)} stroke="var(--border-subtle)" stroke-dasharray="4 4" />
        <text x={tPadL - 6} y={tY(7) + 3} text-anchor="end" class="ax-txt">Rising</text>

        <path d={trendArea} fill="url(#paceTrendFill)" />
        <polyline points={trendPolyline} fill="none" stroke="var(--accent-primary)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />

        {#each series as pt, idx}
          {#if idx === 0 || idx === series.length - 1 || idx % 4 === 0}
            <circle cx={tX(idx)} cy={tY(pt.seismograph_score)} r={idx === series.length - 1 ? 5.5 : 3.5} fill="var(--accent-primary)" />
            <text x={tX(idx)} y={TH - 8} text-anchor="middle" class="ax-txt">{pt.period.slice(0, 7)}</text>
          {/if}
        {/each}
      </svg>

      <!-- Clickable Model Openness Visualizer -->
      <div class="milestone-pills" role="tablist" aria-label="Model releases and openness">
        {#each milestones as ms}
          <button
            type="button"
            class="ms-pill"
            class:selected={selectedMilestoneId === ms.milestone_id}
            class:open-model={ms.human_readable_proofs}
            on:click={() => (selectedMilestoneId = ms.milestone_id)}
          >
            <span class="ms-dot" class:open={ms.human_readable_proofs}></span>
            <span>{(ms.model_or_event || ms.milestone_id || '').split('(')[0].trim()}</span>
          </button>
        {/each}
      </div>

      {#if activeMilestone}
        <div class="ms-visual-meter">
          <div class="ms-vm-top">
            <strong>{activeMilestone.model_or_event || activeMilestone.milestone_id}</strong>
            <span class="ms-badge" class:open={activeMilestone.human_readable_proofs}>
              {activeMilestone.human_readable_proofs ? 'Open weights / visible reasoning' : 'Closed weights / hidden steps'}
            </span>
          </div>
          <div class="vis-bar-row">
            <span class="vis-lbl">How clearly outside researchers can inspect steps:</span>
            <div class="vis-track">
              <div class="vis-fill" class:open={activeMilestone.human_readable_proofs} style="width: {Math.round(activeMilestone.auditability_score * 100)}%"></div>
            </div>
            <strong>{Math.round(activeMilestone.auditability_score * 100)}%</strong>
          </div>
          <p class="ms-note">{activeMilestone.notes}</p>
        </div>
      {/if}
    </section>

    <!-- VISUAL 5: COUNTRY BATTERY COMPARISON & NEXT STEP -->
    <section class="bridge-visual-card">
      <div class="bv-left">
        <span class="pic-kicker">5 · WHY BACKUPS MATTER FOR EVERY COUNTRY</span>
        <h3 class="pic-title">If automated tools pause, how long can essentials keep running?</h3>
        <div class="battery-compare">
          <div class="bat-row">
            <span class="bat-country">Singapore (high digital reliance)</span>
            <div class="bat-cells" aria-label="1 of 5 backup bars (~8 hours)">
              <span class="b-cell low"></span><span class="b-cell"></span><span class="b-cell"></span><span class="b-cell"></span><span class="b-cell"></span>
            </div>
            <strong>{sgpEntry ? `${sgpEntry.t_half_hours}h` : '8h'}</strong>
          </div>
          <div class="bat-row">
            <span class="bat-country">Norway (deep offline reserves)</span>
            <div class="bat-cells" aria-label="5 of 5 backup bars (30+ days)">
              <span class="b-cell ok"></span><span class="b-cell ok"></span><span class="b-cell ok"></span><span class="b-cell ok"></span><span class="b-cell ok"></span>
            </div>
            <strong>{norEntry ? `${Math.round(norEntry.t_half_hours / 24)}d+` : '30d+'}</strong>
          </div>
        </div>
      </div>

      <div class="bv-actions">
        <a href={`${base}/countries/`} class="btn-solid">Explore 39-Country Index &rarr;</a>
        <button type="button" class="btn-ghost" on:click={() => (activeTab = 'backup')}>
          Try Power-Outage Simulator
        </button>
        <a href={`${base}/#wish-doors`} class="btn-ghost">Play 60s Breakthrough Story</a>
      </div>
    </section>
  {/if}

  <!-- TAB 2: 14 EARLY SIGNS (PLAIN SUMMARY FIRST + DEEP DOSSIER) -->
  {#if activeTab === 'signs'}
    <div class="signs-view">
      <!-- Visual 14-Indicator Stacked Bar -->
      <div class="signs-overview-bar">
        <div class="so-top">
          <strong>14 real-world signals researchers watch</strong>
          <span>{countRed} happening today &middot; {countAmber} showing early signs &middot; {countGreen} being watched</span>
        </div>
        <div class="so-segments" aria-hidden="true">
          <div class="seg-red" style="flex: {countRed}">{countRed} Today</div>
          <div class="seg-amber" style="flex: {countAmber}">{countAmber} Early</div>
          {#if countGreen > 0}<div class="seg-green" style="flex: {countGreen}">{countGreen} Watch</div>{/if}
        </div>
      </div>

      <div class="signs-filters">
        <input
          type="search"
          placeholder="Search 14 signals..."
          bind:value={signSearch}
          class="sign-search"
        />
        <div class="sign-pills">
          <button type="button" class="sp-btn" class:active={signStatusFilter === 'all'} on:click={() => (signStatusFilter = 'all')}>All ({asiPrecursors.length})</button>
          <button type="button" class="sp-btn" class:active={signStatusFilter === 'red'} on:click={() => (signStatusFilter = 'red')}>Today ({countRed})</button>
          <button type="button" class="sp-btn" class:active={signStatusFilter === 'amber'} on:click={() => (signStatusFilter = 'amber')}>Early ({countAmber})</button>
          <button type="button" class="sp-btn" class:active={signStatusFilter === 'green'} on:click={() => (signStatusFilter = 'green')}>Watch ({countGreen})</button>
        </div>
      </div>

      <div class="signs-split">
        <div class="signs-list">
          {#each filteredSigns as p}
            <button
              type="button"
              class="sign-card"
              class:selected={selectedSignId === p.id}
              on:click={() => (selectedSignId = p.id)}
            >
              <div class="sc-top">
                <span class="sc-id">{p.id}</span>
                <span class="sc-badge {p.status_color}">{plainStatusLabel(p.status_color)}</span>
              </div>
              <p class="sc-desc">{p.description}</p>
            </button>
          {/each}
        </div>

        {#if selectedSign}
          <aside class="sign-drawer">
            <span class="sc-badge {selectedSign.status_color}">{plainStatusLabel(selectedSign.status_color)}</span>
            <h3>{selectedSign.id}</h3>
            <p class="sd-desc">{selectedSign.description}</p>

            <div class="sd-box">
              <span class="sd-lbl">What researchers watch for</span>
              <p>{selectedSign.proposed_threshold}</p>
            </div>
            <div class="sd-box">
              <span class="sd-lbl">Observed so far</span>
              <p>{selectedSign.baseline_or_time_series}</p>
            </div>

            <details class="pic-details">
              <summary>&#9432; Verification notes &amp; blind-spot risks</summary>
              <p><strong>How measured:</strong> {selectedSign.measurement_method}</p>
              <p><strong>False-alarm risk:</strong> {selectedSign.false_positive_risk}</p>
              <p><strong>Missed-signal risk:</strong> {selectedSign.false_negative_risk}</p>
              <p><strong>Independent checkable:</strong> {selectedSign.outsider_verifiable} &middot; {selectedSign.data_holder}</p>
            </details>
          </aside>
        {/if}
      </div>
    </div>
  {/if}

  <!-- TAB 3: BACKUP SIMULATOR -->
  {#if activeTab === 'backup'}
    <div class="backup-wrap">
      <p class="backup-intro">
        Choose a country and slide the pause duration to see which essential services rely on offline human backups vs continuous cloud AI links.
      </p>
      <CivilizationalAirGap />
    </div>
  {/if}
</div>

<style>
  .seismo-shell {
    padding-top: 0.35rem;
  }

  /* Hero Panel */
  .hero-visual-panel {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 18px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.25rem;
    display: grid;
    grid-template-columns: 1.35fr 0.95fr;
    gap: 1.5rem;
    align-items: center;
    box-shadow: var(--shadow-sm);
  }

  .hv-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.25rem 0.72rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-medium);
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 800;
    color: var(--accent-primary);
    margin-bottom: 0.75rem;
  }

  .hv-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent-primary);
  }

  .hv-title {
    margin: 0 0 0.6rem;
    font-family: var(--font-family-sans);
    font-size: clamp(1.65rem, 3.2vw, 2.3rem);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.025em;
    color: var(--text-primary);
  }

  .hv-lead {
    margin: 0 0 0.85rem;
    font-size: 0.98rem;
    line-height: 1.55;
    color: var(--text-secondary);
  }

  .uptime-wrap :global(.uptime-badge) {
    margin: 0;
  }

  .hv-gauge-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.1rem 1rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .gauge-svg {
    max-width: 100%;
    height: auto;
  }

  .g-zone {
    font-family: var(--font-family-mono);
    font-size: 9.5px;
    font-weight: 700;
    fill: var(--text-secondary);
  }

  .gauge-readout {
    margin-top: 0.35rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .gauge-word {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--threat-critical);
  }

  .gauge-sub {
    font-size: 0.84rem;
    color: var(--text-secondary);
    line-height: 1.4;
  }

  .gauge-tech {
    margin-top: 0.2rem;
    font-size: 0.75rem;
    color: var(--text-secondary);
  }

  .gauge-tech summary {
    cursor: pointer;
    font-family: var(--font-family-mono);
    font-weight: 700;
    color: var(--accent-primary);
  }

  /* Navigation Tabs */
  .visual-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.25rem;
  }

  .vtab {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    min-height: 42px;
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    font-weight: 700;
    font-size: 0.88rem;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .vtab:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .vtab.active {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .vtab-pill {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    padding: 0.12rem 0.48rem;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.2);
  }

  /* Pictogram Cards */
  .pictograms-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
    margin-bottom: 1.35rem;
  }

  .pic-card,
  .timeline-visual-card,
  .bridge-visual-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    padding: 1.35rem;
    box-shadow: var(--shadow-sm);
  }

  .pic-kicker {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--accent-primary);
    margin-bottom: 0.25rem;
  }

  .pic-title {
    margin: 0 0 0.85rem;
    font-size: 1.12rem;
    font-weight: 800;
    line-height: 1.3;
    color: var(--text-primary);
  }

  .dot-grid-wrap,
  .read-blocks-wrap {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.9rem;
    margin-bottom: 0.75rem;
  }

  .dot-matrix {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 6px;
    max-width: 240px;
    margin: 0 auto 0.75rem;
  }

  .m-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--accent-primary);
    opacity: 0.35;
  }

  .m-dot.machine {
    background: var(--threat-warning);
    opacity: 1;
  }

  .read-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.45rem;
    margin-bottom: 0.75rem;
  }

  .r-tile {
    border-radius: 8px;
    padding: 0.45rem 0.25rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    border: 1px solid var(--border-subtle);
  }

  .r-tile.readable {
    background: var(--threat-sovereign-bg);
    border-color: var(--threat-sovereign-border);
    color: var(--threat-sovereign);
  }

  .r-tile.opaque {
    background: var(--bg-surface-sunken);
    color: var(--text-muted);
  }

  .r-icon {
    font-family: var(--font-family-mono);
    font-weight: 800;
    font-size: 0.86rem;
  }

  .r-lbl {
    font-size: 0.65rem;
    font-weight: 700;
  }

  .pic-legend {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem 1rem;
    font-size: 0.76rem;
    color: var(--text-secondary);
  }

  .leg-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-weight: 600;
  }

  .sw-m,
  .sw-h,
  .sw-o {
    width: 10px;
    height: 10px;
    border-radius: 3px;
    display: inline-block;
  }

  .sw-m { background: var(--threat-warning); }
  .sw-h { background: var(--threat-sovereign); }
  .sw-o { background: var(--border-strong); }

  .pic-details summary {
    cursor: pointer;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .pic-details p {
    margin: 0.45rem 0 0;
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.45;
  }

  /* Timeline Visual Card */
  .timeline-visual-card {
    margin-bottom: 1.35rem;
  }

  .tv-head {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }

  .tv-sub {
    margin: 0;
    font-size: 0.88rem;
    color: var(--text-secondary);
    max-width: 680px;
  }

  .tv-now-pill {
    font-family: var(--font-family-mono);
    font-size: 0.76rem;
    font-weight: 700;
    padding: 0.3rem 0.7rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-medium);
    color: var(--accent-primary);
  }

  .trend-svg {
    width: 100%;
    height: auto;
    display: block;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.4rem;
    margin-bottom: 0.85rem;
  }

  .ax-txt {
    font-family: var(--font-family-mono);
    font-size: 9.5px;
    fill: var(--text-muted);
  }

  .milestone-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.85rem;
  }

  .ms-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.38rem;
    padding: 0.36rem 0.72rem;
    border-radius: 9999px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-secondary);
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    min-height: 36px;
  }

  .ms-pill.selected {
    border-color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
    color: var(--text-primary);
  }

  .ms-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--threat-warning);
  }

  .ms-dot.open {
    background: var(--threat-sovereign);
  }

  .ms-visual-meter {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.85rem 1rem;
  }

  .ms-vm-top {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.5rem;
    font-size: 0.94rem;
    color: var(--text-primary);
  }

  .ms-badge {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.16rem 0.55rem;
    border-radius: 9999px;
    background: var(--threat-warning-bg);
    color: var(--threat-warning);
  }

  .ms-badge.open {
    background: var(--threat-sovereign-bg);
    color: var(--threat-sovereign);
  }

  .vis-bar-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 0.4rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
  }

  .vis-track {
    flex: 1;
    height: 10px;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    overflow: hidden;
  }

  .vis-fill {
    height: 100%;
    border-radius: 9999px;
    background: var(--threat-warning);
    transition: width 0.25s ease;
  }

  .vis-fill.open {
    background: var(--threat-sovereign);
  }

  .ms-note {
    margin: 0;
    font-size: 0.82rem;
    color: var(--text-secondary);
  }

  /* Country Battery Bridge */
  .bridge-visual-card {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 1.25rem;
  }

  .bv-left {
    flex: 1 1 380px;
  }

  .battery-compare {
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
  }

  .bat-row {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    font-size: 0.86rem;
    color: var(--text-primary);
  }

  .bat-country {
    min-width: 215px;
  }

  .bat-cells {
    display: flex;
    gap: 4px;
  }

  .b-cell {
    width: 18px;
    height: 10px;
    border-radius: 3px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-medium);
  }

  .b-cell.low {
    background: var(--threat-critical);
    border-color: var(--threat-critical);
  }

  .b-cell.ok {
    background: var(--threat-sovereign);
    border-color: var(--threat-sovereign);
  }

  .bv-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
  }

  .btn-solid,
  .btn-ghost {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 42px;
    padding: 0.55rem 1rem;
    border-radius: 10px;
    font-size: 0.86rem;
    font-weight: 700;
    text-decoration: none;
    cursor: pointer;
  }

  .btn-solid {
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    border: 0;
  }

  .btn-ghost {
    background: var(--bg-surface);
    color: var(--text-primary);
    border: 1px solid var(--border-medium);
  }

  /* Tab 2: 14 Early Signs */
  .signs-overview-bar {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1rem 1.15rem;
    margin-bottom: 1rem;
  }

  .so-top {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 0.4rem;
    margin-bottom: 0.55rem;
    font-size: 0.88rem;
    color: var(--text-primary);
  }

  .so-segments {
    display: flex;
    gap: 4px;
    border-radius: 9999px;
    overflow: hidden;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    color: #fff;
    text-align: center;
  }

  .seg-red { background: var(--threat-critical); padding: 0.3rem 0.5rem; }
  .seg-amber { background: var(--threat-warning); padding: 0.3rem 0.5rem; }
  .seg-green { background: var(--threat-sovereign); padding: 0.3rem 0.5rem; }

  .signs-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    margin-bottom: 1rem;
  }

  .sign-search {
    flex: 1 1 220px;
    min-height: 40px;
    padding: 0.45rem 0.8rem;
    border-radius: 10px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
  }

  .sign-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .sp-btn {
    min-height: 38px;
    padding: 0.35rem 0.8rem;
    border-radius: 9999px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 0.8rem;
    cursor: pointer;
  }

  .sp-btn.active {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .signs-split {
    display: grid;
    grid-template-columns: 1.15fr 0.95fr;
    gap: 1rem;
    align-items: start;
  }

  .signs-list {
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
    max-height: 620px;
    overflow-y: auto;
  }

  .sign-card {
    text-align: start;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    cursor: pointer;
  }

  .sign-card.selected {
    border-color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
  }

  .sc-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.35rem;
  }

  .sc-id {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    color: var(--text-secondary);
  }

  .sc-badge {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.14rem 0.5rem;
    border-radius: 9999px;
  }

  .sc-badge.red {
    background: var(--threat-critical-bg);
    color: var(--threat-critical);
  }
  .sc-badge.amber {
    background: var(--threat-warning-bg);
    color: var(--threat-warning);
  }
  .sc-badge.green {
    background: var(--threat-sovereign-bg);
    color: var(--threat-sovereign);
  }

  .sc-desc {
    margin: 0;
    font-size: 0.86rem;
    color: var(--text-primary);
    line-height: 1.45;
  }

  .sign-drawer {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1.15rem;
    position: sticky;
    top: 84px;
  }

  .sign-drawer h3 {
    margin: 0.45rem 0 0.35rem;
    color: var(--text-primary);
  }

  .sd-desc {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .sd-box {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 0.7rem 0.85rem;
    margin-bottom: 0.65rem;
  }

  .sd-lbl {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.66rem;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--accent-primary);
    margin-bottom: 0.2rem;
  }

  .sd-box p {
    margin: 0;
    font-size: 0.84rem;
    color: var(--text-primary);
  }

  .backup-intro {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    font-size: 0.92rem;
    color: var(--text-secondary);
    margin-bottom: 0.75rem;
  }

  @media (max-width: 900px) {
    .hero-visual-panel,
    .pictograms-grid,
    .signs-split {
      grid-template-columns: 1fr;
    }
    .sign-drawer {
      position: static;
    }
  }

  @media (max-width: 540px) {
    .hero-visual-panel,
    .pic-card,
    .timeline-visual-card,
    .bridge-visual-card {
      padding: 1rem;
    }
    .bat-row {
      flex-wrap: wrap;
    }
    .bat-country {
      min-width: 100%;
    }
    .vis-bar-row {
      flex-wrap: wrap;
    }
  }
</style>
