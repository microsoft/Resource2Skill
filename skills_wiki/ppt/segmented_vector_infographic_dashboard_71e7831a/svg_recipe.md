# SVG Recipe — Segmented Vector Infographic Dashboard

## Visual mechanism
A premium dashboard split into a bold editorial title rail and a clean white analytics canvas, using custom SVG geometry instead of native chart widgets. Percentages are encoded through segmented radial rings, filled pyramid polygons, and rounded donut arcs so every KPI feels like crafted infographic artwork.

## SVG primitives needed
- 2× `<linearGradient>` for the purple title panel and subtle metric-card highlights
- 1× `<filter id="cardShadow">` applied to white dashboard cards
- 1× `<filter id="softGlow">` applied to the segmented radial chart halo
- 6× `<rect>` for background, title rail, cards, and small label chips
- 9× `<circle>` for dashed ring tracks, donut tracks, and legend dots
- 9× `<path>` for value arcs in the radial and donut charts
- 6× `<path>` for pyramid background triangles and filled trapezoid percentage areas
- 1× decorative `<path>` blob on the title panel
- Multiple `<text>` elements with explicit `width` for title, labels, percentages, and captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="purplePanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7A63E8"/>
      <stop offset="55%" stop-color="#6F59D1"/>
      <stop offset="100%" stop-color="#4D3DA8"/>
    </linearGradient>
    <linearGradient id="cardFade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7F8FF"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F3F5FB"/>
  <rect x="0" y="0" width="410" height="720" fill="url(#purplePanel)"/>
  <path d="M-30 580 C85 520 150 645 260 570 C345 512 350 392 465 420 L465 740 L-30 740 Z" fill="#8F7CFF" opacity="0.22"/>
  <circle cx="86" cy="92" r="7" fill="#FFFFFF" opacity="0.85"/>
  <circle cx="117" cy="92" r="7" fill="#FFFFFF" opacity="0.5"/>
  <circle cx="148" cy="92" r="7" fill="#FFFFFF" opacity="0.28"/>

  <text x="58" y="188" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="600" fill="#DED8FF" letter-spacing="3">Q4 INTELLIGENCE</text>
  <text x="56" y="268" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="66" font-weight="800" fill="#FFFFFF">Segmented</text>
  <text x="56" y="342" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="66" font-weight="800" fill="#FFFFFF">Vector</text>
  <text x="58" y="404" width="295" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="500" fill="#E9E5FF">Infographic dashboard for executive KPI reporting</text>
  <rect x="58" y="548" width="244" height="52" rx="26" fill="#FFFFFF" opacity="0.18"/>
  <text x="84" y="582" width="195" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">LIVE KPI SNAPSHOT</text>

  <rect x="450" y="46" width="774" height="170" rx="28" fill="url(#cardFade)" filter="url(#cardShadow)"/>
  <rect x="450" y="254" width="774" height="190" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="450" y="482" width="774" height="168" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <text x="486" y="92" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#32323C">Market Momentum</text>
  <text x="486" y="122" width="305" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8C91A3">Three concentric segmented rings compare adoption, retention, and share.</text>

  <circle cx="756" cy="132" r="105" fill="none" stroke="#F0F1F6" stroke-width="22" stroke-dasharray="10 8"/>
  <circle cx="756" cy="132" r="78" fill="none" stroke="#F0F1F6" stroke-width="20" stroke-dasharray="9 7"/>
  <circle cx="756" cy="132" r="52" fill="none" stroke="#F0F1F6" stroke-width="18" stroke-dasharray="8 6"/>
  <circle cx="756" cy="132" r="108" fill="none" stroke="#6F59D1" stroke-width="4" opacity="0.18" filter="url(#softGlow)"/>
  <path d="M756 27 A105 105 0 1 1 656 165" fill="none" stroke="#6F59D1" stroke-width="22" stroke-dasharray="12 8" stroke-linecap="butt"/>
  <path d="M756 54 A78 78 0 1 1 679 146" fill="none" stroke="#86C58B" stroke-width="20" stroke-dasharray="10 7" stroke-linecap="butt"/>
  <path d="M756 80 A52 52 0 1 1 731 178" fill="none" stroke="#798EE5" stroke-width="18" stroke-dasharray="9 6" stroke-linecap="butt"/>

  <text x="724" y="127" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#32323C">80%</text>
  <text x="722" y="151" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8C91A3" letter-spacing="1.5">INDEX</text>

  <circle cx="976" cy="92" r="7" fill="#6F59D1"/>
  <text x="994" y="98" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#555B6B">Adoption 80%</text>
  <circle cx="976" cy="126" r="7" fill="#86C58B"/>
  <text x="994" y="132" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#555B6B">Retention 72%</text>
  <circle cx="976" cy="160" r="7" fill="#798EE5"/>
  <text x="994" y="166" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#555B6B">Share 58%</text>

  <text x="486" y="304" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#32323C">Pipeline Shape</text>
  <text x="486" y="332" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8C91A3">Filled pyramids show stage completion from base to apex.</text>

  <path d="M545 418 L655 418 L600 288 Z" fill="#ECEEF3"/>
  <path d="M545 418 L655 418 L615 324 L585 324 Z" fill="#6F59D1"/>
  <text x="564" y="460" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" text-anchor="middle" fill="#32323C">72%</text>
  <text x="552" y="486" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#8C91A3">Qualified</text>

  <path d="M700 418 L810 418 L755 288 Z" fill="#ECEEF3"/>
  <path d="M700 418 L810 418 L785 358 L725 358 Z" fill="#86C58B"/>
  <text x="719" y="460" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" text-anchor="middle" fill="#32323C">54%</text>
  <text x="707" y="486" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#8C91A3">Negotiated</text>

  <path d="M855 418 L965 418 L910 288 Z" fill="#ECEEF3"/>
  <path d="M855 418 L965 418 L945 369 L875 369 Z" fill="#798EE5"/>
  <text x="874" y="460" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" text-anchor="middle" fill="#32323C">38%</text>
  <text x="862" y="486" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#8C91A3">Closed Won</text>

  <rect x="1030" y="304" width="124" height="42" rx="21" fill="#F2F0FF"/>
  <text x="1053" y="331" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#6F59D1">+12.4%</text>
  <text x="1028" y="374" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8C91A3">MoM conversion lift</text>

  <text x="486" y="530" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#32323C">Operating Health</text>

  <circle cx="604" cy="582" r="48" fill="none" stroke="#ECEEF3" stroke-width="16"/>
  <path d="M604 534 A48 48 0 1 1 564 556" fill="none" stroke="#6F59D1" stroke-width="16" stroke-linecap="round"/>
  <text x="574" y="590" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="800" text-anchor="middle" fill="#32323C">84</text>
  <text x="552" y="642" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#8C91A3">Velocity</text>

  <circle cx="764" cy="582" r="48" fill="none" stroke="#ECEEF3" stroke-width="16"/>
  <path d="M764 534 A48 48 0 1 1 722 605" fill="none" stroke="#86C58B" stroke-width="16" stroke-linecap="round"/>
  <text x="734" y="590" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="800" text-anchor="middle" fill="#32323C">67</text>
  <text x="712" y="642" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#8C91A3">Efficiency</text>

  <circle cx="924" cy="582" r="48" fill="none" stroke="#ECEEF3" stroke-width="16"/>
  <path d="M924 534 A48 48 0 0 1 947 624" fill="none" stroke="#798EE5" stroke-width="16" stroke-linecap="round"/>
  <text x="894" y="590" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="800" text-anchor="middle" fill="#32323C">42</text>
  <text x="872" y="642" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#8C91A3">Risk Buffer</text>

  <rect x="1030" y="544" width="128" height="62" rx="18" fill="#F7F8FF"/>
  <text x="1054" y="570" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8C91A3">Composite</text>
  <text x="1052" y="596" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#32323C">73.1</text>
</svg>
```

## Avoid in this skill
- ❌ Rasterizing the circular charts into PNG if editability is required; use dashed `<circle>` tracks and stroked `<path>` arcs instead.
- ❌ Native PowerPoint chart objects for this look; they will feel generic and will not reproduce the segmented editorial geometry.
- ❌ Applying `filter` to `<line>` elements for connector effects; use filtered cards or paths instead.
- ❌ Using `<mask>` or clip-path on non-image elements to fake percentage fills; construct filled trapezoids as explicit `<path>` geometry.
- ❌ Overcrowding the white canvas with too many numeric callouts; the premium effect relies on generous spacing between chart families.

## Composition notes
- Keep the left 30–35% of the slide as a saturated title rail; it anchors the dashboard and creates strong keynote-style contrast.
- Reserve the right canvas for three horizontal information bands: radial summary at top, pyramids in the middle, donut health metrics at bottom.
- Use one accent color per KPI family, then repeat those colors consistently in legends, fills, arcs, and callout chips.
- Maintain wide gutters between chart groups; the dashboard should feel like an infographic poster, not a dense BI screen.