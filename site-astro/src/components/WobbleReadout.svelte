<script lang="ts">
  import { onMount } from 'svelte';
  import { dict, activeLocale } from '../i18n/store';
  import type { CountrySummaryItem } from '../lib/countryData';
  import type { HeritageBinding, LangCode } from '../lib/heritageTypes';

  export let countryIso: string = 'GLOBAL';
  export let countryName: string = 'Global';
  export let binding: HeritageBinding;
  export let base = '';

  let catalog: CountrySummaryItem[] = [];
  let loaded = false;

  onMount(async () => {
    try {
      const mod = await import('../data/country_catch_catalog.json');
      catalog = (mod.default ?? mod) as CountrySummaryItem[];
    } catch {
      catalog = [];
    } finally {
      loaded = true;
    }
  });

  $: loc = ($activeLocale === 'es' || $activeLocale === 'ar' ? $activeLocale : 'en') as LangCode;
  $: matchedCountry =
    countryIso && countryIso !== 'GLOBAL'
      ? catalog.find((c) => c.iso === countryIso.toUpperCase()) ?? null
      : null;
  $: boundCheck =
    matchedCountry?.kind === 'rated'
      ? matchedCountry.checklist[binding.safeguardChecklistIdx] ?? matchedCountry.checklist[0]
      : null;
  $: displayName = matchedCountry?.name ?? countryName;
</script>

<aside class="wobble-readout" aria-live="polite">
  <div class="wr-head">
    <span class="wr-tag">
      {$dict.heritageUi.weightBindingTitle.replace('{country}', displayName)}
    </span>
    <span class="wr-dep">{binding.dependencyLabel[loc] ?? binding.dependencyLabel.en}</span>
  </div>

  {#if !loaded}
    <p class="wr-body wr-muted">Checking national safeguard baseline...</p>
  {:else if matchedCountry?.kind === 'rated' && boundCheck}
    <div class="wr-rated-row">
      <span class="wr-status-pill" class:pass={boundCheck.pass} class:gap={!boundCheck.pass}>
        {boundCheck.pass ? `✓ ${$dict.heritageUi.weightRatedInPlace}` : `○ ${$dict.heritageUi.weightRatedGap}`}
      </span>
      <span class="wr-label">{boundCheck.label}</span>
    </div>
    <p class="wr-body">
      {boundCheck.metricNote} &middot;
      <a href={`${base}/countries/${matchedCountry.id}/`} class="wr-link">{$dict.country.openCountryCta} &rarr;</a>
    </p>
  {:else if matchedCountry?.kind === 'unrated'}
    <p class="wr-body">
      {$dict.heritageUi.weightContextNote
        .replace('{country}', matchedCountry.name)
        .replace('{region}', matchedCountry.region)
        .replace('{observed}', matchedCountry.observedSummary)}
      <a href={`${base}/coverage/`} class="wr-link">{$dict.country.unratedHelpCta} &rarr;</a>
    </p>
  {:else}
    <p class="wr-body">
      {$dict.heritageUi.weightNoCountry}
      <a href="#country-check" class="wr-link">{$dict.hero.ctaSecondary} &rarr;</a>
    </p>
  {/if}
</aside>
