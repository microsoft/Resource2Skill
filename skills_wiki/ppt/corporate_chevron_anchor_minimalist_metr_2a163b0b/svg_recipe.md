# SVG Recipe — Corporate Chevron Anchor & Minimalist Metric Cards

## Visual mechanism
A bold left-anchored chevron banner establishes hierarchy and forward motion, while clean white metric cards organize dense business data into executive-readable modules. The premium feel comes from restrained corporate colors, subtle shadows, thin dividers, compact chart shapes, and generous negative space.

## SVG primitives needed
- 1× `<rect>` full-slide off-white background with a soft gradient
- 2× `<path>` left-edge chevron banners for section anchoring and directional emphasis
- 1× `<path>` oversized low-opacity decorative chevron in the background
- 6× `<rect>` rounded metric cards with subtle shadow
- Multiple `<rect>` elements for progress bars, card accents, mini table rows, and small status chips
- Multiple `<text>` elements with explicit `width` attributes for headers, KPI values, labels, and annotations
- 4× `<path>` sparkline / trend-line microcharts inside cards
- 1× `<circle>` / `<ellipse>` cluster for compact KPI status indicators
- 1× `<linearGradient>` for the slide background
- 2× `<linearGradient>` fills for teal and orange chevron accents
- 1× `<filter id="cardShadow">` applied to cards
- 1× `<filter id="softGlow">` applied to selected accent shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="55%" stop-color="#F7F9FA"/>
      <stop offset="100%" stop-color="#EEF3F5"/>
    </linearGradient>
    <linearGradient id="tealAnchor" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#102B38"/>
      <stop offset="100%" stop-color="#1B3C4B"/>
    </linearGradient>
    <linearGradient id="orangeAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F39C12"/>
      <stop offset="100%" stop-color="#FFB84A"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.06  0 0 0 0 0.12  0 0 0 0 0.16  0 0 0 .16 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M870 78 L1220 78 L1280 132 L1220 186 L870 186 L930 132 Z" fill="#1B3C4B" opacity="0.045"/>
  <path d="M0 52 H330 L392 94 L330 136 H0 Z" fill="url(#tealAnchor)"/>
  <path d="M0 146 H206 L250 176 L206 206 H0 Z" fill="url(#orangeAccent)" filter="url(#softGlow)" opacity="0.95"/>

  <text x="42" y="103" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF" letter-spacing="1.5">Q3 BUSINESS REVIEW</text>
  <text x="42" y="184" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="1">FINANCE UPDATE</text>

  <text x="430" y="76" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#24323A">Executive performance dashboard</text>
  <text x="432" y="112" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#687882">Monthly operating metrics, revenue quality, and delivery confidence snapshot</text>
  <rect x="1084" y="62" width="126" height="34" rx="17" fill="#E8F6F8" stroke="#B8E3EA"/>
  <circle cx="1107" cy="79" r="5" fill="#17A2B8"/>
  <text x="1121" y="85" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1B3C4B">ON TRACK</text>

  <rect x="54" y="252" width="348" height="172" rx="18" fill="#FFFFFF" stroke="#DDE5E8" filter="url(#cardShadow)"/>
  <rect x="54" y="252" width="6" height="172" rx="3" fill="#17A2B8"/>
  <text x="82" y="288" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#5D6D75" letter-spacing=".6">NET REVENUE</text>
  <text x="82" y="343" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700" fill="#263238">$42.8M</text>
  <text x="257" y="326" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#17A2B8">▲ 12.4%</text>
  <path d="M82 382 C122 354, 150 392, 188 366 S252 344, 320 366" fill="none" stroke="#17A2B8" stroke-width="4" stroke-linecap="round"/>
  <text x="82" y="409" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7E8D94">Above plan, driven by enterprise renewals</text>

  <rect x="430" y="252" width="348" height="172" rx="18" fill="#FFFFFF" stroke="#DDE5E8" filter="url(#cardShadow)"/>
  <rect x="430" y="252" width="6" height="172" rx="3" fill="#F39C12"/>
  <text x="458" y="288" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#5D6D75" letter-spacing=".6">OPERATING MARGIN</text>
  <text x="458" y="343" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700" fill="#263238">28.6%</text>
  <text x="626" y="326" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#F39C12">▲ 3.1 pts</text>
  <rect x="458" y="376" width="252" height="12" rx="6" fill="#EEF2F4"/>
  <rect x="458" y="376" width="186" height="12" rx="6" fill="#F39C12"/>
  <text x="458" y="409" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7E8D94">Efficiency gains offset higher field investment</text>

  <rect x="806" y="252" width="420" height="172" rx="18" fill="#FFFFFF" stroke="#DDE5E8" filter="url(#cardShadow)"/>
  <text x="836" y="288" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#5D6D75" letter-spacing=".6">PIPELINE COVERAGE</text>
  <text x="836" y="344" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700" fill="#263238">3.4×</text>
  <circle cx="1078" cy="331" r="43" fill="#E8F6F8" stroke="#17A2B8" stroke-width="10"/>
  <circle cx="1078" cy="331" r="24" fill="#FFFFFF"/>
  <text x="1054" y="338" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1B3C4B">82%</text>
  <rect x="836" y="376" width="312" height="1" fill="#E2E8EA"/>
  <text x="836" y="409" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7E8D94">Coverage supports Q4 target with moderate risk</text>

  <rect x="54" y="454" width="536" height="196" rx="18" fill="#FFFFFF" stroke="#DDE5E8" filter="url(#cardShadow)"/>
  <text x="84" y="493" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#263238">Regional attainment</text>
  <text x="84" y="520" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7E8D94">Quota progress by operating theater</text>
  <rect x="86" y="548" width="390" height="12" rx="6" fill="#EDF2F4"/>
  <rect x="86" y="548" width="330" height="12" rx="6" fill="#17A2B8"/>
  <text x="492" y="561" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#263238">85%</text>
  <rect x="86" y="584" width="390" height="12" rx="6" fill="#EDF2F4"/>
  <rect x="86" y="584" width="277" height="12" rx="6" fill="#F39C12"/>
  <text x="492" y="597" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#263238">71%</text>
  <rect x="86" y="620" width="390" height="12" rx="6" fill="#EDF2F4"/>
  <rect x="86" y="620" width="347" height="12" rx="6" fill="#1B3C4B"/>
  <text x="492" y="633" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#263238">89%</text>

  <rect x="620" y="454" width="606" height="196" rx="18" fill="#FFFFFF" stroke="#DDE5E8" filter="url(#cardShadow)"/>
  <text x="650" y="493" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#263238">Strategic initiatives</text>
  <text x="650" y="520" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7E8D94">Milestone confidence and executive attention areas</text>
  <rect x="650" y="546" width="526" height="1" fill="#E2E8EA"/>
  <text x="650" y="579" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#263238">Cloud migration</text>
  <rect x="922" y="559" width="120" height="24" rx="12" fill="#E8F6F8"/>
  <text x="951" y="576" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#17A2B8">GREEN</text>
  <path d="M1064 574 C1092 552, 1118 586, 1148 562" fill="none" stroke="#17A2B8" stroke-width="3" stroke-linecap="round"/>
  <text x="650" y="622" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#263238">Pricing redesign</text>
  <rect x="922" y="602" width="120" height="24" rx="12" fill="#FFF3DF"/>
  <text x="950" y="619" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#D47B00">WATCH</text>
  <path d="M1064 616 C1090 602, 1118 604, 1148 624" fill="none" stroke="#F39C12" stroke-width="3" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Using plain rectangular section headers; the left-side pentagon/chevron is the signature visual anchor.
- ❌ Heavy charting or dense axes inside cards; keep charts as micro-visuals so the dashboard remains executive-readable.
- ❌ Applying shadows to `<line>` elements; use card-level `<rect>` shadows and path-based sparklines instead.
- ❌ Overusing bright accents across every element; reserve cyan/orange for KPI emphasis, progress, and status signaling.
- ❌ Omitting explicit `width` on `<text>` elements; this can cause unpredictable text layout in PowerPoint.

## Composition notes
- Place the chevron banner flush to the left edge, roughly 7–18% from the top, so it feels like a structural slide anchor rather than a label.
- Keep metric cards aligned to a strict grid with 24–32 px gutters and generous internal padding.
- Use white cards on an off-white background; rely on subtle borders and shadows instead of heavy outlines.
- Maintain a left-to-right reading rhythm: chevron title → slide heading → KPI card row → deeper operational cards.