# SVG Recipe — Industrial SCADA & IIoT Dashboard Layout

## Visual mechanism
A SCADA dashboard is built as a rigid operator-console interface: high-level circular KPI gauges across the top, a central machine/process schematic with status lights and tag callouts, and a dense real-time data grid at the bottom. The look depends on industrial greys, hard panel boundaries, small technical labels, and RAG status colors that pop against muted machinery.

## SVG primitives needed
- 1× `<rect>` full-slide background for the low-contrast industrial workspace
- 3× large rounded `<rect>` panels for KPI, process schematic, and tag grid zones
- 1× top application chrome made from `<rect>` and small `<text>` labels to mimic SCADA/HMI software
- 4× gauge widgets, each using 2× stroked `<circle>` rings plus 2× `<text>` labels
- Multiple `<rect>` elements for conveyor beds, machine cabinets, control blocks, product crates, table cells, and software UI panels
- Multiple `<line>` elements for pipes, sensor stems, conveyor rails, and grid dividers
- Multiple `<circle>` elements for LED status indicators, sensor heads, bearings, buttons, and alarm beacons
- Several `<path>` elements for mechanical silhouettes, robot-arm geometry, alarm beacon highlight, and small industrial icons
- 1× `<linearGradient>` for metallic panel/machine fills
- 1× `<radialGradient>` for LED glow styling
- 1× `<filter id="panelShadow">` applied to major panels and machine blocks
- 1× `<filter id="softGlow">` applied to active lights and warning states
- Nested `<tspan>` inside title/status text for inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#d8d8dc"/><stop offset="48%" stop-color="#aeb0b6"/><stop offset="100%" stop-color="#7d8088"/>
    </linearGradient>
    <linearGradient id="darkPanel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3e4248"/><stop offset="100%" stop-color="#22262b"/>
    </linearGradient>
    <radialGradient id="ledGreen" cx="35%" cy="30%" r="65%">
      <stop offset="0%" stop-color="#eafff3"/><stop offset="45%" stop-color="#2ecc71"/><stop offset="100%" stop-color="#087d3b"/>
    </radialGradient>
    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="3"/><feGaussianBlur stdDeviation="5"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#e7e7ec"/>
  <rect x="28" y="24" width="1224" height="672" rx="12" fill="#cfd0d6" stroke="#9ea1a8" filter="url(#panelShadow)"/>
  <rect x="28" y="24" width="1224" height="34" rx="12" fill="#f6f6f7"/>
  <rect x="28" y="50" width="1224" height="22" fill="#d9dadf"/>
  <text x="46" y="46" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333">PlantSuite HMI — <tspan font-weight="700">Production Line 01 / Live Status</tspan></text>
  <text x="48" y="66" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#555">File   Edit   View   Diagnostics   Trends   Tools   Help</text>

  <rect x="44" y="86" width="190" height="520" fill="#efeff2" stroke="#a4a6ad"/>
  <rect x="44" y="86" width="190" height="26" fill="#d4d6dc"/>
  <text x="56" y="104" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#30343a">Project Explorer</text>
  <text x="58" y="136" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#315d9a">▸ Line_01</text>
  <text x="76" y="157" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#444">● Conveyor</text>
  <text x="76" y="178" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#444">● Robot Cell</text>
  <text x="76" y="199" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#444">● Quality Gate</text>
  <rect x="54" y="222" width="170" height="118" fill="#ffffff" stroke="#c4c6cc"/>
  <rect x="54" y="222" width="170" height="22" fill="#293f78"/>
  <text x="62" y="237" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#fff">Alarms / Events</text>
  <circle cx="66" cy="262" r="5" fill="#e74c3c"/><text x="78" y="266" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#333">E-STOP cleared</text>
  <circle cx="66" cy="284" r="5" fill="#f1c40f"/><text x="78" y="288" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#333">Motor temp high</text>
  <circle cx="66" cy="306" r="5" fill="#2ecc71"/><text x="78" y="310" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#333">PLC online</text>

  <rect x="258" y="86" width="974" height="90" rx="8" fill="#bfc1c8" stroke="#9da0a7"/>
  <g font-family="Segoe UI, Microsoft YaHei">
    <g transform="translate(306 130)">
      <circle r="38" fill="none" stroke="#8e929a" stroke-width="11"/><circle r="38" fill="none" stroke="#2ecc71" stroke-width="11" stroke-dasharray="174 239" transform="rotate(-90)" filter="url(#softGlow)"/>
      <text x="-31" y="6" width="62" text-anchor="middle" font-size="22" font-weight="700" fill="#1f252b">73%</text><text x="-35" y="52" width="70" text-anchor="middle" font-size="11" fill="#4b5057">OEE</text>
    </g>
    <g transform="translate(414 130)">
      <circle r="38" fill="none" stroke="#8e929a" stroke-width="11"/><circle r="38" fill="none" stroke="#2ecc71" stroke-width="11" stroke-dasharray="234 239" transform="rotate(-90)" filter="url(#softGlow)"/>
      <text x="-31" y="6" width="62" text-anchor="middle" font-size="22" font-weight="700" fill="#1f252b">98%</text><text x="-42" y="52" width="84" text-anchor="middle" font-size="11" fill="#4b5057">QUALITY</text>
    </g>
    <g transform="translate(522 130)">
      <circle r="38" fill="none" stroke="#8e929a" stroke-width="11"/><circle r="38" fill="none" stroke="#f1c40f" stroke-width="11" stroke-dasharray="203 239" transform="rotate(-90)" filter="url(#softGlow)"/>
      <text x="-31" y="6" width="62" text-anchor="middle" font-size="22" font-weight="700" fill="#1f252b">85%</text><text x="-50" y="52" width="100" text-anchor="middle" font-size="11" fill="#4b5057">AVAILABILITY</text>
    </g>
    <g transform="translate(630 130)">
      <circle r="38" fill="none" stroke="#8e929a" stroke-width="11"/><circle r="38" fill="none" stroke="#2ecc71" stroke-width="11" stroke-dasharray="210 239" transform="rotate(-90)" filter="url(#softGlow)"/>
      <text x="-31" y="6" width="62" text-anchor="middle" font-size="22" font-weight="700" fill="#1f252b">88%</text><text x="-52" y="52" width="104" text-anchor="middle" font-size="11" fill="#4b5057">PERFORMANCE</text>
    </g>
  </g>
  <rect x="740" y="104" width="430" height="52" fill="#dfe0e4" stroke="#a8abb2"/>
  <text x="762" y="126" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#2b3036">RUN MODE: AUTO</text>
  <text x="762" y="148" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555">Shift B · 18,420 units · takt 4.8 sec · PLC S7-1500</text>
  <circle cx="1140" cy="130" r="13" fill="url(#ledGreen)" filter="url(#softGlow)"/>

  <rect x="258" y="194" width="974" height="300" rx="8" fill="#d5d6db" stroke="#9da0a7"/>
  <text x="278" y="220" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#2b3036">Digital Twin — Conveyor Cell A</text>
  <line x1="318" y1="332" x2="1168" y2="332" stroke="#777b83" stroke-width="6"/>
  <line x1="318" y1="374" x2="1168" y2="374" stroke="#777b83" stroke-width="6"/>
  <rect x="340" y="344" width="710" height="18" rx="4" fill="#353940"/>
  <g stroke="#9a9da4" stroke-width="2">
    <line x1="370" y1="344" x2="394" y2="362"/><line x1="430" y1="344" x2="454" y2="362"/><line x1="490" y1="344" x2="514" y2="362"/><line x1="550" y1="344" x2="574" y2="362"/>
    <line x1="610" y1="344" x2="634" y2="362"/><line x1="670" y1="344" x2="694" y2="362"/><line x1="730" y1="344" x2="754" y2="362"/><line x1="790" y1="344" x2="814" y2="362"/>
    <line x1="850" y1="344" x2="874" y2="362"/><line x1="910" y1="344" x2="934" y2="362"/><line x1="970" y1="344" x2="994" y2="362"/>
  </g>
  <rect x="410" y="310" width="48" height="34" rx="3" fill="#3498db" stroke="#1f6fa8"/>
  <rect x="678" y="300" width="62" height="44" rx="3" fill="#e67e22" stroke="#a95b16"/>
  <rect x="920" y="304" width="54" height="40" rx="3" fill="#f39c12" stroke="#a46b0d"/>
  <rect x="1044" y="292" width="42" height="52" rx="4" fill="#f4b46a" stroke="#a46b0d"/>
  <rect x="548" y="270" width="130" height="82" fill="url(#metal)" stroke="#676b72" filter="url(#panelShadow)"/>
  <rect x="568" y="288" width="32" height="22" fill="#20242a"/><rect x="606" y="288" width="48" height="22" fill="#20242a"/>
  <circle cx="582" cy="326" r="8" fill="#2ecc71" filter="url(#softGlow)"/><circle cx="612" cy="326" r="8" fill="#f1c40f" filter="url(#softGlow)"/><circle cx="642" cy="326" r="8" fill="#e74c3c" filter="url(#softGlow)"/>
  <path d="M780 338 L810 286 L850 286 L872 338 Z" fill="#7f858d" stroke="#555b63" filter="url(#panelShadow)"/>
  <circle cx="826" cy="286" r="13" fill="#3c424a"/><line x1="826" y1="286" x2="826" y2="246" stroke="#555b63" stroke-width="8"/>
  <path d="M826 246 C846 230 872 234 884 254" fill="none" stroke="#555b63" stroke-width="12"/>
  <circle cx="890" cy="260" r="10" fill="#2ecc71" filter="url(#softGlow)"/>
  <line x1="330" y1="250" x2="330" y2="330" stroke="#454950" stroke-width="4"/><circle cx="330" cy="248" r="9" fill="#2ecc71" filter="url(#softGlow)"/><rect x="320" y="274" width="20" height="42" fill="#2f80c4"/>
  <line x1="1102" y1="238" x2="1102" y2="330" stroke="#454950" stroke-width="4"/><circle cx="1102" cy="236" r="9" fill="#e74c3c" filter="url(#softGlow)"/>
  <rect x="1124" y="382" width="58" height="36" rx="4" fill="#353940" stroke="#1d2025"/>
  <path d="M1138 381 C1140 363 1166 363 1168 381 Z" fill="#e74c3c" filter="url(#softGlow)"/>
  <rect x="704" y="236" width="118" height="54" fill="#2d3138" stroke="#111"/>
  <text x="714" y="255" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#f5f5f5">Valve Unit</text>
  <text x="714" y="273" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#cfd4db">State: OPEN</text>

  <rect x="258" y="512" width="974" height="152" rx="8" fill="#bfc1c8" stroke="#9da0a7"/>
  <rect x="278" y="534" width="934" height="32" fill="#2f343b"/>
  <text x="294" y="555" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#fff">TAG</text>
  <text x="520" y="555" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#fff">VALUE</text>
  <text x="720" y="555" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#fff">STATUS</text>
  <text x="956" y="555" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#fff">UPDATED</text>
  <g font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#25292f">
    <rect x="278" y="566" width="934" height="26" fill="#ececf0"/><text x="294" y="584" width="180">MTR_01_SPEED</text><text x="520" y="584" width="150">1450 rpm</text><circle cx="734" cy="579" r="7" fill="#2ecc71"/><text x="750" y="584" width="120">RUNNING</text><text x="956" y="584" width="160">14:32:08</text>
    <rect x="278" y="592" width="934" height="26" fill="#dfe0e5"/><text x="294" y="610" width="180">TEMP_BEARING_2</text><text x="520" y="610" width="150">82.4 °C</text><circle cx="734" cy="605" r="7" fill="#f1c40f"/><text x="750" y="610" width="120">WARNING</text><text x="956" y="610" width="160">14:32:07</text>
    <rect x="278" y="618" width="934" height="26" fill="#ececf0"/><text x="294" y="636" width="180">GATE_QA_PASS</text><text x="520" y="636" width="150">98.1%</text><circle cx="734" cy="631" r="7" fill="#2ecc71"/><text x="750" y="636" width="120">NORMAL</text><text x="956" y="636" width="160">14:32:05</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using only generic charts; the SCADA effect depends on the physical process schematic and operator-console zoning.
- ❌ Applying `filter` to `<line>` elements for glowing pipes or rails; use glowing circles/rects/path beacons instead.
- ❌ Using `marker-end` for flow arrows; draw arrowheads manually as small `<path>` triangles if needed.
- ❌ Overusing saturated colors in backgrounds; reserve red, amber, and green for operational state.
- ❌ Omitting `width` on `<text>` labels; dense dashboards need predictable PowerPoint text boxes.

## Composition notes
- Keep the slide strongly gridded: software chrome and navigation on the left, KPI strip at top, process schematic center, tag table bottom.
- Use grey panels and metallic gradients as the neutral base; RAG indicators should be the only high-chroma elements.
- The central machinery should occupy the largest visual area, with conveyors, sensors, callouts, and product blocks arranged left-to-right to imply process flow.
- Text should feel like HMI typography: compact labels, bold numerals, small status captions, and dense engineering data rows.