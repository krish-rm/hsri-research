<script lang="ts">
  import { onMount } from 'svelte';
  import countryScoresData from '../data/country_scores.json';

  const baseCountries = countryScoresData.countries;

  // Sliders for the 4 pillars (in percentage points, 0-100)
  let wLiteracy = 25;
  let wDiscernment = 25;
  let wGovernance = 25;
  let wInfrastructure = 25;

  let showAll = false;
  let searchQuery = '';

  // Calculate customized score and rank shift
  $: totalWeight = Math.max(0.001, wLiteracy + wDiscernment + wGovernance + wInfrastructure);

  $: calculatedCountries = baseCountries.map(c => {
    const p = c.pillars;
    const customScore = (
      p.ai_literacy * wLiteracy +
      p.critical_discernment * wDiscernment +
      p.institutional_governance * wGovernance +
      p.digital_infrastructure * wInfrastructure
    ) / totalWeight;

    return {
      ...c,
      customScore: Math.round(customScore * 10) / 10,
      baselineScore: c.score,
      baselineRank: c.rank
    };
  }).sort((a, b) => b.customScore - a.customScore)
    .map((c, idx) => {
      const newRank = idx + 1;
      const rankShift = c.baselineRank - newRank; // positive = moved up
      return {
        ...c,
        newRank,
        rankShift
      };
    });

  $: filteredCountries = calculatedCountries.filter(c =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.code.toLowerCase().includes(searchQuery.toLowerCase())
  );

  $: displayedCountries = showAll ? filteredCountries : filteredCountries.slice(0, 10);

  function resetWeights() {
    wLiteracy = 25;
    wDiscernment = 25;
    wGovernance = 25;
    wInfrastructure = 25;
  }

  function setPreset(lit: number, disc: number, gov: number, infra: number) {
    wLiteracy = lit;
    wDiscernment = disc;
    wGovernance = gov;
    wInfrastructure = infra;
  }

  function getShiftBadge(shift: number) {
    if (shift > 0) return { text: `+${shift}`, class: 'shift-up', icon: '▲' };
    if (shift < 0) return { text: `${shift}`, class: 'shift-down', icon: '▼' };
    return { text: '—', class: 'shift-none', icon: '' };
  }
</script>

<div class="weight-calculator-card">
  <div class="calc-header">
    <div class="badge-pill">Methodological Sensitivity Simulator</div>
    <h2>Interactive Pillar Weight Calculator</h2>
    <p class="calc-desc">
      Customize the weights of the four core HSRI pillars to test policy sensitivity, explore alternative non-compensatory priorities, and observe dynamic country rank shifts in real time.
    </p>
  </div>

  <div class="presets-bar">
    <span class="preset-label">Presets:</span>
    <button class="preset-btn" onclick={resetWeights}>Equal (25% each)</button>
    <button class="preset-btn" onclick={() => setPreset(15, 15, 50, 20)}>Governance Heavy (50% Gov)</button>
    <button class="preset-btn" onclick={() => setPreset(35, 45, 10, 10)}>Cognitive Defense (45% Discernment)</button>
    <button class="preset-btn" onclick={() => setPreset(15, 15, 20, 50)}>Compute & Infra (50% Infra)</button>
  </div>

  <div class="controls-grid">
    <div class="slider-box">
      <div class="slider-header">
        <span class="pillar-dot lit-dot"></span>
        <span class="slider-title">AI Literacy</span>
        <span class="slider-val">{wLiteracy}%</span>
      </div>
      <input type="range" min="0" max="100" bind:value={wLiteracy} class="calc-slider lit-slider" />
      <span class="slider-hint">Technical workforce skill & prompt/model literacy</span>
    </div>

    <div class="slider-box">
      <div class="slider-header">
        <span class="pillar-dot disc-dot"></span>
        <span class="slider-title">Critical Discernment</span>
        <span class="slider-val">{wDiscernment}%</span>
      </div>
      <input type="range" min="0" max="100" bind:value={wDiscernment} class="calc-slider disc-slider" />
      <span class="slider-hint">Cognitive defense against deepfakes & synthetic epistemic threat</span>
    </div>

    <div class="slider-box">
      <div class="slider-header">
        <span class="pillar-dot gov-dot"></span>
        <span class="slider-title">Institutional Governance</span>
        <span class="slider-val">{wGovernance}%</span>
      </div>
      <input type="range" min="0" max="100" bind:value={wGovernance} class="calc-slider gov-slider" />
      <span class="slider-hint">Enforceable audit mandates & frontier safety regulations</span>
    </div>

    <div class="slider-box">
      <div class="slider-header">
        <span class="pillar-dot infra-dot"></span>
        <span class="slider-title">Digital Infrastructure</span>
        <span class="slider-val">{wInfrastructure}%</span>
      </div>
      <input type="range" min="0" max="100" bind:value={wInfrastructure} class="calc-slider infra-slider" />
      <span class="slider-hint">Sovereign compute density, power redundancy & grid stability</span>
    </div>
  </div>

  <div class="results-toolbar">
    <div class="search-wrap">
      <input
        type="text"
        placeholder="Filter results by nation..."
        bind:value={searchQuery}
        class="calc-search"
      />
    </div>
    <div class="toggle-wrap">
      <button class="toggle-btn" onclick={() => showAll = !showAll}>
        {showAll ? 'Show Top 10 Only' : `Show All ${calculatedCountries.length} Countries`}
      </button>
    </div>
  </div>

  <div class="table-container">
    <table class="calc-table">
      <thead>
        <tr>
          <th>Simulated Rank</th>
          <th>Country</th>
          <th>Base Rank</th>
          <th>Rank Shift</th>
          <th>Simulated Score</th>
          <th>Base Score</th>
          <th class="pillars-col">Pillar Breakdown (Lit / Disc / Gov / Infra)</th>
          <th>Profile</th>
        </tr>
      </thead>
      <tbody>
        {#each displayedCountries as country}
          {@const shift = getShiftBadge(country.rankShift)}
          <tr class="calc-row">
            <td class="rank-cell">
              <span class="rank-badge">#{country.newRank}</span>
            </td>
            <td class="country-cell">
              <div class="c-info">
                <span class="c-code">{country.code}</span>
                <span class="c-name">{country.name}</span>
              </div>
            </td>
            <td class="muted-cell">#{country.baselineRank}</td>
            <td>
              <span class="shift-pill {shift.class}">
                {shift.icon} {shift.text}
              </span>
            </td>
            <td class="score-cell highlight">
              <strong>{country.customScore}</strong>
            </td>
            <td class="muted-cell">{country.baselineScore}</td>
            <td class="pillars-cell">
              <div class="mini-pillars">
                <span class="mini-p lit-tag" title="AI Literacy">{country.pillars.ai_literacy}</span>
                <span class="mini-p disc-tag" title="Critical Discernment">{country.pillars.critical_discernment}</span>
                <span class="mini-p gov-tag" title="Institutional Governance">{country.pillars.institutional_governance}</span>
                <span class="mini-p infra-tag" title="Digital Infrastructure">{country.pillars.digital_infrastructure}</span>
              </div>
            </td>
            <td>
              <a href={`/countries/${country.id}`} class="details-link">
                View &rarr;
              </a>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

<style>
  .weight-calculator-card {
    background: #ffffff;
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
    border: 1px solid #e5e7eb;
    margin-bottom: 2.5rem;
  }

  .calc-header {
    text-align: center;
    max-width: 800px;
    margin: 0 auto 1.75rem auto;
  }

  .badge-pill {
    display: inline-block;
    padding: 0.25rem 0.85rem;
    background: #eff6ff;
    color: #2563eb;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 9999px;
    margin-bottom: 0.75rem;
  }

  .calc-header h2 {
    font-size: 1.75rem;
    color: #0f172a;
    font-weight: 800;
    margin-bottom: 0.5rem;
  }

  .calc-desc {
    color: #475569;
    font-size: 0.95rem;
    line-height: 1.5;
  }

  .presets-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 2rem;
    padding: 0.75rem;
    background: #f8fafc;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
  }

  .preset-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #64748b;
    margin-right: 0.25rem;
  }

  .preset-btn {
    background: white;
    border: 1px solid #cbd5e1;
    color: #334155;
    padding: 0.35rem 0.75rem;
    font-size: 0.8rem;
    font-weight: 500;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .preset-btn:hover {
    background: #2563eb;
    color: white;
    border-color: #2563eb;
  }

  .controls-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2rem;
  }

  .slider-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1.25rem;
  }

  .slider-header {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;
  }

  .pillar-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 0.5rem;
  }

  .lit-dot { background: #3b82f6; }
  .disc-dot { background: #8b5cf6; }
  .gov-dot { background: #10b981; }
  .infra-dot { background: #f59e0b; }

  .slider-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #1e293b;
    flex: 1;
  }

  .slider-val {
    font-size: 1rem;
    font-weight: 800;
    color: #0f172a;
  }

  .calc-slider {
    width: 100%;
    height: 6px;
    border-radius: 3px;
    background: #cbd5e1;
    outline: none;
    cursor: pointer;
    margin-bottom: 0.5rem;
  }

  .slider-hint {
    font-size: 0.75rem;
    color: #64748b;
    display: block;
    line-height: 1.3;
  }

  .results-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .calc-search {
    padding: 0.5rem 1rem;
    border: 1px solid #cbd5e1;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    width: 260px;
  }

  .toggle-btn {
    background: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .toggle-btn:hover {
    background: #2563eb;
    color: white;
  }

  .table-container {
    overflow-x: auto;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
  }

  .calc-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: 0.875rem;
  }

  .calc-table th {
    background: #f1f5f9;
    padding: 0.75rem 1rem;
    font-weight: 700;
    color: #475569;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid #cbd5e1;
  }

  .calc-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #f1f5f9;
  }

  .calc-row:hover {
    background: #f8fafc;
  }

  .rank-badge {
    font-weight: 800;
    color: #1e293b;
    font-size: 0.9rem;
  }

  .c-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .c-code {
    font-weight: 700;
    font-size: 0.75rem;
    background: #e2e8f0;
    padding: 0.15rem 0.4rem;
    border-radius: 0.25rem;
    color: #334155;
  }

  .c-name {
    font-weight: 600;
    color: #0f172a;
  }

  .muted-cell {
    color: #64748b;
  }

  .score-cell.highlight {
    color: #2563eb;
    font-size: 1rem;
  }

  .shift-pill {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    font-weight: 700;
  }

  .shift-up {
    background: #dcfce7;
    color: #166534;
  }

  .shift-down {
    background: #fee2e2;
    color: #991b1b;
  }

  .shift-none {
    background: #f1f5f9;
    color: #64748b;
  }

  .mini-pillars {
    display: flex;
    gap: 0.35rem;
  }

  .mini-p {
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.15rem 0.35rem;
    border-radius: 0.25rem;
  }

  .lit-tag { background: #dbeafe; color: #1e40af; }
  .disc-tag { background: #ede9fe; color: #5b21b6; }
  .gov-tag { background: #d1fae5; color: #065f46; }
  .infra-tag { background: #fef3c7; color: #92400e; }

  .details-link {
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.8rem;
  }

  .details-link:hover {
    text-decoration: underline;
  }
</style>
