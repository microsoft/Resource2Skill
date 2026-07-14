# SVG Recipe — Dynamic KPI Slicer Dashboard

## Visual mechanism
A static SVG snapshot mimics a Power BI/Excel measure slicer: pill-shaped KPI tabs sit above a minimalist bar chart, with one highlighted tab driving the visible chart metric. The dashboard feels “dynamic” by pairing selected-state styling, a master-measure formula card, and refreshed-looking data labels directly on the bars.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark executive dashboard background
- 2× `<path>` for soft abstract background ribbons / glow shapes
- 1× large rounded `<rect>` for the main dashboard card
- 3× rounded `<rect>` for KPI slicer buttons, with one selected accent state
- 5× `<path>` for rounded-top column bars
- 5× faint `<rect>` or `<path>` for comparison/ghost bar tracks behind the active bars
- 5× `<text>` for data labels above bars
- 5× `<text>` for category labels below bars
- Multiple `<line>` elements for the chart baseline and subtle grid ticks
- 1× rounded `<rect>` formula card showing the disconnected slicer + SWITCH measure concept
- 2× `<line>` plus small `<path>` triangles for cause/effect arrows
- 1× `<linearGradient>` for the selected KPI tab
- 1× `<linearGradient>` for active bars
- 1× `<radialGradient>` for background glow
- 1× `<filter id="softShadow">` applied to cards and tabs
- 1× `<filter id="barGlow">` applied to selected chart bars

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#101827"/>
      <stop offset="58%" stop-color="#172033"/>
      <stop offset="100%" stop-color="#0A0F1C"/>
    </linearGradient>
    <radialGradient id="glow" cx="28%" cy="18%" r="70%">
      <stop offset="0%" stop-color="#FFE08A" stop-opacity="0.28"/>
      <stop offset="42%" stop-color="#4EA5FF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#0A0F1C" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="selectedTab" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFE66D"/>
      <stop offset="100%" stop-color="#FFB800"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4EA5FF"/>
      <stop offset="100%" stop-color="#64748B"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="barGlow" x="-30%" y="-30%" width="160%" height="170%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#glow)"/>

  <path d="M-80,620 C140,510 250,670 460,565 C700,445 820,520 1010,405 C1140,325 1230,330 1370,250 L1370,720 L-80,720 Z"
        fill="#23304A" opacity="0.36"/>
  <path d="M910,85 C1010,25 1150,30 1265,95 C1190,112 1105,150 1040,210 C985,260 920,245 875,195 C840,155 850,118 910,85 Z"
        fill="#FFCC33" opacity="0.12"/>

  <text x="64" y="66" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F8FAFC">
    Company Performance
  </text>
  <text x="66" y="98" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94A3B8">
    KPI slicer controls which measure is rendered in the same chart frame
  </text>

  <rect x="62" y="128" width="900" height="520" rx="30" fill="#F8FAFC" opacity="0.98" filter="url(#softShadow)"/>
  <rect x="86" y="153" width="852" height="86" rx="22" fill="#EEF2F7"/>
  <text x="110" y="184" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#334155">
    Select measure
  </text>

  <rect x="108" y="198" width="210" height="40" rx="20" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="133" y="224" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#64748B">
    Number of Orders
  </text>

  <rect x="334" y="198" width="190" height="40" rx="20" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="370" y="224" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#64748B">
    Product Count
  </text>

  <rect x="540" y="191" width="220" height="54" rx="27" fill="url(#selectedTab)" filter="url(#softShadow)"/>
  <text x="585" y="224" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#1E293B">
    Quantity Sold
  </text>
  <circle cx="734" cy="218" r="5" fill="#1E293B"/>

  <rect x="785" y="198" width="126" height="40" rx="20" fill="#E2E8F0"/>
  <text x="813" y="224" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#475569">
    Refresh
  </text>

  <text x="106" y="285" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#0F172A">
    Quantity Sold by Company
  </text>
  <text x="106" y="308" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">
    Value axis removed; precise values are shown as data labels
  </text>

  <line x1="120" y1="580" x2="900" y2="580" stroke="#CBD5E1" stroke-width="2"/>
  <line x1="120" y1="500" x2="900" y2="500" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="120" y1="420" x2="900" y2="420" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="120" y1="340" x2="900" y2="340" stroke="#E2E8F0" stroke-width="1"/>

  <rect x="172" y="330" width="88" height="250" rx="14" fill="#E2E8F0"/>
  <rect x="315" y="330" width="88" height="250" rx="14" fill="#E2E8F0"/>
  <rect x="458" y="330" width="88" height="250" rx="14" fill="#E2E8F0"/>
  <rect x="601" y="330" width="88" height="250" rx="14" fill="#E2E8F0"/>
  <rect x="744" y="330" width="88" height="250" rx="14" fill="#E2E8F0"/>

  <path d="M172,580 L172,312 Q172,294 190,294 L242,294 Q260,294 260,312 L260,580 Z" fill="url(#barGrad)" filter="url(#barGlow)"/>
  <path d="M315,580 L315,356 Q315,340 331,340 L387,340 Q403,340 403,356 L403,580 Z" fill="url(#barGrad)" opacity="0.92"/>
  <path d="M458,580 L458,480 Q458,466 472,466 L532,466 Q546,466 546,480 L546,580 Z" fill="url(#barGrad)" opacity="0.84"/>
  <path d="M601,580 L601,484 Q601,470 615,470 L675,470 Q689,470 689,484 L689,580 Z" fill="url(#barGrad)" opacity="0.78"/>
  <path d="M744,580 L744,508 Q744,494 758,494 L818,494 Q832,494 832,508 L832,580 Z" fill="url(#barGrad)" opacity="0.70"/>

  <text x="183" y="281" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" text-anchor="middle" fill="#0F172A">3,350</text>
  <text x="326" y="327" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" text-anchor="middle" fill="#0F172A">2,770</text>
  <text x="469" y="453" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" text-anchor="middle" fill="#0F172A">1,260</text>
  <text x="612" y="457" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" text-anchor="middle" fill="#0F172A">1,240</text>
  <text x="755" y="481" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" text-anchor="middle" fill="#0F172A">940</text>

  <text x="156" y="615" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#334155">Bold Night</text>
  <text x="299" y="615" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#334155">Urban Right</text>
  <text x="442" y="615" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#334155">Meta Creations</text>
  <text x="585" y="615" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#334155">Lucas Basics</text>
  <text x="728" y="615" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#334155">Pina Lina</text>

  <rect x="995" y="150" width="225" height="170" rx="24" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
  <text x="1020" y="184" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#0F172A">
    Disconnected KPI Table
  </text>
  <text x="1020" y="216" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">• Number of Orders</text>
  <text x="1020" y="242" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">• Product Count</text>
  <text x="1020" y="268" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#B77900">• Quantity Sold</text>

  <rect x="995" y="365" width="225" height="190" rx="24" fill="#111827" filter="url(#softShadow)"/>
  <text x="1020" y="398" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#F8FAFC">
    Master Measure
  </text>
  <text x="1020" y="430" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">KPI Value =</text>
  <text x="1020" y="456" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#93C5FD">SWITCH( selected KPI,</text>
  <text x="1034" y="482" width="168" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FDE68A">"Quantity Sold", SUM(Qty),</text>
  <text x="1034" y="508" width="168" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">"Orders", COUNT(OrderID) )</text>

  <line x1="962" y1="220" x2="995" y2="220" stroke="#FBBF24" stroke-width="3"/>
  <path d="M995,220 L982,212 L982,228 Z" fill="#FBBF24"/>
  <line x1="1107" y1="320" x2="1107" y2="365" stroke="#FBBF24" stroke-width="3"/>
  <path d="M1107,365 L1099,351 L1115,351 Z" fill="#FBBF24"/>

  <rect x="995" y="586" width="225" height="42" rx="21" fill="#1E293B" stroke="#334155"/>
  <text x="1021" y="613" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#E2E8F0">
    One chart, many KPIs
  </text>
</svg>
```

## Avoid in this skill
- ❌ Real slicer interactivity or DAX execution; SVG/PPT shapes should show a static selected-state snapshot only
- ❌ PowerPoint-native chart objects if the goal is fully editable custom styling; draw bars, labels, and axes as SVG shapes
- ❌ Overcrowded dashboards with multiple charts; this technique depends on one chart frame changing measure context
- ❌ Tiny slicer tabs with low contrast; the selected KPI must be obvious at presentation distance
- ❌ `<foreignObject>` for formula/code blocks; use regular `<text>` lines instead

## Composition notes
- Keep the slicer directly above the chart so the audience reads it as the control surface for the visual below.
- Reserve the right side for a compact “data model logic” explanation; this makes the static slide communicate the dynamic mechanism.
- Remove the value axis and lean on large data labels to preserve the clean dashboard look.
- Use a restrained neutral chart palette with one strong accent color for the active KPI tab and linkage arrows.