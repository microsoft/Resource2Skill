# SVG Recipe — 3D Folded Fading Ribbon Agenda

## Visual mechanism
A vertical photo spine anchors the slide while agenda items unfold from its edge as long horizontal ribbons. Each ribbon uses a saturated-to-transparent gradient plus a small dark triangular fold under its left edge, creating a 3D wrapped-paper effect that fades into open negative space.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 1× `<image>` for the tall left-side architectural/photo anchor
- 1× `<rect>` overlay for darkening the image so the vertical title remains readable
- 1× `<text>` rotated vertically for the large spine title
- 5× `<path>` for fading chevron ribbon bodies
- 5× `<path>` for dark triangular fold shadows under the ribbon origins
- 5× `<circle>` for numbered agenda nodes straddling the image edge
- 5× `<text>` for agenda numbers inside the circles
- 5× `<text>` with nested `<tspan>` for agenda item title and subtitle copy
- 5× `<linearGradient>` for ribbon fills that fade from opaque color to transparent
- 1× `<filter id="circleShadow">` applied to numbered circles
- 1× `<filter id="softShadow">` applied to ribbon fold triangles for subtle depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="spineClip">
      <rect x="0" y="0" width="350" height="720"/>
    </clipPath>

    <linearGradient id="ribbonPurple" x1="305" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#673AB7" stop-opacity="0.94"/>
      <stop offset="45%" stop-color="#673AB7" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#673AB7" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ribbonBlue" x1="305" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#3F51B5" stop-opacity="0.94"/>
      <stop offset="45%" stop-color="#3F51B5" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#3F51B5" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ribbonTeal" x1="305" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#009688" stop-opacity="0.94"/>
      <stop offset="45%" stop-color="#009688" stop-opacity="0.23"/>
      <stop offset="100%" stop-color="#009688" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ribbonRed" x1="305" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F44336" stop-opacity="0.92"/>
      <stop offset="45%" stop-color="#F44336" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#F44336" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ribbonOrange" x1="305" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF9800" stop-opacity="0.92"/>
      <stop offset="45%" stop-color="#FF9800" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#FF9800" stop-opacity="0"/>
    </linearGradient>

    <filter id="circleShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F5F5"/>

  <image x="0" y="0" width="350" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#spineClip)"
         href="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&amp;w=1000"/>
  <rect x="0" y="0" width="350" height="720" fill="#101820" opacity="0.48"/>

  <text x="-610" y="112" width="560" transform="rotate(-90)" font-family="Segoe UI, Microsoft YaHei" font-size="64" font-weight="800" letter-spacing="5" fill="#FFFFFF" opacity="0.94">AGENDA</text>
  <text x="42" y="672" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" letter-spacing="2" fill="#FFFFFF" opacity="0.7">STRATEGY SUMMIT 2026</text>

  <path d="M305 86 L1085 86 L1140 116 L1085 146 L305 146 L345 116 Z" fill="url(#ribbonPurple)"/>
  <path d="M305 146 L350 146 L350 174 Z" fill="#2E1555" opacity="0.78" filter="url(#softShadow)"/>
  <circle cx="350" cy="116" r="34" fill="#673AB7" filter="url(#circleShadow)"/>
  <text x="328" y="127" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" text-anchor="middle" fill="#FFFFFF">01</text>
  <text x="425" y="110" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="29" font-weight="800" fill="#673AB7">
    Market context<tspan x="425" dy="31" font-size="16" font-weight="500" fill="#6F7682">Signals, customer shifts, and competitive pressure points</tspan>
  </text>

  <path d="M305 195 L1085 195 L1140 225 L1085 255 L305 255 L345 225 Z" fill="url(#ribbonBlue)"/>
  <path d="M305 255 L350 255 L350 283 Z" fill="#1D275A" opacity="0.78" filter="url(#softShadow)"/>
  <circle cx="350" cy="225" r="34" fill="#3F51B5" filter="url(#circleShadow)"/>
  <text x="328" y="236" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" text-anchor="middle" fill="#FFFFFF">02</text>
  <text x="425" y="219" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="29" font-weight="800" fill="#3F51B5">
    Growth priorities<tspan x="425" dy="31" font-size="16" font-weight="500" fill="#6F7682">Where we focus capital, leadership attention, and talent</tspan>
  </text>

  <path d="M305 304 L1085 304 L1140 334 L1085 364 L305 364 L345 334 Z" fill="url(#ribbonTeal)"/>
  <path d="M305 364 L350 364 L350 392 Z" fill="#004B45" opacity="0.78" filter="url(#softShadow)"/>
  <circle cx="350" cy="334" r="34" fill="#009688" filter="url(#circleShadow)"/>
  <text x="328" y="345" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" text-anchor="middle" fill="#FFFFFF">03</text>
  <text x="425" y="328" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="29" font-weight="800" fill="#009688">
    Operating model<tspan x="425" dy="31" font-size="16" font-weight="500" fill="#6F7682">Decision rhythm, ownership lines, and delivery governance</tspan>
  </text>

  <path d="M305 413 L1085 413 L1140 443 L1085 473 L305 473 L345 443 Z" fill="url(#ribbonRed)"/>
  <path d="M305 473 L350 473 L350 501 Z" fill="#782019" opacity="0.78" filter="url(#softShadow)"/>
  <circle cx="350" cy="443" r="34" fill="#F44336" filter="url(#circleShadow)"/>
  <text x="328" y="454" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" text-anchor="middle" fill="#FFFFFF">04</text>
  <text x="425" y="437" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="29" font-weight="800" fill="#F44336">
    Risk &amp; resilience<tspan x="425" dy="31" font-size="16" font-weight="500" fill="#6F7682">Critical dependencies, mitigations, and escalation triggers</tspan>
  </text>

  <path d="M305 522 L1085 522 L1140 552 L1085 582 L305 582 L345 552 Z" fill="url(#ribbonOrange)"/>
  <path d="M305 582 L350 582 L350 610 Z" fill="#7E4A00" opacity="0.78" filter="url(#softShadow)"/>
  <circle cx="350" cy="552" r="34" fill="#FF9800" filter="url(#circleShadow)"/>
  <text x="328" y="563" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" text-anchor="middle" fill="#FFFFFF">05</text>
  <text x="425" y="546" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="29" font-weight="800" fill="#FF9800">
    Decisions &amp; next steps<tspan x="425" dy="31" font-size="16" font-weight="500" fill="#6F7682">Required executive choices and the 30-day activation plan</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to darken or fade the photo; use a simple translucent `<rect>` overlay instead.
- ❌ Do not clip the ribbon paths; gradient transparency should create the fade, not a mask or non-image clip.
- ❌ Do not apply filters to `<line>` elements; use filtered `<circle>` and `<path>` elements for shadows.
- ❌ Do not build repeated ribbons with `<use>` or `<symbol>`; duplicate the editable paths directly.
- ❌ Do not rely on `marker-end` for the chevron tips; draw each ribbon as a full editable `<path>`.

## Composition notes
- Keep the image spine at roughly 25–30% of slide width; the agenda circles should sit directly on its right edge to visually stitch image and content together.
- Place ribbons in evenly spaced horizontal bands, leaving generous negative space on the far right for the gradient fade to dissolve.
- Use saturated item colors only near the spine and circles; let opacity fade quickly so body copy stays readable.
- The fold triangles should sit beneath the ribbon origins, slightly darker than the main color, to imply the ribbon wraps around the image edge.