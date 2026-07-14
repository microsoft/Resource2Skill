# SVG Recipe — Immersive Interactive Navigation (Cutout Overlays & Web-Style Menus)

## Visual mechanism
A persistent web-style navigation bar anchors the deck like a product interface, while a semi-transparent dimming overlay leaves one agenda row visually “cut out” and active. The active state is reinforced with a glowing focus frame, a moving underline in the top menu, and high-contrast duplicated active text above the overlay.

## SVG primitives needed
- 1× `<rect>` for the full-slide brand-gradient background
- 3× `<path>` for abstract immersive background blobs and diagonal motion accents
- 4× `<rect>` for the cutout overlay panels surrounding the transparent active window
- 1× `<rect>` for the active cutout focus frame with glow
- 1× `<rect>` for the web-style top navigation bar
- 1× `<rect>` for the active navigation underline indicator
- 8× `<text>` for top navigation links and brand label
- 1× `<text>` for the section eyebrow
- 1× `<text>` for the agenda title
- 4× `<text>` for agenda item numbers
- 4× `<text>` for agenda item labels under the overlay
- 2× `<text>` for duplicated active row content above the overlay
- 4× transparent `<rect>` hit-area placeholders for clickable navigation zones
- 2× `<linearGradient>` for premium background and underline color
- 1× `<radialGradient>` for soft ambient light
- 2× `<filter>` definitions for glow and card shadow effects

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B6DFF"/>
      <stop offset="48%" stop-color="#073A9B"/>
      <stop offset="100%" stop-color="#041B44"/>
    </linearGradient>
    <linearGradient id="underlineGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#7CE7FF"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="78%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#48D7FF" stop-opacity="0.55"/>
      <stop offset="55%" stop-color="#1B75FF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#00133D" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="focusGlow" x="-25%" y="-60%" width="150%" height="220%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Immersive brand background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#ambientGlow)"/>

  <!-- Abstract product/web-app atmosphere -->
  <path d="M874 122 C1020 42 1206 86 1298 210 L1298 720 L1032 720 C948 628 905 530 925 426 C946 315 777 176 874 122 Z"
        fill="#5FD8FF" opacity="0.14"/>
  <path d="M-92 600 C86 528 214 580 332 654 C430 716 536 734 656 690 L656 760 L-92 760 Z"
        fill="#031537" opacity="0.42"/>
  <path d="M784 214 L1184 122" stroke="#9EEBFF" stroke-width="2" opacity="0.25" fill="none"/>
  <path d="M820 266 L1248 168" stroke="#FFFFFF" stroke-width="1.5" opacity="0.16" fill="none" stroke-dasharray="9 12"/>

  <!-- Content layer below cutout overlay -->
  <text x="170" y="154" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15" letter-spacing="3"
        fill="#BEEBFF" opacity="0.9">STRATEGIC OPERATING AGENDA</text>
  <text x="170" y="206" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700"
        fill="#FFFFFF">Choose the next chapter</text>

  <text x="188" y="282" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D8F6FF">01</text>
  <text x="246" y="282" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="600" fill="#FFFFFF">
    Accelerate our cultural transformation
  </text>

  <text x="188" y="358" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D8F6FF">02</text>
  <text x="246" y="358" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">
    Strategic enterprise accounts
  </text>

  <text x="188" y="434" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D8F6FF">03</text>
  <text x="246" y="434" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="600" fill="#FFFFFF">
    Customer acquisition
  </text>

  <text x="188" y="510" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D8F6FF">04</text>
  <text x="246" y="510" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="600" fill="#FFFFFF">
    Customer retention and growth
  </text>

  <!-- Cutout overlay: four panels leave a transparent active window at x=160 y=320 w=720 h=72 -->
  <rect x="0" y="86" width="1280" height="234" fill="#001A45" opacity="0.72"/>
  <rect x="0" y="392" width="1280" height="328" fill="#001A45" opacity="0.72"/>
  <rect x="0" y="320" width="160" height="72" fill="#001A45" opacity="0.72"/>
  <rect x="880" y="320" width="400" height="72" fill="#001A45" opacity="0.72"/>

  <!-- Active focus window and duplicated crisp active label -->
  <rect x="160" y="320" width="720" height="72" rx="18" fill="none" stroke="#FFFFFF" stroke-width="2.5"
        opacity="0.95" filter="url(#focusGlow)"/>
  <rect x="166" y="326" width="708" height="60" rx="14" fill="#FFFFFF" opacity="0.06"/>
  <text x="188" y="358" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">02</text>
  <text x="246" y="358" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#FFFFFF">
    Strategic enterprise accounts
  </text>

  <!-- Right-side contextual card -->
  <rect x="915" y="286" width="235" height="164" rx="24" fill="#FFFFFF" opacity="0.14" filter="url(#softShadow)"/>
  <text x="946" y="332" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="14" letter-spacing="2"
        fill="#BEEBFF">ACTIVE SECTION</text>
  <text x="946" y="376" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700"
        fill="#FFFFFF">02</text>
  <text x="946" y="416" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#E8FAFF">
    Tap or hyperlink this region to jump directly into the section.
  </text>

  <!-- Web navigation drawn above overlay -->
  <rect x="0" y="0" width="1280" height="86" fill="#04162F" opacity="0.72"/>
  <text x="58" y="53" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">
    NOVA<span fill="#7CE7FF">/</span>STRATEGY
  </text>

  <text x="662" y="52" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#D7E8FF">Home</text>
  <text x="762" y="52" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Agenda</text>
  <text x="880" y="52" width="94" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#D7E8FF">Services</text>
  <text x="1018" y="52" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#D7E8FF">About Us</text>
  <rect x="760" y="68" width="82" height="4" rx="2" fill="url(#underlineGrad)"/>

  <!-- Optional transparent click targets for PPT hyperlink assignment after import -->
  <rect x="632" y="20" width="92" height="52" fill="#FFFFFF" opacity="0"/>
  <rect x="742" y="20" width="118" height="52" fill="#FFFFFF" opacity="0"/>
  <rect x="858" y="20" width="132" height="52" fill="#FFFFFF" opacity="0"/>
  <rect x="998" y="20" width="142" height="52" fill="#FFFFFF" opacity="0"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to punch the cutout hole; build the dimming layer from four overlay rectangles around the active window.
- ❌ Do not apply `clip-path` to rectangles or text for the cutout effect; clipping should be reserved for `<image>` elements only.
- ❌ Do not rely on `<foreignObject>` for web-menu styling; use native `<text>`, `<rect>`, and gradients.
- ❌ Do not use `marker-end` on paths for menu indicators or arrows; use simple `<line>` or `<rect>` primitives instead.
- ❌ Do not place the navigation under the overlay; redraw the persistent web header above the dimming layer so it stays crisp.

## Composition notes
- Keep the top 10–12% of the slide reserved for persistent navigation; it should feel fixed like a website header.
- The agenda should occupy the left or center-left 55–65% of the canvas, leaving the right side for contextual cards, section metadata, or visual atmosphere.
- The cutout window should be slightly taller than the agenda row text, with enough padding to make the active state feel intentional rather than accidental.
- Use a dark translucent overlay with white or cyan accents; the rhythm should be “dimmed interface, bright active state, crisp navigation.”