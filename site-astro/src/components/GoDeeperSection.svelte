<script lang="ts">
  import { dict, localeReady, resolveViewDict, type LocaleKey } from '../i18n/store';
  import type { TranslationDict } from '../i18n/en';

  export let base = '';
  export let ssrLocale: LocaleKey = 'en';
  export let ssrDict: Partial<TranslationDict> | undefined = undefined;

  $: d = resolveViewDict($dict, $localeReady, ssrLocale, ssrDict);
</script>

<section id="go-deeper" class="evidence-section">
  <div class="story-container">
    <div class="es-head">
      <span class="es-kicker">{d.deeper.eyebrow}</span>
      <h2>{d.deeper.heading}</h2>
      <p>{d.deeper.subhead}</p>
    </div>

    <!-- Non-redundant Empirical Scope Proof Cards (full site navigation lives cleanly in footer below) -->
    <div class="proof-stats" aria-label={d.deeper.heading}>
      <div class="ps-card">
        <strong>39</strong>
        <span>{d.deeper.statNations}</span>
      </div>
      <div class="ps-card">
        <strong>96.5%</strong>
        <span>{d.deeper.statCompleteness}</span>
      </div>
      <div class="ps-card">
        <strong>26</strong>
        <span>{d.deeper.statScenarios}</span>
      </div>
      <div class="ps-card">
        <strong>14</strong>
        <span>{d.deeper.statSignals}</span>
      </div>
    </div>

    <div class="es-actions">
      <a href={`${base}/sandbox/`} class="es-primary-cta">
        {d.deeper.primaryCta} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
      </a>
      <details class="es-citation-note">
        <summary>{d.deeper.citationSummary}</summary>
        <p>{d.deeper.releaseNote}</p>
      </details>
    </div>
  </div>
</section>

<style>
  .evidence-section {
    contain: layout style;
    padding: 1.65rem 0;
    background: var(--bg-surface-sunken);
    border-top: 1px solid var(--border-subtle);
    border-bottom: 1px solid var(--border-subtle);
  }

  .story-container {
    max-width: 960px;
    margin: 0 auto;
    padding: 0 1.15rem;
    text-align: center;
  }

  .es-kicker {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    margin-bottom: 0.3rem;
  }

  .es-head h2 {
    margin: 0 0 0.25rem;
    font-size: clamp(1.22rem, 2.4vw, 1.55rem);
    font-weight: 800;
    color: var(--text-primary);
  }

  .es-head p {
    margin: 0 auto 1rem;
    max-width: 600px;
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.48;
  }

  .proof-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.65rem;
    margin-bottom: 1rem;
  }

  .ps-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 0.8rem 0.65rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.2rem;
  }

  .ps-card strong {
    font-family: var(--font-family-mono);
    font-size: 1.28rem;
    font-weight: 800;
    color: var(--accent-primary);
    line-height: 1.1;
  }

  .ps-card span {
    font-size: 0.76rem;
    color: var(--text-secondary);
    line-height: 1.3;
  }

  .es-actions {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.55rem;
  }

  .es-primary-cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    min-height: 42px;
    padding: 0.58rem 1.25rem;
    border-radius: 10px;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    font-size: 0.88rem;
    font-weight: 700;
    text-decoration: none;
  }

  .es-primary-cta:hover {
    background: var(--accent-primary-hover);
  }

  .es-citation-note {
    font-size: 0.78rem;
    color: var(--text-secondary);
    max-width: 660px;
  }

  .es-citation-note summary {
    cursor: pointer;
    font-weight: 600;
    color: var(--accent-primary);
  }

  .es-citation-note p {
    margin: 0.45rem 0 0;
    line-height: 1.45;
  }

  @media (max-width: 680px) {
    .proof-stats {
      grid-template-columns: repeat(2, 1fr);
      gap: 0.5rem;
    }

    .es-primary-cta {
      width: 100%;
    }
  }
</style>
