<script lang="ts">
  import { onMount } from 'svelte';
  import { dict, activeLocale, getCountryDisplayName } from '../i18n/store';
  import { pickBaseLText } from '../i18n/storyTypes';
  import type { CountrySummaryItem } from '../lib/countryData';
  import type { HeritageBinding } from '../lib/heritageTypes';

  export let countryIso: string = 'GLOBAL';
  export let countryName: string = 'Global';
  export let binding: HeritageBinding;
  export let dependencyText: string = '';
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

  $: matchedCountry =
    countryIso && countryIso !== 'GLOBAL'
      ? catalog.find((c) => c.iso === countryIso.toUpperCase()) ?? null
      : null;
  $: boundCheck =
    matchedCountry?.kind === 'rated'
      ? matchedCountry.checklist[binding.safeguardChecklistIdx] ?? matchedCountry.checklist[0]
      : null;
  $: displayName = matchedCountry
    ? getCountryDisplayName(matchedCountry.iso, matchedCountry.name, $activeLocale)
    : getCountryDisplayName(countryIso, countryName, $activeLocale);
  $: resolvedDependency = dependencyText || pickBaseLText(binding.dependencyLabel, $activeLocale);
</script>

<aside class="wobble-readout" aria-live="polite">
  <div class="wr-head">
    <span class="wr-tag">
      {$dict.heritageUi.weightBindingTitle.replace('{country}', displayName)}
    </span>
    <span class="wr-dep">{resolvedDependency}</span>
  </div>

  {#if !loaded}
    <p class="wr-body wr-muted">{$dict.country.checkingBaseline}</p>
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
        .replace('{country}', displayName)
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
