# SVG Recipe — Interactive Navigation Dashboard

## Visual mechanism
Create an app-like “hub” slide with large, tactile navigation cards that read as clickable zones, each labeled with its destination and supported by iconography, glow, and depth. The slide should feel like a premium product dashboard: dark ambient background, luminous accents, a clear title hierarchy, and consistent utility navigation cues.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark gradient background.
- 3× large translucent `<path>` blobs for ambient decorative depth.
- 1× `<radialGradient>` for cyan/purple background glow.
- 1× `<linearGradient>` for the main dark background.
- 4× `<linearGradient>` fills for distinct navigation button accents.
- 1× `<filter id="softShadow">` applied to button cards and panels.
- 1× `<filter id="glow">` applied to accent rings/icons.
- 1× `<clipPath>` with rounded `<rect>` applied to a dashboard preview `<image>`.
- 1× clipped `<image>` for a visual “live dashboard preview” area.
- 1× main glassmorphism `<rect>` panel for dashboard content.
- 4× rounded `<rect>` navigation cards for clickable zones.
- 4× smaller rounded `<rect>` destination chips such as “SLIDE 02”.
- 4× icon groups built from `<circle>`, `<rect>`, `<line>`, and `<path>`.
- Multiple `<text>` elements with explicit `width` for title, subtitle, button labels, helper text, and utility nav labels.
- Several `<line>` primitives for dashboard graph/connector details, without marker arrows.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#0B1020"/>
      <stop offset="55%" stop-color="#121B2C"/>
      <stop offset="100%" stop-color="#1C2633"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="50%" cy="42%" r="65%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.28"/>
      <stop offset="45%" stop-color="#9B5CFF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#0B1020" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="cyanBtn" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00D4FF"/>
      <stop offset="100%" stop-color="#006DFF"/>
    </linearGradient>
    <linearGradient id="pinkBtn" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF6FB7"/>
      <stop offset="100%" stop-color="#9B3DFF"/>
    </linearGradient>
    <linearGradient id="limeBtn" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7CFF8A"/>
      <stop offset="100%" stop-color="#1FBF75"/>
    </linearGradient>
    <linearGradient id="amberBtn" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFD166"/>
      <stop offset="100%" stop-color="#FF7A00"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="previewClip">
      <rect x="806" y="166" width="314" height="190" rx="24"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#ambientGlow)"/>
  <path d="M-60,120 C160,20 330,80 460,190 C250,210 90,310 -50,430 Z" fill="#00BFFF" opacity="0.08"/>
  <path d="M930,-40 C1120,10 1260,130 1340,280 C1140,240 970,300 840,410 C820,230 840,70 930,-40 Z" fill="#FF6FB7" opacity="0.08"/>
  <path d="M650,640 C810,520 1010,520 1200,610 C1040,750 820,790 620,730 Z" fill="#7CFF8A" opacity="0.07"/>

  <text x="80" y="82" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#FFFFFF">Interactive Navigation Dashboard</text>
  <text x="84" y="124" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#AEB9C8">Choose a module below to jump directly into the content. Use the persistent home button on spoke slides to return here.</text>

  <rect x="1030" y="56" width="150" height="42" rx="21" fill="#FFFFFF" opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.18"/>
  <circle cx="1054" cy="77" r="7" fill="#7CFF8A" filter="url(#glow)"/>
  <text x="1070" y="83" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#EAF2FF">HUB / HOME</text>

  <rect x="74" y="158" width="1050" height="228" rx="32" fill="#FFFFFF" opacity="0.075" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <text x="114" y="205" width="400" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Executive Control Center</text>
  <text x="116" y="237" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#B9C5D6">A non-linear presentation structure: each card acts like a native PowerPoint action button linked to a target slide.</text>

  <rect x="116" y="270" width="126" height="66" rx="18" fill="#0B1324" stroke="#00BFFF" stroke-opacity="0.4"/>
  <text x="136" y="296" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA0B8">Modules</text>
  <text x="136" y="322" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">04</text>
  <rect x="264" y="270" width="126" height="66" rx="18" fill="#0B1324" stroke="#FF6FB7" stroke-opacity="0.4"/>
  <text x="284" y="296" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA0B8">Paths</text>
  <text x="284" y="322" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">12</text>
  <rect x="412" y="270" width="126" height="66" rx="18" fill="#0B1324" stroke="#7CFF8A" stroke-opacity="0.4"/>
  <text x="432" y="296" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA0B8">Status</text>
  <text x="432" y="322" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">LIVE</text>

  <image x="806" y="166" width="314" height="190" clip-path="url(#previewClip)" href="https://images.example.com/premium-dark-analytics-dashboard-preview.png"/>
  <rect x="806" y="166" width="314" height="190" rx="24" fill="none" stroke="#FFFFFF" stroke-opacity="0.22"/>
  <line x1="834" y1="315" x2="1090" y2="315" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="2"/>
  <line x1="834" y1="292" x2="885" y2="270" stroke="#00BFFF" stroke-width="4"/>
  <line x1="885" y1="270" x2="938" y2="285" stroke="#00BFFF" stroke-width="4"/>
  <line x1="938" y1="285" x2="998" y2="240" stroke="#00BFFF" stroke-width="4"/>
  <line x1="998" y1="240" x2="1088" y2="258" stroke="#00BFFF" stroke-width="4"/>

  <g id="nav-card-strategy">
    <rect x="82" y="438" width="260" height="162" rx="30" fill="url(#cyanBtn)" filter="url(#softShadow)"/>
    <circle cx="128" cy="486" r="24" fill="#FFFFFF" opacity="0.18" filter="url(#glow)"/>
    <path d="M119,488 L129,474 L139,488 L132,488 L132,501 L126,501 L126,488 Z" fill="#FFFFFF"/>
    <text x="116" y="541" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Strategy Map</text>
    <text x="116" y="567" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#EAF8FF">Jump to objectives, bets, and priorities.</text>
    <rect x="218" y="462" width="86" height="28" rx="14" fill="#001A33" opacity="0.38"/>
    <text x="236" y="481" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">SLIDE 02</text>
  </g>

  <g id="nav-card-market">
    <rect x="382" y="438" width="260" height="162" rx="30" fill="url(#pinkBtn)" filter="url(#softShadow)"/>
    <circle cx="428" cy="486" r="24" fill="#FFFFFF" opacity="0.18" filter="url(#glow)"/>
    <circle cx="428" cy="486" r="12" fill="none" stroke="#FFFFFF" stroke-width="4"/>
    <line x1="438" y1="496" x2="449" y2="507" stroke="#FFFFFF" stroke-width="4"/>
    <text x="416" y="541" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Market Scan</text>
    <text x="416" y="567" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFF0FA">Open customer, competitor, and trend views.</text>
    <rect x="518" y="462" width="86" height="28" rx="14" fill="#26002E" opacity="0.35"/>
    <text x="536" y="481" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">SLIDE 05</text>
  </g>

  <g id="nav-card-operations">
    <rect x="682" y="438" width="260" height="162" rx="30" fill="url(#limeBtn)" filter="url(#softShadow)"/>
    <circle cx="728" cy="486" r="24" fill="#FFFFFF" opacity="0.18" filter="url(#glow)"/>
    <rect x="715" y="474" width="8" height="25" rx="4" fill="#FFFFFF"/>
    <rect x="727" y="464" width="8" height="35" rx="4" fill="#FFFFFF"/>
    <rect x="739" y="481" width="8" height="18" rx="4" fill="#FFFFFF"/>
    <text x="716" y="541" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Operations</text>
    <text x="716" y="567" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#F0FFF4">Review KPIs, bottlenecks, and service health.</text>
    <rect x="818" y="462" width="86" height="28" rx="14" fill="#002716" opacity="0.35"/>
    <text x="836" y="481" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">SLIDE 08</text>
  </g>

  <g id="nav-card-decisions">
    <rect x="982" y="438" width="216" height="162" rx="30" fill="url(#amberBtn)" filter="url(#softShadow)"/>
    <circle cx="1028" cy="486" r="24" fill="#FFFFFF" opacity="0.18" filter="url(#glow)"/>
    <path d="M1017,486 C1022,474 1038,474 1043,486 C1038,498 1022,498 1017,486 Z" fill="none" stroke="#FFFFFF" stroke-width="4"/>
    <circle cx="1030" cy="486" r="4" fill="#FFFFFF"/>
    <text x="1016" y="541" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Decisions</text>
    <text x="1016" y="567" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFF7E2">Go to options, risks, and next steps.</text>
    <rect x="1082" y="462" width="86" height="28" rx="14" fill="#331500" opacity="0.35"/>
    <text x="1100" y="481" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">SLIDE 11</text>
  </g>

  <text x="84" y="666" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7F8FA6">Implementation note: assign each full card group a PowerPoint hyperlink/action target after conversion. Keep matching “Back to Dashboard” buttons on every spoke slide.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on hover states, sound triggers, animation, or SVG `<animate>`; PowerPoint action behavior should be assigned as native slide hyperlinks after SVG-to-PPT conversion.
- ❌ Do not use `<a href="...">` wrappers as the primary interaction model; translated PowerPoint shapes should receive native click actions instead.
- ❌ Do not make tiny text-only links; clickable zones should be large rounded cards or pills with strong affordance.
- ❌ Do not use `marker-end` on paths for navigation arrows; if arrows are needed, use editable `<line>` elements and separate triangle/path arrowheads.
- ❌ Do not apply `filter` to `<line>` elements; use glow/shadow on surrounding cards, icons, paths, or text instead.

## Composition notes
- Keep the hub slide highly scannable: title and instructions in the upper-left, utility/home status in the upper-right, and the main navigation grid in the lower half.
- Make each action card visually distinct through color, icon, and destination chip, but keep consistent size and corner radius so the deck feels like a coherent app.
- Preserve generous negative space around the navigation cards; avoid crowding the buttons with long descriptions.
- On spoke/content slides, repeat a muted “Back to Dashboard” pill in the exact same top-right location to create predictable navigation behavior.