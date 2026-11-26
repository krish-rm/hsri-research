<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { dict, activeLocale } from '../i18n/store';
  import WishSceneIllustration from './WishSceneIllustration.svelte';
  import {
    readinessStore,
    recordWishCompletion,
    type LightKey,
    type ShadowKey
  } from '../lib/readinessState';
  import { trackEvent } from '../lib/privacyStorage';

  type LangCode = 'en' | 'es' | 'ar';
  type LText = { en: string; es: string; ar: string };

  export interface WishItem {
    id: string;
    door: string;
    order: number;
    icon: string;
    title: LText;
    doorTitle: LText;
    honestyLabel: 'Imagination' | 'Possible soon' | 'Real today';
    honestyNote: LText;
    verbatimFromBrief: boolean;
    shadowTag: ShadowKey;
    atlasRefs: string[];
    wonder: { text: LText; kalpaLine: LText; transcript: LText; draft: boolean };
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
      score: number;
      isConservativeBaseline: boolean;
      statusLabel: LText;
      note: LText;
      source: string;
      sourceUrl: string;
      lastReviewed: string;
    };
  }

  export let wish: WishItem;
  export let base = '';
  export let onClose: () => void = () => {};
  export let onNextWish: () => void = () => {};

  let beat: 'wonder' | 'wobble' | 'weight' | 'way' = 'wonder';
  let startedAt = Date.now();
  let guessedWobble = false;
  let foresightPicked: number | null = null;
  let selectedWeight: 'a' | 'b' | 'c' | null = null;
  let pledged = false;
  let lastSavedKey = '';
  let playerHeadingEl: HTMLHeadingElement | null = null;

  $: loc = ($activeLocale === 'es' || $activeLocale === 'ar' ? $activeLocale : 'en') as LangCode;
  $: lText = (t: LText) => t[loc] ?? t.en;
  $: chosenOpt = wish.weight.options.find((o) => o.id === selectedWeight) ?? null;
  $: countryRef = $readinessStore.selectedCountry;

  onMount(async () => {
    startedAt = Date.now();
    trackEvent('wish_started', { wish: wish.id });
    await tick();
    playerHeadingEl?.focus({ preventScroll: true });
  });

  function chooseForesight(idx: number) {
    foresightPicked = idx;
    const isRealGuess = idx < 3;
    guessedWobble = isRealGuess;
    if (isRealGuess) trackEvent('foresight_guess', { wish: wish.id, choice: idx });
    beat = 'wobble';
  }

  function chooseWeight(optId: 'a' | 'b' | 'c') {
    selectedWeight = optId;
    const opt = wish.weight.options.find((o) => o.id === optId);
    if (opt) {
      trackEvent('weight_choice', { wish: wish.id, choice: optId, light: opt.light, shadow: opt.shadow });
    }
    beat = 'way';
    saveCompletion(pledged);
  }

  function togglePledge() {
    pledged = !pledged;
    if (pledged) trackEvent('way_pledge', { wish: wish.id });
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
      wishTitle: lText(wish.title),
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

<article class="wish-player-shell" aria-label={lText(wish.title)}>
  <header class="wp-head">
    <div>
      <div class="wp-badges">
        <span class="wp-door">{lText(wish.doorTitle)}</span>
        <span class="wp-honesty">{$dict.player.honestyPrefix} {wish.honestyLabel}</span>
        <span class="wp-dur">{$dict.player.durationBadge}</span>
      </div>
      <h3 class="wp-title" tabindex="-1" bind:this={playerHeadingEl}>{lText(wish.title)}</h3>
      <p class="wp-honesty-note">{lText(wish.honestyNote)}</p>
    </div>
    <button type="button" class="wp-back-btn" on:click={onClose}>
      &larr; {$dict.player.backToDoors}
    </button>
  </header>

  <!-- 4-Beat Progress Tabs -->
  <nav class="beat-steps" aria-label="Wish story progression">
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
        transcript={lText(wish.wonder.transcript)}
      />
      <p class="kalpa-badge">{lText(wish.wonder.kalpaLine)}</p>
      <p class="beat-main-text">{lText(wish.wonder.text)}</p>

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
        transcript={lText(wish.wobble.transcript)}
      />
      {#if wish.wobble.draft}
        <span class="draft-pill">{$dict.player.draftTag}</span>
      {/if}
      <p class="beat-main-text">{lText(wish.wobble.text)}</p>
      <button type="button" class="btn-advance" on:click={() => (beat = 'weight')}>
        {$dict.player.toWeightBtn} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
      </button>
    {:else if beat === 'weight'}
      <WishSceneIllustration
        wishId={wish.id}
        door={wish.door}
        beat="weight"
        transcript={lText(wish.weight.transcript)}
      />
      {#if wish.weight.draft}
        <span class="draft-pill">{$dict.player.draftTag}</span>
      {/if}
      <p class="beat-main-text weight-q">{lText(wish.weight.question)}</p>
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
            <span class="wc-text">{lText(opt.text)}</span>
            <span class="wc-meta">{opt.light} · {$dict.player.shadows[opt.shadow]}</span>
          </button>
        {/each}
      </div>
    {:else}
      <WishSceneIllustration
        wishId={wish.id}
        door={wish.door}
        beat="way"
        transcript={lText(wish.way.transcript)}
      />
      <p class="beat-main-text">{lText(wish.way.text)}</p>

      <div class="way-action-box">
        <span class="way-box-tag">{$dict.player.wayActionTitle}</span>
        <h4>{lText(wish.way.actionCardTitle)}</h4>
        <p>{lText(wish.way.actionCardStep)}</p>
        <button type="button" class="btn-pledge" class:pledged={pledged} on:click={togglePledge}>
          {pledged ? `✓ ${$dict.player.pledgeDone}` : $dict.player.pledgeBtn}
        </button>
      </div>

      <!-- Reality Meter + Cited Source & Last Reviewed Date -->
      <div class="reality-grid">
        <div class="reality-card">
          <div class="rc-top">
            <span class="rc-tag">{$dict.player.realityTitle}</span>
            <span class="rc-date">{$dict.player.realityReviewed}: {wish.realityMeter.lastReviewed}</span>
          </div>
          <div class="rm-bar-track" aria-hidden="true">
            <div class="rm-bar-fill" style={`width: ${Math.max(4, wish.realityMeter.score)}%`}></div>
          </div>
          <p class="rm-status">{lText(wish.realityMeter.statusLabel)}</p>
          <p class="rm-note">{lText(wish.realityMeter.note)}</p>
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
            {#if countryRef && countryRef.kind === 'rated'}
              <p>
                To receive &ldquo;{lText(wish.title)}&rdquo;, <strong>{countryRef.name}</strong> has
                <strong>{countryRef.checklistCount} of 5</strong> things in place.
              </p>
            {:else}
              <p><a href="#country-check">{$dict.player.countryHookUnset}</a></p>
            {/if}
          </div>
        </div>
      </div>

      <div class="wish-finale">
        <p class="closing-line">{$dict.player.closingLine}</p>
        <div class="finale-actions">
          <button type="button" class="btn-advance" on:click={onNextWish}>
            {$dict.player.nextWishBtn} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
          </button>
          <a href="#five-lights" class="btn-lights-jump">{$dict.lights.heading} &darr;</a>
        </div>
      </div>
    {/if}
  </div>
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

  .kalpa-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.76rem;
    font-weight: 800;
    color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    margin: 0 0 0.55rem;
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

  .rm-bar-track {
    height: 8px;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    overflow: hidden;
    margin-bottom: 0.45rem;
  }

  .rm-bar-fill {
    height: 100%;
    background: var(--accent-primary);
    border-radius: 9999px;
  }

  .rm-status {
    margin: 0 0 0.25rem;
    font-size: 0.84rem;
    font-weight: 700;
    color: var(--text-primary);
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
    .fp-opts,
    .reality-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
