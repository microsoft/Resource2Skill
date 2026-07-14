# SVG Recipe — Trilobite Morphing Infographic

## Visual mechanism
A premium 3-step cyclical infographic built from three overlapping curved lobes arranged around a center point, resembling a trilobite or rotating yin-yang. The lobes sit on a dark executive-style stage with cyan inner glow, soft shadows, and a vertical image strip that can be shifted between slides to imply a Morph-driven narrative flow.

## SVG primitives needed
- 2× `<rect>` for the full-slide split background and base color fields
- 1× `<rect>` for the large rounded blue content card
- 1× `<rect>` for the dark right-side image panel
- 3× `<rect>` for shadow/backplate cards behind the vertical images
- 3× `<image>` clipped to rounded rectangles for the scrolling story imagery
- 3× `<clipPath>` with rounded `<rect>` for editable rounded photo crops
- 3× `<path>` for the rotated trilobite lobes
- 6× small `<circle>` / `<ellipse>` elements for icon details and center hub
- 8× `<line>` elements for simple editable icons and connector accents
- 5× `<text>` elements with explicit `width` for title, subtitle, and lobe labels
- 3× `<linearGradient>` / `<radialGradient>` definitions for background, card, and lobe fills
- 2× `<filter>` definitions using blur/offset/merge for card shadows and soft lobe depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgSplit" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#011638"/>
      <stop offset="58%" stop-color="#06214E"/>
      <stop offset="100%" stop-color="#1B75BB"/>
    </linearGradient>

    <linearGradient id="cardBlue" x1="70" y1="90" x2="850" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2489D6"/>
      <stop offset="48%" stop-color="#1768A9"/>
      <stop offset="100%" stop-color="#0B326E"/>
    </linearGradient>

    <radialGradient id="lobeFill" cx="42%" cy="38%" r="72%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="64%" stop-color="#FFFFFF"/>
      <stop offset="86%" stop-color="#DDF8FF"/>
      <stop offset="100%" stop-color="#7AD4F0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softLift" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoClip1"><rect x="905" y="60" width="275" height="175" rx="26"/></clipPath>
    <clipPath id="photoClip2"><rect x="905" y="263" width="275" height="175" rx="26"/></clipPath>
    <clipPath id="photoClip3"><rect x="905" y="466" width="275" height="175" rx="26"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#011638"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgSplit)"/>

  <rect x="70" y="88" width="785" height="545" rx="44" fill="url(#cardBlue)" filter="url(#cardShadow)"/>
  <rect x="880" y="42" width="330" height="636" rx="38" fill="#071832" filter="url(#cardShadow)"/>

  <text x="118" y="145" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="700" fill="#FFFFFF">
    CYCLICAL RESPONSE MODEL
  </text>
  <text x="120" y="184" width="485" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#BFEFFF" letter-spacing="1.2">
    THREE INTERLOCKED STAGES MOVING AS ONE SYSTEM
  </text>

  <g transform="translate(455 375)">
    <path d="M 0 -172 C 78 -174 144 -108 129 -31 C 119 22 75 44 36 58 C 7 69 -5 99 15 132 C -63 109 -120 47 -130 -31 C -140 -108 -80 -171 0 -172 Z"
          fill="url(#lobeFill)" stroke="#E9FCFF" stroke-width="3" filter="url(#softLift)"/>
    <path d="M 0 -172 C 78 -174 144 -108 129 -31 C 119 22 75 44 36 58 C 7 69 -5 99 15 132 C -63 109 -120 47 -130 -31 C -140 -108 -80 -171 0 -172 Z"
          transform="rotate(120)" fill="url(#lobeFill)" stroke="#E9FCFF" stroke-width="3" filter="url(#softLift)"/>
    <path d="M 0 -172 C 78 -174 144 -108 129 -31 C 119 22 75 44 36 58 C 7 69 -5 99 15 132 C -63 109 -120 47 -130 -31 C -140 -108 -80 -171 0 -172 Z"
          transform="rotate(240)" fill="url(#lobeFill)" stroke="#E9FCFF" stroke-width="3" filter="url(#softLift)"/>

    <circle cx="0" cy="0" r="42" fill="#FFFFFF" stroke="#7AD4F0" stroke-width="5"/>
    <circle cx="0" cy="0" r="14" fill="#111827"/>

    <circle cx="0" cy="-88" r="25" fill="none" stroke="#111827" stroke-width="6"/>
    <line x1="18" y1="-70" x2="43" y2="-45" stroke="#111827" stroke-width="6" stroke-linecap="round"/>
    <text x="-83" y="-20" width="166" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#111827">
      RESEARCH
    </text>

    <circle cx="94" cy="53" r="9" fill="#111827"/>
    <circle cx="142" cy="53" r="9" fill="#111827"/>
    <circle cx="118" cy="94" r="9" fill="#111827"/>
    <line x1="94" y1="53" x2="142" y2="53" stroke="#111827" stroke-width="5" stroke-linecap="round"/>
    <line x1="105" y1="65" x2="118" y2="94" stroke="#111827" stroke-width="5" stroke-linecap="round"/>
    <line x1="132" y1="65" x2="118" y2="94" stroke="#111827" stroke-width="5" stroke-linecap="round"/>
    <text x="62" y="139" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#111827">
      ANALYZE
    </text>

    <ellipse cx="-115" cy="66" rx="32" ry="22" fill="none" stroke="#111827" stroke-width="6"/>
    <line x1="-148" y1="66" x2="-82" y2="66" stroke="#111827" stroke-width="5" stroke-linecap="round"/>
    <line x1="-115" y1="38" x2="-115" y2="94" stroke="#111827" stroke-width="5" stroke-linecap="round"/>
    <text x="-190" y="139" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#111827">
      IMPACT
    </text>
  </g>

  <text x="120" y="590" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="19" fill="#E7F8FF">
    Rotate this trilobite group by 120° between slides, while shifting the image column upward by one card height to create the Morph storytelling effect.
  </text>

  <rect x="905" y="60" width="275" height="175" rx="26" fill="#000000" opacity="0.28" filter="url(#cardShadow)"/>
  <image x="905" y="60" width="275" height="175" clip-path="url(#photoClip1)"
         href="https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?w=900"/>
  <text x="927" y="214" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">SIGNAL DETECTION</text>

  <rect x="905" y="263" width="275" height="175" rx="26" fill="#000000" opacity="0.28" filter="url(#cardShadow)"/>
  <image x="905" y="263" width="275" height="175" clip-path="url(#photoClip2)"
         href="https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=900"/>
  <text x="927" y="417" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">CLINICAL ANALYSIS</text>

  <rect x="905" y="466" width="275" height="175" rx="26" fill="#000000" opacity="0.28" filter="url(#cardShadow)"/>
  <image x="905" y="466" width="275" height="175" clip-path="url(#photoClip3)"
         href="https://images.unsplash.com/photo-1576086213369-97a306d36557?w=900"/>
  <text x="927" y="620" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">MEASURABLE OUTCOMES</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the trilobite with `<use>` clones; repeat the three `<path>` elements directly and rotate each with `transform="rotate(...)"`.
- ❌ Do not rely on PowerPoint merge-shape operations; encode the lobe geometry as SVG `<path>` data.
- ❌ Do not apply `clip-path` to decorative rectangles or groups; use it only on the `<image>` elements for the photo crops.
- ❌ Do not use SVG masks for the inset glow; approximate the recessed look with radial gradients, strokes, and soft shadow filters.
- ❌ Do not use `marker-end` on curved paths for arrows; if directional arrows are needed, use explicit `<line>` elements with direct marker settings or draw arrowhead paths manually.

## Composition notes
- Keep the trilobite large and centered in the left card, occupying roughly 45–50% of slide width; it should feel like the main object, not a small chart.
- Reserve the right 25–30% of the slide for a vertical image strip; in a Morph sequence, shift this strip upward while rotating the trilobite by 120° per slide.
- Use a dark navy background with cyan-blue gradients to make the white lobes feel luminous and premium.
- Place explanatory copy low on the main card, leaving generous negative space around the rotating center shape.