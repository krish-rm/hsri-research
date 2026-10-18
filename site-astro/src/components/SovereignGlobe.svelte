<script lang="ts">
  import { onMount } from 'svelte';
  import { geoOrthographic, geoPath, geoDistance, geoGraticule, type GeoProjection } from 'd3-geo';
  import { drag } from 'd3-drag';
  import { select } from 'd3-selection';
  import * as topojson from 'topojson-client';
  import type { Topology } from 'topojson-specification';
  import scoresData from '../data/country_scores.json';

  // --- Props (Svelte 5) ---
  let {
    countries = scoresData.countries,
    selectedId = $bindable<string | null>(null),
    onSelect = (id: string | null) => {}
  }: {
    countries?: any[];
    selectedId?: string | null;
    onSelect?: (id: string | null) => void;
  } = $props();

  const base = (import.meta.env.BASE_URL || '').replace(/\/$/, '');

  // --- Coordinates: ingest canonical, fallback to embedded ---
  const fallbackCoords: Record<string, [number, number]> = {
    nor: [10.75, 60.47], fin: [25.75, 61.92], isl: [-19.02, 64.96], dnk: [9.50, 56.26],
    swe: [18.64, 60.13], aut: [14.55, 47.52], deu: [10.45, 51.17], nld: [5.29, 52.13],
    svn: [14.99, 46.15], nzl: [174.88, -40.90], fra: [2.21, 46.23], bel: [4.47, 50.50],
    cze: [15.47, 49.82], irl: [-8.24, 53.41], est: [25.01, 58.60], lux: [6.13, 49.81],
    aus: [133.77, -25.27], jpn: [138.25, 36.20], prt: [-8.22, 39.40], ltu: [23.88, 55.17],
    can: [-106.35, 56.13], pol: [19.14, 51.92], esp: [-3.75, 40.46], svk: [19.70, 48.67],
    lva: [24.60, 56.88], ita: [12.57, 41.87], hun: [19.50, 47.16], gbr: [-3.44, 55.38],
    kor: [127.77, 35.91], grc: [21.82, 39.07], rou: [24.97, 45.94], cyp: [33.43, 35.13],
    isr: [34.85, 31.05], mlt: [14.37, 35.94], bgr: [25.48, 42.73], usa: [-98.50, 39.80],
    mkd: [21.75, 41.61], sgp: [103.82, 1.35], hkg: [114.11, 22.40], che: [8.23, 46.82],
    are: [53.85, 23.42], chl: [-71.54, -35.67], ury: [-55.77, -32.52], cri: [-83.75, 9.75],
    mus: [57.55, -20.35], bhr: [50.55, 26.07]
  };

  let coords: Record<string, [number, number]> = $state(fallbackCoords);

  onMount(async () => {
    try {
      const res = await fetch(`${base}/data/country_coordinates.json`);
      if (res.ok) {
        const arr: Array<{ id: string; lng: number; lat: number }> = await res.json();
        const m: Record<string, [number, number]> = {};
        for (const r of arr) m[r.id.toLowerCase()] = [r.lng, r.lat];
        if (Object.keys(m).length >= 10) coords = m;
      }
    } catch {}
  });

  // --- Color by Leontief sovereignty tier ---
  function tier(c: any): 'resilient' | 'transitional' | 'fragile' {
    const h = c?.H_Layer2 ?? c?.H_L2 ?? c?.variants?.hsri_leontief ?? 0;
    const delta = c?.rank_delta ?? c?.variants?.rank_delta_leo ?? 0;
    if (h >= 0.40 && delta > -15) return 'resilient';
    if (h >= 0.25 && delta > -15) return 'transitional';
    return 'fragile';
  }

  const tierColor: Record<string, string> = {
    resilient: '#10b981',
    transitional: '#f59e0b',
    fragile: '#ef4444'
  };

  // --- Canvas / Projection State ---
  let canvasEl: HTMLCanvasElement | null = $state(null);
  let containerEl: HTMLDivElement | null = $state(null);
  let width = $state(720);
  let height = $state(520);
  let searchQuery = $state('');
  let rotation: [number, number] = $state([-10, -20]); // [lambda, phi]
  let scale = $state(220);
  let isDragging = $state(false);
  let hoverId: string | null = $state(null);
  let world: any = $state(null); // GeoJSON FeatureCollection

  // Projection & Graticule
  const graticule = geoGraticule();

  let projection: GeoProjection = $derived.by(() => {
    const p = geoOrthographic()
      .rotate(rotation)
      .translate([width / 2, height / 2])
      .scale(scale)
      .clipAngle(90);
    return p;
  });

  // Filtered quick-select list
  let filtered = $derived.by(() => {
    const q = searchQuery.trim().toLowerCase();
    if (!q) return [];
    return countries
      .filter(
        (c: any) =>
          c.name.toLowerCase().includes(q) ||
          c.code.toLowerCase().includes(q) ||
          (c.id && c.id.toLowerCase().includes(q))
      )
      .slice(0, 6);
  });

  // --- Load world landmasses once ---
  async function loadWorld() {
    try {
      const res = await fetch(`${base}/data/world-110m.json`);
      if (!res.ok) throw new Error('world missing');
      const topo = (await res.json()) as Topology;
      // @ts-ignore topojson types
      const fc = topojson.feature(topo, (topo.objects as any).land ?? (topo.objects as any).countries);
      world = fc;
    } catch {
      world = null; // globe still renders ocean + nodes without land
    }
  }

  // --- Render Loop (Canvas2D, <2ms/frame) ---
  let raf = 0;
  let autoRotateSpeed = 0.18; // deg per frame ~0.5 rpm at 60fps

  function frame() {
    if (!canvasEl || !containerEl) return;
    const ctx = canvasEl.getContext('2d');
    if (!ctx) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    // auto-rotate when idle
    if (!isDragging && !selectedId && typeof document !== 'undefined' && document.visibilityState === 'visible') {
      rotation = [rotation[0] + autoRotateSpeed, rotation[1]];
      projection.rotate(rotation);
    }
    draw(ctx, dpr);
    raf = requestAnimationFrame(frame);
  }

  function draw(ctx: CanvasRenderingContext2D, dpr: number) {
    const isDark = typeof document !== 'undefined' && document.documentElement.getAttribute('data-theme') !== 'light';
    ctx.clearRect(0, 0, width * dpr, height * dpr);
    ctx.save();
    ctx.scale(dpr, dpr);

    // Outer background matching card
    ctx.beginPath();
    const path: any = geoPath(projection, ctx);
    ctx.fillStyle = isDark ? '#080d17' : '#f7f2e5';
    ctx.fillRect(0, 0, width, height);

    // Ocean Sphere Fill (Dark, high-contrast maritime depth)
    ctx.beginPath();
    // @ts-ignore
    path({ type: 'Sphere' });
    ctx.fillStyle = isDark ? '#0b1626' : '#142531';
    ctx.fill();

    // Graticule (10-degree meridians and parallels)
    ctx.beginPath();
    // @ts-ignore
    path(graticule());
    ctx.strokeStyle = isDark ? 'rgba(45, 212, 191, 0.12)' : 'rgba(78, 175, 155, 0.20)';
    ctx.lineWidth = 0.55;
    ctx.stroke();

    // Landmasses (Dark, defined continents with high contrast)
    if (world) {
      ctx.beginPath();
      path(world as any);
      ctx.fillStyle = isDark ? '#16283d' : '#223c4a';
      ctx.fill();
      ctx.strokeStyle = isDark ? '#2e4868' : '#3d6375';
      ctx.lineWidth = 0.75;
      ctx.stroke();
    }

    // Atmospheric rim (Luminous seafoam atmospheric boundary)
    ctx.beginPath();
    // @ts-ignore
    path({ type: 'Sphere' });
    ctx.strokeStyle = isDark ? 'rgba(45, 212, 191, 0.45)' : 'rgba(35, 160, 135, 0.55)';
    ctx.lineWidth = 1.8;
    ctx.stroke();

    // Nodes — 39 sovereign points
    for (const c of countries) {
      const id = (c.id || '').toLowerCase();
      const ll = coords[id];
      if (!ll) continue;
      const p = projection(ll as [number, number]);
      if (!p) continue;

      // back-face culling: dot product of point vs center
      const center: [number, number] = [-rotation[0], -rotation[1]];
      const dist = geoDistance(ll as [number, number], center);
      if (dist > Math.PI / 2 - 0.08) continue; // slightly beyond hemisphere clipped

      const t = tier(c);
      const isSelected = selectedId === id;
      const isHover = hoverId === id;
      const r = isSelected ? 7.5 : isHover ? 6 : 4.2;
      const col = tierColor[t];

      // outer pulse (only resilient/transitional subtle, fragile intense)
      if (t === 'fragile' || isSelected) {
        ctx.beginPath();
        ctx.arc(p[0], p[1], r + 9, 0, Math.PI * 2);
        ctx.fillStyle = t === 'fragile' ? 'rgba(239,68,68,0.14)' : 'rgba(16,185,129,0.14)';
        ctx.fill();
      }

      // core dot
      ctx.beginPath();
      ctx.arc(p[0], p[1], r, 0, Math.PI * 2);
      ctx.fillStyle = col;
      ctx.shadowColor = col;
      ctx.shadowBlur = isSelected ? 12 : 6;
      ctx.fill();
      ctx.shadowBlur = 0;

      // stroke
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.95)';
      ctx.lineWidth = isSelected ? 1.6 : 1;
      ctx.stroke();

      // selection ring
      if (isSelected) {
        ctx.beginPath();
        ctx.arc(p[0], p[1], r + 5, 0, Math.PI * 2);
        ctx.strokeStyle = col;
        ctx.lineWidth = 1.4;
        ctx.setLineDash([3, 3]);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // Hover / Selection label tag
      if (isHover || isSelected) {
        ctx.save();
        ctx.font = '600 11px Inter, sans-serif';
        const label = `${c.name} (${c.code.toUpperCase()})`;
        const tw = ctx.measureText(label).width;
        const lx = p[0];
        const ly = p[1] - r - 10;
        ctx.fillStyle = 'rgba(15, 23, 42, 0.90)';
        const padX = 7;
        const boxH = 20;
        const boxW = tw + padX * 2;
        const boxX = lx - boxW / 2;
        const boxY = ly - boxH;
        ctx.beginPath();
        ctx.roundRect ? ctx.roundRect(boxX, boxY, boxW, boxH, 5) : ctx.rect(boxX, boxY, boxW, boxH);
        ctx.fill();
        ctx.strokeStyle = col;
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, lx, boxY + boxH / 2);
        ctx.restore();
      }
    }
    ctx.restore();
  }

  // --- Interactions: drag, wheel, tap ---
  function attachDrag() {
    if (!canvasEl) return;
    const sel: any = select(canvasEl as any);
    let startRot: [number, number] = [rotation[0], rotation[1]];
    sel.call(
      drag()
        .on('start', () => {
          isDragging = true;
          startRot = [...rotation] as [number, number];
        })
        .on('drag', (event: any) => {
          const k = 0.28; // sensitivity
          rotation = [startRot[0] + event.x * k, Math.max(-55, Math.min(55, startRot[1] - event.y * k))];
          projection.rotate(rotation);
        })
        .on('end', () => {
          isDragging = false;
          startRot = [...rotation] as [number, number];
        })
    );
  }

  function onWheel(e: WheelEvent) {
    e.preventDefault();
    const delta = -e.deltaY * 0.0012;
    scale = Math.max(150, Math.min(420, scale * (1 + delta)));
    projection.scale(scale);
  }

  function onCanvasClick(e: MouseEvent) {
    if (!canvasEl) return;
    const rect = canvasEl.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // hit test: find nearest visible node within 14px
    let best: string | null = null;
    let bestDist = 14;
    for (const c of countries) {
      const id = (c.id || '').toLowerCase();
      const ll = coords[id];
      if (!ll) continue;
      const p: any = projection(ll as [number, number]);
      if (!p) continue;
      const center: [number, number] = [-rotation[0], -rotation[1]];
      if (geoDistance(ll as [number, number], center) > Math.PI / 2) continue;
      const d = Math.hypot(p[0] - x, p[1] - y);
      if (d < bestDist) {
        bestDist = d;
        best = id;
      }
    }
    if (best) {
      selectedId = best;
      onSelect(best);
      focusOn(best);
    }
  }

  function onCanvasMove(e: MouseEvent) {
    if (!canvasEl || isDragging) return;
    const rect = canvasEl.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    let hit: string | null = null;
    for (const c of countries) {
      const id = (c.id || '').toLowerCase();
      const ll = coords[id];
      if (!ll) continue;
      const p: any = projection(ll as [number, number]);
      if (!p) continue;
      const center: [number, number] = [-rotation[0], -rotation[1]];
      if (geoDistance(ll as [number, number], center) > Math.PI / 2) continue;
      if (Math.hypot(p[0] - x, p[1] - y) < 10) {
        hit = id;
        break;
      }
    }
    hoverId = hit;
    if (canvasEl) canvasEl.style.cursor = hit ? 'pointer' : isDragging ? 'grabbing' : 'grab';
  }

  function focusOn(id: string) {
    const ll = coords[id.toLowerCase()];
    if (!ll) return;
    const target: [number, number] = [-ll[0], -ll[1]];
    const start: [number, number] = [...rotation] as [number, number];
    const dur = 750;
    const t0 = performance.now();
    const ease = (t: number) => 1 - Math.pow(1 - t, 3);
    function step(now: number) {
      const t = Math.min(1, (now - t0) / dur);
      const k = ease(t);
      rotation = [start[0] + (target[0] - start[0]) * k, start[1] + (target[1] - start[1]) * k];
      projection.rotate(rotation);
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function onQuickSelect(id: string) {
    selectedId = id.toLowerCase();
    onSelect(selectedId);
    focusOn(selectedId);
  }

  // --- Responsive sizing ---
  function measure() {
    if (!containerEl) return;
    const w = containerEl.clientWidth;
    const isMobile = window.innerWidth <= 768;
    width = Math.floor(w);
    height = isMobile ? 400 : Math.min(560, Math.max(420, Math.floor(w * 0.62)));
    scale = isMobile ? 170 : Math.min(320, Math.max(200, Math.floor(width * 0.33)));
    projection.translate([width / 2, height / 2]).scale(scale);
    if (canvasEl) {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvasEl.width = width * dpr;
      canvasEl.height = height * dpr;
      canvasEl.style.width = width + 'px';
      canvasEl.style.height = height + 'px';
    }
  }

  onMount(() => {
    measure();
    loadWorld().then(() => {
      attachDrag();
      frame();
    });
    const ro = new ResizeObserver(measure);
    if (containerEl) ro.observe(containerEl);
    window.addEventListener('resize', measure);

    const handleVisibility = () => {
      if (document.visibilityState === 'visible' && !raf) {
        frame();
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);

    return () => {
      cancelAnimationFrame(raf);
      ro.disconnect();
      window.removeEventListener('resize', measure);
      document.removeEventListener('visibilitychange', handleVisibility);
    };
  });

  export function focusCountry(id: string) {
    onQuickSelect(id);
  }
</script>

<div class="globe-wrap" bind:this={containerEl}>
  <div class="globe-toolbar">
    <div class="search-box">
      <input
        type="text"
        placeholder="Find nation — e.g. Singapore, USA, Germany"
        bind:value={searchQuery}
        aria-label="Search nations"
      />
      {#if filtered.length}
        <ul class="search-suggestions" role="listbox">
          {#each filtered as c}
            <li>
              <button
                type="button"
                role="option"
                aria-selected={selectedId === c.id.toLowerCase()}
                onclick={() => {
                  searchQuery = '';
                  onQuickSelect(c.id);
                }}
              >
                <span>{c.name}</span>
                <span class="code">{c.code}</span>
              </button>
            </li>
          {/each}
        </ul>
      {/if}
    </div>
    <div class="quick-pills" aria-label="Quick jump">
      {#each ['nor', 'usa', 'sgp', 'deu', 'jpn', 'gbr', 'kor'] as pid}
        {@const found = countries.find((x: any) => x.id.toLowerCase() === pid)}
        {#if found}
          <button
            type="button"
            class="pill"
            class:active={selectedId === pid}
            onclick={() => onQuickSelect(pid)}
          >
            {found.code}
          </button>
        {/if}
      {/each}
    </div>
  </div>

  <canvas
    bind:this={canvasEl}
    class="globe-canvas"
    onclick={onCanvasClick}
    onmousemove={onCanvasMove}
    onwheel={onWheel}
    aria-label="Interactive sovereign globe — drag to rotate, tap nation to inspect"
  ></canvas>

  <div class="globe-hint" aria-hidden="true">Drag to rotate · Tap nation to inspect · Scroll to zoom</div>

  <div class="globe-legend" aria-hidden="true">
    <span class="dot" style="background:#10b981"></span> Resilient (H≥0.40)
    <span class="dot" style="background:#f59e0b"></span> Transitional
    <span class="dot" style="background:#ef4444"></span> Fragility Trap
  </div>
</div>

<style>
  .globe-wrap {
    position: relative;
    width: 100%;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
  }
  .globe-toolbar {
    position: absolute;
    top: 12px;
    left: 12px;
    right: 12px;
    display: flex;
    gap: 10px;
    align-items: flex-start;
    justify-content: space-between;
    z-index: 3;
    pointer-events: none;
  }
  .search-box {
    position: relative;
    flex: 1;
    max-width: 360px;
    pointer-events: auto;
  }
  .search-box input {
    width: 100%;
    padding: 9px 12px;
    border-radius: 10px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-primary);
    font-size: 0.88rem;
    outline: none;
    box-sizing: border-box;
  }
  .search-box input:focus {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-primary-glow);
  }
  .search-suggestions {
    position: absolute;
    top: calc(100% + 6px);
    left: 0;
    right: 0;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    box-shadow: var(--shadow-lg);
    list-style: none;
    margin: 0;
    padding: 6px;
    z-index: 10;
  }
  .search-suggestions button {
    width: 100%;
    text-align: left;
    padding: 8px 10px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: var(--text-primary);
    cursor: pointer;
    font-size: 0.88rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .search-suggestions button:hover {
    background: var(--bg-surface-sunken);
  }
  .code {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
    border: 1px solid var(--border-subtle);
    padding: 1px 6px;
    border-radius: 9999px;
  }
  .quick-pills {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    pointer-events: auto;
  }
  .pill {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 6px 10px;
    border-radius: 9999px;
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .pill.active,
  .pill:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
    background: var(--accent-primary-glow);
  }
  .globe-canvas {
    display: block;
    width: 100%;
    touch-action: pan-y; /* gesture isolation: vertical scroll not hijacked */
    user-select: none;
    -webkit-user-select: none;
  }
  .globe-hint {
    position: absolute;
    bottom: 10px;
    right: 12px;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    letter-spacing: 0.04em;
    color: var(--text-muted);
    background: var(--bg-glass);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid var(--border-subtle);
    padding: 4px 10px;
    border-radius: 9999px;
    pointer-events: none;
    white-space: nowrap;
  }
  .globe-legend {
    position: absolute;
    bottom: 10px;
    left: 12px;
    display: flex;
    gap: 10px;
    align-items: center;
    font-size: 0.72rem;
    color: var(--text-muted);
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    padding: 5px 10px;
    border-radius: 9999px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
  }
  @media (max-width: 768px) {
    .globe-toolbar {
      flex-direction: column;
    }
    .search-box {
      max-width: 100%;
    }
    .quick-pills {
      width: 100%;
      overflow-x: auto;
      scrollbar-width: none;
      flex-wrap: nowrap;
      padding-bottom: 2px;
    }
    .quick-pills::-webkit-scrollbar {
      display: none;
    }
    .globe-legend {
      display: none; /* saved for inspector on mobile */
    }
    .globe-hint {
      display: none;
    }
  }
</style>
