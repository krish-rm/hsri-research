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
    border-top: 1px solid #e2e8f0;
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
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #2563eb;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
  }

  .radar-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem 0;
  }

  .radar-desc {
    font-size: 1.05rem;
    color: #475569;
    margin: 0;
    line-height: 1.5;
  }

  .layer-toggle-group {
    display: inline-flex;
    background: #f1f5f9;
    padding: 4px;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
  }

  .toggle-btn {
    background: transparent;
    border: none;
    font-size: 0.85rem;
    font-weight: 600;
    color: #64748b;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .toggle-btn.active {
    background: #ffffff;
    color: #0f172a;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  }

  /* Stat Ribbon */
  .stat-ribbon {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .stat-cell {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1.25rem;
  }

  .stat-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
    margin-bottom: 0.25rem;
  }

  .stat-val {
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f172a;
    font-family: 'Roboto Mono', monospace;
  }

  .stat-sub {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 0.25rem;
  }

  .red-text { color: #dc2626; }
  .green-text { color: #16a34a; }

  /* Controls */
  .table-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .search-input {
    padding: 0.65rem 1rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 0.9rem;
    width: 320px;
  }

  .provenance-note {
    font-size: 0.8rem;
    color: #64748b;
    font-style: italic;
  }

  /* Table */
  .table-wrapper {
    overflow-x: auto;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
  }

  .radar-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: 0.9rem;
  }

  .radar-table th {
    background: #f8fafc;
    color: #475569;
    font-weight: 700;
    padding: 0.85rem 1rem;
    border-bottom: 1px solid #e2e8f0;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .radar-table td {
    padding: 0.85rem 1rem;
    border-bottom: 1px solid #f1f5f9;
    color: #334155;
  }

  .radar-table tr:hover {
    background: #f8fafc;
  }

  .trap-row {
    background: #fffbfa;
  }

  .rank-cell {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.95rem;
  }

  .nation-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    color: #0f172a;
    font-weight: 600;
  }

  .nation-link:hover .nation-name {
    color: #2563eb;
    text-decoration: underline;
  }

  .iso-chip {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.72rem;
    color: #64748b;
    background: #f1f5f9;
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
  }

  .trap-pill {
    font-size: 0.65rem;
    font-weight: 700;
    color: #b91c1c;
    background: #fee2e2;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
  }

  .delta-red {
    font-family: 'Roboto Mono', monospace;
    font-weight: 700;
    color: #dc2626;
  }

  .delta-green {
    font-family: 'Roboto Mono', monospace;
    font-weight: 700;
    color: #16a34a;
  }

  .delta-gray {
    font-family: 'Roboto Mono', monospace;
    color: #94a3b8;
  }

  .score-cell {
    font-family: 'Roboto Mono', monospace;
  }

  .score-sub {
    font-size: 0.75rem;
    color: #94a3b8;
  }

  .thalf-badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    font-family: 'Roboto Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
  }

  .badge-green {
    background: #f0fdf4;
    color: #166534;
    border: 1px solid #bbf7d0;
  }

  .badge-amber {
    background: #fefce8;
    color: #854d0e;
    border: 1px solid #fef08a;
  }

  .badge-red {
    background: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
  }

  .bottleneck-text {
    font-size: 0.85rem;
    color: #475569;
  }

  .ci-badge {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.75rem;
    color: #64748b;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
  }

  @media (max-width: 640px) {
    .radar-title { font-size: 1.75rem; }
    .search-input { width: 100%; }
  }
</style>
