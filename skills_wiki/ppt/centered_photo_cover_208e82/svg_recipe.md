# SVG Recipe — Centered Photo Cover

## Visual mechanism
A full-bleed editorial photograph fills the entire slide, darkened by cinematic gradient overlays so a centered title plaque reads crisply. The title sits inside a restrained translucent frame with thin rules, corner ticks, and subtle shadowing for a premium section-divider look.

## SVG primitives needed
- 1× `<image>` for the full-bleed background photo, using `preserveAspectRatio="xMidYMid slice"`
- 3× full-slide `<rect>` overlays for base tint, left-to-right editorial gradient, and radial vignette
- 2× decorative `<path>` shapes for soft diagonal light/dark bands over the photo
- 2× centered `<rect>` shapes for the translucent title panel and fine border frame
- 8× `<line>` elements for minimal corner ticks around the title frame
- 3× `<text>` elements for eyebrow/section label, main title, and subtitle
- 1× `<text>` element for the optional footer
- 2× `<linearGradient>` definitions for photographic color grading and decorative band fills
- 1× `<radialGradient>` definition for the vignette
- 1× `<filter id="panelShadow">` applied to the centered title panel
- 1× `<filter id="softGlow">` applied to the main title text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoGrade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#06101F" stop-opacity="0.82"/>
      <stop offset="45%" stop-color="#0A1422" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#05080E" stop-opacity="0.74"/>
    </linearGradient>

    <radialGradient id="centerLift" cx="50%" cy="48%" r="72%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="46%" stop-color="#152033" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#02050A" stop-opacity="0.74"/>
    </radialGradient>

    <linearGradient id="coolBand" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#9EDCFF" stop-opacity="0.22"/>
      <stop offset="55%" stop-color="#466A8C" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="panelFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0E1B2A" stop-opacity="0.76"/>
      <stop offset="55%" stop-color="#07111D" stop-opacity="0.68"/>
      <stop offset="100%" stop-color="#0A1624" stop-opacity="0.78"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-30%" width="140%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-8%" y="-20%" width="116%" height="140%">
      <feGaussianBlur stdDeviation="2"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#08111E"/>

  <image
    href="https://images.example.com/editorial-full-bleed-mountain-lake-at-dusk.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="#06101A" opacity="0.18"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#photoGrade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerLift)"/>

  <path d="M-80 128 C184 64 360 84 560 30 C740 -18 958 4 1360 -92 L1360 76 C1010 150 766 122 552 168 C320 218 124 198 -80 260 Z"
        fill="url(#coolBand)" opacity="0.58"/>
  <path d="M-60 650 C210 590 348 620 580 568 C838 510 1030 544 1370 430 L1370 720 L-60 720 Z"
        fill="#02060B" opacity="0.35"/>

  <rect x="365" y="238" width="550" height="244" rx="3"
        fill="url(#panelFill)" filter="url(#panelShadow)"/>

  <rect x="385" y="258" width="510" height="204" rx="1"
        fill="none" stroke="#E8F4FF" stroke-opacity="0.68" stroke-width="1.4"/>

  <line x1="385" y1="258" x2="442" y2="258" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.86"/>
  <line x1="385" y1="258" x2="385" y2="315" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.86"/>
  <line x1="895" y1="258" x2="838" y2="258" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.86"/>
  <line x1="895" y1="258" x2="895" y2="315" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.86"/>
  <line x1="385" y1="462" x2="442" y2="462" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.86"/>
  <line x1="385" y1="462" x2="385" y2="405" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.86"/>
  <line x1="895" y1="462" x2="838" y2="462" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.86"/>
  <line x1="895" y1="462" x2="895" y2="405" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.86"/>

  <line x1="490" y1="302" x2="790" y2="302" stroke="#A8C8E8" stroke-width="1" stroke-opacity="0.55"/>
  <line x1="490" y1="418" x2="790" y2="418" stroke="#A8C8E8" stroke-width="1" stroke-opacity="0.55"/>

  <text x="640" y="292" width="420" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="3.5"
        fill="#C8DDF2" opacity="0.92">
    EXECUTIVE BRIEFING
  </text>

  <text x="640" y="371" width="480" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" font-weight="700" letter-spacing="-1.2"
        fill="#FFFFFF" filter="url(#softGlow)">
    Centered Photo Cover
  </text>

  <text x="640" y="404" width="455" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="400"
        fill="#D9E8F6" opacity="0.88">
    A calm visual opening for strategy, product, and leadership narratives
  </text>

  <text x="640" y="658" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="500" letter-spacing="1.6"
        fill="#F3F8FF" opacity="0.72">
    Q4 PLANNING SESSION  ·  CONFIDENTIAL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a flat solid-color background instead of a full-bleed image; the technique depends on photographic atmosphere.
- ❌ Placing text directly on a busy photo without gradient grading or a translucent title panel.
- ❌ Overdecorating the center box with many icons, bullets, or charts; this cover should stay low-density and editorial.
- ❌ Applying `clip-path` or mask effects to non-image elements for the panel; use regular editable rectangles, strokes, and opacity instead.
- ❌ Making the title frame too large; it should feel deliberately centered, not like a full content card.

## Composition notes
- Keep the title plaque centered both horizontally and vertically, occupying roughly 40–45% of slide width and 25–35% of slide height.
- Use strong darkening at the photo edges and a mild lift around the center so the title feels spotlighted.
- Let the image remain visible around all four sides; the negative space is what makes the cover feel premium.
- Use a restrained palette pulled from the photo, typically cool navy, white, mist blue, or warm ivory accents.