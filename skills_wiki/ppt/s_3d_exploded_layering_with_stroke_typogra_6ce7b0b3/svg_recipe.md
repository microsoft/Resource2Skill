# SVG Recipe — 3D Exploded Layering with Stroke Typography

## Visual mechanism
A massive hollow word sits between floating product parts and the central hero object, creating an editorial “exploded view” where foreground and background layers interleave through the typography. Depth comes from strict z-ordering: moody background → distant fragments → stroke-only type → main product → foreground fragments and flecks.

## SVG primitives needed
- 1× `<rect>` for the full-slide radial-gradient background.
- 2× `<text>` for oversized stroke-only typography behind the product.
- 18× `<path>` for burger layers, cheese sheets, lettuce leaves, tomato/patty shapes, and organic ingredient fragments.
- 22× `<ellipse>` for sesame seeds, tomato interiors, ambient glows, and small flying particles.
- 8× `<circle>` for onion rings, cheese holes, and spice flecks.
- 1× `<radialGradient>` for the deep cinematic background.
- 5× `<linearGradient>` for bun, lettuce, cheese, tomato, and patty dimensional fills.
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` for floating-object depth.
- 1× `<filter id="textGlow">` using `feGaussianBlur` for subtle glow on the hollow typography.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="50%" cy="46%" r="78%">
      <stop offset="0%" stop-color="#6a3516"/>
      <stop offset="48%" stop-color="#2b1308"/>
      <stop offset="100%" stop-color="#090503"/>
    </radialGradient>

    <linearGradient id="bunGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f2b061"/>
      <stop offset="55%" stop-color="#c7772f"/>
      <stop offset="100%" stop-color="#7a3b17"/>
    </linearGradient>
    <linearGradient id="lettuceGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a9ff57"/>
      <stop offset="60%" stop-color="#35b53f"/>
      <stop offset="100%" stop-color="#147522"/>
    </linearGradient>
    <linearGradient id="cheeseGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffe66b"/>
      <stop offset="100%" stop-color="#f59b18"/>
    </linearGradient>
    <linearGradient id="tomatoGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff6b55"/>
      <stop offset="100%" stop-color="#b41017"/>
    </linearGradient>
    <linearGradient id="pattyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5d2d18"/>
      <stop offset="100%" stop-color="#1e0e08"/>
    </linearGradient>

    <filter id="softShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>
  <ellipse cx="640" cy="382" rx="360" ry="175" fill="#ff9f33" opacity="0.08"/>
  <ellipse cx="640" cy="610" rx="410" ry="58" fill="#000000" opacity="0.34"/>

  <!-- distant exploded ingredients: behind typography -->
  <g transform="translate(170 145) rotate(-22)">
    <circle cx="0" cy="0" r="54" fill="none" stroke="#be7cff" stroke-width="15" opacity="0.76" filter="url(#softShadow)"/>
    <circle cx="0" cy="0" r="32" fill="none" stroke="#f0d8ff" stroke-width="5" opacity="0.82"/>
  </g>

  <g transform="translate(1070 145) rotate(18)">
    <ellipse cx="0" cy="0" rx="72" ry="48" fill="url(#tomatoGrad)" filter="url(#softShadow)"/>
    <ellipse cx="-24" cy="0" rx="18" ry="31" fill="#861016" opacity="0.62"/>
    <ellipse cx="24" cy="0" rx="18" ry="31" fill="#861016" opacity="0.62"/>
    <ellipse cx="0" cy="-8" rx="8" ry="5" fill="#ffd7a0" opacity="0.9"/>
  </g>

  <g transform="translate(235 455) rotate(16)">
    <path d="M-110 10 C-82 -52 -25 -35 12 -70 C46 -25 102 -52 122 20 C88 72 32 48 -8 84 C-55 48 -92 70 -110 10 Z"
          fill="url(#lettuceGrad)" filter="url(#softShadow)"/>
    <path d="M-82 12 C-30 0 20 -4 96 18" fill="none" stroke="#d9ff8c" stroke-width="5" opacity="0.72"/>
  </g>

  <g transform="translate(1030 475) rotate(-27)">
    <path d="M-80 -34 L86 -12 L48 66 L-94 38 Z" fill="url(#cheeseGrad)" filter="url(#softShadow)"/>
    <circle cx="-25" cy="8" r="9" fill="#bb6c0e" opacity="0.45"/>
    <circle cx="35" cy="20" r="12" fill="#bb6c0e" opacity="0.38"/>
  </g>

  <g transform="translate(350 95) rotate(37)">
    <path d="M-60 -16 C-22 -42 48 -36 76 2 C44 35 -20 36 -72 14 Z" fill="url(#pattyGrad)" filter="url(#softShadow)"/>
  </g>

  <!-- giant hollow typography: middle depth plane -->
  <text x="47" y="304" width="1186" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="178" font-weight="900" letter-spacing="14"
        fill="none" stroke="#ffffff" stroke-width="3.4" opacity="0.86" filter="url(#textGlow)">BURGER</text>
  <text x="82" y="508" width="1116" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="184" font-weight="900" letter-spacing="18"
        fill="none" stroke="#ffffff" stroke-width="2.8" opacity="0.62">CRAFT</text>

  <!-- central hero product: in front of type -->
  <g transform="translate(640 384)">
    <path d="M-220 -88 C-202 -188 202 -188 220 -88 C173 -49 -172 -49 -220 -88 Z"
          fill="url(#bunGrad)" filter="url(#softShadow)"/>
    <ellipse cx="-104" cy="-118" rx="12" ry="5" fill="#ffe4a3" transform="rotate(-17 -104 -118)"/>
    <ellipse cx="-38" cy="-138" rx="13" ry="5" fill="#ffe4a3" transform="rotate(11 -38 -138)"/>
    <ellipse cx="38" cy="-137" rx="12" ry="5" fill="#ffe4a3" transform="rotate(-8 38 -137)"/>
    <ellipse cx="116" cy="-112" rx="13" ry="5" fill="#ffe4a3" transform="rotate(16 116 -112)"/>

    <path d="M-245 -44 C-208 -78 -164 -40 -118 -66 C-73 -31 -20 -73 27 -43 C75 -76 129 -37 171 -65 C206 -42 232 -48 252 -19
             C190 20 127 -12 75 16 C28 -18 -29 18 -81 -7 C-132 24 -190 -14 -245 -44 Z"
          fill="url(#lettuceGrad)" filter="url(#softShadow)"/>
    <path d="M-213 -12 C-118 -28 58 -31 215 -10 C220 24 187 46 128 48 L-154 46 C-207 42 -233 21 -213 -12 Z"
          fill="url(#tomatoGrad)" filter="url(#softShadow)"/>
    <path d="M-205 30 L215 30 L162 96 L68 70 L-8 122 L-78 66 L-164 98 Z"
          fill="url(#cheeseGrad)" filter="url(#softShadow)"/>
    <path d="M-218 76 C-168 43 166 43 219 76 C228 123 178 153 102 154 L-114 153 C-190 151 -235 121 -218 76 Z"
          fill="url(#pattyGrad)" filter="url(#softShadow)"/>
    <path d="M-197 140 C-124 179 124 179 198 140 C182 207 -183 207 -197 140 Z"
          fill="url(#bunGrad)" filter="url(#softShadow)"/>
  </g>

  <!-- foreground exploded ingredients: in front of hero -->
  <g transform="translate(380 548) rotate(-14)">
    <ellipse cx="0" cy="0" rx="70" ry="45" fill="url(#tomatoGrad)" filter="url(#softShadow)"/>
    <ellipse cx="-23" cy="0" rx="16" ry="29" fill="#7a0f14" opacity="0.62"/>
    <ellipse cx="24" cy="0" rx="16" ry="29" fill="#7a0f14" opacity="0.62"/>
    <ellipse cx="0" cy="-7" rx="7" ry="4" fill="#ffd7a0" opacity="0.95"/>
  </g>

  <g transform="translate(890 570) rotate(24)">
    <path d="M-100 2 C-62 -62 -10 -32 28 -76 C62 -28 112 -44 126 24 C81 80 24 50 -14 88 C-54 52 -96 72 -100 2 Z"
          fill="url(#lettuceGrad)" filter="url(#softShadow)"/>
    <path d="M-64 12 C-18 -8 38 -2 92 24" fill="none" stroke="#d8ff91" stroke-width="5" opacity="0.75"/>
  </g>

  <g transform="translate(808 190) rotate(31)">
    <circle cx="0" cy="0" r="47" fill="none" stroke="#d3a0ff" stroke-width="13" opacity="0.84" filter="url(#softShadow)"/>
    <circle cx="0" cy="0" r="26" fill="none" stroke="#fff2ff" stroke-width="4" opacity="0.9"/>
  </g>

  <circle cx="487" cy="198" r="7" fill="#ffd56b" opacity="0.9"/>
  <circle cx="748" cy="128" r="5" fill="#ff6e4a" opacity="0.82"/>
  <circle cx="928" cy="319" r="6" fill="#b6ff57" opacity="0.82"/>
  <ellipse cx="297" cy="302" rx="13" ry="5" fill="#ffe2a1" transform="rotate(27 297 302)" opacity="0.9"/>
  <ellipse cx="1010" cy="628" rx="15" ry="5" fill="#ffe2a1" transform="rotate(-18 1010 628)" opacity="0.82"/>
  <ellipse cx="558" cy="602" rx="9" ry="4" fill="#ff6e4a" transform="rotate(38 558 602)" opacity="0.9"/>

  <text x="434" y="668" width="412" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="4" fill="#fff4e5" opacity="0.72" text-anchor="middle">EXPLODED PRODUCT REVEAL</text>
</svg>
```

## Avoid in this skill
- ❌ Do not place the hollow typography as the topmost layer; it must sit between distant fragments and the hero product to create the 3D interlock.
- ❌ Do not use `<mask>` to knock out text fill. Use `fill="none"` plus a visible `stroke` on `<text>`.
- ❌ Do not rely on one flat product image with no foreground fragments; the effect needs at least three depth planes.
- ❌ Do not apply filters to `<line>` elements for sparks or motion streaks; use small `<path>`, `<circle>`, or `<ellipse>` particles instead.
- ❌ Do not use `<use>` or symbol cloning for repeated seeds/particles; duplicate the editable shapes directly.

## Composition notes
- Keep the hero product centered and large, around 35–45% of slide width, with the biggest typography spanning 85–95% of the canvas.
- Place distant ingredients near the outer thirds and corners, then put a few foreground pieces overlapping the product to sell depth.
- Use dark warm gradients behind food/product subjects; the hollow white typography needs high contrast but should remain slightly transparent.
- Rotate each exploded fragment differently and vary scale to avoid a flat “sticker sheet” look.