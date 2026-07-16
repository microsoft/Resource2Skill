# SVG Recipe — Modern Dashboard Card Layout

## Visual mechanism
A data-heavy report becomes a premium software dashboard by floating rounded dark cards above an ambient gradient background, with strict gutters, consistent internal padding, and subtle shadows. Small neon accents, mini charts, and table-like rows create an executive KPI interface without overwhelming the slide.

## SVG primitives needed
- 1× full-slide `<rect>` for the ambient gradient background
- 3× blurred `<circle>` elements for soft teal/blue/purple glow fields behind the dashboard
- 1× large rounded `<rect>` for the main dashboard shell
- 4× rounded `<rect>` KPI cards across the top row
- 3× rounded `<rect>` larger analytic cards across the bottom row
- Multiple small `<rect>` elements for bar charts, progress bars, table rows, pills, and separators
- Multiple `<line>` elements for chart gridlines and simple axes
- 4× stroked `<path>` elements for sparklines and trend curves
- Multiple `<circle>` elements for legend dots, chart markers, and status indicators
- Multiple `<text>` elements with explicit `width` attributes for all labels, titles, values, and axis captions
- 1× `<linearGradient>` for the background
- 3× `<radialGradient>` definitions for ambient glow accents
- 1× `<filter id="cardShadow">` for soft card elevation
- 1× `<filter id="softGlow">` for blurred atmospheric circles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#122D34"/>
      <stop offset="45%" stop-color="#101827"/>
      <stop offset="100%" stop-color="#070B14"/>
    </linearGradient>
    <radialGradient id="tealGlow">
      <stop offset="0%" stop-color="#38FFD6" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#38FFD6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blueGlow">
      <stop offset="0%" stop-color="#5C7CFF" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#5C7CFF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="violetGlow">
      <stop offset="0%" stop-color="#B15CFF" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#B15CFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="32"/>
    </filter>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="140" cy="90" r="230" fill="url(#tealGlow)" filter="url(#softGlow)"/>
  <circle cx="1110" cy="150" r="260" fill="url(#blueGlow)" filter="url(#softGlow)"/>
  <circle cx="900" cy="680" r="260" fill="url(#violetGlow)" filter="url(#softGlow)"/>

  <text x="70" y="62" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">Performance Tracking 2024</text>
  <text x="70" y="92" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A7B5C8">Executive dashboard · refreshed 09:30 UTC</text>
  <rect x="1030" y="42" width="178" height="38" rx="19" fill="#14212D" stroke="#2A3C4F"/>
  <circle cx="1054" cy="61" r="5" fill="#29FFB4"/>
  <text x="1070" y="67" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#DFFCF4">Live reporting</text>

  <rect x="56" y="116" width="1168" height="548" rx="28" fill="#0E1620" opacity="0.70" stroke="#263949"/>
  <rect x="80" y="140" width="260" height="112" rx="18" fill="#252B31" filter="url(#cardShadow)"/>
  <rect x="360" y="140" width="260" height="112" rx="18" fill="#252B31" filter="url(#cardShadow)"/>
  <rect x="640" y="140" width="260" height="112" rx="18" fill="#252B31" filter="url(#cardShadow)"/>
  <rect x="920" y="140" width="260" height="112" rx="18" fill="#252B31" filter="url(#cardShadow)"/>

  <text x="104" y="171" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A8B0BA">Total sales</text>
  <text x="104" y="210" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">$95M</text>
  <text x="245" y="210" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#35F0B0">+12.4%</text>
  <path d="M104 230 C130 214, 150 226, 170 210 S218 218, 242 196 S285 198, 314 178" fill="none" stroke="#35F0B0" stroke-width="4" stroke-linecap="round"/>

  <text x="384" y="171" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A8B0BA">Units sold</text>
  <text x="384" y="210" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">1,535</text>
  <text x="525" y="210" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6BD7FF">+8.1%</text>
  <rect x="384" y="228" width="188" height="8" rx="4" fill="#111820"/>
  <rect x="384" y="228" width="138" height="8" rx="4" fill="#6BD7FF"/>

  <text x="664" y="171" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A8B0BA">New accounts</text>
  <text x="664" y="210" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">1,481</text>
  <text x="805" y="210" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFD166">+5.7%</text>
  <circle cx="678" cy="232" r="6" fill="#FFD166"/>
  <circle cx="700" cy="232" r="6" fill="#FFD166" opacity="0.75"/>
  <circle cx="722" cy="232" r="6" fill="#FFD166" opacity="0.45"/>

  <text x="944" y="171" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A8B0BA">Average age</text>
  <text x="944" y="210" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">46 yrs</text>
  <text x="1080" y="210" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A8B0BA">stable</text>
  <rect x="944" y="226" width="184" height="10" rx="5" fill="#111820"/>
  <rect x="944" y="226" width="108" height="10" rx="5" fill="#B15CFF"/>

  <rect x="80" y="280" width="344" height="348" rx="20" fill="#252B31" filter="url(#cardShadow)"/>
  <rect x="452" y="280" width="344" height="348" rx="20" fill="#252B31" filter="url(#cardShadow)"/>
  <rect x="824" y="280" width="356" height="348" rx="20" fill="#252B31" filter="url(#cardShadow)"/>

  <text x="108" y="320" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Sales by category</text>
  <circle cx="108" cy="344" r="5" fill="#35F0B0"/>
  <text x="120" y="349" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A8B0BA">Automotive</text>
  <circle cx="214" cy="344" r="5" fill="#6BD7FF"/>
  <text x="226" y="349" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A8B0BA">Leasing</text>
  <line x1="116" y1="562" x2="382" y2="562" stroke="#3A424B" stroke-width="1"/>
  <line x1="116" y1="494" x2="382" y2="494" stroke="#333B43" stroke-width="1"/>
  <line x1="116" y1="426" x2="382" y2="426" stroke="#333B43" stroke-width="1"/>
  <rect x="142" y="398" width="32" height="164" rx="5" fill="#35F0B0"/>
  <rect x="184" y="438" width="32" height="124" rx="5" fill="#6BD7FF" opacity="0.75"/>
  <rect x="244" y="374" width="32" height="188" rx="5" fill="#35F0B0"/>
  <rect x="286" y="416" width="32" height="146" rx="5" fill="#6BD7FF" opacity="0.75"/>
  <text x="146" y="588" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A8B0BA">SUV</text>
  <text x="252" y="588" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A8B0BA">EV</text>

  <text x="480" y="320" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Monthly trend</text>
  <line x1="500" y1="562" x2="758" y2="562" stroke="#3A424B" stroke-width="1"/>
  <line x1="500" y1="502" x2="758" y2="502" stroke="#333B43" stroke-width="1"/>
  <line x1="500" y1="442" x2="758" y2="442" stroke="#333B43" stroke-width="1"/>
  <line x1="500" y1="382" x2="758" y2="382" stroke="#333B43" stroke-width="1"/>
  <path d="M502 516 C535 482, 558 502, 584 466 S636 438, 662 456 S718 470, 756 408" fill="none" stroke="#35F0B0" stroke-width="4" stroke-linecap="round"/>
  <path d="M502 544 C536 534, 560 550, 586 526 S636 512, 666 532 S720 542, 756 520" fill="none" stroke="#6BD7FF" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
  <circle cx="584" cy="466" r="5" fill="#35F0B0"/>
  <circle cx="662" cy="456" r="5" fill="#35F0B0"/>
  <circle cx="756" cy="408" r="5" fill="#35F0B0"/>
  <text x="498" y="592" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#A8B0BA">Jan</text>
  <text x="582" y="592" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#A8B0BA">Mar</text>
  <text x="668" y="592" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#A8B0BA">May</text>
  <text x="736" y="592" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#A8B0BA">Jul</text>

  <text x="852" y="320" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Regional pipeline</text>
  <rect x="852" y="352" width="292" height="1" fill="#39424C"/>
  <text x="852" y="382" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D9E2EC">North</text>
  <rect x="950" y="368" width="178" height="12" rx="6" fill="#111820"/>
  <rect x="950" y="368" width="146" height="12" rx="6" fill="#35F0B0"/>
  <text x="1138" y="381" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A8B0BA">82%</text>
  <text x="852" y="426" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D9E2EC">West</text>
  <rect x="950" y="412" width="178" height="12" rx="6" fill="#111820"/>
  <rect x="950" y="412" width="122" height="12" rx="6" fill="#6BD7FF"/>
  <text x="1138" y="425" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A8B0BA">69%</text>
  <text x="852" y="470" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D9E2EC">Central</text>
  <rect x="950" y="456" width="178" height="12" rx="6" fill="#111820"/>
  <rect x="950" y="456" width="96" height="12" rx="6" fill="#FFD166"/>
  <text x="1138" y="469" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A8B0BA">54%</text>
  <text x="852" y="514" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D9E2EC">South</text>
  <rect x="950" y="500" width="178" height="12" rx="6" fill="#111820"/>
  <rect x="950" y="500" width="156" height="12" rx="6" fill="#B15CFF"/>
  <text x="1138" y="513" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A8B0BA">88%</text>
  <rect x="852" y="548" width="292" height="44" rx="12" fill="#111820" stroke="#314153"/>
  <text x="872" y="575" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D9E2EC">Forecast confidence</text>
  <text x="1080" y="576" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#35F0B0">High</text>
</svg>
```

## Avoid in this skill
- ❌ Using a plain white background with ungrouped numbers; the technique depends on visible card hierarchy and depth.
- ❌ Applying filters to `<line>` chart gridlines or axes; use filters only on card rectangles, glows, paths, circles, or text.
- ❌ Overfilling every card with dense table text; dashboard cards need internal padding and selective detail.
- ❌ Inconsistent gutters between cards; misalignment immediately breaks the premium software-interface feel.
- ❌ Using `<foreignObject>` for HTML tables; recreate tables with editable SVG text, lines, and rectangles instead.

## Composition notes
- Keep a strong grid: outer margins around 56–80 px, card gutters around 24–32 px, and consistent internal padding around 24–28 px.
- Use the top row for fast KPI recognition, then reserve the lower row for charts, tables, or ranking cards.
- The background should stay dark and atmospheric; the cards are the readable surface, while neon accents should be limited to data highlights.
- Let shadows and rounded corners create depth, but keep them subtle so the dashboard feels executive rather than decorative.