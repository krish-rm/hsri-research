<script lang="ts">
  // Props
  export let timelineData;
  export let currentYear = 2026;

  // State
  let selectedScenario = 'all';
  let showDetails = false;

  // Calculate crossing years for different scenarios
  $: crossingYears = {
    plateau: timelineData?.forecasts?.plateau?.find(p => p.probability >= 0.5)?.year || null,
    steady: timelineData?.forecasts?.steady?.find(s => s.probability >= 0.5)?.year || null,
    takeoff: timelineData?.forecasts?.takeoff?.find(t => t.probability >= 0.5)?.year || null
  };

  $: capLevels = timelineData?.capabilityLevels || {
    '2026': 'A',
    '2028': 'B',
    '2030': 'C',
    '2032': 'D',
    '2035': 'E',
    '2040': 'F'
  };

  // Format year
  function formatYear(year) {
    return year.toString();
  }

  // Get scenario color
  function getScenarioColor(scenario) {
    const colors = {
      plateau: '#10b981',  // Green
      steady: '#3b82f6',  // Blue
      takeoff: '#f59e0b'   // Orange/Amber
    };
    return colors[scenario] || '#6b7280';
  }

  // Get scenario name
  function getScenarioName(scenario) {
    const names = {
      plateau: 'Plateau Scenario',
      steady: 'Steady Progress Scenario',
      takeoff: 'Takeoff Scenario'
    };
    return names[scenario] || scenario;
  }

  // Get scenario for level (mock implementation)
  function getScenarioForLevel(level) {
    const mapping = {
      'A': 'takeoff',
      'B': 'steady',
      'C': 'plateau',
      'D': 'plateau',
      'F': 'plateau'
    };
    return mapping[level] || 'plateau';
  }

  // Get capability level description
  function getCapabilityDescription(level) {
    const descriptions = {
      'A': 'Advanced - Systems capable of autonomous reasoning and adaptation',
      'B': 'Intermediate - Systems with specialized capabilities requiring human oversight',
      'C': 'Basic - Current generation AI with narrow domain applications',
      'D': 'Limited - Early-stage AI with constrained functionality',
      'F': 'Very Limited - No functional AI systems'
    };
    return descriptions[level] || 'Unknown';
  }
</script>

<div class="timeline-preview">
  <div class="timeline-header">
    <h3>Superintelligence Timeline Projections</h3>
    <div class="timeline-controls">
      <div class="scenario-selector">
        <button
          class="scenario-btn {selectedScenario === 'all' ? 'active' : ''}"
          onclick={() => selectedScenario = 'all'}
        >
          All Scenarios
        </button>
        <button
          class="scenario-btn {selectedScenario === 'plateau' ? 'active' : ''}"
          onclick={() => selectedScenario = 'plateau'}
          style="background-color: {getScenarioColor('plateau')}"
        >
          Plateau
        </button>
        <button
          class="scenario-btn {selectedScenario === 'steady' ? 'active' : ''}"
          onclick={() => selectedScenario = 'steady'}
          style="background-color: {getScenarioColor('steady')}"
        >
          Steady
        </button>
        <button
          class="scenario-btn {selectedScenario === 'takeoff' ? 'active' : ''}"
          onclick={() => selectedScenario = 'takeoff'}
          style="background-color: {getScenarioColor('takeoff')}"
        >
          Takeoff
        </button>
      </div>

      <button class="details-btn" onclick={() => showDetails = !showDetails}>
        {showDetails ? 'Hide' : 'Show'} Details
      </button>
    </div>
  </div>

  <div class="timeline-content">
    <!-- Two clocks visualization -->
    <div class="two-clocks">
      <div class="clock-container">
        <h4>Capability Timeline</h4>
        <div class="clock">
          <div class="clock-face">
            <!-- Current year marker -->
            <div class="year-marker" style="left: {((currentYear - 2020) / 20) * 100}%">
              {currentYear}
            </div>

            <!-- Capability levels -->
            {#each Object.entries(capLevels) as [year, level], index}
              <div class="capability-level"
                   style="left: {((parseInt(year) - 2020) / 20) * 100}%;
                          border-color: {getScenarioColor(getScenarioForLevel(level))}">
                <span class="level-{level.toLowerCase()}">{level}</span>
                <span class="year-label">{year}</span>
              </div>
            {/each}

            <!-- Center -->
            <div class="clock-center"></div>
          </div>
        </div>

        <div class="clock-legend">
          <div class="legend-item">
            <span class="level-a">A</span>
            <span>Advanced</span>
          </div>
          <div class="legend-item">
            <span class="level-b">B</span>
            <span>Intermediate</span>
          </div>
          <div class="legend-item">
            <span class="level-c">C</span>
            <span>Basic</span>
          </div>
          <div class="legend-item">
            <span class="level-d">D</span>
            <span>Limited</span>
          </div>
          <div class="legend-item">
            <span class="level-f">F</span>
            <span>None</span>
          </div>
        </div>
      </div>

      <div class="clock-container">
        <h4>Probability Timeline</h4>
        <div class="probability-chart">
          <div class="chart-axis">
            <div class="y-axis">
              <span>100%</span>
              <span>75%</span>
              <span>50%</span>
              <span>25%</span>
              <span>0%</span>
            </div>
            <div class="x-axis">
              <span>2025</span>
              <span>2030</span>
              <span>2035</span>
              <span>2040</span>
            </div>
          </div>

          <div class="chart-area">
            <!-- Grid lines -->
            {#each [0, 25, 50, 75, 100] as y}
              <div class="grid-line" style="bottom: {y}%"></div>
            {/each}

            <!-- Forecast lines -->
            {#if selectedScenario === 'all' || selectedScenario === 'plateau'}
              <div class="forecast-line"
                   style="stroke: {getScenarioColor('plateau')}">
                {#each timelineData.forecasts.plateau as point}
                  <div class="data-point"
                       style="left: {((point.year - 2025) / 15) * 100}%;
                              bottom: {point.probability}%"
                       data-year={point.year}
                       data-probability={point.probability}>
                  </div>
                {/each}
              </div>
            {/if}

            {#if selectedScenario === 'all' || selectedScenario === 'steady'}
              <div class="forecast-line"
                   style="stroke: {getScenarioColor('steady')}">
                {#each timelineData.forecasts.steady as point}
                  <div class="data-point"
                       style="left: {((point.year - 2025) / 15) * 100}%;
                              bottom: {point.probability}%"
                       data-year={point.year}
                       data-probability={point.probability}>
                  </div>
                {/each}
              </div>
            {/if}

            {#if selectedScenario === 'all' || selectedScenario === 'takeoff'}
              <div class="forecast-line"
                   style="stroke: {getScenarioColor('takeoff')}">
                {#each timelineData.forecasts.takeoff as point}
                  <div class="data-point"
                       style="left: {((point.year - 2025) / 15) * 100}%;
                              bottom: {point.probability}%"
                       data-year={point.year}
                       data-probability={point.probability}>
                  </div>
                {/each}
              </div>
            {/if}

            <!-- 50% threshold line -->
            <div class="threshold-line"></div>
          </div>
        </div>

        <div class="forecast-legend">
          {#if selectedScenario === 'all'}
            <div class="legend-scenario" style="background-color: {getScenarioColor('plateau')}">
              {getScenarioName('plateau')}
            </div>
            <div class="legend-scenario" style="background-color: {getScenarioColor('steady')}">
              {getScenarioName('steady')}
            </div>
            <div class="legend-scenario" style="background-color: {getScenarioColor('takeoff')}">
              {getScenarioName('takeoff')}
            </div>
          {:else}
            <div class="legend-scenario" style="background-color: {getScenarioColor(selectedScenario)}">
              {getScenarioName(selectedScenario)}
            </div>
          {/if}
        </div>
      </div>
    </div>

    <!-- Crossing years summary -->
    {#if showDetails}
      <div class="crossing-summary">
        <h5>Crossing Years (50% Probability Threshold)</h5>
        <div class="crossing-grid">
          <div class="crossing-item" style="border-color: {getScenarioColor('plateau')}">
            <div class="scenario-header">
              <span class="scenario-name">{getScenarioName('plateau')}</span>
              <span class="scenario-year">{crossingYears.plateau || 'Not reached'}</span>
            </div>
            <p class="scenario-description">
              Gradual improvement with plateaus at each capability level. Most conservative timeline.
            </p>
          </div>

          <div class="crossing-item" style="border-color: {getScenarioColor('steady')}">
            <div class="scenario-header">
              <span class="scenario-name">{getScenarioName('steady')}</span>
              <span class="scenario-year">{crossingYears.steady || 'Not reached'}</span>
            </div>
            <p class="scenario-description">
              Consistent progress without major acceleration. Moderate timeline.
            </p>
          </div>

          <div class="crossing-item" style="border-color: {getScenarioColor('takeoff')}">
            <div class="scenario-header">
              <span class="scenario-name">{getScenarioName('takeoff')}</span>
              <span class="scenario-year">{crossingYears.takeoff || 'Not reached'}</span>
            </div>
            <p class="scenario-description">
              Rapid acceleration once certain thresholds are crossed. Most aggressive timeline.
            </p>
          </div>
        </div>
      </div>
    {/if}

    <!-- Current status -->
    <div class="current-status">
      <h5>Current Status ({currentYear})</h5>
      <div class="status-grid">
        <div class="status-item">
          <span class="status-label">Capability Level:</span>
          <span class="status-value level-{(capLevels[currentYear] || 'A').toLowerCase()}">
            {capLevels[currentYear] || 'Level A'}
          </span>
        </div>
        <div class="status-item">
          <span class="status-label">Time to Level A:</span>
          <span class="status-value">
            {capLevels[currentYear] === 'A' ? 'Current Frontier' :
             capLevels[currentYear] === 'B' ? '~2 years' :
             capLevels[currentYear] === 'C' ? '~4 years' :
             capLevels[currentYear] === 'D' ? '~6 years' :
             '2035+'}
          </span>
        </div>
        <div class="status-item" title="No formal statistical confidence interval has been computed from empirical data yet. Capability crossing years reflect exploratory scenario projections.">
          <span class="status-label">Confidence Interval:</span>
          <span class="status-value" style="font-size: 0.85rem; color: #64748b;">Not yet computed (exploratory projection)</span>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .timeline-preview {
    background-color: white;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .timeline-header {
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .timeline-header h3 {
    margin: 0;
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--text-primary);
  }

  .timeline-controls {
    display: flex;
    gap: var(--spacing-md);
    align-items: center;
  }

  .scenario-selector {
    display: flex;
    gap: var(--spacing-xs);
    background-color: var(--surface-color);
    padding: var(--spacing-xs);
    border-radius: 0.375rem;
  }

  .scenario-btn {
    padding: var(--spacing-xs) var(--spacing-md);
    border: none;
    border-radius: 0.25rem;
    background: none;
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }

  .scenario-btn:hover {
    background-color: rgba(0, 0, 0, 0.05);
  }

  .scenario-btn.active {
    background-color: white;
    color: var(--primary-color);
    font-weight: 500;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .details-btn {
    padding: var(--spacing-xs) var(--spacing-md);
    border: 1px solid var(--border-color);
    background-color: white;
    border-radius: 0.375rem;
    font-size: var(--font-size-sm);
    cursor: pointer;
    transition: all 0.2s;
    color: var(--text-primary);
  }

  .details-btn:hover {
    background-color: var(--surface-color);
  }

  .timeline-content {
    padding: var(--spacing-lg);
  }

  .two-clocks {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-2xl);
    margin-bottom: var(--spacing-2xl);
  }

  .clock-container {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .clock-container h4 {
    margin: 0;
    font-size: var(--font-size-base);
    font-weight: 600;
    color: var(--text-primary);
  }

  .clock {
    position: relative;
    width: 100%;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .clock-face {
    position: relative;
    width: 280px;
    height: 280px;
    border: 2px solid var(--border-color);
    border-radius: 50%;
    background-color: var(--surface-color);
  }

  .year-marker {
    position: absolute;
    top: -10px;
    transform: translateX(-50%);
    background-color: var(--primary-color);
    color: white;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: 0.25rem;
    font-size: var(--font-size-sm);
    font-weight: 600;
    white-space: nowrap;
  }

  .capability-level {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-xs);
  }

  .capability-level span {
    font-weight: 600;
    font-size: var(--font-size-lg);
  }

  .level-a { color: #10b981; }
  .level-b { color: #3b82f6; }
  .level-c { color: #f59e0b; }
  .level-d { color: #ef4444; }
  .level-f { color: #991b1b; }

  .year-label {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .clock-center {
    position: absolute;
    width: 12px;
    height: 12px;
    background-color: var(--primary-color);
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .clock-legend {
    display: flex;
    justify-content: center;
    gap: var(--spacing-lg);
    padding: var(--spacing-sm);
    background-color: var(--surface-color);
    border-radius: 0.375rem;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    font-size: var(--font-size-xs);
  }

  .legend-item span:first-child {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-color);
    border-radius: 0.25rem;
  }

  .probability-chart {
    position: relative;
    width: 100%;
    height: 300px;
    background-color: var(--surface-color);
    border-radius: 0.5rem;
    border: 1px solid var(--border-color);
  }

  .chart-axis {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    right: 0;
    pointer-events: none;
  }

  .y-axis {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 40px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: var(--spacing-sm) 0;
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .x-axis {
    position: absolute;
    left: 40px;
    right: 20px;
    bottom: 0;
    display: flex;
    justify-content: space-between;
    padding-bottom: var(--spacing-sm);
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .chart-area {
    position: absolute;
    left: 40px;
    right: 20px;
    top: 20px;
    bottom: 40px;
  }

  .grid-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 1px;
    background-color: var(--border-color);
  }

  .forecast-line {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    pointer-events: none;
  }

  .forecast-line::before {
    content: '';
    position: absolute;
    left: 0;
    right: 0;
    height: 2px;
    background-color: currentColor;
    opacity: 0.5;
  }

  .data-point {
    position: absolute;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: currentColor;
    transform: translate(-50%, 50%);
    border: 2px solid white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    pointer-events: all;
    cursor: pointer;
  }

  .data-point:hover {
    transform: translate(-50%, 50%) scale(1.5);
  }

  .threshold-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 1px;
    background-color: var(--text-secondary);
    opacity: 0.5;
    bottom: 50%;
  }

  .forecast-legend {
    display: flex;
    justify-content: center;
    gap: var(--spacing-md);
    padding: var(--spacing-sm);
    background-color: var(--surface-color);
    border-radius: 0.375rem;
  }

  .legend-scenario {
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: 0.25rem;
    color: white;
    font-size: var(--font-size-xs);
    font-weight: 500;
  }

  .crossing-summary {
    margin-bottom: var(--spacing-2xl);
  }

  .crossing-summary h5 {
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-base);
  }

  .crossing-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-md);
  }

  .crossing-item {
    padding: var(--spacing-lg);
    background-color: var(--surface-color);
    border-radius: 0.5rem;
    border: 1px solid var(--border-color);
    border-left: 4px solid;
  }

  .scenario-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-sm);
  }

  .scenario-name {
    font-weight: 600;
    font-size: var(--font-size-sm);
  }

  .scenario-year {
    font-weight: 700;
    font-size: var(--font-size-base);
    color: var(--primary-color);
  }

  .scenario-description {
    font-size: var(--font-size-sm);
    line-height: 1.5;
    color: var(--text-secondary);
    margin: 0;
  }

  .current-status {
    padding: var(--spacing-lg);
    background-color: var(--surface-color);
    border-radius: 0.5rem;
    border: 1px solid var(--border-color);
  }

  .current-status h5 {
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-base);
  }

  .status-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-md);
  }

  .status-item {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .status-label {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .status-value {
    font-weight: 600;
    font-size: var(--font-size-sm);
  }

  .status-value.level-a { color: #10b981; }
  .status-value.level-b { color: #3b82f6; }
  .status-value.level-c { color: #f59e0b; }
  .status-value.level-d { color: #ef4444; }
  .status-value.level-f { color: #991b1b; }

  /* Responsive adjustments */
  @media (max-width: 1024px) {
    .two-clocks {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 768px) {
    .timeline-header {
      flex-direction: column;
      gap: var(--spacing-md);
      align-items: flex-start;
    }

    .timeline-controls {
      flex-direction: column;
      width: 100%;
    }

    .scenario-selector {
      width: 100%;
      justify-content: space-between;
    }

    .crossing-grid {
      grid-template-columns: 1fr;
    }

    .status-grid {
      grid-template-columns: 1fr;
    }

    .clock {
      height: 250px;
    }

    .clock-face {
      width: 230px;
      height: 230px;
    }
  }

  @media (max-width: 480px) {
    .timeline-content {
      padding: var(--spacing-md);
    }

    .clock-face {
      width: 200px;
      height: 200px;
    }

    .probability-chart {
      height: 250px;
    }
  }
</style>