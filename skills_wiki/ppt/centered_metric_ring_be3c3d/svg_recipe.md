# SVG Recipe — Centered Metric Ring

## Visual mechanism
A single oversized metric sits at the exact visual center, encircled by layered concentric rings: a muted base ring, a bright gradient progress arc, dashed calibration ticks, and soft glow halos. Sparse headline/subtitle text frames the metric without competing with it, creating a premium dashboard-divider feel.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× `<radialGradient>` / `<linearGradient>` for background depth, ring stroke, and central badge fill
- 2× `<filter>` for soft shadow and luminous glow applied to circles, paths, and text
- 4× `<circle>` for central badge, base ring, dashed outer ring, and inner hairline ring
- 4× `<path>` for gradient progress arcs and small decorative orbital accents
- 6× `<text>` for headline, subtitle, central metric, metric label, and small ring annotations
- 2× `<line>` for subtle horizontal divider accents beside the subtitle

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="52%" stop-color="#0B1C33"/>
      <stop offset="100%" stop-color="#101827"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="48%" r="50%">
      <stop offset="0%" stop-color="#2EE6D6" stop-opacity="0.32"/>
      <stop offset="48%" stop-color="#2186FF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#07111F" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="ringGrad" x1="460" y1="220" x2="820" y2="520">
      <stop offset="0%" stop-color="#7CF7E8"/>
      <stop offset="42%" stop-color="#35A7FF"/>
      <stop offset="100%" stop-color="#8A5CFF"/>
    </linearGradient>

    <linearGradient id="badgeGrad" x1="535" y1="250" x2="745" y2="470">
      <stop offset="0%" stop-color="#132C4E"/>
      <stop offset="100%" stop-color="#07111F"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="640" cy="360" r="300" fill="url(#centerGlow)"/>

  <path d="M100 116 C220 54 325 68 418 136 C302 142 205 188 126 274 C86 226 70 172 100 116 Z"
        fill="#153456" opacity="0.28"/>
  <path d="M1114 494 C1040 622 905 636 810 586 C922 558 1008 502 1068 410 C1116 420 1144 450 1114 494 Z"
        fill="#25315F" opacity="0.26"/>

  <text x="0" y="86" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700"
        fill="#F5FAFF" letter-spacing="0.5">
    Quarterly Growth Signal
  </text>

  <line x1="428" y1="120" x2="515" y2="120" stroke="#2EE6D6" stroke-width="2" opacity="0.55"/>
  <line x1="765" y1="120" x2="852" y2="120" stroke="#8A5CFF" stroke-width="2" opacity="0.55"/>

  <text x="340" y="126" width="600" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="400"
        fill="#9FB3C8" letter-spacing="1.6">
    EXECUTIVE KPI HIGHLIGHT · LOW-DENSITY METRIC VIEW
  </text>

  <circle cx="640" cy="360" r="215" fill="none" stroke="#233A58" stroke-width="1.5"
          stroke-dasharray="4 13" opacity="0.9"/>
  <circle cx="640" cy="360" r="178" fill="none" stroke="#1D314C" stroke-width="34" opacity="0.85"/>
  <circle cx="640" cy="360" r="124" fill="none" stroke="#304962" stroke-width="1.4" opacity="0.7"/>

  <path d="M640 182 A178 178 0 1 1 480 438"
        fill="none" stroke="url(#ringGrad)" stroke-width="34" stroke-linecap="round"
        filter="url(#cyanGlow)"/>
  <path d="M640 182 A178 178 0 1 1 480 438"
        fill="none" stroke="url(#ringGrad)" stroke-width="22" stroke-linecap="round"/>

  <path d="M818 360 A178 178 0 0 1 793 451"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.85"/>
  <path d="M474 296 A178 178 0 0 1 512 236"
        fill="none" stroke="#2EE6D6" stroke-width="5" stroke-linecap="round" opacity="0.8"/>

  <circle cx="640" cy="360" r="112" fill="url(#badgeGrad)" stroke="#375B7D" stroke-width="1.5"
          filter="url(#softShadow)"/>
  <circle cx="640" cy="360" r="96" fill="none" stroke="#2EE6D6" stroke-width="1"
          stroke-dasharray="2 8" opacity="0.38"/>

  <text x="470" y="352" width="340" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="82" font-weight="800"
        fill="#FFFFFF" letter-spacing="-3" filter="url(#softShadow)">
    72%
  </text>
  <text x="500" y="397" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="600"
        fill="#8FEFE8" letter-spacing="2.4">
    ADOPTION LIFT
  </text>

  <text x="302" y="364" width="210" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600"
        fill="#7F93AA" letter-spacing="1.5">
    BASELINE
  </text>
  <text x="768" y="364" width="210" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600"
        fill="#7F93AA" letter-spacing="1.5">
    TARGET RANGE
  </text>

  <text x="270" y="642" width="740" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="400"
        fill="#DCE7F3">
    A focused metric moment for section dividers, investor updates, or dashboard summaries.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the ring with `<mask>` or clipped non-image shapes; use stroked circles and arc paths instead.
- ❌ Do not use `<textPath>` for labels around the ring; PowerPoint translation will drop it. Keep labels as normal horizontal text.
- ❌ Do not apply filters to `<line>` elements; use unfiltered divider lines or convert glowing accents into `<path>` arcs.
- ❌ Do not overcrowd the center with multiple metrics; the visual depends on one dominant number.

## Composition notes
- Keep the metric locked to the slide center; the ring should occupy roughly 45–55% of slide height.
- Place headline/subtitle in the top 15–20% of the canvas and keep the lower caption short.
- Use dark negative space around the ring so glow, dashed ticks, and gradient arcs feel premium rather than busy.
- Color rhythm works best with one cool gradient arc, muted blue-gray support rings, and white metric typography.