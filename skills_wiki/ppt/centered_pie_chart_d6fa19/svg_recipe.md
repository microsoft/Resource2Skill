# SVG Recipe — Centered Pie Chart with Bottom Legend

## Visual mechanism
A clean proportional-data slide built around a large centered pie chart, with each wedge separated by crisp white gutters and a structured legend anchored in a rounded card along the bottom. The composition keeps the chart as the visual focus while the bottom legend provides readable category mapping and exact percentages.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 1× `<radialGradient>` for a soft stage-light backdrop behind the chart
- 4× `<linearGradient>` for premium pie-slice fills
- 1× `<filter id="softShadow">` applied to background cards and chart base
- 1× `<filter id="glow">` applied to the subtle halo behind the pie
- 1× `<ellipse>` for the pie chart ground shadow
- 1× `<circle>` for the pie chart base ring / halo
- 4× `<path>` for editable pie slices
- 1× `<circle>` for the center highlight cap
- 1× `<rect>` for the bottom legend container
- 4× `<rect>` for legend color chips
- 8× `<text>` for legend labels and percentages
- 2× `<text>` for headline and subtitle
- 4× `<line>` for subtle legend dividers

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="50%" cy="40%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#F4F7FB"/>
      <stop offset="100%" stop-color="#E8EEF7"/>
    </radialGradient>

    <linearGradient id="sliceBlue" x1="520" y1="170" x2="760" y2="440">
      <stop offset="0%" stop-color="#4F8DFF"/>
      <stop offset="100%" stop-color="#1F5FD6"/>
    </linearGradient>
    <linearGradient id="sliceCyan" x1="710" y1="250" x2="500" y2="440">
      <stop offset="0%" stop-color="#37D5E8"/>
      <stop offset="100%" stop-color="#009EBD"/>
    </linearGradient>
    <linearGradient id="sliceViolet" x1="540" y1="420" x2="500" y2="190">
      <stop offset="0%" stop-color="#B17CFF"/>
      <stop offset="100%" stop-color="#6846D9"/>
    </linearGradient>
    <linearGradient id="sliceAmber" x1="550" y1="190" x2="700" y2="160">
      <stop offset="0%" stop-color="#FFC75A"/>
      <stop offset="100%" stop-color="#F08A24"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="20"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>

  <text x="120" y="78" width="1040" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#14213D" text-anchor="middle">
    Revenue Mix by Customer Segment
  </text>
  <text x="120" y="114" width="1040" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#65758B" text-anchor="middle">
    FY2026 planning baseline · percentage of total contracted revenue
  </text>

  <ellipse cx="640" cy="334" rx="190" ry="38" fill="#8DA2C7" opacity="0.18" filter="url(#glow)"/>
  <circle cx="640" cy="315" r="170" fill="#FFFFFF" opacity="0.85" filter="url(#softShadow)"/>

  <path d="M 640 315 L 640 165 A 150 150 0 0 1 742.7 424.4 Z"
        fill="url(#sliceBlue)" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 640 315 L 742.7 424.4 A 150 150 0 0 1 518.6 403.2 Z"
        fill="url(#sliceCyan)" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 640 315 L 518.6 403.2 A 150 150 0 0 1 518.6 226.8 Z"
        fill="url(#sliceViolet)" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 640 315 L 518.6 226.8 A 150 150 0 0 1 640 165 Z"
        fill="url(#sliceAmber)" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round"/>

  <circle cx="640" cy="315" r="46" fill="#FFFFFF" opacity="0.94"/>
  <text x="595" y="307" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#14213D" text-anchor="middle">
    100%
  </text>
  <text x="585" y="330" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#718096" text-anchor="middle">
    total mix
  </text>

  <rect x="118" y="548" width="1044" height="112" rx="28" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
  <line x1="380" y1="574" x2="380" y2="634" stroke="#E3EAF4" stroke-width="1"/>
  <line x1="640" y1="574" x2="640" y2="634" stroke="#E3EAF4" stroke-width="1"/>
  <line x1="900" y1="574" x2="900" y2="634" stroke="#E3EAF4" stroke-width="1"/>

  <rect x="168" y="590" width="18" height="18" rx="5" fill="url(#sliceBlue)"/>
  <text x="198" y="588" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#172033">Enterprise</text>
  <text x="198" y="616" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#1F5FD6">38%</text>

  <rect x="428" y="590" width="18" height="18" rx="5" fill="url(#sliceCyan)"/>
  <text x="458" y="588" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#172033">SMB</text>
  <text x="458" y="616" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#009EBD">27%</text>

  <rect x="688" y="590" width="18" height="18" rx="5" fill="url(#sliceViolet)"/>
  <text x="718" y="588" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#172033">Consumer</text>
  <text x="718" y="616" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#6846D9">20%</text>

  <rect x="948" y="590" width="18" height="18" rx="5" fill="url(#sliceAmber)"/>
  <text x="978" y="588" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#172033">Public Sector</text>
  <text x="978" y="616" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#F08A24">15%</text>
</svg>
```

## Avoid in this skill
- ❌ Don’t use `<canvas>`, embedded chart screenshots, or non-editable raster pies; draw each wedge as an editable `<path>`.
- ❌ Don’t use `<textPath>` for curved labels around the pie; it will not translate reliably.
- ❌ Don’t place `clip-path` on the pie slices or legend shapes; clipping is only reliable for `<image>` elements.
- ❌ Don’t use `marker-end` for any legend callout arrows; if callouts are needed, use explicit `<line>` elements and simple triangle `<path>` arrowheads.
- ❌ Don’t omit `width` on `<text>`; PowerPoint will render text boxes unpredictably.

## Composition notes
- Keep the pie centered horizontally and slightly above center vertically, leaving a strong lower band for the legend.
- Use generous negative space around the chart; the legend card should feel anchored, not crowded.
- Match each legend chip directly to the wedge gradient family, but use darker solid text colors for readable percentages.
- For low-density executive slides, use 4–6 slices maximum; more categories should be grouped into “Other” or moved to a bar chart.