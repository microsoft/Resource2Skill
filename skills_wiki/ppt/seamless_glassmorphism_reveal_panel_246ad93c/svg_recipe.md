# SVG Recipe — Seamless Glassmorphism Reveal Panel

## Visual mechanism
A saturated full-bleed image is duplicated in perfect registration, clipped to a rounded central panel, blurred, and overlaid with translucent gradients, highlights, and shadow. The result is a frosted-glass reveal area that preserves the background’s color atmosphere while creating a premium, readable text zone.

## SVG primitives needed
- 2× `<image>` for the full-bleed background and the perfectly aligned duplicate inside the glass panel
- 1× `<clipPath>` with rounded `<rect>` for the glass image crop
- 4× `<rect>` for dark atmospheric overlay, shadow carrier, glass tint, and edge highlights
- 2× `<linearGradient>` for the background vignette and glass sheen
- 1× `<radialGradient>` for soft luminous bokeh behind the panel
- 2× `<filter>`: one blur filter for the duplicated image crop, one drop-shadow filter for the floating panel
- 3× `<path>` for foreground leaf silhouettes that break the panel boundary and add depth
- 3× `<text>` elements with explicit `width` for eyebrow, headline, and supporting copy
- 2× `<line>` for fine divider accents inside the panel

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="glassClip">
      <rect x="282" y="142" width="716" height="436" rx="42" ry="42"/>
    </clipPath>

    <linearGradient id="vignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#04170C" stop-opacity="0.10"/>
      <stop offset="48%" stop-color="#052515" stop-opacity="0.00"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.55"/>
    </linearGradient>

    <linearGradient id="glassSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="42%" stop-color="#FFFFFF" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#A7FFD0" stop-opacity="0.08"/>
    </linearGradient>

    <radialGradient id="emeraldGlow" cx="50%" cy="42%" r="54%">
      <stop offset="0%" stop-color="#55FF9A" stop-opacity="0.34"/>
      <stop offset="58%" stop-color="#1E9F55" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#062012" stop-opacity="0.00"/>
    </radialGradient>

    <filter id="cropBlur" x="230" y="90" width="820" height="540" filterUnits="userSpaceOnUse">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="panelShadow" x="220" y="92" width="840" height="560" filterUnits="userSpaceOnUse">
      <feOffset dx="0" dy="26"/>
      <feGaussianBlur stdDeviation="28"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="leafGlow" x="-40" y="-40" width="1360" height="800" filterUnits="userSpaceOnUse">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#062012"/>

  <image
    href="https://images.unsplash.com/photo-1599598425947-33002629b52a?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#emeraldGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <path d="M82,650 C120,548 206,486 286,474 C244,544 196,612 82,650 Z"
        fill="#0B3A22" opacity="0.72" filter="url(#leafGlow)"/>
  <path d="M1112,70 C1058,166 986,226 884,226 C930,142 994,74 1112,70 Z"
        fill="#1A7F42" opacity="0.58" filter="url(#leafGlow)"/>

  <rect x="282" y="142" width="716" height="436" rx="42" ry="42"
        fill="#000000" opacity="0.34" filter="url(#panelShadow)"/>

  <image
    href="https://images.unsplash.com/photo-1599598425947-33002629b52a?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
    clip-path="url(#glassClip)" filter="url(#cropBlur)" opacity="0.92"/>

  <rect x="282" y="142" width="716" height="436" rx="42" ry="42"
        fill="url(#glassSheen)" opacity="0.78"/>
  <rect x="282" y="142" width="716" height="436" rx="42" ry="42"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.52" stroke-width="1.6"/>
  <rect x="304" y="164" width="672" height="392" rx="30" ry="30"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="1"/>

  <path d="M1022,510 C1076,458 1136,444 1205,474 C1158,548 1094,582 1022,510 Z"
        fill="#21A95C" opacity="0.78"/>
  <path d="M1034,521 C1087,505 1142,501 1194,477"
        fill="none" stroke="#A4FFC7" stroke-opacity="0.55" stroke-width="2"/>

  <text x="380" y="242" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="4"
        fill="#D8FFE8" opacity="0.92">
    REGENERATIVE STRATEGY
  </text>

  <line x1="380" y1="268" x2="476" y2="268"
        stroke="#D8FFE8" stroke-opacity="0.70" stroke-width="2"/>
  <line x1="492" y1="268" x2="900" y2="268"
        stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>

  <text x="378" y="350" width="540"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="750" letter-spacing="-1.8"
        fill="#FFFFFF">
    <tspan x="378" dy="0">THE ARCHITECTURE</tspan>
    <tspan x="378" dy="68">OF RENEWAL</tspan>
  </text>

  <text x="382" y="482" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#E7FFF0" opacity="0.88">
    Redesigning our world to thrive within planetary boundaries.
  </text>

  <rect x="780" y="505" width="152" height="38" rx="19" ry="19"
        fill="#FFFFFF" opacity="0.16" stroke="#FFFFFF" stroke-opacity="0.30"/>
  <text x="805" y="530" width="110"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.6"
        fill="#FFFFFF">
    2026 BRIEF
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using an opaque flat rectangle as the panel; it destroys the seamless frosted-glass illusion.
- ❌ Cropping the glass duplicate differently from the background image; the reveal only works when both images share the same `x`, `y`, `width`, `height`, and `preserveAspectRatio`.
- ❌ Applying `clip-path` to non-image elements for this effect; keep clipping on the duplicated `<image>` and use rounded `<rect>` overlays for tint and borders.
- ❌ Using `<mask>`, `<foreignObject>`, `<textPath>`, or animated SVG tags to simulate the reveal; use PowerPoint Morph between duplicate slides if animation is needed.
- ❌ Overloading the panel with many text boxes; glassmorphism works best with restrained, high-contrast typography.

## Composition notes
- Center the panel and let it occupy roughly 55–60% of the slide width and height, leaving visible saturated background around all sides.
- Use the same full-slide image twice: once as the background and once as the clipped glass layer, perfectly aligned for a seamless reveal.
- Keep text inside the panel left-aligned or centered with generous margins; the glass panel is the reading zone, not just decoration.
- Add one or two foreground organic shapes crossing the panel edge to create depth and make the glass feel physically embedded in the scene.