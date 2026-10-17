<script lang="ts">
  import wedgeHistoryData from '../data/wedge_history.json';

  const trajectory = wedgeHistoryData.benchmark_trajectory || [];
  let selectedGenId = $state('GEN-06');

  let activeItem = $derived.by(() => {
    return trajectory.find((t: any) => t.generation_id === selectedGenId) || trajectory[trajectory.length - 1];
  });
</script>

<div class="horizon-chart-wrap">
  <div class="chart-header">
    <div>
      <div class="chart-tag">STREAM 3 HISTORICAL EMPIRICAL RECORD</div>
      <h3 class="chart-title">The Human Verification Horizon (2022–2026)</h3>
      <p class="chart-subtitle">
        Visualizing the physical collapse of real-time human oversight across 6 model generations.
        Machine execution time flatlines at 1.5s while human audit time rockets to 80 minutes.
      </p>
    </div>
    <div class="horizon-badge">
      <span class="hz-label">Current Divergence Ratio</span>
      <span class="hz-val text-danger">3,200× Speed Deficit</span>
    </div>
  </div>

  <!-- Timeline Cards / Generation Scrubbing Strip -->
  <div class="gen-strip" role="tablist" aria-label="Select model generation">
    {#each trajectory as gen}
      {@const isSelected = selectedGenId === gen.generation_id}
      <button
        type="button"
        class="gen-card"
        class:selected={isSelected}
        onclick={() => selectedGenId = gen.generation_id}
      >
        <span class="gen-date">{gen.date.slice(0, 7)}</span>
        <span class="gen-model">{gen.model_label.split('(')[0].trim()}</span>
        <span class="gen-ratio" class:crisis={gen.wedge_ratio >= 100}>{gen.wedge_ratio}×</span>
        <span class="gen-regime">{gen.cors_regime.split(' ')[0]}</span>
      </button>
    {/each}
  </div>

  <!-- Active Generation Deep Breakdown -->
  {#if activeItem}
    <div class="gen-detail-box">
      <div class="detail-header">
        <div class="dh-left">
          <span class="dh-id">{activeItem.generation_id}</span>
          <span class="dh-title">{activeItem.model_label}</span>
          <span class="dh-date">({activeItem.date})</span>
        </div>
        <span class="dh-status-pill" class:crisis={activeItem.wedge_ratio >= 100}>
          {activeItem.cors_regime}
        </span>
      </div>

      <div class="comparison-bar-grid">
        <!-- Machine Bar -->
        <div class="comp-col">
          <div class="comp-label">
            <span>Machine Generation Time</span>
            <strong class="text-accent">{activeItem.tau_gen_seconds}s</strong>
          </div>
          <div class="bar-shell">
            <div class="bar-core machine" style="width: {Math.max(3, (activeItem.tau_gen_seconds / 15) * 100)}%;"></div>
          </div>
          <span class="comp-caption">Autonomous model output</span>
        </div>

        <!-- Human Bar -->
        <div class="comp-col">
          <div class="comp-label">
            <span>Expert Human Audit Time</span>
            <strong class="text-danger">
              {activeItem.tau_verify_seconds >= 60 ? `${(activeItem.tau_verify_seconds / 60).toFixed(1)} min` : `${activeItem.tau_verify_seconds}s`}
            </strong>
          </div>
          <div class="bar-shell">
            <div class="bar-core human" style="width: {Math.max(4, (activeItem.tau_verify_seconds / 4800) * 100)}%;"></div>
          </div>
          <span class="comp-caption">Independent expert security audit</span>
        </div>
      </div>

      <div class="detail-stats-strip">
        <div class="ds-item">
          <span class="ds-lbl">Verification Deficit (ΔT)</span>
          <span class="ds-num text-danger">{activeItem.delta_t_wedge_seconds.toLocaleString()}s</span>
          <span class="ds-sub">≈ {(activeItem.delta_t_wedge_seconds / 60).toFixed(1)} minutes behind</span>
        </div>
        <div class="ds-item">
          <span class="ds-lbl">Speed Deficit Ratio</span>
          <span class="ds-num text-danger">{activeItem.wedge_ratio.toLocaleString()}×</span>
          <span class="ds-sub">Audit time / generation time</span>
        </div>
        <div class="ds-item">
          <span class="ds-lbl">CORS Richter Level</span>
          <span class="ds-num text-warning">{activeItem.cors_level.toFixed(2)} / 10.0</span>
          <span class="ds-sub">{activeItem.cors_regime}</span>
        </div>
        <div class="ds-item">
          <span class="ds-lbl">Primary Task Domain</span>
          <span class="ds-domain">{activeItem.primary_domain}</span>
          <span class="ds-sub">Hardware: {activeItem.hardware_tier}</span>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .horizon-chart-wrap {
    background: var(--bg-surface, #0f172a);
    border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.1));
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-md, 0 4px 6px -1px rgba(0, 0, 0, 0.2));
  }
  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 18px;
    flex-wrap: wrap;
  }
  .chart-tag {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--accent-primary, #38bdf8);
    margin-bottom: 4px;
  }
  .chart-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-primary, #f8fafc);
    margin: 0 0 6px 0;
  }
  .chart-subtitle {
    font-size: 0.88rem;
    color: var(--text-secondary, #94a3b8);
    max-width: 740px;
    line-height: 1.5;
    margin: 0;
  }
  .horizon-badge {
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.3);
    padding: 8px 14px;
    border-radius: 10px;
    text-align: right;
  }
  .hz-label {
    display: block;
    font-family: var(--font-family-mono, monospace);
    font-size: 0.65rem;
    color: var(--text-muted, #94a3b8);
    text-transform: uppercase;
  }
  .hz-val {
    font-family: var(--font-family-mono, monospace);
    font-weight: 800;
    font-size: 1.05rem;
  }
  .gen-strip {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 8px;
    margin-bottom: 18px;
  }
  .gen-card {
    background: var(--bg-surface-sunken, #060911);
    border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08));
    border-radius: 10px;
    padding: 10px 8px;
    text-align: left;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    gap: 2px;
    transition: all 0.15s ease;
  }
  .gen-card:hover {
    border-color: var(--accent-primary, #38bdf8);
    background: rgba(56, 189, 248, 0.04);
  }
  .gen-card.selected {
    border-color: var(--accent-primary, #38bdf8);
    background: rgba(56, 189, 248, 0.08);
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
  }
  .gen-date {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.65rem;
    color: var(--text-muted, #64748b);
  }
  .gen-model {
    font-weight: 700;
    font-size: 0.8rem;
    color: var(--text-primary, #f8fafc);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .gen-ratio {
    font-family: var(--font-family-mono, monospace);
    font-weight: 800;
    font-size: 0.88rem;
    color: #38bdf8;
    margin-top: 2px;
  }
  .gen-ratio.crisis {
    color: #ef4444;
  }
  .gen-regime {
    font-size: 0.65rem;
    color: var(--text-muted, #94a3b8);
  }
  .gen-detail-box {
    background: var(--bg-surface-elevated, #1e293b);
    border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.1));
    border-radius: 12px;
    padding: 18px;
  }
  .detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 10px;
  }
  .dh-left {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .dh-id {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.72rem;
    font-weight: 800;
    background: rgba(255, 255, 255, 0.08);
    padding: 2px 7px;
    border-radius: 6px;
    color: var(--text-muted, #94a3b8);
  }
  .dh-title {
    font-weight: 800;
    font-size: 1.05rem;
    color: var(--text-primary, #f8fafc);
  }
  .dh-date {
    font-size: 0.82rem;
    color: var(--text-muted, #64748b);
  }
  .dh-status-pill {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 9999px;
    background: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.28);
  }
  .dh-status-pill.crisis {
    background: rgba(239, 68, 68, 0.12);
    color: #ef4444;
    border-color: rgba(239, 68, 68, 0.3);
  }
  .comparison-bar-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 18px;
  }
  .comp-col {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .comp-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.82rem;
    color: var(--text-secondary, #cbd5e1);
  }
  .bar-shell {
    height: 10px;
    background: var(--bg-surface-sunken, #060911);
    border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.08));
    border-radius: 9999px;
    overflow: hidden;
  }
  .bar-core {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.3s ease;
  }
  .bar-core.machine {
    background: #38bdf8;
  }
  .bar-core.human {
    background: #ef4444;
  }
  .comp-caption {
    font-size: 0.72rem;
    color: var(--text-muted, #64748b);
  }
  .detail-stats-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    padding-top: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }
  .ds-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .ds-lbl {
    font-family: var(--font-family-mono, monospace);
    font-size: 0.65rem;
    text-transform: uppercase;
    color: var(--text-muted, #94a3b8);
  }
  .ds-num {
    font-family: var(--font-family-mono, monospace);
    font-weight: 800;
    font-size: 1rem;
  }
  .ds-domain {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-primary, #f8fafc);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .ds-sub {
    font-size: 0.7rem;
    color: var(--text-muted, #64748b);
  }
  .text-danger { color: #ef4444; }
  .text-warning { color: #f59e0b; }
  .text-accent { color: #38bdf8; }

  @media (max-width: 900px) {
    .gen-strip {
      grid-template-columns: repeat(3, 1fr);
    }
    .detail-stats-strip {
      grid-template-columns: 1fr 1fr;
    }
  }
  @media (max-width: 600px) {
    .comparison-bar-grid {
      grid-template-columns: 1fr;
    }
    .detail-stats-strip {
      grid-template-columns: 1fr;
    }
  }
</style>
