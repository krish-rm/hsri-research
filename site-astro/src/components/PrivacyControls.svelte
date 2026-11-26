<script lang="ts">
  import { onMount } from 'svelte';
  import { readAllLocalData, clearAllLocalData } from '../lib/privacyStorage';

  let snapshot: Record<string, unknown> = {};
  let keysCount = 0;
  let statusMessage = '';

  function refresh() {
    snapshot = readAllLocalData();
    keysCount = Object.keys(snapshot).length;
  }

  function exportJson() {
    refresh();
    const blob = new Blob([JSON.stringify(snapshot, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `humanity-readiness-local-data-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    statusMessage = 'Downloaded a copy of your local browser state.';
  }

  function wipeData() {
    const count = clearAllLocalData();
    refresh();
    statusMessage = count > 0
      ? `Cleared ${count} local record(s) from this browser.`
      : 'No local Humanity Readiness records were stored.';
  }

  onMount(() => {
    refresh();
  });
</script>

<div class="privacy-controls">
  <div class="pc-head">
    <h3>Manage Your Local Browser State (<code>hr:v1:*</code>)</h3>
    <span class="pc-count">{keysCount} active key{keysCount === 1 ? '' : 's'}</span>
  </div>

  <p class="pc-copy">
    Your choices, five readiness lights, preferred language mode, and navigation state stay strictly inside your device's browser storage. Nothing is uploaded without your explicit consent.
  </p>

  <div class="pc-actions">
    <button type="button" class="btn-inspect" onclick={refresh}>Refresh View</button>
    <button type="button" class="btn-export" onclick={exportJson}>Export My Data (JSON)</button>
    <button type="button" class="btn-delete" onclick={wipeData}>Delete All My Local Data</button>
  </div>

  {#if statusMessage}
    <p class="pc-status" role="status">{statusMessage}</p>
  {/if}

  <pre class="pc-json">{keysCount > 0 ? JSON.stringify(snapshot, null, 2) : '// No hr:v1:* keys stored on this browser yet.'}</pre>
</div>

<style>
  .privacy-controls {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1.35rem;
    margin: 1.5rem 0;
  }

  .pc-head {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .pc-head h3 {
    margin: 0;
    font-size: 1.08rem;
  }

  .pc-count {
    font-family: var(--font-family-mono);
    font-size: 0.76rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    color: var(--accent-primary);
  }

  .pc-copy {
    font-size: 0.92rem;
    color: var(--text-secondary);
    margin: 0 0 1rem;
    line-height: 1.55;
  }

  .pc-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    margin-bottom: 0.9rem;
  }

  .pc-actions button {
    min-height: 40px;
    padding: 0.5rem 0.95rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.84rem;
    cursor: pointer;
    border: 1px solid var(--border-medium);
  }

  .btn-inspect {
    background: var(--bg-surface);
    color: var(--text-primary);
  }

  .btn-export {
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    border-color: var(--accent-primary);
  }

  .btn-delete {
    background: var(--threat-critical-bg);
    color: var(--threat-critical);
    border-color: var(--threat-critical-border);
  }

  .pc-status {
    font-size: 0.84rem;
    font-weight: 600;
    color: var(--accent-primary);
    margin: 0 0 0.75rem;
  }

  .pc-json {
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.85rem;
    font-family: var(--font-family-mono);
    font-size: 0.78rem;
    overflow-x: auto;
    color: var(--text-secondary);
    margin: 0;
  }
</style>
