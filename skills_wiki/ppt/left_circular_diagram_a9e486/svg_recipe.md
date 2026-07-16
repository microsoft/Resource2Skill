# SVG Recipe — Circular Process Diagram

## Visual mechanism
A bold donut cycle occupies the left side of the slide, with 8 colored arc segments orbiting a central concept. The right side carries the narrative headline and short explanation, creating a balanced “visual system + executive takeaway” layout.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× decorative `<path>` for a soft abstract background blob behind the circular diagram
- 8× donut-segment `<path>` elements for the circular process steps
- 8× small `<circle>` elements for numbered step badges
- 8× `<text>` elements for step labels arranged around the circle
- 1× central `<circle>` for the core idea
- 2× central `<text>` elements for the core title and subtitle
- 1× right-side `<rect>` panel for the content block
- 4× right-side `<text>` blocks for eyebrow, headline, body copy, and takeaway
- 3× small `<line>` elements for subtle decorative dividers
- 1× `<filter id="softShadow">` applied to cards, center circle, and donut segments
- 1× `<filter id="glow">` applied to the decorative background blob
- Multiple `<linearGradient>` and `<radialGradient>` definitions for premium color depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="55%" stop-color="#EEF4FF"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <radialGradient id="blobGrad" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#7DD3FC" stop-opacity="0.50"/>
      <stop offset="55%" stop-color="#A78BFA" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="coreGrad" x1="260" y1="230" x2="560" y2="500">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>

    <linearGradient id="seg1" x1="340" y1="140" x2="480" y2="235"><stop offset="0%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#2563EB"/></linearGradient>
    <linearGradient id="seg2" x1="500" y1="155" x2="615" y2="300"><stop offset="0%" stop-color="#22C55E"/><stop offset="100%" stop-color="#0F766E"/></linearGradient>
    <linearGradient id="seg3" x1="540" y1="290" x2="630" y2="430"><stop offset="0%" stop-color="#FACC15"/><stop offset="100%" stop-color="#F97316"/></linearGradient>
    <linearGradient id="seg4" x1="475" y1="420" x2="615" y2="560"><stop offset="0%" stop-color="#FB7185"/><stop offset="100%" stop-color="#E11D48"/></linearGradient>
    <linearGradient id="seg5" x1="340" y1="490" x2="480" y2="575"><stop offset="0%" stop-color="#C084FC"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient>
    <linearGradient id="seg6" x1="210" y1="420" x2="350" y2="560"><stop offset="0%" stop-color="#2DD4BF"/><stop offset="100%" stop-color="#0891B2"/></linearGradient>
    <linearGradient id="seg7" x1="190" y1="290" x2="285" y2="430"><stop offset="0%" stop-color="#F472B6"/><stop offset="100%" stop-color="#BE185D"/></linearGradient>
    <linearGradient id="seg8" x1="210" y1="155" x2="350" y2="300"><stop offset="0%" stop-color="#A3E635"/><stop offset="100%" stop-color="#65A30D"/></linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.10 0 0 0 0 0.15 0 0 0 0 0.25 0 0 0 0.20 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M116 174 C205 42 414 60 526 142 C653 235 646 445 535 552 C420 662 226 655 121 540 C20 430 31 299 116 174 Z"
        fill="url(#blobGrad)" filter="url(#glow)"/>

  <text x="72" y="70" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#2563EB" letter-spacing="2.5">
    CIRCULAR OPERATING MODEL
  </text>

  <path d="M340.5 146 A225 225 0 0 1 479.5 146 L451.7 231.6 A135 135 0 0 0 368.3 231.6 Z" fill="url(#seg1)" filter="url(#softShadow)"/>
  <path d="M512.2 159.5 A225 225 0 0 1 610.5 257.8 L530.3 298.7 A135 135 0 0 0 471.3 239.7 Z" fill="url(#seg2)" filter="url(#softShadow)"/>
  <path d="M624 290.5 A225 225 0 0 1 624 429.5 L538.4 401.7 A135 135 0 0 0 538.4 318.3 Z" fill="url(#seg3)" filter="url(#softShadow)"/>
  <path d="M610.5 462.2 A225 225 0 0 1 512.2 560.5 L471.3 480.3 A135 135 0 0 0 530.3 421.3 Z" fill="url(#seg4)" filter="url(#softShadow)"/>
  <path d="M479.5 574 A225 225 0 0 1 340.5 574 L368.3 488.4 A135 135 0 0 0 451.7 488.4 Z" fill="url(#seg5)" filter="url(#softShadow)"/>
  <path d="M307.8 560.5 A225 225 0 0 1 209.5 462.2 L289.7 421.3 A135 135 0 0 0 348.7 480.3 Z" fill="url(#seg6)" filter="url(#softShadow)"/>
  <path d="M196 429.5 A225 225 0 0 1 196 290.5 L281.6 318.3 A135 135 0 0 0 281.6 401.7 Z" fill="url(#seg7)" filter="url(#softShadow)"/>
  <path d="M209.5 257.8 A225 225 0 0 1 307.8 159.5 L348.7 239.7 A135 135 0 0 0 289.7 298.7 Z" fill="url(#seg8)" filter="url(#softShadow)"/>

  <circle cx="410" cy="360" r="118" fill="url(#coreGrad)" filter="url(#softShadow)"/>
  <circle cx="410" cy="360" r="94" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2"/>
  <text x="330" y="345" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#FFFFFF">
    CUSTOMER
  </text>
  <text x="322" y="380" width="176" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="500" fill="#CBD5E1">
    value flywheel
  </text>

  <circle cx="410" cy="116" r="20" fill="#FFFFFF" filter="url(#softShadow)"/><text x="398" y="123" width="24" text-anchor="middle" font-family="Segoe UI" font-size="17" font-weight="800" fill="#2563EB">1</text>
  <circle cx="594" cy="176" r="20" fill="#FFFFFF" filter="url(#softShadow)"/><text x="582" y="183" width="24" text-anchor="middle" font-family="Segoe UI" font-size="17" font-weight="800" fill="#047857">2</text>
  <circle cx="654" cy="360" r="20" fill="#FFFFFF" filter="url(#softShadow)"/><text x="642" y="367" width="24" text-anchor="middle" font-family="Segoe UI" font-size="17" font-weight="800" fill="#C2410C">3</text>
  <circle cx="594" cy="544" r="20" fill="#FFFFFF" filter="url(#softShadow)"/><text x="582" y="551" width="24" text-anchor="middle" font-family="Segoe UI" font-size="17" font-weight="800" fill="#BE123C">4</text>
  <circle cx="410" cy="604" r="20" fill="#FFFFFF" filter="url(#softShadow)"/><text x="398" y="611" width="24" text-anchor="middle" font-family="Segoe UI" font-size="17" font-weight="800" fill="#6D28D9">5</text>
  <circle cx="226" cy="544" r="20" fill="#FFFFFF" filter="url(#softShadow)"/><text x="214" y="551" width="24" text-anchor="middle" font-family="Segoe UI" font-size="17" font-weight="800" fill="#0E7490">6</text>
  <circle cx="166" cy="360" r="20" fill="#FFFFFF" filter="url(#softShadow)"/><text x="154" y="367" width="24" text-anchor="middle" font-family="Segoe UI" font-size="17" font-weight="800" fill="#BE185D">7</text>
  <circle cx="226" cy="176" r="20" fill="#FFFFFF" filter="url(#softShadow)"/><text x="214" y="183" width="24" text-anchor="middle" font-family="Segoe UI" font-size="17" font-weight="800" fill="#4D7C0F">8</text>

  <text x="336" y="91" width="148" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0F172A">Discover</text>
  <text x="604" y="142" width="156" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0F172A" transform="rotate(20 604 142)">Segment</text>
  <text x="674" y="330" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0F172A" transform="rotate(90 674 330)">Activate</text>
  <text x="602" y="592" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0F172A" transform="rotate(-20 602 592)">Measure</text>
  <text x="332" y="640" width="156" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0F172A">Optimize</text>
  <text x="88" y="592" width="168" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0F172A" transform="rotate(20 88 592)">Retain</text>
  <text x="54" y="330" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0F172A" transform="rotate(-90 54 330)">Expand</text>
  <text x="86" y="142" width="168" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0F172A" transform="rotate(-20 86 142)">Advocate</text>

  <rect x="742" y="102" width="430" height="516" rx="34" fill="#FFFFFF" fill-opacity="0.92" filter="url(#softShadow)"/>
  <line x1="792" y1="190" x2="1122" y2="190" stroke="#D8E2F3" stroke-width="2"/>
  <line x1="792" y1="504" x2="1122" y2="504" stroke="#D8E2F3" stroke-width="2"/>
  <line x1="792" y1="536" x2="842" y2="536" stroke="#2563EB" stroke-width="5" stroke-linecap="round"/>

  <text x="792" y="152" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#2563EB" letter-spacing="2">
    PROCESS DESIGN
  </text>
  <text x="792" y="244" width="345" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#0F172A">
    One loop, eight repeatable motions
  </text>
  <text x="792" y="350" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="400" fill="#475569">
    <tspan x="792" dy="0">Use the cycle to show how each capability</tspan>
    <tspan x="792" dy="30">feeds the next. The center names the</tspan>
    <tspan x="792" dy="30">strategic idea, while the orbit names the</tspan>
    <tspan x="792" dy="30">operational steps that keep it moving.</tspan>
  </text>
  <text x="792" y="576" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0F172A">
    Best for maturity models, flywheels, product loops, and service journeys.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<textPath>` to curve labels around the ring; it will not translate reliably. Use rotated `<text>` elements with explicit `width` instead.
- ❌ Applying `clip-path` to donut paths or text; clipping is only safe on `<image>` elements.
- ❌ Building the ring with `<use>` clones of one segment; duplicate the paths directly so every segment remains editable.
- ❌ Relying on `marker-end` for circular arrows; use visible arc segments or separate editable arrow shapes instead.
- ❌ Overloading the diagram with more than 8 steps; label legibility collapses quickly.

## Composition notes
- Keep the circular diagram on the left 55% of the slide and the explanatory content panel on the right 35–40%.
- The center circle should be visually heavier than the outer labels so the audience reads the core idea first.
- Use saturated segment colors but place them on a calm, pale background to maintain executive polish.
- Leave generous negative space around the outer labels; the diagram needs breathing room to feel premium rather than like a dense radial chart.