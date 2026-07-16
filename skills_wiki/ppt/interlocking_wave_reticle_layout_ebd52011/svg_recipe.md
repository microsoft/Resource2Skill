# SVG Recipe — Interlocking Wave & Reticle Layout

## Visual mechanism
A continuous dark wavy channel cuts horizontally through three circular team portraits, while oversized colored rings sit behind the channel and the cropped photo discs sit in front. Small triangular reticles orbit each circle, making the portraits feel targeted, layered, and physically interlocked with the wave.

## SVG primitives needed
- 1× `<rect>` for the dark charcoal slide background
- 1× `<path>` for the recessed interlocking wave channel
- 2× `<path>` for subtle top/bottom wave edge shading to fake an inset groove
- 3× `<circle>` for thick accent rings placed behind the wave
- 3× `<circle>` for white portrait border discs placed above the wave
- 3× `<image>` clipped into circular portraits
- 3× `<clipPath>` with `<circle>` for avatar crops
- 6× `<path>` for triangular reticle pointers around the circular rings
- 1× `<filter id="waveShadow">` applied to the wave channel for soft depth
- 1× `<filter id="photoShadow">` applied to photo border circles for lift
- 1× `<linearGradient>` for the recessed wave fill
- Multiple `<text>` elements with explicit `width` for title, names, roles, and captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="waveFill" x1="0" y1="250" x2="0" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#8a8585"/>
      <stop offset="0.45" stop-color="#777272"/>
      <stop offset="1" stop-color="#696565"/>
    </linearGradient>

    <filter id="waveShadow" x="-5%" y="-25%" width="110%" height="150%">
      <feOffset dx="0" dy="-7" result="off1"/>
      <feGaussianBlur in="off1" stdDeviation="9" result="blur1"/>
      <feOffset dx="0" dy="7" result="off2"/>
      <feGaussianBlur in="off2" stdDeviation="7" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur1"/>
        <feMergeNode in="blur2"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="photoShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="7" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="avatarClip1"><circle cx="270" cy="355" r="148"/></clipPath>
    <clipPath id="avatarClip2"><circle cx="640" cy="355" r="148"/></clipPath>
    <clipPath id="avatarClip3"><circle cx="1010" cy="355" r="148"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#343131"/>

  <text x="640" y="92" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="70" font-weight="700" letter-spacing="6" fill="#ffffff">
    MY BUSINESS TEAM
  </text>

  <!-- Back layer: accent rings and reticles -->
  <circle cx="270" cy="355" r="157" fill="none" stroke="#efff00" stroke-width="17"/>
  <circle cx="640" cy="355" r="157" fill="none" stroke="#ff1010" stroke-width="17"/>
  <circle cx="1010" cy="355" r="157" fill="none" stroke="#ff3aae" stroke-width="17"/>

  <path d="M188 158 L205 209 L147 173 Z" fill="#efff00"/>
  <path d="M209 175 L190 218 L232 181 Z" fill="#efff00" opacity="0.95"/>
  <path d="M396 484 L437 519 L407 471 Z" fill="#efff00"/>
  <path d="M390 516 L418 509 L394 479 Z" fill="#efff00" opacity="0.95"/>

  <path d="M555 158 L569 209 L529 173 Z" fill="#ff1010"/>
  <path d="M576 176 L557 218 L596 182 Z" fill="#ff1010" opacity="0.95"/>
  <path d="M786 484 L828 518 L798 471 Z" fill="#ff1010"/>
  <path d="M780 515 L811 509 L787 480 Z" fill="#ff1010" opacity="0.95"/>

  <path d="M949 158 L963 209 L909 173 Z" fill="#ff3aae"/>
  <path d="M970 177 L951 218 L990 182 Z" fill="#ff3aae" opacity="0.95"/>
  <path d="M1180 484 L1221 518 L1192 471 Z" fill="#ff3aae"/>
  <path d="M1174 515 L1204 509 L1181 480 Z" fill="#ff3aae" opacity="0.95"/>

  <!-- Middle layer: wave channel covers the rear rings -->
  <path filter="url(#waveShadow)" fill="url(#waveFill)"
        d="M0 276
           C150 246 263 253 400 257
           C548 263 689 249 835 268
           C975 286 1115 297 1280 302
           L1280 446
           C1118 440 978 429 833 415
           C684 401 544 414 399 416
           C260 418 144 421 0 412
           Z"/>

  <path d="M0 276 C150 246 263 253 400 257 C548 263 689 249 835 268 C975 286 1115 297 1280 302"
        fill="none" stroke="#211f1f" stroke-width="10" opacity="0.42"/>
  <path d="M0 412 C260 418 144 421 399 416 C544 414 684 401 833 415 C978 429 1118 440 1280 446"
        fill="none" stroke="#9a9696" stroke-width="6" opacity="0.28"/>

  <!-- Front layer: circular portrait discs -->
  <circle cx="270" cy="355" r="153" fill="#ffffff" filter="url(#photoShadow)"/>
  <image href="https://images.example.com/team/business-leader-laptop-portrait.jpg"
         x="122" y="207" width="296" height="296"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#avatarClip1)"/>
  <circle cx="270" cy="355" r="149" fill="none" stroke="#ffffff" stroke-width="3"/>

  <circle cx="640" cy="355" r="153" fill="#ffffff" filter="url(#photoShadow)"/>
  <image href="https://images.example.com/team/consultant-at-desk-bright-office.jpg"
         x="492" y="207" width="296" height="296"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#avatarClip2)"/>
  <circle cx="640" cy="355" r="149" fill="none" stroke="#ffffff" stroke-width="3"/>

  <circle cx="1010" cy="355" r="153" fill="#ffffff" filter="url(#photoShadow)"/>
  <image href="https://images.example.com/team/outdoor-executive-coffee-portrait.jpg"
         x="862" y="207" width="296" height="296"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#avatarClip3)"/>
  <circle cx="1010" cy="355" r="149" fill="none" stroke="#ffffff" stroke-width="3"/>

  <!-- Text blocks -->
  <text x="270" y="574" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="800" fill="#efff00">
    <tspan x="270">TEAM MEMBER NAME</tspan>
    <tspan x="270" dy="27">DESIGNATION</tspan>
  </text>
  <text x="270" y="620" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#e5e0e0">
    <tspan x="270">Lorem ipsum dolor sit amet, consectetur</tspan>
    <tspan x="270" dy="19">adipiscing elit. Cras urna odio, dictum ac</tspan>
    <tspan x="270" dy="19">sem nec, elementum egestas purus.</tspan>
    <tspan x="270" dy="19">Pellentesque ac est a elit commodo cursus.</tspan>
  </text>

  <text x="640" y="574" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="800" fill="#ff1010">
    <tspan x="640">TEAM MEMBER NAME</tspan>
    <tspan x="640" dy="27">DESIGNATION</tspan>
  </text>
  <text x="640" y="620" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#e5e0e0">
    <tspan x="640">Lorem ipsum dolor sit amet, consectetur</tspan>
    <tspan x="640" dy="19">adipiscing elit. Cras urna odio, dictum ac</tspan>
    <tspan x="640" dy="19">sem nec, elementum egestas purus.</tspan>
    <tspan x="640" dy="19">Pellentesque ac est a elit commodo cursus.</tspan>
  </text>

  <text x="1010" y="574" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="800" fill="#ff3aae">
    <tspan x="1010">TEAM MEMBER NAME</tspan>
    <tspan x="1010" dy="27">DESIGNATION</tspan>
  </text>
  <text x="1010" y="620" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#e5e0e0">
    <tspan x="1010">Lorem ipsum dolor sit amet, consectetur</tspan>
    <tspan x="1010" dy="19">adipiscing elit. Cras urna odio, dictum ac</tspan>
    <tspan x="1010" dy="19">sem nec, elementum egestas purus.</tspan>
    <tspan x="1010" dy="19">Pellentesque ac est a elit commodo cursus.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not draw the wave first; the interlocking illusion depends on accent rings behind the wave and portraits above it.
- ❌ Do not apply `clip-path` to circles or groups; only clip the `<image>` elements for reliable PPT translation.
- ❌ Do not use `<mask>` for avatar crops or inner shadows; use circular clip paths and layered wave-edge strokes instead.
- ❌ Do not use `<use>` to repeat reticles or profile groups; duplicate the editable paths/shapes explicitly.
- ❌ Do not make the portrait photos rectangular with rounded corners; perfect circles are central to the reticle effect.

## Composition notes
- Keep the title in the top 15–18% of the slide and reserve the lower 20% for the three centered text blocks.
- Place the wave through the vertical midpoint of the portraits so it visibly interrupts the rear accent rings but disappears behind the photo discs.
- Use three high-saturation accent colors with equal visual weight; repeat each color in the ring, reticles, name, and designation.
- Leave generous dark negative space around the title and between team modules so the bright rings feel premium rather than crowded.