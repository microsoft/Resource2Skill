# SVG Recipe — 3D Spotlight Podium Reveal

## Visual mechanism
A cinematic “hero stage” is built with a dark radial-gradient environment, blurred cone-shaped spotlights, and a layered oval/rectangle podium that fakes 3D cylinder depth. A magenta perspective ramp pulls the eye toward the center reveal object, making a metric, logo, award, or product announcement feel monumental.

## SVG primitives needed
- 1× `<rect>` full-slide background using a radial gradient for the stage glow
- 2× blurred `<path>` spotlight cones angled in from the upper corners
- 1× large `<ellipse>` floor shadow/glow under the stage
- 2× `<path>` trapezoids for the perspective ramp top and ramp extrusion
- 3× `<ellipse>` for podium base shadow, top surface, and front rim highlights
- 2× `<rect>` for the podium cylinder side wall and inner magenta face
- 4× `<path>` for side facets, rim accents, and decorative reveal badge
- 2× `<circle>` for the central reveal medallion and halo
- 3× `<text>` blocks with explicit `width` for title, metric, and label
- 1× `<filter id="softBlur">` for volumetric spotlights
- 1× `<filter id="stageShadow">` for heavy cinematic depth
- 1× `<filter id="glow">` for the reveal object halo
- Multiple `<linearGradient>` and `<radialGradient>` definitions for metallic rims, magenta stage material, and background lighting

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#B7E7F5"/>
      <stop offset="34%" stop-color="#31577E"/>
      <stop offset="100%" stop-color="#101B33"/>
    </radialGradient>

    <radialGradient id="floorGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45"/>
      <stop offset="38%" stop-color="#E20074" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="rampTop" x1="0" y1="355" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF4CB1"/>
      <stop offset="48%" stop-color="#E20074"/>
      <stop offset="100%" stop-color="#A60055"/>
    </linearGradient>

    <linearGradient id="rampSide" x1="0" y1="420" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#9B004F"/>
      <stop offset="100%" stop-color="#430026"/>
    </linearGradient>

    <linearGradient id="podiumSide" x1="0" y1="405" x2="0" y2="570" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="52%" stop-color="#D7DCE5"/>
      <stop offset="100%" stop-color="#9EA8B8"/>
    </linearGradient>

    <linearGradient id="podiumTop" x1="420" y1="360" x2="860" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="55%" stop-color="#F1F4F8"/>
      <stop offset="100%" stop-color="#C7CEDA"/>
    </linearGradient>

    <linearGradient id="magentaInset" x1="420" y1="370" x2="860" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF5ABA"/>
      <stop offset="50%" stop-color="#E20074"/>
      <stop offset="100%" stop-color="#8B0046"/>
    </linearGradient>

    <filter id="softBlur" x="-40%" y="-30%" width="180%" height="170%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <filter id="stageShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="0" dy="22"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <path d="M95,-80 L205,-80 L610,545 L390,545 Z" fill="#FFFFFF" opacity="0.22" filter="url(#softBlur)" transform="rotate(-12 120 0)"/>
  <path d="M1075,-80 L1185,-80 L890,545 L670,545 Z" fill="#FFFFFF" opacity="0.22" filter="url(#softBlur)" transform="rotate(12 1160 0)"/>

  <ellipse cx="640" cy="585" rx="475" ry="105" fill="url(#floorGlow)"/>
  <ellipse cx="640" cy="625" rx="420" ry="42" fill="#00081A" opacity="0.35"/>

  <path d="M595,420 L685,420 L1180,720 L100,720 Z" fill="url(#rampSide)" opacity="0.95"/>
  <path d="M604,389 L676,389 L1110,720 L170,720 Z" fill="url(#rampTop)"/>
  <path d="M604,389 L676,389 L712,417 L568,417 Z" fill="#FF7CC8" opacity="0.42"/>

  <g filter="url(#stageShadow)">
    <ellipse cx="640" cy="540" rx="320" ry="62" fill="#070B18" opacity="0.42"/>
    <rect x="365" y="398" width="550" height="120" fill="url(#podiumSide)"/>
    <path d="M365,398 C410,455 870,455 915,398 L915,518 C870,582 410,582 365,518 Z" fill="url(#podiumSide)"/>
    <ellipse cx="640" cy="398" rx="275" ry="76" fill="url(#podiumTop)"/>
    <ellipse cx="640" cy="397" rx="220" ry="50" fill="url(#magentaInset)"/>
    <path d="M367,505 C430,566 850,566 913,505 L913,535 C845,607 435,607 367,535 Z" fill="#E8ECF2"/>
    <ellipse cx="640" cy="510" rx="276" ry="61" fill="none" stroke="#FFFFFF" stroke-width="10" opacity="0.9"/>
  </g>

  <circle cx="640" cy="355" r="92" fill="#FFFFFF" opacity="0.35" filter="url(#glow)"/>
  <circle cx="640" cy="355" r="76" fill="#F8FBFF" stroke="#FFFFFF" stroke-width="6"/>
  <path d="M640,298 L656,334 L695,338 L666,363 L675,402 L640,381 L605,402 L614,363 L585,338 L624,334 Z" fill="#E20074"/>
  <path d="M620,438 C636,449 662,449 678,438" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="0.75"/>

  <text x="640" y="86" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF" letter-spacing="2">
    MARKET LEADER REVEAL
  </text>

  <text x="640" y="365" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#121A2B">
    #1
  </text>

  <text x="640" y="655" width="720" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="600" fill="#FFFFFF">
    <tspan fill="#FF7CC8">42%</tspan><tspan> growth powered by the new AI platform</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using flat rectangles only; the illusion depends on stacked ellipses, trapezoids, shadows, and gradients.
- ❌ Applying `filter` to `<line>` elements for light rays; use blurred filled `<path>` cones instead.
- ❌ Using `<mask>` for spotlight fading; use low-opacity paths plus `feGaussianBlur`.
- ❌ Cropping non-image podium parts with `clip-path`; build editable geometric layers directly.
- ❌ Overloading the center with chart axes or gridlines; this is a reveal stage, not a literal data plot.

## Composition notes
- Keep the podium centered horizontally and anchored in the lower-middle third; the top surface should sit around y=390–430 on a 1280×720 canvas.
- Use the ramp as a visual funnel: narrow near the podium, very wide at the bottom edge for aggressive perspective.
- Reserve the upper third for a short reveal headline; avoid dense paragraphs that compete with the spotlight beams.
- Maintain a strong color rhythm: deep blue environment, white metallic podium, magenta ramp/accent, and a high-contrast central badge.