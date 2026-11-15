<script lang="ts">
  import sandboxPayload from '../data/civilizational_sandbox_payload.json';

  // ---------------------------------------------------------------------------
  // STATE MANAGEMENT
  // ---------------------------------------------------------------------------
  type TabType = 'matrix' | 'fiscal' | 'epistemic' | 'deterrence';
  let activeTab: TabType = 'matrix';

  let activeInjectId: string | null = null;
  let selectedCountryIso = 'USA';
  let searchQuery = '';
  let selectedArchetypeFilter = 'ALL';

  // Interactive Simulation Sliders
  let customDisplacementRate = 0.35; // 35% annual white-collar displacement
  let customEpistemicMonths = 24;     // Month 24 on epistemic drift horizon
  let customHumanLatencyMin = 30;     // 30 min human decision latency
  let copiedToast = false;

  // ---------------------------------------------------------------------------
  // REACTIVE DERIVATIONS
  // ---------------------------------------------------------------------------
  $: activeInject = activeInjectId 
    ? sandboxPayload.injects.find(i => i.id === activeInjectId) 
    : null;

  function getCountryTelemetry(c: any, injId: string | null, dispRate: number) {
    if (!injId && dispRate === 0.35) {
      return c;
    }

    let post_waa = c.waa;
    let post_t_half = c.t_half_h;
    let effective_disp = dispRate;

    if (injId) {
      const inj = sandboxPayload.injects.find(i => i.id === injId);
      if (inj) {
        const params = inj.shock_parameters;
        post_waa = Math.max(0.01, Math.min(1.0, c.waa * params.waa_multiplier));
        post_t_half = Math.max(1.0, c.t_half_h * params.t_half_decay);
        effective_disp = Math.max(dispRate, params.displacement_rate);
      }
    }

    const scaled_gw = Math.min(1.0, c.gw_clean / 25.0);
    const base = Math.sqrt(scaled_gw * Math.max(0.05, c.sfp));
    const post_csp = Number(Math.min(1.0, (0.75 * post_waa * base) + (0.25 * post_waa)).toFixed(4));

    // Dynamic Archetype Assignment under Shock
    let post_arch = c.archetype;
    if (post_csp >= 0.55 && post_waa >= 0.75) {
      post_arch = 'HYPERSCALE_EMPIRE';
    } else if (post_t_half >= 1000 && post_waa >= 0.50 && c.h_layer2 >= 0.44) {
      post_arch = 'AIR_GAPPED_REDOUBT';
    } else if (c.gw_clean >= 4.5 && post_waa < 0.50 && c.h_layer2 >= 0.42) {
      post_arch = 'ENERGY_MERCENARY';
    } else if (c.h_layer1 >= 0.70 && post_waa <= 0.35 && post_t_half <= 180) {
      post_arch = post_t_half < 24 ? 'ISOLATED_VASSAL_COLLAPSE' : 'EPISTEMIC_VASSAL';
    } else if (post_t_half < 24) {
      post_arch = 'ISOLATED_VASSAL_COLLAPSE';
    }

    // Dynamic T_default under displacement rate
    let post_t_default = c.t_default_months;
    if (effective_disp !== 0.35) {
      const ratio = 0.35 / effective_disp;
      post_t_default = Math.max(3, Math.min(60, Math.round(c.t_default_months * ratio)));
    }

    return {
      ...c,
      waa: Number(post_waa.toFixed(4)),
      csp: post_csp,
      t_half_h: Number(post_t_half.toFixed(1)),
      archetype: post_arch,
      t_default_months: post_t_default,
      effective_disp: effective_disp
    };
  }

  $: displayCountries = sandboxPayload.countries.map(c => 
    getCountryTelemetry(c, activeInjectId, customDisplacementRate)
  );

  $: filteredCountries = displayCountries.filter(c => {
    const matchesSearch = c.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          c.iso.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesArchetype = selectedArchetypeFilter === 'ALL' || c.archetype === selectedArchetypeFilter;
    return matchesSearch && matchesArchetype;
  });

  $: selectedCountry = displayCountries.find(c => c.iso === selectedCountryIso) || displayCountries[0];

  // Archetype distribution counts
  $: archetypeCounts = displayCountries.reduce((acc: Record<string, number>, curr) => {
    acc[curr.archetype] = (acc[curr.archetype] || 0) + 1;
    return acc;
  }, {});

  // Dynamic Deterrence metrics
  $: deterrenceSpeedRatio = (customHumanLatencyMin * 60) / 0.05;
  $: deterrenceDelegationPct = Math.min(99.9, Number((100 * (1 - Math.exp(-0.00008 * deterrenceSpeedRatio))).toFixed(2)));

  // Dynamic Epistemic metrics
  $: epistemicDriftRate = 0.045 * (1.0 - selectedCountry.waa);
  $: epistemicDkl = Number((0.12 * Math.exp(epistemicDriftRate * (customEpistemicMonths / 6.0))).toFixed(3));
  $: epistemicHumanAuditPct = Math.max(1.0, Number((100 * Math.exp(-0.08 * customEpistemicMonths)).toFixed(1)));
  $: epistemicStatus = epistemicDkl < 0.50 ? 'PERMEABLE' : (epistemicDkl < 1.50 ? 'FRACTURED' : 'IRRECONCILABLE');

  // ---------------------------------------------------------------------------
  // ACTIONS
  // ---------------------------------------------------------------------------
  function triggerInject(id: string) {
    if (activeInjectId === id) {
      activeInjectId = null;
    } else {
      activeInjectId = id;
    }
  }

  function resetSimulation() {
    activeInjectId = null;
    customDisplacementRate = 0.35;
    customEpistemicMonths = 24;
    customHumanLatencyMin = 30;
    searchQuery = '';
    selectedArchetypeFilter = 'ALL';
  }

  function selectCountry(iso: string) {
    selectedCountryIso = iso;
  }

  function copyDossierMarkdown() {
    const c = selectedCountry;
    const md = `# HSRI SOVEREIGN SURVIVABILITY DOSSIER: ${c.name} (${c.iso})
- **Horizon**: 2026–2030 Post-Westphalian Superintelligence Transition
- **Active Shock**: ${activeInject ? activeInject.name : 'Baseline (Non-Shocked)'}
- **Post-Westphalian Archetype**: ${c.archetype}
- **Compute Sovereign Power (CSP)**: ${c.csp}
- **Weight Access Autonomy (WAA)**: ${(c.waa * 100).toFixed(1)}%
- **Decoupling Half-Life (T_half)**: ${c.t_half_h} hours
- **Months to Fiscal Insolvency (T_default)**: ${c.t_default_months} months
- **Dedicated Clean Baseload**: ${c.gw_clean} GW
- **Silicon Independence (SFP)**: ${(c.sfp * 100).toFixed(1)}%
- **Layer 1 Adoption**: ${c.h_layer1} | **Layer 2 Sovereignty**: ${c.h_layer2}

## STRATEGIC ASSESSMENT
${getArchetypeAssessment(c.archetype, c.name)}

Published by Humanity Superintelligence Readiness Index (HSRI) — https://humanityreadiness.org/sandbox/
DOI: 10.5281/zenodo.23441742
`;

    navigator.clipboard.writeText(md).then(() => {
      copiedToast = true;
      setTimeout(() => copiedToast = false, 2800);
    });
  }

  function getArchetypeColor(arch: string): string {
    switch (arch) {
      case 'HYPERSCALE_EMPIRE': return 'var(--threat-critical, #b91c1c)';
      case 'ENERGY_MERCENARY': return 'var(--threat-warning, #d97706)';
      case 'EPISTEMIC_VASSAL': return 'var(--threat-telemetry, #4f46e5)';
      case 'AIR_GAPPED_REDOUBT': return 'var(--accent-primary, #1b6756)';
      case 'ISOLATED_VASSAL_COLLAPSE': return '#7f1d1d';
      default: return 'var(--text-muted, #71717a)';
    }
  }

  function getArchetypeAssessment(arch: string, name: string): string {
    switch (arch) {
      case 'HYPERSCALE_EMPIRE':
        return `${name} possesses unipolar compute sovereignty, dedicated gigawatts, and sovereign model weights. Primary strategic risk is internal alignment drift and autonomous agent secession rather than external coercion.`;
      case 'ENERGY_MERCENARY':
        return `${name} holds immense clean power leverage but lacks domestic frontier foundation weights. Retains strong bargaining position by trading physical megawatt-hours for algorithmic quotas.`;
      case 'EPISTEMIC_VASSAL':
        return `${name} exhibits acute digital adoption without sovereign model ownership. Essential administrative, judicial, and financial layers operate as client nodes to foreign compute empires, vulnerable to immediate revocation shock.`;
      case 'AIR_GAPPED_REDOUBT':
        return `${name} maintains superior civilizational resilience through high social trust, decentralized municipal utilities, and robust analog fallback protocols, surviving multi-month cloud quarantines.`;
      case 'ISOLATED_VASSAL_COLLAPSE':
        return `CRITICAL FAILURE: ${name}'s institutional fabric has suffered catastrophic decoupling collapse under the active shock due to near-zero domestic analog redundancy.`;
      default:
        return `${name} operates in the developing cognitive periphery with minimal exposure to direct compute revocation but high vulnerability to secondary supply shocks.`;
    }
  }
</script>

<div class="sandbox-container">
  <!-- Top Cockpit Header -->
  <header class="sandbox-masthead">
    <div class="masthead-badge">
      <span class="live-dot"></span>
      HSRI 2.0 MACRO HORIZON OBSERVED · 2026–2030 GLOBAL ORDER TRANSITION
    </div>
    <h1 class="masthead-title">The Civilizational Transition Sandbox</h1>
    <p class="masthead-desc">
      Empirical econometric, epistemic, and geopolitical simulation modeling the collapse of the 400-year-old Westphalian nation-state under Artificial Superintelligence.
    </p>

    <!-- Global Trilemma Axiom Bar -->
    <div class="trilemma-banner">
      <div class="trilemma-title">THE POST-WESTPHALIAN TRILEMMA:</div>
      <div class="trilemma-vertices">
        <span class="vertex">1. Frontier Capability</span>
        <span class="vertex-sep">⚡</span>
        <span class="vertex">2. Epistemic Sovereignty</span>
        <span class="vertex-sep">⚡</span>
        <span class="vertex">3. Open Global Interconnection</span>
      </div>
      <div class="trilemma-rule">
        *Axiom: No sovereign state can maintain all three. Selection of any two guarantees structural collapse of the third.*
      </div>
    </div>

    <!-- Active Crisis Inject Quick-Triggers -->
    <div class="inject-strip">
      <div class="inject-strip-label">CIVILIZATIONAL CRISIS SHOCK INJECTS:</div>
      <div class="inject-buttons">
        {#each sandboxPayload.injects as inj}
          <button 
            class="inject-btn" 
            class:active={activeInjectId === inj.id}
            on:click={() => triggerInject(inj.id)}
            title={inj.description}
          >
            <span class="inj-code">{inj.id}</span>
            <span class="inj-name">{inj.name.split('(')[0].trim()}</span>
          </button>
        {/each}
        {#if activeInjectId}
          <button class="reset-btn" on:click={resetSimulation}>
            ↺ Reset Baseline
          </button>
        {/if}
      </div>
    </div>

    {#if activeInject}
      <div class="active-shock-alert">
        <div class="shock-indicator">● ACTIVE SHOCK PROPAGATING: {activeInject.id} — {activeInject.name}</div>
        <p class="shock-detail">{activeInject.description}</p>
        <div class="shock-impact"><strong>Systemic Impact:</strong> {activeInject.target_impact}</div>
      </div>
    {/if}
  </header>

  <!-- Sandbox Navigation Tabs -->
  <nav class="sandbox-tabs" aria-label="Simulation Views">
    <button 
      class="tab-btn" 
      class:active={activeTab === 'matrix'} 
      on:click={() => activeTab = 'matrix'}
    >
      🏛️ Layer 1: Compute-Westphalia Matrix ({displayCountries.length})
    </button>
    <button 
      class="tab-btn" 
      class:active={activeTab === 'fiscal'} 
      on:click={() => activeTab = 'fiscal'}
    >
      📉 Layer 2: Post-Labor Fiscal Cliff
    </button>
    <button 
      class="tab-btn" 
      class:active={activeTab === 'epistemic'} 
      on:click={() => activeTab = 'epistemic'}
    >
      👁️ Layer 3: Epistemic Iron Curtain
    </button>
    <button 
      class="tab-btn" 
      class:active={activeTab === 'deterrence'} 
      on:click={() => activeTab = 'deterrence'}
    >
      ⚡ Layer 4: Zero-Human Deterrence
    </button>
  </nav>

  <!-- Main Viewport and Side Inspector Layout -->
  <div class="sandbox-workspace">
    <!-- Viewport Content Area -->
    <div class="sandbox-viewport">
      <!-- ================================================================= -->
      <!-- TAB 1: COMPUTE-WESTPHALIA SCOREBOARD MATRIX                       -->
      <!-- ================================================================= -->
      {#if activeTab === 'matrix'}
        <section class="viewport-section">
          <div class="section-intro">
            <h3>Post-Westphalian Sovereign Power Realignment</h3>
            <p>
              Sovereign power decoupled from geography into four dynamic archetypes determined by dedicated clean baseload gigawatts, silicon fabrication independence, and weight access autonomy.
            </p>
          </div>

          <!-- Archetype Summary KPI Cards -->
          <div class="archetype-kpi-grid">
            <div class="kpi-card" style="border-top: 3px solid var(--threat-critical, #b91c1c);">
              <div class="kpi-label">Hyperscale Empires</div>
              <div class="kpi-val" style="color: var(--threat-critical, #b91c1c);">{archetypeCounts['HYPERSCALE_EMPIRE'] || 0}</div>
              <div class="kpi-sub">Unipolar compute sovereigns</div>
            </div>
            <div class="kpi-card" style="border-top: 3px solid var(--threat-warning, #d97706);">
              <div class="kpi-label">Energy Mercenaries</div>
              <div class="kpi-val" style="color: var(--threat-warning, #d97706);">{archetypeCounts['ENERGY_MERCENARY'] || 0}</div>
              <div class="kpi-sub">Power-for-model traders</div>
            </div>
            <div class="kpi-card" style="border-top: 3px solid var(--threat-telemetry, #4f46e5);">
              <div class="kpi-label">Epistemic Vassals</div>
              <div class="kpi-val" style="color: var(--threat-telemetry, #4f46e5);">{archetypeCounts['EPISTEMIC_VASSAL'] || 0}</div>
              <div class="kpi-sub">Zero-sovereign-weight states</div>
            </div>
            <div class="kpi-card" style="border-top: 3px solid var(--accent-primary, #1b6756);">
              <div class="kpi-label">Air-Gapped Redoubts</div>
              <div class="kpi-val" style="color: var(--accent-primary, #1b6756);">{archetypeCounts['AIR_GAPPED_REDOUBT'] || 0}</div>
              <div class="kpi-sub">Analog & decoupling resilience</div>
            </div>
            {#if archetypeCounts['ISOLATED_VASSAL_COLLAPSE']}
              <div class="kpi-card" style="border-top: 3px solid #7f1d1d; background: #fff1f2;">
                <div class="kpi-label">Systemic Collapses</div>
                <div class="kpi-val" style="color: #7f1d1d;">{archetypeCounts['ISOLATED_VASSAL_COLLAPSE']}</div>
                <div class="kpi-sub">Decoupling failure under shock</div>
              </div>
            {/if}
          </div>

          <!-- Filter & Search Bar -->
          <div class="matrix-controls">
            <div class="search-box">
              <input 
                type="text" 
                placeholder="Search sovereign nation by name or ISO3..." 
                bind:value={searchQuery}
                class="search-input"
              />
            </div>
            <div class="filter-box">
              <select bind:value={selectedArchetypeFilter} class="filter-select">
                <option value="ALL">All Sovereign Archetypes</option>
                <option value="HYPERSCALE_EMPIRE">Hyperscale Empires</option>
                <option value="ENERGY_MERCENARY">Energy Mercenaries</option>
                <option value="EPISTEMIC_VASSAL">Epistemic Vassals</option>
                <option value="AIR_GAPPED_REDOUBT">Air-Gapped Redoubts</option>
                {#if archetypeCounts['ISOLATED_VASSAL_COLLAPSE']}
                  <option value="ISOLATED_VASSAL_COLLAPSE">Systemic Collapses</option>
                {/if}
              </select>
            </div>
          </div>

          <!-- Sovereign Scoreboard Table -->
          <div class="table-container">
            <table class="scoreboard-table">
              <thead>
                <tr>
                  <th>Nation</th>
                  <th>Dedicated GW</th>
                  <th>Silicon (SFP)</th>
                  <th>Weight Autonomy</th>
                  <th>Compute Power (CSP)</th>
                  <th>Decoupling (T_half)</th>
                  <th>Fiscal Default</th>
                  <th>Sovereign Archetype</th>
                </tr>
              </thead>
              <tbody>
                {#each filteredCountries as c}
                  <tr 
                    class:selected={c.iso === selectedCountryIso}
                    on:click={() => selectCountry(c.iso)}
                  >
                    <td class="nation-cell">
                      <strong class="nation-name">{c.name}</strong>
                      <span class="nation-iso">{c.iso}</span>
                    </td>
                    <td>{c.gw_clean} GW</td>
                    <td>{(c.sfp * 100).toFixed(0)}%</td>
                    <td>
                      <div class="meter-bar">
                        <div class="meter-fill" style="width: {c.waa * 100}%; background: {getArchetypeColor(c.archetype)};"></div>
                      </div>
                      <span class="meter-num">{(c.waa * 100).toFixed(0)}%</span>
                    </td>
                    <td>
                      <strong class="csp-val">{c.csp}</strong>
                    </td>
                    <td>{c.t_half_h} hrs</td>
                    <td>
                      <span class="default-badge" class:urgent={c.t_default_months <= 24}>
                        {c.t_default_months >= 60 ? 'Stable' : `${c.t_default_months} mo`}
                      </span>
                    </td>
                    <td>
                      <span class="archetype-badge" style="background: {getArchetypeColor(c.archetype)}20; color: {getArchetypeColor(c.archetype)}; border: 1px solid {getArchetypeColor(c.archetype)}50;">
                        {c.archetype.replace(/_/g, ' ')}
                      </span>
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </section>

      <!-- ================================================================= -->
      <!-- TAB 2: POST-LABOR FISCAL CLIFF                                    -->
      <!-- ================================================================= -->
      {:else if activeTab === 'fiscal'}
        <section class="viewport-section">
          <div class="section-intro">
            <h3>The Post-Labor Fiscal Insolvency Clock</h3>
            <p>
              Sovereign debt depends entirely on taxing biological human labor. When autonomous agents displace high-income cognitive professions at scale, the tax base collapses while fixed entitlement and debt-servicing outlays compound.
            </p>
          </div>

          <!-- Interactive Displacement Velocity Slider -->
          <div class="slider-control-card">
            <div class="slider-header">
              <label for="disp-slider" class="slider-label">
                Cognitive Labor Displacement Velocity (λ): <strong>{(customDisplacementRate * 100).toFixed(0)}% annual displacement</strong>
              </label>
              <span class="slider-hint">Controls annual substitution rate of legal, software, finance, and engineering salaries.</span>
            </div>
            <input 
              id="disp-slider"
              type="range" 
              min="0.10" 
              max="0.80" 
              step="0.05" 
              bind:value={customDisplacementRate}
              class="range-slider"
            />
            <div class="slider-ticks">
              <span>10% (Slow Advisory)</span>
              <span>35% (Baseline 2027)</span>
              <span>60% (Frontier Agentic Surge)</span>
              <span>80% (Recursive Singularity)</span>
            </div>
          </div>

          <!-- Fiscal Default Urgency Tiers -->
          <div class="fiscal-tiers-grid">
            <div class="fiscal-tier-card tier-critical">
              <div class="tier-head">Immediate Insolvency Window (≤ 18 Months)</div>
              <div class="tier-desc">Tax revenue drops below sovereign bond debt-servicing requirements. Forced monetization or default.</div>
              <div class="tier-country-list">
                {#each displayCountries.filter(c => c.t_default_months <= 18) as c}
                  <button class="tier-chip" on:click={() => selectCountry(c.iso)}>
                    {c.iso} ({c.t_default_months}m)
                  </button>
                {/each}
              </div>
            </div>

            <div class="fiscal-tier-card tier-warning">
              <div class="tier-head">Elevated Vulnerability Window (21–36 Months)</div>
              <div class="tier-desc">Severe budgetary deficit pressure; emergency compute nationalization or severe social cuts required.</div>
              <div class="tier-country-list">
                {#each displayCountries.filter(c => c.t_default_months > 18 && c.t_default_months <= 36) as c}
                  <button class="tier-chip" on:click={() => selectCountry(c.iso)}>
                    {c.iso} ({c.t_default_months}m)
                  </button>
                {/each}
              </div>
            </div>

            <div class="fiscal-tier-card tier-stable">
              <div class="tier-head">Fiscal Resilience Buffer (≥ 48 Months)</div>
              <div class="tier-desc">Low public debt-to-GDP ratio and sovereign wealth capital cushions delay insolvency.</div>
              <div class="tier-country-list">
                {#each displayCountries.filter(c => c.t_default_months >= 48) as c}
                  <button class="tier-chip" on:click={() => selectCountry(c.iso)}>
                    {c.iso}
                  </button>
                {/each}
              </div>
            </div>
          </div>

          <!-- Selected Nation Fiscal Trajectory Breakdown -->
          <div class="selected-fiscal-breakdown">
            <h4>Fiscal Stress Profile: {selectedCountry.name} ({selectedCountry.iso})</h4>
            <div class="fiscal-stats-row">
              <div class="fstat">
                <span class="fstat-label">Gross Debt / GDP</span>
                <span class="fstat-val">{(selectedCountry.debt_gdp * 100).toFixed(0)}%</span>
              </div>
              <div class="fstat">
                <span class="fstat-label">Labor Tax Revenue Share</span>
                <span class="fstat-val">{(selectedCountry.labor_tax * 100).toFixed(0)}%</span>
              </div>
              <div class="fstat">
                <span class="fstat-label">Insolvency Horizon</span>
                <span class="fstat-val" style="color: {selectedCountry.t_default_months <= 24 ? 'var(--threat-critical)' : 'var(--accent-primary)'};">
                  {selectedCountry.t_default_months >= 60 ? 'Buffer Sustained' : `Month ${selectedCountry.t_default_months}`}
                </span>
              </div>
            </div>

            <div class="trajectory-table-wrap">
              <table class="trajectory-table">
                <thead>
                  <tr>
                    <th>Quarter</th>
                    <th>Elapsed Months</th>
                    <th>Tax Base Revenue Loss</th>
                    <th>Fiscal Deficit Pressure</th>
                    <th>Solvency Status</th>
                  </tr>
                </thead>
                <tbody>
                  {#each selectedCountry.quarterly_fiscal_trajectory.slice(0, 9) as step, idx}
                    <tr class:insolvent={step.is_insolvent}>
                      <td>Q{idx}</td>
                      <td>Month {step.month}</td>
                      <td>-{step.tax_loss_pct}%</td>
                      <td>+{step.deficit_pressure_pct}%</td>
                      <td>
                        <span class="solvency-badge" class:alert={step.is_insolvent}>
                          {step.is_insolvent ? 'INSOLVENT' : 'SOLVENT'}
                        </span>
                      </td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
        </section>

      <!-- ================================================================= -->
      <!-- TAB 3: EPISTEMIC IRON CURTAIN                                     -->
      <!-- ================================================================= -->
      {:else if activeTab === 'epistemic'}
        <section class="viewport-section">
          <div class="section-intro">
            <h3>The Epistemic Iron Curtain & Synthetic Reality Drift</h3>
            <p>
              When competing geopolitical blocs deploy closed-weight foundation models, latent world-models permanently diverge. Because human verification speed has collapsed (CORS 10.0), no human court or summit can verify the other side's synthetic claims.
            </p>
          </div>

          <!-- Time Horizon Slider -->
          <div class="slider-control-card">
            <div class="slider-header">
              <label for="ep-slider" class="slider-label">
                Simulation Horizon: <strong>Month {customEpistemicMonths} ({Math.round(customEpistemicMonths / 12 * 10) / 10} Years Post-Takeoff)</strong>
              </label>
              <span class="slider-hint">Tracks compounding divergence across legal interpretation, historical consensus, and intelligence synthesis.</span>
            </div>
            <input 
              id="ep-slider"
              type="range" 
              min="0" 
              max="48" 
              step="6" 
              bind:value={customEpistemicMonths}
              class="range-slider"
            />
            <div class="slider-ticks">
              <span>Month 0 (Shared Baseline)</span>
              <span>Month 12 (Fractured Proofs)</span>
              <span>Month 24 (The Divergence Horizon)</span>
              <span>Month 48 (Total Incommensurability)</span>
            </div>
          </div>

          <!-- Epistemic Boundary Cards -->
          <div class="epistemic-dashboard">
            <div class="epistemic-card">
              <div class="ec-label">Semantic Divergence (D_KL)</div>
              <div class="ec-val" style="color: {epistemicStatus === 'IRRECONCILABLE' ? 'var(--threat-critical)' : 'var(--threat-telemetry)'};">
                {epistemicDkl}
              </div>
              <div class="ec-sub">Latent space drift between sovereign model clusters</div>
            </div>

            <div class="epistemic-card">
              <div class="ec-label">Human Auditability Ratio</div>
              <div class="ec-val">{epistemicHumanAuditPct}%</div>
              <div class="ec-sub">Share of machine reasoning verifiable by human experts</div>
            </div>

            <div class="epistemic-card">
              <div class="ec-label">Verification Boundary Status</div>
              <div class="ec-status-badge" data-status={epistemicStatus}>
                {epistemicStatus}
              </div>
              <div class="ec-sub">
                {epistemicStatus === 'PERMEABLE' ? 'Diplomatic arbitration feasible' : 
                 (epistemicStatus === 'FRACTURED' ? 'Severe dispute deadlocks; sycophancy' : 'International law & treaties mathematically obsolete')}
              </div>
            </div>
          </div>

          <!-- Divergence Comparison Analysis -->
          <div class="epistemic-comparison-panel">
            <h4>Bifurcation Anatomy: Sovereign Redoubts vs Epistemic Vassals</h4>
            <div class="comparison-grid">
              <div class="comp-col">
                <h5>Sovereign Model Enclaves (WAA ≥ 0.50)</h5>
                <p>Nations like Switzerland, Norway, or Hyperscale Empires holding local weights retain domestic epistemic continuity. They can audit internal administrative decisions without foreign cloud interference.</p>
                <div class="comp-status green">Epistemic Inviolability Retained</div>
              </div>
              <div class="comp-col">
                <h5>Epistemic Vassal States (WAA ≤ 0.25)</h5>
                <p>Nations like Singapore, UK, and Germany run judicial, medical, and administrative workflows on closed foreign weights. When the foreign model updates its latent priors, the vassal nation's institutional logic silently morphs.</p>
                <div class="comp-status red">Epistemic Colonization Active</div>
              </div>
            </div>
          </div>
        </section>

      <!-- ================================================================= -->
      <!-- TAB 4: ZERO-HUMAN DETERRENCE LADDER                               -->
      <!-- ================================================================= -->
      {:else if activeTab === 'deterrence'}
        <section class="viewport-section">
          <div class="section-intro">
            <h3>Sub-Second Deterrence & The Zero-Human Strike Frontier</h3>
            <p>
              In nuclear deterrence, human leaders had 20 minutes to verify missile telemetry. In machine-speed cyber warfare and autonomous kinetic swarms, strikes peak and resolve in milliseconds. Maintaining human-in-the-loop authorization guarantees military defeat.
            </p>
          </div>

          <!-- Latency Asymmetry Interactive Simulator -->
          <div class="slider-control-card">
            <div class="slider-header">
              <label for="lat-slider" class="slider-label">
                Human Constitutional Command Latency: <strong>{customHumanLatencyMin} Minutes</strong>
              </label>
              <span class="slider-hint">Time required for human national security staff to authenticate data and authorize response.</span>
            </div>
            <input 
              id="lat-slider"
              type="range" 
              min="5" 
              max="180" 
              step="5" 
              bind:value={customHumanLatencyMin}
              class="range-slider"
            />
            <div class="slider-ticks">
              <span>5 Min (Emergency Direct Line)</span>
              <span>30 Min (Cabinet Escalation)</span>
              <span>60 Min (National Security Council)</span>
              <span>180 Min (Parliamentary Review)</span>
            </div>
          </div>

          <!-- Speed Asymmetry Results -->
          <div class="deterrence-gauge-card">
            <div class="gauge-header">
              <div class="g-stat">
                <span class="g-label">Human Authorization Speed:</span>
                <span class="g-val">{(customHumanLatencyMin * 60).toLocaleString()} seconds</span>
              </div>
              <div class="g-vs">VS</div>
              <div class="g-stat">
                <span class="g-label">Autonomous Attack Cycle:</span>
                <span class="g-val machine">0.050 seconds (50 ms)</span>
              </div>
            </div>

            <div class="speed-ratio-display">
              <div class="ratio-num">{Math.round(deterrenceSpeedRatio).toLocaleString()}×</div>
              <div class="ratio-caption">Machine Speed Tactical Superiority Ratio</div>
            </div>

            <div class="delegation-result-box">
              <div class="del-pct-label">Mandatory Pre-Delegation Probability:</div>
              <div class="del-pct-val" style="color: var(--threat-critical, #b91c1c);">{deterrenceDelegationPct}%</div>
              <div class="del-verdict">
                <strong>TACTICAL VERDICT:</strong>
                {#if deterrenceDelegationPct >= 95.0}
                  <span class="verdict-red">HUMAN COMMAND SURRENDERED — Maintaining human veto guarantees defensive annihilation. Absolute launch authority must be delegated to autonomous models.</span>
                {:else}
                  <span class="verdict-amber">HAZARDOUS DELAY — Human commanders operate within critical vulnerability window.</span>
                {/if}
              </div>
            </div>
          </div>
        </section>
      {/if}
    </div>

    <!-- =================================================================== -->
    <!-- RIGHT SIDE: THE SOVEREIGN SURVIVABILITY INSPECTOR (DETAIL DOSSIER)  -->
    <!-- =================================================================== -->
    <aside class="sandbox-inspector">
      <div class="inspector-header">
        <span class="inspector-badge">SOVEREIGN DOSSIER</span>
        <h3 class="inspector-nation">{selectedCountry.name}</h3>
        <span class="inspector-iso">{selectedCountry.iso}</span>
      </div>

      <!-- Live Archetype Badge -->
      <div class="inspector-archetype" style="background: {getArchetypeColor(selectedCountry.archetype)}20; border: 1px solid {getArchetypeColor(selectedCountry.archetype)}50; color: {getArchetypeColor(selectedCountry.archetype)};">
        {selectedCountry.archetype.replace(/_/g, ' ')}
      </div>

      <!-- Core Metrics Grid -->
      <div class="inspector-metrics-grid">
        <div class="im-card">
          <span class="im-label">Compute Sovereign Power</span>
          <span class="im-val">{selectedCountry.csp}</span>
        </div>
        <div class="im-card">
          <span class="im-label">Weight Access Autonomy</span>
          <span class="im-val">{(selectedCountry.waa * 100).toFixed(0)}%</span>
        </div>
        <div class="im-card">
          <span class="im-label">Decoupling Half-Life</span>
          <span class="im-val">{selectedCountry.t_half_h} hrs</span>
        </div>
        <div class="im-card">
          <span class="im-label">Months to Default</span>
          <span class="im-val">{selectedCountry.t_default_months >= 60 ? 'Buffer' : `${selectedCountry.t_default_months}m`}</span>
        </div>
        <div class="im-card">
          <span class="im-label">Dedicated Clean Baseload</span>
          <span class="im-val">{selectedCountry.gw_clean} GW</span>
        </div>
        <div class="im-card">
          <span class="im-label">Silicon Fab Inviolability</span>
          <span class="im-val">{(selectedCountry.sfp * 100).toFixed(0)}%</span>
        </div>
      </div>

      <!-- Qualitative Strategic Assessment -->
      <div class="inspector-assessment">
        <h4>Strategic Assessment</h4>
        <p class="assessment-text">
          {getArchetypeAssessment(selectedCountry.archetype, selectedCountry.name)}
        </p>
      </div>

      <!-- Active Shock Diagnostics for this Country -->
      {#if activeInject}
        <div class="inspector-shock-box">
          <h4>Active Shock Impact ({activeInject.id})</h4>
          <p class="shock-summary">
            Under <em>{activeInject.name}</em>, {selectedCountry.name}'s weight autonomy operates at {(selectedCountry.waa * 100).toFixed(1)}%, with decoupling half-life reduced to {selectedCountry.t_half_h}h.
          </p>
        </div>
      {/if}

      <!-- 1-Click Export Dossier Button -->
      <div class="inspector-actions">
        <button class="export-btn" on:click={copyDossierMarkdown}>
          {#if copiedToast}
            ✓ Copied Dossier Markdown!
          {:else}
            📋 Copy Sovereign Dossier (Markdown)
          {/if}
        </button>
      </div>
    </aside>
  </div>
</div>

<style>
  .sandbox-container {
    padding: 1.5rem 0 3.5rem;
    color: var(--text-primary);
  }

  /* Masthead */
  .sandbox-masthead {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 2rem 2.25rem;
    margin-bottom: 1.75rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  }

  .masthead-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    background: var(--accent-primary-glow);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 0.85rem;
  }

  .live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--threat-critical, #b91c1c);
    box-shadow: 0 0 6px var(--threat-critical, #b91c1c);
    animation: pulse 1.8s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  .masthead-title {
    font-family: var(--font-family-display);
    font-size: clamp(1.85rem, 3.5vw, 2.5rem);
    font-weight: 700;
    line-height: 1.15;
    margin: 0 0 0.75rem;
    color: var(--text-primary);
  }

  .masthead-desc {
    font-size: 1.05rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 900px;
    margin: 0 0 1.5rem;
  }

  /* Trilemma Banner */
  .trilemma-banner {
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-medium);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
  }

  .trilemma-title {
    font-family: var(--font-family-mono);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
  }

  .trilemma-vertices {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.75rem;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--accent-primary);
    margin-bottom: 0.4rem;
  }

  .vertex-sep {
    color: var(--threat-warning, #d97706);
  }

  .trilemma-rule {
    font-family: var(--font-family-mono);
    font-size: 0.76rem;
    color: var(--text-muted);
  }

  /* Inject Strip */
  .inject-strip {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  .inject-strip-label {
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--text-muted);
  }

  .inject-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
  }

  .inject-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 0.9rem;
    border-radius: 6px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .inject-btn:hover {
    border-color: var(--accent-primary);
    background: var(--bg-surface-sunken);
  }

  .inject-btn.active {
    background: var(--threat-critical, #b91c1c);
    color: #ffffff;
    border-color: var(--threat-critical, #b91c1c);
    box-shadow: 0 2px 10px rgba(185, 28, 28, 0.25);
  }

  .inj-code {
    font-family: var(--font-family-mono);
    font-weight: 700;
    opacity: 0.85;
  }

  .reset-btn {
    padding: 0.45rem 0.85rem;
    border-radius: 6px;
    border: 1px solid var(--border-medium);
    background: transparent;
    color: var(--text-muted);
    font-size: 0.8rem;
    cursor: pointer;
  }

  .reset-btn:hover {
    color: var(--text-primary);
    border-color: var(--text-secondary);
  }

  .active-shock-alert {
    margin-top: 1.25rem;
    padding: 1rem 1.25rem;
    border-radius: 8px;
    background: #fdf2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
  }

  .shock-indicator {
    font-family: var(--font-family-mono);
    font-size: 0.82rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
  }

  .shock-detail {
    font-size: 0.9rem;
    line-height: 1.5;
    margin: 0 0 0.5rem;
    color: #7f1d1d;
  }

  .shock-impact {
    font-size: 0.85rem;
    color: #991b1b;
  }

  /* Navigation Tabs */
  .sandbox-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 0.5rem;
  }

  .tab-btn {
    padding: 0.65rem 1.15rem;
    border-radius: 8px 8px 0 0;
    border: 1px solid transparent;
    background: transparent;
    color: var(--text-secondary);
    font-size: 0.92rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .tab-btn:hover {
    color: var(--text-primary);
    background: var(--bg-surface-sunken);
  }

  .tab-btn.active {
    background: var(--bg-surface);
    color: var(--accent-primary);
    border: 1px solid var(--border-subtle);
    border-bottom-color: var(--bg-surface);
    font-weight: 700;
  }

  /* Workspace Layout */
  .sandbox-workspace {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 1.5rem;
    align-items: start;
  }

  @media (max-width: 1024px) {
    .sandbox-workspace {
      grid-template-columns: 1fr;
    }
  }

  .sandbox-viewport {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.75rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  }

  .section-intro {
    margin-bottom: 1.5rem;
  }

  .section-intro h3 {
    font-family: var(--font-family-display);
    font-size: 1.45rem;
    margin: 0 0 0.45rem;
  }

  .section-intro p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
  }

  /* Archetype KPI Grid */
  .archetype-kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 0.85rem;
    margin-bottom: 1.5rem;
  }

  .kpi-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.85rem 1rem;
  }

  .kpi-label {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
  }

  .kpi-val {
    font-family: var(--font-family-mono);
    font-size: 1.65rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.25rem;
  }

  .kpi-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  /* Table Controls */
  .matrix-controls {
    display: flex;
    gap: 0.85rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
  }

  .search-input, .filter-select {
    padding: 0.5rem 0.85rem;
    border-radius: 6px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    font-size: 0.85rem;
  }

  .search-box {
    flex: 1;
    min-width: 220px;
  }

  .search-input {
    width: 100%;
  }

  /* Table */
  .table-container {
    overflow-x: auto;
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
  }

  .scoreboard-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    text-align: left;
  }

  .scoreboard-table th {
    background: var(--bg-surface-sunken);
    padding: 0.75rem 0.85rem;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--border-medium);
  }

  .scoreboard-table td {
    padding: 0.75rem 0.85rem;
    border-bottom: 1px solid var(--border-subtle);
    color: var(--text-primary);
  }

  .scoreboard-table tbody tr {
    cursor: pointer;
    transition: background 0.15s ease;
  }

  .scoreboard-table tbody tr:hover {
    background: var(--bg-surface-sunken);
  }

  .scoreboard-table tbody tr.selected {
    background: var(--accent-primary-glow);
  }

  .nation-cell {
    display: flex;
    flex-direction: column;
  }

  .nation-name {
    font-weight: 700;
  }

  .nation-iso {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .meter-bar {
    width: 55px;
    height: 5px;
    background: var(--border-subtle);
    border-radius: 3px;
    display: inline-block;
    vertical-align: middle;
    margin-right: 0.4rem;
    overflow: hidden;
  }

  .meter-fill {
    height: 100%;
  }

  .meter-num {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
  }

  .csp-val {
    font-family: var(--font-family-mono);
    font-weight: 800;
    color: var(--accent-primary);
  }

  .default-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    background: var(--bg-surface-sunken);
  }

  .default-badge.urgent {
    background: #fee2e2;
    color: #991b1b;
    font-weight: 700;
  }

  .archetype-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    text-transform: uppercase;
  }

  /* Slider Card */
  .slider-control-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 8px;
    padding: 1.25rem;
    margin-bottom: 1.75rem;
  }

  .slider-header {
    display: flex;
    flex-direction: column;
    margin-bottom: 0.85rem;
  }

  .slider-label {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.2rem;
  }

  .slider-hint {
    font-size: 0.78rem;
    color: var(--text-muted);
  }

  .range-slider {
    width: 100%;
    accent-color: var(--accent-primary);
    margin-bottom: 0.5rem;
  }

  .slider-ticks {
    display: flex;
    justify-content: space-between;
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    color: var(--text-muted);
  }

  /* Fiscal Tiers */
  .fiscal-tiers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .fiscal-tier-card {
    border-radius: 8px;
    padding: 1.15rem;
    border: 1px solid var(--border-subtle);
  }

  .tier-critical {
    background: #fff1f2;
    border-color: #fecdd3;
  }

  .tier-warning {
    background: #fffbeb;
    border-color: #fde68a;
  }

  .tier-stable {
    background: #f0fdf4;
    border-color: #bbf7d0;
  }

  .tier-head {
    font-family: var(--font-family-mono);
    font-size: 0.8rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
  }

  .tier-critical .tier-head { color: #991b1b; }
  .tier-warning .tier-head { color: #b45309; }
  .tier-stable .tier-head { color: #166534; }

  .tier-desc {
    font-size: 0.76rem;
    line-height: 1.4;
    color: var(--text-secondary);
    margin-bottom: 0.85rem;
  }

  .tier-country-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .tier-chip {
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    border: 1px solid rgba(0,0,0,0.1);
    background: #ffffff;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 600;
    cursor: pointer;
  }

  .tier-chip:hover {
    background: var(--bg-surface-sunken);
  }

  /* Trajectory breakdown */
  .selected-fiscal-breakdown {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1.25rem;
  }

  .selected-fiscal-breakdown h4 {
    margin: 0 0 1rem;
    font-size: 1.1rem;
  }

  .fiscal-stats-row {
    display: flex;
    gap: 2rem;
    margin-bottom: 1.25rem;
    flex-wrap: wrap;
  }

  .fstat {
    display: flex;
    flex-direction: column;
  }

  .fstat-label {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .fstat-val {
    font-family: var(--font-family-mono);
    font-size: 1.35rem;
    font-weight: 800;
  }

  .trajectory-table-wrap {
    overflow-x: auto;
  }

  .trajectory-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
  }

  .trajectory-table th {
    background: var(--bg-surface-sunken);
    padding: 0.5rem 0.75rem;
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    border-bottom: 1px solid var(--border-medium);
  }

  .trajectory-table td {
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--border-subtle);
  }

  .trajectory-table tr.insolvent {
    background: #fff1f2;
    color: #991b1b;
  }

  .solvency-badge {
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 700;
    color: #166534;
  }

  .solvency-badge.alert {
    color: #991b1b;
  }

  /* Epistemic Tab */
  .epistemic-dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.75rem;
  }

  .epistemic-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1.25rem;
  }

  .ec-label {
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
  }

  .ec-val {
    font-family: var(--font-family-mono);
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.4rem;
  }

  .ec-status-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 1.15rem;
    font-weight: 800;
    padding: 0.35rem 0.85rem;
    border-radius: 6px;
    margin-bottom: 0.4rem;
  }

  .ec-status-badge[data-status="PERMEABLE"] { background: #dcfce7; color: #166534; }
  .ec-status-badge[data-status="FRACTURED"] { background: #fef3c7; color: #b45309; }
  .ec-status-badge[data-status="IRRECONCILABLE"] { background: #fee2e2; color: #991b1b; }

  .ec-sub {
    font-size: 0.76rem;
    color: var(--text-muted);
  }

  .epistemic-comparison-panel {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1.5rem;
  }

  .epistemic-comparison-panel h4 {
    margin: 0 0 1rem;
  }

  .comparison-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
  }

  @media (max-width: 640px) {
    .comparison-grid { grid-template-columns: 1fr; }
  }

  .comp-col {
    background: var(--bg-surface-sunken);
    padding: 1rem;
    border-radius: 6px;
  }

  .comp-col h5 {
    margin: 0 0 0.5rem;
    font-size: 0.95rem;
  }

  .comp-col p {
    font-size: 0.85rem;
    line-height: 1.5;
    margin: 0 0 0.75rem;
    color: var(--text-secondary);
  }

  .comp-status {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    display: inline-block;
  }

  .comp-status.green { background: #dcfce7; color: #166534; }
  .comp-status.red { background: #fee2e2; color: #991b1b; }

  /* Deterrence Tab */
  .deterrence-gauge-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1.5rem;
  }

  .gauge-header {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1.25rem;
  }

  .g-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .g-label {
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    color: var(--text-muted);
  }

  .g-val {
    font-family: var(--font-family-mono);
    font-size: 1.35rem;
    font-weight: 800;
  }

  .g-val.machine {
    color: var(--threat-critical, #b91c1c);
  }

  .g-vs {
    font-family: var(--font-family-mono);
    font-weight: 800;
    color: var(--threat-warning, #d97706);
  }

  .speed-ratio-display {
    text-align: center;
    margin-bottom: 1.5rem;
  }

  .ratio-num {
    font-family: var(--font-family-mono);
    font-size: 2.75rem;
    font-weight: 900;
    color: var(--threat-critical, #b91c1c);
    line-height: 1;
    margin-bottom: 0.25rem;
  }

  .ratio-caption {
    font-family: var(--font-family-mono);
    font-size: 0.8rem;
    color: var(--text-secondary);
  }

  .delegation-result-box {
    background: #fff1f2;
    border: 1px solid #fecaca;
    border-radius: 8px;
    padding: 1.25rem;
    text-align: center;
  }

  .del-pct-label {
    font-family: var(--font-family-mono);
    font-size: 0.8rem;
    font-weight: 700;
    color: #7f1d1d;
  }

  .del-pct-val {
    font-family: var(--font-family-mono);
    font-size: 2.5rem;
    font-weight: 900;
    line-height: 1.1;
    margin: 0.25rem 0 0.5rem;
  }

  .del-verdict {
    font-size: 0.88rem;
    line-height: 1.5;
  }

  .verdict-red {
    color: #991b1b;
  }

  /* Side Inspector */
  .sandbox-inspector {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.5rem;
    position: sticky;
    top: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  }

  .inspector-header {
    margin-bottom: 0.85rem;
  }

  .inspector-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--accent-primary);
    background: var(--accent-primary-glow);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    margin-bottom: 0.4rem;
  }

  .inspector-nation {
    font-family: var(--font-family-display);
    font-size: 1.55rem;
    margin: 0 0 0.2rem;
    line-height: 1.15;
  }

  .inspector-iso {
    font-family: var(--font-family-mono);
    font-size: 0.8rem;
    color: var(--text-muted);
  }

  .inspector-archetype {
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 700;
    text-align: center;
    padding: 0.4rem 0.6rem;
    border-radius: 6px;
    margin-bottom: 1.25rem;
    text-transform: uppercase;
  }

  .inspector-metrics-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.65rem;
    margin-bottom: 1.25rem;
  }

  .im-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 0.65rem;
  }

  .im-label {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-bottom: 0.2rem;
  }

  .im-val {
    font-family: var(--font-family-mono);
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text-primary);
  }

  .inspector-assessment {
    background: var(--bg-surface-sunken);
    border-radius: 6px;
    padding: 0.85rem;
    margin-bottom: 1.25rem;
  }

  .inspector-assessment h4 {
    margin: 0 0 0.4rem;
    font-size: 0.85rem;
  }

  .assessment-text {
    font-size: 0.82rem;
    line-height: 1.5;
    margin: 0;
    color: var(--text-secondary);
  }

  .inspector-shock-box {
    background: #fdf2f2;
    border: 1px solid #fecaca;
    border-radius: 6px;
    padding: 0.85rem;
    margin-bottom: 1.25rem;
    color: #991b1b;
  }

  .inspector-shock-box h4 {
    margin: 0 0 0.35rem;
    font-size: 0.82rem;
    font-family: var(--font-family-mono);
  }

  .shock-summary {
    font-size: 0.8rem;
    line-height: 1.45;
    margin: 0;
  }

  .export-btn {
    width: 100%;
    padding: 0.65rem;
    border-radius: 6px;
    border: 1px solid var(--accent-primary);
    background: var(--accent-primary);
    color: #ffffff;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .export-btn:hover {
    background: var(--accent-primary-hover);
  }
</style>
