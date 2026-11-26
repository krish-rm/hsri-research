<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { dict, activeLocale } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';
  import { readinessStore } from '../lib/readinessState';
  import {
    CORE_BREAKTHROUGHS,
    loadAllBreakthroughs
  } from '../lib/breakthroughCatalog';

  const SHOW_DRAFT_BADGE = __HSRI_SHOW_DRAFTS__;
  const INCLUDE_DEV_BREAKTHROUGHS = __HSRI_INCLUDE_DEV15__;
  import WishPlayer, { type WishItem } from './WishPlayer.svelte';
  import TrailAndShadowCard from './TrailAndShadowCard.svelte';

  export let base = '';

  let catalog: WishItem[] = CORE_BREAKTHROUGHS;
  const FEATURED_IDS = ['sanjeevani', 'jarvis-for-my-life', 'prove-riemann-hypothesis'];

  let revealed = false;
  let activeDoorId = 'epic';
  let activeWishId: string | null = null;
  let playerAnchorEl: HTMLElement | null = null;

  onMount(async () => {
    revealed = true;
    if (INCLUDE_DEV_BREAKTHROUGHS) {
      catalog = await loadAllBreakthroughs();
    }
  });

  $: loc = ($activeLocale === 'es' || $activeLocale === 'ar' ? $activeLocale : 'en') as 'en' | 'es' | 'ar';
  $: PLAYABLE_WISHES = catalog;
  $: WISH_BY_ID = new Map(PLAYABLE_WISHES.map((w) => [w.id, w]));
  $: selectedDoor = $dict.doors.items.find((d) => d.id === activeDoorId) ?? $dict.doors.items[0];
  $: activeWish = activeWishId ? WISH_BY_ID.get(activeWishId) ?? null : null;
  $: completedIds = $readinessStore.wishes;
  $: domainDevItems = INCLUDE_DEV_BREAKTHROUGHS
    ? PLAYABLE_WISHES.filter((w) => w.door === selectedDoor.id)
    : [];

  function chooseDoor(id: string) {
    activeDoorId = id;
    activeWishId = null;
    trackEvent('door_preview_select', { door: id });
  }

  async function launchWish(wishId: string) {
    activeWishId = wishId;
    await tick();
    playerAnchorEl?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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

<!-- SECTION 3: FIVE DOMAINS -->
<section id="wish-doors" class="story-section doors-section">
  <div class="section-wrap">
    <div class="section-head">
      <h2 class="sec-title">{$dict.doors.heading}</h2>
      <p class="sec-sub">{$dict.doors.subhead}</p>
      <p class="sec-micro">{$dict.doors.microcopy}</p>
    </div>

    {#if revealed}
      <!-- Quick-Launch Bar for the 3 Core Flagship Breakthroughs (~60s) -->
      <div class="featured-bar" aria-label={$dict.player.featuredLabel}>
        <span class="featured-label">{$dict.player.featuredLabel}</span>
        <div class="featured-btns">
          {#each FEATURED_IDS as fId}
            {@const fw = WISH_BY_ID.get(fId)}
            {#if fw}
              <button
                type="button"
                class="featured-wish-btn"
                class:active={activeWishId === fw.id}
                onclick={() => launchWish(fw.id)}
              >
                <span class="fw-title">{fw.title[loc] ?? fw.title.en}</span>
                <span class="fw-meta">
                  {completedIds[fw.id] ? `✓ ${$dict.player.playedBadge}` : fw.honestyLabel}
                </span>
              </button>
            {/if}
          {/each}
        </div>
      </div>

      <div class="doors-grid" role="tablist" aria-label="Five breakthrough domains">
      {#each $dict.doors.items as door}
        <button
          type="button"
          role="tab"
          aria-selected={activeDoorId === door.id}
          class="door-card"
          class:selected={activeDoorId === door.id}
          onclick={() => chooseDoor(door.id)}
        >
          <div class="door-icon" aria-hidden="true">
            {#if door.icon === 'chalkboard'}
              <svg viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="4" y="6" width="28" height="20" rx="2" />
                <path d="M10 14h10M10 19h14M13 26l-2 5M23 26l2 5" stroke-linecap="round" />
              </svg>
            {:else if door.icon === 'pocket'}
              <svg viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 9h22v10a11 11 0 0 1-22 0V9z" />
                <circle cx="18" cy="18" r="4" stroke="var(--accent-primary)" />
              </svg>
            {:else if door.icon === 'eye'}
              <svg viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 18s5.5-8 14-8 14 8 14 8-5.5 8-14 8-14-8-14-8z" />
                <circle cx="18" cy="18" r="4.5" />
              </svg>
            {:else if door.icon === 'frame'}
              <svg viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="5" y="7" width="26" height="22" rx="2" />
                <path d="M10 7v22M26 7v22M15 14l7 4-7 4v-8z" stroke-linejoin="round" />
              </svg>
            {:else}
              <svg viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 24h12l-2 6h-8l-2-6z" />
                <path d="M18 6v4M10 10l2.5 2.5M26 10l-2.5 2.5" stroke-linecap="round" />
                <circle cx="18" cy="18" r="5" />
              </svg>
            {/if}
          </div>
          <h3 class="door-title">{door.title}</h3>
          <ul class="door-samples">
            {#each door.samples as s}
              <li>{s}</li>
            {/each}
          </ul>
          <span class="door-more">{door.moreCount}</span>
        </button>
      {/each}
    </div>

    <!-- Interactive Domain Preview or Active 4-Beat Breakthrough Player -->
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
          <div class="dp-top">
            <span class="dp-door-tag">{selectedDoor.title}</span>
            <span class="dp-phase-pill">{$dict.doors.phase2Badge}</span>
          </div>
          <p class="dp-lead">{selectedDoor.lead}</p>
          <div class="dp-wishes-grid">
            {#if INCLUDE_DEV_BREAKTHROUGHS && domainDevItems.length > 0}
              {#each domainDevItems as item}
                <article class="dp-wish-card">
                  <div class="dp-wish-head">
                    <h4>{item.title[loc] ?? item.title.en}</h4>
                    <span class="honesty-pill" title={item.honestyNote[loc] ?? item.honestyNote.en}>{item.honestyLabel}</span>
                  </div>
                  <p class="dp-wish-honesty-note">{item.honestyNote[loc] ?? item.honestyNote.en}</p>
                  <p class="dp-wish-beat">{item.wobble.text[loc] ?? item.wobble.text.en}</p>
                  <button
                    type="button"
                    class="dp-play-btn"
                    onclick={() => launchWish(item.id)}
                  >
                    {completedIds[item.id] ? `✓ ${$dict.player.playedBadge} · ` : ''}{$dict.player.playBtn}
                    {#if SHOW_DRAFT_BADGE && item.status === 'draft'} (DRAFT){/if}
                    <span class="arrow-flip" aria-hidden="true">&rarr;</span>
                  </button>
                </article>
              {/each}
            {:else}
              {#each selectedDoor.wishes as wish}
                {@const playableObj = 'id' in wish && wish.id ? WISH_BY_ID.get(wish.id) : null}
                <article class="dp-wish-card">
                  <div class="dp-wish-head">
                    <h4>{wish.title}</h4>
                    <span class="honesty-pill" title={wish.honestyNote}>{wish.honesty}</span>
                  </div>
                  <p class="dp-wish-honesty-note">{wish.honestyNote}</p>
                  <p class="dp-wish-beat">{wish.beatSummary}</p>
                  {#if playableObj}
                    <button
                      type="button"
                      class="dp-play-btn"
                      onclick={() => launchWish(playableObj.id)}
                    >
                      {completedIds[playableObj.id] ? `✓ ${$dict.player.playedBadge} · ` : ''}{$dict.player.playBtn}
                      {#if SHOW_DRAFT_BADGE && playableObj.status === 'draft'} (DRAFT){/if}
                      <span class="arrow-flip" aria-hidden="true">&rarr;</span>
                    </button>
                  {:else}
                    <span class="dp-soon-note">{$dict.player.previewOnlyNote}</span>
                  {/if}
                </article>
              {/each}
            {/if}
          </div>
        </div>
      {/if}
    </div>
    {/if}
  </div>
</section>

<!-- SECTION 4: HOW A BREAKTHROUGH WORKS -->
<section id="how-it-works" class="story-section alt-surface how-section">
  <div class="section-wrap">
    <div class="section-head">
      <h2 class="sec-title">{$dict.beats.heading}</h2>
    </div>

    {#if revealed}
      <div class="beats-grid">
        {#each $dict.beats.items as beat, idx}
          <div class="beat-card">
            <div class="beat-num">0{idx + 1}</div>
            <h3 class="beat-name">{beat.key}</h3>
            <p class="beat-desc">{beat.desc}</p>
          </div>
        {/each}
      </div>

      <p class="beats-footer-line">{$dict.beats.footerLine}</p>
    {/if}
  </div>
</section>

<!-- SECTION 5: YOUR FIVE LIGHTS -->
<section id="five-lights" class="story-section lights-section">
  <div class="section-wrap">
    <div class="section-head">
      <h2 class="sec-title">{$dict.lights.heading}</h2>
    </div>

    {#if revealed}
      <TrailAndShadowCard />
    {/if}
  </div>
</section>

<style>
  .story-section {
    contain: layout style;
    padding: clamp(2.25rem, 4.5vw, 3.75rem) 0;
    scroll-margin-top: 112px;
  }

  .doors-section {
    min-height: 755px;
  }

  .how-section {
    min-height: 362px;
  }

  .lights-section {
    min-height: 408px;
  }

  .alt-surface {
    background: var(--bg-surface-sunken);
    border-top: 1px solid var(--border-subtle);
    border-bottom: 1px solid var(--border-subtle);
  }

  .section-wrap {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 1.15rem;
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
    font-size: clamp(0.98rem, 1.5vw, 1.1rem);
    color: var(--text-secondary);
    margin: 0 0 0.45rem;
    line-height: 1.6;
  }

  .sec-micro {
    font-family: var(--font-family-mono);
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--accent-primary);
    margin: 0;
  }

  .doors-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.85rem;
    margin-bottom: 1.25rem;
  }

  .door-card {
    text-align: start;
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.1rem 1rem;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
    transition: border-color 0.16s ease, transform 0.16s ease, box-shadow 0.16s ease;
  }

  .door-card:hover {
    border-color: var(--accent-primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
  }

  .door-card.selected {
    border-color: var(--accent-primary);
    background: var(--bg-surface);
    box-shadow: var(--shadow-md);
  }

  .door-icon {
    width: 34px;
    height: 34px;
    color: var(--accent-primary);
  }

  .door-title {
    margin: 0;
    font-size: 1.02rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.25;
  }

  .door-samples {
    margin: 0;
    padding-inline-start: 1.05rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.45;
  }

  .door-more {
    margin-top: auto;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-secondary);
  }

  .door-preview-panel {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    padding: 1.25rem 1.35rem;
    box-shadow: var(--shadow-sm);
  }

  .dp-top {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .dp-door-tag {
    font-family: var(--font-family-mono);
    font-size: 0.76rem;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--accent-primary);
  }

  .dp-phase-pill {
    font-size: 0.74rem;
    padding: 0.22rem 0.65rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    color: var(--text-secondary);
    border: 1px solid var(--border-subtle);
  }

  .dp-lead {
    font-size: 0.94rem;
    color: var(--text-secondary);
    margin: 0 0 1rem;
  }

  .dp-wishes-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.9rem;
  }

  .dp-wish-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem;
  }

  .dp-wish-head {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: baseline;
    gap: 0.4rem;
    margin-bottom: 0.4rem;
  }

  .dp-wish-head h4 {
    margin: 0;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .honesty-pill {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.16rem 0.5rem;
    border-radius: 6px;
    background: var(--threat-sovereign-bg);
    color: var(--threat-sovereign);
    border: 1px solid var(--threat-sovereign-border);
  }

  .dp-wish-honesty-note {
    font-size: 0.79rem;
    color: var(--text-secondary);
    margin: 0 0 0.45rem;
    line-height: 1.45;
  }

  .dp-wish-beat {
    font-size: 0.88rem;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.5;
  }

  .beats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.9rem;
    margin-bottom: 1.5rem;
  }

  .beat-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1.25rem 1.1rem;
  }

  .beat-num {
    font-family: var(--font-family-mono);
    font-size: 0.76rem;
    font-weight: 800;
    color: var(--accent-primary);
    margin-bottom: 0.35rem;
  }

  .beat-name {
    font-family: var(--font-family-display);
    font-size: 1.15rem;
    margin: 0 0 0.35rem;
    color: var(--text-primary);
  }

  .beat-desc {
    margin: 0;
    font-size: 0.92rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .beats-footer-line {
    text-align: center;
    font-family: var(--font-family-sans);
    font-size: 1.12rem;
    font-weight: 800;
    line-height: 1.35;
    color: var(--accent-primary);
    margin: 0;
  }

  .featured-bar {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 0.85rem 1rem;
    margin-bottom: 1.1rem;
  }

  .featured-label {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    color: var(--accent-primary);
    margin-bottom: 0.55rem;
  }

  .featured-btns {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.55rem;
  }

  .featured-wish-btn {
    text-align: start;
    border: 1.5px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    border-radius: 10px;
    padding: 0.55rem 0.75rem;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    min-height: 48px;
  }

  .featured-wish-btn:hover,
  .featured-wish-btn.active {
    border-color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
  }

  .fw-title {
    font-size: 0.88rem;
    font-weight: 700;
  }

  .fw-meta {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    color: var(--accent-primary);
  }

  .dp-play-btn {
    margin-top: 0.75rem;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    border: 0;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    border-radius: 8px;
    padding: 0.45rem 0.85rem;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    min-height: 36px;
  }

  .dp-soon-note {
    display: inline-block;
    margin-top: 0.75rem;
    font-size: 0.76rem;
    color: var(--text-secondary);
    font-style: italic;
  }

  @media (max-width: 1024px) {
    .doors-section {
      min-height: 1766px;
    }
    .how-section {
      min-height: 731px;
    }
    .lights-section {
      min-height: 693px;
    }
    .doors-grid,
    .featured-btns {
      grid-template-columns: repeat(2, 1fr);
    }
    .beats-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 640px) {
    .doors-section {
      min-height: 1761px;
    }
    .how-section {
      min-height: 760px;
    }
    .lights-section {
      min-height: 717px;
    }
    .doors-grid,
    .featured-btns,
    .dp-wishes-grid,
    .beats-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
