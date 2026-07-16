# SVG Recipe — Sub-Zero Axis Annotation

## Visual mechanism
Shift the visual zero-baseline upward by reserving a “sub-zero” annotation band beneath the columns, then place category icons and short labels inside that band. The viewer reads each icon as structurally attached to its column group rather than as a separate legend.

## SVG primitives needed
- 1× `<image>` for the full-bleed thematic background photo
- 2× `<rect>` for dark overlay and translucent chart panel
- 14× `<rect>` for clustered column bars, two per category
- 1× `<rect>` for the semi-transparent sub-zero annotation tray
- 5× `<line>` for horizontal chart gridlines and zero baseline
- 7× `<line>` for faint vertical category guides connecting icons to columns
- 7× `<text>` for y-axis tick labels
- 7× `<text>` for category labels in the sub-zero region
- 2× `<text>` for title and subtitle
- 2× `<text>` plus 2× small `<rect>` swatches for legend
- Multiple `<path>`, `<circle>`, and `<ellipse>` elements for monochrome category icons
- 2× `<linearGradient>` for premium bar fills
- 1× `<filter id="softShadow">` applied to chart panel and bars
- 1× `<filter id="glow">` applied to the zero baseline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="maleBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4757FF"/>
      <stop offset="100%" stop-color="#11194F"/>
    </linearGradient>
    <linearGradient id="femaleBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FF6A91"/>
      <stop offset="100%" stop-color="#D91F5D"/>
    </linearGradient>
    <linearGradient id="panelGlass" x1="0" y1="110" x2="0" y2="600">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.05"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-20%" y="-200%" width="140%" height="500%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.example.com/hero/blurred-fitness-studio-cycling-yoga-1920x1080.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="#3023AE" opacity="0.76"/>
  <rect x="0" y="0" width="1280" height="720" fill="#07112F" opacity="0.34"/>

  <text x="76" y="68" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#FFFFFF">Participation by Activity</text>
  <text x="78" y="101" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#DDE2FF" opacity="0.9">Axis minimum extended below zero to create a native annotation lane for category icons.</text>

  <rect x="94" y="120" width="1092" height="500" rx="28" fill="url(#panelGlass)" stroke="#FFFFFF" stroke-opacity="0.24" filter="url(#softShadow)"/>
  <rect x="150" y="473" width="1030" height="82" rx="18" fill="#090F35" opacity="0.52"/>

  <line x1="150" y1="145" x2="1180" y2="145" stroke="#FFFFFF" stroke-opacity="0.24" stroke-dasharray="4 8"/>
  <line x1="150" y1="227" x2="1180" y2="227" stroke="#FFFFFF" stroke-opacity="0.18" stroke-dasharray="4 8"/>
  <line x1="150" y1="309" x2="1180" y2="309" stroke="#FFFFFF" stroke-opacity="0.18" stroke-dasharray="4 8"/>
  <line x1="150" y1="391" x2="1180" y2="391" stroke="#FFFFFF" stroke-opacity="0.18" stroke-dasharray="4 8"/>
  <line x1="150" y1="473" x2="1180" y2="473" stroke="#FFFFFF" stroke-width="2.4" stroke-opacity="0.82" filter="url(#glow)"/>

  <text x="107" y="150" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.82" text-anchor="end">80%</text>
  <text x="107" y="232" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.72" text-anchor="end">60%</text>
  <text x="107" y="314" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.72" text-anchor="end">40%</text>
  <text x="107" y="396" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.72" text-anchor="end">20%</text>
  <text x="107" y="478" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" font-weight="700" text-anchor="end">0%</text>

  <line x1="220" y1="145" x2="220" y2="555" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="355" y1="145" x2="355" y2="555" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="490" y1="145" x2="490" y2="555" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="625" y1="145" x2="625" y2="555" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="760" y1="145" x2="760" y2="555" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="895" y1="145" x2="895" y2="555" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="1030" y1="145" x2="1030" y2="555" stroke="#FFFFFF" stroke-opacity="0.08"/>

  <rect x="188" y="288" width="26" height="185" rx="7" fill="url(#maleBar)" filter="url(#softShadow)"/>
  <rect x="218" y="247" width="26" height="226" rx="7" fill="url(#femaleBar)" filter="url(#softShadow)"/>
  <rect x="323" y="219" width="26" height="254" rx="7" fill="url(#maleBar)" filter="url(#softShadow)"/>
  <rect x="353" y="317" width="26" height="156" rx="7" fill="url(#femaleBar)" filter="url(#softShadow)"/>
  <rect x="458" y="321" width="26" height="152" rx="7" fill="url(#maleBar)" filter="url(#softShadow)"/>
  <rect x="488" y="215" width="26" height="258" rx="7" fill="url(#femaleBar)" filter="url(#softShadow)"/>
  <rect x="593" y="358" width="26" height="115" rx="7" fill="url(#maleBar)" filter="url(#softShadow)"/>
  <rect x="623" y="178" width="26" height="295" rx="7" fill="url(#femaleBar)" filter="url(#softShadow)"/>
  <rect x="728" y="202" width="26" height="271" rx="7" fill="url(#maleBar)" filter="url(#softShadow)"/>
  <rect x="758" y="334" width="26" height="139" rx="7" fill="url(#femaleBar)" filter="url(#softShadow)"/>
  <rect x="863" y="153" width="26" height="320" rx="7" fill="url(#maleBar)" filter="url(#softShadow)"/>
  <rect x="893" y="383" width="26" height="90" rx="7" fill="url(#femaleBar)" filter="url(#softShadow)"/>
  <rect x="998" y="334" width="26" height="139" rx="7" fill="url(#maleBar)" filter="url(#softShadow)"/>
  <rect x="1028" y="202" width="26" height="271" rx="7" fill="url(#femaleBar)" filter="url(#softShadow)"/>

  <g stroke="#FFFFFF" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.95">
    <g transform="translate(220 508)"><path d="M-22 8 C-10 -22 16 -20 22 2"/><circle cx="-11" cy="13" r="7"/><circle cx="15" cy="13" r="7"/><path d="M-3 -4 L8 6"/></g>
    <g transform="translate(355 508)"><circle cx="-14" cy="14" r="8"/><circle cx="15" cy="14" r="8"/><path d="M-14 14 L-2 -8 L13 14 M-2 -8 L9 -8 M-2 -8 L-8 14"/></g>
    <g transform="translate(490 508)"><path d="M-18 16 C-4 -12 4 -12 18 16"/><path d="M-10 -1 C-3 8 4 8 11 -1"/><circle cx="0" cy="-17" r="7"/></g>
    <g transform="translate(625 508)"><path d="M-18 20 C-4 3 4 3 18 20"/><path d="M0 2 L0 -21 M0 -21 C-13 -16 -19 -7 -19 4 M0 -21 C13 -16 19 -7 19 4"/></g>
    <g transform="translate(760 508)"><path d="M-22 12 L-12 12 M12 12 L22 12 M-12 4 L12 4 M-12 20 L12 20"/><path d="M-12 0 L-12 24 M12 0 L12 24"/></g>
    <g transform="translate(895 508)"><circle cx="0" cy="3" r="20"/><path d="M-16 -8 C-5 2 5 2 16 -8 M-18 8 C-5 -2 5 -2 18 8"/></g>
    <g transform="translate(1030 508)"><path d="M-22 15 C-9 -6 9 -6 22 15"/><path d="M-10 3 L0 -18 L10 3 M-2 -5 L8 -5"/></g>
  </g>

  <text x="175" y="584" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" text-anchor="middle">Run</text>
  <text x="310" y="584" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" text-anchor="middle">Cycle</text>
  <text x="445" y="584" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" text-anchor="middle">Dance</text>
  <text x="580" y="584" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" text-anchor="middle">Yoga</text>
  <text x="715" y="584" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" text-anchor="middle">Weights</text>
  <text x="850" y="584" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" text-anchor="middle">Ball</text>
  <text x="985" y="584" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" text-anchor="middle">Stretch</text>

  <rect x="902" y="75" width="18" height="18" rx="5" fill="url(#maleBar)"/>
  <text x="930" y="90" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF">Male %</text>
  <rect x="1018" y="75" width="18" height="18" rx="5" fill="url(#femaleBar)"/>
  <text x="1046" y="90" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF">Female %</text>
</svg>
```

## Avoid in this skill
- ❌ Do not place icons in a detached legend; the entire point is direct alignment beneath each category.
- ❌ Do not let the bars extend into the annotation lane; the zero baseline must visibly separate data from labels/icons.
- ❌ Do not use dense multi-line category labels in the sub-zero band; they will compete with the icons.
- ❌ Do not use `<marker-end>` arrows or `<textPath>` for axis decoration; keep the annotation band simple and editable.

## Composition notes
- Reserve roughly 15–20% of the chart plot height below the zero baseline for the sub-zero annotation tray.
- Keep the title and legend outside the plot area so the chart can dominate the slide.
- Use strong color contrast: subdued background, white axis/icon treatment, and saturated bar colors.
- Align every icon to the center of its column cluster; this alignment is the visual “lock” that makes the technique work.