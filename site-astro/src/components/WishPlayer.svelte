<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { dict, activeLocale, storyOverlay, getCountryDisplayName } from '../i18n/store';
  import { pickHonestyScale, pickLightLabel, resolvePlayableWishCopy } from '../i18n/storyTypes';
  import WishSceneIllustration from './WishSceneIllustration.svelte';
  import TotoIllustration from './TotoIllustration.svelte';
  import WobbleReadout from './WobbleReadout.svelte';
  import {
    readinessStore,
    recordWishCompletion,
    hasSeenTotoIntro,
    markTotoIntroSeen,
    type LightKey,
    type ShadowKey
  } from '../lib/readinessState';
  import { countryContextStore, focusSafeguardInCountryCheck } from '../lib/countryContext';
  import { trackEvent } from '../lib/privacyStorage';
  import type { PlayableHeritageWish } from '../lib/heritageTypes';

  const SHOW_DRAFT_BADGE = __HSRI_SHOW_DRAFTS__;

  type LangCode = 'en' | 'es' | 'ar';
  type LText = { en: string; es: string; ar: string };

  export interface WishItem {
    id: string;
    door: string;
    order: number;
    icon: string;
    status: 'draft' | 'owner_approved';
    devOnly: boolean;
    title: LText;
    doorTitle: LText;
    honestyLabel: 'Imagination' | 'Possible soon' | 'Real today';
    honestyNote: LText;
    verbatimFromBrief: boolean;
    shadowTag: ShadowKey;
    atlasRefs: string[];
    wonder: { text: LText; totoLine: LText; transcript: LText; draft: boolean };
    wobble: { text: LText; transcript: LText; draft: boolean };
    weight: {
      question: LText;
      transcript: LText;
      draft: boolean;
      options: Array<{ id: 'a' | 'b' | 'c'; text: LText; light: LightKey; shadow: ShadowKey }>;
    };
    way: {
      text: LText;
      actionCardTitle: LText;
      actionCardStep: LText;
      pledgeLabel: LText;
      transcript: LText;
      draft: boolean;
    };
    closingLine: string;
    realityMeter: {
      scale: 'Imagination' | 'Possible soon' | 'Real today';
      reason: LText;
      observedMetric?: { value: string; label: LText; directCapabilityMatch: true } | null;
      source: string;
      sourceUrl: string;
      lastReviewed: string;
    };
  }

  export let wish: WishItem | PlayableHeritageWish;
  export let base = '';
  export let onClose: () => void = () => {};
  export let onNextWish: () => void = () => {};

  $: heritageWish = ('isHeritage' in wish && wish.isHeritage ? wish : null) as PlayableHeritageWish | null;
  $: ctxCountryIso =
    $countryContextStore.iso && $countryContextStore.iso !== 'GLOBAL'
      ? $countryContextStore.iso
      : countryRef?.iso ?? 'GLOBAL';
  $: ctxCountryName =
    $countryContextStore.iso && $countryContextStore.iso !== 'GLOBAL'
      ? getCountryDisplayName($countryContextStore.iso, $countryContextStore.countryName, $activeLocale)
      : countryRef
        ? getCountryDisplayName(countryRef.iso, countryRef.name, $activeLocale)
        : $dict.hero.cityNeutralName;

  let showIntro = false;
  let introStartBtnEl: HTMLButtonElement | null = null;
  let beat: 'wonder' | 'wobble' | 'weight' | 'way' = 'wonder';
  let startedAt = Date.now();
  let guessedWobble = false;
  let foresightPicked: number | null = null;
  let selectedWeight: 'a' | 'b' | 'c' | null = null;
  let pledged = false;
  let lastSavedKey = '';
  let playerHeadingEl: HTMLHeadingElement | null = null;

  $: wishCopy = resolvePlayableWishCopy(wish, $activeLocale, $storyOverlay);
  $: chosenOpt = wish.weight.options.find((o) => o.id === selectedWeight) ?? null;
  $: countryRef = $readinessStore.selectedCountry;
  $: scaleIdx =
    wish.realityMeter.scale === 'Real today' ? 2 : wish.realityMeter.scale === 'Possible soon' ? 1 : 0;

  onMount(async () => {
    startedAt = Date.now();
    trackEvent('breakthrough_started', { breakthrough: wish.id });
    showIntro = !hasSeenTotoIntro();
    await tick();
    if (showIntro) {
      introStartBtnEl?.focus({ preventScroll: true });
    } else {
      playerHeadingEl?.focus({ preventScroll: true });
    }
  });

  async function dismissIntro(method: 'begin' | 'skip') {
    markTotoIntroSeen(method);
    showIntro = false;
    await tick();
    playerHeadingEl?.focus({ preventScroll: true });
  }

  function chooseForesight(idx: number) {
    foresightPicked = idx;
    const isRealGuess = idx < 3;
    guessedWobble = isRealGuess;
    if (isRealGuess) trackEvent('foresight_guess', { breakthrough: wish.id, choice: idx });
    beat = 'wobble';
  }

  function chooseWeight(optId: 'a' | 'b' | 'c') {
    selectedWeight = optId;
    const opt = wish.weight.options.find((o) => o.id === optId);
    if (opt) {
      trackEvent('weight_choice', { breakthrough: wish.id, choice: optId, light: opt.light, shadow: opt.shadow });
    }
    beat = 'way';
    saveCompletion(pledged);
  }

  function togglePledge() {
    pledged = !pledged;
    if (pledged) trackEvent('way_pledge', { breakthrough: wish.id });
    saveCompletion(pledged);
  }

  function saveCompletion(isPledged: boolean) {
    const opt = chosenOpt ?? wish.weight.options[0];
    if (!opt) return;
    const key = `${wish.id}:${opt.id}:${isPledged}`;
    if (key === lastSavedKey) return;
    lastSavedKey = key;
    const sec = Math.max(1, Math.round((Date.now() - startedAt) / 1000));
    recordWishCompletion({
      wishId: wish.id,
      wishTitle: wishCopy.title,
      guessedWobble,
      weightChoiceId: opt.id,
      weightLight: opt.light,
      weightShadow: opt.shadow,
      pledged: isPledged,
      durationSec: sec,
      completedAt: new Date().toISOString()
    });
  }
</script>

<svelte:window
  on:keydown={(e) => {
    if (showIntro && e.key === 'Escape') {
      e.preventDefault();
      dismissIntro('skip');
    }
  }}
/>

<article class="wish-player-shell" aria-label={wishCopy.title}>
  <header class="wp-head">
    <div>
      <div class="wp-badges">
        <span class="wp-door">{wishCopy.doorTitle}</span>
        <span class="wp-honesty">{$dict.player.honestyPrefix} {pickHonestyScale(wish.honestyLabel, $dict)}</span>
        <span class="wp-dur">{$dict.player.durationBadge}</span>
        {#if heritageWish}
          <span class="wp-heritage-pill">{wishCopy.traditionLabel}</span>
          <a href={`${base}/traditions/${heritageWish.slug}/`} class="wp-archive-link">
            {$dict.heritageUi.readArchiveLink} &rarr;
          </a>
        {:else if SHOW_DRAFT_BADGE && wish.status === 'draft'}
          <span class="draft-pill wp-draft-tag">{$dict.player.draftTag}</span>
        {/if}
      </div>
      <h3 class="wp-title" tabindex="-1" bind:this={playerHeadingEl}>{wishCopy.title}</h3>
      <p class="wp-honesty-note">{wishCopy.honestyNote}</p>
    </div>
    <button type="button" class="wp-back-btn" on:click={onClose}>
      &larr; {$dict.player.backToDoors}
    </button>
  </header>

  {#if showIntro}
    <div class="toto-intro-panel" role="region" aria-label={$dict.totoIntro.ariaLabel}>
      <div class="toto-intro-top">
        <span class="toto-intro-badge">{$dict.totoIntro.badge}</span>
        <button type="button" class="toto-skip-btn" on:click={() => dismissIntro('skip')}>
          {$dict.totoIntro.skipBtn}
        </button>
      </div>

      <div class="toto-intro-body">
        <div class="toto-intro-orb">
          <TotoIllustration pose="curious" size={88} label={$dict.totoIntro.svgAlt} />
        </div>
        <div class="toto-intro-lines">
          {#each $dict.totoIntro.lines as line, idx}
            <p class={idx === 0 ? 'ti-lead' : 'ti-text'}>{line}</p>
          {/each}
        </div>
      </div>

      <div class="toto-intro-actions">
        <button
          type="button"
          class="btn-advance"
          bind:this={introStartBtnEl}
          on:click={() => dismissIntro('begin')}
        >
          {$dict.totoIntro.startBtn} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
        </button>
        <p class="ti-footnote">{$dict.totoIntro.footnote}</p>
      </div>
    </div>
  {:else}
  <!-- 4-Beat Progress Tabs -->
  <nav class="beat-steps" aria-label="Breakthrough story progression">
    {#each ['wonder', 'wobble', 'weight', 'way'] as b, idx}
      {@const isEnabled =
        b === 'wonder' ||
        b === 'wobble' ||
        (b === 'weight' && (beat === 'weight' || beat === 'way' || selectedWeight !== null)) ||
        (b === 'way' && (beat === 'way' || selectedWeight !== null))}
      <button
        type="button"
        class="beat-tab"
        class:active={beat === b}
        disabled={!isEnabled}
        on:click={() => {
          if (isEnabled) beat = b as 'wonder' | 'wobble' | 'weight' | 'way';
        }}
      >
        {$dict.player.stepLabels[idx]}
      </button>
    {/each}
  </nav>

  <!-- Beat Content -->
  <div class="beat-stage" aria-live="polite">
    {#if beat === 'wonder'}
      <WishSceneIllustration
        wishId={wish.id}
        door={wish.door}
        beat="wonder"
        transcript={wishCopy.wonder.transcript}
      />
      {@const rawToto = wishCopy.wonder.totoLine.replace(/^(?:Toto|توتو|토토|トト|টোটো|टोटो|托托|多多)\s*[:：]\s*/i, '').trim()}
      <div class="toto-beat-bar">
        <TotoIllustration pose="calm" size={44} label={$dict.totoPage.poses[0].alt} />
        <p class="toto-speech">
          <strong class="toto-speaker">{$dict.totoBeats.speaker}:</strong> {$dict.totoBeats.wonder}
          {#if rawToto && rawToto.toLowerCase() !== $dict.totoBeats.wonder.toLowerCase()}
            <span class="toto-detail">&middot; {rawToto}</span>
          {/if}
        </p>
      </div>
      <p class="beat-main-text">{wishCopy.wonder.text}</p>

      <!-- Optional Foresight Prediction (Pre-Wobble) -->
      <div class="foresight-prompt">
        <p class="fp-lead">{$dict.player.foresightLead}</p>
        <p class="fp-q">{$dict.player.foresightQuestion}</p>
        <div class="fp-opts">
          {#each $dict.player.foresightOptions as optLabel, idx}
            <button
              type="button"
              class={idx === 3 ? 'btn-skip-wobble' : 'btn-foresight-opt'}
              class:picked={foresightPicked === idx}
              on:click={() => chooseForesight(idx)}
            >
              {optLabel}
            </button>
          {/each}
        </div>
      </div>
    {:else if beat === 'wobble'}
      <WishSceneIllustration
        wishId={wish.id}
        door={wish.door}
        beat="wobble"
        transcript={wishCopy.wobble.transcript}
      />
      <div class="toto-beat-bar is-wobble">
        <TotoIllustration pose="apologetic" size={44} label={$dict.totoPage.poses[2].alt} />
        <p class="toto-speech">
          <strong class="toto-speaker">{$dict.totoBeats.speaker}:</strong> {$dict.totoBeats.wobble}
        </p>
      </div>
      {#if SHOW_DRAFT_BADGE && (wish.wobble.draft || wish.status === 'draft')}
        <span class="draft-pill">{$dict.player.draftTag}</span>
      {/if}
      <p class="beat-main-text">{wishCopy.wobble.text}</p>
      <button type="button" class="btn-advance" on:click={() => (beat = 'weight')}>
        {$dict.player.toWeightBtn} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
      </button>
    {:else if beat === 'weight'}
      <WishSceneIllustration
        wishId={wish.id}
        door={wish.door}
        beat="weight"
        transcript={wishCopy.weight.transcript}
      />
      <div class="toto-beat-bar">
        <TotoIllustration pose="curious" size={44} label={$dict.totoPage.poses[1].alt} />
        <p class="toto-speech">
          <strong class="toto-speaker">{$dict.totoBeats.speaker}:</strong> {$dict.totoBeats.weight}
        </p>
      </div>
      {#if SHOW_DRAFT_BADGE && (wish.weight.draft || wish.status === 'draft')}
        <span class="draft-pill">{$dict.player.draftTag}</span>
      {/if}
      <p class="beat-main-text weight-q">{wishCopy.weight.question}</p>
      {#if heritageWish}
        <WobbleReadout
          countryIso={ctxCountryIso}
          countryName={ctxCountryName}
          binding={heritageWish.binding}
          dependencyText={wishCopy.dependencyLabel}
          base={base}
        />
      {/if}
      <p class="weight-lead">{$dict.player.weightLead}</p>

      <div class="weight-options">
        {#each wish.weight.options as opt}
          <button
            type="button"
            class="weight-choice-btn"
            class:selected={selectedWeight === opt.id}
            on:click={() => chooseWeight(opt.id)}
          >
            <span class="wc-key">({opt.id})</span>
            <span class="wc-text">{wishCopy.weight.optionText(opt.id, opt.text)}</span>
            <span class="wc-meta">{pickLightLabel(opt.light, $dict)} · {$dict.player.shadows[opt.shadow]}</span>
          </button>
        {/each}
      </div>
    {:else}
      <WishSceneIllustration
        wishId={wish.id}
        door={wish.door}
        beat="way"
        transcript={wishCopy.way.transcript}
      />
      <div class="toto-beat-bar">
        <TotoIllustration pose="calm" size={44} label={$dict.totoPage.poses[0].alt} />
        <p class="toto-speech">
          <strong class="toto-speaker">{$dict.totoBeats.speaker}:</strong> {$dict.totoBeats.way}
        </p>
      </div>
      <p class="beat-main-text">{wishCopy.way.text}</p>

      <div class="way-action-box">
        <span class="way-box-tag">{$dict.player.wayActionTitle}</span>
        <h4>{wishCopy.way.actionCardTitle}</h4>
        <p>{wishCopy.way.actionCardStep}</p>
        <button type="button" class="btn-pledge" class:pledged={pledged} on:click={togglePledge}>
          {pledged ? `✓ ${$dict.player.pledgeDone}` : $dict.player.pledgeBtn}
        </button>
      </div>

      <!-- 3-Step Reality Meter + One-Line Reason, Cited Source & Last Reviewed Date -->
      <div class="reality-grid">
        <div class="reality-card">
          <div class="rc-top">
            <span class="rc-tag">{$dict.player.realityTitle}</span>
            <span class="rc-date">{$dict.player.realityReviewed}: {wish.realityMeter.lastReviewed}</span>
          </div>
          <ol class="rm-scale-steps" aria-label={$dict.player.realityTitle}>
            <li class="rm-step" class:active={scaleIdx === 0}>
              <span class="rm-dot" aria-hidden="true"></span>
              <span>{$dict.player.realityScales.imagination}</span>
            </li>
            <li class="rm-step" class:active={scaleIdx === 1}>
              <span class="rm-dot" aria-hidden="true"></span>
              <span>{$dict.player.realityScales.possibleSoon}</span>
            </li>
            <li class="rm-step" class:active={scaleIdx === 2}>
              <span class="rm-dot" aria-hidden="true"></span>
              <span>{$dict.player.realityScales.realToday}</span>
            </li>
          </ol>
          <p class="rm-note">{wishCopy.realityReason}</p>
          {#if wish.realityMeter.observedMetric?.directCapabilityMatch}
            <p class="rm-direct-metric">
              <strong>{wish.realityMeter.observedMetric.value}</strong> — {wishCopy.metricLabel}
            </p>
          {/if}
          <p class="rm-source">
            {$dict.player.realitySource}:
            {#if wish.realityMeter.sourceUrl.startsWith('/')}
              <a href={`${base}${wish.realityMeter.sourceUrl}`}>{wish.realityMeter.source}</a>
            {:else}
              <a href={wish.realityMeter.sourceUrl} target="_blank" rel="noopener noreferrer">{wish.realityMeter.source}</a>
            {/if}
          </p>
        </div>

        <div class="atlas-card">
          <span class="rc-tag">{$dict.player.shadowTitle}</span>
          <div class="atlas-pills">
            {#each wish.atlasRefs as scId}
              <a href={`${base}/scenarios/`} class="atlas-pill">{scId} &rarr;</a>
            {/each}
          </div>
          <div class="country-hook-box">
            <strong>{$dict.player.countryHookPrefix}</strong>
            {#if heritageWish}
              {@const ctaCountryIso = ctxCountryIso !== 'GLOBAL' ? ctxCountryIso : (heritageWish.countries[0] ?? 'NOR')}
              {@const ctaCountryLabel = ctxCountryIso !== 'GLOBAL' ? ctxCountryName : getCountryDisplayName(ctaCountryIso, ctaCountryIso, $activeLocale)}
              <p>
                <button
                  type="button"
                  class="btn-country-test"
                  on:click={() => focusSafeguardInCountryCheck(ctaCountryIso, heritageWish.binding.safeguardChecklistIdx)}
                >
                  {$dict.heritageUi.wayTestCountryCta.replace('{country}', ctaCountryLabel)} &rarr;
                </button>
              </p>
              <p class="heritage-review-note">
                {$dict.heritageUi.reviewOpenNote} &middot;
                <a href={`${base}/traditions/${heritageWish.slug}/`}>{$dict.heritageUi.readArchiveLink}</a>
              </p>
            {:else if countryRef && countryRef.kind === 'rated'}
              <p>
                {$dict.country.countryHookTpl
                  .replace('{title}', wishCopy.title)
                  .replace('{country}', getCountryDisplayName(countryRef.iso, countryRef.name, $activeLocale))
                  .replace('{count}', String(countryRef.checklistCount))}
              </p>
            {:else}
              <p><a href="#country-check">{$dict.player.countryHookUnset}</a></p>
            {/if}
          </div>
        </div>
      </div>

      <div class="wish-finale">
        <p class="closing-line">{$dict.totoBeats.close}</p>
        <div class="finale-actions">
          <button type="button" class="btn-advance" on:click={onNextWish}>
            {$dict.player.nextWishBtn} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
          </button>
          <a href="#five-lights" class="btn-lights-jump">{$dict.lights.heading} &darr;</a>
        </div>
      </div>
    {/if}
  </div>
  {/if}
</article>

<style>
  .wish-player-shell {
    background: var(--bg-surface-elevated);
    border: 2px solid var(--accent-primary);
    border-radius: 16px;
    padding: 1.35rem;
    box-shadow: var(--shadow-md);
  }

  .wp-head {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.75rem 1rem;
    margin-bottom: 1rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--border-subtle);
  }

  .wp-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.45rem;
  }

  .wp-door,
  .wp-honesty,
  .wp-dur {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.18rem 0.55rem;
    border-radius: 9999px;
  }

  .wp-door {
    background: var(--threat-sovereign-bg);
    color: var(--accent-primary);
    border: 1px solid var(--threat-sovereign-border);
  }

  .wp-honesty {
    background: var(--bg-surface-sunken);
    color: var(--text-primary);
    border: 1px solid var(--border-medium);
  }

  .wp-dur {
    background: var(--bg-surface);
    color: var(--text-secondary);
    border: 1px solid var(--border-subtle);
  }

  .wp-title {
    margin: 0 0 0.3rem;
    font-size: clamp(1.25rem, 2.5vw, 1.65rem);
    color: var(--text-primary);
  }

  .wp-title:focus,
  .wp-title:focus-visible {
    outline: none;
  }

  .wp-honesty-note {
    margin: 0;
    font-size: 0.82rem;
    color: var(--text-secondary);
  }

  .wp-back-btn {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    border-radius: 9px;
    padding: 0.42rem 0.85rem;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    min-height: 36px;
  }

  .beat-steps {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.45rem;
    margin-bottom: 1rem;
  }

  .beat-tab {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-secondary);
    border-radius: 10px;
    padding: 0.45rem 0.5rem;
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 700;
    cursor: pointer;
  }

  .beat-tab.active {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .beat-tab:disabled {
    opacity: 0.48;
    cursor: not-allowed;
  }

  .toto-intro-panel {
    background: var(--bg-surface);
    border: 1.5px solid var(--border-medium);
    border-radius: 14px;
    padding: 1.15rem 1.25rem;
    margin-bottom: 0.5rem;
  }

  .toto-intro-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.9rem;
  }

  .toto-intro-badge {
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
    padding: 0.2rem 0.65rem;
    border-radius: 9999px;
  }

  .toto-skip-btn {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    border-radius: 8px;
    padding: 0.35rem 0.75rem;
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
    min-height: 36px;
  }

  .toto-skip-btn:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .toto-intro-body {
    display: flex;
    align-items: center;
    gap: 1.15rem;
    margin-bottom: 1rem;
  }

  .toto-intro-orb {
    flex-shrink: 0;
  }

  .ti-lead {
    margin: 0 0 0.45rem;
    font-size: 1.16rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .ti-text {
    margin: 0 0 0.4rem;
    font-size: 0.95rem;
    line-height: 1.55;
    color: var(--text-primary);
  }

  .toto-intro-actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.65rem 1rem;
  }

  .ti-footnote {
    margin: 0;
    font-size: 0.74rem;
    color: var(--text-secondary);
  }

  .toto-beat-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
    border-radius: 12px;
    padding: 0.5rem 0.85rem;
    margin-bottom: 0.75rem;
  }

  .toto-beat-bar.is-wobble {
    background: var(--threat-warning-bg);
    border-color: var(--threat-warning-border);
  }

  .toto-speech {
    margin: 0;
    font-size: 0.9rem;
    line-height: 1.45;
    color: var(--text-primary);
  }

  .toto-speaker {
    color: var(--accent-primary);
    font-weight: 800;
  }

  .toto-detail {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-inline-start: 0.35rem;
  }

  :global([dir='rtl']) .wp-door,
  :global([dir='rtl']) .wp-honesty,
  :global([dir='rtl']) .wp-dur,
  :global([dir='rtl']) .beat-tab,
  :global([dir='rtl']) .draft-pill,
  :global([dir='rtl']) .toto-intro-badge,
  :global([dir='rtl']) .way-box-tag {
    font-family: var(--font-family-sans);
    letter-spacing: 0;
  }

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  .draft-pill {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    color: var(--threat-warning);
    background: var(--threat-warning-bg);
    border: 1px solid var(--threat-warning-border);
    border-radius: 9999px;
    padding: 0.16rem 0.55rem;
    margin-bottom: 0.5rem;
  }

  .beat-main-text {
    font-size: clamp(1.02rem, 1.8vw, 1.18rem);
    line-height: 1.6;
    color: var(--text-primary);
    font-weight: 600;
    margin: 0 0 1rem;
  }

  .foresight-prompt {
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 0.95rem 1rem;
  }

  .fp-lead {
    margin: 0 0 0.25rem;
    font-size: 0.76rem;
    color: var(--accent-primary);
    font-weight: 700;
  }

  .fp-q {
    margin: 0 0 0.7rem;
    font-size: 0.94rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .fp-opts {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }

  .btn-foresight-opt,
  .btn-skip-wobble {
    text-align: start;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    border-radius: 10px;
    padding: 0.55rem 0.8rem;
    font-size: 0.84rem;
    font-weight: 600;
    cursor: pointer;
    min-height: 44px;
  }

  .btn-foresight-opt:hover,
  .btn-foresight-opt.picked {
    border-color: var(--accent-primary);
    background: var(--bg-surface);
  }

  .btn-skip-wobble {
    border-style: dashed;
    color: var(--accent-primary);
    font-weight: 700;
  }

  .weight-lead {
    margin: 0 0 0.65rem;
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text-secondary);
  }

  .weight-options {
    display: grid;
    gap: 0.6rem;
  }

  .weight-choice-btn {
    text-align: start;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.2rem 0.65rem;
    align-items: baseline;
    border: 1.5px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    border-radius: 12px;
    padding: 0.75rem 0.95rem;
    cursor: pointer;
    min-height: 48px;
  }

  .weight-choice-btn:hover,
  .weight-choice-btn.selected {
    border-color: var(--accent-primary);
    background: var(--bg-surface-elevated);
  }

  .wc-key {
    font-family: var(--font-family-mono);
    font-weight: 800;
    color: var(--accent-primary);
  }

  .wc-text {
    font-size: 0.94rem;
    font-weight: 700;
  }

  .wc-meta {
    grid-column: 2;
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    color: var(--text-secondary);
  }

  .way-action-box {
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
  }

  .way-box-tag {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    color: var(--threat-sovereign);
    margin-bottom: 0.3rem;
  }

  .way-action-box h4 {
    margin: 0 0 0.3rem;
    font-size: 1rem;
    color: var(--text-primary);
  }

  .way-action-box p {
    margin: 0 0 0.75rem;
    font-size: 0.86rem;
    color: var(--text-secondary);
  }

  .btn-pledge {
    border: 1.5px solid var(--accent-primary);
    background: var(--bg-surface-elevated);
    color: var(--accent-primary);
    border-radius: 9px;
    padding: 0.5rem 0.95rem;
    font-weight: 700;
    font-size: 0.84rem;
    cursor: pointer;
    min-height: 42px;
  }

  .btn-pledge.pledged {
    background: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .reality-grid {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 0.85rem;
    margin-bottom: 1rem;
  }

  .reality-card,
  .atlas-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.9rem;
  }

  .rc-top {
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.45rem;
  }

  .rc-tag,
  .rc-date {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--text-secondary);
  }

  .wp-draft-tag {
    margin-bottom: 0;
  }

  .rm-scale-steps {
    list-style: none;
    margin: 0 0 0.65rem;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.35rem;
  }

  .rm-step {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.34rem 0.5rem;
    border-radius: 8px;
    border: 1px solid var(--border-subtle);
    background: var(--bg-surface-sunken);
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .rm-step.active {
    background: var(--threat-sovereign-bg);
    border-color: var(--accent-primary);
    color: var(--accent-primary);
    font-weight: 800;
  }

  .rm-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
    background: var(--border-medium);
  }

  .rm-step.active .rm-dot {
    background: var(--accent-primary);
  }

  .rm-direct-metric {
    margin: 0 0 0.3rem;
    font-size: 0.78rem;
    color: var(--accent-primary);
  }

  .rm-note,
  .rm-source {
    margin: 0 0 0.25rem;
    font-size: 0.78rem;
    color: var(--text-secondary);
    line-height: 1.45;
  }

  .rm-source a,
  .country-hook-box a {
    color: var(--accent-primary);
    font-weight: 600;
  }

  .atlas-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin: 0.45rem 0 0.75rem;
  }

  .atlas-pill {
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 700;
    padding: 0.28rem 0.6rem;
    border-radius: 8px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-medium);
    color: var(--accent-primary);
    text-decoration: none;
  }

  .country-hook-box {
    font-size: 0.8rem;
    color: var(--text-secondary);
  }

  .country-hook-box p {
    margin: 0.25rem 0 0;
  }

  .wp-heritage-pill {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.18rem 0.55rem;
    border-radius: 9999px;
    background: #fef3c7;
    color: #92400e;
    border: 1px solid #f59e0b;
  }

  .wp-archive-link {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--accent-primary);
    text-decoration: none;
  }

  .btn-country-test {
    border: 1px solid var(--accent-primary);
    background: var(--threat-sovereign-bg);
    color: var(--accent-primary);
    border-radius: 8px;
    padding: 0.36rem 0.7rem;
    font-size: 0.78rem;
    font-weight: 700;
    cursor: pointer;
    min-height: 36px;
  }

  .btn-country-test:hover {
    background: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .heritage-review-note {
    font-size: 0.74rem;
    color: var(--text-muted);
  }

  .wish-player-shell :global(.wobble-readout) {
    background: var(--bg-surface);
    border: 1.5px solid var(--border-medium);
    border-inline-start: 4px solid var(--accent-primary);
    border-radius: 10px;
    padding: 0.72rem 0.9rem;
    margin: 0.75rem 0 0.85rem;
  }

  .wish-player-shell :global(.wr-head) {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.45rem;
    margin-bottom: 0.35rem;
  }

  .wish-player-shell :global(.wr-tag) {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--accent-primary);
  }

  .wish-player-shell :global(.wr-dep) {
    font-size: 0.78rem;
    color: var(--text-muted);
  }

  .wish-player-shell :global(.wr-rated-row) {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.28rem;
  }

  .wish-player-shell :global(.wr-status-pill) {
    font-size: 0.72rem;
    font-weight: 800;
    padding: 0.14rem 0.5rem;
    border-radius: 9999px;
  }

  .wish-player-shell :global(.wr-status-pill.pass) {
    background: var(--threat-sovereign-bg);
    color: var(--accent-primary);
  }

  .wish-player-shell :global(.wr-status-pill.gap) {
    background: #fef3c7;
    color: #92400e;
  }

  .wish-player-shell :global(.wr-label) {
    font-size: 0.86rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .wish-player-shell :global(.wr-body) {
    margin: 0;
    font-size: 0.82rem;
    line-height: 1.48;
    color: var(--text-secondary);
  }

  .wish-player-shell :global(.wr-muted) {
    color: var(--text-muted);
  }

  .wish-player-shell :global(.wr-link) {
    display: inline-block;
    margin-inline-start: 0.35rem;
    color: var(--accent-primary);
    font-weight: 700;
    text-decoration: none;
  }

  .wish-player-shell :global(.wr-link:hover) {
    text-decoration: underline;
  }

  .wish-finale {
    border-top: 1px solid var(--border-subtle);
    padding-top: 1rem;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
  }

  .closing-line {
    margin: 0;
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .finale-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    align-items: center;
  }

  .btn-advance {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    border: 0;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    min-height: 44px;
  }

  .btn-lights-jump {
    font-size: 0.84rem;
    font-weight: 700;
    color: var(--accent-primary);
    text-decoration: none;
  }

  @media (max-width: 720px) {
    .beat-steps {
      grid-template-columns: repeat(2, 1fr);
    }
    .toto-intro-body {
      flex-direction: column;
      align-items: flex-start;
    }
    .fp-opts,
    .reality-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 440px) {
    .rm-scale-steps {
      grid-template-columns: 1fr;
    }
  }
</style>
