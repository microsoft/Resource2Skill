# SVG Recipe — Interactive KPI Performance Dashboard

## Visual mechanism
A polished executive dashboard frame simulates an interactive KPI view: visual filter controls define the current state, while the main chart compares actual performance bars against a target line over time. The “interactivity” is represented as a static selected state, using highlighted pills, dropdown styling, a slider thumb, and dynamic chart/table labels.

## SVG primitives needed
- 1× full-slide `<rect>` for the neutral dashboard background
- 2× decorative `<path>` blobs for premium ambient depth
- 2× `<linearGradient>` fills for background and primary header/control surfaces
- 1× `<radialGradient>` for soft accent glow
- 1× `<filter id="cardShadow">` applied to dashboard cards
- 1× `<filter id="softGlow">` applied to selected controls and key dots
- Multiple `<rect>` cards for header, control panel, chart panel, KPI chips, dropdowns, slider, and data table rows
- 3× rounded `<rect>` department pills to simulate radio/filter selection
- 7× `<rect>` bars for actual KPI values
- 1× stroked `<path>` for the target line chart
- 7× `<circle>` markers for target data points
- Multiple `<line>` elements for chart gridlines, axes, and slider ticks
- Multiple `<text>` elements with explicit `width` for titles, labels, values, axis labels, legends, and table cells
- Small `<path>` icons for dropdown caret, chart trend cue, and selected-state decoration

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" font-family="Segoe UI, Microsoft YaHei, sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7f9fc"/>
      <stop offset="100%" stop-color="#eef3f8"/>
    </linearGradient>
    <linearGradient id="headerBlue" x1="36" y1="24" x2="1244" y2="156">
      <stop offset="0%" stop-color="#1f5fae"/>
      <stop offset="55%" stop-color="#2f7ed8"/>
      <stop offset="100%" stop-color="#173b75"/>
    </linearGradient>
    <linearGradient id="selectedGreen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#25d06f"/>
      <stop offset="100%" stop-color="#078d46"/>
    </linearGradient>
    <radialGradient id="glowGold" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffc400" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#ffc400" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.05 0 0 0 0 0.12 0 0 0 0 0.24 0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M1020 0 C1135 25 1238 96 1280 188 L1280 0 Z" fill="#dcecff"/>
  <path d="M0 610 C90 590 160 635 210 720 L0 720 Z" fill="#d9f4e5"/>
  <circle cx="1110" cy="108" r="92" fill="url(#glowGold)" opacity="0.55"/>

  <rect x="36" y="24" width="1208" height="132" rx="30" fill="url(#headerBlue)" filter="url(#cardShadow)"/>
  <text x="70" y="68" width="560" font-size="31" font-weight="700" fill="#ffffff">Interactive KPI Performance Dashboard</text>
  <text x="72" y="103" width="600" font-size="15" fill="#dcecff">Static selected state: Finance department · Pramod Bhavsar · rolling seven-year view</text>
  <rect x="760" y="52" width="128" height="72" rx="18" fill="#ffffff" opacity="0.16"/>
  <text x="782" y="79" width="90" font-size="13" fill="#dcecff">ACTUAL</text>
  <text x="782" y="112" width="90" font-size="30" font-weight="700" fill="#ffffff">5.12K</text>
  <rect x="908" y="52" width="128" height="72" rx="18" fill="#ffffff" opacity="0.16"/>
  <text x="930" y="79" width="90" font-size="13" fill="#dcecff">TARGET</text>
  <text x="930" y="112" width="90" font-size="30" font-weight="700" fill="#ffffff">5.46K</text>
  <rect x="1056" y="52" width="150" height="72" rx="18" fill="#ffffff" opacity="0.16"/>
  <path d="M1082 105 L1096 91 L1110 99 L1130 72" fill="none" stroke="#ffc400" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="1144" y="82" width="48" font-size="13" fill="#dcecff">GAP</text>
  <text x="1144" y="113" width="48" font-size="25" font-weight="700" fill="#ffffff">-6%</text>

  <rect x="36" y="180" width="300" height="500" rx="28" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="66" y="222" width="230" font-size="18" font-weight="700" fill="#172033">FILTER CONTROLS</text>
  <text x="66" y="253" width="230" font-size="12" font-weight="700" fill="#7c8798">DEPARTMENT</text>
  <rect x="66" y="267" width="220" height="42" rx="21" fill="url(#selectedGreen)" filter="url(#softGlow)"/>
  <circle cx="88" cy="288" r="8" fill="#ffffff"/>
  <text x="106" y="294" width="150" font-size="14" font-weight="700" fill="#ffffff">Finance</text>
  <rect x="66" y="320" width="220" height="42" rx="21" fill="#eef3f8"/>
  <circle cx="88" cy="341" r="8" fill="#c4ceda"/>
  <text x="106" y="347" width="150" font-size="14" font-weight="700" fill="#536174">Operation</text>
  <rect x="66" y="373" width="220" height="42" rx="21" fill="#eef3f8"/>
  <circle cx="88" cy="394" r="8" fill="#c4ceda"/>
  <text x="106" y="400" width="150" font-size="14" font-weight="700" fill="#536174">HR</text>

  <text x="66" y="452" width="230" font-size="12" font-weight="700" fill="#7c8798">EMPLOYEE NAME</text>
  <rect x="66" y="466" width="220" height="48" rx="13" fill="#f8fafc" stroke="#d7e0ea" stroke-width="1.5"/>
  <text x="84" y="496" width="160" font-size="15" font-weight="600" fill="#172033">Pramod Bhavsar</text>
  <path d="M260 485 L272 485 L266 494 Z" fill="#536174"/>

  <text x="66" y="552" width="230" font-size="12" font-weight="700" fill="#7c8798">YEAR WINDOW</text>
  <line x1="82" y1="582" x2="270" y2="582" stroke="#d7e0ea" stroke-width="6" stroke-linecap="round"/>
  <line x1="120" y1="582" x2="240" y2="582" stroke="#2f7ed8" stroke-width="6" stroke-linecap="round"/>
  <circle cx="120" cy="582" r="13" fill="#ffffff" stroke="#2f7ed8" stroke-width="5"/>
  <circle cx="240" cy="582" r="13" fill="#ffffff" stroke="#2f7ed8" stroke-width="5"/>
  <text x="66" y="619" width="70" font-size="13" fill="#536174">2018</text>
  <text x="226" y="619" width="70" font-size="13" fill="#536174">2024</text>
  <rect x="66" y="636" width="220" height="24" rx="12" fill="#e9f6ee"/>
  <text x="88" y="653" width="178" font-size="12" font-weight="700" fill="#078d46">ACTIVE FILTER APPLIED</text>

  <rect x="360" y="180" width="884" height="500" rx="28" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="398" y="226" width="450" font-size="23" font-weight="700" fill="#172033">Performance Review: Pramod Bhavsar</text>
  <text x="398" y="252" width="510" font-size="14" fill="#6b7687">Actual KPI score vs target benchmark, by year</text>
  <rect x="952" y="208" width="92" height="28" rx="14" fill="#eaf2ff"/>
  <rect x="1060" y="208" width="92" height="28" rx="14" fill="#fff0ee"/>
  <rect x="966" y="218" width="14" height="8" rx="2" fill="#2f7ed8"/>
  <text x="986" y="228" width="48" font-size="12" font-weight="600" fill="#536174">Actual</text>
  <circle cx="1076" cy="222" r="5" fill="#c0504d"/>
  <text x="1088" y="228" width="50" font-size="12" font-weight="600" fill="#536174">Target</text>

  <line x1="440" y1="300" x2="1175" y2="300" stroke="#edf1f6" stroke-width="1"/>
  <line x1="440" y1="360" x2="1175" y2="360" stroke="#edf1f6" stroke-width="1"/>
  <line x1="440" y1="420" x2="1175" y2="420" stroke="#edf1f6" stroke-width="1"/>
  <line x1="440" y1="480" x2="1175" y2="480" stroke="#edf1f6" stroke-width="1"/>
  <line x1="440" y1="540" x2="1175" y2="540" stroke="#edf1f6" stroke-width="1"/>
  <line x1="440" y1="585" x2="1175" y2="585" stroke="#bac7d6" stroke-width="1.5"/>
  <line x1="440" y1="285" x2="440" y2="585" stroke="#bac7d6" stroke-width="1.5"/>

  <text x="392" y="305" width="36" font-size="11" fill="#7c8798">900</text>
  <text x="392" y="365" width="36" font-size="11" fill="#7c8798">750</text>
  <text x="392" y="425" width="36" font-size="11" fill="#7c8798">600</text>
  <text x="392" y="485" width="36" font-size="11" fill="#7c8798">450</text>
  <text x="398" y="545" width="30" font-size="11" fill="#7c8798">300</text>

  <rect x="485" y="420" width="42" height="165" rx="8" fill="#2f7ed8"/>
  <rect x="585" y="388" width="42" height="197" rx="8" fill="#2f7ed8"/>
  <rect x="685" y="405" width="42" height="180" rx="8" fill="#2f7ed8"/>
  <rect x="785" y="348" width="42" height="237" rx="8" fill="#2f7ed8"/>
  <rect x="885" y="370" width="42" height="215" rx="8" fill="#2f7ed8"/>
  <rect x="985" y="318" width="42" height="267" rx="8" fill="#2f7ed8"/>
  <rect x="1085" y="333" width="42" height="252" rx="8" fill="#2f7ed8"/>

  <path d="M506 430 L606 398 L706 384 L806 340 L906 356 L1006 310 L1106 295" fill="none" stroke="#c0504d" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="506" cy="430" r="7" fill="#c0504d" stroke="#ffffff" stroke-width="3"/>
  <circle cx="606" cy="398" r="7" fill="#c0504d" stroke="#ffffff" stroke-width="3"/>
  <circle cx="706" cy="384" r="7" fill="#c0504d" stroke="#ffffff" stroke-width="3"/>
  <circle cx="806" cy="340" r="7" fill="#c0504d" stroke="#ffffff" stroke-width="3"/>
  <circle cx="906" cy="356" r="7" fill="#c0504d" stroke="#ffffff" stroke-width="3"/>
  <circle cx="1006" cy="310" r="7" fill="#c0504d" stroke="#ffffff" stroke-width="3"/>
  <circle cx="1106" cy="295" r="7" fill="#c0504d" stroke="#ffffff" stroke-width="3"/>

  <text x="485" y="612" width="50" font-size="12" fill="#536174">2018</text>
  <text x="585" y="612" width="50" font-size="12" fill="#536174">2019</text>
  <text x="685" y="612" width="50" font-size="12" fill="#536174">2020</text>
  <text x="785" y="612" width="50" font-size="12" fill="#536174">2021</text>
  <text x="885" y="612" width="50" font-size="12" fill="#536174">2022</text>
  <text x="985" y="612" width="50" font-size="12" fill="#536174">2023</text>
  <text x="1085" y="612" width="50" font-size="12" fill="#536174">2024</text>

  <rect x="398" y="638" width="230" height="24" rx="12" fill="#f8fafc"/>
  <text x="418" y="655" width="190" font-size="12" fill="#536174">Best year: 2023 · 890 actual</text>
  <rect x="646" y="638" width="250" height="24" rx="12" fill="#f8fafc"/>
  <text x="666" y="655" width="210" font-size="12" fill="#536174">Target gap closed in 4 of 7 years</text>
  <rect x="914" y="638" width="250" height="24" rx="12" fill="#fff6e0"/>
  <text x="934" y="655" width="210" font-size="12" font-weight="700" fill="#9a6500">Review focus: 2024 shortfall</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use actual HTML form elements, `<foreignObject>`, or embedded Excel controls; represent interactivity as editable SVG/PPT shapes.
- ❌ Do not rely on animation or scripted hover/click behavior; create one static “selected state” per slide, or duplicate slides for multiple states.
- ❌ Do not use `marker-end` on chart trend paths; if arrows are needed, build arrowheads manually with small `<path>` shapes.
- ❌ Do not apply filters to `<line>` gridlines or axes; shadows/glows should be applied only to cards, circles, rects, paths, or text.
- ❌ Avoid overcrowding the chart with every raw data label; reserve labels for selected callouts, summaries, and axis context.

## Composition notes
- Give the chart panel roughly 70% of the slide width; the control panel should feel important but secondary.
- Use a strong blue header/control rhythm, one green selected-state accent, and one red/orange target line for instant semantic clarity.
- Keep gridlines pale and thin so the bars and target line remain the visual focus.
- Treat faux controls like presentation objects: selected pills, dropdowns, and sliders should be readable from the back of the room.