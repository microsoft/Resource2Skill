# SVG Recipe — 3D Out-of-Bounds Pop-out Effect (3D 立体出画效果)

## Visual mechanism
Create depth by splitting one scene into layers: a trapezoid “perspective floor” cropped from an environment image, then a transparent foreground subject that rises beyond the floor boundary. Large atmospheric text sits behind the subject, making the cutout feel like it is stepping out of the slide plane.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient sky / studio backdrop.
- 2× `<path>` for soft atmospheric background silhouettes and depth haze.
- 1× `<text>` for oversized backdrop typography behind the subject.
- 1× `<clipPath>` with a polygon-like `<path>` for the perspective floor crop.
- 1× `<image>` clipped to the trapezoid floor shape.
- 3× `<path>` for floor bevels, rim highlights, and underside depth shadow.
- 2× `<ellipse>` for soft contact shadows under the subject.
- 1× transparent `<image>` for the cutout subject that breaks the frame.
- 1× `<text>` title block and 1× `<text>` subtitle block for foreground narrative.
- 2× `<filter>` definitions: one blur glow for atmosphere, one offset blur shadow for editable depth.
- 2× `<linearGradient>` definitions for background and floor-edge lighting.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#46A7E8"/>
      <stop offset="48%" stop-color="#DDF3FF"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <linearGradient id="floorEdgeGrad" x1="0" y1="430" x2="0" y2="670">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.88"/>
      <stop offset="35%" stop-color="#6DB68A" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#0E3628" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="textFade" x1="160" y1="0" x2="1120" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.52"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.10"/>
    </linearGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="depthShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="floorClip">
      <path d="M294 418 L986 418 L1158 668 L122 668 Z"/>
    </clipPath>
  </defs>

  <!-- Sky / atmosphere -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#skyGrad)"/>

  <!-- Soft background haze shapes -->
  <path d="M-40 520 C140 430 280 460 420 510 C575 565 700 525 835 470 C980 410 1130 430 1320 520 L1320 720 L-40 720 Z"
        fill="#FFFFFF" opacity="0.38" filter="url(#softGlow)"/>
  <path d="M80 178 C210 120 310 160 390 225 C470 292 590 285 675 220 C790 132 940 138 1078 220 C1162 270 1225 276 1300 252 L1300 0 L80 0 Z"
        fill="#BFEAFF" opacity="0.42" filter="url(#softGlow)"/>

  <!-- Oversized backdrop typography, intentionally behind subject -->
  <text x="116" y="352" width="1048"
        font-family="Segoe UI, Microsoft YaHei" font-size="132" font-weight="800"
        letter-spacing="30" fill="url(#textFade)" text-anchor="middle">
    NATURE
  </text>

  <!-- Floor underside shadow and bevel: gives the trapezoid physical thickness -->
  <path d="M122 668 L1158 668 L1040 704 L240 704 Z"
        fill="#0A2018" opacity="0.26" filter="url(#depthShadow)"/>
  <path d="M294 418 L986 418 L1158 668 L122 668 Z"
        fill="#214E39" opacity="0.18" filter="url(#depthShadow)"/>

  <!-- Perspective floor texture clipped to trapezoid -->
  <image x="122" y="418" width="1036" height="250"
         href="https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?q=80&amp;w=1400&amp;auto=format&amp;fit=crop"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#floorClip)"/>

  <!-- Editable highlight / edge lines on the floor -->
  <path d="M294 418 L986 418 L1158 668 L122 668 Z"
        fill="url(#floorEdgeGrad)" opacity="0.22"/>
  <path d="M294 418 L986 418"
        fill="none" stroke="#FFFFFF" stroke-width="5" stroke-opacity="0.75"/>
  <path d="M122 668 L294 418 M986 418 L1158 668"
        fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-opacity="0.34"/>

  <!-- Contact shadows: place below transparent PNG subject -->
  <ellipse cx="644" cy="628" rx="235" ry="42" fill="#082219" opacity="0.30" filter="url(#softGlow)"/>
  <ellipse cx="646" cy="610" rx="142" ry="22" fill="#061912" opacity="0.32"/>

  <!-- Transparent foreground cutout; top extends outside the trapezoid boundary -->
  <image x="374" y="108" width="520" height="545"
         href="https://upload.wikimedia.org/wikipedia/commons/png/3/37/African_Elephant_Transparent.png"
         preserveAspectRatio="xMidYMax meet"/>

  <!-- Foreground editorial copy, kept clear of the pop-out subject -->
  <text x="70" y="92" width="390"
        font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        letter-spacing="3" fill="#0F5A7D">
    IMMERSIVE HERO VISUAL
  </text>
  <text x="70" y="136" width="370"
        font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800"
        fill="#07344A">
    Step beyond the frame
  </text>
  <text x="74" y="186" width="340"
        font-family="Segoe UI, Microsoft YaHei" font-size="18"
        fill="#24586B" opacity="0.86">
    A cutout subject breaks the image plane while the trapezoid floor anchors depth.
  </text>

  <!-- Small caption on the opposite corner for balance -->
  <text x="956" y="112" width="250"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600"
        fill="#FFFFFF" opacity="0.86" text-anchor="end">
    3D 立体出画效果
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to regular shapes or groups; use clipping only on the `<image>` that forms the trapezoid floor.
- ❌ Using `<mask>` to hide parts of the subject or floor; masks are not reliable for PPT translation.
- ❌ Trying to perspective-warp the image with `matrix(...)` or `skewX/skewY`; those transforms are dropped. Simulate perspective with a clipped trapezoid and directional highlights.
- ❌ Adding filter effects directly to `<line>` elements; use `<path>` for highlighted edges or shadowed rim shapes.
- ❌ Using `marker-end` on paths for perspective guides; if arrows are needed, use native `<line>` with marker settings directly on each line.

## Composition notes
- Keep the floor in the lower 25–35% of the canvas; the subject should overlap it and rise into the upper half of the slide.
- Place oversized text behind the subject with low opacity or gradient fill so it adds scale without competing with the cutout.
- Align the subject’s feet/base exactly on the floor’s top-middle zone; contact shadows sell the illusion.
- Use bright atmospheric background colors and darker grounded floor tones to create strong depth contrast.