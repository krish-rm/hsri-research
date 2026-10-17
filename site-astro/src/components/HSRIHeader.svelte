<script lang="ts">
  import { onMount } from 'svelte';

  export let currentPath = '';

  // ── Types ──────────────────────────────────────────────────────────
  type NavChild = { name: string; href: string; desc: string; external?: boolean };
  type NavGroup = { name: string; href?: string; live?: boolean; badge?: string; children?: NavChild[] };
  type PrimaryItem = { name: string; href: string; badge?: string; live?: boolean };

  // ── Config — THE SINGLE SOURCE OF TRUTH ─────────────────────────
  // Primary = foveal, always visible on desktop. Max 3.
  const primaryNav: PrimaryItem[] = [
    { name: 'Monograph', href: '/monograph/', badge: 'ESSAY' },
    { name: 'Country Index', href: '/countries/' },
    { name: 'Seismograph', href: '/seismograph/', live: true },
  ];

  // Secondary dropdown — progressive disclosure for Persona C
  const utilityGroup: NavGroup = {
    name: 'Science & Data',
    children: [
      { name: 'Methodology', href: '/methodology/', desc: 'Leontief engine & formal proofs' },
      { name: 'Data & Coverage', href: '/data/', desc: 'Indicators & downloads' },
      { name: 'Research Log', href: '/research-updates/', desc: 'Updates & preprints' },
      { name: 'Scenario Atlas', href: '/scenarios/', desc: '26 takeoff simulations' },
      { name: 'DOI 10.5281/zenodo.10842000', href: 'https://doi.org/10.5281/zenodo.10842000', desc: 'Permanent record — CC BY-SA 4.0', external: true },
    ],
  };

  const base = (import.meta.env.BASE_URL || '/').replace(/\/$/, '');
  const withBase = (href: string) => {
    if (href.startsWith('http')) return href;
    if (!base) return href;
    return href.startsWith('/') ? `${base}${href}` : `${base}/${href}`;
  };

  // ── State ─────────────────────────────────────────────────────────
  let isMenuOpen = false;
  let isUtilityOpen = false;
  let isUtilityMobileOpen = false;
  let isScrolled = false;
  let currentTheme: 'dark' | 'light' = 'dark';

  let utilityTriggerEl: HTMLButtonElement | null = null;
  let utilityMenuEl: HTMLDivElement | null = null;

  function toggleMenu(e?: Event) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    isMenuOpen = !isMenuOpen;
    if (!isMenuOpen) isUtilityMobileOpen = false;
  }
  function closeMenu() { isMenuOpen = false; isUtilityMobileOpen = false; }
  function toggleUtility() { isUtilityOpen = !isUtilityOpen; }
  function closeUtility() { isUtilityOpen = false; }

  // ── Theme ─────────────────────────────────────────────────────────
  function initTheme() {
    if (typeof window === 'undefined') return;
    const saved = localStorage.getItem('hsri-theme') as 'dark' | 'light' | null;
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    currentTheme = saved ?? (prefersDark ? 'dark' : 'dark');
    document.documentElement.setAttribute('data-theme', currentTheme);
  }
  function toggleTheme() {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    if (typeof window !== 'undefined') {
      document.documentElement.setAttribute('data-theme', currentTheme);
      localStorage.setItem('hsri-theme', currentTheme);
    }
  }

  // ── Active matching ───────────────────────────────────────────────
  function isActive(href: string): boolean {
    if (!currentPath) return false;
    const p = currentPath.replace(/\/$/, '') || '/';
    const h = href.replace(/\/$/, '') || '/';
    const fullH = withBase(href).replace(/\/$/, '') || '/';
    if (h === '/' || h === base || fullH === '/') {
      return p === '/' || p === base || p === '';
    }
    return p === h || p === fullH || p.startsWith(h + '/') || p.startsWith(fullH + '/');
  }
  function isGroupActive(children?: NavChild[]): boolean {
    if (!children) return false;
    return children.some(c => !c.external && isActive(c.href));
  }

  // ── A11y: click outside + Escape + focus management ──────────────
  function onWindowClick(e: MouseEvent) {
    if (!isUtilityOpen) return;
    const t = e.target as Node;
    if (utilityTriggerEl?.contains(t) || utilityMenuEl?.contains(t)) return;
    closeUtility();
  }
  function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') {
      if (isUtilityOpen) { closeUtility(); utilityTriggerEl?.focus(); }
      if (isMenuOpen) closeMenu();
    }
  }

  onMount(() => {
    initTheme();
    if (typeof window !== 'undefined') {
      if (!currentPath) {
        currentPath = window.location.pathname;
      }
      const onScroll = () => { isScrolled = window.scrollY > 20; };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
      return () => window.removeEventListener('scroll', onScroll);
    }
  });
</script>

<svelte:window on:click={onWindowClick} on:keydown={onKeydown} />

<header class="hsri-header">
  <div class="header-outer-container">
    <div class="header-content">
      <!-- Brand — sole Home affordance -->
      <a href={withBase('/')} class="header-brand" aria-label="HSRI — Home">
        <svg class="logo" width="38" height="38" viewBox="0 0 40 40" fill="none" aria-hidden="true">
          <circle cx="20" cy="20" r="19" stroke="var(--primary-color)" stroke-width="2"/>
          <path d="M20 5 L15 15 L5 20 L15 25 L20 35 L25 25 L35 20 L25 15 Z" fill="var(--primary-color)" opacity="0.8"/>
          <circle cx="20" cy="20" r="8" fill="white"/>
        </svg>
        <div class="brand-text">
          <h1 class="site-title">HSRI</h1>
          <p class="site-tagline">Human Superintelligence Readiness Index</p>
        </div>
      </a>

      <!-- Desktop Primary Nav — 3 pillars -->
      <nav class="main-nav" aria-label="Primary">
        <ul class="nav-list">
          {#each primaryNav as item}
            <li class="nav-item">
              <a
                href={withBase(item.href)}
                class="nav-link"
                class:active={isActive(item.href)}
                class:live-link={item.live}
                aria-current={isActive(item.href) ? 'page' : undefined}
              >
                {#if item.live}<span class="live-dot" aria-hidden="true"></span>{/if}
                {item.name}
                {#if item.live}<span class="live-label">LIVE</span>{/if}
                {#if item.badge}<span class="nav-badge">{item.badge}</span>{/if}
              </a>
            </li>
          {/each}

          <!-- Utility dropdown — desktop -->
          <li class="nav-item utility-item">
            <button
              bind:this={utilityTriggerEl}
              type="button"
              class="nav-link utility-trigger"
              class:active={isGroupActive(utilityGroup.children) || isUtilityOpen}
              aria-haspopup="true"
              aria-expanded={isUtilityOpen}
              aria-controls="utility-menu"
              on:click={toggleUtility}
            >
              {utilityGroup.name}
              <span class="chevron" class:open={isUtilityOpen} aria-hidden="true">▾</span>
            </button>

            {#if isUtilityOpen}
              <div
                bind:this={utilityMenuEl}
                id="utility-menu"
                class="utility-menu"
                role="menu"
              >
                {#each utilityGroup.children ?? [] as child}
                  <a
                    href={withBase(child.href)}
                    class="utility-link"
                    role="menuitem"
                    target={child.external ? '_blank' : undefined}
                    rel={child.external ? 'noopener noreferrer' : undefined}
                    on:click={closeUtility}
                  >
                    <span class="utility-name">
                      {child.name}
                      {#if child.external}<span aria-hidden="true" class="ext">↗</span>{/if}
                    </span>
                    <span class="utility-desc">{child.desc}</span>
                  </a>
                {/each}
              </div>
            {/if}
          </li>
        </ul>

        <!-- Divider + Theme -->
        <span class="nav-divider" aria-hidden="true"></span>

        <button type="button" class="theme-toggle-btn" on:click={toggleTheme}
          aria-label={`Switch to ${currentTheme === 'dark' ? 'light' : 'dark'} mode`}>
          {#if currentTheme === 'dark'}
            <svg class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="12" cy="12" r="5"/>
              <line x1="12" y1="1" x2="12" y2="3"/>
              <line x1="12" y1="21" x2="12" y2="23"/>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
              <line x1="1" y1="12" x2="3" y2="12"/>
              <line x1="21" y1="12" x2="23" y2="12"/>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
            </svg>
            <span class="theme-label">LIGHT</span>
          {:else}
            <svg class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
            </svg>
            <span class="theme-label">DARK</span>
          {/if}
        </button>

        <!-- Hamburger — only <768px -->
        <button type="button" class="mobile-menu-button" on:click={toggleMenu}
          aria-label={isMenuOpen ? 'Close navigation' : 'Open navigation'} aria-expanded={isMenuOpen}>
          {#if isMenuOpen}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          {:else}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <line x1="3" y1="12" x2="21" y2="12"/>
              <line x1="3" y1="6" x2="21" y2="6"/>
              <line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          {/if}
        </button>
      </nav>
    </div>

    <!-- Stats bar — desktop only, hides on scroll -->
    <div class="stats-bar" class:hidden-on-scroll={isScrolled}>
      <div class="stats-container">
        <div class="stat-item"><span class="stat-label">Benchmark Scope</span><span class="stat-value">39 <small>Nations</small></span></div>
        <div class="stat-item"><span class="stat-label">Benchmark Mean</span><span class="stat-value">53.8 <small>/ 100</small></span></div>
        <div class="stat-item"><span class="stat-label">Data Completeness</span><span class="stat-value">84.6% <small>Harmonized</small></span></div>
        <div class="stat-item"><span class="stat-label">Index Status</span><span class="stat-value" style="display:flex;align-items:center;gap:6px;"><span class="status-dot"></span><span style="font-size:0.85rem;color:#92400e;">Preview Release</span></span></div>
      </div>
    </div>
  </div>

  <!-- Mobile Drawer -->
  {#if isMenuOpen}
    <div class="mobile-menu" role="dialog" aria-modal="true" aria-label="Navigation">
      <ul class="mobile-nav-list">
        {#each primaryNav as item}
          <li class="mobile-nav-item">
            <a href={withBase(item.href)} class="mobile-nav-link" class:active={isActive(item.href)} on:click={closeMenu}>
              {#if item.live}<span class="live-dot" aria-hidden="true"></span>{/if}
              {item.name}
              {#if item.live}<span class="live-label">LIVE</span>{/if}
              {#if item.badge}<span class="nav-badge">{item.badge}</span>{/if}
            </a>
          </li>
        {/each}

        <!-- Mobile accordion for Science & Data -->
        <li class="mobile-nav-item mobile-accordion">
          <button type="button" class="mobile-accordion-trigger" on:click={() => (isUtilityMobileOpen = !isUtilityMobileOpen)} aria-expanded={isUtilityMobileOpen}>
            <span>{utilityGroup.name}</span>
            <span class="chevron" class:open={isUtilityMobileOpen} aria-hidden="true">▾</span>
          </button>
          {#if isUtilityMobileOpen}
            <ul class="mobile-sub-list">
              {#each utilityGroup.children ?? [] as child}
                <li>
                  <a href={withBase(child.href)} class="mobile-sub-link" target={child.external ? '_blank' : undefined} rel={child.external ? 'noopener noreferrer' : undefined} on:click={closeMenu}>
                    <span>{child.name}</span><span class="sub-desc">{child.desc}</span>
                  </a>
                </li>
              {/each}
            </ul>
          {/if}
        </li>

        <li class="mobile-nav-item mobile-theme-item">
          <button type="button" class="mobile-theme-btn" on:click={toggleTheme}>
            <span>Theme: <strong>{currentTheme.toUpperCase()}</strong></span>
            <span class="theme-pill-action">{currentTheme === 'dark' ? 'Switch to Light' : 'Switch to Dark'}</span>
          </button>
        </li>
      </ul>
    </div>
  {/if}
</header>

<style>
  /* ── Header shell ── */
  .hsri-header{
    background-color: var(--bg-surface-elevated, #0f172a);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border-subtle, rgba(226, 232, 240, 0.15));
    position: sticky; top: 0; z-index: 1000;
    box-shadow: var(--shadow-sm); width: 100%;
    transition: background-color 0.25s ease, border-color 0.25s ease;
  }
  .header-outer-container{ width: 100%; max-width: 100%; padding: 0 1.5rem; box-sizing: border-box; }
  .header-content{ display: flex; justify-content: flex-start; align-items: center; gap: clamp(1rem, 2vw, 2.5rem); padding: 0.65rem 0; width: 100%; box-sizing: border-box; }
  .header-brand{ display: flex; align-items: center; gap: 0.65rem; flex-shrink: 0; text-decoration: none; color: inherit; }
  .logo{ flex-shrink: 0; }
  .brand-text{ display: flex; flex-direction: column; }
  .site-title{ margin: 0; font-size: 1.4rem; font-weight: 800; color: var(--primary-color); line-height: 1.1; letter-spacing: -0.02em; }
  .site-tagline{ margin: 0; font-size: 0.72rem; color: var(--text-secondary); white-space: nowrap; line-height: 1.2; }

  /* ── Primary nav ── */
  .main-nav{ display: flex; align-items: center; flex: 1; justify-content: flex-start; min-width: 0; }
  .nav-list{ display: flex; align-items: center; gap: clamp(0.35rem, 0.85vw, 1.1rem); margin: 0; padding: 0; list-style: none; white-space: nowrap; }
  .nav-item{ flex-shrink: 0; position: relative; }
  .utility-item{ position: relative; }

  .nav-link{
    color: var(--text-secondary); text-decoration: none; font-weight: 500;
    font-size: clamp(0.85rem, 0.92vw, 0.95rem); white-space: nowrap;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    padding: 0.35rem 0.55rem; border-radius: 6px; position: relative; display: inline-flex; align-items: center; gap: 6px;
    border: 1px solid transparent; background: transparent; cursor: pointer; font-family: inherit;
  }
  .nav-link:hover{ color: var(--text-primary); background-color: var(--bg-surface-elevated); }
  .nav-link.active{ color: var(--accent-primary); font-weight: 700; background-color: var(--accent-primary-glow); }
  .nav-link::after{
    content: ''; position: absolute; bottom: -2px; left: 0.55rem; right: 0.55rem; height: 2.5px;
    background-color: var(--primary-color); border-radius: 2px; transform: scaleX(0); transition: transform 0.2s ease;
  }
  .nav-link:hover::after{ transform: scaleX(0.7); }
  .nav-link.active::after{ transform: scaleX(1); background-color: var(--primary-color); }

  /* Live dot */
  .live-dot{ width: 6px; height: 6px; border-radius: 50%; background: #ef4444; display: inline-block; flex-shrink: 0;
    box-shadow: 0 0 0 0 rgba(239,68,68,0.7); animation: pulseDot 2s infinite; }
  @keyframes pulseDot{
    0%{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239,68,68,0.7); }
    70%{ transform: scale(1); box-shadow: 0 0 0 6px rgba(239,68,68,0); }
    100%{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239,68,68,0); }
  }
  .live-label{ font-family: var(--font-family-mono, monospace); font-size: 0.62rem; font-weight: 800; letter-spacing: 0.08em; color: var(--threat-critical, #ef4444); margin-left: 2px; }
  .nav-badge{ font-family: var(--font-family-mono, monospace); font-size: 0.58rem; font-weight: 800; letter-spacing: 0.06em; color: #fff; background: var(--accent-primary); padding: 1px 5px; border-radius: 9999px; line-height: 1.4; }

  /* Utility trigger */
  .utility-trigger{ gap: 4px; }
  .chevron{ font-size: 0.65rem; transition: transform 0.2s ease; display: inline-block; }
  .chevron.open{ transform: rotate(180deg); }

  /* Divider before theme */
  .nav-divider{ width: 1px; height: 22px; background: var(--border-subtle, rgba(226, 232, 240, 0.2)); margin: 0 0.35rem 0 0.65rem; flex-shrink: 0; }

  /* Utility dropdown */
  .utility-menu{
    position: absolute; top: calc(100% + 10px); right: 0; min-width: 300px;
    background: var(--bg-surface-elevated, #ffffff);
    border: 1px solid var(--border-subtle, #e2e8f0);
    border-radius: 12px;
    box-shadow: var(--shadow-lg, 0 10px 25px -5px rgba(0,0,0,0.2));
    padding: 6px;
    display: flex; flex-direction: column; gap: 2px;
    z-index: 1001;
  }
  .utility-link{
    display: flex; flex-direction: column; gap: 1px;
    padding: 9px 12px; border-radius: 8px; text-decoration: none;
    transition: background 0.15s ease;
  }
  .utility-link:hover{ background: var(--bg-surface-sunken, #f8fafc); }
  .utility-name{ font-size: 0.88rem; font-weight: 600; color: var(--text-primary); display: inline-flex; align-items: center; gap: 4px; }
  .utility-desc{ font-size: 0.73rem; color: var(--text-muted, #64748b); font-weight: 400; }
  .ext{ font-size: 0.7rem; opacity: 0.7; }

  /* Theme */
  .theme-toggle-btn{
    display: inline-flex; align-items: center; gap: 0.45rem; margin-left: 0.25rem; padding: 0.35rem 0.65rem; border-radius: 6px;
    background-color: var(--bg-surface-elevated); border: 1px solid var(--border-medium); color: var(--text-secondary);
    font-family: var(--font-family-mono, monospace); font-size: 0.70rem; font-weight: 700; letter-spacing: 0.08em; cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1); flex-shrink: 0;
  }
  .theme-toggle-btn:hover{ color: var(--text-primary); border-color: var(--accent-primary); box-shadow: 0 0 10px -2px var(--accent-primary-glow); }
  .theme-icon{ width: 14px; height: 14px; }

  /* Hamburger — hidden on desktop */
  .mobile-menu-button{ display: none; background: none; border: none; padding: var(--spacing-sm); cursor: pointer; color: var(--text-primary); margin-left: auto; }

  /* Stats bar */
  .stats-bar{
    background-color: var(--surface-color); border-top: 1px solid var(--border-color); padding: 0.5rem 0;
    transition: max-height 0.28s cubic-bezier(0.4,0,0.2,1), opacity 0.22s ease, padding 0.28s ease, border-color 0.28s ease;
    max-height: 80px; opacity: 1; overflow: hidden;
  }
  .stats-bar.hidden-on-scroll{ max-height: 0; opacity: 0; padding-top: 0; padding-bottom: 0; border-top: 1px solid transparent; pointer-events: none; }
  .stats-container{ display: flex; justify-content: center; gap: clamp(1rem, 3.5vw, var(--spacing-xl)); align-items: center; }
  .stat-item{ display: flex; flex-direction: column; align-items: center; }
  .stat-label{ font-size: var(--font-size-xs); color: var(--text-secondary); margin-bottom: 2px; }
  .stat-value{ font-size: 1.05rem; font-weight: 700; color: var(--primary-color); }
  .stat-value small{ font-size: 0.72rem; font-weight: 400; opacity: 0.85; }
  .status-dot{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #f59e0b; flex-shrink: 0; }

  /* ── Responsive: hide tagline at 1280, keep 4 items inline until 768 ── */
  @media (max-width: 1280px){
    .site-tagline{ display: none; }
  }
  @media (max-width: 1024px){
    /* At 1024 4 items still fit cleanly. Only tighten gaps. */
    .nav-list{ gap: 0.45rem; }
    .nav-link{ font-size: 0.88rem; padding: 0.3rem 0.5rem; }
    .nav-divider{ margin: 0 0.2rem 0 0.35rem; }
  }
  @media (max-width: 768px){
    .header-content{ justify-content: space-between; gap: 0.75rem; }
    .main-nav{ flex: none; display: flex; align-items: center; gap: 0.5rem; margin-left: auto; }
    .nav-list{ display: none; }
    .nav-divider{ display: none; }
    .theme-toggle-btn{ padding: 0.35rem 0.5rem; }
    .theme-toggle-btn .theme-label{ display: none; }
    .mobile-menu-button{
      display: inline-flex !important; align-items: center; justify-content: center; width: 40px; height: 40px; padding: 0;
      border-radius: 8px; border: 1px solid var(--border-medium); background-color: var(--bg-surface-elevated); color: var(--text-primary);
      cursor: pointer; box-shadow: var(--shadow-sm); transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .mobile-menu-button:hover{ border-color: var(--accent-primary); color: var(--accent-primary); background-color: var(--bg-surface); }
    .stats-bar{ display: none; }
    .mobile-menu{
      position: absolute; top: 100%; left: 0; right: 0;
      background-color: var(--bg-surface-elevated); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
      box-shadow: var(--shadow-lg); border-bottom: 2px solid var(--border-medium);
      padding: 1rem 1.25rem; z-index: 9999; display: block;
      max-height: calc(100dvh - 60px); overflow-y: auto;
    }
    .mobile-nav-list{ list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.35rem; }
    .mobile-nav-item{ border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.35rem; }
    .mobile-nav-item:last-child{ border-bottom: none; padding-bottom: 0; }
    .mobile-nav-link{
      color: var(--text-primary); text-decoration: none; font-size: 1.05rem; font-weight: 600;
      display: flex; align-items: center; gap: 8px; padding: 12px 10px; border-radius: 8px; min-height: 44px; transition: all 0.15s ease;
    }
    .mobile-nav-link.active{ color: var(--accent-primary); background-color: var(--accent-primary-glow); font-weight: 700; border-left: 3px solid var(--accent-primary); }
    .mobile-nav-link:hover{ color: var(--accent-primary); background-color: var(--bg-surface); }
    .mobile-accordion{ border-bottom: 1px solid var(--border-subtle); }
    .mobile-accordion-trigger{
      width: 100%; display: flex; align-items: center; justify-content: space-between;
      padding: 12px 10px; min-height: 44px; border: none; background: transparent; color: var(--text-primary);
      font-size: 1.05rem; font-weight: 600; cursor: pointer; border-radius: 8px; text-align: left;
    }
    .mobile-accordion-trigger:hover{ background: var(--bg-surface); color: var(--accent-primary); }
    .mobile-sub-list{ list-style: none; margin: 6px 0 8px 12px; padding: 0; display: flex; flex-direction: column; gap: 0.25rem; border-left: 2px solid var(--border-subtle); padding-left: 12px; }
    .mobile-sub-link{ display: flex; flex-direction: column; gap: 2px; padding: 8px 10px; border-radius: 8px; text-decoration: none; color: var(--text-primary); }
    .mobile-sub-link:hover{ background: var(--bg-surface); }
    .mobile-sub-link span:first-child{ font-size: 0.92rem; font-weight: 600; }
    .sub-desc{ font-size: 0.75rem; color: var(--text-muted); }
    .mobile-theme-item{ margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--border-subtle); }
    .mobile-theme-btn{
      display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 0.75rem 1rem;
      background: var(--bg-surface-elevated); border: 1px solid var(--border-medium); border-radius: 8px;
      font-family: var(--font-family-mono, monospace); font-size: 0.85rem; cursor: pointer; color: var(--text-primary);
    }
    .theme-pill-action{ font-size: 0.75rem; padding: 0.2rem 0.6rem; background: var(--accent-primary); color: #fff; border-radius: 9999px; }
  }
</style>
