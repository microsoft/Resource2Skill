# SVG Recipe — Morphing Spinning Carousel Wheel

## Visual mechanism
A massive image wheel sits partially off-canvas, divided into four photographic quadrants with clean cross-shaped gaps. Across slides, keep the same wheel group and rotate it in 90° increments so PowerPoint Morph creates the illusion of a spinning carousel that reveals the next story segment.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep navy background
- 2× `<circle>` for oversized radial glow and subtle wheel halo
- 4× `<clipPath>` with `<path>` wedges to crop each photo into a separated quadrant
- 4× `<image>` for quadrant photography, each clipped by its own wedge path
- 4× `<path>` for thin white quadrant rim arcs / separators
- 1× `<filter id="softShadow">` applied to the wheel halo for depth
- 1× `<radialGradient>` for the background bloom
- 1× `<linearGradient>` for the right-side text accent bar
- 5× `<text>` blocks for headline, subtitle, body, section number, and micro-label
- 1× `<line>` for a minimal editorial divider

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="30%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#1d3c72"/>
      <stop offset="45%" stop-color="#122341"/>
      <stop offset="100%" stop-color="#090f1e"/>
    </radialGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#7dd3fc"/>
      <stop offset="55%" stop-color="#a78bfa"/>
      <stop offset="100%" stop-color="#f97316"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="18" dy="26"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Wheel center: 300,360. Radius: 560. Gap: 44. -->
    <clipPath id="clipQ1" clipPathUnits="userSpaceOnUse">
      <path d="M344 316 L344 -200 A560 560 0 0 1 860 316 Z"/>
    </clipPath>
    <clipPath id="clipQ2" clipPathUnits="userSpaceOnUse">
      <path d="M344 404 L860 404 A560 560 0 0 1 344 920 Z"/>
    </clipPath>
    <clipPath id="clipQ3" clipPathUnits="userSpaceOnUse">
      <path d="M256 404 L256 920 A560 560 0 0 1 -260 404 Z"/>
    </clipPath>
    <clipPath id="clipQ4" clipPathUnits="userSpaceOnUse">
      <path d="M256 316 L-260 316 A560 560 0 0 1 256 -200 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <circle cx="300" cy="360" r="594" fill="#06101f" opacity="0.36" filter="url(#softShadow)"/>
  <circle cx="300" cy="360" r="565" fill="none" stroke="#ffffff" stroke-opacity="0.12" stroke-width="2"/>

  <!-- Copy this entire group to later slides and rotate it by 90, 180, 270 degrees around 300,360 for Morph. -->
  <g id="carousel-wheel-state-0" transform="rotate(0 300 360)">
    <image x="-260" y="-200" width="1120" height="1120"
      href="https://images.unsplash.com/photo-1574512995535-6126dc6a066a?q=80&amp;w=1400&amp;auto=format&amp;fit=crop"
      preserveAspectRatio="xMidYMid slice" clip-path="url(#clipQ1)"/>
    <image x="-260" y="-200" width="1120" height="1120"
      href="https://images.unsplash.com/photo-1538481199705-c710c4e965fc?q=80&amp;w=1400&amp;auto=format&amp;fit=crop"
      preserveAspectRatio="xMidYMid slice" clip-path="url(#clipQ2)"/>
    <image x="-260" y="-200" width="1120" height="1120"
      href="https://images.unsplash.com/photo-1580971510443-45f866415ee5?q=80&amp;w=1400&amp;auto=format&amp;fit=crop"
      preserveAspectRatio="xMidYMid slice" clip-path="url(#clipQ3)"/>
    <image x="-260" y="-200" width="1120" height="1120"
      href="https://images.unsplash.com/photo-1596700685412-25e408ec21ba?q=80&amp;w=1400&amp;auto=format&amp;fit=crop"
      preserveAspectRatio="xMidYMid slice" clip-path="url(#clipQ4)"/>

    <path d="M344 316 L344 -200 A560 560 0 0 1 860 316 Z" fill="none" stroke="#ffffff" stroke-opacity="0.20" stroke-width="3"/>
    <path d="M344 404 L860 404 A560 560 0 0 1 344 920 Z" fill="none" stroke="#ffffff" stroke-opacity="0.16" stroke-width="3"/>
    <path d="M256 404 L256 920 A560 560 0 0 1 -260 404 Z" fill="none" stroke="#ffffff" stroke-opacity="0.12" stroke-width="3"/>
    <path d="M256 316 L-260 316 A560 560 0 0 1 256 -200 Z" fill="none" stroke="#ffffff" stroke-opacity="0.12" stroke-width="3"/>
  </g>

  <rect x="842" y="150" width="6" height="310" rx="3" fill="url(#accentGrad)"/>
  <text x="884" y="150" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" letter-spacing="3" fill="#7dd3fc">
    WORLD FESTIVAL SERIES
  </text>
  <text x="884" y="236" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#ffffff">
    DIWALI
    <tspan x="884" dy="56">CELEBRATION</tspan>
  </text>
  <text x="890" y="334" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="29" font-weight="300" letter-spacing="7" fill="#d7e3f7" transform="rotate(-4 890 334)">
    INDIA
  </text>
  <line x1="884" y1="380" x2="1180" y2="380" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>
  <text x="884" y="420" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#c8d2e3">
    The festival of lights celebrates the triumph of light over darkness and good over evil.
    <tspan x="884" dy="30">Oil lamps, fireworks, floral colors, and shared meals turn the city into a glowing communal stage.</tspan>
  </text>
  <text x="1090" y="625" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#ffffff" opacity="0.16">
    01/04
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; the spin should be created with PowerPoint Morph by rotating the same wheel group on duplicate slides.
- ❌ `<mask>` for quadrant gaps; use clipped images with wedge-shaped `<clipPath>` paths instead.
- ❌ Applying `clip-path` to decorative paths or rectangles; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ Rebuilding the wheel differently on each slide; Morph needs the wheel objects to remain visually and structurally consistent.
- ❌ Using `<use>` or `<symbol>` to duplicate quadrant geometry; expand each path explicitly.

## Composition notes
- Place the wheel center far left of the slide, around `x=280–330`, so the circle feels oversized and cinematic rather than like a chart.
- Keep the active text block on the right third of the canvas, with generous negative space between the wheel and headline.
- Use a dark radial background so colorful photography becomes the hero while white typography stays crisp.
- For the full carousel sequence, duplicate the slide and rotate `carousel-wheel-state-0` by `90`, `180`, and `270` degrees around the same center point.