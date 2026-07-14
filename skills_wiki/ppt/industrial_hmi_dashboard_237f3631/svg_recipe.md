# SVG Recipe — Industrial HMI Dashboard

## Visual mechanism
Create a static “control room” snapshot: high-level KPI tiles across the top and a schematic production line beneath, using metallic grays for machinery and saturated green/yellow/red lights for operational status. The layout should read left-to-right like a physical process, with gauges, panels, pipes, conveyors, robot arms, and control buttons forming an editable HMI-style dashboard.

## SVG primitives needed
- 1× `<rect>` for the full-slide industrial gray background
- 6–10× `<line>` for subtle blueprint/grid guides and process connectors
- 8–12× `<rect>` for dark KPI cards, machine bodies, conveyor sections, and control panels
- 6–10× `<circle>` for gauge rings, conveyor rollers, warning lights, and status lamps
- 3–5× `<ellipse>` for tanks, vessel tops, and metallic end caps
- 5–8× `<path>` for gauge arcs, robotic arm geometry, product-flow arrows, mini trend line, and custom machine silhouettes
- 1× `<linearGradient>` for steel/metal fills
- 1× `<linearGradient>` for dark glass-like KPI panels
- 1× `<linearGradient>` for the conveyor belt
- 2× `<filter>` definitions: soft panel shadow and colored status glow
- 20+× `<text>` labels with explicit `width` attributes for KPI values, station names, units, and status labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4d4d4d"/>
      <stop offset="100%" stop-color="#2f2f2f"/>
    </linearGradient>
    <linearGradient id="steelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#d8d8d8"/>
      <stop offset="45%" stop-color="#9e9e9e"/>
      <stop offset="100%" stop-color="#6d6d6d"/>
    </linearGradient>
    <linearGradient id="beltGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#575757"/>
      <stop offset="50%" stop-color="#2d2d2d"/>
      <stop offset="100%" stop-color="#171717"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="greenGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="redGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#e3e3e3"/>
  <line x1="0" y1="175" x2="1280" y2="175" stroke="#c7c7c7" stroke-width="2"/>
  <line x1="0" y1="610" x2="1280" y2="610" stroke="#c7c7c7" stroke-width="2"/>
  <line x1="80" y1="205" x2="80" y2="590" stroke="#d0d0d0" stroke-width="1" stroke-dasharray="6 10"/>
  <line x1="320" y1="205" x2="320" y2="590" stroke="#d0d0d0" stroke-width="1" stroke-dasharray="6 10"/>
  <line x1="560" y1="205" x2="560" y2="590" stroke="#d0d0d0" stroke-width="1" stroke-dasharray="6 10"/>
  <line x1="800" y1="205" x2="800" y2="590" stroke="#d0d0d0" stroke-width="1" stroke-dasharray="6 10"/>
  <line x1="1040" y1="205" x2="1040" y2="590" stroke="#d0d0d0" stroke-width="1" stroke-dasharray="6 10"/>

  <text x="42" y="42" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#222">Factory Operations Dashboard</text>
  <text x="42" y="68" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#666">Line A-17 · Live HMI Snapshot · Shift 2</text>
  <circle cx="1205" cy="43" r="9" fill="#69be28" filter="url(#greenGlow)"/>
  <text x="1220" y="48" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#333">ONLINE</text>

  <rect x="42" y="92" width="184" height="62" rx="8" fill="url(#panelGrad)" filter="url(#shadow)"/>
  <text x="58" y="116" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cfcfcf">OEE</text>
  <text x="58" y="146" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#fff">87%</text>
  <circle cx="184" cy="123" r="23" fill="none" stroke="#6b6b6b" stroke-width="8"/>
  <circle cx="184" cy="123" r="23" fill="none" stroke="#69be28" stroke-width="8" stroke-dasharray="126 145" transform="rotate(-90 184 123)"/>

  <rect x="248" y="92" width="184" height="62" rx="8" fill="url(#panelGrad)" filter="url(#shadow)"/>
  <text x="264" y="116" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cfcfcf">PRODUCTION</text>
  <text x="264" y="146" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#fff">14.2k</text>
  <text x="374" y="146" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#b8b8b8">units</text>

  <rect x="454" y="92" width="184" height="62" rx="8" fill="url(#panelGrad)" filter="url(#shadow)"/>
  <text x="470" y="116" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cfcfcf">SCRAP RATE</text>
  <text x="470" y="146" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#fff">1.8%</text>
  <circle cx="598" cy="123" r="23" fill="none" stroke="#6b6b6b" stroke-width="8"/>
  <circle cx="598" cy="123" r="23" fill="none" stroke="#ffc000" stroke-width="8" stroke-dasharray="54 145" transform="rotate(-90 598 123)"/>

  <rect x="660" y="92" width="184" height="62" rx="8" fill="url(#panelGrad)" filter="url(#shadow)"/>
  <text x="676" y="116" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cfcfcf">CYCLE TIME</text>
  <text x="676" y="146" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#fff">42s</text>
  <path d="M775 141 C790 118, 812 132, 825 108" fill="none" stroke="#69be28" stroke-width="4"/>

  <rect x="866" y="92" width="184" height="62" rx="8" fill="url(#panelGrad)" filter="url(#shadow)"/>
  <text x="882" y="116" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cfcfcf">ENERGY LOAD</text>
  <text x="882" y="146" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#fff">68%</text>
  <circle cx="1010" cy="123" r="23" fill="none" stroke="#6b6b6b" stroke-width="8"/>
  <circle cx="1010" cy="123" r="23" fill="none" stroke="#69be28" stroke-width="8" stroke-dasharray="98 145" transform="rotate(-90 1010 123)"/>

  <rect x="1072" y="92" width="166" height="62" rx="8" fill="#3b3b3b" filter="url(#shadow)"/>
  <text x="1088" y="116" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cfcfcf">ALARMS</text>
  <text x="1088" y="146" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#ff4040">2</text>
  <circle cx="1190" cy="123" r="10" fill="#ff0000" filter="url(#redGlow)"/>
  <circle cx="1215" cy="123" r="10" fill="#ffc000"/>

  <rect x="92" y="442" width="1040" height="66" rx="16" fill="url(#beltGrad)" filter="url(#shadow)"/>
  <line x1="122" y1="475" x2="1100" y2="475" stroke="#888" stroke-width="3" stroke-dasharray="24 18"/>
  <circle cx="150" cy="508" r="22" fill="#777" stroke="#444" stroke-width="4"/>
  <circle cx="322" cy="508" r="22" fill="#777" stroke="#444" stroke-width="4"/>
  <circle cx="494" cy="508" r="22" fill="#777" stroke="#444" stroke-width="4"/>
  <circle cx="666" cy="508" r="22" fill="#777" stroke="#444" stroke-width="4"/>
  <circle cx="838" cy="508" r="22" fill="#777" stroke="#444" stroke-width="4"/>
  <circle cx="1010" cy="508" r="22" fill="#777" stroke="#444" stroke-width="4"/>
  <path d="M258 465 l24 10 l-24 10 z M548 465 l24 10 l-24 10 z M836 465 l24 10 l-24 10 z" fill="#bdbdbd"/>

  <rect x="128" y="394" width="58" height="48" rx="6" fill="#4472c4" stroke="#1f3f77" stroke-width="3"/>
  <rect x="250" y="392" width="62" height="50" rx="6" fill="#4472c4" stroke="#1f3f77" stroke-width="3"/>
  <rect x="930" y="392" width="76" height="50" rx="6" fill="#4472c4" stroke="#1f3f77" stroke-width="3"/>

  <path d="M108 410 L152 260 L232 260 L276 410 Z" fill="url(#steelGrad)" stroke="#5a5a5a" stroke-width="3"/>
  <ellipse cx="192" cy="260" rx="40" ry="13" fill="#c8c8c8" stroke="#666" stroke-width="3"/>
  <text x="125" y="235" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#333">RAW MATERIAL</text>
  <circle cx="245" cy="285" r="10" fill="#69be28" filter="url(#greenGlow)"/>

  <rect x="354" y="262" width="160" height="142" rx="12" fill="url(#steelGrad)" stroke="#5a5a5a" stroke-width="3"/>
  <ellipse cx="434" cy="262" rx="80" ry="18" fill="#d5d5d5" stroke="#666" stroke-width="3"/>
  <ellipse cx="434" cy="404" rx="80" ry="18" fill="#8b8b8b" stroke="#666" stroke-width="3"/>
  <path d="M405 322 C430 300, 462 344, 489 314" fill="none" stroke="#69be28" stroke-width="5"/>
  <text x="374" y="239" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#333">MIXING TANK</text>
  <circle cx="494" cy="286" r="10" fill="#69be28" filter="url(#greenGlow)"/>

  <rect x="610" y="238" width="240" height="36" rx="8" fill="#777" stroke="#4f4f4f" stroke-width="3"/>
  <rect x="630" y="274" width="26" height="146" fill="#777" stroke="#4f4f4f" stroke-width="3"/>
  <rect x="804" y="274" width="26" height="146" fill="#777" stroke="#4f4f4f" stroke-width="3"/>
  <path d="M731 274 L772 314 L746 340 L705 300 Z" fill="#a6a6a6" stroke="#555" stroke-width="3"/>
  <path d="M748 336 L714 392 L682 372 L716 316 Z" fill="#bfbfbf" stroke="#555" stroke-width="3"/>
  <rect x="672" y="374" width="46" height="18" rx="4" fill="#555"/>
  <line x1="686" y1="392" x2="686" y2="424" stroke="#555" stroke-width="5"/>
  <line x1="704" y1="392" x2="704" y2="424" stroke="#555" stroke-width="5"/>
  <text x="658" y="221" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#333">ROBOT PICK ARM</text>
  <circle cx="824" cy="252" r="10" fill="#ffc000"/>

  <rect x="914" y="272" width="150" height="128" rx="10" fill="url(#steelGrad)" stroke="#5a5a5a" stroke-width="3"/>
  <rect x="946" y="302" width="86" height="48" rx="4" fill="#2f2f2f"/>
  <path d="M959 335 C980 310, 1000 353, 1022 318" fill="none" stroke="#69be28" stroke-width="4"/>
  <circle cx="989" cy="374" r="15" fill="#222"/>
  <circle cx="989" cy="374" r="7" fill="#69be28" filter="url(#greenGlow)"/>
  <text x="932" y="248" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#333">VISION QC</text>

  <rect x="1136" y="224" width="96" height="342" rx="10" fill="#4a4a4a" filter="url(#shadow)"/>
  <text x="1153" y="252" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#fff">CONTROL</text>
  <circle cx="1164" cy="292" r="12" fill="#69be28" filter="url(#greenGlow)"/>
  <text x="1184" y="297" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#eee">RUN</text>
  <circle cx="1164" cy="330" r="12" fill="#ffc000"/>
  <text x="1184" y="335" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#eee">HOLD</text>
  <circle cx="1164" cy="368" r="12" fill="#ff0000" filter="url(#redGlow)"/>
  <text x="1184" y="373" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#eee">STOP</text>
  <rect x="1154" y="418" width="58" height="28" rx="5" fill="#69be28"/>
  <text x="1165" y="437" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#fff">AUTO</text>
  <rect x="1154" y="458" width="58" height="28" rx="5" fill="#777"/>
  <text x="1160" y="477" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#fff">MANUAL</text>

  <rect x="42" y="630" width="260" height="50" rx="8" fill="#595959"/>
  <text x="62" y="660" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#fff">Throughput</text>
  <text x="196" y="660" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#69be28">+12%</text>
  <rect x="326" y="630" width="260" height="50" rx="8" fill="#595959"/>
  <text x="346" y="660" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#fff">Maintenance ETA</text>
  <text x="505" y="660" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffc000">3h</text>
  <rect x="610" y="630" width="260" height="50" rx="8" fill="#595959"/>
  <text x="630" y="660" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#fff">Line Status</text>
  <text x="760" y="660" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#69be28">STABLE</text>
  <rect x="894" y="630" width="344" height="50" rx="8" fill="#595959"/>
  <text x="914" y="660" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#fff">Operator Note</text>
  <text x="1060" y="660" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#d9d9d9">QC camera recalibrated</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on animation for the HMI effect; create a polished static dashboard snapshot instead.
- ❌ Do not use `<mask>` or clipping on non-image elements for gauge rings; use editable circles/paths with strokes and dash arrays.
- ❌ Do not apply filters to `<line>` connectors; shadows/glows should be applied to panels, circles, paths, or text only.
- ❌ Do not build the entire diagram as a single screenshot; use native rectangles, paths, circles, ellipses, and text so PowerPoint users can edit every station.
- ❌ Do not use muted colors for status lamps; green/yellow/red indicators must be saturated enough to stand out against the gray machinery.

## Composition notes
- Reserve the top 20–25% of the canvas for KPI cards; keep them dark so white numbers and colored gauge arcs feel like real HMI readouts.
- Use the center 55–60% for the production schematic, flowing left-to-right from raw material to inspection and packaging.
- Keep the background and machinery mostly grayscale; only products, alarms, and live-status lights should carry strong color.
- Add a compact bottom strip for control states, maintenance timing, and operator notes to complete the “operations command center” feel.