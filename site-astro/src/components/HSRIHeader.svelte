<script lang="ts">
  import { onMount } from 'svelte';

  export let currentPath = '';

  // Component state
  let isMenuOpen = false;
  let isScrolled = false;

  function toggleMenu(event?: Event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    isMenuOpen = !isMenuOpen;
  }

  function closeMenu() {
    isMenuOpen = false;
  }

  const base = (import.meta.env.BASE_URL || '/').replace(/\/$/, '');

  // Navigation items
  const navItems = [
    { name: 'Home', href: `${base}/` },
    { name: 'Countries', href: `${base}/countries/` },
    { name: 'Seismograph', href: `${base}/seismograph/` },
    { name: 'Scenarios', href: `${base}/scenarios/` },
    { name: 'Experiments', href: `${base}/experiments/` },
    { name: 'Methodology', href: `${base}/methodology/` },
    { name: 'Research', href: `${base}/research-updates/` },
    { name: 'Timeline', href: `${base}/timeline/` },
    { name: 'Compare', href: `${base}/compare/` },
    { name: 'Data', href: `${base}/data/` },
  ];

  // Quick stats - reconciled authoritative definitions
  const stats = {
    totalCountries: 195,
    benchmarkRatedCountries: 39,
    unratedEvaluatedCountries: 86,
    avgScore: 53.8,
    avgCoverage: 96.5,
    lastUpdated: '2026-09-22',
  };

  onMount(() => {
    if (typeof window !== 'undefined') {
      currentPath = window.location.pathname;

      const handleScroll = () => {
        isScrolled = window.scrollY > 20;
      };

      window.addEventListener('scroll', handleScroll, { passive: true });
      handleScroll();

      return () => {
        window.removeEventListener('scroll', handleScroll);
      };
    }
  });

  function isActive(href: string): boolean {
    if (!currentPath) return false;
    const p = currentPath.replace(/\/$/, '') || '/';
    const h = href.replace(/\/$/, '') || '/';

    if (h === '/' || h === base || h === `${base}/`) {
      return p === '/' || p === base;
    }
    return p === h || p.startsWith(h + '/');
  }
</script>

<header class="hsri-header">
  <div class="header-outer-container">
    <div class="header-content">
      <!-- Logo and Title shifted to the left edge -->
      <a href={`${base}/`} class="header-brand" style="text-decoration: none; color: inherit;">
        <svg class="logo" width="38" height="38" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="20" cy="20" r="19" stroke="var(--primary-color)" stroke-width="2"/>
          <path d="M20 5 L15 15 L5 20 L15 25 L20 35 L25 25 L35 20 L25 15 Z" fill="var(--primary-color)" opacity="0.8"/>
          <circle cx="20" cy="20" r="8" fill="white"/>
        </svg>
        <div class="brand-text">
          <h1 class="site-title">HSRI</h1>
          <p class="site-tagline">Human Superintelligence Readiness Index</p>
        </div>
      </a>

      <!-- Navigation spans horizontally to the right of brand with ample space -->
      <nav class="main-nav" role="navigation">
        <ul class="nav-list">
          {#each navItems as item}
            <li class="nav-item">
              <a
                href={item.href}
                class="nav-link"
                class:active={isActive(item.href)}
                aria-current={isActive(item.href) ? 'page' : undefined}
              >
                {item.name}
              </a>
            </li>
          {/each}
        </ul>

        <!-- Mobile menu button -->
        <button
          type="button"
          class="mobile-menu-button"
          on:click={toggleMenu}
          aria-label={isMenuOpen ? "Close navigation menu" : "Open navigation menu"}
          aria-expanded={isMenuOpen}
        >
          {#if isMenuOpen}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          {:else}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          {/if}
        </button>
      </nav>
    </div>

    <!-- Stats bar: Disappears smoothly on scroll -->
    <div class="stats-bar" class:hidden-on-scroll={isScrolled}>
      <div class="stats-container">
        <div class="stat-item" title="39 of 195 recognized nations benchmarked (OECD/high-income preview cohort; 86 unrated in coverage audit)">
          <span class="stat-label">Benchmark Scope</span>
          <span class="stat-value">{stats.benchmarkRatedCountries}/{stats.totalCountries} <small style="font-size: 0.72rem; font-weight: normal; opacity: 0.85;">(86 unrated)</small></span>
        </div>
        <div class="stat-item" title="Empirical mean across the 39 rated benchmark nations">
          <span class="stat-label">Benchmark Mean</span>
          <span class="stat-value">{stats.avgScore} <small style="font-size: 0.72rem; font-weight: normal; opacity: 0.85;">/ 100</small></span>
        </div>
        <div class="stat-item" title="Empirical data completeness across 17 retained indicators in the 39 benchmark nations">
          <span class="stat-label">Data Completeness</span>
          <span class="stat-value">{stats.avgCoverage}% <small style="font-size: 0.72rem; font-weight: normal; opacity: 0.85;">(Harmonized)</small></span>
        </div>
        <div class="stat-item" title="Early-stage preview release. Indicators and coverage unverified.">
          <span class="stat-label">Index Status</span>
          <span class="stat-value" style="display: flex; align-items: center; gap: 4px;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #f59e0b;"></span>
            <span style="font-size: 0.85rem; color: #92400e;">Preview Release</span>
          </span>
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
            <a
              href={item.href}
              class="mobile-nav-link"
              class:active={isActive(item.href)}
              on:click={closeMenu}
            >
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
    background-color: #ffffff;
    border-bottom: 2px solid var(--border-color);
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    width: 100%;
  }

  /* Full-width container shifting brand to the left and eliminating cutoffs */
  .header-outer-container {
    width: 100%;
    max-width: 100%;
    padding: 0 1.5rem;
    box-sizing: border-box;
  }

  .header-content {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: clamp(1rem, 2vw, 2.5rem);
    padding: 0.65rem 0;
    width: 100%;
    box-sizing: border-box;
  }

  .header-brand {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    flex-shrink: 0;
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
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--primary-color);
    line-height: 1.1;
    letter-spacing: -0.02em;
  }

  .site-tagline {
    margin: 0;
    font-size: 0.72rem;
    color: var(--text-secondary);
    white-space: nowrap;
    line-height: 1.2;
  }

  .main-nav {
    display: flex;
    align-items: center;
    flex: 1;
    justify-content: flex-start;
    min-width: 0;
  }

  .nav-list {
    display: flex;
    align-items: center;
    gap: clamp(0.35rem, 0.85vw, 1.1rem);
    margin: 0;
    padding: 0;
    list-style: none;
    flex-wrap: nowrap;
  }

  .nav-item {
    flex-shrink: 0;
  }

  .nav-link {
    color: #475569;
    text-decoration: none;
    font-weight: 500;
    font-size: clamp(0.85rem, 0.92vw, 0.95rem);
    white-space: nowrap;
    transition: all 0.2s ease;
    padding: 0.35rem 0.55rem;
    border-radius: 6px;
    position: relative;
    display: inline-block;
  }

  .nav-link:hover {
    color: var(--primary-color);
    background-color: rgba(30, 64, 175, 0.05);
  }

  /* Active Tab Highlighting */
  .nav-link.active {
    color: var(--primary-color);
    font-weight: 700;
    background-color: rgba(30, 64, 175, 0.09);
  }

  .nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0.55rem;
    right: 0.55rem;
    height: 2.5px;
    background-color: var(--primary-color);
    border-radius: 2px;
    transform: scaleX(0);
    transition: transform 0.2s ease;
  }

  .nav-link:hover::after {
    transform: scaleX(0.7);
  }

  .nav-link.active::after {
    transform: scaleX(1);
    background-color: var(--primary-color);
  }

  .mobile-menu-button {
    display: none;
    background: none;
    border: none;
    padding: var(--spacing-sm);
    cursor: pointer;
    color: var(--text-primary);
    margin-left: auto;
  }

  /* Disappearing stats bar on scroll */
  .stats-bar {
    background-color: var(--surface-color);
    border-top: 1px solid var(--border-color);
    padding: 0.5rem 0;
    transition: max-height 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                opacity 0.22s ease,
                padding 0.28s ease,
                border-color 0.2s ease;
    max-height: 80px;
    opacity: 1;
    overflow: hidden;
  }

  .stats-bar.hidden-on-scroll {
    max-height: 0;
    opacity: 0;
    padding-top: 0;
    padding-bottom: 0;
    border-top: 1px solid transparent;
    pointer-events: none;
  }

  .stats-container {
    display: flex;
    justify-content: center;
    gap: clamp(1rem, 3.5vw, var(--spacing-xl));
  }

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .stat-label {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    margin-bottom: 2px;
  }

  .stat-value {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--primary-color);
  }

  /* Mobile & Tablet styles */
  @media (max-width: 1024px) {
    .header-content {
      justify-content: space-between;
    }

    .main-nav {
      flex: none;
    }

    .nav-list {
      display: none;
    }

    .mobile-menu-button {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0.5rem;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: #f8fafc;
      cursor: pointer;
    }

    .mobile-menu-button:hover,
    .mobile-menu-button:focus {
      background: #f1f5f9;
      outline: none;
    }

    .stats-bar {
      padding: 0.4rem 0;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }

    .stats-container {
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      gap: 1.25rem;
      font-size: 0.8rem;
      min-width: max-content;
      padding: 0 0.5rem;
    }

    .mobile-menu {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background-color: #ffffff;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.18), 0 4px 10px rgba(0, 0, 0, 0.08);
      border-bottom: 2px solid var(--border-color);
      padding: 1.25rem 1.5rem;
      z-index: 9999;
      display: block;
    }

    .mobile-nav-list {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .mobile-nav-item {
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 0.35rem;
    }

    .mobile-nav-item:last-child {
      border-bottom: none;
      padding-bottom: 0;
    }

    .mobile-nav-link {
      color: var(--text-primary);
      text-decoration: none;
      font-size: 1.05rem;
      font-weight: 600;
      display: block;
      padding: 0.35rem 0.5rem;
      border-radius: 6px;
    }

    .mobile-nav-link.active {
      color: var(--primary-color);
      background-color: rgba(30, 64, 175, 0.09);
      font-weight: 700;
    }

    .mobile-nav-link:hover {
      color: var(--primary-color);
    }
  }
</style>
