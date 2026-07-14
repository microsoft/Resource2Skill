# SVG Recipe — Organic Wave Section Divider

## Visual mechanism
A deep gradient backdrop is anchored by 3–4 overlapping, smooth organic wave bands rising from the bottom edge. Centered uppercase typography floats in the calm negative space above the waves, creating a polished chapter-divider slide with strong contrast and gentle motion.

## SVG primitives needed
- 1× `<rect>` for the full-slide navy gradient background
- 4× `<path>` for stacked organic wave layers with different amplitudes, colors, and depths
- 2× `<ellipse>` for soft atmospheric glow accents behind the waves
- 1× `<path>` for a thin translucent highlight crest line on the front wave
- 3× `<text>` for eyebrow, main title, and optional section descriptor
- 2× `<linearGradient>` for the background and front wave color depth
- 2× `<radialGradient>` for soft teal glow accents
- 2× `<filter>` using `feGaussianBlur` / `feOffset` for glow and soft shadow depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgNavy" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#0C102A"/>
      <stop offset="52%" stop-color="#11183E"/>
      <stop offset="100%" stop-color="#191E50"/>
    </linearGradient>

    <linearGradient id="frontTeal" x1="0" y1="340" x2="1280" y2="720">
      <stop offset="0%" stop-color="#70E2C6"/>
      <stop offset="46%" stop-color="#58D3B6"/>
      <stop offset="100%" stop-color="#34B99E"/>
    </linearGradient>

    <linearGradient id="midGreen" x1="0" y1="390" x2="1280" y2="690">
      <stop offset="0%" stop-color="#327F77"/>
      <stop offset="55%" stop-color="#459681"/>
      <stop offset="100%" stop-color="#286E69"/>
    </linearGradient>

    <radialGradient id="tealGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#74F2D7" stop-opacity="0.48"/>
      <stop offset="72%" stop-color="#2CBFA8" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#2CBFA8" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="violetGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#4960FF" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#4960FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="waveShadow" x="-10%" y="-15%" width="120%" height="140%">
      <feOffset dx="0" dy="-10" in="SourceAlpha" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="30"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgNavy)"/>

  <ellipse cx="215" cy="610" rx="360" ry="165" fill="url(#tealGlow)" filter="url(#softGlow)" opacity="0.62"/>
  <ellipse cx="1040" cy="505" rx="310" ry="145" fill="url(#violetGlow)" filter="url(#softGlow)" opacity="0.72"/>

  <path
    d="M 0 720
       L 0 414
       C 140 318, 280 292, 423 354
       C 560 413, 665 550, 815 520
       C 984 486, 1052 327, 1280 365
       L 1280 720 Z"
    fill="#191C4D"
    opacity="0.98"/>

  <path
    d="M 0 720
       L 0 482
       C 126 390, 252 372, 404 430
       C 560 490, 640 593, 810 560
       C 980 527, 1062 422, 1280 444
       L 1280 720 Z"
    fill="url(#midGreen)"
    opacity="0.96"
    filter="url(#waveShadow)"/>

  <path
    d="M 0 720
       L 0 525
       C 160 382, 314 370, 468 455
       C 606 532, 736 642, 892 598
       C 1048 554, 1124 427, 1280 468
       L 1280 720 Z"
    fill="#3FB69E"
    opacity="0.92"/>

  <path
    d="M 0 720
       L 0 558
       C 138 438, 268 394, 430 472
       C 566 538, 678 665, 844 631
       C 1018 596, 1112 478, 1280 506
       L 1280 720 Z"
    fill="url(#frontTeal)"
    filter="url(#waveShadow)"/>

  <path
    d="M 18 558
       C 155 443, 276 414, 424 486
       C 564 554, 684 661, 842 628
       C 1008 594, 1112 493, 1264 511"
    fill="none"
    stroke="#B8FFF0"
    stroke-width="3"
    stroke-opacity="0.34"/>

  <path
    d="M 0 720
       L 0 649
       C 185 603, 305 633, 456 656
       C 642 685, 816 704, 1004 662
       C 1118 636, 1210 631, 1280 646
       L 1280 720 Z"
    fill="#96F3DE"
    opacity="0.20"/>

  <text x="640" y="155" width="720"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="27"
        font-weight="700"
        letter-spacing="5"
        fill="#D6FFF5"
        opacity="0.95">PART 01</text>

  <text x="640" y="260" width="980"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="66"
        font-weight="800"
        letter-spacing="1"
        fill="#FFFFFF">
    <tspan x="640" dy="0">ORGANIC GROWTH</tspan>
    <tspan x="640" dy="78">STRATEGY</tspan>
  </text>

  <text x="640" y="404" width="760"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22"
        font-weight="400"
        letter-spacing="0.4"
        fill="#BFD0FF"
        opacity="0.82">A fluid transition into the next chapter</text>
</svg>
```

## Avoid in this skill
- ❌ Using rasterized wave images when editable `<path>` waves can reproduce the same premium effect.
- ❌ Hard straight dividers or rectangular blocks; the technique depends on fluid, asymmetric curves.
- ❌ Applying `clip-path` to wave paths; clipping only translates reliably on `<image>`.
- ❌ Overloading the upper half with icons, charts, or body copy; this is a section divider, not a content slide.
- ❌ Using low-contrast pastel text over the dark background; keep typography crisp and white or near-white.

## Composition notes
- Keep the main title centered in the upper-middle third, roughly y=210–340, with generous negative space around it.
- Let waves occupy the lower 40–50% of the slide; the front wave should touch the bottom edge and feel grounded.
- Use 3 layered wave colors: darkest in back, muted teal in the middle, brightest mint/teal in front.
- For a Morph transition series, duplicate the slide and slightly change each wave path’s control points or phase while keeping text position stable.