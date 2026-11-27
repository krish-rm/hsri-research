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

  <!-- Relocated Background Guides & Community Roadmap (keeping / overload-free) -->
  <section class="toto-extra-section" aria-label={$dict.beats.heading}>
    <h2>{$dict.beats.heading}</h2>
    <div class="beats-grid">
      {#each $dict.beats.items as beat, idx}
        <div class="beat-card">
          <span class="beat-num">0{idx + 1}</span>
          <h3>{beat.key}</h3>
          <p>{beat.desc}</p>
        </div>
      {/each}
    </div>
    <p class="beats-footer">{$dict.beats.footerLine}</p>
  </section>

  <section class="toto-extra-section" aria-label={$dict.wisher.heading}>
    <h2>{$dict.wisher.heading}</h2>
    <div class="wisher-grid">
      {#each $dict.wisher.cards as card}
        <article class="story-card">
          <h3>{card.title}</h3>
          <p>{card.body}</p>
          <details class="card-tech">
            <summary>&#9432; {$dict.pulse.tooltipTrigger}</summary>
            <p>{card.techHint}</p>
          </details>
        </article>
      {/each}
    </div>
    <p class="beats-footer">{$dict.wisher.closingLine}</p>
  </section>

  <section id="this-week" class="toto-extra-section" aria-label={$dict.episode.heading}>
    <h2>{$dict.episode.heading}</h2>
    <div class="wisher-grid">
      <article class="story-card">
        <span class="toto-pill">{$dict.episode.badge}</span>
        <h3>Episode 1: &ldquo;{$dict.episode.title}&rdquo;</h3>
        <p>{$dict.episode.synopsis}</p>
        <p class="muted-note">{$dict.episode.voteNote}</p>
      </article>
      <article class="story-card">
        <h3>{$dict.wishWall.heading}</h3>
        <p>{$dict.wishWall.emptyHeadline}</p>
        <p>{$dict.wishWall.emptyBody}</p>
        <p class="muted-note">{$dict.episode.recapTitle}: {$dict.episode.recapStatus}</p>
      </article>
    </div>
  </section>
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

  .toto-extra-section {
    margin-top: 2.25rem;
    padding-top: 1.75rem;
    border-top: 1px solid var(--border-subtle);
  }

  .toto-extra-section h2 {
    text-align: center;
    font-size: clamp(1.25rem, 2.5vw, 1.6rem);
    margin: 0 0 1rem;
    color: var(--text-primary);
  }

  .beats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  .beat-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 0.9rem;
  }

  .beat-num {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .beat-card h3 {
    margin: 0.2rem 0 0.25rem;
    font-size: 1rem;
    color: var(--text-primary);
  }

  .beat-card p {
    margin: 0;
    font-size: 0.86rem;
    color: var(--text-secondary);
  }

  .beats-footer {
    text-align: center;
    font-weight: 800;
    color: var(--accent-primary);
    margin: 0;
  }

  .wisher-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .story-card h3 {
    margin: 0 0 0.45rem;
    font-size: 1.06rem;
    color: var(--text-primary);
  }

  .card-tech summary {
    cursor: pointer;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .muted-note {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 0;
  }

  @media (max-width: 760px) {
    .poses-row,
    .sections-grid,
    .beats-grid,
    .wisher-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
