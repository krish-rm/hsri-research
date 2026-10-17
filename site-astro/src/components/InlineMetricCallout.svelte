<script lang="ts">
  export let value: string = '';
  export let label: string = '';
  export let sub: string = '';
  export let variant: 'critical' | 'sovereign' | 'telemetry' | 'warning' = 'telemetry';
  export let source: string = '';
</script>

<aside class={`metric-callout-box variant-${variant}`}>
  <div class="callout-header">
    <span class="callout-label">{label}</span>
    {#if source}
      <span class="callout-source" title={`Verified Source: ${source}`}>{source}</span>
    {/if}
  </div>
  <div class="callout-value">{value}</div>
  {#if sub}
    <div class="callout-sub">{sub}</div>
  {/if}
</aside>

<style>
  .metric-callout-box {
    margin: 1.5rem 0;
    padding: 1.25rem 1.5rem;
    border-radius: 10px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    box-shadow: var(--shadow-sm);
    box-sizing: border-box;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }

  .metric-callout-box:hover {
    border-color: var(--border-medium);
  }

  .callout-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
  }

  .callout-label {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .callout-source {
    font-family: var(--font-family-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
  }

  .callout-value {
    font-family: var(--font-family-mono);
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.1;
    font-variant-numeric: tabular-nums;
  }

  .callout-sub {
    font-size: 0.825rem;
    color: var(--text-muted);
    margin-top: 0.35rem;
    line-height: 1.4;
  }

  /* Variants */
  .variant-critical {
    border-left: 4px solid var(--threat-critical);
  }
  .variant-critical .callout-value {
    color: var(--threat-critical);
  }
  .variant-critical .callout-label {
    color: var(--threat-critical);
  }

  .variant-sovereign {
    border-left: 4px solid var(--threat-sovereign);
  }
  .variant-sovereign .callout-value {
    color: var(--threat-sovereign);
  }
  .variant-sovereign .callout-label {
    color: var(--threat-sovereign);
  }

  .variant-telemetry {
    border-left: 4px solid var(--threat-telemetry);
  }
  .variant-telemetry .callout-value {
    color: var(--threat-telemetry);
  }
  .variant-telemetry .callout-label {
    color: var(--threat-telemetry);
  }

  .variant-warning {
    border-left: 4px solid var(--threat-warning);
  }
  .variant-warning .callout-value {
    color: var(--threat-warning);
  }
  .variant-warning .callout-label {
    color: var(--threat-warning);
  }
</style>
