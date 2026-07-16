# SVG Recipe — Atmospheric Pathway Diagram

## Visual mechanism
A dark, full-bleed atmospheric photo becomes a cinematic stage for a high-contrast white pathway of dashed connectors and circular “portal” nodes. The viewer reads the slide as a journey: title at the top, then 3–5 glowing waypoints flowing across the canvas in an undulating route.

## SVG primitives needed
- 1× `<image>` for the full-bleed moody background photo
- 3× `<rect>` for dark overlays, top/bottom gradients, and title-legibility wash
- 4× `<line>` for dashed pathway connectors and small node tick marks
- 4× `<circle>` for large outlined node portals
- 4× `<circle>` for inner dark glass fills / center disks
- 8× `<path>` for simple white line icons inside nodes and decorative terrain silhouettes
- 5× `<ellipse>` for blurred atmospheric fog / moonlight glows
- 10× `<text>` for title, subtitle, node labels, and microcopy
- 1× `<linearGradient>` for cinematic dark overlay
- 2× `<radialGradient>` for subtle spotlight and node-fill effects
- 2× `<filter>` using `feGaussianBlur` / `feOffset` / `feMerge` for mist glow and node shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkWash" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#020508" stop-opacity="0.82"/>
      <stop offset="48%" stop-color="#071018" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#020508" stop-opacity="0.88"/>
    </linearGradient>
    <radialGradient id="coldSpot" cx="50%" cy="38%" r="70%">
      <stop offset="0%" stop-color="#94c8ff" stop-opacity="0.18"/>
      <stop offset="55%" stop-color="#1c3140" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="nodeGlass" cx="42%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="45%" stop-color="#0d1820" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#020609" stop-opacity="0.92"/>
    </radialGradient>
    <filter id="mistBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
    <filter id="nodeShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&amp;fit=crop&amp;w=1920&amp;q=80" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#darkWash)"/>
  <rect x="0" y="0" width="1280" height="210" fill="#000000" opacity="0.28"/>
  <rect x="0" y="520" width="1280" height="200" fill="#000000" opacity="0.38"/>

  <ellipse cx="650" cy="220" rx="520" ry="250" fill="url(#coldSpot)" filter="url(#mistBlur)"/>
  <ellipse cx="230" cy="540" rx="310" ry="70" fill="#c7e6ff" opacity="0.10" filter="url(#mistBlur)"/>
  <ellipse cx="810" cy="570" rx="420" ry="80" fill="#c7e6ff" opacity="0.08" filter="url(#mistBlur)"/>
  <ellipse cx="1080" cy="270" rx="160" ry="58" fill="#ffffff" opacity="0.07" filter="url(#mistBlur)"/>
  <ellipse cx="110" cy="250" rx="180" ry="60" fill="#ffffff" opacity="0.05" filter="url(#mistBlur)"/>

  <path d="M0 650 C120 612 210 635 325 600 C455 560 560 610 680 584 C810 554 900 580 1010 548 C1125 514 1190 548 1280 510 L1280 720 L0 720 Z" fill="#020406" opacity="0.78"/>
  <path d="M0 603 C135 566 240 590 365 552 C510 508 625 560 760 525 C900 490 1018 520 1145 472 C1205 450 1244 444 1280 438 L1280 720 L0 720 Z" fill="#071018" opacity="0.42"/>

  <line x1="220" y1="430" x2="470" y2="300" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-dasharray="18 18" opacity="0.78"/>
  <line x1="470" y1="300" x2="740" y2="455" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-dasharray="18 18" opacity="0.78"/>
  <line x1="740" y1="455" x2="1010" y2="325" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-dasharray="18 18" opacity="0.78"/>

  <circle cx="220" cy="430" r="83" fill="#000000" opacity="0.22" filter="url(#nodeShadow)"/>
  <circle cx="220" cy="430" r="76" fill="url(#nodeGlass)" stroke="#ffffff" stroke-width="8"/>
  <circle cx="220" cy="430" r="48" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.55"/>
  <path d="M198 433 L216 451 L246 407" fill="none" stroke="#ffffff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="220" y1="337" x2="220" y2="357" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity="0.7"/>

  <circle cx="470" cy="300" r="83" fill="#000000" opacity="0.22" filter="url(#nodeShadow)"/>
  <circle cx="470" cy="300" r="76" fill="url(#nodeGlass)" stroke="#ffffff" stroke-width="8"/>
  <path d="M440 324 L440 288 L458 288 L458 324 M466 324 L466 270 L484 270 L484 324 M492 324 L492 298 L510 298 L510 324" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M438 337 L514 337" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
  <line x1="470" y1="207" x2="470" y2="227" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity="0.7"/>

  <circle cx="740" cy="455" r="83" fill="#000000" opacity="0.22" filter="url(#nodeShadow)"/>
  <circle cx="740" cy="455" r="76" fill="url(#nodeGlass)" stroke="#ffffff" stroke-width="8"/>
  <path d="M740 411 C762 424 778 426 790 426 C786 464 768 490 740 507 C712 490 694 464 690 426 C702 426 718 424 740 411 Z" fill="none" stroke="#ffffff" stroke-width="7" stroke-linejoin="round"/>
  <path d="M718 456 L735 473 L765 439" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="740" y1="362" x2="740" y2="382" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity="0.7"/>

  <circle cx="1010" cy="325" r="83" fill="#000000" opacity="0.22" filter="url(#nodeShadow)"/>
  <circle cx="1010" cy="325" r="76" fill="url(#nodeGlass)" stroke="#ffffff" stroke-width="8"/>
  <path d="M1010 276 C1033 300 1040 329 1030 356 L1010 344 L990 356 C980 329 987 300 1010 276 Z" fill="none" stroke="#ffffff" stroke-width="7" stroke-linejoin="round"/>
  <path d="M995 365 L985 389 M1025 365 L1035 389 M1002 322 L1018 322" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
  <line x1="1010" y1="232" x2="1010" y2="252" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity="0.7"/>

  <text x="640" y="82" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="64" font-weight="900" letter-spacing="4" fill="#ffffff">ATMOSPHERIC PATHWAY</text>
  <text x="640" y="123" width="560" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="400" letter-spacing="8" fill="#d8e8f4" opacity="0.9">STRATEGIC ROADMAP / EXECUTIVE AGENDA</text>

  <text x="220" y="548" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" letter-spacing="1.5" fill="#ffffff">DISCOVER</text>
  <text x="220" y="578" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="400" fill="#d5e6f2" opacity="0.82">Map the terrain</text>

  <text x="470" y="180" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" letter-spacing="1.5" fill="#ffffff">MEASURE</text>
  <text x="470" y="210" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="400" fill="#d5e6f2" opacity="0.82">Read the signals</text>

  <text x="740" y="585" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" letter-spacing="1.5" fill="#ffffff">ALIGN</text>
  <text x="740" y="615" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="400" fill="#d5e6f2" opacity="0.82">Commit the team</text>

  <text x="1010" y="205" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" letter-spacing="1.5" fill="#ffffff">LAUNCH</text>
  <text x="1010" y="235" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="400" fill="#d5e6f2" opacity="0.82">Enter the market</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` for the dark vignette; use translucent `<rect>` overlays and gradients instead.
- ❌ Do not put `filter` on dashed connector `<line>` elements; PowerPoint translation may drop it. Keep glow/shadow filters on circles, ellipses, paths, or text.
- ❌ Do not use `marker-end` arrowheads for the pathway; if arrows are needed, draw arrowheads manually with small `<path>` triangles.
- ❌ Do not clip non-image elements; if you need cropped photography inside nodes, apply `clipPath` only to `<image>` elements.
- ❌ Avoid tiny low-contrast body text over the photo; this style depends on bold, legible white typography.

## Composition notes
- Keep the title in the top 15–20% of the slide; the pathway should own the lower two-thirds.
- Use 3–5 nodes maximum. More nodes dilute the cinematic wayfinding effect and make labels too small.
- Let the node path zigzag vertically: low-high-low-high creates motion and prevents the slide from feeling like a flat timeline.
- Maintain strong contrast: dark blue/black atmosphere, white strokes, soft mist, and only subtle cool highlights.