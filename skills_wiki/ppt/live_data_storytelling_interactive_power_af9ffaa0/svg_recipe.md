# SVG Recipe — Embed Interactive Power BI Dashboard

## Visual mechanism
A premium “live dashboard inside the slide” is conveyed by a large web-add-in frame: Power BI-like chrome, authenticated status, live badge, filter rail, KPI cards, and dense charts all contained in one dominant interactive surface. The SVG cannot create the actual live add-in, so it reproduces the executive presentation visual state that surrounds and previews an embedded Power BI report; the real Power BI add-in is added in PowerPoint on top of or in place of this frame.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× blurred `<path>` / `<ellipse>` decorative glows behind the dashboard
- 1× large rounded `<rect>` for the embedded web-add-in shell
- 1× rounded `<rect>` for browser/add-in chrome
- 3× `<circle>` for browser window controls
- 1× dark header `<rect>` for the Power BI report title bar
- 4× small rounded `<rect>` bars for a Power BI-style logo mark
- 1× rounded `<rect>` live status badge plus 1× glowing `<circle>` indicator
- 1× left filter rail `<rect>` with multiple slicer chips
- 4× KPI card `<rect>` panels with sparkline `<path>` overlays
- 3× chart container `<rect>` panels for bar, line/area, and donut visuals
- Multiple `<line>` elements for chart axes and gridlines
- Multiple `<rect>` elements for bars, slicers, chips, and UI controls
- Multiple `<path>` elements for sparklines, area fills, line charts, donut arcs, and interaction handles
- Multiple `<text>` elements with explicit `width` attributes for report labels, values, captions, and UI hints
- 2× `<filter>` definitions: soft drop shadow and live glow
- 5× `<linearGradient>` / `<radialGradient>` definitions for premium background, report header, cards, chart fills, and glow accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" font-family="Segoe UI, Microsoft YaHei, sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#eef2ff"/>
      <stop offset="48%" stop-color="#f7f3ff"/>
      <stop offset="100%" stop-color="#fff5ed"/>
    </linearGradient>
    <linearGradient id="chrome" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f3f5fb"/>
    </linearGradient>
    <linearGradient id="header" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#353e8e"/>
      <stop offset="62%" stop-color="#5b50a8"/>
      <stop offset="100%" stop-color="#d65224"/>
    </linearGradient>
    <linearGradient id="cardTint" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f7f8ff"/>
    </linearGradient>
    <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6e62d9" stop-opacity="0.50"/>
      <stop offset="100%" stop-color="#6e62d9" stop-opacity="0.03"/>
    </linearGradient>
    <radialGradient id="liveRadial" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2ee58b" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#2ee58b" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.08 0 0 0 0 0.10 0 0 0 0 0.20 0 0 0 0.22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M-40,96 C120,18 220,55 330,18 C466,-27 565,52 506,145 C444,241 242,187 137,270 C45,343 -40,292 -40,96 Z" fill="#c9d4ff" opacity="0.38" filter="url(#glow)"/>
  <ellipse cx="1125" cy="625" rx="220" ry="92" fill="#ffc7a6" opacity="0.34" filter="url(#glow)"/>

  <text x="70" y="48" width="690" font-size="28" font-weight="700" fill="#20233a">Live Power BI Dashboard</text>
  <text x="70" y="75" width="820" font-size="14" fill="#686f86">Embedded report surface for real-time exploration, slicers, drill-downs, and executive Q&amp;A without leaving the slide.</text>

  <rect x="64" y="96" width="1152" height="566" rx="30" fill="#ffffff" filter="url(#shadow)"/>
  <rect x="64" y="96" width="1152" height="48" rx="30" fill="url(#chrome)"/>
  <rect x="64" y="126" width="1152" height="20" fill="#f3f5fb"/>
  <circle cx="96" cy="120" r="6" fill="#ff6159"/>
  <circle cx="118" cy="120" r="6" fill="#ffbd2e"/>
  <circle cx="140" cy="120" r="6" fill="#28c840"/>
  <rect x="174" y="110" width="610" height="20" rx="10" fill="#e8ebf5"/>
  <text x="194" y="125" width="540" font-size="11" fill="#697087">app.powerbi.com/reportEmbed?groupId=executive-review&amp;reportId=commercial-cockpit</text>
  <rect x="1036" y="108" width="145" height="24" rx="12" fill="#edf7f1" stroke="#bce7cc"/>
  <circle cx="1054" cy="120" r="18" fill="url(#liveRadial)" filter="url(#glow)"/>
  <circle cx="1054" cy="120" r="5" fill="#17b26a"/>
  <text x="1068" y="125" width="96" font-size="12" font-weight="700" fill="#157348">CONNECTED</text>

  <rect x="88" y="160" width="1104" height="476" rx="20" fill="#f6f7fc"/>
  <rect x="88" y="160" width="1104" height="62" rx="20" fill="url(#header)"/>
  <rect x="88" y="198" width="1104" height="24" fill="#353e8e"/>
  <rect x="116" y="178" width="8" height="24" rx="3" fill="#f6c547"/>
  <rect x="130" y="170" width="8" height="32" rx="3" fill="#f6c547"/>
  <rect x="144" y="184" width="8" height="18" rx="3" fill="#f6c547"/>
  <rect x="158" y="164" width="8" height="38" rx="3" fill="#f6c547"/>
  <text x="184" y="188" width="420" font-size="18" font-weight="700" fill="#ffffff">Commercial Performance Cockpit</text>
  <text x="184" y="208" width="520" font-size="11" fill="#dfe2ff">QBR live dataset • refreshed 4 minutes ago • row-level security enabled</text>
  <rect x="1008" y="176" width="78" height="28" rx="14" fill="#ffffff" opacity="0.16"/>
  <text x="1028" y="195" width="46" font-size="12" font-weight="700" fill="#ffffff">LIVE</text>
  <circle cx="1019" cy="190" r="4" fill="#30e38f"/>
  <rect x="1098" y="176" width="70" height="28" rx="14" fill="#ffffff" opacity="0.16"/>
  <text x="1113" y="195" width="44" font-size="12" font-weight="600" fill="#ffffff">Share</text>

  <rect x="108" y="240" width="174" height="376" rx="16" fill="#ffffff"/>
  <text x="128" y="266" width="120" font-size="14" font-weight="700" fill="#252a43">Report filters</text>
  <text x="128" y="292" width="120" font-size="11" fill="#7b8196">Region</text>
  <rect x="128" y="302" width="130" height="28" rx="8" fill="#eef1ff" stroke="#cfd5ff"/>
  <text x="142" y="321" width="92" font-size="12" font-weight="600" fill="#4e55a7">North America</text>
  <text x="128" y="352" width="120" font-size="11" fill="#7b8196">Product line</text>
  <rect x="128" y="362" width="54" height="26" rx="8" fill="#5b50a8"/>
  <text x="143" y="380" width="26" font-size="11" font-weight="700" fill="#ffffff">SaaS</text>
  <rect x="190" y="362" width="68" height="26" rx="8" fill="#f2f3fa" stroke="#dde1ee"/>
  <text x="204" y="380" width="42" font-size="11" fill="#596073">Cloud</text>
  <text x="128" y="418" width="120" font-size="11" fill="#7b8196">Fiscal period</text>
  <rect x="128" y="430" width="130" height="36" rx="8" fill="#f2f3fa" stroke="#dde1ee"/>
  <text x="143" y="453" width="92" font-size="13" font-weight="600" fill="#252a43">FY25 Q2</text>
  <line x1="128" y1="496" x2="258" y2="496" stroke="#e5e8f3" stroke-width="1"/>
  <text x="128" y="524" width="126" font-size="12" font-weight="700" fill="#252a43">Interaction mode</text>
  <rect x="128" y="538" width="130" height="32" rx="16" fill="#fff6f0" stroke="#ffd5bf"/>
  <text x="146" y="559" width="96" font-size="12" font-weight="700" fill="#c34f1d">Click to explore</text>

  <rect x="304" y="240" width="198" height="96" rx="16" fill="url(#cardTint)" stroke="#e5e8f3"/>
  <text x="326" y="266" width="120" font-size="11" fill="#7b8196">Revenue</text>
  <text x="326" y="300" width="120" font-size="30" font-weight="800" fill="#252a43">$42.8M</text>
  <path d="M326,318 C350,309 364,314 384,304 C407,292 426,312 455,295 C471,286 482,287 490,282" fill="none" stroke="#17b26a" stroke-width="3"/>
  <text x="440" y="266" width="44" font-size="11" font-weight="700" fill="#17b26a">+12%</text>

  <rect x="522" y="240" width="198" height="96" rx="16" fill="url(#cardTint)" stroke="#e5e8f3"/>
  <text x="544" y="266" width="120" font-size="11" fill="#7b8196">Gross margin</text>
  <text x="544" y="300" width="120" font-size="30" font-weight="800" fill="#252a43">61.4%</text>
  <path d="M544,319 C568,306 589,321 610,311 C636,298 660,301 704,286" fill="none" stroke="#5b50a8" stroke-width="3"/>
  <text x="658" y="266" width="44" font-size="11" font-weight="700" fill="#5b50a8">+3.1</text>

  <rect x="740" y="240" width="198" height="96" rx="16" fill="url(#cardTint)" stroke="#e5e8f3"/>
  <text x="762" y="266" width="120" font-size="11" fill="#7b8196">Pipeline</text>
  <text x="762" y="300" width="120" font-size="30" font-weight="800" fill="#252a43">$118M</text>
  <path d="M762,318 C788,322 812,310 834,314 C860,318 886,299 922,304" fill="none" stroke="#d65224" stroke-width="3"/>
  <text x="876" y="266" width="44" font-size="11" font-weight="700" fill="#d65224">-4%</text>

  <rect x="958" y="240" width="210" height="96" rx="16" fill="url(#cardTint)" stroke="#e5e8f3"/>
  <text x="980" y="266" width="130" font-size="11" fill="#7b8196">Customer health</text>
  <text x="980" y="300" width="120" font-size="30" font-weight="800" fill="#252a43">87</text>
  <rect x="1030" y="286" width="112" height="10" rx="5" fill="#e9ecf5"/>
  <rect x="1030" y="286" width="91" height="10" rx="5" fill="#17b26a"/>
  <text x="980" y="323" width="138" font-size="11" fill="#7b8196">Weighted renewal index</text>

  <rect x="304" y="358" width="416" height="258" rx="18" fill="#ffffff" stroke="#e5e8f3"/>
  <text x="328" y="388" width="240" font-size="15" font-weight="700" fill="#252a43">Revenue by region</text>
  <text x="328" y="408" width="300" font-size="11" fill="#7b8196">Hover bars in Power BI to inspect country-level detail</text>
  <line x1="334" y1="560" x2="682" y2="560" stroke="#dfe3ef"/>
  <line x1="334" y1="514" x2="682" y2="514" stroke="#eef0f6"/>
  <line x1="334" y1="468" x2="682" y2="468" stroke="#eef0f6"/>
  <rect x="352" y="482" width="34" height="78" rx="5" fill="#5b50a8"/>
  <rect x="400" y="438" width="34" height="122" rx="5" fill="#d65224"/>
  <rect x="448" y="454" width="34" height="106" rx="5" fill="#5b50a8"/>
  <rect x="496" y="410" width="34" height="150" rx="5" fill="#d65224"/>
  <rect x="544" y="494" width="34" height="66" rx="5" fill="#5b50a8"/>
  <rect x="592" y="430" width="34" height="130" rx="5" fill="#d65224"/>
  <text x="349" y="586" width="46" font-size="10" fill="#7b8196">NA</text>
  <text x="398" y="586" width="46" font-size="10" fill="#7b8196">EU</text>
  <text x="447" y="586" width="46" font-size="10" fill="#7b8196">APAC</text>
  <text x="493" y="586" width="46" font-size="10" fill="#7b8196">LATAM</text>
  <text x="546" y="586" width="46" font-size="10" fill="#7b8196">MEA</text>
  <text x="594" y="586" width="46" font-size="10" fill="#7b8196">JP</text>

  <rect x="740" y="358" width="428" height="258" rx="18" fill="#ffffff" stroke="#e5e8f3"/>
  <text x="764" y="388" width="260" font-size="15" font-weight="700" fill="#252a43">Run-rate forecast</text>
  <text x="764" y="408" width="315" font-size="11" fill="#7b8196">Slicer selections update the forecast and confidence band live</text>
  <line x1="772" y1="560" x2="1028" y2="560" stroke="#dfe3ef"/>
  <line x1="772" y1="514" x2="1028" y2="514" stroke="#eef0f6"/>
  <line x1="772" y1="468" x2="1028" y2="468" stroke="#eef0f6"/>
  <path d="M772,542 C806,520 828,532 858,501 C894,464 915,486 944,452 C975,415 1002,430 1028,390 L1028,560 L772,560 Z" fill="url(#areaFill)"/>
  <path d="M772,542 C806,520 828,532 858,501 C894,464 915,486 944,452 C975,415 1002,430 1028,390" fill="none" stroke="#5b50a8" stroke-width="4"/>
  <circle cx="1028" cy="390" r="6" fill="#5b50a8"/>
  <path d="M1080,430 A54,54 0 1,1 1079,429" fill="none" stroke="#e9ecf5" stroke-width="18"/>
  <path d="M1080,376 A54,54 0 0,1 1126,458" fill="none" stroke="#5b50a8" stroke-width="18" stroke-linecap="round"/>
  <path d="M1126,458 A54,54 0 0,1 1045,474" fill="none" stroke="#d65224" stroke-width="18" stroke-linecap="round"/>
  <text x="1058" y="432" width="72" font-size="24" font-weight="800" fill="#252a43">72%</text>
  <text x="1046" y="456" width="96" font-size="10" fill="#7b8196">target attainment</text>

  <rect x="792" y="580" width="148" height="18" rx="9" fill="#eef1ff"/>
  <text x="810" y="593" width="110" font-size="10" font-weight="600" fill="#4e55a7">Drill-through enabled</text>
  <rect x="954" y="580" width="166" height="18" rx="9" fill="#fff6f0"/>
  <text x="972" y="593" width="130" font-size="10" font-weight="600" fill="#c34f1d">Tooltip pages available</text>

  <rect x="884" y="647" width="298" height="28" rx="14" fill="#ffffff" opacity="0.78" stroke="#dfe3ef" stroke-dasharray="5 5"/>
  <text x="902" y="666" width="260" font-size="12" fill="#596073">Place the real Power BI add-in over this frame for live interaction.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<foreignObject>`, iframe-like HTML, or embedded web code inside the SVG; it will not translate as an interactive Power BI object.
- ❌ Do not rely on a static dashboard screenshot alone if the intent is “live data”; use the SVG as a premium editable shell/preview and add the actual Power BI add-in in PowerPoint.
- ❌ Do not use `<mask>` or `clip-path` on dashboard shapes to fake complex report panels; those are unreliable unless clipping an `<image>`.
- ❌ Do not put filter effects on `<line>` chart gridlines; PowerPoint translation drops line filters.
- ❌ Do not use marker-based arrows for interaction hints; if needed, build arrows from editable `<line>` plus small `<path>` arrowheads.

## Composition notes
- Let the embedded report dominate the slide: reserve roughly 85–90% of the canvas for the dashboard frame so charts remain legible in presentation mode.
- Keep the title and explanatory copy outside the frame minimal; the report itself should feel like the main application surface.
- Use a Power BI-inspired palette: dark blue/purple header, orange accents, white cards, and soft lavender background to signal Microsoft analytics without copying a screenshot.
- Include subtle “CONNECTED,” “LIVE,” “drill-through,” or “tooltip” cues so the audience understands this is intended as an interactive live-data surface.