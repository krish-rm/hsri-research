<script lang="ts">
  import { dict } from '../i18n/store';
  import TotoIllustration from './TotoIllustration.svelte';

  export let base = '';
</script>

<section id="meet-toto" class="meet-toto-section">
  <div class="toto-container">
    <div class="toto-card">
      <div class="toto-avatar-col">
        <TotoIllustration pose="curious" size={104} label={$dict.totoCard.svgAlt} />
      </div>

      <div class="toto-copy-col">
        <span class="toto-eyebrow">{$dict.totoCard.eyebrow}</span>
        <h2 class="toto-heading">{$dict.totoCard.heading}</h2>
        <p class="toto-body">{$dict.totoCard.body}</p>

        <div class="toto-chips" aria-label={$dict.totoCard.chipsLabel}>
          {#each $dict.totoCard.chips as chip}
            <span class="toto-chip">{chip}</span>
          {/each}
        </div>

        <div class="toto-actions">
          <a href="#wish-doors" class="btn-toto-primary">
            {$dict.totoCard.ctaPrimary} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
          </a>
          <a href={`${base}/toto/`} class="btn-toto-secondary">
            {$dict.totoCard.ctaSecondary}
          </a>
        </div>

        <p class="toto-footnote">{$dict.totoCard.footnote}</p>
      </div>
    </div>
  </div>
</section>

<style>
  .meet-toto-section {
    contain: layout style;
    padding: clamp(1.75rem, 3.5vw, 2.75rem) 0;
    min-height: 292px;
  }

  .toto-container {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 1.15rem;
    box-sizing: border-box;
  }

  .toto-card {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 1.5rem 2rem;
    align-items: center;
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-medium);
    border-radius: 18px;
    padding: clamp(1.25rem, 3vw, 1.85rem);
    box-shadow: var(--shadow-sm);
  }

  .toto-avatar-col {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0.45rem;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    border-radius: 9999px;
  }

  .toto-eyebrow {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    margin-bottom: 0.35rem;
  }

  :global([dir='rtl']) .toto-eyebrow {
    font-family: var(--font-family-sans);
    letter-spacing: 0;
  }

  .toto-heading {
    font-family: var(--font-family-sans);
    font-size: clamp(1.38rem, 2.6vw, 1.85rem);
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 0.55rem;
    line-height: 1.25;
  }

  .toto-body {
    font-size: 0.96rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin: 0 0 0.85rem;
    max-width: 72ch;
  }

  .toto-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-bottom: 1rem;
  }

  .toto-chip {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.22rem 0.65rem;
    border-radius: 9999px;
    background: var(--threat-sovereign-bg);
    color: var(--threat-sovereign);
    border: 1px solid var(--threat-sovereign-border);
  }

  :global([dir='rtl']) .toto-chip {
    font-family: var(--font-family-sans);
  }

  .toto-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    margin-bottom: 0.85rem;
  }

  .btn-toto-primary,
  .btn-toto-secondary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    min-height: 44px;
    padding: 0.6rem 1.2rem;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.9rem;
    text-decoration: none;
  }

  .btn-toto-primary {
    background: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .btn-toto-primary:hover {
    background: var(--accent-primary-hover);
  }

  .btn-toto-secondary {
    background: var(--bg-surface);
    color: var(--text-primary);
    border: 1.5px solid var(--border-medium);
  }

  .btn-toto-secondary:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .toto-footnote {
    margin: 0;
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-style: italic;
  }

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  @media (max-width: 720px) {
    .meet-toto-section {
      min-height: 470px;
    }
    .toto-card {
      grid-template-columns: 1fr;
      text-align: start;
      gap: 1rem;
    }
    .toto-avatar-col {
      justify-self: start;
    }
    .btn-toto-primary,
    .btn-toto-secondary {
      width: 100%;
    }
  }
</style>
