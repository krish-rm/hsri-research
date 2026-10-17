<script lang="ts">
  import { onMount } from 'svelte';
  import countryData from '../data/country_scores.json';

  export let preselectCode: string = 'USA';
  export let showHeader: boolean = true;

  const countries = countryData.countries || [];
  let selectedCode = preselectCode;

  $: selectedCountry = countries.find((c: any) => c.code === selectedCode) || countries[0];
</script>

<div class="country-lookup-card">
  {#if showHeader}
    <div class="lookup-header">
      <div class="eyebrow-chip">SOVEREIGN VULNERABILITY AUDIT</div>
      <h4 class="lookup-title">How Long Does Your Nation Endure Without the Cloud?</h4>
      <p class="lookup-desc">
        Search any benchmark nation to inspect its Leontief Decoupling Half-Life (T_half) and sovereign rank drop:
      </p>
    </div>
  {/if}

  <div class="search-row" style={!showHeader ? 'margin-top: 0;' : ''}>
      <label for="country-selector" class="sr-only">Select Nation</label>
      <select id="country-selector" bind:value={selectedCode} class="country-select">
        {#each countries as c}
          <option value={c.code}>{c.name} ({c.code})</option>
        {/each}
      </select>
    </div>

  {#if selectedCountry}
    <div class="result-cockpit">
      <div class="stat-card half-life">
        <span class="stat-meta">Decoupling Half-Life</span>
        <span class="stat-num">{selectedCountry.T_half_h} Hours</span>
        <span class="stat-context">Survival floor under digital severance</span>
      </div>

      <div class="stat-card rank-delta">
        <span class="stat-meta">Sovereignty Rank Shift</span>
        <span class="stat-num" class:negative={selectedCountry.rank_delta < 0} class:positive={selectedCountry.rank_delta > 0}>
          {selectedCountry.rank_delta > 0 ? `▲ +${selectedCountry.rank_delta}` : selectedCountry.rank_delta < 0 ? `▼ ${selectedCountry.rank_delta}` : '— 0'}
        </span>
        <span class="stat-context">Layer 1 Adoption (#{selectedCountry.rank_L1}) → Layer 2 Sovereignty (#{selectedCountry.rank_L2})</span>
      </div>

      <div class="stat-card bottleneck">
        <span class="stat-meta">Critical Weakest Link</span>
        <span class="stat-num bottleneck-text">{selectedCountry.bottleneck_pillar || 'Energy / Grid'}</span>
        <span class="stat-context">Leontief non-compensatory bottleneck</span>
      </div>
    </div>

    <div class="audit-summary-strip">
      <span class="flag-icon">{selectedCountry.code}</span>
      <span class="summary-body">
        {#if selectedCountry.rank_delta <= -15}
          <strong>High-Compute Fragility Trap:</strong> Extreme digital adoption with zero analog fallback. Ranks #{selectedCountry.rank_L1} in adoption but plunges to #{selectedCountry.rank_L2} in sovereign survivability.
        {:else if selectedCountry.rank_delta >= 5}
          <strong>Resilient Modular Sovereignty:</strong> Preserved analog backups and high energy self-sufficiency allow continued function despite cloud blackout.
        {:else}
          <strong>Balanced Decoupling Baseline:</strong> Moderate survival floor with typical supply chain vulnerabilities.
        {/if}
      </span>
    </div>
  {/if}
</div>

<style>
  .country-lookup-card {
    margin: 2rem 0;
    padding: 1.5rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    box-shadow: var(--shadow-sm);
  }

  .eyebrow-chip {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--accent-primary);
    letter-spacing: 0.08em;
    margin-bottom: 0.35rem;
  }

  .lookup-title {
    margin: 0 0 0.35rem 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .lookup-desc {
    margin: 0 0 1rem 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .search-row {
    margin-bottom: 1.25rem;
  }

  .country-select {
    width: 100%;
    max-width: 360px;
    padding: 0.65rem 1rem;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-strong);
    color: var(--text-primary);
    font-family: var(--font-family-sans);
    font-size: 0.95rem;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
  }

  .country-select:focus {
    outline: none;
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-primary-glow);
  }

  .result-cockpit {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .stat-card {
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
  }

  .stat-meta {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 0.25rem;
  }

  .stat-num {
    font-family: var(--font-family-mono);
    font-size: 1.45rem;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
    font-variant-numeric: tabular-nums;
  }

  .stat-num.negative {
    color: var(--threat-critical);
  }

  .stat-num.positive {
    color: var(--threat-sovereign);
  }

  .bottleneck-text {
    font-size: 1.05rem;
    color: var(--threat-warning);
  }

  .stat-context {
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .audit-summary-strip {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.85rem 1rem;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.45;
  }

  .flag-icon {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--accent-primary);
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    flex-shrink: 0;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
  }

  @media (max-width: 640px) {
    .result-cockpit {
      grid-template-columns: 1fr;
    }
  }
</style>