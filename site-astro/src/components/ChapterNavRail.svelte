<script lang="ts">
  import { onMount } from 'svelte';

  export let chapters: Array<{ id: string; num: string; title: string; minutes: number }> = [
    { id: 'prologue', num: '0', title: 'Speed of Thought', minutes: 4 },
    { id: 'chapter-1', num: 'I', title: 'The Gorilla Problem', minutes: 6 },
    { id: 'chapter-2', num: 'II', title: 'The Abundance Trap', minutes: 7 },
    { id: 'chapter-3', num: 'III', title: 'The 26 Tripwires', minutes: 5 },
    { id: 'chapter-4', num: 'IV', title: 'The Readiness Audit', minutes: 6 },
    { id: 'chapter-5', num: 'V', title: 'The S-Curve Objection', minutes: 3 },
    { id: 'epilogue', num: 'VI', title: 'Sovereign Path', minutes: 4 },
  ];

  let activeChapterId = 'prologue';
  let scrollPercent = 0;
  let isDrawerOpen = false;

  $: activeIndex = chapters.findIndex((c) => c.id === activeChapterId);
  $: activeChapter = chapters[activeIndex >= 0 ? activeIndex : 0];
  $: minutesRemaining = chapters
    .slice(Math.max(0, activeIndex))
    .reduce((acc, c) => acc + c.minutes, 0);

  onMount(() => {
    if (typeof window === 'undefined') return;

    // Track scroll percentage
    function handleScroll() {
      const scrollY = window.scrollY || document.documentElement.scrollTop;
      const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (docHeight > 0) {
        scrollPercent = Math.min(100, Math.max(0, Math.round((scrollY / docHeight) * 100)));
      }
    }

    // Track active chapter
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            activeChapterId = entry.target.id;
          }
        });
      },
      { rootMargin: '-20% 0px -65% 0px', threshold: 0 }
    );

    chapters.forEach((ch) => {
      const el = document.getElementById(ch.id);
      if (el) observer.observe(el);
    });

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    return () => {
      observer.disconnect();
      window.removeEventListener('scroll', handleScroll);
    };
  });

  function scrollToChapter(id: string, e?: MouseEvent) {
    if (e) e.preventDefault();
    const el = document.getElementById(id);
    if (el) {
      const offset = 75; // sticky header offset
      const bodyRect = document.body.getBoundingClientRect().top;
      const elementRect = el.getBoundingClientRect().top;
      const offsetPosition = elementRect - bodyRect - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
      activeChapterId = id;
      isDrawerOpen = false;
    }
  }

  function toggleDrawer() {
    isDrawerOpen = !isDrawerOpen;
  }
</script>

<!-- ========================================================================= -->
<!-- DESKTOP CHAPTER NAV RAIL (Sticky below Header)                            -->
<!-- ========================================================================= -->
<nav class="chapter-nav-rail desktop-rail" aria-label="Monograph Chapters Navigation">
  <div class="rail-inner">
    <div class="rail-meta-block">
      <span class="active-badge">{activeChapter.num} · {activeChapter.title}</span>
      <span class="progress-badge">{scrollPercent}% READ · ~{minutesRemaining}M LEFT</span>
    </div>

    <div class="pills-scroll-container">
      {#each chapters as ch, idx}
        <a
          href={`#${ch.id}`}
          class="chapter-pill"
          class:active={activeChapterId === ch.id}
          class:completed={idx < activeIndex}
          on:click={(e) => scrollToChapter(ch.id, e)}
        >
          <span class="ch-num">{ch.num}</span>
          <span class="ch-title">{ch.title}</span>
          <span class="ch-time">{ch.minutes}m</span>
        </a>
      {/each}
    </div>
  </div>
</nav>

<!-- ========================================================================= -->
<!-- MOBILE FLOATING READING DOCK (Bottom center on mobile screens)            -->
<!-- ========================================================================= -->
<div class="mobile-reading-dock">
  <button type="button" class="dock-summary" on:click={toggleDrawer}>
    <div class="dock-progress-ring">
      <span class="dock-percent">{scrollPercent}%</span>
    </div>
    <div class="dock-text">
      <span class="dock-label">READING SECTION</span>
      <span class="dock-title">{activeChapter.num} · {activeChapter.title}</span>
    </div>
    <div class="dock-action-btn">
      <span>{isDrawerOpen ? '✕ Close' : '≡ Chapters'}</span>
    </div>
  </button>
</div>

<!-- ========================================================================= -->
<!-- MOBILE TABLE OF CONTENTS DRAWER / BOTTOM SHEET                            -->
<!-- ========================================================================= -->
{#if isDrawerOpen}
  <div class="drawer-backdrop" on:click={toggleDrawer} role="presentation"></div>
  <div class="toc-bottom-sheet" role="dialog" aria-modal="true" aria-label="Table of Contents">
    <div class="sheet-header">
      <div class="sheet-title-col">
        <span class="sheet-eyebrow">MONOGRAPH NAVIGATION</span>
        <h3 class="sheet-title">Chapters &amp; Reading Timeline</h3>
      </div>
      <button type="button" class="sheet-close-btn" on:click={toggleDrawer} aria-label="Close chapter list">✕</button>
    </div>

    <div class="sheet-progress-row">
      <div class="sheet-progress-bar">
        <div class="sheet-progress-fill" style={`width: ${scrollPercent}%;`}></div>
      </div>
      <span class="sheet-progress-text">{scrollPercent}% Completed (~{minutesRemaining} min remaining)</span>
    </div>

    <ul class="sheet-chapter-list">
      {#each chapters as ch, idx}
        <li class="sheet-chapter-item">
          <button
            type="button"
            class="sheet-chapter-btn"
            class:active={activeChapterId === ch.id}
            on:click={() => scrollToChapter(ch.id)}
          >
            <span class="sheet-num">{ch.num}</span>
            <div class="sheet-content">
              <span class="sheet-ch-title">{ch.title}</span>
              <span class="sheet-ch-meta">{ch.minutes} min read</span>
            </div>
            {#if idx < activeIndex}
              <span class="status-icon completed">✓</span>
            {:else if activeChapterId === ch.id}
              <span class="status-icon active-dot">●</span>
            {/if}
          </button>
        </li>
      {/each}
    </ul>
  </div>
{/if}

<style>
  /* Desktop Top Sticky Rail */
  .chapter-nav-rail {
    position: sticky;
    top: 58px;
    z-index: 990;
    background: var(--bg-glass);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border-subtle);
    padding: 0.5rem 0;
    transition: background-color 0.25s ease, border-color 0.25s ease;
  }

  .rail-inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.25rem;
    box-sizing: border-box;
  }

  .rail-meta-block {
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
  }

  .active-badge {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--text-primary);
    white-space: nowrap;
  }

  .progress-badge {
    font-family: var(--font-family-mono);
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--accent-primary);
    letter-spacing: 0.04em;
  }

  .pills-scroll-container {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    overflow-x: auto;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
    padding: 0.2rem 0;
  }
  .pills-scroll-container::-webkit-scrollbar {
    display: none;
  }

  .chapter-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.65rem;
    border-radius: 6px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.78rem;
    font-weight: 500;
    white-space: nowrap;
    flex-shrink: 0;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .chapter-pill:hover {
    color: var(--text-primary);
    border-color: var(--border-medium);
    background: var(--bg-surface-elevated);
  }

  .chapter-pill.active {
    color: var(--text-primary);
    background: var(--accent-primary-glow);
    border-color: var(--accent-primary);
    font-weight: 700;
    box-shadow: 0 0 10px -2px var(--accent-primary-glow);
  }

  .chapter-pill.completed {
    border-color: var(--border-medium);
    opacity: 0.85;
  }

  .ch-num {
    font-family: var(--font-family-mono);
    font-size: 0.70rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .ch-time {
    font-family: var(--font-family-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
  }

  /* Mobile Floating Reading Dock */
  .mobile-reading-dock {
    display: none;
    position: fixed;
    bottom: 1.25rem;
    left: 1rem;
    right: 1rem;
    z-index: 1000;
  }

  .dock-summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    padding: 0.65rem 1rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    cursor: pointer;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }

  .dock-progress-ring {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--accent-primary-glow);
    border: 2px solid var(--accent-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .dock-percent {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    color: var(--text-primary);
  }

  .dock-text {
    display: flex;
    flex-direction: column;
    text-align: left;
    margin: 0 0.75rem;
    flex-grow: 1;
    overflow: hidden;
  }

  .dock-label {
    font-family: var(--font-family-mono);
    font-size: 0.62rem;
    font-weight: 700;
    color: var(--accent-primary);
    letter-spacing: 0.05em;
  }

  .dock-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .dock-action-btn {
    font-family: var(--font-family-mono);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.35rem 0.65rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 6px;
    color: var(--text-primary);
    flex-shrink: 0;
  }

  /* Table of Contents Bottom Sheet */
  .drawer-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.65);
    z-index: 1001;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
  }

  .toc-bottom-sheet {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-height: 80vh;
    background: var(--bg-surface-elevated);
    border-top: 2px solid var(--border-medium);
    border-radius: 20px 20px 0 0;
    padding: 1.5rem 1.25rem 2.5rem;
    z-index: 1002;
    overflow-y: auto;
    box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.4);
    animation: slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }

  .sheet-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }

  .sheet-eyebrow {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
  }

  .sheet-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0.25rem 0 0;
  }

  .sheet-close-btn {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 50%;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-primary);
    font-size: 0.9rem;
    cursor: pointer;
  }

  .sheet-progress-row {
    margin-bottom: 1.25rem;
  }

  .sheet-progress-bar {
    width: 100%;
    height: 6px;
    background: var(--bg-surface-sunken);
    border-radius: 9999px;
    overflow: hidden;
    margin-bottom: 0.4rem;
  }

  .sheet-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-primary) 0%, #38bdf8 100%);
    transition: width 0.2s ease;
  }

  .sheet-progress-text {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .sheet-chapter-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .sheet-chapter-btn {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 0.75rem 1rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    color: var(--text-primary);
    text-align: left;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .sheet-chapter-btn:hover {
    border-color: var(--border-medium);
    background: var(--bg-surface-elevated);
  }

  .sheet-chapter-btn.active {
    border-color: var(--accent-primary);
    background: var(--accent-primary-glow);
  }

  .sheet-num {
    font-family: var(--font-family-mono);
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--accent-primary);
    width: 2rem;
    flex-shrink: 0;
  }

  .sheet-content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
  }

  .sheet-ch-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .sheet-ch-meta {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    color: var(--text-muted);
  }

  .status-icon.completed {
    color: var(--threat-sovereign);
    font-weight: 800;
  }

  .status-icon.active-dot {
    color: var(--accent-primary);
    font-size: 0.9rem;
  }

  @media (max-width: 768px) {
    .desktop-rail {
      display: none;
    }
    .mobile-reading-dock {
      display: block;
    }
  }
</style>
