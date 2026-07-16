# SVG Recipe — Interactive KPI Control Panel

## Visual mechanism
A polished, app-like navigation hub: three elevated KPI section cards sit on a quiet blue-grey workspace, each containing color-coded rounded “buttons” that read like clickable PowerPoint controls. Subtle shadows, gradient chrome, micro-icons, and status chips make the slide feel like an executive dashboard rather than a static menu.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient workspace background
- 1× `<rect>` for a top application header bar
- 3× large `<rect>` for the main white KPI section cards
- 6× rounded `<rect>` for the primary navigation buttons
- 3× small rounded `<rect>` for section status chips
- 8× small `<circle>` for app chrome dots, status indicators, and decorative texture
- 8× `<path>` for decorative background blobs, button icons, and KPI glyphs
- 4× `<line>` for faint panel separators and dashboard guide accents
- Multiple `<text>` elements with explicit `width=` for title, section headers, labels, and button text
- 2× `<linearGradient>` for background and header/button polish
- 1× `<radialGradient>` for soft ambient highlight
- 2× `<filter>` using blur/offset/merge for card shadows and soft accent glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F4F7FD"/>
      <stop offset="55%" stop-color="#EBEFF8"/>
      <stop offset="100%" stop-color="#E3E9F5"/>
    </linearGradient>
    <linearGradient id="chromeGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF3FB"/>
    </linearGradient>
    <linearGradient id="blueBtn" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4F7DD2"/>
      <stop offset="100%" stop-color="#315FAE"/>
    </linearGradient>
    <linearGradient id="purpleBtn" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8248B8"/>
      <stop offset="100%" stop-color="#66309D"/>
    </linearGradient>
    <linearGradient id="lightBlueBtn" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#A9D3F2"/>
      <stop offset="100%" stop-color="#7FB3DE"/>
    </linearGradient>
    <radialGradient id="ambient" cx="50%" cy="38%" r="58%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="13"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#ambient)"/>

  <path d="M-40,585 C120,515 206,650 360,594 C475,552 520,455 655,500 C810,552 840,686 1012,641 C1130,610 1195,535 1325,570 L1325,760 L-40,760 Z"
        fill="#D8E2F4" opacity="0.42"/>
  <path d="M1005,94 C1080,45 1190,50 1243,118 C1302,194 1232,287 1142,263 C1050,239 935,140 1005,94 Z"
        fill="#C9D7F1" opacity="0.5" filter="url(#softGlow)"/>

  <circle cx="88" cy="176" r="3" fill="#C5CFE4" opacity="0.7"/>
  <circle cx="150" cy="226" r="2" fill="#C5CFE4" opacity="0.6"/>
  <circle cx="1164" cy="394" r="3" fill="#C5CFE4" opacity="0.7"/>
  <circle cx="1090" cy="508" r="2" fill="#C5CFE4" opacity="0.6"/>

  <rect x="96" y="54" width="1088" height="76" rx="24" fill="url(#chromeGrad)" stroke="#D7DFF0" stroke-width="1.4" filter="url(#cardShadow)"/>
  <circle cx="132" cy="92" r="7" fill="#FF6B6B"/>
  <circle cx="154" cy="92" r="7" fill="#FFCF5B"/>
  <circle cx="176" cy="92" r="7" fill="#58C878"/>
  <text x="210" y="88" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#303849">KPI Performance Control Center</text>
  <text x="210" y="112" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8497">Choose a view, input source, or KPI definition module</text>
  <rect x="946" y="77" width="188" height="31" rx="15.5" fill="#EDF3FF" stroke="#BFD0EE"/>
  <circle cx="972" cy="92.5" r="5" fill="#30B66D"/>
  <text x="990" y="98" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#546070">Live deck navigation</text>

  <line x1="122" y1="165" x2="1158" y2="165" stroke="#D8DFEF" stroke-width="1" stroke-dasharray="7 9"/>
  <line x1="122" y1="645" x2="1158" y2="645" stroke="#D8DFEF" stroke-width="1" stroke-dasharray="7 9"/>

  <rect x="124" y="188" width="316" height="388" rx="22" fill="#FFFFFF" stroke="#BFB8DE" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="482" y="188" width="316" height="388" rx="22" fill="#FFFFFF" stroke="#BFB8DE" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="840" y="188" width="316" height="388" rx="22" fill="#FFFFFF" stroke="#BFB8DE" stroke-width="1.6" filter="url(#cardShadow)"/>

  <path d="M252,228 h60 a12,12 0 0 1 12,12 v22 h-84 v-22 a12,12 0 0 1 12,-12 Z M252,272 h72 v34 h-72 Z"
        fill="#EEF4FF" stroke="#BFD1F2" stroke-width="1.2"/>
  <text x="172" y="338" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#404040">Dashboard</text>
  <rect x="214" y="354" width="136" height="28" rx="14" fill="#EEF3FF"/>
  <circle cx="234" cy="368" r="5" fill="#4472C4"/>
  <text x="248" y="373" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#60708D">2 linked views</text>

  <rect x="172" y="410" width="220" height="54" rx="14" fill="url(#blueBtn)"/>
  <path d="M198,431 h18 v18 h-18 Z M222,422 h18 v27 h-18 Z M246,437 h18 v12 h-18 Z" fill="#FFFFFF" opacity="0.95"/>
  <text x="282" y="444" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#FFFFFF">Executive Dashboard</text>

  <rect x="172" y="484" width="220" height="54" rx="14" fill="url(#blueBtn)" opacity="0.93"/>
  <path d="M198,515 C216,492 231,527 249,501 C258,488 268,494 273,500" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="282" y="518" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#FFFFFF">KPI Trend</text>

  <path d="M603,226 h74 a12,12 0 0 1 12,12 v52 a12,12 0 0 1 -12,12 h-74 a12,12 0 0 1 -12,-12 v-52 a12,12 0 0 1 12,-12 Z M608,246 h76 M608,266 h76"
        fill="#F6F0FF" stroke="#D7C0EA" stroke-width="1.2"/>
  <text x="530" y="338" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#404040">Input Sheets</text>
  <rect x="572" y="354" width="136" height="28" rx="14" fill="#F5EDFF"/>
  <circle cx="592" cy="368" r="5" fill="#7030A0"/>
  <text x="606" y="373" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#6B527D">3 data sources</text>

  <rect x="530" y="398" width="220" height="46" rx="13" fill="url(#purpleBtn)"/>
  <path d="M555,412 h24 v18 h-24 Z M559,408 h24 v18 h-24 Z" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
  <text x="640" y="427" width="132" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#FFFFFF">Actual</text>

  <rect x="530" y="458" width="220" height="46" rx="13" fill="url(#purpleBtn)" opacity="0.95"/>
  <path d="M558,471 l19,19 M577,471 l-19,19" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  <text x="640" y="487" width="132" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#FFFFFF">Target</text>

  <rect x="530" y="518" width="220" height="46" rx="13" fill="url(#purpleBtn)" opacity="0.9"/>
  <path d="M577,532 C564,532 554,542 554,550 C554,558 563,562 572,556 M554,550 h-9 M554,550 v-9" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  <text x="640" y="547" width="132" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#FFFFFF">Previous Year</text>

  <path d="M998,224 C1021,224 1041,244 1041,267 C1041,290 1021,310 998,310 C975,310 955,290 955,267 C955,244 975,224 998,224 Z M998,241 v28 l22,14"
        fill="#F0F8FF" stroke="#BBD9F2" stroke-width="1.2"/>
  <text x="888" y="338" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#404040">KPI</text>
  <rect x="930" y="354" width="136" height="28" rx="14" fill="#EDF7FF"/>
  <circle cx="950" cy="368" r="5" fill="#9BC2E6"/>
  <text x="964" y="373" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#55718C">definition hub</text>

  <rect x="888" y="444" width="220" height="58" rx="15" fill="url(#lightBlueBtn)"/>
  <path d="M915,462 h21 a8,8 0 0 1 8,8 v14 a8,8 0 0 1 -8,8 h-21 a8,8 0 0 1 -8,-8 v-14 a8,8 0 0 1 8,-8 Z M916,477 h20"
        fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  <text x="998" y="480" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Define KPI</text>

  <line x1="440" y1="382" x2="482" y2="382" stroke="#CAD4E7" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="798" y1="382" x2="840" y2="382" stroke="#CAD4E7" stroke-width="2" stroke-dasharray="5 7"/>

  <text x="124" y="684" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8397">Tip: assign PowerPoint hyperlinks to each converted button shape to create a non-linear KPI deck.</text>
  <text x="1012" y="684" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9AA4B7">QBR navigation panel</text>
</svg>
```

## Avoid in this skill
- ❌ Do not wrap buttons in SVG `<a>` hyperlinks; create hyperlinks on the converted PowerPoint shapes after translation.
- ❌ Do not use `<foreignObject>` for HTML-style UI controls; build the interface from native SVG rectangles, text, lines, circles, and paths.
- ❌ Do not rely on `<pattern>` or procedural texture fills for the background; use gradients, soft blobs, sparse dots, or a full-slide image if texture is essential.
- ❌ Do not apply `filter` to `<line>` connectors; use unfiltered dashed lines for separators.
- ❌ Do not use `marker-end` for arrows between panels; if arrows are needed, draw them as separate `<line>` plus small `<path>` arrowheads.

## Composition notes
- Keep the navigation panel centered with generous outer margins; the three cards should occupy roughly 80% of slide width and 55–60% of slide height.
- Use one accent color per functional group: blue for dashboards, purple for data input, light blue for KPI definitions.
- Treat buttons as the primary visual focus: high-contrast fill, white centered text, rounded corners, and small icons help them read as clickable.
- Preserve negative space around the cards and use subtle background ornamentation only at the edges so the control panel remains clear and executive-ready.