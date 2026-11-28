<script lang="ts">
  import { dict } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';
  import TotoCinemaPlayer from './TotoCinemaPlayer.svelte';

  export let base = '';
  export let pulseKey: 'steady' | 'stirring' | 'rising' = 'rising';
  export let pulseScore = 8.44;

  $: clampedPulse = Math.max(0, Math.min(10, Number.isFinite(pulseScore) ? pulseScore : 8.44));
  $: needleAngleDeg = -90 + (clampedPulse / 10) * 180;

  function handleCta(target: 'breakthrough' | 'country') {
    trackEvent('hero_cta_click', { target });
  }
</script>

<section class="hero-story">
  <div class="hero-container">
    <div class="hero-grid">
      <!-- Left: Primary Question, Clear Value Prop & Actions -->
      <div class="hero-copy">
        <div class="eyebrow-pill">
          <span class="pulse-dot" aria-hidden="true"></span>
          <span>{$dict.hero.eyebrow}</span>
        </div>

        <h1 class="hero-title">
          {$dict.hero.headlineLead}<span class="hero-title-accent">{$dict.hero.headlineAccent}</span>
        </h1>

        <p class="hero-subhead">{$dict.hero.subhead}</p>

        <div class="cta-row">
          <a href="#wish-doors" class="btn-primary-hero" onclick={() => handleCta('breakthrough')}>
            {$dict.hero.ctaPrimary}
            <span class="arrow-flip" aria-hidden="true">&rarr;</span>
          </a>
          <a href="#country-check" class="btn-secondary-hero" onclick={() => handleCta('country')}>
            {$dict.hero.ctaSecondary}
          </a>
        </div>
      </div>

      <!-- Right / Visual Flow: 1. Video-Style Toto Intro Over Real Painted Cityscapes -> 2. Humanity's Pulse -->
      <div class="hero-visual">
        <TotoCinemaPlayer base={base} compact={true} />

        <!-- Humanity's Pulse Visual Card (Speedometer + Pace Gap Visual) -->
        <a href={`${base}/seismograph/`} class="pulse-visual-card">
          <div class="pv-gauge-wrap" aria-hidden="true">
            <svg viewBox="0 0 132 82" width="112" height="70" class="pv-dial-svg">
              <path d="M 16 68 A 50 50 0 0 1 42 25" fill="none" stroke="var(--threat-sovereign)" stroke-width="10" stroke-linecap="round" opacity="0.88" />
              <path d="M 47 22 A 50 50 0 0 1 92 27" fill="none" stroke="var(--threat-warning)" stroke-width="10" stroke-linecap="round" opacity="0.9" />
              <path d="M 97 30 A 50 50 0 0 1 116 68" fill="none" stroke="var(--threat-critical)" stroke-width="10" stroke-linecap="round" opacity="0.95" />

              <text x="10" y="79" class="pv-zone-lbl">0</text>
              <text x="66" y="12" text-anchor="middle" class="pv-zone-lbl">5</text>
              <text x="122" y="79" text-anchor="end" class="pv-zone-lbl">10</text>

              <g transform={`translate(66 68) rotate(${needleAngleDeg})`}>
                <polygon points="-3,0 0,-44 3,0" fill="var(--text-primary)" />
                <circle cx="0" cy="0" r="5.5" fill="var(--text-primary)" />
                <circle cx="0" cy="0" r="2" fill="var(--bg-surface-elevated)" />
              </g>
            </svg>
          </div>

          <div class="pv-info">
            <div class="pv-head-row">
              <span class="pv-title-line">
                <span class={`hm-dot state-${pulseKey}`} aria-hidden="true"></span>
                <span>{$dict.pulse.label}: <strong>{$dict.pulse.states[pulseKey].word}</strong></span>
              </span>
              <span class="pv-score-pill">{clampedPulse.toFixed(1)}/10</span>
            </div>

            <div class="pv-pace-bars" aria-hidden="true">
              <div class="pace-row">
                <span class="pace-lbl">Human pace</span>
                <span class="pace-track"><i class="pace-fill-human"></i></span>
              </div>
              <div class="pace-row">
                <span class="pace-lbl">AI pace (~3,200&times;)</span>
                <span class="pace-track"><i class="pace-fill-ai" style={`width:${Math.round(clampedPulse * 10)}%`}></i></span>
              </div>
            </div>

            <div class="pv-foot">
              <span class="pv-explain">{$dict.pulse.states[pulseKey].sentence}</span>
              <span class="mini-arrow pv-link">{$dict.pulse.cta} <span class="arrow-flip" aria-hidden="true">&rarr;</span></span>
            </div>
          </div>
        </a>
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

  .cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
  }

  .btn-primary-hero,
  .btn-secondary-hero {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    min-height: 44px;
    padding: 0.65rem 1.25rem;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.94rem;
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

  /* Humanity's Pulse Visual Card */
  .pulse-visual-card {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.68rem 0.85rem;
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-medium);
    border-radius: 14px;
    text-decoration: none;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.16s ease, transform 0.16s ease;
  }

  .pulse-visual-card:hover {
    border-color: var(--accent-primary);
    transform: translateY(-1px);
  }

  .pv-gauge-wrap {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.35rem 0.45rem;
    border-radius: 10px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
  }

  .pv-dial-svg {
    display: block;
  }

  .pv-zone-lbl {
    font-family: var(--font-family-mono);
    font-size: 9px;
    font-weight: 700;
    fill: var(--text-secondary);
  }

  .pv-info {
    flex: 1 1 auto;
    min-width: 0;
  }

  .pv-head-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.35rem;
    margin-bottom: 0.35rem;
  }

  .pv-title-line {
    display: inline-flex;
    align-items: center;
    gap: 0.38rem;
    font-size: 0.85rem;
    color: var(--text-primary);
  }

  .pv-score-pill {
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 800;
    padding: 0.12rem 0.45rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
  }

  .hm-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .hm-dot.state-steady { background: var(--threat-sovereign); }
  .hm-dot.state-stirring,
  .hm-dot.state-rising { background: var(--threat-warning); }

  .pv-pace-bars {
    display: flex;
    flex-direction: column;
    gap: 0.22rem;
    margin-bottom: 0.35rem;
  }

  .pace-row {
    display: grid;
    grid-template-columns: 112px 1fr;
    align-items: center;
    gap: 0.45rem;
  }

  .pace-lbl {
    font-family: var(--font-family-mono);
    font-size: 0.64rem;
    color: var(--text-secondary);
    white-space: nowrap;
  }

  .pace-track {
    height: 6px;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    overflow: hidden;
    display: block;
  }

  .pace-fill-human {
    display: block;
    width: 10%;
    height: 100%;
    border-radius: 9999px;
    background: var(--threat-sovereign);
  }

  .pace-fill-ai {
    display: block;
    height: 100%;
    border-radius: 9999px;
    background: linear-gradient(90deg, var(--threat-warning), var(--threat-critical));
  }

  .pv-foot {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: baseline;
    gap: 0.25rem 0.5rem;
  }

  .pv-explain {
    font-size: 0.74rem;
    color: var(--text-secondary);
    line-height: 1.35;
  }

  .mini-arrow {
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--accent-primary);
    white-space: nowrap;
  }

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  @media (max-width: 920px) {
    .hero-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 480px) {
    .cta-row {
      flex-direction: column;
    }

    .btn-primary-hero,
    .btn-secondary-hero {
      width: 100%;
    }

    .pulse-visual-card {
      flex-direction: column;
      align-items: stretch;
      gap: 0.55rem;
    }

    .pv-gauge-wrap {
      padding: 0.35rem;
    }
  }
</style>
