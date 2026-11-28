<script lang="ts">
  import { dict } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';
  import { countryContextStore } from '../lib/countryContext';
  import TotoCinemaPlayer from './TotoCinemaPlayer.svelte';

  export let base = '';

  $: activeCountryName =
    $countryContextStore.iso && $countryContextStore.iso !== 'GLOBAL'
      ? $countryContextStore.countryName
      : '';

  function handleCta(target: 'breakthrough' | 'country') {
    trackEvent('hero_cta_click', { target });
  }
</script>

<section class="hero-story">
  <div class="hero-container">
    <div class="hero-grid">
      <!-- Left: Primary Question, Clear Value Prop & Directional Cue to Toto's Country Chooser -->
      <div class="hero-copy">
        <div class="eyebrow-pill">
          <span class="pulse-dot" aria-hidden="true"></span>
          <span>{$dict.hero.eyebrow}</span>
        </div>

        <h1 class="hero-title">
          {$dict.hero.headlineLead}<span class="hero-title-accent">{$dict.hero.headlineAccent}</span>
        </h1>

        <p class="hero-subhead">{$dict.hero.subhead}</p>

        <div class="hero-start-cue">
          <span class="hsc-step" aria-hidden="true">1</span>
          <span class="hsc-text">
            {$dict.hero.guideCue}
            <strong id="hero-cue-country">{activeCountryName || $dict.hero.cityNeutralName}</strong>
            <span class="hsc-arrow hsc-desktop arrow-flip" aria-hidden="true">&rarr;</span>
            <span class="hsc-arrow hsc-mobile" aria-hidden="true">&darr;</span>
          </span>
        </div>
      </div>

      <!-- Right: 1. Choose Country in Toto Cinema -> 2. Country-Aware Actions -->
      <div class="hero-visual">
        <TotoCinemaPlayer base={base} compact={true} />

        <div class="cta-row">
          <a href="#wish-doors" class="btn-primary-hero" onclick={() => handleCta('breakthrough')}>
            <span id="hero-cta-primary-label">
              {activeCountryName
                ? $dict.hero.ctaCountryPrimary.replace('{country}', activeCountryName)
                : $dict.hero.ctaPrimary}
            </span>
            <span class="arrow-flip" aria-hidden="true">&rarr;</span>
          </a>
          <a href="#country-check" class="btn-secondary-hero" onclick={() => handleCta('country')}>
            <span id="hero-cta-secondary-label">
              {activeCountryName
                ? $dict.hero.ctaCountrySecondary.replace('{country}', activeCountryName)
                : $dict.hero.ctaSecondary}
            </span>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .hero-story {
    contain: layout style;
    padding: clamp(1.35rem, 3vw, 2.35rem) 0 clamp(1.2rem, 2.5vw, 1.9rem);
    background: radial-gradient(900px 420px at 50% 0%, var(--accent-primary-glow), transparent 65%),
      var(--bg-canvas);
  }

  .hero-container {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 1.15rem;
  }

  .hero-grid {
    display: grid;
    grid-template-columns: 1.05fr 1fr;
    gap: clamp(1.2rem, 3vw, 2.25rem);
    align-items: center;
  }

  .eyebrow-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.28rem 0.8rem;
    border-radius: 9999px;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    margin-bottom: 0.7rem;
  }

  :global([dir='rtl']) .eyebrow-pill {
    font-family: var(--font-family-sans);
    letter-spacing: 0;
  }

  .pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent-primary);
  }

  .hero-title {
    font-family: var(--font-family-display);
    font-size: clamp(1.8rem, 3.85vw, 2.88rem);
    font-weight: 800;
    line-height: 1.36;
    letter-spacing: -0.01em;
    color: var(--text-primary);
    max-width: 21ch;
    margin: 0 0 0.8rem;
  }

  .hero-title-accent {
    color: var(--accent-primary);
  }

  :global([dir='rtl']) .hero-title {
    font-family: var(--font-family-sans);
    font-weight: 800;
    letter-spacing: 0;
    line-height: 1.28;
  }

  .hero-subhead {
    font-size: clamp(0.96rem, 1.5vw, 1.1rem);
    line-height: 1.56;
    color: var(--text-secondary);
    max-width: 520px;
    margin: 0 0 1.15rem;
  }

  .hero-start-cue {
    display: inline-flex;
    align-items: center;
    gap: 0.48rem;
    padding: 0.45rem 0.78rem;
    border-radius: 12px;
    background: var(--bg-surface-elevated);
    border: 1px dashed var(--threat-sovereign-border);
    font-size: 0.84rem;
    color: var(--text-secondary);
  }

  .hsc-step {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    flex-shrink: 0;
  }

  .hsc-text {
    line-height: 1.38;
  }

  .hsc-text strong {
    color: var(--accent-primary);
  }

  .hsc-arrow {
    font-weight: 800;
    color: var(--accent-primary);
    margin-inline-start: 0.25rem;
    white-space: nowrap;
  }

  .hsc-mobile {
    display: none;
  }

  .cta-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.55rem;
  }

  .btn-primary-hero,
  .btn-secondary-hero {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    min-height: 44px;
    padding: 0.58rem 0.95rem;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.88rem;
    text-align: center;
    text-decoration: none;
    transition: transform 0.16s ease, background-color 0.16s ease, border-color 0.16s ease;
  }

  .btn-primary-hero {
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    box-shadow: var(--shadow-sm);
  }

  .btn-primary-hero:hover {
    background: var(--accent-primary-hover);
    transform: translateY(-1px);
  }

  .btn-secondary-hero {
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    border: 1.5px solid var(--border-medium);
  }

  .btn-secondary-hero:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .hero-visual {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  @media (max-width: 920px) {
    .hero-grid {
      grid-template-columns: 1fr;
    }
    .hsc-desktop {
      display: none;
    }
    .hsc-mobile {
      display: inline;
    }
  }

  @media (max-width: 520px) {
    .cta-row {
      grid-template-columns: 1fr;
    }
  }
</style>
