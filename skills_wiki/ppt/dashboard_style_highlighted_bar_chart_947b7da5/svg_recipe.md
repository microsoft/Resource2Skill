# SVG Recipe — Dashboard-Style Highlighted Bar Chart

## Visual mechanism
A dark executive-dashboard canvas frames a minimalist bar chart where most bars are muted gray and one key bar is saturated with a bright accent color. Sparse gridlines, glowing value labels, dashed comparison guides, and a directional annotation turn the chart from “data display” into a focused data story.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 1× `<rect>` for the soft chart panel surface
- 5× `<rect>` for vertical bars, with one highlighted in the accent color
- 5× `<rect>` for subtle rounded “cap” overlays at the top of each bar
- 6× `<line>` for horizontal gridlines and baseline
- 2× `<line>` for dashed comparison guide lines
- 1× `<path>` for the curved dashed trend annotation
- 1× `<path>` for a custom arrowhead triangle
- 1× `<rect>` for the highlighted KPI callout pill
- Multiple `<text>` elements with explicit `width` for title, axis labels, category labels, values, and annotation copy
- 1× `<linearGradient>` for the background
- 1× `<linearGradient>` for the highlighted bar fill
- 1× `<radialGradient>` for a soft ambient glow behind the highlighted bar
- 2× `<filter>` definitions: one shadow for panel/bars, one glow for the accent highlight

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#101820"/>
      <stop offset="58%" stop-color="#1F1F1F"/>
      <stop offset="100%" stop-color="#111318"/>
    </linearGradient>

    <linearGradient id="accentBar" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#E36F12"/>
      <stop offset="55%" stop-color="#F7941D"/>
      <stop offset="100%" stop-color="#FFBF55"/>
    </linearGradient>

    <radialGradient id="accentAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F7941D" stop-opacity="0.35"/>
      <stop offset="65%" stop-color="#F7941D" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#F7941D" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="785" cy="365" r="235" fill="url(#accentAura)"/>

  <text x="72" y="68" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">
    Annual City PM2.5 Average Ranking
  </text>
  <text x="74" y="105" width="690" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#AAB2BD">
    Dark dashboard view with one priority city isolated for executive attention
  </text>

  <rect x="92" y="132" width="1096" height="505" rx="28" fill="#20242B" opacity="0.92" filter="url(#softShadow)"/>
  <rect x="92" y="132" width="1096" height="505" rx="28" fill="none" stroke="#333A44" stroke-width="1.2"/>

  <text x="126" y="177" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#F4F6F8">
    Average annual concentration, μg/m³
  </text>
  <text x="952" y="177" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8E98A6" text-anchor="end">
    Ranked sample cities
  </text>

  <line x1="140" y1="190" x2="1090" y2="190" stroke="#414852" stroke-width="1"/>
  <line x1="140" y1="290" x2="1090" y2="290" stroke="#3B424C" stroke-width="1"/>
  <line x1="140" y1="390" x2="1090" y2="390" stroke="#3B424C" stroke-width="1"/>
  <line x1="140" y1="490" x2="1090" y2="490" stroke="#3B424C" stroke-width="1"/>
  <line x1="140" y1="590" x2="1090" y2="590" stroke="#59616D" stroke-width="1.4"/>
  <line x1="140" y1="150" x2="140" y2="590" stroke="#4B535E" stroke-width="1.2"/>

  <text x="102" y="196" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E98A6" text-anchor="end">160</text>
  <text x="102" y="296" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E98A6" text-anchor="end">120</text>
  <text x="102" y="396" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E98A6" text-anchor="end">80</text>
  <text x="102" y="496" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E98A6" text-anchor="end">40</text>
  <text x="102" y="596" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E98A6" text-anchor="end">0</text>

  <line x1="140" y1="390" x2="255" y2="390" stroke="#B8BEC7" stroke-width="1.2" stroke-dasharray="6 7" opacity="0.65"/>
  <line x1="140" y1="284" x2="435" y2="284" stroke="#B8BEC7" stroke-width="1.2" stroke-dasharray="6 7" opacity="0.65"/>
  <text x="154" y="373" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DDE2E8">City A: 80.0</text>
  <text x="154" y="267" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DDE2E8">City B: 122.6</text>

  <rect x="210" y="390" width="90" height="200" rx="12" fill="#A9AFB7" opacity="0.82"/>
  <rect x="210" y="390" width="90" height="18" rx="9" fill="#D3D7DC" opacity="0.28"/>
  <text x="205" y="369" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF" text-anchor="middle">80.0</text>
  <text x="205" y="624" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DCE1E7" text-anchor="middle">City A</text>

  <rect x="390" y="284" width="90" height="306" rx="12" fill="#A9AFB7" opacity="0.82"/>
  <rect x="390" y="284" width="90" height="18" rx="9" fill="#D3D7DC" opacity="0.28"/>
  <text x="385" y="263" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF" text-anchor="middle">122.6</text>
  <text x="385" y="624" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DCE1E7" text-anchor="middle">City B</text>

  <rect x="570" y="272" width="90" height="318" rx="12" fill="#A9AFB7" opacity="0.82"/>
  <rect x="570" y="272" width="90" height="18" rx="9" fill="#D3D7DC" opacity="0.28"/>
  <text x="565" y="251" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF" text-anchor="middle">127.2</text>
  <text x="565" y="624" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DCE1E7" text-anchor="middle">City C</text>

  <rect x="750" y="226" width="90" height="364" rx="12" fill="url(#accentBar)" filter="url(#accentGlow)"/>
  <rect x="750" y="226" width="90" height="18" rx="9" fill="#FFE1A1" opacity="0.45"/>
  <text x="745" y="203" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFB64B" text-anchor="middle">145.6</text>
  <text x="745" y="624" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFB64B" text-anchor="middle">City D</text>

  <rect x="930" y="356" width="90" height="234" rx="12" fill="#A9AFB7" opacity="0.82"/>
  <rect x="930" y="356" width="90" height="18" rx="9" fill="#D3D7DC" opacity="0.28"/>
  <text x="925" y="335" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF" text-anchor="middle">93.4</text>
  <text x="925" y="624" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DCE1E7" text-anchor="middle">City E</text>

  <path d="M620 246 C680 205, 716 195, 780 216" fill="none" stroke="#F7941D" stroke-width="3" stroke-linecap="round" stroke-dasharray="9 8"/>
  <path d="M778 216 L757 207 L765 230 Z" fill="#F7941D"/>

  <rect x="858" y="215" width="230" height="78" rx="22" fill="#2B241B" stroke="#F7941D" stroke-width="1.4"/>
  <text x="882" y="245" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFB64B">
    Highest exposure
  </text>
  <text x="882" y="271" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#F3E5D0">
    +18.4 vs. City C, requiring immediate action
  </text>

  <text x="92" y="679" width="880" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#717B88">
    Source: Environmental monitoring sample dataset · Highlight color intentionally reserved for the primary insight.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Exporting the chart as a single screenshot; build bars, labels, gridlines, and annotations as editable SVG shapes.
- ❌ Using a bright color for every bar; the technique depends on one isolated accent point.
- ❌ Heavy axis frames, dense tick labels, or multicolor legends that compete with the highlighted bar.
- ❌ Applying `filter` to `<line>` gridlines or annotation lines; keep filters on bars, panels, paths, or text only.
- ❌ Using `marker-end` on a curved `<path>` for the arrow; draw the arrowhead as a separate editable `<path>` triangle.

## Composition notes
- Keep the chart panel large, centered, and low-clutter; the highlighted bar should sit near the visual center-right where it can carry the story.
- Use dark charcoal/navy surfaces with low-contrast gridlines, then reserve orange, green, or cyan for exactly one important bar and its annotation.
- Place title and subtitle above the panel; keep axis/category labels small so the data labels and callout remain dominant.
- Add one narrative device only — a dashed comparison line, curved trend arrow, or KPI callout — to avoid turning the slide into a crowded dashboard.