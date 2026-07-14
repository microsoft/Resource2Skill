# SVG Recipe — Focused Metric Doughnut Slide

## Visual mechanism
A single oversized doughnut progress ring dominates the slide, framing an extra-large KPI value in the center. A rotated sidebar accent and sparse headline copy create a premium executive dashboard feel without competing with the metric.

## SVG primitives needed
- 2× `<rect>` for the full-slide background and rotated sidebar rail
- 3× `<path>` for soft background sweep shapes and the active doughnut arc
- 2× `<circle>` for the inactive doughnut track and endpoint accent
- 6× `<text>` for headline, subtitle, central metric, KPI label, footnote, and rotated sidebar text
- 2× `<linearGradient>` for the sidebar and active doughnut stroke
- 1× `<radialGradient>` for the subtle center glow
- 2× `<filter>` definitions: one soft shadow for the doughnut card/glow elements, one blur glow for the active KPI arc

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgSweep" x1="120" y1="80" x2="1180" y2="690" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#EAF2FF" stop-opacity="0.95"/>
      <stop offset="0.52" stop-color="#F7FAFF" stop-opacity="0.35"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="sidebarGrad" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#1E3A8A"/>
      <stop offset="0.55" stop-color="#2563EB"/>
      <stop offset="1" stop-color="#22D3EE"/>
    </linearGradient>

    <linearGradient id="ringGrad" x1="520" y1="190" x2="920" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#22D3EE"/>
      <stop offset="0.45" stop-color="#2563EB"/>
      <stop offset="1" stop-color="#7C3AED"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="0.62" stop-color="#F4F8FF" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#E7EEF9" stop-opacity="0.15"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="arcGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8FAFC"/>

  <path d="M 136 0 C 310 78, 320 206, 520 235 C 776 272, 883 105, 1160 0 L 1280 0 L 1280 720 L 1086 720 C 1020 610, 916 552, 750 575 C 540 604, 407 688, 182 625 C 72 594, 25 519, 0 438 L 0 0 Z"
        fill="url(#bgSweep)"/>

  <path d="M 890 54 C 1030 98, 1146 202, 1198 338 C 1245 463, 1220 588, 1130 720 L 1280 720 L 1280 0 L 1016 0 C 975 15, 933 31, 890 54 Z"
        fill="#DBEAFE" opacity="0.42"/>

  <rect x="-72" y="0" width="138" height="720" fill="url(#sidebarGrad)"/>
  <rect x="42" y="-80" width="16" height="880" rx="8" fill="#FFFFFF" opacity="0.22" transform="rotate(-8 50 360)"/>

  <text x="96" y="112" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3" fill="#2563EB">
    EXECUTIVE KPI
  </text>

  <text x="96" y="174" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" font-weight="800" fill="#0F172A">
    Conversion Momentum
  </text>

  <text x="98" y="218" width="450" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400" fill="#64748B">
    Q4 funnel efficiency against annual operating target
  </text>

  <text x="68" y="612" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="2.6" fill="#FFFFFF"
        transform="rotate(-90 68 612)">
    NORTH AMERICA · DIGITAL SALES
  </text>

  <circle cx="730" cy="365" r="218" fill="url(#centerGlow)" filter="url(#softShadow)"/>
  <circle cx="730" cy="365" r="190" fill="none" stroke="#E2E8F0" stroke-width="54"/>

  <path d="M 730 175 A 190 190 0 1 1 543.4 329.4"
        fill="none" stroke="#93C5FD" stroke-width="64" stroke-linecap="round"
        opacity="0.28" filter="url(#arcGlow)"/>

  <path d="M 730 175 A 190 190 0 1 1 543.4 329.4"
        fill="none" stroke="url(#ringGrad)" stroke-width="54" stroke-linecap="round"/>

  <circle cx="543.4" cy="329.4" r="16" fill="#FFFFFF" stroke="#7C3AED" stroke-width="7"/>

  <text x="590" y="324" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="90" font-weight="800" text-anchor="middle" fill="#0F172A"
        transform="translate(140 0)">
    78%
  </text>

  <text x="590" y="366" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="2.5" text-anchor="middle" fill="#2563EB"
        transform="translate(140 0)">
    TARGET ATTAINMENT
  </text>

  <text x="590" y="420" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="400" text-anchor="middle" fill="#64748B"
        transform="translate(140 0)">
    +12 pts versus prior quarter
  </text>

  <rect x="970" y="520" width="210" height="76" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="998" y="552" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.8" fill="#64748B">
    RUN RATE
  </text>
  <text x="998" y="582" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#0F172A">
    $42.8M
  </text>
</svg>
```

## Avoid in this skill
- ❌ Building the doughnut from raster images; use editable circles and arc paths so the ring can be recolored in PowerPoint.
- ❌ Adding many small dashboard widgets around the KPI; this layout works because the metric has visual priority.
- ❌ Using `<mask>` to hollow out the doughnut; use stroked circles/paths with large stroke widths instead.
- ❌ Applying filters to `<line>` elements; if callouts are added, keep shadows on rects, circles, paths, or text only.
- ❌ Omitting `width` on text; PowerPoint will not reliably preserve the intended text box sizing.

## Composition notes
- Keep the doughnut slightly right of center, leaving the left third for headline and context.
- Use a low-density layout: one hero metric, one subtitle, and at most one small supporting stat.
- The rotated sidebar should feel like a brand/navigation accent, not a content column.
- Let the active arc carry the strongest color; background shapes should stay pale and atmospheric.