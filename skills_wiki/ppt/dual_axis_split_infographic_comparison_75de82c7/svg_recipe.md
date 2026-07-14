# SVG Recipe — Dual-Axis Split Infographic Comparison

## Visual mechanism
A symmetrical A-vs-B comparison uses two tall floating cards as anchors, with saturated horizontal pill bars extending inward from large overlapping circular badges. Strong color polarity, central “V/S” typography, gradients, and soft shadows create a layered executive-infographic look.

## SVG primitives needed
- 1× `<rect>` for the dark navy slide background.
- 2× `<rect>` for the tall white floating side cards.
- 8× `<rect>` for the horizontal pill-shaped comparison bars.
- 4× `<circle>` per side for outer badge shadow/ring, colored badge face, inner rim, and highlight depth.
- 4× `<path>` for simple white avatar/person icons inside the badges.
- Multiple `<text>` elements with explicit `width=` for the central title, card headings, descriptions, bar numbers, bar labels, and badge labels.
- 2× `<linearGradient>` for cyan and magenta badge fills.
- 2× `<radialGradient>` for subtle badge highlight/glass volume.
- 2× `<filter>` using `feOffset + feGaussianBlur + feMerge` for soft object shadows and bold title shadow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="10" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="titleShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="5" dy="6" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="cyanBadge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#12d9ff"/>
      <stop offset="52%" stop-color="#00b5f5"/>
      <stop offset="100%" stop-color="#0087d8"/>
    </linearGradient>
    <linearGradient id="magentaBadge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff86ef"/>
      <stop offset="55%" stop-color="#f24dd7"/>
      <stop offset="100%" stop-color="#d425ad"/>
    </linearGradient>
    <radialGradient id="badgeShine" cx="35%" cy="20%" r="75%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.42"/>
      <stop offset="42%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.14"/>
    </radialGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#152a5a"/>

  <rect x="55" y="28" width="358" height="667" rx="12" fill="#f4f4f6" filter="url(#softShadow)"/>
  <rect x="867" y="28" width="358" height="667" rx="12" fill="#f4f4f6" filter="url(#softShadow)"/>

  <text x="640" y="126" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="104" font-weight="800" fill="#ffffff" filter="url(#titleShadow)">V/S</text>
  <text x="640" y="181" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" letter-spacing="1.5" fill="#ffffff">COMPARISON</text>

  <text x="234" y="107" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="800" fill="#11b9f4" filter="url(#titleShadow)">A</text>
  <text x="1046" y="107" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="800" fill="#f65adf" filter="url(#titleShadow)">B</text>

  <text x="101" y="166" width="265" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#111111">
    <tspan x="101" dy="0">Lorem ipsum dolor sit amet,</tspan>
    <tspan x="101" dy="26">consectetuer adipiscing elit.</tspan>
    <tspan x="101" dy="26">Maecenas porttitor congue</tspan>
    <tspan x="101" dy="26">massa. Fusce posuere, magna</tspan>
    <tspan x="101" dy="26">sed pulvinar ultricies, purus</tspan>
    <tspan x="101" dy="26">lectus malesuada libero, sit</tspan>
    <tspan x="101" dy="26">amet commodo magna eros</tspan>
    <tspan x="101" dy="26">quis urna.</tspan>
  </text>
  <text x="918" y="166" width="265" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#111111">
    <tspan x="918" dy="0">Lorem ipsum dolor sit amet,</tspan>
    <tspan x="918" dy="26">consectetuer adipiscing elit.</tspan>
    <tspan x="918" dy="26">Maecenas porttitor congue</tspan>
    <tspan x="918" dy="26">massa. Fusce posuere, magna</tspan>
    <tspan x="918" dy="26">sed pulvinar ultricies, purus</tspan>
    <tspan x="918" dy="26">lectus malesuada libero, sit</tspan>
    <tspan x="918" dy="26">amet commodo magna eros</tspan>
    <tspan x="918" dy="26">quis urna.</tspan>
  </text>

  <rect x="230" y="395" width="355" height="43" rx="7" fill="#40d7e9" filter="url(#softShadow)"/>
  <rect x="230" y="447" width="355" height="43" rx="7" fill="#15a7dd" filter="url(#softShadow)"/>
  <rect x="230" y="499" width="355" height="43" rx="7" fill="#0874bd" filter="url(#softShadow)"/>
  <rect x="230" y="551" width="355" height="43" rx="7" fill="#032e68" filter="url(#softShadow)"/>

  <rect x="700" y="395" width="355" height="43" rx="7" fill="#ee79df" filter="url(#softShadow)"/>
  <rect x="700" y="447" width="355" height="43" rx="7" fill="#e84697" filter="url(#softShadow)"/>
  <rect x="700" y="499" width="355" height="43" rx="7" fill="#d91a65" filter="url(#softShadow)"/>
  <rect x="700" y="551" width="355" height="43" rx="7" fill="#f00658" filter="url(#softShadow)"/>

  <text x="381" y="425" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">01</text>
  <text x="424" y="423" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff">Add your text here</text>
  <text x="381" y="477" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">02</text>
  <text x="424" y="475" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff">Add your text here</text>
  <text x="381" y="529" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">03</text>
  <text x="424" y="527" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff">Add your text here</text>
  <text x="381" y="581" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">04</text>
  <text x="424" y="579" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff">Add your text here</text>

  <text x="727" y="423" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff">Add your text here</text>
  <text x="876" y="425" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">01</text>
  <text x="727" y="475" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff">Add your text here</text>
  <text x="876" y="477" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">02</text>
  <text x="727" y="527" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff">Add your text here</text>
  <text x="876" y="529" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">03</text>
  <text x="727" y="579" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff">Add your text here</text>
  <text x="876" y="581" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">04</text>

  <circle cx="233" cy="505" r="130" fill="#dce7ed" filter="url(#softShadow)"/>
  <circle cx="233" cy="505" r="112" fill="url(#cyanBadge)"/>
  <circle cx="233" cy="505" r="112" fill="url(#badgeShine)"/>
  <circle cx="233" cy="505" r="111" fill="none" stroke="#0089cc" stroke-width="3"/>

  <circle cx="1046" cy="505" r="130" fill="#dce7ed" filter="url(#softShadow)"/>
  <circle cx="1046" cy="505" r="112" fill="url(#magentaBadge)"/>
  <circle cx="1046" cy="505" r="112" fill="url(#badgeShine)"/>
  <circle cx="1046" cy="505" r="111" fill="none" stroke="#d229b3" stroke-width="3"/>

  <circle cx="233" cy="443" r="18" fill="#ffffff"/>
  <path d="M200 503 C200 484 214 473 233 473 C252 473 266 484 266 503 L266 512 L243 512 L243 486 L233 493 L223 486 L223 512 L200 512 Z" fill="#ffffff"/>
  <path d="M213 432 C226 420 241 417 252 431 C241 429 230 431 220 441 C224 437 224 433 222 428 C218 429 215 431 213 432 Z" fill="#ffffff"/>

  <path d="M1018 469 C1028 461 1025 443 1032 432 C1038 423 1054 423 1060 432 C1067 443 1063 461 1074 469 C1063 469 1058 463 1057 452 C1053 459 1039 459 1035 452 C1034 463 1029 469 1018 469 Z" fill="#ffffff"/>
  <path d="M1015 504 C1015 486 1029 475 1046 475 C1063 475 1077 486 1077 504 L1077 512 L1056 512 L1056 487 L1046 496 L1036 487 L1036 512 L1015 512 Z" fill="#ffffff"/>

  <text x="233" y="546" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" fill="#ffffff">INFOGRAPHIC</text>
  <text x="233" y="576" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" fill="#ffffff">TITLE</text>
  <text x="1046" y="546" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" fill="#ffffff">INFOGRAPHIC</text>
  <text x="1046" y="576" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" fill="#ffffff">TITLE</text>
</svg>
```

## Avoid in this skill
- ❌ Using plain two-column bullet lists; the technique depends on badge-anchored bars and layered depth.
- ❌ Applying `filter` to `<line>` arrows or connector lines; keep shadows on cards, bars, circles, paths, and text only.
- ❌ Using `<use>` to duplicate icons or badge parts; repeat the editable paths/shapes directly.
- ❌ Clipping or masking non-image shapes to create the circles; use native `<circle>` layers instead.
- ❌ Making the center gap too crowded; the split comparison needs a clean central axis for “V/S”.

## Composition notes
- Keep the two vertical cards aligned symmetrically, each occupying roughly the outer third of the slide.
- Place the circular badges low enough to overlap both the card body and the horizontal bars, creating the layered infographic anchor.
- Reserve the middle 15–20% of the canvas for the “V/S” title and negative space between the two bar stacks.
- Use one cool palette and one warm palette with descending bar shades so each side reads as a coherent data family.