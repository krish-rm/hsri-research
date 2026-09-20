<script lang="ts">
  import countryScoresData from '../data/country_scores.json';

  export let countries = countryScoresData.countries;

  // State
  let searchTerm = '';
  let selectedRegion = '';
  let selectedBand = '';
  let sortBy = 'rank';

  // Filtered and sorted countries
  $: filteredCountries = countries.filter(country => {
    const matchesSearch = country.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         country.code.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRegion = !selectedRegion || country.region === selectedRegion;
    const matchesBand = !selectedBand || country.band === selectedBand;
    return matchesSearch && matchesRegion && matchesBand;
  });

  $: sortedCountries = [...filteredCountries].sort((a, b) => {
    switch (sortBy) {
      case 'name':
        return a.name.localeCompare(b.name);
      case 'score':
        return b.score - a.score;
      case 'score-low':
        return a.score - b.score;
      case 'exposure':
        return b.exposure - a.exposure;
      default: // rank
        return a.rank - b.rank;
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

  function viewCountry(id: string) {
    if (typeof window !== 'undefined') {
      window.location.href = `/countries/${id.toLowerCase()}`;
    }
  }
</script>

<div class="country-list-container">
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

      <select bind:value={sortBy} class="filter-select">
        <option value="rank">Sort: By Rank</option>
        <option value="score">Sort: Score (High-Low)</option>
        <option value="score-low">Sort: Score (Low-High)</option>
        <option value="exposure">Sort: By Exposure</option>
        <option value="name">Sort: Name (A-Z)</option>
      </select>
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
        {sortedCountries.length > 0 ? (sortedCountries.reduce((sum, c) => sum + c.score, 0) / sortedCountries.length).toFixed(1) : '0.0'}
      </div>
      <div class="stat-label">Average Score</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">
        {sortedCountries.filter(c => c.band === 'A').length}
      </div>
      <div class="stat-label">Band A Nations</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">
        {sortedCountries.filter(c => c.gap > 0).length}
      </div>
      <div class="stat-label">Deficit Nations</div>
    </div>
  </div>

  <!-- Cards Grid -->
  <div class="countries-grid">
    {#each sortedCountries as country}
      <a href={`/countries/${country.id.toLowerCase()}`} class="country-card">
        <div class="card-header">
          <div class="country-info">
            <span class="rank-badge">#{country.rank}</span>
            <div class="name-group">
              <h3>{country.name}</h3>
              <span class="country-code">{country.code}</span>
            </div>
          </div>
          <div class="country-score">
            <div class="score-value" style="background-color: {getBandColor(country.band)}">
              {country.score}
            </div>
            <span class="score-band" style="background-color: {getBandColor(country.band)}">
              Band {country.band}
            </span>
          </div>
        </div>

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
      <button class="reset-filters-btn" onclick={() => { searchTerm = ''; selectedRegion = ''; selectedBand = ''; }}>
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
    min-width: 260px;
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
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .filter-select {
    padding: 0.6rem 0.85rem;
    border: 1px solid #cbd5e1;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    background: white;
    color: #334155;
    cursor: pointer;
  }

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
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
  }

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

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.25rem;
  }

  .country-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .rank-badge {
    font-size: 0.85rem;
    font-weight: 800;
    color: #64748b;
    background: #f1f5f9;
    padding: 0.25rem 0.5rem;
    border-radius: 0.35rem;
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

  .country-metrics {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
    margin-bottom: 1.25rem;
    flex: 1;
  }

  .metric-bar {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }

  .bar-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
  }

  .metric-label {
    color: #475569;
    font-weight: 500;
  }

  .metric-value {
    color: #0f172a;
    font-weight: 700;
  }

  .bar-container {
    height: 6px;
    background: #f1f5f9;
    border-radius: 3px;
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    border-radius: 3px;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 0.85rem;
    border-top: 1px solid #f1f5f9;
    font-size: 0.75rem;
  }

  .country-exposure {
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }

  .exposure-label {
    color: #64748b;
  }

  .exposure-bar {
    width: 45px;
    height: 5px;
    background: #e2e8f0;
    border-radius: 3px;
    overflow: hidden;
  }

  .exposure-fill {
    height: 100%;
    background: #ef4444;
  }

  .exposure-value {
    font-weight: 700;
    color: #0f172a;
  }

  .view-profile-cta {
    color: #2563eb;
    font-weight: 700;
    font-size: 0.8rem;
  }

  .no-results {
    text-align: center;
    padding: 3rem;
    background: white;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
    color: #64748b;
  }

  .reset-filters-btn {
    margin-top: 1rem;
    background: #2563eb;
    color: white;
    border: none;
    padding: 0.5rem 1.25rem;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
  }
</style>