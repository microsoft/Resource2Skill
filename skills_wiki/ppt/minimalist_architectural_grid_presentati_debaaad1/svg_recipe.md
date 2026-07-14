# SVG Recipe — Minimalist Architectural Grid Presentation

## Visual mechanism
A premium editorial board built from a strict modular grid: one dominant architectural image anchors the composition while smaller analytical panels align precisely to its edges. The style depends on generous whitespace, thin rules, monochrome typography, and restrained diagrammatic detail rather than decoration.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 8–12× `<line>` for visible grid guide rules and panel alignment lines
- 4× `<rect>` for white content cards / image frames with subtle shadow
- 1× `<image>` for the large hero architectural render or project photograph
- 1× `<clipPath>` with rounded `<rect>` applied only to the hero `<image>`
- 1× `<linearGradient>` for a soft white fade over the hero image
- 1× `<filter id="softShadow">` applied to card `<rect>` elements for quiet depth
- Multiple `<text>` elements with explicit `width` for title, metadata, captions, labels, and body copy
- Multiple `<path>` elements for massing outlines, floor-plan walls, section cuts, circulation paths, and miniature diagram graphics
- Multiple `<circle>` elements for process nodes and plan/diagram markers
- Several `<rect>` elements for program bars, legends, and architectural plan blocks

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperTint" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#fbfbfa"/>
      <stop offset="1" stop-color="#f3f3f1"/>
    </linearGradient>
    <linearGradient id="heroFade" x1="64" y1="154" x2="788" y2="606" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="0.72" stop-color="#ffffff" stop-opacity="0.00"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.35"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="heroClip">
      <rect x="64" y="154" width="724" height="452" rx="4"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paperTint)"/>

  <!-- architectural grid scaffold -->
  <line x1="64" y1="112" x2="1216" y2="112" stroke="#d8d8d5" stroke-width="1"/>
  <line x1="64" y1="154" x2="1216" y2="154" stroke="#c9c9c6" stroke-width="1"/>
  <line x1="64" y1="606" x2="1216" y2="606" stroke="#c9c9c6" stroke-width="1"/>
  <line x1="64" y1="650" x2="1216" y2="650" stroke="#d8d8d5" stroke-width="1"/>
  <line x1="64" y1="112" x2="64" y2="650" stroke="#d8d8d5" stroke-width="1"/>
  <line x1="788" y1="112" x2="788" y2="650" stroke="#d8d8d5" stroke-width="1"/>
  <line x1="824" y1="112" x2="824" y2="650" stroke="#d8d8d5" stroke-width="1"/>
  <line x1="1216" y1="112" x2="1216" y2="650" stroke="#d8d8d5" stroke-width="1"/>

  <!-- header -->
  <text x="64" y="66" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="32" font-weight="700" fill="#222222" letter-spacing="3">
    URBAN RENEWAL PAVILION
  </text>
  <text x="66" y="94" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#777777" letter-spacing="1.4">
    ARCHITECTURAL STRATEGY BOARD / CONCEPT + SYSTEMS
  </text>
  <text x="1010" y="64" width="206" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#444444" text-anchor="end">
    SITE 04 · MIXED-USE CIVIC EDGE
  </text>
  <text x="1010" y="88" width="206" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#8a8a8a" text-anchor="end">
    LAT 40.72 / LONG -73.99
  </text>

  <!-- hero image board -->
  <rect x="64" y="154" width="724" height="452" rx="4" fill="#ffffff" filter="url(#softShadow)"/>
  <image x="64" y="154" width="724" height="452" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/architectural-hero-brutalist-pavilion-courtyard.jpg"
         clip-path="url(#heroClip)"/>
  <rect x="64" y="154" width="724" height="452" rx="4" fill="url(#heroFade)"/>
  <rect x="64" y="154" width="724" height="452" rx="4" fill="none" stroke="#1e1e1e" stroke-width="1.2"/>

  <!-- subtle measured overlay on hero -->
  <line x1="154" y1="154" x2="154" y2="606" stroke="#ffffff" stroke-opacity="0.35" stroke-width="1"/>
  <line x1="245" y1="154" x2="245" y2="606" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1"/>
  <line x1="335" y1="154" x2="335" y2="606" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1"/>
  <line x1="426" y1="154" x2="426" y2="606" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1"/>
  <line x1="516" y1="154" x2="516" y2="606" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1"/>
  <line x1="607" y1="154" x2="607" y2="606" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1"/>
  <line x1="697" y1="154" x2="697" y2="606" stroke="#ffffff" stroke-opacity="0.35" stroke-width="1"/>
  <path d="M130 510 L335 300 L560 430 L716 350" fill="none" stroke="#ffffff" stroke-opacity="0.72" stroke-width="2"/>
  <circle cx="335" cy="300" r="4" fill="#ffffff"/>
  <circle cx="560" cy="430" r="4" fill="#ffffff"/>
  <text x="86" y="584" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#ffffff" letter-spacing="1.2">
    FIG.01 / PRIMARY MASSING + PUBLIC GROUND PLANE
  </text>

  <!-- concept text card -->
  <rect x="824" y="154" width="392" height="148" rx="3" fill="#ffffff" filter="url(#softShadow)"/>
  <text x="846" y="184" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#1e1e1e" letter-spacing="1.6">
    DESIGN INTENT
  </text>
  <line x1="846" y1="198" x2="1194" y2="198" stroke="#d7d7d3" stroke-width="1"/>
  <text x="846" y="224" width="332" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#414141">
    <tspan x="846" dy="0">The pavilion organizes civic programs through a</tspan>
    <tspan x="846" dy="16">clear structural grid. Heavy service volumes sit at</tspan>
    <tspan x="846" dy="16">the perimeter, leaving the ground level porous and</tspan>
    <tspan x="846" dy="16">public. The board reads as evidence: image first,</tspan>
    <tspan x="846" dy="16">then concept, then analytical proof.</tspan>
  </text>

  <!-- plan card -->
  <rect x="824" y="326" width="184" height="128" rx="3" fill="#ffffff" filter="url(#softShadow)"/>
  <text x="842" y="350" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" font-weight="700" fill="#222222" letter-spacing="1.4">
    PLAN 1:500
  </text>
  <rect x="852" y="370" width="112" height="58" fill="#f1f1ef" stroke="#222222" stroke-width="2"/>
  <path d="M852 398 H906 M920 370 V428 M964 392 H940" fill="none" stroke="#222222" stroke-width="2"/>
  <path d="M862 416 C890 386, 918 386, 954 378" fill="none" stroke="#8a8a8a" stroke-width="1.5" stroke-dasharray="4 4"/>
  <circle cx="862" cy="416" r="3" fill="#222222"/>
  <circle cx="954" cy="378" r="3" fill="#222222"/>

  <!-- section card -->
  <rect x="1032" y="326" width="184" height="128" rx="3" fill="#ffffff" filter="url(#softShadow)"/>
  <text x="1050" y="350" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" font-weight="700" fill="#222222" letter-spacing="1.4">
    SECTION A-A
  </text>
  <rect x="1054" y="411" width="138" height="18" fill="#d0d0cc"/>
  <path d="M1070 411 V378 H1172 V411" fill="none" stroke="#222222" stroke-width="3"/>
  <line x1="1062" y1="378" x2="1180" y2="378" stroke="#222222" stroke-width="3"/>
  <line x1="1090" y1="392" x2="1152" y2="392" stroke="#9a9a96" stroke-width="1"/>
  <line x1="1090" y1="402" x2="1152" y2="402" stroke="#9a9a96" stroke-width="1"/>
  <path d="M1070 430 C1100 420, 1136 438, 1192 425" fill="none" stroke="#7e7e7a" stroke-width="1" stroke-dasharray="3 4"/>

  <!-- program / process card -->
  <rect x="824" y="478" width="392" height="128" rx="3" fill="#ffffff" filter="url(#softShadow)"/>
  <text x="846" y="502" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" font-weight="700" fill="#222222" letter-spacing="1.4">
    PROGRAM MIX
  </text>
  <rect x="846" y="526" width="136" height="10" fill="#222222"/>
  <rect x="846" y="546" width="96" height="10" fill="#747474"/>
  <rect x="846" y="566" width="64" height="10" fill="#b7b7b2"/>
  <text x="996" y="535" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="9" fill="#555555">PUBLIC FORUM</text>
  <text x="996" y="555" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="9" fill="#555555">WORKSHOP</text>
  <text x="996" y="575" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="9" fill="#555555">SERVICE</text>
  <line x1="1102" y1="548" x2="1188" y2="548" stroke="#222222" stroke-width="1"/>
  <circle cx="1102" cy="548" r="5" fill="#222222"/>
  <circle cx="1145" cy="548" r="5" fill="#ffffff" stroke="#222222" stroke-width="1.5"/>
  <circle cx="1188" cy="548" r="5" fill="#ffffff" stroke="#222222" stroke-width="1.5"/>
  <text x="1090" y="580" width="112" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="9" fill="#777777" text-anchor="middle">
    SITE → GRID → MASS
  </text>

  <!-- footer -->
  <text x="64" y="676" width="480" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="9" fill="#777777" letter-spacing="1.2">
    ALL PANELS SNAP TO A 12-COLUMN ARCHITECTURAL GRID · NEGATIVE SPACE IS INTENTIONAL
  </text>
  <text x="1120" y="676" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="9" fill="#777777" text-anchor="end">
    BOARD 01 / 06
  </text>
</svg>
```

## Avoid in this skill
- ❌ Floating scrapbook placement; every image, diagram, and label must snap to shared grid edges.
- ❌ Heavy decorative gradients, saturated template colors, or ornamental icons that compete with the project evidence.
- ❌ Using `<clipPath>` on text, rects, or paths; for PPT translation, apply clipping only to `<image>`.
- ❌ Dense paragraphs without hierarchy; small body copy should be grouped into clearly labeled information cards.
- ❌ PowerPoint arrows via `marker-end` on `<path>`; use plain `<line>` or hand-drawn arrow geometry if directional annotation is required.

## Composition notes
- Keep the hero image dominant: roughly 55–65% of the slide width, aligned to the main vertical grid.
- Reserve the right column for evidence modules: concept copy, plan, section, and program data stacked with consistent gutters.
- Use thin visible rules and white card surfaces to reveal the grid without making the slide feel like a spreadsheet.
- Let color come primarily from the architectural image; keep typography, diagrams, borders, and labels monochrome.