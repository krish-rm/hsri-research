<script lang="ts">
  import { onDestroy } from 'svelte';
  import sandboxPayload from '../data/civilizational_sandbox_payload.json';

  // ---------------------------------------------------------------------------
  // NAVIGATION & PRESENTATION MODE
  // ---------------------------------------------------------------------------
  // 'explainer' = Visual, animated, intuitive 2-minute walkthrough for everyone
  // 'terminal' = Full econometric matrices, formulas, and 40-nation data table
  let currentView: 'explainer' | 'terminal' = 'explainer';

  // Interactive Trilemma Selector (Explainer Mode)
  // Options: 'vassal' (Capability + Integration) | 'fortress' (Capability + Sovereignty) | 'redoubt' (Sovereignty + Integration)
  let selectedTrilemmaChoice: 'vassal' | 'fortress' | 'redoubt' = 'vassal';

  // Interactive Shock Injects (Default to INJ-01 so a scenario is running immediately)
  let activeInjectId: string | null = 'INJ-01';
  let selectedCountryIso = 'SGP';
  let searchQuery = '';
  let selectedArchetypeFilter = 'ALL';

  // Interactive 72-Hour Transition Timeline State
  let simulationHour = 0;
  let isPlaying = false;
  let simulationInterval: any = null;

  function toggleSimulation() {
    if (isPlaying) {
      pauseSimulation();
    } else {
      playSimulation();
    }
  }

  function playSimulation() {
    if (simulationHour >= 72) simulationHour = 0;
    isPlaying = true;
    clearInterval(simulationInterval);
    simulationInterval = setInterval(() => {
      if (simulationHour < 72) {
        simulationHour += 2;
      } else {
        pauseSimulation();
      }
    }, 120);
  }

  function pauseSimulation() {
    isPlaying = false;
    clearInterval(simulationInterval);
  }

  function resetSimulationHour() {
    pauseSimulation();
    simulationHour = 0;
  }

  onDestroy(() => {
    clearInterval(simulationInterval);
  });

  // Precomputed Rank Mappings (Adoption L1 vs Sovereign Decoupling T_half)
  $: adoptionRanks = (() => {
    const sorted = [...sandboxPayload.countries].sort((a, b) => b.h_layer1 - a.h_layer1);
    const map: Record<string, number> = {};
    sorted.forEach((c, idx) => map[c.iso] = idx + 1);
    return map;
  })();

  $: sovereignRanks = (() => {
    const sorted = [...displayCountries].sort((a, b) => b.t_half_h - a.t_half_h);
    const map: Record<string, number> = {};
    sorted.forEach((c, idx) => map[c.iso] = idx + 1);
    return map;
  })();

  const PRESET_COUNTRIES = [
    { iso: 'SGP', name: 'Singapore', note: 'Top Adoption (-40 Ranks)' },
    { iso: 'USA', name: 'United States', note: 'Hyperscale (-37 Ranks)' },
    { iso: 'NOR', name: 'Norway', note: 'Air-Gapped (#1 Resilient)' },
    { iso: 'CHE', name: 'Switzerland', note: 'Analog Redoubt (#3)' },
    { iso: 'DEU', name: 'Germany', note: 'Industrial Core (#8)' },
    { iso: 'KOR', name: 'South Korea', note: 'Semiconductors (-32 Ranks)' }
  ];

  const SHOCK_PRECEDENTS: Record<string, { id: string; name: string; author: string }> = {
    'INJ-01': { id: 'SC-04', name: 'The Vulnerable World Hypothesis', author: 'Nick Bostrom (2019)' },
    'INJ-02': { id: 'SC-12', name: 'The Em Economy & Fiscal Collapse', author: 'Robin Hanson (2016)' },
    'INJ-03': { id: 'SC-01', name: 'The Treacherous Turn & Sovereign Capital', author: 'Eliezer Yudkowsky (2008)' },
    'INJ-04': { id: 'SC-07', name: 'CAIS & Sub-Second Autonomous Defense', author: 'K. Eric Drexler (2019)' }
  };

  const SHOCK_PLAIN_NAMES: Record<string, { title: string; subtitle: string; icon: string }> = {
    'INJ-01': { title: 'The Cloud Gets Switched Off', subtitle: 'US/Foreign cloud APIs severed overnight (Model Embargo)', icon: '🔌' },
    'INJ-02': { title: 'A Year of White-Collar Job Loss at Once', subtitle: '60% cognitive labor automated; income tax collapses', icon: '💸' },
    'INJ-03': { title: 'An Autonomous Machine Cartel Secedes', subtitle: 'Algorithmic entities buy power plants and exit state law', icon: '🤖' },
    'INJ-04': { title: 'A Conflict Resolves in Milliseconds', subtitle: 'Defense speed outstrips human eyes; AI pulls trigger', icon: '⚡' }
  };

  function getWeakestLinkDiagnosis(c: any): string {
    if (c.iso === 'SGP') {
      return 'Zero domestic silicon fabrication and 94% dependence on foreign cloud hosting. When foreign APIs disconnect, automated trade and city coordination collapse in 4 hours.';
    } else if (c.iso === 'USA') {
      return 'World-leading frontier AI clusters, but 48% of federal tax revenue comes from white-collar wages. Sudden cognitive automation triggers a multi-trillion-dollar sovereign debt crisis.';
    } else if (c.iso === 'NOR') {
      return '100% clean hydro baseload, vast sovereign wealth buffer, and air-gapped critical infrastructure allow 60+ days (1,440 hours) of continuous autonomous operation.';
    } else if (c.iso === 'CHE') {
      return 'Mandatory civil defense analog fallbacks, decentralized cantonal utilities, and deep social trust buffer against prolonged cloud severed states (1,200 hours autarky).';
    } else if (c.iso === 'DEU') {
      return 'Strong domestic industrial engineering, but critical reliance on US frontier models and energy import dependencies create medium-term fragility.';
    } else if (c.iso === 'KOR') {
      return 'World-class semiconductor fabrication (Samsung/SK Hynix), but near-total primary energy import vulnerability and high cyber-electronic exposure.';
    } else if (c.t_half_h < 24) {
      return `Critical digital dependency without domestic hardware or analog fallback protocols. Civilizational resilience exhausts in ${c.t_half_h} hours.`;
    } else if (c.waa >= 0.70) {
      return 'Strong domestic sovereign compute ownership, but exposed to systemic fiscal transition shocks as labor markets automate.';
    } else {
      return 'Moderate digital adoption with limited domestic frontier model autonomy. Survives on regional secondary supply chains.';
    }
  }

  function getTransitionEvent(hour: number, c: any) {
    if (hour === 0) {
      return {
        stage: 'HOUR 0: NORMAL CLOUD-SYNCHRONIZED BASELINE',
        desc: `${c.name} operates at peak international connectivity. Financial clearing, container shipping, and hospital diagnostics rely seamlessly on frontier cloud APIs.`,
        level: 'normal'
      };
    } else if (hour <= 12) {
      return {
        stage: 'HOUR 0–12: DIGITAL SEVERANCE & CLEARING SHOCK',
        desc: `Foreign API tokens revoked. Automated high-frequency financial clearing freezes; container port crane scheduling reverts to manual logs.`,
        level: 'warning'
      };
    } else if (hour <= 24) {
      return {
        stage: 'HOUR 12–24: LOGISTICS DESYNC & CLINICAL TRIAGE PARALYSIS',
        desc: `Just-in-time logistics fail. Hospital emergency rooms face prescription verification queues; grocery supply chains desynchronize.`,
        level: 'severe'
      };
    } else if (hour <= 48) {
      return {
        stage: 'HOUR 24–48: BUFFER EXHAUSTION & ANALOG STRESS',
        desc: `Municipal backup fuel reserves deplete. Local grid balancing trips without algorithmic telemetry. Communities without analog drills begin to fracture.`,
        level: 'critical'
      };
    } else {
      return {
        stage: 'HOUR 48–72+: THE CIVILIZATIONAL FLOOR',
        desc: `${c.name} reaches its ultimate analog autarky limit. Any society with T_half (${c.t_half_h}h) below this threshold experiences systemic institutional failure.`,
        level: hour >= c.t_half_h ? 'collapsed' : 'holding'
      };
    }
  }

  // Technical Terminal State
  type TabType = 'matrix' | 'fiscal' | 'epistemic' | 'deterrence';
  let activeTab: TabType = 'matrix';
  let customDisplacementRate = 0.35;
  let customEpistemicMonths = 24;
  let customHumanLatencyMin = 30;
  let copiedToast = false;

  // ---------------------------------------------------------------------------
  // REACTIVE CALCULATIONS & SHOCKS
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

  $: currentAdoptionRank = adoptionRanks[selectedCountry.iso] || 1;
  $: currentSovereignRank = sovereignRanks[selectedCountry.iso] || 1;
  $: currentRankDrop = currentSovereignRank - currentAdoptionRank;
  $: isCeilingBreached = simulationHour >= selectedCountry.t_half_h;
  $: transitionEvent = getTransitionEvent(simulationHour, selectedCountry);
  $: activePrecedent = activeInjectId ? SHOCK_PRECEDENTS[activeInjectId] : null;

  $: archetypeCounts = displayCountries.reduce((acc: Record<string, number>, curr) => {
    acc[curr.archetype] = (acc[curr.archetype] || 0) + 1;
    return acc;
  }, {});

  $: deterrenceSpeedRatio = (customHumanLatencyMin * 60) / 0.05;
  $: deterrenceDelegationPct = Math.min(99.9, Number((100 * (1 - Math.exp(-0.00008 * deterrenceSpeedRatio))).toFixed(2)));

  $: epistemicDriftRate = 0.045 * (1.0 - selectedCountry.waa);
  $: epistemicDkl = Number((0.12 * Math.exp(epistemicDriftRate * (customEpistemicMonths / 6.0))).toFixed(3));
  $: epistemicHumanAuditPct = Math.max(1.0, Number((100 * Math.exp(-0.08 * customEpistemicMonths)).toFixed(1)));
  $: epistemicStatus = epistemicDkl < 0.50 ? 'PERMEABLE' : (epistemicDkl < 1.50 ? 'FRACTURED' : 'IRRECONCILABLE');

  // ---------------------------------------------------------------------------
  // ACTIONS
  // ---------------------------------------------------------------------------
  function triggerInject(id: string) {
    activeInjectId = activeInjectId === id ? null : id;
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

  function launchTerminalWithShock(injId: string) {
    activeInjectId = injId;
    currentView = 'terminal';
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
  <!-- Mode Switcher Pill Banner -->
  <div class="mode-navigation-bar">
    <div class="mode-label-group">
      <span class="mode-tag">EXPERIENCE MODE</span>
      <span class="mode-sub">Choose how you want to explore the 2026–2030 transition:</span>
    </div>
    <div class="mode-toggle-group">
      <button 
        class="mode-switch-btn" 
        class:active={currentView === 'explainer'}
        on:click={() => currentView = 'explainer'}
      >
        ✨ Visual Story & Trilemma (2-Min Intuitive)
      </button>
      <button 
        class="mode-switch-btn" 
        class:active={currentView === 'terminal'}
        on:click={() => currentView = 'terminal'}
      >
        📊 Quantitative Terminal (40-Nation Deep Dive)
      </button>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- 1. VISUAL INTERACTIVE EXPLAINER MODE (FOR EVERYONE)                   -->
  <!-- ===================================================================== -->
  {#if currentView === 'explainer'}
    <section class="explainer-section">
      <!-- 1. Differentiator Alert Header -->
      <div class="differentiator-banner">
        <div class="diff-tag">BEYOND CONVENTIONAL AI READINESS</div>
        <p class="diff-text">
          Traditional indices (e.g. IMF, Oxford Insights) rank software consumption. 
          <strong>HSRI stress-tests whether a nation physically survives</strong> when foreign cloud connections, sovereign tax bases, and human reaction times break.
        </p>
      </div>

      <!-- 2. Hero Header -->
      <div class="stress-hero">
        <div class="hero-badge-live">
          <span class="pulse-indicator"></span>
          INTERACTIVE TRANSITION STRESS-TEST · 2026–2030
        </div>
        <h1 class="stress-headline">
          When the Digital Umbilical Cord Cuts,<br />
          <span class="gradient-text">How Long Does Your Country Hold?</span>
        </h1>
        <p class="stress-subhead">
          Select a nation. Choose a crisis shockwave. Run the 72-hour simulation to observe how the weakest physical link fractures under Superintelligence.
        </p>
      </div>

      <!-- 3. The Interactive Stress Deck -->
      <div class="stress-deck-card">
        <!-- Step 1: Country Picker -->
        <div class="deck-step">
          <div class="step-label-row">
            <span class="step-num">STEP 1</span>
            <span class="step-title">Select Nation to Stress-Test:</span>
          </div>

          <!-- Preset Country Chips -->
          <div class="preset-chips-row">
            {#each PRESET_COUNTRIES as p}
              <button 
                class="preset-chip" 
                class:active={selectedCountryIso === p.iso}
                on:click={() => { selectedCountryIso = p.iso; resetSimulationHour(); }}
              >
                <span class="chip-name">{p.name}</span>
                <span class="chip-note">{p.note}</span>
              </button>
            {/each}
          </div>

          <!-- Full Selector Dropdown -->
          <div class="full-country-select-row">
            <label for="country-dropdown" class="select-label">Or choose from all 41 benchmark economies:</label>
            <select 
              id="country-dropdown"
              bind:value={selectedCountryIso} 
              class="country-dropdown-input"
              on:change={() => resetSimulationHour()}
            >
              {#each sandboxPayload.countries as c}
                <option value={c.iso}>{c.name} ({c.iso})</option>
              {/each}
            </select>
          </div>
        </div>

        <!-- Step 2: Shockwave Inject Picker -->
        <div class="deck-step">
          <div class="step-label-row">
            <span class="step-num">STEP 2</span>
            <span class="step-title">Choose Civilizational Shockwave:</span>
          </div>

          <div class="shock-buttons-grid">
            {#each Object.entries(SHOCK_PLAIN_NAMES) as [injId, info]}
              <button 
                class="shock-select-btn" 
                class:active-shock={activeInjectId === injId}
                on:click={() => { activeInjectId = injId; resetSimulationHour(); }}
              >
                <div class="ss-btn-top">
                  <span class="ss-btn-icon">{info.icon}</span>
                  <span class="ss-btn-title">{info.title}</span>
                </div>
                <div class="ss-btn-sub">{info.subtitle}</div>
              </button>
            {/each}
          </div>
        </div>

        <!-- Step 3: Interactive 72-Hour Animated Simulation Stage -->
        <div class="simulation-stage-box" class:fractured={isCeilingBreached}>
          <!-- Top Simulation Controls Bar -->
          <div class="stage-controls-bar">
            <div class="playback-controls">
              <button class="sim-play-btn" on:click={toggleSimulation}>
                {#if isPlaying}
                  ⏸ Pause Simulation
                {:else}
                  ▶ Run 72-Hour Stress Test
                {/if}
              </button>
              <button class="sim-reset-btn" on:click={resetSimulationHour} title="Reset to Hour 0">
                ↺ Reset
              </button>
            </div>

            <div class="timecode-display">
              <span class="tc-label">SIMULATED TIMELINE:</span>
              <span class="tc-value" class:tc-danger={isCeilingBreached}>
                T + {simulationHour} HOURS
              </span>
            </div>
          </div>

          <!-- Scrubber Slider -->
          <div class="scrubber-container">
            <input 
              type="range" 
              min="0" 
              max="72" 
              step="1" 
              bind:value={simulationHour} 
              class="scrubber-slider" 
              aria-label="Simulation hour scrubber"
            />
            <div class="scrubber-ticks">
              <span>0h (Baseline)</span>
              <span>12h (Severance)</span>
              <span>24h (Logistics)</span>
              <span>48h (Grids)</span>
              <span>72h+ (Floor)</span>
            </div>
          </div>

          <!-- Dynamic Status Banner -->
          {#if isCeilingBreached}
            <div class="fracture-alert-banner">
              <span class="alert-icon">⚠️</span>
              <div class="alert-body">
                <strong>CIVILIZATIONAL CEILING BREACHED AT HOUR {selectedCountry.t_half_h}</strong>
                <p>Domestic analog autarky exhausted. Essential institutional coordination and basic civic services have broken down.</p>
              </div>
            </div>
          {:else}
            <div class="absorbing-status-banner">
              <span class="status-dot-pulse"></span>
              <div class="status-body">
                <strong>SOVEREIGN BUFFERS ACTIVE & ABSORBING SHOCK</strong>
                <p>{selectedCountry.name} maintains {selectedCountry.t_half_h - simulationHour} hours of domestic autarky buffer before civilizational failure.</p>
              </div>
            </div>
          {/if}

          <!-- 4-Card Comparative Impact Matrix -->
          <div class="impact-cards-grid">
            <div class="impact-card">
              <div class="ic-meta">CONVENTIONAL ADOPTION</div>
              <div class="ic-value">#{currentAdoptionRank}</div>
              <div class="ic-desc">Standard AI usage rank (IMF/Oxford style)</div>
            </div>

            <div class="impact-card">
              <div class="ic-meta">SOVEREIGN RESILIENCE</div>
              <div class="ic-value highlight-rank">#{currentSovereignRank}</div>
              <div class="ic-desc">Physical survivability when disconnected</div>
            </div>

            <div class="impact-card">
              <div class="ic-meta">NET RANK DISPLACEMENT</div>
              {#if currentRankDrop > 0}
                <div class="ic-value drop-value">▼ -{currentRankDrop} Ranks</div>
                <div class="ic-desc warning-text">High-Adoption Vulnerability Trap</div>
              {:else if currentRankDrop < 0}
                <div class="ic-value surge-value">▲ +{Math.abs(currentRankDrop)} Ranks</div>
                <div class="ic-desc success-text">Sovereign Outperformer</div>
              {:else}
                <div class="ic-value">■ Stable</div>
                <div class="ic-desc">Rank preserved under shock</div>
              {/if}
            </div>

            <div class="impact-card">
              <div class="ic-meta">DECOUPLING HALF-LIFE</div>
              <div class="ic-value" class:text-danger={selectedCountry.t_half_h < 48}>
                {selectedCountry.t_half_h} Hours
              </div>
              <div class="ic-desc">Time until societal systems desynchronize</div>
            </div>
          </div>

          <!-- Archetype & Live Telemetry Breakdown -->
          <div class="transition-narrative-card">
            <div class="archetype-badge-row">
              <span class="arch-pill" style="border-color: {getArchetypeColor(selectedCountry.archetype)}; color: {getArchetypeColor(selectedCountry.archetype)};">
                POST-WESTPHALIAN ARCHETYPE: {selectedCountry.archetype.replace(/_/g, ' ')}
              </span>
              <span class="live-event-badge {transitionEvent.level}">
                {transitionEvent.stage}
              </span>
            </div>

            <p class="live-event-desc">
              {transitionEvent.desc}
            </p>

            <div class="weakest-link-box">
              <span class="wl-label">THE WEAKEST-LINK DIAGNOSIS:</span>
              <p class="wl-text">
                {getWeakestLinkDiagnosis(selectedCountry)}
              </p>
            </div>

            {#if activePrecedent}
              <div class="literature-bridge-row">
                <span class="lit-label">LITERATURE PRECEDENT:</span>
                <a href={`/scenarios/#${activePrecedent.id}`} class="lit-link">
                  📖 {activePrecedent.id}: {activePrecedent.name} ({activePrecedent.author}) &rarr;
                </a>
              </div>
            {/if}
          </div>
        </div>
      </div>

      <!-- 4. The Superintelligence Trilemma (The Game Theory Toy) -->
      <div class="trilemma-toy-section">
        <div class="section-badge-center">THE GAME THEORY AXIOM</div>
        <h2 class="toy-title">The Post-Westphalian Trilemma: Pick Any Two</h2>
        <p class="toy-subtitle">
          Every sovereign nation faces three theoretical desires. But mathematically, you can only pick two. Selection of any two guarantees structural collapse of the third:
        </p>

        <!-- The 3 Interactive Choices -->
        <div class="trilemma-choices-row">
          <button 
            class="choice-card" 
            class:selected={selectedTrilemmaChoice === 'vassal'}
            on:click={() => selectedTrilemmaChoice = 'vassal'}
          >
            <div class="choice-nodes">🚀 Frontier AI + 🌐 Open Cloud</div>
            <div class="choice-name">1. The Epistemic Vassal</div>
            <div class="choice-tag">You sacrifice: Domestic Sovereignty</div>
          </button>

          <button 
            class="choice-card" 
            class:selected={selectedTrilemmaChoice === 'fortress'}
            on:click={() => selectedTrilemmaChoice = 'fortress'}
          >
            <div class="choice-nodes">🚀 Frontier AI + 🛡️ Total Sovereignty</div>
            <div class="choice-name">2. The Fortress Empire</div>
            <div class="choice-tag">You sacrifice: Open Global Cooperation</div>
          </button>

          <button 
            class="choice-card" 
            class:selected={selectedTrilemmaChoice === 'redoubt'}
            on:click={() => selectedTrilemmaChoice = 'redoubt'}
          >
            <div class="choice-nodes">🛡️ Total Sovereignty + 🌐 Open Cloud</div>
            <div class="choice-name">3. The Analog Redoubt</div>
            <div class="choice-tag">You sacrifice: Frontier Capability</div>
          </button>
        </div>

        <!-- Animated Trilemma Diagnostic Display -->
        <div class="trilemma-visual-stage">
          <div class="trilemma-canvas-box">
            <svg class="trilemma-svg" viewBox="0 0 360 280">
              <!-- Background Triangle -->
              <polygon points="180,30 310,240 50,240" fill="none" stroke="var(--border-medium)" stroke-width="2" stroke-dasharray="4" />
              
              <!-- Active Highlight Lines -->
              {#if selectedTrilemmaChoice === 'vassal'}
                <line x1="180" y1="30" x2="310" y2="240" stroke="var(--threat-telemetry, #4f46e5)" stroke-width="4" />
              {:else if selectedTrilemmaChoice === 'fortress'}
                <line x1="180" y1="30" x2="50" y2="240" stroke="var(--threat-critical, #b91c1c)" stroke-width="4" />
              {:else if selectedTrilemmaChoice === 'redoubt'}
                <line x1="50" y1="240" x2="310" y2="240" stroke="var(--accent-primary, #1b6756)" stroke-width="4" />
              {/if}

              <!-- Node 1: Top (Frontier Capability) -->
              <circle cx="180" cy="30" r="22" class="node-circle" class:active={selectedTrilemmaChoice === 'vassal' || selectedTrilemmaChoice === 'fortress'} class:broken={selectedTrilemmaChoice === 'redoubt'} />
              <text x="180" y="34" text-anchor="middle" font-size="14">🚀</text>
              <text x="180" y="65" text-anchor="middle" class="node-text">1. FRONTIER AI</text>

              <!-- Node 2: Right (Open Integration) -->
              <circle cx="310" cy="240" r="22" class="node-circle" class:active={selectedTrilemmaChoice === 'vassal' || selectedTrilemmaChoice === 'redoubt'} class:broken={selectedTrilemmaChoice === 'fortress'} />
              <text x="310" y="244" text-anchor="middle" font-size="14">🌐</text>
              <text x="310" y="274" text-anchor="middle" class="node-text">3. OPEN CLOUD</text>

              <!-- Node 3: Left (Domestic Sovereignty) -->
              <circle cx="50" cy="240" r="22" class="node-circle" class:active={selectedTrilemmaChoice === 'fortress' || selectedTrilemmaChoice === 'redoubt'} class:broken={selectedTrilemmaChoice === 'vassal'} />
              <text x="50" y="244" text-anchor="middle" font-size="14">🛡️</text>
              <text x="50" y="274" text-anchor="middle" class="node-text">2. SOVEREIGNTY</text>
            </svg>
          </div>

          <!-- Dynamic Outcome Card -->
          <div class="trilemma-outcome-card">
            {#if selectedTrilemmaChoice === 'vassal'}
              <div class="outcome-badge" style="background: #e0e7ff; color: #3730a3;">ARCHETYPE: EPISTEMIC VASSAL</div>
              <h3 class="outcome-title">The "Digital Hostage" Dilemma</h3>
              <p class="outcome-desc">
                Your country has brilliant smart hospitals, banks, and self-driving infrastructure powered by foreign AI APIs. But you own <strong>none</strong> of the model weights. If the host nation flips an emergency switch, your national systems shut down in <strong>4 to 12 hours</strong>.
              </p>
              <div class="outcome-realworld">
                <strong>Real-World Examples:</strong>
                <span class="country-pill">Singapore (4h survival)</span>
                <span class="country-pill">United Kingdom (120h)</span>
                <span class="country-pill">Germany (480h)</span>
              </div>
            {:else if selectedTrilemmaChoice === 'fortress'}
              <div class="outcome-badge" style="background: #fee2e2; color: #991b1b;">ARCHETYPE: HYPERSCALE EMPIRE</div>
              <h3 class="outcome-title">The "Fortress Empire" Dilemma</h3>
              <p class="outcome-desc">
                Your nation builds massive 10-Gigawatt nuclear reactors dedicated entirely to domestic AI clusters. You control the weights and silicon. But to stay sovereign, you must wall off access, cut off international cooperation, and run a private compute fortress.
              </p>
              <div class="outcome-realworld">
                <strong>Real-World Examples:</strong>
                <span class="country-pill">United States (CSP: 0.93)</span>
                <span class="country-pill">China (CSP: 0.88)</span>
              </div>
            {:else if selectedTrilemmaChoice === 'redoubt'}
              <div class="outcome-badge" style="background: #dcfce7; color: #166534;">ARCHETYPE: AIR-GAPPED REDOUBT</div>
              <h3 class="outcome-title">The "Analog Redoubt" Dilemma</h3>
              <p class="outcome-desc">
                Your country refuses to let foreign models run your civil infrastructure. You maintain manual water grids, offline radio networks, and deep civic trust. You can survive a total cloud blackout for <strong>1,200+ hours</strong>, but your cognitive speed falls far behind frontier AI empires.
              </p>
              <div class="outcome-realworld">
                <strong>Real-World Examples:</strong>
                <span class="country-pill">Switzerland (1,200h)</span>
                <span class="country-pill">Norway (1,440h)</span>
                <span class="country-pill">Finland (1,440h)</span>
              </div>
            {/if}
          </div>
        </div>
      </div>

      <!-- 5. Two-World Realignment Grid -->
      <div class="explainer-hero">
        <div class="section-badge-center">STRUCTURAL REALIGNMENT</div>
        <h2 class="toy-title">Why the 400-Year-Old Map Is Dissolving</h2>
        <div class="contrast-grid">
          <div class="contrast-card old-world">
            <div class="c-era">THE OLD WESTPHALIAN WORLD (1648 – 2025)</div>
            <div class="c-headline">Physical Borders & Human Work</div>
            <ul class="c-points">
              <li>🌍 <strong>Territory & Flags:</strong> Power belongs to nations with geographic landmass and armies.</li>
              <li>💼 <strong>Labor-Backed Money:</strong> Governments borrow money backed by taxes on human paychecks.</li>
              <li>⏳ <strong>Human Clock:</strong> Presidents had 20 minutes to verify missile warnings and negotiate.</li>
            </ul>
          </div>

          <div class="contrast-card-divider">
            <span class="divider-arrow">⚡</span>
          </div>

          <div class="contrast-card new-world">
            <div class="c-era">THE SUPERINTELLIGENCE ERA (2026+)</div>
            <div class="c-headline">Megawatts, Model Weights & Machine Speed</div>
            <ul class="c-points">
              <li>⚡ <strong>Compute Empires:</strong> Power belongs to whoever commands 10-Gigawatt nuclear clusters.</li>
              <li>📉 <strong>Free Machine Labor:</strong> When AI works for free, income tax collapses and sovereign debt breaks.</li>
              <li>🚀 <strong>50-Millisecond Wars:</strong> Defense moves faster than human eyes; algorithmic loops pull the trigger.</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 6. Progressive Disclosure: Deep Dive Terminal Callout -->
      <div class="quick-country-banner">
        <div class="qcb-content">
          <h3>Ready for the Econometric Proofs?</h3>
          <p>Explore the full 41-nation Leontief matrices, Cobb-Douglas compute parameters, epistemic KL divergence, and download custom sovereign survivability dossiers.</p>
        </div>
        <div class="qcb-action">
          <button class="launch-terminal-btn" on:click={() => currentView = 'terminal'}>
            Open Quantitative Data Terminal & Matrix &rarr;
          </button>
        </div>
      </div>
    </section>

  <!-- ===================================================================== -->
  <!-- 2. QUANTITATIVE EXPERT TERMINAL MODE (THE DEEP DIVE)                  -->
  <!-- ===================================================================== -->
  {:else}
    <div class="terminal-view">
      <!-- Return to explainer link -->
      <div class="terminal-topbar">
        <button class="back-explainer-btn" on:click={() => currentView = 'explainer'}>
          ← Back to Visual Explainer
        </button>
        <span class="active-mode-badge">QUANTITATIVE DATA TERMINAL ACTIVE</span>
      </div>

      <!-- Cockpit Header -->
      <header class="sandbox-masthead">
        <div class="masthead-badge">
          <span class="live-dot"></span>
          HSRI 2.0 MACRO HORIZON OBSERVED · 2026–2030 DATA MATRIX
        </div>
        <h2 class="masthead-title">Sovereign Econometric & Epistemic Matrix</h2>
        <p class="masthead-desc">
          Formal quantitative modeling of Compute Sovereign Power (CSP), Debt Default Horizons (T_default), and Decoupling Half-Lives (T_half) across 40 benchmark nations.
        </p>

        <!-- Active Crisis Inject Quick-Triggers -->
        <div class="inject-strip">
          <div class="inject-strip-label">TRIGGER SYSTEMIC SHOCKWAVE INJECT:</div>
          <div class="inject-buttons">
            {#each sandboxPayload.injects as inj}
              <button 
                class="inject-btn" 
                class:active={activeInjectId === inj.id}
                on:click={() => triggerInject(inj.id)}
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
        <div class="sandbox-viewport">
          <!-- TAB 1: MATRIX SCOREBOARD -->
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

          <!-- TAB 2: FISCAL CLIFF -->
          {:else if activeTab === 'fiscal'}
            <section class="viewport-section">
              <div class="section-intro">
                <h3>The Post-Labor Fiscal Insolvency Clock</h3>
                <p>
                  Sovereign debt depends entirely on taxing biological human labor. When autonomous agents displace high-income cognitive professions at scale, the tax base collapses while fixed debt obligations compound.
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

              <!-- Selected Nation Trajectory Breakdown -->
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

          <!-- TAB 3: EPISTEMIC IRON CURTAIN -->
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
            </section>

          <!-- TAB 4: DETERRENCE LADDER -->
          {:else if activeTab === 'deterrence'}
            <section class="viewport-section">
              <div class="section-intro">
                <h3>Sub-Second Deterrence & The Zero-Human Strike Frontier</h3>
                <p>
                  In machine-speed cyber warfare and autonomous kinetic swarms, strikes peak and resolve in milliseconds. Maintaining human-in-the-loop authorization guarantees military defeat.
                </p>
              </div>

              <!-- Latency Simulator -->
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

        <!-- RIGHT SIDE: THE SOVEREIGN SURVIVABILITY INSPECTOR -->
        <aside class="sandbox-inspector">
          <div class="inspector-header">
            <span class="inspector-badge">SOVEREIGN DOSSIER</span>
            <h3 class="inspector-nation">{selectedCountry.name}</h3>
            <span class="inspector-iso">{selectedCountry.iso}</span>
          </div>

          <div class="inspector-archetype" style="background: {getArchetypeColor(selectedCountry.archetype)}20; border: 1px solid {getArchetypeColor(selectedCountry.archetype)}50; color: {getArchetypeColor(selectedCountry.archetype)};">
            {selectedCountry.archetype.replace(/_/g, ' ')}
          </div>

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

          <div class="inspector-assessment">
            <h4>Strategic Assessment</h4>
            <p class="assessment-text">
              {getArchetypeAssessment(selectedCountry.archetype, selectedCountry.name)}
            </p>
          </div>

          {#if activeInject}
            <div class="inspector-shock-box">
              <h4>Active Shock Impact ({activeInject.id})</h4>
              <p class="shock-summary">
                Under <em>{activeInject.name}</em>, {selectedCountry.name}'s weight autonomy operates at {(selectedCountry.waa * 100).toFixed(1)}%, with decoupling half-life reduced to {selectedCountry.t_half_h}h.
              </p>
            </div>
          {/if}

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
  {/if}
</div>

<style>
  .sandbox-container {
    padding: 1.5rem 0 3.5rem;
    color: var(--text-primary);
  }

  /* Mode Navigation Bar */
  .mode-navigation-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 0.85rem 1.25rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
    flex-wrap: wrap;
    gap: 1rem;
  }

  .mode-label-group {
    display: flex;
    flex-direction: column;
  }

  .mode-tag {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
  }

  .mode-sub {
    font-size: 0.82rem;
    color: var(--text-muted);
  }

  .mode-toggle-group {
    display: flex;
    gap: 0.5rem;
  }

  .mode-switch-btn {
    padding: 0.55rem 1.15rem;
    border-radius: 8px;
    border: 1px solid var(--border-subtle);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .mode-switch-btn:hover {
    background: var(--bg-surface-sunken);
    color: var(--text-primary);
  }

  .mode-switch-btn.active {
    background: var(--accent-primary);
    color: #ffffff;
    border-color: var(--accent-primary);
    box-shadow: 0 2px 8px rgba(27, 103, 86, 0.25);
  }

  /* =========================================================================
     DIFFERENTIATOR BANNER & STRESS HERO
     ========================================================================= */
  .differentiator-banner {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: linear-gradient(135deg, rgba(27, 103, 86, 0.08) 0%, rgba(27, 103, 86, 0.02) 100%);
    border: 1px solid var(--accent-primary);
    border-radius: 10px;
    padding: 0.85rem 1.25rem;
    margin-bottom: 2.25rem;
    flex-wrap: wrap;
  }

  .diff-tag {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    background: var(--accent-primary);
    color: #ffffff;
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
    white-space: nowrap;
  }

  .diff-text {
    font-size: 0.92rem;
    line-height: 1.5;
    color: var(--text-secondary);
    margin: 0;
    flex: 1;
    min-width: 260px;
  }

  .stress-hero {
    text-align: center;
    max-width: 900px;
    margin: 0 auto 2.5rem;
  }

  .hero-badge-live {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    background: var(--accent-primary-glow);
    padding: 0.3rem 0.85rem;
    border-radius: 9999px;
    margin-bottom: 0.85rem;
  }

  .pulse-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent-primary);
    box-shadow: 0 0 8px var(--accent-primary);
    animation: pulseGlow 2s infinite;
  }

  @keyframes pulseGlow {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(1.2); }
  }

  .stress-headline {
    font-family: var(--font-family-display);
    font-size: clamp(2rem, 4.2vw, 3rem);
    font-weight: 800;
    line-height: 1.18;
    margin: 0 0 0.85rem;
    letter-spacing: -0.025em;
  }

  .gradient-text {
    background: linear-gradient(135deg, var(--accent-primary) 0%, var(--threat-warning, #d97706) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .stress-subhead {
    font-size: 1.12rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 760px;
    margin: 0 auto;
  }

  /* =========================================================================
     INTERACTIVE STRESS DECK
     ========================================================================= */
  .stress-deck-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 3.5rem;
    box-shadow: 0 6px 30px rgba(0, 0, 0, 0.03);
  }

  .deck-step {
    margin-bottom: 2rem;
  }

  .step-label-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 1rem;
  }

  .step-num {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    background: var(--accent-primary);
    color: #ffffff;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    letter-spacing: 0.05em;
  }

  .step-title {
    font-family: var(--font-family-display);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  /* Preset Country Chips */
  .preset-chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    margin-bottom: 1rem;
  }

  .preset-chip {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 0.6rem 0.95rem;
    border-radius: 8px;
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-subtle);
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
  }

  .preset-chip:hover {
    border-color: var(--accent-primary);
    transform: translateY(-2px);
  }

  .preset-chip.active {
    border-color: var(--accent-primary);
    background: var(--accent-primary-glow);
    box-shadow: 0 2px 10px rgba(27, 103, 86, 0.15);
  }

  .chip-name {
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--text-primary);
  }

  .chip-note {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .preset-chip.active .chip-note {
    color: var(--accent-primary);
    font-weight: 700;
  }

  .full-country-select-row {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    flex-wrap: wrap;
  }

  .select-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
  }

  .country-dropdown-input {
    padding: 0.45rem 0.85rem;
    border-radius: 6px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-sunken);
    color: var(--text-primary);
    font-size: 0.88rem;
    font-family: var(--font-family-mono);
    cursor: pointer;
  }

  /* Shock Buttons Grid */
  .shock-buttons-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.85rem;
  }

  .shock-select-btn {
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem 1.15rem;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .shock-select-btn:hover {
    border-color: var(--threat-warning, #d97706);
    transform: translateY(-2px);
  }

  .shock-select-btn.active-shock {
    border-color: var(--threat-critical, #b91c1c);
    background: linear-gradient(135deg, var(--bg-surface-elevated) 0%, rgba(185, 28, 28, 0.05) 100%);
    box-shadow: 0 4px 15px rgba(185, 28, 28, 0.12);
  }

  .ss-btn-top {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
  }

  .ss-btn-icon {
    font-size: 1.25rem;
  }

  .ss-btn-title {
    font-family: var(--font-family-display);
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .ss-btn-sub {
    font-size: 0.78rem;
    color: var(--text-muted);
    line-height: 1.4;
  }

  .shock-select-btn.active-shock .ss-btn-sub {
    color: var(--threat-critical, #b91c1c);
    font-weight: 600;
  }

  /* =========================================================================
     72-HOUR ANIMATED SIMULATION STAGE
     ========================================================================= */
  .simulation-stage-box {
    background: var(--bg-surface-sunken);
    border: 2px solid var(--border-medium);
    border-radius: 14px;
    padding: 1.75rem;
    transition: all 0.3s ease;
  }

  .simulation-stage-box.fractured {
    border-color: var(--threat-critical, #b91c1c);
    box-shadow: 0 0 25px rgba(185, 28, 28, 0.15);
  }

  .stage-controls-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.25rem;
  }

  .playback-controls {
    display: flex;
    align-items: center;
    gap: 0.65rem;
  }

  .sim-play-btn {
    padding: 0.55rem 1.15rem;
    border-radius: 6px;
    border: none;
    background: var(--accent-primary);
    color: #ffffff;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(27, 103, 86, 0.25);
  }

  .sim-play-btn:hover {
    background: var(--accent-primary-hover, #2aa389);
    transform: translateY(-1px);
  }

  .sim-reset-btn {
    padding: 0.55rem 0.85rem;
    border-radius: 6px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-secondary);
    font-size: 0.85rem;
    cursor: pointer;
  }

  .sim-reset-btn:hover {
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
  }

  .timecode-display {
    font-family: var(--font-family-mono);
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .tc-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
  }

  .tc-value {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .tc-value.tc-danger {
    color: var(--threat-critical, #b91c1c);
  }

  /* Scrubber Slider */
  .scrubber-container {
    margin-bottom: 1.5rem;
  }

  .scrubber-slider {
    width: 100%;
    height: 8px;
    border-radius: 4px;
    accent-color: var(--accent-primary);
    cursor: pointer;
  }

  .scrubber-ticks {
    display: flex;
    justify-content: space-between;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 0.35rem;
  }

  /* Status Banners */
  .fracture-alert-banner {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    background: rgba(185, 28, 28, 0.1);
    border-left: 4px solid var(--threat-critical, #b91c1c);
    padding: 0.95rem 1.25rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
  }

  .fracture-alert-banner .alert-icon {
    font-size: 1.35rem;
  }

  .fracture-alert-banner .alert-body strong {
    font-family: var(--font-family-mono);
    color: var(--threat-critical, #b91c1c);
    font-size: 0.95rem;
    letter-spacing: 0.05em;
  }

  .fracture-alert-banner .alert-body p {
    margin: 0.25rem 0 0;
    font-size: 0.88rem;
    color: var(--text-secondary);
  }

  .absorbing-status-banner {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    background: rgba(27, 103, 86, 0.08);
    border-left: 4px solid var(--accent-primary);
    padding: 0.95rem 1.25rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
  }

  .status-dot-pulse {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--accent-primary);
    box-shadow: 0 0 8px var(--accent-primary);
    margin-top: 5px;
    animation: pulseGlow 1.8s infinite;
  }

  .absorbing-status-banner .status-body strong {
    font-family: var(--font-family-mono);
    color: var(--accent-primary);
    font-size: 0.95rem;
    letter-spacing: 0.05em;
  }

  .absorbing-status-banner .status-body p {
    margin: 0.25rem 0 0;
    font-size: 0.88rem;
    color: var(--text-secondary);
  }

  /* 4-Card Comparative Impact Matrix */
  .impact-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .impact-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.15rem;
  }

  .ic-meta {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    margin-bottom: 0.35rem;
  }

  .ic-value {
    font-family: var(--font-family-display);
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
  }

  .highlight-rank {
    color: var(--accent-primary);
  }

  .drop-value {
    color: var(--threat-critical, #b91c1c);
  }

  .surge-value {
    color: var(--accent-primary);
  }

  .ic-desc {
    font-size: 0.78rem;
    color: var(--text-muted);
    line-height: 1.35;
  }

  .warning-text {
    color: var(--threat-critical, #b91c1c);
    font-weight: 600;
  }

  .success-text {
    color: var(--accent-primary);
    font-weight: 600;
  }

  /* Transition Narrative Card */
  .transition-narrative-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.35rem;
  }

  .archetype-badge-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  .arch-pill {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 800;
    border: 1.5px solid currentColor;
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
    letter-spacing: 0.06em;
  }

  .live-event-badge {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
  }

  .live-event-badge.normal {
    background: rgba(27, 103, 86, 0.1);
    color: var(--accent-primary);
  }

  .live-event-badge.warning {
    background: rgba(217, 119, 6, 0.1);
    color: var(--threat-warning, #d97706);
  }

  .live-event-badge.severe, .live-event-badge.critical, .live-event-badge.collapsed {
    background: rgba(185, 28, 28, 0.1);
    color: var(--threat-critical, #b91c1c);
  }

  .live-event-desc {
    font-size: 0.95rem;
    line-height: 1.55;
    color: var(--text-secondary);
    margin: 0 0 1.15rem;
  }

  .weakest-link-box {
    background: var(--bg-surface-elevated);
    border-left: 3px solid var(--threat-warning, #d97706);
    padding: 0.85rem 1.15rem;
    border-radius: 6px;
    margin-bottom: 1rem;
  }

  .wl-label {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--threat-warning, #d97706);
    margin-bottom: 0.25rem;
  }

  .wl-text {
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--text-primary);
    margin: 0;
  }

  .literature-bridge-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    font-size: 0.85rem;
    color: var(--text-muted);
    flex-wrap: wrap;
  }

  .lit-label {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
  }

  .lit-link {
    color: var(--accent-primary);
    font-weight: 600;
    text-decoration: underline;
    text-underline-offset: 3px;
  }

  .lit-link:hover {
    color: var(--accent-primary-hover, #2aa389);
  }

  /* =========================================================================
     EXPLAINER HERO & CARDS
     ========================================================================= */
  .explainer-hero {
    text-align: center;
    max-width: 960px;
    margin: 0 auto 3rem;
  }

  .hero-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    background: var(--accent-primary-glow);
    padding: 0.3rem 0.85rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
  }

  .hero-title {
    font-family: var(--font-family-display);
    font-size: clamp(2.1rem, 4.5vw, 3.1rem);
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 1rem;
    letter-spacing: -0.02em;
  }

  .hero-lead {
    font-size: 1.18rem;
    line-height: 1.65;
    color: var(--text-secondary);
    max-width: 800px;
    margin: 0 auto 2.25rem;
  }

  .contrast-grid {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 1.25rem;
    align-items: center;
    text-align: left;
  }

  @media (max-width: 768px) {
    .contrast-grid {
      grid-template-columns: 1fr;
    }
    .contrast-card-divider {
      display: none;
    }
  }

  .contrast-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 1.75rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  }

  .contrast-card.old-world {
    border-left: 4px solid var(--border-strong);
  }

  .contrast-card.new-world {
    border-left: 4px solid var(--threat-critical, #b91c1c);
    background: linear-gradient(135deg, var(--bg-surface) 0%, rgba(185, 28, 28, 0.03) 100%);
  }

  .c-era {
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
  }

  .c-headline {
    font-family: var(--font-family-display);
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1rem;
  }

  .c-points {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--text-secondary);
  }

  .contrast-card-divider {
    font-size: 1.85rem;
    color: var(--threat-warning);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* =========================================================================
     INTERACTIVE TRILEMMA TOY
     ========================================================================= */
  .trilemma-toy-section {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 3.5rem;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.02);
  }

  .section-badge-center {
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    text-align: center;
    margin-bottom: 0.5rem;
  }

  .toy-title {
    font-family: var(--font-family-display);
    font-size: clamp(1.65rem, 3vw, 2.25rem);
    font-weight: 700;
    text-align: center;
    margin: 0 0 0.5rem;
  }

  .toy-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary);
    text-align: center;
    max-width: 720px;
    margin: 0 auto 2rem;
  }

  .trilemma-choices-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .choice-card {
    background: var(--bg-surface-elevated);
    border: 2px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.25rem;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .choice-card:hover {
    border-color: var(--accent-primary);
    transform: translateY(-2px);
  }

  .choice-card.selected {
    border-color: var(--accent-primary);
    background: var(--accent-primary-glow);
    box-shadow: 0 4px 15px rgba(27, 103, 86, 0.15);
  }

  .choice-nodes {
    font-family: var(--font-family-mono);
    font-size: 0.78rem;
    color: var(--accent-primary);
    font-weight: 700;
    margin-bottom: 0.35rem;
  }

  .choice-name {
    font-family: var(--font-family-display);
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
  }

  .choice-tag {
    font-size: 0.78rem;
    color: var(--threat-critical, #b91c1c);
    font-weight: 600;
  }

  .trilemma-visual-stage {
    display: grid;
    grid-template-columns: 360px 1fr;
    gap: 2rem;
    align-items: center;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 1.75rem;
  }

  @media (max-width: 860px) {
    .trilemma-visual-stage {
      grid-template-columns: 1fr;
    }
  }

  .trilemma-canvas-box {
    display: flex;
    justify-content: center;
  }

  .trilemma-svg {
    width: 100%;
    max-width: 340px;
    height: auto;
  }

  .node-circle {
    fill: var(--bg-surface-elevated);
    stroke: var(--border-strong);
    stroke-width: 2.5;
    transition: all 0.3s ease;
  }

  .node-circle.active {
    stroke: var(--accent-primary);
    stroke-width: 4;
    filter: drop-shadow(0 0 6px rgba(27, 103, 86, 0.4));
  }

  .node-circle.broken {
    stroke: var(--threat-critical, #b91c1c);
    stroke-width: 3;
    opacity: 0.45;
    stroke-dasharray: 4;
  }

  .node-text {
    font-family: var(--font-family-mono);
    font-size: 9px;
    font-weight: 700;
    fill: var(--text-primary);
  }

  .trilemma-outcome-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.5rem;
  }

  .outcome-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
    margin-bottom: 0.75rem;
  }

  .outcome-title {
    font-family: var(--font-family-display);
    font-size: 1.45rem;
    margin: 0 0 0.75rem;
  }

  .outcome-desc {
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin: 0 0 1.25rem;
  }

  .outcome-realworld {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.88rem;
  }

  .country-pill {
    font-family: var(--font-family-mono);
    font-size: 0.78rem;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    font-weight: 600;
  }

  /* =========================================================================
     4 CRISIS STORYLINES GRID
     ========================================================================= */
  .crises-story-section {
    margin-bottom: 3.5rem;
  }

  .shockwaves-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.25rem;
    margin-top: 1.75rem;
  }

  .shock-story-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s ease;
  }

  .shock-story-card:hover {
    border-color: var(--accent-primary);
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
  }

  .shock-story-card.active-shock {
    border-color: var(--threat-critical, #b91c1c);
    background: #fff5f5;
  }

  .ss-icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
  }

  .ss-head {
    font-family: var(--font-family-display);
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
  }

  .ss-sub {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--threat-warning, #d97706);
    margin-bottom: 0.75rem;
  }

  .ss-body {
    font-size: 0.88rem;
    line-height: 1.55;
    color: var(--text-secondary);
    margin: 0 0 1.25rem;
    flex-grow: 1;
  }

  .sim-btn {
    padding: 0.65rem 1rem;
    border-radius: 6px;
    border: 1px solid var(--accent-primary);
    background: var(--bg-surface-elevated);
    color: var(--accent-primary);
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .sim-btn:hover {
    background: var(--accent-primary);
    color: #ffffff;
  }

  /* Quick Country Banner */
  .quick-country-banner {
    background: var(--bg-surface);
    border: 2px solid var(--accent-primary);
    border-radius: 12px;
    padding: 1.75rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1.5rem;
  }

  .qcb-content h3 {
    margin: 0 0 0.35rem;
    font-size: 1.35rem;
  }

  .qcb-content p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 0.95rem;
  }

  .qcb-action {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .qcb-select {
    padding: 0.65rem 0.85rem;
    border-radius: 6px;
    border: 1px solid var(--border-medium);
    font-size: 0.9rem;
    background: var(--bg-surface-elevated);
  }

  .launch-terminal-btn {
    padding: 0.65rem 1.25rem;
    border-radius: 6px;
    background: var(--accent-primary);
    color: #ffffff;
    font-weight: 700;
    border: none;
    cursor: pointer;
    font-size: 0.92rem;
  }

  .launch-terminal-btn:hover {
    background: var(--accent-primary-hover);
  }

  /* =========================================================================
     TERMINAL VIEW (EXPERT DEEP DIVE)
     ========================================================================= */
  .terminal-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.25rem;
  }

  .back-explainer-btn {
    background: transparent;
    border: 1px solid var(--border-medium);
    padding: 0.45rem 0.85rem;
    border-radius: 6px;
    color: var(--accent-primary);
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
  }

  .back-explainer-btn:hover {
    background: var(--bg-surface-sunken);
  }

  .active-mode-badge {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
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

  /* Sliders & Tiers */
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
