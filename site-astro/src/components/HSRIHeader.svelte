<script lang="ts">
  // Component state
  let isMenuOpen = false;

  const base = (import.meta.env.BASE_URL || '/').replace(/\/$/, '');

  // Navigation items
  const navItems = [
    { name: 'Home', href: base || '/' },
    { name: 'Countries', href: `${base}/countries` },
    { name: 'Methodology', href: `${base}/methodology` },
    { name: 'Timeline', href: `${base}/timeline` },
    { name: 'Compare', href: `${base}/compare` },
    { name: 'Data', href: `${base}/data` },
  ];

  // Quick stats
  const stats = {
    totalCountries: 195,
    ratedCountries: 86,
    avgScore: 62.4,
    lastUpdated: '2026-09-20',
  };
</script>

<header class="hsri-header">
  <div class="container">
    <div class="header-content">
      <!-- Logo and Title -->
      <a href={base || '/'} class="header-brand" style="text-decoration: none; color: inherit;">
        <svg class="logo" width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="20" cy="20" r="19" stroke="var(--primary-color)" stroke-width="2"/>
          <path d="M20 5 L15 15 L5 20 L15 25 L20 35 L25 25 L35 20 L25 15 Z" fill="var(--primary-color)" opacity="0.8"/>
          <circle cx="20" cy="20" r="8" fill="white"/>
        </svg>
        <div class="brand-text">
          <h1 class="site-title">HSRI</h1>
          <p class="site-tagline">Human Superintelligence Readiness Index</p>
        </div>
      </a>

      <!-- Navigation -->
      <nav class="main-nav" role="navigation">
        <ul class="nav-list">
          {#each navItems as item}
            <li class="nav-item">
              <a href={item.href} class="nav-link">
                {item.name}
              </a>
            </li>
          {/each}
        </ul>

        <!-- Mobile menu button -->
        <button
          class="mobile-menu-button"
          onclick={() => isMenuOpen = !isMenuOpen}
          aria-label="Toggle navigation menu"
          aria-expanded={isMenuOpen}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12h18M3 6h18M3 18h18" />
          </svg>
        </button>
      </nav>
    </div>

    <!-- Stats bar -->
    <div class="stats-bar">
      <div class="stats-container">
        <div class="stat-item">
          <span class="stat-label">Countries Rated</span>
          <span class="stat-value">{stats.ratedCountries}/{stats.totalCountries}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Average Score</span>
          <span class="stat-value">{stats.avgScore}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Last Updated</span>
          <span class="stat-value">{stats.lastUpdated}</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Mobile menu -->
  {#if isMenuOpen}
    <div class="mobile-menu" role="dialog" aria-modal="true">
      <ul class="mobile-nav-list">
        {#each navItems as item}
          <li class="mobile-nav-item">
            <a href={item.href} class="mobile-nav-link">
              {item.name}
            </a>
          </li>
        {/each}
      </ul>
    </div>
  {/if}
</header>

<style>
  .hsri-header {
    background-color: white;
    border-bottom: 2px solid var(--border-color);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md) 0;
  }

  .header-brand {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .logo {
    flex-shrink: 0;
  }

  .brand-text {
    display: flex;
    flex-direction: column;
  }

  .site-title {
    margin: 0;
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: var(--primary-color);
  }

  .site-tagline {
    margin: 0;
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
  }

  .main-nav {
    display: flex;
    align-items: center;
  }

  .nav-list {
    display: flex;
    gap: var(--spacing-lg);
    margin: 0;
    padding: 0;
    list-style: none;
  }

  .nav-link {
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
    padding: var(--spacing-xs) 0;
    position: relative;
  }

  .nav-link:hover {
    color: var(--accent-color);
  }

  .nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background-color: var(--accent-color);
    transition: width 0.2s;
  }

  .nav-link:hover::after {
    width: 100%;
  }

  .mobile-menu-button {
    display: none;
    background: none;
    border: none;
    padding: var(--spacing-sm);
    cursor: pointer;
    color: var(--text-primary);
  }

  .stats-bar {
    background-color: var(--surface-color);
    border-top: 1px solid var(--border-color);
    padding: var(--spacing-sm) 0;
  }

  .stats-container {
    display: flex;
    justify-content: center;
    gap: var(--spacing-xl);
  }

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .stat-label {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-xs);
  }

  .stat-value {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--primary-color);
  }

  /* Mobile styles */
  @media (max-width: 768px) {
    .header-content {
      flex-direction: column;
      gap: var(--spacing-md);
    }

    .main-nav {
      width: 100%;
      justify-content: space-between;
    }

    .nav-list {
      display: none;
    }

    .mobile-menu-button {
      display: block;
    }

    .stats-container {
      flex-direction: row;
      gap: var(--spacing-lg);
      font-size: var(--font-size-sm);
    }

    .stats-bar {
      padding: var(--spacing-md) 0;
    }

    .mobile-menu {
      position: fixed;
      top: 100%;
      left: 0;
      right: 0;
      background-color: white;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      padding: var(--spacing-lg);
      z-index: 50;
    }

    .mobile-nav-list {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: var(--spacing-md);
    }

    .mobile-nav-link {
      color: var(--text-primary);
      text-decoration: none;
      font-size: var(--font-size-lg);
      font-weight: 500;
    }
  }
</style>