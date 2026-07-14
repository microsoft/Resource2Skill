# SVG Recipe — UI/UX Logic Flow & Wireframe Mapping

## Visual mechanism
Translate a user journey into large editable “screen” cards connected by orthogonal logic lines, with peach action pills and navy decision diamonds sitting directly on the flow. Each screen card contains simplified wireframe UI blocks plus feature notes, so the slide bridges requirements, navigation logic, and prototype structure in one view.

## SVG primitives needed
- 1× `<rect>` for the warm parchment slide background
- 1× `<rect>` with low opacity for a subtle blueprint grid panel
- 4× large `<rect>` for primary UI screen/page cards
- 12–18× small `<rect>` and `<circle>` elements inside cards for editable wireframe details: top bars, buttons, cards, inputs, avatar dots, charts
- 4× rounded `<rect>` for action/button labels on the connector routes
- 1× `<path>` diamond for the decision node
- 8–12× `<line>` elements for orthogonal connector segments
- 5× small filled `<path>` triangles for manual arrowheads
- Multiple `<text width="...">` elements with nested `<tspan>` for page IDs, feature lists, action labels, branch labels, and title
- 2× `<linearGradient>` fills for premium screen surfaces and action pills
- 1× `<filter id="softShadow">` applied to screen cards, action pills, and the decision diamond
- 1× `<filter id="glow">` optionally applied to the active/current screen card

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="screenGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FBFF"/>
      <stop offset="100%" stop-color="#D9E2EC"/>
    </linearGradient>
    <linearGradient id="actionGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF4EC"/>
      <stop offset="100%" stop-color="#FFE5D9"/>
    </linearGradient>
    <linearGradient id="navyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#183B5B"/>
      <stop offset="100%" stop-color="#102A43"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F4EFE6"/>
  <rect x="34" y="92" width="1212" height="566" rx="28" fill="#FFFFFF" opacity="0.34"/>
  <line x1="80" y1="140" x2="1200" y2="140" stroke="#102A43" stroke-width="1" opacity="0.08" stroke-dasharray="4 14"/>
  <line x1="80" y1="260" x2="1200" y2="260" stroke="#102A43" stroke-width="1" opacity="0.08" stroke-dasharray="4 14"/>
  <line x1="80" y1="380" x2="1200" y2="380" stroke="#102A43" stroke-width="1" opacity="0.08" stroke-dasharray="4 14"/>
  <line x1="80" y1="500" x2="1200" y2="500" stroke="#102A43" stroke-width="1" opacity="0.08" stroke-dasharray="4 14"/>
  <line x1="160" y1="112" x2="160" y2="635" stroke="#102A43" stroke-width="1" opacity="0.06" stroke-dasharray="4 14"/>
  <line x1="400" y1="112" x2="400" y2="635" stroke="#102A43" stroke-width="1" opacity="0.06" stroke-dasharray="4 14"/>
  <line x1="640" y1="112" x2="640" y2="635" stroke="#102A43" stroke-width="1" opacity="0.06" stroke-dasharray="4 14"/>
  <line x1="880" y1="112" x2="880" y2="635" stroke="#102A43" stroke-width="1" opacity="0.06" stroke-dasharray="4 14"/>
  <line x1="1120" y1="112" x2="1120" y2="635" stroke="#102A43" stroke-width="1" opacity="0.06" stroke-dasharray="4 14"/>

  <text x="64" y="52" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#102A43">User Login &amp; Dashboard Logic Map</text>
  <text x="66" y="82" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#486581">Screen architecture, user actions, and decision branches mapped before high-fidelity design.</text>

  <line x1="286" y1="354" x2="326" y2="354" stroke="#102A43" stroke-width="3"/>
  <line x1="446" y1="354" x2="492" y2="354" stroke="#102A43" stroke-width="3"/>
  <line x1="610" y1="354" x2="674" y2="354" stroke="#102A43" stroke-width="3"/>
  <line x1="908" y1="354" x2="955" y2="354" stroke="#102A43" stroke-width="3"/>
  <line x1="1065" y1="354" x2="1110" y2="354" stroke="#102A43" stroke-width="3"/>
  <line x1="551" y1="414" x2="551" y2="506" stroke="#102A43" stroke-width="3"/>
  <line x1="551" y1="506" x2="404" y2="506" stroke="#102A43" stroke-width="3"/>
  <line x1="404" y1="506" x2="404" y2="486" stroke="#102A43" stroke-width="3"/>
  <path d="M674 354 L662 347 L662 361 Z" fill="#102A43"/>
  <path d="M1110 354 L1098 347 L1098 361 Z" fill="#102A43"/>
  <path d="M551 506 L544 494 L558 494 Z" fill="#102A43"/>
  <path d="M404 486 L397 498 L411 498 Z" fill="#102A43"/>

  <rect x="66" y="212" width="220" height="274" rx="16" fill="url(#screenGrad)" stroke="#102A43" stroke-width="2" filter="url(#softShadow)"/>
  <rect x="82" y="230" width="188" height="26" rx="8" fill="#102A43" opacity="0.9"/>
  <circle cx="96" cy="243" r="4" fill="#FFB703"/>
  <circle cx="110" cy="243" r="4" fill="#FB8500"/>
  <text x="82" y="286" width="188" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#102A43">01 Login</text>
  <rect x="88" y="308" width="176" height="34" rx="8" fill="#FFFFFF" stroke="#BCCCDC"/>
  <rect x="88" y="354" width="176" height="34" rx="8" fill="#FFFFFF" stroke="#BCCCDC"/>
  <rect x="104" y="404" width="144" height="30" rx="15" fill="#F97316" opacity="0.88"/>
  <text x="96" y="460" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#243B53">• email + password input<tspan x="96" dy="15">• remember session</tspan><tspan x="96" dy="15">• forgot password link</tspan></text>

  <rect x="326" y="331" width="120" height="46" rx="23" fill="url(#actionGrad)" stroke="#D97706" stroke-width="2" filter="url(#softShadow)"/>
  <text x="343" y="359" width="86" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#B45309">Tap Sign In</text>

  <path d="M551 294 L611 354 L551 414 L491 354 Z" fill="#F4EFE6" stroke="#102A43" stroke-width="2.5" filter="url(#softShadow)"/>
  <text x="506" y="345" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#102A43">Auth<tspan x="506" dy="16">valid?</tspan></text>
  <rect x="614" y="331" width="58" height="46" rx="23" fill="#E6FFFA" stroke="#2F855A" stroke-width="2"/>
  <text x="632" y="359" width="22" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2F855A">Yes</text>
  <text x="562" y="480" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#B91C1C">No</text>

  <rect x="674" y="212" width="234" height="274" rx="16" fill="url(#screenGrad)" stroke="#102A43" stroke-width="2" filter="url(#glow)"/>
  <rect x="690" y="230" width="202" height="26" rx="8" fill="#102A43" opacity="0.9"/>
  <text x="704" y="286" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#102A43">02 Dashboard</text>
  <rect x="704" y="308" width="76" height="54" rx="10" fill="#FFFFFF" stroke="#BCCCDC"/>
  <rect x="792" y="308" width="76" height="54" rx="10" fill="#FFFFFF" stroke="#BCCCDC"/>
  <rect x="704" y="380" width="164" height="48" rx="10" fill="#FFFFFF" stroke="#BCCCDC"/>
  <line x1="720" y1="416" x2="750" y2="396" stroke="#2F80ED" stroke-width="3"/>
  <line x1="750" y1="396" x2="782" y2="407" stroke="#2F80ED" stroke-width="3"/>
  <line x1="782" y1="407" x2="842" y2="386" stroke="#2F80ED" stroke-width="3"/>
  <text x="704" y="460" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#243B53">• KPI summary cards<tspan x="704" dy="15">• activity feed</tspan><tspan x="704" dy="15">• report entry point</tspan></text>

  <rect x="955" y="331" width="110" height="46" rx="23" fill="url(#actionGrad)" stroke="#D97706" stroke-width="2" filter="url(#softShadow)"/>
  <text x="982" y="359" width="56" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#B45309">Open Report</text>

  <rect x="1110" y="212" width="116" height="274" rx="16" fill="url(#screenGrad)" stroke="#102A43" stroke-width="2" filter="url(#softShadow)"/>
  <rect x="1124" y="230" width="88" height="26" rx="8" fill="#102A43" opacity="0.9"/>
  <text x="1124" y="286" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#102A43">03 Detail</text>
  <rect x="1126" y="312" width="84" height="88" rx="10" fill="#FFFFFF" stroke="#BCCCDC"/>
  <rect x="1138" y="418" width="60" height="18" rx="9" fill="#F97316" opacity="0.85"/>
  <text x="1128" y="462" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#243B53">• drilldown<tspan x="1128" dy="14">• export PDF</tspan></text>

  <rect x="286" y="486" width="118" height="94" rx="14" fill="#FFF7ED" stroke="#D97706" stroke-width="2" filter="url(#softShadow)"/>
  <text x="306" y="516" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#B45309">Error Toast</text>
  <text x="304" y="542" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#7C2D12">Show message<tspan x="304" dy="14">Keep user on</tspan><tspan x="304" dy="14">Login screen</tspan></text>

  <rect x="930" y="52" width="250" height="34" rx="17" fill="#102A43" opacity="0.9"/>
  <circle cx="953" cy="69" r="6" fill="#D9E2EC"/>
  <text x="970" y="74" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#FFFFFF">Editable SVG-to-PPT wireframe system</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<path marker-end="...">` for flow arrows; marker arrowheads on paths may disappear. Use `<line>` connector segments plus small filled `<path>` triangle arrowheads.
- ❌ Relying on automatic connector rerouting or smart snapping; place orthogonal line segments explicitly.
- ❌ Putting all page details into one giant text box; keep page title, feature notes, and wireframe annotations as separate editable `<text width="...">` elements.
- ❌ Clipping or masking non-image shapes for screen cards; use rounded `<rect>` and internal primitives instead.
- ❌ Overcrowding every screen with tiny UI controls; prioritize 3–5 recognizable wireframe elements per screen.

## Composition notes
- Keep the main journey on a strong left-to-right horizontal axis through the vertical center of the slide; reserve lower space for exception branches and loops.
- Use cool blue screen cards for pages, warm peach pills for user actions, and a neutral parchment background to make the logic readable without feeling like a raw diagram.
- Put connectors behind action pills and screen cards so the action labels appear to “interrupt” the flow line.
- Preserve generous negative space between cards; the premium look comes from rhythm, clear hierarchy, and restrained feature text rather than dense flowchart complexity.