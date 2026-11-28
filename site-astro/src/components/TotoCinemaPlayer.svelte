<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import { dict } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';
  import {
    COUNTRY_SKIES,
    REGION_GROUP_ORDER,
    SHOWCASE_CYCLE_IDS,
    findCityById,
    matchCityByTimezone,
    type CountrySky,
    type RegionGroup
  } from '../lib/countrySkies';
  import CountrySkylineSvg from './CountrySkylineSvg.svelte';

  export let base = '';
  export let compact = false;

  const DURATION_SEC = 16;

  let activeCityId = 'neutral';
  let playing = true;
  let elapsedSec = 0;
  let seekOffsetSec = 0;
  let cycleKey = 0;
  let clockTimer: ReturnType<typeof setInterval> | null = null;
  let lastTickMs = 0;

  $: city = findCityById(activeCityId);
  $: cityImgSrc = `${base}${city.imagePath}`;
  $: activeSceneIdx = Math.min(3, Math.floor((elapsedSec % DURATION_SEC) / 4));
  $: progressPct = Math.min(100, Math.max(0, ((elapsedSec % DURATION_SEC) / DURATION_SEC) * 100));

  function formatSec(sec: number): string {
    const whole = Math.max(0, Math.floor(sec % DURATION_SEC));
    return `0:${whole < 10 ? '0' : ''}${whole}`;
  }

  function startClock() {
    if (clockTimer) clearInterval(clockTimer);
    lastTickMs = Date.now();
    clockTimer = setInterval(() => {
      if (!playing) {
        lastTickMs = Date.now();
        return;
      }
      const now = Date.now();
      const dt = (now - lastTickMs) / 1000;
      lastTickMs = now;
      elapsedSec = (elapsedSec + dt) % DURATION_SEC;
    }, 100);
  }

  function togglePlay() {
    playing = !playing;
    lastTickMs = Date.now();
  }

  function restartFrom(sec = 0) {
    seekOffsetSec = Math.max(0, Math.min(DURATION_SEC - 0.1, sec));
    elapsedSec = seekOffsetSec;
    playing = true;
    cycleKey += 1;
    lastTickMs = Date.now();
  }

  function handleCitySelect(id: string) {
    activeCityId = id;
    restartFrom(0);
    trackEvent('hero_city_switch', { city: id });
  }

  const countriesByGroup = REGION_GROUP_ORDER.reduce(
    (acc, group) => {
      acc[group] = COUNTRY_SKIES.filter((c) => c.regionGroup === group);
      return acc;
    },
    {} as Record<Exclude<RegionGroup, 'Featured Skies'>, CountrySky[]>
  );

  function cycleNextCity() {
    const sIdx = SHOWCASE_CYCLE_IDS.indexOf(activeCityId);
    if (sIdx >= 0) {
      const nextId = SHOWCASE_CYCLE_IDS[(sIdx + 1) % SHOWCASE_CYCLE_IDS.length];
      handleCitySelect(nextId);
      return;
    }
    const idx = COUNTRY_SKIES.findIndex((c) => c.id === activeCityId);
    const next = COUNTRY_SKIES[(idx + 1) % COUNTRY_SKIES.length];
    if (next) handleCitySelect(next.id);
  }

  function handleScrubClick(ev: MouseEvent) {
    const bar = ev.currentTarget as HTMLElement;
    const rect = bar.getBoundingClientRect();
    if (!rect.width) return;
    const ratio = Math.max(0, Math.min(1, (ev.clientX - rect.left) / rect.width));
    restartFrom(ratio * DURATION_SEC);
  }

  onMount(() => {
    try {
      const preset = (window as any).__hc || (window as any).__hrHeroCity;
      if (preset && COUNTRY_SKIES.some((c) => c.id === preset || c.iso.toLowerCase() === String(preset).toLowerCase())) {
        activeCityId = findCityById(preset).id;
      } else {
        const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
        const matched = matchCityByTimezone(tz);
        if (matched) activeCityId = matched.id;
      }
    } catch {
      // Keep Coastal Harbour default
    }
    startClock();
  });

  onDestroy(() => {
    if (clockTimer) clearInterval(clockTimer);
  });
</script>

<div class="toto-cinema-card" class:compact class:paused={!playing}>
  <!-- Top Cinema Header & Interactive City Chooser -->
  <div class="tc-top-bar">
    <span class="tc-city-label" title={city.horizonMotif}>
      <span class="live-dot" aria-hidden="true"></span>
      {$dict.hero.cityLabel}
      <strong id="hcn">{activeCityId === 'neutral' ? $dict.hero.cityNeutralName : city.name}</strong>
      <span id="hcr" class="region-chip">{city.regionHint}</span>
    </span>

    <div class="tc-controls-top">
      <label class="sr-only" for="hero-city-select">Switch country or city backdrop</label>
      <select
        id="hero-city-select"
        class="city-select-mini"
        bind:value={activeCityId}
        onchange={() => handleCitySelect(activeCityId)}
      >
        <option value="neutral">Coastal Harbour (Global)</option>
        {#each REGION_GROUP_ORDER as groupName}
          <optgroup label={`${groupName} (${countriesByGroup[groupName].length})`}>
            {#each countriesByGroup[groupName] as c}
              <option value={c.id}>{c.name}</option>
            {/each}
          </optgroup>
        {/each}
      </select>
      <button
        type="button"
        class="btn-next-city"
        onclick={cycleNextCity}
        title="Fly Toto over next country"
      >
        &#8635; Next city
      </button>
    </div>
  </div>

  <!-- 16:9 Animated Cityscape & Flying Toto Cinema Frame -->
  <div class="cinema-viewport" style={`--seek-delay: -${seekOffsetSec}s;`}>
    <!-- Real Watercolor Sky / City Backdrop with Smooth Ken Burns Motion -->
    <img
      id="hero-city-bg"
      src={cityImgSrc}
      alt={`Dawn sky over ${city.name} (${city.horizonMotif}) with Toto flying smoothly across the open morning sky`}
      width="760"
      height="428"
      decoding="async"
      class="cinema-bg-img"
    />

    {#if !city.painted}
      <CountrySkylineSvg archetype={city.archetype} />
    {/if}

    {#key cycleKey}

      <!-- Atmospheric Clouds, Flight Arc Ribbon & Shimmering Horizon Rays -->
      <svg class="cinema-fx-svg" viewBox="0 0 760 428" aria-hidden="true">
        <defs>
          <radialGradient id="tc-dawn-sun" cx="50%" cy="62%" r="48%">
            <stop offset="0%" stop-color="#fffbeb" stop-opacity="0.65" />
            <stop offset="55%" stop-color="#fde68a" stop-opacity="0.18" />
            <stop offset="100%" stop-color="#fde68a" stop-opacity="0" />
          </radialGradient>
          <linearGradient id="tc-trail-grad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#1b6756" stop-opacity="0" />
            <stop offset="45%" stop-color="#5eead4" stop-opacity="0.6" />
            <stop offset="100%" stop-color="#fbbf24" stop-opacity="0.85" />
          </linearGradient>
        </defs>

        <!-- Dawn shimmer bloom -->
        <ellipse cx="420" cy="215" rx="220" ry="120" fill="url(#tc-dawn-sun)" class="fx-sun-bloom" />

        <!-- Drifting translucent clouds -->
        <g class="fx-cloud-slow" opacity="0.52" fill="#fffdf7">
          <path d="M90 88 q24 -18 52 -6 q22 -14 48 0 q16 2 18 14 h-124 q-8 -6 6 -8 z" />
          <path d="M510 74 q20 -14 44 -4 q18 -12 40 2 q12 2 12 10 h-102 q-6 -6 6 -8 z" />
        </g>

        <!-- Glowing curved flight arc across the sky -->
        <path
          d="M 40 120 Q 270 30 530 96 T 710 72"
          fill="none"
          stroke="url(#tc-trail-grad)"
          stroke-width="2.6"
          stroke-dasharray="7 7"
          stroke-linecap="round"
          class="fx-flight-arc"
        />

        <!-- Gentle water sparkles -->
        <g class="fx-water-spark" fill="#fffbeb">
          <circle cx="290" cy="348" r="2.2" />
          <circle cx="385" cy="364" r="1.8" />
          <circle cx="490" cy="352" r="2.4" />
        </g>
      </svg>

      <!-- Real Toto Transparent Character Sprite Flying Across Sky -->
      <div class="toto-flyer-track" aria-hidden="true">
        <div class="toto-flyer">
          <span class="flyer-aura"></span>
          <img
            src={`${base}/assets/toto-flying.webp`}
            alt=""
            width="180"
            height="204"
            decoding="async"
            class="toto-flyer-sprite"
          />
          <svg class="flyer-star" viewBox="0 0 16 16" width="16" height="16">
            <path d="M8 1 L9.6 6.4 L15 8 L9.6 9.6 L8 15 L6.4 9.6 L1 8 L6.4 6.4 Z" fill="#f59e0b" />
          </svg>
        </div>
      </div>

      <!-- Synchronized Multi-Scene Captions (CSS Pure Loop + Live JS Sync) -->
      <div class="cinema-captions" aria-live="polite">
        <div class="caption-pill" class:sync-hidden={cycleKey > 0}>
          <span class="scene-chip">{activeSceneIdx + 1}/4</span>
          <span class="caption-text css-cap cap-1">&ldquo;{$dict.totoIntro.lines[0]}&rdquo;</span>
          <span class="caption-text css-cap cap-2">{$dict.totoIntro.lines[1]}</span>
          <span class="caption-text css-cap cap-3">{$dict.totoIntro.lines[2]}</span>
          <span class="caption-text css-cap cap-4">{city.name}: {$dict.totoBeats.close}</span>
        </div>
        {#if cycleKey > 0}
          <div class="caption-pill js-synced-cap">
            <span class="scene-chip">{activeSceneIdx + 1}/4</span>
            <span class="caption-text">
              {#if activeSceneIdx === 0}
                &ldquo;{$dict.totoIntro.lines[0]}&rdquo;
              {:else if activeSceneIdx === 1}
                {$dict.totoIntro.lines[1]}
              {:else if activeSceneIdx === 2}
                {$dict.totoIntro.lines[2]}
              {:else}
                {city.name}: {$dict.totoBeats.close}
              {/if}
            </span>
          </div>
        {/if}
      </div>
    {/key}

    <!-- Interactive Video Scrubber Bar along Bottom Edge -->
    <button
      type="button"
      class="cinema-scrub-bar"
      onclick={handleScrubClick}
      aria-label="Seek Toto arrival animation timeline"
    >
      <span class="scrub-track">
        {#key `${activeCityId}-${cycleKey}`}
          <span
            class="scrub-fill"
            class:has-js-sync={cycleKey > 0}
            style={cycleKey > 0 ? `width: ${progressPct.toFixed(1)}%` : undefined}
          ></span>
        {/key}
      </span>
    </button>
  </div>

  <!-- Video Playback Control Bar + Story Link -->
  <div class="tc-footer-bar">
    <div class="tc-play-controls">
      <button type="button" class="btn-video-ctrl" onclick={togglePlay} aria-label={playing ? 'Pause intro animation' : 'Play intro animation'}>
        {playing ? '⏸ Pause' : '▶ Play'}
      </button>
      <button type="button" class="btn-video-ctrl" onclick={() => restartFrom(0)} aria-label="Replay intro animation">
        ↺ Replay
      </button>
      <span class="tc-time-code">{formatSec(elapsedSec)} / 0:{DURATION_SEC}</span>
    </div>

    <div class="tc-scene-dots" role="group" aria-label="Jump to animation moment">
      {#each [0, 4, 8, 12] as sec, idx}
        <button
          type="button"
          class="scene-dot"
          class:active={activeSceneIdx === idx}
          onclick={() => restartFrom(sec)}
          aria-label={`Jump to scene ${idx + 1}`}
        >
          {idx + 1}
        </button>
      {/each}
    </div>

    {#if compact}
      <a href={`${base}/toto/`} class="tc-story-link">
        {$dict.totoCard.ctaSecondary} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
      </a>
    {/if}
  </div>
</div>

<style>
  .toto-cinema-card {
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-medium);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow-md);
  }

  .tc-top-bar {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.45rem;
    padding: 0.48rem 0.85rem;
    background: var(--bg-surface-elevated);
    border-bottom: 1px solid var(--border-subtle);
    font-size: 0.76rem;
    color: var(--text-secondary);
  }

  .tc-city-label {
    display: inline-flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.35rem;
  }

  .live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--accent-primary);
    animation: pulseGlow 2.4s ease-in-out infinite;
    flex-shrink: 0;
  }

  .region-chip {
    padding: 0.06rem 0.42rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    font-family: var(--font-family-mono);
    font-size: 0.62rem;
    color: var(--text-secondary);
  }

  .tc-controls-top {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
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
    max-width: min(195px, 54vw);
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    cursor: pointer;
  }

  .btn-next-city {
    border: 1px solid var(--accent-primary);
    background: var(--threat-sovereign-bg);
    color: var(--accent-primary);
    border-radius: 8px;
    padding: 0.22rem 0.58rem;
    font-size: 0.72rem;
    font-weight: 700;
    min-height: 30px;
    cursor: pointer;
    white-space: nowrap;
  }

  .btn-next-city:hover {
    background: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  /* 16:9 Cinema Stage */
  .cinema-viewport {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    container-type: size;
    overflow: hidden;
    background: #fbf7ee;
  }

  .cinema-bg-img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transform-origin: center center;
    animation: kenBurns16s 16s ease-in-out infinite;
    animation-delay: var(--seek-delay, 0s);
  }

  .cinema-fx-svg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }

  .fx-sun-bloom {
    animation: pulseGlow 5s ease-in-out infinite;
    transform-origin: 420px 215px;
  }

  .fx-cloud-slow {
    animation: cloudGlide 16s linear infinite;
    animation-delay: var(--seek-delay, 0s);
  }

  .fx-flight-arc {
    animation: arcGlow 16s linear infinite;
    animation-delay: var(--seek-delay, 0s);
  }

  .fx-water-spark {
    animation: sparkleWater 3.2s ease-in-out infinite;
  }

  /* Toto Transparent Sprite Flying Trajectory */
  .toto-flyer-track {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .toto-flyer {
    position: absolute;
    left: 0;
    top: 0;
    width: 15cqw;
    max-width: 118px;
    min-width: 52px;
    animation: totoFlyLoop 16s cubic-bezier(0.42, 0, 0.58, 1) infinite;
    animation-delay: var(--seek-delay, 0s);
    will-change: transform, opacity;
  }

  .toto-flyer-sprite {
    position: relative;
    display: block;
    width: 100%;
    height: auto;
    animation: totoWingBob 2.2s ease-in-out infinite;
    filter: drop-shadow(0 6px 12px rgba(27, 103, 86, 0.25));
  }

  .flyer-aura {
    position: absolute;
    inset: 10%;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 251, 235, 0.65), rgba(124, 224, 198, 0.28) 55%, transparent 75%);
    animation: pulseGlow 2.6s ease-in-out infinite;
  }

  .flyer-star {
    position: absolute;
    top: 2px;
    inset-inline-end: 0;
    animation: starTwinkle 2.1s ease-in-out infinite;
  }

  /* Captions */
  .cinema-captions {
    position: absolute;
    left: 0.7rem;
    right: 0.7rem;
    bottom: 0.75rem;
    display: flex;
    justify-content: center;
    pointer-events: none;
  }

  .caption-pill {
    position: relative;
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    align-items: center;
    gap: 0.45rem;
    max-width: min(96%, 500px);
    padding: 0.36rem 0.78rem;
    border-radius: 14px;
    background: rgba(18, 22, 20, 0.8);
    backdrop-filter: blur(6px);
    color: #fffdf7;
    font-size: clamp(0.7rem, 1.5cqw, 0.82rem);
    font-weight: 600;
    line-height: 1.32;
    text-align: start;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.24);
  }

  .caption-pill.sync-hidden {
    display: none;
  }

  .scene-chip {
    grid-column: 1;
    grid-row: 1;
    font-family: var(--font-family-mono);
    font-size: 0.66rem;
    font-weight: 800;
    padding: 0.1rem 0.4rem;
    border-radius: 9999px;
    background: var(--accent-primary);
    color: #ffffff;
  }

  .caption-text {
    grid-column: 2;
    grid-row: 1;
  }

  .css-cap.cap-1 { animation: capShow1 16s linear infinite; animation-delay: var(--seek-delay, 0s); }
  .css-cap.cap-2 { animation: capShow2 16s linear infinite; animation-delay: var(--seek-delay, 0s); }
  .css-cap.cap-3 { animation: capShow3 16s linear infinite; animation-delay: var(--seek-delay, 0s); }
  .css-cap.cap-4 { animation: capShow4 16s linear infinite; animation-delay: var(--seek-delay, 0s); }

  /* Bottom Scrubber Track */
  .cinema-scrub-bar {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 10px;
    padding: 0;
    border: 0;
    background: transparent;
    cursor: pointer;
    display: flex;
    align-items: flex-end;
  }

  .scrub-track {
    display: block;
    width: 100%;
    height: 4px;
    background: rgba(255, 255, 255, 0.28);
  }

  .scrub-fill {
    display: block;
    height: 100%;
    width: 0%;
    background: #34d399;
    animation: scrubProgress 16s linear infinite;
    animation-delay: var(--seek-delay, 0s);
  }

  .scrub-fill.has-js-sync {
    animation: none;
    transition: width 0.1s linear;
  }

  /* Paused State */
  .toto-cinema-card.paused .cinema-bg-img,
  .toto-cinema-card.paused .fx-cloud-slow,
  .toto-cinema-card.paused .fx-flight-arc,
  .toto-cinema-card.paused .toto-flyer,
  .toto-cinema-card.paused .toto-flyer-sprite,
  .toto-cinema-card.paused .scrub-fill,
  .toto-cinema-card.paused .css-cap {
    animation-play-state: paused !important;
  }

  /* Bottom Controls Strip */
  .tc-footer-bar {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.45rem;
    padding: 0.45rem 0.85rem;
    background: var(--bg-surface);
    border-top: 1px solid var(--border-subtle);
  }

  .tc-play-controls {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
  }

  .btn-video-ctrl {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    border-radius: 7px;
    padding: 0.22rem 0.52rem;
    font-size: 0.72rem;
    font-weight: 700;
    min-height: 28px;
    cursor: pointer;
  }

  .btn-video-ctrl:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .tc-time-code {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    color: var(--text-muted);
    margin-inline-start: 0.15rem;
  }

  .tc-scene-dots {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
  }

  .scene-dot {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    font-family: var(--font-family-mono);
    font-size: 0.66rem;
    font-weight: 700;
    cursor: pointer;
    padding: 0;
  }

  .scene-dot.active {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .tc-story-link {
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--accent-primary);
    text-decoration: none;
    white-space: nowrap;
  }

  .tc-story-link:hover {
    text-decoration: underline;
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

  /* Keyframes: 16s Movie Choreography */
  @keyframes kenBurns16s {
    0%, 100% { transform: scale(1) translate3d(0, 0, 0); }
    50% { transform: scale(1.05) translate3d(-1.2%, -0.6%, 0); }
  }

  @keyframes totoFlyLoop {
    0%   { transform: translate3d(10cqw, 16cqh, 0) scale(0.88) rotate(8deg); opacity: 1; }
    24%  { transform: translate3d(68cqw, 14cqh, 0) scale(0.96) rotate(-6deg); opacity: 1; }
    44%  { transform: translate3d(42cqw, 18cqh, 0) scale(1.22) rotate(0deg); opacity: 1; }
    66%  { transform: translate3d(24cqw, 22cqh, 0) scale(1.02) rotate(-8deg); opacity: 1; }
    84%  { transform: translate3d(66cqw, 10cqh, 0) scale(0.92) rotate(8deg); opacity: 1; }
    100% { transform: translate3d(10cqw, 16cqh, 0) scale(0.88) rotate(8deg); opacity: 1; }
  }

  @keyframes totoWingBob {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-4px); }
  }

  @keyframes cloudGlide {
    0% { transform: translateX(-28px); }
    50% { transform: translateX(28px); }
    100% { transform: translateX(-28px); }
  }

  @keyframes arcGlow {
    0%, 100% { opacity: 0.28; }
    25% { opacity: 0.85; }
    65% { opacity: 0.45; }
  }

  @keyframes sparkleWater {
    0%, 100% { opacity: 0.25; }
    50% { opacity: 0.9; }
  }

  @keyframes pulseGlow {
    0%, 100% { opacity: 0.72; transform: scale(0.96); }
    50% { opacity: 1; transform: scale(1.05); }
  }

  @keyframes starTwinkle {
    0%, 100% { opacity: 0.55; transform: scale(0.8) rotate(0deg); }
    50% { opacity: 1; transform: scale(1.15) rotate(22deg); }
  }

  @keyframes scrubProgress {
    0% { width: 0%; }
    100% { width: 100%; }
  }

  @keyframes capShow1 {
    0%, 23% { opacity: 1; }
    25%, 100% { opacity: 0; }
  }
  @keyframes capShow2 {
    0%, 24% { opacity: 0; }
    26%, 48% { opacity: 1; }
    50%, 100% { opacity: 0; }
  }
  @keyframes capShow3 {
    0%, 49% { opacity: 0; }
    51%, 73% { opacity: 1; }
    75%, 100% { opacity: 0; }
  }
  @keyframes capShow4 {
    0%, 74% { opacity: 0; }
    76%, 98% { opacity: 1; }
    100% { opacity: 0; }
  }

  @media (prefers-reduced-motion: reduce) {
    .cinema-bg-img,
    .fx-sun-bloom,
    .fx-cloud-slow,
    .fx-flight-arc,
    .fx-water-spark,
    .toto-flyer,
    .toto-flyer-sprite,
    .flyer-aura,
    .flyer-star,
    .scrub-fill,
    .live-dot {
      animation: none !important;
    }
    .toto-flyer {
      transform: translate3d(42cqw, 16cqh, 0) scale(1);
      opacity: 1;
    }
  }
</style>
