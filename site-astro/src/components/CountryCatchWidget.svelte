<script lang="ts">
  import { onMount } from 'svelte';
  import type { CountrySummaryItem } from '../lib/countryData';
  import { dict } from '../i18n/store';
  import { trackEvent } from '../lib/privacyStorage';
  import { completedWishList, setSelectedCountryForReadiness } from '../lib/readinessState';

  export let countries: CountrySummaryItem[] = [];
  export let base = '';

  let allCountries: CountrySummaryItem[] = countries;
  let revealed = false;
  let selectedIso = 'NOR';
  let searchFilter = '';
  let localeDetected = false;
  let openTooltip: 'offline' | 'catch' | 'pattern' | 'weak' | 'checklist' | null = null;

  // Global cross-continental starter examples (balanced mix of rated & unrated)
  const QUICK_ISOS = ['NOR', 'DEU', 'JPN', 'USA', 'SGP', 'BRA', 'IND', 'NGA'];

  // Map unambiguous browser region subtags or timezones to ISO3 country codes
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

  $: quickCountries = QUICK_ISOS.map((iso) => allCountries.find((c) => c.iso === iso)).filter(Boolean) as CountrySummaryItem[];
  $: filteredCountries = allCountries.filter((c) =>
    !searchFilter.trim()
      ? true
      : c.name.toLowerCase().includes(searchFilter.trim().toLowerCase()) ||
        c.iso.toLowerCase().includes(searchFilter.trim().toLowerCase())
  );
  $: ratedFiltered = filteredCountries.filter((c) => c.kind === 'rated');
  $: unratedFiltered = filteredCountries.filter((c) => c.kind === 'unrated');
  $: activeCountry = allCountries.find((c) => c.iso === selectedIso) ?? allCountries[0];

  function pickCountry(iso: string) {
    selectedIso = iso;
    localeDetected = false;
    openTooltip = null;
    const found = allCountries.find((c) => c.iso === iso);
    if (found) {
      setSelectedCountryForReadiness({
        iso: found.iso,
        name: found.name,
        kind: found.kind,
        checklistCount: found.kind === 'rated' ? found.checklistCount : undefined
      });
    }
    trackEvent('country_selected', { iso });
  }

  function toggleTip(id: 'offline' | 'catch' | 'pattern' | 'weak' | 'checklist') {
    openTooltip = openTooltip === id ? null : id;
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

<section id="country-check" class="country-section">
  <div class="section-wrap">
    <div class="section-head">
      <h2 class="sec-title">{$dict.country.heading}</h2>
      <p class="sec-sub">{$dict.country.subhead}</p>
    </div>

    {#if revealed}
      <!-- Picker Bar -->
      <div class="picker-shell">
      <div class="quick-row" role="group" aria-label="Example countries across world regions">
        {#each quickCountries as qc}
          <button
            type="button"
            class="quick-chip"
            class:selected={selectedIso === qc.iso}
            onclick={() => pickCountry(qc.iso)}
          >
            <span>{qc.name}</span>
            {#if qc.kind === 'unrated'}
              <span class="chip-unrated">Partial</span>
            {/if}
          </button>
        {/each}
      </div>

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
              <optgroup label="Rated Benchmark Nations (39)">
                {#each ratedFiltered as c}
                  <option value={c.iso}>{c.name} ({c.iso})</option>
                {/each}
              </optgroup>
            {/if}
            {#if unratedFiltered.length > 0}
              <optgroup label="Not Yet Rated in 39-Nation Index ({unratedFiltered.length})">
                {#each unratedFiltered as c}
                  <option value={c.iso}>{c.name} ({c.iso}) — Not yet rated</option>
                {/each}
              </optgroup>
            {/if}
          </select>
        </div>
      </div>

      {#if localeDetected}
        <p class="locale-note">Detected from your browser region or time zone — switch to any country above.</p>
      {/if}
    </div>

    <!-- Country Card Output -->
    {#if activeCountry && activeCountry.kind === 'rated'}
      <div class="rated-panel">
        <div class="rp-header">
          <div>
            <span class="rp-badge rated-badge">INCLUDED IN 39-NATION BENCHMARK · {activeCountry.region}</span>
            <h3 class="rp-name">{activeCountry.name}</h3>
          </div>
          <div class="rp-header-actions">
            <a href={`${base}/countries/${activeCountry.id}/`} class="btn-country-link">
              {$dict.country.openCountryCta} <span aria-hidden="true">&rarr;</span>
            </a>
          </div>
        </div>

        <!-- Plain Metrics Cards -->
        <div class="plain-metrics-grid">
          <!-- Offline Window -->
          <div class="pm-card">
            <div class="pm-top">
              <span class="pm-label">Days {activeCountry.name} keeps running without the cloud</span>
              <button type="button" class="tip-btn" onclick={() => toggleTip('offline')} aria-expanded={openTooltip === 'offline'}>
                ⓘ {$dict.country.techReadingLabel}
              </button>
            </div>
            <div class="pm-value">{activeCountry.cloudDaysText}</div>
            <div class="battery-bar" role="img" aria-label={`${activeCountry.batterySegments} out of 5 offline capacity bars`}>
              {#each [1, 2, 3, 4, 5] as seg}
                <span class="bat-seg" class:filled={seg <= activeCountry.batterySegments}></span>
              {/each}
            </div>
            {#if openTooltip === 'offline'}
              <p class="tip-drawer">Measured offline window: <strong>{activeCountry.tHalfH} hours</strong> before essential services fall behind without external cloud authentication.</p>
            {/if}
          </div>

          <!-- Catches the Breakthrough -->
          <div class="pm-card">
            <div class="pm-top">
              <span class="pm-label">Catches the breakthrough</span>
              <button type="button" class="tip-btn" onclick={() => toggleTip('catch')} aria-expanded={openTooltip === 'catch'}>
                ⓘ {$dict.country.techReadingLabel}
              </button>
            </div>
            <div
              class="pm-value"
              class:good={activeCountry.catchStatus === 'Easily'}
              class:mid={activeCountry.catchStatus === 'With effort'}
              class:warn={activeCountry.catchStatus === 'Struggles'}
            >
              {activeCountry.catchStatus}
            </div>
            <p class="pm-sub">
              {#if activeCountry.catchStatus === 'Easily'}
                Strong physical buffers hold even as systems accelerate.
              {:else if activeCountry.catchStatus === 'With effort'}
                Workable foundations, though a few key buffers lag software speed.
              {:else}
                Fast software adoption outpaces manual fallback capacity.
              {/if}
            </p>
            {#if openTooltip === 'catch'}
              <p class="tip-drawer">Adoption rank <strong>#{activeCountry.rankL1}</strong> vs. readiness floor rank <strong>#{activeCountry.rankL2}</strong> of 39 (shift: {activeCountry.rankDelta >= 0 ? `+${activeCountry.rankDelta}` : activeCountry.rankDelta}).</p>
            {/if}
          </div>

          <!-- Plain Country Pattern -->
          <div class="pm-card">
            <div class="pm-top">
              <span class="pm-label">Resilience style</span>
              <button type="button" class="tip-btn" onclick={() => toggleTip('pattern')} aria-expanded={openTooltip === 'pattern'}>
                ⓘ {$dict.country.techReadingLabel}
              </button>
            </div>
            <div class="pm-value">{activeCountry.plainPattern}</div>
            <p class="pm-sub">A clock that slows: relies on manual rules, skills, and physical backup capacity.</p>
            {#if openTooltip === 'pattern'}
              <p class="tip-drawer">{activeCountry.plainPatternTech}</p>
            {/if}
          </div>

          <!-- One Thing Most Likely to Hold Country Back -->
          <div class="pm-card">
            <div class="pm-top">
              <span class="pm-label">The one thing most likely to hold {activeCountry.name} back</span>
              <button type="button" class="tip-btn" onclick={() => toggleTip('weak')} aria-expanded={openTooltip === 'weak'}>
                ⓘ {$dict.country.techReadingLabel}
              </button>
            </div>
            <p class="pm-body-text">{activeCountry.weakestLinkPlain}</p>
            {#if openTooltip === 'weak'}
              <p class="tip-drawer">Primary bottleneck pillar in index: <strong>{activeCountry.weakestLinkTech}</strong>.</p>
            {/if}
          </div>
        </div>

        <!-- Simple 5-Thing Checklist -->
        <div class="checklist-box">
          <div class="cl-head">
            <div>
              <span class="cl-kicker">{$dict.country.checklistLabel}</span>
              <h4 class="cl-title">
                {#if $completedWishList.length > 0}
                  To receive &ldquo;{$completedWishList[$completedWishList.length - 1].wishTitle}&rdquo;, {activeCountry.name} currently has <strong>{activeCountry.checklistCount} of 5 things in place</strong>
                {:else}
                  To receive fast AI tools safely, {activeCountry.name} currently has <strong>{activeCountry.checklistCount} of 5 things in place</strong>
                {/if}
              </h4>
            </div>
            <button type="button" class="tip-btn" onclick={() => toggleTip('checklist')} aria-expanded={openTooltip === 'checklist'}>
              ⓘ How this checklist works
            </button>
          </div>

          {#if openTooltip === 'checklist'}
            <p class="tip-drawer cl-tip">
              Five transparent checks from published country figures: 72h offline backup plus 70/100 readability cutoffs across everyday infrastructure, public claim-checking skills, oversight governance, and an economic cushion floor (25/100). These cutoffs are editorial reading aids, not official model rankings.
            </p>
          {/if}

          <ul class="cl-items">
            {#each activeCountry.checklist as item}
              <li class:passed={item.pass}>
                <span class="cl-mark" aria-hidden="true">{item.pass ? '✓' : '○'}</span>
                <span class="cl-text">
                  <strong>{item.label}</strong>
                  <small>{item.metricNote}</small>
                </span>
              </li>
            {/each}
          </ul>

          <div class="lab-bridge-row">
            <a href={`${base}/sandbox/`} class="lab-bridge-link">{$dict.country.openLabCta} &rarr;</a>
          </div>
        </div>
      </div>
    {:else if activeCountry && activeCountry.kind === 'unrated'}
      <!-- Strictly Uniform Honest Display for ALL 109 Unrated / Context Countries -->
      <div class="unrated-panel">
        <div class="rp-header">
          <div>
            <span class="rp-badge unrated-badge">{$dict.country.unratedBadge}</span>
            <h3 class="rp-name">{activeCountry.name} <small class="iso-small">({activeCountry.iso})</small></h3>
          </div>
          <a href={`${base}/coverage/`} class="btn-country-link">
            {$dict.country.unratedHelpCta} <span aria-hidden="true">&rarr;</span>
          </a>
        </div>

        <div class="unrated-grid">
          <div class="ur-card">
            <span class="pm-label">What is observed today</span>
            <p class="pm-body-text">{activeCountry.observedSummary}</p>
          </div>
          <div class="ur-card">
            <span class="pm-label">Why no full score is shown yet</span>
            <p class="pm-body-text">{activeCountry.missingSummary}</p>
          </div>
        </div>

        <p class="ur-footnote">
          {activeCountry.coverageDetail} We never guess or invent country scores or readiness checklists where international survey data is missing.
        </p>
      </div>
    {/if}
    {:else}
      <noscript>
        <p class="ur-footnote">
          Explore all 148 countries in the <a href={`${base}/countries/`}>39-nation index</a> and <a href={`${base}/coverage/`}>global coverage audit</a>.
        </p>
      </noscript>
    {/if}
  </div>
</section>

<style>
  .country-section {
    contain: layout style;
    padding: clamp(1.75rem, 3.8vw, 3.25rem) 0;
    scroll-margin-top: 112px;
    background: var(--bg-surface-sunken);
    border-top: 1px solid var(--border-subtle);
    border-bottom: 1px solid var(--border-subtle);
    min-height: 620px;
  }

  .section-wrap {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 1.15rem;
  }

  .section-head {
    text-align: center;
    max-width: 700px;
    margin: 0 auto 1.25rem;
  }

  .sec-title {
    font-family: var(--font-family-sans);
    font-size: clamp(1.5rem, 3.2vw, 2.15rem);
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 0.5rem;
    line-height: 1.22;
    letter-spacing: -0.02em;
  }

  .sec-sub {
    font-size: 1.02rem;
    color: var(--text-secondary);
    margin: 0;
  }

  .picker-shell {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 1.25rem;
  }

  .quick-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-bottom: 0.85rem;
  }

  .quick-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-secondary);
    border-radius: 9999px;
    padding: 0.32rem 0.78rem;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    min-height: 34px;
  }

  .quick-chip:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .quick-chip.selected {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
    color: var(--btn-primary-text);
  }

  .chip-unrated {
    font-family: var(--font-family-mono);
    font-size: 0.64rem;
    opacity: 0.8;
    border-inline-start: 1px solid currentColor;
    padding-inline-start: 0.35rem;
  }

  .select-grid {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    gap: 0.65rem;
  }

  .search-input,
  .country-select {
    width: 100%;
    min-height: 44px;
    padding: 0.55rem 0.85rem;
    border-radius: 10px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface);
    color: var(--text-primary);
    font-size: 0.92rem;
    font-family: var(--font-family-sans);
  }

  .locale-note {
    margin: 0.6rem 0 0;
    font-size: 0.78rem;
    color: var(--accent-primary);
    font-weight: 600;
  }

  .rated-panel,
  .unrated-panel {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    padding: 1.35rem;
    box-shadow: var(--shadow-sm);
  }

  .rp-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.85rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid var(--border-subtle);
  }

  .rp-badge {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    padding: 0.22rem 0.6rem;
    border-radius: 6px;
    margin-bottom: 0.35rem;
  }

  .rated-badge {
    background: var(--threat-sovereign-bg);
    color: var(--threat-sovereign);
    border: 1px solid var(--threat-sovereign-border);
  }

  .unrated-badge {
    background: var(--threat-warning-bg);
    color: var(--threat-warning);
    border: 1px solid var(--threat-warning-border);
  }

  .rp-name {
    margin: 0;
    font-family: var(--font-family-sans);
    font-weight: 800;
    font-size: clamp(1.3rem, 2.4vw, 1.75rem);
    color: var(--text-primary);
    letter-spacing: -0.015em;
  }

  .iso-small {
    font-family: var(--font-family-mono);
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 500;
  }

  .btn-country-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    min-height: 42px;
    padding: 0.55rem 1.05rem;
    border-radius: 9px;
    background: var(--accent-primary);
    color: var(--btn-primary-text);
    text-decoration: none;
    font-weight: 700;
    font-size: 0.88rem;
  }

  .btn-country-link:hover {
    background: var(--accent-primary-hover);
  }

  .plain-metrics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.9rem;
    margin-bottom: 1.25rem;
  }

  .pm-card,
  .ur-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem;
  }

  .pm-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.5rem;
    margin-bottom: 0.45rem;
  }

  .pm-label {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--text-secondary);
  }

  .tip-btn {
    border: 1px solid var(--border-subtle);
    background: var(--bg-surface-sunken);
    color: var(--text-secondary);
    border-radius: 9999px;
    padding: 0.16rem 0.5rem;
    font-size: 0.7rem;
    font-weight: 600;
    cursor: pointer;
    flex-shrink: 0;
  }

  .tip-btn:hover {
    color: var(--accent-primary);
    border-color: var(--accent-primary);
  }

  .pm-value {
    font-family: var(--font-family-sans);
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 0.45rem;
  }

  .pm-value.good { color: var(--threat-sovereign); }
  .pm-value.mid { color: var(--threat-warning); }
  .pm-value.warn { color: var(--threat-critical); }

  .battery-bar {
    display: flex;
    gap: 0.35rem;
    max-width: 190px;
  }

  .bat-seg {
    height: 10px;
    flex: 1;
    border-radius: 3px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-medium);
  }

  .bat-seg.filled {
    background: var(--threat-sovereign);
    border-color: var(--threat-sovereign);
  }

  .pm-sub,
  .pm-body-text {
    margin: 0;
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .tip-drawer {
    margin: 0.65rem 0 0;
    padding: 0.55rem 0.75rem;
    border-radius: 8px;
    background: var(--bg-surface-sunken);
    border-inline-start: 3px solid var(--accent-primary);
    font-size: 0.79rem;
    color: var(--text-secondary);
    line-height: 1.45;
  }

  .checklist-box {
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 1.15rem;
  }

  .cl-head {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.5rem;
    margin-bottom: 0.85rem;
  }

  .cl-kicker {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--accent-primary);
    margin-bottom: 0.2rem;
  }

  .cl-title {
    margin: 0;
    font-size: 1.02rem;
    color: var(--text-primary);
    line-height: 1.35;
  }

  .cl-tip {
    margin-bottom: 0.85rem;
  }

  .cl-items {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.55rem;
  }

  .cl-items li {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    padding: 0.55rem 0.7rem;
    border-radius: 8px;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
  }

  .cl-items li.passed {
    border-color: var(--threat-sovereign-border);
    background: var(--threat-sovereign-bg);
  }

  .cl-mark {
    font-weight: 800;
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin-top: 1px;
  }

  .cl-items li.passed .cl-mark {
    color: var(--threat-sovereign);
  }

  .cl-text {
    display: flex;
    flex-direction: column;
    gap: 0.12rem;
  }

  .cl-text strong {
    font-size: 0.86rem;
    color: var(--text-primary);
  }

  .cl-text small {
    font-size: 0.74rem;
    color: var(--text-secondary);
  }

  .lab-bridge-row {
    margin-top: 0.9rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border-subtle);
    text-align: end;
  }

  .lab-bridge-link {
    font-size: 0.84rem;
    font-weight: 700;
    color: var(--accent-primary);
    text-decoration: none;
  }

  .lab-bridge-link:hover {
    text-decoration: underline;
  }

  .unrated-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.9rem;
    margin-bottom: 0.9rem;
  }

  .ur-footnote {
    margin: 0;
    font-size: 0.84rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
  }

  @media (max-width: 900px) {
    .country-section {
      min-height: 540px;
    }
  }

  @media (max-width: 720px) {
    .country-section {
      padding: 1.55rem 0;
      min-height: 920px;
    }
    .section-head {
      margin-bottom: 1rem;
    }
    .picker-shell {
      padding: 0.75rem 0.85rem;
      margin-bottom: 0.85rem;
    }
    .quick-row {
      flex-wrap: nowrap;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      gap: 0.4rem;
      margin-bottom: 0.65rem;
      padding-bottom: 0.2rem;
    }
    .quick-chip {
      flex: 0 0 auto;
      white-space: nowrap;
      padding: 0.28rem 0.68rem;
      font-size: 0.78rem;
      min-height: 36px;
    }
    .select-grid,
    .plain-metrics-grid,
    .cl-items,
    .unrated-grid {
      grid-template-columns: 1fr;
      gap: 0.55rem;
    }
    .rated-panel,
    .unrated-panel {
      padding: 0.9rem;
    }
    .rp-header {
      gap: 0.55rem;
      margin-bottom: 0.8rem;
      padding-bottom: 0.65rem;
    }
    .pm-card,
    .ur-card {
      padding: 0.75rem;
    }
    .pm-value {
      font-size: 1.18rem;
      margin-bottom: 0.28rem;
    }
    .checklist-box {
      padding: 0.85rem;
    }
    .cl-items li {
      padding: 0.45rem 0.6rem;
    }
  }
</style>
