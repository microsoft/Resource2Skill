# SVG Recipe — Isometric 3D Photo Cube (Dynamic Faces)

## Visual mechanism
Three square photos are clipped into mathematically aligned isometric polygons to form the visible top, left, and right faces of a cube. Thin bevel strips, directional tint overlays, and a blurred floor shadow make the clipped images read as one premium 3D object rather than three flat pictures.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× `<clipPath>` with polygonal face shapes for top, left, and right photo crops
- 3× `<image>` elements for the dynamic cube faces
- 1× `<path>` with blur filter for the projected floor shadow
- 3× `<path>` overlays for face lighting / darkening tints
- 8× `<path>` elements for bevel rims, dark seams, and highlight edges
- 1× `<filter id="floorShadow">` using `feGaussianBlur` for the soft ground shadow
- 1× `<filter id="softGlow">` using `feGaussianBlur` for atmospheric glow accents
- 5× `<linearGradient>` definitions for background, face tints, and bevels
- 2× `<circle>` decorative glows behind the cube
- 4× `<text>` elements with explicit `width` attributes for headline, subtitle, and face labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgSky" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#dff5ff"/>
      <stop offset="0.55" stop-color="#9ed2f2"/>
      <stop offset="1" stop-color="#287ab5"/>
    </linearGradient>

    <linearGradient id="topTint" x1="455" y1="125" x2="855" y2="260">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.34"/>
      <stop offset="0.55" stop-color="#ffffff" stop-opacity="0.05"/>
      <stop offset="1" stop-color="#06172b" stop-opacity="0.28"/>
    </linearGradient>

    <linearGradient id="leftShade" x1="455" y1="170" x2="600" y2="545">
      <stop offset="0" stop-color="#00162b" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#00162b" stop-opacity="0.48"/>
    </linearGradient>

    <linearGradient id="rightShade" x1="600" y1="205" x2="855" y2="545">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#2a1200" stop-opacity="0.28"/>
    </linearGradient>

    <linearGradient id="bevelBlue" x1="455" y1="170" x2="855" y2="545">
      <stop offset="0" stop-color="#a7f6ff"/>
      <stop offset="0.45" stop-color="#163a54"/>
      <stop offset="1" stop-color="#050911"/>
    </linearGradient>

    <filter id="floorShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>

    <clipPath id="clipTop">
      <polygon points="455,170 704,125 855,205 600,260"/>
    </clipPath>
    <clipPath id="clipLeft">
      <polygon points="455,170 600,260 600,545 455,455"/>
    </clipPath>
    <clipPath id="clipRight">
      <polygon points="600,260 855,205 855,495 600,545"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgSky)"/>

  <circle cx="656" cy="262" r="270" fill="#ffffff" opacity="0.28" filter="url(#softGlow)"/>
  <circle cx="870" cy="190" r="160" fill="#79d8ff" opacity="0.18" filter="url(#softGlow)"/>

  <path d="M407 454 L664 365 L895 465 L612 570 Z" fill="#09233a" opacity="0.42" filter="url(#floorShadow)"/>
  <path d="M431 452 L665 382 L868 462 L612 540 Z" fill="#0a1e2d" opacity="0.20"/>

  <image x="455" y="170" width="185" height="375" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&amp;fit=crop&amp;w=900&amp;q=80"
         clip-path="url(#clipLeft)"/>
  <path d="M455 170 L600 260 L600 545 L455 455 Z" fill="url(#leftShade)"/>
  <path d="M455 170 L600 260 L600 545 L455 455 Z" fill="none" stroke="#07121d" stroke-width="2.2"/>

  <image x="600" y="205" width="255" height="340" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1474044159687-1ee9f3a51722?auto=format&amp;fit=crop&amp;w=1000&amp;q=80"
         clip-path="url(#clipRight)"/>
  <path d="M600 260 L855 205 L855 495 L600 545 Z" fill="url(#rightShade)"/>
  <path d="M600 260 L855 205 L855 495 L600 545 Z" fill="none" stroke="#130b07" stroke-width="2.2"/>

  <image x="455" y="125" width="400" height="150" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1508780709619-79562169bc64?auto=format&amp;fit=crop&amp;w=1000&amp;q=80"
         clip-path="url(#clipTop)"/>
  <path d="M455 170 L704 125 L855 205 L600 260 Z" fill="url(#topTint)"/>
  <path d="M455 170 L704 125 L855 205 L600 260 Z" fill="none" stroke="#07121d" stroke-width="2.5"/>

  <path d="M455 170 L704 125 L855 205 L600 260 Z" fill="none" stroke="#ffffff" stroke-opacity="0.55" stroke-width="1.2"/>
  <path d="M455 170 L600 260 L600 545 L455 455 Z" fill="none" stroke="#5ad8ff" stroke-opacity="0.35" stroke-width="1.2"/>
  <path d="M600 260 L855 205 L855 495 L600 545 Z" fill="none" stroke="#ffd18a" stroke-opacity="0.34" stroke-width="1.2"/>

  <path d="M595 258 L604 261 L604 548 L595 543 Z" fill="#05080d" opacity="0.72"/>
  <path d="M455 170 L464 166 L609 255 L600 260 Z" fill="url(#bevelBlue)" opacity="0.78"/>
  <path d="M600 260 L609 255 L863 200 L855 205 Z" fill="#e7faff" opacity="0.40"/>
  <path d="M455 455 L600 545 L600 558 L455 468 Z" fill="#05111d" opacity="0.55"/>
  <path d="M600 545 L855 495 L855 508 L600 558 Z" fill="#08121a" opacity="0.48"/>

  <path d="M455 170 L455 455" fill="none" stroke="#06111c" stroke-width="4" opacity="0.64"/>
  <path d="M855 205 L855 495" fill="none" stroke="#2d1609" stroke-width="4" opacity="0.38"/>
  <path d="M704 125 L855 205" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.42"/>

  <text x="72" y="88" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff" opacity="0.86">
    DYNAMIC FACE SET
  </text>
  <text x="72" y="126" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#07395a">
    Isometric Photo Cube
  </text>
  <text x="74" y="160" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#154a69" opacity="0.88">
    Three editable image faces, clipped into one sculptural 3D anchor.
  </text>

  <text x="32" y="682" width="1220" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="900"
        letter-spacing="3" fill="#ffffff" stroke="#0b1824" stroke-width="3">
    3D CUBE WITH AUTO CHANGE PICTURE
  </text>
</svg>
```

## Avoid in this skill
- ❌ `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` to fake perspective; these transforms are dropped by the PPT translator.
- ❌ Applying `clip-path` to gradient overlays or bevel paths; clip paths should be used only on `<image>` elements.
- ❌ `<mask>` or masked lighting effects for the faces; use explicit polygon `<path>` overlays with opacity instead.
- ❌ `filter` on `<line>` elements for shadows; use a blurred `<path>` or `<ellipse>` under the cube.
- ❌ `<use>` / `<symbol>` for repeated edges; duplicate the bevel paths directly so PowerPoint keeps them editable.

## Composition notes
- Keep the cube centered slightly above the vertical midpoint; the floor shadow should sit below it and extend down-right to imply a consistent light source.
- Use three related but distinct photos so the cube reads as a unified portfolio object while each face remains visually recognizable.
- Reserve the lower 15–20% of the slide for a bold keynote headline; the cube should occupy the central 40–50% of the canvas height.
- For auto-changing faces in PowerPoint, duplicate the entire cube group, swap the three image URLs/fills, align perfectly, then crossfade the duplicated groups.