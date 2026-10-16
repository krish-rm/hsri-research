<script lang="ts">
  import countryData from '../data/country_scores.json';

  let activeLayer = 'layer2'; // 'layer2' | 'layer1'
  let searchQuery = '';

  const countries = countryData.countries || [];
  const meta = countryData.metadata || {};

  $: sortedList = [...countries].sort((a: any, b: any) => {
    if (activeLayer === 'layer2') {
      return (a.rank_L2 || a.rank) - (b.rank_L2 || b.rank);
    } else {
      return (a.rank_L1 || a.legacy_rank_linear || 99) - (b.rank_L1 || b.legacy_rank_linear || 99);
    }
  });

  $: filteredList = sortedList.filter((c: any) => {
    const q = searchQuery.toLowerCase();
    return c.name.toLowerCase().includes(q) || c.code.toLowerCase().includes(q);
  });

  function getTHalfColor(hours: number): string {
    if (hours >= 336) return 'badge-green';
    if (hours >= 72) return 'badge-amber';
    return 'badge-red';
  }

  const base = (import.meta.env.BASE_URL || '/').replace(/\/$/, '');
</script>

<div class="radar-container" id="countries">
  <div class="radar-header">
    <div class="header-left">
      <span class="eyebrow-pill">DECIVILIZATIONAL RESILIENCE</span>
      <h2 class="radar-title">The Sovereign Decoupling Scoreboard</h2>
      <p class="radar-desc">
        Adoption is not resilience. Benchmarking 39 nations on <strong>Decoupling Half-Life (T_half)</strong>—how many hours basic social functionality endures if foreign cloud AI dark-screens.
      </p>
    </div>

    <div class="header-right">
      <div class="layer-toggle-group">
        <button 
          type="button" 
          class="toggle-btn" 
          class:active={activeLayer === 'layer2'} 
          on:click={() => activeLayer = 'layer2'}
        >
          Layer 2: Sovereignty &amp; Air-Gap
        </button>
        <button 
          type="button" 
          class="toggle-btn" 
          class:active={activeLayer === 'layer1'} 
          on:click={() => activeLayer = 'layer1'}
        >
          Layer 1: Adoption Baseline
        </button>
      </div>
    </div>
  </div>

  <!-- Stat Ribbon -->
  <div class="stat-ribbon">
    <div class="stat-cell">
      <div class="stat-label">Global Median T_half</div>
      <div class="stat-val">{meta.medianTHalf || 48.0}h</div>
      <div class="stat-sub">Before infrastructure degradation</div>
    </div>
    <div class="stat-cell">
      <div class="stat-label">High-Compute Trap</div>
      <div class="stat-val red-text">{meta.highComputeTrapCount || 9} Nations</div>
      <div class="stat-sub">High adoption, 0 analog fallback</div>
    </div>
    <div class="stat-cell">
      <div class="stat-label">Most Resilient Sovereign</div>
      <div class="stat-val green-text">Norway (#1)</div>
      <div class="stat-sub">T_half > 720h (Hydro/local grid)</div>
    </div>
    <div class="stat-cell">
      <div class="stat-label">Sharpest Decoupling Rank Shock</div>
      <div class="stat-val red-text">Singapore (-34)</div>
      <div class="stat-sub">Rank #4 → #38 (8h energy floor)</div>
    </div>
  </div>

  <!-- Search and filter -->
  <div class="table-controls">
    <input 
      type="text" 
      placeholder="Search nation by name or ISO code..." 
      bind:value={searchQuery}
      class="search-input"
    />
    <div class="provenance-note">
      {meta.provenanceNote || 'Canonical Dual-Layer Schema v2.0 • B=1000 Dirichlet Monte Carlo Audited'}
    </div>
  </div>

  <!-- Country Leaderboard Table -->
  <div class="table-wrapper">
    <table class="radar-table">
      <thead>
        <tr>
          <th style="width: 70px;">Rank</th>
          <th>Nation</th>
          <th style="width: 100px;">Rank Delta</th>
          <th style="width: 130px;">{activeLayer === 'layer2' ? 'Sovereign Score' : 'Adoption Score'}</th>
          <th style="width: 140px;">Decoupling T_half</th>
          <th>Primary Bottleneck</th>
          <th style="width: 120px;">95% CI</th>
        </tr>
      </thead>
      <tbody>
        {#each filteredList as c}
          <tr class:trap-row={c.high_compute_trap}>
            <td class="rank-cell">
              <strong>#{activeLayer === 'layer2' ? (c.rank_L2 || c.rank) : (c.rank_L1 || c.legacy_rank_linear)}</strong>
            </td>
            <td class="nation-cell">
              <a href={`${base}/countries/${c.id}`} class="nation-link">
                <span class="nation-name">{c.name}</span>
                <span class="iso-chip">{c.code}</span>
                {#if c.high_compute_trap}
                  <span class="trap-pill">TRAP</span>
                {/if}
              </a>
            </td>
            <td class="delta-cell">
              {#if (c.rank_delta || 0) < 0}
                <span class="delta-red">▼ {c.rank_delta}</span>
              {:else if (c.rank_delta || 0) > 0}
                <span class="delta-green">▲ +{c.rank_delta}</span>
              {:else}
                <span class="delta-gray">— 0</span>
              {/if}
            </td>
            <td class="score-cell">
              <strong>{activeLayer === 'layer2' ? (c.H_L2 ? (c.H_L2 * 100).toFixed(1) : c.score) : (c.H_L1 ? (c.H_L1 * 100).toFixed(1) : c.legacy_score_linear)}</strong>
              <span class="score-sub">/ 100</span>
            </td>
            <td>
              <span class={`thalf-badge ${getTHalfColor(c.T_half_h || 48)}`}>
                {c.T_half_h || 48} Hours
              </span>
            </td>
            <td class="bottleneck-cell">
              <span class="bottleneck-text">{c.bottleneck_pillar || 'Infrastructure'}</span>
            </td>
            <td class="ci-cell">
              {#if c.ci_95}
                <span class="ci-badge">[{c.ci_95[0]}–{c.ci_95[1]}]</span>
              {:else}
                <span class="ci-badge">—</span>
              {/if}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

<style>
  .radar-container {
    padding: 3.5rem 0;
    border-top: 1px solid var(--border-subtle);
  }

  .radar-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1.5rem;
  }

  .header-left {
    max-width: 680px;
  }

  .eyebrow-pill {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: var(--accent-primary);
    background: var(--threat-telemetry-bg);
    border: 1px solid var(--threat-telemetry-border);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
  }

  .radar-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem 0;
  }

  .radar-desc {
    font-size: 1.05rem;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.5;
  }

  .layer-toggle-group {
    display: inline-flex;
    background: var(--bg-surface-sunken);
    padding: 4px;
    border-radius: 10px;
    border: 1px solid var(--border-subtle);
  }

  .toggle-btn {
    background: transparent;
    border: none;
    font-family: var(--font-family-sans);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-muted);
    padding: 0.6rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .toggle-btn.active {
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    box-shadow: var(--shadow-sm);
  }

  /* Stat Ribbon */
  .stat-ribbon {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .stat-cell {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    box-shadow: var(--shadow-sm);
  }

  .stat-label {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
  }

  .stat-val {
    font-family: var(--font-family-mono);
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
  }

  .stat-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 0.15rem;
  }

  /* Table Controls */
  .table-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .search-input {
    flex: 1;
    max-width: 340px;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    font-size: 0.875rem;
  }

  .table-legend {
    display: flex;
    gap: 1rem;
    font-size: 0.75rem;
    color: var(--text-muted);
    align-items: center;
  }

  .legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
  }

  /* Table Container */
  .table-outer {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    overflow-x: auto;
    box-shadow: var(--shadow-sm);
  }

  .radar-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
    text-align: left;
  }

  .radar-table th {
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    padding: 0.85rem 1rem;
    font-weight: 700;
    border-bottom: 1px solid var(--border-subtle);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    position: sticky;
    top: 0;
    z-index: 5;
  }

  .radar-table td {
    padding: 0.85rem 1rem;
    border-bottom: 1px solid var(--border-subtle);
    color: var(--text-secondary);
  }

  .radar-table tr:hover td {
    background: var(--bg-surface-sunken);
  }

  .rank-col {
    font-family: var(--font-family-mono);
    font-weight: 700;
    color: var(--text-muted);
    width: 50px;
    font-variant-numeric: tabular-nums;
  }

  .country-cell {
    display: flex;
    align-items: center;
    gap: 0.65rem;
  }

  .flag-icon {
    font-size: 1.15rem;
  }

  .c-name {
    font-weight: 600;
    color: var(--text-primary);
  }

  .c-code {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .score-val {
    font-family: var(--font-family-mono);
    font-weight: 800;
    font-size: 0.95rem;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
  }

  .delta-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.2rem;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.2rem 0.55rem;
    border-radius: 9999px;
  }

  .delta-pill.negative {
    color: var(--threat-critical);
    background: var(--threat-critical-bg);
    border: 1px solid var(--threat-critical-border);
  }

  .delta-pill.positive {
    color: var(--threat-sovereign);
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
  }

  .delta-pill.neutral {
    color: var(--text-muted);
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
  }

  .half-life-badge {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    color: var(--text-primary);
  }

  .ci-span {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .action-link {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--accent-primary);
    text-decoration: none;
  }

  .action-link:hover {
    text-decoration: underline;
  }
</style>