<script lang="ts">
  import scoresData from '../data/country_scores.json';

  let {
    selectedId = null,
    countries = scoresData.countries,
    onClose = () => {}
  }: {
    selectedId: string | null;
    countries?: any[];
    onClose?: () => void;
  } = $props();

  const base = (import.meta.env.BASE_URL || '').replace(/\/$/, '');

  let selected = $derived.by(() => {
    if (!selectedId) return null;
    return countries.find((c: any) => (c.id || '').toLowerCase() === selectedId.toLowerCase()) ?? null;
  });

  function tier(c: any) {
    const h = c?.H_Layer2 ?? c?.H_L2 ?? c?.variants?.hsri_leontief ?? 0;
    const delta = c?.rank_delta ?? c?.variants?.rank_delta_leo ?? 0;
    if (h >= 0.40 && delta > -15) {
      return { label: 'Resilient Sovereignty', color: '#10b981', bg: 'rgba(16,185,129,0.14)' };
    }
    if (h >= 0.25 && delta > -15) {
      return { label: 'Transitional', color: '#f59e0b', bg: 'rgba(245,158,11,0.14)' };
    }
    return { label: 'High-Compute Fragility Trap', color: '#ef4444', bg: 'rgba(239,68,68,0.14)' };
  }

  function halfLifeLabel(h: any) {
    const v = h ?? 48;
    if (v >= 336) return `${v}+ Hours · Resilient Autarky`;
    if (v >= 72) return `${v} Hours · Sustained Hold`;
    if (v >= 24) return `${v} Hours · Constrained Window`;
    return `${v} Hours · Extreme Cloud Exposure`;
  }

  // Deterministic 2-sentence cliff from dataset fields (zero hallucination)
  function cliff(c: any): string {
    if (!c) return '';
    const b = c.variants?.bottleneck_pillar ?? c.bottleneck_pillar ?? 'institutional capacity';
    const isTrap = c.variants?.high_compute_trap ?? c.high_compute_trap ?? false;
    const trap = isTrap
      ? 'High digital infrastructure masks acute deficits in ' + b.toLowerCase() + '.'
      : 'Balanced capacity preserves manual fallback under severance.';
    const exp = c.exposure != null ? ` Macro exposure ${c.exposure}%.` : '';
    return `${trap}${exp} Bottleneck: ${b}.`;
  }

  let sheetY = $state(0);
  let dragging = $state(false);
  let startTouchY = 0;

  function onTouchStart(e: TouchEvent) {
    dragging = true;
    startTouchY = e.touches[0].clientY;
  }

  function onTouchMove(e: TouchEvent) {
    if (!dragging) return;
    const dy = e.touches[0].clientY - startTouchY;
    if (dy > 0) sheetY = dy;
  }

  function onTouchEnd() {
    dragging = false;
    if (sheetY > 120) {
      onClose();
    }
    sheetY = 0;
  }

  function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') {
      onClose();
    }
  }
</script>

<svelte:window onkeydown={onKeydown} />

{#if selected}
  {@const t = tier(selected)}
  {@const th = selected.T_half_h ?? selected.variants?.T_half_h ?? 48}
  {@const d = selected.rank_delta ?? selected.variants?.rank_delta_leo ?? 0}
  <aside
    class="inspector"
    role="dialog"
    aria-modal="false"
    aria-label={`${selected.name} sovereign telemetry`}
    style:transform={sheetY ? `translateY(${sheetY}px)` : undefined}
    ontouchstart={onTouchStart}
    ontouchmove={onTouchMove}
    ontouchend={onTouchEnd}
  >
    <div class="drag-handle" aria-hidden="true"></div>
    <button type="button" class="close" aria-label="Close inspector" onclick={onClose}>×</button>

    <div class="head">
      <div class="flag" aria-hidden="true">{selected.flag ?? '◆'}</div>
      <div class="head-info">
        <div class="name">
          {selected.name} <span class="code">{selected.code}</span>
        </div>
        <div class="meta">
          {selected.region ?? '—'} · {selected.peerGroup ?? selected.incomeGroup ?? 'Benchmark'} · Rank #{selected.rank_L2 ?? selected.rank}
        </div>
      </div>
      <span class="tier" style:background={t.bg} style:color={t.color} style:border-color={t.color}>
        {t.label}
      </span>
    </div>

    <div class="metrics">
      <div class="metric">
        <div class="label">Decoupling Half-Life (T<sub>half</sub>)</div>
        <div class="value" style:color={t.color}>{halfLifeLabel(th)}</div>
        {#if selected.ci_95 || selected.variants?.ci_95}
          <div class="sub">
            95% CI [{(selected.ci_95 ?? selected.variants?.ci_95)[0]} – {(selected.ci_95 ?? selected.variants?.ci_95)[1]}] · Dirichlet B=1000
          </div>
        {/if}
      </div>
      <div class="metric">
        <div class="label">Dual-Layer Rank Delta</div>
        <div class="delta">
          L1 #{selected.rank_L1 ?? selected.legacy_rank_linear ?? '—'} → L2 #{selected.rank_L2 ?? selected.rank ?? '—'}
          <span class="badge" class:neg={d < 0} class:pos={d > 0}>
            {d === 0 ? '— 0' : d < 0 ? `▼ ${d}` : `▲ +${d}`}
          </span>
        </div>
        <div class="sub">
          Leontief floor β=0.50 · {selected.variants?.high_compute_trap || selected.high_compute_trap ? 'Flagged as High-Compute Trap' : 'Balanced Profile'}
        </div>
      </div>
    </div>

    <div class="pillars">
      <div class="label">4-Pillar Balance</div>
      <div class="bars">
        {#each [
          ['P1 Cognitive Discernment', selected.pillars?.critical_discernment ?? selected.pillars?.ai_literacy ?? selected.pillars?.P1 ?? 0, '#38bdf8'],
          ['P2 Institutional Agency', selected.pillars?.institutional_governance ?? selected.pillars?.institutional ?? selected.pillars?.P2 ?? 0, '#8b5cf6'],
          ['P3 Tech Exposure', selected.pillars?.digital_infrastructure ?? selected.pillars?.technological ?? selected.pillars?.P3 ?? 0, '#f59e0b'],
          ['P4 Societal Resilience', selected.pillars?.social ?? selected.pillars?.economic ?? selected.pillars?.P4 ?? 0, '#10b981']
        ] as [pLabel, val, col]}
          <div class="bar-row">
            <span class="bar-label">{pLabel}</span>
            <div class="bar-track">
              <div
                class="bar-fill"
                style:width={`${Math.max(4, Math.min(100, Number(val)))}%`}
                style:background={col}
              ></div>
            </div>
            <span class="bar-val">{Number(val).toFixed(1)}</span>
          </div>
        {/each}
      </div>
    </div>

    <div class="cliff">
      <div class="label">Decoupling Cliff</div>
      <p>{cliff(selected)}</p>
    </div>

    <a class="cta" href={`${base}/countries/${(selected.id || '').toLowerCase()}/`}>
      View Full Sovereign Dossier &amp; SWOT Breakdown →
    </a>
    <div class="prov">HSRI Research Consortium · DOI 10.5281/zenodo.23441742 · CC BY-SA 4.0</div>
  </aside>
{/if}

<style>
  .inspector {
    position: relative;
    background: var(--bg-surface-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 18px;
    box-shadow: var(--shadow-lg);
    display: flex;
    flex-direction: column;
    gap: 14px;
    box-sizing: border-box;
  }
  .drag-handle {
    display: none;
  }
  .close {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 28px;
    height: 28px;
    border-radius: 9999px;
    border: 1px solid var(--border-subtle);
    background: var(--bg-surface);
    color: var(--text-muted);
    cursor: pointer;
    font-size: 18px;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
  }
  .close:hover {
    color: var(--text-primary);
    border-color: var(--border-medium);
  }
  .head {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    flex-wrap: wrap;
    padding-right: 28px;
  }
  .flag {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: grid;
    place-items: center;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    font-size: 18px;
    flex-shrink: 0;
  }
  .head-info {
    flex: 1;
    min-width: 140px;
  }
  .name {
    font-weight: 800;
    color: var(--text-primary);
    font-size: 1.05rem;
  }
  .code {
    font-family: var(--font-family-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
    border: 1px solid var(--border-subtle);
    padding: 1px 6px;
    border-radius: 9999px;
    margin-left: 6px;
    vertical-align: middle;
  }
  .meta {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 2px;
  }
  .tier {
    margin-left: auto;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    padding: 4px 8px;
    border-radius: 9999px;
    border: 1px solid;
    white-space: nowrap;
  }
  .metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  .label {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 4px;
  }
  .value {
    font-weight: 800;
    font-size: 0.98rem;
    color: var(--text-primary);
    line-height: 1.3;
  }
  .sub {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 3px;
    line-height: 1.4;
  }
  .delta {
    font-family: var(--font-family-mono);
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
  }
  .badge {
    font-size: 0.72rem;
    padding: 2px 7px;
    border-radius: 9999px;
    border: 1px solid var(--border-subtle);
  }
  .badge.neg {
    color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
    border-color: rgba(239, 68, 68, 0.28);
  }
  .badge.pos {
    color: #10b981;
    background: rgba(16, 185, 129, 0.12);
    border-color: rgba(16, 185, 129, 0.28);
  }
  .bars {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .bar-row {
    display: grid;
    grid-template-columns: 160px 1fr 38px;
    gap: 8px;
    align-items: center;
  }
  .bar-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .bar-track {
    height: 7px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    border-radius: 9999px;
    overflow: hidden;
  }
  .bar-fill {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.3s ease;
  }
  .bar-val {
    font-family: var(--font-family-mono);
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--text-primary);
    text-align: right;
  }
  .cliff p {
    margin: 0;
    font-size: 0.86rem;
    color: var(--text-secondary);
    line-height: 1.5;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    padding: 10px 12px;
    border-radius: 10px;
  }
  .cta {
    display: block;
    text-align: center;
    padding: 10px 14px;
    border-radius: 10px;
    background: var(--accent-primary);
    color: white;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.88rem;
    transition: background 0.15s ease;
  }
  .cta:hover {
    background: var(--accent-primary-hover);
  }
  .prov {
    font-family: var(--font-family-mono);
    font-size: 0.62rem;
    color: var(--text-muted);
    text-align: center;
  }

  /* Mobile: bottom sheet */
  @media (max-width: 768px) {
    .inspector {
      position: fixed;
      left: 10px;
      right: 10px;
      bottom: 10px;
      z-index: 40;
      max-height: min(72vh, 580px);
      overflow-y: auto;
      border-radius: 16px;
      background: rgba(15, 23, 42, 0.94);
      backdrop-filter: blur(16px) saturate(1.2);
      -webkit-backdrop-filter: blur(16px) saturate(1.2);
      border-color: rgba(255, 255, 255, 0.12);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
      animation: sheetIn 0.32s cubic-bezier(0.16, 1, 0.3, 1);
    }
    :global([data-theme="light"]) .inspector {
      background: rgba(255, 255, 255, 0.95);
      border-color: rgba(15, 23, 42, 0.12);
    }
    .drag-handle {
      display: block;
      width: 36px;
      height: 4px;
      border-radius: 9999px;
      background: var(--border-medium);
      margin: 0 auto 6px auto;
      opacity: 0.9;
    }
    .metrics {
      grid-template-columns: 1fr;
    }
    .bar-row {
      grid-template-columns: 1fr 1fr 38px;
    }
    .bar-row .bar-label {
      grid-column: 1 / -1;
    }
  }
  @keyframes sheetIn {
    from {
      transform: translateY(18px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
</style>
