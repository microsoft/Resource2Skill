# SVG Recipe — Dynamic Asymmetric Overlap Layout

## Visual mechanism
A massive left-aligned headline anchors the slide while oversized, tilted layout blocks intrude from the right, creating asymmetric overlap and a strong z-axis. The composition uses a muted editorial panel over a dark stage, then guides the eye with a curved arrow and footer CTA line.

## SVG primitives needed
- 1× `<rect>` for the full dark background stage
- 1× `<path>` for the large asymmetric rounded editorial panel
- 4× `<rect>` for the rotated overlapping layout mockup blocks on the right
- 4× `<text>` for stacked headline, footer title, footer subtitle, and tiny accent symbols
- 2× `<line>` for top and bottom editorial rules
- 1× `<path>` for the curved white arrow body and arrowhead
- 2× `<filter>` definitions for soft shadow/depth on the panel and layout blocks
- 2× `<linearGradient>` definitions for subtle panel depth and stage vignette

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="stageGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2b2b2b"/>
      <stop offset="58%" stop-color="#181818"/>
      <stop offset="100%" stop-color="#101010"/>
    </linearGradient>

    <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#c8c8c8"/>
      <stop offset="62%" stop-color="#bcbcbc"/>
      <stop offset="100%" stop-color="#a9a9a9"/>
    </linearGradient>

    <filter id="panelShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blockShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feOffset dx="-8" dy="10"/>
      <feGaussianBlur stdDeviation="9"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#stageGrad)"/>

  <path filter="url(#panelShadow)"
        d="M50 15 H1232 Q1250 15 1258 29 L807 104 Q792 107 795 125 L893 705 H50 Q20 705 20 675 V45 Q20 15 50 15 Z"
        fill="url(#panelGrad)"/>

  <text x="51" y="64" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#111111">✣</text>
  <line x1="98" y1="53" x2="752" y2="53" stroke="#111111" stroke-width="3"/>

  <text x="62" y="233" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="138" font-weight="900" letter-spacing="-8" fill="#050505">Layout</text>
  <text x="62" y="388" width="650" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="138" font-weight="900" letter-spacing="-8" fill="#050505">Design</text>
  <text x="62" y="542" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="138" font-weight="900" letter-spacing="-8" fill="#050505">Pro</text>

  <path d="M416 490 C505 540 645 545 723 469 L687 447 L774 422 L755 511 L729 484 C646 565 510 566 416 490 Z"
        fill="#f5f5f5"/>

  <text x="63" y="621" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="800" fill="#111111">✣</text>
  <line x1="109" y1="607" x2="766" y2="607" stroke="#111111" stroke-width="3"/>

  <text x="64" y="658" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="900" letter-spacing="-2" fill="#101010">SATORI GRAPHICS 2K25</text>
  <text x="66" y="678" width="600" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="500" fill="#101010">Design your future today, and elevate your graphic design awareness</text>

  <rect x="795" y="77" width="500" height="123" rx="17" ry="17"
        transform="rotate(-8 1045 138)" fill="#151515" filter="url(#blockShadow)"/>

  <rect x="843" y="220" width="243" height="309" rx="17" ry="17"
        transform="rotate(-8 965 374)" fill="#151515" filter="url(#blockShadow)"/>

  <rect x="1082" y="197" width="243" height="309" rx="17" ry="17"
        transform="rotate(-8 1204 351)" fill="#151515" filter="url(#blockShadow)"/>

  <rect x="877" y="551" width="431" height="126" rx="17" ry="17"
        transform="rotate(-8 1092 614)" fill="#151515" filter="url(#blockShadow)"/>

  <path d="M1055 205 L1070 203 L1121 556 L1106 558 Z" fill="#151515"/>
  <rect x="1027" y="154" width="240" height="14" transform="rotate(-8 1147 161)" fill="#b9b9b9"/>
  <rect x="1115" y="493" width="153" height="14" transform="rotate(-8 1192 500)" fill="#b9b9b9"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `clip-path` on text or shape layers to fake overlaps; PPT-Master only preserves clipping reliably on images.
- ❌ Do not use `marker-end` for the curved arrow; draw the arrowhead as part of a filled `<path>`.
- ❌ Do not use `<mask>` to hide portions of the headline behind the tilted blocks; instead layer objects directly.
- ❌ Avoid centered title/image layouts; the effect depends on strong left-heavy typography balanced by a right-side invading object.
- ❌ Avoid thin or light headline weights; the headline must be dense enough for the overlap to feel intentional.

## Composition notes
- Keep the headline huge, left-aligned, and stacked; it should occupy roughly the left half of the canvas and feel cropped close to the margins.
- Place the overlapping graphic or layout mockup on the right third, rotated slightly so it breaks the static rectangular grid.
- Use a dark outer stage with a lighter asymmetric panel to create premium poster-like depth.
- Reserve the lower-left band for the closing CTA or brand lockup; the curved arrow can bridge the headline to the right-side visual.