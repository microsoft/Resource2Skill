# SVG Recipe — Pictograph Matrix (100-Icon Array) Percentage Visualizer

## Visual mechanism
A 10×10 icon matrix turns a percentage into 100 discrete visual units: highlighted icons represent the measured share, while inactive icons recede in white or pale tint. The grid is paired with oversized numeric typography so the audience reads both the exact value and the visceral scale instantly.

## SVG primitives needed
- 1× `<rect>` for the full-slide executive blue background
- 1× `<rect>` for the rotated mint data card holding the pictograph and copy
- 1× `<rect>` for a small dark accent tab behind the data callout
- 1× `<ellipse>` for a soft background glow behind the card
- 10× `<text>` rows for the 100 pictograph glyphs, using nested `<tspan>` to split active vs inactive icons
- 4× `<text>` blocks for the large percentage, context label, emphasized keyword, and source note
- 1× `<path>` for a subtle decorative swoosh that adds motion and premium polish
- 1× `<linearGradient>` for the blue backdrop
- 1× `<radialGradient>` for the glow
- 1× `<filter id="softShadow">` applied to the card and large type
- 1× `<filter id="tinyLift">` applied to the icon rows for slight depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3158A8"/>
      <stop offset="48%" stop-color="#0D7FA1"/>
      <stop offset="100%" stop-color="#203A86"/>
    </linearGradient>
    <radialGradient id="aquaGlow" cx="45%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#66F4DE" stop-opacity="0.9"/>
      <stop offset="70%" stop-color="#66F4DE" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#66F4DE" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="tinyLift" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="2" result="off"/>
      <feGaussianBlur in="off" stdDeviation="1.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBlue)"/>
  <ellipse cx="545" cy="375" rx="520" ry="260" fill="url(#aquaGlow)"/>
  <path d="M88 565 C275 500 420 555 595 510 C820 452 1000 482 1195 420" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="34"/>

  <g transform="rotate(-3 640 360)">
    <rect x="86" y="118" width="1085" height="470" rx="24" fill="#63F4DE" filter="url(#softShadow)"/>
    <rect x="784" y="154" width="18" height="374" rx="9" fill="#0D1F2D" opacity="0.14"/>

    <text x="150" y="188" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" fill="#0D1F2D" filter="url(#tinyLift)">♟♟♟♟♟♟♟♟♟♟</text>
    <text x="150" y="224" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" fill="#0D1F2D" filter="url(#tinyLift)">♟♟♟♟♟♟♟♟♟♟</text>
    <text x="150" y="260" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" fill="#0D1F2D" filter="url(#tinyLift)">♟♟♟♟♟♟♟♟♟♟</text>
    <text x="150" y="296" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" filter="url(#tinyLift)">
      <tspan fill="#0D1F2D">♟♟♟♟♟</tspan><tspan fill="#FFFFFF">♟♟♟♟♟</tspan>
    </text>
    <text x="150" y="332" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" fill="#FFFFFF" filter="url(#tinyLift)">♟♟♟♟♟♟♟♟♟♟</text>
    <text x="150" y="368" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" fill="#FFFFFF" filter="url(#tinyLift)">♟♟♟♟♟♟♟♟♟♟</text>
    <text x="150" y="404" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" fill="#FFFFFF" filter="url(#tinyLift)">♟♟♟♟♟♟♟♟♟♟</text>
    <text x="150" y="440" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" fill="#FFFFFF" filter="url(#tinyLift)">♟♟♟♟♟♟♟♟♟♟</text>
    <text x="150" y="476" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" fill="#FFFFFF" filter="url(#tinyLift)">♟♟♟♟♟♟♟♟♟♟</text>
    <text x="150" y="512" width="405" font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" letter-spacing="9" fill="#FFFFFF" filter="url(#tinyLift)">♟♟♟♟♟♟♟♟♟♟</text>

    <rect x="612" y="181" width="176" height="42" rx="21" fill="#0D1F2D"/>
    <text x="636" y="211" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#63F4DE" letter-spacing="2">SURVEY RESULT</text>

    <text x="608" y="346" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="116" font-weight="900" fill="#0D1F2D" filter="url(#softShadow)">35%</text>
    <text x="805" y="292" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="39" font-weight="900" fill="#0D1F2D" letter-spacing="1.5">
      <tspan x="805" dy="0">OF CAMPERS</tspan>
      <tspan x="805" dy="46">DON’T LIKE</tspan>
    </text>
    <text x="805" y="414" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="43" font-weight="900" fill="#A46B16" letter-spacing="1.5">SMORES*</text>
    <text x="610" y="522" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-style="italic" fill="#0D1F2D" opacity="0.72">*According to a recent customer camping survey</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ `<use>` or `<symbol>` to repeat one icon 100 times; duplicate editable glyph rows or explicit paths instead.
- ❌ `<pattern>` fills for the icon matrix; PowerPoint translation will not preserve them as editable pictographs.
- ❌ Clipping or masking non-image elements to “fill” the percentage; instead color complete icons by count.
- ❌ Overly tiny icons with weak contrast; the grid must read as 100 individual units from slide-view distance.
- ❌ Centering the number inside the grid unless the story requires it; the strongest layout is usually grid left, data statement right.

## Composition notes
- Keep the 10×10 matrix in a square zone occupying roughly 35–45% of slide width; it should feel dense but not cramped.
- Use a high-contrast active color and a calm inactive color so the percentage is understood before the audience reads the number.
- Pair the matrix with massive typography; the number should be the dominant text element, with context stacked beside or below it.
- Leave generous negative space around the card or grid so 100 icons do not visually overwhelm the slide.