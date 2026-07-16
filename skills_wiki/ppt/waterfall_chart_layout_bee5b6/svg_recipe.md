# SVG Recipe — Waterfall Chart Layout

## Visual mechanism
A full-slide executive chart layout with a dominant headline and a large centered waterfall chart, using floating bars, dashed step connectors, muted gridlines, and strong color semantics for positive/negative movements. The design reads as a polished financial bridge: calm background, white chart stage, restrained labels, and one accent callout to highlight the key variance.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<path>` for a subtle decorative background sweep
- 1× `<rect>` for the main chart card with shadow
- 6× `<line>` for horizontal gridlines
- 1× `<line>` for the chart baseline axis
- 7× `<line>` for dashed waterfall step connectors
- 8× `<rect>` for waterfall bars: start/end totals, positive bars, and negative bars
- 8× `<rect>` for soft category label pills below the x-axis
- 1× `<rect>` for the highlighted insight callout
- Multiple `<text>` elements with explicit `width` for title, subtitle, axis labels, bar values, category labels, and callout copy
- 4× `<linearGradient>` for background, total bars, positive bars, negative bars, and the insight callout
- 1× `<filter id="cardShadow">` applied to the chart card
- 1× `<filter id="barShadow">` applied to bars for subtle depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>
    <linearGradient id="totalGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#245BFF"/>
      <stop offset="100%" stop-color="#123B9E"/>
    </linearGradient>
    <linearGradient id="posGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#20C997"/>
      <stop offset="100%" stop-color="#0B8F6A"/>
    </linearGradient>
    <linearGradient id="negGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FF8A65"/>
      <stop offset="100%" stop-color="#D94E36"/>
    </linearGradient>
    <linearGradient id="calloutGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#102A56"/>
      <stop offset="100%" stop-color="#1F4E8C"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="barShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M880,0 C1040,54 1130,155 1280,142 L1280,0 Z" fill="#DCE8F6" opacity="0.65"/>
  <path d="M0,640 C155,585 250,690 408,630 C516,589 585,610 660,720 L0,720 Z" fill="#E6EEF8" opacity="0.55"/>

  <text x="72" y="64" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#122033">
    FY25 margin bridge: growth tailwinds offset by churn and operating drag
  </text>
  <text x="74" y="102" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#64748B">
    Waterfall view, USD millions; totals shown as ending run-rate margin contribution
  </text>

  <rect x="1110" y="54" width="98" height="30" rx="15" fill="#EAF1FF"/>
  <text x="1128" y="75" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#245BFF">BOARD</text>

  <rect x="70" y="132" width="1140" height="510" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="108" y="176" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1E293B">
    Margin contribution bridge
  </text>
  <text x="108" y="201" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7B8794">
    Step connectors show the running cumulative contribution after each driver
  </text>

  <rect x="896" y="160" width="256" height="72" rx="18" fill="url(#calloutGrad)"/>
  <text x="920" y="188" width="212" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">
    Net impact: +$20M
  </text>
  <text x="920" y="212" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#C9DAF4">
    Efficiency program nearly neutralizes churn, COGS, and Opex pressure.
  </text>

  <line x1="122" y1="530" x2="1158" y2="530" stroke="#E6EAF0" stroke-width="1"/>
  <line x1="122" y1="470" x2="1158" y2="470" stroke="#E6EAF0" stroke-width="1"/>
  <line x1="122" y1="410" x2="1158" y2="410" stroke="#E6EAF0" stroke-width="1"/>
  <line x1="122" y1="350" x2="1158" y2="350" stroke="#E6EAF0" stroke-width="1"/>
  <line x1="122" y1="290" x2="1158" y2="290" stroke="#E6EAF0" stroke-width="1"/>
  <line x1="122" y1="230" x2="1158" y2="230" stroke="#E6EAF0" stroke-width="1"/>
  <line x1="122" y1="590" x2="1158" y2="590" stroke="#B8C2CF" stroke-width="1.5"/>

  <text x="86" y="535" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">100</text>
  <text x="86" y="475" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">200</text>
  <text x="86" y="415" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">300</text>
  <text x="86" y="355" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">400</text>
  <text x="86" y="295" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">500</text>
  <text x="86" y="235" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">600</text>

  <line x1="215" y1="338" x2="275" y2="338" stroke="#AAB6C6" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="345" y1="272" x2="405" y2="272" stroke="#AAB6C6" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="475" y1="239" x2="535" y2="239" stroke="#AAB6C6" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="605" y1="281" x2="665" y2="281" stroke="#AAB6C6" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="735" y1="308" x2="795" y2="308" stroke="#AAB6C6" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="865" y1="356" x2="925" y2="356" stroke="#AAB6C6" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="995" y1="326" x2="1055" y2="326" stroke="#AAB6C6" stroke-width="1.5" stroke-dasharray="5 5"/>

  <rect x="145" y="338" width="70" height="252" rx="8" fill="url(#totalGrad)" filter="url(#barShadow)"/>
  <rect x="275" y="272" width="70" height="66" rx="8" fill="url(#posGrad)" filter="url(#barShadow)"/>
  <rect x="405" y="239" width="70" height="33" rx="8" fill="url(#posGrad)" filter="url(#barShadow)"/>
  <rect x="535" y="239" width="70" height="42" rx="8" fill="url(#negGrad)" filter="url(#barShadow)"/>
  <rect x="665" y="281" width="70" height="27" rx="8" fill="url(#negGrad)" filter="url(#barShadow)"/>
  <rect x="795" y="308" width="70" height="48" rx="8" fill="url(#negGrad)" filter="url(#barShadow)"/>
  <rect x="925" y="326" width="70" height="30" rx="8" fill="url(#posGrad)" filter="url(#barShadow)"/>
  <rect x="1055" y="326" width="70" height="264" rx="8" fill="url(#totalGrad)" filter="url(#barShadow)"/>

  <text x="180" y="323" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#123B9E" text-anchor="middle">$420</text>
  <text x="310" y="259" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0B8F6A" text-anchor="middle">+$110</text>
  <text x="440" y="226" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0B8F6A" text-anchor="middle">+$55</text>
  <text x="570" y="231" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#D94E36" text-anchor="middle">−$70</text>
  <text x="700" y="273" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#D94E36" text-anchor="middle">−$45</text>
  <text x="830" y="300" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#D94E36" text-anchor="middle">−$80</text>
  <text x="960" y="314" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0B8F6A" text-anchor="middle">+$50</text>
  <text x="1090" y="311" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#123B9E" text-anchor="middle">$440</text>

  <rect x="130" y="610" width="100" height="34" rx="17" fill="#F1F5F9"/>
  <rect x="260" y="610" width="100" height="34" rx="17" fill="#ECFDF5"/>
  <rect x="390" y="610" width="100" height="34" rx="17" fill="#ECFDF5"/>
  <rect x="520" y="610" width="100" height="34" rx="17" fill="#FFF1F0"/>
  <rect x="650" y="610" width="100" height="34" rx="17" fill="#FFF1F0"/>
  <rect x="780" y="610" width="100" height="34" rx="17" fill="#FFF1F0"/>
  <rect x="910" y="610" width="100" height="34" rx="17" fill="#ECFDF5"/>
  <rect x="1040" y="610" width="100" height="34" rx="17" fill="#F1F5F9"/>

  <text x="180" y="632" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#475569" text-anchor="middle">FY24 base</text>
  <text x="310" y="632" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">New logo</text>
  <text x="440" y="632" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Pricing</text>
  <text x="570" y="632" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#B42318" text-anchor="middle">Churn</text>
  <text x="700" y="632" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#B42318" text-anchor="middle">COGS</text>
  <text x="830" y="632" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#B42318" text-anchor="middle">Opex</text>
  <text x="960" y="632" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Efficiency</text>
  <text x="1090" y="632" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#475569" text-anchor="middle">FY25 plan</text>
</svg>
```

## Avoid in this skill
- ❌ Using only stacked rectangles without step connectors; it will read as a bar chart, not a waterfall bridge.
- ❌ Applying `filter` to connector `<line>` elements; shadows on lines are dropped, so keep connectors flat.
- ❌ Relying on `marker-end` arrows for movement direction; arrowheads may disappear, and waterfall charts do not need them.
- ❌ Dense y-axis labeling or heavy borders; the executive style depends on a clean chart stage and high data-to-ink ratio.
- ❌ Clipping non-image elements for bar shapes; use rounded `<rect>` bars directly.

## Composition notes
- Reserve the top 15–18% of the slide for a clear headline and concise subtitle; keep the chart dominant below.
- Place the chart card with generous side margins and a soft shadow so the analytical content feels premium rather than spreadsheet-like.
- Use strong semantic color rhythm: blue for opening/closing totals, green for positive drivers, red/orange for negative drivers.
- Keep value labels close to bars and category labels in soft pills below the baseline to reduce clutter while preserving scanability.