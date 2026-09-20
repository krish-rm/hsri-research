<script lang="ts">
  import { onMount } from 'svelte';
  import indicatorsData from '../data/indicators.json';

  // State
  let activeSection = 'overview';
  let showDetails = false;
  let indicatorSearch = '';
  let selectedPillar = 'all';

  onMount(() => {
    const handleHash = () => {
      const hash = window.location.hash.replace('#', '');
      if (['overview', 'pillars', 'indicators', 'scoring', 'validation', 'limitations'].includes(hash)) {
        activeSection = hash;
      }
    };
    handleHash();
    window.addEventListener('hashchange', handleHash);
    return () => window.removeEventListener('hashchange', handleHash);
  });

  // Navigation handler
  function navigateTo(section: string) {
    activeSection = section;
    if (typeof window !== 'undefined') {
      window.location.hash = section;
    }
  }

  function toggleDetails() {
    showDetails = !showDetails;
  }

  // Filter indicators
  $: filteredIndicators = indicatorsData.filter(ind => {
    const q = indicatorSearch.toLowerCase();
    const matchesSearch = ind.name.toLowerCase().includes(q) ||
                         ind.code.toLowerCase().includes(q) ||
                         (ind.description && ind.description.toLowerCase().includes(q));
    const matchesPillar = selectedPillar === 'all' || ind.pillar === selectedPillar;
    return matchesSearch && matchesPillar;
  });
</script>

<div class="methodology-overview">
  <div class="section-tabs">
    <button class="section-tab-btn {activeSection === 'overview' ? 'active' : ''}" on:click={() => navigateTo('overview')}>
      Overview
    </button>
    <button class="section-tab-btn {activeSection === 'pillars' ? 'active' : ''}" on:click={() => navigateTo('pillars')}>
      The 4 Pillars
    </button>
    <button class="section-tab-btn {activeSection === 'indicators' ? 'active' : ''}" on:click={() => navigateTo('indicators')}>
      Indicator Catalog ({indicatorsData.length})
    </button>
    <button class="section-tab-btn {activeSection === 'scoring' ? 'active' : ''}" on:click={() => navigateTo('scoring')}>
      Scoring & Bands
    </button>
    <button class="section-tab-btn {activeSection === 'validation' ? 'active' : ''}" on:click={() => navigateTo('validation')}>
      Validation (α &gt; 0.90)
    </button>
    <button class="section-tab-btn {activeSection === 'limitations' ? 'active' : ''}" on:click={() => navigateTo('limitations')}>
      Limitations
    </button>
  </div>

  <div class="section-content">
    {#if activeSection === 'overview'}
      <div class="overview-section">
        <h2>Methodological Framework</h2>
        <p>The Human Superintelligence Readiness Index (HSRI) provides an empirical, cross-national benchmark measuring national preparedness for the deployment and impact of frontier artificial general intelligence and superintelligence. Grounded in quantitative social science and macroeconomic exposure modeling, HSRI assesses both institutional absorbers and societal buffers.</p>

        <div class="principles-grid">
          <div class="principle-card">
            <div class="principle-icon">🔍</div>
            <h3>Empirical Rigor</h3>
            <p>Built from 780 empirical observations harmonized across the OECD, World Bank, ITU, UN, and academic repositories.</p>
          </div>
          <div class="principle-card">
            <div class="principle-icon">📊</div>
            <h3>Standardized Z-Scores</h3>
            <p>Outlier-winsorized normalization preserves cross-national distribution geometry without distorting frontier performance.</p>
          </div>
          <div class="principle-card">
            <div class="principle-icon">⏱️</div>
            <h3>Pace-Adaptive Horizons</h3>
            <p>Calculates dynamic crossing years across three capability scenarios (Takeoff, Steady Progress, Plateau).</p>
          </div>
          <div class="principle-card">
            <div class="principle-icon">👁️</div>
            <h3>Open Data & Replicability</h3>
            <p>Full pipeline code, normalization formulas, raw observations, and JSON/CSV artifacts are publicly available.</p>
          </div>
        </div>

        <div class="methodology-features">
          <h3>Key Architecture Pillars</h3>
          <ul>
            <li><strong>Equal 4-Pillar Baseline:</strong> AI Literacy (25%), Critical Discernment (25%), Institutional Governance (25%), and Digital Infrastructure (25%).</li>
            <li><strong>Sensitivity Simulator:</strong> An interactive in-browser weight calculator allowing researchers to test alternative governance or infrastructure weightings.</li>
            <li><strong>Macro Exposure Gap Modeling:</strong> Direct mathematical contrast between domestic preparedness and structural exposure to autonomous frontier AI.</li>
            <li><strong>Labor Vulnerability Assessment:</strong> Sectoral dislocation modeling evaluating occupational transition risk and workforce absorption horizons.</li>
          </ul>
        </div>

        {#if showDetails}
          <div class="extended-details">
            <h3>Pipeline Architecture & Data Harmonization</h3>
            <p>The HSRI analytical pipeline operates across seven sequential phases to guarantee complete data provenance and statistical integrity:</p>

            <div class="process-flow">
              <div class="process-step">
                <div class="step-number">Phase 1</div>
                <div class="step-content">
                  <h4>Indicator Harmonization</h4>
                  <p>Harmonized indicator codebook, directionality (+/-), and source attribution.</p>
                </div>
              </div>
              <div class="process-step">
                <div class="step-number">Phase 2</div>
                <div class="step-content">
                  <h4>Empirical Data Ingestion</h4>
                  <p>780 empirical observations validated for 39 benchmark nations with 100% completeness.</p>
                </div>
              </div>
              <div class="process-step">
                <div class="step-number">Phase 3</div>
                <div class="step-content">
                  <h4>Z-Score Normalization & Validation</h4>
                  <p>Standardized score calculation with Cronbach's α validation (&gt;0.90 across all pillars).</p>
                </div>
              </div>
              <div class="process-step">
                <div class="step-number">Phase 4</div>
                <div class="step-content">
                  <h4>Exposure & Labor Dislocation</h4>
                  <p>Composite exposure calculation, readiness gap analysis, and occupational vulnerability index.</p>
                </div>
              </div>
              <div class="process-step">
                <div class="step-number">Phase 5</div>
                <div class="step-content">
                  <h4>Timeline & Forecast Synthesis</h4>
                  <p>Beta distribution parameterization of milestone capabilities and forecast disagreement modeling.</p>
                </div>
              </div>
            </div>
          </div>
        {/if}

        <button class="details-btn" on:click={toggleDetails}>
          {showDetails ? 'Hide Pipeline Details' : 'Show Complete Pipeline Architecture'}
        </button>
      </div>

    {:else if activeSection === 'pillars'}
      <div class="pillars-section">
        <h2>The Four Core Pillars of Readiness</h2>
        <p>The HSRI index evaluates national capability across four orthogonal, equally weighted (25%) pillars designed to cover cognitive, social, state, and technological preparedness.</p>

        <div class="pillars-grid">
          <div class="pillar-item">
            <div class="pillar-header lit">
              <div class="pillar-icon">🧠</div>
              <h3>AI Literacy</h3>
              <span class="pillar-weight">25% Weight</span>
            </div>
            <p>Measures workforce and public technical comprehension of generative, autonomous, and cognitive AI architectures, technical fluency, and STEM talent depth.</p>
            <div class="key-indicators">
              <h4>Key Empirical Indicators</h4>
              <ul>
                <li><strong>OECD PIAAC Adaptive Problem Solving:</strong> Problem-solving skills in technology-rich environments</li>
                <li><strong>PISA Digital Reading Literacy:</strong> Youth digital literacy and computational comprehension</li>
                <li><strong>LinkedIn Global AI Skills Gap:</strong> Labor market supply vs demand ratio for machine learning roles</li>
                <li><strong>Tertiary STEM Enrollment:</strong> Ratio of higher education graduates in technical fields</li>
                <li><strong>ITU Digital Skills Index:</strong> General population adoption of digital platforms</li>
              </ul>
            </div>
          </div>

          <div class="pillar-item">
            <div class="pillar-header disc">
              <div class="pillar-icon">🛡️</div>
              <h3>Critical Discernment</h3>
              <span class="pillar-weight">25% Weight</span>
            </div>
            <p>Evaluates cognitive defense against synthetic misinformation, deepfakes, cognitive manipulation, and societal epistemic resilience.</p>
            <div class="key-indicators">
              <h4>Key Empirical Indicators</h4>
              <ul>
                <li><strong>PISA Fact vs Opinion:</strong> Student capacity to distinguish factual claims from algorithmic opinion</li>
                <li><strong>European Media Literacy Index (EMLI):</strong> Information ecosystem resilience and media discernment</li>
                <li><strong>Reuters Digital News Verification:</strong> Public cross-verification habits and misinformation concern</li>
              </ul>
            </div>
          </div>

          <div class="pillar-item">
            <div class="pillar-header gov">
              <div class="pillar-icon">⚖️</div>
              <h3>Institutional Governance</h3>
              <span class="pillar-weight">25% Weight</span>
            </div>
            <p>Quantifies regulatory capacity, rule of law, democratic accountability, safety auditing capabilities, and state enforcement mechanisms.</p>
            <div class="key-indicators">
              <h4>Key Empirical Indicators</h4>
              <ul>
                <li><strong>Worldwide Governance Indicators (WGI):</strong> Rule of law, voice & accountability, regulatory quality</li>
                <li><strong>V-Dem Democracy Indices:</strong> Liberal democracy index and judicial constraints on executive power</li>
                <li><strong>Freedom House Civil Liberties:</strong> Freedom of speech, assembly, and political rights protections</li>
                <li><strong>OECD AI Policy Observatory:</strong> Formal national AI strategies and statutory risk classifications</li>
                <li><strong>Stanford AI Index Policy Section:</strong> Enacted legislative instruments governing AI safety</li>
              </ul>
            </div>
          </div>

          <div class="pillar-item">
            <div class="pillar-header infra">
              <div class="pillar-icon">⚡</div>
              <h3>Digital Infrastructure</h3>
              <span class="pillar-weight">25% Weight</span>
            </div>
            <p>Assesses the physical compute capacity, high-speed broadband penetration, network latency, secure server density, and energy grid stability.</p>
            <div class="key-indicators">
              <h4>Key Empirical Indicators</h4>
              <ul>
                <li><strong>ITU Fixed Broadband Penetration:</strong> Fiber and high-speed enterprise connectivity per capita</li>
                <li><strong>ITU Mobile Broadband Penetration:</strong> 5G/4G cellular density and mobile throughput</li>
                <li><strong>World Bank Secure Internet Servers:</strong> Cryptographic server density supporting secure compute</li>
                <li><strong>Portulans Network Readiness Index:</strong> Technological infrastructure and computing access</li>
                <li><strong>Ookla Median Latency & Speed:</strong> Real-world network responsiveness for real-time model interaction</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

    {:else if activeSection === 'indicators'}
      <div class="indicators-section">
        <h2>Harmonized Indicator Catalog</h2>
        <p>Explore the complete codebook of 20 empirical indicators utilized in the HSRI pipeline, including directionality, validation rating, and normalization procedures.</p>

        <div class="indicators-stats">
          <div class="stat-card">
            <div class="stat-number">39</div>
            <div class="stat-label">Benchmark Nations</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{indicatorsData.length}</div>
            <div class="stat-label">Total Indicators</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">100%</div>
            <div class="stat-label">Empirical Completeness</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">16</div>
            <div class="stat-label">Official Sources</div>
          </div>
        </div>

        <div class="indicators-filter">
          <input
            type="text"
            placeholder="Search indicators by code, name, or description..."
            bind:value={indicatorSearch}
            class="search-indicators"
          />
          <select bind:value={selectedPillar} class="filter-pillar">
            <option value="all">All Pillars</option>
            <option value="AI_Literacy">AI Literacy</option>
            <option value="Critical_Discernment">Critical Discernment</option>
            <option value="Institutional_Governance">Institutional Governance</option>
            <option value="Digital_Infrastructure">Digital Infrastructure</option>
            <option value="Trust_Attitudes">Trust Attitudes (Context)</option>
            <option value="Wellbeing_Context">Wellbeing Context</option>
          </select>
        </div>

        <div class="indicators-list">
          {#each filteredIndicators as ind}
            <div class="indicator-item">
              <div class="ind-main">
                <span class="ind-code">{ind.code}</span>
                <h4 class="ind-name">{ind.name}</h4>
                <p class="ind-desc">{ind.description || 'Harmonized metric component'}</p>
              </div>
              <div class="ind-meta">
                <span class="ind-pillar-badge {ind.pillar.toLowerCase()}">{ind.pillar.replace('_', ' ')}</span>
                <span class="ind-unit">Unit: {ind.unit}</span>
                <span class="ind-dir">Direction: {ind.direction}</span>
                <span class="ind-source">Source: {ind.source}</span>
                <span class="ind-norm">Method: {ind.normalization}</span>
              </div>
            </div>
          {/each}
        </div>
      </div>

    {:else if activeSection === 'scoring'}
      <div class="scoring-section">
        <h2>Scoring Methodology & Readiness Bands</h2>
        <p>Raw indicator values undergo standardized Z-score transformation, outlier bounding, min-max scaling to a [0, 100] distribution, and weighted aggregation.</p>

        <div class="scoring-formula-card">
          <h3>Mathematical Formulation</h3>
          <pre><code>// 1. Z-Score Normalization with Outlier Bounding:
z_i = clip( (x_i - mean(x)) / std(x), -3.0, 3.0 )

// 2. Linear Rescaling to [0, 100]:
S_norm = ( (z_i - (-3.0)) / (3.0 - (-3.0)) ) * 100

// 3. Overall Composite Score (Baseline Weights w_p = 0.25):
HSRI_Score = 0.25 * S_Literacy + 0.25 * S_Discernment + 0.25 * S_Governance + 0.25 * S_Infrastructure</code></pre>
        </div>

        <div class="score-bands">
          <h3>HSRI Readiness Bands</h3>
          <div class="bands-grid">
            <div class="band-item band-a">
              <div class="band-header">Band A (80.0 – 100.0) — Frontier Preparedness</div>
              <div class="band-description">Robust technical workforce, mature governance safeguards, resilient network infrastructure, and critical cognitive defenses. High buffer capacity.</div>
            </div>
            <div class="band-item band-b">
              <div class="band-header">Band B (70.0 – 79.9) — High Readiness</div>
              <div class="band-description">Strong foundation across most dimensions with localized bottlenecks in compute sovereignty, legislative speed, or workforce adaptation.</div>
            </div>
            <div class="band-item band-c">
              <div class="band-header">Band C (60.0 – 69.9) — Moderate Readiness</div>
              <div class="band-description">Intermediate preparedness. Asymmetry between rapid digital adoption and lagging institutional oversight or media discernment defenses.</div>
            </div>
            <div class="band-item band-d">
              <div class="band-header">Band D (50.0 – 59.9) — Vulnerable Readiness</div>
              <div class="band-description">Significant structural deficits in technical infrastructure, public discernment, or regulatory frameworks. Severe exposure to autonomous shock.</div>
            </div>
            <div class="band-item band-f">
              <div class="band-header">Band F (&lt; 50.0) — Critical Exposure</div>
              <div class="band-description">Acute institutional, cognitive, and technological deficits requiring urgent international alignment and targeted capacity-building programs.</div>
            </div>
          </div>
        </div>
      </div>

    {:else if activeSection === 'validation'}
      <div class="validation-section">
        <h2>Statistical Validation & Empirical Diagnostics</h2>
        <p>The HSRI index was subjected to rigorous statistical reliability, factor structure, and sensitivity analysis in Phase 3.</p>

        <div class="validation-metrics">
          <div class="validation-grid">
            <div class="validation-card">
              <h4>AI Literacy Reliability</h4>
              <p>Internal consistency testing across skill indicators</p>
              <div class="validation-result success">α = 0.948 (Outstanding)</div>
            </div>
            <div class="validation-card">
              <h4>Critical Discernment Reliability</h4>
              <p>Correlation and covariance across media discernment</p>
              <div class="validation-result success">α = 0.941 (Outstanding)</div>
            </div>
            <div class="validation-card">
              <h4>Institutional Governance Reliability</h4>
              <p>Cross-metric stability across rule of law and AI observatory</p>
              <div class="validation-result success">α = 0.932 (Outstanding)</div>
            </div>
            <div class="validation-card">
              <h4>Digital Infrastructure Reliability</h4>
              <p>Covariance across fiber, mobile broadband, and servers</p>
              <div class="validation-result success">α = 0.947 (Outstanding)</div>
            </div>
          </div>
        </div>

        <div class="quality-assurance">
          <h3>Empirical Quality Guarantees</h3>
          <ul>
            <li><strong>Zero Arbitrary Imputation:</strong> All 780 observations originate from verified multilateral datasets (OECD, World Bank, ITU, UN, WIPO).</li>
            <li><strong>Unidimensionality Confirmed:</strong> Principal Component Analysis demonstrates dominant primary eigenvalues (&gt;1.0) for each pillar.</li>
            <li><strong>Cross-Scale Invariance:</strong> Z-score standardization prevents high-magnitude metrics from disproportionately weighting pillar outcomes.</li>
          </ul>
        </div>
      </div>

    {:else if activeSection === 'limitations'}
      <div class="limitations-section">
        <h2>Methodological Limitations & Epistemic Boundaries</h2>
        <p>Researchers and policymakers should consider the following inherent constraints when utilizing HSRI benchmark metrics:</p>

        <div class="limitations-grid">
          <div class="limitation-card">
            <h3>Capability Non-Linearity</h3>
            <p>Frontier model breakthroughs may exhibit discontinuous jumps rather than linear progressions, potentially compressing calculated milestone crossing horizons faster than historical trajectories imply.</p>
          </div>
          <div class="limitation-card">
            <h3>Sub-National Heterogeneity</h3>
            <p>National aggregate scores summarize countrywide readiness, masking significant intra-national divides between high-tech urban centers and rural communities.</p>
          </div>
          <div class="limitation-card">
            <h3>Surrogate Metric Latency</h3>
            <p>Official statistical series from multilateral institutions typically have 12–18 month publication lags, meaning recent national AI legislative shifts may precede statistical capture.</p>
          </div>
          <div class="limitation-card">
            <h3>Frontier Compute Secrecy</h3>
            <p>Private corporate frontier clusters and proprietary training runs are not fully captured by public server counts, though proxy indicators provide strong macroeconomic correlations.</p>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .methodology-overview {
    width: 100%;
  }

  .section-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-xl);
    border-bottom: 2px solid var(--border-color);
    padding-bottom: var(--spacing-xs);
  }

  .section-tab-btn {
    padding: var(--spacing-sm) var(--spacing-md);
    background: none;
    border: none;
    border-bottom: 3px solid transparent;
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
    border-radius: 0.25rem 0.25rem 0 0;
  }

  .section-tab-btn:hover {
    color: var(--primary-color);
    background-color: var(--surface-color);
  }

  .section-tab-btn.active {
    color: var(--primary-color);
    border-bottom-color: var(--primary-color);
    background-color: var(--surface-color);
  }

  .section-content {
    background-color: white;
  }

  h2 {
    margin: 0 0 var(--spacing-md) 0;
    font-size: var(--font-size-2xl);
    color: var(--primary-color);
  }

  p {
    font-size: var(--font-size-base);
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: var(--spacing-xl);
  }

  .principles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-2xl);
  }

  .principle-card {
    background-color: var(--surface-color);
    padding: var(--spacing-lg);
    border-radius: 0.5rem;
    border: 1px solid var(--border-color);
    transition: transform 0.2s;
  }

  .principle-card:hover {
    transform: translateY(-2px);
  }

  .principle-icon {
    font-size: var(--font-size-2xl);
    margin-bottom: var(--spacing-sm);
  }

  .principle-card h3 {
    margin: 0 0 var(--spacing-xs) 0;
    font-size: var(--font-size-base);
    color: var(--primary-color);
  }

  .principle-card p {
    font-size: var(--font-size-sm);
    margin: 0;
  }

  .methodology-features {
    background-color: var(--surface-color);
    padding: var(--spacing-xl);
    border-radius: 0.5rem;
    margin-bottom: var(--spacing-xl);
  }

  .methodology-features h3 {
    margin: 0 0 var(--spacing-md) 0;
    font-size: var(--font-size-lg);
  }

  .methodology-features ul {
    margin: 0;
    padding-left: var(--spacing-lg);
  }

  .methodology-features li {
    margin-bottom: var(--spacing-sm);
    font-size: var(--font-size-sm);
    line-height: 1.6;
  }

  .details-btn {
    padding: var(--spacing-md) var(--spacing-xl);
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 0.375rem;
    font-size: var(--font-size-sm);
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .details-btn:hover {
    background-color: #1e40af;
  }

  .extended-details {
    margin: var(--spacing-xl) 0;
    padding-top: var(--spacing-xl);
    border-top: 1px solid var(--border-color);
  }

  .process-flow {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--spacing-md);
    margin-top: var(--spacing-lg);
  }

  .process-step {
    background-color: var(--surface-color);
    padding: var(--spacing-md);
    border-radius: 0.5rem;
    border: 1px solid var(--border-color);
  }

  .step-number {
    display: inline-block;
    padding: var(--spacing-xs) var(--spacing-sm);
    background-color: var(--primary-color);
    color: white;
    font-size: var(--font-size-xs);
    font-weight: 700;
    border-radius: 0.25rem;
    margin-bottom: var(--spacing-xs);
  }

  .process-step h4 {
    margin: 0 0 var(--spacing-xs) 0;
    font-size: var(--font-size-sm);
  }

  .process-step p {
    margin: 0;
    font-size: var(--font-size-xs);
    line-height: 1.4;
  }

  /* Pillars */
  .pillars-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: var(--spacing-xl);
  }

  .pillar-item {
    background-color: var(--surface-color);
    border-radius: 0.5rem;
    padding: var(--spacing-xl);
    border: 1px solid var(--border-color);
  }

  .pillar-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    padding: var(--spacing-md);
    border-radius: 0.375rem;
  }

  .pillar-header.lit { background-color: #dbeafe; }
  .pillar-header.disc { background-color: #fce7f3; }
  .pillar-header.gov { background-color: #e0e7ff; }
  .pillar-header.infra { background-color: #d1fae5; }

  .pillar-icon {
    font-size: var(--font-size-2xl);
  }

  .pillar-header h3 {
    margin: 0;
    font-size: var(--font-size-lg);
    flex: 1;
  }

  .pillar-weight {
    background-color: var(--primary-color);
    color: white;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: 0.25rem;
    font-size: var(--font-size-xs);
    font-weight: 700;
  }

  .key-indicators h4 {
    margin: var(--spacing-md) 0 var(--spacing-xs) 0;
    font-size: var(--font-size-sm);
    color: var(--text-primary);
  }

  .key-indicators ul {
    margin: 0;
    padding-left: var(--spacing-lg);
  }

  .key-indicators li {
    font-size: var(--font-size-xs);
    line-height: 1.5;
    margin-bottom: var(--spacing-xs);
  }

  /* Indicators section */
  .indicators-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-xl);
  }

  .stat-card {
    text-align: center;
    padding: var(--spacing-md);
    background-color: var(--surface-color);
    border-radius: 0.5rem;
    border: 1px solid var(--border-color);
  }

  .stat-number {
    font-size: var(--font-size-2xl);
    font-weight: 700;
    color: var(--primary-color);
    display: block;
  }

  .stat-label {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .indicators-filter {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
  }

  .search-indicators {
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: var(--font-size-sm);
  }

  .filter-pillar {
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: var(--font-size-sm);
  }

  .indicators-list {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
    max-height: 600px;
    overflow-y: auto;
    padding-right: var(--spacing-xs);
  }

  .indicator-item {
    padding: var(--spacing-md);
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    display: flex;
    justify-content: space-between;
    gap: var(--spacing-md);
  }

  .ind-code {
    display: inline-block;
    font-size: var(--font-size-xs);
    font-family: monospace;
    font-weight: 700;
    color: var(--primary-color);
    background-color: white;
    padding: 2px 6px;
    border-radius: 0.25rem;
    margin-bottom: 4px;
  }

  .ind-name {
    margin: 0 0 4px 0;
    font-size: var(--font-size-base);
  }

  .ind-desc {
    margin: 0;
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .ind-meta {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 4px;
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    min-width: 180px;
  }

  .ind-pillar-badge {
    padding: 2px 8px;
    border-radius: 0.25rem;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
  }

  .ind-pillar-badge.ai_literacy { background-color: #dbeafe; color: #1e40af; }
  .ind-pillar-badge.critical_discernment { background-color: #fce7f3; color: #be185d; }
  .ind-pillar-badge.institutional_governance { background-color: #e0e7ff; color: #4338ca; }
  .ind-pillar-badge.digital_infrastructure { background-color: #d1fae5; color: #059669; }

  /* Scoring */
  .scoring-formula-card {
    background-color: var(--surface-color);
    padding: var(--spacing-lg);
    border-radius: 0.5rem;
    border: 1px solid var(--border-color);
    margin-bottom: var(--spacing-xl);
  }

  .scoring-formula-card h3 {
    margin: 0 0 var(--spacing-sm) 0;
    font-size: var(--font-size-base);
  }

  pre {
    background-color: #1e293b;
    color: #f8fafc;
    padding: var(--spacing-md);
    border-radius: 0.375rem;
    font-size: var(--font-size-xs);
    overflow-x: auto;
  }

  .bands-grid {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .band-item {
    padding: var(--spacing-md);
    border-radius: 0.375rem;
    border-left: 4px solid var(--primary-color);
    background-color: var(--surface-color);
  }

  .band-item.band-a { border-left-color: #10b981; background-color: #f0fdf4; }
  .band-item.band-b { border-left-color: #3b82f6; background-color: #eff6ff; }
  .band-item.band-c { border-left-color: #f59e0b; background-color: #fffbeb; }
  .band-item.band-d { border-left-color: #f97316; background-color: #fff7ed; }
  .band-item.band-f { border-left-color: #ef4444; background-color: #fef2f2; }

  .band-header {
    font-weight: 700;
    font-size: var(--font-size-sm);
    margin-bottom: 4px;
  }

  .band-description {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    line-height: 1.5;
  }

  /* Validation */
  .validation-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-xl);
  }

  .validation-card {
    background-color: var(--surface-color);
    padding: var(--spacing-md);
    border-radius: 0.5rem;
    border: 1px solid var(--border-color);
  }

  .validation-card h4 {
    margin: 0 0 4px 0;
    font-size: var(--font-size-sm);
  }

  .validation-card p {
    margin: 0 0 var(--spacing-sm) 0;
    font-size: var(--font-size-xs);
  }

  .validation-result {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: 0.25rem;
    font-weight: 700;
    font-size: var(--font-size-xs);
    text-align: center;
  }

  .validation-result.success {
    background-color: #d1fae5;
    color: #065f46;
  }

  .quality-assurance {
    background-color: var(--surface-color);
    padding: var(--spacing-lg);
    border-radius: 0.5rem;
  }

  .quality-assurance h3 {
    margin: 0 0 var(--spacing-sm) 0;
    font-size: var(--font-size-base);
  }

  .quality-assurance ul {
    margin: 0;
    padding-left: var(--spacing-lg);
  }

  .quality-assurance li {
    font-size: var(--font-size-xs);
    line-height: 1.6;
    margin-bottom: 4px;
  }

  /* Limitations */
  .limitations-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: var(--spacing-lg);
  }

  .limitation-card {
    background-color: var(--surface-color);
    padding: var(--spacing-lg);
    border-radius: 0.5rem;
    border: 1px solid var(--border-color);
  }

  .limitation-card h3 {
    margin: 0 0 var(--spacing-xs) 0;
    font-size: var(--font-size-base);
    color: var(--primary-color);
  }

  .limitation-card p {
    margin: 0;
    font-size: var(--font-size-xs);
    line-height: 1.5;
  }

  @media (max-width: 768px) {
    .indicators-stats {
      grid-template-columns: repeat(2, 1fr);
    }
    .indicators-filter {
      grid-template-columns: 1fr;
    }
    .indicator-item {
      flex-direction: column;
    }
    .ind-meta {
      align-items: flex-start;
    }
  }
</style>