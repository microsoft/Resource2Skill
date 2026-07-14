# SVG Recipe — Architectural Blueprint & Typographic Grid

## Visual mechanism
A warm drafting-paper field is overlaid with a precise 12×8 architectural grid, then populated with Swiss-style typography locked tightly to the grid. A single saturated yellow geometric accent and a high-contrast monochrome architecture image create the poster-like hierarchy.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm paper base
- 1× `<linearGradient>` and 1× `<radialGradient>` for subtle paper warmth and edge falloff
- 20–30× `<line>` for the visible drafting grid, measurement rules, and typographic alignment guides
- 8–12× low-opacity `<path>` / `<circle>` marks for editable faux paper grain and drafting scuffs
- 1× `<circle>` for the bold yellow geometric focal accent
- 1× `<image>` clipped by 1× `<clipPath>` for the strict-grid architectural photograph crop
- 1× `<filter id="softShadow">` applied sparingly to the photo block and accent for premium depth
- Multiple `<text>` elements with explicit `width` for massive title typography, small wide-tracked labels, body definition text, and data-like process annotations
- 2–4× `<path>` elements for crop marks, measurement brackets, and technical drawing ticks

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7f6f1"/>
      <stop offset="56%" stop-color="#efeee8"/>
      <stop offset="100%" stop-color="#f4f3ee"/>
    </linearGradient>
    <radialGradient id="edgeWarmth" cx="42%" cy="45%" r="75%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.18"/>
      <stop offset="70%" stop-color="#e7e4dc" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#d8d5cc" stop-opacity="0.20"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photoCrop">
      <rect x="747" y="180" width="426" height="450" rx="0"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paperBase)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeWarmth)"/>

  <g opacity="0.23" stroke="#d7d5ce" stroke-width="1">
    <line x1="106.7" y1="0" x2="106.7" y2="720"/>
    <line x1="213.3" y1="0" x2="213.3" y2="720"/>
    <line x1="320" y1="0" x2="320" y2="720"/>
    <line x1="426.7" y1="0" x2="426.7" y2="720"/>
    <line x1="533.3" y1="0" x2="533.3" y2="720"/>
    <line x1="640" y1="0" x2="640" y2="720"/>
    <line x1="746.7" y1="0" x2="746.7" y2="720"/>
    <line x1="853.3" y1="0" x2="853.3" y2="720"/>
    <line x1="960" y1="0" x2="960" y2="720"/>
    <line x1="1066.7" y1="0" x2="1066.7" y2="720"/>
    <line x1="1173.3" y1="0" x2="1173.3" y2="720"/>
    <line x1="0" y1="90" x2="1280" y2="90"/>
    <line x1="0" y1="180" x2="1280" y2="180"/>
    <line x1="0" y1="270" x2="1280" y2="270"/>
    <line x1="0" y1="360" x2="1280" y2="360"/>
    <line x1="0" y1="450" x2="1280" y2="450"/>
    <line x1="0" y1="540" x2="1280" y2="540"/>
    <line x1="0" y1="630" x2="1280" y2="630"/>
  </g>

  <g opacity="0.16" stroke="#c7c5bd" stroke-width="0.6">
    <line x1="53.3" y1="0" x2="53.3" y2="720"/>
    <line x1="160" y1="0" x2="160" y2="720"/>
    <line x1="0" y1="45" x2="1280" y2="45"/>
    <line x1="0" y1="135" x2="1280" y2="135"/>
    <line x1="0" y1="675" x2="1280" y2="675"/>
  </g>

  <g opacity="0.18" fill="none" stroke="#b8b6ae" stroke-width="0.7">
    <path d="M74 612 C116 608, 138 616, 176 611"/>
    <path d="M506 112 C548 118, 590 103, 642 111"/>
    <path d="M890 78 C934 83, 970 74, 1018 80"/>
    <path d="M368 660 C414 652, 466 664, 520 656"/>
  </g>
  <g opacity="0.18" fill="#c9c7be">
    <circle cx="84" cy="184" r="1.6"/>
    <circle cx="231" cy="67" r="1.2"/>
    <circle cx="612" cy="524" r="1.5"/>
    <circle cx="1112" cy="143" r="1.3"/>
    <circle cx="1196" cy="594" r="1.8"/>
  </g>

  <circle cx="160" cy="225" r="124" fill="#ffcc00" filter="url(#softShadow)"/>

  <image x="747" y="180" width="426" height="450"
         href="https://images.example.com/high-contrast-grayscale-modern-architecture-facade.jpg"
         clip-path="url(#photoCrop)" preserveAspectRatio="xMidYMid slice" filter="url(#softShadow)"/>

  <g fill="none" stroke="#161616" stroke-width="1.2" opacity="0.9">
    <path d="M747 164 L747 142 L790 142"/>
    <path d="M1173 646 L1173 668 L1130 668"/>
    <path d="M692 180 L720 180 M706 166 L706 194"/>
    <path d="M1188 405 L1218 405 M1203 390 L1203 420"/>
  </g>

  <text x="48" y="52" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" letter-spacing="4" fill="#171717">SYSTEM / METHOD BOARD</text>
  <text x="1030" y="52" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" letter-spacing="4" fill="#171717">GRID 12×8</text>
  <text x="48" y="685" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="10" letter-spacing="3.2" fill="#171717">ARCHITECTURAL WORKFLOW</text>
  <text x="982" y="685" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="10" letter-spacing="3.2" fill="#171717">REVISION 04 / 2026</text>

  <text x="51" y="372" width="650" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="132" font-weight="900" letter-spacing="-7" fill="#141414">workflow</text>

  <text x="57" y="424" width="520" font-family="Georgia, serif" font-size="22"
        font-style="italic" fill="#242424">/ˈwərkˌflō/</text>

  <text x="57" y="468" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#171717">
    <tspan x="57" dy="0">the order of stages in a structured</tspan>
    <tspan x="57" dy="29">work process; a deliberate sequence</tspan>
    <tspan x="57" dy="29">for turning ambiguity into output.</tspan>
  </text>

  <text x="320" y="111" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" letter-spacing="3" fill="#171717">01 / DISCOVER</text>
  <text x="320" y="142" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#171717">Map constraints, actors, and known unknowns.</text>

  <text x="534" y="111" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" letter-spacing="3" fill="#171717">02 / MODEL</text>
  <text x="534" y="142" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#171717">Convert raw inputs into a repeatable system.</text>

  <text x="747" y="154" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" letter-spacing="3.5" fill="#171717">REFERENCE IMAGE FIELD</text>
  <text x="747" y="654" width="426" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" letter-spacing="2.2" fill="#171717">CONCRETE / STEEL / VOID / SCALE</text>

  <text x="640" y="608" width="72" font-family="Segoe UI Black, Segoe UI, sans-serif"
        font-size="44" font-weight="900" fill="#141414">03</text>
  <text x="640" y="635" width="88" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" letter-spacing="2.4" fill="#141414">OUTPUT</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` for paper noise; it will not translate reliably. Use editable low-opacity speckles, paths, and subtle gradients instead.
- ❌ Do not rely on SVG grayscale filters such as `feColorMatrix`; prepare or choose a grayscale image before inserting it.
- ❌ Do not place `clip-path` on text, rectangles, or decorative shapes. Use clipping only on the `<image>`.
- ❌ Do not omit `width` on any `<text>` element; PowerPoint will otherwise render text unpredictably.
- ❌ Do not make the grid visually heavy. The grid should feel like drafting construction lines, not a table.

## Composition notes
- Keep the image block locked to exact grid boundaries, typically occupying the lower-right 4 columns by 5 rows.
- Let the massive wordmark dominate the left half; it should overlap the yellow circle but remain sharply readable.
- Use tiny wide-tracked labels in the corners and along grid intersections to create the technical-board atmosphere.
- Maintain a restrained palette: warm paper, charcoal text, pale gray grid, and one saturated yellow accent.