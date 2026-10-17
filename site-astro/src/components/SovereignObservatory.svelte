<script lang="ts">
  import SovereignGlobe from './SovereignGlobe.svelte';
  import SovereignInspectorCard from './SovereignInspectorCard.svelte';
  import scoresData from '../data/country_scores.json';

  let {
    countries = scoresData.countries
  }: {
    countries?: any[];
  } = $props();

  const base = (import.meta.env.BASE_URL || '').replace(/\/$/, '');

  let selectedId: string | null = $state(null);

  function handleSelect(id: string | null) {
    selectedId = id;
  }

  function handleClose() {
    selectedId = null;
  }
</script>

<div class="globe-layout">
  <div class="globe-main">
    <SovereignGlobe
      {countries}
      bind:selectedId
      onSelect={handleSelect}
    />
    <p class="scope-note">
      <strong>Sample scope:</strong> 39 benchmark nations (OECD/high-income preview cohort). 86 evaluated nations remain unrated pending multi-pillar coverage.
      <a href={`${base}/coverage/`}>Coverage details →</a> ·
      <a href={`${base}/data/`}>Downloads</a>
    </p>
  </div>
  <div class="globe-inspector" id="globe-inspector">
    {#if selectedId}
      <SovereignInspectorCard
        {selectedId}
        {countries}
        onClose={handleClose}
      />
    {:else}
      <div class="inspector-placeholder">
        <div class="ph-title">Sovereign Telemetry Inspector</div>
        <p>Select a nation on the globe or search above to inspect Decoupling Half-Life, dual-layer rank delta, and weakest-link floor.</p>
        <div class="ph-legend">
          <span><i style="background:#10b981"></i> Resilient</span>
          <span><i style="background:#f59e0b"></i> Transitional</span>
          <span><i style="background:#ef4444"></i> Fragility Trap</span>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .globe-layout {
    display: grid;
    grid-template-columns: 1.45fr 0.85fr;
    gap: 18px;
    align-items: start;
  }
  .globe-main {
    min-width: 0;
  }
  .globe-inspector {
    position: sticky;
    top: 88px;
  }
  .inspector-placeholder {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 24px;
    box-shadow: var(--shadow-sm);
  }
  .ph-title {
    font-weight: 800;
    color: var(--text-primary);
    font-size: 1.05rem;
    margin-bottom: 8px;
  }
  .inspector-placeholder p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.55;
  }
  .ph-legend {
    display: flex;
    gap: 14px;
    margin-top: 14px;
    font-size: 0.76rem;
    color: var(--text-muted);
    flex-wrap: wrap;
  }
  .ph-legend span {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .ph-legend i {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
  }
  .scope-note {
    margin-top: 10px;
    font-size: 0.82rem;
    color: var(--text-muted);
    background: var(--bg-surface);
    border-left: 3px solid var(--accent-primary);
    padding: 8px 12px;
    border-radius: 0 10px 10px 0;
    border-top: 1px solid var(--border-subtle);
    border-right: 1px solid var(--border-subtle);
    border-bottom: 1px solid var(--border-subtle);
  }
  .scope-note a {
    color: var(--accent-primary);
    font-weight: 600;
    text-decoration: none;
  }
  .scope-note a:hover {
    text-decoration: underline;
  }
  @media (max-width: 980px) {
    .globe-layout {
      grid-template-columns: 1fr;
    }
    .globe-inspector {
      position: static;
    }
  }
</style>
