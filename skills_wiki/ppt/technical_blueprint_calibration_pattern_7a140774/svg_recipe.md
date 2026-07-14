# SVG Recipe — Technical Blueprint Calibration Pattern

## Visual mechanism
A dark, high-contrast calibration slide built from mathematically centered cyan geometry: a 16:9 safe-area frame, a dashed 4:3 frame, concentric circular targets, crosshairs, tick marks, and small engineering labels. The result feels like a precision AV test card or technical schematic while remaining fully editable vector geometry.

## SVG primitives needed
- 1× `<rect>` for the full dark blueprint background
- 2× `<rect>` for the outer 16:9 frame and inner dashed 4:3 frame
- 4× `<circle>` for the central circular target and concentric calibration rings
- 18× `<line>` for crosshairs, diagonal guides, ruler ticks, and center axes
- 8× `<path>` for L-shaped corner brackets and small schematic accent marks
- 12× `<text>` labels for aspect ratios, coordinates, title, subtitle, and measurement annotations
- 1× `<radialGradient>` for subtle dark-center blueprint depth
- 1× `<linearGradient>` for cyan-to-blue stroke accents
- 1× `<filter id="cyanGlow">` applied to editable rect/circle/path/text elements for neon schematic glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="50%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#081923"/>
      <stop offset="58%" stop-color="#02090e"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>
    <linearGradient id="cyanStroke" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#7ff7ff"/>
      <stop offset="48%" stop-color="#00bfff"/>
      <stop offset="100%" stop-color="#1683ff"/>
    </linearGradient>
    <filter id="cyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="softGlow"/>
      <feMerge>
        <feMergeNode in="softGlow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>

  <!-- faint blueprint grid -->
  <line x1="160" y1="0" x2="160" y2="720" stroke="#06384a" stroke-width="1"/>
  <line x1="320" y1="0" x2="320" y2="720" stroke="#06384a" stroke-width="1"/>
  <line x1="480" y1="0" x2="480" y2="720" stroke="#06384a" stroke-width="1"/>
  <line x1="640" y1="0" x2="640" y2="720" stroke="#0a5268" stroke-width="1.5"/>
  <line x1="800" y1="0" x2="800" y2="720" stroke="#06384a" stroke-width="1"/>
  <line x1="960" y1="0" x2="960" y2="720" stroke="#06384a" stroke-width="1"/>
  <line x1="1120" y1="0" x2="1120" y2="720" stroke="#06384a" stroke-width="1"/>
  <line x1="0" y1="120" x2="1280" y2="120" stroke="#06384a" stroke-width="1"/>
  <line x1="0" y1="240" x2="1280" y2="240" stroke="#06384a" stroke-width="1"/>
  <line x1="0" y1="360" x2="1280" y2="360" stroke="#0a5268" stroke-width="1.5"/>
  <line x1="0" y1="480" x2="1280" y2="480" stroke="#06384a" stroke-width="1"/>
  <line x1="0" y1="600" x2="1280" y2="600" stroke="#06384a" stroke-width="1"/>

  <!-- exact aspect frames -->
  <rect x="80" y="45" width="1120" height="630" fill="none" stroke="url(#cyanStroke)" stroke-width="2.5" filter="url(#cyanGlow)"/>
  <rect x="220" y="45" width="840" height="630" fill="none" stroke="#00bfff" stroke-width="2" stroke-dasharray="14 10" filter="url(#cyanGlow)"/>

  <!-- corner engineering brackets -->
  <path d="M80 95 L80 45 L130 45" fill="none" stroke="#7ff7ff" stroke-width="5" filter="url(#cyanGlow)"/>
  <path d="M1150 45 L1200 45 L1200 95" fill="none" stroke="#7ff7ff" stroke-width="5" filter="url(#cyanGlow)"/>
  <path d="M80 625 L80 675 L130 675" fill="none" stroke="#7ff7ff" stroke-width="5" filter="url(#cyanGlow)"/>
  <path d="M1150 675 L1200 675 L1200 625" fill="none" stroke="#7ff7ff" stroke-width="5" filter="url(#cyanGlow)"/>

  <!-- diagonals and center axes -->
  <line x1="80" y1="45" x2="1200" y2="675" stroke="#095f78" stroke-width="1.5" stroke-dasharray="8 10"/>
  <line x1="1200" y1="45" x2="80" y2="675" stroke="#095f78" stroke-width="1.5" stroke-dasharray="8 10"/>
  <line x1="80" y1="360" x2="1200" y2="360" stroke="#00bfff" stroke-width="2"/>
  <line x1="640" y1="45" x2="640" y2="675" stroke="#00bfff" stroke-width="2"/>

  <!-- central circular calibration target -->
  <circle cx="640" cy="360" r="158" fill="none" stroke="url(#cyanStroke)" stroke-width="4" filter="url(#cyanGlow)"/>
  <circle cx="640" cy="360" r="118" fill="none" stroke="#00bfff" stroke-width="1.8" stroke-dasharray="9 8" filter="url(#cyanGlow)"/>
  <circle cx="640" cy="360" r="76" fill="none" stroke="#7ff7ff" stroke-width="1.5"/>
  <circle cx="640" cy="360" r="8" fill="#00bfff" stroke="#ffffff" stroke-width="2" filter="url(#cyanGlow)"/>

  <!-- target tick marks -->
  <line x1="640" y1="175" x2="640" y2="214" stroke="#7ff7ff" stroke-width="3"/>
  <line x1="640" y1="506" x2="640" y2="545" stroke="#7ff7ff" stroke-width="3"/>
  <line x1="455" y1="360" x2="494" y2="360" stroke="#7ff7ff" stroke-width="3"/>
  <line x1="786" y1="360" x2="825" y2="360" stroke="#7ff7ff" stroke-width="3"/>

  <!-- ruler-style edge ticks -->
  <path d="M220 45 L220 72 M360 45 L360 64 M500 45 L500 72 M780 45 L780 72 M920 45 L920 64 M1060 45 L1060 72" fill="none" stroke="#00bfff" stroke-width="2"/>
  <path d="M220 675 L220 648 M360 675 L360 656 M500 675 L500 648 M780 675 L780 648 M920 675 L920 656 M1060 675 L1060 648" fill="none" stroke="#00bfff" stroke-width="2"/>
  <path d="M80 150 L108 150 M80 255 L100 255 M80 465 L100 465 M80 570 L108 570" fill="none" stroke="#00bfff" stroke-width="2"/>
  <path d="M1200 150 L1172 150 M1200 255 L1180 255 M1200 465 L1180 465 M1200 570 L1172 570" fill="none" stroke="#00bfff" stroke-width="2"/>

  <!-- small calibration chips -->
  <rect x="510" y="92" width="44" height="12" fill="#ffffff"/>
  <rect x="558" y="92" width="44" height="12" fill="#b7f9ff"/>
  <rect x="606" y="92" width="44" height="12" fill="#00bfff"/>
  <rect x="654" y="92" width="44" height="12" fill="#006b8a"/>
  <rect x="702" y="92" width="44" height="12" fill="#001b25"/>

  <!-- labels -->
  <text x="96" y="72" width="260" fill="#7ff7ff" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2">16:9 SAFE FRAME</text>
  <text x="236" y="665" width="220" fill="#00bfff" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2">4:3 CENTER CROP</text>
  <text x="1010" y="665" width="180" fill="#7ff7ff" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="end">1280×720 GRID</text>
  <text x="640" y="304" width="420" fill="#ffffff" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" text-anchor="middle" filter="url(#cyanGlow)">ASPECT RATIO TEST</text>
  <text x="640" y="340" width="360" fill="#b7f9ff" font-family="Segoe UI, Microsoft YaHei" font-size="17" text-anchor="middle">center target should appear perfectly circular</text>
  <text x="640" y="402" width="300" fill="#00bfff" font-family="Segoe UI, Microsoft YaHei" font-size="14" text-anchor="middle" letter-spacing="3">X 640  /  Y 360</text>
  <text x="640" y="428" width="330" fill="#7ff7ff" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle">NO STRETCH · NO OVERSCAN · NO CROP</text>
  <text x="96" y="638" width="140" fill="#00bfff" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700">16:9</text>
  <text x="236" y="638" width="140" fill="#00bfff" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700">4:3</text>
  <text x="1085" y="72" width="100" fill="#7ff7ff" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end">CAL-01</text>
  <text x="1085" y="92" width="120" fill="#7ff7ff" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end">BLUEPRINT HUD</text>
  <text x="640" y="116" width="280" fill="#b7f9ff" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle">LUMINANCE STRIP</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `filter` to `<line>` elements; PowerPoint translation may drop the effect, so use glow only on rects, circles, paths, or text.
- ❌ Using `<pattern>` for the blueprint grid; draw individual editable grid lines instead.
- ❌ Using `marker-end` arrowheads for schematic callouts; if arrows are needed, use simple `<line>` plus separate `<path>` chevrons.
- ❌ Clipping or masking vector shapes to create scanlines; keep calibration geometry as direct editable strokes.
- ❌ Overcrowding the slide with dense micro-labels that become unreadable after PowerPoint scaling.

## Composition notes
- Keep the whole design perfectly symmetrical around `cx=640`, `cy=360`; the central circle is the functional and visual anchor.
- Use cyan strokes against a near-black background, with white reserved only for the main test title and small luminance chips.
- The outer frame should read as the 16:9 boundary; the dashed inner frame should clearly imply a secondary 4:3 crop/safe zone.
- Leave the center target mostly uncluttered so distortion is obvious during projection or screen calibration.