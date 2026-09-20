<script lang="ts">
  // Props
  export let selectedCountries = [];
  export let showDetails = false;

  // State
  let comparisonMode = 'side-by-side';
  let showPillarDetails = false;
  let showExposureDetails = false;

  // Get score band color
  function getScoreBandClass(score) {
    if (score >= 80) return 'score-band-a';
    if (score >= 70) return 'score-band-b';
    if (score >= 60) return 'score-band-c';
    if (score >= 50) return 'score-band-d';
    return 'score-band-f';
  }

  // Get band description
  function getBandDescription(band) {
    const descriptions = {
      'A': 'High readiness',
      'B': 'Good readiness',
      'C': 'Moderate readiness',
      'D': 'Limited readiness',
      'F': 'Very limited readiness'
    };
    return descriptions[band] || 'Unknown';
  }

  // Format number
  function formatNumber(num: any): string {
    if (num === undefined || num === null || isNaN(Number(num))) {
      return '0.0';
    }
    return Number(num).toFixed(1);
  }
</script>

<div class="country-comparison">
  <div class="comparison-header">
    <h3>Country Comparison</h3>
    <div class="comparison-controls">
      <div class="mode-selector">
        <button
          class="mode-btn {comparisonMode === 'side-by-side' ? 'active' : ''}"
          onclick={() => comparisonMode = 'side-by-side'}
        >
          Side by Side
        </button>
        <button
          class="mode-btn {comparisonMode === 'detailed' ? 'active' : ''}"
          onclick={() => comparisonMode = 'detailed'}
        >
          Detailed
        </button>
      </div>
    </div>
  </div>

  {#if selectedCountries.length === 0}
    <div class="empty-state">
      <p>Select countries to compare</p>
    </div>
  {:else if selectedCountries.length === 1}
    <div class="single-country">
      <div class="country-overview">
        <div class="country-header">
          <h4>{selectedCountries[0].name}</h4>
          <span class="country-code">{selectedCountries[0].code}</span>
        </div>

        <div class="score-display">
          <div class="score-value {getScoreBandClass(selectedCountries[0].score)}">
            {formatNumber(selectedCountries[0].score)}
          </div>
          <div class="band-badge {getScoreBandClass(selectedCountries[0].score)}">
            {selectedCountries[0].band}
          </div>
          <div class="band-description">
            {getBandDescription(selectedCountries[0].band)}
          </div>
        </div>

        {#if showDetails}
          <div class="details-section">
            <h5>Overview</h5>
            <p>{selectedCountries[0].name} scores {formatNumber(selectedCountries[0].score)} out of 100,
               placing it in the {getBandDescription(selectedCountries[0].band)} category.</p>

            <h5>Peer Group</h5>
            <p>Compared to other countries in the "{selectedCountries[0].peerGroup}" group.</p>

            <h5>Last Updated</h5>
            <p>Data last updated on {selectedCountries[0].lastUpdated}</p>
          </div>
        {/if}
      </div>
    </div>
  {:else}
    <div class="multi-country-comparison">
      {#if comparisonMode === 'side-by-side'}
        <div class="side-by-side-view">
          <!-- Country cards -->
          <div class="country-cards">
            {#each selectedCountries as country}
              <div class="country-card">
                <div class="card-header">
                  <h4>{country.name}</h4>
                  <span class="country-code">{country.code}</span>
                </div>

                <div class="card-score">
                  <div class="score-value {getScoreBandClass(country.score)}">
                    {formatNumber(country.score)}
                  </div>
                  <div class="band-badge {getScoreBandClass(country.score)}">
                    {country.band}
                  </div>
                </div>

                <div class="card-exposure">
                  <h5>Exposure Level</h5>
                  <div class="exposure-bar">
                    <div class="exposure-fill" style="width: {country.exposure}%"></div>
                  </div>
                  <div class="exposure-value">{formatNumber(country.exposure)}%</div>
                </div>

                <div class="card-metrics">
                  <h5>Key Pillar Metrics</h5>
                  <div class="metrics-grid">
                    <div class="metric">
                      <span class="metric-label">AI Literacy</span>
                      <span class="metric-value">{formatNumber(country.pillars?.ai_literacy ?? country.pillars?.economic)}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-label">Critical Discernment</span>
                      <span class="metric-value">{formatNumber(country.pillars?.critical_discernment ?? country.pillars?.social)}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-label">Governance</span>
                      <span class="metric-value">{formatNumber(country.pillars?.institutional_governance ?? country.pillars?.institutional)}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-label">Infrastructure</span>
                      <span class="metric-value">{formatNumber(country.pillars?.digital_infrastructure ?? country.pillars?.technological)}</span>
                    </div>
                  </div>
                </div>

                {#if showDetails}
                  <div class="card-details">
                    <h5>Readiness Analysis</h5>
                    <p>{country.name} shows {country.score >= 70 ? 'strong' : country.score >= 60 ? 'moderate' : 'limited'}
                       readiness across all pillars, evaluated on four orthogonal empirical dimensions.</p>
                  </div>
                {/if}
              </div>
            {/each}
          </div>

          <!-- Comparison summary -->
          <div class="comparison-summary">
            <h5>Comparison Summary</h5>
            <div class="summary-content">
              {#if selectedCountries.length === 2}
                <p>
                  <strong>{selectedCountries[0].name}</strong> scores {formatNumber(selectedCountries[0].score)}
                  while <strong>{selectedCountries[1].name}</strong> scores {formatNumber(selectedCountries[1].score)}.
                  {selectedCountries[0].score > selectedCountries[1].score
                    ? ` ${selectedCountries[0].name} leads by ${formatNumber(selectedCountries[0].score - selectedCountries[1].score)} points.`
                    : selectedCountries[1].score > selectedCountries[0].score
                      ? ` ${selectedCountries[1].name} leads by ${formatNumber(selectedCountries[1].score - selectedCountries[0].score)} points.`
                      : ' Both countries have identical scores.'
                  }
                </p>
              {:else}
                <p>Comparing {selectedCountries.length} countries reveals varying levels of readiness for superintelligence.</p>
              {/if}

              <div class="key-differences">
                <h6>Key Differences</h6>
                <ul>
                  <li>
                    <strong>AI Literacy:</strong>
                    {formatNumber(selectedCountries.reduce((max, c) => (c.pillars?.ai_literacy ?? c.pillars?.economic ?? 0) > max ? (c.pillars?.ai_literacy ?? c.pillars?.economic ?? 0) : max, 0))}
                    (highest) vs
                    {formatNumber(selectedCountries.reduce((min, c) => (c.pillars?.ai_literacy ?? c.pillars?.economic ?? 100) < min ? (c.pillars?.ai_literacy ?? c.pillars?.economic ?? 100) : min, 100))}
                    (lowest)
                  </li>
                  <li>
                    <strong>Exposure Level:</strong>
                    {formatNumber(selectedCountries.reduce((max, c) => (c.exposure ?? 0) > max ? c.exposure : max, 0))}%
                    (highest) vs
                    {formatNumber(selectedCountries.reduce((min, c) => (c.exposure ?? 100) < min ? c.exposure : min, 100))}%
                    (lowest)
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      {:else if comparisonMode === 'detailed'}
        <div class="detailed-view">
          <!-- Pillar comparison -->
          <div class="pillar-comparison">
            <h5>Pillar Scores Comparison</h5>
            <div class="pillar-bars">
              {#each [
                { key: 'ai_literacy', alt: 'economic', label: 'AI Literacy' },
                { key: 'critical_discernment', alt: 'social', label: 'Critical Discernment' },
                { key: 'institutional_governance', alt: 'institutional', label: 'Institutional Governance' },
                { key: 'digital_infrastructure', alt: 'technological', label: 'Digital Infrastructure' }
              ] as pillar}
                <div class="pillar-row">
                  <div class="pillar-label">{pillar.label}</div>
                  {#each selectedCountries as country}
                    <div class="pillar-bar-container">
                      <div class="pillar-bar" style="width: {country.pillars?.[pillar.key] ?? country.pillars?.[pillar.alt] ?? 0}%; background-color: {getScoreBandClass(country.pillars?.[pillar.key] ?? country.pillars?.[pillar.alt] ?? 0)}"></div>
                      <div class="pillar-value">{formatNumber(country.pillars?.[pillar.key] ?? country.pillars?.[pillar.alt] ?? 0)}</div>
                    </div>
                  {/each}
                </div>
              {/each}
            </div>
          </div>

          <!-- Detailed metrics -->
          <div class="detailed-metrics">
            <h5>Detailed Analysis</h5>
            {#each selectedCountries as country, index}
              <div class="metric-section">
                <h6>{country.name}</h6>
                <div class="metric-details">
                  <div class="metric-item">
                    <span class="metric-name">Overall Score:</span>
                    <span class="metric-value {getScoreBandClass(country.score)}">
                      {formatNumber(country.score)} ({country.band})
                    </span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-name">Exposure Level:</span>
                    <span class="metric-value">{formatNumber(country.exposure)}%</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-name">Peer Group:</span>
                    <span class="metric-value">{country.peerGroup}</span>
                  </div>
                  {#if showPillarDetails}
                    <div class="pillars-details">
                      <h7>Pillar Breakdown</h7>
                      {#each Object.entries(country.pillars) as [pillar, value]}
                        <div class="pillar-detail">
                          <span class="pillar-name capitalize">{pillar}:</span>
                          <span class="pillar-score {getScoreBandClass(value)}">{formatNumber(value)}</span>
                        </div>
                      {/each}
                    </div>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  {/if}

  {#if selectedCountries.length > 0}
    <div class="comparison-actions">
      <button class="btn btn-secondary" onclick={() => showDetails = !showDetails}>
        {showDetails ? 'Hide Details' : 'Show Details'}
      </button>
      {#if selectedCountries.length === 2}
        <button class="btn btn-primary" onclick={() => showPillarDetails = !showPillarDetails}>
          {showPillarDetails ? 'Hide Pillar Details' : 'Show Pillar Details'}
        </button>
      {/if}
      <button class="btn btn-secondary" onclick={() => window.location.href = '/compare'}>
        Full Comparison Tool
      </button>
    </div>
  {/if}
</div>

<style>
  .country-comparison {
    background-color: white;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .comparison-header {
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .comparison-header h3 {
    margin: 0;
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--text-primary);
  }

  .comparison-controls {
    display: flex;
    gap: var(--spacing-sm);
  }

  .mode-selector {
    display: flex;
    background-color: var(--surface-color);
    border-radius: 0.375rem;
    padding: var(--spacing-xs);
  }

  .mode-btn {
    padding: var(--spacing-xs) var(--spacing-md);
    border: none;
    background: none;
    border-radius: 0.25rem;
    font-size: var(--font-size-sm);
    cursor: pointer;
    transition: background-color 0.2s;
    color: var(--text-secondary);
  }

  .mode-btn:hover {
    background-color: rgba(0, 0, 0, 0.05);
  }

  .mode-btn.active {
    background-color: white;
    color: var(--primary-color);
    font-weight: 500;
  }

  .empty-state {
    padding: var(--spacing-2xl);
    text-align: center;
    color: var(--text-secondary);
  }

  .single-country .country-overview {
    padding: var(--spacing-lg);
  }

  .country-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
  }

  .country-code {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    text-transform: uppercase;
  }

  .score-display {
    text-align: center;
    margin-bottom: var(--spacing-lg);
  }

  .score-value {
    font-size: var(--font-size-3xl);
    font-weight: 700;
    padding: var(--spacing-md) var(--spacing-xl);
    border-radius: 0.5rem;
    margin-bottom: var(--spacing-sm);
  }

  .band-badge {
    display: inline-block;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: 0.25rem;
    font-weight: 600;
    font-size: var(--font-size-sm);
    text-transform: uppercase;
    margin-bottom: var(--spacing-sm);
  }

  .band-description {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }

  .details-section {
    margin-top: var(--spacing-xl);
    padding-top: var(--spacing-lg);
    border-top: 1px solid var(--border-color);
  }

  .details-section h5 {
    margin-bottom: var(--spacing-sm);
    font-size: var(--font-size-base);
  }

  .details-section p {
    margin-bottom: var(--spacing-md);
    line-height: 1.6;
  }

  .multi-country-comparison {
    padding: var(--spacing-lg);
  }

  .country-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
  }

  .country-card {
    background-color: var(--surface-color);
    border-radius: 0.5rem;
    padding: var(--spacing-lg);
    border: 1px solid var(--border-color);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-md);
  }

  .card-header h4 {
    margin: 0;
    font-size: var(--font-size-lg);
    font-weight: 600;
  }

  .card-score {
    text-align: center;
    margin-bottom: var(--spacing-md);
  }

  .card-score .score-value {
    font-size: var(--font-size-2xl);
    margin-bottom: var(--spacing-xs);
  }

  .card-exposure {
    margin-bottom: var(--spacing-md);
  }

  .card-exposure h5 {
    margin-bottom: var(--spacing-sm);
    font-size: var(--font-size-sm);
    font-weight: 500;
  }

  .exposure-bar {
    width: 100%;
    height: 8px;
    background-color: var(--border-color);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: var(--spacing-xs);
  }

  .exposure-fill {
    height: 100%;
    background-color: var(--accent-color);
    border-radius: 4px;
    transition: width 0.3s ease;
  }

  .exposure-value {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }

  .card-metrics {
    margin-bottom: var(--spacing-md);
  }

  .card-metrics h5 {
    margin-bottom: var(--spacing-sm);
    font-size: var(--font-size-sm);
    font-weight: 500;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-sm);
  }

  .metric {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-xs);
    background-color: white;
    border-radius: 0.25rem;
    border: 1px solid var(--border-color);
  }

  .metric-label {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .metric-value {
    font-weight: 600;
    font-size: var(--font-size-sm);
  }

  .card-details {
    margin-top: var(--spacing-md);
    padding-top: var(--spacing-md);
    border-top: 1px solid var(--border-color);
  }

  .card-details h5 {
    margin-bottom: var(--spacing-sm);
    font-size: var(--font-size-sm);
  }

  .card-details p {
    font-size: var(--font-size-sm);
    line-height: 1.5;
  }

  .comparison-summary {
    background-color: var(--surface-color);
    border-radius: 0.5rem;
    padding: var(--spacing-lg);
    border: 1px solid var(--border-color);
  }

  .comparison-summary h5 {
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-base);
  }

  .summary-content p {
    margin-bottom: var(--spacing-md);
    line-height: 1.6;
  }

  .key-differences {
    margin-top: var(--spacing-md);
  }

  .key-differences h6 {
    margin-bottom: var(--spacing-sm);
    font-size: var(--font-size-sm);
    font-weight: 600;
  }

  .key-differences ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .key-differences li {
    margin-bottom: var(--spacing-xs);
    font-size: var(--font-size-sm);
    line-height: 1.5;
  }

  .pillar-comparison {
    margin-bottom: var(--spacing-2xl);
  }

  .pillar-comparison h5 {
    margin-bottom: var(--spacing-lg);
    font-size: var(--font-size-base);
  }

  .pillar-bars {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .pillar-row {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .pillar-label {
    font-weight: 500;
    width: 120px;
    text-transform: capitalize;
  }

  .pillar-bar-container {
    flex: 1;
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
  }

  .pillar-bar {
    height: 24px;
    border-radius: 4px;
    transition: width 0.3s ease;
    min-width: 20px;
  }

  .pillar-value {
    font-weight: 600;
    font-size: var(--font-size-sm);
    width: 45px;
    text-align: right;
  }

  .detailed-metrics {
    margin-top: var(--spacing-2xl);
  }

  .detailed-metrics h5 {
    margin-bottom: var(--spacing-lg);
    font-size: var(--font-size-base);
  }

  .metric-section {
    margin-bottom: var(--spacing-xl);
    padding-bottom: var(--spacing-xl);
    border-bottom: 1px solid var(--border-color);
  }

  .metric-section:last-child {
    border-bottom: none;
  }

  .metric-section h6 {
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-lg);
    font-weight: 600;
  }

  .metric-details {
    display: grid;
    gap: var(--spacing-md);
  }

  .metric-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-sm);
    background-color: var(--surface-color);
    border-radius: 0.25rem;
  }

  .metric-name {
    font-weight: 500;
    color: var(--text-secondary);
  }

  .metric-details .metric-value {
    font-weight: 600;
  }

  .pillars-details {
    margin-top: var(--spacing-md);
    padding-top: var(--spacing-md);
    border-top: 1px solid var(--border-color);
  }

  .pillars-details h7 {
    margin-bottom: var(--spacing-sm);
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: var(--text-secondary);
  }

  .pillar-detail {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-xs) 0;
  }

  .pillar-name {
    font-size: var(--font-size-sm);
    text-transform: capitalize;
  }

  .pillar-score {
    font-weight: 600;
    font-size: var(--font-size-sm);
  }

  .comparison-actions {
    padding: var(--spacing-lg);
    border-top: 1px solid var(--border-color);
    background-color: var(--surface-color);
    display: flex;
    gap: var(--spacing-sm);
    justify-content: center;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .comparison-header {
      flex-direction: column;
      gap: var(--spacing-md);
      align-items: flex-start;
    }

    .country-cards {
      grid-template-columns: 1fr;
    }

    .pillar-row {
      flex-direction: column;
      align-items: stretch;
      gap: var(--spacing-sm);
    }

    .pillar-label {
      width: 100%;
    }

    .pillar-bar-container {
      width: 100%;
    }

    .comparison-actions {
      flex-direction: column;
    }
  }

  @media (max-width: 480px) {
    .metric-grid {
      grid-template-columns: 1fr;
    }

    .pillar-bar {
      height: 20px;
    }
  }
</style>