# SVG Recipe — Diagonal Matte Reveal (Paper Cutout Effect)

## Visual mechanism
A full-slide matte layer owns the composition, while diagonal rounded “holes” reveal the same underlying photo in tightly controlled slashes. Soft blurred shadow shapes around each reveal create the illusion that the matte is thick cut paper sitting above the image.

## SVG primitives needed
- 2× `<linearGradient>` for the warm matte background and deeper orange lower wash
- 1× full-canvas `<rect>` for the base matte
- 2× large decorative `<circle>` elements for soft color fields behind the typography
- 1× `<path>` for the lower orange diagonal color wash
- 4× `<clipPath>` elements using rotated rounded rectangles and a circle for the photo reveals
- 4× clipped `<image>` copies using the same photo, one per cutout
- 4× shadow carrier shapes (`<rect>` / `<circle>`) with blur filters behind the clipped images
- 3× `<filter>` definitions for cutout rim shadows, heavy text shadows, and icon shadows
- 5× `<text>` elements for editable typography and symbol-like lettering
- 1× filled `<path>` for a bold editable curved arrow accent
- Several `<rect>` elements for the editable PowerPoint-style app icon and plus sign

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="matteWarm" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E7FF14"/>
      <stop offset="42%" stop-color="#FFD000"/>
      <stop offset="100%" stop-color="#FF6A00"/>
    </linearGradient>

    <linearGradient id="orangeWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFB000" stop-opacity="0.25"/>
      <stop offset="55%" stop-color="#FF7A00" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#F04E00"/>
    </linearGradient>

    <filter id="cutoutShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
      </feMerge>
    </filter>

    <filter id="typeShadow" x="-12%" y="-12%" width="130%" height="130%">
      <feOffset dx="8" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="iconShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoSlashA" clipPathUnits="userSpaceOnUse">
      <rect x="625" y="-115" width="230" height="670" rx="72" transform="rotate(31 740 220)"/>
    </clipPath>
    <clipPath id="photoSlashB" clipPathUnits="userSpaceOnUse">
      <rect x="875" y="-135" width="150" height="720" rx="62" transform="rotate(31 950 225)"/>
    </clipPath>
    <clipPath id="photoSlashC" clipPathUnits="userSpaceOnUse">
      <rect x="1040" y="-40" width="205" height="820" rx="72" transform="rotate(31 1142 370)"/>
    </clipPath>
    <clipPath id="photoCircle" clipPathUnits="userSpaceOnUse">
      <circle cx="935" cy="558" r="70"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#matteWarm)"/>
  <circle cx="206" cy="160" r="205" fill="#FF5A2E" opacity="0.88"/>
  <circle cx="318" cy="-45" r="200" fill="#FFB07A" opacity="0.76"/>
  <path d="M0 342 C190 290 380 336 530 392 C720 465 870 414 1010 354 C1125 305 1215 286 1280 300 L1280 720 L0 720 Z"
        fill="url(#orangeWash)"/>

  <!-- Cutout rim shadows: same geometry as the image clips, drawn above matte and below photos -->
  <rect x="625" y="-115" width="230" height="670" rx="72" transform="rotate(31 740 220)"
        fill="#2C1D00" opacity="0.38" filter="url(#cutoutShadow)"/>
  <rect x="875" y="-135" width="150" height="720" rx="62" transform="rotate(31 950 225)"
        fill="#2C1D00" opacity="0.38" filter="url(#cutoutShadow)"/>
  <rect x="1040" y="-40" width="205" height="820" rx="72" transform="rotate(31 1142 370)"
        fill="#2C1D00" opacity="0.42" filter="url(#cutoutShadow)"/>
  <circle cx="935" cy="558" r="70" fill="#2C1D00" opacity="0.36" filter="url(#cutoutShadow)"/>

  <!-- Same full-slide photo repeated and clipped, so all revealed slashes align visually -->
  <image href="https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?q=80&w=1920&auto=format&fit=crop"
         x="520" y="0" width="760" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoSlashA)"/>
  <image href="https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?q=80&w=1920&auto=format&fit=crop"
         x="520" y="0" width="760" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoSlashB)"/>
  <image href="https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?q=80&w=1920&auto=format&fit=crop"
         x="520" y="0" width="760" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoSlashC)"/>
  <image href="https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?q=80&w=1920&auto=format&fit=crop"
         x="520" y="0" width="760" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoCircle)"/>

  <!-- Editable PowerPoint-style badge -->
  <rect x="-8" y="58" width="216" height="230" rx="18" fill="#9E2B19" opacity="0.35" filter="url(#iconShadow)"/>
  <rect x="-22" y="48" width="222" height="220" rx="18" fill="#F04423" filter="url(#iconShadow)"/>
  <rect x="0" y="48" width="200" height="220" rx="16" fill="#FF552D"/>
  <text x="38" y="218" width="122" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="170" font-weight="800" fill="#FFFFFF">P</text>

  <!-- Plus mark built from editable rectangles instead of a glyph -->
  <rect x="512" y="90" width="126" height="34" fill="#FFFFFF" filter="url(#typeShadow)"/>
  <rect x="558" y="45" width="34" height="124" fill="#FFFFFF" filter="url(#typeShadow)"/>

  <!-- Oversized editable headline typography -->
  <text x="226" y="432" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="445" font-weight="900" fill="#FFFFFF" letter-spacing="-18"
        filter="url(#typeShadow)">A</text>
  <text x="18" y="622" width="605" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="190" font-weight="900" fill="#FFFFFF" letter-spacing="-8"
        filter="url(#typeShadow)">SLIDE</text>

  <!-- Curved white arrow accent, drawn as a filled path so it stays editable -->
  <path d="M590 309 C622 397 682 437 753 402 L723 389 C710 384 710 366 725 362
           L812 383 C828 387 835 404 826 418 L773 489 C764 502 744 496 745 479
           L747 444 C650 482 562 426 539 334 C535 318 584 294 590 309 Z"
        fill="#FFFFFF" filter="url(#typeShadow)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or `mask="url(#...)"` to subtract holes from the matte; it will hard-fail translation.
- ❌ Do not apply `clip-path` to a `<rect>`, `<path>`, or `<g>` to simulate the matte cutout; clipping is reliable here only on `<image>`.
- ❌ Do not rely on Boolean subtraction, even-odd compound paths, or `<pattern>` fills for the paper layer; instead, place clipped photo copies above the matte.
- ❌ Do not use `marker-end` for the arrow; draw the arrowhead as part of a filled editable `<path>`.
- ❌ Do not place a filter on `<line>` elements; use filtered rectangles, paths, circles, or text for shadows.

## Composition notes
- Keep the left 45–50% of the slide mostly matte so large white typography has strong contrast and remains the visual anchor.
- Place diagonal reveals on the right half, letting some extend beyond the canvas for a cropped editorial feel.
- Use identical image positioning for every clipped reveal so the photo appears continuous beneath the cut paper.
- The shadow carrier shapes should sit between the matte and clipped images; this creates the tactile rim without needing unsupported masks.