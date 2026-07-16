# SVG Recipe — Digital Twin Command Center

## Visual mechanism
A dark, gridded HUD canvas frames a central axonometric “digital twin” schematic, with neon telemetry panels, gauges, alert pings, and live-feed cards layered above it. The effect depends on depth: muted wireframe infrastructure in the middle, glowing operational states on top, and compact executive KPIs around the perimeter.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background.
- 2× `<path>` for subtle minor/major background grid lines.
- 6–8× translucent `<rect>` for glassmorphism dashboard panels and section headers.
- 10–14× `<path>` for the axonometric factory floor, buildings, conveyor lanes, zone overlays, and callout connectors.
- 6–10× `<circle>` for KPI gauges, alert pings, status LEDs, and map nodes.
- 1× `<image>` clipped with a rounded `<clipPath>` for a live camera / digital twin reference feed.
- 2× `<linearGradient>` for premium panel and map-surface fills.
- 1× `<radialGradient>` for ambient cyan glow behind the schematic.
- 2× `<filter>` definitions: one soft neon glow and one panel drop shadow.
- Multiple `<text>` elements with explicit `width` attributes for command-center labels, KPI numerals, chart labels, and alert annotations.
- 1× compact bottom bar chart built from editable `<rect>` bars plus axis/grid `<line>` elements.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#172136" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#080d18" stop-opacity="0.86"/>
    </linearGradient>
    <linearGradient id="deckFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2f6f95" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#0fe0ff" stop-opacity="0.08"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="50%" cy="48%" r="48%">
      <stop offset="0%" stop-color="#00dcff" stop-opacity="0.22"/>
      <stop offset="65%" stop-color="#00dcff" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#00dcff" stop-opacity="0"/>
    </radialGradient>
    <filter id="neonGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="feedClip">
      <rect x="1020" y="90" width="190" height="108" rx="16"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#141825"/>
  <rect x="250" y="80" width="780" height="520" fill="url(#centerGlow)"/>

  <path d="M0 40H1280 M0 80H1280 M0 120H1280 M0 160H1280 M0 200H1280 M0 240H1280 M0 280H1280 M0 320H1280 M0 360H1280 M0 400H1280 M0 440H1280 M0 480H1280 M0 520H1280 M0 560H1280 M0 600H1280 M0 640H1280 M0 680H1280 M40 0V720 M80 0V720 M120 0V720 M160 0V720 M200 0V720 M240 0V720 M280 0V720 M320 0V720 M360 0V720 M400 0V720 M440 0V720 M480 0V720 M520 0V720 M560 0V720 M600 0V720 M640 0V720 M680 0V720 M720 0V720 M760 0V720 M800 0V720 M840 0V720 M880 0V720 M920 0V720 M960 0V720 M1000 0V720 M1040 0V720 M1080 0V720 M1120 0V720 M1160 0V720 M1200 0V720 M1240 0V720" stroke="#324058" stroke-width="1" opacity="0.28"/>
  <path d="M0 160H1280 M0 320H1280 M0 480H1280 M0 640H1280 M160 0V720 M320 0V720 M480 0V720 M640 0V720 M800 0V720 M960 0V720 M1120 0V720" stroke="#60708c" stroke-width="1.2" opacity="0.22"/>

  <text x="56" y="54" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#ffffff" filter="url(#neonGlow)">DIGITAL TWIN COMMAND CENTER</text>
  <text x="56" y="82" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#aeb8ca">Plant A · Live operational state · 14:32:09 UTC</text>
  <text x="1052" y="52" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#50ff96">● SYSTEM NOMINAL</text>

  <rect x="38" y="118" width="230" height="238" rx="18" fill="url(#panelFill)" stroke="#00dcff" stroke-opacity="0.35" filter="url(#panelShadow)"/>
  <text x="62" y="150" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">THROUGHPUT</text>
  <circle cx="153" cy="235" r="62" fill="none" stroke="#28334a" stroke-width="16"/>
  <circle cx="153" cy="235" r="62" fill="none" stroke="#00dcff" stroke-width="16" stroke-dasharray="292 390" stroke-linecap="round" transform="rotate(-90 153 235)" filter="url(#neonGlow)"/>
  <text x="96" y="230" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#ffffff" text-anchor="middle">87%</text>
  <text x="96" y="258" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#aeb8ca" text-anchor="middle">line utilization</text>
  <path d="M76 323H230" stroke="#28334a" stroke-width="8" stroke-linecap="round"/>
  <path d="M76 323H201" stroke="#50ff96" stroke-width="8" stroke-linecap="round" filter="url(#neonGlow)"/>
  <text x="76" y="345" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#c8c8d2">OEE target 92%</text>

  <rect x="1012" y="118" width="230" height="238" rx="18" fill="url(#panelFill)" stroke="#ff0096" stroke-opacity="0.35" filter="url(#panelShadow)"/>
  <image href="https://images.example.com/factory-floor-thermal-camera-feed.jpg" x="1020" y="90" width="190" height="108" clip-path="url(#feedClip)" opacity="0.72"/>
  <rect x="1020" y="90" width="190" height="108" rx="16" fill="none" stroke="#00dcff" stroke-opacity="0.45"/>
  <text x="1038" y="150" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ffffff">LIVE BAY CAMERA</text>
  <text x="1038" y="226" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">ALERT QUEUE</text>
  <circle cx="1052" cy="262" r="7" fill="#ff0050" filter="url(#neonGlow)"/>
  <text x="1070" y="267" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffdbe6">Robot cell B4 latency</text>
  <circle cx="1052" cy="296" r="7" fill="#ffdc00" filter="url(#neonGlow)"/>
  <text x="1070" y="301" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#fff2a8">Compressor temp rising</text>
  <circle cx="1052" cy="330" r="7" fill="#50ff96" filter="url(#neonGlow)"/>
  <text x="1070" y="335" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#c9ffe0">Dock 3 cleared</text>

  <path d="M426 210L656 124L905 250L674 356Z" fill="url(#deckFill)" stroke="#77c9ff" stroke-width="1.4" opacity="0.92"/>
  <path d="M426 210L426 282L674 438L674 356Z M674 356L905 250L905 315L674 438Z" fill="#13314a" stroke="#77c9ff" stroke-width="1.2" opacity="0.54"/>
  <path d="M505 214L620 172L710 218L594 262Z M690 243L790 205L855 238L756 278Z M548 294L648 250L745 300L644 346Z" fill="#1c5b79" stroke="#9adfff" stroke-width="1.1" opacity="0.62"/>
  <path d="M515 190L620 150L620 172L505 214Z M620 150L716 196L710 218L620 172Z" fill="#2a7fa5" stroke="#a9e9ff" stroke-width="1" opacity="0.52"/>
  <path d="M690 217L790 180L790 205L690 243Z M790 180L860 215L855 238L790 205Z" fill="#2a7fa5" stroke="#a9e9ff" stroke-width="1" opacity="0.52"/>
  <path d="M548 270L648 225L648 250L548 294Z M648 225L748 276L745 300L648 250Z" fill="#2a7fa5" stroke="#a9e9ff" stroke-width="1" opacity="0.52"/>

  <path d="M486 252C560 224 632 224 724 270C779 298 823 300 866 280" fill="none" stroke="#00dcff" stroke-width="7" stroke-opacity="0.32" stroke-linecap="round"/>
  <path d="M486 252C560 224 632 224 724 270C779 298 823 300 866 280" fill="none" stroke="#00dcff" stroke-width="2.2" stroke-dasharray="8 10" stroke-linecap="round" filter="url(#neonGlow)"/>
  <path d="M725 260L808 225L858 250L776 288Z" fill="#ffdc00" fill-opacity="0.28" stroke="#ffdc00" stroke-width="1.3" filter="url(#neonGlow)"/>
  <path d="M564 286L643 252L696 279L617 315Z" fill="#ff0050" fill-opacity="0.25" stroke="#ff0050" stroke-width="1.3" filter="url(#neonGlow)"/>

  <circle cx="617" cy="280" r="12" fill="#ff0050" fill-opacity="0.32" stroke="#ff0050" stroke-width="2" filter="url(#neonGlow)"/>
  <circle cx="617" cy="280" r="26" fill="none" stroke="#ff0050" stroke-width="1.4" stroke-opacity="0.52"/>
  <circle cx="777" cy="254" r="10" fill="#ffdc00" fill-opacity="0.35" stroke="#ffdc00" stroke-width="2" filter="url(#neonGlow)"/>
  <circle cx="514" cy="246" r="8" fill="#50ff96" stroke="#50ff96" stroke-width="2" filter="url(#neonGlow)"/>
  <path d="M617 280L348 162" stroke="#ff0050" stroke-width="1.4" stroke-dasharray="5 7" fill="none"/>
  <path d="M777 254L963 166" stroke="#ffdc00" stroke-width="1.4" stroke-dasharray="5 7" fill="none"/>

  <rect x="316" y="126" width="178" height="72" rx="14" fill="#10182a" stroke="#ff0050" stroke-opacity="0.58"/>
  <text x="338" y="153" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ff78a8">B4 ROBOT CELL</text>
  <text x="338" y="179" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">+18 ms</text>

  <rect x="904" y="126" width="170" height="72" rx="14" fill="#10182a" stroke="#ffdc00" stroke-opacity="0.58"/>
  <text x="926" y="153" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#fff07a">THERMAL DRIFT</text>
  <text x="926" y="179" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">74.2°C</text>

  <rect x="38" y="394" width="1204" height="252" rx="22" fill="url(#panelFill)" stroke="#40506d" stroke-opacity="0.55" filter="url(#panelShadow)"/>
  <text x="66" y="430" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">SHIFT TELEMETRY</text>
  <line x1="86" y1="586" x2="510" y2="586" stroke="#3b4964" stroke-width="1"/>
  <line x1="86" y1="536" x2="510" y2="536" stroke="#3b4964" stroke-width="1" stroke-dasharray="4 8"/>
  <line x1="86" y1="486" x2="510" y2="486" stroke="#3b4964" stroke-width="1" stroke-dasharray="4 8"/>
  <rect x="102" y="524" width="24" height="62" rx="5" fill="#00dcff" opacity="0.72"/>
  <rect x="150" y="492" width="24" height="94" rx="5" fill="#00dcff" opacity="0.86"/>
  <rect x="198" y="506" width="24" height="80" rx="5" fill="#00dcff" opacity="0.78"/>
  <rect x="246" y="462" width="24" height="124" rx="5" fill="#50ff96" opacity="0.82"/>
  <rect x="294" y="480" width="24" height="106" rx="5" fill="#50ff96" opacity="0.72"/>
  <rect x="342" y="445" width="24" height="141" rx="5" fill="#ffdc00" opacity="0.78"/>
  <rect x="390" y="516" width="24" height="70" rx="5" fill="#ff0096" opacity="0.76"/>
  <rect x="438" y="468" width="24" height="118" rx="5" fill="#00dcff" opacity="0.82"/>

  <text x="574" y="430" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">ENERGY / UNIT</text>
  <path d="M585 570C620 530 648 552 676 512C711 462 748 496 780 452C810 411 848 450 880 418" fill="none" stroke="#50ff96" stroke-width="3" stroke-linecap="round" filter="url(#neonGlow)"/>
  <path d="M585 600H895 M585 550H895 M585 500H895 M585 450H895" stroke="#3b4964" stroke-width="1" stroke-dasharray="4 8"/>
  <circle cx="676" cy="512" r="5" fill="#50ff96"/>
  <circle cx="780" cy="452" r="5" fill="#50ff96"/>
  <circle cx="880" cy="418" r="5" fill="#50ff96"/>

  <text x="956" y="430" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">EXECUTIVE KPIs</text>
  <circle cx="1018" cy="520" r="46" fill="none" stroke="#28334a" stroke-width="12"/>
  <circle cx="1018" cy="520" r="46" fill="none" stroke="#50ff96" stroke-width="12" stroke-dasharray="231 289" stroke-linecap="round" transform="rotate(-90 1018 520)" filter="url(#neonGlow)"/>
  <text x="978" y="526" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff" text-anchor="middle">80%</text>
  <text x="974" y="590" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#aeb8ca" text-anchor="middle">SLA health</text>
  <circle cx="1148" cy="520" r="46" fill="none" stroke="#28334a" stroke-width="12"/>
  <circle cx="1148" cy="520" r="46" fill="none" stroke="#ff0096" stroke-width="12" stroke-dasharray="176 289" stroke-linecap="round" transform="rotate(-90 1148 520)" filter="url(#neonGlow)"/>
  <text x="1108" y="526" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff" text-anchor="middle">61%</text>
  <text x="1102" y="590" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#aeb8ca" text-anchor="middle">risk burn-down</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for the background grid; use explicit editable `<path>` or `<line>` grid strokes instead.
- ❌ Applying `filter` to `<line>` elements for glowing connectors; use `<path>` connectors when glow is needed.
- ❌ `mask` overlays for HUD fades or glass cards; use translucent fills, gradients, and opacity.
- ❌ `clip-path` on panels or map shapes; clipping is reliable for `<image>` crops only.
- ❌ `marker-end` on `<path>` callouts; if arrows are needed, draw the arrowhead manually with a small `<path>` triangle or use direct `<line>` arrow support.

## Composition notes
- Keep the central digital twin dominant: roughly 50–60% of the slide width, centered slightly above midline, with KPI panels orbiting it.
- Use dark negative space and thin grid strokes so neon cyan, green, yellow, and magenta remain the visual hierarchy.
- Bottom third should feel like a telemetry strip: compact charts, dense but aligned, with consistent card padding.
- Reserve red and yellow for spatial alerts only; this makes the viewer immediately connect the alert queue to exact locations on the schematic.