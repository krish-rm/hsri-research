<script lang="ts">
  import { onMount } from 'svelte';
  import countryScoresData from '../data/country_scores.json';

  export let countries = countryScoresData.countries;

  const allCountries = countries && countries.length > 0 ? countries : countryScoresData.countries;

  let selectedCountries: any[] = [];
  let currentView: 'overview' | 'pillars' | 'timelines' = 'overview';
  let searchQuery = '';
  let copyFeedback = false;

  onMount(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const paramCountries = params.get('countries');

      if (paramCountries) {
        const codes = paramCountries.toUpperCase().split(',').map(s => s.trim());
        const matched = allCountries.filter(c => codes.includes(c.code.toUpperCase()) || codes.includes(c.id.toUpperCase()));
        if (matched.length > 0) {
          selectedCountries = matched.slice(0, 5);
        }
      }

      // Default to top 3 if none specified
      if (selectedCountries.length === 0 && allCountries.length >= 3) {
        selectedCountries = [allCountries[0], allCountries[1], allCountries[2]];
        updateUrl();
      }
    }
  });

  function updateUrl() {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      if (selectedCountries.length > 0) {
        params.set('countries', selectedCountries.map(c => c.code).join(','));
      } else {
        params.delete('countries');
      }
      const newUrl = `${window.location.pathname}?${params.toString()}`;
      window.history.replaceState({}, '', newUrl);
    }
  }

  function toggleCountry(country: any) {
    const idx = selectedCountries.findIndex(c => c.id === country.id);
    if (idx > -1) {
      selectedCountries = selectedCountries.filter(c => c.id !== country.id);
    } else if (selectedCountries.length < 5) {
      selectedCountries = [...selectedCountries, country];
    }
    updateUrl();
  }

  function removeCountry(id: string) {
    selectedCountries = selectedCountries.filter(c => c.id !== id);
    updateUrl();
  }

  function copyShareLink() {
    if (typeof window !== 'undefined') {
      navigator.clipboard.writeText(window.location.href);
      copyFeedback = true;
      setTimeout(() => { copyFeedback = false; }, 2000);
    }
  }

  function exportComparisonCSV() {
    if (selectedCountries.length === 0) return;

    const headers = [
      "Country", "Code", "Rank", "Overall Score", "Band",
      "AI Literacy", "Critical Discernment", "Institutional Governance", "Digital Infrastructure",
      "Exposure Score", "Gap Score", "Gap Status",
      "Labor Vulnerability (%)", "Labor Crossing Year",
      "Takeoff Crossing", "Steady Progress Crossing", "Plateau Crossing"
    ];

    const rows = selectedCountries.map(c => [
      `"${c.name}"`, c.code, c.rank, c.score, c.band,
      c.pillars.ai_literacy, c.pillars.critical_discernment, c.pillars.institutional_governance, c.pillars.digital_infrastructure,
      c.exposure, c.gap, `"${c.gapStatus}"`,
      c.laborVulnerability, c.laborCrossingYear,
      c.crossingYears.takeoff || "Post-2045",
      c.crossingYears.steady || "Post-2045",
      c.crossingYears.plateau || "Post-2045"
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `hsri_comparison_${selectedCountries.map(c => c.code).join("_")}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  $: filteredCountries = allCountries.filter(c =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.code.toLowerCase().includes(searchQuery.toLowerCase())
  );

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
</script>

<div class="comparison-tool-container">
  <!-- Top Comparison Section (Active Selections) -->
  <div class="comparison-display-card">
    <div class="display-header">
      <div class="header-left">
        <h2>Comparing {selectedCountries.length} of max 5 Nations</h2>
        <p class="subtitle">Side-by-side empirical benchmark analysis across 4 core readiness pillars</p>
      </div>
      <div class="header-right">
        <button class="action-btn share-btn" onclick={copyShareLink}>
          {copyFeedback ? '✓ Link Copied!' : '🔗 Copy Share Link'}
        </button>
        <button class="action-btn export-btn" onclick={exportComparisonCSV}>
          📥 Export CSV
        </button>
      </div>
    </div>

    <!-- Active Selection Tags -->
    <div class="selected-tags-bar">
      {#each selectedCountries as country}
        <div class="country-tag">
          <span class="tag-code">{country.code}</span>
          <span class="tag-name">{country.name}</span>
          <button class="remove-btn" onclick={() => removeCountry(country.id)}>✕</button>
        </div>
      {/each}
      {#if selectedCountries.length < 5}
        <span class="slots-left">({5 - selectedCountries.length} more slots available)</span>
      {/if}
    </div>

    <!-- View Mode Switcher -->
    <div class="view-tabs">
      <button
        class="tab-button {currentView === 'overview' ? 'active' : ''}"
        onclick={() => currentView = 'overview'}
      >
        Overview & Macro Gap
      </button>
      <button
        class="tab-button {currentView === 'pillars' ? 'active' : ''}"
        onclick={() => currentView = 'pillars'}
      >
        4 Core Pillars
      </button>
      <button
        class="tab-button {currentView === 'timelines' ? 'active' : ''}"
        onclick={() => currentView = 'timelines'}
      >
        Crossing Horizons
      </button>
    </div>

    <!-- VIEW 1: Overview -->
    {#if currentView === 'overview'}
      <div class="comparison-grid">
        {#each selectedCountries as country}
          <div class="country-column-card">
            <div class="col-header">
              <span class="col-rank">#{country.rank}</span>
              <h3>{country.name}</h3>
              <span class="col-code">{country.code}</span>
            </div>

            <div class="col-score-block" style="border-top: 3px solid {getBandColor(country.band)}">
              <div class="score-display">
                <span class="score-num">{country.score}</span>
                <span class="score-den">/ 100</span>
              </div>
              <span class="band-tag" style="background: {getBandColor(country.band)}">Band {country.band}</span>
            </div>

            <div class="metric-list">
              <div class="metric-item">
                <span class="lbl">Macro Exposure:</span>
                <span class="val">{country.exposure}%</span>
              </div>
              <div class="metric-item">
                <span class="lbl">Readiness Gap:</span>
                <span class="val {country.gap > 0 ? 'deficit' : 'surplus'}">
                  {country.gap > 0 ? `+${country.gap}` : country.gap}
                </span>
              </div>
              <div class="metric-item">
                <span class="lbl">Gap Status:</span>
                <span class="val">{country.gapStatus}</span>
              </div>
              <div class="metric-item">
                <span class="lbl">Labor Dislocation Horizon:</span>
                <span class="val highlight">{country.laborCrossingYear}</span>
              </div>
            </div>

            <a href={`/countries/${country.id.toLowerCase()}`} class="profile-cta">
              View Complete Profile &rarr;
            </a>
          </div>
        {/each}
      </div>
    {/if}

    <!-- VIEW 2: Pillars -->
    {#if currentView === 'pillars'}
      <div class="pillars-comparison-table">
        <div class="p-row header-p-row">
          <div class="p-label-cell">Pillar Domain</div>
          {#each selectedCountries as country}
            <div class="p-col-cell"><strong>{country.name} ({country.code})</strong></div>
          {/each}
        </div>

        <div class="p-row">
          <div class="p-label-cell">
            <span class="dot lit-dot"></span> AI Literacy
          </div>
          {#each selectedCountries as country}
            <div class="p-col-cell">
              <span class="p-val">{country.pillars.ai_literacy}%</span>
              <div class="p-bar"><div class="p-fill lit-fill" style="width: {country.pillars.ai_literacy}%"></div></div>
            </div>
          {/each}
        </div>

        <div class="p-row">
          <div class="p-label-cell">
            <span class="dot disc-dot"></span> Critical Discernment
          </div>
          {#each selectedCountries as country}
            <div class="p-col-cell">
              <span class="p-val">{country.pillars.critical_discernment}%</span>
              <div class="p-bar"><div class="p-fill disc-fill" style="width: {country.pillars.critical_discernment}%"></div></div>
            </div>
          {/each}
        </div>

        <div class="p-row">
          <div class="p-label-cell">
            <span class="dot gov-dot"></span> Institutional Governance
          </div>
          {#each selectedCountries as country}
            <div class="p-col-cell">
              <span class="p-val">{country.pillars.institutional_governance}%</span>
              <div class="p-bar"><div class="p-fill gov-fill" style="width: {country.pillars.institutional_governance}%"></div></div>
            </div>
          {/each}
        </div>

        <div class="p-row">
          <div class="p-label-cell">
            <span class="dot infra-dot"></span> Digital Infrastructure
          </div>
          {#each selectedCountries as country}
            <div class="p-col-cell">
              <span class="p-val">{country.pillars.digital_infrastructure}%</span>
              <div class="p-bar"><div class="p-fill infra-fill" style="width: {country.pillars.digital_infrastructure}%"></div></div>
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <!-- VIEW 3: Crossing Horizons -->
    {#if currentView === 'timelines'}
      <div class="pillars-comparison-table">
        <div class="p-row header-p-row">
          <div class="p-label-cell">Scenario Horizon</div>
          {#each selectedCountries as country}
            <div class="p-col-cell"><strong>{country.name} ({country.code})</strong></div>
          {/each}
        </div>

        <div class="p-row">
          <div class="p-label-cell">Takeoff Scenario (Accelerated AGI)</div>
          {#each selectedCountries as country}
            <div class="p-col-cell">
              <span class="yr-pill takeoff-yr">{country.crossingYears.takeoff || 'Post-2045'}</span>
            </div>
          {/each}
        </div>

        <div class="p-row">
          <div class="p-label-cell">Steady Progress (Baseline)</div>
          {#each selectedCountries as country}
            <div class="p-col-cell">
              <span class="yr-pill steady-yr">{country.crossingYears.steady || 'Post-2045'}</span>
            </div>
          {/each}
        </div>

        <div class="p-row">
          <div class="p-label-cell">Plateau Scenario (Sustained Bottlenecks)</div>
          {#each selectedCountries as country}
            <div class="p-col-cell">
              <span class="yr-pill plateau-yr">{country.crossingYears.plateau || 'Post-2045'}</span>
            </div>
          {/each}
        </div>

        <div class="p-row">
          <div class="p-label-cell">Labor Market Vulnerability</div>
          {#each selectedCountries as country}
            <div class="p-col-cell">
              <span class="p-val">{country.laborVulnerability}%</span>
            </div>
          {/each}
        </div>
      </div>
    {/if}
  </div>

  <!-- Bottom Country Selector Grid -->
  <div class="selector-section">
    <div class="selector-header">
      <h3>Select Nations to Compare</h3>
      <input
        type="text"
        placeholder="Filter by country or code..."
        bind:value={searchQuery}
        class="selector-search"
      />
    </div>

    <div class="selector-grid">
      {#each filteredCountries as country}
        {@const isSelected = selectedCountries.some(c => c.id === country.id)}
        <button
          class="selector-pill {isSelected ? 'selected' : ''}"
          onclick={() => toggleCountry(country)}
        >
          <span class="pill-code">{country.code}</span>
          <span class="pill-name">{country.name}</span>
          <span class="pill-score">{country.score}</span>
          <span class="pill-check">{isSelected ? '✓' : '+'}</span>
        </button>
      {/each}
    </div>
  </div>
</div>

<style>
  .comparison-tool-container {
    max-width: 1300px;
    margin: 0 auto;
  }

  .comparison-display-card {
    background: #ffffff;
    border-radius: 1rem;
    padding: 2rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    margin-bottom: 2.5rem;
  }

  .display-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .header-left h2 {
    font-size: 1.75rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 0.35rem 0;
  }

  .header-left .subtitle {
    color: #64748b;
    font-size: 0.95rem;
    margin: 0;
  }

  .header-right {
    display: flex;
    gap: 0.75rem;
  }

  .action-btn {
    padding: 0.6rem 1.15rem;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .share-btn {
    background: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
  }

  .share-btn:hover {
    background: #2563eb;
    color: white;
  }

  .export-btn {
    background: #f8fafc;
    color: #334155;
    border: 1px solid #cbd5e1;
  }

  .export-btn:hover {
    background: #0f172a;
    color: white;
  }

  .selected-tags-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    padding: 0.85rem 1rem;
    background: #f8fafc;
    border-radius: 0.5rem;
    border: 1px solid #e2e8f0;
    margin-bottom: 1.75rem;
  }

  .country-tag {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    background: white;
    border: 1px solid #cbd5e1;
    padding: 0.3rem 0.65rem;
    border-radius: 0.35rem;
    font-size: 0.85rem;
  }

  .tag-code {
    font-weight: 800;
    color: #2563eb;
  }

  .tag-name {
    font-weight: 600;
    color: #334155;
  }

  .remove-btn {
    background: none;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 0.8rem;
    margin-left: 0.25rem;
  }

  .remove-btn:hover {
    color: #dc2626;
  }

  .slots-left {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-left: 0.5rem;
  }

  .view-tabs {
    display: flex;
    gap: 0.5rem;
    border-bottom: 2px solid #e2e8f0;
    margin-bottom: 2rem;
  }

  .tab-button {
    background: none;
    border: none;
    padding: 0.75rem 1.25rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: #64748b;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
    transition: all 0.15s ease;
  }

  .tab-button.active {
    color: #2563eb;
    border-bottom-color: #2563eb;
  }

  .comparison-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
  }

  .country-column-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
  }

  .col-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .col-rank {
    font-size: 0.8rem;
    font-weight: 800;
    background: #e2e8f0;
    padding: 0.15rem 0.4rem;
    border-radius: 0.25rem;
  }

  .col-header h3 {
    margin: 0;
    font-size: 1.05rem;
    color: #0f172a;
    font-weight: 700;
    flex: 1;
  }

  .col-code {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 700;
  }

  .col-score-block {
    padding: 0.85rem 0;
    text-align: center;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1rem;
  }

  .score-num {
    font-size: 2rem;
    font-weight: 800;
    color: #0f172a;
  }

  .score-den {
    font-size: 0.85rem;
    color: #94a3b8;
  }

  .band-tag {
    display: inline-block;
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.15rem 0.5rem;
    border-radius: 0.25rem;
    margin-top: 0.35rem;
  }

  .metric-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.825rem;
    flex: 1;
    margin-bottom: 1.25rem;
  }

  .metric-item {
    display: flex;
    justify-content: space-between;
  }

  .metric-item .lbl {
    color: #64748b;
  }

  .metric-item .val {
    font-weight: 700;
    color: #1e293b;
  }

  .metric-item .deficit { color: #dc2626; }
  .metric-item .surplus { color: #16a34a; }
  .metric-item .highlight { color: #2563eb; }

  .profile-cta {
    display: block;
    text-align: center;
    background: white;
    border: 1px solid #cbd5e1;
    color: #2563eb;
    padding: 0.5rem;
    border-radius: 0.5rem;
    font-size: 0.8rem;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.15s ease;
  }

  .profile-cta:hover {
    background: #2563eb;
    color: white;
    border-color: #2563eb;
  }

  .pillars-comparison-table {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .p-row {
    display: grid;
    grid-template-columns: 240px repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    align-items: center;
    padding: 0.85rem 1rem;
    background: #f8fafc;
    border-radius: 0.5rem;
    border: 1px solid #e2e8f0;
  }

  .header-p-row {
    background: #f1f5f9;
    font-size: 0.85rem;
    color: #475569;
  }

  .p-label-cell {
    font-weight: 700;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }

  .lit-dot { background: #3b82f6; }
  .disc-dot { background: #8b5cf6; }
  .gov-dot { background: #10b981; }
  .infra-dot { background: #f59e0b; }

  .p-col-cell {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .p-val {
    font-weight: 800;
    color: #0f172a;
    font-size: 0.95rem;
  }

  .p-bar {
    height: 6px;
    background: #e2e8f0;
    border-radius: 3px;
    overflow: hidden;
  }

  .p-fill { height: 100%; border-radius: 3px; }
  .lit-fill { background: #3b82f6; }
  .disc-fill { background: #8b5cf6; }
  .gov-fill { background: #10b981; }
  .infra-fill { background: #f59e0b; }

  .yr-pill {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-weight: 800;
    font-size: 0.9rem;
    text-align: center;
  }

  .takeoff-yr { background: #fee2e2; color: #991b1b; }
  .steady-yr { background: #eff6ff; color: #1e40af; }
  .plateau-yr { background: #ecfdf5; color: #065f46; }

  .selector-section {
    background: #ffffff;
    border-radius: 1rem;
    padding: 1.75rem;
    border: 1px solid #e2e8f0;
  }

  .selector-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.25rem;
  }

  .selector-header h3 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
  }

  .selector-search {
    padding: 0.5rem 0.85rem;
    border: 1px solid #cbd5e1;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    width: 250px;
  }

  .selector-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0.65rem;
  }

  .selector-pill {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    font-size: 0.8rem;
    cursor: pointer;
    text-align: left;
    transition: all 0.15s ease;
  }

  .selector-pill:hover {
    background: #eff6ff;
    border-color: #93c5fd;
  }

  .selector-pill.selected {
    background: #2563eb;
    color: white;
    border-color: #2563eb;
  }

  .pill-code {
    font-weight: 800;
    font-size: 0.75rem;
  }

  .selector-pill.selected .pill-code {
    color: #bfdbfe;
  }

  .pill-name {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 600;
  }

  .pill-score {
    font-weight: 700;
    font-size: 0.75rem;
    color: #64748b;
  }

  .selector-pill.selected .pill-score {
    color: #e2e8f0;
  }

  .pill-check {
    font-weight: 800;
    font-size: 0.85rem;
  }
</style>