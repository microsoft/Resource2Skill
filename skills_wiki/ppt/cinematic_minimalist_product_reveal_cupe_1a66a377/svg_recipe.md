# SVG Recipe — Cinematic Product Reveal Slide

## Visual mechanism
A nearly empty, white keynote slide uses oversized Swiss-style typography and a dark, low-profile product silhouette floating above a saturated neon under-glow. The visual drama comes from the contrast between crisp matte hardware edges and large, blurred magenta/purple light pools that imply depth, mystery, and premium technology.

## SVG primitives needed
- 1× `<rect>` for the full-slide off-white background
- 3× blurred `<ellipse>` for the diffuse cinematic neon under-glow
- 1× blurred `<path>` for the concentrated horizontal light core beneath the product
- 3× `<rect>` for the product silhouette: main body, subtle top highlight, and front rim
- 2× `<line>` for small edge seams and speaker-like detail on the product
- 2× `<path>` for tiny specular glints along the product edge
- 2× `<text>` blocks for the large reveal title and restrained subtitle
- 3× `<linearGradient>` definitions for background softness, product metal shading, and glow color transitions
- 2× `<filter>` definitions: one heavy Gaussian blur for neon glow, one soft shadow for the product body

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="62%" stop-color="#F8F8FA"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <linearGradient id="deviceMetal" x1="230" y1="0" x2="1050" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1C1C1E"/>
      <stop offset="14%" stop-color="#3A3A3D"/>
      <stop offset="50%" stop-color="#232326"/>
      <stop offset="86%" stop-color="#424247"/>
      <stop offset="100%" stop-color="#19191B"/>
    </linearGradient>

    <linearGradient id="rimLight" x1="260" y1="0" x2="1020" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#606067" stop-opacity="0.25"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#606067" stop-opacity="0.25"/>
    </linearGradient>

    <linearGradient id="hotCore" x1="250" y1="0" x2="1030" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#5856D6" stop-opacity="0"/>
      <stop offset="18%" stop-color="#5856D6" stop-opacity="0.85"/>
      <stop offset="52%" stop-color="#FF00A8" stop-opacity="1"/>
      <stop offset="82%" stop-color="#AF52DE" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#FF00A8" stop-opacity="0"/>
    </linearGradient>

    <filter id="neonBlur" x="-35%" y="-150%" width="170%" height="400%">
      <feGaussianBlur stdDeviation="42"/>
    </filter>

    <filter id="productShadow" x="-10%" y="-80%" width="120%" height="260%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="118" y="123" width="660"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="700" letter-spacing="-2.2"
        fill="#1D1D1F">Proprietary Tech</text>

  <text x="121" y="173" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400" letter-spacing="-0.25"
        fill="#86868B">What advantages do we have?</text>

  <ellipse cx="640" cy="432" rx="425" ry="82" fill="#FF00A8" opacity="0.42" filter="url(#neonBlur)"/>
  <ellipse cx="540" cy="444" rx="300" ry="68" fill="#5856D6" opacity="0.36" filter="url(#neonBlur)"/>
  <ellipse cx="770" cy="438" rx="290" ry="62" fill="#AF52DE" opacity="0.28" filter="url(#neonBlur)"/>

  <path d="M285 407
           C390 386, 890 386, 995 407
           C1008 410, 1007 425, 992 427
           C858 445, 420 445, 287 427
           C272 425, 272 410, 285 407 Z"
        fill="url(#hotCore)" opacity="0.88" filter="url(#neonBlur)"/>

  <rect x="252" y="352" width="776" height="116" rx="34" ry="34"
        fill="url(#deviceMetal)" stroke="#5B5B61" stroke-width="1.4"
        filter="url(#productShadow)"/>

  <rect x="274" y="362" width="732" height="19" rx="9.5" ry="9.5"
        fill="url(#rimLight)" opacity="0.55"/>

  <rect x="287" y="432" width="706" height="14" rx="7" ry="7"
        fill="#101012" opacity="0.72"/>

  <line x1="338" y1="390" x2="475" y2="390"
        stroke="#77777E" stroke-width="2" stroke-linecap="round" opacity="0.42"/>

  <line x1="808" y1="390" x2="944" y2="390"
        stroke="#77777E" stroke-width="2" stroke-linecap="round" opacity="0.34"/>

  <path d="M286 370 C332 356, 402 356, 448 369"
        fill="none" stroke="#FFFFFF" stroke-width="2.4"
        stroke-linecap="round" opacity="0.18"/>

  <path d="M820 369 C875 355, 957 357, 1000 374"
        fill="none" stroke="#FFFFFF" stroke-width="2"
        stroke-linecap="round" opacity="0.14"/>

  <text x="118" y="622" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" letter-spacing="1.7"
        fill="#A1A1A6">REVEALING NEXT-GENERATION ARCHITECTURE</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade the glow; build the effect from blurred ellipses and paths instead.
- ❌ Do not apply `filter` to `<line>` details on the product; line filters are dropped, so keep seams crisp.
- ❌ Do not use `<pattern>` for metal texture; use subtle linear gradients and a few editable highlight paths.
- ❌ Do not overcrowd the slide with feature bullets, icons, or UI panels; this technique depends on cinematic restraint.
- ❌ Do not place `clip-path` on the product silhouette; clipping is reliable for images only, and this reveal works better as native rounded rectangles and paths.

## Composition notes
- Keep the upper-left typography large but sparse; title and subtitle should occupy no more than the top-left third of the slide.
- Place the product horizontally across the middle-lower band, with the glow extending wider than the hardware to create a volumetric light spill.
- Use a white or near-white background for maximum contrast against graphite hardware and saturated magenta/purple lighting.
- Let the bottom and right side breathe; negative space is part of the premium launch-slide effect.