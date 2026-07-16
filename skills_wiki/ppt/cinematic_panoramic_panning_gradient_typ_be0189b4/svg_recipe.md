# SVG Recipe — Cinematic Panoramic Panning & Gradient Typography

## Visual mechanism
Use one ultra-wide panoramic image that extends beyond the 1280×720 slide and shift its `x` position between duplicated slides to create a Morph-style camera pan. Overlay huge typography filled with a white-to-transparent gradient so the words feel absorbed by mist, light, or atmosphere rather than pasted on top.

## SVG primitives needed
- 1× oversized `<image>` for the panoramic background, wider than the canvas and horizontally offset
- 1× `<clipPath>` with a full-slide `<rect>` applied to the image so the panorama crops cleanly to the viewport
- 3× `<linearGradient>` for atmospheric edge shading, title gradient fill, and subtitle gradient fill
- 2× `<rect>` overlays for cinematic darkening and readable text contrast
- 1× `<filter id="softShadow">` applied to small accent cards/text for premium depth
- 1× `<filter id="mistBlur">` applied to translucent mist paths for environmental blending
- 3× organic `<path>` shapes for foreground mist and depth haze
- 1× accent `<rect>` badge in crimson to punctuate the natural color field
- 5× `<text>` elements with explicit `width` attributes for title, subtitle, label, body copy, and small location metadata
- 2× `<line>` elements for minimal cinematic guide marks / title anchoring

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="slideCrop">
      <rect x="0" y="0" width="1280" height="720" rx="0"/>
    </clipPath>

    <linearGradient id="vignetteLeft" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#061014" stop-opacity="0.86"/>
      <stop offset="42%" stop-color="#061014" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#061014" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bottomFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#061014" stop-opacity="0"/>
      <stop offset="70%" stop-color="#061014" stop-opacity="0.44"/>
      <stop offset="100%" stop-color="#061014" stop-opacity="0.9"/>
    </linearGradient>

    <linearGradient id="titleFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.78"/>
      <stop offset="78%" stop-color="#FFFFFF" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="subtitleFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.56"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="mistBlur" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <!-- Oversized panorama: duplicate this slide and change x from -210 to about -760 for the next Morph keyframe -->
  <image
    href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&amp;w=2400&amp;auto=format&amp;fit=crop"
    xlink:href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&amp;w=2400&amp;auto=format&amp;fit=crop"
    x="-210" y="0" width="1980" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#slideCrop)"/>

  <!-- Cinematic grading overlays -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignetteLeft)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomFade)"/>

  <!-- Environmental mist, deliberately soft and irregular -->
  <path d="M-40 565 C150 520 250 610 405 560 C590 500 690 620 850 560 C1010 505 1130 570 1340 525 L1340 760 L-40 760 Z"
        fill="#D9EDF2" opacity="0.18" filter="url(#mistBlur)"/>
  <path d="M-80 115 C110 75 245 138 380 102 C520 64 628 92 790 72 C940 54 1090 72 1360 28 L1360 -40 L-80 -40 Z"
        fill="#FFFFFF" opacity="0.08" filter="url(#mistBlur)"/>
  <path d="M760 428 C870 390 955 430 1040 398 C1135 362 1200 390 1320 350 L1320 472 C1160 502 1020 494 890 520 C820 535 775 506 720 490 Z"
        fill="#BBD9D2" opacity="0.14" filter="url(#mistBlur)"/>

  <!-- Small premium accent -->
  <rect x="76" y="92" width="136" height="34" rx="17" fill="#B4141E" opacity="0.95" filter="url(#softShadow)"/>
  <text x="96" y="115" width="108" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.8" fill="#FFFFFF">EXPEDITION</text>

  <!-- Fine guide marks -->
  <line x1="76" y1="165" x2="212" y2="165" stroke="#FFFFFF" stroke-opacity="0.48" stroke-width="1.5"/>
  <line x1="76" y1="598" x2="188" y2="598" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="1.5"/>

  <!-- Gradient typography: fades into the landscape on the right edge -->
  <text x="70" y="312" width="820"
        font-family="Segoe UI Light, Microsoft YaHei, sans-serif"
        font-size="126" font-weight="300" letter-spacing="9"
        fill="url(#titleFade)">JOURNEY</text>

  <text x="76" y="365" width="580"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" letter-spacing="7"
        fill="url(#subtitleFade)">TO THE SECRET LAND</text>

  <text x="78" y="430" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" line-height="1.45"
        fill="#FFFFFF" opacity="0.78">
    <tspan x="78" dy="0">Explore the untouched wilderness and experience</tspan>
    <tspan x="78" dy="27">a five-day immersive expedition through mist,</tspan>
    <tspan x="78" dy="27">stone, forest, and high alpine silence.</tspan>
  </text>

  <text x="76" y="575" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" letter-spacing="3.2"
        fill="#FFFFFF" opacity="0.58">PANORAMA FRAME 01 / MOUNTAIN NORTHWEST</text>

  <text x="1030" y="646" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="200"
        fill="#FFFFFF" opacity="0.22">01</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the pan; create two duplicated slides with the same oversized image and different `x` positions, then use PowerPoint Morph.
- ❌ Do not use `<mask>` for fading text; use a native `<linearGradient>` as the text fill instead.
- ❌ Do not crop the panorama to a normal slide-sized image before placing it; the background must extend well beyond the canvas to make the camera move believable.
- ❌ Do not use `<textPath>` for artistic lettering; it will not translate reliably.
- ❌ Do not put `clip-path` on text or overlay shapes; use clipping only on the panoramic `<image>` if needed.

## Composition notes
- Keep the panorama 150–200% of slide width; for the next Morph keyframe, duplicate the slide and shift the image left by several hundred pixels while preserving the same `width`, `height`, and `y`.
- Place the giant title in the lower-left or mid-left third, letting the transparent side dissolve into bright sky, fog, water, or snow.
- Use dark vignette overlays only where text sits; preserve a wide untouched scenic area on the right so the slide feels cinematic rather than poster-like.
- Add one small saturated accent, such as crimson, amber, or electric blue, to create a premium focal point without competing with the landscape.