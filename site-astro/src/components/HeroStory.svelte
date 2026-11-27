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
      <!-- Left: Clear Question, Concise Subtitle, Single Status Strip & Primary Actions -->
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

        <!-- Inline Quick Context Strip (replaces separate Pulse + Meet Toto wall) -->
        <div class="hero-meta-strip">
          <a href={`${base}/toto/`} class="hm-pill">
            <strong>Toto:</strong> {$dict.totoCard.heading.replace('.', '')} &rarr;
          </a>
          <a href={`${base}/seismograph/`} class="hm-pill pulse-badge">
            <span class={`hm-dot state-${pulseKey}`} aria-hidden="true"></span>
            <span>{$dict.pulse.label}: <strong>{$dict.pulse.states[pulseKey].word}</strong> ({pulseScore.toFixed(1)}/10)</span>
          </a>
        </div>
      </div>

      <!-- Right: Clean Visual Horizon Card with Compact City Dropdown -->
      <div class="hero-visual">
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
            viewBox="0 0 640 200"
            width="640"
            height="200"
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

            <rect width="640" height="145" fill="url(#dawn-sky)" />

            <circle cx="430" cy="64" r="68" fill="url(#toto-glow)" class="toto-halo" />
            <g class="toto-orb" transform="translate(430 62)">
              <circle cx="0" cy="0" r="18" fill="none" stroke="#1b6756" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.7" />
              <circle cx="0" cy="0" r="9.5" fill="#ffffff" stroke="#1b6756" stroke-width="1.5" />
              <circle cx="0" cy="0" r="3" fill="#1b6756" />
            </g>

            <g fill="#2b3838" opacity="0.86">
              <rect x="28" y="106" width="38" height="39" rx="2" />
              <rect x="72" y="90" width="32" height="55" rx="2" />
              <rect x="110" y="114" width="44" height="31" rx="2" />

              {#if city.feature === 'cranes'}
                <path d="M180 145 L180 86 L216 74 M194 94 L194 145" stroke="#2b3838" stroke-width="3" fill="none" />
                <rect x="242" y="100" width="34" height="45" rx="2" />
                <path d="M510 145 L516 92 L528 92 L534 145 Z" />
                <circle cx="522" cy="87" r="4" fill="#f59e0b" />
              {:else if city.feature === 'bridge'}
                <path d="M172 145 L182 82 L190 145 M274 145 L284 82 L292 145" stroke="#2b3838" stroke-width="2" />
                <path d="M150 120 Q232 95 316 120" stroke="#2b3838" stroke-width="2.5" fill="none" />
                <rect x="145" y="122" width="175" height="6" />
                <rect x="495" y="102" width="46" height="43" rx="2" />
              {:else if city.feature === 'domes'}
                <path d="M185 145 L185 98 Q208 78 231 98 L231 145 Z" />
                <rect x="242" y="88" width="28" height="57" rx="2" />
                <rect x="496" y="108" width="52" height="37" rx="2" />
              {:else if city.feature === 'spires'}
                <polygon points="196,145 204,52 212,145" />
                <rect x="225" y="92" width="28" height="53" rx="2" />
                <path d="M268 145 Q286 92 296 145 Z" />
                <rect x="506" y="106" width="36" height="39" rx="2" />
              {:else if city.feature === 'tvtower'}
                <rect x="196" y="64" width="6" height="81" />
                <ellipse cx="199" cy="88" rx="14" ry="5" />
                <rect x="224" y="98" width="38" height="47" rx="2" />
                <rect x="498" y="104" width="44" height="41" rx="2" />
              {:else if city.feature === 'island'}
                <polygon points="182,118 206,96 230,118" />
                <rect x="186" y="118" width="40" height="27" />
                <rect x="244" y="94" width="32" height="51" rx="2" />
                <path d="M510 145 Q528 112 548 145 Z" />
              {:else if city.feature === 'hills'}
                <path d="M150 145 Q225 96 300 145 Z" opacity="0.65" />
                <rect x="200" y="96" width="28" height="49" rx="2" />
                <rect x="502" y="105" width="40" height="40" rx="2" />
              {:else}
                <rect x="174" y="84" width="26" height="61" rx="2" />
                <rect x="206" y="70" width="24" height="75" rx="2" />
                <rect x="236" y="96" width="32" height="49" rx="2" />
                <rect x="498" y="106" width="42" height="39" rx="2" />
              {/if}

              <rect x="330" y="122" width="46" height="23" rx="2" />
              <rect x="556" y="116" width="52" height="29" rx="2" />
            </g>

            <rect x="0" y="145" width="640" height="55" fill="url(#sea-grad)" />
            <g fill="#fde68a" opacity="0.45">
              <rect x="398" y="152" width="64" height="3" rx="1.5" />
              <rect x="408" y="162" width="44" height="2.5" rx="1.2" />
              <rect x="418" y="172" width="24" height="2" rx="1" />
            </g>

            <g transform="translate(292 152)" class="boat-drift">
              <path d="M0 10 L36 10 L30 17 L6 17 Z" fill="#f8fafc" />
              <polygon points="16,0 16,9 28,9" fill="#fef3c7" />
            </g>
          </svg>

          <figcaption class="skyline-figcaption">
            <span>{$dict.hero.totoCaption}</span>
          </figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>

<style>
  .hero-story {
    contain: layout style;
    padding: clamp(1.4rem, 3.2vw, 2.75rem) 0 clamp(1.25rem, 2.5vw, 2rem);
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
    grid-template-columns: 1.25fr 0.95fr;
    gap: clamp(1.25rem, 3vw, 2.25rem);
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
    margin-bottom: 0.75rem;
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
    font-size: clamp(1.82rem, 4vw, 2.95rem);
    font-weight: 800;
    line-height: 1.38;
    letter-spacing: -0.01em;
    color: var(--text-primary);
    max-width: 21ch;
    margin: 0 0 0.85rem;
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
    font-size: clamp(0.98rem, 1.55vw, 1.12rem);
    line-height: 1.58;
    color: var(--text-secondary);
    max-width: 540px;
    margin: 0 0 1.25rem;
  }

  .cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    margin-bottom: 1rem;
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

  .hero-meta-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .hm-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.32rem 0.72rem;
    border-radius: 9999px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    font-size: 0.78rem;
    color: var(--text-secondary);
    text-decoration: none;
    min-height: 36px;
  }

  .hm-pill:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
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

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  .skyline-card {
    margin: 0;
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow-md);
  }

  .skyline-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    min-height: 44px;
    padding: 0.5rem 0.85rem;
    background: var(--bg-surface-elevated);
    border-bottom: 1px solid var(--border-subtle);
    font-size: 0.78rem;
    color: var(--text-secondary);
  }

  .region-chip {
    display: inline-block;
    margin-inline-start: 0.3rem;
    padding: 0.08rem 0.42rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    font-family: var(--font-family-mono);
    font-size: 0.65rem;
  }

  .city-select-mini {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    border-radius: 8px;
    padding: 0.25rem 0.5rem;
    font-size: 0.76rem;
    font-weight: 600;
    min-height: 32px;
    cursor: pointer;
  }

  .harbour-svg {
    display: block;
    width: 100%;
    height: auto;
  }

  .skyline-figcaption {
    padding: 0.6rem 0.9rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
    font-style: italic;
    border-top: 1px solid var(--border-subtle);
    background: var(--bg-surface);
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
  }

  @media (max-width: 900px) {
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
  }
</style>
