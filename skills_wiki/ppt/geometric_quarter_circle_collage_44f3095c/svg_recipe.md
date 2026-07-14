# SVG Recipe — Geometric Quarter-Circle Collage

## Visual mechanism
A single hero photo is repeated in the exact same global position, but each copy is clipped by a different circle, half-circle, or quarter-circle mask on a strict grid. Solid pastel geometric blocks fill selected cells, creating an editorial collage with generous white typography space.

## SVG primitives needed
- 1× `<rect>` for the pure white slide background
- 1× `<circle>` for a soft background halo accent
- 2× `<linearGradient>` for dusty pink and taupe editorial color blocks
- 1× `<radialGradient>` for the pale decorative halo
- 1× `<filter id="softShadow">` applied to white geometric backplates for subtle depth
- 9× `<clipPath>` using `<circle>` or `<path>` to define full-circle, half-circle, and quarter-circle image windows
- 9× `<image>` copies of the same photo, all with identical `x`, `y`, `width`, and `height`, each clipped by a different geometric mask
- 6× `<path>` for pastel quarter-circle / half-circle color blocks and shadow backplates
- 1× `<circle>` for a solid taupe circular color block
- 1× `<rect>` for a pale editorial square color block
- 5× `<text>` elements for title, subtitle, caption, section number, and rotated label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pinkWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F2D8D4"/>
      <stop offset="100%" stop-color="#E2B8B2"/>
    </linearGradient>

    <linearGradient id="taupeWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#A08A84" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#6F5D59" stop-opacity="0.74"/>
    </linearGradient>

    <radialGradient id="softHalo" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#E2B8B2" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#E2B8B2" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- 4 columns × 3 rows grid begins at x=320, cell size=240 -->
    <clipPath id="clipCircleA" clipPathUnits="userSpaceOnUse">
      <circle cx="440" cy="120" r="120"/>
    </clipPath>

    <clipPath id="clipQuarterTR" clipPathUnits="userSpaceOnUse">
      <path d="M800 0 L800 240 A240 240 0 0 1 560 0 Z"/>
    </clipPath>

    <clipPath id="clipHalfTop" clipPathUnits="userSpaceOnUse">
      <path d="M800 120 A120 120 0 0 1 1040 120 L1040 0 L800 0 Z"/>
    </clipPath>

    <clipPath id="clipQuarterBL" clipPathUnits="userSpaceOnUse">
      <path d="M1040 240 L1040 0 A240 240 0 0 1 1280 240 Z"/>
    </clipPath>

    <clipPath id="clipQuarterTL" clipPathUnits="userSpaceOnUse">
      <path d="M320 240 L560 240 A240 240 0 0 1 320 480 Z"/>
    </clipPath>

    <clipPath id="clipCircleB" clipPathUnits="userSpaceOnUse">
      <circle cx="920" cy="360" r="120"/>
    </clipPath>

    <clipPath id="clipHalfRight" clipPathUnits="userSpaceOnUse">
      <path d="M1160 240 A120 120 0 0 1 1160 480 L1280 480 L1280 240 Z"/>
    </clipPath>

    <clipPath id="clipQuarterBR" clipPathUnits="userSpaceOnUse">
      <path d="M800 720 L560 720 A240 240 0 0 1 800 480 Z"/>
    </clipPath>

    <clipPath id="clipHalfBottom" clipPathUnits="userSpaceOnUse">
      <path d="M800 600 A120 120 0 0 0 1040 600 L1040 720 L800 720 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <circle cx="1240" cy="-40" r="310" fill="url(#softHalo)"/>

  <!-- Typography zone -->
  <text x="72" y="96" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" letter-spacing="2.8" fill="#9B7F7A">
    01 / LOOKBOOK
  </text>

  <text x="70" y="196" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" letter-spacing="2" fill="#505050">
    FASHION
  </text>

  <text x="74" y="248" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-style="italic" fill="#E2B8B2">
    <tspan>show</tspan>
  </text>

  <text x="76" y="315" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="13" line-height="1.5" fill="#77706E">
    <tspan x="76" dy="0">A modular image collage built</tspan>
    <tspan x="76" dy="22">from circles, half-circles, and</tspan>
    <tspan x="76" dy="22">quarter-circle photo windows.</tspan>
  </text>

  <text x="304" y="674" width="190" transform="rotate(-90 304 674)" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" letter-spacing="3" fill="#C7A19C">
    GEOMETRIC EDITORIAL
  </text>

  <!-- Solid pastel cells -->
  <rect x="320" y="480" width="240" height="240" fill="#F8EEEE"/>
  <path d="M560 240 L800 240 A240 240 0 0 1 560 480 Z" fill="url(#pinkWash)"/>
  <path d="M1040 480 L1280 480 A240 240 0 0 1 1040 720 Z" fill="url(#taupeWash)"/>
  <circle cx="1160" cy="600" r="120" fill="#8C7873" opacity="0.58"/>
  <path d="M320 0 L560 0 A240 240 0 0 1 320 240 Z" fill="#F3DEDB" opacity="0.55"/>

  <!-- White backplates with soft shadow under selected fragments -->
  <circle cx="440" cy="120" r="120" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.86"/>
  <path d="M800 720 L560 720 A240 240 0 0 1 800 480 Z" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.82"/>

  <!-- Same image repeated in identical global position; only clipPath changes -->
  <image href="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="320" y="0" width="960" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCircleA)"/>

  <image href="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="320" y="0" width="960" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipQuarterTR)"/>

  <image href="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="320" y="0" width="960" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipHalfTop)"/>

  <image href="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="320" y="0" width="960" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipQuarterBL)"/>

  <image href="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="320" y="0" width="960" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipQuarterTL)"/>

  <image href="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="320" y="0" width="960" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCircleB)"/>

  <image href="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="320" y="0" width="960" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipHalfRight)"/>

  <image href="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="320" y="0" width="960" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipQuarterBR)"/>

  <image href="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="320" y="0" width="960" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipHalfBottom)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to reveal the image; use `<clipPath>` applied directly to each `<image>` copy.
- ❌ Do not clip a parent `<g>` containing images or shapes; PPT translation only preserves clipping reliably on `<image>`.
- ❌ Do not use `<pattern>` fills to simulate the photo collage; repeat the same `<image>` with identical placement instead.
- ❌ Do not use `<use href="#...">` to duplicate image fragments; duplicate the `<image>` elements explicitly.
- ❌ Do not place text over the busy photo area unless it sits inside a clear white/pastel cell.

## Composition notes
- Reserve the left 25% of the slide for quiet typography; keep it mostly white for luxury editorial balance.
- Use a strict 4×3 grid on the right: each cell is 240×240 on a 1280×720 canvas.
- Keep all photo fragments aligned by giving every clipped image the same `x`, `y`, `width`, `height`, and `preserveAspectRatio`.
- Balance photo-heavy cells with pastel solid shapes so the collage feels designed, not randomly cut up.