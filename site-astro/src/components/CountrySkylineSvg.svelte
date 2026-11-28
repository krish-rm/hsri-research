<script lang="ts">
  import type { SkyArchetype } from '../lib/countrySkies';

  export let archetype: SkyArchetype = 'central_europe';
</script>

<!-- Watercolor-and-ink horizon landmarks layered over dawn-sky-base.webp (waterline at y=318).
     Upper y=0..165 stays open so Toto flies cleanly across every country sky without visual collision. -->
<svg
  class="country-skyline-svg"
  viewBox="0 0 760 428"
  preserveAspectRatio="xMidYMid slice"
  aria-hidden="true"
>
  <defs>
    <linearGradient id="wl-hill-far" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#a8c3bc" stop-opacity="0.72" />
      <stop offset="100%" stop-color="#c9dad3" stop-opacity="0.88" />
    </linearGradient>
    <linearGradient id="wl-stone-warm" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e5cfad" />
      <stop offset="100%" stop-color="#c9af8a" />
    </linearGradient>
    <linearGradient id="wl-stone-terracotta" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e0a988" />
      <stop offset="100%" stop-color="#be8264" />
    </linearGradient>
    <linearGradient id="wl-slate-city" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#87a29b" />
      <stop offset="100%" stop-color="#607b74" />
    </linearGradient>
    <linearGradient id="wl-foliage" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#82a57a" />
      <stop offset="100%" stop-color="#5a7b58" />
    </linearGradient>
    <linearGradient id="wl-aurora" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#6ee7b7" stop-opacity="0" />
      <stop offset="35%" stop-color="#5eead4" stop-opacity="0.22" />
      <stop offset="70%" stop-color="#a7f3d0" stop-opacity="0.16" />
      <stop offset="100%" stop-color="#fde68a" stop-opacity="0" />
    </linearGradient>
    <linearGradient id="wl-desert-haze" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fde68a" stop-opacity="0" />
      <stop offset="100%" stop-color="#f6c78c" stop-opacity="0.26" />
    </linearGradient>
    <linearGradient id="wl-water-refl" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#84a39a" stop-opacity="0.26" />
      <stop offset="100%" stop-color="#84a39a" stop-opacity="0" />
    </linearGradient>
  </defs>

  {#if archetype === 'nordic'}
    <!-- Soft pastel morning aurora veil & deep fjord sea -->
    <path d="M20 75 Q 240 24 440 82 T 740 52 L 740 155 Q 500 115 260 140 T 20 118 Z" fill="url(#wl-aurora)" />
    <path d="M0 318 L0 218 L92 178 L168 238 L225 196 L310 248 L398 188 L475 236 L585 182 L670 232 L760 202 L760 318 Z" fill="url(#wl-hill-far)" />
    <path d="M90 318 L90 264 L106 248 L122 264 L122 276 L138 256 L154 276 L154 318 Z" fill="url(#wl-stone-terracotta)" stroke="#62574c" stroke-width="1.2" />
    <path d="M180 318 L180 282 L198 262 L216 282 L216 318 M232 318 L232 278 L248 258 L264 278 L264 318" fill="url(#wl-stone-warm)" stroke="#62574c" stroke-width="1.2" />
    <!-- Slender copper Nordic church spire -->
    <path d="M472 318 L472 254 L478 254 L486 196 L494 254 L500 254 L500 318 Z" fill="url(#wl-slate-city)" stroke="#555e59" stroke-width="1.2" />
    <path d="M518 318 L518 286 L552 286 L552 318 M565 318 L565 276 L588 260 L610 276 L610 318 Z" fill="url(#wl-stone-warm)" stroke="#62574c" stroke-width="1.2" />
    <!-- Pine headland & sailboat -->
    <path d="M0 318 L0 284 Q 35 270 74 292 Q 46 310 92 318 Z" fill="url(#wl-foliage)" />
    <path d="M350 314 L366 314 L359 292 Z M346 316 L372 316 L367 321 L350 321 Z" fill="#fffaf0" stroke="#62574c" stroke-width="1" />
    <path d="M472 320 L500 320 L488 378 L480 378 Z M180 320 L264 320 L260 354 L184 354 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'japan'}
    <!-- Distant Mt Fuji & morning sakura mist -->
    <path d="M360 318 L485 246 L546 198 L586 198 L652 248 L760 286 L760 318 Z" fill="url(#wl-hill-far)" />
    <path d="M533 210 L546 198 L586 198 L600 212 Q 576 205 564 214 Q 548 205 533 210 Z" fill="#fffdf8" opacity="0.92" />
    <!-- Low misty ridge -->
    <path d="M0 318 L0 278 Q 140 252 310 282 T 760 278 L760 318 Z" fill="#9fb9b1" opacity="0.55" />
    <!-- Five-tiered Pagoda left-mid -->
    <g stroke="#5c5247" stroke-width="1.2" stroke-linejoin="round">
      <line x1="158" y1="186" x2="158" y2="206" />
      <path d="M138 214 Q 158 202 178 214 Z" fill="url(#wl-stone-terracotta)" />
      <rect x="145" y="214" width="26" height="12" fill="url(#wl-stone-warm)" />
      <path d="M133 230 Q 158 218 183 230 Z" fill="url(#wl-stone-terracotta)" />
      <rect x="142" y="230" width="32" height="14" fill="url(#wl-stone-warm)" />
      <path d="M128 248 Q 158 235 188 248 Z" fill="url(#wl-stone-terracotta)" />
      <rect x="139" y="248" width="38" height="15" fill="url(#wl-stone-warm)" />
      <path d="M122 268 Q 158 253 194 268 Z" fill="url(#wl-stone-terracotta)" />
      <rect x="135" y="268" width="46" height="50" fill="url(#wl-stone-warm)" />
      <!-- Tokyo Tower coral-terracotta lattice -->
      <path d="M272 318 L286 248 L294 176 L302 248 L316 318 L302 318 L294 282 L286 318 Z" fill="url(#wl-stone-terracotta)" />
      <rect x="283" y="244" width="22" height="7" fill="#fffaf0" />
      <rect x="287" y="212" width="14" height="6" fill="#fffaf0" />
      <!-- Modern skyline cluster center -->
      <rect x="336" y="254" width="24" height="64" fill="url(#wl-slate-city)" />
      <rect x="366" y="240" width="28" height="78" fill="url(#wl-slate-city)" />
      <rect x="400" y="264" width="22" height="54" fill="url(#wl-stone-warm)" />
    </g>
    <!-- Soft cherry-blossom & river shoreline -->
    <path d="M0 318 Q 52 282 104 302 Q 112 312 128 318 Z" fill="url(#wl-foliage)" />
    <circle cx="48" cy="272" r="18" fill="#f7c5cc" opacity="0.72" />
    <circle cx="72" cy="282" r="14" fill="#f9d8dc" opacity="0.76" />
    <path d="M276 320 L312 320 L306 382 L282 382 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'egypt'}
    <rect x="0" y="160" width="760" height="160" fill="url(#wl-desert-haze)" />
    <!-- Giza Pyramids & sandstone Citadel ridge -->
    <g stroke="#6b5a45" stroke-width="1.2" stroke-linejoin="round">
      <polygon points="96,318 202,216 296,318" fill="#ecd5ad" />
      <polygon points="202,216 296,318 232,318" fill="#d3b484" opacity="0.65" />
      <polygon points="246,318 334,232 414,318" fill="#ebd1a5" />
      <polygon points="334,232 414,318 362,318" fill="#cca978" opacity="0.65" />
      <polygon points="384,318 438,266 490,318" fill="#e5c799" />
      <!-- Historic Cairo Citadel dome & slender minarets -->
      <path d="M518 318 L518 264 L548 264 C550 236 588 236 590 264 L624 264 L624 318 Z" fill="url(#wl-stone-warm)" />
      <path d="M524 264 L527 202 L532 264 Z M610 264 L614 206 L618 264 Z" fill="url(#wl-stone-warm)" />
    </g>
    <!-- Date palm & curving Nile feluccas -->
    <path d="M46 318 Q 52 284 60 264" fill="none" stroke="#62574c" stroke-width="2" />
    <path d="M60 264 Q 36 254 24 266 M60 264 Q 44 244 62 238 M60 264 Q 82 250 90 266 M60 264 Q 78 272 86 284" fill="none" stroke="#5f7f56" stroke-width="2.2" stroke-linecap="round" />
    <path d="M210 342 L222 292 L246 342 Z M202 346 L252 346 L242 353 L210 353 Z" fill="#fffdf6" stroke="#62574c" stroke-width="1.1" />
    <path d="M468 336 L478 298 L498 336 Z M462 340 L504 340 L496 346 L468 346 Z" fill="#fffdf6" stroke="#62574c" stroke-width="1.1" />
    <polygon points="106,320 286,320 202,386" fill="url(#wl-water-refl)" />

  {:else if archetype === 'uk'}
    <path d="M0 318 L0 284 Q 180 268 360 284 T 760 278 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5b544c" stroke-width="1.2" stroke-linejoin="round">
      <!-- Palace of Westminster & Elizabeth Tower (Big Ben) -->
      <rect x="86" y="274" width="110" height="44" fill="url(#wl-stone-warm)" />
      <rect x="196" y="216" width="22" height="102" fill="url(#wl-stone-warm)" />
      <polygon points="196,216 207,184 218,216" fill="url(#wl-slate-city)" />
      <circle cx="207" cy="232" r="6" fill="#fff9eb" />
      <!-- St Paul's dome -->
      <rect x="278" y="274" width="66" height="44" fill="url(#wl-stone-warm)" />
      <path d="M292 274 C292 232 330 232 330 274 Z" fill="url(#wl-slate-city)" />
      <line x1="311" y1="230" x2="311" y2="242" />
      <!-- London Eye subtle rim -->
      <circle cx="408" cy="264" r="36" fill="none" stroke="#859e97" stroke-width="1.8" />
      <!-- Tower Bridge twin towers & bascule -->
      <rect x="492" y="226" width="22" height="92" fill="url(#wl-stone-warm)" />
      <polygon points="492,226 503,204 514,226" fill="url(#wl-slate-city)" />
      <rect x="582" y="226" width="22" height="92" fill="url(#wl-stone-warm)" />
      <polygon points="582,226 593,204 604,226" fill="url(#wl-slate-city)" />
      <rect x="514" y="246" width="68" height="8" fill="url(#wl-slate-city)" />
      <rect x="462" y="294" width="168" height="7" fill="url(#wl-slate-city)" />
    </g>
    <path d="M196 320 L218 320 L216 382 L198 382 Z M492 320 L604 320 L598 368 L498 368 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'france'}
    <path d="M0 318 L0 282 Q 200 264 400 284 T 760 280 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5e554a" stroke-width="1.2" stroke-linejoin="round">
      <!-- Eiffel Tower scaled cleanly below upper sky flight path -->
      <path d="M196 318 Q 214 272 222 182 L228 182 Q 236 272 254 318 L240 318 Q 225 288 210 318 Z" fill="url(#wl-stone-terracotta)" />
      <rect x="206" y="272" width="38" height="6" fill="#70665c" />
      <rect x="214" y="242" width="22" height="5" fill="#70665c" />
      <!-- Haussmann roofs & Seine stone arch bridge -->
      <rect x="282" y="278" width="128" height="40" fill="url(#wl-stone-warm)" />
      <polygon points="282,278 292,268 400,268 410,278" fill="url(#wl-slate-city)" />
      <!-- Notre-Dame twin towers & spire -->
      <rect x="478" y="240" width="20" height="78" fill="url(#wl-stone-warm)" />
      <rect x="512" y="240" width="20" height="78" fill="url(#wl-stone-warm)" />
      <rect x="498" y="256" width="14" height="62" fill="url(#wl-stone-warm)" />
      <line x1="505" y1="226" x2="505" y2="256" />
      <!-- River stone arches -->
      <path d="M320 318 Q 355 298 390 318 M400 318 Q 435 298 470 318 M550 318 Q 585 298 620 318" fill="none" stroke-width="2" />
    </g>
    <path d="M0 318 Q 62 276 124 318 Z M610 318 Q 675 276 760 296 L760 318 Z" fill="url(#wl-foliage)" />
    <path d="M202 320 L248 320 L240 384 L210 384 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'usa'}
    <g stroke="#5b544b" stroke-width="1.2" stroke-linejoin="round">
      <!-- Statue of Liberty silhouette left harbour island -->
      <rect x="116" y="286" width="32" height="32" fill="url(#wl-stone-warm)" />
      <path d="M124 286 L127 238 L120 218 L125 218 L130 236 L138 236 L140 286 Z" fill="#82aba1" />
      <circle cx="132" cy="232" r="5" fill="#82aba1" />
      <line x1="122" y1="214" x2="122" y2="206" stroke="#d97706" stroke-width="2" />
      <!-- Manhattan Art Deco & spire cluster -->
      <rect x="234" y="258" width="26" height="60" fill="url(#wl-slate-city)" />
      <rect x="266" y="230" width="30" height="88" fill="url(#wl-stone-warm)" />
      <rect x="304" y="242" width="24" height="76" fill="url(#wl-slate-city)" />
      <rect x="334" y="206" width="26" height="112" fill="url(#wl-stone-warm)" />
      <line x1="347" y1="176" x2="347" y2="206" />
      <rect x="368" y="236" width="28" height="82" fill="url(#wl-slate-city)" />
      <rect x="402" y="258" width="24" height="60" fill="url(#wl-stone-warm)" />
      <!-- Suspension bridge towers & cables -->
      <rect x="478" y="240" width="16" height="78" fill="url(#wl-stone-warm)" />
      <rect x="614" y="240" width="16" height="78" fill="url(#wl-stone-warm)" />
      <path d="M435 304 Q 460 284 486 240 Q 554 294 622 240 Q 652 280 692 304" fill="none" stroke="#62574c" stroke-width="1.6" />
      <line x1="428" y1="304" x2="700" y2="304" stroke-width="2" />
    </g>
    <path d="M266 320 L396 320 L386 382 L276 382 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'canada'}
    <path d="M0 318 L0 288 Q 140 264 280 288 T 760 278 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5b544b" stroke-width="1.2" stroke-linejoin="round">
      <rect x="242" y="264" width="28" height="54" fill="url(#wl-slate-city)" />
      <rect x="278" y="246" width="32" height="72" fill="url(#wl-stone-warm)" />
      <!-- CN Tower slender needle & sky pod -->
      <path d="M342 318 L350 226 L354 172 L358 226 L366 318 Z" fill="url(#wl-stone-warm)" />
      <ellipse cx="354" cy="222" rx="14" ry="5" fill="#fffaf0" />
      <path d="M380 318 C382 282 436 282 438 318 Z" fill="url(#wl-slate-city)" />
      <rect x="448" y="258" width="28" height="60" fill="url(#wl-stone-warm)" />
    </g>
    <!-- Crimson-autumn maple & pine shoreline -->
    <path d="M0 318 Q 52 276 112 318 Z" fill="url(#wl-foliage)" />
    <circle cx="118" cy="298" r="16" fill="#d97757" opacity="0.82" />
    <circle cx="96" cy="304" r="14" fill="#e69d66" opacity="0.82" />
    <path d="M560 314 L574 286 L584 314 Z M554 316 L590 316 L583 322 L560 322 Z" fill="#fffaf0" />
    <path d="M344 320 L364 320 L360 388 L348 388 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'korea'}
    <path d="M0 318 Q 180 264 380 228 Q 560 258 760 282 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5b544b" stroke-width="1.2" stroke-linejoin="round">
      <!-- Gyeongbokgung curved palace eaves left -->
      <path d="M98 282 Q 152 262 206 282 L198 288 L106 288 Z" fill="url(#wl-slate-city)" />
      <path d="M116 266 Q 152 252 188 266 L182 272 L122 272 Z" fill="url(#wl-slate-city)" />
      <rect x="114" y="288" width="76" height="30" fill="url(#wl-stone-terracotta)" />
      <!-- N Seoul Tower atop wooded hill -->
      <rect x="378" y="200" width="8" height="58" fill="url(#wl-stone-warm)" />
      <rect x="372" y="196" width="20" height="8" fill="#fffaf0" />
      <line x1="382" y1="176" x2="382" y2="196" />
      <!-- Han River modern skyline & bridge -->
      <rect x="468" y="252" width="26" height="66" fill="url(#wl-slate-city)" />
      <rect x="502" y="240" width="24" height="78" fill="url(#wl-stone-warm)" />
      <rect x="534" y="264" width="28" height="54" fill="url(#wl-slate-city)" />
      <path d="M220 310 Q 320 292 420 310 L420 318 L220 318 Z" fill="url(#wl-stone-warm)" />
    </g>

  {:else if archetype === 'china'}
    <!-- Misty karst/mountain ridge & wall towers -->
    <path d="M0 318 Q 85 246 185 268 Q 290 218 415 260 Q 525 224 640 258 L760 282 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5b544b" stroke-width="1.2" stroke-linejoin="round">
      <!-- Triple circular Temple of Heaven roof -->
      <path d="M158 286 L236 286 L236 318 L158 318 Z" fill="url(#wl-stone-warm)" />
      <path d="M148 286 Q 197 268 246 286 Z" fill="url(#wl-slate-city)" />
      <path d="M162 268 Q 197 252 232 268 Z" fill="url(#wl-slate-city)" />
      <path d="M174 252 Q 197 236 220 252 Z" fill="url(#wl-slate-city)" />
      <circle cx="197" cy="233" r="3.5" fill="#d97706" />
      <!-- Distant Pearl/skyline & watchtower ridge -->
      <rect x="336" y="242" width="12" height="18" fill="url(#wl-stone-warm)" />
      <rect x="464" y="254" width="24" height="64" fill="url(#wl-slate-city)" />
      <rect x="494" y="236" width="26" height="82" fill="url(#wl-stone-warm)" />
      <path d="M556 318 L560 202 L564 318 Z" fill="url(#wl-stone-terracotta)" />
      <circle cx="560" cy="236" r="8" fill="#e0a988" />
    </g>
    <path d="M464 320 L570 320 L562 378 L472 378 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'australia'}
    <path d="M0 318 L0 288 Q 220 272 440 288 T 760 284 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5b544b" stroke-width="1.2" stroke-linejoin="round">
      <!-- Harbour Bridge steel arch left-mid -->
      <rect x="116" y="256" width="14" height="62" fill="url(#wl-stone-warm)" />
      <rect x="314" y="256" width="14" height="62" fill="url(#wl-stone-warm)" />
      <path d="M130 296 Q 222 214 314 296" fill="none" stroke="#607b74" stroke-width="4" />
      <path d="M130 278 Q 222 198 314 278" fill="none" stroke="#607b74" stroke-width="2" />
      <line x1="90" y1="298" x2="352" y2="298" stroke-width="2.2" />
      <!-- Sydney Opera House billowing white shells right-center -->
      <path d="M398 310 Q 418 242 468 292 Z" fill="#fffaf0" />
      <path d="M438 310 Q 464 226 512 290 Z" fill="#fef6e4" />
      <path d="M482 310 Q 508 248 548 298 Z" fill="#fffaf0" />
      <path d="M524 310 Q 546 270 572 308 Z" fill="#fef6e4" />
      <rect x="386" y="308" width="194" height="10" fill="url(#wl-stone-warm)" />
    </g>
    <path d="M388 320 L574 320 L560 364 L402 364 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'mediterranean'}
    <!-- Terracotta hills, classical colonnade temple, basilica dome & cypresses -->
    <path d="M0 318 L0 264 Q 150 220 290 258 Q 450 240 620 268 L760 284 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5e5449" stroke-width="1.2" stroke-linejoin="round">
      <!-- Hilltop classical temple colonnade -->
      <rect x="132" y="220" width="76" height="8" fill="url(#wl-stone-warm)" />
      <polygon points="128,220 170,202 212,220" fill="url(#wl-stone-warm)" />
      <line x1="140" y1="228" x2="140" y2="250" stroke-width="2.5" />
      <line x1="155" y1="228" x2="155" y2="250" stroke-width="2.5" />
      <line x1="170" y1="228" x2="170" y2="250" stroke-width="2.5" />
      <line x1="185" y1="228" x2="185" y2="250" stroke-width="2.5" />
      <line x1="200" y1="228" x2="200" y2="250" stroke-width="2.5" />
      <!-- Warm coastal terracotta town & basilica dome -->
      <rect x="292" y="276" width="96" height="42" fill="url(#wl-stone-warm)" />
      <polygon points="288,276 340,264 392,276" fill="url(#wl-stone-terracotta)" />
      <rect x="436" y="270" width="72" height="48" fill="url(#wl-stone-warm)" />
      <path d="M446 270 C448 228 496 228 498 270 Z" fill="url(#wl-stone-terracotta)" />
      <line x1="472" y1="226" x2="472" y2="236" />
    </g>
    <!-- Slender Mediterranean cypress silhouettes -->
    <path d="M72 318 C68 274 78 242 82 242 C86 242 96 274 92 318 Z M548 318 C544 268 552 248 556 248 C560 248 568 268 564 318 Z" fill="url(#wl-foliage)" />
    <path d="M292 320 L512 320 L496 364 L306 364 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'anatolia_maghreb'}
    <rect x="0" y="170" width="760" height="150" fill="url(#wl-desert-haze)" />
    <path d="M0 318 L0 282 Q 190 248 410 282 T 760 272 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5e5346" stroke-width="1.2" stroke-linejoin="round">
      <!-- Cascading domes, courtyard arch gate & slender minarets -->
      <rect x="190" y="276" width="112" height="42" fill="url(#wl-stone-warm)" />
      <path d="M214 276 C216 246 274 246 276 276 Z" fill="url(#wl-slate-city)" />
      <path d="M234 318 L234 294 Q 246 282 258 294 L258 318 Z" fill="#6b5c4d" opacity="0.65" />
      <rect x="338" y="256" width="136" height="62" fill="url(#wl-stone-warm)" />
      <path d="M364 256 C366 210 446 210 448 256 Z" fill="url(#wl-slate-city)" />
      <path d="M342 256 L345 194 L350 256 Z M462 256 L466 196 L471 256 Z" fill="url(#wl-stone-warm)" />
      <!-- Terraced kasbah wall right -->
      <rect x="520" y="276" width="66" height="42" fill="url(#wl-stone-terracotta)" />
    </g>
    <!-- Date palm cluster left -->
    <path d="M76 318 Q 82 284 88 264" fill="none" stroke="#62574c" stroke-width="2.2" />
    <path d="M88 264 Q 62 256 54 270 M88 264 Q 76 242 96 238 M88 264 Q 114 252 120 268" fill="none" stroke="url(#wl-foliage)" stroke-width="2.5" stroke-linecap="round" />
    <path d="M338 320 L474 320 L462 372 L348 372 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'andean_latin'}
    <!-- Twin Andean/volcanic peaks & sunlit colonial belltower/terraces -->
    <path d="M0 318 L86 246 L168 186 L246 248 L368 272 L494 198 L610 278 L760 248 L760 318 Z" fill="url(#wl-hill-far)" />
    <path d="M148 202 L168 186 L186 202 Q 168 196 148 202 Z M476 214 L494 198 L514 214 Q 496 208 476 214 Z" fill="#fffdf7" opacity="0.88" />
    <g stroke="#5d5247" stroke-width="1.2" stroke-linejoin="round">
      <!-- Stepped highland terraces -->
      <path d="M90 318 L112 292 L242 292 L254 318 Z" fill="url(#wl-stone-warm)" />
      <line x1="102" y1="304" x2="246" y2="304" />
      <!-- Plaza bell tower & terracotta roofs -->
      <rect x="336" y="274" width="114" height="44" fill="url(#wl-stone-warm)" />
      <polygon points="332,274 393,262 454,274" fill="url(#wl-stone-terracotta)" />
      <rect x="444" y="242" width="24" height="76" fill="url(#wl-stone-warm)" />
      <path d="M446 242 C448 226 464 226 466 242 Z" fill="url(#wl-stone-terracotta)" />
    </g>
    <path d="M558 318 Q 596 286 648 318 Z" fill="url(#wl-foliage)" />
    <path d="M336 320 L468 320 L458 366 L346 366 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'southeast_pagoda'}
    <path d="M0 318 L0 282 Q 180 264 380 284 T 760 278 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5c5247" stroke-width="1.2" stroke-linejoin="round">
      <!-- Ornate tiered stupa / prang spires -->
      <path d="M168 318 L178 272 L188 228 L194 188 L200 228 L210 272 L220 318 Z" fill="#ebd093" />
      <path d="M236 318 L244 282 L252 246 L260 282 L268 318 Z" fill="#ebd093" />
      <!-- Sleek modern harbour towers right -->
      <rect x="424" y="242" width="24" height="76" fill="url(#wl-slate-city)" />
      <rect x="456" y="232" width="26" height="86" fill="url(#wl-stone-warm)" />
      <rect x="488" y="252" width="24" height="66" fill="url(#wl-slate-city)" />
      <path d="M418 242 Q 468 232 518 242 L512 248 L424 248 Z" fill="#e5cfad" />
    </g>
    <path d="M52 318 Q 58 286 64 266 M64 266 Q 42 256 34 268 M64 266 Q 82 254 90 268" fill="none" stroke="url(#wl-foliage)" stroke-width="2.4" stroke-linecap="round" />
    <path d="M338 334 L388 334 L378 342 L346 342 Z" fill="url(#wl-stone-warm)" stroke="#5c5247" stroke-width="1" />
    <path d="M168 320 L220 320 L212 372 L176 372 Z M424 320 L512 320 L504 378 L432 378 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'central_europe'}
    <path d="M0 318 L0 284 Q 180 266 390 282 T 760 280 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5c5247" stroke-width="1.2" stroke-linejoin="round">
      <!-- Gothic spire, onion dome & stepped canal gables -->
      <rect x="136" y="276" width="28" height="42" fill="url(#wl-stone-warm)" />
      <polygon points="136,276 150,256 164,276" fill="url(#wl-stone-terracotta)" />
      <rect x="170" y="268" width="32" height="50" fill="url(#wl-stone-warm)" />
      <polygon points="170,268 186,248 202,268" fill="url(#wl-slate-city)" />
      <!-- Tall cathedral spire center-left -->
      <rect x="262" y="256" width="24" height="62" fill="url(#wl-stone-warm)" />
      <polygon points="262,256 274,186 286,256" fill="url(#wl-slate-city)" />
      <!-- Arched stone bridge center & dome -->
      <path d="M320 318 L320 298 L516 298 L516 318 M346 318 Q 368 298 390 318 M418 318 Q 440 298 462 318" fill="url(#wl-stone-warm)" />
      <rect x="536" y="272" width="68" height="46" fill="url(#wl-stone-warm)" />
      <path d="M548 272 C550 236 590 236 592 272 Z" fill="url(#wl-slate-city)" />
    </g>
    <path d="M0 318 Q 48 278 106 318 Z" fill="url(#wl-foliage)" />
    <path d="M262 320 L286 320 L282 376 L266 376 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'africa_savannah'}
    <rect x="0" y="170" width="760" height="150" fill="url(#wl-desert-haze)" />
    <!-- Iconic flat-topped escarpment / Table plateau -->
    <path d="M0 318 L76 266 L186 218 L356 218 L428 268 L610 278 L760 258 L760 318 Z" fill="url(#wl-hill-far)" />
    <g stroke="#5e5346" stroke-width="1.2" stroke-linejoin="round">
      <!-- Civic domes & modern harbour/city skyline -->
      <rect x="444" y="268" width="26" height="50" fill="url(#wl-slate-city)" />
      <rect x="476" y="250" width="28" height="68" fill="url(#wl-stone-warm)" />
      <rect x="510" y="272" width="24" height="46" fill="url(#wl-slate-city)" />
      <path d="M328 318 L328 286 L372 286 L372 318 M336 286 C338 264 362 264 364 286 Z" fill="url(#wl-stone-warm)" />
    </g>
    <!-- Flat-crown acacia trees -->
    <path d="M128 318 L130 276 L114 256 M130 276 L146 258" fill="none" stroke="#5d5044" stroke-width="2" />
    <ellipse cx="130" cy="252" rx="44" ry="11" fill="url(#wl-foliage)" />
    <ellipse cx="222" cy="272" rx="30" ry="8" fill="url(#wl-foliage)" />
    <line x1="222" y1="276" x2="222" y2="318" stroke="#5d5044" stroke-width="1.8" />
    <path d="M444 320 L534 320 L524 370 L452 370 Z" fill="url(#wl-water-refl)" />

  {:else if archetype === 'himalaya_central'}
    <!-- Jagged Himalayan / Pamir snow crest & turquoise-domed archways -->
    <path d="M0 318 L72 246 L146 190 L218 242 L310 180 L402 244 L486 196 L592 252 L680 218 L760 264 L760 318 Z" fill="url(#wl-hill-far)" />
    <path d="M132 204 L146 190 L162 204 Z M294 196 L310 180 L328 196 Z M472 212 L486 196 L502 212 Z" fill="#fffdf8" opacity="0.92" />
    <g stroke="#5c5247" stroke-width="1.2" stroke-linejoin="round">
      <!-- Arched iwan gate & melon domes / pagoda shrine -->
      <rect x="234" y="274" width="96" height="44" fill="url(#wl-stone-warm)" />
      <path d="M264 318 L264 290 Q 282 276 300 290 L300 318 Z" fill="#5e766e" opacity="0.72" />
      <path d="M366 318 L366 266 L414 266 L414 318 M374 266 C370 236 410 236 406 266 Z" fill="#73ada2" />
      <rect x="424" y="280" width="58" height="38" fill="url(#wl-stone-warm)" />
    </g>
    <path d="M366 320 L482 320 L468 370 L376 370 Z" fill="url(#wl-water-refl)" />

  {:else}
    <!-- pacific_island: Emerald volcanic twin peaks, palms & sailing cove -->
    <path d="M0 318 L64 274 Q 146 218 230 278 Q 312 292 380 282 Q 490 228 594 278 L760 288 L760 318 Z" fill="url(#wl-hill-far)" />
    <path d="M0 318 Q 76 286 168 318 Z M580 318 Q 664 282 760 298 L760 318 Z" fill="url(#wl-foliage)" />
    <path d="M74 318 Q 84 282 96 260 M96 260 Q 70 250 58 264 M96 260 Q 86 240 106 236 M96 260 Q 124 252 128 268" fill="none" stroke="url(#wl-foliage)" stroke-width="2.5" stroke-linecap="round" />
    <path d="M344 312 L362 278 L374 312 Z M336 314 L382 314 L374 321 L342 321 Z" fill="#fffdf7" stroke="#5c5247" stroke-width="1.1" />
    <path d="M446 320 L462 294 L472 320 Z" fill="#fffdf7" opacity="0.88" />
  {/if}
</svg>

<style>
  .country-skyline-svg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    animation: horizonDrift 16s ease-in-out infinite;
    animation-delay: var(--seek-delay, 0s);
  }

  :global(.toto-cinema-card.paused) .country-skyline-svg {
    animation-play-state: paused !important;
  }

  @keyframes horizonDrift {
    0%, 100% { transform: scale(1) translate3d(0, 0, 0); }
    50% { transform: scale(1.05) translate3d(-1.2%, -0.6%, 0); }
  }

  @media (prefers-reduced-motion: reduce) {
    .country-skyline-svg {
      animation: none !important;
    }
  }
</style>
