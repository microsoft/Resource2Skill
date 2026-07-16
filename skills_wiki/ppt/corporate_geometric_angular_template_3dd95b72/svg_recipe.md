# SVG Recipe — Corporate Geometric Angular Template

## Visual mechanism
A mostly white executive slide is given depth with a barely visible hexagonal line mesh, then energized by a large angled corporate color block on the right edge. The diagonal boundary creates motion while preserving a disciplined left-side content zone for editable titles, body copy, and chart callouts.

## SVG primitives needed
- 1× `<rect>` for the clean white slide base.
- 25–40× `<path>` for the subtle hexagonal background watermark.
- 4–6× `<path>` for the large right-side angular trapezoid and overlapping geometric facets.
- 2–4× `<line>` or stroked `<path>` elements for thin diagonal highlight accents on the colored block.
- 1× `<filter id="softShadow">` applied to the main angular block for slight depth.
- 1× `<linearGradient>` for the main corporate accent block.
- 3–5× `<text>` elements with explicit `width` attributes for editable title, subtitle, body, and small labels.
- 1× `<rect>` for the short thick accent divider beneath the headline.
- Optional small `<circle>` or `<rect>` elements for metric chips or content anchors.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentGrad" x1="760" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#E35B3B"/>
      <stop offset="55%" stop-color="#D34B32"/>
      <stop offset="100%" stop-color="#B93D2A"/>
    </linearGradient>

    <linearGradient id="facetGrad" x1="980" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF8A5C" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#8E2B22" stop-opacity="0.25"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feOffset dx="-10" dy="0" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Clean base -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Subtle geometric watermark mesh: do not use pattern; draw editable paths -->
  <g fill="none" stroke="#EDEDED" stroke-width="1.2" opacity="0.82">
    <path d="M44 22 L80 43 L80 85 L44 106 L8 85 L8 43 Z"/>
    <path d="M118 64 L154 85 L154 127 L118 148 L82 127 L82 85 Z"/>
    <path d="M192 22 L228 43 L228 85 L192 106 L156 85 L156 43 Z"/>
    <path d="M266 64 L302 85 L302 127 L266 148 L230 127 L230 85 Z"/>
    <path d="M340 22 L376 43 L376 85 L340 106 L304 85 L304 43 Z"/>
    <path d="M414 64 L450 85 L450 127 L414 148 L378 127 L378 85 Z"/>
    <path d="M488 22 L524 43 L524 85 L488 106 L452 85 L452 43 Z"/>
    <path d="M562 64 L598 85 L598 127 L562 148 L526 127 L526 85 Z"/>

    <path d="M44 148 L80 169 L80 211 L44 232 L8 211 L8 169 Z"/>
    <path d="M118 190 L154 211 L154 253 L118 274 L82 253 L82 211 Z"/>
    <path d="M192 148 L228 169 L228 211 L192 232 L156 211 L156 169 Z"/>
    <path d="M266 190 L302 211 L302 253 L266 274 L230 253 L230 211 Z"/>
    <path d="M340 148 L376 169 L376 211 L340 232 L304 211 L304 169 Z"/>
    <path d="M414 190 L450 211 L450 253 L414 274 L378 253 L378 211 Z"/>
    <path d="M488 148 L524 169 L524 211 L488 232 L452 211 L452 169 Z"/>
    <path d="M562 190 L598 211 L598 253 L562 274 L526 253 L526 211 Z"/>

    <path d="M44 274 L80 295 L80 337 L44 358 L8 337 L8 295 Z"/>
    <path d="M118 316 L154 337 L154 379 L118 400 L82 379 L82 337 Z"/>
    <path d="M192 274 L228 295 L228 337 L192 358 L156 337 L156 295 Z"/>
    <path d="M266 316 L302 337 L302 379 L266 400 L230 379 L230 337 Z"/>
    <path d="M340 274 L376 295 L376 337 L340 358 L304 337 L304 295 Z"/>
    <path d="M414 316 L450 337 L450 379 L414 400 L378 379 L378 337 Z"/>
    <path d="M488 274 L524 295 L524 337 L488 358 L452 337 L452 295 Z"/>
    <path d="M562 316 L598 337 L598 379 L562 400 L526 379 L526 337 Z"/>

    <path d="M44 400 L80 421 L80 463 L44 484 L8 463 L8 421 Z"/>
    <path d="M118 442 L154 463 L154 505 L118 526 L82 505 L82 463 Z"/>
    <path d="M192 400 L228 421 L228 463 L192 484 L156 463 L156 421 Z"/>
    <path d="M266 442 L302 463 L302 505 L266 526 L230 505 L230 463 Z"/>
    <path d="M340 400 L376 421 L376 463 L340 484 L304 463 L304 421 Z"/>
    <path d="M414 442 L450 463 L450 505 L414 526 L378 505 L378 463 Z"/>
    <path d="M488 400 L524 421 L524 463 L488 484 L452 463 L452 421 Z"/>
    <path d="M562 442 L598 463 L598 505 L562 526 L526 505 L526 463 Z"/>
  </g>

  <!-- Angular right-side corporate accent -->
  <path d="M918 0 H1280 V720 H756 Z" fill="url(#accentGrad)" filter="url(#softShadow)"/>
  <path d="M1048 0 H1280 V232 L970 158 Z" fill="url(#facetGrad)" opacity="0.75"/>
  <path d="M1280 416 V720 H890 L1016 585 Z" fill="#922B24" opacity="0.34"/>
  <path d="M1142 86 L1280 122 V312 L1062 236 Z" fill="#FFFFFF" opacity="0.08"/>
  <path d="M845 0 L918 0 L756 720 L690 720 Z" fill="#2F2F2F" opacity="0.055"/>

  <!-- Fine diagonal highlights on the color block -->
  <path d="M1014 72 L1280 148" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.22"/>
  <path d="M952 218 L1280 316" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.16"/>
  <path d="M880 610 L1280 488" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.18"/>

  <!-- Left content zone -->
  <text x="86" y="122" width="650" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600" fill="#D34B32" letter-spacing="2">
    CORPORATE SYSTEMS PRESENTATION
  </text>

  <text x="84" y="202" width="660" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="800" fill="#333333">
    <tspan x="84" dy="0">MODERN CORPORATE</tspan>
    <tspan x="84" dy="62">TEMPLATE STYLE</tspan>
  </text>

  <rect x="86" y="330" width="142" height="7" rx="3.5" fill="#D34B32"/>

  <text x="86" y="384" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="400" fill="#666666">
    <tspan x="86" dy="0">A structured white workspace with a geometric mesh,</tspan>
    <tspan x="86" dy="34">strong angular framing, and a high-contrast brand accent.</tspan>
    <tspan x="86" dy="34">Ideal for executive summaries, data stories, and B2B decks.</tspan>
  </text>

  <!-- Small editable metric chips for chart/data layouts -->
  <g>
    <rect x="86" y="535" width="156" height="72" rx="12" fill="#FFFFFF" stroke="#E8E8E8" stroke-width="1.2"/>
    <text x="108" y="566" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#888888">REVENUE</text>
    <text x="108" y="594" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#333333">+18%</text>

    <rect x="268" y="535" width="156" height="72" rx="12" fill="#FFFFFF" stroke="#E8E8E8" stroke-width="1.2"/>
    <text x="290" y="566" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#888888">PIPELINE</text>
    <text x="290" y="594" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#333333">$42M</text>

    <rect x="450" y="535" width="156" height="72" rx="12" fill="#FFFFFF" stroke="#E8E8E8" stroke-width="1.2"/>
    <text x="472" y="566" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#888888">REGIONS</text>
    <text x="472" y="594" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#333333">24</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for the hex mesh; draw repeated editable `<path>` hexagons instead.
- ❌ `clip-path` on the angular color blocks; use direct polygon-like `<path>` shapes.
- ❌ Overly dark geometric mesh lines that compete with body copy or charts.
- ❌ Center-aligned typography; the design depends on a strong left content axis.
- ❌ `marker-end` arrows on paths for data callouts; use native `<line>` arrows only if arrows are needed.

## Composition notes
- Keep roughly 60–65% of the slide as a white content zone on the left; reserve the right 35–40% for the angled brand block.
- The title should sit in the upper-left quadrant with generous breathing room and a short accent divider beneath it.
- The hex mesh should be visible enough to texture the canvas but light enough to disappear behind charts and text.
- Repeat the accent color sparingly in labels, dividers, and small metrics so the right-side block feels integrated rather than decorative.