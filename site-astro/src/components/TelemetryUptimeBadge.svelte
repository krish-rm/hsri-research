<script lang="ts">
  import { onMount } from 'svelte';

  interface BadgeData {
    schemaVersion: number;
    label: string;
    message: string;
    color: string;
    is_fallback: boolean;
    provenance: string;
    data_timestamp: string | null;
    window_30d: { total_runs: number; success_runs: number; success_rate: number };
    window_7d: { total_runs: number; success_runs: number; success_rate: number };
  }

  let badge: BadgeData | null = null;
  let loading = true;
  let error: string | null = null;

  onMount(async () => {
    try {
      const res = await fetch('/badges/telemetry-uptime.json');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      badge = await res.json();
    } catch (e: any) {
      error = e?.message || 'badge unavailable';
      // fallback: try src/data path (Astro dev)
      try {
        const alt = await fetch('/src/data/telemetry-uptime.json');
        if (alt.ok) badge = await alt.json();
        if (badge) error = null;
      } catch {}
    } finally {
      loading = false;
    }
  });

  $: dotColor =
    !badge ? '#64748b' :
    badge.color === 'brightgreen' ? '#10b981' :
    badge.color === 'yellow' ? '#f59e0b' :
    badge.color === 'orange' ? '#f97316' : '#ef4444';

  $: bgColor =
    !badge ? 'rgba(100,116,139,0.12)' :
    badge.color === 'brightgreen' ? 'rgba(16,185,129,0.12)' :
    badge.color === 'yellow' ? 'rgba(245,158,11,0.12)' :
    badge.color === 'orange' ? 'rgba(249,115,22,0.15)' : 'rgba(239,68,68,0.15)';

  $: borderColor =
    !badge ? 'rgba(100,116,139,0.3)' :
    badge.color === 'brightgreen' ? 'rgba(16,185,129,0.35)' :
    badge.color === 'yellow' ? 'rgba(245,158,11,0.35)' :
    badge.color === 'orange' ? 'rgba(249,115,22,0.4)' : 'rgba(239,68,68,0.4)';
</script>

{#if loading}
  <div class="uptime-badge skeleton" aria-busy="true">
    <span class="badge-dot" style="background:#64748b"></span>
    <span class="badge-text">Checking live telemetry…</span>
  </div>
{:else if badge}
  <div class="uptime-badge" style="background:{bgColor}; border-color:{borderColor}">
    <span class="badge-dot" style="background:{dotColor}; box-shadow: 0 0 6px {dotColor}"></span>
    <span class="badge-label">Live Telemetry:</span>
    <span class="badge-msg">{badge.message}</span>
    {#if badge.is_fallback}
      <span class="badge-fallback">· fallback</span>
    {/if}
    <span class="badge-meta">
      · {badge.provenance} · 30d {(badge.window_30d.success_rate * 100).toFixed(1)}% · 7d {(badge.window_7d.success_rate * 100).toFixed(1)}%
    </span>
    <a class="badge-link" href="https://github.com/krish-rm/hsri-research/actions/workflows/precursor-sentinel.yml" target="_blank" rel="noopener">→ logs</a>
  </div>
{:else if error}
  <div class="uptime-badge" style="background:rgba(100,116,139,0.08); border-color:rgba(100,116,139,0.2)">
    <span class="badge-dot" style="background:#64748b"></span>
    <span class="badge-text">Telemetry badge unavailable · {error}</span>
  </div>
{/if}

<style>
  .uptime-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    flex-wrap: wrap;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.4rem 0.75rem;
    border-radius: 9999px;
    border: 1px solid;
    margin: 0.75rem 0 1.25rem 0;
    line-height: 1.3;
  }
  .uptime-badge.skeleton {
    background: rgba(100,116,139,0.08);
    border-color: rgba(100,116,139,0.15);
    color: #94a3b8;
  }
  .badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .badge-label { color: #e2e8f0; }
  .badge-msg { color: #f8fafc; font-weight: 700; }
  .badge-fallback { color: #fb923c; font-weight: 700; }
  .badge-meta { color: #94a3b8; font-weight: 500; font-size: 0.72rem; }
  .badge-link {
    color: #38bdf8;
    text-decoration: none;
    font-size: 0.72rem;
    margin-left: 0.15rem;
  }
  .badge-link:hover { text-decoration: underline; }
  .badge-text { color: #94a3b8; }
</style>
