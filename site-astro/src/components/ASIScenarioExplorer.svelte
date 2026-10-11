<script lang="ts">
  import { onMount } from 'svelte';
  import asiData from '../data/asi_scenarios.json';

  let searchQuery = '';
  let selectedSeverity = 'All';
  let activeTab = 'scenarios'; // 'scenarios' | 'precursors' | 'matrix'
  let selectedScenario: any = null;

  $: filteredScenarios = asiData.scenarios.filter((sc: any) => {
    const matchesSearch = sc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          sc.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          sc.mechanism.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          sc.failureMode.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSeverity = selectedSeverity === 'All' || 
                            (selectedSeverity === 'Catastrophic' && sc.severity.toLowerCase().includes('catastrophic')) ||
                            (selectedSeverity === 'High' && sc.severity.toLowerCase().includes('high'));
    return matchesSearch && matchesSeverity;
  });

  $: filteredPrecursors = asiData.precursors.filter((pr: any) => {
    return pr.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
           pr.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
           pr.currentEvidence.toLowerCase().includes(searchQuery.toLowerCase());
  });

  function selectScenario(sc: any) {
    selectedScenario = sc;
  }

  function closeModal() {
    selectedScenario = null;
  }
</script>

<div class="asi-explorer-container">
  <!-- Navigation Header Tabs -->
  <div class="explorer-nav">
    <button 
      class="tab-btn" 
      class:active={activeTab === 'scenarios'} 
      on:click={() => activeTab = 'scenarios'}
    >
      Transition Scenarios (26)
    </button>
    <button 
      class="tab-btn" 
      class:active={activeTab === 'precursors'} 
      on:click={() => activeTab = 'precursors'}
    >
      Observable Precursors (14)
    </button>
    <button 
      class="tab-btn" 
      class:active={activeTab === 'matrix'} 
      on:click={() => activeTab = 'matrix'}
    >
      7-Axis Capability Matrix
    </button>
  </div>

  <!-- Search and Filter Bar -->
  <div class="filter-bar">
    <div class="search-input-wrapper">
      <input 
        type="text" 
        placeholder="Search by scenario, failure mode, or mechanism..." 
        bind:value={searchQuery}
        class="search-input"
      />
    </div>
    {#if activeTab === 'scenarios'}
      <div class="severity-filters">
        <label for="severity-select" class="filter-label">Severity:</label>
        <select id="severity-select" bind:value={selectedSeverity} class="filter-select">
          <option value="All">All Severities</option>
          <option value="Catastrophic">Catastrophic / Existential</option>
          <option value="High">High Severity</option>
        </select>
      </div>
    {/if}
  </div>

  <!-- Tab 1: Scenarios Grid -->
  {#if activeTab === 'scenarios'}
    <div class="scenario-grid">
      {#each filteredScenarios as sc}
        <div class="scenario-card" on:click={() => selectScenario(sc)} role="button" tabindex="0">
          <div class="card-header">
            <span class="scenario-badge">{sc.id}</span>
            <span class="severity-badge" class:catastrophic={sc.severity.toLowerCase().includes('catastrophic')}>
              {sc.severity}
            </span>
          </div>
          <h3 class="scenario-title">{sc.name}</h3>
          <p class="scenario-question">{sc.question}</p>
          <div class="card-footer">
            <span class="card-status">{sc.status}</span>
            <span class="view-link">Explore Details &rarr;</span>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Tab 2: Precursors Grid -->
  {#if activeTab === 'precursors'}
    <div class="precursors-list">
      {#each filteredPrecursors as pr}
        <div class="precursor-card">
          <div class="precursor-header">
            <span class="precursor-id">{pr.id}</span>
            <span class="timing-badge timing-{pr.timing}">{pr.timing.toUpperCase()}</span>
            <span class="observability-badge">Observability: {pr.observability}</span>
            <span class="observable-today" class:today-yes={pr.observableToday === 'yes'}>
              Today: {pr.observableToday.toUpperCase()}
            </span>
          </div>
          <h4 class="precursor-title">{pr.description}</h4>
          <div class="precursor-body">
            <div class="evidence-block">
              <strong>Current Empirical Evidence:</strong>
              <p>{pr.currentEvidence}</p>
            </div>
            <div class="implication-block">
              <strong>HSRI Construct Implication:</strong>
              <p>{pr.hsriImplication}</p>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Tab 3: 7-Axis Matrix -->
  {#if activeTab === 'matrix'}
    <div class="matrix-container">
      <div class="matrix-intro">
        <h3>The 7-Axis Multi-Dimensional Transition Matrix</h3>
        <p>
          HSRI rejects linear timeline projections or subjective probability distributions. Instead, transition trajectories
          are classified across seven structural dimensions governing capability asymmetry, autonomous operational scope,
          and human reaction horizons.
        </p>
      </div>
      <div class="axes-grid">
        {#each asiData.capabilityAxes as ax}
          <div class="axis-card">
            <h4 class="axis-title">{ax.axis}</h4>
            <div class="axis-levels">
              {#each ax.levels as lvl, idx}
                <div class="level-item level-{idx}">
                  <span class="level-step">Tier {idx + 1}:</span>
                  <span class="level-name">{lvl}</span>
                </div>
              {/each}
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Scenario Detail Modal -->
  {#if selectedScenario}
    <div class="modal-backdrop" on:click={closeModal}>
      <div class="modal-content" on:click|stopPropagation>
        <button class="modal-close-btn" on:click={closeModal}>&times;</button>
        <div class="modal-header">
          <span class="modal-badge">{selectedScenario.id}</span>
          <h2>{selectedScenario.name}</h2>
          <span class="modal-severity">{selectedScenario.severity}</span>
        </div>
        <div class="modal-body">
          <div class="modal-section">
            <h4>Core Analytical Mechanism</h4>
            <p>{selectedScenario.mechanism}</p>
          </div>
          <div class="modal-section">
            <h4>Predicted Failure Mode</h4>
            <p>{selectedScenario.failureMode}</p>
          </div>
          <div class="modal-section">
            <h4>Relevance to Sovereign Human Agency</h4>
            <p>{selectedScenario.relevance}</p>
          </div>
          {#if selectedScenario.matrix}
            <div class="modal-section">
              <h4>Capability Coordinates</h4>
              <ul class="matrix-list">
                {#each Object.entries(selectedScenario.matrix) as [k, v]}
                  <li><strong>{k.replace('_', ' ')}:</strong> {v}</li>
                {/each}
              </ul>
            </div>
          {/if}
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .asi-explorer-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
    font-family: inherit;
  }

  .explorer-nav {
    display: flex;
    gap: 1rem;
    border-bottom: 2px solid var(--border-color, #e2e8f0);
    margin-bottom: 1.5rem;
  }

  .tab-btn {
    background: none;
    border: none;
    padding: 0.75rem 1.25rem;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-secondary, #64748b);
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.2s;
  }

  .tab-btn:hover {
    color: var(--primary-color, #0f172a);
  }

  .tab-btn.active {
    color: var(--primary-color, #0f172a);
    border-bottom-color: #3b82f6;
  }

  .filter-bar {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
  }

  .search-input-wrapper {
    flex: 1;
    min-width: 280px;
  }

  .search-input {
    width: 100%;
    padding: 0.65rem 1rem;
    border: 1px solid var(--border-color, #cbd5e1);
    border-radius: 8px;
    font-size: 0.95rem;
  }

  .severity-filters {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .filter-label {
    font-size: 0.9rem;
    font-weight: 500;
  }

  .filter-select {
    padding: 0.65rem 1rem;
    border: 1px solid var(--border-color, #cbd5e1);
    border-radius: 8px;
    background: white;
  }

  .scenario-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 1.25rem;
  }

  .scenario-card {
    background: white;
    border: 1px solid var(--border-color, #e2e8f0);
    border-radius: 10px;
    padding: 1.25rem;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .scenario-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .scenario-badge {
    background: #0f172a;
    color: white;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
  }

  .severity-badge {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    background: #f1f5f9;
    color: #475569;
  }

  .severity-badge.catastrophic {
    background: #fee2e2;
    color: #b91c1c;
  }

  .scenario-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0.25rem 0 0.5rem 0;
    color: #0f172a;
  }

  .scenario-question {
    font-size: 0.85rem;
    color: #475569;
    line-height: 1.4;
    margin-bottom: 1rem;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #f1f5f9;
    padding-top: 0.75rem;
    font-size: 0.8rem;
  }

  .card-status {
    color: #64748b;
  }

  .view-link {
    color: #2563eb;
    font-weight: 600;
  }

  /* Precursors */
  .precursors-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .precursor-card {
    background: white;
    border: 1px solid var(--border-color, #e2e8f0);
    border-radius: 8px;
    padding: 1.25rem;
  }

  .precursor-header {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
  }

  .precursor-id {
    font-weight: 700;
    background: #1e293b;
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
  }

  .timing-badge {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
  }

  .timing-leading { background: #dcfce7; color: #166534; }
  .timing-coincident { background: #fef9c3; color: #854d0e; }
  .timing-lagging { background: #e0e7ff; color: #3730a3; }

  .observability-badge {
    font-size: 0.75rem;
    background: #f1f5f9;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    color: #334155;
  }

  .observable-today {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    background: #f1f5f9;
    color: #64748b;
  }

  .observable-today.today-yes {
    background: #fee2e2;
    color: #991b1b;
  }

  .precursor-title {
    font-size: 1.05rem;
    margin: 0 0 0.75rem 0;
    color: #0f172a;
  }

  .precursor-body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    font-size: 0.85rem;
    color: #334155;
  }

  @media (max-width: 768px) {
    .precursor-body {
      grid-template-columns: 1fr;
    }
  }

  /* Matrix */
  .axes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }

  .axis-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1rem;
  }

  .axis-title {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 0.75rem 0;
    color: #1e293b;
  }

  .level-item {
    font-size: 0.85rem;
    padding: 0.35rem 0.5rem;
    margin-bottom: 0.35rem;
    border-radius: 4px;
    background: #f8fafc;
  }

  .level-step {
    font-weight: 600;
    color: #64748b;
    margin-right: 0.35rem;
  }

  /* Modal */
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
  }

  .modal-content {
    background: white;
    border-radius: 12px;
    max-width: 650px;
    width: 100%;
    max-height: 85vh;
    overflow-y: auto;
    padding: 1.75rem;
    position: relative;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  }

  .modal-close-btn {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #64748b;
  }

  .modal-header {
    margin-bottom: 1.25rem;
  }

  .modal-badge {
    background: #0f172a;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 700;
  }

  .modal-header h2 {
    font-size: 1.35rem;
    margin: 0.5rem 0;
    color: #0f172a;
  }

  .modal-severity {
    display: inline-block;
    background: #fee2e2;
    color: #991b1b;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
  }

  .modal-section {
    margin-bottom: 1.25rem;
  }

  .modal-section h4 {
    font-size: 0.95rem;
    font-weight: 600;
    color: #334155;
    margin: 0 0 0.35rem 0;
  }

  .modal-section p {
    font-size: 0.9rem;
    line-height: 1.5;
    color: #475569;
    margin: 0;
  }

  .matrix-list {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 0.85rem;
    color: #475569;
  }

  .matrix-list li {
    padding: 0.25rem 0;
    text-transform: capitalize;
  }
</style>
