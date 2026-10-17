<script lang="ts">
  let machineSpeed = 0.8; // ms
  let humanAuditTime = 2560; // seconds (~42 minutes for 1,000 lines)

  // Interactive slider factor (1x to 5,000x)
  let simulatedModelTier = 4; // 1: GPT-3.5, 2: GPT-4, 3: Claude 3.5, 4: Current Swarm

  const tiers = [
    { name: 'Human Biology (Baseline)', machineMs: 200, humanAuditSec: 300, ratio: '1x', cors: '1.0' },
    { name: 'GPT-4 Era (2023)', machineMs: 15.0, humanAuditSec: 900, ratio: '60x', cors: '4.2' },
    { name: 'Claude 3.5 Sonnet (2024)', machineMs: 4.2, humanAuditSec: 1800, ratio: '428x', cors: '6.8' },
    { name: 'Autonomous Swarm / EXP-07-SYN', machineMs: 0.8, humanAuditSec: 2560, ratio: '3,200x', cors: '10.0' },
  ];

  $: currentTier = tiers[simulatedModelTier - 1];
</script>

<div class="wedge-widget-card">
  <div class="wedge-header">
    <div class="badge-row">
      <span class="mono-badge">INTERACTIVE SPEED COMPARATOR</span>
      <span class="cors-badge">CORS {currentTier.cors}</span>
    </div>
    <h4 class="wedge-title">The Verification Latency Wedge</h4>
    <p class="wedge-desc">
      Drag to observe how execution velocity decouples from biological human supervisory capacity:
    </p>
  </div>

  <div class="slider-wrapper">
    <input
      type="range"
      min="1"
      max="4"
      step="1"
      bind:value={simulatedModelTier}
      class="tier-slider"
      aria-label="Model Generation Tier"
    />
    <div class="slider-marks">
      <span>Baseline</span>
      <span>GPT-4</span>
      <span>Frontier</span>
      <span class="active-mark">Swarm (CORS 10)</span>
    </div>
  </div>

  <div class="comparison-grid">
    <div class="speed-box machine">
      <span class="box-label">Machine Code Synthesis</span>
      <span class="box-value">{currentTier.machineMs} ms</span>
      <span class="box-sub">Sub-millisecond execution</span>
    </div>

    <div class="speed-box human">
      <span class="box-label">Human Expert Audit</span>
      <span class="box-value">{currentTier.humanAuditSec} s</span>
      <span class="box-sub">Biological comprehension buffer</span>
    </div>

    <div class="speed-box divergence">
      <span class="box-label">Supervisory Gap</span>
      <span class="box-value highlight">{currentTier.ratio}</span>
      <span class="box-sub">Speed Divergence Multiplier</span>
    </div>
  </div>

  <div class="widget-footer">
    <span class="verdict-text">
      <strong>Verdict:</strong>
      {#if simulatedModelTier === 4}
        Human-in-the-loop is an administrative fiction. Autonomous systems execute 3,200x faster than audit speed.
      {:else if simulatedModelTier === 3}
        Cognitive friction causes significant operator defect leakage (>40%).
      {:else}
        Human audit remains feasible within synchronous operational limits.
      {/if}
    </span>
  </div>
</div>

<style>
  .wedge-widget-card {
    margin: 2rem 0;
    padding: 1.5rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-radius: 12px;
    box-shadow: var(--shadow-sm);
  }

  .badge-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .mono-badge {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--accent-primary);
    letter-spacing: 0.08em;
  }

  .cors-badge {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    font-weight: 800;
    color: var(--threat-critical);
    background: var(--threat-critical-bg);
    border: 1px solid var(--threat-critical-border);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
  }

  .wedge-title {
    margin: 0 0 0.35rem 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .wedge-desc {
    margin: 0 0 1.25rem 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .slider-wrapper {
    margin-bottom: 1.5rem;
  }

  .tier-slider {
    width: 100%;
    cursor: pointer;
    accent-color: var(--accent-primary);
  }

  .slider-marks {
    display: flex;
    justify-content: space-between;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    color: var(--text-muted);
    margin-top: 0.35rem;
  }

  .active-mark {
    color: var(--threat-critical);
    font-weight: 700;
  }

  .comparison-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .speed-box {
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.85rem 1rem;
    text-align: center;
  }

  .box-label {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 0.25rem;
  }

  .box-value {
    display: block;
    font-family: var(--font-family-mono);
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
  }

  .box-value.highlight {
    color: var(--accent-primary);
  }

  .box-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .widget-footer {
    padding-top: 0.85rem;
    border-top: 1px solid var(--border-subtle);
    font-size: 0.825rem;
    color: var(--text-secondary);
    line-height: 1.4;
  }

  @media (max-width: 640px) {
    .comparison-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
