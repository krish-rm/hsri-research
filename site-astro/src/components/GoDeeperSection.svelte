<script lang="ts">
  import { onMount } from 'svelte';
  import { dict } from '../i18n/store';

  export let base = '';
  let revealed = false;

  onMount(() => {
    revealed = true;
  });
</script>

<section id="go-deeper" class="story-block alt-surface go-deeper-section">
  <div class="story-container">
    <div class="section-head">
      <h2 class="sec-title">{$dict.deeper.heading}</h2>
      <p class="sec-sub">{$dict.deeper.subhead}</p>
    </div>

    {#if revealed}
      <div class="deeper-grid">
        {#each $dict.deeper.cards as card}
          <article class="deeper-card">
            <span class="dc-tag">{card.tag}</span>
            <h3 class="dc-title">{card.title}</h3>
            <p class="dc-desc">{card.desc}</p>

            {#if 'extraLinks' in card && card.extraLinks}
              <div class="dc-multi-links">
                {#each card.extraLinks as sub}
                  <a href={`${base}${sub.href}`} class="dc-link-inline">{sub.label} &rarr;</a>
                {/each}
              </div>
            {:else}
              <a href={`${base}${card.href}`} class="dc-link">
                Open {card.title} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
              </a>
            {/if}
          </article>
        {/each}
      </div>
    {:else}
      <noscript>
        <ul class="noscript-links">
          <li><a href={`${base}/sandbox/`}>Open the Lab</a></li>
          <li><a href={`${base}/countries/`}>39-country index</a></li>
          <li><a href={`${base}/seismograph/`}>Live Pulse</a></li>
          <li><a href={`${base}/scenarios/`}>Scenario Atlas</a></li>
          <li><a href={`${base}/monograph/`}>The Monograph</a></li>
          <li><a href={`${base}/methodology/`}>Methodology</a></li>
          <li><a href={`${base}/data/`}>Data &amp; Downloads</a></li>
          <li><a href={`${base}/coverage/`}>Global Coverage Audit</a></li>
        </ul>
      </noscript>
    {/if}

    <div class="release-footer-box">
      <p class="release-note">{$dict.deeper.releaseNote}</p>
      <p class="release-doi">
        Permanent academic archive:
        <a href="https://doi.org/10.5281/zenodo.23441742" target="_blank" rel="noopener noreferrer">
          DOI 10.5281/zenodo.23441742
        </a>
        &middot; Open Access (CC BY-SA 4.0)
      </p>
    </div>
  </div>
</section>

<style>
  .go-deeper-section {
    contain: layout style;
    padding: clamp(2.25rem, 4.5vw, 3.75rem) 0;
    scroll-margin-top: 112px;
    background: var(--bg-surface-sunken);
    border-top: 1px solid var(--border-subtle);
    border-bottom: 1px solid var(--border-subtle);
    min-height: 802px;
  }

  .story-container {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 1.15rem;
    box-sizing: border-box;
  }

  .section-head {
    text-align: center;
    max-width: 720px;
    margin: 0 auto 2rem;
  }

  .sec-title {
    font-family: var(--font-family-sans);
    font-size: clamp(1.5rem, 3.2vw, 2.15rem);
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 0.55rem;
    line-height: 1.22;
    letter-spacing: -0.02em;
  }

  .sec-sub {
    font-size: clamp(0.98rem, 1.5vw, 1.08rem);
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.6;
  }

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  .deeper-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .deeper-card {
    contain: layout style;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
  }

  .dc-tag {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--accent-primary);
    margin-bottom: 0.4rem;
  }

  .dc-title {
    font-size: 1.08rem;
    font-weight: 700;
    margin: 0 0 0.45rem;
    color: var(--text-primary);
  }

  .dc-desc {
    margin: 0 0 1rem;
    font-size: 0.88rem;
    line-height: 1.52;
    color: var(--text-secondary);
    flex-grow: 1;
  }

  .dc-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    width: fit-content;
    padding: 0.5rem 0.95rem;
    border-radius: 8px;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 700;
  }

  .dc-link:hover {
    background: var(--accent-primary-hover);
  }

  .dc-multi-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 0.9rem;
  }

  .dc-link-inline {
    font-size: 0.84rem;
    font-weight: 700;
    color: var(--accent-primary);
    text-decoration: none;
  }

  .dc-link-inline:hover {
    text-decoration: underline;
  }

  .release-footer-box {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    text-align: center;
  }

  .release-note {
    margin: 0 0 0.35rem;
    font-size: 0.86rem;
    color: var(--text-secondary);
  }

  .release-doi {
    margin: 0;
    font-size: 0.82rem;
    color: var(--text-secondary);
  }

  .release-doi a {
    color: var(--accent-primary);
    font-weight: 600;
  }

  @media (max-width: 960px) {
    .go-deeper-section {
      min-height: 1120px;
    }
    .deeper-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 680px) {
    .go-deeper-section {
      min-height: 1743px;
    }
    .deeper-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
