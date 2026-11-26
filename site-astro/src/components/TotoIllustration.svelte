<script lang="ts">
  export let pose: 'calm' | 'curious' | 'apologetic' = 'calm';
  export let size = 96;
  export let label = 'Toto, a fictional superintelligence depicted as a soft glowing dawn orb inside a thin ring';
</script>

<svg
  class={`toto-svg pose-${pose}`}
  viewBox="0 0 120 120"
  width={size}
  height={size}
  role="img"
  aria-label={label}
>
  <defs>
    <radialGradient id="toto-halo-grad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fff9e6" stop-opacity="0.98" />
      <stop offset="52%" stop-color={pose === 'apologetic' ? '#fcd34d' : '#7ce0c6'} stop-opacity="0.48" />
      <stop offset="100%" stop-color="#1b6756" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="toto-core-grad" cx="42%" cy="38%" r="60%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="65%" stop-color={pose === 'apologetic' ? '#fde68a' : '#a7f3d0'} />
      <stop offset="100%" stop-color={pose === 'apologetic' ? '#d97706' : '#1b6756'} />
    </radialGradient>
  </defs>

  <!-- Warm atmospheric glow (static radial gradient, zero filter/blur) -->
  <circle cx="60" cy="60" r="54" fill="url(#toto-halo-grad)" class="toto-halo" />

  <!-- Thin orbital ring (rotates gently or rests static cleanly) -->
  <g class="toto-ring-group">
    <ellipse
      cx="60"
      cy="60"
      rx="40"
      ry={pose === 'curious' ? 24 : 36}
      transform={pose === 'curious' ? 'rotate(-16 60 60)' : pose === 'apologetic' ? 'rotate(12 60 60)' : undefined}
      fill="none"
      stroke={pose === 'apologetic' ? '#b45309' : '#1b6756'}
      stroke-width="2"
      stroke-dasharray="6 4"
      opacity="0.72"
    />
    <circle
      cx={pose === 'apologetic' ? 88 : 96}
      cy={pose === 'curious' ? 50 : 60}
      r="4"
      fill={pose === 'apologetic' ? '#d97706' : '#1b6756'}
    />
  </g>

  <!-- Central orb + calm pose indicator dots -->
  <g class="toto-orb-group">
    <circle
      cx="60"
      cy={pose === 'apologetic' ? 63 : 60}
      r="22"
      fill="url(#toto-core-grad)"
      stroke={pose === 'apologetic' ? '#b45309' : '#1b6756'}
      stroke-width="2"
    />
    {#if pose === 'calm'}
      <circle cx="54" cy="58" r="2.2" fill="#1e1915" opacity="0.75" />
      <circle cx="66" cy="58" r="2.2" fill="#1e1915" opacity="0.75" />
      <path d="M55 66 Q60 69 65 66" fill="none" stroke="#1e1915" stroke-width="1.8" stroke-linecap="round" opacity="0.75" />
    {:else if pose === 'curious'}
      <circle cx="54" cy="57" r="2.4" fill="#1e1915" opacity="0.8" />
      <circle cx="66" cy="55" r="2.7" fill="#1e1915" opacity="0.8" />
      <circle cx="60" cy="66" r="2.2" fill="none" stroke="#1e1915" stroke-width="1.7" opacity="0.75" />
    {:else}
      <path d="M51 61 Q54 58 57 61" fill="none" stroke="#1e1915" stroke-width="1.8" stroke-linecap="round" opacity="0.8" />
      <path d="M63 61 Q66 58 69 61" fill="none" stroke="#1e1915" stroke-width="1.8" stroke-linecap="round" opacity="0.8" />
      <path d="M56 70 Q60 68 64 70" fill="none" stroke="#1e1915" stroke-width="1.7" stroke-linecap="round" opacity="0.75" />
    {/if}
  </g>
</svg>

<style>
  .toto-svg {
    display: block;
    flex-shrink: 0;
    height: auto;
  }

  .toto-halo {
    animation: totoHalo 4.5s ease-in-out infinite;
    transform-origin: center;
  }

  .toto-orb-group {
    animation: totoBob 3.8s ease-in-out infinite;
  }

  @keyframes totoHalo {
    0%, 100% { opacity: 0.78; }
    50% { opacity: 1; }
  }

  @keyframes totoBob {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-2.5px); }
  }

  @media (prefers-reduced-motion: reduce) {
    .toto-halo,
    .toto-orb-group {
      animation: none !important;
    }
  }
</style>
