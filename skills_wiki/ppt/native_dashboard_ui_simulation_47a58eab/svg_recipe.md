# SVG Recipe — Native Dashboard UI Simulation

## Visual mechanism
A static slide is composed to look like a live BI application: a persistent top app bar, clickable-looking tabs, KPI cards, a large central chart canvas, and a right-side filter/slicer panel. Subtle lavender background, white floating cards, soft shadows, and restrained purple/blue accents create the “native dashboard” illusion while remaining fully editable.

## SVG primitives needed
- 1× `<rect>` for the tinted slide background
- 1× `<rect>` for the white top application header
- 4× `<rect>` for tab navigation pills, with the active tab in dark purple
- 4× `<rect>` for KPI card containers
- 1× `<rect>` for the main chart card
- 1× `<rect>` for the right filter panel card
- Multiple small `<rect>` elements for slicer buttons, checkbox controls, mini status chips, and chart legend swatches
- Multiple `<line>` elements for chart gridlines, axes, and table dividers
- Several `<path>` elements for the area chart, line chart, mini sparklines, UI icons, and decorative app glyph
- Multiple `<circle>` elements for chart data points and checkbox ticks
- Multiple `<text>` elements with explicit `width` attributes for dashboard title, tabs, KPI values, filters, labels, axis ticks, and table content
- 2× `<linearGradient>` for branded app icon and chart area fill
- 1× `<filter id="cardShadow">` for soft dashboard card shadows
- 1× `<filter id="softGlow">` for subtle active-state emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="brandGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6F6FE8"/>
      <stop offset="100%" stop-color="#373787"/>
    </linearGradient>
    <linearGradient id="areaGrad" x1="0" y1="270" x2="0" y2="610">
      <stop offset="0%" stop-color="#5B61D6" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#5B61D6" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="profitGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#28A6FF"/>
      <stop offset="100%" stop-color="#6C5CE7"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="7"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#EBEBF5"/>

  <rect x="0" y="0" width="1280" height="64" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="28" y="15" width="34" height="34" rx="8" fill="url(#brandGrad)"/>
  <path d="M37 40 L37 28 L45 28 L45 40 Z M49 40 L49 21 L57 21 L57 40 Z" fill="#FFFFFF"/>
  <text x="76" y="40" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#464696">OfficePlus California Sales</text>
  <text x="1040" y="27" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#767692">Updated 08:45 AM</text>
  <rect x="1190" y="18" width="26" height="26" rx="13" fill="#F1F1FA"/>
  <circle cx="1203" cy="31" r="4" fill="#464696"/>
  <rect x="1226" y="18" width="26" height="26" rx="13" fill="#F1F1FA"/>
  <path d="M1234 31 L1240 25 L1246 31 L1240 37 Z" fill="#464696"/>

  <rect x="32" y="78" width="142" height="34" rx="7" fill="#464696" filter="url(#softGlow)"/>
  <text x="32" y="100" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Overview</text>
  <rect x="184" y="78" width="142" height="34" rx="7" fill="#D7D7EA"/>
  <text x="184" y="100" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#464696">Products</text>
  <rect x="336" y="78" width="142" height="34" rx="7" fill="#D7D7EA"/>
  <text x="336" y="100" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#464696">Customers</text>
  <rect x="488" y="78" width="164" height="34" rx="7" fill="#D7D7EA"/>
  <text x="488" y="100" width="164" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#464696">Online vs Store</text>

  <rect x="32" y="126" width="226" height="108" rx="16" fill="#FFFFFF" stroke="#D9D9E8" filter="url(#cardShadow)"/>
  <text x="52" y="154" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#74748B">Total Sales</text>
  <text x="52" y="194" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#252538">$225.44K</text>
  <rect x="52" y="207" width="74" height="16" rx="8" fill="#EAF7F0"/>
  <text x="62" y="219" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#18A058">▲ 8.3%</text>
  <path d="M190 205 C204 188 216 194 235 174" fill="none" stroke="#18A058" stroke-width="3"/>

  <rect x="282" y="126" width="226" height="108" rx="16" fill="#FFFFFF" stroke="#D9D9E8" filter="url(#cardShadow)"/>
  <text x="302" y="154" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#74748B">Profit</text>
  <text x="302" y="194" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#252538">$44.98K</text>
  <rect x="302" y="207" width="78" height="16" rx="8" fill="#EEF2FF"/>
  <text x="312" y="219" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#464696">● Stable</text>
  <path d="M435 210 C448 198 461 203 484 185" fill="none" stroke="#5B61D6" stroke-width="3"/>

  <rect x="532" y="126" width="226" height="108" rx="16" fill="#FFFFFF" stroke="#D9D9E8" filter="url(#cardShadow)"/>
  <text x="552" y="154" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#74748B">Margin</text>
  <text x="552" y="194" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#252538">19.95%</text>
  <rect x="552" y="207" width="86" height="16" rx="8" fill="#F7F0EA"/>
  <text x="562" y="219" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#C9822D">▼ 1.1 pts</text>
  <path d="M685 180 L705 180 L705 210 L685 210 Z M712 160 L732 160 L732 210 L712 210 Z" fill="#F0B44E"/>

  <rect x="782" y="126" width="226" height="108" rx="16" fill="#FFFFFF" stroke="#D9D9E8" filter="url(#cardShadow)"/>
  <text x="802" y="154" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#74748B">MoM Change</text>
  <text x="802" y="194" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#C73535">-12.17%</text>
  <rect x="802" y="207" width="90" height="16" rx="8" fill="#FCECEC"/>
  <text x="812" y="219" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#C73535">Below plan</text>
  <path d="M930 180 C948 176 960 198 982 190" fill="none" stroke="#C73535" stroke-width="3"/>

  <rect x="32" y="258" width="976" height="412" rx="18" fill="#FFFFFF" stroke="#D9D9E8" filter="url(#cardShadow)"/>
  <text x="56" y="292" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#252538">Total Sales by Month and Channel</text>
  <text x="56" y="314" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A7A92">Minimal Power BI-style visual with editable native lines, paths, points, and labels</text>
  <rect x="804" y="278" width="12" height="12" rx="2" fill="#5B61D6"/>
  <text x="824" y="289" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#62627A">Online</text>
  <rect x="894" y="278" width="12" height="12" rx="2" fill="url(#profitGrad)"/>
  <text x="914" y="289" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#62627A">Store</text>

  <line x1="82" y1="600" x2="950" y2="600" stroke="#E7E7F1" stroke-width="1"/>
  <line x1="82" y1="535" x2="950" y2="535" stroke="#E7E7F1" stroke-width="1"/>
  <line x1="82" y1="470" x2="950" y2="470" stroke="#E7E7F1" stroke-width="1"/>
  <line x1="82" y1="405" x2="950" y2="405" stroke="#E7E7F1" stroke-width="1"/>
  <line x1="82" y1="340" x2="950" y2="340" stroke="#E7E7F1" stroke-width="1"/>
  <line x1="82" y1="600" x2="82" y2="340" stroke="#D5D5E6" stroke-width="1"/>
  <line x1="82" y1="600" x2="950" y2="600" stroke="#D5D5E6" stroke-width="1"/>

  <text x="50" y="604" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A" text-anchor="end">$0</text>
  <text x="50" y="539" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A" text-anchor="end">$50K</text>
  <text x="50" y="474" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A" text-anchor="end">$100K</text>
  <text x="50" y="409" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A" text-anchor="end">$150K</text>
  <text x="50" y="344" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A" text-anchor="end">$200K</text>

  <path d="M82 548 C150 520 198 512 255 480 C318 443 370 464 430 424 C495 381 558 395 620 366 C690 333 742 354 805 318 C860 286 905 306 950 274 L950 600 L82 600 Z" fill="url(#areaGrad)"/>
  <path d="M82 548 C150 520 198 512 255 480 C318 443 370 464 430 424 C495 381 558 395 620 366 C690 333 742 354 805 318 C860 286 905 306 950 274" fill="none" stroke="#5B61D6" stroke-width="4"/>
  <path d="M82 566 C150 552 199 540 255 528 C318 507 370 520 430 486 C495 455 558 472 620 438 C690 408 742 421 805 392 C860 368 905 376 950 348" fill="none" stroke="#28A6FF" stroke-width="4"/>
  <circle cx="255" cy="480" r="5" fill="#FFFFFF" stroke="#5B61D6" stroke-width="3"/>
  <circle cx="430" cy="424" r="5" fill="#FFFFFF" stroke="#5B61D6" stroke-width="3"/>
  <circle cx="620" cy="366" r="5" fill="#FFFFFF" stroke="#5B61D6" stroke-width="3"/>
  <circle cx="805" cy="318" r="5" fill="#FFFFFF" stroke="#5B61D6" stroke-width="3"/>
  <circle cx="950" cy="274" r="5" fill="#FFFFFF" stroke="#5B61D6" stroke-width="3"/>

  <text x="80" y="624" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A">Jan</text>
  <text x="225" y="624" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A">Mar</text>
  <text x="400" y="624" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A">May</text>
  <text x="590" y="624" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A">Jul</text>
  <text x="775" y="624" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A">Sep</text>
  <text x="920" y="624" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#88889A">Nov</text>

  <rect x="1032" y="126" width="216" height="544" rx="18" fill="#FFFFFF" stroke="#D9D9E8" filter="url(#cardShadow)"/>
  <text x="1056" y="160" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#252538">Filters</text>
  <text x="1056" y="188" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#74748B">Report slicers</text>
  <line x1="1056" y1="210" x2="1224" y2="210" stroke="#E7E7F1" stroke-width="1"/>

  <text x="1056" y="240" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#464696">Department</text>
  <rect x="1056" y="256" width="76" height="28" rx="6" fill="#464696"/>
  <text x="1066" y="275" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#FFFFFF">Office</text>
  <rect x="1140" y="256" width="84" height="28" rx="6" fill="#EFEFF8"/>
  <text x="1150" y="275" width="66" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#55556C">Creative</text>
  <rect x="1056" y="292" width="76" height="28" rx="6" fill="#EFEFF8"/>
  <text x="1066" y="311" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#55556C">Tech</text>
  <rect x="1140" y="292" width="84" height="28" rx="6" fill="#EFEFF8"/>
  <text x="1150" y="311" width="66" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#55556C">Sports</text>

  <text x="1056" y="356" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#464696">Sales Channel</text>
  <rect x="1056" y="374" width="14" height="14" rx="3" fill="#464696"/>
  <path d="M1059 381 L1064 386 L1071 377" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="1080" y="386" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#3D3D4D">Online Purchase</text>
  <rect x="1056" y="402" width="14" height="14" rx="3" fill="#464696"/>
  <path d="M1059 409 L1064 414 L1071 405" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="1080" y="414" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#3D3D4D">Store Purchase</text>

  <text x="1056" y="462" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#464696">Top Customer Locations</text>
  <line x1="1056" y1="484" x2="1224" y2="484" stroke="#E7E7F1" stroke-width="1"/>
  <text x="1056" y="506" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#3D3D4D">Colorado</text>
  <text x="1160" y="506" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#3D3D4D" text-anchor="end">$810</text>
  <line x1="1056" y1="518" x2="1224" y2="518" stroke="#EFEFF6" stroke-width="1"/>
  <text x="1056" y="540" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#3D3D4D">Des Moines</text>
  <text x="1160" y="540" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#3D3D4D" text-anchor="end">$1,339</text>
  <line x1="1056" y1="552" x2="1224" y2="552" stroke="#EFEFF6" stroke-width="1"/>
  <text x="1056" y="574" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#3D3D4D">Forest Hills</text>
  <text x="1160" y="574" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#3D3D4D" text-anchor="end">$659</text>

  <rect x="1056" y="612" width="168" height="32" rx="8" fill="#F1F1FA"/>
  <text x="1070" y="633" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#464696">Reset all filters</text>
</svg>
```

## Avoid in this skill
- ❌ Embedding a screenshot of a dashboard as the main content; it defeats editability and makes numbers impossible to update.
- ❌ Heavy axis styling, dense legends, or Excel-like chart chrome; modern BI simulations need restrained UI detail.
- ❌ `clip-path` on non-image dashboard cards or chart paths; use normal rectangles, paths, and lines instead.
- ❌ `marker-end` arrows for UI affordances; if arrows are needed, draw them as simple paths or lines without markers.
- ❌ Too many saturated colors at once; reserve the brand purple/blue for active UI, key chart lines, and selected filters.

## Composition notes
- Keep the top 15% reserved for the app header and tab navigation so the slide immediately reads as software, not a normal report page.
- Use a 4-card KPI row beneath the tabs; values should be large, sparse, and easy to scan from a distance.
- Allocate roughly 75–80% of the lower width to the primary visualization and 15–20% to the right filter panel.
- Maintain generous gutters, pale lavender background, and consistent shadow depth so the white cards feel like floating web UI surfaces.