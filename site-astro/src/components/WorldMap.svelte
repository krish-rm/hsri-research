<script lang="ts">
  // Import D3 for map rendering
  import { onMount } from 'svelte';

  // Props
  export let countries = [];
  export let currentView = 'world';
  export let onCountrySelect = null;

  // State
  let svgElement;
  let selectedCountry = null;

  // Mock map data - in a real implementation, you'd use proper geoJSON
  const mapData = {
    width: 800,
    height: 400,
    projection: 'mercator',
    countries: [
      // Simplified country data for demonstration
      { id: 'usa', name: 'United States', x: 150, y: 150, score: 78.5, band: 'A' },
      { id: 'can', name: 'Canada', x: 140, y: 120, score: 75.2, band: 'A' },
      { id: 'mex', name: 'Mexico', x: 130, y: 180, score: 58.3, band: 'C' },
      { id: 'gbr', name: 'United Kingdom', x: 400, y: 100, score: 76.8, band: 'A' },
      { id: 'fra', name: 'France', x: 420, y: 120, score: 72.4, band: 'B' },
      { id: 'deu', name: 'Germany', x: 430, y: 110, score: 74.6, band: 'A' },
      { id: 'ita', name: 'Italy', x: 430, y: 140, score: 68.9, band: 'B' },
      { id: 'esp', name: 'Spain', x: 410, y: 150, score: 65.7, band: 'C' },
      { id: 'rus', name: 'Russia', x: 550, y: 100, score: 62.1, band: 'C' },
      { id: 'chn', name: 'China', x: 600, y: 180, score: 71.8, band: 'B' },
      { id: 'jpn', name: 'Japan', x: 680, y: 150, score: 77.2, band: 'A' },
      { id: 'kor', name: 'South Korea', x: 680, y: 170, score: 76.5, band: 'A' },
      { id: 'ind', name: 'India', x: 580, y: 200, score: 55.4, band: 'C' },
      { id: 'aus', name: 'Australia', x: 680, y: 250, score: 74.3, band: 'A' },
      { id: 'bra', name: 'Brazil', x: 250, y: 250, score: 59.7, band: 'C' },
      { id: 'arg', name: 'Argentina', x: 220, y: 280, score: 56.8, band: 'C' },
      { id: 'zaf', name: 'South Africa', x: 450, y: 300, score: 52.3, band: 'D' },
      { id: 'nga', name: 'Nigeria', x: 400, y: 250, score: 43.2, band: 'D' },
      { id: 'egy', name: 'Egypt', x: 460, y: 180, score: 48.7, band: 'D' },
      { id: 'ken', name: 'Kenya', x: 450, y: 220, score: 41.5, band: 'D' },
    ]
  };

  // Color scale for score bands
  const scoreColors = {
    'A': '#10b981',  // Green
    'B': '#3b82f6',  // Blue
    'C': '#f59e0b',  // Yellow
    'D': '#ef4444',  // Red
    'F': '#991b1b'   // Dark Red
  };

  // Get color for country based on score band
  function getCountryColor(country) {
    if (!country) return '#e5e7eb'; // Gray for no data
    return scoreColors[country.band] || '#e5e7eb';
  }

  // Handle country click
  function handleCountryClick(country) {
    selectedCountry = country;
    if (onCountrySelect) {
      onCountrySelect(country.id);
    }
  }

  // Get tooltip text for country
  function getTooltip(country) {
    if (!country) return '';
    return `
      <div class="country-tooltip">
        <div class="tooltip-country-name">${country.name}</div>
        <div class="tooltip-score">Score: ${country.score}</div>
        <div class="tooltip-band">Band: ${country.band}</div>
      </div>
    `;
  }
</script>

<div class="world-map-container">
  <div class="map-controls">
    <div class="view-selector">
      <button class="view-btn {currentView === 'world' ? 'active' : ''}"
              onclick={() => currentView = 'world'}>
        World
      </button>
      <button class="view-btn {currentView === 'region' ? 'active' : ''}"
              onclick={() => currentView = 'region'}>
        Region
      </button>
      <button class="view-btn {currentView === 'country' ? 'active' : ''}"
              onclick={() => currentView = 'country'}>
        Country
      </button>
    </div>

    <div class="legend">
      <h4>Score Bands</h4>
      <div class="legend-items">
        {#each Object.entries(scoreColors) as [band, color]}
          <div class="legend-item">
            <div class="legend-color" style="background-color: {color}"></div>
            <span class="legend-label">Band {band}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <div class="map-viewport">
    <svg
      {svgElement}
      width={mapData.width}
      height={mapData.height}
      class="world-map"
      viewBox={`0 0 ${mapData.width} ${mapData.height}`}
    >
      <!-- Background -->
      <rect width={mapData.width} height={mapData.height} fill="#f3f4f6" />

      <!-- Grid lines -->
      <g class="grid-lines" opacity="0.1">
        <!-- Horizontal lines -->
        {#each Array.from({ length: 8 }, (_, i) => i * 50) as y}
          <line x1="0" y1={y} x2={mapData.width} y2={y} stroke="#94a3b8" stroke-width="1" />
        {/each}

        <!-- Vertical lines -->
        {#each Array.from({ length: 16 }, (_, i) => i * 50) as x}
          <line x1={x} y1="0" x2={x} y2={mapData.height} stroke="#94a3b8" stroke-width="1" />
        {/each}
      </g>

      <!-- Countries -->
      <g class="countries">
        {#each mapData.countries as country}
          <g
            class="country {selectedCountry?.id === country.id ? 'selected' : ''}"
            transform={`translate(${country.x}, ${country.y})`}
            onclick={() => handleCountryClick(country)}
          >
            <!-- Country shape (simplified as circle) -->
            <circle
              r="8"
              fill={getCountryColor(country)}
              stroke={selectedCountry?.id === country.id ? '#1e40af' : 'none'}
              stroke-width="2"
              class="country-shape"
            />

            <!-- Country label -->
            <text
              x="0"
              y="20"
              text-anchor="middle"
              font-size="10"
              fill="#374151"
              class="country-label"
            >
              {country.code}
            </text>
          </g>
        {/each}
      </g>

      <!-- Interactive hover areas -->
      <g class="hover-areas">
        {#each mapData.countries as country}
          <circle
            cx={country.x}
            cy={country.y}
            r="15"
            fill="transparent"
            onmouseover={() => {
              // Show tooltip
            }}
            onmouseout={() => {
              // Hide tooltip
            }}
          />
        {/each}
      </g>
    </svg>

    <!-- Tooltip -->
    {#if selectedCountry}
      <div class="map-tooltip"
           style="left: {selectedCountry.x + 20}px; top: {selectedCountry.y - 20}px;">
        {@html getTooltip(selectedCountry)}
      </div>
    {/if}
  </div>
</div>

<style>
  .world-map-container {
    background-color: white;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .map-controls {
    background-color: var(--surface-color);
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .view-selector {
    display: flex;
    gap: var(--spacing-sm);
  }

  .view-btn {
    padding: var(--spacing-xs) var(--spacing-md);
    border: 1px solid var(--border-color);
    background-color: white;
    border-radius: 0.375rem;
    font-size: var(--font-size-sm);
    cursor: pointer;
    transition: all 0.2s;
  }

  .view-btn:hover {
    background-color: var(--surface-color);
  }

  .view-btn.active {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
  }

  .legend {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .legend h4 {
    margin: 0;
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: var(--text-primary);
  }

  .legend-items {
    display: flex;
    gap: var(--spacing-md);
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
  }

  .legend-color {
    width: 16px;
    height: 16px;
    border-radius: 0.25rem;
    border: 1px solid var(--border-color);
  }

  .legend-label {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .map-viewport {
    position: relative;
    padding: var(--spacing-md);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 500px;
  }

  .world-map {
    max-width: 100%;
    height: auto;
  }

  .country {
    cursor: pointer;
    transition: transform 0.2s;
  }

  .country:hover {
    transform: scale(1.1);
  }

  .country.selected .country-shape {
    stroke: #1e40af;
    stroke-width: 3;
  }

  .country-shape {
    transition: all 0.2s;
  }

  .country-label {
    pointer-events: none;
    user-select: none;
  }

  .map-tooltip {
    position: absolute;
    background-color: white;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    padding: var(--spacing-sm);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 10;
    pointer-events: none;
  }

  .country-tooltip {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .tooltip-country-name {
    font-weight: 600;
    font-size: var(--font-size-sm);
  }

  .tooltip-score, .tooltip-band {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .map-controls {
      flex-direction: column;
      gap: var(--spacing-md);
      align-items: flex-start;
    }

    .legend-items {
      flex-wrap: wrap;
    }

    .map-viewport {
      padding: var(--spacing-sm);
    }

    .world-map {
      max-width: 100%;
    }
  }
</style>