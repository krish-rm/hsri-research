<script lang="ts">
  // State
  let selectedScenario = 'all';
  let startYear = 2026;
  let endYear = 2040;
  let currentYear = 2026;
  let timelineData = [];

  // Initialize timeline data
  $: initializeTimeline();

  function initializeTimeline() {
    // Generate mock timeline data
    timelineData = [];
    for (let year = startYear; year <= endYear; year++) {
      timelineData.push({
        year,
        plateau: calculateProbability(year, 'plateau'),
        steady: calculateProbability(year, 'steady'),
        takeoff: calculateProbability(year, 'takeoff')
      });
    }
  }

  // Calculate probability based on scenario
  function calculateProbability(year, scenario) {
    const baseYear = startYear;
    const totalYears = endYear - startYear;
    const yearProgress = (year - baseYear) / totalYears;

    switch (scenario) {
      case 'plateau':
        // Gradual increase with plateaus
        if (yearProgress < 0.2) return 5 + yearProgress * 10;
        if (yearProgress < 0.4) return 10 + (yearProgress - 0.2) * 15;
        if (yearProgress < 0.6) return 20 + (yearProgress - 0.4) * 10;
        if (yearProgress < 0.8) return 25 + (yearProgress - 0.6) * 25;
        return 40 + (yearProgress - 0.8) * 60;

      case 'steady':
        // Consistent exponential growth
        return Math.min(95, 3 * Math.exp(yearProgress * 3.5));

      case 'takeoff':
        // Slow start, rapid acceleration
        if (yearProgress < 0.6) return yearProgress * 5;
        return Math.min(95, 10 + (yearProgress - 0.6) * 200);

      default:
        return 0;
    }
  }

  // Scenario handler
  function selectScenario(scenario) {
    selectedScenario = scenario;
  }

  // Year handlers
  function updateStartYear(year) {
    startYear = parseInt(year);
    initializeTimeline();
  }

  function updateEndYear(year) {
    endYear = parseInt(year);
    initializeTimeline();
  }

  function updateCurrentYear(year) {
    currentYear = parseInt(year);
  }
</script>

<div class="timeline-explorer">
  <div class="timeline-controls">
    <div class="scenario-selector">
      <h3>Select Scenario</h3>
      <div class="scenario-buttons">
        <button
          class="scenario-btn {selectedScenario === 'all' ? 'active' : ''}"
          onclick={selectScenario.bind(null, 'all')}
        >
          All Scenarios
        </button>
        <button
          class="scenario-btn {selectedScenario === 'plateau' ? 'active' : ''}"
          onclick={selectScenario.bind(null, 'plateau')}
        >
          Plateau
        </button>
        <button
          class="scenario-btn {selectedScenario === 'steady' ? 'active' : ''}"
          onclick={selectScenario.bind(null, 'steady')}
        >
          Steady Progress
        </button>
        <button
          class="scenario-btn {selectedScenario === 'takeoff' ? 'active' : ''}"
          onclick={selectScenario.bind(null, 'takeoff')}
        >
          Takeoff
        </button>
      </div>
    </div>

    <div class="time-controls">
      <h3>Timeline Settings</h3>
      <div class="time-options">
        <div class="time-option">
          <label>Start Year:</label>
          <select
            on:change={(e) => updateStartYear(parseInt(e.target.value))}
            bind:value={startYear}
          >
            <option>2025</option>
            <option selected>2026</option>
            <option>2027</option>
          </select>
        </div>
        <div class="time-option">
          <label>End Year:</label>
          <select
            on:change={(e) => updateEndYear(parseInt(e.target.value))}
            bind:value={endYear}
          >
            <option>2030</option>
            <option selected>2035</option>
            <option>2040</option>
            <option>2045</option>
          </select>
        </div>
        <div class="time-option">
          <label>Current Year:</label>
          <input
            type="number"
            bind:value={currentYear}
            min={startYear}
            max={endYear}
            on:change={(e) => updateCurrentYear(parseInt(e.target.value))}
          />
        </div>
      </div>
    </div>
  </div>

  <div class="timeline-chart">
    <canvas id="timelineChart"></canvas>
  </div>

  <div class="timeline-legend">
    <div class="legend-item" style="background-color: #10b981;">
      <span>Plateau Scenario</span>
    </div>
    <div class="legend-item" style="background-color: #3b82f6;">
      <span>Steady Progress</span>
    </div>
    <div class="legend-item" style="background-color: #f59e0b;">
      <span>Takeoff Scenario</span>
    </div>
    <div class="legend-item" style="background-color: #1e40af;">
      <span>Current Year</span>
    </div>
  </div>

  <div class="milestone-markers">
    {#each timelineData as data, i}
      {data.year === 2026 && (
        <div class="milestone-marker" style="left: `${(2026 - startYear) / (endYear - startYear) * 100}%`">
          <div class="milestone-dot"></div>
          <div class="milestone-label">2026</div>
        </div>
      )}
    {/each}
  </div>
</div>

<style>
  .timeline-explorer {
    width: 100%;
    margin-top: var(--spacing-xl);
  }

  .timeline-controls {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-xl);
    margin-bottom: var(--spacing-2xl);
  }

  .scenario-selector,
  .time-controls {
    background-color: white;
    padding: var(--spacing-lg);
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .scenario-selector h3,
  .time-controls h3 {
    margin: 0 0 var(--spacing-md) 0;
    font-size: var(--font-size-base);
  }

  .scenario-buttons {
    display: flex;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
  }

  .scenario-btn {
    padding: var(--spacing-sm) var(--spacing-lg);
    border: 1px solid var(--border-color);
    background-color: white;
    border-radius: 0.375rem;
    font-size: var(--font-size-sm);
    cursor: pointer;
    transition: all 0.2s;
  }

  .scenario-btn:hover {
    background-color: var(--surface-color);
  }

  .scenario-btn.active {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
  }

  .time-options {
    display: grid;
    gap: var(--spacing-md);
  }

  .time-option {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .time-option label {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    min-width: 80px;
  }

  .time-option select,
  .time-option input {
    padding: var(--spacing-xs);
    border: 1px solid var(--border-color);
    border-radius: 0.25rem;
    font-size: var(--font-size-sm);
  }

  .timeline-chart {
    background-color: white;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    padding: var(--spacing-lg);
    height: 400px;
    position: relative;
  }

  #timelineChart {
    width: 100%;
    height: 100%;
  }

  .timeline-legend {
    display: flex;
    justify-content: center;
    gap: var(--spacing-lg);
    margin-top: var(--spacing-lg);
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: 0.25rem;
    background-color: var(--surface-color);
  }

  .legend-item span {
    font-size: var(--font-size-sm);
  }

  .milestone-markers {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
  }

  .milestone-marker {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
  }

  .milestone-dot {
    width: 10px;
    height: 10px;
    background-color: #1e40af;
    border-radius: 50%;
    margin: 0 auto var(--spacing-xs);
  }

  .milestone-label {
    background-color: #1e40af;
    color: white;
    padding: 2px var(--spacing-xs);
    border-radius: 0.125rem;
    font-size: var(--font-size-xs);
    white-space: nowrap;
  }

  @media (max-width: 1024px) {
    .timeline-controls {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 768px) {
    .scenario-buttons {
      flex-direction: column;
    }

    .time-options {
      grid-template-columns: 1fr;
    }

    .time-option {
      flex-direction: column;
      align-items: flex-start;
    }

    .timeline-legend {
      flex-wrap: wrap;
    }
  }
</style>