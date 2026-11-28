<script lang="ts">
  import { dict } from '../i18n/store';
  import {
    readinessStore,
    completedWishList,
    shadowSummary,
    deriveTrailArchetype,
    type LightKey,
    type ShadowKey
  } from '../lib/readinessState';
  import { countryContextStore } from '../lib/countryContext';
  import { trackEvent } from '../lib/privacyStorage';

  const LIGHT_KEYS: LightKey[] = ['Clarity', 'Foresight', 'Fairness', 'Wisdom', 'Capability'];
  const SHADOW_KEYS: ShadowKey[] = ['Control', 'Dependence', 'Power', 'Truth', 'Speed'];

  export let activeLightKey: LightKey = 'Clarity';
  export let compact = false;

  $: state = $readinessStore;
  $: completed = $completedWishList;
  $: shadows = $shadowSummary;
  $: doneCount = completed.length;
  $: heritageDoneCount = completed.filter((w) => w.wishId.startsWith('heritage-')).length;
  $: archetypeKey = deriveTrailArchetype(state.lights, shadows);
  $: archetypeInfo = $dict.player.trails[archetypeKey];

  $: selectedCountryText = (() => {
    const c = state.selectedCountry;
    if (!c) return $dict.player.countryCapabilityUnset;
    if (c.kind === 'unrated') {
      return $dict.player.countryCapabilityUnrated.replace('{name}', c.name);
    }
    return $dict.player.countryCapabilityNote
      .replace('{name}', c.name)
      .replace('{count}', String(c.checklistCount ?? 0));
  })();

  $: activeCountryLabel =
    state.selectedCountry?.name ??
    ($countryContextStore.iso !== 'GLOBAL' ? $countryContextStore.countryName : '');
  $: countryCapStatus = (() => {
    const c = state.selectedCountry;
    if (!c) return '';
    if (c.kind === 'rated') return `${c.checklistCount ?? 0}/5`;
    return $dict.heritageUi.livingBadge ? 'Partial' : 'Partial';
  })();

  function getLocalizedLight(idx: number) {
    return $dict.lights.items[idx] ?? $dict.lights.items[0];
  }

  function downloadBlob(blob: Blob, filename: string) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function exportCardPng(w: number, h: number, mode: 'trail' | 'shadow') {
    const canvas = document.createElement('canvas');
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Warm dawn paper backdrop
    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, '#fdf7ec');
    grad.addColorStop(1, '#ede3ce');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // Subtle seafoam border frame
    ctx.strokeStyle = '#1b6756';
    ctx.lineWidth = Math.round(w * 0.008);
    ctx.strokeRect(32, 32, w - 64, h - 64);

    const padX = Math.round(w * 0.065);
    const isStory = h > w;

    ctx.fillStyle = '#1b6756';
    ctx.font = `700 ${isStory ? 28 : 22}px sans-serif`;
    ctx.fillText('HUMANITY READINESS · TOTO', padX, isStory ? 130 : 100);

    ctx.fillStyle = '#1e1915';
    ctx.font = `800 ${isStory ? 56 : 44}px sans-serif`;
    const title = mode === 'trail' ? archetypeInfo.name : 'My 5-Breakthrough Shadow Map';
    ctx.fillText(title, padX, isStory ? 210 : 165);

    ctx.fillStyle = '#4a4034';
    ctx.font = `500 ${isStory ? 30 : 22}px sans-serif`;
    const sub =
      mode === 'trail'
        ? archetypeInfo.note.slice(0, 74)
        : `Completed ${doneCount} breakthroughs across Control, Dependence, Power, Truth & Speed`;
    ctx.fillText(sub, padX, isStory ? 265 : 210);

    // Draw the 5 lights (glow levels 0..3 as luminous circles, zero raw digits)
    const startY = isStory ? 390 : 295;
    const stepX = isStory ? 0 : Math.floor((w - padX * 2) / 5);
    const stepY = isStory ? 140 : 0;

    LIGHT_KEYS.forEach((lk, i) => {
      const level = state.lights[lk];
      const cx = isStory ? padX + 44 : padX + i * stepX + 44;
      const cy = startY + i * stepY;

      ctx.beginPath();
      ctx.arc(cx, cy, level === 3 ? 28 : level === 2 ? 24 : 20, 0, Math.PI * 2);
      ctx.fillStyle =
        level === 3 ? '#f59e0b' : level === 2 ? '#fbbf24' : level === 1 ? '#fde68a' : '#e2d9c5';
      ctx.fill();
      ctx.lineWidth = 3;
      ctx.strokeStyle = level > 0 ? '#b45309' : '#a49782';
      ctx.stroke();

      ctx.fillStyle = '#1e1915';
      ctx.font = `700 ${isStory ? 34 : 20}px sans-serif`;
      const label = getLocalizedLight(i).key;
      if (isStory) {
        ctx.fillText(label, cx + 56, cy + 11);
      } else {
        ctx.fillText(label, cx - 32, cy + 56);
      }
    });

    if (mode === 'shadow') {
      const syBase = isStory ? 1140 : 410;
      SHADOW_KEYS.forEach((sk, idx) => {
        const y = syBase + idx * (isStory ? 75 : 32);
        ctx.fillStyle = '#1e1915';
        ctx.font = `700 ${isStory ? 28 : 17}px sans-serif`;
        ctx.fillText($dict.player.shadows[sk], padX, y);
        const count = shadows[sk] || 0;
        for (let b = 0; b < 5; b++) {
          ctx.fillStyle = b < count ? '#1b6756' : '#ddd4be';
          ctx.fillRect(padX + (isStory ? 220 : 140) + b * (isStory ? 64 : 42), y - 16, isStory ? 52 : 34, isStory ? 20 : 14);
        }
      });
    }

    if (heritageDoneCount > 0) {
      ctx.fillStyle = '#1b6756';
      ctx.font = `700 ${isStory ? 26 : 19}px sans-serif`;
      ctx.fillText(`Cultural horizons explored: ${heritageDoneCount}`, padX, h - (isStory ? 190 : 122));
    }

    ctx.fillStyle = '#1b6756';
    ctx.font = `700 ${isStory ? 32 : 24}px sans-serif`;
    ctx.fillText('Every great breakthrough needs a ready world.', padX, h - (isStory ? 140 : 88));

    ctx.fillStyle = '#6c6152';
    ctx.font = `600 ${isStory ? 24 : 18}px monospace`;
    ctx.fillText('humanityreadiness.org · open science · local browser record', padX, h - (isStory ? 90 : 54));

    canvas.toBlob((blob) => {
      if (blob) {
        downloadBlob(blob, `humanity-readiness-${mode}-${w}x${h}.png`);
        trackEvent('share_clicked', { format: `${mode}_${w}x${h}` });
      }
    }, 'image/png');
  }

  function exportSvgCard() {
    const svgEl = document.getElementById('hr-trail-preview-svg');
    if (!svgEl) return;
    const xml = new XMLSerializer().serializeToString(svgEl);
    downloadBlob(new Blob([xml], { type: 'image/svg+xml' }), 'humanity-readiness-trail-card.svg');
    trackEvent('share_clicked', { format: 'svg' });
  }
</script>

<!-- Compact visual readiness diagram on homepage until visitor begins playing -->
{#if compact && doneCount === 0}
  <div class="compact-lights-strip">
    <div class="cls-top">
      <span class="cls-title">
        {activeCountryLabel
          ? $dict.heritageUi.lightsCountryHeading.replace('{country}', activeCountryLabel)
          : `${$dict.lights.heading}:`}
      </span>
      <span class="cls-hint">{$dict.lights.emptyState}</span>
    </div>

    <div class="lights-visual-diagram" role="tablist" aria-label={$dict.lights.heading}>
      <div class="lvd-group human-group">
        <span class="lvd-group-lbl">{$dict.heritageUi.lightsHumanGroup}</span>
        <div class="lvd-orbs-track">
          <span class="lvd-rail" aria-hidden="true"></span>
          {#each LIGHT_KEYS.slice(0, 4) as lk, idx}
            {@const info = getLocalizedLight(idx)}
            <button
              type="button"
              role="tab"
              aria-selected={activeLightKey === lk}
              class="light-pill compact-pill"
              class:active={activeLightKey === lk}
              on:click={() => (activeLightKey = lk)}
            >
              <span class="lamp-orb glow-0" aria-hidden="true"></span>
              <strong>{info.key}</strong>
            </button>
          {/each}
        </div>
      </div>

      <span class="lvd-bridge-arrow" aria-hidden="true">+</span>

      <div class="lvd-group country-group" class:has-country={Boolean(activeCountryLabel)}>
        <span class="lvd-group-lbl">
          {activeCountryLabel
            ? $dict.heritageUi.lightsCountryGroup.replace('{country}', activeCountryLabel)
            : getLocalizedLight(4).key}
        </span>
        <button
          type="button"
          role="tab"
          aria-selected={activeLightKey === 'Capability'}
          class="light-pill compact-pill cap-pill"
          class:active={activeLightKey === 'Capability'}
          on:click={() => (activeLightKey = 'Capability')}
        >
          <span class="lamp-orb" class:glow-country={Boolean(activeCountryLabel)} aria-hidden="true"></span>
          <strong>{getLocalizedLight(4).key}</strong>
          {#if state.selectedCountry}
            <span class="cap-chip">
              {state.selectedCountry.kind === 'rated'
                ? `${state.selectedCountry.checklistCount ?? 0}/5`
                : 'Audit'}
            </span>
          {/if}
        </button>
      </div>
    </div>

    <p class="cls-meaning">
      <strong>{getLocalizedLight(LIGHT_KEYS.indexOf(activeLightKey)).key}:</strong>
      {getLocalizedLight(LIGHT_KEYS.indexOf(activeLightKey)).meaning}
      <span class="cls-local-note">&middot; {$dict.lights.trailNote}</span>
    </p>
  </div>
{:else}
<!-- Interactive 5 Lights Array (glow levels 0-3 only, zero numeric scores) -->
<div class="lights-row" role="tablist" aria-label={$dict.lights.heading}>
  {#each LIGHT_KEYS as lk, idx}
    {@const info = getLocalizedLight(idx)}
    {@const glow = state.lights[lk]}
    <button
      type="button"
      role="tab"
      aria-selected={activeLightKey === lk}
      class="light-pill"
      class:active={activeLightKey === lk}
      on:click={() => (activeLightKey = lk)}
    >
      <span
        class={`lamp-orb glow-${glow}`}
        aria-label={`${info.key}: glow level ${glow} of 3`}
      ></span>
      <span class="lamp-text">
        <strong>{info.key}</strong>
        <span>{info.meaning}</span>
      </span>
    </button>
  {/each}
</div>

<div class="lights-status-box">
  <p class="lights-empty">
    {doneCount === 0
      ? $dict.lights.emptyState
      : `${doneCount} breakthrough${doneCount === 1 ? '' : 's'} completed · ${$dict.lights.lowLightNote}`}
  </p>
  <p class="lights-reassurance">
    <strong>{getLocalizedLight(LIGHT_KEYS.indexOf(activeLightKey)).key}:</strong>
    {getLocalizedLight(LIGHT_KEYS.indexOf(activeLightKey)).meaning}
  </p>
  <p class="lights-country-cap">{selectedCountryText}</p>
  <p class="lights-trail-note">{$dict.player.lightsLegend}</p>
</div>

<!-- Trail Card (3+ breakthroughs) & Shadow Map (5+ breakthroughs) -->
<div class="trail-wrap">
  <h3 class="trail-heading">{$dict.player.trailSectionTitle}</h3>

  {#if doneCount < 3}
    <div class="unlock-box">
      <p>{$dict.player.trailLocked.replace('{done}', String(doneCount))}</p>
      <p class="sub-lock">{$dict.player.shadowLocked.replace('{done}', String(doneCount))}</p>
    </div>
  {:else}
    <div class="trail-unlocked-card">
      <div class="trail-meta">
        <span class="unlock-badge">{$dict.player.trailUnlockedBadge}</span>
        <h4>{archetypeInfo.name}</h4>
        <p>{archetypeInfo.note}</p>
        {#if heritageDoneCount > 0}
          <p class="heritage-stamp-pill">
            {$dict.heritageUi.trailStampLabel.replace('{count}', String(heritageDoneCount))}
          </p>
        {/if}

        <div class="share-actions">
          <button type="button" class="btn-share" on:click={() => exportCardPng(1200, 630, 'trail')}>
            {$dict.player.downloadLandscape}
          </button>
          <button type="button" class="btn-share-sec" on:click={() => exportCardPng(1080, 1920, 'trail')}>
            {$dict.player.downloadStory}
          </button>
          <button type="button" class="btn-share-sec" on:click={exportSvgCard}>
            {$dict.player.downloadSvg}
          </button>
        </div>
      </div>

      <svg
        id="hr-trail-preview-svg"
        class="trail-svg"
        viewBox="0 0 360 190"
        width="360"
        height="190"
        role="img"
        aria-label={`Readiness Trail card: ${archetypeInfo.name}`}
      >
        <rect width="360" height="190" rx="12" fill="#fdf7ec" stroke="#1b6756" stroke-width="2" />
        <text x="18" y="28" font-family="monospace" font-size="10" font-weight="bold" fill="#1b6756">HUMANITY READINESS TRAIL</text>
        <text x="18" y="52" font-family="sans-serif" font-size="18" font-weight="bold" fill="#1e1915">{archetypeInfo.name}</text>
        {#each LIGHT_KEYS as lk, idx}
          {@const g = state.lights[lk]}
          <circle
            cx={42 + idx * 68}
            cy="102"
            r={g === 3 ? 16 : g === 2 ? 14 : 11}
            fill={g === 3 ? '#f59e0b' : g === 2 ? '#fbbf24' : g === 1 ? '#fde68a' : '#e2d9c5'}
            stroke={g > 0 ? '#b45309' : '#a49782'}
            stroke-width="2"
          />
          <text x={42 + idx * 68} y="132" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="#4a4034">
            {getLocalizedLight(idx).key}
          </text>
        {/each}
        <text x="18" y="166" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1b6756">Every great breakthrough needs a ready world.</text>
      </svg>
    </div>

    {#if doneCount < 5}
      <div class="unlock-box mt-gap">
        <p>{$dict.player.shadowLocked.replace('{done}', String(doneCount))}</p>
      </div>
    {:else}
      <div class="shadow-map-card mt-gap">
        <span class="unlock-badge">{$dict.player.shadowUnlockedBadge}</span>
        <div class="shadow-bars">
          {#each SHADOW_KEYS as sk}
            {@const c = shadows[sk] || 0}
            <div class="sb-row">
              <span class="sb-name">{$dict.player.shadows[sk]}</span>
              <div class="sb-cells" aria-label={`${$dict.player.shadows[sk]} spotted ${c} times`}>
                {#each [0, 1, 2, 3, 4] as step}
                  <span class="sb-cell" class:filled={step < c}></span>
                {/each}
              </div>
            </div>
          {/each}
        </div>
        <button type="button" class="btn-share-sec" on:click={() => exportCardPng(1200, 630, 'shadow')}>
          {$dict.player.downloadShadowPng}
        </button>
      </div>
    {/if}
  {/if}
</div>
{/if}

<style>
  .compact-lights-strip {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 0.85rem 1rem;
    text-align: center;
  }

  .cls-top {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.35rem;
    margin-bottom: 0.55rem;
    font-size: 0.84rem;
  }

  .cls-title {
    font-weight: 800;
    color: var(--text-primary);
  }

  .cls-hint {
    color: var(--text-secondary);
  }

  .lights-visual-diagram {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.55rem 0.75rem;
    margin-bottom: 0.55rem;
  }

  .lvd-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
    padding: 0.42rem 0.65rem;
    border-radius: 12px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
  }

  .lvd-group.country-group.has-country {
    background: var(--threat-sovereign-bg);
    border-color: var(--threat-sovereign-border);
  }

  .lvd-group-lbl {
    font-family: var(--font-family-mono);
    font-size: 0.62rem;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 0.04em;
  }

  .lvd-group.country-group.has-country .lvd-group-lbl {
    color: var(--accent-primary);
  }

  .lvd-orbs-track {
    position: relative;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.35rem;
  }

  .lvd-rail {
    position: absolute;
    left: 10%;
    right: 10%;
    top: 50%;
    height: 2px;
    background: var(--border-medium);
    transform: translateY(-50%);
    z-index: 0;
  }

  .lvd-orbs-track .light-pill.compact-pill {
    position: relative;
    z-index: 1;
  }

  .lvd-bridge-arrow {
    font-family: var(--font-family-mono);
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .lamp-orb.glow-country {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
  }

  .cap-chip {
    font-family: var(--font-family-mono);
    font-size: 0.64rem;
    font-weight: 800;
    padding: 0.06rem 0.36rem;
    border-radius: 9999px;
    background: var(--bg-surface-elevated);
    color: var(--accent-primary);
    border: 1px solid var(--threat-sovereign-border);
  }

  .light-pill.compact-pill.active .cap-chip {
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff;
    border-color: rgba(255, 255, 255, 0.45);
  }

  .light-pill.compact-pill {
    padding: 0.42rem 0.85rem;
    border-radius: 9999px;
    border: 1.5px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    align-items: center;
    gap: 0.42rem;
    min-height: 40px;
    font-size: 0.84rem;
    font-weight: 700;
    transition: border-color 0.15s ease, background-color 0.15s ease, color 0.15s ease;
  }

  .light-pill.compact-pill strong {
    color: inherit;
  }

  .light-pill.compact-pill:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .light-pill.compact-pill.active {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .light-pill.compact-pill.active strong {
    color: var(--btn-primary-text);
  }

  .light-pill.compact-pill.active .lamp-orb {
    border-color: rgba(255, 255, 255, 0.85);
    background: rgba(255, 255, 255, 0.25);
  }

  .cls-meaning {
    margin: 0;
    font-size: 0.8rem;
    color: var(--text-secondary);
  }

  .cls-local-note {
    color: var(--text-muted);
  }

  .lights-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.25rem;
  }

  .light-pill {
    text-align: start;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 0.9rem 0.85rem;
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    cursor: pointer;
    transition: all 0.16s ease;
  }

  .light-pill:hover,
  .light-pill.active {
    border-color: var(--accent-primary);
    background: var(--bg-surface);
  }

  .lamp-orb {
    width: 16px;
    height: 16px;
    margin-top: 2px;
    border-radius: 50%;
    flex-shrink: 0;
    border: 2px solid var(--border-strong);
    background: var(--bg-surface-sunken);
    transition: all 0.2s ease;
  }

  .lamp-orb.glow-1 {
    background: #fde68a;
    border-color: #d97706;
    box-shadow: 0 0 6px rgba(245, 158, 11, 0.35);
  }

  .lamp-orb.glow-2 {
    background: #fbbf24;
    border-color: #b45309;
    box-shadow: 0 0 11px rgba(245, 158, 11, 0.55);
  }

  .lamp-orb.glow-3 {
    background: #f59e0b;
    border-color: #92400e;
    box-shadow: 0 0 16px rgba(245, 158, 11, 0.8);
  }

  .lamp-text {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }

  .lamp-text strong {
    font-size: 0.94rem;
    color: var(--text-primary);
  }

  .lamp-text span {
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.35;
  }

  .lights-status-box {
    text-align: center;
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1.15rem 1.25rem;
  }

  .lights-empty {
    font-weight: 700;
    font-size: 0.96rem;
    color: var(--text-primary);
    margin: 0 0 0.3rem;
  }

  .lights-reassurance {
    font-size: 0.88rem;
    color: var(--text-secondary);
    margin: 0 0 0.3rem;
  }

  .lights-country-cap {
    font-size: 0.82rem;
    color: var(--accent-primary);
    font-weight: 600;
    margin: 0 0 0.3rem;
  }

  .lights-trail-note {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin: 0;
  }

  .trail-wrap {
    margin-top: 1.4rem;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    padding: 1.25rem;
  }

  .trail-heading {
    margin: 0 0 0.75rem;
    font-size: 1.08rem;
    color: var(--text-primary);
  }

  .unlock-box {
    padding: 0.85rem 1rem;
    border-radius: 12px;
    background: var(--bg-surface-sunken);
    border: 1px dashed var(--border-medium);
    font-size: 0.86rem;
    color: var(--text-secondary);
  }

  .unlock-box p {
    margin: 0;
  }

  .sub-lock {
    margin-top: 0.35rem !important;
    font-size: 0.8rem;
  }

  .trail-unlocked-card {
    display: grid;
    grid-template-columns: 1.25fr 0.9fr;
    gap: 1.1rem;
    align-items: center;
  }

  .unlock-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    padding: 0.2rem 0.55rem;
    border-radius: 9999px;
    background: var(--threat-sovereign-bg);
    color: var(--threat-sovereign);
    border: 1px solid var(--threat-sovereign-border);
    margin-bottom: 0.4rem;
  }

  .trail-meta h4 {
    margin: 0 0 0.35rem;
    font-size: 1.25rem;
    color: var(--text-primary);
  }

  .trail-meta p {
    margin: 0 0 0.9rem;
    font-size: 0.88rem;
    color: var(--text-secondary);
  }

  .share-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
  }

  .btn-share {
    border: 0;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    padding: 0.5rem 0.9rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.8rem;
    cursor: pointer;
    min-height: 36px;
  }

  .btn-share-sec {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    padding: 0.48rem 0.85rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.78rem;
    cursor: pointer;
    min-height: 36px;
  }

  .trail-svg {
    width: 100%;
    height: auto;
    border-radius: 10px;
  }

  .mt-gap {
    margin-top: 1rem;
  }

  .shadow-map-card {
    padding: 1rem;
    border-radius: 12px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-medium);
  }

  .shadow-bars {
    display: grid;
    gap: 0.5rem;
    margin: 0.65rem 0 0.9rem;
  }

  .sb-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
  }

  .sb-name {
    font-size: 0.84rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .sb-cells {
    display: flex;
    gap: 0.25rem;
  }

  .sb-cell {
    width: 24px;
    height: 10px;
    border-radius: 3px;
    background: var(--border-subtle);
  }

  .sb-cell.filled {
    background: var(--accent-primary);
  }

  .heritage-stamp-pill {
    display: inline-block;
    margin: 0.45rem 0 0;
    padding: 0.18rem 0.6rem;
    border-radius: 9999px;
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
    color: var(--accent-primary);
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
  }

  @media (max-width: 1024px) {
    .lights-row {
      grid-template-columns: repeat(2, 1fr);
    }
    .trail-unlocked-card {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 640px) {
    .lights-row {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 0.4rem;
      margin-bottom: 0.75rem;
    }
    .light-pill {
      flex: 0 1 auto;
      padding: 0.42rem 0.8rem;
      border-radius: 9999px;
      border: 1.5px solid var(--border-medium);
      align-items: center;
      gap: 0.42rem;
      min-height: 40px;
    }
    .light-pill.active {
      background: var(--accent-primary);
      border-color: var(--accent-primary);
      color: var(--btn-primary-text);
    }
    .light-pill.active strong {
      color: var(--btn-primary-text);
    }
    .light-pill.active .lamp-orb.glow-0 {
      border-color: rgba(255, 255, 255, 0.85);
      background: rgba(255, 255, 255, 0.25);
    }
    .lamp-orb {
      margin-top: 0;
      width: 14px;
      height: 14px;
    }
    .lamp-text span {
      display: none;
    }
    .lamp-text strong {
      font-size: 0.84rem;
    }
    .lights-status-box {
      padding: 0.85rem 0.9rem;
    }
    .lights-empty {
      font-size: 0.88rem;
    }
    .lights-reassurance,
    .lights-country-cap {
      font-size: 0.8rem;
    }
    .lights-trail-note {
      font-size: 0.72rem;
    }
    .trail-wrap {
      margin-top: 0.85rem;
      padding: 0.9rem;
    }
    .trail-heading {
      margin-bottom: 0.5rem;
      font-size: 0.98rem;
    }
    .unlock-box {
      padding: 0.7rem 0.8rem;
      font-size: 0.8rem;
    }
  }
</style>
