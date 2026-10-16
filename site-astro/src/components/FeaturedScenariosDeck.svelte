<script lang="ts">
  import asiData from '../data/asi_scenarios.json';

  let showAll = false;
  let selectedCategory = 'all';
  let searchQuery = '';

  const featuredIds = ['SC-25', 'SC-20', 'SC-19'];
  const allScenarios = asiData.scenarios || [];

  $: featuredList = allScenarios.filter((s: any) => featuredIds.includes(s.id));

  $: filteredAll = allScenarios.filter((s: any) => {
    const q = searchQuery.toLowerCase();
    const matchesSearch = s.name.toLowerCase().includes(q) ||
                          s.id.toLowerCase().includes(q) ||
                          s.mechanism.toLowerCase().includes(q) ||
                          s.failureMode.toLowerCase().includes(q);
    
    if (selectedCategory === 'all') return matchesSearch;
    if (selectedCategory === 'attack') {
      return matchesSearch && (s.id === 'SC-25' || s.id === 'SC-24' || s.id === 'SC-05');
    }
    if (selectedCategory === 'cognitive') {
      return matchesSearch && (s.id === 'SC-20' || s.id === 'SC-21' || s.id === 'SC-06' || s.id === 'SC-16');
    }
    if (selectedCategory === 'systemic') {
      return matchesSearch && (s.id === 'SC-19' || s.id === 'SC-08' || s.id === 'SC-09' || s.id === 'SC-10' || s.id === 'SC-23');
    }
    return matchesSearch;
  });

  const base = (import.meta.env.BASE_URL || '/').replace(/\/$/, '');
</script>

<div class="scenarios-deck-container" id="scenarios">
  <div class="deck-header">
    <div class="header-left">
      <span class="eyebrow-pill">RADAR MAPPING</span>
      <h2 class="deck-title">The 26 Takeoff Scenarios</h2>
      <p class="deck-desc">
        Observable crisis injects spanning machine-speed conflict, human supervisory collapse, and civilizational blackouts.
      </p>
    </div>
    <div class="header-right">
      <button 
        type="button" 
        class="toggle-all-btn" 
        on:click={() => showAll = !showAll}
      >
        {showAll ? 'Show Featured 3 Only' : 'Explore All 26 Scenarios & Precursors (' + allScenarios.length + ')'}
      </button>
    </div>
  </div>

  {#if !showAll}
    <!-- Default Featured 3 View -->
    <div class="featured-grid">
      {#each featuredList as sc}
        <div class="scenario-card featured">
          <div class="card-status-bar">
            <span class="sc-id">{sc.id}</span>
            <span class="severity-badge">{sc.severity}</span>
          </div>

          <h3 class="sc-name">{sc.name.split('(')[0].trim()}</h3>
          <p class="sc-question">"{sc.question}"</p>
          <p class="sc-mechanism">{sc.mechanism}</p>

          <div class="precursors-row">
            <span class="pre-label">Precursors:</span>
            {#each (sc.precursors || []) as p}
              <span class="pre-chip">{p}</span>
            {/each}
          </div>

          <div class="card-footer">
            <a href={`${base}/scenarios`} class="sc-link">Deep Scenario Details &rarr;</a>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <!-- Full 26 Filterable Grid -->
    <div class="filter-toolbar">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="Filter scenarios by name, failure mode, or mechanism..." 
          bind:value={searchQuery}
        />
      </div>
      <div class="category-pills">
        <button 
          class="cat-pill" 
          class:active={selectedCategory === 'all'} 
          on:click={() => selectedCategory = 'all'}
        >All ({allScenarios.length})</button>
        <button 
          class="cat-pill" 
          class:active={selectedCategory === 'attack'} 
          on:click={() => selectedCategory = 'attack'}
        >Asymmetric Attack</button>
        <button 
          class="cat-pill" 
          class:active={selectedCategory === 'cognitive'} 
          on:click={() => selectedCategory = 'cognitive'}
        >Cognitive Atrophy</button>
        <button 
          class="cat-pill" 
          class:active={selectedCategory === 'systemic'} 
          on:click={() => selectedCategory = 'systemic'}
        >Systemic Decoupling</button>
      </div>
    </div>

    <div class="all-grid">
      {#each filteredAll as sc}
        <div class="scenario-card">
          <div class="card-status-bar">
            <span class="sc-id">{sc.id}</span>
            <span class="severity-badge">{sc.severity}</span>
          </div>
          <h4 class="sc-name-small">{sc.name.split('(')[0].trim()}</h4>
          <p class="sc-mechanism-compact">{sc.mechanism}</p>
          <div class="precursors-row">
            {#each (sc.precursors || []) as p}
              <span class="pre-chip-small">{p}</span>
            {/each}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .scenarios-deck-container {
    padding: 3.5rem 0;
    border-top: 1px solid var(--border-subtle);
  }

  .deck-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
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

  .deck-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem 0;
  }

  .deck-desc {
    font-size: 1.05rem;
    color: var(--text-secondary);
    margin: 0;
  }

  .toggle-all-btn {
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    font-size: 0.875rem;
    font-weight: 600;
    border: 1px solid var(--border-medium);
    border-radius: 8px;
    padding: 0.75rem 1.25rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .toggle-all-btn:hover {
    background: var(--bg-surface-sunken);
    border-color: var(--accent-primary);
    transform: translateY(-1px);
  }

  .featured-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
  }

  .scenario-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s ease;
  }

  .scenario-card:hover {
    transform: translateY(-2px);
    border-color: var(--border-medium);
  }

  .card-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.85rem;
  }

  .scenario-id {
    font-family: var(--font-family-mono);
    font-size: 0.8rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .badge-cluster {
    display: flex;
    gap: 0.4rem;
  }

  .horizon-chip {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-muted);
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
  }

  .trajectory-chip {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--threat-critical);
    background: var(--threat-critical-bg);
    border: 1px solid var(--threat-critical-border);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
  }

  .scenario-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.5rem 0;
    line-height: 1.35;
  }

  .scenario-premise {
    font-size: 0.875rem;
    color: var(--text-secondary);
    line-height: 1.5;
    margin: 0 0 1rem 0;
    flex-grow: 1;
  }

  .card-footer {
    border-top: 1px solid var(--border-subtle);
    padding-top: 0.85rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .prob-label {
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .prob-val {
    font-family: var(--font-family-mono);
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--accent-primary);
  }

  .detail-link {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--accent-primary);
    text-decoration: none;
    transition: color 0.15s ease;
  }

  .detail-link:hover {
    color: var(--accent-primary-hover);
    text-decoration: underline;
  }

  /* Filter Panel & Search */
  .all-scenarios-panel {
    margin-top: 2.5rem;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.75rem;
  }

  .controls-bar {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
  }

  .search-input {
    flex: 1;
    min-width: 240px;
    padding: 0.65rem 1rem;
    border-radius: 8px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    font-size: 0.875rem;
  }

  .filter-pills {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .filter-pill {
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    color: var(--text-muted);
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.4rem 0.85rem;
    border-radius: 9999px;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .filter-pill.active {
    background: var(--accent-primary);
    color: #ffffff;
    border-color: var(--accent-primary);
  }

  .compact-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.15s ease;
  }

  .compact-card:hover {
    border-color: var(--border-strong);
  }

  .compact-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0.25rem 0;
  }

  .compact-desc {
    font-size: 0.825rem;
    color: var(--text-secondary);
    margin: 0;
  }
</style>