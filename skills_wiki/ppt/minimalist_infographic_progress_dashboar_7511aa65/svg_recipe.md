# SVG Recipe — Minimalist Infographic Progress Dashboard

## Visual mechanism
Convert bar-chart data into airy UI-style progress sliders: each row pairs a colored label block on the left with a thin horizontal track, a vibrant completion fill, small scale ticks, and a floating percentage pin anchored to the fill endpoint. The result feels like a premium product dashboard rather than a conventional chart.

## SVG primitives needed
- 1× `<rect>` for the white slide background / card base.
- 1× `<rect>` for a subtle outer stage or margin accent if placing the dashboard on a colored background.
- 3× `<text>` groups for left-side category titles and descriptions.
- 1× `<text>` for the centered uppercase dashboard title.
- 3× `<rect>` for pale grey progress tracks.
- 3× `<rect>` for colored progress fills with slight gradient polish.
- 15× small `<rect>` tick marks for 0%, 25%, 50%, 75%, and 100% scale positions.
- 3× rounded `<rect>` percentage pin bodies.
- 3× `<path>` downward pin pointers, color-matched to the pin body.
- 3× `<text>` labels inside the percentage pins.
- 1× `<filter id="softShadow">` applied to the main white card.
- 1× `<filter id="pinShadow">` applied to the floating pin bodies and pointers.
- 3× `<linearGradient>` definitions for crimson, teal, and blue progress fills.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pinShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="redFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#b90012"/>
      <stop offset="100%" stop-color="#d62828"/>
    </linearGradient>
    <linearGradient id="tealFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#16837b"/>
      <stop offset="100%" stop-color="#2a9d8f"/>
    </linearGradient>
    <linearGradient id="blueFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#005f9e"/>
      <stop offset="100%" stop-color="#0077b6"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f4f7fb"/>
  <rect x="58" y="54" width="1164" height="612" rx="18" fill="#ffffff" filter="url(#softShadow)"/>

  <text x="120" y="116" width="1040" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800"
        letter-spacing="1.2" fill="#333333">
    MINIMALIST PROGRESS DASHBOARD
  </text>

  <text x="112" y="186" width="290"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600"
        letter-spacing="1.8" fill="#9aa3ad">
    QUARTERLY OBJECTIVES
  </text>

  <!-- Row 1 text -->
  <text x="112" y="252" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800"
        fill="#d62828">TASK ONE</text>
  <text x="112" y="279" width="270"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#666666">
    <tspan x="112" dy="0">Launch readiness score across</tspan>
    <tspan x="112" dy="17">core operations, product, and</tspan>
    <tspan x="112" dy="17">commercial enablement.</tspan>
  </text>

  <!-- Row 2 text -->
  <text x="112" y="397" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800"
        fill="#2a9d8f">TASK TWO</text>
  <text x="112" y="424" width="270"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#666666">
    <tspan x="112" dy="0">Adoption progress measured</tspan>
    <tspan x="112" dy="17">against the target usage curve</tspan>
    <tspan x="112" dy="17">for priority accounts.</tspan>
  </text>

  <!-- Row 3 text -->
  <text x="112" y="542" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800"
        fill="#0077b6">TASK THREE</text>
  <text x="112" y="569" width="270"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#666666">
    <tspan x="112" dy="0">Completion of high-impact work</tspan>
    <tspan x="112" dy="17">streams required before the</tspan>
    <tspan x="112" dy="17">executive review milestone.</tspan>
  </text>

  <!-- Row 1 slider: 72% -->
  <rect x="430" y="262" width="700" height="10" rx="5" fill="#dedede"/>
  <rect x="430" y="262" width="504" height="10" rx="5" fill="url(#redFill)"/>
  <rect x="430" y="276" width="3" height="10" fill="#222222"/>
  <rect x="605" y="276" width="3" height="10" fill="#222222"/>
  <rect x="780" y="276" width="3" height="10" fill="#222222"/>
  <rect x="955" y="276" width="3" height="10" fill="#222222"/>
  <rect x="1128" y="276" width="3" height="10" fill="#222222"/>
  <rect x="890" y="202" width="88" height="44" rx="8" fill="#c40015" filter="url(#pinShadow)"/>
  <path d="M 922 246 L 946 246 L 934 266 Z" fill="#c40015" filter="url(#pinShadow)"/>
  <text x="934" y="231" width="88" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800"
        fill="#ffffff">72%</text>

  <!-- Row 2 slider: 85% -->
  <rect x="430" y="407" width="700" height="10" rx="5" fill="#dedede"/>
  <rect x="430" y="407" width="595" height="10" rx="5" fill="url(#tealFill)"/>
  <rect x="430" y="421" width="3" height="10" fill="#222222"/>
  <rect x="605" y="421" width="3" height="10" fill="#222222"/>
  <rect x="780" y="421" width="3" height="10" fill="#222222"/>
  <rect x="955" y="421" width="3" height="10" fill="#222222"/>
  <rect x="1128" y="421" width="3" height="10" fill="#222222"/>
  <rect x="981" y="347" width="88" height="44" rx="8" fill="#238f85" filter="url(#pinShadow)"/>
  <path d="M 1013 391 L 1037 391 L 1025 411 Z" fill="#238f85" filter="url(#pinShadow)"/>
  <text x="1025" y="376" width="88" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800"
        fill="#ffffff">85%</text>

  <!-- Row 3 slider: 96% -->
  <rect x="430" y="552" width="700" height="10" rx="5" fill="#dedede"/>
  <rect x="430" y="552" width="672" height="10" rx="5" fill="url(#blueFill)"/>
  <rect x="430" y="566" width="3" height="10" fill="#222222"/>
  <rect x="605" y="566" width="3" height="10" fill="#222222"/>
  <rect x="780" y="566" width="3" height="10" fill="#222222"/>
  <rect x="955" y="566" width="3" height="10" fill="#222222"/>
  <rect x="1128" y="566" width="3" height="10" fill="#222222"/>
  <rect x="1058" y="492" width="88" height="44" rx="8" fill="#0077b6" filter="url(#pinShadow)"/>
  <path d="M 1090 536 L 1114 536 L 1102 556 Z" fill="#0077b6" filter="url(#pinShadow)"/>
  <text x="1102" y="521" width="88" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800"
        fill="#ffffff">96%</text>

  <text x="430" y="628" width="700" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#9aa3ad">
    Each marker represents a 25% interval; pins indicate current completion.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use native chart objects or dense chart furniture; the style depends on simple editable slider-like shapes.
- ❌ Do not put `filter` on tick `<line>` elements; use small `<rect>` ticks instead if you need reliable PowerPoint output.
- ❌ Do not use `marker-end` for pointers or callout arrows; build the pin pointer as a small triangular `<path>`.
- ❌ Do not use clipped or masked shapes for the progress fill; plain rounded rectangles translate more predictably and stay editable.
- ❌ Do not crowd the scale with numeric labels at every tick unless the slide is analytical; the minimalist version works best with sparse ticks and strong percentage pins.

## Composition notes
- Keep the left metadata column to roughly 25–30% of the slide width; reserve the remaining 70–75% for the progress tracks.
- Use generous vertical spacing between rows so each progress bar reads as an independent dashboard module.
- Anchor all tracks to the same left x-position and width; let the colored fills and pins create the dynamic staggered visual rhythm.
- Match each task title, fill bar, and percentage pin color to create fast row association without needing legends.