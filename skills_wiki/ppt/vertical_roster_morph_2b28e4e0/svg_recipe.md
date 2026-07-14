# SVG Recipe — Vertical Roster Morph

## Visual mechanism
A tall, right-side portrait filmstrip and a left-side roster list move vertically in synced increments across consecutive slides. The active person stays visually anchored by a teal highlight pill on the roster and a centered portrait, while the main name/bio content changes per slide.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<linearGradient>` for a subtle executive-style right rail wash
- 1× `<filter id="softShadow">` applied to portrait cards and highlight pill
- 1× `<filter id="tealGlow">` applied to the active highlight pill
- 5× `<clipPath>` with rounded `<rect>` for editable rounded-corner portrait crops
- 5× `<rect>` for portrait card frames behind clipped images
- 5× `<image>` for the vertical portrait filmstrip, including off-slide top/bottom images
- 1× `<rect>` for the active roster highlight bar
- 5× `<text>` for roster labels, with active label in white
- 3× `<text>` for active person name, role, and bio
- 2× `<path>` for decorative curved motion accents near the image rail
- 1× `<line>` for a subtle vertical roster guide
- 4× `<circle>` for guide dots / slide-state indicators
- Optional repeated slide states: same primitives with changed `y` positions to let PowerPoint Morph animate the vertical movement

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="railWash" x1="820" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F4FBFB"/>
      <stop offset="0.55" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#E8F5F5"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="tealGlow" x="-30%" y="-60%" width="160%" height="220%">
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoClipA"><rect x="905" y="-214" width="290" height="214" rx="24"/></clipPath>
    <clipPath id="photoClipB"><rect x="905" y="32" width="290" height="214" rx="24"/></clipPath>
    <clipPath id="photoClipC"><rect x="905" y="278" width="290" height="214" rx="24"/></clipPath>
    <clipPath id="photoClipD"><rect x="905" y="524" width="290" height="214" rx="24"/></clipPath>
    <clipPath id="photoClipE"><rect x="905" y="770" width="290" height="214" rx="24"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="820" y="0" width="460" height="720" fill="url(#railWash)"/>

  <path d="M842 70 C900 144 872 232 924 310 C976 388 957 480 1035 578"
        fill="none" stroke="#D7EEEE" stroke-width="3" stroke-dasharray="10 14"/>
  <path d="M1225 118 C1160 202 1192 300 1130 382 C1066 466 1080 556 1012 642"
        fill="none" stroke="#BFE2E2" stroke-width="2" stroke-dasharray="6 12"/>

  <line x1="96" y1="154" x2="96" y2="442" stroke="#DDE4E4" stroke-width="2"/>
  <circle cx="96" cy="188" r="5" fill="#C8D2D2"/>
  <circle cx="96" cy="246" r="5" fill="#C8D2D2"/>
  <circle cx="96" cy="304" r="6" fill="#0C7E84"/>
  <circle cx="96" cy="362" r="5" fill="#C8D2D2"/>

  <rect x="118" y="282" width="268" height="52" rx="26" fill="#0C7E84" filter="url(#tealGlow)"/>
  <text x="134" y="193" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#7A7A7A">Experience Design</text>
  <text x="134" y="251" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#7A7A7A">Data Architecture</text>
  <text x="134" y="316" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Product Strategy</text>
  <text x="134" y="367" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#7A7A7A">Market Expansion</text>
  <text x="134" y="425" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#7A7A7A">Operations Lead</text>

  <text x="440" y="232" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="4" fill="#0C7E84">FEATURED EXPERT</text>
  <text x="438" y="302" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#111111">MAYA</text>
  <text x="438" y="365" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#111111">IYER</text>
  <text x="442" y="408" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#333333">VP, Product Strategy</text>
  <text x="442" y="458" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#666666">
    <tspan x="442" dy="0">Leads the portfolio narrative across emerging</tspan>
    <tspan x="442" dy="28">platforms, aligning customer insight, product</tspan>
    <tspan x="442" dy="28">signals, and executive decision rhythms.</tspan>
  </text>

  <rect x="905" y="-214" width="290" height="214" rx="24" fill="#FFFFFF" opacity="0.35"/>
  <image href="https://images.example.com/executive-portrait-adrianna-vance.jpg" x="905" y="-214" width="290" height="214" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClipA)"/>

  <rect x="905" y="32" width="290" height="214" rx="24" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.72"/>
  <image href="https://images.example.com/executive-portrait-marcus-reid.jpg" x="905" y="32" width="290" height="214" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClipB)"/>

  <rect x="890" y="263" width="320" height="244" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="905" y="278" width="290" height="214" rx="24" fill="#D9EEEE"/>
  <image href="https://images.example.com/executive-portrait-maya-iyer-product-strategist.jpg" x="905" y="278" width="290" height="214" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClipC)"/>

  <rect x="905" y="524" width="290" height="214" rx="24" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.72"/>
  <image href="https://images.example.com/executive-portrait-sofia-chen.jpg" x="905" y="524" width="290" height="214" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClipD)"/>

  <rect x="905" y="770" width="290" height="214" rx="24" fill="#FFFFFF" opacity="0.35"/>
  <image href="https://images.example.com/executive-portrait-noah-okafor.jpg" x="905" y="770" width="290" height="214" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClipE)"/>

  <text x="442" y="630" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="2" fill="#A0A0A0">03 / 05</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the scroll; build separate slide states and let PowerPoint Morph interpolate object positions.
- ❌ Do not combine the entire portrait strip into one raster screenshot if editability matters; keep each portrait as a separate clipped `<image>` with its own card frame.
- ❌ Do not use `<mask>` fades at the top/bottom of the filmstrip; use off-canvas placement, opacity changes, or pale overlay rectangles instead.
- ❌ Do not apply `clip-path` to groups or rectangles for cropping; only apply clip paths directly to `<image>` elements.
- ❌ Do not use `<use>` to duplicate portrait cards or roster rows; duplicate the actual SVG elements so PPT-Master can translate them reliably.

## Composition notes
- Keep the active portrait vertically centered in the right 30% of the slide; neighboring portraits should extend above and below the canvas to imply continuous scrolling.
- Put the roster in the left 25% with a fixed highlight pill position per slide state, or move the pill down one row between Morph slides for a stronger “selection travels” effect.
- Reserve the central 40–45% for the featured name and bio; leave generous white space so the movement does not compete with reading.
- For a multi-slide Morph sequence, preserve the same object order and visual styling on every slide, changing only the `y` positions of the portrait cards, highlight pill, active roster color, and central text content.