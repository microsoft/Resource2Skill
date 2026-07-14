# SVG Recipe — Scattered 3D Cubic Typography

## Visual mechanism
Turn single characters into tactile “thrown blocks” by building each letter tile from a front square plus two extruded polygon faces, then scatter the blocks with different rotations and offsets. The bright flat background and deep shadows make the typography feel like physical cubes dropped onto a tabletop.

## SVG primitives needed
- 1× `<rect>` for the full-slide saturated yellow background
- 2× `<circle>` for blurred ambient glow accents behind the blocks
- 6× `<ellipse>` for soft contact shadows under the scattered cubes
- 6× `<rect>` for the front faces of the main and accent letter blocks
- 12× `<path>` for top/right extrusion faces that create the 3D cubic illusion
- 6× `<path>` for small bevel/highlight strokes on block faces
- 8× `<text>` for title/caption typography and one bold character per block
- 4× `<linearGradient>` for block faces, extrusion sides, highlights, and background accents
- 2× `<filter>`: one `feGaussianBlur` glow and one `feOffset + feGaussianBlur + feMerge` shadow filter

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="44%" r="70%">
      <stop offset="0%" stop-color="#FFE96A"/>
      <stop offset="55%" stop-color="#FFD600"/>
      <stop offset="100%" stop-color="#F5B800"/>
    </radialGradient>

    <linearGradient id="frontGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFD84A"/>
      <stop offset="45%" stop-color="#FFC000"/>
      <stop offset="100%" stop-color="#E7A400"/>
    </linearGradient>

    <linearGradient id="topGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF2A0"/>
      <stop offset="100%" stop-color="#FFC928"/>
    </linearGradient>

    <linearGradient id="sideGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D99000"/>
      <stop offset="100%" stop-color="#8F5B00"/>
    </linearGradient>

    <linearGradient id="coolSide" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4D3B14"/>
      <stop offset="100%" stop-color="#201A10"/>
    </linearGradient>

    <filter id="softShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset in="SourceAlpha" dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="13" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ambientBlur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <circle cx="245" cy="165" r="94" fill="#FFF6B8" opacity="0.42" filter="url(#ambientBlur)"/>
  <circle cx="1035" cy="580" r="135" fill="#FFB000" opacity="0.35" filter="url(#ambientBlur)"/>

  <text x="72" y="78" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#3A2A00" opacity="0.72" letter-spacing="4">
    SCATTERED CUBIC TYPE
  </text>
  <text x="73" y="118" width="600" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="500" fill="#5D4300" opacity="0.64">
    Characters behave like physical blocks — readable, playful, and dimensional.
  </text>

  <g transform="translate(250 318) rotate(-13)">
    <ellipse cx="91" cy="157" rx="98" ry="30" fill="#3A2500" opacity="0.20" filter="url(#softShadow)"/>
    <path d="M0 0 L38 -30 L166 -30 L128 0 Z" fill="url(#topGold)" stroke="#FFF0A6" stroke-width="2"/>
    <path d="M128 0 L166 -30 L166 98 L128 128 Z" fill="url(#sideGold)" stroke="#A86C00" stroke-width="2"/>
    <rect x="0" y="0" width="128" height="128" rx="18" fill="url(#frontGold)" stroke="#FCE68A" stroke-width="3"/>
    <path d="M17 21 C38 8 91 7 114 20" fill="none" stroke="#FFF3A8" stroke-width="6" stroke-linecap="round" opacity="0.65"/>
    <text x="64" y="86" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="68" font-weight="900" fill="#272727">翻</text>
  </g>

  <g transform="translate(482 238) rotate(10)">
    <ellipse cx="90" cy="160" rx="104" ry="32" fill="#3A2500" opacity="0.22" filter="url(#softShadow)"/>
    <path d="M0 0 L42 -34 L170 -34 L128 0 Z" fill="url(#topGold)" stroke="#FFF0A6" stroke-width="2"/>
    <path d="M128 0 L170 -34 L170 94 L128 128 Z" fill="url(#sideGold)" stroke="#A86C00" stroke-width="2"/>
    <rect x="0" y="0" width="128" height="128" rx="18" fill="url(#frontGold)" stroke="#FCE68A" stroke-width="3"/>
    <path d="M18 104 C46 119 92 119 112 101" fill="none" stroke="#A06000" stroke-width="5" stroke-linecap="round" opacity="0.35"/>
    <text x="64" y="86" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="68" font-weight="900" fill="#252525">轉</text>
  </g>

  <g transform="translate(682 353) rotate(-4)">
    <ellipse cx="86" cy="160" rx="100" ry="31" fill="#3A2500" opacity="0.21" filter="url(#softShadow)"/>
    <path d="M0 0 L34 -27 L162 -27 L128 0 Z" fill="url(#topGold)" stroke="#FFF0A6" stroke-width="2"/>
    <path d="M128 0 L162 -27 L162 101 L128 128 Z" fill="url(#sideGold)" stroke="#A86C00" stroke-width="2"/>
    <rect x="0" y="0" width="128" height="128" rx="18" fill="url(#frontGold)" stroke="#FCE68A" stroke-width="3"/>
    <path d="M16 19 C47 8 83 8 113 19" fill="none" stroke="#FFF5B8" stroke-width="6" stroke-linecap="round" opacity="0.58"/>
    <text x="64" y="86" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="68" font-weight="900" fill="#262626">立</text>
  </g>

  <g transform="translate(890 270) rotate(16)">
    <ellipse cx="92" cy="162" rx="105" ry="32" fill="#3A2500" opacity="0.23" filter="url(#softShadow)"/>
    <path d="M0 0 L45 -32 L173 -32 L128 0 Z" fill="url(#topGold)" stroke="#FFF0A6" stroke-width="2"/>
    <path d="M128 0 L173 -32 L173 96 L128 128 Z" fill="url(#sideGold)" stroke="#A86C00" stroke-width="2"/>
    <rect x="0" y="0" width="128" height="128" rx="18" fill="url(#frontGold)" stroke="#FCE68A" stroke-width="3"/>
    <path d="M18 20 C47 9 88 9 113 22" fill="none" stroke="#FFF4AC" stroke-width="6" stroke-linecap="round" opacity="0.60"/>
    <text x="64" y="86" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="68" font-weight="900" fill="#262626">方</text>
  </g>

  <g transform="translate(168 518) rotate(18) scale(0.68)">
    <ellipse cx="68" cy="122" rx="74" ry="22" fill="#3A2500" opacity="0.16" filter="url(#softShadow)"/>
    <path d="M0 0 L28 -21 L108 -21 L80 0 Z" fill="#FFE16A" stroke="#FFF2AA" stroke-width="2"/>
    <path d="M80 0 L108 -21 L108 59 L80 80 Z" fill="url(#coolSide)" stroke="#6E520D" stroke-width="2"/>
    <rect x="0" y="0" width="80" height="80" rx="13" fill="#FFD147" stroke="#FFF2A0" stroke-width="3"/>
    <text x="40" y="52" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="900" fill="#2A2A2A">3D</text>
  </g>

  <g transform="translate(1075 500) rotate(-22) scale(0.78)">
    <ellipse cx="68" cy="122" rx="74" ry="22" fill="#3A2500" opacity="0.17" filter="url(#softShadow)"/>
    <path d="M0 0 L28 -21 L108 -21 L80 0 Z" fill="#FFE16A" stroke="#FFF2AA" stroke-width="2"/>
    <path d="M80 0 L108 -21 L108 59 L80 80 Z" fill="url(#coolSide)" stroke="#6E520D" stroke-width="2"/>
    <rect x="0" y="0" width="80" height="80" rx="13" fill="#FFD147" stroke="#FFF2A0" stroke-width="3"/>
    <text x="40" y="54" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="900" fill="#2A2A2A">!</text>
  </g>

  <text x="790" y="660" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#5C4100" opacity="0.62" text-anchor="end">
    Tip: duplicate blocks and Morph positions for a premium kinetic title.
  </text>
</svg>
```

## Avoid in this skill
- ❌ `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` to fake isometric type; these transforms are dropped by the translator.
- ❌ `<use href="#cube">` for repeating cube geometry; duplicate the actual paths and rects so PowerPoint keeps everything editable.
- ❌ Applying `clip-path` or `mask` to text or cube faces; clipping is only reliable for images.
- ❌ `filter` on `<line>` elements; use filtered ellipses or paths for shadows instead.
- ❌ Expecting SVG to create real PowerPoint 3D extrusion properties; this recipe visually simulates extrusion with editable 2D faces.

## Composition notes
- Keep the main block cluster centered, occupying roughly 45–55% of the slide width, with uneven vertical positions to create “organized chaos.”
- Use one saturated background color and one dominant block color; let side faces and shadows provide depth rather than adding many hues.
- Rotate each cube differently, but keep characters upright within their cube group so the word remains decipherable.
- Leave generous negative space in the corners for a small caption, subtitle, or presentation section label.