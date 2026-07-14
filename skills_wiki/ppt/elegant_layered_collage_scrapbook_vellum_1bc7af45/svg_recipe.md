# SVG Recipe — Elegant Layered Collage (Scrapbook / Vellum Card Style)

## Visual mechanism
Build a tactile, premium “paper craft” slide by stacking centered mats, ribbons, clipped imagery, and die-cut decorations with soft shadows. A semi-transparent vellum tag sits on top, muting the busy collage beneath while preserving depth and handmade elegance.

## SVG primitives needed
- 8× `<rect>` for the full-slide color base, metallic mat, ivory card, ribbon strips, borders, and photo shadow backing
- 2× `<image>` for subtle paper texture and a clipped botanical/photo scrap layer
- 1× `<clipPath>` with rounded `<rect>` applied to the photo scrap image
- 10× `<path>` for ribbon tails, vellum tag silhouette, pine sprigs, gold flourishes, and decorative corner accents
- 8× `<circle>` for berry embellishments and punched vellum fasteners
- 3× `<text>` with explicit `width` for central invitation-style typography
- 5× `<linearGradient>` / `<radialGradient>` for metallic gold, ivory paper, crimson ribbon, vellum sheen, and background vignette
- 2× `<filter>` using `feOffset`, `feGaussianBlur`, and `feMerge` for paper-layer shadows and a softer vellum lift

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="forestVignette" cx="50%" cy="45%" r="75%">
      <stop offset="0%" stop-color="#245F4B"/>
      <stop offset="70%" stop-color="#1B4D3E"/>
      <stop offset="100%" stop-color="#0F3028"/>
    </radialGradient>

    <linearGradient id="antiqueGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F1D58B"/>
      <stop offset="38%" stop-color="#C5A059"/>
      <stop offset="72%" stop-color="#8F6C2D"/>
      <stop offset="100%" stop-color="#E8C879"/>
    </linearGradient>

    <linearGradient id="ivoryPaper" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFDF2"/>
      <stop offset="58%" stop-color="#FDF8E7"/>
      <stop offset="100%" stop-color="#EFE1BE"/>
    </linearGradient>

    <linearGradient id="crimsonRibbon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6C0000"/>
      <stop offset="50%" stop-color="#A01E1E"/>
      <stop offset="100%" stop-color="#5B0000"/>
    </linearGradient>

    <linearGradient id="vellumSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.74"/>
      <stop offset="100%" stop-color="#F8F1DB" stop-opacity="0.82"/>
    </linearGradient>

    <filter id="paperShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .33 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="vellumShadow" x="-18%" y="-18%" width="136%" height="145%">
      <feOffset dx="0" dy="6" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .24 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoRound">
      <rect x="300" y="116" width="270" height="168" rx="16"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#forestVignette)"/>
  <image href="https://images.example.com/deep-green-handmade-paper-texture.jpg"
         x="0" y="0" width="1280" height="720" opacity="0.28" preserveAspectRatio="xMidYMid slice"/>

  <path d="M75 80 C210 25 320 78 410 36 C500 -4 565 24 612 62" fill="none" stroke="#D8B968" stroke-width="2" opacity="0.32"/>
  <path d="M1186 642 C1026 690 952 610 850 666 C765 712 664 690 600 650" fill="none" stroke="#D8B968" stroke-width="2" opacity="0.28"/>

  <rect x="205" y="52" width="870" height="616" rx="8" fill="url(#antiqueGold)" filter="url(#paperShadow)"/>
  <rect x="238" y="84" width="804" height="552" rx="6" fill="url(#ivoryPaper)" filter="url(#paperShadow)"/>
  <rect x="265" y="111" width="750" height="498" rx="4" fill="none" stroke="#C5A059" stroke-width="2" opacity="0.72"/>

  <rect x="594" y="84" width="92" height="552" fill="url(#crimsonRibbon)" opacity="0.96"/>
  <rect x="630" y="84" width="18" height="552" fill="#F2D27D" opacity="0.44"/>
  <path d="M210 313 L1070 313 L1024 361 L1070 409 L210 409 L256 361 Z"
        fill="url(#crimsonRibbon)" filter="url(#paperShadow)"/>
  <rect x="255" y="348" width="770" height="24" fill="url(#antiqueGold)" opacity="0.86"/>

  <rect x="310" y="126" width="270" height="168" rx="16" fill="#000000" opacity="0.18" filter="url(#paperShadow)" transform="rotate(-4 445 210)"/>
  <image href="https://images.example.com/elegant-evergreen-and-gold-botanical-paper-scrap.jpg"
         x="300" y="116" width="270" height="168" opacity="0.92" clip-path="url(#photoRound)"
         preserveAspectRatio="xMidYMid slice" transform="rotate(-4 435 200)"/>

  <path d="M392 226
           C418 226 418 198 448 198
           L832 198
           C862 198 862 226 888 226
           L888 494
           C862 494 862 522 832 522
           L448 522
           C418 522 418 494 392 494
           Z"
        fill="url(#vellumSheen)" stroke="#D3AE62" stroke-width="2.2" opacity="0.91" filter="url(#vellumShadow)"/>

  <circle cx="448" cy="236" r="8" fill="url(#antiqueGold)" opacity="0.78"/>
  <circle cx="832" cy="236" r="8" fill="url(#antiqueGold)" opacity="0.78"/>
  <circle cx="448" cy="484" r="8" fill="url(#antiqueGold)" opacity="0.78"/>
  <circle cx="832" cy="484" r="8" fill="url(#antiqueGold)" opacity="0.78"/>

  <path d="M426 302 C374 286 342 252 327 213" fill="none" stroke="#1B4D3E" stroke-width="4" stroke-linecap="round" opacity="0.78"/>
  <path d="M392 289 L361 265 M377 276 L349 276 M360 257 L334 243 M410 296 L382 316" fill="none" stroke="#1B4D3E" stroke-width="3" stroke-linecap="round" opacity="0.7"/>
  <circle cx="345" cy="253" r="6" fill="#A01E1E"/>
  <circle cx="363" cy="282" r="5" fill="#A01E1E"/>
  <circle cx="390" cy="306" r="5" fill="#A01E1E"/>

  <path d="M854 418 C910 430 945 463 962 507" fill="none" stroke="#1B4D3E" stroke-width="4" stroke-linecap="round" opacity="0.78"/>
  <path d="M884 424 L914 400 M900 438 L932 438 M919 458 L949 474 M866 419 L893 394" fill="none" stroke="#1B4D3E" stroke-width="3" stroke-linecap="round" opacity="0.7"/>
  <circle cx="934" cy="450" r="6" fill="#A01E1E"/>
  <circle cx="914" cy="404" r="5" fill="#A01E1E"/>
  <circle cx="956" cy="486" r="5" fill="#A01E1E"/>

  <path d="M280 126 C310 146 332 145 356 126" fill="none" stroke="#C5A059" stroke-width="3" opacity="0.72"/>
  <path d="M1000 594 C970 574 948 575 924 594" fill="none" stroke="#C5A059" stroke-width="3" opacity="0.72"/>

  <text x="640" y="306" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" letter-spacing="5"
        fill="#1B4D3E" opacity="0.92">WISHING YOU</text>

  <text x="640" y="380" width="610" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="66" font-weight="300"
        fill="#9B7532" filter="url(#vellumShadow)">Peace &amp; Joy</text>

  <text x="640" y="432" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" letter-spacing="3"
        fill="#1B4D3E">
    <tspan x="640" dy="0">THIS HOLIDAY SEASON</tspan>
    <tspan x="640" dy="34" font-size="17" letter-spacing="2" fill="#6B5A32">A handcrafted moment of gratitude and warmth</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to create frosted glass; use a semi-transparent vellum fill instead.
- ❌ Do not apply `clip-path` to paper rectangles or decorative paths; clipping is reliable here only on `<image>`.
- ❌ Do not use `<pattern>` for paper grain; use a low-opacity texture `<image>` or scattered editable shapes.
- ❌ Do not rely on actual backdrop blur behind the vellum card; PowerPoint will not reproduce that effect natively.
- ❌ Do not use `<use>` for repeated flourishes or berries; duplicate the editable paths/circles directly.

## Composition notes
- Keep the collage centered and concentric: large gold mat, smaller ivory card, then vellum tag occupying roughly the middle 40–45% of slide height.
- Let ribbons and photo scraps extend behind the vellum so the translucent panel has visible material to soften.
- Use deep green, antique gold, ivory, and crimson in a restrained rhythm: green background, gold edges, ivory paper, crimson crossing accents.
- Preserve generous margins around the central tag; the outer paper layers are part of the visual luxury, not empty space.