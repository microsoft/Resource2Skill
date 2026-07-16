# SVG Recipe — Interactive Dashboard with Custom Zoom Triggers

## Visual mechanism
A premium dashboard hub is built from oversized, color-coded cards that read as custom “zoom buttons,” each combining a title, KPI hint, icon, and subtle hotspot outline. In PowerPoint, the SVG supplies the fully editable visual layer; transparent Slide Zoom objects or hyperlinks are then placed over each card to create the actual interactive navigation.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× decorative `<path>` blobs for ambient depth behind the dashboard
- 6× rounded `<rect>` cards for the interactive dashboard panels
- 6× semi-transparent/dashed `<rect>` overlays for “clickable hotspot” affordances
- Multiple small `<rect>` elements for chart bars, KPI pills, and icon construction
- Multiple `<circle>` / `<ellipse>` elements for icon details, nodes, and status dots
- Multiple `<line>` elements for chart axes, connector lines, and roadmap strokes
- Multiple `<path>` elements for custom icons such as funnel, gear, heart, route, cursor chevron, and arrowheads
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, panel labels, metrics, and zoom hints
- 8× `<linearGradient>` fills for premium background and panel color variation
- 1× `<radialGradient>` for soft ambient background lighting
- 1× `<filter id="cardShadow">` applied to card rectangles
- 1× `<filter id="softGlow">` applied to decorative background paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F8FBFF"/>
      <stop offset="1" stop-color="#EEF3F8"/>
    </linearGradient>
    <radialGradient id="ambient" cx="50%" cy="35%" r="70%">
      <stop offset="0" stop-color="#D9ECFF" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#D9ECFF" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="gSales" x1="70" y1="135" x2="822" y2="355">
      <stop offset="0" stop-color="#4AACFF"/>
      <stop offset="1" stop-color="#006FD6"/>
    </linearGradient>
    <linearGradient id="gMarketing" x1="846" y1="135" x2="1210" y2="355">
      <stop offset="0" stop-color="#22D27C"/>
      <stop offset="1" stop-color="#0D9B5A"/>
    </linearGradient>
    <linearGradient id="gOps" x1="70" y1="386" x2="434" y2="606">
      <stop offset="0" stop-color="#FFC84D"/>
      <stop offset="1" stop-color="#F39C12"/>
    </linearGradient>
    <linearGradient id="gCustomer" x1="458" y1="386" x2="822" y2="606">
      <stop offset="0" stop-color="#7A4DD8"/>
      <stop offset="1" stop-color="#4A247F"/>
    </linearGradient>
    <linearGradient id="gFinance" x1="846" y1="386" x2="1210" y2="606">
      <stop offset="0" stop-color="#F0645B"/>
      <stop offset="1" stop-color="#C0392B"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#ambient)"/>
  <path d="M930 55 C1060 5 1210 50 1260 160 C1310 272 1190 335 1065 300 C945 266 850 185 930 55 Z" fill="#B9E4FF" opacity="0.35" filter="url(#softGlow)"/>
  <path d="M-90 510 C20 420 180 425 250 535 C320 642 190 735 40 720 C-70 707 -170 610 -90 510 Z" fill="#D7CBFF" opacity="0.34" filter="url(#softGlow)"/>

  <text x="70" y="62" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#1B2430">Executive Performance Hub</text>
  <text x="72" y="96" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6776">Choose a business area to zoom into the detailed story, then return to this dashboard.</text>
  <rect x="1058" y="54" width="152" height="36" rx="18" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="1080" cy="72" r="5" fill="#21C77A"/>
  <text x="1094" y="77" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#405060">LIVE REVIEW</text>

  <rect x="70" y="135" width="752" height="220" rx="26" fill="url(#gSales)" filter="url(#cardShadow)"/>
  <rect x="94" y="157" width="704" height="176" rx="20" fill="url(#glass)"/>
  <text x="108" y="187" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" letter-spacing="1.5" fill="#FFFFFF">SALES PERFORMANCE</text>
  <text x="108" y="230" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#FFFFFF">$24.8M</text>
  <text x="112" y="259" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#EAF6FF">Quarter-to-date pipeline</text>
  <rect x="110" y="286" width="112" height="28" rx="14" fill="#FFFFFF" opacity="0.22"/>
  <text x="128" y="306" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">ZOOM ↗</text>
  <line x1="430" y1="292" x2="740" y2="292" stroke="#FFFFFF" stroke-width="2" opacity="0.55"/>
  <line x1="430" y1="185" x2="430" y2="292" stroke="#FFFFFF" stroke-width="2" opacity="0.55"/>
  <rect x="458" y="246" width="36" height="46" rx="8" fill="#FFFFFF" opacity="0.75"/>
  <rect x="514" y="216" width="36" height="76" rx="8" fill="#FFFFFF" opacity="0.86"/>
  <rect x="570" y="196" width="36" height="96" rx="8" fill="#FFFFFF" opacity="0.96"/>
  <rect x="626" y="226" width="36" height="66" rx="8" fill="#FFFFFF" opacity="0.8"/>
  <path d="M456 235 C500 204 530 220 570 188 C612 155 658 172 715 142" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.75"/>
  <path d="M702 139 L724 137 L714 158 Z" fill="#FFFFFF" opacity="0.82"/>
  <rect x="82" y="147" width="728" height="196" rx="22" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="8 10" opacity="0.34"/>

  <rect x="846" y="135" width="364" height="220" rx="26" fill="url(#gMarketing)" filter="url(#cardShadow)"/>
  <text x="878" y="187" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" letter-spacing="1.5" fill="#FFFFFF">MARKETING FUNNEL</text>
  <path d="M924 218 L1132 218 L1060 290 L996 290 Z" fill="#FFFFFF" opacity="0.88"/>
  <path d="M980 304 L1074 304 L1044 326 L1010 326 Z" fill="#FFFFFF" opacity="0.62"/>
  <text x="882" y="310" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF">38%</text>
  <text x="944" y="310" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#EFFFF6">lead-to-opportunity</text>
  <rect x="1080" y="286" width="98" height="28" rx="14" fill="#FFFFFF" opacity="0.22"/>
  <text x="1096" y="306" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">ZOOM ↗</text>
  <rect x="858" y="147" width="340" height="196" rx="22" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="8 10" opacity="0.34"/>

  <rect x="70" y="386" width="364" height="220" rx="26" fill="url(#gOps)" filter="url(#cardShadow)"/>
  <text x="102" y="438" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" letter-spacing="1.5" fill="#FFFFFF">OPERATIONS</text>
  <circle cx="252" cy="494" r="58" fill="#FFFFFF" opacity="0.25"/>
  <path d="M252 424 L268 454 L302 458 L278 482 L284 516 L252 500 L220 516 L226 482 L202 458 L236 454 Z" fill="#FFFFFF" opacity="0.9"/>
  <line x1="140" y1="554" x2="360" y2="554" stroke="#FFFFFF" stroke-width="5" opacity="0.42"/>
  <circle cx="164" cy="554" r="9" fill="#FFFFFF"/>
  <circle cx="250" cy="554" r="9" fill="#FFFFFF"/>
  <circle cx="338" cy="554" r="9" fill="#FFFFFF"/>
  <text x="102" y="578" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">ZOOM ↗</text>
  <rect x="82" y="398" width="340" height="196" rx="22" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="8 10" opacity="0.34"/>

  <rect x="458" y="386" width="364" height="220" rx="26" fill="url(#gCustomer)" filter="url(#cardShadow)"/>
  <text x="490" y="438" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" letter-spacing="1.5" fill="#FFFFFF">CUSTOMER SUCCESS</text>
  <path d="M640 530 C592 494 556 464 576 426 C592 396 628 406 640 432 C652 406 688 396 704 426 C724 464 688 494 640 530 Z" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="574" cy="536" r="8" fill="#FFFFFF" opacity="0.65"/>
  <circle cx="706" cy="536" r="8" fill="#FFFFFF" opacity="0.65"/>
  <text x="490" y="566" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF">91 NPS</text>
  <text x="700" y="578" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">ZOOM ↗</text>
  <rect x="470" y="398" width="340" height="196" rx="22" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="8 10" opacity="0.34"/>

  <rect x="846" y="386" width="364" height="220" rx="26" fill="url(#gFinance)" filter="url(#cardShadow)"/>
  <text x="878" y="438" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" letter-spacing="1.5" fill="#FFFFFF">FINANCE OUTLOOK</text>
  <ellipse cx="1028" cy="492" rx="72" ry="72" fill="#FFFFFF" opacity="0.20"/>
  <text x="990" y="520" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="800" fill="#FFFFFF">$</text>
  <path d="M914 552 C952 520 980 544 1012 508 C1044 472 1084 486 1148 430" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.78"/>
  <path d="M1134 426 L1158 422 L1148 446 Z" fill="#FFFFFF" opacity="0.86"/>
  <text x="878" y="578" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">ZOOM ↗</text>
  <rect x="858" y="398" width="340" height="196" rx="22" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="8 10" opacity="0.34"/>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on SVG `<a href="">` links for the zoom behavior; create the visual dashboard in SVG, then add native PowerPoint Slide Zoom or hyperlink hotspots over the imported shapes.
- ❌ Do not use `<use>` or `<symbol>` to repeat icons across cards; duplicate simple editable paths/rectangles directly.
- ❌ Do not apply `filter` to `<line>` elements for glowing charts; use thick strokes without filters or convert glow accents to `<path>` / `<rect>`.
- ❌ Do not use `clip-path` on card groups or text to fake thumbnails; clipping only translates reliably for `<image>` elements.
- ❌ Do not place one transparent SVG rectangle over the entire dashboard as a single trigger; each card needs its own separate PowerPoint zoom object or hotspot.

## Composition notes
- Keep the dashboard title area shallow, around 90–110 px tall, so the interaction grid owns most of the slide.
- Use one oversized hero card and several equal secondary cards to create a hierarchy of likely audience choices.
- Make gutters generous and consistent; 20–28 px gaps make each zoom trigger feel intentional and touch-friendly.
- Use white icons and text on saturated card colors, with dashed inner outlines to subtly signal clickable regions without cluttering the dashboard.