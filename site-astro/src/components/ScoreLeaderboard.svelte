<script lang="ts">
  // Props
  export let countries = [];
  export let sortBy = 'score';
  export let ascending = false;

  // State
  let sortColumn = sortBy;
  let sortDirection = ascending ? 'asc' : 'desc';

  // Sort countries
  $: sortedCountries = [...countries].sort((a, b) => {
    let valueA, valueB;

    if (sortColumn === 'score') {
      valueA = a.score;
      valueB = b.score;
    } else if (sortColumn === 'name') {
      valueA = a.name;
      valueB = b.name;
    } else if (sortColumn === 'exposure') {
      valueA = a.exposure;
      valueB = b.exposure;
    } else {
      valueA = a[sortColumn];
      valueB = b[sortColumn];
    }

    // Handle numeric vs string comparison
    if (typeof valueA === 'number' && typeof valueB === 'number') {
      return sortDirection === 'asc' ? valueA - valueB : valueB - valueA;
    } else {
      const comparison = String(valueA).localeCompare(String(valueB));
      return sortDirection === 'asc' ? comparison : -comparison;
    }
  });

  // Handle column header click
  function handleSort(column) {
    if (sortColumn === column) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sortColumn = column;
      sortDirection = 'desc';
    }
  }

  // Get score band class
  function getScoreBandClass(score) {
    if (score >= 80) return 'score-band-a';
    if (score >= 70) return 'score-band-b';
    if (score >= 60) return 'score-band-c';
    if (score >= 50) return 'score-band-d';
    return 'score-band-f';
  }

  // Format number
  function formatNumber(num) {
    return num.toFixed(1);
  }
</script>

<div class="score-leaderboard">
  <div class="leaderboard-header">
    <h3>Top Countries</h3>
    <div class="sort-info">
      Sorted by {sortColumn} ({sortDirection})
    </div>
  </div>

  <table class="leaderboard-table">
    <thead>
      <tr>
        <th class="rank">Rank</th>
        <th class="country" onclick={() => handleSort('name')}>
          Country
          {#if sortColumn === 'name'}
            <span class="sort-icon">{sortDirection === 'asc' ? '↑' : '↓'}</span>
          {/if}
        </th>
        <th class="score" onclick={() => handleSort('score')}>
          HSRI Score
          {#if sortColumn === 'score'}
            <span class="sort-icon">{sortDirection === 'asc' ? '↑' : '↓'}</span>
          {/if}
        </th>
        <th class="band">Band</th>
        <th class="exposure" onclick={() => handleSort('exposure')}>
          Exposure
          {#if sortColumn === 'exposure'}
            <span class="sort-icon">{sortDirection === 'asc' ? '↑' : '↓'}</span>
          {/if}
        </th>
        <th class="peer-group">Peer Group</th>
        <th class="updated">Updated</th>
      </tr>
    </thead>
    <tbody>
      {#each sortedCountries as country, index}
        <tr class="country-row">
          <td class="rank">#{index + 1}</td>
          <td class="country">
            <div class="country-info">
              <div class="country-name">{country.name}</div>
              <div class="country-code">{country.code}</div>
            </div>
          </td>
          <td class="score">
            <div class="score-value {getScoreBandClass(country.score)}">
              {formatNumber(country.score)}
            </div>
          </td>
          <td class="band">
            <span class="band-badge {getScoreBandClass(country.score)}">
              {country.band}
            </span>
          </td>
          <td class="exposure">
            <div class="exposure-bar">
              <div class="exposure-fill" style="width: {country.exposure}%"></div>
            </div>
            <div class="exposure-value">{formatNumber(country.exposure)}%</div>
          </td>
          <td class="peer-group">{country.peerGroup}</td>
          <td class="updated">{country.lastUpdated}</td>
        </tr>
      {/each}
    </tbody>
  </table>

  <div class="leaderboard-footer">
    <div class="table-info">
      Showing {sortedCountries.length} of {countries.length} countries
    </div>
  </div>
</div>

<style>
  .score-leaderboard {
    background-color: white;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .leaderboard-header {
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .leaderboard-header h3 {
    margin: 0;
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--text-primary);
  }

  .sort-info {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }

  .leaderboard-table {
    width: 100%;
    border-collapse: collapse;
  }

  .leaderboard-table th {
    background-color: var(--surface-color);
    padding: var(--spacing-md);
    text-align: left;
    font-weight: 600;
    font-size: var(--font-size-sm);
    color: var(--text-primary);
    cursor: pointer;
    user-select: none;
    transition: background-color 0.2s;
  }

  .leaderboard-table th:hover {
    background-color: #f1f5f9;
  }

  .leaderboard-table td {
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--border-color);
    font-size: var(--font-size-sm);
  }

  .rank {
    font-weight: 600;
    color: var(--text-secondary);
    width: 60px;
  }

  .country {
    width: 25%;
  }

  .country-info {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .country-name {
    font-weight: 500;
    color: var(--text-primary);
  }

  .country-code {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    text-transform: uppercase;
  }

  .score {
    width: 100px;
    text-align: center;
  }

  .score-value {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: 0.25rem;
    font-weight: 600;
    font-size: var(--font-size-base);
  }

  .band {
    width: 80px;
    text-align: center;
  }

  .band-badge {
    display: inline-block;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: 0.25rem;
    font-weight: 600;
    font-size: var(--font-size-sm);
    text-transform: uppercase;
  }

  .exposure {
    width: 150px;
  }

  .exposure-bar {
    width: 100%;
    height: 6px;
    background-color: var(--border-color);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: var(--spacing-xs);
  }

  .exposure-fill {
    height: 100%;
    background-color: var(--accent-color);
    border-radius: 3px;
    transition: width 0.3s ease;
  }

  .exposure-value {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .peer-group {
    width: 20%;
    color: var(--text-secondary);
  }

  .updated {
    width: 120px;
    color: var(--text-secondary);
    font-size: var(--font-size-xs);
  }

  .sort-icon {
    margin-left: var(--spacing-xs);
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .country-row:hover {
    background-color: var(--surface-color);
  }

  .country-row:last-child td {
    border-bottom: none;
  }

  .leaderboard-footer {
    padding: var(--spacing-md) var(--spacing-lg);
    border-top: 1px solid var(--border-color);
    background-color: var(--surface-color);
  }

  .table-info {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    text-align: center;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .leaderboard-header {
      flex-direction: column;
      gap: var(--spacing-sm);
      align-items: flex-start;
    }

    .leaderboard-table {
      font-size: var(--font-size-xs);
    }

    .leaderboard-table th,
    .leaderboard-table td {
      padding: var(--spacing-sm);
    }

    .country {
      width: 30%;
    }

    .country-name {
      font-size: var(--font-size-sm);
    }

    .country-code {
      font-size: 10px;
    }

    .exposure {
      width: 100px;
    }

    .exposure-bar {
      display: none;
    }

    .peer-group {
      display: none;
    }

    .updated {
      display: none;
    }
  }

  @media (max-width: 480px) {
    .leaderboard-table {
      display: block;
      overflow-x: auto;
      white-space: nowrap;
    }

    .leaderboard-table th,
    .leaderboard-table td {
      white-space: nowrap;
    }

    .country {
      width: 20%;
    }

    .country-info {
      flex-direction: row;
      gap: var(--spacing-xs);
      align-items: center;
    }

    .country-code {
      font-size: 10px;
    }
  }
</style>