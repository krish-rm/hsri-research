<script lang="ts">
  import { onMount } from 'svelte';
  import { dict } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';

  export let base = '';
  export let pulseKey: 'steady' | 'stirring' | 'rising' = 'rising';
  export let pulseScore = 8.44;

  interface CitySkin {
    id: string;
    name: string;
    regionHint: string;
    tzPrefixes: string[];
    skyTop: string;
    skyBottom: string;
    waterTint: string;
    feature: 'cranes' | 'spires' | 'bridge' | 'domes' | 'tvtower' | 'island' | 'skyline' | 'hills';
  }

  const CITIES: CitySkin[] = [
    { id: 'neutral', name: 'Coastal Harbour', regionHint: 'Global view', tzPrefixes: [], skyTop: '#fdf5e6', skyBottom: '#f2d9b8', waterTint: '#256b64', feature: 'cranes' },
    { id: 'lagos', name: 'Lagos', regionHint: 'West Africa', tzPrefixes: ['Africa/Lagos'], skyTop: '#fff3df', skyBottom: '#f4ca92', waterTint: '#1f6e68', feature: 'bridge' },
    { id: 'saopaulo', name: 'São Paulo', regionHint: 'South America', tzPrefixes: ['America/Sao_Paulo'], skyTop: '#fef2e4', skyBottom: '#e9c89f', waterTint: '#246669', feature: 'skyline' },
    { id: 'mumbai', name: 'Mumbai', regionHint: 'South Asia', tzPrefixes: ['Asia/Kolkata', 'Asia/Calcutta'], skyTop: '#fff4e1', skyBottom: '#f3c68f', waterTint: '#1b6756', feature: 'domes' },
    { id: 'berlin', name: 'Berlin', regionHint: 'Europe', tzPrefixes: ['Europe/Berlin'], skyTop: '#f4f7f9', skyBottom: '#d8e3e9', waterTint: '#2d6370', feature: 'tvtower' },
    { id: 'jakarta', name: 'Jakarta', regionHint: 'Southeast Asia', tzPrefixes: ['Asia/Jakarta'], skyTop: '#fef6e8', skyBottom: '#f1d2a7', waterTint: '#1d6e6c', feature: 'island' },
    { id: 'dubai', name: 'Dubai', regionHint: 'Middle East', tzPrefixes: ['Asia/Dubai'], skyTop: '#fdf6ea', skyBottom: '#f5cfa0', waterTint: '#1b7375', feature: 'spires' },
    { id: 'toronto', name: 'Toronto', regionHint: 'North America', tzPrefixes: ['America/Toronto'], skyTop: '#f3f7fa', skyBottom: '#d6e3ee', waterTint: '#235e78', feature: 'tvtower' },
    { id: 'nairobi', name: 'Nairobi', regionHint: 'East Africa', tzPrefixes: ['Africa/Nairobi'], skyTop: '#fdf4e4', skyBottom: '#ebd0a2', waterTint: '#226b5c', feature: 'hills' }
  ];

  let activeCityId = 'neutral';

  $: city = CITIES.find((c) => c.id === activeCityId) ?? CITIES[0];
  $: clampedPulse = Math.max(0, Math.min(10, Number.isFinite(pulseScore) ? pulseScore : 8.44));
  $: needleAngleDeg = -90 + (clampedPulse / 10) * 180;

  function selectCity(id: string) {
    activeCityId = id;
    trackEvent('hero_city_switch', { city: id });
  }

  function handleCta(target: 'breakthrough' | 'country') {
    trackEvent('hero_cta_click', { target });
  }

  onMount(() => {
    try {
      const preset = (window as any).__hc || (window as any).__hrHeroCity;
      if (preset && CITIES.some((c) => c.id === preset)) {
        activeCityId = preset;
        return;
      }
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
      const matched = CITIES.find((c) => c.tzPrefixes.some((p) => tz.startsWith(p)));
      if (matched) {
        activeCityId = matched.id;
      }
    } catch {
      // Keep neutral Coastal Harbour fallback
    }
  });
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

      <!-- Right / Visual Flow: 1. Meet Toto Portrait -> 2. Arrival Sky -> 3. Humanity's Pulse Visual -->
      <div class="hero-visual">
        <!-- 1. Meet Toto Character Card -->
        <a href={`${base}/toto/`} class="toto-mini-card">
          <div class="toto-portrait-frame">
            <img
              src={`${base}/assets/toto-character.webp`}
              alt={$dict.totoCard.svgAlt}
              width="72"
              height="72"
              decoding="async"
              class="toto-portrait-img"
            />
          </div>
          <div class="toto-mini-copy">
            <div class="toto-mini-top">
              <span class="mini-tag">{$dict.totoCard.eyebrow}</span>
              <span class="mini-arrow">{$dict.totoCard.ctaSecondary} <span class="arrow-flip" aria-hidden="true">&rarr;</span></span>
            </div>
            <strong class="toto-mini-title">{$dict.totoCard.heading}</strong>
            <p class="toto-mini-desc">{$dict.totoCard.chips.join(' · ')}</p>
          </div>
        </a>

        <!-- 2. Arrival Sky Over Card -->
        <figure class="skyline-card" aria-label={`Dawn harbour scene for ${city.name} showing Toto arriving as a calm light`}>
          <div class="skyline-top-bar">
            <span class="skyline-caption-label">
              {$dict.hero.cityLabel} <strong id="hcn">{activeCityId === 'neutral' ? $dict.hero.cityNeutralName : city.name}</strong>
              <span id="hcr" class="region-chip">{city.regionHint}</span>
            </span>

            <label class="sr-only" for="hero-city-select">Switch city horizon</label>
            <select
              id="hero-city-select"
              class="city-select-mini"
              bind:value={activeCityId}
              onchange={() => selectCity(activeCityId)}
            >
              {#each CITIES as c}
                <option value={c.id}>{c.name}</option>
              {/each}
            </select>
          </div>

          <svg
            class="harbour-svg"
            viewBox="0 0 640 160"
            width="640"
            height="160"
            role="img"
            aria-label={`Calm dawn illustration of ${city.name} harbour as Toto arrives softly above the horizon`}
          >
            <defs>
              <linearGradient id="dawn-sky" x1="0" y1="0" x2="0" y2="1">
                <stop id="hst" offset="0%" stop-color={city.skyTop} />
                <stop id="hsb" offset="100%" stop-color={city.skyBottom} />
              </linearGradient>
              <radialGradient id="toto-glow" cx="50%" cy="42%" r="38%">
                <stop offset="0%" stop-color="#fff8dc" stop-opacity="0.98" />
                <stop offset="42%" stop-color="#7ce0c6" stop-opacity="0.52" />
                <stop offset="100%" stop-color="#1b6756" stop-opacity="0" />
              </radialGradient>
              <linearGradient id="sea-grad" x1="0" y1="0" x2="0" y2="1">
                <stop id="hsa" offset="0%" stop-color={city.waterTint} stop-opacity="0.82" />
                <stop offset="100%" stop-color="#113c37" stop-opacity="0.95" />
              </linearGradient>
            </defs>

            <rect width="640" height="118" fill="url(#dawn-sky)" />

            <circle cx="430" cy="52" r="56" fill="url(#toto-glow)" class="toto-halo" />
            <g class="toto-orb" transform="translate(430 50)">
              <circle cx="0" cy="0" r="16" fill="none" stroke="#1b6756" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.7" />
              <circle cx="0" cy="0" r="8.5" fill="#ffffff" stroke="#1b6756" stroke-width="1.5" />
              <circle cx="0" cy="0" r="2.8" fill="#1b6756" />
            </g>

            <g fill="#2b3838" opacity="0.86">
              <rect x="28" y="82" width="38" height="36" rx="2" />
              <rect x="72" y="66" width="32" height="52" rx="2" />
              <rect x="110" y="90" width="44" height="28" rx="2" />

              {#if city.feature === 'cranes'}
                <path d="M180 118 L180 62 L216 50 M194 70 L194 118" stroke="#2b3838" stroke-width="3" fill="none" />
                <rect x="242" y="76" width="34" height="42" rx="2" />
                <path d="M510 118 L516 68 L528 68 L534 118 Z" />
                <circle cx="522" cy="63" r="4" fill="#f59e0b" />
              {:else if city.feature === 'bridge'}
                <path d="M172 118 L182 58 L190 118 M274 118 L284 58 L292 118" stroke="#2b3838" stroke-width="2" />
                <path d="M150 96 Q232 72 316 96" stroke="#2b3838" stroke-width="2.5" fill="none" />
                <rect x="145" y="98" width="175" height="6" />
                <rect x="495" y="78" width="46" height="40" rx="2" />
              {:else if city.feature === 'domes'}
                <path d="M185 118 L185 74 Q208 54 231 74 L231 118 Z" />
                <rect x="242" y="64" width="28" height="54" rx="2" />
                <rect x="496" y="84" width="52" height="34" rx="2" />
              {:else if city.feature === 'spires'}
                <polygon points="196,118 204,32 212,118" />
                <rect x="225" y="68" width="28" height="50" rx="2" />
                <path d="M268 118 Q286 68 296 118 Z" />
                <rect x="506" y="82" width="36" height="36" rx="2" />
              {:else if city.feature === 'tvtower'}
                <rect x="196" y="42" width="6" height="76" />
                <ellipse cx="199" cy="64" rx="14" ry="5" />
                <rect x="224" y="74" width="38" height="44" rx="2" />
                <rect x="498" y="80" width="44" height="38" rx="2" />
              {:else if city.feature === 'island'}
                <polygon points="182,94 206,72 230,94" />
                <rect x="186" y="94" width="40" height="24" />
                <rect x="244" y="70" width="32" height="48" rx="2" />
                <path d="M510 118 Q528 86 548 118 Z" />
              {:else if city.feature === 'hills'}
                <path d="M150 118 Q225 70 300 118 Z" opacity="0.65" />
                <rect x="200" y="72" width="28" height="46" rx="2" />
                <rect x="502" y="81" width="40" height="37" rx="2" />
              {:else}
                <rect x="174" y="60" width="26" height="58" rx="2" />
                <rect x="206" y="48" width="24" height="70" rx="2" />
                <rect x="236" y="72" width="32" height="46" rx="2" />
                <rect x="498" y="82" width="42" height="36" rx="2" />
              {/if}

              <rect x="330" y="96" width="46" height="22" rx="2" />
              <rect x="556" y="92" width="52" height="26" rx="2" />
            </g>

            <rect x="0" y="118" width="640" height="42" fill="url(#sea-grad)" />
            <g fill="#fde68a" opacity="0.45">
              <rect x="398" y="124" width="64" height="3" rx="1.5" />
              <rect x="408" y="133" width="44" height="2.5" rx="1.2" />
              <rect x="418" y="142" width="24" height="2" rx="1" />
            </g>

            <g transform="translate(292 124)" class="boat-drift">
              <path d="M0 9 L36 9 L30 15 L6 15 Z" fill="#f8fafc" />
              <polygon points="16,0 16,8 28,8" fill="#fef3c7" />
            </g>
          </svg>

          <figcaption class="skyline-figcaption">
            <span>{$dict.hero.totoCaption}</span>
          </figcaption>
        </figure>

        <!-- 3. Humanity's Pulse Visual Card (Speedometer + Pace Gap Visual) -->
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

            <!-- Simple visual pace comparison bar -->
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
    grid-template-columns: 1.08fr 1fr;
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

  /* 1. Meet Toto Character Mini Card */
  .toto-mini-card {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.65rem 0.85rem;
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-medium);
    border-radius: 14px;
    text-decoration: none;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.16s ease, transform 0.16s ease;
  }

  .toto-mini-card:hover {
    border-color: var(--accent-primary);
    transform: translateY(-1px);
  }

  .toto-portrait-frame {
    flex-shrink: 0;
    width: 68px;
    height: 68px;
    border-radius: 12px;
    overflow: hidden;
    background: #fbf7ee;
    border: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .toto-portrait-img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .toto-mini-copy {
    flex: 1 1 auto;
    min-width: 0;
  }

  .toto-mini-top {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.35rem;
    margin-bottom: 0.15rem;
  }

  .mini-tag {
    font-family: var(--font-family-mono);
    font-size: 0.64rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--accent-primary);
  }

  .mini-arrow {
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--accent-primary);
    white-space: nowrap;
  }

  .toto-mini-title {
    display: block;
    font-size: 0.96rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.25;
  }

  .toto-mini-desc {
    margin: 0.15rem 0 0;
    font-size: 0.78rem;
    color: var(--text-secondary);
    line-height: 1.38;
  }

  /* 2. Arrival Sky Over Card */
  .skyline-card {
    margin: 0;
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
  }

  .skyline-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    min-height: 40px;
    padding: 0.4rem 0.8rem;
    background: var(--bg-surface-elevated);
    border-bottom: 1px solid var(--border-subtle);
    font-size: 0.76rem;
    color: var(--text-secondary);
  }

  .region-chip {
    display: inline-block;
    margin-inline-start: 0.3rem;
    padding: 0.06rem 0.4rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    font-family: var(--font-family-mono);
    font-size: 0.64rem;
  }

  .city-select-mini {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    border-radius: 8px;
    padding: 0.22rem 0.45rem;
    font-size: 0.75rem;
    font-weight: 600;
    min-height: 30px;
    cursor: pointer;
  }

  .harbour-svg {
    display: block;
    width: 100%;
    height: auto;
  }

  .skyline-figcaption {
    padding: 0.48rem 0.8rem;
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-style: italic;
    border-top: 1px solid var(--border-subtle);
    background: var(--bg-surface);
  }

  /* 3. Humanity's Pulse Visual Card */
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

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
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
