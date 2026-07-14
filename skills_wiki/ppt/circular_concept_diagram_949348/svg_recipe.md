# SVG Recipe — Circular Concept Diagram

## Visual mechanism
A bold central idea is surrounded by a segmented orbital ring: each curved segment implies clockwise progression, while numbered satellite labels explain the supporting concepts. The composition works because the center remains visually dominant and the outer labels are evenly distributed around a circular path.

## SVG primitives needed
- 1× `<rect>` for the subtle executive-style gradient background
- 2× `<circle>` for the central concept medallion and inner glow
- 2× `<circle>` for dashed orbital guide rings
- 6× `<path>` with thick strokes for curved donut-ring segments
- 6× `<path>` triangle arrowheads for segment direction, avoiding unsupported path markers
- 6× `<circle>` for numbered step badges on the orbit
- 6× `<path>` mini icon glyphs inside badges / near labels
- 7× `<text>` groups for the central label and six surrounding concept labels
- 6× `<linearGradient>` for premium segment color variation
- 1× `<radialGradient>` for the center medallion
- 2× `<filter>` definitions for soft shadow and glow on editable shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="55%" stop-color="#EDF3FF"/>
      <stop offset="100%" stop-color="#E7EEF8"/>
    </linearGradient>
    <radialGradient id="centerGrad" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#ECF4FF"/>
      <stop offset="100%" stop-color="#CFE0FF"/>
    </radialGradient>
    <linearGradient id="seg1" x1="650" y1="110" x2="870" y2="260"><stop offset="0%" stop-color="#35C6FF"/><stop offset="100%" stop-color="#2364FF"/></linearGradient>
    <linearGradient id="seg2" x1="850" y1="280" x2="850" y2="470"><stop offset="0%" stop-color="#7D5CFF"/><stop offset="100%" stop-color="#C24BFF"/></linearGradient>
    <linearGradient id="seg3" x1="830" y1="500" x2="630" y2="600"><stop offset="0%" stop-color="#FF7A59"/><stop offset="100%" stop-color="#FFB13B"/></linearGradient>
    <linearGradient id="seg4" x1="600" y1="600" x2="430" y2="500"><stop offset="0%" stop-color="#20C997"/><stop offset="100%" stop-color="#00A6A6"/></linearGradient>
    <linearGradient id="seg5" x1="420" y1="450" x2="430" y2="250"><stop offset="0%" stop-color="#00B7FF"/><stop offset="100%" stop-color="#3DDC97"/></linearGradient>
    <linearGradient id="seg6" x1="470" y1="220" x2="630" y2="120"><stop offset="0%" stop-color="#FF5FA2"/><stop offset="100%" stop-color="#7D5CFF"/></linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <circle cx="640" cy="360" r="286" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="8 14" opacity="0.85"/>
  <circle cx="640" cy="360" r="182" fill="none" stroke="#BFD0EA" stroke-width="1.5" stroke-dasharray="5 10" opacity="0.7"/>

  <path d="M678 143 A220 220 0 0 1 822 237" fill="none" stroke="url(#seg1)" stroke-width="52" stroke-linecap="round" filter="url(#softShadow)"/>
  <path d="M847 285 A220 220 0 0 1 838 456" fill="none" stroke="url(#seg2)" stroke-width="52" stroke-linecap="round" filter="url(#softShadow)"/>
  <path d="M809 501 A220 220 0 0 1 655 579" fill="none" stroke="url(#seg3)" stroke-width="52" stroke-linecap="round" filter="url(#softShadow)"/>
  <path d="M602 577 A220 220 0 0 1 458 483" fill="none" stroke="url(#seg4)" stroke-width="52" stroke-linecap="round" filter="url(#softShadow)"/>
  <path d="M433 435 A220 220 0 0 1 442 264" fill="none" stroke="url(#seg5)" stroke-width="52" stroke-linecap="round" filter="url(#softShadow)"/>
  <path d="M472 219 A220 220 0 0 1 625 140" fill="none" stroke="url(#seg6)" stroke-width="52" stroke-linecap="round" filter="url(#softShadow)"/>

  <path d="M0 -15 L34 0 L0 15 Z" fill="#2364FF" transform="translate(822 237) rotate(56)"/>
  <path d="M0 -15 L34 0 L0 15 Z" fill="#C24BFF" transform="translate(838 456) rotate(116)"/>
  <path d="M0 -15 L34 0 L0 15 Z" fill="#FFB13B" transform="translate(655 579) rotate(176)"/>
  <path d="M0 -15 L34 0 L0 15 Z" fill="#00A6A6" transform="translate(458 483) rotate(236)"/>
  <path d="M0 -15 L34 0 L0 15 Z" fill="#3DDC97" transform="translate(442 264) rotate(296)"/>
  <path d="M0 -15 L34 0 L0 15 Z" fill="#7D5CFF" transform="translate(625 140) rotate(356)"/>

  <circle cx="640" cy="360" r="124" fill="#FFFFFF" opacity="0.72" filter="url(#glow)"/>
  <circle cx="640" cy="360" r="108" fill="url(#centerGrad)" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <path d="M640 302 C672 326 693 348 712 360 C690 374 671 395 640 418 C609 394 590 374 568 360 C589 347 608 326 640 302 Z" fill="#2364FF" opacity="0.12"/>
  <text x="540" y="338" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#1B2A41" text-anchor="middle">
    <tspan x="640" dy="0">CORE</tspan>
    <tspan x="640" dy="30">CONCEPT</tspan>
  </text>
  <text x="548" y="393" width="184" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="500" fill="#52657F" text-anchor="middle">
    <tspan x="640" dy="0">shared strategic theme</tspan>
  </text>

  <circle cx="760" cy="166" r="28" fill="#FFFFFF" stroke="#2364FF" stroke-width="4" filter="url(#softShadow)"/>
  <text x="745" y="176" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#2364FF" text-anchor="middle">1</text>
  <text x="820" y="92" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1B2A41">
    <tspan x="820" dy="0">Market Pulse</tspan><tspan x="820" dy="25" font-size="14" font-weight="500" fill="#607089">Sense external shifts early</tspan>
  </text>

  <circle cx="879" cy="369" r="28" fill="#FFFFFF" stroke="#A64BFF" stroke-width="4" filter="url(#softShadow)"/>
  <text x="864" y="379" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#A64BFF" text-anchor="middle">2</text>
  <text x="942" y="338" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1B2A41">
    <tspan x="942" dy="0">Customer Fit</tspan><tspan x="942" dy="25" font-size="14" font-weight="500" fill="#607089">Map needs to value levers</tspan>
  </text>

  <circle cx="736" cy="574" r="28" fill="#FFFFFF" stroke="#FF8C3B" stroke-width="4" filter="url(#softShadow)"/>
  <text x="721" y="584" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FF8C3B" text-anchor="middle">3</text>
  <text x="765" y="627" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1B2A41" text-anchor="middle">
    <tspan x="875" dy="0">Operating Model</tspan><tspan x="875" dy="25" font-size="14" font-weight="500" fill="#607089">Convert intent into routines</tspan>
  </text>

  <circle cx="544" cy="574" r="28" fill="#FFFFFF" stroke="#00A6A6" stroke-width="4" filter="url(#softShadow)"/>
  <text x="529" y="584" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#00A6A6" text-anchor="middle">4</text>
  <text x="295" y="627" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1B2A41" text-anchor="middle">
    <tspan x="405" dy="0">Capability Build</tspan><tspan x="405" dy="25" font-size="14" font-weight="500" fill="#607089">Invest in repeatable strengths</tspan>
  </text>

  <circle cx="401" cy="369" r="28" fill="#FFFFFF" stroke="#1CBFB4" stroke-width="4" filter="url(#softShadow)"/>
  <text x="386" y="379" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#1CBFB4" text-anchor="middle">5</text>
  <text x="130" y="338" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1B2A41">
    <tspan x="130" dy="0">Proof Points</tspan><tspan x="130" dy="25" font-size="14" font-weight="500" fill="#607089">Demonstrate measurable wins</tspan>
  </text>

  <circle cx="520" cy="166" r="28" fill="#FFFFFF" stroke="#C05BFF" stroke-width="4" filter="url(#softShadow)"/>
  <text x="505" y="176" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#C05BFF" text-anchor="middle">6</text>
  <text x="255" y="92" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1B2A41">
    <tspan x="255" dy="0">Scale System</tspan><tspan x="255" dy="25" font-size="14" font-weight="500" fill="#607089">Reinforce and expand adoption</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ `marker-end` on curved `<path>` segments; use separate editable triangular `<path>` arrowheads instead.
- ❌ Rotating outer text around the circle; it often reduces readability and can create upside-down labels.
- ❌ Applying `clip-path` to ring segments or other non-image shapes; it will be ignored by the translator.
- ❌ Using `<use>` to duplicate repeated badges or arrowheads; duplicate the native shapes directly.
- ❌ Overcrowding the ring with more than 6–8 concepts unless labels become very short.

## Composition notes
- Keep the central medallion at roughly 25–32% of slide height so it anchors the diagram without crowding the orbital labels.
- Use the strongest color saturation on the ring segments, then repeat each color in its numbered badge for visual continuity.
- Leave generous negative space between the outer labels and the ring; the diagram should read as an executive keynote visual, not a radial table.
- For 4–5 concepts, increase arc span and label size; for 7–8 concepts, reduce badge size and use shorter two-line captions.