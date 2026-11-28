<script lang="ts">
  export let variant = 'epic';
  export let compact = false;

  $: key = (variant || 'epic').toLowerCase();
</script>

<svg
  class="concept-visual-svg"
  class:compact
  viewBox="0 0 260 156"
  width={compact ? 84 : 260}
  height={compact ? 50 : 156}
  aria-hidden="true"
>
  <defs>
    <linearGradient id="cv-sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e3f1eb" />
      <stop offset="68%" stop-color="#f9edd5" />
      <stop offset="100%" stop-color="#efe3ca" />
    </linearGradient>
    <linearGradient id="cv-water" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2c8470" stop-opacity="0.72" />
      <stop offset="100%" stop-color="#1b6756" stop-opacity="0.9" />
    </linearGradient>
    <radialGradient id="cv-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fffbeb" stop-opacity="0.95" />
      <stop offset="60%" stop-color="#fde68a" stop-opacity="0.45" />
      <stop offset="100%" stop-color="#fde68a" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Soft Dawn Archival Frame Backdrop -->
  <rect x="0" y="0" width="260" height="156" rx="12" fill="url(#cv-sky)" />

  {#if key === 'south-asia-healing-commons'}
    <!-- Radiant Sanjeevani leaf orb + 3 decentralized village clinic nodes -->
    <circle cx="130" cy="54" r="36" fill="url(#cv-glow)" />
    <path d="M130 22 C152 34 158 58 130 78 C102 58 108 34 130 22 Z" fill="#2e9378" stroke="#1b6756" stroke-width="2" />
    <path d="M130 30 L130 76 M130 48 L142 40 M130 56 L118 48" stroke="#e8f5f1" stroke-width="1.8" stroke-linecap="round" />
    <path d="M62 114 L130 88 L198 114 M62 114 L198 114" stroke="#1b6756" stroke-width="2" stroke-dasharray="4 4" fill="none" />
    <g stroke="#1b6756" stroke-width="1.8">
      <rect x="42" y="102" width="40" height="30" rx="6" fill="#fdfbf7" />
      <path d="M62 110v14M55 117h14" stroke="#b45309" stroke-width="2.5" stroke-linecap="round" />
      <rect x="110" y="96" width="40" height="36" rx="6" fill="#fdfbf7" />
      <path d="M130 106v16M122 114h16" stroke="#1b6756" stroke-width="2.8" stroke-linecap="round" />
      <rect x="178" y="102" width="40" height="30" rx="6" fill="#fdfbf7" />
      <path d="M198 110v14M191 117h14" stroke="#b45309" stroke-width="2.5" stroke-linecap="round" />
    </g>

  {:else if key === 'polynesian-wayfinding'}
    <!-- Star Compass (Kaveinga) + double-hulled canoe + ocean swells -->
    <circle cx="130" cy="64" r="40" fill="none" stroke="#1b6756" stroke-width="1.6" stroke-dasharray="3 4" />
    <circle cx="130" cy="64" r="24" fill="url(#cv-glow)" stroke="#b45309" stroke-width="1.2" />
    <path d="M130 18v12M130 98v12M84 64h12M164 64h12" stroke="#1b6756" stroke-width="2" stroke-linecap="round" />
    <circle cx="102" cy="36" r="2.6" fill="#d97706" />
    <circle cx="160" cy="34" r="2.8" fill="#d97706" />
    <circle cx="174" cy="76" r="2.4" fill="#d97706" />
    <!-- Outrigger sail & canoe -->
    <path d="M104 114 L158 114 L148 126 L112 126 Z" fill="#a47148" stroke="#5c4028" stroke-width="1.5" />
    <path d="M126 114 L126 56 L154 106 Z" fill="#fffdf7" stroke="#1b6756" stroke-width="1.6" stroke-linejoin="round" />
    <path d="M14 134 Q 56 122 98 134 T 182 134 T 248 134" fill="none" stroke="#1b6756" stroke-width="2.2" stroke-linecap="round" />

  {:else if key === 'netherlands-delta-works'}
    <!-- Storm surge lock gates + green "room for the river" overflow basin -->
    <path d="M0 108 L260 108 L260 156 L0 156 Z" fill="url(#cv-water)" />
    <path d="M14 118 Q 52 94 94 118 L94 138 L14 138 Z" fill="#639a78" stroke="#1b6756" stroke-width="1.5" />
    <rect x="86" y="54" width="14" height="72" rx="3" fill="#fdfbf7" stroke="#1b6756" stroke-width="1.8" />
    <rect x="160" y="54" width="14" height="72" rx="3" fill="#fdfbf7" stroke="#1b6756" stroke-width="1.8" />
    <path d="M100 84 Q 130 98 160 84" fill="none" stroke="#b45309" stroke-width="4" stroke-linecap="round" />
    <path d="M180 96 Q 214 78 248 96" fill="none" stroke="#1b6756" stroke-width="2.6" stroke-linecap="round" />
    <circle cx="130" cy="40" r="14" fill="url(#cv-glow)" />

  {:else if key === 'china-river-stewardship'}
    <!-- Dujiangyan curved fish-mouth diversion weir splitting river gracefully -->
    <path d="M18 136 Q 82 108 130 88 Q 178 68 244 76" fill="none" stroke="url(#cv-water)" stroke-width="18" stroke-linecap="round" />
    <path d="M130 88 Q 186 106 244 128" fill="none" stroke="#32997f" stroke-width="12" stroke-linecap="round" />
    <path d="M116 84 Q 136 74 146 92 Q 128 98 116 84 Z" fill="#e5cfad" stroke="#5c4d3b" stroke-width="1.8" />
    <!-- Misty karst peaks above -->
    <path d="M30 86 Q 58 34 86 86 Q 112 42 142 80" fill="none" stroke="#5f7f75" stroke-width="2" />
    <rect x="176" y="42" width="44" height="14" rx="4" fill="#fdfbf7" stroke="#1b6756" stroke-width="1.4" />
    <path d="M184 49h28" stroke="#1b6756" stroke-width="2" stroke-dasharray="3 3" />

  {:else if key === 'arab-house-of-wisdom'}
    <!-- Astrolabe precision ring + House of Wisdom arch + linked witness chain -->
    <circle cx="130" cy="64" r="36" fill="url(#cv-glow)" stroke="#b45309" stroke-width="2" />
    <circle cx="130" cy="64" r="24" fill="none" stroke="#1b6756" stroke-width="1.6" stroke-dasharray="5 3" />
    <line x1="102" y1="92" x2="158" y2="36" stroke="#b45309" stroke-width="2" stroke-linecap="round" />
    <path d="M84 140 L84 96 Q 130 62 176 96 L176 140" fill="none" stroke="#1b6756" stroke-width="2.2" />
    <circle cx="72" cy="116" r="7" fill="#fdfbf7" stroke="#1b6756" stroke-width="1.8" />
    <circle cx="130" cy="116" r="7" fill="#e8f5f1" stroke="#1b6756" stroke-width="1.8" />
    <circle cx="188" cy="116" r="7" fill="#fdfbf7" stroke="#1b6756" stroke-width="1.8" />
    <path d="M79 116 H123 M137 116 H181" stroke="#1b6756" stroke-width="2" />

  {:else if key === 'west-africa-timbuktu-keepers'}
    <!-- Sahelian mud-brick archive portal + family folio + custody key -->
    <path d="M62 132 L62 66 L80 42 L98 66 L162 66 L180 42 L198 66 L198 132 Z" fill="#e5c89e" stroke="#6b5235" stroke-width="1.8" stroke-linejoin="round" />
    <path d="M114 132 L114 96 Q 130 82 146 96 L146 132 Z" fill="#fdfbf7" stroke="#1b6756" stroke-width="1.8" />
    <rect x="80" y="78" width="22" height="28" rx="3" fill="#fdfbf7" stroke="#1b6756" stroke-width="1.5" />
    <path d="M85 86h12M85 92h10M85 98h12" stroke="#b45309" stroke-width="1.6" />
    <circle cx="174" cy="96" r="7" fill="none" stroke="#1b6756" stroke-width="2.2" />
    <path d="M174 103v16m0-5h5" stroke="#1b6756" stroke-width="2.2" stroke-linecap="round" />

  {:else if key === 'andean-water-terraces'}
    <!-- Stepped green mountain andenes terraces + stone amuna canal -->
    <polygon points="24,142 108,34 196,142" fill="#8bb08d" stroke="#1b6756" stroke-width="1.6" stroke-linejoin="round" />
    <polygon points="108,34 128,58 92,58" fill="#fffdf8" />
    <path d="M68 84 H148 M54 102 H164 M40 120 H180" stroke="#fdfbf7" stroke-width="2.2" />
    <path d="M138 66 Q 190 92 232 130" fill="none" stroke="#2c8470" stroke-width="4" stroke-linecap="round" />
    <circle cx="212" cy="48" r="16" fill="url(#cv-glow)" />

  {:else if key === 'japan-craft-repair'}
    <!-- Openable Monozukuri vessel + precision gear + kintsugi repair join -->
    <circle cx="106" cy="80" r="34" fill="#fdfbf7" stroke="#1b6756" stroke-width="2" />
    <circle cx="106" cy="80" r="14" fill="none" stroke="#b45309" stroke-width="2.2" stroke-dasharray="4 3" />
    <path d="M84 56 Q 106 80 126 104" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" fill="none" />
    <path d="M160 54 L196 90 M188 46 Q 204 46 204 62 Q 188 64 188 46 Z" stroke="#1b6756" stroke-width="2.5" fill="#e8f5f1" stroke-linecap="round" />
    <circle cx="160" cy="96" r="12" fill="url(#cv-glow)" stroke="#1b6756" stroke-width="1.8" />

  {:else if key === 'nordic-right-to-roam'}
    <!-- Open wooden commons trail gate under aurora arc -->
    <path d="M16 42 Q 130 10 244 46" fill="none" stroke="#32997f" stroke-width="7" stroke-linecap="round" opacity="0.45" />
    <polygon points="44,116 66,68 88,116" fill="#2c8470" />
    <polygon points="172,116 194,68 216,116" fill="#2c8470" />
    <path d="M92 78 V124 M168 78 V124 M92 86 L122 96 M168 86 L138 96" stroke="#6b5235" stroke-width="2.8" stroke-linecap="round" />
    <path d="M114 140 Q 130 112 146 140" fill="#fde68a" opacity="0.85" />

  {:else if key === 'anatolia-mediterranean-crossroads'}
    <!-- Arched stone civic square beside harbor + backup plaza lantern -->
    <path d="M0 120 H260 V156 H0 Z" fill="url(#cv-water)" />
    <path d="M40 120 L40 80 L220 80 L220 120" fill="#fdfbf7" stroke="#5c4d3b" stroke-width="1.8" />
    <path d="M64 120 A 20 20 0 0 1 104 120 M110 120 A 20 20 0 0 1 150 120 M156 120 A 20 20 0 0 1 196 120" fill="#e3f1eb" stroke="#1b6756" stroke-width="1.8" />
    <circle cx="130" cy="48" r="16" fill="url(#cv-glow)" stroke="#b45309" stroke-width="1.5" />

  {:else if key === 'mysteries'}
    <!-- Open Problems: constellation telescope + open book + proof prism -->
    <circle cx="130" cy="64" r="38" fill="url(#cv-glow)" />
    <path d="M74 114 Q 102 98 130 110 Q 158 98 186 114 L186 132 Q 158 118 130 130 Q 102 118 74 132 Z" fill="#fdfbf7" stroke="#1b6756" stroke-width="1.8" />
    <circle cx="94" cy="44" r="3" fill="#1b6756" />
    <circle cx="130" cy="32" r="4" fill="#d97706" />
    <circle cx="166" cy="48" r="3" fill="#1b6756" />
    <path d="M94 44 L130 32 L166 48" stroke="#1b6756" stroke-width="1.5" stroke-dasharray="3 3" fill="none" />

  {:else if key === 'gadgets'}
    <!-- Everyday Technologies: pocket sphere + modular open cubes -->
    <circle cx="130" cy="70" r="36" fill="url(#cv-glow)" stroke="#1b6756" stroke-width="1.8" />
    <rect x="108" y="54" width="20" height="20" rx="4" fill="#fdfbf7" stroke="#1b6756" stroke-width="1.8" />
    <rect x="134" y="64" width="20" height="20" rx="4" fill="#e8f5f1" stroke="#b45309" stroke-width="1.8" />
    <path d="M88 122 H172" stroke="#1b6756" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 4" />

  {:else if key === 'movie'}
    <!-- Culture & Creativity: open cinema frame + human storytellers -->
    <rect x="64" y="34" width="132" height="80" rx="8" fill="#fdfbf7" stroke="#1b6756" stroke-width="2" />
    <polygon points="120,56 150,74 120,92" fill="#2c8470" opacity="0.85" />
    <circle cx="72" cy="128" r="8" fill="#e8f5f1" stroke="#1b6756" stroke-width="1.8" />
    <circle cx="130" cy="128" r="8" fill="#fde68a" stroke="#b45309" stroke-width="1.8" />
    <circle cx="188" cy="128" r="8" fill="#e8f5f1" stroke="#1b6756" stroke-width="1.8" />

  {:else}
    <!-- Global Epic / Public Good: glowing world horizon & shared human bridge -->
    <circle cx="130" cy="68" r="42" fill="url(#cv-glow)" />
    <circle cx="130" cy="68" r="28" fill="#fdfbf7" stroke="#1b6756" stroke-width="2" />
    <ellipse cx="130" cy="68" rx="13" ry="28" fill="none" stroke="#2c8470" stroke-width="1.4" />
    <line x1="102" y1="68" x2="158" y2="68" stroke="#2c8470" stroke-width="1.4" />
    <path d="M54 126 Q 130 98 206 126" fill="none" stroke="#b45309" stroke-width="2.4" stroke-linecap="round" />
    <circle cx="54" cy="126" r="5" fill="#1b6756" />
    <circle cx="206" cy="126" r="5" fill="#1b6756" />
  {/if}
</svg>

<style>
  .concept-visual-svg {
    display: block;
    width: 100%;
    max-width: 260px;
    height: auto;
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
  }

  .concept-visual-svg.compact {
    width: 78px;
    height: auto;
    border-radius: 8px;
    flex-shrink: 0;
  }
</style>
