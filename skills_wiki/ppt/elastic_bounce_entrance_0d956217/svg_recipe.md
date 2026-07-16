# SVG Recipe — Elastic Bounce Entrance

## Visual mechanism
A static SVG cannot contain PowerPoint entrance animation, so represent the elastic bounce as a polished “motion blueprint”: ghosted positions, overshoot markers, and a final emphasized object. After PPT conversion, apply a PowerPoint **Fly In** entrance with **Bounce End** to the final object or group.

## SVG primitives needed
- 1× `<rect>` for the dark keynote-style background
- 2× `<radialGradient>` / `<linearGradient>` fills for ambient depth and the animated object
- 2× `<filter>` definitions for glow and drop shadow on editable shapes
- 1× `<circle>` for the final entering object
- 5× translucent `<circle>` elements for motion ghosts and overshoot/settle positions
- 3× `<path>` elements for elastic motion curves and spring-like bounce trace
- 1× `<line>` for the vertical entrance axis
- 1× `<path>` arrowhead triangle for the entrance direction cue
- 4× `<rect>` elements for labels, setting cards, and timing chips
- 7× `<text>` elements with explicit `width` attributes for title, labels, and animation settings
- 3× small `<circle>` elements for timing dots / bounce keyframes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="55%" cy="38%" r="70%">
      <stop offset="0%" stop-color="#2A1A14"/>
      <stop offset="42%" stop-color="#121212"/>
      <stop offset="100%" stop-color="#050505"/>
    </radialGradient>

    <linearGradient id="orbFill" x1="365" y1="195" x2="590" y2="505" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFB15E"/>
      <stop offset="45%" stop-color="#FF5722"/>
      <stop offset="100%" stop-color="#B92C12"/>
    </linearGradient>

    <linearGradient id="cardFill" x1="780" y1="160" x2="1110" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#272727"/>
      <stop offset="100%" stop-color="#111111"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="orangeGlow" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <text x="80" y="86" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF">
    Elastic Bounce Entrance
  </text>
  <text x="82" y="126" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#B8B8B8">
    Fly in, overshoot, recoil, and settle — a premium motion cue for new content.
  </text>

  <line x1="448" y1="118" x2="448" y2="560" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="2" stroke-dasharray="10 12"/>
  <path d="M448 98 L434 124 L462 124 Z" fill="#FFFFFF" opacity="0.28"/>

  <path d="M448 100 C448 190 448 260 448 336 C448 390 448 420 448 448"
        fill="none" stroke="#FF7A3C" stroke-width="6" stroke-linecap="round" opacity="0.22"/>

  <path d="M448 444
           C448 492 508 496 508 458
           C508 428 388 428 388 458
           C388 482 486 482 486 458
           C486 442 416 442 416 458
           C416 470 462 470 462 458"
        fill="none" stroke="#FFB15E" stroke-width="4" stroke-linecap="round" opacity="0.85"/>

  <circle cx="448" cy="132" r="38" fill="#FF5722" opacity="0.08"/>
  <circle cx="448" cy="218" r="48" fill="#FF5722" opacity="0.14"/>
  <circle cx="448" cy="312" r="58" fill="#FF5722" opacity="0.22"/>
  <circle cx="448" cy="506" r="70" fill="#FF5722" opacity="0.18"/>
  <circle cx="448" cy="414" r="62" fill="#FF5722" opacity="0.28"/>

  <ellipse cx="448" cy="534" rx="108" ry="22" fill="#000000" opacity="0.45" filter="url(#softShadow)"/>
  <circle cx="448" cy="448" r="86" fill="url(#orbFill)" filter="url(#orangeGlow)"/>
  <circle cx="414" cy="410" r="24" fill="#FFFFFF" opacity="0.18"/>
  <path d="M387 448 C420 386 502 382 536 448 C507 507 419 513 387 448 Z"
        fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.16"/>

  <rect x="323" y="585" width="250" height="42" rx="21" fill="#FFFFFF" opacity="0.08"/>
  <text x="352" y="612" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#FFFFFF">
    Final resting position
  </text>

  <rect x="770" y="160" width="370" height="400" rx="32" fill="url(#cardFill)" stroke="#FFFFFF" stroke-opacity="0.10" filter="url(#softShadow)"/>
  <text x="818" y="218" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">
    Animation setup
  </text>

  <rect x="818" y="255" width="276" height="56" rx="18" fill="#FF5722" opacity="0.16" stroke="#FF8A50" stroke-opacity="0.55"/>
  <text x="842" y="291" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="650" fill="#FFFFFF">
    Entrance: Fly In from Top
  </text>

  <rect x="818" y="333" width="276" height="56" rx="18" fill="#FFFFFF" opacity="0.07" stroke="#FFFFFF" stroke-opacity="0.15"/>
  <text x="842" y="369" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#EDEDED">
    Duration: 0.75 seconds
  </text>

  <rect x="818" y="411" width="276" height="56" rx="18" fill="#FFFFFF" opacity="0.07" stroke="#FFFFFF" stroke-opacity="0.15"/>
  <text x="842" y="447" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#EDEDED">
    Bounce End: 0.50 seconds
  </text>

  <path d="M832 514 C878 482 910 482 952 514 C992 546 1032 546 1080 514"
        fill="none" stroke="#FFB15E" stroke-width="4" stroke-linecap="round"/>
  <circle cx="832" cy="514" r="7" fill="#FF5722"/>
  <circle cx="952" cy="514" r="7" fill="#FFB15E"/>
  <circle cx="1080" cy="514" r="7" fill="#FFFFFF" opacity="0.9"/>

  <text x="80" y="665" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#8F8F8F">
    Build this as editable SVG artwork, then apply the actual PowerPoint animation to the final orange object/group after import.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; they hard-fail and will not become PowerPoint animations.
- ❌ Do not use `<textPath>` for curved motion labels; use normal `<text>` plus separate editable paths.
- ❌ Do not use masks or clipping on shapes to fake motion blur; clip paths are only reliable on `<image>`.
- ❌ Do not put `filter` on `<line>` elements; use filtered circles/paths for glow and leave guide lines unfiltered.
- ❌ Do not rely on SVG alone to create the live bounce; the actual motion must be added in PowerPoint as Fly In + Bounce End.

## Composition notes
- Keep the final animated object large and central-left, with ghost positions showing the inbound path and overshoot amplitude.
- Reserve the right third of the slide for concise animation settings so the technique is self-documenting.
- Use a high-contrast dark background with a warm accent object; the orange glow makes the entrance target feel energetic.
- For real deck use, delete or hide the instructional ghost trail once the PowerPoint animation is applied, unless presenting the animation concept itself.