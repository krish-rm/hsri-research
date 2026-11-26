<script lang="ts">
  import { onMount } from 'svelte';
  import { dict } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';

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
  let autoDetectedNote = '';

  $: city = CITIES.find((c) => c.id === activeCityId) ?? CITIES[0];

  function selectCity(id: string) {
    activeCityId = id;
    autoDetectedNote = '';
    trackEvent('hero_city_switch', { city: id });
  }

  function handleCta(target: 'wish' | 'country') {
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
      <!-- Left: Headline, Subhead, CTAs, City Switcher -->
      <div class="hero-copy">
        <div class="eyebrow-pill">
          <span class="pulse-dot" aria-hidden="true"></span>
          <span>{$dict.hero.eyebrow}</span>
        </div>

        <h1 class="hero-title">{$dict.hero.headline}</h1>

        <p class="hero-subhead">{$dict.hero.subhead}</p>

        <div class="cta-row">
          <a href="#wish-doors" class="btn-primary-hero" onclick={() => handleCta('wish')}>
            {$dict.hero.ctaPrimary}
            <span class="arrow-flip" aria-hidden="true">&rarr;</span>
          </a>
          <a href="#country-check" class="btn-secondary-hero" onclick={() => handleCta('country')}>
            {$dict.hero.ctaSecondary}
          </a>
        </div>

        <!-- Original Calm Coastal Harbour SVG -->
        <figure class="skyline-card" aria-label={`Dawn harbour scene for ${city.name} showing Kalpa arriving as a calm light`}>
          <div class="skyline-top-bar">
            <span class="skyline-caption-label">
              {$dict.hero.cityLabel} <strong id="hcn">{activeCityId === 'neutral' ? $dict.hero.cityNeutralName : city.name}</strong>
              <span id="hcr" class="region-chip">{city.regionHint}</span>
            </span>
          </div>

          <svg
            class="harbour-svg"
            viewBox="0 0 640 200"
            width="640"
            height="200"
            role="img"
            aria-label={`Calm dawn illustration of ${city.name} harbour as Kalpa arrives softly above the horizon`}
          >
            <defs>
              <linearGradient id="dawn-sky" x1="0" y1="0" x2="0" y2="1">
                <stop id="hst" offset="0%" stop-color={city.skyTop} />
                <stop id="hsb" offset="100%" stop-color={city.skyBottom} />
              </linearGradient>
              <radialGradient id="kalpa-glow" cx="50%" cy="42%" r="38%">
                <stop offset="0%" stop-color="#fff8dc" stop-opacity="0.98" />
                <stop offset="42%" stop-color="#7ce0c6" stop-opacity="0.52" />
                <stop offset="100%" stop-color="#1b6756" stop-opacity="0" />
              </radialGradient>
              <linearGradient id="sea-grad" x1="0" y1="0" x2="0" y2="1">
                <stop id="hsa" offset="0%" stop-color={city.waterTint} stop-opacity="0.82" />
                <stop offset="100%" stop-color="#113c37" stop-opacity="0.95" />
              </linearGradient>
            </defs>

            <!-- Dawn Sky -->
            <rect width="640" height="145" fill="url(#dawn-sky)" />

            <!-- Kalpa arrival prism & soft halo over harbour -->
            <circle cx="430" cy="64" r="68" fill="url(#kalpa-glow)" class="kalpa-halo" />
            <g class="kalpa-prism" transform="translate(430 62)">
              <polygon points="0,-16 11,0 0,16 -11,0" fill="#ffffff" stroke="#1b6756" stroke-width="1.5" />
              <circle cx="0" cy="0" r="3.5" fill="#1b6756" />
            </g>

            <!-- City-varied silhouette (calm coastal blocks + landmark detail) -->
            <g fill="#2b3838" opacity="0.86">
              <rect x="28" y="106" width="38" height="39" rx="2" />
              <rect x="72" y="90" width="32" height="55" rx="2" />
              <rect x="110" y="114" width="44" height="31" rx="2" />

              {#if city.feature === 'cranes'}
                <!-- Coastal Harbour cranes & lighthouse -->
                <path d="M180 145 L180 86 L216 74 M194 94 L194 145" stroke="#2b3838" stroke-width="3" fill="none" />
                <rect x="242" y="100" width="34" height="45" rx="2" />
                <path d="M510 145 L516 92 L528 92 L534 145 Z" />
                <circle cx="522" cy="87" r="4" fill="#f59e0b" />
              {:else if city.feature === 'bridge'}
                <!-- Harbour suspension bridge -->
                <path d="M172 145 L182 82 L190 145 M274 145 L284 82 L292 145" stroke="#2b3838" stroke-width="2" />
                <path d="M150 120 Q232 95 316 120" stroke="#2b3838" stroke-width="2.5" fill="none" />
                <rect x="145" y="122" width="175" height="6" />
                <rect x="495" y="102" width="46" height="43" rx="2" />
              {:else if city.feature === 'domes'}
                <!-- Archway & coastal domes -->
                <path d="M185 145 L185 98 Q208 78 231 98 L231 145 Z" />
                <rect x="242" y="88" width="28" height="57" rx="2" />
                <rect x="496" y="108" width="52" height="37" rx="2" />
              {:else if city.feature === 'spires'}
                <!-- Modern harbour spires -->
                <polygon points="196,145 204,52 212,145" />
                <rect x="225" y="92" width="28" height="53" rx="2" />
                <path d="M268 145 Q286 92 296 145 Z" />
                <rect x="506" y="106" width="36" height="39" rx="2" />
              {:else if city.feature === 'tvtower'}
                <!-- Observation spire & riverside halls -->
                <rect x="196" y="64" width="6" height="81" />
                <ellipse cx="199" cy="88" rx="14" ry="5" />
                <rect x="224" y="98" width="38" height="47" rx="2" />
                <rect x="498" y="104" width="44" height="41" rx="2" />
              {:else if city.feature === 'island'}
                <!-- Archipelago vessels & tropical roofs -->
                <polygon points="182,118 206,96 230,118" />
                <rect x="186" y="118" width="40" height="27" />
                <rect x="244" y="94" width="32" height="51" rx="2" />
                <path d="M510 145 Q528 112 548 145 Z" />
              {:else if city.feature === 'hills'}
                <!-- Distant green hills & sunlit rooftops -->
                <path d="M150 145 Q225 96 300 145 Z" opacity="0.65" />
                <rect x="200" y="96" width="28" height="49" rx="2" />
                <rect x="502" y="105" width="40" height="40" rx="2" />
              {:else}
                <!-- Varied city blocks -->
                <rect x="174" y="84" width="26" height="61" rx="2" />
                <rect x="206" y="70" width="24" height="75" rx="2" />
                <rect x="236" y="96" width="32" height="49" rx="2" />
                <rect x="498" y="106" width="42" height="39" rx="2" />
              {/if}

              <!-- Low waterfront warehouses right -->
              <rect x="330" y="122" width="46" height="23" rx="2" />
              <rect x="556" y="116" width="52" height="29" rx="2" />
            </g>

            <!-- Sea & soft light path -->
            <rect x="0" y="145" width="640" height="55" fill="url(#sea-grad)" />
            <g fill="#fde68a" opacity="0.45">
              <rect x="398" y="152" width="64" height="3" rx="1.5" />
              <rect x="408" y="162" width="44" height="2.5" rx="1.2" />
              <rect x="418" y="172" width="24" height="2" rx="1" />
            </g>

            <!-- Small calm harbour boat -->
            <g transform="translate(292 152)" class="boat-drift">
              <path d="M0 10 L36 10 L30 17 L6 17 Z" fill="#f8fafc" />
              <polygon points="16,0 16,9 28,9" fill="#fef3c7" />
            </g>
          </svg>

          <figcaption class="skyline-figcaption">
            <span>{$dict.hero.kalpaCaption}</span>
          </figcaption>

          <div class="city-pills" role="group" aria-label="Choose example coastal city skyline">
            {#each CITIES as c}
              <button
                type="button"
                class="city-pill"
                class:active={activeCityId === c.id}
                data-city={c.id}
                data-c={`${c.regionHint}|${c.skyTop}|${c.skyBottom}|${c.waterTint}`}
                onclick={() => selectCity(c.id)}
              >
                {c.name}
              </button>
            {/each}
          </div>
        </figure>
      </div>

      <!-- Right / Below on mobile: Crowd Readiness Ring (Honest empty state) -->
      <div class="ring-panel">
        <div class="ring-card">
          <div class="ring-svg-wrap">
            <svg viewBox="0 0 160 160" width="160" height="160" class="ring-svg" role="img" aria-label="Crowd readiness gauge awaiting the first 200 wishers">
              <circle cx="80" cy="80" r="64" fill="none" stroke="var(--border-medium)" stroke-width="10" stroke-dasharray="6 6" />
              <circle cx="80" cy="80" r="50" fill="none" stroke="var(--accent-primary)" stroke-width="2" opacity="0.25" class="ring-breath" />
              <text x="80" y="76" text-anchor="middle" class="ring-num">0 / 200</text>
              <text x="80" y="95" text-anchor="middle" class="ring-unit">WISHERS</text>
            </svg>
          </div>
          <p class="ring-title">{$dict.hero.ringTitle}</p>
          <p class="ring-empty-headline">{$dict.hero.ringEmptyHeadline}</p>
          <p class="ring-empty-sub">{$dict.hero.ringEmptySub}</p>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .hero-story {
    contain: layout style;
    padding: clamp(2rem, 4vw, 3.75rem) 0 clamp(1.75rem, 3vw, 2.75rem);
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
    grid-template-columns: 1.55fr 0.85fr;
    gap: clamp(1.5rem, 3vw, 2.5rem);
    align-items: start;
  }

  .eyebrow-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.32rem 0.85rem;
    border-radius: 9999px;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    margin-bottom: 1rem;
  }

  :global([dir='rtl']) .eyebrow-pill {
    letter-spacing: 0;
  }

  .pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent-primary);
  }

  .hero-title {
    font-family: var(--font-family-sans);
    font-size: clamp(1.85rem, 4vw, 2.85rem);
    font-weight: 800;
    line-height: 1.18;
    letter-spacing: -0.025em;
    color: var(--text-primary);
    margin: 0 0 1rem;
  }

  .hero-subhead {
    font-size: clamp(1rem, 1.8vw, 1.18rem);
    line-height: 1.65;
    color: var(--text-secondary);
    max-width: 660px;
    margin: 0 0 1.4rem;
  }

  .cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.75rem;
  }

  .btn-primary-hero,
  .btn-secondary-hero {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    min-height: 46px;
    padding: 0.7rem 1.35rem;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.96rem;
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

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

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
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.35rem 0.5rem;
    min-height: 44px;
    padding: 0.55rem 0.9rem;
    background: var(--bg-surface-elevated);
    border-bottom: 1px solid var(--border-subtle);
    font-size: 0.8rem;
    color: var(--text-secondary);
  }

  .region-chip {
    display: inline-block;
    margin-inline-start: 0.35rem;
    padding: 0.1rem 0.45rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
  }

  .tz-note {
    font-size: 0.72rem;
    color: var(--accent-primary);
    font-weight: 600;
  }

  .harbour-svg {
    display: block;
    width: 100%;
    height: auto;
  }

  .kalpa-halo {
    opacity: 0.92;
  }

  .boat-drift {
    transform: translate(292px, 152px);
  }

  .skyline-figcaption {
    padding: 0.55rem 0.9rem;
    font-size: 0.84rem;
    color: var(--text-secondary);
    font-style: italic;
    border-top: 1px solid var(--border-subtle);
    background: var(--bg-surface);
  }

  .city-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    padding: 0.65rem 0.9rem;
    border-top: 1px solid var(--border-subtle);
    background: var(--bg-surface-sunken);
  }

  .city-pill {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    border-radius: 9999px;
    padding: 0.3rem 0.7rem;
    font-size: 0.76rem;
    font-weight: 600;
    cursor: pointer;
    min-height: 32px;
    transition: all 0.15s ease;
  }

  .city-pill:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .city-pill.active {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .ring-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    padding: 1.5rem 1.25rem;
    text-align: center;
    box-shadow: var(--shadow-md);
  }

  .ring-svg-wrap {
    width: 148px;
    margin: 0 auto 0.85rem;
  }

  .ring-svg {
    width: 100%;
    height: auto;
  }

  .ring-num {
    font-family: var(--font-family-mono);
    font-size: 16px;
    font-weight: 700;
    fill: var(--text-primary);
    direction: ltr;
    unicode-bidi: isolate;
  }

  .ring-unit {
    font-family: var(--font-family-mono);
    font-size: 10px;
    letter-spacing: 0.12em;
    fill: var(--text-secondary);
  }

  .ring-breath {
    stroke-opacity: 0.35;
  }

  .ring-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin: 0 0 0.45rem;
  }

  .ring-empty-headline {
    font-family: var(--font-family-sans);
    font-size: 1.12rem;
    font-weight: 800;
    color: var(--accent-primary);
    margin: 0 0 0.35rem;
  }

  .ring-empty-sub {
    font-size: 0.82rem;
    line-height: 1.5;
    color: var(--text-secondary);
    margin: 0;
  }

  @media (max-width: 900px) {
    .hero-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 480px) {
    .skyline-top-bar {
      min-height: 62px;
      align-items: center;
    }
    .cta-row {
      flex-direction: column;
    }
    .btn-primary-hero,
    .btn-secondary-hero {
      width: 100%;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .pulse-dot,
    .kalpa-halo,
    .boat-drift,
    .ring-breath {
      animation: none !important;
    }
  }
</style>
