# SVG Recipe — Split-Spine Comparative Bar Layout

## Visual mechanism
A mirrored diverging bar chart is anchored by two tall white rounded “spine” columns in the center, which visually mask the inner ends of horizontal capsule bars. Percentages determine how far each colored bar extends outward, while dark icon medallions in the central gap turn each row into a scannable comparison unit.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft neutral background
- 2× decorative `<path>` blobs for premium keynote atmosphere without distracting from the chart
- 8× `<rect>` for left/right colored capsule bars, sized by comparative percentage values
- 2× `<rect>` for the central split-spine white vertical rounded columns
- 4× `<circle>` for central dark icon medallions
- 4× `<text>` for icon glyphs inside the medallions
- 8× `<text>` for large percentage labels at the outer ends of bars
- 8× `<text>` for short qualitative bar descriptors near the spine
- 6× `<text>` for title, subtitle, and column headers
- 4× `<linearGradient>` for premium colored bar fills
- 1× `<radialGradient>` for a subtle background glow
- 2× `<filter>` definitions: one soft shadow for the spine and one smaller shadow for icon medallions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="18%" r="80%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="55%" stop-color="#f4f6fb"/>
      <stop offset="100%" stop-color="#eceff5"/>
    </radialGradient>

    <linearGradient id="redBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#c8304b"/>
      <stop offset="100%" stop-color="#f35b74"/>
    </linearGradient>
    <linearGradient id="greenBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#20a962"/>
      <stop offset="100%" stop-color="#3fe084"/>
    </linearGradient>
    <linearGradient id="blueBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2589c7"/>
      <stop offset="100%" stop-color="#55b9f2"/>
    </linearGradient>
    <linearGradient id="purpleBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8246b3"/>
      <stop offset="100%" stop-color="#b86fe8"/>
    </linearGradient>

    <filter id="spineShadow" x="-25%" y="-10%" width="150%" height="120%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="9"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="medallionShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="5"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <path d="M-20,120 C120,55 210,80 300,150 C390,220 455,205 555,165 C485,285 350,325 215,280 C105,245 35,210 -20,245 Z"
        fill="#dfe8ff" opacity="0.48"/>
  <path d="M1320,500 C1195,440 1100,465 1008,535 C928,596 850,610 740,565 C812,675 945,720 1085,690 C1195,665 1270,615 1320,650 Z"
        fill="#f3ddff" opacity="0.45"/>

  <text x="640" y="58" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="700" fill="#242a33">
    Product Strategy: Split-Spine Performance Comparison
  </text>
  <text x="640" y="92" width="780" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#6c7480">
    Capsule bars grow away from the shared center, making percentage differences visible at a glance.
  </text>

  <text x="350" y="136" width="320" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" letter-spacing="2" fill="#d83e58">
    OPTION 1
  </text>
  <text x="350" y="164" width="390" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#7b828c">
    Current approach: familiar, lower risk, but less scalable across the full portfolio.
  </text>
  <text x="930" y="136" width="320" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" letter-spacing="2" fill="#24ae67">
    OPTION 2
  </text>
  <text x="930" y="164" width="390" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#7b828c">
    New approach: higher upside, stronger automation, and better long-term operating leverage.
  </text>

  <!-- Row 1: Cost -->
  <rect x="250" y="224" width="390" height="58" rx="29" fill="url(#redBar)"/>
  <rect x="640" y="224" width="300" height="58" rx="29" fill="url(#redBar)"/>
  <text x="286" y="262" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff">78%</text>
  <text x="936" y="262" width="96" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff">60%</text>
  <text x="446" y="259" width="135" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#ffffff">Lower upfront cost</text>
  <text x="704" y="259" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#ffffff">Higher platform ROI</text>

  <!-- Row 2: Speed -->
  <rect x="400" y="318" width="240" height="58" rx="29" fill="url(#greenBar)"/>
  <rect x="640" y="318" width="425" height="58" rx="29" fill="url(#greenBar)"/>
  <text x="436" y="356" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff">48%</text>
  <text x="1060" y="356" width="96" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff">85%</text>
  <text x="474" y="353" width="108" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#ffffff">Manual delivery</text>
  <text x="704" y="353" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#ffffff">Faster launch cycle</text>

  <!-- Row 3: Experience -->
  <rect x="300" y="412" width="340" height="58" rx="29" fill="url(#blueBar)"/>
  <rect x="640" y="412" width="245" height="58" rx="29" fill="url(#blueBar)"/>
  <text x="336" y="450" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff">68%</text>
  <text x="882" y="450" width="96" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff">49%</text>
  <text x="440" y="447" width="142" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#ffffff">Known user flows</text>
  <text x="704" y="447" width="132" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#ffffff">Learning curve</text>

  <!-- Row 4: Scalability -->
  <rect x="350" y="506" width="290" height="58" rx="29" fill="url(#purpleBar)"/>
  <rect x="640" y="506" width="455" height="58" rx="29" fill="url(#purpleBar)"/>
  <text x="386" y="544" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff">58%</text>
  <text x="1090" y="544" width="96" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff">91%</text>
  <text x="466" y="541" width="116" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#ffffff">Team dependent</text>
  <text x="704" y="541" width="154" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#ffffff">Enterprise ready</text>

  <!-- Split spine drawn above the bars to mask their inner edges -->
  <rect x="586" y="196" width="46" height="396" rx="23" fill="#ffffff" filter="url(#spineShadow)"/>
  <rect x="648" y="196" width="46" height="396" rx="23" fill="#ffffff" filter="url(#spineShadow)"/>

  <circle cx="640" cy="253" r="25" fill="#28313d" filter="url(#medallionShadow)"/>
  <circle cx="640" cy="347" r="25" fill="#28313d" filter="url(#medallionShadow)"/>
  <circle cx="640" cy="441" r="25" fill="#28313d" filter="url(#medallionShadow)"/>
  <circle cx="640" cy="535" r="25" fill="#28313d" filter="url(#medallionShadow)"/>

  <text x="640" y="262" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff">$</text>
  <text x="640" y="356" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="800" fill="#ffffff">↗</text>
  <text x="640" y="450" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#ffffff">★</text>
  <text x="640" y="544" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#ffffff">✓</text>

  <text x="640" y="635" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8a929d">
    Design tip: keep the spine perfectly vertical and let bar width carry the quantitative story.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to hide the inner bar edges; simply layer white rounded spine rectangles above the bars.
- ❌ Applying `clip-path` to bar rectangles; clipping non-image shapes is ignored by the translator.
- ❌ Building bars from many tiny segments; use one rounded `<rect>` per side so each bar remains editable.
- ❌ Putting icons in external SVG symbols or `<use>` references; use direct text glyphs or direct `<path>` icons.
- ❌ Placing percentage text under the spine layer; draw all bar labels before the spine only if they sit outside the masked center, or draw them after if they must overlap visibly.

## Composition notes
- Keep the central spine between 8–12% of slide width; it should feel structural, not like a thin axis line.
- Reserve the outer thirds for large percentage labels and the inner thirds for short qualitative descriptors.
- Use one color per row across both sides to reinforce that each row compares the same criterion.
- Leave generous top space for title and headers; the visual focus should begin around the upper-middle of the slide.