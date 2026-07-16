# SVG Recipe — Asymmetric Tri-Panel Pillar Layout (Editorial Split-Screen)

## Visual mechanism
A magazine-like split-screen: the left 38–40% of the slide stays typographic and airy, while the right 60% becomes three full-height vertical pillars with alternating treatments—photo + overlay, pale negative-space column, and dark solid column. The composition feels premium because the pillars bleed edge-to-edge, the left title is oversized, and the accent color appears only in a few controlled moments.

## SVG primitives needed
- 4× `<rect>` for the full-slide background and three full-height pillar fields
- 1× `<image>` for the editorial photo pillar
- 1× `<rect>` gradient overlay on the photo pillar
- 1× `<rect>` and 1× `<circle>` for the decorative presentation-app emblem on the left
- 1× `<text>` glyph inside the emblem
- 8× `<text>` blocks for the left headline, accent line, body copy, pillar body copy, and bottom numerals
- 15× `<path>` for hand-drawn-style outline icons and logo highlight details
- 8× `<line>` for thin editorial divider rules and corner frames
- 2× `<circle>` for icon details
- 1× `<linearGradient>` for the page background
- 1× `<radialGradient>` and 1× `<linearGradient>` for the orange emblem
- 3× `<linearGradient>` for pillar fills/overlays
- 2× `<filter>` effects: one soft shadow for the emblem and one subtle glow/shadow for oversized headline text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#c9d9c5"/>
      <stop offset="0.52" stop-color="#b9c5c9"/>
      <stop offset="1" stop-color="#8f9aad"/>
    </linearGradient>

    <radialGradient id="logoDisc" cx="58%" cy="34%" r="70%">
      <stop offset="0" stop-color="#ffb176"/>
      <stop offset="0.45" stop-color="#e75f31"/>
      <stop offset="1" stop-color="#b93119"/>
    </radialGradient>

    <linearGradient id="logoTile" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#9d2b18"/>
      <stop offset="1" stop-color="#d64523"/>
    </linearGradient>

    <linearGradient id="photoOverlay" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#a8842b" stop-opacity="0.72"/>
      <stop offset="0.48" stop-color="#524432" stop-opacity="0.62"/>
      <stop offset="1" stop-color="#20263c" stop-opacity="0.86"/>
    </linearGradient>

    <linearGradient id="pillarLight" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#cbdccf"/>
      <stop offset="0.55" stop-color="#aebbc5"/>
      <stop offset="1" stop-color="#99a3b8"/>
    </linearGradient>

    <linearGradient id="pillarDark" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#405445"/>
      <stop offset="0.45" stop-color="#2e3c3e"/>
      <stop offset="1" stop-color="#272c42"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="headlineGlow" x="-8%" y="-8%" width="116%" height="116%">
      <feOffset dx="0" dy="3"/>
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- base canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#pageBg)"/>

  <!-- right-side tri-panel pillars -->
  <image href="https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&amp;fit=crop&amp;w=700&amp;h=1400&amp;q=80"
         x="480" y="0" width="267" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="480" y="0" width="267" height="720" fill="url(#photoOverlay)"/>
  <rect x="747" y="0" width="267" height="720" fill="url(#pillarLight)"/>
  <rect x="1014" y="0" width="266" height="720" fill="url(#pillarDark)"/>

  <!-- editorial rules -->
  <line x1="480" y1="68" x2="747" y2="68" stroke="#e6e8df" stroke-width="2" opacity="0.75"/>
  <line x1="480" y1="649" x2="747" y2="649" stroke="#d9dbe2" stroke-width="1.2" opacity="0.65"/>
  <line x1="1014" y1="68" x2="1204" y2="68" stroke="#dfe6dc" stroke-width="1.6" opacity="0.8"/>
  <line x1="1204" y1="68" x2="1204" y2="175" stroke="#dfe6dc" stroke-width="1.6" opacity="0.8"/>

  <!-- left decorative presentation emblem -->
  <circle cx="200" cy="124" r="108" fill="url(#logoDisc)" filter="url(#softShadow)"/>
  <path d="M200 18 L200 124 L306 124 C303 71 256 25 200 18 Z" fill="#ffb987" opacity="0.58"/>
  <path d="M200 124 L306 124 C303 186 258 231 200 232 Z" fill="#d43c20" opacity="0.55"/>
  <rect x="60" y="62" width="128" height="128" rx="10" fill="url(#logoTile)" filter="url(#softShadow)"/>
  <text x="97" y="153" width="72" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="88" font-weight="700" fill="#f5f7f4">P</text>

  <!-- left title system -->
  <text x="270" y="126" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="300" letter-spacing="8" fill="#1d2529" text-anchor="middle">
    <tspan x="270" dy="0">A SLIDE,</tspan>
    <tspan x="270" dy="48">BEAUTIFUL</tspan>
    <tspan x="270" dy="48">AS THIS!</tspan>
  </text>

  <text x="242" y="276" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="300" letter-spacing="7" fill="#9f7a32" text-anchor="middle">
    JUST ONE
  </text>

  <text x="86" y="360" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="300" fill="#4a5664" opacity="0.72">
    <tspan x="86" dy="0">Lorem ipsum dolor sit amet,</tspan>
    <tspan x="86" dy="32">consectetur adipiscing elit,</tspan>
    <tspan x="86" dy="32">sed do eiusmod tempor</tspan>
    <tspan x="86" dy="32">incididunt ut labore et</tspan>
    <tspan x="86" dy="32">dolore magna aliqua. Ut</tspan>
    <tspan x="86" dy="32">enim ad minim veniam.</tspan>
  </text>

  <text x="58" y="459" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="74" font-weight="800" letter-spacing="1" fill="#ffffff" filter="url(#headlineGlow)">
    4 SECTIONS
  </text>
  <text x="56" y="617" width="435" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="124" font-weight="800" letter-spacing="4" fill="#ffffff" filter="url(#headlineGlow)">
    SLIDE
  </text>

  <!-- pillar 01 icon: speech bubble + pencil -->
  <path d="M596 84 C579 91 574 110 582 125 L579 139 L593 132 C609 139 630 132 636 114 C642 95 622 77 596 84 Z"
        fill="none" stroke="#dfe6dc" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity="0.86"/>
  <path d="M604 118 L626 96" fill="none" stroke="#dfe6dc" stroke-width="4" stroke-linecap="round"/>
  <path d="M625 96 L631 102 L609 124 L599 128 L603 118 Z"
        fill="none" stroke="#dfe6dc" stroke-width="3" stroke-linejoin="round"/>

  <text x="613" y="248" width="158" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="300" fill="#eef2ec" text-anchor="middle">
    <tspan x="613" dy="0">Lorem ipsum</tspan>
    <tspan x="613" dy="32">dolor sit amet,</tspan>
    <tspan x="613" dy="32">consectetur</tspan>
    <tspan x="613" dy="32">adipiscing elit,</tspan>
    <tspan x="613" dy="32">sed do eiusmod</tspan>
    <tspan x="613" dy="32">tempor incididunt</tspan>
    <tspan x="613" dy="32">ut labore et</tspan>
    <tspan x="613" dy="32">dolore magna</tspan>
    <tspan x="613" dy="32">aliqua. Ut enim</tspan>
  </text>
  <text x="613" y="635" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="300" letter-spacing="8" fill="#e6e8ef" text-anchor="middle">01</text>

  <!-- pillar 02 icon: cloud gear + bulb -->
  <path d="M872 82 C866 82 863 87 863 91 C855 90 849 96 849 103 C842 106 840 115 846 120 C842 128 849 137 858 136 C862 143 874 143 878 136 C887 139 896 132 894 123 C901 119 901 108 893 105 C895 96 887 90 879 93 C878 87 875 82 872 82 Z"
        fill="none" stroke="#303a39" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M862 105 C862 99 868 95 874 98 C880 101 881 109 876 113 C873 116 873 119 873 122"
        fill="none" stroke="#303a39" stroke-width="4" stroke-linecap="round"/>
  <line x1="867" y1="128" x2="877" y2="128" stroke="#303a39" stroke-width="4" stroke-linecap="round"/>
  <circle cx="872" cy="101" r="2.6" fill="#303a39"/>

  <text x="880" y="248" width="158" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="300" fill="#3e484e" opacity="0.72" text-anchor="middle">
    <tspan x="880" dy="0">Lorem ipsum</tspan>
    <tspan x="880" dy="32">dolor sit amet,</tspan>
    <tspan x="880" dy="32">consectetur</tspan>
    <tspan x="880" dy="32">adipiscing elit,</tspan>
    <tspan x="880" dy="32">sed do eiusmod</tspan>
    <tspan x="880" dy="32">tempor incididunt</tspan>
    <tspan x="880" dy="32">ut labore et</tspan>
    <tspan x="880" dy="32">dolore magna</tspan>
    <tspan x="880" dy="32">aliqua. Ut enim</tspan>
  </text>
  <text x="880" y="635" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="300" letter-spacing="8" fill="#252a3a" text-anchor="middle">02</text>

  <!-- pillar 03 icon: open book + pencil -->
  <path d="M1118 82 L1145 82 C1151 82 1156 85 1161 89 L1161 135 C1156 132 1151 130 1145 130 L1118 130 Z"
        fill="none" stroke="#dfe6dc" stroke-width="4" stroke-linejoin="round" opacity="0.86"/>
  <path d="M1161 89 C1166 85 1171 82 1177 82 L1177 130 C1170 130 1165 132 1161 135"
        fill="none" stroke="#dfe6dc" stroke-width="4" stroke-linejoin="round" opacity="0.86"/>
  <line x1="1127" y1="96" x2="1139" y2="96" stroke="#dfe6dc" stroke-width="4" stroke-linecap="round" opacity="0.86"/>
  <line x1="1127" y1="112" x2="1139" y2="112" stroke="#dfe6dc" stroke-width="4" stroke-linecap="round" opacity="0.86"/>
  <path d="M1168 124 L1194 98 L1201 105 L1175 131 L1164 135 Z"
        fill="none" stroke="#dfe6dc" stroke-width="4" stroke-linejoin="round" opacity="0.86"/>

  <text x="1147" y="248" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="300" fill="#e8ede8" opacity="0.82" text-anchor="middle">
    <tspan x="1147" dy="0">Lorem ipsum</tspan>
    <tspan x="1147" dy="32">dolor sit amet,</tspan>
    <tspan x="1147" dy="32">consectetur</tspan>
    <tspan x="1147" dy="32">adipiscing elit,</tspan>
    <tspan x="1147" dy="32">sed do eiusmod</tspan>
    <tspan x="1147" dy="32">tempor incididunt</tspan>
    <tspan x="1147" dy="32">ut labore et</tspan>
    <tspan x="1147" dy="32">dolore magna</tspan>
    <tspan x="1147" dy="32">aliqua. Ut enim</tspan>
  </text>
  <text x="1147" y="635" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="300" letter-spacing="8" fill="#dce1ea" text-anchor="middle">03</text>
</svg>
```

## Avoid in this skill
- ❌ Using three small floating cards instead of full-bleed pillars; the technique depends on edge-to-edge vertical columns.
- ❌ Applying `clip-path` to text or rectangles; only use it on `<image>` if a custom image crop is required.
- ❌ Using `marker-end` for arrows or inherited markers inside icon groups; draw icon strokes directly with `<path>` and `<line>`.
- ❌ Overfilling the left panel with body copy; the left side should feel like editorial whitespace, not a report page.
- ❌ Making all three pillars the same color treatment; the rhythm comes from photo / light / dark alternation.

## Composition notes
- Keep the left content area around 480–510 px wide on a 1280 px canvas; the three pillars should divide the remaining width evenly.
- Let the pillars bleed to the top and bottom edges with no outer margins, creating a strong architectural split.
- Use one warm accent color—burnt orange or ochre—sparingly on the left title/emblem and in the photo overlay.
- Center-align pillar icons, text, and numerals so each narrow column reads like a self-contained editorial module.