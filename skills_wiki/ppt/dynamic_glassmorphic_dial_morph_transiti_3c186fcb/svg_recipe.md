# SVG Recipe — Dynamic Glassmorphic Dial (Morph Transition)

## Visual mechanism
A scenic full-slide image is darkened by a right-weighted gradient overlay, then duplicate copies of the same image are clipped into circular “portals” so the dial appears to reveal the untouched background beneath. For Morph, duplicate the slide and rotate the entire dial group by 90° while keeping the same object structure, creating a premium rotating aperture/navigation effect.

## SVG primitives needed
- 1× full-canvas `<image>` for the scenic background.
- 1× full-canvas `<rect>` with `<linearGradient>` for the dark cinematic overlay.
- 4× clipped `<image>` elements for circular background-reveal portals.
- 4× `<clipPath>` definitions using `<circle>` for the large dial, center hub, and two satellite windows.
- 6× `<circle>` for portal rims, translucent glass surfaces, inner rings, and decorative dial geometry.
- 4× `<path>` for orbital arcs, luminous accent ticks, and curved mechanical dial details.
- 1× `<filter id="dialShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for floating depth.
- 1× `<filter id="softGlow">` using `feGaussianBlur` for blue glass highlights.
- Multiple `<text>` elements with explicit `width` for title, body copy, step number, and radial navigation labels.
- 1× `<linearGradient>` for the overlay, plus 2× additional gradients for glass edge and accent strokes.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkSweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#07111f" stop-opacity="0.05"/>
      <stop offset="45%" stop-color="#07111f" stop-opacity="0.46"/>
      <stop offset="100%" stop-color="#02050b" stop-opacity="0.88"/>
    </linearGradient>

    <linearGradient id="glassRim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.96"/>
      <stop offset="42%" stop-color="#bfe9ff" stop-opacity="0.52"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.28"/>
    </linearGradient>

    <linearGradient id="cyanStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7ce8ff" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#6d7cff" stop-opacity="0.35"/>
    </linearGradient>

    <filter id="dialShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="22" dy="12" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="14" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .58 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>

    <clipPath id="clipOuterDial">
      <circle cx="320" cy="360" r="250"/>
    </clipPath>
    <clipPath id="clipHub">
      <circle cx="320" cy="360" r="82"/>
    </clipPath>
    <clipPath id="clipTopPortal">
      <circle cx="320" cy="152" r="54"/>
    </clipPath>
    <clipPath id="clipRightPortal">
      <circle cx="528" cy="360" r="54"/>
    </clipPath>
  </defs>

  <image href="https://images.example.com/scenic-night-mountains-with-blue-city-lights.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#darkSweep)"/>

  <g id="morph-dial-assembly" transform="rotate(0 320 360)">
    <circle cx="320" cy="360" r="250" fill="#dff7ff" opacity="0.08" filter="url(#dialShadow)"/>
    <image href="https://images.example.com/scenic-night-mountains-with-blue-city-lights.jpg"
           x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipOuterDial)"/>
    <circle cx="320" cy="360" r="250" fill="none" stroke="url(#glassRim)" stroke-width="3.5"/>
    <circle cx="320" cy="360" r="216" fill="none" stroke="#ffffff" stroke-width="1.1" opacity="0.34"/>
    <circle cx="320" cy="360" r="168" fill="none" stroke="#8feaff" stroke-width="1.4" opacity="0.42" stroke-dasharray="10 16"/>

    <path d="M 320 94 A 266 266 0 0 1 586 360" fill="none" stroke="url(#cyanStroke)" stroke-width="9" opacity="0.68" stroke-linecap="round"/>
    <path d="M 92 360 A 228 228 0 0 1 320 132" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.56" stroke-linecap="round"/>
    <path d="M 382 594 A 246 246 0 0 1 99 426" fill="none" stroke="#7ce8ff" stroke-width="4" opacity="0.32" stroke-linecap="round"/>
    <path d="M 526 225 L 548 199 M 555 253 L 586 235 M 573 291 L 608 282" fill="none" stroke="#ffffff" stroke-width="2.2" opacity="0.66" stroke-linecap="round"/>

    <circle cx="320" cy="152" r="62" fill="#8feaff" opacity="0.14" filter="url(#softGlow)"/>
    <image href="https://images.example.com/scenic-night-mountains-with-blue-city-lights.jpg"
           x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipTopPortal)"/>
    <circle cx="320" cy="152" r="54" fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.92"/>

    <circle cx="528" cy="360" r="62" fill="#8feaff" opacity="0.12" filter="url(#softGlow)"/>
    <image href="https://images.example.com/scenic-night-mountains-with-blue-city-lights.jpg"
           x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipRightPortal)"/>
    <circle cx="528" cy="360" r="54" fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.92"/>

    <image href="https://images.example.com/scenic-night-mountains-with-blue-city-lights.jpg"
           x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipHub)"/>
    <circle cx="320" cy="360" r="82" fill="#ffffff" opacity="0.05"/>
    <circle cx="320" cy="360" r="82" fill="none" stroke="#ffffff" stroke-width="3"/>
    <text x="277" y="350" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">CHAPTER</text>
    <text x="320" y="390" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#ffffff" text-anchor="middle">01</text>

    <text x="286" y="72" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff" text-anchor="middle">DISCOVER</text>
    <text x="562" y="366" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff" transform="rotate(90 562 366)" text-anchor="middle">ALIGN</text>
    <text x="322" y="660" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff" transform="rotate(180 322 660)" text-anchor="middle">SCALE</text>
    <text x="76" y="366" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff" transform="rotate(-90 76 366)" text-anchor="middle">LAUNCH</text>
  </g>

  <g id="content-panel">
    <text x="720" y="194" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#7ce8ff" letter-spacing="3">MORPH NAVIGATION</text>
    <text x="720" y="263" width="455" font-family="Segoe UI, Microsoft YaHei" font-size="56" font-weight="700" fill="#ffffff">Introduction</text>
    <rect x="720" y="292" width="92" height="4" rx="2" fill="#7ce8ff" opacity="0.9"/>
    <text x="720" y="350" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#dbe8f6">
      <tspan x="720" dy="0">Turn a static agenda into a rotating glass</tspan>
      <tspan x="720" dy="34">aperture. Each Morph step advances the</tspan>
      <tspan x="720" dy="34">dial while the content pane updates with</tspan>
      <tspan x="720" dy="34">cinematic continuity.</tspan>
    </text>
    <text x="720" y="532" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9fb3c7">
      Duplicate this slide, keep the same dial objects, then set the group rotation to -90°, -180°, and -270° for subsequent sections.
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the rotation; create separate Morph slides in PowerPoint with the same editable objects instead.
- ❌ Do not use `<mask>` to punch holes through the overlay; use duplicated background images clipped with `<clipPath>` on `<image>` elements.
- ❌ Do not apply `clip-path` to circles or groups expecting PowerPoint to preserve it; clip only the duplicated background `<image>`.
- ❌ Do not use `<filter>` on `<line>` elements for glowing tick marks; use short `<path>` strokes or circles instead.
- ❌ Do not rely on real SVG backdrop blur for glassmorphism; PowerPoint translation will be more reliable with clipped background portals, translucent fills, rim strokes, and shadows.

## Composition notes
- Place the dial center around 25% of slide width and let it occupy 70–80% of slide height; the visual should feel partially mechanical and oversized.
- Keep the right half dark and calm for title/body text; the gradient overlay should be strongest behind the copy.
- Use the exact same background image for the full slide and every clipped portal so the circular windows align perfectly with the scenery.
- For Morph, preserve object hierarchy and positions, then rotate only the dial group between slides; update the highlighted radial label and right-side text per section.