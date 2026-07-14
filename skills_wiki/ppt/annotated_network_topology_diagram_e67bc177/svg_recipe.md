# SVG Recipe — Annotated Network Topology Diagram

## Visual mechanism
A clean node-and-link network map uses standardized geometric device icons, high-contrast connection lines, and numbered callout badges placed directly on network segments. Soft subnet zones and subtle shadows add hierarchy without compromising technical readability.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 4× translucent rounded `<rect>` / `<path>` subnet zones behind device clusters
- 14× `<line>` for physical/logical links between devices
- 4× `<circle>` for router nodes
- 2× rounded `<rect>` for switch nodes
- 6× monitor-style endpoint icons built from `<rect>` and `<line>`
- 8× small `<path>` glyphs inside routers/switches for standardized networking iconography
- 9× numbered annotation badges built from `<rect>` + `<text>`
- 18× `<text>` labels for title, device names, subnet names, and annotation numbers
- 3× `<linearGradient>` fills for premium device and zone styling
- 1× `<filter id="softShadow">` applied to devices and badges
- 1× `<filter id="zoneGlow">` applied to subnet zone paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFF"/>
      <stop offset="100%" stop-color="#EDF3FA"/>
    </linearGradient>
    <linearGradient id="deviceBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4F93D1"/>
      <stop offset="100%" stop-color="#2E5F9E"/>
    </linearGradient>
    <linearGradient id="switchBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5EA2DB"/>
      <stop offset="100%" stop-color="#3F6FA9"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="7"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="zoneGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="64" y="62" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#1C2B39">Annotated Network Topology</text>
  <text x="65" y="92" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#607285">Sequential labels identify routed links, LAN segments, and broadcast domains</text>

  <path d="M75 130 H365 Q390 130 390 155 V255 Q390 280 365 280 H75 Q50 280 50 255 V155 Q50 130 75 130 Z" fill="#DCEBFF" opacity="0.55" filter="url(#zoneGlow)"/>
  <path d="M900 130 H1205 Q1230 130 1230 155 V315 Q1230 340 1205 340 H900 Q875 340 875 315 V155 Q875 130 900 130 Z" fill="#E5F3E6" opacity="0.58" filter="url(#zoneGlow)"/>
  <path d="M315 455 H735 Q760 455 760 480 V665 Q760 690 735 690 H315 Q290 690 290 665 V480 Q290 455 315 455 Z" fill="#FFF1D7" opacity="0.62" filter="url(#zoneGlow)"/>
  <path d="M515 190 H830 Q858 190 858 218 V438 Q858 466 830 466 H515 Q487 466 487 438 V218 Q487 190 515 190 Z" fill="#EFE8FF" opacity="0.50" filter="url(#zoneGlow)"/>

  <text x="70" y="154" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#45668F">Subnet A · Branch LAN</text>
  <text x="895" y="154" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#4D7A57">Subnet B · Services LAN</text>
  <text x="310" y="480" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8A6332">Subnet C · User Access</text>
  <text x="515" y="214" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#66539D">Routed Core</text>

  <line x1="190" y1="210" x2="285" y2="210" stroke="#1E2C38" stroke-width="3"/>
  <line x1="345" y1="210" x2="930" y2="210" stroke="#1E2C38" stroke-width="3"/>
  <line x1="990" y1="210" x2="1125" y2="210" stroke="#1E2C38" stroke-width="3"/>
  <line x1="315" y1="240" x2="500" y2="340" stroke="#1E2C38" stroke-width="3"/>
  <line x1="960" y1="240" x2="700" y2="340" stroke="#1E2C38" stroke-width="3"/>
  <line x1="530" y1="370" x2="670" y2="370" stroke="#1E2C38" stroke-width="3"/>
  <line x1="700" y1="400" x2="905" y2="505" stroke="#1E2C38" stroke-width="3"/>
  <line x1="960" y1="250" x2="1045" y2="320" stroke="#1E2C38" stroke-width="3"/>
  <line x1="1075" y1="365" x2="1145" y2="430" stroke="#1E2C38" stroke-width="3"/>
  <line x1="530" y1="400" x2="520" y2="535" stroke="#1E2C38" stroke-width="3"/>
  <line x1="700" y1="400" x2="520" y2="535" stroke="#1E2C38" stroke-width="3"/>
  <line x1="520" y1="575" x2="370" y2="625" stroke="#1E2C38" stroke-width="3"/>
  <line x1="520" y1="575" x2="520" y2="625" stroke="#1E2C38" stroke-width="3"/>
  <line x1="520" y1="575" x2="670" y2="625" stroke="#1E2C38" stroke-width="3"/>

  <line x1="345" y1="206" x2="930" y2="206" stroke="#38A7FF" stroke-width="5" stroke-dasharray="12 12" opacity="0.42"/>
  <line x1="530" y1="366" x2="670" y2="366" stroke="#38A7FF" stroke-width="5" stroke-dasharray="12 12" opacity="0.42"/>

  <rect x="130" y="180" width="60" height="42" rx="6" fill="#77838F" filter="url(#softShadow)"/>
  <rect x="140" y="188" width="40" height="24" rx="3" fill="#E9EEF4"/>
  <line x1="150" y1="228" x2="170" y2="228" stroke="#77838F" stroke-width="5"/>

  <circle cx="315" cy="210" r="42" fill="url(#deviceBlue)" filter="url(#softShadow)"/>
  <path d="M294 203 H336 M315 182 V224 M300 191 L288 203 L300 215 M330 191 L342 203 L330 215" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="285" y="265" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#24384B">R1</text>

  <circle cx="960" cy="210" r="42" fill="url(#deviceBlue)" filter="url(#softShadow)"/>
  <path d="M939 203 H981 M960 182 V224 M945 191 L933 203 L945 215 M975 191 L987 203 L975 215" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="930" y="265" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#24384B">R2</text>

  <circle cx="530" cy="370" r="42" fill="url(#deviceBlue)" filter="url(#softShadow)"/>
  <path d="M509 363 H551 M530 342 V384 M515 351 L503 363 L515 375 M545 351 L557 363 L545 375" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="500" y="425" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#24384B">R3</text>

  <circle cx="700" cy="370" r="42" fill="url(#deviceBlue)" filter="url(#softShadow)"/>
  <path d="M679 363 H721 M700 342 V384 M685 351 L673 363 L685 375 M715 351 L727 363 L715 375" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="670" y="425" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#24384B">R4</text>

  <rect x="470" y="535" width="100" height="58" rx="10" fill="url(#switchBlue)" filter="url(#softShadow)"/>
  <path d="M490 558 H550 M495 573 H545 M505 550 V582 M535 550 V582" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="490" y="610" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#24384B">S1</text>

  <rect x="1025" y="320" width="100" height="58" rx="10" fill="url(#switchBlue)" filter="url(#softShadow)"/>
  <path d="M1045 343 H1105 M1050 358 H1100 M1060 335 V367 M1090 335 V367" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="1045" y="395" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#24384B">S2</text>

  <rect x="1125" y="180" width="60" height="42" rx="6" fill="#77838F" filter="url(#softShadow)"/><rect x="1135" y="188" width="40" height="24" rx="3" fill="#E9EEF4"/><line x1="1145" y1="228" x2="1165" y2="228" stroke="#77838F" stroke-width="5"/>
  <rect x="1145" y="430" width="60" height="42" rx="6" fill="#77838F" filter="url(#softShadow)"/><rect x="1155" y="438" width="40" height="24" rx="3" fill="#E9EEF4"/><line x1="1165" y1="478" x2="1185" y2="478" stroke="#77838F" stroke-width="5"/>
  <rect x="340" y="625" width="60" height="42" rx="6" fill="#77838F" filter="url(#softShadow)"/><rect x="350" y="633" width="40" height="24" rx="3" fill="#E9EEF4"/><line x1="360" y1="673" x2="380" y2="673" stroke="#77838F" stroke-width="5"/>
  <rect x="490" y="625" width="60" height="42" rx="6" fill="#77838F" filter="url(#softShadow)"/><rect x="500" y="633" width="40" height="24" rx="3" fill="#E9EEF4"/><line x1="510" y1="673" x2="530" y2="673" stroke="#77838F" stroke-width="5"/>
  <rect x="640" y="625" width="60" height="42" rx="6" fill="#77838F" filter="url(#softShadow)"/><rect x="650" y="633" width="40" height="24" rx="3" fill="#E9EEF4"/><line x1="660" y1="673" x2="680" y2="673" stroke="#77838F" stroke-width="5"/>

  <rect x="456" y="193" width="34" height="34" rx="7" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/><text x="456" y="217" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#111827">1</text>
  <rect x="241" y="276" width="34" height="34" rx="7" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/><text x="241" y="300" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#111827">2</text>
  <rect x="751" y="279" width="34" height="34" rx="7" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/><text x="751" y="303" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#111827">3</text>
  <rect x="598" y="338" width="34" height="34" rx="7" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/><text x="598" y="362" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#111827">4</text>
  <rect x="874" y="458" width="34" height="34" rx="7" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/><text x="874" y="482" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#111827">5</text>
  <rect x="585" y="488" width="34" height="34" rx="7" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/><text x="585" y="512" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#111827">6</text>
  <rect x="410" y="586" width="34" height="34" rx="7" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/><text x="410" y="610" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#111827">7</text>
  <rect x="540" y="607" width="34" height="34" rx="7" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/><text x="540" y="631" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#111827">8</text>
  <rect x="655" y="585" width="34" height="34" rx="7" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/><text x="655" y="609" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#111827">9</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `filter` to `<line>` connectors; shadows on links are dropped and make topology harder to read.
- ❌ Using `marker-end` on `<path>` for arrows; if directionality is required, use short separate `<line>` segments or small triangle `<path>` arrowheads.
- ❌ Overloading every node with long labels; keep device labels short and move explanations into numbered annotations.
- ❌ Placing badges directly over device centers; badges should sit on links or subnet boundaries so the physical topology remains visible.
- ❌ Using `<use>` for repeated icons; duplicate the native SVG primitives so the PowerPoint output stays fully editable.

## Composition notes
- Keep the slide mostly white or pale blue, with subnet zones at 40–65% opacity behind the topology so connectors remain dominant.
- Place core routers near the center and access/end devices toward the perimeter; this preserves a readable hierarchy from WAN/core to LAN edge.
- Use annotation badges as the visual sequence: 1–4 for routed/core links, then 5–9 for LAN or endpoint segments.
- Use one strong device color, one neutral endpoint color, and only subtle zone tints; too many saturated colors make the diagram feel like a dashboard rather than an architecture explanation.