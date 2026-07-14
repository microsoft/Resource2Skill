# SVG Recipe — Composite Call-to-Action (CTA) Graphic

## Visual mechanism
A CTA becomes visually “clickable” by stacking a high-contrast rounded pill button, urgent hook text, inward-pointing curved arrows, and soft elevation shadows into one centered composite object. The arrows act as visual brackets that pull the eye toward the primary action text.

## SVG primitives needed
- 1× `<rect>` for the full-slide premium background.
- 2× `<ellipse>` for soft spotlight/halo emphasis behind the CTA.
- 3× `<rect>` for the button body, glossy top highlight, and crisp border.
- 2× `<path>` for large inward-facing curved block arrows.
- 2× `<path>` for arrow highlight strokes.
- 2× `<path>` for subtle background motion arcs.
- 1× `<rect>` for a small accent underline below the main button text.
- 3× `<text>` elements for the secondary hook, primary action, and supporting microcopy.
- 3× `<linearGradient>` for the button surface, accent arrows, and shine.
- 1× `<radialGradient>` for the central spotlight.
- 2× `<filter>` definitions: one drop shadow for clickability, one soft blur for the halo.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="backgroundGlow" cx="50%" cy="48%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="48%" stop-color="#F4F8FC"/>
      <stop offset="100%" stop-color="#E8EEF6"/>
    </radialGradient>

    <linearGradient id="buttonBlue" x1="360" y1="356" x2="920" y2="474" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1F78B4"/>
      <stop offset="52%" stop-color="#174F8A"/>
      <stop offset="100%" stop-color="#0F355F"/>
    </linearGradient>

    <linearGradient id="accentRed" x1="210" y1="260" x2="1070" y2="430" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#E53935"/>
      <stop offset="48%" stop-color="#C00000"/>
      <stop offset="100%" stop-color="#8F0000"/>
    </linearGradient>

    <linearGradient id="buttonShine" x1="380" y1="368" x2="900" y2="398" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.46"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-40%" width="150%" height="190%">
      <feOffset in="SourceAlpha" dx="0" dy="14" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="haloBlur" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#backgroundGlow)"/>

  <ellipse cx="640" cy="418" rx="390" ry="165" fill="#9CC9F4" opacity="0.22" filter="url(#haloBlur)"/>
  <ellipse cx="640" cy="432" rx="305" ry="92" fill="#FFFFFF" opacity="0.72"/>

  <path d="M132,510 C278,418 369,561 512,488 C622,432 717,305 896,352 C1016,384 1073,319 1152,258"
        fill="none" stroke="#C7DDF2" stroke-width="5" stroke-linecap="round" opacity="0.42"/>
  <path d="M176,224 C311,300 429,176 570,240 C720,309 828,208 965,258 C1041,286 1095,275 1156,232"
        fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.72"/>

  <text x="640" y="288" width="660" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', serif" font-size="31" font-weight="700"
        fill="#C00000" letter-spacing="1.4">
    GET INSTANT ACCESS
  </text>

  <path d="M214,402 C238,338 291,300 350,299 L350,263 L433,332 L350,401 L350,365 C307,366 276,389 257,434 Z"
        fill="url(#accentRed)" filter="url(#softShadow)"/>
  <path d="M237,394 C263,341 306,320 364,322"
        fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.32"/>

  <path d="M1066,402 C1042,338 989,300 930,299 L930,263 L847,332 L930,401 L930,365 C973,366 1004,389 1023,434 Z"
        fill="url(#accentRed)" filter="url(#softShadow)"/>
  <path d="M1043,394 C1017,341 974,320 916,322"
        fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.32"/>

  <rect x="360" y="356" width="560" height="118" rx="59" ry="59"
        fill="url(#buttonBlue)" stroke="#092746" stroke-width="3" filter="url(#softShadow)"/>
  <rect x="383" y="371" width="514" height="31" rx="15" ry="15"
        fill="url(#buttonShine)" opacity="0.9"/>
  <rect x="367" y="363" width="546" height="104" rx="52" ry="52"
        fill="none" stroke="#69A8D9" stroke-width="2" opacity="0.44"/>

  <text x="640" y="434" width="560" text-anchor="middle"
        font-family="'Arial Black', 'Segoe UI', Microsoft YaHei, sans-serif"
        font-size="52" font-weight="900" fill="#FFFFFF" letter-spacing="1">
    DOWNLOAD <tspan fill="#FFD166">NOW</tspan>
  </text>

  <rect x="505" y="452" width="270" height="5" rx="2.5" ry="2.5"
        fill="#FFD166" opacity="0.86"/>

  <text x="640" y="526" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        font-weight="600" fill="#4B6075" letter-spacing="0.4">
    One click. No friction. Start immediately.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` arrowheads for the curved arrows; build the arrows as filled `<path>` shapes so they remain editable and visible.
- ❌ Do not place `filter` on a parent `<g>` and expect all CTA parts to shadow correctly; apply the shadow directly to the button `<rect>` and arrow `<path>` elements.
- ❌ Do not rely on PowerPoint text autofit; every `<text>` needs an explicit `width` so the CTA label does not reflow unexpectedly.
- ❌ Do not use `<mask>` or clipping on non-image shapes to create shine; use a simple rounded `<rect>` highlight with opacity/gradient instead.

## Composition notes
- Keep the whole CTA cluster centered, occupying roughly 50–60% of slide width; it should read as one interactive object.
- Put the hook text above the button with enough breathing room that it feels urgent but not crowded.
- Use strong color contrast: dark saturated button, white primary action, warm accent for arrows and emphasis.
- Arrows should overlap the CTA zone visually but not compete with the main label; their purpose is to guide the eye inward.