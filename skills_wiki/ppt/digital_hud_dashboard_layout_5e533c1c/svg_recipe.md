# SVG Recipe — Digital HUD Dashboard Layout

## Visual mechanism
A dark radial-gradient stage supports a grid of floating, rounded HUD panels with thin luminous borders, glowing KPI typography, and neon chart marks. The premium look comes from layered depth: vignette background, faint grid/radar decoration, soft panel shadows, and high-contrast lime/cyan data accents.

## SVG primitives needed
- 1× `<rect>` for the full-slide radial-gradient background
- 1× `<path>` for a subtle topographic/radar background glow
- 9× `<rect>` for floating rounded dashboard panels and chart containers
- 16× `<line>` for chart axes, gridlines, and small HUD separators
- 20× `<rect>` for bar charts, progress meters, micro cards, and status pills
- 8× `<circle>` for donut/ring charts, radar nodes, and glowing data points
- 3× `<path>` for line/area chart data traces and small HUD icons
- 1× `<linearGradient>` for panel edge sheen
- 1× `<radialGradient>` for the red-black vignette background
- 2× `<filter>` effects: soft shadow on panels and lime/cyan glow on text/data marks
- Multiple `<text>` elements with explicit `width` attributes for editable labels, KPI values, and chart annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="50%" cy="42%" r="76%">
      <stop offset="0%" stop-color="#340000"/>
      <stop offset="45%" stop-color="#171012"/>
      <stop offset="100%" stop-color="#08090A"/>
    </radialGradient>

    <linearGradient id="panelFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2B3035"/>
      <stop offset="55%" stop-color="#202428"/>
      <stop offset="100%" stop-color="#171A1E"/>
    </linearGradient>

    <linearGradient id="limeSheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#DAFF70" stop-opacity="0.1"/>
      <stop offset="50%" stop-color="#DAFF70" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#3CCCD6" stop-opacity="0.15"/>
    </linearGradient>

    <linearGradient id="areaGreen" x1="0" y1="270" x2="0" y2="570">
      <stop offset="0%" stop-color="#DAFF70" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#DAFF70" stop-opacity="0.02"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="hudGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>

  <path d="M58 618 C170 548, 234 644, 352 560 S566 470, 690 536 S916 646, 1064 538 S1186 448, 1240 502"
        fill="none" stroke="#DAFF70" stroke-width="1.2" stroke-opacity="0.18"/>
  <circle cx="1084" cy="148" r="88" fill="none" stroke="#3CCCD6" stroke-width="1" stroke-opacity="0.16"/>
  <circle cx="1084" cy="148" r="52" fill="none" stroke="#DAFF70" stroke-width="1" stroke-opacity="0.12"/>
  <line x1="996" y1="148" x2="1172" y2="148" stroke="#3CCCD6" stroke-width="1" stroke-opacity="0.14"/>
  <line x1="1084" y1="60" x2="1084" y2="236" stroke="#3CCCD6" stroke-width="1" stroke-opacity="0.14"/>

  <text x="54" y="62" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700"
        letter-spacing="3" fill="#DAFF70" filter="url(#hudGlow)">SALES COMMAND CENTER</text>
  <text x="56" y="92" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        letter-spacing="1.4" fill="#D7DEE6" opacity="0.75">LIVE PERFORMANCE HUD · Q4 EXECUTIVE SNAPSHOT</text>

  <rect x="930" y="42" width="290" height="42" rx="21" fill="#14171A" stroke="#46505A" stroke-width="1"/>
  <circle cx="958" cy="63" r="6" fill="#21AE62" filter="url(#hudGlow)"/>
  <text x="975" y="68" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600"
        fill="#FFFFFF">SYSTEM HEALTH 98.7%</text>

  <rect x="54" y="122" width="274" height="138" rx="22" fill="url(#panelFill)" stroke="#46505A" stroke-width="1.2" filter="url(#panelShadow)"/>
  <rect x="70" y="138" width="80" height="7" rx="3.5" fill="url(#limeSheen)"/>
  <text x="72" y="172" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#D7DEE6">Total Revenue</text>
  <text x="72" y="218" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800"
        fill="#DAFF70" filter="url(#hudGlow)">$42.8M</text>
  <text x="74" y="240" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#21AE62">▲ 18.4% vs target</text>

  <rect x="354" y="122" width="274" height="138" rx="22" fill="url(#panelFill)" stroke="#46505A" stroke-width="1.2" filter="url(#panelShadow)"/>
  <rect x="370" y="138" width="80" height="7" rx="3.5" fill="url(#limeSheen)"/>
  <text x="372" y="172" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#D7DEE6">Active Pipeline</text>
  <text x="372" y="218" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800"
        fill="#DAFF70" filter="url(#hudGlow)">1,284</text>
  <text x="374" y="240" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#3CCCD6">64 enterprise deals</text>

  <rect x="654" y="122" width="274" height="138" rx="22" fill="url(#panelFill)" stroke="#46505A" stroke-width="1.2" filter="url(#panelShadow)"/>
  <rect x="670" y="138" width="80" height="7" rx="3.5" fill="url(#limeSheen)"/>
  <text x="672" y="172" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#D7DEE6">Win Rate</text>
  <text x="672" y="218" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800"
        fill="#DAFF70" filter="url(#hudGlow)">72%</text>
  <text x="674" y="240" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.7">Best region: APAC</text>

  <rect x="954" y="122" width="212" height="138" rx="22" fill="url(#panelFill)" stroke="#46505A" stroke-width="1.2" filter="url(#panelShadow)"/>
  <text x="976" y="158" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#D7DEE6">Quota Burn</text>
  <circle cx="1060" cy="200" r="42" fill="none" stroke="#353C43" stroke-width="14"/>
  <circle cx="1060" cy="200" r="42" fill="none" stroke="#DAFF70" stroke-width="14" stroke-dasharray="198 264" filter="url(#hudGlow)"/>
  <text x="1034" y="208" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#FFFFFF">75%</text>

  <rect x="54" y="292" width="574" height="348" rx="24" fill="url(#panelFill)" stroke="#46505A" stroke-width="1.2" filter="url(#panelShadow)"/>
  <text x="80" y="332" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Revenue Velocity</text>
  <text x="80" y="356" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D7DEE6" opacity="0.65">Monthly close volume and forecast trajectory</text>
  <line x1="94" y1="560" x2="590" y2="560" stroke="#5B6670" stroke-width="1"/>
  <line x1="94" y1="500" x2="590" y2="500" stroke="#5B6670" stroke-width="1" stroke-opacity="0.35"/>
  <line x1="94" y1="440" x2="590" y2="440" stroke="#5B6670" stroke-width="1" stroke-opacity="0.35"/>
  <line x1="94" y1="380" x2="590" y2="380" stroke="#5B6670" stroke-width="1" stroke-opacity="0.35"/>
  <path d="M104 560 L104 520 L160 498 L216 510 L272 452 L328 470 L384 418 L440 390 L496 402 L574 338 L574 560 Z"
        fill="url(#areaGreen)"/>
  <path d="M104 520 L160 498 L216 510 L272 452 L328 470 L384 418 L440 390 L496 402 L574 338"
        fill="none" stroke="#DAFF70" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" filter="url(#hudGlow)"/>
  <circle cx="272" cy="452" r="5" fill="#DAFF70"/>
  <circle cx="384" cy="418" r="5" fill="#DAFF70"/>
  <circle cx="574" cy="338" r="6" fill="#DAFF70" filter="url(#hudGlow)"/>
  <text x="92" y="590" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#B7C0C8">JAN</text>
  <text x="278" y="590" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#B7C0C8">JUN</text>
  <text x="526" y="590" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#B7C0C8">DEC</text>

  <rect x="654" y="292" width="274" height="348" rx="24" fill="url(#panelFill)" stroke="#46505A" stroke-width="1.2" filter="url(#panelShadow)"/>
  <text x="680" y="332" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Channel Mix</text>
  <rect x="700" y="520" width="34" height="54" rx="6" fill="#21AE62"/>
  <rect x="752" y="470" width="34" height="104" rx="6" fill="#3CCCD6"/>
  <rect x="804" y="426" width="34" height="148" rx="6" fill="#DAFF70" filter="url(#hudGlow)"/>
  <rect x="856" y="492" width="34" height="82" rx="6" fill="#EF4164"/>
  <line x1="682" y1="574" x2="904" y2="574" stroke="#5B6670" stroke-width="1"/>
  <text x="692" y="598" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#B7C0C8">WEB</text>
  <text x="746" y="598" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#B7C0C8">ABM</text>
  <text x="798" y="598" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#B7C0C8">PART</text>
  <text x="850" y="598" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#B7C0C8">FIELD</text>
  <rect x="684" y="366" width="206" height="18" rx="9" fill="#14171A" stroke="#46505A" stroke-width="1"/>
  <rect x="684" y="366" width="152" height="18" rx="9" fill="#DAFF70"/>
  <text x="684" y="408" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEE6">Partner channel is pacing 31% ahead of plan.</text>

  <rect x="954" y="292" width="212" height="348" rx="24" fill="url(#panelFill)" stroke="#46505A" stroke-width="1.2" filter="url(#panelShadow)"/>
  <text x="978" y="332" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Region Pulse</text>
  <path d="M1018 404 L1058 360 L1108 388 L1092 464 L1032 478 Z"
        fill="#182B2E" stroke="#3CCCD6" stroke-width="2" stroke-opacity="0.75"/>
  <path d="M1036 422 L1062 392 L1088 410 L1078 446 L1046 452 Z"
        fill="#DAFF70" fill-opacity="0.18" stroke="#DAFF70" stroke-width="2" filter="url(#hudGlow)"/>
  <circle cx="1062" cy="392" r="4" fill="#DAFF70"/>
  <circle cx="1078" cy="446" r="4" fill="#DAFF70"/>
  <text x="982" y="524" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEE6">APAC momentum</text>
  <text x="982" y="558" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800"
        fill="#3CCCD6" filter="url(#hudGlow)">+24%</text>
  <rect x="982" y="584" width="140" height="8" rx="4" fill="#14171A"/>
  <rect x="982" y="584" width="106" height="8" rx="4" fill="#3CCCD6"/>
</svg>
```

## Avoid in this skill
- ❌ Using only flat rectangles without glow, gradients, or subtle background HUD detail; the result will feel like a generic dark dashboard rather than a premium command center.
- ❌ Applying filters to `<line>` elements for glowing gridlines; use glow on nearby paths, circles, text, or data traces instead.
- ❌ Overcrowding the slide with tiny tables; this style works best with large KPI numerals, simplified charts, and spacious panels.
- ❌ Using masks or clip paths on non-image elements for HUD effects; keep panels and charts as native editable shapes.
- ❌ Relying on `marker-end` path arrows for callouts; if arrows are needed, use explicit `<line>` elements with marker attributes directly on each line, or draw arrowheads as small paths.

## Composition notes
- Reserve the top 15% for title, status pill, and ambient HUD decoration; keep it lighter than the data zone.
- Use a 3–4 card KPI row across the upper third, then larger chart panels in the lower two-thirds.
- Keep gutters consistent at roughly 24–30 px; dark dashboards need breathing room so glowing accents do not visually merge.
- Use lime as the primary “live data” color and cyan as the secondary signal color; limit pink/yellow to alerts or comparison bars.