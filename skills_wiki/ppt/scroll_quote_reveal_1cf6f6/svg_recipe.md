# SVG Recipe — Scroll Quote Reveal

## Visual mechanism
A quote is staged as if it has just been revealed on a descending paper scroll or projector canvas: a soft-lit background, cylindrical top roll, hanging sheet, accent ribbon, and oversized quotation marks create a premium “unfurling” moment. The center remains calm and typographic while shadows, curls, and gradients imply physical depth.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<radialGradient>` for the spotlight wash behind the scroll
- 4× `<linearGradient>` fills for the paper, roller, accent ribbon, and metallic end caps
- 2× `<filter>` definitions: one soft drop shadow for the paper/roller and one subtle glow for decorative emphasis
- 1× large `<rect>` for the paper canvas
- 1× `<path>` for the curled lower paper edge
- 1× `<rect>` for the top cylindrical roller body
- 2× `<ellipse>` for the roller end caps
- 2× `<line>` for the hanging cords
- 2× small `<circle>` elements for cord knobs
- 1× `<rect>` for the horizontal accent strip
- 4× decorative `<path>` elements for abstract background swooshes and reveal glints
- 4× `<text>` elements for headline, quote mark, main quote, and author attribution

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="42%" r="70%">
      <stop offset="0%" stop-color="#2E4667"/>
      <stop offset="52%" stop-color="#14243A"/>
      <stop offset="100%" stop-color="#07111F"/>
    </radialGradient>

    <linearGradient id="paperGrad" x1="0" y1="110" x2="0" y2="555" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFF8E8"/>
      <stop offset="55%" stop-color="#F7EBCF"/>
      <stop offset="100%" stop-color="#EEDDB7"/>
    </linearGradient>

    <linearGradient id="rollerGrad" x1="250" y1="95" x2="1030" y2="153" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#8A5A2F"/>
      <stop offset="18%" stop-color="#D29A54"/>
      <stop offset="48%" stop-color="#F0C278"/>
      <stop offset="78%" stop-color="#B87538"/>
      <stop offset="100%" stop-color="#6E421F"/>
    </linearGradient>

    <linearGradient id="capGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F6D18D"/>
      <stop offset="48%" stop-color="#B77335"/>
      <stop offset="100%" stop-color="#4B2B16"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="330" y1="0" x2="950" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF6A3D"/>
      <stop offset="55%" stop-color="#FFB000"/>
      <stop offset="100%" stop-color="#FFD36B"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="warmGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <path d="M92,184 C198,96 286,92 392,152 C252,168 158,228 92,184 Z" fill="#6DD7FF" opacity="0.10" filter="url(#warmGlow)"/>
  <path d="M930,558 C1068,470 1162,494 1224,602 C1090,570 1016,616 930,558 Z" fill="#FFB000" opacity="0.12" filter="url(#warmGlow)"/>
  <path d="M106,570 C238,610 332,588 414,520" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="5 14" opacity="0.20"/>
  <path d="M884,178 C986,126 1092,136 1174,218" fill="none" stroke="#FFD36B" stroke-width="3" stroke-dasharray="2 18" opacity="0.28"/>

  <line x1="352" y1="132" x2="352" y2="604" stroke="#D9A35B" stroke-width="4" opacity="0.55"/>
  <line x1="928" y1="132" x2="928" y2="604" stroke="#D9A35B" stroke-width="4" opacity="0.55"/>
  <circle cx="352" cy="613" r="12" fill="#FFB000" opacity="0.85"/>
  <circle cx="928" cy="613" r="12" fill="#FFB000" opacity="0.85"/>

  <rect x="330" y="126" width="620" height="418" rx="16" fill="url(#paperGrad)" filter="url(#softShadow)"/>
  <path d="M330,512 C414,548 498,548 580,514 C672,476 770,478 950,518 L950,544 L330,544 Z"
        fill="#D8BD85" opacity="0.55"/>
  <path d="M330,517 C426,546 522,546 618,516 C716,486 816,490 950,523"
        fill="none" stroke="#B88948" stroke-width="2" opacity="0.40"/>

  <rect x="330" y="126" width="620" height="20" rx="10" fill="url(#accentGrad)"/>
  <rect x="250" y="94" width="780" height="60" rx="30" fill="url(#rollerGrad)" filter="url(#softShadow)"/>
  <ellipse cx="250" cy="124" rx="34" ry="31" fill="url(#capGrad)"/>
  <ellipse cx="1030" cy="124" rx="34" ry="31" fill="url(#capGrad)"/>
  <ellipse cx="250" cy="124" rx="17" ry="15" fill="#5C351A" opacity="0.65"/>
  <ellipse cx="1030" cy="124" rx="17" ry="15" fill="#5C351A" opacity="0.65"/>

  <text x="640" y="204" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700"
        letter-spacing="3" fill="#9C6A2E" opacity="0.92">
    LEADERSHIP NOTE
  </text>

  <text x="640" y="294" width="520" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', serif" font-size="108" font-weight="700"
        fill="#D9A35B" opacity="0.28">
    “
  </text>

  <text x="640" y="322" width="510" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700"
        fill="#263246">
    <tspan x="640" dy="0">The best strategy is the one</tspan>
    <tspan x="640" dy="46">people can remember, repeat,</tspan>
    <tspan x="640" dy="46">and rally behind.</tspan>
  </text>

  <rect x="526" y="472" width="228" height="3" rx="1.5" fill="#FFB000" opacity="0.85"/>
  <text x="640" y="508" width="420" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700"
        fill="#7B5B2B">
    — Maya Chen, Chief Strategy Officer
  </text>

  <path d="M438,246 L456,260 L438,274 L420,260 Z" fill="#FFB000" opacity="0.55" filter="url(#warmGlow)"/>
  <path d="M828,420 L844,432 L828,444 L812,432 Z" fill="#FF6A3D" opacity="0.45" filter="url(#warmGlow)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to reveal the quote; use layered paper shapes, gradients, and cropped-looking geometry instead.
- ❌ Do not apply `filter` to `<line>` cords; shadows/glows on lines are dropped by the translator.
- ❌ Do not use `<textPath>` for curved scroll lettering; keep quote text as editable horizontal `<text>` with explicit `width`.
- ❌ Do not use `<pattern>` for paper texture; simulate texture with subtle gradients, translucent paths, and low-opacity strokes.

## Composition notes
- Keep the scroll centered and large, occupying roughly 55–65% of slide width so the quote feels ceremonial.
- Reserve the brightest accent color for the top reveal strip and small glints; this guides the eye without overwhelming the quote.
- Use a dark, spacious background to make the warm paper feel illuminated and premium.
- Main quote should sit in the middle third of the paper; author attribution belongs near the lower edge with a thin divider.