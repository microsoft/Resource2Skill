# SVG Recipe — Cinematic Orbital Quote Reveal

## Visual mechanism
A dark cinematic background is dimmed into a high-contrast stage, then a bold uppercase quote is locked in the exact center and framed by glowing, incomplete orbital arcs. The arcs use gradient-faded strokes and slight rotational offsets to imply ambient motion and a premium sci-fi HUD reveal without relying on SVG animation.

## SVG primitives needed
- 1× `<image>` for the full-slide moody space / lunar / night-sky background
- 2× full-canvas `<rect>` overlays for darkening and subtle blue-violet cinematic grading
- 4× `<path>` circular arc strokes for the orbital quote frame
- 2× `<linearGradient>` definitions for fading arc strokes
- 1× `<radialGradient>` definition for center emphasis / vignette color wash
- 1× `<filter id="orbGlow">` applied to arc paths for soft glow
- 1× `<filter id="textShadow">` applied to main quote text for cinematic depth
- 1× `<line>` for the thin accent divider
- 3× `<text>` blocks for oversized quotation marks, the quote, and author attribution
- Optional small `<circle>` particles for subtle star / dust texture

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="arcWhiteFadeA" x1="350" y1="120" x2="930" y2="600" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="38%" stop-color="#FFFFFF" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.02"/>
    </linearGradient>

    <linearGradient id="arcWhiteFadeB" x1="940" y1="110" x2="340" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF5A2F" stop-opacity="0"/>
      <stop offset="42%" stop-color="#FFFFFF" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#78A7FF" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="cinematicWash" cx="50%" cy="50%" r="68%">
      <stop offset="0%" stop-color="#1E4C8F" stop-opacity="0.24"/>
      <stop offset="45%" stop-color="#090D19" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.92"/>
    </radialGradient>

    <filter id="orbGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/cinematic-dark-moon-surface-deep-space-background.jpg"
         preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.68"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#cinematicWash)"/>

  <circle cx="190" cy="118" r="1.4" fill="#FFFFFF" opacity="0.38"/>
  <circle cx="1045" cy="172" r="1.2" fill="#FFFFFF" opacity="0.32"/>
  <circle cx="1112" cy="536" r="1.6" fill="#FFFFFF" opacity="0.26"/>
  <circle cx="256" cy="592" r="1.1" fill="#FFFFFF" opacity="0.28"/>
  <circle cx="829" cy="96" r="1.3" fill="#FFFFFF" opacity="0.30"/>

  <!-- Orbital frame: duplicate incomplete rings at slightly different radii and rotations -->
  <g transform="rotate(-14 640 360)">
    <path d="M 640 102 A 258 258 0 0 1 898 360"
          fill="none" stroke="url(#arcWhiteFadeA)" stroke-width="5"
          stroke-linecap="round" filter="url(#orbGlow)" opacity="0.95"/>
    <path d="M 640 618 A 258 258 0 0 1 382 360"
          fill="none" stroke="url(#arcWhiteFadeA)" stroke-width="5"
          stroke-linecap="round" filter="url(#orbGlow)" opacity="0.82"/>
  </g>

  <g transform="rotate(28 640 360)">
    <path d="M 397 246 A 270 270 0 0 1 883 246"
          fill="none" stroke="url(#arcWhiteFadeB)" stroke-width="3.2"
          stroke-linecap="round" filter="url(#orbGlow)" opacity="0.72"/>
    <path d="M 883 474 A 270 270 0 0 1 397 474"
          fill="none" stroke="url(#arcWhiteFadeB)" stroke-width="3.2"
          stroke-linecap="round" filter="url(#orbGlow)" opacity="0.58"/>
  </g>

  <text x="640" y="300" width="780" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="148" font-weight="900" fill="#FFFFFF"
        opacity="0.16" filter="url(#textShadow)">“</text>

  <text x="640" y="326" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="45" font-weight="900" letter-spacing="1.5"
        fill="#FFFFFF" filter="url(#textShadow)">
    <tspan x="640" dy="0">ONE SMALL STEP FOR A MAN,</tspan>
    <tspan x="640" dy="58">A GIANT LEAP FOR MANKIND.</tspan>
  </text>

  <line x1="560" y1="448" x2="720" y2="448"
        stroke="#FF4A22" stroke-width="3.5" stroke-linecap="round"/>

  <text x="640" y="494" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600" letter-spacing="5"
        fill="#B9C0CB">NEIL ARMSTRONG</text>

  <text x="640" y="560" width="780" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="400" letter-spacing="2.8"
        fill="#8C93A1" opacity="0.72">VISION · COURAGE · FORWARD MOMENTUM</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for orbital rotation; they hard-fail translation. Use static rotated arc groups, then add PowerPoint rotation animation later if needed.
- ❌ `<mask>` for fading arcs; use gradient strokes instead.
- ❌ `clip-path` on the arc paths or overlay rectangles; clipping only translates reliably on `<image>`.
- ❌ `marker-end` arrowheads for orbital accents; the effect should be rings/arcs, not arrows.
- ❌ Thin low-contrast typography; the quote must remain crisp above the atmospheric background.

## Composition notes
- Keep the quote block centered inside a circular visual safe zone about 480–560 px wide; the arcs should frame, not touch, the text.
- Use 60–70% black overlay on the background image so the white quote has keynote-level readability.
- Let the orbital arcs occupy the middle 60% of slide height, leaving the corners dark and quiet.
- Use one warm accent, usually orange-red, only for the divider or a single arc highlight to prevent the HUD look from becoming cluttered.