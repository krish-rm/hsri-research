<script lang="ts">
  import { dict } from '../i18n/store';

  export let wishId: string;
  export let door: string;
  export let beat: 'wonder' | 'wobble' | 'weight' | 'way';
  export let transcript = '';

  let playing = true;
  let replayTick = 0;
  let showTranscript = false;

  function togglePlay() {
    playing = !playing;
  }

  function replay() {
    playing = true;
    replayTick += 1;
  }
</script>

<div class="scene-card" class:paused={!playing}>
  {#key `${wishId}-${beat}-${replayTick}`}
    <svg
      class="scene-svg"
      viewBox="0 0 420 150"
      width="420"
      height="150"
      role="img"
      aria-label={transcript}
    >
      <defs>
        <linearGradient id="ws-sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color={beat === 'wobble' ? '#fdf3df' : '#fdf7ec'} />
          <stop offset="100%" stop-color={beat === 'way' ? '#dff4ee' : '#f4e6cf'} />
        </linearGradient>
        <radialGradient id="ws-kalpa" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#fff8dc" stop-opacity="0.95" />
          <stop offset="55%" stop-color="#7ce0c6" stop-opacity="0.55" />
          <stop offset="100%" stop-color="#1b6756" stop-opacity="0" />
        </radialGradient>
      </defs>

      <rect width="420" height="150" rx="10" fill="url(#ws-sky)" />
      <rect x="0" y="118" width="420" height="32" fill="#1b6756" opacity="0.14" />

      <!-- Soft Kalpa diamond core -->
      <circle cx="72" cy="54" r="36" fill="url(#ws-kalpa)" class="anim-pulse" />
      <g transform="translate(72 54)" class="anim-float">
        <polygon points="0,-13 9,0 0,13 -9,0" fill="#ffffff" stroke="#1b6756" stroke-width="1.6" />
        <circle cx="0" cy="0" r="3" fill="#1b6756" />
      </g>

      <!-- Beat-specific narrative vector art -->
      {#if beat === 'wonder'}
        {#if wishId === 'sanjeevani'}
          <rect x="148" y="42" width="136" height="66" rx="8" fill="#ffffff" stroke="#b4e3d7" stroke-width="2" />
          <path d="M168 88h96M180 78h24M224 78h28" stroke="#1b6756" stroke-width="2.5" stroke-linecap="round" />
          <circle cx="328" cy="58" r="18" fill="#fef3c7" stroke="#d97706" stroke-width="1.8" class="anim-float" />
          <path d="M322 58l4 4 9-9" fill="none" stroke="#1b6756" stroke-width="2.2" stroke-linecap="round" />
        {:else if wishId === 'jarvis-for-my-life'}
          <circle cx="235" cy="70" r="34" fill="none" stroke="#1b6756" stroke-width="2.2" stroke-dasharray="5 5" class="anim-spin" />
          <rect x="218" y="54" width="34" height="32" rx="6" fill="#ffffff" stroke="#1b6756" stroke-width="2" />
          <path d="M226 68l6 6 11-12" fill="none" stroke="#1b6756" stroke-width="2.2" stroke-linecap="round" />
          <circle cx="320" cy="52" r="10" fill="#d9f4ec" stroke="#1b6756" />
          <circle cx="342" cy="84" r="10" fill="#fef3c7" stroke="#d97706" />
        {:else if wishId === 'prove-riemann-hypothesis'}
          <rect x="135" y="30" width="225" height="80" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2" />
          <path d="M152 84 Q195 36 245 70 T340 48" fill="none" stroke="#5eead4" stroke-width="2.5" class="anim-draw" />
          <circle cx="245" cy="70" r="4" fill="#fbbf24" />
          <text x="155" y="52" font-family="monospace" font-size="11" fill="#fde68a">zeta(s) = 0</text>
        {:else if door === 'movie'}
          <rect x="148" y="28" width="190" height="84" rx="8" fill="#fffdf7" stroke="#d97706" stroke-width="2" />
          <circle cx="205" cy="60" r="14" fill="#fef3c7" stroke="#d97706" />
          <rect x="242" y="48" width="66" height="44" rx="4" fill="#1b6756" opacity="0.22" />
        {:else}
          <path d="M120 92 Q195 54 270 86 T385 68" fill="none" stroke="#1b6756" stroke-width="6" opacity="0.5" />
          <path d="M120 100 Q195 62 270 94 T385 76" fill="none" stroke="#32997f" stroke-width="3" />
          <circle cx="265" cy="64" r="14" fill="#fef3c7" class="anim-float" />
        {/if}
      {:else if beat === 'wobble'}
        <g transform="translate(230 72) rotate(-6)" class="anim-tilt">
          <rect x="-74" y="-34" width="148" height="68" rx="8" fill="#ffffff" stroke="#d97706" stroke-width="2" />
          <line x1="-54" y1="-14" x2="54" y2="-14" stroke="#d97706" stroke-width="2.5" />
          <line x1="-54" y1="2" x2="36" y2="2" stroke="#94a3b8" stroke-width="2.5" />
          <line x1="-54" y1="16" x2="48" y2="16" stroke="#94a3b8" stroke-width="2.5" />
        </g>
        <circle cx="348" cy="46" r="14" fill="#fef3c7" stroke="#b45309" stroke-width="2" />
        <text x="348" y="51" text-anchor="middle" font-weight="bold" font-size="14" fill="#b45309">?</text>
      {:else if beat === 'weight'}
        <line x1="250" y1="32" x2="250" y2="108" stroke="#1e1915" stroke-width="2.5" />
        <g class="anim-tilt">
          <line x1="172" y1="54" x2="328" y2="54" stroke="#1b6756" stroke-width="2.5" stroke-linecap="round" />
          <circle cx="172" cy="76" r="14" fill="#e8f5f1" stroke="#1b6756" stroke-width="2" />
          <circle cx="328" cy="76" r="14" fill="#fdf7ec" stroke="#b45309" stroke-width="2" />
        </g>
        <rect x="218" y="106" width="64" height="8" rx="4" fill="#1e1915" opacity="0.7" />
      {:else}
        <rect x="160" y="34" width="160" height="76" rx="10" fill="#ffffff" stroke="#1b6756" stroke-width="2" />
        <path d="M182 58h96M182 74h76M182 90h64" stroke="#1b6756" stroke-width="2.5" stroke-linecap="round" />
        <circle cx="302" cy="76" r="16" fill="#e8f5f1" stroke="#1b6756" stroke-width="2" class="anim-pulse" />
        <path d="M295 76l5 5 10-10" fill="none" stroke="#1b6756" stroke-width="2.5" stroke-linecap="round" />
      {/if}
    </svg>
  {/key}

  <div class="scene-controls">
    <div class="ctrl-left">
      <button type="button" class="sc-btn" on:click={togglePlay}>
        {playing ? $dict.player.animPause : $dict.player.animPlay}
      </button>
      <button type="button" class="sc-btn" on:click={replay}>
        {$dict.player.animReplay}
      </button>
    </div>
    <button
      type="button"
      class="sc-btn"
      aria-expanded={showTranscript}
      on:click={() => (showTranscript = !showTranscript)}
    >
      {$dict.player.transcriptBtn}
    </button>
  </div>

  {#if showTranscript && transcript}
    <p class="scene-transcript">{transcript}</p>
  {/if}
</div>

<style>
  .scene-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.65rem;
    margin-bottom: 0.9rem;
  }

  .scene-svg {
    display: block;
    width: 100%;
    height: auto;
    max-height: 165px;
  }

  .anim-pulse {
    animation: hrPulse 3.6s ease-in-out infinite;
    transform-origin: center;
  }

  .anim-float {
    animation: hrFloat 3.2s ease-in-out infinite;
  }

  .anim-tilt {
    animation: hrTilt 4s ease-in-out infinite;
    transform-origin: center;
  }

  .anim-spin {
    animation: hrSpin 16s linear infinite;
    transform-origin: 235px 70px;
  }

  .scene-card.paused .anim-pulse,
  .scene-card.paused .anim-float,
  .scene-card.paused .anim-tilt,
  .scene-card.paused .anim-spin {
    animation-play-state: paused;
  }

  @keyframes hrPulse {
    0%, 100% { opacity: 0.72; }
    50% { opacity: 1; }
  }

  @keyframes hrFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-3px); }
  }

  @keyframes hrTilt {
    0%, 100% { transform: rotate(-2deg); }
    50% { transform: rotate(2deg); }
  }

  @keyframes hrSpin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .scene-controls {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.45rem;
    margin-top: 0.5rem;
  }

  .ctrl-left {
    display: flex;
    gap: 0.4rem;
  }

  .sc-btn {
    border: 1px solid var(--border-medium);
    background: var(--bg-surface-elevated);
    color: var(--text-secondary);
    border-radius: 9999px;
    padding: 0.2rem 0.65rem;
    font-size: 0.72rem;
    font-weight: 600;
    cursor: pointer;
    min-height: 28px;
  }

  .sc-btn:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .scene-transcript {
    margin: 0.5rem 0 0;
    padding: 0.5rem 0.7rem;
    border-radius: 8px;
    background: var(--bg-surface-sunken);
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.45;
  }

  @media (prefers-reduced-motion: reduce) {
    .anim-pulse,
    .anim-float,
    .anim-tilt,
    .anim-spin {
      animation: none !important;
    }
  }
</style>
