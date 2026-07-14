# SVG Recipe — KPI Grid Dashboard Widget

## Visual mechanism
A compact executive dashboard card turns a table of people/projects into an at-a-glance KPI module: colored status dots, a 12-period achievement grid, and right-aligned target bars communicate performance faster than numbers alone. The premium look comes from a dark glassy container, subtle glows, column structure, and disciplined color coding.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 1× `<rect>` for the main rounded dashboard widget container with shadow
- 1× `<rect>` for the thin accent header strip
- 5× `<rect>` for alternating row bands
- 60× small `<rect>` for the 5-row × 12-month sparkline achievement grid
- 5× `<circle>` for red/yellow/green KPI status indicators
- 5× `<rect>` for orange target-value bars
- 5× `<path>` for subtle white trend overlays across each month grid
- Multiple `<line>` elements for column separators and row dividers
- Multiple `<text>` elements for title, headers, names, values, and month labels; every text element includes explicit `width`
- 2× decorative blurred `<ellipse>` elements for background glow
- 1× `<linearGradient>` for slide/card depth
- 1× `<radialGradient>` for glow color
- 1× `<filter id="cardShadow">` for widget elevation
- 1× `<filter id="softGlow">` for ambient dashboard lighting

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#05070B"/>
      <stop offset="55%" stop-color="#0B111B"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="120" x2="0" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#252A32"/>
      <stop offset="100%" stop-color="#16191F"/>
    </linearGradient>
    <linearGradient id="blueAccent" x1="110" y1="116" x2="1170" y2="116" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2F5597"/>
      <stop offset="55%" stop-color="#2C7BE5"/>
      <stop offset="100%" stop-color="#6EA8FF"/>
    </linearGradient>
    <radialGradient id="glowBlue" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2C7BE5" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#2C7BE5" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="1040" cy="118" rx="260" ry="110" fill="url(#glowBlue)" filter="url(#softGlow)" opacity="0.55"/>
  <ellipse cx="165" cy="610" rx="250" ry="105" fill="#00B050" filter="url(#softGlow)" opacity="0.12"/>

  <rect x="92" y="102" width="1096" height="514" rx="26" fill="#05070A" opacity="0.55" filter="url(#cardShadow)"/>
  <rect x="104" y="96" width="1072" height="502" rx="22" fill="url(#cardGrad)" stroke="#4A5363" stroke-width="1.2"/>
  <rect x="104" y="96" width="1072" height="12" rx="6" fill="url(#blueAccent)"/>
  <rect x="126" y="126" width="1028" height="74" rx="16" fill="#0E1420" opacity="0.72" stroke="#2D3748" stroke-width="1"/>

  <text x="146" y="164" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">Status: Top Five Employees</text>
  <text x="146" y="188" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#AAB6C8">Monthly sales attainment by employee · rolling 12-month view</text>
  <text x="930" y="157" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7F8DA3">TEAM TARGET</text>
  <text x="930" y="184" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">$117.8K</text>
  <circle cx="1126" cy="166" r="18" fill="#00B050"/>
  <text x="1113" y="171" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#07110B">82</text>

  <text x="146" y="236" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8895A8">STATUS</text>
  <text x="248" y="236" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8895A8">EMPLOYEE</text>
  <text x="454" y="236" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8895A8">MONTHLY TOTAL SALES REVENUE</text>
  <text x="956" y="236" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8895A8">SALES TARGET</text>

  <line x1="220" y1="250" x2="220" y2="554" stroke="#334155" stroke-width="1"/>
  <line x1="420" y1="250" x2="420" y2="554" stroke="#334155" stroke-width="1"/>
  <line x1="910" y1="250" x2="910" y2="554" stroke="#334155" stroke-width="1"/>

  <text x="460" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">J</text>
  <text x="494" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">F</text>
  <text x="528" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">M</text>
  <text x="562" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">A</text>
  <text x="596" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">M</text>
  <text x="630" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">J</text>
  <text x="664" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">J</text>
  <text x="698" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">A</text>
  <text x="732" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">S</text>
  <text x="766" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">O</text>
  <text x="800" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">N</text>
  <text x="834" y="258" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B778A">D</text>

  <g>
    <rect x="126" y="272" width="1028" height="52" rx="10" fill="#202733" opacity="0.92"/>
    <circle cx="176" cy="298" r="11" fill="#00B050"/>
    <text x="248" y="304" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#FFFFFF">Andrew</text>
    <rect x="456" y="285" width="24" height="24" rx="4" fill="#92D050"/><rect x="490" y="285" width="24" height="24" rx="4" fill="#92D050"/><rect x="524" y="285" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="558" y="285" width="24" height="24" rx="4" fill="#92D050"/><rect x="592" y="285" width="24" height="24" rx="4" fill="#92D050"/><rect x="626" y="285" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="660" y="285" width="24" height="24" rx="4" fill="#92D050"/><rect x="694" y="285" width="24" height="24" rx="4" fill="#92D050"/><rect x="728" y="285" width="24" height="24" rx="4" fill="#92D050"/><rect x="762" y="285" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="796" y="285" width="24" height="24" rx="4" fill="#92D050"/><rect x="830" y="285" width="24" height="24" rx="4" fill="#92D050"/>
    <path d="M468 303 C510 284, 552 312, 602 294 S710 288, 748 300 S814 286, 842 292" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.45"/>
    <rect x="956" y="285" width="138" height="24" rx="5" fill="#ED7D31"/>
    <text x="978" y="303" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">$23,719</text>
  </g>

  <g>
    <rect x="126" y="332" width="1028" height="52" rx="10" fill="#171D27"/>
    <circle cx="176" cy="358" r="11" fill="#00B050"/>
    <text x="248" y="364" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#FFFFFF">Janet</text>
    <rect x="456" y="345" width="24" height="24" rx="4" fill="#92D050"/><rect x="490" y="345" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="524" y="345" width="24" height="24" rx="4" fill="#92D050"/><rect x="558" y="345" width="24" height="24" rx="4" fill="#92D050"/><rect x="592" y="345" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="626" y="345" width="24" height="24" rx="4" fill="#92D050"/><rect x="660" y="345" width="24" height="24" rx="4" fill="#92D050"/><rect x="694" y="345" width="24" height="24" rx="4" fill="#92D050"/><rect x="728" y="345" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="762" y="345" width="24" height="24" rx="4" fill="#92D050"/><rect x="796" y="345" width="24" height="24" rx="4" fill="#92D050"/><rect x="830" y="345" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/>
    <path d="M468 360 C506 352, 548 345, 592 358 S690 350, 724 356 S802 348, 842 365" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.45"/>
    <rect x="956" y="345" width="112" height="24" rx="5" fill="#ED7D31"/>
    <text x="978" y="363" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">$19,172</text>
  </g>

  <g>
    <rect x="126" y="392" width="1028" height="52" rx="10" fill="#202733" opacity="0.92"/>
    <circle cx="176" cy="418" r="11" fill="#FFC000"/>
    <text x="248" y="424" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#FFFFFF">Laura</text>
    <rect x="456" y="405" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="490" y="405" width="24" height="24" rx="4" fill="#92D050"/><rect x="524" y="405" width="24" height="24" rx="4" fill="#92D050"/><rect x="558" y="405" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="592" y="405" width="24" height="24" rx="4" fill="#92D050"/><rect x="626" y="405" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="660" y="405" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="694" y="405" width="24" height="24" rx="4" fill="#92D050"/><rect x="728" y="405" width="24" height="24" rx="4" fill="#92D050"/><rect x="762" y="405" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="796" y="405" width="24" height="24" rx="4" fill="#92D050"/><rect x="830" y="405" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/>
    <path d="M468 424 C512 398, 548 404, 592 414 S668 432, 708 410 S792 410, 842 421" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.45"/>
    <rect x="956" y="405" width="88" height="24" rx="5" fill="#ED7D31"/>
    <text x="978" y="423" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">$15,112</text>
  </g>

  <g>
    <rect x="126" y="452" width="1028" height="52" rx="10" fill="#171D27"/>
    <circle cx="176" cy="478" r="11" fill="#FF3B30"/>
    <text x="248" y="484" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#FFFFFF">Margaret</text>
    <rect x="456" y="465" width="24" height="24" rx="4" fill="#92D050"/><rect x="490" y="465" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="524" y="465" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="558" y="465" width="24" height="24" rx="4" fill="#92D050"/><rect x="592" y="465" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="626" y="465" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="660" y="465" width="24" height="24" rx="4" fill="#92D050"/><rect x="694" y="465" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="728" y="465" width="24" height="24" rx="4" fill="#92D050"/><rect x="762" y="465" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="796" y="465" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="830" y="465" width="24" height="24" rx="4" fill="#92D050"/>
    <path d="M468 470 C512 489, 558 465, 596 481 S668 462, 710 478 S790 492, 842 469" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.45"/>
    <rect x="956" y="465" width="186" height="24" rx="5" fill="#ED7D31"/>
    <text x="978" y="483" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">$31,997</text>
  </g>

  <g>
    <rect x="126" y="512" width="1028" height="52" rx="10" fill="#202733" opacity="0.92"/>
    <circle cx="176" cy="538" r="11" fill="#00B050"/>
    <text x="248" y="544" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#FFFFFF">Nancy</text>
    <rect x="456" y="525" width="24" height="24" rx="4" fill="#92D050"/><rect x="490" y="525" width="24" height="24" rx="4" fill="#92D050"/><rect x="524" y="525" width="24" height="24" rx="4" fill="#92D050"/><rect x="558" y="525" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="592" y="525" width="24" height="24" rx="4" fill="#92D050"/><rect x="626" y="525" width="24" height="24" rx="4" fill="#92D050"/><rect x="660" y="525" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="694" y="525" width="24" height="24" rx="4" fill="#92D050"/><rect x="728" y="525" width="24" height="24" rx="4" fill="#92D050"/><rect x="762" y="525" width="24" height="24" rx="4" fill="#92D050"/><rect x="796" y="525" width="24" height="24" rx="4" fill="#18202A" stroke="#E5E7EB" stroke-width="1"/><rect x="830" y="525" width="24" height="24" rx="4" fill="#92D050"/>
    <path d="M468 537 C516 529, 558 532, 600 540 S688 526, 732 534 S798 528, 842 537" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.45"/>
    <rect x="956" y="525" width="162" height="24" rx="5" fill="#ED7D31"/>
    <text x="978" y="543" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">$27,765</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using one raster screenshot of the whole widget; keep rows, dots, grid cells, and bars editable.
- ❌ Using `<pattern>` for the month grid; create explicit small rectangles so each cell can be recolored in PowerPoint.
- ❌ Applying `filter` to `<line>` separators; filters on lines are dropped, so keep separators flat.
- ❌ Using `<use>` to duplicate month cells or row structures; duplicate explicit SVG elements instead.
- ❌ Using `clip-path` on rectangles or groups for row effects; clipping is only reliable on images.

## Composition notes
- Keep the widget self-contained with generous outer margins; on a 1280×720 slide, a 1050–1100 px wide card reads well as a dashboard centerpiece.
- Reserve the widest column for the 12-period grid; status and target columns should stay narrow so the eye lands on color-density patterns.
- Use a dark neutral base, one cool accent for structure, green/yellow/red for KPI semantics, and orange for target bars.
- Alternate row shading subtly; the grid should feel dense but not noisy, with enough contrast for empty vs achieved cells.