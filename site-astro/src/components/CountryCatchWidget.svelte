<script lang="ts">
  import { onMount } from 'svelte';
  import type { CountrySummaryItem } from '../lib/countryData';
  import { dict, activeLocale } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';
  import { completedWishList, setSelectedCountryForReadiness } from '../lib/readinessState';
  import { countryContextStore, syncCountryContext } from '../lib/countryContext';
  import { findCityById } from '../lib/countrySkies';
  import { findAnyHeritageForCountry } from '../lib/heritageLoader';

  export let countries: CountrySummaryItem[] = [];
  export let base = '';

  let allCountries: CountrySummaryItem[] = countries;
  let revealed = true;
  let selectedIso = 'NOR';
  let searchFilter = '';
  let localeDetected = false;
  let highlightedIdx: number | null = null;
  let detailsOpen = false;
  let lastSyncedCtxKey = '';

  const LOCALE_TO_ISO: Record<string, string> = {
    AU: 'AUS', AT: 'AUT', BE: 'BEL', BG: 'BGR', BR: 'BRA', CA: 'CAN',
    CN: 'CHN', CY: 'CYP', CZ: 'CZE', DE: 'DEU', DK: 'DNK', EG: 'EGY',
    ES: 'ESP', EE: 'EST', FI: 'FIN', FR: 'FRA', GB: 'GBR', UK: 'GBR',
    GR: 'GRC', HK: 'HKG', HR: 'HRV', HU: 'HUN', ID: 'IDN', IE: 'IRL',
    IL: 'ISR', IN: 'IND', IS: 'ISL', IT: 'ITA', JP: 'JPN', KE: 'KEN',
    KR: 'KOR', LT: 'LTU', LU: 'LUX', LV: 'LVA', MK: 'MKD', MT: 'MLT',
    MX: 'MEX', MY: 'MYS', NG: 'NGA', NL: 'NLD', NO: 'NOR', NZ: 'NZL',
    OM: 'OMN', PH: 'PHL', PK: 'PAK', PL: 'POL', PT: 'PRT', QA: 'QAT',
    RO: 'ROU', RU: 'RUS', SA: 'SAU', SE: 'SWE', SG: 'SGP', SK: 'SVK',
    SI: 'SVN', TH: 'THA', TR: 'TUR', TW: 'TWN', UA: 'UKR', AE: 'ARE',
    US: 'USA', VN: 'VNM', ZA: 'ZAF'
  };

  const TZ_TO_ISO: Array<[string, string]> = [
    ['Africa/Lagos', 'NGA'], ['Africa/Nairobi', 'KEN'], ['Africa/Cairo', 'EGY'],
    ['Africa/Johannesburg', 'ZAF'], ['America/Sao_Paulo', 'BRA'], ['America/Toronto', 'CAN'],
    ['America/Vancouver', 'CAN'], ['America/Mexico_City', 'MEX'], ['America/New_York', 'USA'],
    ['America/Chicago', 'USA'], ['America/Los_Angeles', 'USA'], ['Asia/Tokyo', 'JPN'],
    ['Asia/Seoul', 'KOR'], ['Asia/Singapore', 'SGP'], ['Asia/Hong_Kong', 'HKG'],
    ['Asia/Kolkata', 'IND'], ['Asia/Calcutta', 'IND'], ['Asia/Jakarta', 'IDN'],
    ['Asia/Dubai', 'ARE'], ['Asia/Riyadh', 'SAU'], ['Asia/Qatar', 'QAT'],
    ['Asia/Taipei', 'TWN'], ['Asia/Bangkok', 'THA'], ['Asia/Manila', 'PHL'],
    ['Asia/Karachi', 'PAK'], ['Australia/Sydney', 'AUS'], ['Australia/Melbourne', 'AUS'],
    ['Pacific/Auckland', 'NZL'], ['Europe/London', 'GBR'], ['Europe/Berlin', 'DEU'],
    ['Europe/Paris', 'FRA'], ['Europe/Oslo', 'NOR'], ['Europe/Helsinki', 'FIN'],
    ['Europe/Stockholm', 'SWE'], ['Europe/Copenhagen', 'DNK'], ['Europe/Amsterdam', 'NLD'],
    ['Europe/Madrid', 'ESP'], ['Europe/Rome', 'ITA'], ['Europe/Warsaw', 'POL'],
    ['Europe/Dublin', 'IRL'], ['Europe/Vienna', 'AUT'], ['Europe/Lisbon', 'PRT'],
    ['Europe/Athens', 'GRC']
  ];

  $: filteredCountries = allCountries.filter((c) =>
    !searchFilter.trim()
      ? true
      : c.name.toLowerCase().includes(searchFilter.trim().toLowerCase()) ||
        c.iso.toLowerCase().includes(searchFilter.trim().toLowerCase())
  );
  $: ratedFiltered = filteredCountries.filter((c) => c.kind === 'rated');
  $: unratedFiltered = filteredCountries.filter((c) => c.kind === 'unrated');
  $: activeCountry = allCountries.find((c) => c.iso === selectedIso) ?? allCountries[0];
  $: loc = ($activeLocale === 'es' || $activeLocale === 'ar' ? $activeLocale : 'en') as 'en' | 'es' | 'ar';
  $: countryHeritage = activeCountry ? findAnyHeritageForCountry(activeCountry.iso) : null;

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

  $: if ($countryContextStore.explicit && $countryContextStore.iso && $countryContextStore.iso !== 'GLOBAL') {
    const syncKey = `${$countryContextStore.iso}:${$countryContextStore.highlightChecklistIdx ?? ''}`;
    if (syncKey !== lastSyncedCtxKey && allCountries.some((c) => c.iso === $countryContextStore.iso)) {
      lastSyncedCtxKey = syncKey;
      searchFilter = '';
      if (selectedIso !== $countryContextStore.iso) {
        applyCountrySelection($countryContextStore.iso, false);
      }
      if ($countryContextStore.highlightChecklistIdx !== null) {
        highlightedIdx = $countryContextStore.highlightChecklistIdx;
        detailsOpen = true;
      }
    }
  }

  onMount(async () => {
    revealed = true;
    try {
      const mod = await import('../data/country_catch_catalog.json');
      allCountries = (mod.default ?? mod) as CountrySummaryItem[];
    } catch {
      allCountries = countries;
    }
    try {
      const availSet = new Set(allCountries.map((c) => c.iso));
      let matchIso = '';
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
      const tzHit = TZ_TO_ISO.find(([prefix]) => tz.startsWith(prefix));
      if (tzHit && availSet.has(tzHit[1])) matchIso = tzHit[1];

      if (!matchIso) {
        const langs = navigator.languages?.length ? navigator.languages : [navigator.language];
        for (const loc of langs) {
          const region = loc?.split(/[-_]/)[1]?.toUpperCase();
          if (region && LOCALE_TO_ISO[region] && availSet.has(LOCALE_TO_ISO[region])) {
            matchIso = LOCALE_TO_ISO[region];
            break;
          }
        }
      }

      if (matchIso) {
        selectedIso = matchIso;
        localeDetected = true;
      }
    } catch {
      // Keep neutral fallback NOR
    }
  });
</script>

<!-- STEP 3: COMPACT 148-COUNTRY SNAPSHOT -->
<section id="country-check" class="country-section">
  <div class="section-wrap">
    <div class="section-head">
      <h2 class="sec-title">{$dict.country.heading}</h2>
      <p class="sec-sub">{$dict.country.subhead}</p>
    </div>

    {#if revealed}
      <div class="compact-country-box">
        <div class="select-grid">
          <div class="input-group">
            <label for="country-search-input" class="sr-only">Filter countries by name</label>
            <input
              id="country-search-input"
              type="search"
              bind:value={searchFilter}
              placeholder={$dict.country.searchPlaceholder}
              class="search-input"
            />
          </div>
          <div class="input-group">
            <label for="country-select" class="sr-only">Select country</label>
            <select
              id="country-select"
              bind:value={selectedIso}
              onchange={() => pickCountry(selectedIso)}
              class="country-select"
            >
              {#if ratedFiltered.length > 0}
                <optgroup label="Benchmark Nations (39)">
                  {#each ratedFiltered as c}
                    <option value={c.iso}>{c.name} ({c.iso})</option>
                  {/each}
                </optgroup>
              {/if}
              {#if unratedFiltered.length > 0}
                <optgroup label="Coverage Audits ({unratedFiltered.length})">
                  {#each unratedFiltered as c}
                    <option value={c.iso}>{c.name} ({c.iso}) — Partial data</option>
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
                <span class="rp-badge rated-badge">39-NATION BENCHMARK &middot; {activeCountry.region}{#if localeDetected}&nbsp;&middot; AUTO-DETECTED{/if}</span>
                <h3 class="rp-name">{activeCountry.name}</h3>
              </div>
              <a href={`${base}/countries/${activeCountry.id}/`} class="btn-country-link">
                {$dict.country.openCountryCta} <span aria-hidden="true">&rarr;</span>
              </a>
            </div>

            <div class="metrics-strip">
              <div class="m-chip">
                <span>Runs offline</span>
                <strong>{activeCountry.cloudDaysText}</strong>
              </div>
              <div class="m-chip">
                <span>Catches breakthrough</span>
                <strong
                  class:good={activeCountry.catchStatus === 'Easily'}
                  class:mid={activeCountry.catchStatus === 'With effort'}
                  class:warn={activeCountry.catchStatus === 'Struggles'}
                >{activeCountry.catchStatus}</strong>
              </div>
              <div class="m-chip">
                <span>Safeguards ready</span>
                <strong>{activeCountry.checklistCount} of 5</strong>
              </div>
            </div>

            <details class="cc-details" bind:open={detailsOpen}>
              <summary>See the 5 safeguards &amp; primary bottleneck for {activeCountry.name}</summary>
              <p class="cc-weak"><strong>Main constraint:</strong> {activeCountry.weakestLinkPlain}</p>
              <ul class="cl-items">
                {#each activeCountry.checklist as item, idx}
                  <li class:passed={item.pass} class:focused-check={highlightedIdx === idx}>
                    <span>{item.pass ? '✓' : '○'} {item.label}</span>
                    <small>{item.metricNote}</small>
                  </li>
                {/each}
              </ul>
            </details>

            {#if countryHeritage}
              <div class="cc-heritage-strip">
                <span>🌍 <strong>{countryHeritage.traditionLabel[loc] ?? countryHeritage.traditionLabel.en}</strong> &middot; {countryHeritage.chipTitle[loc] ?? countryHeritage.chipTitle.en}</span>
                <a href={`${base}/traditions/${countryHeritage.slug}/`}>{$dict.heritageUi.readArchiveLink} &rarr;</a>
              </div>
            {/if}
          </div>
        {:else if activeCountry && activeCountry.kind === 'unrated'}
          <div class="country-card-row">
            <div class="cc-top">
              <div>
                <span class="rp-badge unrated-badge">{$dict.country.unratedBadge}{#if localeDetected}&nbsp;&middot; AUTO-DETECTED{/if}</span>
                <h3 class="rp-name">{activeCountry.name} <small class="iso-small">({activeCountry.iso})</small></h3>
              </div>
              <a href={`${base}/coverage/`} class="btn-country-link">
                {$dict.country.unratedHelpCta} <span aria-hidden="true">&rarr;</span>
              </a>
            </div>
            <p class="ur-summary">{activeCountry.observedSummary} Never guessed — {activeCountry.missingSummary}</p>
            {#if countryHeritage}
              <div class="cc-heritage-strip">
                <span>🌍 <strong>{countryHeritage.traditionLabel[loc] ?? countryHeritage.traditionLabel.en}</strong> &middot; {countryHeritage.chipTitle[loc] ?? countryHeritage.chipTitle.en}</span>
                <a href={`${base}/traditions/${countryHeritage.slug}/`}>{$dict.heritageUi.readArchiveLink} &rarr;</a>
              </div>
            {/if}
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

  .cc-heritage-strip {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.35rem 0.65rem;
    margin-top: 0.7rem;
    padding-top: 0.6rem;
    border-top: 1px dashed var(--border-subtle);
    font-size: 0.8rem;
    color: var(--text-secondary);
  }

  .cc-heritage-strip a {
    color: var(--accent-primary);
    font-weight: 700;
    text-decoration: none;
    white-space: nowrap;
  }

  .cc-heritage-strip a:hover {
    text-decoration: underline;
  }

  .ur-summary {
    margin: 0;
    font-size: 0.86rem;
    line-height: 1.5;
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
    .cl-items {
      grid-template-columns: 1fr;
    }
    .btn-country-link {
      width: 100%;
      justify-content: center;
    }
  }
</style>
