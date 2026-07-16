# SVG Recipe — Layered Title Block

## Visual mechanism
A large, bold background title anchors the slide, then a darker translucent panel slices across it to partially obscure the lower portion and create depth. The foreground title sits inside the panel, producing a sharp hierarchy between broad theme and precise message.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 2× `<circle>` with radial gradient fills for soft atmospheric color halos
- 3× `<path>` for abstract diagonal/architectural background accents
- 1× large `<text>` block for the oversized background title
- 1× `<rect>` for the semi-transparent overlay panel
- 1× narrow `<rect>` for the accent bar on the overlay
- 1× `<text>` block with nested `<tspan>` elements for the foreground title and small eyebrow label
- 2× `<line>` elements for thin executive-style framing rules
- 1× `<linearGradient id="bgGradient">` for the premium navy background
- 1× `<linearGradient id="panelGradient">` for the glassy overlay panel
- 1× `<radialGradient id="haloGradient">` for subtle glow fields
- 1× `<filter id="panelShadow">` applied to the overlay rectangle
- 1× `<filter id="softGlow">` applied to decorative background paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07152F"/>
      <stop offset="48%" stop-color="#0D1B38"/>
      <stop offset="100%" stop-color="#020817"/>
    </linearGradient>

    <linearGradient id="panelGradient" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.82"/>
      <stop offset="56%" stop-color="#07101F" stop-opacity="0.70"/>
      <stop offset="100%" stop-color="#12284A" stop-opacity="0.62"/>
    </linearGradient>

    <radialGradient id="haloGradient" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2ED3FF" stop-opacity="0.30"/>
      <stop offset="55%" stop-color="#1B76FF" stop-opacity="0.11"/>
      <stop offset="100%" stop-color="#1B76FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-10%" y="-40%" width="120%" height="190%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>

  <circle cx="1040" cy="124" r="250" fill="url(#haloGradient)" opacity="0.85"/>
  <circle cx="170" cy="650" r="310" fill="url(#haloGradient)" opacity="0.42"/>

  <path d="M-80 528 C170 430 268 466 472 360 C650 268 740 272 894 172 C1018 92 1124 70 1370 92"
        fill="none" stroke="#3A8DFF" stroke-width="2" opacity="0.20" filter="url(#softGlow)"/>
  <path d="M-30 588 C198 502 340 540 548 428 C722 334 812 328 966 242 C1090 174 1188 152 1330 166"
        fill="none" stroke="#9BE7FF" stroke-width="1.5" opacity="0.13"/>
  <path d="M850 -40 L1280 -40 L1280 260 C1150 234 1052 192 970 126 C918 84 886 30 850 -40 Z"
        fill="#FFFFFF" opacity="0.035"/>

  <line x1="104" y1="178" x2="348" y2="178" stroke="#68D8FF" stroke-width="2" opacity="0.72"/>
  <line x1="932" y1="544" x2="1176" y2="544" stroke="#68D8FF" stroke-width="2" opacity="0.38" stroke-dasharray="10 10"/>

  <text x="112" y="294" width="1060"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="82" font-weight="800" letter-spacing="3"
        fill="#FFFFFF" opacity="0.92">
    <tspan x="112" dy="0">THE BUSINESS NEEDS</tspan>
    <tspan x="112" dy="92">DRIVE THE</tspan>
  </text>

  <rect x="84" y="350" width="1112" height="142" rx="10"
        fill="url(#panelGradient)" filter="url(#panelShadow)"/>
  <rect x="84" y="350" width="10" height="142" rx="5"
        fill="#68D8FF"/>
  <rect x="110" y="360" width="1060" height="1.5"
        fill="#FFFFFF" opacity="0.16"/>

  <text x="128" y="395" width="1018"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        fill="#FFFFFF">
    <tspan x="128" dy="0" font-size="15" font-weight="700" letter-spacing="5" fill="#68D8FF">
      ENTERPRISE ARCHITECTURE PRINCIPLE
    </tspan>
    <tspan x="128" dy="53" font-size="38" font-weight="800" letter-spacing="1.2">
      ARCHITECTURE, NOT THE TECHNOLOGY ITSELF
    </tspan>
  </text>

  <text x="108" y="632" width="600"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" fill="#B7C8E8" opacity="0.78">
    Strategy alignment · Operating model · Scalable platforms
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a fully opaque overlay; the background title must remain partially visible to preserve the layered effect.
- ❌ Do not place the overlay completely below the large title; it should deliberately intersect the background title.
- ❌ Do not use low-contrast foreground text on the panel; the overlay title is the focal point and must remain highly legible.
- ❌ Do not rely on `<mask>` or clipping non-image elements to hide parts of the title; simple stacking order and opacity are more reliable for editable PowerPoint output.
- ❌ Do not overfill the slide with multiple competing text blocks; this technique works best when one title block dominates.

## Composition notes
- Keep the title block centered vertically or slightly below center; the overlay should cut across the lower third to lower half of the background title.
- Use a dark, restrained background so the white typography and translucent panel carry the hierarchy.
- Let the large background title occupy 70–85% of slide width, while the overlay panel can extend wider for confident executive-slide presence.
- Add only minimal accent lines, glow, or geometric traces; decorative elements should support depth without distracting from the title.