<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { dict, activeLocale } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';
  import { readinessStore } from '../lib/readinessState';
  import { countryContextStore, syncCountryContext } from '../lib/countryContext';
  import { findCityById } from '../lib/countrySkies';
  import {
    CORE_BREAKTHROUGHS,
    loadAllBreakthroughs
  } from '../lib/breakthroughCatalog';
  import {
    HERITAGE_INDEX,
    doorHasHeritageForCountry,
    findAnyHeritageForCountry,
    findHeritageForCountryAndDoor,
    loadHeritageBreakthrough
  } from '../lib/heritageLoader';
  import type { HeritageIndexEntry, PlayableHeritageWish } from '../lib/heritageTypes';

  const SHOW_DRAFT_BADGE = __HSRI_SHOW_DRAFTS__;
  const INCLUDE_DEV_BREAKTHROUGHS = __HSRI_INCLUDE_DEV15__;
  import WishPlayer, { type WishItem } from './WishPlayer.svelte';
  import TrailAndShadowCard from './TrailAndShadowCard.svelte';

  export let base = '';

  let catalog: WishItem[] = CORE_BREAKTHROUGHS;
  let heritageCache: Record<string, PlayableHeritageWish> = {};
  let revealed = false;
  let activeDoorId = 'epic';
  let activeWishId: string | null = null;
  let preferGlobal = false;
  let lastSeenIso = 'GLOBAL';
  let loadingHeritage = false;
  let playerAnchorEl: HTMLElement | null = null;

  onMount(async () => {
    revealed = true;
    if (INCLUDE_DEV_BREAKTHROUGHS) {
      catalog = await loadAllBreakthroughs();
    }
  });

  $: loc = ($activeLocale === 'es' || $activeLocale === 'ar' ? $activeLocale : 'en') as 'en' | 'es' | 'ar';
  $: activeIso = $countryContextStore.iso;
  $: activeCountryLabel = $countryContextStore.countryName;
  $: if (activeIso !== lastSeenIso) {
    lastSeenIso = activeIso;
    preferGlobal = false;
    const localMatch = findAnyHeritageForCountry(activeIso);
    if (localMatch && !activeWishId) {
      activeDoorId = localMatch.door;
    }
  }
  $: PLAYABLE_WISHES = catalog;
  $: WISH_BY_ID = new Map(PLAYABLE_WISHES.map((w) => [w.id, w]));
  $: selectedDoor = $dict.doors.items.find((d) => d.id === activeDoorId) ?? $dict.doors.items[0];
  $: doorHeritage = findHeritageForCountryAndDoor(activeIso, selectedDoor.id);
  $: anyCountryHeritage = findAnyHeritageForCountry(activeIso);
  $: showingHeritage = Boolean(doorHeritage && !preferGlobal);
  $: activeWish =
    (activeWishId ? WISH_BY_ID.get(activeWishId) ?? heritageCache[activeWishId] : null) ?? null;
  $: completedIds = $readinessStore.wishes;
  $: domainDevItems = INCLUDE_DEV_BREAKTHROUGHS
    ? PLAYABLE_WISHES.filter((w) => w.door === selectedDoor.id)
    : [];

  function chooseDoor(id: string) {
    activeDoorId = id;
    activeWishId = null;
    preferGlobal = false;
    trackEvent('door_preview_select', { door: id });
  }

  async function launchWish(wishId: string) {
    activeWishId = wishId;
    await tick();
    playerAnchorEl?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  async function launchHeritage(entry: HeritageIndexEntry) {
    loadingHeritage = true;
    try {
      const loaded = await loadHeritageBreakthrough(entry.id);
      if (loaded) {
        heritageCache = { ...heritageCache, [loaded.id]: loaded };
        activeWishId = loaded.id;
        await tick();
        playerAnchorEl?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    } finally {
      loadingHeritage = false;
    }
  }

  function selectWorldTradition(entry: HeritageIndexEntry) {
    const targetIso = entry.countries[0] ?? 'NOR';
    syncCountryContext(findCityById(targetIso), true);
    activeDoorId = entry.door;
    activeWishId = null;
    preferGlobal = false;
    trackEvent('door_preview_select', { door: `heritage:${entry.id}` });
  }

  function playNextUnseenWish() {
    const next = PLAYABLE_WISHES.find((w) => !completedIds[w.id] && w.id !== activeWishId)
      ?? PLAYABLE_WISHES[(PLAYABLE_WISHES.findIndex((w) => w.id === activeWishId) + 1) % PLAYABLE_WISHES.length];
    if (next) {
      activeDoorId = next.door;
      launchWish(next.id);
    }
  }
</script>

<!-- STEP 2: COMPACT 60-SECOND BREAKTHROUGH EXPLORER -->
<section id="wish-doors" class="story-section doors-section">
  <div class="section-wrap">
    <div class="section-head">
      <h2 class="sec-title">{$dict.doors.heading}</h2>
      <p class="sec-sub">{$dict.doors.microcopy}</p>
    </div>

    {#if revealed}
      <!-- 1-Line Scrollable World Traditions Strip (surfaced upfront, zero mobile vertical bloat) -->
      <div class="world-horizons-bar" aria-label="Cultural traditions around the world">
        <span class="wh-label">World traditions:</span>
        <div class="wh-scroll">
          {#each HERITAGE_INDEX as h}
            {@const isSelected = Boolean(doorHeritage?.id === h.id && showingHeritage)}
            <button
              type="button"
              class="wh-chip"
              class:active={isSelected}
              onclick={() => selectWorldTradition(h)}
              title={`${h.originRegion[loc] ?? h.originRegion.en}: ${h.chipTitle[loc] ?? h.chipTitle.en}`}
            >
              {h.traditionLabel[loc] ?? h.traditionLabel.en}
            </button>
          {/each}
        </div>
        <a href={`${base}/traditions/`} class="wh-all-link">All {HERITAGE_INDEX.length} &rarr;</a>
      </div>

      <!-- Clean 5-Domain Pill Tabs -->
      <div class="doors-tabs" role="tablist" aria-label="Five breakthrough domains">
        {#each $dict.doors.items as door}
          <button
            type="button"
            role="tab"
            aria-selected={activeDoorId === door.id}
            class="door-tab"
            class:selected={activeDoorId === door.id}
            onclick={() => chooseDoor(door.id)}
          >
            <span class="door-icon" aria-hidden="true">
              {#if door.icon === 'chalkboard'}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="13" rx="1.5" />
                  <path d="M7 9h6M7 13h9M9 17l-1.5 3M15 17l1.5 3" stroke-linecap="round" />
                </svg>
              {:else if door.icon === 'pocket'}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 6h14v7a7 7 0 0 1-14 0V6z" />
                  <circle cx="12" cy="12" r="2.5" stroke="var(--accent-primary)" />
                </svg>
              {:else if door.icon === 'eye'}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M2 12s4-5.5 10-5.5S22 12 22 12s-4 5.5-10 5.5S2 12 2 12z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
              {:else if door.icon === 'frame'}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="5" width="18" height="14" rx="1.5" />
                  <path d="M10 9l5 3-5 3V9z" stroke-linejoin="round" />
                </svg>
              {:else}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M8 16h8l-1.5 4h-5L8 16z" />
                  <circle cx="12" cy="11" r="3.5" />
                </svg>
              {/if}
            </span>
            <span class="door-title">{door.title}</span>
            {#if doorHasHeritageForCountry(activeIso, door.id)}
              <span
                class="door-heritage-dot"
                title={$dict.heritageUi.localHorizonTag.replace('{country}', activeCountryLabel)}
                aria-hidden="true"
              ></span>
            {/if}
          </button>
        {/each}
      </div>

      <!-- Active Domain Focus Card OR Interactive 4-Beat Player -->
      <div bind:this={playerAnchorEl}>
        {#if activeWish}
          {#key activeWish.id}
            <WishPlayer
              wish={activeWish}
              base={base}
              onClose={() => (activeWishId = null)}
              onNextWish={playNextUnseenWish}
            />
          {/key}
        {:else}
          <div class="door-preview-panel" role="tabpanel" aria-live="polite">
            <div class="dp-header-line">
              <span class="dp-door-tag">{selectedDoor.title}</span>
              <span class="dp-lead">{selectedDoor.lead}</span>
            </div>

            <!-- Fixed-height 1-line heritage swap bar (zero extra mobile scroll / CLS=0) -->
            <div class="heritage-swap-bar">
              {#if doorHeritage && showingHeritage}
                <div class="hs-left">
                  <span class="hs-pill">
                    {$dict.heritageUi.localHorizonTag.replace('{country}', activeCountryLabel)}
                  </span>
                  <span class="hs-era">
                    {doorHeritage.era === 'living' ? $dict.heritageUi.livingBadge : $dict.heritageUi.historicalBadge}
                  </span>
                </div>
                <div class="hs-actions">
                  <a href={`${base}/traditions/${doorHeritage.slug}/`} class="hs-archive-link">
                    {$dict.heritageUi.readArchiveLink} &rarr;
                  </a>
                  <button type="button" class="hs-toggle-btn" onclick={() => (preferGlobal = true)}>
                    {$dict.heritageUi.seeGlobalBtn}
                  </button>
                </div>
              {:else if doorHeritage && preferGlobal}
                <div class="hs-left">
                  <span class="hs-muted">{$dict.doors.sampleHeading}</span>
                </div>
                <div class="hs-actions">
                  <button type="button" class="hs-toggle-btn active" onclick={() => (preferGlobal = false)}>
                    {$dict.heritageUi.seeLocalBtn.replace('{country}', activeCountryLabel)}
                  </button>
                </div>
              {:else if anyCountryHeritage && anyCountryHeritage.door !== selectedDoor.id}
                {@const targetDoor = $dict.doors.items.find((d) => d.id === anyCountryHeritage.door)}
                <div class="hs-left">
                  <span class="hs-muted">
                    {$dict.heritageUi.livesInOtherDoor
                      .replace('{country}', activeCountryLabel)
                      .replace('{door}', targetDoor?.title ?? anyCountryHeritage.door)}
                  </span>
                </div>
                <div class="hs-actions">
                  <button
                    type="button"
                    class="hs-toggle-btn active"
                    onclick={() => chooseDoor(anyCountryHeritage.door)}
                  >
                    {targetDoor?.title ?? 'Open'} &rarr;
                  </button>
                </div>
              {:else if activeIso !== 'GLOBAL'}
                <div class="hs-left">
                  <span class="hs-muted">{$dict.heritageUi.noLocalYet.replace('{country}', activeCountryLabel)}</span>
                </div>
              {:else}
                <div class="hs-left">
                  <span class="hs-muted">{$dict.doors.sampleHeading}</span>
                </div>
              {/if}
            </div>

            {#if doorHeritage && showingHeritage}
              {@const hTitle = doorHeritage.chipTitle[loc] ?? doorHeritage.chipTitle.en}
              {@const hId = `heritage-${doorHeritage.id}`}
              <article class="dp-focus-card is-heritage-focus">
                <div class="dp-focus-copy">
                  <div class="dp-wish-head">
                    <h3>{hTitle}</h3>
                    <span class="honesty-pill">{doorHeritage.honestyLabel}</span>
                    <span class="tradition-mini-pill">{doorHeritage.traditionLabel[loc] ?? doorHeritage.traditionLabel.en}</span>
                  </div>
                  <p class="dp-wish-beat">{doorHeritage.summary[loc] ?? doorHeritage.summary.en}</p>
                </div>
                <button
                  type="button"
                  class="dp-play-btn"
                  disabled={loadingHeritage}
                  onclick={() => launchHeritage(doorHeritage)}
                >
                  {completedIds[hId] ? `✓ ${$dict.player.playedBadge} · ` : ''}{$dict.player.playBtn}
                  <span class="arrow-flip" aria-hidden="true">&rarr;</span>
                </button>
              </article>
            {:else if INCLUDE_DEV_BREAKTHROUGHS && domainDevItems.length > 0}
              <div class="dp-wishes-grid">
                {#each domainDevItems as item}
                  <article class="dp-wish-card">
                    <div class="dp-wish-head">
                      <h4>{item.title[loc] ?? item.title.en}</h4>
                      <span class="honesty-pill">{item.honestyLabel}</span>
                    </div>
                    <p class="dp-wish-beat">{item.wobble.text[loc] ?? item.wobble.text.en}</p>
                    <button type="button" class="dp-play-btn" onclick={() => launchWish(item.id)}>
                      {completedIds[item.id] ? `✓ ${$dict.player.playedBadge} · ` : ''}{$dict.player.playBtn}
                      {#if SHOW_DRAFT_BADGE && item.status === 'draft'} (DRAFT){/if}
                      <span class="arrow-flip" aria-hidden="true">&rarr;</span>
                    </button>
                  </article>
                {/each}
              </div>
            {:else}
              {@const playableList = selectedDoor.wishes.filter((w) => 'id' in w && w.id && WISH_BY_ID.has(w.id))}
              {@const stubList = selectedDoor.wishes.filter((w) => !('id' in w && w.id && WISH_BY_ID.has(w.id)))}

              {#each playableList as wish}
                {@const playableObj = WISH_BY_ID.get(wish.id!)}
                {#if playableObj}
                  <article class="dp-focus-card">
                    <div class="dp-focus-copy">
                      <div class="dp-wish-head">
                        <h3>{wish.title}</h3>
                        <span class="honesty-pill" title={wish.honestyNote}>{wish.honesty}</span>
                      </div>
                      <p class="dp-wish-beat">{wish.beatSummary}</p>
                    </div>
                    <button
                      type="button"
                      class="dp-play-btn"
                      onclick={() => launchWish(playableObj.id)}
                    >
                      {completedIds[playableObj.id] ? `✓ ${$dict.player.playedBadge} · ` : ''}{$dict.player.playBtn}
                      {#if SHOW_DRAFT_BADGE && playableObj.status === 'draft'} (DRAFT){/if}
                      <span class="arrow-flip" aria-hidden="true">&rarr;</span>
                    </button>
                  </article>
                {/if}
              {/each}

              {#if stubList.length > 0}
                <p class="dp-upcoming-line">
                  Planned next: {stubList.map((s) => `${s.title} (${s.honesty})`).join(' · ')}
                </p>
              {/if}
            {/if}
          </div>
        {/if}
      </div>

      <!-- Compact Five Lights Progress Bar (Expands smoothly once player runs) -->
      <div id="five-lights" class="lights-inline-wrap">
        <TrailAndShadowCard compact={true} />
      </div>
    {/if}
  </div>
</section>

<style>
  .story-section {
    contain: layout style;
    padding: clamp(1.35rem, 3vw, 2.25rem) 0;
    scroll-margin-top: 90px;
  }

  .doors-section {
    background: var(--bg-surface-sunken);
    border-top: 1px solid var(--border-subtle);
    border-bottom: 1px solid var(--border-subtle);
    min-height: 410px;
  }

  .section-wrap {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 1.15rem;
  }

  .section-head {
    text-align: center;
    max-width: 680px;
    margin: 0 auto 1rem;
  }

  .sec-title {
    font-family: var(--font-family-sans);
    font-size: clamp(1.4rem, 2.8vw, 1.95rem);
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 0.35rem;
    line-height: 1.2;
    letter-spacing: -0.02em;
  }

  .sec-sub {
    font-size: 0.94rem;
    color: var(--text-secondary);
    margin: 0;
  }

  .doors-tabs {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.45rem;
    margin-bottom: 0.95rem;
  }

  .world-horizons-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 auto 0.75rem;
    padding: 0.36rem 0.65rem;
    border-radius: 12px;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
  }

  .wh-label {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--accent-primary);
    white-space: nowrap;
    flex-shrink: 0;
  }

  .wh-scroll {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    overflow-x: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
    padding: 2px 0;
    flex: 1 1 auto;
    min-width: 0;
  }

  .wh-scroll::-webkit-scrollbar {
    display: none;
  }

  .wh-chip {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-secondary);
    border-radius: 9999px;
    padding: 0.22rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 700;
    white-space: nowrap;
    cursor: pointer;
    flex-shrink: 0;
    min-height: 28px;
  }

  .wh-chip:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .wh-chip.active {
    background: var(--threat-sovereign-bg);
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .wh-all-link {
    font-size: 0.74rem;
    font-weight: 800;
    color: var(--accent-primary);
    text-decoration: none;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .wh-all-link:hover {
    text-decoration: underline;
  }

  .door-tab {
    display: inline-flex;
    align-items: center;
    gap: 0.42rem;
    min-height: 40px;
    padding: 0.42rem 0.85rem;
    border-radius: 9999px;
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-medium);
    color: var(--text-secondary);
    font-size: 0.84rem;
    font-weight: 700;
    cursor: pointer;
    transition: border-color 0.15s ease, background-color 0.15s ease, color 0.15s ease;
  }

  .door-tab:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .door-tab.selected {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .door-heritage-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--accent-primary);
    flex-shrink: 0;
  }

  .door-tab.selected .door-heritage-dot {
    background: #fef3c7;
  }

  .heritage-swap-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.4rem 0.65rem;
    min-height: 30px;
    margin-bottom: 0.65rem;
    padding: 0.35rem 0.65rem;
    border-radius: 9px;
    background: var(--bg-surface);
    border: 1px dashed var(--border-medium);
    font-size: 0.78rem;
  }

  .hs-left,
  .hs-actions {
    display: inline-flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.45rem;
  }

  .hs-pill {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .hs-era {
    font-size: 0.7rem;
    color: var(--text-muted);
    padding: 0.05rem 0.42rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
  }

  .hs-muted {
    color: var(--text-secondary);
  }

  .hs-archive-link {
    color: var(--accent-primary);
    font-weight: 700;
    text-decoration: none;
    font-size: 0.75rem;
  }

  .hs-archive-link:hover {
    text-decoration: underline;
  }

  .hs-toggle-btn {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    border-radius: 7px;
    padding: 0.2rem 0.55rem;
    font-size: 0.74rem;
    font-weight: 700;
    cursor: pointer;
    min-height: 28px;
  }

  .hs-toggle-btn.active,
  .hs-toggle-btn:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
  }

  .tradition-mini-pill {
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.14rem 0.5rem;
    border-radius: 6px;
    background: var(--bg-surface-sunken);
    color: var(--text-secondary);
  }

  .door-icon {
    width: 18px;
    height: 18px;
    display: inline-flex;
    flex-shrink: 0;
  }

  .door-icon svg {
    width: 100%;
    height: 100%;
  }

  .door-preview-panel {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    padding: 1.15rem 1.25rem;
    box-shadow: var(--shadow-sm);
  }

  .dp-header-line {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.35rem 0.75rem;
    margin-bottom: 0.75rem;
  }

  .dp-door-tag {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--accent-primary);
  }

  .dp-lead {
    font-size: 0.86rem;
    color: var(--text-secondary);
  }

  .dp-focus-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.85rem 1.25rem;
  }

  .dp-focus-copy {
    flex: 1 1 380px;
  }

  .dp-wish-head {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
  }

  .dp-wish-head h3,
  .dp-wish-head h4 {
    margin: 0;
    font-size: 1.08rem;
    font-weight: 800;
    color: var(--text-primary);
  }

  .honesty-pill {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.14rem 0.5rem;
    border-radius: 6px;
    background: var(--threat-sovereign-bg);
    color: var(--threat-sovereign);
    border: 1px solid var(--threat-sovereign-border);
  }

  .dp-wish-beat {
    margin: 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .dp-play-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    border: 0;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    border-radius: 10px;
    padding: 0.65rem 1.15rem;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    min-height: 44px;
    flex-shrink: 0;
  }

  .dp-play-btn:hover {
    background: var(--accent-primary-hover);
  }

  .dp-upcoming-line {
    margin: 0.65rem 0 0;
    font-size: 0.78rem;
    color: var(--text-muted);
  }

  .lights-inline-wrap {
    margin-top: 0.95rem;
  }

  .dp-wishes-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .dp-wish-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.9rem;
  }

  @media (max-width: 640px) {
    .doors-section {
      min-height: 450px;
    }
    .world-horizons-bar {
      flex-wrap: wrap;
      gap: 0.32rem 0.5rem;
    }
    .wh-label {
      order: 1;
    }
    .wh-all-link {
      order: 2;
      margin-inline-start: auto;
    }
    .wh-scroll {
      order: 3;
      flex: 1 0 100%;
    }
    .door-tab {
      flex: 1 1 calc(50% - 0.25rem);
      justify-content: center;
      font-size: 0.78rem;
      padding: 0.4rem 0.55rem;
    }
    .door-preview-panel {
      padding: 0.85rem;
    }
    .dp-focus-card {
      padding: 0.85rem;
    }
    .dp-play-btn {
      width: 100%;
      justify-content: center;
    }
    .dp-wishes-grid {
      grid-template-columns: 1fr;
    }
  }
</style>

