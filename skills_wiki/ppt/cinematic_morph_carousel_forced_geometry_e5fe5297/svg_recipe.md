# SVG Recipe — Cinematic Morph Carousel & Forced Geometry Metamorphosis

## Visual mechanism
Build two or more slides as “keyframes” of one oversized cinematic canvas: the hero image, title, carousel cards, and abstract geometry keep the same object identities while changing position, scale, and shape between slides. PowerPoint Morph then interpolates the spatial movement, and a forced `!!` name lets a circle on one slide become a triangle, blob, or badge on the next.

## SVG primitives needed
- 1× `<linearGradient>` for the warm cinematic sand-to-gold background
- 1× `<radialGradient>` for a soft spotlight behind the active hero area
- 2× `<filter>` definitions for elevated photo-card shadows and glowing geometry
- 2× `<clipPath>` definitions for rounded hero/photo crops
- 3× `<image>` elements for carousel photo cards: previous, active, and next state
- 6× `<rect>` elements for background overlays, cards, UI rails, and text panels
- 2× `<path>` elements for forced-morph geometry and organic cinematic accent shapes
- 3× `<circle>` elements for carousel pagination dots and glow anchors
- 2× `<line>` elements for motion guide accents; use plain lines, not marker arrows
- 6× `<text>` elements with explicit `width` for title, labels, body copy, and morph notes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgSand" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FAD7A1"/>
      <stop offset="48%" stop-color="#F4D03F"/>
      <stop offset="100%" stop-color="#B9770E"/>
    </linearGradient>

    <radialGradient id="spotlight" cx="42%" cy="44%" r="62%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.46"/>
      <stop offset="55%" stop-color="#FFD86B" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#8A4F00" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="geoGlow" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>

    <clipPath id="heroRounded">
      <rect x="168" y="196" width="480" height="338" rx="34"/>
    </clipPath>

    <clipPath id="sideRounded">
      <rect x="0" y="0" width="230" height="160" rx="22"/>
    </clipPath>
  </defs>

  <rect id="BackgroundPlate" x="0" y="0" width="1280" height="720" fill="url(#bgSand)"/>
  <rect id="VignetteOverlay" x="0" y="0" width="1280" height="720" fill="url(#spotlight)"/>

  <text id="MainTitle" x="40" y="122" width="1200"
        font-family="Segoe UI, Microsoft YaHei" font-size="88" font-weight="800"
        letter-spacing="8" fill="#FFFFFF" opacity="0.62">TAJ MAHAL</text>

  <path id="CinematicSweep" d="M-80,620 C210,520 350,650 590,560 C820,475 880,270 1370,280 L1370,720 L-80,720 Z"
        fill="#FFFFFF" opacity="0.16"/>

  <circle id="!!GeoMorphGlow" cx="585" cy="238" r="92" fill="#FFFFFF" opacity="0.22" filter="url(#geoGlow)"/>
  <path id="!!GeoMorph" d="M586 132 L690 315 L474 315 Z"
        fill="#FFFFFF" opacity="0.88" filter="url(#geoGlow)"/>
  <text id="MorphLabel" x="480" y="356" width="260"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        fill="#5C3700" text-anchor="middle">same name: !!GeoMorph</text>

  <g id="CarouselGroup">
    <g id="PreviousCard" transform="translate(55 270) scale(0.82)">
      <rect x="0" y="0" width="230" height="160" rx="22" fill="#FFFFFF" opacity="0.30"/>
      <image href="https://images.example.com/mughal-garden-previous-card.jpg"
             x="0" y="0" width="230" height="160" preserveAspectRatio="xMidYMid slice"
             clip-path="url(#sideRounded)" opacity="0.72"/>
    </g>

    <rect id="HeroCardShell" x="154" y="182" width="508" height="366" rx="42"
          fill="#FFFFFF" opacity="0.34" filter="url(#cardShadow)"/>
    <image id="HeroImage" href="https://images.example.com/taj-mahal-sunrise-hero-photo.jpg"
           x="168" y="196" width="480" height="338" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#heroRounded)"/>

    <g id="NextCard" transform="translate(610 292) scale(0.72)">
      <rect x="0" y="0" width="230" height="160" rx="22" fill="#FFFFFF" opacity="0.26"/>
      <image href="https://images.example.com/marble-arches-next-card.jpg"
             x="0" y="0" width="230" height="160" preserveAspectRatio="xMidYMid slice"
             clip-path="url(#sideRounded)" opacity="0.62"/>
    </g>
  </g>

  <rect id="CopyPanel" x="760" y="170" width="410" height="390" rx="34"
        fill="#FFFFFF" opacity="0.70" filter="url(#cardShadow)"/>
  <text id="SectionKicker" x="805" y="225" width="330"
        font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800"
        letter-spacing="3" fill="#A06000">MORPH KEYFRAME 02</text>
  <text id="DetailHeadline" x="805" y="286" width="345"
        font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800"
        fill="#3F2A00">Geometry becomes narrative motion.</text>
  <text id="BodyCopy" x="808" y="348" width="320"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#5A430E">
    The hero image scales from a centered monument into a left-side carousel card. A circle from the opener is renamed with the same !! identity and resolves here as a glowing triangle.
  </text>

  <line id="MotionRailA" x1="212" y1="604" x2="630" y2="604" stroke="#FFFFFF" stroke-width="3" opacity="0.62"/>
  <line id="MotionRailB" x1="650" y1="604" x2="892" y2="604" stroke="#5C3700" stroke-width="3" opacity="0.28" stroke-dasharray="10 12"/>
  <circle id="DotPrev" cx="578" cy="604" r="7" fill="#FFFFFF" opacity="0.48"/>
  <circle id="DotActive" cx="628" cy="604" r="10" fill="#FFFFFF"/>
  <circle id="DotNext" cx="678" cy="604" r="7" fill="#FFFFFF" opacity="0.48"/>

  <text id="BuildNote" x="72" y="672" width="760"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#FFFFFF" opacity="0.86">
    Duplicate this slide as adjacent Morph states; keep ids stable, then move/scale elements. Change only the forced geometry path while preserving the !!GeoMorph identity.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; PowerPoint Morph, not SVG animation, creates the motion.
- ❌ Do not use `<use>` or `<symbol>` for repeated carousel cards; duplicate real editable shapes/images so Morph can track them.
- ❌ Do not rely on `marker-end` arrowheads for motion paths; use plain `<line>` accents or small editable paths instead.
- ❌ Do not apply `clip-path` to shapes or groups; only apply it to `<image>` crops for reliable editable PPT output.
- ❌ Do not change object identities between Morph slides unless you intentionally want an object to fade instead of interpolate.

## Composition notes
- Treat each slide as a camera crop of a larger continuous canvas: Slide 1 can be centered and monumental, while Slide 2 shifts the hero image left and opens a copy panel on the right.
- Keep the same `id` values across adjacent SVG slides for objects that should Morph; for forced geometry, use an explicit `!!` identity such as `!!GeoMorph` on both the source circle and destination triangle/path.
- Use warm gradients, soft glow, and large translucent typography to make the movement feel cinematic rather than like a UI carousel.
- Leave generous negative space around the destination copy panel so the audience notices both the spatial image move and the geometry metamorphosis.