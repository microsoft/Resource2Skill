# SVG Recipe — 8-Segment Wheel with CTA

## Visual mechanism
A bold donut wheel is divided into eight separated arc segments, each carrying a short step label, with a confident center badge and a bottom pill-shaped call-to-action. The composition reads as a circular process that resolves into a single action button.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× decorative `<path>` blobs for premium depth and energy
- 8× donut-wedge `<path>` shapes for the wheel segments
- 1× `<circle>` for the center badge
- 1× `<circle>` for the subtle inner ring highlight
- 10× `<text>` blocks for headline, center badge, segment labels, and CTA copy
- 1× CTA `<rect>` with rounded corners
- 1× `<line>` plus 1× small `<path>` triangle for the CTA arrow
- 9× `<linearGradient>` fills for background, segments, and CTA button
- 1× `<radialGradient>` for the center badge
- 2× `<filter>` definitions for soft shadow and glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#0B1020"/>
      <stop offset="55%" stop-color="#151B3A"/>
      <stop offset="100%" stop-color="#09111F"/>
    </linearGradient>

    <linearGradient id="seg1" x1="600" y1="110" x2="820" y2="260"><stop offset="0%" stop-color="#FF6B6B"/><stop offset="100%" stop-color="#FF9F43"/></linearGradient>
    <linearGradient id="seg2" x1="760" y1="160" x2="870" y2="360"><stop offset="0%" stop-color="#FFB347"/><stop offset="100%" stop-color="#FFD166"/></linearGradient>
    <linearGradient id="seg3" x1="770" y1="330" x2="830" y2="520"><stop offset="0%" stop-color="#2ED3B7"/><stop offset="100%" stop-color="#5EEAD4"/></linearGradient>
    <linearGradient id="seg4" x1="650" y1="440" x2="800" y2="560"><stop offset="0%" stop-color="#22C55E"/><stop offset="100%" stop-color="#A3E635"/></linearGradient>
    <linearGradient id="seg5" x1="470" y1="430" x2="630" y2="560"><stop offset="0%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#60A5FA"/></linearGradient>
    <linearGradient id="seg6" x1="410" y1="300" x2="570" y2="440"><stop offset="0%" stop-color="#818CF8"/><stop offset="100%" stop-color="#A78BFA"/></linearGradient>
    <linearGradient id="seg7" x1="420" y1="130" x2="580" y2="300"><stop offset="0%" stop-color="#C084FC"/><stop offset="100%" stop-color="#F472B6"/></linearGradient>
    <linearGradient id="seg8" x1="520" y1="90" x2="700" y2="250"><stop offset="0%" stop-color="#FB7185"/><stop offset="100%" stop-color="#F97316"/></linearGradient>

    <linearGradient id="ctaGrad" x1="440" y1="625" x2="840" y2="683">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#C7D2FE"/>
    </linearGradient>

    <radialGradient id="centerGrad" cx="50%" cy="38%" r="68%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="48%" stop-color="#EEF2FF"/>
      <stop offset="100%" stop-color="#C7D2FE"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <path d="M92 115 C175 24 315 46 358 136 C403 231 319 329 206 306 C97 284 27 190 92 115 Z" fill="#263BFF" opacity="0.16" filter="url(#softGlow)"/>
  <path d="M1015 83 C1124 27 1227 85 1240 190 C1254 299 1128 356 1042 292 C952 225 912 136 1015 83 Z" fill="#FF7A59" opacity="0.14" filter="url(#softGlow)"/>

  <text x="640" y="58" width="720" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="700" fill="#FFFFFF">
    8 Moves to Turn Strategy Into Momentum
  </text>
  <text x="640" y="94" width="660" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#AAB4D8">
    A circular operating model for teams that need clarity, speed, and follow-through.
  </text>

  <path d="M650.7 120.3 A205 205 0 0 1 777.2 172.7 L698.9 259.6 A88 88 0 0 0 644.6 237.1 Z" fill="url(#seg1)" filter="url(#shadow)"/>
  <path d="M792.4 187.8 A205 205 0 0 1 844.7 314.3 L727.9 320.4 A88 88 0 0 0 705.4 266.1 Z" fill="url(#seg2)" filter="url(#shadow)"/>
  <path d="M844.7 335.7 A205 205 0 0 1 792.4 462.2 L705.4 383.9 A88 88 0 0 0 727.9 329.6 Z" fill="url(#seg3)" filter="url(#shadow)"/>
  <path d="M777.2 477.3 A205 205 0 0 1 650.7 529.7 L644.6 412.9 A88 88 0 0 0 698.9 390.4 Z" fill="url(#seg4)" filter="url(#shadow)"/>
  <path d="M629.3 529.7 A205 205 0 0 1 502.8 477.3 L581.1 390.4 A88 88 0 0 0 635.4 412.9 Z" fill="url(#seg5)" filter="url(#shadow)"/>
  <path d="M487.6 462.2 A205 205 0 0 1 435.3 335.7 L552.1 329.6 A88 88 0 0 0 574.6 383.9 Z" fill="url(#seg6)" filter="url(#shadow)"/>
  <path d="M435.3 314.3 A205 205 0 0 1 487.6 187.8 L574.6 266.1 A88 88 0 0 0 552.1 320.4 Z" fill="url(#seg7)" filter="url(#shadow)"/>
  <path d="M502.8 172.7 A205 205 0 0 1 629.3 120.3 L635.4 237.1 A88 88 0 0 0 581.1 259.6 Z" fill="url(#seg8)" filter="url(#shadow)"/>

  <circle cx="640" cy="325" r="92" fill="url(#centerGrad)" filter="url(#shadow)"/>
  <circle cx="640" cy="325" r="78" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>

  <text x="640" y="306" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#27304F">
    ACTION
    <tspan x="640" dy="23" font-size="28" font-weight="800">WHEEL</tspan>
    <tspan x="640" dy="22" font-size="12" font-weight="600" fill="#66709A">8 connected moves</tspan>
  </text>

  <text x="696" y="181" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">01<tspan x="696" dy="18" font-size="16">Discover</tspan></text>
  <text x="775" y="260" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">02<tspan x="775" dy="18" font-size="16">Segment</tspan></text>
  <text x="775" y="372" width="126" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">03<tspan x="775" dy="18" font-size="16">Prioritize</tspan></text>
  <text x="696" y="452" width="126" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">04<tspan x="696" dy="18" font-size="16">Prototype</tspan></text>
  <text x="584" y="452" width="126" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">05<tspan x="584" dy="18" font-size="16">Validate</tspan></text>
  <text x="505" y="372" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">06<tspan x="505" dy="18" font-size="16">Launch</tspan></text>
  <text x="505" y="260" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">07<tspan x="505" dy="18" font-size="16">Measure</tspan></text>
  <text x="584" y="181" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">08<tspan x="584" dy="18" font-size="16">Scale</tspan></text>

  <rect x="440" y="625" width="400" height="58" rx="29" fill="url(#ctaGrad)" filter="url(#shadow)"/>
  <text x="620" y="662" width="310" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="800" fill="#111827">
    Book the strategy sprint
  </text>
  <line x1="772" y1="654" x2="805" y2="654" stroke="#111827" stroke-width="3" stroke-linecap="round"/>
  <path d="M805 654 L794 646 L794 662 Z" fill="#111827"/>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to carve the donut hole or segment gaps; use real donut-wedge paths instead.
- ❌ Using `<use>` or `<symbol>` for repeated wheel slices; duplicate explicit paths so every segment remains editable.
- ❌ Putting `marker-end` on curved `<path>` arrows around the wheel; if arrows are needed, build them from editable lines and small triangle paths.
- ❌ Long paragraph labels inside the segments; the wheel works best with one number and one short verb or noun phrase per segment.
- ❌ Text without `width`; every `<text>` block needs an explicit width for predictable PowerPoint rendering.

## Composition notes
- Keep the wheel centered slightly above the slide midpoint, leaving a clean lower band for the CTA button.
- Use saturated gradients on the eight segments, but keep the background dark and quiet so the wheel remains the visual focus.
- Segment labels should be short, high-contrast, and centered within each arc; avoid rotating the labels unless the deck style demands it.
- The CTA should feel like the visual conclusion of the loop: align it directly below the wheel and make it wide enough to read as the next action.