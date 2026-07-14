# SVG Recipe — Hierarchical Sunburst Breakdown

## Visual mechanism
A hierarchical sunburst breakdown uses concentric donut-ring wedges where each outer level only appears over the selected parent wedge. The viewer sees the total context in the inner ring, then follows one highlighted branch outward into progressively finer subcomponents.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 1× `<rect>` for a subtle left-side legend panel
- 10× `<path>` for editable donut wedges across three concentric hierarchy levels
- 1× `<circle>` for the central hole / KPI label plate
- 1× `<filter id="softShadow">` applied to the legend panel and center circle
- 1× `<filter id="wedgeGlow">` applied to selected outer wedges for premium depth
- 4× `<rect>` for legend color swatches
- 5× `<line>` for divider accents and outer callout leader lines
- 20+× `<text>` elements for title, subtitle, percentages, legend labels, and callouts
- 1× `<radialGradient>` for the central plate fill
- 1× `<linearGradient>` for a faint analytical backdrop accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FAF7EF"/>
      <stop offset="100%" stop-color="#EEF2F5"/>
    </linearGradient>

    <radialGradient id="centerPlate" cx="45%" cy="40%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#E8EDF0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="wedgeGlow" x="-12%" y="-12%" width="124%" height="124%">
      <feGaussianBlur stdDeviation="3" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="70" y="74" width="610" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="700" fill="#26323A">
    Figure 3. Share and Breakdown of Heat Demand
  </text>
  <text x="72" y="112" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#66737C">
    A selective sunburst isolates the industrial heat branch while preserving the full 100% context.
  </text>
  <line x1="72" y1="138" x2="410" y2="138" stroke="#D6A832" stroke-width="4"/>

  <rect x="70" y="205" width="330" height="292" rx="24" fill="#FFFFFF" opacity="0.88" filter="url(#softShadow)"/>
  <text x="104" y="250" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" letter-spacing="1.4" fill="#7B858C">
    PRIMARY DEMAND MIX
  </text>

  <rect x="106" y="286" width="18" height="18" rx="4" fill="#E5B82A"/>
  <text x="140" y="301" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#26323A">Industry heat</text>
  <text x="333" y="301" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#26323A">32%</text>

  <rect x="106" y="334" width="18" height="18" rx="4" fill="#3B5B75"/>
  <text x="140" y="349" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#26323A">Buildings</text>
  <text x="333" y="349" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#26323A">31%</text>

  <rect x="106" y="382" width="18" height="18" rx="4" fill="#885E8E"/>
  <text x="140" y="397" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#26323A">Transport</text>
  <text x="333" y="397" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#26323A">24%</text>

  <rect x="106" y="430" width="18" height="18" rx="4" fill="#85878A"/>
  <text x="140" y="445" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#26323A">Other use</text>
  <text x="333" y="445" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#26323A">13%</text>

  <text x="104" y="528" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#66737C">
    Outer rings are intentionally absent outside the selected 32% parent slice.
  </text>

  <!-- Level 1: full inner ring, total = 100% -->
  <path d="M 790 225 A 160 160 0 0 1 935.7 450.0 L 871.9 421.6 A 90 90 0 0 0 790 295 Z" fill="#E5B82A" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M 935.7 450.0 A 160 160 0 0 1 673.4 494.6 L 724.4 446.7 A 90 90 0 0 0 871.9 421.6 Z" fill="#3B5B75" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M 673.4 494.6 A 160 160 0 0 1 673.4 275.4 L 724.4 323.3 A 90 90 0 0 0 724.4 446.7 Z" fill="#885E8E" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M 673.4 275.4 A 160 160 0 0 1 790 225 L 790 295 A 90 90 0 0 0 724.4 323.3 Z" fill="#85878A" stroke="#FFFFFF" stroke-width="3"/>

  <!-- Level 2: only the 32% parent branch is decomposed; remainder is omitted -->
  <path d="M 790 145 A 240 240 0 0 1 1029.5 369.9 L 957.7 374.4 A 168 168 0 0 0 790 217 Z" fill="#E68A2E" stroke="#FFFFFF" stroke-width="3" filter="url(#wedgeGlow)"/>
  <path d="M 1029.5 369.9 A 240 240 0 0 1 1007.2 487.2 L 942.0 456.6 A 168 168 0 0 0 957.7 374.4 Z" fill="#9E596E" stroke="#FFFFFF" stroke-width="3"/>

  <!-- Level 3: only the 24% heat branch is decomposed; remainder is omitted -->
  <path d="M 790 65 A 320 320 0 0 1 993.8 138.3 L 948.0 193.8 A 248 248 0 0 0 790 137 Z" fill="#4E77B8" stroke="#FFFFFF" stroke-width="3" filter="url(#wedgeGlow)"/>
  <path d="M 993.8 138.3 A 320 320 0 0 1 1079.6 248.7 L 1014.5 279.4 A 248 248 0 0 0 948.0 193.8 Z" fill="#E38D34" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M 1079.6 248.7 A 320 320 0 0 1 1104.3 325.1 L 1033.6 338.6 A 248 248 0 0 0 1014.5 279.4 Z" fill="#B3B4B8" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M 1104.3 325.1 A 320 320 0 0 1 1109.4 364.9 L 1037.5 369.4 A 248 248 0 0 0 1033.6 338.6 Z" fill="#9EBC4B" stroke="#FFFFFF" stroke-width="3"/>

  <circle cx="790" cy="385" r="76" fill="url(#centerPlate)" filter="url(#softShadow)"/>
  <text x="735" y="372" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" text-anchor="middle" fill="#6A747A">TOTAL</text>
  <text x="735" y="405" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" text-anchor="middle" fill="#26323A">100%</text>

  <text x="852" y="323" width="88" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" text-anchor="middle" fill="#FFFFFF">32%</text>
  <text x="778" y="514" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" text-anchor="middle" fill="#FFFFFF">31%</text>
  <text x="632" y="391" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" text-anchor="middle" fill="#FFFFFF">24%</text>
  <text x="706" y="275" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" text-anchor="middle" fill="#FFFFFF">13%</text>

  <text x="884" y="235" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" text-anchor="middle" fill="#FFFFFF">
    <tspan x="932" dy="0">24%</tspan><tspan x="932" dy="23">Heat</tspan>
  </text>
  <text x="954" y="421" width="86" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" text-anchor="middle" fill="#FFFFFF">
    <tspan x="997" dy="0">8%</tspan><tspan x="997" dy="20">Elec.</tspan>
  </text>

  <text x="846" y="123" width="86" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" text-anchor="middle" fill="#FFFFFF">11%</text>
  <text x="980" y="213" width="76" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" text-anchor="middle" fill="#FFFFFF">7%</text>

  <line x1="1098" y1="288" x2="1160" y2="262" stroke="#6D747A" stroke-width="2"/>
  <text x="1170" y="267" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#424A50">Oil 4%</text>

  <line x1="1110" y1="348" x2="1160" y2="356" stroke="#6D747A" stroke-width="2"/>
  <text x="1170" y="362" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#424A50">Renew. 2%</text>

  <line x1="888" y1="106" x2="930" y2="72" stroke="#6D747A" stroke-width="2"/>
  <text x="940" y="77" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#424A50">Coal</text>

  <line x1="1016" y1="182" x2="1082" y2="146" stroke="#6D747A" stroke-width="2"/>
  <text x="1092" y="151" width="128" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#424A50">Natural gas</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use an embedded chart screenshot if editability is required; draw each wedge as a native `<path>`.
- ❌ Do not draw invisible outer-ring “remainder” wedges with white strokes; omitted segments should truly disappear so the drill-down branch is visually isolated.
- ❌ Do not use `<mask>` or clip paths on wedge shapes; donut segments should be explicit compound arc paths.
- ❌ Do not use `marker-end` for callout arrows; use plain `<line>` leaders and place text manually.
- ❌ Do not rely on auto-sized text; every `<text>` element needs an explicit `width` attribute for predictable PowerPoint rendering.

## Composition notes
- Put the sunburst slightly right of center and let it occupy roughly 55–60% of the slide width; the chart needs room for outer callouts.
- Reserve the left third for title, explanation, and the level-1 legend so the concentric rings remain uncluttered.
- Use a restrained neutral background with saturated categorical wedges; the selected hierarchy should be the most colorful area on the slide.
- Align all hierarchy levels to the same 12 o’clock start angle so the viewer can immediately see which parent slice is being decomposed.