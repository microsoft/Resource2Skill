# SVG Recipe — Vertical Infographic Canvas

## Visual mechanism
A tall-scroll infographic is built from stacked, full-width horizontal color bands that guide the reader down a continuous narrative. Each band repeats a modular rhythm: numbered node, concise headline, short explanation, and a simple icon, with a strong framed title block at the top.

## SVG primitives needed
- 16× `<rect>` for the page base, header, alternating narrative bands, framed title card, icon badges, photo border, and footer
- 7× `<circle>` for timeline nodes, numbered steps, and circular icon details
- 1× `<ellipse>` for the eye icon
- 10× `<line>` for the vertical timeline spine and simple icon strokes
- 7× `<path>` for decorative header waves and editable flat icons
- 1× `<image>` for a clipped editorial/header photo accent
- 1× `<clipPath>` using a rounded `<rect>` applied only to the header image
- 3× `<linearGradient>` for premium header and subtle band depth
- 1× `<filter id="softShadow">` applied to cards/badges for gentle elevation
- Multiple `<text>` elements with explicit `width` attributes for title, intro, step labels, descriptions, and footer metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#41566A"/>
      <stop offset="58%" stop-color="#546A7B"/>
      <stop offset="100%" stop-color="#2F4050"/>
    </linearGradient>
    <linearGradient id="blueBand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7399AC"/>
      <stop offset="100%" stop-color="#6590A6"/>
    </linearGradient>
    <linearGradient id="sandBand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E6C08F"/>
      <stop offset="100%" stop-color="#D9AD73"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="7" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photoRound">
      <rect x="958" y="36" width="226" height="132" rx="26" ry="26"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F3EA"/>
  <rect x="0" y="0" width="1280" height="158" fill="url(#headerGrad)"/>
  <path d="M0 126 C150 102 250 152 390 128 C550 100 650 145 800 122 C985 94 1095 144 1280 112 L1280 158 L0 158 Z"
        fill="#FFFFFF" opacity="0.12"/>

  <rect x="82" y="32" width="544" height="92" rx="4" fill="#F7F3EA" filter="url(#softShadow)"/>
  <rect x="101" y="48" width="506" height="60" rx="2" fill="none" stroke="#546A7B" stroke-width="6"/>
  <text x="126" y="73" width="456" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800"
        letter-spacing="2" fill="#41566A">
    REMOTE WORK RESET
  </text>
  <text x="104" y="140" width="575" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#EAF0F2">
    Five habits for building a calm, productive day when your office is also your home.
  </text>

  <image href="https://images.example.com/editorial/home-office-laptop-plants-warm-light.jpg"
         x="958" y="36" width="226" height="132" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoRound)"/>
  <rect x="958" y="36" width="226" height="132" rx="26" fill="none" stroke="#F7F3EA" stroke-width="5"/>

  <rect x="0" y="158" width="1280" height="104" fill="url(#blueBand)"/>
  <rect x="0" y="262" width="1280" height="104" fill="url(#sandBand)"/>
  <rect x="0" y="366" width="1280" height="104" fill="#CCD6D9"/>
  <rect x="0" y="470" width="1280" height="104" fill="url(#blueBand)"/>
  <rect x="0" y="574" width="1280" height="104" fill="url(#sandBand)"/>

  <line x1="248" y1="194" x2="248" y2="642" stroke="#FFFFFF" stroke-width="5" opacity="0.48"/>

  <circle cx="248" cy="210" r="31" fill="#41566A" stroke="#FFFFFF" stroke-width="5"/>
  <text x="238" y="222" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">1</text>
  <text x="310" y="198" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#FFFFFF">ESTABLISH A ROUTINE</text>
  <text x="310" y="225" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#EEF7FA">
    <tspan x="310" dy="0">Anchor the day with a start ritual, fixed focus blocks,</tspan>
    <tspan x="310" dy="18">and a clear shutdown moment.</tspan>
  </text>
  <rect x="988" y="177" width="124" height="66" rx="18" fill="#FFFFFF" opacity="0.24" filter="url(#softShadow)"/>
  <circle cx="1050" cy="210" r="21" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <line x1="1050" y1="210" x2="1050" y2="196" stroke="#FFFFFF" stroke-width="4"/>
  <line x1="1050" y1="210" x2="1062" y2="216" stroke="#FFFFFF" stroke-width="4"/>

  <circle cx="248" cy="314" r="31" fill="#41566A" stroke="#FFFFFF" stroke-width="5"/>
  <text x="238" y="326" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">2</text>
  <text x="310" y="302" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#263238">SCHEDULE BREAKS</text>
  <text x="310" y="329" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#384850">
    <tspan x="310" dy="0">Use short resets between meetings to stretch, hydrate,</tspan>
    <tspan x="310" dy="18">and prevent the day from becoming one long call.</tspan>
  </text>
  <rect x="988" y="281" width="124" height="66" rx="18" fill="#FFFFFF" opacity="0.35" filter="url(#softShadow)"/>
  <path d="M1028 310 h35 v14 c0 12 -8 20 -20 20 h-7 c-12 0 -20 -8 -20 -20 v-14 h12"
        fill="none" stroke="#41566A" stroke-width="5"/>
  <path d="M1064 314 c14 0 15 22 0 22" fill="none" stroke="#41566A" stroke-width="5"/>
  <path d="M1030 294 c-7 -8 7 -12 0 -20 M1050 294 c-7 -8 7 -12 0 -20"
        fill="none" stroke="#41566A" stroke-width="4"/>

  <circle cx="248" cy="418" r="31" fill="#41566A" stroke="#FFFFFF" stroke-width="5"/>
  <text x="238" y="430" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">3</text>
  <text x="310" y="406" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#263238">PROTECT YOUR EYES</text>
  <text x="310" y="433" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#384850">
    <tspan x="310" dy="0">Every twenty minutes, look away from the screen</tspan>
    <tspan x="310" dy="18">and soften the visual load.</tspan>
  </text>
  <rect x="988" y="385" width="124" height="66" rx="18" fill="#2F4050" opacity="0.12" filter="url(#softShadow)"/>
  <ellipse cx="1050" cy="418" rx="34" ry="20" fill="none" stroke="#41566A" stroke-width="5"/>
  <circle cx="1050" cy="418" r="9" fill="#41566A"/>

  <circle cx="248" cy="522" r="31" fill="#41566A" stroke="#FFFFFF" stroke-width="5"/>
  <text x="238" y="534" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">4</text>
  <text x="310" y="510" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#FFFFFF">CREATE A WORKSPACE</text>
  <text x="310" y="537" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#EEF7FA">
    <tspan x="310" dy="0">Choose one visual zone for deep work, even if it is</tspan>
    <tspan x="310" dy="18">a small corner of the dining table.</tspan>
  </text>
  <rect x="988" y="489" width="124" height="66" rx="18" fill="#FFFFFF" opacity="0.24" filter="url(#softShadow)"/>
  <rect x="1022" y="505" width="56" height="34" rx="3" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <line x1="1050" y1="539" x2="1050" y2="550" stroke="#FFFFFF" stroke-width="5"/>
  <line x1="1028" y1="550" x2="1072" y2="550" stroke="#FFFFFF" stroke-width="5"/>

  <circle cx="248" cy="626" r="31" fill="#41566A" stroke="#FFFFFF" stroke-width="5"/>
  <text x="238" y="638" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">5</text>
  <text x="310" y="614" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#263238">AVOID DISTRACTIONS</text>
  <text x="310" y="641" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#384850">
    <tspan x="310" dy="0">Turn notifications into scheduled inputs instead of</tspan>
    <tspan x="310" dy="18">constant interruptions.</tspan>
  </text>
  <rect x="988" y="593" width="124" height="66" rx="18" fill="#FFFFFF" opacity="0.35" filter="url(#softShadow)"/>
  <path d="M1050 598 L1080 610 L1076 634 C1072 650 1062 658 1050 664 C1038 658 1028 650 1024 634 L1020 610 Z"
        fill="none" stroke="#41566A" stroke-width="5"/>
  <line x1="1037" y1="631" x2="1063" y2="619" stroke="#41566A" stroke-width="5"/>
  <line x1="1037" y1="619" x2="1063" y2="631" stroke="#41566A" stroke-width="5"/>

  <rect x="0" y="678" width="1280" height="42" fill="#2F4050"/>
  <text x="92" y="704" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="1.5" fill="#DDE6E8">
    EXPORT AS PDF  •  EMBED ONLINE  •  READ AS A CONTINUOUS SCROLL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Splitting the story into separate slide-like boxes with heavy gaps; the technique should feel like one continuous vertical page.
- ❌ Using `<mask>` or clipping non-image objects for band transitions; keep bands as editable rectangles and decorative waves as editable paths.
- ❌ Overloading each band with long paragraphs; vertical infographics work best with headline-first scanning.
- ❌ Tiny body text across the full width; constrain content to a safe central column with generous side margins.
- ❌ Relying on image-only infographic exports; build the bands, icons, numbers, and text as editable SVG/PPT shapes.

## Composition notes
- Treat the header as the strongest visual anchor: framed title on the left, optional clipped editorial image on the right, and a short intro beneath.
- Use equal-height horizontal bands for rhythm; alternate muted colors so the reader can parse each step instantly while scrolling.
- Keep a vertical spine and numbered nodes aligned consistently; this gives the page a timeline feel without needing arrows.
- For a true long-form export, extend the same module pattern down a taller custom page; preserve the same margins, band height ratio, and title-to-section hierarchy.