# SVG Recipe — Interlocking Diamond Image Grid

## Visual mechanism
A dense cluster of image-cropped diamonds occupies one side of the slide, mixing photography, solid color diamonds, and hollow outline diamonds into an interlocking diagonal grid. The opposite side stays clean and typographic, letting the angled image lattice create motion and executive-keynote polish.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 1× `<linearGradient>` for a subtle background wash
- 1× `<clipPath id="diamondClip">` with a diamond `<path>` used only on `<image>` elements
- 6× `<image>` elements clipped to diamond shapes for portfolio/team/value photography
- 6× `<path>` shadow diamonds behind the clipped images
- 5× `<path>` hollow diamond outlines for interlocking accent structure
- 4× `<path>` solid diamonds for navy and burgundy visual anchors
- 4× small white `<path>` icon marks inside solid diamonds
- 1× `<filter id="softShadow">` applied to diamond paths for depth
- 1× `<filter id="titleGlow">` applied subtly to the accent label
- 4× `<text>` blocks with explicit `width` attributes for title, subtitle, kicker, and caption
- 2× `<line>` elements for restrained typographic dividers

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="62%" stop-color="#F7F3EF"/>
      <stop offset="100%" stop-color="#ECE5DF"/>
    </linearGradient>

    <linearGradient id="navyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2F465E"/>
      <stop offset="100%" stop-color="#1F3446"/>
    </linearGradient>

    <linearGradient id="burgundyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#A33B48"/>
      <stop offset="100%" stop-color="#7E2434"/>
    </linearGradient>

    <clipPath id="diamondClip" clipPathUnits="objectBoundingBox">
      <path d="M .5 0 L 1 .5 L .5 1 L 0 .5 Z"/>
    </clipPath>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <!-- Left-side editorial typography -->
  <line x1="84" y1="102" x2="188" y2="102" stroke="#8E2836" stroke-width="7"/>
  <text x="84" y="142" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="3" fill="#8E2836">
    PORTFOLIO OVERVIEW
  </text>

  <text x="82" y="236" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="62" font-weight="800" fill="#151B22">
    <tspan x="82" dy="0">Interlocking</tspan>
    <tspan x="82" dy="72">Product</tspan>
    <tspan x="82" dy="72">Ecosystem</tspan>
  </text>

  <text x="86" y="492" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="21" fill="#4D5862">
    A diagonal image grid turns related teams, products, and values into one connected visual system.
  </text>

  <line x1="86" y1="578" x2="292" y2="578" stroke="#C9C9C9" stroke-width="2"/>
  <text x="86" y="620" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#233446">
    Your Company Name
  </text>

  <!-- Decorative large outline diamonds behind the grid -->
  <path d="M 980 18 L 1158 196 L 980 374 L 802 196 Z" fill="none" stroke="#D1D1D1" stroke-width="10" opacity=".65"/>
  <path d="M 1082 168 L 1272 358 L 1082 548 L 892 358 Z" fill="none" stroke="#8E2836" stroke-width="13" opacity=".88"/>
  <path d="M 760 252 L 924 416 L 760 580 L 596 416 Z" fill="none" stroke="#C8C8C8" stroke-width="8" opacity=".7"/>
  <path d="M 1162 420 L 1318 576 L 1162 732 L 1006 576 Z" fill="none" stroke="#233446" stroke-width="10" opacity=".18"/>
  <path d="M 694 54 L 818 178 L 694 302 L 570 178 Z" fill="none" stroke="#8E2836" stroke-width="8" opacity=".28"/>

  <!-- Image diamond 1 -->
  <path d="M 807 56 L 901 150 L 807 244 L 713 150 Z" fill="#000000" opacity=".18" filter="url(#softShadow)"/>
  <image x="713" y="56" width="188" height="188" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/corporate-product-lab-team-collaboration.jpg"
         clip-path="url(#diamondClip)"/>

  <!-- Image diamond 2 -->
  <path d="M 1000 56 L 1094 150 L 1000 244 L 906 150 Z" fill="#000000" opacity=".18" filter="url(#softShadow)"/>
  <image x="906" y="56" width="188" height="188" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/industrial-design-detail-closeup.jpg"
         clip-path="url(#diamondClip)"/>

  <!-- Image diamond 3 -->
  <path d="M 904 152 L 1002 250 L 904 348 L 806 250 Z" fill="#000000" opacity=".2" filter="url(#softShadow)"/>
  <image x="806" y="152" width="196" height="196" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/executive-workshop-whiteboard-strategy.jpg"
         clip-path="url(#diamondClip)"/>

  <!-- Image diamond 4 -->
  <path d="M 1098 252 L 1196 350 L 1098 448 L 1000 350 Z" fill="#000000" opacity=".2" filter="url(#softShadow)"/>
  <image x="1000" y="252" width="196" height="196" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/premium-product-interface-dashboard.jpg"
         clip-path="url(#diamondClip)"/>

  <!-- Image diamond 5 -->
  <path d="M 806 350 L 900 444 L 806 538 L 712 444 Z" fill="#000000" opacity=".18" filter="url(#softShadow)"/>
  <image x="712" y="350" width="188" height="188" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/diverse-team-portrait-modern-office.jpg"
         clip-path="url(#diamondClip)"/>

  <!-- Image diamond 6 -->
  <path d="M 1000 446 L 1094 540 L 1000 634 L 906 540 Z" fill="#000000" opacity=".18" filter="url(#softShadow)"/>
  <image x="906" y="446" width="188" height="188" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/technology-manufacturing-detail-blue-light.jpg"
         clip-path="url(#diamondClip)"/>

  <!-- Solid anchor diamonds -->
  <path d="M 711 252 L 795 336 L 711 420 L 627 336 Z" fill="url(#navyGrad)" filter="url(#softShadow)"/>
  <path d="M 1190 108 L 1260 178 L 1190 248 L 1120 178 Z" fill="url(#burgundyGrad)" filter="url(#softShadow)"/>
  <path d="M 904 350 L 984 430 L 904 510 L 824 430 Z" fill="url(#burgundyGrad)" filter="url(#softShadow)"/>
  <path d="M 1168 498 L 1248 578 L 1168 658 L 1088 578 Z" fill="url(#navyGrad)" filter="url(#softShadow)"/>

  <!-- Simple editable icon marks inside solid anchors -->
  <path d="M 681 336 L 703 358 L 744 314" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 1160 178 C 1174 154 1206 154 1220 178 C 1206 202 1174 202 1160 178 Z M 1190 166 A 12 12 0 1 1 1189 166" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  <path d="M 875 430 L 904 400 L 933 430 L 904 460 Z M 904 400 L 904 460" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>
  <path d="M 1138 578 L 1168 548 L 1198 578 L 1168 608 Z M 1149 578 L 1187 578" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Small caption tag near the grid -->
  <text x="1014" y="690" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#8E2836" text-anchor="end" filter="url(#titleGlow)">
    SIX CONNECTED PROOF POINTS
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to `<rect>` or `<path>` for diamond crops; use the clip only on `<image>` elements.
- ❌ Using `<use>` to repeat the diamond shape; duplicate the path geometry directly so PPT-Master keeps everything editable.
- ❌ Building the grid from rotated bitmap PNGs; use clipped SVG images plus native editable path outlines and solid diamonds.
- ❌ Overfilling the slide with diamonds; the technique needs a calm text field to make the image grid feel premium rather than chaotic.
- ❌ Using `marker-end` arrows for diagonal motion cues; the diamond geometry already supplies direction.

## Composition notes
- Keep the title block on the left 40–45% of the canvas with generous negative space and a short accent rule.
- Place the diamond cluster on the right 55–60%, allowing a few outline diamonds to bleed near the top/right edges for scale.
- Use a disciplined palette: off-white background, dark navy anchors, burgundy accents, neutral gray outline diamonds.
- Mix image diamonds, hollow outlines, and solid color anchors in roughly a 6:5:4 ratio so the grid feels layered but not repetitive.