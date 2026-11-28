<script lang="ts">
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';
  import type { CountrySummaryItem } from '../lib/countryData';
  import { dict, activeLocale, storyOverlay, localeReady, resolveViewDict, getCountryDisplayName, type LocaleKey } from '../i18n/store';
  import { resolveHeritageMeta, type StoryLocalePack } from '../i18n/storyTypes';
  import type { TranslationDict } from '../i18n/en';
  import { trackEvent } from '../lib/privacyStorage';
  import { completedWishList, setSelectedCountryForReadiness } from '../lib/readinessState';
  import { countryContextStore, syncCountryContext } from '../lib/countryContext';
  import { detectBrowserCountrySky, findCityById } from '../lib/countrySkies';
  import { findAnyHeritageForCountry } from '../lib/heritageLoader';
  import ConceptVisualSvg from './ConceptVisualSvg.svelte';

  export let countries: CountrySummaryItem[] = [];
  export let base = '';
  export let ssrLocale: LocaleKey = 'en';
  export let ssrDict: Partial<TranslationDict> | undefined = undefined;
  export let ssrStoryOverlay: StoryLocalePack | undefined = undefined;
  $: d = resolveViewDict($dict, $localeReady, ssrLocale, ssrDict);
  $: effectiveLocale = (!$localeReady && ssrLocale !== 'en' ? ssrLocale : $activeLocale) as LocaleKey;
  $: effectiveOverlay = (!$localeReady && ssrLocale !== 'en' && ssrStoryOverlay ? ssrStoryOverlay : $storyOverlay);

  const initialCtx = get(countryContextStore);
  const initialDetectedIso =
    initialCtx.iso && initialCtx.iso !== 'GLOBAL' ? initialCtx.iso : 'NOR';

  let allCountries: CountrySummaryItem[] = countries;
  let revealed = true;
  let catalogReady = false;
  let boxEl: HTMLDivElement | null = null;
  let selectedIso = initialDetectedIso;
  let searchFilter = '';
  let localeDetected = initialCtx.iso !== 'GLOBAL' && !initialCtx.explicit;
  let highlightedIdx: number | null = null;
  let detailsOpen = false;
  let lastSyncedCtxKey =
    initialCtx.iso !== 'GLOBAL'
      ? `${initialCtx.iso}::${initialCtx.explicit ? '1' : '0'}`
      : '';

  $: filteredCountries = allCountries.filter((c) => {
    const q = searchFilter.trim().toLowerCase();
    if (!q) return true;
    const locName = getCountryDisplayName(c.iso, c.name, effectiveLocale).toLowerCase();
    return (
      c.name.toLowerCase().includes(q) ||
      locName.includes(q) ||
      c.iso.toLowerCase().includes(q)
    );
  });
  $: ratedFiltered = filteredCountries.filter((c) => c.kind === 'rated');
  $: unratedFiltered = filteredCountries.filter((c) => c.kind === 'unrated');
  $: activeCountry =
    allCountries.find((c) => c.iso === selectedIso) ?? (catalogReady ? allCountries[0] : null);
  $: fallbackCountryLabel =
    selectedIso !== 'GLOBAL'
      ? getCountryDisplayName(
          selectedIso,
          $countryContextStore.iso === selectedIso && $countryContextStore.countryName !== 'Global'
            ? $countryContextStore.countryName
            : selectedIso,
          effectiveLocale
        )
      : '';
  $: activeCountryName = activeCountry
    ? getCountryDisplayName(activeCountry.iso, activeCountry.name, effectiveLocale)
    : fallbackCountryLabel;
  $: countryHeritage =
    selectedIso && selectedIso !== 'GLOBAL'
      ? findAnyHeritageForCountry(activeCountry?.iso ?? selectedIso)
      : null;
  $: countryHeritageMeta = countryHeritage
    ? resolveHeritageMeta(countryHeritage, effectiveLocale, effectiveOverlay)
    : null;
  $: localizedCatchStatus =
    activeCountry?.kind === 'rated'
      ? activeCountry.catchStatus === 'Easily'
        ? d.country.catchStates.easily
        : activeCountry.catchStatus === 'With effort'
          ? d.country.catchStates.effort
          : d.country.catchStates.struggles
      : '';

  interface VisualCoverage {
    total: number;
    observed: number;
    observedFlags: string[];
    missingFlags: string[];
    headline: string;
  }

  function splitFlagsList(raw: string): string[] {
    const colonIdx = raw.indexOf(':');
    if (colonIdx < 0) return [];
    return raw
      .slice(colonIdx + 1)
      .replace(/\.$/, '')
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
  }

  function parseVisualCoverage(obs: string, miss: string): VisualCoverage {
    const nineMatch = obs.match(/(\d+)\/(\d+)/);
    const fourMatch = obs.match(/(\d+)\s+of\s+(\d+)/i);
    const total = nineMatch ? Number(nineMatch[2]) : fourMatch ? Number(fourMatch[2]) : 4;
    const observed = nineMatch ? Number(nineMatch[1]) : fourMatch ? Number(fourMatch[1]) : 1;
    const observedFlags = splitFlagsList(obs);
    const missingFlags = splitFlagsList(miss);
    const obsClean = obs.split(':')[0].replace(/\.$/, '').trim();
    const rawMiss = miss.split(':')[0].replace(/\.$/, '').replace(/\s+for$/i, '').trim();
    const missClean = missingFlags.length > 0 && /^Missing/i.test(rawMiss) && !/\(\d+\/\d+\)/.test(rawMiss)
      ? `${missingFlags.length} unmeasured survey gap${missingFlags.length === 1 ? '' : 's'}`
      : rawMiss;
    return {
      total,
      observed,
      observedFlags,
      missingFlags,
      headline: `${obsClean} · ${missClean}`
    };
  }

  $: unratedVisual =
    activeCountry && activeCountry.kind === 'unrated'
      ? parseVisualCoverage(activeCountry.observedSummary, activeCountry.missingSummary)
      : null;

  function applyCountrySelection(iso: string, pushContext = true) {
    selectedIso = iso;
    localeDetected = false;
    const found = allCountries.find((c) => c.iso === iso);
    if (found) {
      setSelectedCountryForReadiness({
        iso: found.iso,
        name: found.name,
        kind: found.kind,
        checklistCount: found.kind === 'rated' ? found.checklistCount : undefined
      });
    }
    if (pushContext) {
      syncCountryContext(findCityById(iso), true);
      highlightedIdx = null;
    }
    trackEvent('country_selected', { iso });
  }

  function pickCountry(iso: string) {
    applyCountrySelection(iso, true);
  }

  $: if ($countryContextStore.iso && $countryContextStore.iso !== 'GLOBAL') {
    const syncKey = `${$countryContextStore.iso}:${$countryContextStore.highlightChecklistIdx ?? ''}:${$countryContextStore.explicit ? '1' : '0'}`;
    if (syncKey !== lastSyncedCtxKey && allCountries.some((c) => c.iso === $countryContextStore.iso)) {
      lastSyncedCtxKey = syncKey;
      searchFilter = '';
      if (selectedIso !== $countryContextStore.iso) {
        applyCountrySelection($countryContextStore.iso, false);
        localeDetected = !$countryContextStore.explicit;
      }
      if ($countryContextStore.highlightChecklistIdx !== null) {
        highlightedIdx = $countryContextStore.highlightChecklistIdx;
        detailsOpen = true;
      }
    }
  }

  onMount(async () => {
    revealed = true;
    boxEl?.removeAttribute('data-prepaint-pending');
    try {
      const mod = await import('../data/country_catch_catalog.json');
      allCountries = (mod.default ?? mod) as CountrySummaryItem[];
      catalogReady = true;
    } catch {
      allCountries = countries;
      catalogReady = true;
    }
    try {
      const availSet = new Set(allCountries.map((c) => c.iso));
      let matchIso = '';
      if ($countryContextStore.iso && $countryContextStore.iso !== 'GLOBAL' && availSet.has($countryContextStore.iso)) {
        matchIso = $countryContextStore.iso;
        localeDetected = !$countryContextStore.explicit;
      } else {
        const detected = detectBrowserCountrySky();
        if (detected.sky.iso !== 'GLOBAL' && availSet.has(detected.sky.iso)) {
          matchIso = detected.sky.iso;
          localeDetected = true;
          syncCountryContext(detected.sky, false);
        }
      }

      if (matchIso) {
        selectedIso = matchIso;
        const found = allCountries.find((c) => c.iso === matchIso);
        if (found) {
          setSelectedCountryForReadiness({
            iso: found.iso,
            name: found.name,
            kind: found.kind,
            checklistCount: found.kind === 'rated' ? found.checklistCount : undefined
          });
        }
      }
    } catch {
      // Keep neutral fallback NOR
    }
  });
</script>

<!-- STEP 3: COMPACT 148-COUNTRY VISUAL READINESS SNAPSHOT -->
<section id="country-check" class="country-section">
  <div class="section-wrap">
    <div class="section-head">
      <h2 id="country-check-heading" class="sec-title">
        {activeCountryName
          ? d.heritageUi.countryCatchHeading.replace('{country}', activeCountryName)
          : d.country.heading}
      </h2>
      <p class="sec-sub">{d.country.subhead}</p>
    </div>

    {#if revealed}
      <div class="compact-country-box" bind:this={boxEl}>
        <p class="cc-prepaint-pending" aria-hidden="true"></p>
        <div class="select-grid">
          <div class="input-group">
            <label for="country-search-input" class="sr-only">{d.country.searchLabel}</label>
            <input
              id="country-search-input"
              type="search"
              bind:value={searchFilter}
              placeholder={d.country.searchPlaceholder}
              class="search-input"
            />
          </div>
          <div class="input-group">
            <label for="country-select" class="sr-only">{d.country.selectLabel}</label>
            <select
              id="country-select"
              bind:value={selectedIso}
              onchange={() => pickCountry(selectedIso)}
              class="country-select"
            >
              {#if ratedFiltered.length > 0}
                <optgroup label={d.country.benchmarkGroupTpl.replace('{count}', String(ratedFiltered.length))}>
                  {#each ratedFiltered as c}
                    <option value={c.iso}>{getCountryDisplayName(c.iso, c.name, effectiveLocale)} ({c.iso})</option>
                  {/each}
                </optgroup>
              {/if}
              {#if unratedFiltered.length > 0}
                <optgroup label={d.country.coverageGroupTpl.replace('{count}', String(unratedFiltered.length))}>
                  {#each unratedFiltered as c}
                    <option value={c.iso}>{getCountryDisplayName(c.iso, c.name, effectiveLocale)} ({c.iso}) — {d.country.partialDataSuffix}</option>
                  {/each}
                </optgroup>
              {/if}
            </select>
          </div>
        </div>

        {#if activeCountry && activeCountry.kind === 'rated'}
          <div class="country-card-row">
            <div class="cc-top">
              <div>
                <span class="rp-badge rated-badge">{d.country.benchmarkBadge} &middot; {activeCountry.region}{#if localeDetected}&nbsp;&middot; {d.country.autoDetectedBadge}{/if}</span>
                <h3 class="rp-name">{activeCountryName}</h3>
              </div>
              <a href={`${base}/countries/${activeCountry.id}/`} class="btn-country-link">
                {d.country.openCountryCta} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
              </a>
            </div>

            {#if countryHeritage && countryHeritageMeta}
              <div class="cc-tradition-banner">
                <ConceptVisualSvg variant={countryHeritage.id} compact={true} />
                <div class="cct-copy">
                  <span class="cct-label">{d.heritageUi.traditionTestsLabel} <strong>{countryHeritageMeta.traditionLabel}</strong></span>
                  <p class="cct-title">{countryHeritageMeta.chipTitle}</p>
                  <p class="cct-dep">{countryHeritageMeta.dependencyLabel}</p>
                </div>
                <a href={`${base}/traditions/${countryHeritage.slug}/`} class="cct-link">
                  {d.heritageUi.readArchiveLink} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
                </a>
              </div>
            {/if}

            <div class="metrics-strip">
              <div class="m-chip">
                <span>{d.country.runsOfflineLabel}</span>
                <strong>{activeCountry.cloudDaysText}</strong>
                <div class="battery-bars" aria-hidden="true">
                  {#each [1, 2, 3, 4, 5] as bSeg}
                    <span class="b-seg" class:on={bSeg <= activeCountry.batterySegments}></span>
                  {/each}
                </div>
              </div>
              <div class="m-chip">
                <span>{d.country.catchesLabel}</span>
                <strong
                  class:good={activeCountry.catchStatus === 'Easily'}
                  class:mid={activeCountry.catchStatus === 'With effort'}
                  class:warn={activeCountry.catchStatus === 'Struggles'}
                >{localizedCatchStatus}</strong>
              </div>
              <div class="m-chip">
                <span>{d.country.safeguardsReadyLabel}</span>
                <strong>{d.country.ofFiveTpl.replace('{count}', String(activeCountry.checklistCount))}</strong>
                <div class="battery-bars" aria-hidden="true">
                  {#each activeCountry.checklist as chk}
                    <span class="b-seg" class:on={chk.pass} class:gap={!chk.pass}></span>
                  {/each}
                </div>
              </div>
            </div>

            <div class="visual-safeguards-bar" aria-label={activeCountryName}>
              {#each activeCountry.checklist as item, idx}
                {@const shortLabel = d.country.safeguardPills[idx] ?? item.label}
                <span class="vs-pill" class:pass={item.pass} class:focused={highlightedIdx === idx} title={item.label}>
                  {item.pass ? '✓' : '○'} {shortLabel}
                </span>
              {/each}
            </div>

            <details class="cc-details" bind:open={detailsOpen}>
              <summary>{d.country.detailsSummaryTpl.replace('{country}', activeCountryName)}</summary>
              <p class="cc-weak"><strong>{d.country.mainConstraintLabel}</strong> {activeCountry.weakestLinkPlain}</p>
              <ul class="cl-items">
                {#each activeCountry.checklist as item, idx}
                  <li class:passed={item.pass} class:focused-check={highlightedIdx === idx}>
                    <span>{item.pass ? '✓' : '○'} {item.label}</span>
                    <small>{item.metricNote}</small>
                  </li>
                {/each}
              </ul>
            </details>
          </div>
        {:else if activeCountry && activeCountry.kind === 'unrated'}
          <div class="country-card-row">
            <div class="cc-top">
              <div>
                <span class="rp-badge unrated-badge">{d.country.unratedBadge}{#if localeDetected}&nbsp;&middot; {d.country.autoDetectedBadge}{/if}</span>
                <h3 class="rp-name">{activeCountryName} <small class="iso-small">({activeCountry.iso})</small></h3>
              </div>
              <a href={`${base}/countries/${activeCountry.iso.toLowerCase()}/`} class="btn-country-link">
                {d.country.openCountryCta} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
              </a>
            </div>

            {#if countryHeritage && countryHeritageMeta}
              <div class="cc-tradition-banner">
                <ConceptVisualSvg variant={countryHeritage.id} compact={true} />
                <div class="cct-copy">
                  <span class="cct-label">{d.heritageUi.traditionTestsLabel} <strong>{countryHeritageMeta.traditionLabel}</strong></span>
                  <p class="cct-title">{countryHeritageMeta.chipTitle}</p>
                  <p class="cct-dep">{countryHeritageMeta.dependencyLabel}</p>
                </div>
                <a href={`${base}/traditions/${countryHeritage.slug}/`} class="cct-link">
                  {d.heritageUi.readArchiveLink} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
                </a>
              </div>
            {/if}

            {#if unratedVisual}
              <div class="coverage-visual-panel">
                <div class="cov-head-row">
                  <p class="ur-summary">{unratedVisual.headline} &middot; {d.country.neverGuessedNote}</p>
                  <span class="cov-ratio-pill">{unratedVisual.observed} / {unratedVisual.total}</span>
                </div>
                <div class="cov-progress-bars" aria-hidden="true">
                  {#each Array.from({ length: unratedVisual.total }) as _, sIdx}
                    <span class="cov-seg" class:filled={sIdx < unratedVisual.observed}></span>
                  {/each}
                </div>

                {#if unratedVisual.observedFlags.length > 0 || unratedVisual.missingFlags.length > 0}
                  <div class="cov-flags-board">
                    {#if unratedVisual.observedFlags.length > 0}
                      <div class="cov-group">
                        <span class="cov-grp-lbl good">{d.heritageUi.coverageObservedLabel}</span>
                        <div class="cov-chips">
                          {#each unratedVisual.observedFlags as flag}
                            <span class="cov-chip good">✓ {flag}</span>
                          {/each}
                        </div>
                      </div>
                    {/if}
                    {#if unratedVisual.missingFlags.length > 0}
                      <div class="cov-group">
                        <span class="cov-grp-lbl warn">{d.heritageUi.coverageMissingLabel}</span>
                        <div class="cov-chips">
                          {#each unratedVisual.missingFlags as flag}
                            <span class="cov-chip warn">○ {flag}</span>
                          {/each}
                        </div>
                      </div>
                    {/if}
                  </div>
                {/if}
              </div>
            {/if}
          </div>
        {:else if !activeCountry && activeCountryName}
          <div class="country-card-row">
            <div class="cc-top">
              <div>
                <span class="rp-badge unrated-badge">{d.country.autoDetectedBadge}</span>
                <h3 class="rp-name">{activeCountryName} <small class="iso-small">({selectedIso})</small></h3>
              </div>
            </div>
            <p class="ur-summary">{d.country.checkingBaseline}</p>
          </div>
        {/if}
      </div>
    {:else}
      <noscript>
        <p class="ur-summary">Explore all 148 countries in the <a href={`${base}/countries/`}>39-nation index</a> and <a href={`${base}/coverage/`}>global coverage audit</a>.</p>
      </noscript>
    {/if}
  </div>
</section>

<style>
  .country-section {
    contain: layout style;
    padding: clamp(1.35rem, 3vw, 2.25rem) 0;
    scroll-margin-top: 90px;
    background: var(--bg-canvas);
    min-height: 295px;
  }

  .section-wrap {
    max-width: 960px;
    margin: 0 auto;
    padding: 0 1.15rem;
  }

  .section-head {
    text-align: center;
    max-width: 660px;
    margin: 0 auto 0.95rem;
  }

  .sec-title {
    font-family: var(--font-family-sans);
    font-size: clamp(1.4rem, 2.8vw, 1.95rem);
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 0.35rem;
    line-height: 1.2;
  }

  .sec-sub {
    font-size: 0.94rem;
    color: var(--text-secondary);
    margin: 0;
  }

  .cc-prepaint-pending {
    display: none;
    margin: 0.85rem 0 0;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    background: var(--bg-surface);
    border: 1px dashed var(--border-medium);
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
    text-align: center;
  }

  .compact-country-box:global([data-prepaint-pending='true']) .country-card-row {
    display: none;
  }

  .compact-country-box:global([data-prepaint-pending='true']) .cc-prepaint-pending {
    display: block;
  }

  .compact-country-box {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    padding: 1rem 1.15rem;
    box-shadow: var(--shadow-sm);
  }

  .select-grid {
    display: grid;
    grid-template-columns: 1fr 1.35fr;
    gap: 0.55rem;
    margin-bottom: 0.85rem;
  }

  .search-input,
  .country-select {
    width: 100%;
    min-height: 42px;
    padding: 0.45rem 0.8rem;
    border-radius: 10px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    font-size: 0.9rem;
    font-family: var(--font-family-sans);
  }

  .country-card-row {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.9rem 1rem;
  }

  .cc-top {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 0.65rem;
  }

  .rp-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.66rem;
    font-weight: 800;
    padding: 0.16rem 0.5rem;
    border-radius: 6px;
    margin-bottom: 0.2rem;
  }

  .rated-badge {
    background: var(--threat-sovereign-bg);
    color: var(--threat-sovereign);
  }

  .unrated-badge {
    background: var(--threat-warning-bg);
    color: var(--threat-warning);
  }

  .rp-name {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-primary);
  }

  .iso-small {
    font-family: var(--font-family-mono);
    font-size: 0.82rem;
    color: var(--text-muted);
    font-weight: 500;
  }

  .btn-country-link {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    min-height: 38px;
    padding: 0.45rem 0.9rem;
    border-radius: 9px;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    text-decoration: none;
    font-weight: 700;
    font-size: 0.84rem;
  }

  .metrics-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.55rem;
    margin-bottom: 0.65rem;
  }

  .m-chip {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 0.5rem 0.7rem;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .m-chip span {
    font-size: 0.72rem;
    color: var(--text-muted);
    font-weight: 600;
  }

  .m-chip strong {
    font-size: 0.96rem;
    color: var(--text-primary);
  }

  .m-chip strong.good { color: var(--threat-sovereign); }
  .m-chip strong.mid { color: var(--threat-warning); }
  .m-chip strong.warn { color: var(--threat-critical); }

  .cc-details summary {
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--accent-primary);
  }

  .cc-weak {
    margin: 0.5rem 0;
    font-size: 0.84rem;
    color: var(--text-secondary);
  }

  .cl-items {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.4rem;
    font-size: 0.8rem;
  }

  .cl-items li {
    padding: 0.4rem 0.6rem;
    border-radius: 8px;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    display: flex;
    flex-direction: column;
    color: var(--text-secondary);
  }

  .cl-items li.passed {
    border-color: var(--threat-sovereign-border);
    color: var(--text-primary);
  }

  .cl-items li.focused-check {
    border: 2px solid var(--accent-primary);
    background: var(--threat-sovereign-bg);
    box-shadow: 0 0 0 2px rgba(27, 103, 86, 0.14);
  }

  .cc-tradition-banner {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.75rem 0.95rem;
    padding: 0.68rem 0.8rem;
    margin-bottom: 0.75rem;
    border-radius: 12px;
    background: var(--threat-sovereign-bg);
    border: 1px solid var(--threat-sovereign-border);
  }

  .cct-copy {
    flex: 1 1 240px;
    min-width: 0;
  }

  .cct-label {
    display: block;
    font-size: 0.72rem;
    color: var(--accent-primary);
    margin-bottom: 0.14rem;
  }

  .cct-title {
    margin: 0;
    font-size: 0.92rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.3;
  }

  .cct-dep {
    margin: 0.18rem 0 0;
    font-size: 0.76rem;
    color: var(--text-secondary);
    line-height: 1.35;
  }

  .cct-link {
    font-size: 0.76rem;
    font-weight: 800;
    color: var(--accent-primary);
    text-decoration: none;
    white-space: nowrap;
  }

  .cct-link:hover {
    text-decoration: underline;
  }

  .battery-bars {
    display: flex;
    gap: 3px;
    margin-top: 0.25rem;
  }

  .b-seg {
    flex: 1 1 0;
    height: 6px;
    border-radius: 3px;
    background: var(--border-subtle);
  }

  .b-seg.on {
    background: var(--threat-sovereign);
  }

  .b-seg.gap {
    background: var(--threat-warning-bg);
    border: 1px dashed var(--threat-warning-border);
  }

  .visual-safeguards-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-bottom: 0.6rem;
  }

  .vs-pill {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.2rem 0.55rem;
    border-radius: 9999px;
    background: var(--threat-warning-bg);
    color: var(--threat-warning);
    border: 1px dashed var(--threat-warning-border);
  }

  .vs-pill.pass {
    background: var(--threat-sovereign-bg);
    color: var(--threat-sovereign);
    border: 1px solid var(--threat-sovereign-border);
  }

  .vs-pill.focused {
    box-shadow: 0 0 0 2px var(--accent-primary-glow);
    border-width: 2px;
    border-style: solid;
  }

  .coverage-visual-panel {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .cov-head-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.35rem;
  }

  .cov-ratio-pill {
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 800;
    padding: 0.14rem 0.5rem;
    border-radius: 9999px;
    background: var(--bg-surface-elevated);
    color: var(--accent-primary);
    border: 1px solid var(--threat-sovereign-border);
  }

  .cov-progress-bars {
    display: flex;
    gap: 4px;
  }

  .cov-seg {
    flex: 1 1 0;
    height: 8px;
    border-radius: 4px;
    background: var(--bg-surface-elevated);
    border: 1px dashed var(--threat-warning-border);
  }

  .cov-seg.filled {
    background: var(--threat-sovereign);
    border: 0;
  }

  .cov-flags-board {
    display: grid;
    grid-template-columns: 1.3fr 1fr;
    gap: 0.6rem;
    margin-top: 0.15rem;
  }

  .cov-group {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 0.55rem 0.65rem;
  }

  .cov-grp-lbl {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.64rem;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
  }

  .cov-grp-lbl.good { color: var(--threat-sovereign); }
  .cov-grp-lbl.warn { color: var(--threat-warning); }

  .cov-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
  }

  .cov-chip {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.16rem 0.48rem;
    border-radius: 6px;
  }

  .cov-chip.good {
    background: var(--threat-sovereign-bg);
    color: var(--text-primary);
    border: 1px solid var(--threat-sovereign-border);
  }

  .cov-chip.warn {
    background: var(--threat-warning-bg);
    color: var(--threat-warning);
    border: 1px dashed var(--threat-warning-border);
  }

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  .ur-summary {
    margin: 0;
    font-size: 0.84rem;
    font-weight: 600;
    line-height: 1.4;
    color: var(--text-secondary);
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
  }

  @media (max-width: 680px) {
    .country-section {
      min-height: 360px;
    }
    .select-grid,
    .metrics-strip,
    .cl-items,
    .cov-flags-board {
      grid-template-columns: 1fr;
    }
    .btn-country-link {
      width: 100%;
      justify-content: center;
    }
  }
</style>
