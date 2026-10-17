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

  onMount(() => {
    if (typeof window === 'undefined') return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            activeChapterId = entry.target.id;
          }
        });
      },
      { rootMargin: '-20% 0px -70% 0px', threshold: 0 }
    );

    chapters.forEach((ch) => {
      const el = document.getElementById(ch.id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  });

  function scrollToChapter(id: string, e: MouseEvent) {
    e.preventDefault();
    const el = document.getElementById(id);
    if (el) {
      const offset = 80; // height of sticky bar
      const bodyRect = document.body.getBoundingClientRect().top;
      const elementRect = el.getBoundingClientRect().top;
      const elementPosition = elementRect - bodyRect;
      const offsetPosition = elementPosition - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
      activeChapterId = id;
    }
  }
</script>

<nav class="chapter-nav-rail" aria-label="Monograph Chapters Navigation">
  <div class="rail-inner">
    <div class="rail-label">
      <span class="mono-prefix">[MONOGRAPH]</span>
      <span class="read-total">35 MIN READ</span>
    </div>

    <div class="pills-scroll-container">
      {#each chapters as ch}
        <a
          href={`#${ch.id}`}
          class="chapter-pill"
          class:active={activeChapterId === ch.id}
          on:click={(e) => scrollToChapter(ch.id, e)}
        >
          <span class="ch-num">{ch.num}</span>
          <span class="ch-title">{ch.title}</span>
          <span class="ch-time">⏱ {ch.minutes}m</span>
        </a>
      {/each}
    </div>
  </div>
</nav>

<style>
  .chapter-nav-rail {
    position: sticky;
    top: 0;
    z-index: 999;
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
    gap: 1.25rem;
    box-sizing: border-box;
  }

  .rail-label {
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    font-family: var(--font-family-mono);
  }

  .mono-prefix {
    font-size: 0.65rem;
    font-weight: 800;
    color: var(--accent-primary);
    letter-spacing: 0.08em;
  }

  .read-total {
    font-size: 0.62rem;
    color: var(--text-muted);
  }

  .pills-scroll-container {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
    padding: 0.2rem 0;
    width: 100%;
  }

  .pills-scroll-container::-webkit-scrollbar {
    display: none;
  }

  .chapter-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.65rem;
    border-radius: 6px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.75rem;
    font-weight: 500;
    white-space: nowrap;
    scroll-snap-align: start;
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

  .ch-num {
    font-family: var(--font-family-mono);
    font-size: 0.70rem;
    font-weight: 700;
    color: var(--accent-primary);
  }

  .ch-time {
    font-family: var(--font-family-mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    opacity: 0.85;
  }

  @media (max-width: 768px) {
    .rail-label {
      display: none;
    }
  }
</style>
