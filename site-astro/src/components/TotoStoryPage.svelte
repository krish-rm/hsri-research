<script lang="ts">
  import { onMount } from 'svelte';
  import { dict, initLocale } from '../i18n/store';
  import TotoIllustration from './TotoIllustration.svelte';

  export let base = '';

  onMount(() => {
    initLocale();
  });
</script>

<section class="toto-story-main">
  <div class="toto-head">
    <span class="toto-pill">{$dict.totoPage.eyebrow}</span>
    <h1>{$dict.totoPage.title}</h1>
    <p class="toto-lead">{$dict.totoPage.lead}</p>
  </div>

  <!-- Interactive / Accessible Pose Strip -->
  <div class="poses-row" aria-label={$dict.totoPage.posesLabel}>
    <figure class="pose-card">
      <TotoIllustration pose="calm" size={84} label={$dict.totoPage.poses[0].alt} />
      <figcaption>
        <strong>{$dict.totoPage.poses[0].name}</strong>
        <span>{$dict.totoPage.poses[0].caption}</span>
      </figcaption>
    </figure>
    <figure class="pose-card">
      <TotoIllustration pose="curious" size={84} label={$dict.totoPage.poses[1].alt} />
      <figcaption>
        <strong>{$dict.totoPage.poses[1].name}</strong>
        <span>{$dict.totoPage.poses[1].caption}</span>
      </figcaption>
    </figure>
    <figure class="pose-card">
      <TotoIllustration pose="apologetic" size={84} label={$dict.totoPage.poses[2].alt} />
      <figcaption>
        <strong>{$dict.totoPage.poses[2].name}</strong>
        <span>{$dict.totoPage.poses[2].caption}</span>
      </figcaption>
    </figure>
  </div>

  <!-- Three Core Sections (Section 9.2 C) -->
  <div class="sections-grid">
    <article class="story-card">
      <h2>{$dict.totoPage.whoTitle}</h2>
      <p>{$dict.totoPage.whoBody}</p>
    </article>

    <article class="story-card">
      <h2>{$dict.totoPage.rulesTitle}</h2>
      <ul>
        {#each $dict.totoPage.rules as rule}
          <li>{rule}</li>
        {/each}
      </ul>
    </article>

    <article class="story-card">
      <h2>{$dict.totoPage.notTitle}</h2>
      <p>{$dict.totoPage.notBody}</p>
    </article>
  </div>

  <div class="toto-footer-cta">
    <a href={`${base}/#wish-doors`} class="btn-start">
      {$dict.totoPage.backCta} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
    </a>
    <a href={`${base}/`} class="btn-home">{$dict.totoPage.homeLink}</a>
  </div>
</section>

<style>
  .toto-story-main {
    max-width: 960px;
    margin: 0 auto;
    padding: 2.5rem 1.25rem 3.5rem;
  }

  .toto-head {
    text-align: center;
    max-width: 720px;
    margin: 0 auto 2rem;
  }

  .toto-pill {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 0.65rem;
  }

  :global([dir='rtl']) .toto-pill {
    font-family: var(--font-family-sans);
    letter-spacing: 0;
  }

  .toto-head h1 {
    font-size: clamp(1.85rem, 3.6vw, 2.6rem);
    font-weight: 800;
    margin: 0 0 0.65rem;
    color: var(--text-primary);
  }

  .toto-lead {
    font-size: 1.04rem;
    line-height: 1.65;
    color: var(--text-secondary);
    margin: 0;
  }

  .poses-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.75rem;
  }

  .pose-card {
    margin: 0;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1.1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.65rem;
  }

  .pose-card figcaption {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }

  .pose-card strong {
    font-size: 0.96rem;
    color: var(--text-primary);
  }

  .pose-card span {
    font-size: 0.82rem;
    color: var(--text-secondary);
  }

  .sections-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .story-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1.25rem;
  }

  .story-card h2 {
    font-size: 1.12rem;
    margin: 0 0 0.55rem;
    color: var(--accent-primary);
  }

  .story-card p,
  .story-card li {
    font-size: 0.9rem;
    line-height: 1.6;
    color: var(--text-secondary);
  }

  .story-card ul {
    margin: 0;
    padding-inline-start: 1.2rem;
  }

  .toto-footer-cta {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.85rem;
    align-items: center;
  }

  .btn-start {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    min-height: 44px;
    padding: 0.65rem 1.3rem;
    border-radius: 10px;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    text-decoration: none;
    font-weight: 700;
    font-size: 0.94rem;
  }

  .btn-home {
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--accent-primary);
    text-decoration: none;
  }

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  @media (max-width: 760px) {
    .poses-row,
    .sections-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
