<script lang="ts">
  import countryScoresData from '../data/country_scores.json';

  export let countries = countryScoresData.countries;

  // Aggregation Mode State
  let aggregationMode: 'linear' | 'geometric' | 'leontief' | 'choquet' = 'linear';
  let showTrapsOnly = false;
  let selectedFragilityTier = '';

  // Standard filters
  let searchTerm = '';
  let selectedRegion = '';
  let selectedBand = '';
  let sortBy = 'rank';

  // Helper functions for active model metrics
  function getActiveScore(country: any, mode: string): number {
    if (!country.variants) return country.score;
    switch (mode) {
      case 'geometric': return country.variants.hsri_geometric;
      case 'leontief': return country.variants.hsri_leontief;
      case 'choquet': return country.variants.hsri_choquet;
      default: return country.variants.hsri_linear || country.score;
    }
  }

  function getActiveRank(country: any, mode: string): number {
    if (!country.variants) return country.rank;
    switch (mode) {
      case 'geometric': return country.variants.rank_geometric;
      case 'leontief': return country.variants.rank_leontief;
      case 'choquet': return country.variants.rank_choquet;
      default: return country.variants.rank_linear || country.rank;
    }
  }

  function getRankDelta(country: any, mode: string): number {
    if (!country.variants) return 0;
    switch (mode) {
      case 'geometric': return country.variants.rank_delta_geo;
      case 'leontief': return country.variants.rank_delta_leo;
      case 'choquet': return country.variants.rank_delta_choq;
      default: return 0;
    }
  }

  // Filtered and sorted countries
  $: filteredCountries = countries.filter(country => {
    const matchesSearch = country.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         country.code.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRegion = !selectedRegion || country.region === selectedRegion;
    const matchesBand = !selectedBand || country.band === selectedBand;
    const matchesTrap = !showTrapsOnly || (country.variants && country.variants.high_compute_trap);
    const matchesFragility = !selectedFragilityTier || (country.variants && country.variants.fragility_tier === selectedFragilityTier);
    return matchesSearch && matchesRegion && matchesBand && matchesTrap && matchesFragility;
  });

  $: sortedCountries = [...filteredCountries].sort((a, b) => {
    switch (sortBy) {
      case 'name':
        return a.name.localeCompare(b.name);
      case 'score':
        return getActiveScore(b, aggregationMode) - getActiveScore(a, aggregationMode);
      case 'score-low':
        return getActiveScore(a, aggregationMode) - getActiveScore(b, aggregationMode);
      case 'exposure':
        return b.exposure - a.exposure;
      case 'vulnerability':
        return (b.variants?.vulnerability_index || 0) - (a.variants?.vulnerability_index || 0);
      case 'delta-drop':
        return getRankDelta(b, aggregationMode) - getRankDelta(a, aggregationMode);
      default: // rank
        return getActiveRank(a, aggregationMode) - getActiveRank(b, aggregationMode);
    }
  });

  // Get band color
  function getBandColor(band: string) {
    const colors: Record<string, string> = {
      'A': '#10b981',
      'B': '#3b82f6',
      'C': '#f59e0b',
      'D': '#ef4444',
      'F': '#991b1b'
    };
    return colors[band] || '#6b7280';
  }

  const base = (import.meta.env.BASE_URL || '').replace(/\/$/, '');
</script>

<div class="country-list-container">
  <!-- Aggregation Model Toggle Banner (Study 2) -->
  <div class="aggregation-mode-bar">
    <div class="mode-header">
      <div class="mode-badge-wrap">
        <span class="mode-badge">STUDY 2 EVALUATION RATIFIED</span>
        <span class="mode-title">Econometric Aggregation Model</span>
      </div>
      <p class="mode-description">
        Compensatory linear averaging allows world-class digital infrastructure to mask critical discernment and governance deficits.
        Toggle non-compensatory models to inspect institutional weakest-link bottlenecks.
      </p>
    </div>

    <div class="mode-buttons-group">
      <button
        class="mode-btn {aggregationMode === 'linear' ? 'active' : ''}"
        on:click={() => aggregationMode = 'linear'}
      >
        <span class="btn-name">Linear (Compensatory)</span>
        <span class="btn-sub">HSRI Baseline ($0.25 \times 4$)</span>
      </button>

      <button
        class="mode-btn {aggregationMode === 'geometric' ? 'active' : ''}"
        on:click={() => aggregationMode = 'geometric'}
      >
        <span class="btn-name">Geometric Mean</span>
        <span class="btn-sub">AM-GM Discounting ($\epsilon=0.01$)</span>
      </button>

      <button
        class="mode-btn {aggregationMode === 'leontief' ? 'active' : ''}"
        on:click={() => aggregationMode = 'leontief'}
      >
        <span class="btn-name">Leontief Floor (Weakest-Link)</span>
        <span class="btn-sub">Critical Bottleneck ($\beta=0.5$)</span>
      </button>

      <button
        class="mode-btn {aggregationMode === 'choquet' ? 'active' : ''}"
        on:click={() => aggregationMode = 'choquet'}
      >
        <span class="btn-name">Choquet Integral</span>
        <span class="btn-sub">Infra-Discernment 2-Additive Synergy</span>
      </button>
    </div>

    {#if aggregationMode !== 'linear'}
      <div class="mode-active-alert">
        <strong>Active Non-Compensatory Model:</strong>
        {#if aggregationMode === 'leontief'}
          <span>Leontief Floor penalizes countries whose weakest pillar collapses below system baseline. Countries with balanced capacity (e.g. Germany, Austria) rise in rank, while unbalanced nations (e.g. Hong Kong, USA, UK) drop.</span>
        {:else if aggregationMode === 'geometric'}
          <span>Geometric mean strictly enforces the AM-GM inequality, penalizing uneven investments across the four pillars.</span>
        {:else}
          <span>Choquet 2-additive capacity penalizes uncoordinated digital infrastructure built without concurrent cognitive discernment defenses.</span>
        {/if}
      </div>
    {/if}
  </div>

  <!-- Interactive Filters Bar -->
  <div class="list-filters-bar">
    <div class="search-box">
      <input
        type="text"
        placeholder="Search countries by name or ISO code..."
        bind:value={searchTerm}
        class="search-input"
      />
    </div>

    <div class="filter-dropdowns">
      <select bind:value={selectedRegion} class="filter-select">
        <option value="">All Regions</option>
        <option value="europe">Europe</option>
        <option value="north-america">North America</option>
        <option value="asia">Asia</option>
        <option value="oceania">Oceania</option>
      </select>

      <select bind:value={selectedBand} class="filter-select">
        <option value="">All Bands</option>
        <option value="A">Band A (80-100)</option>
        <option value="B">Band B (70-79)</option>
        <option value="C">Band C (60-69)</option>
        <option value="D">Band D (50-59)</option>
        <option value="F">Band F (&lt;50)</option>
      </select>

      <select bind:value={selectedFragilityTier} class="filter-select">
        <option value="">All Fragility Tiers</option>
        <option value="Low">Resilience: Low Fragility</option>
        <option value="Moderate">Resilience: Moderate</option>
        <option value="High">Resilience: High Fragility</option>
        <option value="Critical">Resilience: Critical Bottleneck</option>
      </select>

      <select bind:value={sortBy} class="filter-select">
        <option value="rank">Sort: By Active Rank</option>
        <option value="score">Sort: Active Score (High-Low)</option>
        <option value="score-low">Sort: Active Score (Low-High)</option>
        <option value="vulnerability">Sort: By Vulnerability Index</option>
        <option value="delta-drop">Sort: By Rank Drop (Worst)</option>
        <option value="exposure">Sort: By Macro Exposure</option>
        <option value="name">Sort: Name (A-Z)</option>
      </select>
    </div>

    <div class="trap-toggle-box">
      <label class="trap-checkbox-label">
        <input type="checkbox" bind:checked={showTrapsOnly} />
        <span class="trap-label-text">⚠️ High-Compute Traps Only</span>
      </label>
    </div>
  </div>

  <!-- Summary Stats Bar -->
  <div class="country-stats">
    <div class="stat-item">
      <div class="stat-number">{sortedCountries.length}</div>
      <div class="stat-label">Filtered Nations</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">
        {sortedCountries.length > 0 ? (sortedCountries.reduce((sum, c) => sum + getActiveScore(c, aggregationMode), 0) / sortedCountries.length).toFixed(1) : '0.0'}
      </div>
      <div class="stat-label">Avg Active Score</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">
        {sortedCountries.filter(c => c.variants?.high_compute_trap).length}
      </div>
      <div class="stat-label">High-Compute Traps Flagged</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">
        {sortedCountries.filter(c => (c.variants?.vulnerability_index || 0) >= 0.02).length}
      </div>
      <div class="stat-label">High/Critical Fragility</div>
    </div>
  </div>

  <!-- Cards Grid -->
  <div class="countries-grid">
    {#each sortedCountries as country}
      {@const activeRank = getActiveRank(country, aggregationMode)}
      {@const activeScore = getActiveScore(country, aggregationMode)}
      {@const rankDelta = getRankDelta(country, aggregationMode)}
      <a href={`${base}/countries/${country.id.toLowerCase()}/`} class="country-card {country.variants?.high_compute_trap ? 'trap-border' : ''}">
        <div class="card-header">
          <div class="country-info">
            <div class="rank-container">
              <span class="rank-badge">#{activeRank}</span>
              {#if aggregationMode !== 'linear' && rankDelta !== 0}
                <span class="delta-badge {rankDelta > 0 ? 'delta-down' : 'delta-up'}">
                  {rankDelta > 0 ? `▼ -${rankDelta}` : `▲ +${Math.abs(rankDelta)}`}
                </span>
              {/if}
            </div>
            <div class="name-group">
              <h3>{country.name}</h3>
              <span class="country-code">{country.code}</span>
              {#if country.variants?.high_compute_trap}
                <span class="trap-badge-card" title="High digital infrastructure masks acute human or governance deficits">
                  ⚠️ Trap
                </span>
              {/if}
            </div>
          </div>
          <div class="country-score">
            <div class="score-value" style="background-color: {getBandColor(country.band)}">
              {activeScore.toFixed(1)}
            </div>
            <span class="score-band" style="background-color: {getBandColor(country.band)}">
              Band {country.band}
            </span>
          </div>
        </div>

        <!-- Vulnerability & Bottleneck Row -->
        {#if country.variants}
          <div class="bottleneck-row">
            <span class="bottleneck-tag">
              Bottleneck: <strong>{country.variants.bottleneck_pillar}</strong>
            </span>
            <span class="fragility-tag tier-{country.variants.fragility_tier.toLowerCase()}">
              Vn: {country.variants.vulnerability_index.toFixed(3)} ({country.variants.fragility_tier})
            </span>
          </div>
        {/if}

        <div class="country-metrics">
          <div class="metric-bar">
            <div class="bar-labels">
              <span class="metric-label">AI Literacy</span>
              <span class="metric-value">{country.pillars.ai_literacy}%</span>
            </div>
            <div class="bar-container">
              <div class="bar-fill" style="width: {country.pillars.ai_literacy}%; background-color: #3b82f6"></div>
            </div>
          </div>

          <div class="metric-bar">
            <div class="bar-labels">
              <span class="metric-label">Critical Discernment</span>
              <span class="metric-value">{country.pillars.critical_discernment}%</span>
            </div>
            <div class="bar-container">
              <div class="bar-fill" style="width: {country.pillars.critical_discernment}%; background-color: #8b5cf6"></div>
            </div>
          </div>

          <div class="metric-bar">
            <div class="bar-labels">
              <span class="metric-label">Institutional Governance</span>
              <span class="metric-value">{country.pillars.institutional_governance}%</span>
            </div>
            <div class="bar-container">
              <div class="bar-fill" style="width: {country.pillars.institutional_governance}%; background-color: #10b981"></div>
            </div>
          </div>

          <div class="metric-bar">
            <div class="bar-labels">
              <span class="metric-label">Digital Infrastructure</span>
              <span class="metric-value">{country.pillars.digital_infrastructure}%</span>
            </div>
            <div class="bar-container">
              <div class="bar-fill" style="width: {country.pillars.digital_infrastructure}%; background-color: #f59e0b"></div>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <div class="country-exposure">
            <span class="exposure-label">Macro Exposure:</span>
            <div class="exposure-bar">
              <div class="exposure-fill" style="width: {country.exposure}%"></div>
            </div>
            <span class="exposure-value">{country.exposure}%</span>
          </div>
          <span class="view-profile-cta">View Profile &rarr;</span>
        </div>
      </a>
    {/each}
  </div>

  {#if sortedCountries.length === 0}
    <div class="no-results">
      <p>No countries match your current filter parameters.</p>
      <button class="reset-filters-btn" on:click={() => { searchTerm = ''; selectedRegion = ''; selectedBand = ''; showTrapsOnly = false; selectedFragilityTier = ''; }}>
        Reset Filters
      </button>
    </div>
  {/if}
</div>

<style>
  .country-list-container {
    max-width: 1300px;
    margin: 0 auto;
  }

  /* Aggregation Toggle Bar */
  .aggregation-mode-bar {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 0.75rem;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
  }

  .mode-header {
    margin-bottom: 1.25rem;
  }

  .mode-badge-wrap {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.4rem;
  }

  .mode-badge {
    background: #0f172a;
    color: #38bdf8;
    font-size: 0.7rem;
    font-weight: 800;
    padding: 0.2rem 0.5rem;
    border-radius: 0.25rem;
    letter-spacing: 0.05em;
  }

  .mode-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #0f172a;
  }

  .mode-description {
    font-size: 0.85rem;
    color: #475569;
    margin: 0;
    line-height: 1.45;
  }

  .mode-buttons-group {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.75rem;
  }

  .mode-btn {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 0.5rem;
    padding: 0.75rem 1rem;
    text-align: left;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    flex-direction: column;
  }

  .mode-btn:hover {
    background: #f1f5f9;
    border-color: #94a3b8;
  }

  .mode-btn.active {
    background: #0f172a;
    border-color: #0f172a;
    color: #ffffff;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15);
  }

  .btn-name {
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
  }

  .mode-btn.active .btn-name {
    color: #38bdf8;
  }

  .btn-sub {
    font-size: 0.72rem;
    color: #64748b;
  }

  .mode-btn.active .btn-sub {
    color: #cbd5e1;
  }

  .mode-active-alert {
    margin-top: 1rem;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 0.5rem;
    padding: 0.75rem 1rem;
    font-size: 0.82rem;
    color: #166534;
    line-height: 1.4;
  }

  .mode-active-alert strong {
    color: #14532d;
    margin-right: 0.35rem;
  }

  /* Filters Bar */
  .list-filters-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    background: #ffffff;
    padding: 1.25rem;
    border-radius: 0.75rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    border: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
  }

  .search-box {
    flex: 1;
    min-width: 240px;
  }

  .search-input {
    width: 100%;
    padding: 0.65rem 1rem;
    border: 1px solid #cbd5e1;
    border-radius: 0.5rem;
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.15s;
  }

  .search-input:focus {
    border-color: #2563eb;
  }

  .filter-dropdowns {
    display: flex;
    gap: 0.65rem;
    flex-wrap: wrap;
  }

  .filter-select {
    padding: 0.6rem 0.85rem;
    border: 1px solid #cbd5e1;
    border-radius: 0.5rem;
    font-size: 0.82rem;
    background: white;
    color: #334155;
    cursor: pointer;
  }

  .trap-toggle-box {
    display: flex;
    align-items: center;
  }

  .trap-checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    font-size: 0.82rem;
    font-weight: 700;
    color: #b45309;
    background: #fef3c7;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    border: 1px solid #fde68a;
  }

  /* Country Stats */
  .country-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .stat-item {
    background: #ffffff;
    padding: 1.25rem;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  }

  .stat-number {
    font-size: 1.75rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1;
    margin-bottom: 0.35rem;
  }

  .stat-label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
  }

  /* Grid & Cards */
  .countries-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 1.5rem;
  }

  .country-card {
    background: #ffffff;
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    border: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    text-decoration: none;
    color: inherit;
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
  }

  .country-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.1);
    border-color: #93c5fd;
  }

  .country-card.trap-border {
    border-left: 4px solid #f59e0b;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.85rem;
  }

  .country-info {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .rank-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
  }

  .rank-badge {
    font-size: 0.85rem;
    font-weight: 800;
    color: #64748b;
    background: #f1f5f9;
    padding: 0.25rem 0.5rem;
    border-radius: 0.35rem;
  }

  .delta-badge {
    font-size: 0.65rem;
    font-weight: 800;
    padding: 0.1rem 0.35rem;
    border-radius: 0.25rem;
    line-height: 1.2;
  }

  .delta-down {
    background: #fee2e2;
    color: #b91c1c;
  }

  .delta-up {
    background: #dcfce7;
    color: #15803d;
  }

  .name-group h3 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 0.15rem 0;
  }

  .country-code {
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748b;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 0.1rem 0.35rem;
    border-radius: 0.25rem;
  }

  .trap-badge-card {
    font-size: 0.65rem;
    font-weight: 800;
    color: #b45309;
    background: #fef3c7;
    border: 1px solid #fde68a;
    padding: 0.1rem 0.4rem;
    border-radius: 0.25rem;
    margin-left: 0.35rem;
  }

  .country-score {
    text-align: right;
  }

  .score-value {
    color: white;
    font-weight: 800;
    font-size: 1.15rem;
    padding: 0.2rem 0.6rem;
    border-radius: 0.35rem;
    margin-bottom: 0.25rem;
    display: inline-block;
  }

  .score-band {
    display: block;
    font-size: 0.7rem;
    font-weight: 700;
    color: white;
    padding: 0.1rem 0.4rem;
    border-radius: 0.25rem;
    text-align: center;
  }

  .bottleneck-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.35rem;
    padding: 0.35rem 0.65rem;
    margin-bottom: 1rem;
    font-size: 0.72rem;
  }

  .bottleneck-tag {
    color: #475569;
  }

  .fragility-tag {
    font-weight: 700;
    padding: 0.05rem 0.35rem;
    border-radius: 0.2rem;
  }

  .tier-critical { background: #fee2e2; color: #991b1b; }
  .tier-high { background: #fed7aa; color: #9a3412; }
  .tier-moderate { background: #fef08a; color: #854d0e; }
  .tier-low { background: #dcfce7; color: #166534; }

  /* Metric Bars */
  .country-metrics {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    margin-bottom: 1.25rem;
  }

  .metric-bar {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .bar-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
  }

  .metric-label {
    color: #64748b;
  }

  .metric-value {
    font-weight: 600;
    color: #1e293b;
  }

  .bar-container {
    height: 6px;
    background: #e2e8f0;
    border-radius: 3px;
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    border-radius: 3px;
  }

  /* Card Footer */
  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #f1f5f9;
    padding-top: 0.85rem;
    margin-top: auto;
  }

  .country-exposure {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
  }

  .exposure-label {
    color: #64748b;
  }

  .exposure-bar {
    width: 50px;
    height: 6px;
    background: #e2e8f0;
    border-radius: 3px;
    overflow: hidden;
  }

  .exposure-fill {
    height: 100%;
    background: #64748b;
    border-radius: 3px;
  }

  .exposure-value {
    font-weight: 600;
    color: #475569;
  }

  .view-profile-cta {
    font-size: 0.75rem;
    font-weight: 600;
    color: #2563eb;
  }

  .no-results {
    text-align: center;
    padding: 3rem;
    background: #ffffff;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
  }

  .reset-filters-btn {
    background: #2563eb;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.35rem;
    cursor: pointer;
    font-weight: 600;
    margin-top: 0.5rem;
  }
</style>
