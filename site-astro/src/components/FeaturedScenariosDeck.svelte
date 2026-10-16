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
    border-top: 1px solid #e2e8f0;
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

  .deck-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem 0;
  }

  .deck-desc {
    font-size: 1.05rem;
    color: #475569;
    margin: 0;
  }

  .toggle-all-btn {
    background: #1e293b;
    color: #ffffff;
    font-size: 0.875rem;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.25rem;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.15s ease;
  }

  .toggle-all-btn:hover {
    background: #0f172a;
    transform: translateY(-1px);
  }

  .featured-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
  }

  .scenario-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }

  .scenario-card:hover {
    transform: translateY(-2px);
    border-color: #93c5fd;
  }

  .scenario-card.featured {
    border-top: 4px solid #2563eb;
  }

  .card-status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
  }

  .sc-id {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    color: #2563eb;
    background: #eff6ff;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
  }

  .severity-badge {
    font-size: 0.75rem;
    font-weight: 700;
    color: #b91c1c;
    background: #fef2f2;
    border: 1px solid #fecaca;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
  }

  .sc-name {
    font-size: 1.2rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 0.5rem 0;
  }

  .sc-name-small {
    font-size: 1rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 0.5rem 0;
  }

  .sc-question {
    font-size: 0.9rem;
    font-style: italic;
    color: #2563eb;
    margin: 0 0 0.75rem 0;
  }

  .sc-mechanism {
    font-size: 0.9rem;
    color: #475569;
    line-height: 1.5;
    margin: 0 0 1rem 0;
    flex-grow: 1;
  }

  .sc-mechanism-compact {
    font-size: 0.85rem;
    color: #475569;
    line-height: 1.4;
    margin: 0 0 0.75rem 0;
    flex-grow: 1;
  }

  .precursors-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    align-items: center;
    margin-bottom: 1rem;
  }

  .pre-label {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 600;
  }

  .pre-chip {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    color: #475569;
    background: #f1f5f9;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
  }

  .pre-chip-small {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    color: #475569;
    background: #f1f5f9;
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
  }

  .card-footer {
    border-top: 1px solid #f1f5f9;
    padding-top: 0.75rem;
    margin-top: auto;
  }

  .sc-link {
    font-size: 0.85rem;
    font-weight: 600;
    color: #2563eb;
    text-decoration: none;
  }

  .sc-link:hover {
    text-decoration: underline;
  }

  /* Filter toolbar */
  .filter-toolbar {
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .search-box input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 0.95rem;
  }

  .category-pills {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .cat-pill {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #e2e8f0;
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .cat-pill.active {
    background: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
  }

  .all-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.25rem;
  }

  @media (max-width: 640px) {
    .deck-title {
      font-size: 1.75rem;
    }
  }
</style>
