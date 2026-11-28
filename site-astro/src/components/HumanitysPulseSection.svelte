<script lang="ts">
  import { dict } from '../i18n/store';

  export let base = '';
  export let pulseKey: 'steady' | 'stirring' | 'rising' = 'rising';
  export let pulseScore = 8.44;

  $: clampedPulse = Math.max(0, Math.min(10, Number.isFinite(pulseScore) ? pulseScore : 8.44));
  $: needleAngleDeg = -90 + (clampedPulse / 10) * 180;
</script>

<!-- STEP 4: HUMANITY'S PULSE BRIDGE (Just Above Research Behind the Story) -->
<section id="humanitys-pulse" class="pulse-section" aria-label={$dict.pulse.label}>
  <div class="pulse-container">
    <div class="pulse-section-head">
      <span class="pulse-kicker">{$dict.pulse.sectionKicker}</span>
    </div>

    <a href={`${base}/seismograph/`} class="pulse-visual-card">
      <div class="pv-gauge-wrap" aria-hidden="true">
        <svg viewBox="0 0 132 82" width="124" height="77" class="pv-dial-svg">
          <path
            d="M 16 68 A 50 50 0 0 1 42 25"
            fill="none"
            stroke="var(--threat-sovereign)"
            stroke-width="10"
            stroke-linecap="round"
            opacity="0.88"
          />
          <path
            d="M 47 22 A 50 50 0 0 1 92 27"
            fill="none"
            stroke="var(--threat-warning)"
            stroke-width="10"
            stroke-linecap="round"
            opacity="0.9"
          />
          <path
            d="M 97 30 A 50 50 0 0 1 116 68"
            fill="none"
            stroke="var(--threat-critical)"
            stroke-width="10"
            stroke-linecap="round"
            opacity="0.95"
          />

          <text x="10" y="79" class="pv-zone-lbl">0</text>
          <text x="66" y="12" text-anchor="middle" class="pv-zone-lbl">5</text>
          <text x="122" y="79" text-anchor="end" class="pv-zone-lbl">10</text>

          <g transform={`translate(66 68) rotate(${needleAngleDeg})`}>
            <polygon points="-3,0 0,-44 3,0" fill="var(--text-primary)" />
            <circle cx="0" cy="0" r="5.5" fill="var(--text-primary)" />
            <circle cx="0" cy="0" r="2" fill="var(--bg-surface-elevated)" />
          </g>
        </svg>
      </div>

      <div class="pv-info">
        <div class="pv-head-row">
          <span class="pv-title-line">
            <span class={`hm-dot state-${pulseKey}`} aria-hidden="true"></span>
            <span>{$dict.pulse.label}: <strong>{$dict.pulse.states[pulseKey].word}</strong></span>
          </span>
          <span class="pv-score-pill">{clampedPulse.toFixed(1)}/10</span>
        </div>

        <div class="pv-pace-bars" aria-hidden="true">
          <div class="pace-row">
            <span class="pace-lbl">{$dict.pulse.humanPaceLabel}</span>
            <span class="pace-track"><i class="pace-fill-human"></i></span>
          </div>
          <div class="pace-row">
            <span class="pace-lbl">{$dict.pulse.aiPaceLabel}</span>
            <span class="pace-track">
              <i class="pace-fill-ai" style={`width:${Math.round(clampedPulse * 10)}%`}></i>
            </span>
          </div>
        </div>

        <div class="pv-foot">
          <span class="pv-explain">{$dict.pulse.states[pulseKey].sentence}</span>
          <span class="mini-arrow">
            {$dict.pulse.cta} <span class="arrow-flip" aria-hidden="true">&rarr;</span>
          </span>
        </div>
      </div>
    </a>
  </div>
</section>

<style>
  .pulse-section {
    contain: layout style;
    scroll-margin-top: 90px;
    padding: clamp(0.85rem, 2vw, 1.35rem) 0 clamp(1.35rem, 3vw, 2.25rem);
    background: var(--bg-canvas);
  }

  .pulse-container {
    max-width: 960px;
    margin: 0 auto;
    padding: 0 1.15rem;
  }

  .pulse-section-head {
    text-align: center;
    margin-bottom: 0.55rem;
  }

  .pulse-kicker {
    display: inline-block;
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
  }

  .pulse-visual-card {
    display: flex;
    align-items: center;
    gap: 1.05rem;
    padding: 0.9rem 1.1rem;
    background: var(--bg-surface-elevated);
    border: 1.5px solid var(--border-medium);
    border-radius: 16px;
    text-decoration: none;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.16s ease, transform 0.16s ease;
  }

  .pulse-visual-card:hover {
    border-color: var(--accent-primary);
    transform: translateY(-1px);
  }

  .pv-gauge-wrap {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.45rem 0.55rem;
    border-radius: 12px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
  }

  .pv-dial-svg {
    display: block;
  }

  .pv-zone-lbl {
    font-family: var(--font-family-mono);
    font-size: 9px;
    font-weight: 700;
    fill: var(--text-secondary);
  }

  .pv-info {
    flex: 1 1 auto;
    min-width: 0;
  }

  .pv-head-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.35rem;
    margin-bottom: 0.42rem;
  }

  .pv-title-line {
    display: inline-flex;
    align-items: center;
    gap: 0.42rem;
    font-size: 0.96rem;
    color: var(--text-primary);
  }

  .pv-score-pill {
    font-family: var(--font-family-mono);
    font-size: 0.74rem;
    font-weight: 800;
    padding: 0.14rem 0.5rem;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
  }

  .hm-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .hm-dot.state-steady { background: var(--threat-sovereign); }
  .hm-dot.state-stirring,
  .hm-dot.state-rising { background: var(--threat-warning); }

  .pv-pace-bars {
    display: flex;
    flex-direction: column;
    gap: 0.28rem;
    margin-bottom: 0.45rem;
  }

  .pace-row {
    display: grid;
    grid-template-columns: 118px 1fr;
    align-items: center;
    gap: 0.5rem;
  }

  .pace-lbl {
    font-family: var(--font-family-mono);
    font-size: 0.68rem;
    color: var(--text-secondary);
    white-space: nowrap;
  }

  .pace-track {
    height: 7px;
    border-radius: 9999px;
    background: var(--bg-surface-sunken);
    overflow: hidden;
    display: block;
  }

  .pace-fill-human {
    display: block;
    width: 10%;
    height: 100%;
    border-radius: 9999px;
    background: var(--threat-sovereign);
  }

  .pace-fill-ai {
    display: block;
    height: 100%;
    border-radius: 9999px;
    background: linear-gradient(90deg, var(--threat-warning), var(--threat-critical));
  }

  .pv-foot {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: baseline;
    gap: 0.3rem 0.65rem;
  }

  .pv-explain {
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.42;
  }

  .mini-arrow {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--accent-primary);
    white-space: nowrap;
  }

  :global([dir='rtl']) .arrow-flip {
    display: inline-block;
    transform: scaleX(-1);
  }

  @media (max-width: 640px) {
    .pulse-visual-card {
      flex-direction: column;
      align-items: stretch;
      gap: 0.65rem;
      padding: 0.85rem 0.9rem;
    }

    .pv-gauge-wrap {
      padding: 0.4rem;
    }
  }
</style>
