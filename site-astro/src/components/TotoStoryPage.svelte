<script lang="ts">
  import { onMount } from 'svelte';
  import { dict, initLocale } from '../i18n/store';
  import TotoIllustration from './TotoIllustration.svelte';
  import TotoCinemaPlayer from './TotoCinemaPlayer.svelte';

  export let base = '';

  onMount(() => {
    initLocale();
  });
</script>

<section class="toto-story-main">
  <!-- Hero Character Portrait + Concise Intro -->
  <header class="toto-hero-header">
    <div class="toto-portrait-wrap">
      <img
        src={`${base}/assets/toto-character.webp`}
        alt={$dict.totoCard.svgAlt}
        width="136"
        height="136"
        decoding="async"
        class="toto-hero-portrait"
      />
    </div>
    <div class="toto-head-copy">
      <span class="toto-pill">{$dict.totoPage.eyebrow}</span>
      <h1>{$dict.totoPage.title}</h1>
      <p class="toto-lead">{$dict.totoPage.lead}</p>
      <div class="toto-top-cta">
        <a href={`${base}/#wish-doors`} class="btn-start">
          {$dict.totoPage.backCta} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
        </a>
        <a href={`${base}/`} class="btn-home">{$dict.totoPage.homeLink}</a>
      </div>
    </div>
  </header>

  <!-- Animated Intro Video Over Global Cities -->
  <div class="toto-cinema-showcase">
    <TotoCinemaPlayer base={base} compact={false} />
  </div>

  <!-- Compact Visual Expression Strip -->
  <div class="poses-row" aria-label={$dict.totoPage.posesLabel}>
    <figure class="pose-card">
      <TotoIllustration pose="calm" size={62} label={$dict.totoPage.poses[0].alt} />
      <figcaption>
        <strong>{$dict.totoPage.poses[0].name}</strong>
        <span>{$dict.totoPage.poses[0].caption}</span>
      </figcaption>
    </figure>
    <figure class="pose-card">
      <TotoIllustration pose="curious" size={62} label={$dict.totoPage.poses[1].alt} />
      <figcaption>
        <strong>{$dict.totoPage.poses[1].name}</strong>
        <span>{$dict.totoPage.poses[1].caption}</span>
      </figcaption>
    </figure>
    <figure class="pose-card">
      <TotoIllustration pose="apologetic" size={62} label={$dict.totoPage.poses[2].alt} />
      <figcaption>
        <strong>{$dict.totoPage.poses[2].name}</strong>
        <span>{$dict.totoPage.poses[2].caption}</span>
      </figcaption>
    </figure>
  </div>

  <!-- Structured Character Guide: Paired Identity + Numbered Rules -->
  <div class="guide-layout">
    <div class="identity-pair">
      <article class="story-card accent-card">
        <h2>{$dict.totoPage.whoTitle}</h2>
        <p>{$dict.totoPage.whoBody}</p>
      </article>

      <article class="story-card">
        <h2>{$dict.totoPage.notTitle}</h2>
        <p>{$dict.totoPage.notBody}</p>
      </article>
    </div>

    <article class="story-card rules-card">
      <h2>{$dict.totoPage.rulesTitle}</h2>
      <ol class="numbered-rules">
        {#each $dict.totoPage.rules as rule, idx}
          <li>
            <span class="rule-badge" aria-hidden="true">{idx + 1}</span>
            <span>{rule}</span>
          </li>
        {/each}
      </ol>
    </article>
  </div>

  <!-- Relocated Background Guides (Compact Mobile Grid) -->
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

  <!-- Why a Ready World Matters (Visual Icons + Tight Prose) -->
  <section class="toto-extra-section" aria-label={$dict.wisher.heading}>
    <h2>{$dict.wisher.heading}</h2>
    <div class="wisher-grid">
      {#each $dict.wisher.cards as card, idx}
        <article class="story-card">
          <div class="wc-title-row">
            <span class="wc-icon" aria-hidden="true">
              {#if idx === 0}
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z" stroke-linejoin="round" />
                </svg>
              {:else}
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="6" cy="12" r="3" />
                  <circle cx="18" cy="6" r="3" />
                  <circle cx="18" cy="18" r="3" />
                  <path d="M8.7 10.7l6.6-3.4M8.7 13.3l6.6 3.4" />
                </svg>
              {/if}
            </span>
            <h3>{card.title}</h3>
          </div>
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

  <!-- Weekly Episode & Private Wall (Digestible Chips + Collapsible Details) -->
  <section id="this-week" class="toto-extra-section" aria-label={$dict.episode.heading}>
    <h2>{$dict.episode.heading}</h2>
    <div class="wisher-grid">
      <article class="story-card">
        <span class="toto-pill">{$dict.episode.badge}</span>
        <h3>{$dict.episode.episodeLabel}: &ldquo;{$dict.episode.title}&rdquo;</h3>
        <p>{$dict.episode.synopsis}</p>
        <p class="muted-note">{$dict.episode.voteNote}</p>
      </article>

      <article class="story-card">
        <h3>{$dict.wishWall.heading}</h3>
        <div class="theme-chips" aria-label={$dict.wishWall.heading}>
          {#each $dict.wishWall.themes as th}
            <span class="theme-chip">{th}</span>
          {/each}
        </div>
        <p>{$dict.wishWall.emptyHeadline}</p>
        <details class="card-tech">
          <summary>{$dict.episode.recapTitle}</summary>
          <p>{$dict.wishWall.emptyBody}</p>
          <p class="muted-note">{$dict.episode.recapStatus}</p>
        </details>
      </article>
    </div>
  </section>
</section>

<style>
  .toto-story-main {
    max-width: 960px;
    margin: 0 auto;
    padding: 2rem 1.25rem 3rem;
  }

  /* Hero Portrait + Intro */
  .toto-hero-header {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-medium);
    border-radius: 18px;
    padding: 1.35rem 1.5rem;
    margin-bottom: 1.35rem;
    box-shadow: var(--shadow-sm);
  }

  .toto-portrait-wrap {
    flex-shrink: 0;
    width: 136px;
    height: 136px;
    border-radius: 20px;
    overflow: hidden;
    background: #fbf7ee;
    border: 1px solid var(--border-medium);
  }

  .toto-hero-portrait {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    animation: totoGentleFloat 3.8s ease-in-out infinite;
  }

  @keyframes totoGentleFloat {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-3px) scale(1.02); }
  }

  @media (prefers-reduced-motion: reduce) {
    .toto-hero-portrait {
      animation: none !important;
    }
  }

  .toto-head-copy {
    flex: 1 1 auto;
    min-width: 0;
  }

  .toto-pill {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
    padding: 0.22rem 0.65rem;
    border-radius: 9999px;
    margin-bottom: 0.5rem;
  }

  :global([dir='rtl']) .toto-pill {
    font-family: var(--font-family-sans);
    letter-spacing: 0;
  }

  .toto-head-copy h1 {
    font-size: clamp(1.7rem, 3.4vw, 2.35rem);
    font-weight: 800;
    margin: 0 0 0.4rem;
    color: var(--text-primary);
    line-height: 1.15;
  }

  .toto-lead {
    font-size: 0.98rem;
    line-height: 1.55;
    color: var(--text-secondary);
    margin: 0 0 0.9rem;
    max-width: 58ch;
  }

  .toto-top-cta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    align-items: center;
  }

  .btn-start {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    min-height: 42px;
    padding: 0.55rem 1.15rem;
    border-radius: 10px;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    text-decoration: none;
    font-weight: 700;
    font-size: 0.9rem;
  }

  .btn-home {
    font-weight: 700;
    font-size: 0.88rem;
    color: var(--accent-primary);
    text-decoration: none;
  }

  .toto-cinema-showcase {
    margin-bottom: 1.4rem;
  }

  /* Poses */
  .poses-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.85rem;
    margin-bottom: 1.35rem;
  }

  .pose-card {
    margin: 0;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.5rem;
  }

  .pose-card figcaption {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }

  .pose-card strong {
    font-size: 0.94rem;
    color: var(--text-primary);
  }

  .pose-card span {
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.42;
  }

  /* Identity & Numbered Rules */
  .guide-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.9rem;
    margin-bottom: 1.5rem;
  }

  .identity-pair {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
  }

  .story-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1rem 1.1rem;
  }

  .accent-card {
    border-inline-start: 4px solid var(--accent-primary);
  }

  .story-card h2,
  .story-card h3 {
    font-size: 1.04rem;
    margin: 0 0 0.42rem;
    color: var(--accent-primary);
  }

  .story-card p {
    font-size: 0.89rem;
    line-height: 1.52;
    color: var(--text-secondary);
    margin: 0 0 0.45rem;
  }

  .story-card p:last-child {
    margin-bottom: 0;
  }

  .numbered-rules {
    list-style: none;
    padding: 0;
    margin: 0.35rem 0 0;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  .numbered-rules li {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    font-size: 0.89rem;
    line-height: 1.48;
    color: var(--text-secondary);
  }

  .rule-badge {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
    color: var(--accent-primary);
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-top: 0.05rem;
  }

  /* Relocated Sections */
  .toto-extra-section {
    margin-top: 1.75rem;
    padding-top: 1.45rem;
    border-top: 1px solid var(--border-subtle);
  }

  .toto-extra-section h2 {
    text-align: center;
    font-size: clamp(1.2rem, 2.4vw, 1.5rem);
    margin: 0 0 0.9rem;
    color: var(--text-primary);
  }

  .beats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.7rem;
    margin-bottom: 0.85rem;
  }

  .beat-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 0.8rem 0.85rem;
  }

  .beat-num {
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .beat-card h3 {
    margin: 0.18rem 0 0.2rem;
    font-size: 0.98rem;
    color: var(--text-primary);
  }

  .beat-card p {
    margin: 0;
    font-size: 0.84rem;
    color: var(--text-secondary);
    line-height: 1.38;
  }

  .beats-footer {
    text-align: center;
    font-weight: 800;
    font-size: 0.94rem;
    color: var(--accent-primary);
    margin: 0;
  }

  .wisher-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.9rem;
    margin-bottom: 0.85rem;
  }

  .wc-title-row {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.4rem;
  }

  .wc-title-row h3 {
    margin: 0;
    color: var(--text-primary);
  }

  .wc-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 8px;
    background: var(--threat-sovereign-bg);
    color: var(--accent-primary);
  }

  .theme-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.38rem;
    margin: 0.25rem 0 0.6rem;
  }

  .theme-chip {
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.18rem 0.55rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
  }

  .card-tech {
    margin-top: 0.35rem;
  }

  .card-tech summary {
    cursor: pointer;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--accent-primary);
  }

  .card-tech p {
    margin-top: 0.35rem;
    font-size: 0.82rem;
  }

  .muted-note {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
  }

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  @media (max-width: 760px) {
    .toto-story-main {
      padding: 1.2rem 0.9rem 2rem;
    }

    .toto-hero-header {
      flex-direction: column;
      text-align: center;
      gap: 0.85rem;
      padding: 1.05rem;
    }

    .toto-portrait-wrap {
      width: 104px;
      height: 104px;
      border-radius: 16px;
    }

    .toto-top-cta {
      justify-content: center;
    }

    .poses-row {
      grid-template-columns: 1fr;
      gap: 0.55rem;
    }

    .pose-card {
      flex-direction: row;
      text-align: start;
      align-items: center;
      padding: 0.68rem 0.8rem;
      gap: 0.75rem;
    }

    .guide-layout,
    .wisher-grid {
      grid-template-columns: 1fr;
      gap: 0.7rem;
    }

    .beats-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 0.55rem;
    }
  }
</style>
