# SVG Recipe — Isometric Tech-Architecture Showcase

## Visual mechanism
A clean light-grey stage holds dark, glossy isometric infrastructure objects built from shaded SVG path faces. Thick red orthogonal/isometric connector routes sit between the objects, making the architecture flow feel precise, premium, and executive-ready.

## SVG primitives needed
- 1× `<rect>` for the full-slide radial-gradient background.
- 6–10× faint `<path>` strokes for subtle isometric floor-grid perspective.
- 3–5× thick red `<path>` connector routes with soft glow.
- 4× blurred `<ellipse>` shadows beneath the isometric objects.
- 30–45× `<path>` faces for isometric servers, database, gateway, cloud block, and platform modules.
- 12–18× small `<rect>` details for rack dividers, LEDs, ports, and status bars.
- 8–12× `<circle>` or `<ellipse>` details for database bands, indicator lights, and highlights.
- 5–7× `<text>` labels with explicit `width` attributes.
- 1× `<radialGradient>` for the background stage.
- 4–6× `<linearGradient>` fills for top/front/side component faces.
- 2× `<filter>` effects: one soft drop shadow for objects and one red glow for connector routes.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bg" cx="50%" cy="44%" r="72%">
      <stop offset="0%" stop-color="#f7f7f7"/>
      <stop offset="62%" stop-color="#eeeeee"/>
      <stop offset="100%" stop-color="#dadada"/>
    </radialGradient>

    <linearGradient id="topFace" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6a6a6a"/>
      <stop offset="100%" stop-color="#303030"/>
    </linearGradient>
    <linearGradient id="frontFace" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#313131"/>
      <stop offset="100%" stop-color="#121212"/>
    </linearGradient>
    <linearGradient id="sideFace" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#454545"/>
      <stop offset="100%" stop-color="#0b0b0b"/>
    </linearGradient>
    <linearGradient id="redAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff3a32"/>
      <stop offset="100%" stop-color="#b80000"/>
    </linearGradient>

    <filter id="softShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="redGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <!-- subtle isometric stage grid -->
  <path d="M190 525 L430 390 L1090 390" fill="none" stroke="#cfcfcf" stroke-width="1" opacity="0.35"/>
  <path d="M120 570 L410 405 L1160 405" fill="none" stroke="#cfcfcf" stroke-width="1" opacity="0.28"/>
  <path d="M270 585 L520 440 L1090 440" fill="none" stroke="#cfcfcf" stroke-width="1" opacity="0.24"/>
  <path d="M330 610 L610 455 L990 455" fill="none" stroke="#cfcfcf" stroke-width="1" opacity="0.20"/>
  <path d="M365 300 L650 465 L905 310" fill="none" stroke="#d7d7d7" stroke-width="1" opacity="0.26"/>
  <path d="M230 385 L585 585 L1020 335" fill="none" stroke="#d7d7d7" stroke-width="1" opacity="0.22"/>

  <!-- architecture flow lines behind objects -->
  <path d="M315 430 L485 330 L640 420 L815 315" fill="none" stroke="url(#redAccent)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" filter="url(#redGlow)" opacity="0.95"/>
  <path d="M640 420 L810 520 L995 410" fill="none" stroke="url(#redAccent)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" filter="url(#redGlow)" opacity="0.95"/>
  <path d="M640 420 L640 292 L760 222" fill="none" stroke="url(#redAccent)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" filter="url(#redGlow)" opacity="0.88"/>

  <!-- left client stack -->
  <ellipse cx="305" cy="476" rx="118" ry="34" fill="#000000" opacity="0.16" filter="url(#softShadow)"/>
  <g filter="url(#softShadow)">
    <path d="M225 395 L320 340 L420 395 L325 452 Z" fill="url(#topFace)" stroke="#111" stroke-width="1"/>
    <path d="M225 395 L325 452 L325 505 L225 448 Z" fill="url(#frontFace)" stroke="#111" stroke-width="1"/>
    <path d="M325 452 L420 395 L420 448 L325 505 Z" fill="url(#sideFace)" stroke="#111" stroke-width="1"/>
    <path d="M248 405 L321 363 L396 405 L323 447 Z" fill="#1f1f1f" stroke="#777" stroke-width="1"/>
    <rect x="250" y="428" width="55" height="6" rx="3" fill="#777" opacity="0.55"/>
    <circle cx="313" cy="431" r="4" fill="#ff2d27"/>
  </g>
  <text x="202" y="545" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#222" text-anchor="middle">Enterprise Users</text>

  <!-- central platform / API core -->
  <ellipse cx="635" cy="508" rx="150" ry="44" fill="#000000" opacity="0.18" filter="url(#softShadow)"/>
  <g filter="url(#softShadow)">
    <path d="M500 390 L635 312 L775 392 L640 470 Z" fill="url(#topFace)" stroke="#101010" stroke-width="1"/>
    <path d="M500 390 L640 470 L640 560 L500 480 Z" fill="url(#frontFace)" stroke="#101010" stroke-width="1"/>
    <path d="M640 470 L775 392 L775 482 L640 560 Z" fill="url(#sideFace)" stroke="#101010" stroke-width="1"/>
    <path d="M535 402 L636 344 L739 403 L638 461 Z" fill="#171717" stroke="#6b6b6b" stroke-width="1"/>
    <path d="M552 414 L636 366 L721 415 L638 463 Z" fill="none" stroke="#cc0000" stroke-width="4" opacity="0.9"/>
    <rect x="525" y="438" width="88" height="8" rx="4" fill="#777" opacity="0.45"/>
    <rect x="525" y="462" width="88" height="8" rx="4" fill="#777" opacity="0.35"/>
    <rect x="525" y="486" width="88" height="8" rx="4" fill="#777" opacity="0.25"/>
    <circle cx="624" cy="442" r="5" fill="#ff332d"/>
    <circle cx="624" cy="466" r="5" fill="#ff332d" opacity="0.75"/>
    <circle cx="624" cy="490" r="5" fill="#ff332d" opacity="0.55"/>
  </g>
  <text x="505" y="606" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#111" text-anchor="middle">API Orchestration Core</text>
  <text x="520" y="632" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#666" text-anchor="middle">routing · policy · observability</text>

  <!-- top cloud service block -->
  <ellipse cx="760" cy="266" rx="112" ry="31" fill="#000000" opacity="0.13" filter="url(#softShadow)"/>
  <g filter="url(#softShadow)">
    <path d="M680 205 L765 156 L855 207 L770 256 Z" fill="url(#topFace)" stroke="#101010" stroke-width="1"/>
    <path d="M680 205 L770 256 L770 315 L680 264 Z" fill="url(#frontFace)" stroke="#101010" stroke-width="1"/>
    <path d="M770 256 L855 207 L855 266 L770 315 Z" fill="url(#sideFace)" stroke="#101010" stroke-width="1"/>
    <circle cx="737" cy="218" r="20" fill="#242424" stroke="#777" stroke-width="1"/>
    <circle cx="768" cy="200" r="28" fill="#242424" stroke="#777" stroke-width="1"/>
    <circle cx="800" cy="220" r="22" fill="#242424" stroke="#777" stroke-width="1"/>
    <rect x="703" y="238" width="118" height="18" rx="9" fill="#242424"/>
    <path d="M715 264 L748 283 L820 241" fill="none" stroke="#ff302a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="672" y="134" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#222" text-anchor="middle">Cloud Services</text>

  <!-- right data warehouse -->
  <ellipse cx="988" cy="456" rx="120" ry="35" fill="#000000" opacity="0.17" filter="url(#softShadow)"/>
  <g filter="url(#softShadow)">
    <path d="M900 374 C900 348 1070 348 1070 374 L1070 486 C1070 512 900 512 900 486 Z" fill="url(#frontFace)" stroke="#111" stroke-width="1"/>
    <ellipse cx="985" cy="374" rx="85" ry="26" fill="url(#topFace)" stroke="#111" stroke-width="1"/>
    <path d="M900 412 C900 438 1070 438 1070 412" fill="none" stroke="#5e5e5e" stroke-width="2" opacity="0.7"/>
    <path d="M900 450 C900 476 1070 476 1070 450" fill="none" stroke="#5e5e5e" stroke-width="2" opacity="0.55"/>
    <path d="M930 376 C950 388 1022 388 1040 376" fill="none" stroke="#ff302a" stroke-width="5" stroke-linecap="round"/>
    <circle cx="1038" cy="475" r="5" fill="#ff302a"/>
    <circle cx="1020" cy="482" r="4" fill="#ff302a" opacity="0.7"/>
  </g>
  <text x="884" y="545" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#222" text-anchor="middle">Operational Data Store</text>

  <!-- bottom security gateway -->
  <ellipse cx="815" cy="574" rx="100" ry="28" fill="#000000" opacity="0.15" filter="url(#softShadow)"/>
  <g filter="url(#softShadow)">
    <path d="M750 505 L820 465 L895 508 L825 548 Z" fill="url(#topFace)" stroke="#111" stroke-width="1"/>
    <path d="M750 505 L825 548 L825 604 L750 562 Z" fill="url(#frontFace)" stroke="#111" stroke-width="1"/>
    <path d="M825 548 L895 508 L895 564 L825 604 Z" fill="url(#sideFace)" stroke="#111" stroke-width="1"/>
    <path d="M807 498 L850 522 L850 557 C850 580 829 590 822 593 C815 590 794 580 794 557 L794 522 Z" fill="#202020" stroke="#777" stroke-width="1.5"/>
    <path d="M806 545 L818 558 L842 528" fill="none" stroke="#ff302a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="710" y="650" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#222" text-anchor="middle">Security Gateway</text>

  <!-- title block -->
  <text x="74" y="80" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#111">Reference Architecture</text>
  <text x="76" y="112" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666">isometric infrastructure map with highlighted data-flow paths</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` to clone repeated isometric modules; duplicate the paths directly so PowerPoint receives editable shapes.
- ❌ Do not rely on `skewX`, `skewY`, or matrix transforms to fake perspective; build the isometric faces as explicit path coordinates.
- ❌ Do not put arrowheads on connector `<path>` elements with `marker-end`; if arrows are required, draw small triangular `<path>` arrowheads manually.
- ❌ Do not apply filters to `<line>` elements; use stroked `<path>` connectors if glow is needed.
- ❌ Do not overfill the canvas with tiny technical labels; this style works because the architecture is simplified and premium.

## Composition notes
- Keep the main platform near the lower-middle of the slide, with secondary systems placed on isometric diagonals around it.
- Put red connector routes behind the 3D components so the objects feel physically connected rather than merely overdrawn.
- Use a mostly monochrome component palette and reserve the saturated accent color for data flow, status lights, and one or two key outlines.
- Leave generous light-grey negative space around the architecture so the dark objects and red routes read clearly from the back of a room.