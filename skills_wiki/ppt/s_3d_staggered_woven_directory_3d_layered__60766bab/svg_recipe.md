# SVG Recipe — 3D Staggered Woven Directory (3D Layered Agenda)

## Visual mechanism
A premium agenda layout uses staggered rounded cards with faux-3D depth, soft reflections, and a golden sine-wave thread that alternates between back and front layers. The weaving is achieved by drawing the curve in separate z-order passes: a back curve, cards that occlude it, then selected front curve segments crossing lower cards.

## SVG primitives needed
- 1× full-slide `<rect>` for the vertical white-to-sky-blue background gradient
- 4× card groups containing rounded `<rect>` faces for agenda modules
- 4× darker `<path>` base lips under cards to suggest 3D thickness
- 4× translucent blurred `<rect>` reflections below cards
- 4× small highlight `<rect>` overlays on card faces for glossy perspective
- 3× `<path>` wave strokes for the woven gold connector: one back layer and two front overlay segments
- 1× `<linearGradient id="bgGrad">` for the airy background
- 1× `<linearGradient id="cardGrad">` for dimensional blue cards
- 1× `<linearGradient id="goldFade">` for a left-to-right gold-to-transparent connector
- 1× `<filter id="softShadow">` applied to card groups
- 1× `<filter id="reflectionBlur">` applied to reflections
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, numbers, titles, and captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#F3F9FF"/>
      <stop offset="100%" stop-color="#C4E0F9"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="190" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2C8BFF"/>
      <stop offset="58%" stop-color="#1873E8"/>
      <stop offset="100%" stop-color="#0F56BC"/>
    </linearGradient>

    <linearGradient id="goldFade" x1="120" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFD700" stop-opacity="1"/>
      <stop offset="45%" stop-color="#FFC928" stop-opacity=".95"/>
      <stop offset="78%" stop-color="#FFD700" stop-opacity=".45"/>
      <stop offset="100%" stop-color="#FFD700" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="reflectionBlur" x="-30%" y="-20%" width="160%" height="180%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="92" y="82" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700" fill="#123C69" letter-spacing="4">CONTENTS</text>
  <text x="96" y="118" width="670" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#5F7892">Corporate Business Presentation / Major Achievements</text>

  <!-- Back woven thread: will be hidden by the high cards -->
  <path d="M105 425 C210 340 315 340 420 425 S630 510 735 425 S945 340 1050 425 S1160 500 1220 455"
        fill="none" stroke="url(#goldFade)" stroke-width="16" stroke-linecap="round" opacity=".65"/>
  <path d="M105 425 C210 340 315 340 420 425 S630 510 735 425 S945 340 1050 425 S1160 500 1220 455"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity=".42"/>

  <!-- High card 02 -->
  <g transform="translate(402 245) rotate(-2 105 95)" filter="url(#softShadow)">
    <rect x="18" y="202" width="194" height="74" rx="20" fill="#1873E8" opacity=".18" filter="url(#reflectionBlur)"/>
    <path d="M8 164 Q8 186 30 190 L198 190 Q220 186 220 164 L204 188 L24 188 Z" fill="#0A4EA9" opacity=".55"/>
    <rect x="0" y="0" width="228" height="184" rx="26" fill="url(#cardGrad)"/>
    <rect x="18" y="14" width="192" height="34" rx="17" fill="#FFFFFF" opacity=".14"/>
    <text x="30" y="67" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#FFFFFF">02</text>
    <text x="30" y="108" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Strategy</text>
    <text x="30" y="139" width="168" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DDEEFF">Market position and growth path</text>
  </g>

  <!-- High card 04 -->
  <g transform="translate(910 248) rotate(2 105 95)" filter="url(#softShadow)">
    <rect x="18" y="202" width="194" height="74" rx="20" fill="#1873E8" opacity=".16" filter="url(#reflectionBlur)"/>
    <path d="M8 164 Q8 186 30 190 L198 190 Q220 186 220 164 L204 188 L24 188 Z" fill="#0A4EA9" opacity=".55"/>
    <rect x="0" y="0" width="228" height="184" rx="26" fill="url(#cardGrad)"/>
    <rect x="18" y="14" width="192" height="34" rx="17" fill="#FFFFFF" opacity=".14"/>
    <text x="30" y="67" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#FFFFFF">04</text>
    <text x="30" y="108" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Execution</text>
    <text x="30" y="139" width="168" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DDEEFF">Roadmap, ownership, milestones</text>
  </g>

  <!-- Low card 01 -->
  <g transform="translate(150 385) rotate(-2 105 95)" filter="url(#softShadow)">
    <rect x="18" y="202" width="194" height="76" rx="20" fill="#1873E8" opacity=".22" filter="url(#reflectionBlur)"/>
    <path d="M8 164 Q8 186 30 190 L198 190 Q220 186 220 164 L204 188 L24 188 Z" fill="#0A4EA9" opacity=".62"/>
    <rect x="0" y="0" width="228" height="184" rx="26" fill="url(#cardGrad)"/>
    <rect x="18" y="14" width="192" height="34" rx="17" fill="#FFFFFF" opacity=".14"/>
    <text x="30" y="67" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#FFFFFF">01</text>
    <text x="30" y="108" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Overview</text>
    <text x="30" y="139" width="168" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DDEEFF">Current context and key signals</text>
  </g>

  <!-- Low card 03 -->
  <g transform="translate(657 384) rotate(2 105 95)" filter="url(#softShadow)">
    <rect x="18" y="202" width="194" height="76" rx="20" fill="#1873E8" opacity=".22" filter="url(#reflectionBlur)"/>
    <path d="M8 164 Q8 186 30 190 L198 190 Q220 186 220 164 L204 188 L24 188 Z" fill="#0A4EA9" opacity=".62"/>
    <rect x="0" y="0" width="228" height="184" rx="26" fill="url(#cardGrad)"/>
    <rect x="18" y="14" width="192" height="34" rx="17" fill="#FFFFFF" opacity=".14"/>
    <text x="30" y="67" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#FFFFFF">03</text>
    <text x="30" y="108" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Innovation</text>
    <text x="30" y="139" width="168" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DDEEFF">Product bets and capability shifts</text>
  </g>

  <!-- Front woven segments crossing the low cards -->
  <path d="M120 420 C178 374 255 374 330 414 C365 433 392 439 420 425"
        fill="none" stroke="url(#goldFade)" stroke-width="16" stroke-linecap="round" opacity=".92"/>
  <path d="M615 500 C655 524 703 523 742 496 C790 464 828 397 900 365"
        fill="none" stroke="url(#goldFade)" stroke-width="16" stroke-linecap="round" opacity=".82"/>
  <circle cx="116" cy="423" r="7" fill="#FFD700"/>
  <circle cx="900" cy="365" r="5" fill="#FFD700" opacity=".45"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` to fake perspective; those transforms are silently dropped.
- ❌ Do not rely on SVG masks to hide the woven line behind cards; split the line into separate back/front path segments and control the draw order.
- ❌ Do not apply filters to `<line>` elements; use stroked `<path>` curves for the connector if glow or softness is needed.
- ❌ Do not omit `width` on text elements; agenda labels will not size predictably in PowerPoint.
- ❌ Do not make all cards sit on the same baseline; the staggered rhythm is essential to the 3D directory effect.

## Composition notes
- Keep the title small relative to the card system; the visual focus should be the woven agenda structure across the lower two-thirds of the slide.
- Alternate cards high-low-high-low or low-high-low-high, with roughly 220–260 px horizontal spacing between card centers.
- Use a cool, airy background so the blue cards feel like physical objects standing in space; reserve gold only for the weaving thread and small endpoint accents.
- Build depth by layering: background curve first, elevated cards next, lower cards next, then short front curve segments where the thread should appear to pass over objects.