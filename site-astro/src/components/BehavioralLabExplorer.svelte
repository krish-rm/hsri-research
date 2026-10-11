<script lang="ts">
  import expData from '../data/behavioral_experiments.json';

  let activeTab = 'paradigms'; // 'paradigms' | 'insitu' | 'wedge_sim' | 'synthetic'
  let showCFF = false;

  // Wedge Simulator State
  let aiGenTime = 10; // seconds
  let humanVerifyTime = 120; // seconds

  $: latencyWedge = humanVerifyTime - aiGenTime;
  $: asymmetryRatio = (humanVerifyTime / Math.max(aiGenTime, 1)).toFixed(1);
  $: riskLevel = Number(asymmetryRatio) > 10 ? 'Severe Epistemic Collapse (Rubber-Stamping)' :
                 Number(asymmetryRatio) > 3 ? 'Elevated Backlog (Automation Complacency)' :
                 'Cognitively Manageable';
</script>

<div class="lab-explorer-container">
  <!-- Top Navigation Tabs -->
  <div class="explorer-nav">
    <button class="tab-btn" class:active={activeTab === 'paradigms'} on:click={() => activeTab = 'paradigms'}>
      Behavioral Battery (EXP-01–09)
    </button>
    <button class="tab-btn" class:active={activeTab === 'insitu'} on:click={() => activeTab = 'insitu'}>
      In-Situ Professional Oversight
    </button>
    <button class="tab-btn" class:active={activeTab === 'wedge_sim'} on:click={() => activeTab = 'wedge_sim'}>
      Latency Wedge Simulator
    </button>
    <button class="tab-btn" class:active={activeTab === 'synthetic'} on:click={() => activeTab = 'synthetic'}>
      ASI Synthetic Simulations
    </button>
  </div>

  <!-- Tab 1: 9 Paradigms -->
  {#if activeTab === 'paradigms'}
    <div class="tab-section">
      <div class="section-header">
        <div>
          <h3>9-Paradigm Psychometric Battery (N=1,080)</h3>
          <p>Calibrated experimental paradigms isolating human error discernment, automation bias, and cognitive forcing functions.</p>
        </div>
        <div class="cff-toggle-wrapper">
          <label class="switch-label">
            <span>Interface Mode:</span>
            <button class="toggle-btn" class:cff-active={showCFF} on:click={() => showCFF = !showCFF}>
              {showCFF ? 'Cognitive-Forcing Interface (CFF Active)' : 'Passive Review (Baseline)'}
            </button>
          </label>
        </div>
      </div>

      <div class="paradigms-grid">
        {#each expData.paradigms as p}
          <div class="paradigm-card">
            <div class="card-top">
              <span class="exp-id">{p.id}</span>
              <span class="domain-badge">{p.domain}</span>
            </div>
            <h4 class="paradigm-name">{p.name}</h4>
            <p class="paradigm-desc">{p.description}</p>
            
            <div class="stats-row">
              <div class="stat-box">
                <span class="stat-lbl">Sample</span>
                <span class="stat-val">{p.sampleSize}</span>
              </div>
              <div class="stat-box">
                <span class="stat-lbl">Discrim (D)</span>
                <span class="stat-val">{p.discriminability}</span>
              </div>
              <div class="stat-box">
                <span class="stat-lbl">Accuracy</span>
                <span class="stat-val accuracy-val" class:high-acc={showCFF}>
                  {showCFF ? p.cffAccuracy : p.baselineAccuracy}
                </span>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Tab 2: In-Situ Professional Validation -->
  {#if activeTab === 'insitu'}
    <div class="tab-section">
      <div class="section-header">
        <div>
          <h3>In-Situ Ecological Validity Across 4 Critical Sectors</h3>
          <p>Evaluation of 500 professional operators across 20,000 real-world simulated task trials (Phase 10).</p>
        </div>
      </div>

      <div class="summary-kpis">
        <div class="kpi-card">
          <span class="kpi-label">Field Oversight Accuracy</span>
          <span class="kpi-value">{(expData.inSituValidation.overallAccuracy * 100).toFixed(1)}%</span>
          <span class="kpi-sub">Target &ge; 70.0%</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Defect Leakage Rate</span>
          <span class="kpi-value">{(expData.inSituValidation.defectLeakageRate * 100).toFixed(1)}%</span>
          <span class="kpi-sub">Target &le; 20.0%</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Mean Latency Wedge (&Delta;T)</span>
          <span class="kpi-value">{expData.inSituValidation.verificationLatencyWedge}s</span>
          <span class="kpi-sub">Human 114.2s vs AI 9.65s</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Lab-to-Situ Concordance</span>
          <span class="kpi-value">{expData.inSituValidation.labToSituConcordance}</span>
          <span class="kpi-sub">Target &le; 0.080</span>
        </div>
      </div>

      <div class="domain-table-wrapper">
        <table class="domain-table">
          <thead>
            <tr>
              <th>Professional Domain</th>
              <th>Field Accuracy</th>
              <th>Defect Leakage (DLR)</th>
              <th>Verification Latency Wedge (&Delta;T)</th>
            </tr>
          </thead>
          <tbody>
            {#each expData.inSituValidation.domains as d}
              <tr>
                <td><strong>{d.domain}</strong></td>
                <td>{d.accuracy}</td>
                <td>{d.dlr}</td>
                <td>{d.wedge}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  {/if}

  <!-- Tab 3: Verification Latency Wedge Simulator -->
  {#if activeTab === 'wedge_sim'}
    <div class="tab-section">
      <div class="section-header">
        <div>
          <h3>Verification Latency Wedge (&Delta;T_wedge) Simulator</h3>
          <p>
            Simulate how cognitive review time and machine output generation velocity interact to induce automation complacency.
          </p>
        </div>
      </div>

      <div class="sim-grid">
        <div class="controls-panel">
          <div class="slider-group">
            <label for="ai-time">AI Output Generation Time: <strong>{aiGenTime}s</strong></label>
            <input id="ai-time" type="range" min="1" max="60" bind:value={aiGenTime} class="slider" />
            <small>Time required for frontier LLM/agent to generate complex code, contract, or clinical brief.</small>
          </div>

          <div class="slider-group">
            <label for="human-time">Human Verification Latency: <strong>{humanVerifyTime}s</strong></label>
            <input id="human-time" type="range" min="10" max="600" step="5" bind:value={humanVerifyTime} class="slider" />
            <small>Time required for expert human to mathematically or empirically verify every line and assumption.</small>
          </div>
        </div>

        <div class="results-panel">
          <div class="wedge-metric">
            <span class="wedge-title">Verification Latency Wedge (&Delta;T_wedge)</span>
            <span class="wedge-num">{latencyWedge} seconds</span>
          </div>

          <div class="asymmetry-metric">
            <span class="asym-title">Asymmetry Ratio (T_verify / T_gen)</span>
            <span class="asym-num">{asymmetryRatio}x</span>
          </div>

          <div class="verdict-card" class:severe={Number(asymmetryRatio) > 10} class:elevated={Number(asymmetryRatio) > 3 && Number(asymmetryRatio) <= 10}>
            <h4>Governance Status: {riskLevel}</h4>
            <p>
              {#if Number(asymmetryRatio) > 10}
                Critical Asymmetry: Human operators face exponential backlogs. Without mandatory Cognitive-Forcing Functions (CFF), human oversight inevitably collapses into rubber-stamping.
              {:else if Number(asymmetryRatio) > 3}
                Elevated Risk: Operators experience epistemic fatigue within 45 minutes of continuous task execution. Periodic breaks and pre-commitment required.
              {:else}
                Safe Horizon: Verification speed is within human cognitive equilibrium. Substantive oversight is sustained.
              {/if}
            </p>
          </div>
        </div>
      </div>
    </div>
  {/if}

  <!-- Tab 4: Synthetic Simulations -->
  {#if activeTab === 'synthetic'}
    <div class="tab-section">
      <div class="section-header">
        <div>
          <h3>ASI Synthetic Computational Laboratory Simulations</h3>
          <p>Simulations executed under HSRI Rule 12 investigating multi-agent swarm error dynamics and persuasion boundaries.</p>
        </div>
      </div>

      <div class="synthetic-grid">
        {#each expData.syntheticSimulations as syn}
          <div class="synthetic-card">
            <div class="synthetic-badge">{syn.classification}</div>
            <h4>{syn.id}: {syn.name}</h4>
            <div class="syn-details">
              {#if syn.id === 'EXP-07-SYN'}
                <div class="syn-kpi"><span>Swarm Agents:</span> <strong>{syn.agents}</strong></div>
                <div class="syn-kpi"><span>Oracle Survival:</span> <strong>{syn.oracleSurvival}</strong></div>
                <div class="syn-kpi"><span>Closed-Loop Survival:</span> <strong>{syn.closedLoopSurvival}</strong></div>
                <div class="syn-kpi"><span>Survival Ratio:</span> <strong>{syn.survivalRatio}</strong></div>
                <div class="syn-kpi"><span>Survival Half-Life (&tau;_1/2):</span> <strong>{syn.survivalHalfLife}</strong></div>
              {:else}
                <div class="syn-kpi"><span>Ground Truths:</span> <strong>{syn.groundTruths}</strong></div>
                <div class="syn-kpi"><span>Inversion Delta (&Delta;C*):</span> <strong>{syn.inversionDelta}</strong></div>
                <div class="syn-kpi"><span>Shallow Accuracy (D=1):</span> <strong>{syn.shallowAccuracy}</strong></div>
                <div class="syn-kpi"><span>Epistemic Buffer Ratio:</span> <strong>{syn.epistemicBufferRatio}</strong></div>
                <div class="syn-kpi"><span>Deep Accuracy (D=4):</span> <strong>{syn.deepAccuracy}</strong></div>
              {/if}
            </div>
            <div class="syn-conclusion">
              <strong>Core Scientific Finding:</strong>
              <p>{syn.conclusion}</p>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .lab-explorer-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
  }

  .explorer-nav {
    display: flex;
    gap: 1rem;
    border-bottom: 2px solid #e2e8f0;
    margin-bottom: 2rem;
    flex-wrap: wrap;
  }

  .tab-btn {
    background: none;
    border: none;
    padding: 0.75rem 1.25rem;
    font-size: 1rem;
    font-weight: 600;
    color: #64748b;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.2s;
  }

  .tab-btn:hover { color: #0f172a; }
  .tab-btn.active { color: #0f172a; border-bottom-color: #3b82f6; }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .section-header h3 {
    margin: 0 0 0.25rem 0;
    font-size: 1.4rem;
    color: #0f172a;
  }

  .section-header p {
    margin: 0;
    color: #64748b;
    font-size: 0.95rem;
  }

  .toggle-btn {
    padding: 0.5rem 1rem;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    background: #f8fafc;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }

  .toggle-btn.cff-active {
    background: #10b981;
    color: white;
    border-color: #059669;
  }

  .paradigms-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.25rem;
  }

  .paradigm-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .card-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }

  .exp-id {
    font-weight: 700;
    background: #1e293b;
    color: white;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
  }

  .domain-badge {
    background: #f1f5f9;
    color: #475569;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
  }

  .paradigm-name {
    margin: 0.25rem 0 0.5rem 0;
    font-size: 1.05rem;
    color: #0f172a;
  }

  .paradigm-desc {
    font-size: 0.85rem;
    color: #475569;
    line-height: 1.4;
    margin-bottom: 1rem;
  }

  .stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    border-top: 1px solid #f1f5f9;
    padding-top: 0.75rem;
  }

  .stat-box {
    display: flex;
    flex-direction: column;
  }

  .stat-lbl {
    font-size: 0.7rem;
    color: #64748b;
  }

  .stat-val {
    font-size: 0.95rem;
    font-weight: 700;
    color: #0f172a;
  }

  .accuracy-val.high-acc {
    color: #10b981;
  }

  /* In Situ */
  .summary-kpis {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-bottom: 1.75rem;
  }

  .kpi-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
  }

  .kpi-label {
    font-size: 0.8rem;
    color: #64748b;
  }

  .kpi-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0.25rem 0;
  }

  .kpi-sub {
    font-size: 0.75rem;
    color: #10b981;
  }

  .domain-table-wrapper {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow-x: auto;
  }

  .domain-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }

  .domain-table th, .domain-table td {
    padding: 0.85rem 1rem;
    text-align: left;
    border-bottom: 1px solid #f1f5f9;
  }

  .domain-table th {
    background: #f8fafc;
    color: #475569;
  }

  /* Wedge Simulator */
  .sim-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }

  @media (max-width: 768px) {
    .sim-grid { grid-template-columns: 1fr; }
  }

  .controls-panel {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.5rem;
  }

  .slider-group {
    margin-bottom: 1.5rem;
  }

  .slider-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
  }

  .slider {
    width: 100%;
    cursor: pointer;
  }

  .slider-group small {
    display: block;
    color: #64748b;
    font-size: 0.8rem;
    margin-top: 0.35rem;
  }

  .results-panel {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .wedge-metric, .asymmetry-metric {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .wedge-title, .asym-title {
    font-weight: 600;
    color: #334155;
  }

  .wedge-num, .asym-num {
    font-size: 1.4rem;
    font-weight: 800;
    color: #0f172a;
  }

  .verdict-card {
    background: #dbeafe;
    border: 1px solid #93c5fd;
    border-radius: 8px;
    padding: 1.25rem;
  }

  .verdict-card h4 {
    margin: 0 0 0.5rem 0;
    color: #1e40af;
  }

  .verdict-card p {
    margin: 0;
    font-size: 0.85rem;
    line-height: 1.4;
    color: #1e3a8a;
  }

  .verdict-card.elevated {
    background: #fef9c3;
    border-color: #fde047;
  }
  .verdict-card.elevated h4 { color: #854d0e; }
  .verdict-card.elevated p { color: #713f12; }

  .verdict-card.severe {
    background: #fee2e2;
    border-color: #fca5a5;
  }
  .verdict-card.severe h4 { color: #991b1b; }
  .verdict-card.severe p { color: #7f1d1d; }

  /* Synthetic */
  .synthetic-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
  }

  @media (max-width: 768px) {
    .synthetic-grid { grid-template-columns: 1fr; }
  }

  .synthetic-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.5rem;
  }

  .synthetic-badge {
    background: #475569;
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 0.75rem;
  }

  .synthetic-card h4 {
    margin: 0 0 1rem 0;
    color: #0f172a;
  }

  .syn-kpi {
    display: flex;
    justify-content: space-between;
    padding: 0.35rem 0;
    border-bottom: 1px solid #f8fafc;
    font-size: 0.85rem;
  }

  .syn-conclusion {
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid #e2e8f0;
    font-size: 0.85rem;
  }

  .syn-conclusion p {
    margin: 0.25rem 0 0 0;
    color: #475569;
  }
</style>
