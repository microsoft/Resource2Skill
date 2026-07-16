# SVG Recipe — Dynamic Color-Coded Structural Ribbon

## Visual mechanism
A persistent bottom navigation ribbon maps the deck’s full section structure with flush, color-coded segments. The active section doubles in width and rises upward like a lifted tab, using larger bold typography and a soft shadow to signal “you are here.”

## SVG primitives needed
- 1× `<rect>` for the full-slide premium light-gray background
- 2× `<radialGradient>` / `<linearGradient>` for subtle ambient background and card accent polish
- 2× organic `<path>` blobs for quiet background energy behind the content
- 1× elevated `<rect>` for the main white content card
- 1× `<filter id="softShadow">` applied to the content card
- 1× `<filter id="tabShadow">` applied to the active ribbon tab
- 5× inactive ribbon `<rect>` segments anchored to the bottom edge
- 1× active ribbon `<path>` segment with rounded top corners and square/clipped bottom edge
- 6× ribbon `<text>` labels, with active label larger and bold
- Multiple small `<rect>`, `<circle>`, and `<line>` elements inside the card to demonstrate section-aware content
- Several `<text>` blocks with explicit `width` attributes for title, metadata, card copy, and labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="30%" r="80%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="55%" stop-color="#f5f6f8"/>
      <stop offset="100%" stop-color="#eceff3"/>
    </radialGradient>

    <linearGradient id="cardTopSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f7f9fc"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-15%" width="120%" height="135%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="tabShadow" x="-8%" y="-35%" width="116%" height="160%">
      <feOffset dx="0" dy="-6" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <path d="M1040 64 C1138 56 1206 114 1218 202 C1231 297 1145 335 1058 315 C958 292 914 220 946 142 C961 105 991 75 1040 64 Z"
        fill="#4285F4" opacity="0.07"/>
  <path d="M73 484 C151 423 246 430 299 492 C354 557 305 621 221 629 C135 637 58 595 46 541 C41 518 50 501 73 484 Z"
        fill="#EB576E" opacity="0.06"/>

  <text x="80" y="82" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#7b8190" letter-spacing="2">
    SECTION 03 / 06
  </text>
  <text x="80" y="139" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#4285F4">
    PRODUCT
  </text>
  <text x="82" y="177" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#596070">
    The active ribbon tab mirrors the current chapter color and creates spatial context across a long deck.
  </text>

  <rect x="80" y="220" width="1120" height="340" rx="28" fill="url(#cardTopSheen)" filter="url(#softShadow)"/>
  <rect x="80" y="220" width="10" height="340" rx="5" fill="#4285F4"/>

  <text x="122" y="276" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="750" fill="#18212f">
    Product narrative checkpoint
  </text>
  <text x="122" y="316" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#667085">
    Use this slide body for the section’s key argument. The ribbon remains fixed, while only the elevated tab changes by section.
  </text>

  <rect x="122" y="358" width="168" height="46" rx="23" fill="#EAF2FF"/>
  <circle cx="148" cy="381" r="9" fill="#4285F4"/>
  <text x="168" y="388" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#2f6fd6">
    Active tab
  </text>

  <rect x="314" y="358" width="190" height="46" rx="23" fill="#F2F4F7"/>
  <circle cx="340" cy="381" r="9" fill="#B0B4B8"/>
  <text x="360" y="388" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="650" fill="#667085">
    Inactive tabs
  </text>

  <rect x="650" y="275" width="438" height="34" rx="17" fill="#F2F5FA"/>
  <rect x="650" y="275" width="206" height="34" rx="17" fill="#4285F4"/>
  <text x="672" y="298" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">
    Progress: 43%
  </text>

  <line x1="672" y1="364" x2="1058" y2="364" stroke="#E4E8EF" stroke-width="3"/>
  <circle cx="672" cy="364" r="12" fill="#B0B4B8"/>
  <circle cx="749" cy="364" r="12" fill="#EB576E"/>
  <circle cx="826" cy="364" r="15" fill="#4285F4"/>
  <circle cx="903" cy="364" r="12" fill="#34A853"/>
  <circle cx="980" cy="364" r="12" fill="#FBBC05"/>
  <circle cx="1058" cy="364" r="12" fill="#203348"/>

  <text x="650" y="434" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#18212f">
    6-part structure
  </text>
  <text x="652" y="471" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#667085">
    The audience always sees what came before, where they are now, and what remains.
  </text>

  <!-- Bottom structural ribbon: active index = Product -->
  <rect x="0" y="672" width="182.86" height="56" fill="#B0B4B8"/>
  <rect x="182.86" y="672" width="182.86" height="56" fill="#EB576E"/>
  <rect x="731.43" y="672" width="182.86" height="56" fill="#34A853"/>
  <rect x="914.29" y="672" width="182.86" height="56" fill="#FBBC05"/>
  <rect x="1097.14" y="672" width="182.86" height="56" fill="#203348"/>

  <path d="M365.71 720 L365.71 652 C365.71 640.95 374.66 632 385.71 632 L711.43 632 C722.48 632 731.43 640.95 731.43 652 L731.43 720 Z"
        fill="#4285F4" filter="url(#tabShadow)"/>

  <text x="0" y="704" width="182.86" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="650" fill="#32363d">
    Intro
  </text>
  <text x="182.86" y="704" width="182.86" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="650" fill="#ffffff">
    Status Quo
  </text>
  <text x="365.71" y="684" width="365.72" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">
    Product
  </text>
  <text x="731.43" y="704" width="182.86" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="650" fill="#ffffff">
    Market
  </text>
  <text x="914.29" y="704" width="182.86" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#2c2c2c">
    Why Us
  </text>
  <text x="1097.14" y="704" width="182.86" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="650" fill="#ffffff">
    Ask
  </text>
</svg>
```

## Avoid in this skill
- ❌ Leaving 1–2 px gaps between ribbon segments; calculate widths so the ribbon spans exactly `0–1280`.
- ❌ Using equal-width active and inactive tabs; the technique depends on the active tab being both taller and wider.
- ❌ Applying shadow filters to `<line>` elements; use the shadow only on the active `<path>` tab or card `<rect>`.
- ❌ Using `<mask>` or clipping on non-image shapes to create the tab; draw the active tab directly as a rounded-top `<path>`.
- ❌ Omitting `width` on ribbon labels; PowerPoint text boxes need explicit width for reliable placement.

## Composition notes
- Keep the bottom ribbon persistent and flush to the slide edge; inactive tabs should sit low, while the active tab rises into the slide.
- Let the active section color echo elsewhere on the slide: title color, card accent rail, progress pill, or diagram highlight.
- Preserve generous negative space above the ribbon so it reads as navigation, not as a competing chart.
- Use dark text only on pale tabs like gray or yellow; use white text on saturated magenta, blue, green, and navy.