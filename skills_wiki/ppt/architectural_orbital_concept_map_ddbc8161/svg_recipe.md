# SVG Recipe — Architectural Orbital Concept Map

## Visual mechanism
A dark blueprint field anchors a central thesis inside concentric orbital rings, with 4–5 peripheral concept nodes positioned like architectural plan callouts. Thin drafting lines, miniature schematic drawings, and one disruptive red accent connector create a rigorous but dramatic conceptual framework.

## SVG primitives needed
- 1× `<rect>` for the dark full-slide background
- 1× `<rect>` with radial/linear gradient overlay for subtle vignette depth
- 2× `<path>` for blueprint grid linework, using long compound paths instead of patterns
- 4× `<circle>` for transparent concentric orbit rings around the core
- 5× `<line>` for node-to-core connectors, including one red accent connector
- 5× `<circle>` for node image/diagram containers
- 5× `<rect>` for small architectural sketch panels behind each node
- 20–30× `<path>` and `<line>` for miniature architectural diagrams, axes, floor-plan marks, and drafting ticks
- 1× `<rect>` for the central thesis card
- 1× `<circle>` for the central gravity point / core diagram
- 8–10× `<text>` blocks with explicit `width` attributes for core title, section labels, captions, and coordinate annotations
- 1× `<filter id="softGlow">` for faint halo around the central thesis and accent node
- 1× `<filter id="cardShadow">` for subtle depth beneath cards and node panels
- 2× `<linearGradient>` / `<radialGradient>` definitions for background and node highlights

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="50%" cy="48%" r="70%">
      <stop offset="0%" stop-color="#18181d"/>
      <stop offset="55%" stop-color="#0b0b0e"/>
      <stop offset="100%" stop-color="#050506"/>
    </radialGradient>
    <linearGradient id="nodeSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.14"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.18"/>
    </linearGradient>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cardShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.12"/>

  <path d="M0 80 H1280 M0 160 H1280 M0 240 H1280 M0 320 H1280 M0 400 H1280 M0 480 H1280 M0 560 H1280 M0 640 H1280" stroke="#23232b" stroke-width="1" opacity="0.55"/>
  <path d="M80 0 V720 M160 0 V720 M240 0 V720 M320 0 V720 M400 0 V720 M480 0 V720 M560 0 V720 M640 0 V720 M720 0 V720 M800 0 V720 M880 0 V720 M960 0 V720 M1040 0 V720 M1120 0 V720 M1200 0 V720" stroke="#23232b" stroke-width="1" opacity="0.55"/>
  <path d="M0 40 H1280 M0 120 H1280 M0 200 H1280 M0 280 H1280 M0 360 H1280 M0 440 H1280 M0 520 H1280 M0 600 H1280 M0 680 H1280" stroke="#15151a" stroke-width="1" opacity="0.9"/>
  <path d="M40 0 V720 M120 0 V720 M200 0 V720 M280 0 V720 M360 0 V720 M440 0 V720 M520 0 V720 M600 0 V720 M680 0 V720 M760 0 V720 M840 0 V720 M920 0 V720 M1000 0 V720 M1080 0 V720 M1160 0 V720 M1240 0 V720" stroke="#15151a" stroke-width="1" opacity="0.9"/>

  <circle cx="640" cy="360" r="86" fill="none" stroke="#e8e8e8" stroke-width="1.2" opacity="0.48"/>
  <circle cx="640" cy="360" r="150" fill="none" stroke="#cfcfd6" stroke-width="1" opacity="0.28"/>
  <circle cx="640" cy="360" r="236" fill="none" stroke="#e8e8e8" stroke-width="1.2" opacity="0.36"/>
  <circle cx="640" cy="360" r="302" fill="none" stroke="#777783" stroke-width="1" stroke-dasharray="8 12" opacity="0.42"/>

  <line x1="640" y1="360" x2="640" y2="124" stroke="#cfcfd6" stroke-width="1.2" opacity="0.62"/>
  <line x1="640" y1="360" x2="876" y2="360" stroke="#cfcfd6" stroke-width="1.2" opacity="0.62"/>
  <line x1="640" y1="360" x2="640" y2="596" stroke="#cfcfd6" stroke-width="1.2" opacity="0.62"/>
  <line x1="640" y1="360" x2="404" y2="360" stroke="#cfcfd6" stroke-width="1.2" opacity="0.62"/>
  <line x1="640" y1="360" x2="862" y2="512" stroke="#dc3c3c" stroke-width="3" opacity="0.9"/>

  <rect x="506" y="286" width="268" height="148" rx="10" fill="#111116" stroke="#f0f0f0" stroke-width="1.2" filter="url(#cardShadow)"/>
  <circle cx="640" cy="360" r="38" fill="#17171d" stroke="#f0f0f0" stroke-width="1.2" filter="url(#softGlow)"/>
  <path d="M620 362 L640 338 L661 362 L640 384 Z M628 362 H652 M640 338 V384" fill="none" stroke="#dc3c3c" stroke-width="2"/>
  <text x="540" y="326" width="200" font-family="Georgia, serif" font-size="15" font-weight="700" fill="#f2f2f2" text-anchor="middle" letter-spacing="2">CORE THESIS</text>
  <text x="540" y="408" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#a8a8ad" text-anchor="middle">A spatial framework where context, access, program, material, and disruption orbit one governing idea.</text>

  <rect x="552" y="56" width="176" height="92" rx="8" fill="#0f0f13" stroke="#bfc0c8" stroke-width="1" filter="url(#cardShadow)"/>
  <circle cx="640" cy="124" r="44" fill="url(#nodeSheen)" stroke="#f0f0f0" stroke-width="1.1"/>
  <path d="M610 122 H670 M620 106 V138 M640 100 V144 M660 110 V134 M614 134 L666 110" stroke="#d5d5d8" stroke-width="1.4" fill="none"/>
  <text x="560" y="176" width="160" font-family="Georgia, serif" font-size="12" font-weight="700" fill="#f2f2f2" text-anchor="middle" letter-spacing="1.4">CONTEXT</text>
  <text x="548" y="194" width="184" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#9a9aa2" text-anchor="middle">site forces / cultural grain</text>

  <rect x="788" y="314" width="176" height="92" rx="8" fill="#0f0f13" stroke="#bfc0c8" stroke-width="1" filter="url(#cardShadow)"/>
  <circle cx="876" cy="360" r="44" fill="url(#nodeSheen)" stroke="#f0f0f0" stroke-width="1.1"/>
  <path d="M846 350 H906 M846 370 H906 M858 338 V382 M876 338 V382 M894 338 V382" stroke="#d5d5d8" stroke-width="1.4" fill="none"/>
  <text x="796" y="434" width="160" font-family="Georgia, serif" font-size="12" font-weight="700" fill="#f2f2f2" text-anchor="middle" letter-spacing="1.4">PROGRAM</text>
  <text x="784" y="452" width="184" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#9a9aa2" text-anchor="middle">functions / adjacencies</text>

  <rect x="552" y="572" width="176" height="92" rx="8" fill="#0f0f13" stroke="#bfc0c8" stroke-width="1" filter="url(#cardShadow)"/>
  <circle cx="640" cy="596" r="44" fill="url(#nodeSheen)" stroke="#f0f0f0" stroke-width="1.1"/>
  <path d="M612 608 C626 580 654 580 668 608 M612 608 H668 M622 608 V584 M640 608 V576 M658 608 V584" stroke="#d5d5d8" stroke-width="1.4" fill="none"/>
  <text x="560" y="684" width="160" font-family="Georgia, serif" font-size="12" font-weight="700" fill="#f2f2f2" text-anchor="middle" letter-spacing="1.4">MATERIAL</text>

  <rect x="316" y="314" width="176" height="92" rx="8" fill="#0f0f13" stroke="#bfc0c8" stroke-width="1" filter="url(#cardShadow)"/>
  <circle cx="404" cy="360" r="44" fill="url(#nodeSheen)" stroke="#f0f0f0" stroke-width="1.1"/>
  <path d="M374 360 L404 330 L434 360 L404 390 Z M404 330 V390 M374 360 H434" stroke="#d5d5d8" stroke-width="1.4" fill="none"/>
  <text x="324" y="434" width="160" font-family="Georgia, serif" font-size="12" font-weight="700" fill="#f2f2f2" text-anchor="middle" letter-spacing="1.4">ACCESS</text>
  <text x="312" y="452" width="184" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#9a9aa2" text-anchor="middle">movement / thresholds</text>

  <rect x="774" y="466" width="176" height="92" rx="8" fill="#180c0c" stroke="#dc3c3c" stroke-width="1.6" filter="url(#cardShadow)"/>
  <circle cx="862" cy="512" r="44" fill="#1a0d0d" stroke="#dc3c3c" stroke-width="2" filter="url(#softGlow)"/>
  <path d="M836 530 L862 486 L888 530 Z M846 522 H878 M862 486 V530" stroke="#dc3c3c" stroke-width="2.2" fill="none"/>
  <text x="782" y="588" width="160" font-family="Georgia, serif" font-size="12" font-weight="700" fill="#dc3c3c" text-anchor="middle" letter-spacing="1.4">DISRUPTION</text>
  <text x="770" y="606" width="184" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#b9a0a0" text-anchor="middle">the critical counter-force</text>

  <text x="54" y="70" width="360" font-family="Georgia, serif" font-size="22" font-weight="700" fill="#f2f2f2" letter-spacing="2">ARCHITECTURAL ORBITAL MAP</text>
  <text x="56" y="104" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#8e8e96">CONCEPTUAL MODEL / 01 CORE + 05 SYSTEMS</text>
  <text x="1040" y="664" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#6f6f78" text-anchor="end">RADIUS 236 / GRID 40 / DRAFT RED</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` for the blueprint grid; create compound `<path>` grid lines so the result remains editable.
- ❌ Do not use `<mask>` to fade orbit rings or crop cards; use opacity, gradients, and native shapes instead.
- ❌ Do not apply filters to `<line>` connectors; filter effects on lines may be dropped, so keep connectors crisp and unfiltered.
- ❌ Do not build the whole concept map as one raster image; the value of this technique is editable rings, labels, connectors, and node diagrams.
- ❌ Do not overcrowd with more than 5 orbit nodes unless the ring radius and text scale are redesigned.

## Composition notes
- Keep the central thesis card near the exact canvas center; the entire slide should feel like a gravity system organized around that point.
- Use 55–65% of the slide width for the orbital diagram, leaving corners for title, coordinates, legends, or thesis metadata.
- Make most geometry monochrome and reserve one saturated red node/connector for the disruptive or most important concept.
- Node labels should sit just outside their diagram containers, with enough negative space that the orbit rings remain visible through the structure.