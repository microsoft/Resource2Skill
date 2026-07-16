# SVG Recipe — Circular Morph Reveal

## Visual mechanism
A segmented, photo-filled donut acts as a persistent navigation wheel; one annular segment is translated outward to reveal the current topic while the wheel remains as a visual anchor. Across slides, keep the same segment shapes and change only their rotation/translation so PowerPoint Morph creates the circular reveal motion.

## SVG primitives needed
- 1× `<image>` for the full-bleed atmospheric background photo
- 6× `<clipPath>` with `<path>` annular-sector geometry for image-filled donut segments
- 6× `<image>` clipped into the donut segments, one per topic
- 6× visible `<path>` overlays for white gutters/borders around each segment
- 1× `<circle>` for the central white title hub
- 1× `<circle>` translucent ring accent behind the wheel
- 1× `<filter id="softShadow">` applied to the popped-out segment and central hub
- 1× `<linearGradient>` for the dark readability wash over the background
- 1× `<radialGradient>` for subtle spotlighting behind the wheel
- 1× `<rect>` for the right-side content card
- 4× `<text>` blocks with explicit `width` attributes for title, eyebrow, heading, and body copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#07121F" stop-opacity="0.58"/>
      <stop offset="48%" stop-color="#07121F" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#07121F" stop-opacity="0.78"/>
    </linearGradient>
    <radialGradient id="wheelGlow" cx="34%" cy="50%" r="34%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="segNutrition">
      <path d="M628 250 A245 245 0 0 1 628 470 L511 409 A112 112 0 0 0 511 311 Z"/>
    </clipPath>
    <clipPath id="segMovement">
      <path d="M613 497 A245 245 0 0 1 427 604 L418 472 A112 112 0 0 0 503 422 Z"/>
    </clipPath>
    <clipPath id="segMind">
      <path d="M393 604 A245 245 0 0 1 207 497 L317 422 A112 112 0 0 0 402 472 Z"/>
    </clipPath>
    <clipPath id="segRest">
      <path d="M190 467 A245 245 0 0 1 190 253 L309 311 A112 112 0 0 0 309 409 Z"/>
    </clipPath>
    <clipPath id="segHydration">
      <path d="M207 223 A245 245 0 0 1 393 116 L402 248 A112 112 0 0 0 317 298 Z"/>
    </clipPath>
    <clipPath id="segCommunity">
      <path d="M427 116 A245 245 0 0 1 613 223 L503 298 A112 112 0 0 0 418 248 Z"/>
    </clipPath>
  </defs>

  <image href="https://images.example.com/healthy-living/soft-morning-kitchen-background.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#wheelGlow)"/>

  <circle cx="410" cy="360" r="282" fill="#FFFFFF" opacity="0.10"/>
  <circle cx="410" cy="360" r="255" fill="none" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="1.5"/>

  <g id="wheel-stable-segments">
    <image href="https://images.example.com/healthy-living/morning-runner-park.jpg" x="160" y="110" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#segMovement)"/>
    <path d="M613 497 A245 245 0 0 1 427 604 L418 472 A112 112 0 0 0 503 422 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>

    <image href="https://images.example.com/healthy-living/calm-meditation-window.jpg" x="160" y="110" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#segMind)"/>
    <path d="M393 604 A245 245 0 0 1 207 497 L317 422 A112 112 0 0 0 402 472 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>

    <image href="https://images.example.com/healthy-living/cozy-bedroom-sleep.jpg" x="160" y="110" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#segRest)"/>
    <path d="M190 467 A245 245 0 0 1 190 253 L309 311 A112 112 0 0 0 309 409 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>

    <image href="https://images.example.com/healthy-living/water-glass-citrus.jpg" x="160" y="110" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#segHydration)"/>
    <path d="M207 223 A245 245 0 0 1 393 116 L402 248 A112 112 0 0 0 317 298 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>

    <image href="https://images.example.com/healthy-living/friends-cooking-together.jpg" x="160" y="110" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#segCommunity)"/>
    <path d="M427 116 A245 245 0 0 1 613 223 L503 298 A112 112 0 0 0 418 248 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
  </g>

  <g id="active-nutrition-segment" transform="translate(92 0)" filter="url(#softShadow)">
    <image href="https://images.example.com/healthy-living/colorful-market-vegetables.jpg" x="160" y="110" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#segNutrition)"/>
    <path d="M628 250 A245 245 0 0 1 628 470 L511 409 A112 112 0 0 0 511 311 Z" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>
  </g>

  <circle cx="410" cy="360" r="112" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="315" y="342" width="190" font-family="Georgia, 'Times New Roman', serif" font-size="30" font-weight="700" fill="#162033" text-anchor="middle">
    <tspan x="410">Healthy</tspan>
    <tspan x="410" dy="38">Living</tspan>
  </text>

  <rect x="745" y="132" width="410" height="456" rx="34" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <text x="792" y="198" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" letter-spacing="2.6" fill="#5D8B71">PILLAR 01</text>
  <text x="792" y="256" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="800" fill="#172033">Eat with intention</text>
  <text x="792" y="328" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" fill="#465163">
    <tspan x="792">Build meals around color, fiber,</tspan>
    <tspan x="792" dy="34">and steady energy — not strict</tspan>
    <tspan x="792" dy="34">rules. Small rituals make nutrition</tspan>
    <tspan x="792" dy="34">feel effortless and repeatable.</tspan>
  </text>
  <text x="792" y="504" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#7B8492">
    <tspan x="792">Morph setup: duplicate this slide, rotate the</tspan>
    <tspan x="792" dy="24">wheel group by 60°, and translate the next</tspan>
    <tspan x="792" dy="24">segment outward on the same radial axis.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the reveal; create separate slide states and let PowerPoint Morph animate them.
- ❌ `<mask>` for donut holes; use annular-sector clip paths on the images and a normal center circle on top.
- ❌ Applying `clip-path` to non-image segment overlays; draw duplicate visible `<path>` outlines instead.
- ❌ `<use href="#segment">` to reuse wedge paths; duplicate the path data for each visible outline because `<use>` hard-fails.
- ❌ Arrow markers or line filters for motion cues; if you need direction hints, use plain `<line>` arrows or small paths without markers.

## Composition notes
- Keep the wheel slightly left of center, around x=400, so the popped segment can move outward without colliding with the right-side content card.
- Use the full-bleed background as atmosphere only; darken it with a translucent gradient so the wheel and white content card remain dominant.
- Preserve identical segment IDs and geometry across slide states; change only `transform="rotate(... 410 360)"` on the wheel group and `translate(...)` on the active segment for clean Morph interpolation.
- The central hub should remain visually stable across slides, acting as the audience’s anchor while the photo segments rotate and reveal the current topic.