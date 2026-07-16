# SVG Recipe — Liquid Image Mask Reveal

## Visual mechanism
A landscape photo is revealed only through one oversized organic “liquid” window on a clean white canvas, making the image feel like it is surfacing through the slide. Semi-transparent color blobs overlap the photo edge to amplify the fluid, premium keynote look while crisp typography stays isolated in negative space.

## SVG primitives needed
- 1× `<image>` for the full-color hero photograph, clipped to the organic reveal shape
- 1× `<clipPath>` containing a custom `<path>` for the liquid photo crop
- 1× large `<path>` behind the image for the soft shadow of the liquid window
- 2× translucent decorative `<path>` blobs for magenta and violet liquid overlays
- 5× `<rect>` for white canvas, left label rail, page number tile, title underline, and small logo accent
- 6× `<text>` elements for logo, rail label, page number, hero title, subtitle, and tiny eyebrow copy
- 2× `<linearGradient>` fills for saturated liquid accent blobs
- 2× `<filter>` definitions: one soft ambient shadow for blobs/photo silhouette, one sharper shadow for title/logo depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pinkBlob" x1="210" y1="65" x2="520" y2="320" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff3f8f"/>
      <stop offset="0.55" stop-color="#f01670"/>
      <stop offset="1" stop-color="#c90062"/>
    </linearGradient>

    <linearGradient id="violetBlob" x1="720" y1="450" x2="940" y2="665" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#4214bd"/>
      <stop offset="1" stop-color="#7c3bc6"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.02  0 0 0 0 0.02  0 0 0 0 0.05  0 0 0 0.22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="typeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="8" dy="12"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.03  0 0 0 0 0.03  0 0 0 0 0.04  0 0 0 0.24 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="liquidReveal">
      <path d="M178,452
               C158,355 229,257 347,204
               C463,151 568,104 708,127
               C842,149 932,243 906,364
               C885,464 814,519 707,519
               C580,518 511,548 413,587
               C320,624 207,579 178,452 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <rect x="0" y="210" width="58" height="302" fill="#ffffff" filter="url(#softShadow)"/>
  <text x="36" y="428" width="220" transform="rotate(-90 36 428)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700"
        fill="#111111" text-anchor="middle">Liquid Image Mask</text>

  <rect x="0" y="663" width="58" height="57" fill="#ffffff" filter="url(#softShadow)"/>
  <text x="29" y="697" width="42"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700"
        fill="#111111" text-anchor="middle">21</text>

  <text x="60" y="79" width="90"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="900"
        fill="#ffffff" stroke="#160531" stroke-width="5" paint-order="stroke" letter-spacing="-2">ONE</text>
  <text x="61" y="96" width="90"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="900"
        fill="#ffffff" stroke="#160531" stroke-width="5" paint-order="stroke" letter-spacing="-1">SKILL</text>
  <rect x="59" y="94" width="62" height="5" fill="#ff2e8a" transform="rotate(-4 59 94)"/>

  <path d="M178,452
           C158,355 229,257 347,204
           C463,151 568,104 708,127
           C842,149 932,243 906,364
           C885,464 814,519 707,519
           C580,518 511,548 413,587
           C320,624 207,579 178,452 Z"
        fill="#ffffff" filter="url(#softShadow)"/>

  <image x="120" y="70" width="850" height="580"
         href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&amp;w=1800&amp;auto=format&amp;fit=crop"
         xlink:href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&amp;w=1800&amp;auto=format&amp;fit=crop"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#liquidReveal)"/>

  <path d="M238,72
           C288,16 332,25 360,96
           C397,190 503,179 520,239
           C540,311 428,340 333,309
           C244,280 184,220 200,139
           C205,113 219,89 238,72 Z"
        fill="url(#pinkBlob)" opacity="0.88" filter="url(#softShadow)"/>

  <path d="M735,467
           C791,436 887,456 929,514
           C956,552 910,575 860,589
           C812,602 812,659 773,677
           C735,695 717,644 722,586
           C727,532 693,490 735,467 Z"
        fill="url(#violetBlob)" opacity="0.90" filter="url(#softShadow)"/>

  <text x="1040" y="250" width="290"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="48" font-weight="500"
        fill="#050505" text-anchor="middle" letter-spacing="1.5" filter="url(#typeShadow)">
    <tspan x="1040" dy="0">LIQUID</tspan>
    <tspan x="1040" dy="52">IMAGE</tspan>
    <tspan x="1040" dy="52">MASK</tspan>
  </text>

  <rect x="1050" y="395" width="76" height="5" fill="#12051f"/>

  <text x="1088" y="455" width="205"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="400"
        fill="#666666" text-anchor="middle">
    <tspan x="1088" dy="0">Insert some</tspan>
    <tspan x="1088" dy="16">awesome text right</tspan>
    <tspan x="1088" dy="16">here. just remember</tspan>
    <tspan x="1088" dy="16">keep it short and</tspan>
    <tspan x="1088" dy="16">sweet.</tspan>
  </text>

  <text x="1040" y="590" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="600"
        fill="#b8b8b8" text-anchor="middle" letter-spacing="2">ORGANIC REVEAL / HERO INTRO</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to punch a transparent hole through a white overlay; masks on shapes are not reliable in the PPT translator.
- ❌ Do not apply `clip-path` to the white overlay or decorative paths; only clip the `<image>` itself.
- ❌ Do not use `<animate>` or `<animateTransform>` for the breathing/rotation effect; add PowerPoint animation later if needed.
- ❌ Do not use `<pattern>` or `<textPath>` for the organic treatment; use editable paths, gradients, and clipped images instead.
- ❌ Do not create the liquid shape with many small circles; use one smooth Bézier `<path>` so the silhouette feels intentional and premium.

## Composition notes
- Place the liquid photo window left-of-center, occupying roughly 55–60% of slide width, with its optical center around the vertical midpoint.
- Keep the right third mostly white and quiet; reserve it for stacked title typography, a short underline, and a compact caption.
- Use saturated translucent blobs partially crossing the image boundary to sell the “liquid” reveal and add color rhythm.
- The organic image crop should have a soft shadow behind it, but the clipped photo itself should stay crisp and full contrast.