<script lang="ts">
  import asiData from '../data/asi_scenarios.json';

  let searchQuery = '';
  let selectedSeverity = 'All';
  let selectedCategory = 'All';
  let activeTab = 'scenarios'; // 'scenarios' | 'precursors' | 'matrix'
  let selectedScenario: any = null;

  const accentColorMap: Record<string, string> = {
    crimson: 'var(--threat-critical, #b91c1c)',
    amber: 'var(--threat-warning, #d97706)',
    indigo: 'var(--threat-telemetry, #4f46e5)',
    jade: 'var(--accent-primary, #1b6756)'
  };

  function cardTitle(sc: any): string {
    return sc.shortTitle ?? sc.name.replace(/\s*\(.*\)\s*$/, '').trim();
  }

  function cardTeaser(sc: any): string {
    return sc.teaser ?? sc.question;
  }

  function getSeverityTone(severityStr: string): string {
    const s = (severityStr || '').toLowerCase();
    if (s.includes('catastrophic') || s.includes('existential')) return 'crimson';
    if (s.includes('high') || s.includes('severe')) return 'amber';
    return 'indigo';
  }

  function getCardAccent(sc: any): string {
    if (sc.accentColor && accentColorMap[sc.accentColor]) {
      return accentColorMap[sc.accentColor];
    }
    const tone = getSeverityTone(sc.severity);
    return accentColorMap[tone] || 'var(--accent-primary, #1b6756)';
  }

  $: filteredScenarios = asiData.scenarios.filter((sc: any) => {
    const searchTarget = `${sc.name} ${sc.shortTitle ?? ''} ${sc.teaser ?? ''} ${sc.categoryTag ?? ''} ${sc.id} ${sc.mechanism} ${sc.failureMode}`.toLowerCase();
    const matchesSearch = !searchQuery || searchTarget.includes(searchQuery.toLowerCase());
    
    const tone = getSeverityTone(sc.severity);
    const matchesSeverity = selectedSeverity === 'All' || 
                            (selectedSeverity === 'Catastrophic' && tone === 'crimson') ||
                            (selectedSeverity === 'High' && tone === 'amber') ||
                            (selectedSeverity === 'Moderate' && tone === 'indigo');

    const matchesCategory = selectedCategory === 'All' || sc.categoryTag === selectedCategory;

    return matchesSearch && matchesSeverity && matchesCategory;
  });

  $: filteredPrecursors = asiData.precursors.filter((pr: any) => {
    const searchTarget = `${pr.id} ${pr.description} ${pr.currentEvidence}`.toLowerCase();
    return !searchQuery || searchTarget.includes(searchQuery.toLowerCase());
  });

  function selectScenario(sc: any) {
    selectedScenario = sc;
  }

  function closeModal() {
    selectedScenario = null;
  }

  function handleKeydown(event: KeyboardEvent, sc: any) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      selectScenario(sc);
    }
  }

  function handleModalKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      closeModal();
    }
  }
</script>

<svelte:window on:keydown={handleModalKeydown} />

<div class="asi-explorer-container">
  <!-- Navigation Header Tabs -->
  <nav class="explorer-nav" aria-label="Atlas Views">
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
  </nav>

  <!-- Search and Filter Bar -->
  <div class="filter-bar">
    <div class="search-input-wrapper">
      <svg class="search-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" aria-hidden="true">
        <circle cx="8.5" cy="8.5" r="5.5" stroke-width="1.75"/>
        <path d="M12.5 12.5L17 17" stroke-width="1.75" stroke-linecap="round"/>
      </svg>
      <input 
        type="text" 
        placeholder="Search 26 scenarios by name, mechanism, category, or failure mode..." 
        bind:value={searchQuery}
        class="search-input"
        aria-label="Search scenarios"
      />
      {#if searchQuery}
        <button class="clear-search-btn" on:click={() => searchQuery = ''} aria-label="Clear search">×</button>
      {/if}
    </div>

    {#if activeTab === 'scenarios'}
      <div class="filter-group">
        <label for="category-select" class="filter-label">Archetype:</label>
        <select id="category-select" bind:value={selectedCategory} class="filter-select">
          <option value="All">All Archetypes (6)</option>
          <option value="Instrumental Catastrophe">Instrumental Catastrophe</option>
          <option value="Strategic Deception">Strategic Deception</option>
          <option value="Epistemic Collapse">Epistemic Collapse</option>
          <option value="Economic Displacement">Economic Displacement</option>
          <option value="Systemic Disempowerment">Systemic Disempowerment</option>
          <option value="Governance & Coordination">Governance & Coordination</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="severity-select" class="filter-label">Severity:</label>
        <select id="severity-select" bind:value={selectedSeverity} class="filter-select">
          <option value="All">All Severities</option>
          <option value="Catastrophic">Catastrophic / Existential</option>
          <option value="High">High / Severe</option>
          <option value="Moderate">Moderate / Variable</option>
        </select>
      </div>
    {/if}
  </div>

  <!-- Tab 1: Scenarios Grid (Archetype 1: Speculative Field Guide) -->
  {#if activeTab === 'scenarios'}
    <div class="scenarios-count-bar">
      <span>Showing <strong>{filteredScenarios.length}</strong> of 26 transition pathways</span>
      {#if searchQuery || selectedCategory !== 'All' || selectedSeverity !== 'All'}
        <button class="reset-filter-link" on:click={() => { searchQuery = ''; selectedCategory = 'All'; selectedSeverity = 'All'; }}>
          Reset filters
        </button>
      {/if}
    </div>

    <div class="scenario-grid">
      {#each filteredScenarios as sc (sc.id)}
        <article 
          class="scenario-card"
          style="--card-accent: {getCardAccent(sc)}"
          on:click={() => selectScenario(sc)}
          on:keydown={(e) => handleKeydown(e, sc)}
          role="button"
          tabindex="0"
          aria-label="{cardTitle(sc)} — {sc.categoryTag ?? 'Transition Scenario'}"
        >
          <!-- 16:9 Dossier Plate -->
          <div class="card-plate">
            <!-- Strategy B: Precision Blueprint SVG Fallback (rendered behind or if image loading) -->
            <div class="blueprint-fallback" aria-hidden="true">
              <svg viewBox="0 0 300 169" class="blueprint-svg" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <pattern id="grid-{sc.id}" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill="var(--bg-surface-sunken)" />
                <rect width="100%" height="100%" fill="url(#grid-{sc.id})" />
                <!-- Orbital / Radar Geometrics -->
                <circle cx="150" cy="84.5" r="60" fill="none" stroke="currentColor" stroke-width="0.75" opacity="0.22" stroke-dasharray="3,3"/>
                <circle cx="150" cy="84.5" r="35" fill="none" stroke="currentColor" stroke-width="0.75" opacity="0.28"/>
                <circle cx="150" cy="84.5" r="5" fill="currentColor" opacity="0.4"/>
                <path d="M 150 14 L 150 155 M 35 84.5 L 265 84.5" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
                <!-- Schematic Glyph / Identifier text -->
                <text x="15" y="24" font-family="var(--font-family-mono)" font-size="9" font-weight="700" fill="currentColor" opacity="0.45" letter-spacing="1">{sc.id} · SPECULATIVE BLUEPRINT</text>
                <text x="15" y="150" font-family="var(--font-family-mono)" font-size="8" fill="currentColor" opacity="0.35">{sc.categoryTag ? sc.categoryTag.toUpperCase() : 'SCENARIO ARCHETYPE'}</text>
              </svg>
            </div>

            <!-- Strategy A: Editorial Linocut WebP Image -->
            {#if sc.previewImage}
              <img 
                src={sc.previewImage} 
                alt={cardTeaser(sc)}
                loading="lazy" 
                decoding="async"
                width="600"
                height="338"
                class="plate-img"
                on:load={(e) => {
                  const target = e.currentTarget;
                  if (target instanceof HTMLElement) {
                    target.classList.add('loaded');
                  }
                }}
                on:error={(e) => {
                  const target = e.currentTarget;
                  if (target instanceof HTMLElement) {
                    target.style.display = 'none';
                  }
                }}
              />
            {/if}

            <div class="plate-scrim"></div>

            <!-- Overlaid Badges -->
            <div class="plate-badges">
              <span class="badge-id-pill">
                {sc.id} · {sc.categoryTag ?? 'SCENARIO'}
              </span>
              <span class="badge-severity" data-tone={getSeverityTone(sc.severity)}>
                <span class="severity-dot"></span>
                {sc.severity ? sc.severity.split('/')[0].split('(')[0].trim() : 'Unrated'}
              </span>
            </div>
          </div>

          <!-- Card Content Body -->
          <div class="card-body">
            <h3 class="scenario-title">{cardTitle(sc)}</h3>
            <p class="scenario-teaser">{cardTeaser(sc)}</p>
          </div>

          <!-- Telemetry & Action Footer -->
          <div class="card-footer">
            <div class="telemetry-pill">
              <span class="telemetry-dot" style="background: var(--card-accent)"></span>
              <span class="telemetry-text">
                {sc.matrix?.speed_ratio ? sc.matrix.speed_ratio.split('(')[0].trim() : (sc.reversibility || 'Irreversible')}
              </span>
            </div>
            <span class="view-link">
              <span>Inspect Dossier</span>
              <svg class="arrow-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor">
                <path d="M3 8H13M9 4L13 8L9 12" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
          </div>
        </article>
      {/each}
    </div>
  {/if}

  <!-- Tab 2: Precursors Grid -->
  {#if activeTab === 'precursors'}
    <div class="precursors-list">
      {#each filteredPrecursors as pr (pr.id)}
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
            <div class="precursor-col">
              <strong>Current Empirical Evidence:</strong>
              <p>{pr.currentEvidence}</p>
            </div>
            <div class="precursor-col">
              <strong>Associated Scenarios:</strong>
              <div class="linked-scenarios">
                {#each pr.associatedScenarios as scId}
                  <span class="linked-badge">{scId}</span>
                {/each}
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Tab 3: Matrix Grid -->
  {#if activeTab === 'matrix'}
    <div class="matrix-overview">
      <div class="matrix-intro">
        <h3>The 7-Axis Takeoff Capability Matrix</h3>
        <p>Mathematical taxonomy formalizing the sovereign capability boundaries and speed differentials between biological human supervisors and artificial cognitive architectures.</p>
      </div>
      <div class="axes-grid">
        {#each asiData.capabilityAxes as axis (axis.id)}
          <div class="axis-card">
            <div class="axis-header">
              <span class="axis-id">{axis.id}</span>
              <h4 class="axis-title">{axis.name}</h4>
            </div>
            <p class="axis-desc">{axis.description}</p>
            <div class="levels-stack">
              {#each axis.levels as level}
                <div class="level-item">
                  <span class="level-step">L{level.step}:</span>
                  <span class="level-text">{level.label}</span>
                </div>
              {/each}
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Full Dossier Modal (Scholarly Rigor Preserved) -->
  {#if selectedScenario}
    <div class="modal-backdrop" on:click={closeModal} role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div class="modal-content" on:click|stopPropagation>
        <button class="modal-close-btn" on:click={closeModal} aria-label="Close dossier">&times;</button>
        
        <header class="modal-header">
          <div class="modal-meta-row">
            <span class="modal-badge">{selectedScenario.id}</span>
            <span class="modal-category-tag">{selectedScenario.categoryTag ?? 'Transition Pathway'}</span>
            <span class="modal-severity" data-tone={getSeverityTone(selectedScenario.severity)}>
              {selectedScenario.severity}
            </span>
          </div>
          
          <h2 id="modal-title">{cardTitle(selectedScenario)}</h2>
          <p class="modal-citation-name">{selectedScenario.name}</p>
          
          <div class="modal-teaser-callout">
            <p>{cardTeaser(selectedScenario)}</p>
          </div>
        </header>

        <div class="modal-body">
          <div class="modal-section">
            <h4>1. Core Analytical Mechanism</h4>
            <p>{selectedScenario.mechanism}</p>
          </div>

          <div class="modal-section">
            <h4>2. Predicted Failure Mode</h4>
            <p>{selectedScenario.failureMode}</p>
          </div>

          <div class="modal-section">
            <h4>3. Relevance to Sovereign Human Agency</h4>
            <p>{selectedScenario.relevance}</p>
          </div>

          <div class="modal-grid-row">
            <div class="modal-col">
              <h4>Reversibility</h4>
              <p class="meta-field">{selectedScenario.reversibility || 'Irreversible once unaligned dominance achieved'}</p>
            </div>
            <div class="modal-col">
              <h4>Empirical / Theoretical Status</h4>
              <p class="meta-field">{selectedScenario.status || 'Class C/E Theoretical Model'}</p>
            </div>
          </div>

          {#if selectedScenario.matrix}
            <div class="modal-section matrix-section">
              <h4>Capability Coordinates &amp; Asymmetry</h4>
              <ul class="matrix-list">
                {#each Object.entries(selectedScenario.matrix) as [k, v]}
                  <li>
                    <strong>{k.replace(/_/g, ' ')}:</strong>
                    <span>{v}</span>
                  </li>
                {/each}
              </ul>
            </div>
          {/if}

          {#if selectedScenario.precursors && selectedScenario.precursors.length > 0}
            <div class="modal-section">
              <h4>Observed Tripwires &amp; Precursors</h4>
              <div class="tripwire-tags">
                {#each selectedScenario.precursors as precId}
                  <span class="tripwire-pill">{precId}</span>
                {/each}
              </div>
            </div>
          {/if}
        </div>

        <footer class="modal-footer">
          <button class="btn-close-dossier" on:click={closeModal}>Return to Atlas</button>
        </footer>
      </div>
    </div>
  {/if}
</div>

<style>
  .asi-explorer-container {
    max-width: 1200px;
    margin: 0 auto;
    font-family: inherit;
  }

  /* Navigation Header Tabs */
  .explorer-nav {
    display: flex;
    gap: 0.75rem;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1.75rem;
    overflow-x: auto;
    padding-bottom: 0.25rem;
  }

  .tab-btn {
    background: none;
    border: none;
    padding: 0.75rem 1.25rem;
    font-family: var(--font-family-display, inherit);
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-secondary);
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    white-space: nowrap;
    border-radius: 4px 4px 0 0;
  }

  .tab-btn:hover {
    color: var(--text-primary);
    background: var(--bg-surface-sunken);
  }

  .tab-btn.active {
    color: var(--accent-primary);
    border-bottom-color: var(--accent-primary);
    background: var(--accent-primary-glow, rgba(27, 103, 86, 0.08));
  }

  /* Search & Filter Bar */
  .filter-bar {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1.25rem;
    flex-wrap: wrap;
    background: var(--bg-surface);
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
    box-shadow: var(--shadow-sm);
  }

  .search-input-wrapper {
    flex: 1;
    min-width: 280px;
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-icon {
    position: absolute;
    left: 0.85rem;
    width: 1.1rem;
    height: 1.1rem;
    color: var(--text-muted);
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    padding: 0.65rem 2.2rem 0.65rem 2.4rem;
    border: 1px solid var(--border-medium);
    border-radius: 8px;
    font-size: 0.92rem;
    background: var(--bg-surface-elevated, #ffffff);
    color: var(--text-primary);
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .search-input:focus {
    outline: none;
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-primary-glow);
  }

  .clear-search-btn {
    position: absolute;
    right: 0.75rem;
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 1.25rem;
    cursor: pointer;
    line-height: 1;
    padding: 0.2rem;
  }

  .filter-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .filter-label {
    font-family: var(--font-family-mono);
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .filter-select {
    padding: 0.6rem 1.8rem 0.6rem 0.85rem;
    border: 1px solid var(--border-medium);
    border-radius: 8px;
    background: var(--bg-surface-elevated, #ffffff);
    color: var(--text-primary);
    font-size: 0.88rem;
    font-weight: 500;
    cursor: pointer;
    transition: border-color 0.2s;
  }

  .filter-select:focus {
    outline: none;
    border-color: var(--accent-primary);
  }

  .scenarios-count-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 1.25rem;
    padding: 0 0.25rem;
  }

  .reset-filter-link {
    background: none;
    border: none;
    color: var(--accent-primary);
    text-decoration: underline;
    cursor: pointer;
    font-size: 0.82rem;
    font-weight: 600;
  }

  /* Scenario Grid & Archetype 1 Field Guide Card */
  .scenario-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
    align-items: stretch;
  }

  .scenario-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    position: relative;
    box-shadow: var(--shadow-sm);
    transition: transform 260ms cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 260ms cubic-bezier(0.16, 1, 0.3, 1), 
                border-color 260ms;
  }

  .scenario-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg, 0 16px 32px -8px rgba(0, 0, 0, 0.12));
    border-color: var(--border-medium);
  }

  .scenario-card:focus-visible {
    outline: 2px solid var(--accent-primary);
    outline-offset: 2px;
    box-shadow: 0 0 0 4px var(--accent-primary-glow);
  }

  /* 16:9 Dossier Plate */
  .card-plate {
    position: relative;
    aspect-ratio: 16 / 9;
    width: 100%;
    overflow: hidden;
    background: var(--bg-surface-sunken);
    border-bottom: 1px solid var(--border-subtle);
  }

  .blueprint-fallback {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
  }

  .blueprint-svg {
    width: 100%;
    height: 100%;
    display: block;
  }

  .plate-img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0;
    transition: opacity 350ms ease-in-out, transform 450ms cubic-bezier(0.16, 1, 0.3, 1);
  }

  .plate-img.loaded {
    opacity: 1;
  }

  .scenario-card:hover .plate-img {
    transform: scale(1.045);
  }

  .plate-scrim {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(14, 21, 30, 0.55) 0%, transparent 60%);
    pointer-events: none;
  }

  .plate-badges {
    position: absolute;
    top: 0.7rem;
    left: 0.7rem;
    right: 0.7rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    pointer-events: none;
    z-index: 2;
  }

  .badge-id-pill {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    background: var(--bg-glass, rgba(251, 247, 238, 0.92));
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    color: var(--text-primary);
    padding: 0.22rem 0.55rem;
    border-radius: 9999px;
    border: 1px solid var(--border-subtle);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
  }

  .badge-severity {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.22rem 0.55rem;
    border-radius: 9999px;
    background: var(--bg-surface-elevated, #ffffff);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
  }

  .severity-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
    display: inline-block;
  }

  .badge-severity[data-tone="crimson"] {
    color: var(--threat-critical, #b91c1c);
    background: var(--threat-critical-bg, #fee2e2);
    border-color: var(--threat-critical-border, #fca5a5);
  }

  .badge-severity[data-tone="amber"] {
    color: var(--threat-warning, #d97706);
    background: var(--threat-warning-bg, #fef3c7);
    border-color: var(--threat-warning-border, #fcd34d);
  }

  .badge-severity[data-tone="indigo"] {
    color: var(--threat-telemetry, #4f46e5);
    background: var(--threat-telemetry-bg, #e0e7ff);
    border-color: var(--threat-telemetry-border, #c7d2fe);
  }

  /* Card Body */
  .card-body {
    padding: 1.1rem 1.15rem 0.85rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
  }

  .scenario-title {
    font-family: var(--font-family-display);
    font-size: 1.12rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .scenario-teaser {
    font-family: var(--font-family-sans);
    font-size: 0.88rem;
    line-height: 1.5;
    color: var(--text-secondary);
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 2.65em;
  }

  /* Card Footer */
  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1.15rem;
    border-top: 1px solid var(--border-subtle);
    background: var(--bg-surface-sunken);
  }

  .telemetry-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
    font-weight: 600;
    letter-spacing: 0.02em;
    max-width: 60%;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .telemetry-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .view-link {
    font-family: var(--font-family-sans);
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--accent-primary);
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    transition: transform 180ms ease-out;
  }

  .arrow-icon {
    width: 14px;
    height: 14px;
    transition: transform 180ms ease-out;
  }

  .scenario-card:hover .arrow-icon {
    transform: translateX(4px);
  }

  /* Precursors & Matrix Views */
  .precursors-list {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .precursor-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.35rem;
    box-shadow: var(--shadow-sm);
  }

  .precursor-header {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    margin-bottom: 0.85rem;
    flex-wrap: wrap;
  }

  .precursor-id {
    font-family: var(--font-family-mono);
    font-weight: 700;
    background: var(--text-primary);
    color: var(--bg-surface);
    padding: 0.22rem 0.65rem;
    border-radius: 4px;
    font-size: 0.78rem;
  }

  .timing-badge {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
  }

  .timing-leading { background: #dcfce7; color: #166534; }
  .timing-coincident { background: #fef9c3; color: #854d0e; }
  .timing-lagging { background: #e0e7ff; color: #3730a3; }

  .observability-badge, .observable-today {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    background: var(--bg-surface-sunken);
    color: var(--text-secondary);
  }

  .observable-today.today-yes {
    background: var(--threat-critical-bg, #fee2e2);
    color: var(--threat-critical, #b91c1c);
    font-weight: 700;
  }

  .precursor-title {
    font-family: var(--font-family-display);
    font-size: 1.1rem;
    margin: 0 0 0.85rem 0;
    color: var(--text-primary);
    line-height: 1.35;
  }

  .precursor-body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .linked-scenarios {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    margin-top: 0.4rem;
  }

  .linked-badge {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    color: var(--accent-primary);
  }

  @media (max-width: 768px) {
    .precursor-body {
      grid-template-columns: 1fr;
    }
  }

  /* Matrix View */
  .matrix-intro {
    text-align: center;
    max-width: 760px;
    margin: 0 auto 2rem;
  }

  .matrix-intro h3 {
    font-family: var(--font-family-display);
    font-size: 1.5rem;
    color: var(--text-primary);
    margin: 0 0 0.5rem 0;
  }

  .matrix-intro p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
  }

  .axes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.25rem;
  }

  .axis-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: var(--shadow-sm);
  }

  .axis-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.5rem;
  }

  .axis-id {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 700;
    background: var(--accent-primary);
    color: white;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
  }

  .axis-title {
    font-family: var(--font-family-display);
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0;
    color: var(--text-primary);
  }

  .axis-desc {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.45;
    margin: 0 0 1rem 0;
  }

  .levels-stack {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .level-item {
    font-size: 0.82rem;
    padding: 0.4rem 0.6rem;
    border-radius: 6px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    display: flex;
    gap: 0.5rem;
  }

  .level-step {
    font-family: var(--font-family-mono);
    font-weight: 700;
    color: var(--accent-primary);
    flex-shrink: 0;
  }

  .level-text {
    color: var(--text-secondary);
  }

  /* Modal (Scholarly Dossier) */
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(14, 21, 30, 0.75);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
    padding: 1.25rem;
  }

  .modal-content {
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    max-width: 720px;
    width: 100%;
    max-height: 88vh;
    overflow-y: auto;
    padding: 2rem;
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
  }

  .modal-close-btn {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    border-radius: 50%;
    width: 34px;
    height: 34px;
    display: grid;
    place-items: center;
    font-size: 1.4rem;
    cursor: pointer;
    color: var(--text-secondary);
    line-height: 1;
    transition: all 0.15s;
  }

  .modal-close-btn:hover {
    color: var(--text-primary);
    background: var(--bg-surface-elevated);
    border-color: var(--border-medium);
  }

  .modal-header {
    margin-bottom: 1.5rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border-subtle);
  }

  .modal-meta-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 0.75rem;
  }

  .modal-badge {
    font-family: var(--font-family-mono);
    background: var(--text-primary);
    color: var(--bg-surface);
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
  }

  .modal-category-tag {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--accent-primary);
    background: var(--accent-primary-glow, rgba(27, 103, 86, 0.1));
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    border: 1px solid var(--border-subtle);
  }

  .modal-severity {
    font-family: var(--font-family-mono);
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
  }

  .modal-severity[data-tone="crimson"] {
    background: var(--threat-critical-bg, #fee2e2);
    color: var(--threat-critical, #b91c1c);
    border: 1px solid var(--threat-critical-border, #fca5a5);
  }

  .modal-severity[data-tone="amber"] {
    background: var(--threat-warning-bg, #fef3c7);
    color: var(--threat-warning, #d97706);
    border: 1px solid var(--threat-warning-border, #fcd34d);
  }

  .modal-severity[data-tone="indigo"] {
    background: var(--threat-telemetry-bg, #e0e7ff);
    color: var(--threat-telemetry, #4f46e5);
    border: 1px solid var(--threat-telemetry-border, #c7d2fe);
  }

  .modal-header h2 {
    font-family: var(--font-family-display);
    font-size: 1.65rem;
    margin: 0.35rem 0 0.25rem 0;
    color: var(--text-primary);
    line-height: 1.25;
  }

  .modal-citation-name {
    font-family: var(--font-family-mono);
    font-size: 0.8rem;
    color: var(--text-muted);
    margin: 0 0 1rem 0;
    line-height: 1.4;
  }

  .modal-teaser-callout {
    background: var(--bg-surface-sunken);
    border-left: 3px solid var(--accent-primary);
    padding: 0.85rem 1rem;
    border-radius: 0 8px 8px 0;
  }

  .modal-teaser-callout p {
    font-family: var(--font-family-sans);
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--text-primary);
    margin: 0;
    font-weight: 500;
  }

  .modal-section {
    margin-bottom: 1.5rem;
  }

  .modal-section h4 {
    font-family: var(--font-family-display);
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.45rem 0;
  }

  .modal-section p {
    font-size: 0.92rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin: 0;
  }

  .modal-grid-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: var(--bg-surface-sunken);
    border-radius: 8px;
    border: 1px solid var(--border-subtle);
  }

  .modal-col h4 {
    font-family: var(--font-family-mono);
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    margin: 0 0 0.35rem 0;
  }

  .meta-field {
    font-size: 0.88rem;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.45;
  }

  .matrix-section {
    background: var(--bg-surface-sunken);
    padding: 1.15rem;
    border-radius: 10px;
    border: 1px solid var(--border-subtle);
  }

  .matrix-list {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 0.88rem;
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
  }

  .matrix-list li {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 0.75rem;
    color: var(--text-secondary);
    line-height: 1.4;
  }

  .matrix-list li strong {
    font-family: var(--font-family-mono);
    font-size: 0.78rem;
    color: var(--text-primary);
    text-transform: capitalize;
  }

  @media (max-width: 600px) {
    .matrix-list li {
      grid-template-columns: 1fr;
      gap: 0.2rem;
    }
  }

  .tripwire-tags {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .tripwire-pill {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    color: var(--threat-critical, #b91c1c);
  }

  .modal-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: 1.5rem;
    padding-top: 1.25rem;
    border-top: 1px solid var(--border-subtle);
  }

  .btn-close-dossier {
    background: var(--accent-primary);
    color: white;
    border: none;
    padding: 0.65rem 1.4rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    transition: opacity 0.2s;
  }

  .btn-close-dossier:hover {
    opacity: 0.92;
  }

  /* Responsive Adjustments */
  @media (max-width: 768px) {
    .modal-content {
      padding: 1.35rem;
    }

    .modal-grid-row {
      grid-template-columns: 1fr;
      gap: 0.75rem;
    }

    .scenario-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
