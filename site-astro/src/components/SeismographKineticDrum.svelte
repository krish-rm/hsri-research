<script lang="ts">
  import { onMount } from 'svelte';

  let {
    score = 8.44,
    stream1Score = 8.78,
    stream2Score = 6.55,
    stream3Score = 10.0
  }: {
    score?: number;
    stream1Score?: number;
    stream2Score?: number;
    stream3Score?: number;
  } = $props();

  let canvasEl: HTMLCanvasElement | null = $state(null);
  let containerEl: HTMLDivElement | null = $state(null);
  let width = $state(800);
  let height = $state(220);
  let rafId = 0;
  let offset = 0;

  // Pre-generate pseudo-random deterministic noise arrays for smooth waveform rendering
  const pointCount = 300;
  const pWaveSeed: number[] = [];
  const sWaveSeed: number[] = [];
  const surfWaveSeed: number[] = [];

  for (let i = 0; i < pointCount * 2; i++) {
    pWaveSeed.push((Math.sin(i * 0.35) * 0.5 + Math.sin(i * 1.2) * 0.3 + (Math.random() - 0.5) * 0.4));
    sWaveSeed.push((Math.sin(i * 0.18) * 0.7 + Math.cos(i * 0.6) * 0.3 + (Math.random() - 0.5) * 0.2));
    surfWaveSeed.push((Math.sin(i * 0.08) * 0.9 + Math.sin(i * 0.25) * 0.4 + (Math.random() - 0.5) * 0.15));
  }

  function measure() {
    if (!containerEl) return;
    width = containerEl.clientWidth || 800;
    if (canvasEl) {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvasEl.width = width * dpr;
      canvasEl.height = height * dpr;
      canvasEl.style.width = width + 'px';
      canvasEl.style.height = height + 'px';
    }
  }

  function renderWaveform() {
    if (!canvasEl) return;
    const ctx = canvasEl.getContext('2d');
    if (!ctx) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    ctx.clearRect(0, 0, width * dpr, height * dpr);
    ctx.save();
    ctx.scale(dpr, dpr);

    // Background well (Dynamic: Aged mechanical roll paper in light/cream mode vs obsidian well in dark mode)
    const isPaperTheme = typeof document !== 'undefined' && (document.documentElement.getAttribute('data-theme') === 'light' || document.documentElement.getAttribute('data-theme') === 'paper');
    ctx.fillStyle = isPaperTheme ? '#f0ebd9' : '#060911';
    ctx.fillRect(0, 0, width, height);

    // Grid lines (drum roll lines)
    ctx.strokeStyle = isPaperTheme ? 'rgba(70, 50, 30, 0.08)' : 'rgba(255, 255, 255, 0.04)';
    ctx.lineWidth = 1;
    const gridStep = 40;
    const gridOffset = (offset * 0.8) % gridStep;
    for (let x = -gridOffset; x < width; x += gridStep) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }

    const rowHeight = height / 3;

    // Baseline dividers
    ctx.strokeStyle = isPaperTheme ? 'rgba(70, 50, 30, 0.15)' : 'rgba(255, 255, 255, 0.08)';
    ctx.beginPath();
    ctx.moveTo(0, rowHeight);
    ctx.lineTo(width, rowHeight);
    ctx.moveTo(0, rowHeight * 2);
    ctx.lineTo(width, rowHeight * 2);
    ctx.stroke();

    // 1. CHANNEL P (Top): Autonomy Micro-Tremors
    drawTrace(
      ctx,
      0,
      rowHeight,
      pWaveSeed,
      stream1Score / 10,
      '#ef4444',
      offset * 1.4,
      14
    );

    // 2. CHANNEL S (Middle): Latent Language Compression
    drawTrace(
      ctx,
      rowHeight,
      rowHeight * 2,
      sWaveSeed,
      stream2Score / 10,
      '#f59e0b',
      offset * 0.9,
      18
    );

    // 3. CHANNEL SURFACE (Bottom): Verification Latency Wedge Rupture
    drawTrace(
      ctx,
      rowHeight * 2,
      height,
      surfWaveSeed,
      stream3Score / 10,
      '#38bdf8',
      offset * 0.6,
      24
    );

    // Red needle playhead at 85% width
    const playheadX = width - 60;
    ctx.strokeStyle = 'rgba(239, 68, 68, 0.7)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(playheadX, 0);
    ctx.lineTo(playheadX, height);
    ctx.stroke();
    ctx.setLineDash([]);

    // Playhead sensor dot
    ctx.fillStyle = '#ef4444';
    ctx.shadowColor = '#ef4444';
    ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.arc(playheadX, height / 2, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    ctx.restore();

    offset += 0.85;
    rafId = requestAnimationFrame(renderWaveform);
  }

  function drawTrace(
    ctx: CanvasRenderingContext2D,
    topY: number,
    bottomY: number,
    seed: number[],
    intensity: number,
    color: string,
    timeOffset: number,
    maxAmp: number
  ) {
    const midY = (topY + bottomY) / 2;
    const points = 120;
    const dx = width / points;

    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.6;

    for (let i = 0; i <= points; i++) {
      const seedIdx = Math.floor((i + timeOffset) % pointCount);
      const amp = (seed[seedIdx] || 0) * maxAmp * (0.3 + intensity * 0.7);
      const x = i * dx;
      const y = midY + amp;

      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    }
    ctx.stroke();

    // Subtle glow on intense spikes
    if (intensity > 0.75) {
      ctx.save();
      ctx.strokeStyle = color;
      ctx.globalAlpha = 0.25;
      ctx.lineWidth = 4;
      ctx.stroke();
      ctx.restore();
    }
  }

  onMount(() => {
    measure();
    rafId = requestAnimationFrame(renderWaveform);

    const ro = new ResizeObserver(measure);
    if (containerEl) ro.observe(containerEl);
    window.addEventListener('resize', measure);

    const onVisibility = () => {
      if (document.visibilityState === 'visible' && !rafId) {
        rafId = requestAnimationFrame(renderWaveform);
      } else if (document.visibilityState === 'hidden' && rafId) {
        cancelAnimationFrame(rafId);
        rafId = 0;
      }
    };
    document.addEventListener('visibilitychange', onVisibility);

    return () => {
      cancelAnimationFrame(rafId);
      ro.disconnect();
      window.removeEventListener('resize', measure);
      document.removeEventListener('visibilitychange', onVisibility);
    };
  });
</script>

<div class="drum-container" bind:this={containerEl}>
  <div class="drum-header">
    <div class="drum-title">
      <span class="live-dot"></span>
      <span>LIVE KINETIC SEISMOGRAM DRUM · SYNCHRONIZED TRIAD SENSORS</span>
    </div>
    <div class="drum-scale">
      <span>Time Drum: 1 sec = 24h Telemetry</span>
    </div>
  </div>

  <canvas bind:this={canvasEl} class="drum-canvas"></canvas>

  <div class="drum-legend">
    <div class="legend-channel">
      <span class="chan-dot" style="background: #ef4444;"></span>
      <span class="chan-name">P-Wave: Autonomy Micro-Tremor (8.78/10)</span>
      <span class="chan-desc">M2M tool execution spikes</span>
    </div>
    <div class="legend-channel">
      <span class="chan-dot" style="background: #f59e0b;"></span>
      <span class="chan-name">S-Wave: Latent Shorthand Drift (6.55/10)</span>
      <span class="chan-desc">Compressed machine dialects</span>
    </div>
    <div class="legend-channel">
      <span class="chan-dot" style="background: #38bdf8;"></span>
      <span class="chan-name">Surface Rupture: Audit Debt (10.0/10)</span>
      <span class="chan-desc">3,200x oversight gap expansion</span>
    </div>
  </div>
</div>

<style>
  .drum-container {
    background: #060911;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 14px 16px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  }
  .drum-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    font-family: var(--font-family-mono, monospace);
    font-size: 0.7rem;
    color: var(--text-muted, #94a3b8);
  }
  .drum-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--text-primary, #f8fafc);
  }
  .live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #ef4444;
    box-shadow: 0 0 8px #ef4444;
    animation: blink 1.2s infinite ease-in-out;
  }
  @keyframes blink {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
  }
  .drum-canvas {
    display: block;
    width: 100%;
    height: 220px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }
  .drum-legend {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    font-size: 0.72rem;
  }
  .legend-channel {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .chan-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
  }
  .chan-name {
    font-weight: 700;
    color: var(--text-primary, #f8fafc);
    display: flex;
    align-items: center;
  }
  .chan-desc {
    color: var(--text-muted, #64748b);
    font-size: 0.68rem;
    padding-left: 11px;
  }
  @media (max-width: 820px) {
    .drum-legend {
      grid-template-columns: 1fr;
      gap: 8px;
    }
    .drum-canvas {
      height: 180px;
    }
  }
</style>
