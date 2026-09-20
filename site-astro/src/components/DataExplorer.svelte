<script lang="ts">
  // State
  let searchTerm = '';
  let selectedDataset = 'all';
  let activeTab = 'explorer';

  // Empirical datasets from Phase 2-6 pipeline
  const datasets = [
    {
      id: 'country-scores',
      name: 'Country Readiness Scores',
      description: 'Comprehensive country-level HSRI readiness scores across all 4 pillars for 39 benchmark nations',
      countries: 39,
      pillars: 4,
      updateFreq: 'Phase 7 Empirical',
      lastUpdate: '2026-09-20',
      formats: ['csv', 'json'],
      viewUrl: '/countries'
    },
    {
      id: 'pillar-scores',
      name: 'Pillar-Level Scores & Z-Scores',
      description: 'Standardized z-scores and normalized aggregate pillar ratings across all 4 dimensions',
      countries: 39,
      pillars: 4,
      updateFreq: 'Phase 7 Empirical',
      lastUpdate: '2026-09-20',
      formats: ['csv', 'json'],
      viewUrl: '/countries'
    },
    {
      id: 'exposure-gap',
      name: 'Readiness-Exposure Gap & Horizons',
      description: 'Macro exposure trajectories and predicted milestone crossing horizons under 3 AI pace scenarios',
      countries: 39,
      pillars: 3,
      updateFreq: 'Phase 7 Empirical',
      lastUpdate: '2026-09-20',
      formats: ['csv', 'json'],
      viewUrl: '/compare'
    },
    {
      id: 'labor-vulnerability',
      name: 'Labor Dislocation & Transition Risk',
      description: 'Occupational risk factors, displacement exposure, and labor crossing horizon projections',
      countries: 39,
      pillars: 4,
      updateFreq: 'Phase 7 Empirical',
      lastUpdate: '2026-09-20',
      formats: ['csv', 'json'],
      viewUrl: '/countries'
    },
    {
      id: 'indicator-db',
      name: 'Harmonized Indicator Database',
      description: 'Complete catalog of 20 empirical indicators, measurement units, directionality, and source attributions',
      indicators: 20,
      sources: 16,
      updateFreq: 'Harmonized 2026',
      lastUpdate: '2026-09-20',
      formats: ['csv', 'json'],
      viewUrl: '/methodology'
    },
    {
      id: 'timeline-data',
      name: 'Timeline & Forecast Synthesis',
      description: 'Beta distribution milestone forecasts, expert distributions, and readiness/exposure trajectories',
      indicators: 12,
      sources: 6,
      updateFreq: 'Forecast 2026',
      lastUpdate: '2026-09-20',
      formats: ['csv', 'json'],
      viewUrl: '/timeline'
    }
  ];

  const fileMap: Record<string, Record<string, string>> = {
    'country-scores': {
      csv: '/data/final_country_scores.csv',
      json: '/data/country_scores.json'
    },
    'pillar-scores': {
      csv: '/data/pillar_scores.csv',
      json: '/data/country_scores.json'
    },
    'exposure-gap': {
      csv: '/data/readiness_exposure_gap.csv',
      json: '/data/country_scores.json'
    },
    'labor-vulnerability': {
      csv: '/data/labor_vulnerability.csv',
      json: '/data/country_scores.json'
    },
    'indicator-db': {
      csv: '/data/indicators.csv',
      json: '/data/indicators.json'
    },
    'timeline-data': {
      csv: '/data/scenario_crossing_years.csv',
      json: '/data/timeline_data.json'
    }
  };

  // Filter datasets based on search
  $: filteredDatasets = datasets.filter(dataset => {
    const matchesSearch = dataset.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         dataset.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDataset = selectedDataset === 'all' || dataset.id === selectedDataset;
    return matchesSearch && matchesDataset;
  });

  // Tab navigation
  function setActiveTab(tab: string) {
    activeTab = tab;
  }

  // Download handler
  function triggerDownload(datasetId: string, format: string = 'csv') {
    const targetUrl = fileMap[datasetId]?.[format] || fileMap[datasetId]?.['csv'];
    if (targetUrl) {
      const a = document.createElement('a');
      a.href = targetUrl;
      a.download = targetUrl.split('/').pop() || 'dataset.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  }

  // API endpoint generation
  function generateApiEndpoint(datasetId: string) {
    return `/data/${fileMap[datasetId]?.json?.split('/').pop() || 'country_scores.json'}`;
  }
</script>

<div class="data-explorer">
  <div class="explorer-tabs">
    <button
      class="tab-btn {activeTab === 'explorer' ? 'active' : ''}"
      on:click={() => setActiveTab('explorer')}
    >
      Interactive Explorer
    </button>
    <button
      class="tab-btn {activeTab === 'api' ? 'active' : ''}"
      on:click={() => setActiveTab('api')}
    >
      API Access
    </button>
    <button
      class="tab-btn {activeTab === 'code' ? 'active' : ''}"
      on:click={() => setActiveTab('code')}
    >
      Code Packages
    </button>
  </div>

  {#if activeTab === 'explorer'}
    <div class="explorer-content">
      <div class="search-filter">
        <input
          type="text"
          placeholder="Search datasets..."
          bind:value={searchTerm}
          class="search-input"
        />
        <select bind:value={selectedDataset} class="filter-select">
          <option value="all">All Datasets</option>
          {#each datasets as dataset}
            <option value={dataset.id}>{dataset.name}</option>
          {/each}
        </select>
      </div>

      <div class="datasets-grid">
        {#each filteredDatasets as dataset}
          <div class="dataset-card">
            <div class="dataset-header">
              <h3>{dataset.name}</h3>
              <span class="dataset-status">
                <span class="status-dot"></span>
                {dataset.updateFreq}
              </span>
            </div>

            <p class="dataset-description">{dataset.description}</p>

            <div class="dataset-stats">
              <div class="stat-item">
                <span class="stat-number">{dataset.countries || dataset.indicators}</span>
                <span class="stat-label">
                  {dataset.countries ? 'Countries' : 'Indicators'}
                </span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{dataset.pillars || dataset.sources}</span>
                <span class="stat-label">
                  {dataset.pillars ? 'Pillars' : 'Sources'}
                </span>
              </div>
            </div>

            <div class="dataset-formats">
              <h4>Direct Downloads</h4>
              <div class="format-tags">
                {#each dataset.formats as format}
                  <button
                    class="format-tag-btn"
                    on:click={() => triggerDownload(dataset.id, format)}
                  >
                    📥 {format.toUpperCase()}
                  </button>
                {/each}
              </div>
            </div>

            <div class="dataset-actions">
              <button
                class="download-btn"
                on:click={() => triggerDownload(dataset.id, 'csv')}
              >
                Download CSV
              </button>
              <a href={dataset.viewUrl} class="view-btn">View Online</a>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {:else if activeTab === 'api'}
    <div class="api-content">
      <div class="api-intro">
        <h3>REST API Access</h3>
        <p>Access HSRI data programmatically through our RESTful API. All endpoints support JSON format and require authentication.</p>
      </div>

      <div class="api-examples">
        <div class="example-card">
          <h4>Country Readiness Scores</h4>
          <pre><code>GET /data/country_scores.json
Content-Type: application/json</code></pre>
        </div>

        <div class="example-card">
          <h4>Country Profiles &amp; Horizons</h4>
          <pre><code>GET /data/country_profiles.json
Content-Type: application/json</code></pre>
        </div>

        <div class="example-card">
          <h4>Harmonized Indicators Catalog</h4>
          <pre><code>GET /data/indicators.json
Content-Type: application/json</code></pre>
        </div>
      </div>

      <div class="api-documentation">
        <h4>Direct REST Data Access</h4>
        <p>All HSRI pipeline datasets are served statically and cache-optimized. You can fetch raw JSON directly via cURL or client-side fetch():</p>
        <a href="/data/country_scores.json" target="_blank" class="api-docs-link">Inspect Raw country_scores.json</a>
      </div>
    </div>
  {:else if activeTab === 'code'}
    <div class="code-packages">
      <div class="package-grid">
        <div class="package-card">
          <div class="package-header">
            <h4>R Package</h4>
            <span class="version">v1.2.0</span>
          </div>
          <div class="package-description">
            <p>Statistical analysis and visualization of HSRI data with R</p>
            <div class="package-features">
              <ul>
                <li>CRAN distribution</li>
                <li>Comprehensive vignettes</li>
                <li>Data visualization templates</li>
                <li>Statistical functions</li>
              </ul>
            </div>
          </div>
          <div class="package-install">
            <code>install.packages("hsri")</code>
          </div>
        </div>

        <div class="package-card">
          <div class="package-header">
            <h4>Python Package</h4>
            <span class="version">v0.8.0</span>
          </div>
          <div class="package-description">
            <p>Data analysis with pandas integration and visualization library</p>
            <div class="package-features">
              <ul>
                <li>pip install available</li>
                <li>Jupyter notebook examples</li>
                <li>DataFrames support</li>
                <li>Visualization library</li>
              </ul>
            </div>
          </div>
          <div class="package-install">
            <code>pip install hsri-python</code>
          </div>
        </div>

        <div class="package-card">
          <div class="package-header">
            <h4>JavaScript Library</h4>
            <span class="version">v1.0.0</span>
          </div>
          <div class="package-description">
            <p>Browser-side data visualization and chart generation</p>
            <div class="package-features">
              <ul>
                <li>ES6 modules</li>
                <li>React/Vue support</li>
                <li>Interactive charts</li>
                <li>WebGL rendering</li>
              </ul>
            </div>
          </div>
          <div class="package-install">
            <code>npm install hsri-js</code>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .data-explorer {
    max-width: 1200px;
    margin: 0 auto;
  }

  .explorer-tabs {
    display: flex;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-xl);
    border-bottom: 1px solid var(--border-color);
  }

  .tab-btn {
    padding: var(--spacing-md) var(--spacing-lg);
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: var(--font-size-base);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
  }

  .tab-btn:hover {
    color: var(--primary-color);
  }

  .tab-btn.active {
    color: var(--primary-color);
    border-bottom-color: var(--primary-color);
  }

  .explorer-content {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-2xl);
  }

  .search-filter {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: var(--spacing-lg);
    align-items: end;
  }

  .search-input {
    padding: var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: var(--font-size-base);
  }

  .filter-select {
    padding: var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: var(--font-size-base);
    min-width: 200px;
  }

  .datasets-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: var(--spacing-xl);
  }

  .dataset-card {
    background-color: white;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    padding: var(--spacing-xl);
    transition: transform 0.2s;
  }

  .dataset-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .dataset-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-md);
  }

  .dataset-header h3 {
    margin: 0;
    font-size: var(--font-size-lg);
    color: var(--primary-color);
  }

  .dataset-status {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }

  .status-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
  }

  .dataset-description {
    margin-bottom: var(--spacing-lg);
    font-size: var(--font-size-sm);
    line-height: 1.5;
    color: var(--text-secondary);
  }

  .dataset-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
  }

  .stat-item {
    text-align: center;
    padding: var(--spacing-md);
    background-color: var(--surface-color);
    border-radius: 0.375rem;
  }

  .stat-number {
      font-size: var(--font-size-2xl);
      font-weight: 700;
      color: var(--primary-color);
      display: block;
      margin-bottom: var(--spacing-xs);
    }

    .stat-label {
      font-size: var(--font-size-xs);
      color: var(--text-secondary);
      text-transform: uppercase;
    }

    .dataset-formats {
      margin-bottom: var(--spacing-lg);
    }

    .dataset-formats h4 {
      margin: 0 0 var(--spacing-sm) 0;
      font-size: var(--font-size-sm);
      font-weight: 600;
    }

    .format-tags {
      display: flex;
      flex-wrap: wrap;
      gap: var(--spacing-xs);
    }

    .format-tag,
    .format-tag-btn {
      padding: var(--spacing-xs) var(--spacing-sm);
      background-color: var(--surface-color);
      border: 1px solid var(--border-color);
      border-radius: 0.25rem;
      font-size: var(--font-size-xs);
      font-weight: 500;
      color: var(--text-primary);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .format-tag-btn:hover {
      background-color: var(--primary-color);
      color: white;
      border-color: var(--primary-color);
    }

    .dataset-actions {
      display: flex;
      gap: var(--spacing-sm);
    }

    .download-btn {
      flex: 1;
      padding: var(--spacing-md);
      background-color: var(--primary-color);
      color: white;
      border: none;
      border-radius: 0.375rem;
      font-size: var(--font-size-sm);
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
    }

    .download-btn:hover {
      background-color: #1e40af;
    }

    .view-btn {
      padding: var(--spacing-md);
      border: 1px solid var(--border-color);
      background-color: white;
      color: var(--text-primary);
      border-radius: 0.375rem;
      font-size: var(--font-size-sm);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
    }

    .view-btn:hover {
      background-color: var(--surface-color);
    }

    .api-content {
      display: flex;
      flex-direction: column;
      gap: var(--spacing-2xl);
    }

    .api-intro {
      background-color: white;
      padding: var(--spacing-xl);
      border-radius: 0.5rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .api-intro h3 {
      margin: 0 0 var(--spacing-md) 0;
      font-size: var(--font-size-xl);
      color: var(--primary-color);
    }

    .api-intro p {
      font-size: var(--font-size-base);
      line-height: 1.6;
      color: var(--text-secondary);
    }

    .api-examples {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: var(--spacing-xl);
    }

    .example-card {
      background-color: white;
      padding: var(--spacing-xl);
      border-radius: 0.5rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .example-card h4 {
      margin: 0 0 var(--spacing-md) 0;
      font-size: var(--font-size-base);
      color: var(--primary-color);
    }

    pre {
      background-color: var(--surface-color);
      padding: var(--spacing-md);
      border-radius: 0.375rem;
      font-size: var(--font-size-sm);
      overflow-x: auto;
    }

    code {
      font-family: 'Courier New', monospace;
    }

    .api-documentation {
      background-color: white;
      padding: var(--spacing-xl);
      border-radius: 0.5rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      text-align: center;
    }

    .api-documentation h4 {
      margin: 0 0 var(--spacing-md) 0;
    }

    .api-docs-link {
      display: inline-block;
      padding: var(--spacing-md) var(--spacing-xl);
      background-color: var(--primary-color);
      color: white;
      text-decoration: none;
      border-radius: 0.375rem;
      font-weight: 500;
      transition: all 0.2s;
    }

    .api-docs-link:hover {
      background-color: #1e40af;
    }

    .code-packages {
      display: flex;
      flex-direction: column;
      gap: var(--spacing-2xl);
    }

    .package-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: var(--spacing-xl);
    }

    .package-card {
      background-color: white;
      border-radius: 0.5rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      padding: var(--spacing-xl);
      transition: transform 0.2s;
    }

    .package-card:hover {
      transform: translateY(-2px);
    }

    .package-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: var(--spacing-lg);
    }

    .package-header h4 {
      margin: 0;
      font-size: var(--font-size-lg);
      color: var(--primary-color);
    }

    .version {
      background-color: var(--surface-color);
      padding: var(--spacing-xs) var(--spacing-sm);
      border-radius: 0.25rem;
      font-size: var(--font-size-xs);
      font-weight: 600;
    }

    .package-description p {
      margin: 0 0 var(--spacing-lg) 0;
      font-size: var(--font-size-sm);
      line-height: 1.5;
      color: var(--text-secondary);
    }

    .package-features ul {
      margin: 0 0 var(--spacing-lg) 0;
      padding-left: var(--spacing-lg);
    }

    .package-features li {
      margin-bottom: var(--spacing-xs);
      font-size: var(--font-size-sm);
    }

    .package-install {
      background-color: var(--surface-color);
      padding: var(--spacing-md);
      border-radius: 0.375rem;
      text-align: center;
    }

    @media (max-width: 768px) {
      .search-filter {
        grid-template-columns: 1fr;
      }

      .filter-select {
        width: 100%;
      }

      .datasets-grid,
      .api-examples,
      .package-grid {
        grid-template-columns: 1fr;
      }

      .explorer-tabs {
        flex-direction: column;
      }

      .tab-btn {
        text-align: left;
      }
    }
  </style>