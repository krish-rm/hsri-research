<script lang="ts">
  import { onDestroy } from 'svelte';
  import wedgeHistoryData from '../data/wedge_history.json';

  const trajectory = wedgeHistoryData.benchmark_trajectory || [];
  let selectedGenId = $state('GEN-06');
  let animating = $state(false);
  let animTick = $state(0);
  let timer: ReturnType<typeof setInterval> | null = null;

  let activeItem = $derived.by(() => {
    return trajectory.find((t: any) => t.generation_id === selectedGenId) || trajectory[trajectory.length - 1];
  });

  // Visual SVG chart coordinates (2022-2026 log/scaled height for clear visual readability)
  const W = 640;
  const H = 195;
  const padL = 48;
  const padR = 26;
  const padT = 20;
  const padB = 34;

  // Map seconds (1s..4800s) onto visual percentage cleanly via sqrt-compressed scale so 8s vs 4800s both read smoothly
  function mapY(sec: number) {
    const maxS = 4800;
    const norm = Math.sqrt(Math.max(0.5, sec) / maxS);
    return H - padB - norm * (H - padT - padB);
  }

  function mapX(idx: number) {
    const span = Math.max(1, trajectory.length - 1);
    return padL + (idx / span) * (W - padL - padR);
  }

  let humanPoints = $derived(
    trajectory.map((t: any, i: number) => `${mapX(i).toFixed(1)},${mapY(t.tau_verify_seconds).toFixed(1)}`).join(' ')
  );
  let machinePoints = $derived(
    trajectory.map((t: any, i: number) => `${mapX(i).toFixed(1)},${mapY(t.tau_gen_seconds).toFixed(1)}`).join(' ')
  );
  let humanArea = $derived.by(() => {
    if (!trajectory.length) return '';
    const firstX = mapX(0).toFixed(1);
    const lastX = mapX(trajectory.length - 1).toFixed(1);
    const base = (H - padB).toFixed(1);
    return `M ${firstX},${base} L ${humanPoints} L ${lastX},${base} Z`;
  });

  function formatDuration(sec: number) {
    if (sec >= 60) {
      const m = sec / 60;
      return `${Number.isInteger(m) ? m : m.toFixed(1)} min`;
    }
    return `${sec} sec`;
  }

  function replayRace() {
    if (timer) clearInterval(timer);
    animating = true;
    animTick = 0;
    timer = setInterval(() => {
      animTick += 1;
      if (animTick >= 40) {
        if (timer) clearInterval(timer);
        timer = null;
        animating = false;
      }
    }, 65);
  }

  onDestroy(() => {
    if (timer) clearInterval(timer);
  });

  // Simulated visual race positions
  let machineProgress = $derived(animating ? Math.min(100, animTick * 35) : 100);
  let ratioValue = $derived(activeItem ? activeItem.wedge_ratio : 3200);
  let humanProgress = $derived.by(() => {
    if (!activeItem) return 100;
    if (animating) {
      const targetAtTick = Math.min(100, (animTick * 35) / Math.max(1, Math.min(45, Math.sqrt(ratioValue))));
      return Math.max(4, targetAtTick);
    }
    return Math.max(8, Math.min(100, (activeItem.tau_verify_seconds / 4800) * 100));
  });
</script>

<section class="speed-visual-card" aria-label="AI speed versus human checking time visual comparison">
  <div class="sv-head">
    <div>
      <span class="sv-kicker">1 · THE SPEED GAP AT A GLANCE</span>
      <h3 class="sv-title">How fast AI finishes vs. how long a person needs to check</h3>
      <p class="sv-sub">Tap any year below to compare how quickly software finishes one complex task versus how long an expert needs to verify every step.</p>
    </div>
    <button type="button" class="replay-btn" onclick={replayRace}>
      &#9654; {animating ? 'Running 1 task...' : 'Replay 1-task race'}
    </button>
  </div>

  <!-- Year / Generation Visual Pills -->
  <div class="year-strip" role="tablist" aria-label="Select year and AI generation">
    {#each trajectory as gen}
      {@const isSelected = selectedGenId === gen.generation_id}
      <button
        type="button"
        role="tab"
        aria-selected={isSelected}
        class="year-pill"
        class:selected={isSelected}
        onclick={() => { selectedGenId = gen.generation_id; }}
      >
        <span class="yp-year">{gen.date.slice(0, 4)}</span>
        <span class="yp-name">{gen.model_label.split('(')[0].trim()}</span>
      </button>
    {/each}
  </div>

  {#if activeItem}
    <!-- Side-by-Side 2-Lane Visual Race -->
    <div class="race-box">
      <div class="race-row">
        <div class="race-meta">
          <span class="race-actor ai-tag">AI finishes in</span>
          <strong class="race-time ai-num">{formatDuration(activeItem.tau_gen_seconds)}</strong>
        </div>
        <div class="lane-track" aria-hidden="true">
          <div class="lane-fill ai-fill" style="width: {Math.max(5, Math.min(100, (activeItem.tau_gen_seconds / 15) * (machineProgress / 100) * 18))}%"></div>
          <span class="lane-note">Practically instant ({activeItem.tau_gen_seconds}s)</span>
        </div>
      </div>

      <div class="race-row">
        <div class="race-meta">
          <span class="race-actor human-tag">Human check takes</span>
          <strong class="race-time human-num">{formatDuration(activeItem.tau_verify_seconds)}</strong>
        </div>
        <div class="lane-track" aria-hidden="true">
          <div class="lane-fill human-fill" style="width: {humanProgress}%"></div>
        </div>
      </div>

      <!-- Visual Ratio Callout + Clock Icon -->
      <div class="ratio-callout">
        <div class="clock-svg-wrap" aria-hidden="true">
          <svg viewBox="0 0 64 64" width="54" height="54">
            <circle cx="32" cy="32" r="28" fill="var(--bg-surface-sunken)" stroke="var(--border-medium)" stroke-width="2" />
            <!-- Highlighted arc scaling smoothly with verify minutes -->
            <circle
              cx="32"
              cy="32"
              r="21"
              fill="none"
              stroke="var(--threat-critical)"
              stroke-width="6"
              stroke-dasharray={`${Math.min(132, Math.max(8, (activeItem.tau_verify_seconds / 4800) * 132))} 132`}
              transform="rotate(-90 32 32)"
              stroke-linecap="round"
            />
            <line x1="32" y1="32" x2="32" y2="17" stroke="var(--text-primary)" stroke-width="2.5" stroke-linecap="round" />
            <line x1="32" y1="32" x2="43" y2="32" stroke="var(--accent-primary)" stroke-width="2" stroke-linecap="round" />
            <circle cx="32" cy="32" r="3" fill="var(--text-primary)" />
          </svg>
        </div>
        <div class="callout-copy">
          <strong class="callout-big">{activeItem.wedge_ratio.toLocaleString()}&times; gap</strong>
          <span>
            {#if activeItem.tau_verify_seconds >= 3600}
              Checking <strong>1</strong> task takes an expert as long as watching a short film ({formatDuration(activeItem.tau_verify_seconds)}), while AI moves on in <strong>{activeItem.tau_gen_seconds}s</strong>.
            {:else if activeItem.tau_verify_seconds >= 60}
              Checking <strong>1</strong> task takes <strong>{formatDuration(activeItem.tau_verify_seconds)}</strong> compared to <strong>{activeItem.tau_gen_seconds}s</strong> of computer time.
            {:else}
              In {activeItem.date.slice(0, 4)}, a person could still read and verify an answer in seconds (<strong>{formatDuration(activeItem.tau_verify_seconds)}</strong>).
            {/if}
          </span>
        </div>
      </div>
    </div>

    <!-- Visual Curve Chart (2022 -> 2026) -->
    <div class="curve-wrap">
      <div class="curve-caption-row">
        <span class="legend-item"><i class="dot-human"></i> Human check time (8 sec &rarr; 80 min)</span>
        <span class="legend-item"><i class="dot-ai"></i> AI run time (~1.5–12 sec)</span>
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} class="horizon-svg" role="img" aria-label="Chart showing human review time growing from 8 seconds in 2022 to 80 minutes in 2026 while AI generation stays near 2 seconds">
        <defs>
          <linearGradient id="humanAreaGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="var(--threat-critical)" stop-opacity="0.28" />
            <stop offset="100%" stop-color="var(--threat-critical)" stop-opacity="0.02" />
          </linearGradient>
        </defs>

        <!-- Clean Horizontal Reference Lines -->
        <line x1={padL} y1={mapY(60)} x2={W - padR} y2={mapY(60)} stroke="var(--border-subtle)" stroke-dasharray="4 4" />
        <text x={padL - 6} y={mapY(60) + 3} text-anchor="end" class="svg-axis-label">1m</text>

        <line x1={padL} y1={mapY(1200)} x2={W - padR} y2={mapY(1200)} stroke="var(--border-subtle)" stroke-dasharray="4 4" />
        <text x={padL - 6} y={mapY(1200) + 3} text-anchor="end" class="svg-axis-label">20m</text>

        <line x1={padL} y1={mapY(4800)} x2={W - padR} y2={mapY(4800)} stroke="var(--border-subtle)" stroke-dasharray="4 4" />
        <text x={padL - 6} y={mapY(4800) + 3} text-anchor="end" class="svg-axis-label">80m</text>

        <path d={humanArea} fill="url(#humanAreaGrad)" />
        <polyline points={humanPoints} fill="none" stroke="var(--threat-critical)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
        <polyline points={machinePoints} fill="none" stroke="var(--accent-primary)" stroke-width="2.5" stroke-dasharray="5 3" stroke-linecap="round" />

        {#each trajectory as pt, i}
          {@const cx = mapX(i)}
          {@const cyH = mapY(pt.tau_verify_seconds)}
          {@const cyM = mapY(pt.tau_gen_seconds)}
          {@const active = pt.generation_id === selectedGenId}
          <g class="chart-pt-group" onclick={() => { selectedGenId = pt.generation_id; }}>
            <circle cx={cx} cy={cyH} r={active ? 7 : 4.5} fill={active ? 'var(--threat-critical)' : 'var(--bg-surface-elevated)'} stroke="var(--threat-critical)" stroke-width="2.5" />
            <circle cx={cx} cy={cyM} r={3.5} fill="var(--accent-primary)" />
            <text x={cx} y={H - 10} text-anchor="middle" class="svg-year-label" class:active-yr={active}>{pt.date.slice(0, 4)}</text>
            <text x={cx} y={Math.max(14, cyH - 11)} text-anchor="middle" class="svg-val-label" class:active-val={active}>
              {formatDuration(pt.tau_verify_seconds)}
            </text>
          </g>
        {/each}
      </svg>
    </div>

    <details class="tech-drawer">
      <summary>&#9432; Researcher details &amp; formal measurements ({activeItem.generation_id})</summary>
      <div class="tech-grid">
        <div><span>Benchmark Model:</span> <strong>{activeItem.model_label}</strong> ({activeItem.date})</div>
        <div><span>Audit Deficit (&Delta;T):</span> <strong>{activeItem.delta_t_wedge_seconds.toLocaleString()}s</strong></div>
        <div><span>Domain:</span> <strong>{activeItem.primary_domain}</strong></div>
        <div><span>CORS Rating:</span> <strong>{activeItem.cors_level.toFixed(2)} / 10 ({activeItem.cors_regime})</strong></div>
      </div>
    </details>
  {/if}
</section>

<style>
  .speed-visual-card {
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-medium);
    border-radius: 16px;
    padding: 1.35rem 1.45rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.35rem;
  }

  .sv-head {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.75rem 1rem;
    margin-bottom: 1rem;
  }

  .sv-kicker {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--accent-primary);
    margin-bottom: 0.25rem;
  }

  .sv-title {
    margin: 0 0 0.28rem;
    font-size: clamp(1.15rem, 2.2vw, 1.42rem);
    font-weight: 800;
    color: var(--text-primary);
  }

  .sv-sub {
    margin: 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
    max-width: 680px;
    line-height: 1.5;
  }

  .replay-btn {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-sunken);
    color: var(--accent-primary);
    font-weight: 700;
    font-size: 0.82rem;
    padding: 0.5rem 0.9rem;
    border-radius: 9999px;
    cursor: pointer;
    min-height: 38px;
    flex-shrink: 0;
  }

  .replay-btn:hover {
    border-color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
  }

  .year-strip {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.45rem;
    margin-bottom: 1rem;
  }

  .year-pill {
    border: 1px solid var(--border-subtle);
    background: var(--bg-surface);
    border-radius: 10px;
    padding: 0.48rem 0.55rem;
    text-align: start;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-height: 44px;
    transition: border-color 0.15s ease, background-color 0.15s ease;
  }

  .year-pill:hover {
    border-color: var(--accent-primary);
  }

  .year-pill.selected {
    border-color: var(--accent-primary);
    background: var(--threat-sovereign-bg);
  }

  .yp-year {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    color: var(--accent-primary);
  }

  .yp-name {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .race-box {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
  }

  .race-row {
    margin-bottom: 0.85rem;
  }

  .race-meta {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.3rem;
    font-size: 0.84rem;
  }

  .race-actor {
    font-weight: 600;
    color: var(--text-secondary);
  }

  .ai-num {
    font-family: var(--font-family-mono);
    color: var(--accent-primary);
    font-size: 0.96rem;
  }

  .human-num {
    font-family: var(--font-family-mono);
    color: var(--threat-critical);
    font-size: 1rem;
  }

  .lane-track {
    position: relative;
    height: 18px;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    overflow: hidden;
    display: flex;
    align-items: center;
  }

  .lane-fill {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.25s ease;
  }

  .ai-fill {
    background: var(--accent-primary);
  }

  .human-fill {
    background: var(--threat-critical);
  }

  .lane-note {
    margin-inline-start: 0.5rem;
    font-size: 0.72rem;
    color: var(--text-secondary);
    font-weight: 600;
  }

  .ratio-callout {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border-subtle);
  }

  .callout-copy {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    font-size: 0.86rem;
    color: var(--text-secondary);
    line-height: 1.45;
  }

  .callout-big {
    font-size: 1.08rem;
    color: var(--text-primary);
  }

  .curve-wrap {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.85rem 0.9rem 0.55rem;
    margin-bottom: 0.75rem;
  }

  .curve-caption-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem 1.25rem;
    font-size: 0.76rem;
    color: var(--text-secondary);
    margin-bottom: 0.4rem;
  }

  .legend-item {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-weight: 600;
  }

  .dot-human,
  .dot-ai {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
  }

  .dot-human { background: var(--threat-critical); }
  .dot-ai { background: var(--accent-primary); }

  .horizon-svg {
    width: 100%;
    height: auto;
    display: block;
    overflow: visible;
  }

  .svg-axis-label {
    font-family: var(--font-family-mono);
    font-size: 10px;
    fill: var(--text-muted);
  }

  .svg-year-label {
    font-family: var(--font-family-mono);
    font-size: 10.5px;
    fill: var(--text-secondary);
  }

  .svg-year-label.active-yr {
    fill: var(--text-primary);
    font-weight: 800;
  }

  .svg-val-label {
    font-family: var(--font-family-mono);
    font-size: 10px;
    font-weight: 700;
    fill: var(--text-secondary);
  }

  .svg-val-label.active-val {
    fill: var(--threat-critical);
    font-size: 11px;
  }

  .chart-pt-group {
    cursor: pointer;
  }

  .tech-drawer summary {
    cursor: pointer;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .tech-grid {
    margin-top: 0.55rem;
    padding: 0.7rem 0.85rem;
    border-radius: 10px;
    background: var(--bg-surface-sunken);
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.4rem 0.9rem;
    font-size: 0.78rem;
    color: var(--text-secondary);
  }

  .tech-grid strong {
    color: var(--text-primary);
  }

  @media (max-width: 820px) {
    .year-strip {
      grid-template-columns: repeat(3, 1fr);
    }
    .tech-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 540px) {
    .speed-visual-card {
      padding: 1rem;
    }
    .year-strip {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
