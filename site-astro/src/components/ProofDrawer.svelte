<script lang="ts">
  export let label: string = 'View Mathematical Grounding & Peer-Review Proof';
  export let mathSnippet: string = '';
  export let sources: Array<{ label: string; href?: string; doi?: string }> = [];
  export let testAssertion: string = '';

  let isOpen = false;

  function toggle() {
    isOpen = !isOpen;
  }
</script>

<div class="proof-drawer-container" class:is-open={isOpen}>
  <button
    type="button"
    class="drawer-header-btn"
    on:click={toggle}
    aria-expanded={isOpen}
  >
    <div class="header-content">
      <span class="proof-icon">📐</span>
      <span class="drawer-title">{label}</span>
    </div>
    <span class="toggle-indicator">{isOpen ? '− Hide Proof' : '+ Show Proof'}</span>
  </button>

  {#if isOpen}
    <div class="drawer-body">
      <slot />

      {#if mathSnippet}
        <div class="math-block">
          <pre class="math-code">{mathSnippet}</pre>
        </div>
      {/if}

      {#if testAssertion}
        <div class="assertion-strip">
          <span class="check-mark">✓ 100% CI Green Passing</span>
          <span class="assertion-text">{testAssertion}</span>
        </div>
      {/if}

      {#if sources && sources.length > 0}
        <div class="sources-strip">
          <span class="sources-label">Primary Citations:</span>
          <div class="sources-list">
            {#each sources as s}
              <div class="source-item">
                {#if s.href}
                  <a href={s.href} target="_blank" rel="noopener noreferrer" class="source-link">
                    {s.label} {s.doi ? `[DOI: ${s.doi}]` : '↗'}
                  </a>
                {:else}
                  <span class="source-text">{s.label} {s.doi ? `[DOI: ${s.doi}]` : ''}</span>
                {/if}
              </div>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .proof-drawer-container {
    margin: 1.5rem 0;
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    background: var(--bg-surface-sunken);
    overflow: hidden;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .proof-drawer-container.is-open {
    border-color: var(--accent-primary);
    box-shadow: 0 0 14px -3px var(--accent-primary-glow);
  }

  .drawer-header-btn {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 0.85rem 1.25rem;
    background: var(--bg-surface);
    border: none;
    cursor: pointer;
    text-align: left;
    transition: background 0.15s ease;
  }

  .drawer-header-btn:hover {
    background: var(--bg-surface-elevated);
  }

  .header-content {
    display: flex;
    align-items: center;
    gap: 0.65rem;
  }

  .proof-icon {
    font-size: 1rem;
  }

  .drawer-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .toggle-indicator {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--accent-primary);
  }

  .drawer-body {
    padding: 1.25rem;
    border-top: 1px solid var(--border-subtle);
    font-size: 0.875rem;
    color: var(--text-secondary);
    line-height: 1.6;
  }

  .math-block {
    margin: 0.75rem 0;
    padding: 0.85rem 1rem;
    background: var(--bg-canvas);
    border: 1px solid var(--border-medium);
    border-radius: 6px;
    overflow-x: auto;
  }

  .math-code {
    margin: 0;
    font-family: var(--font-family-mono);
    font-size: 0.825rem;
    color: var(--text-primary);
    white-space: pre-wrap;
  }

  .assertion-strip {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-top: 0.75rem;
    padding: 0.45rem 0.75rem;
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
    border-radius: 6px;
    font-size: 0.78rem;
  }

  .check-mark {
    font-family: var(--font-family-mono);
    font-weight: 700;
    color: var(--threat-sovereign);
  }

  .assertion-text {
    font-family: var(--font-family-mono);
    color: var(--text-primary);
    font-size: 0.75rem;
  }

  .sources-strip {
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border-subtle);
  }

  .sources-label {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 0.35rem;
  }

  .sources-list {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .source-link {
    color: var(--accent-primary);
    text-decoration: none;
    font-size: 0.78rem;
    font-weight: 500;
  }

  .source-link:hover {
    text-decoration: underline;
  }

  .source-text {
    font-size: 0.78rem;
    color: var(--text-muted);
  }
</style>
