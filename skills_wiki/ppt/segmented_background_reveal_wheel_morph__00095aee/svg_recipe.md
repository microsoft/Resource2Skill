# SVG Recipe — Segmented Wheel Reveal with Morph

## Visual mechanism
A full-bleed photo is darkened by a left-to-right navy gradient, while oversized doughnut segments on the right re-show the same photo at full brightness through clipped image “windows.” Across Morph slides, keep the wheel group’s center fixed and rotate it 90° while swapping the photo, creating a cinematic rotating reveal.

## SVG primitives needed
- 1× full-slide `<image>` for the darkened background photograph
- 1× `<rect>` with transparent linear gradient for the readability overlay
- 4× `<clipPath>` with doughnut-segment `<path>` geometry for the reveal windows
- 4× clipped `<image>` duplicates using the same photo, one per segment
- 4× `<path>` shadow silhouettes behind the segments for depth
- 4× `<path>` highlight strokes over the segments for glass/lens edges
- 1× `<filter id="wheelShadow">` using `feOffset + feGaussianBlur + feMerge` for the elevated wheel shadow
- 1× `<filter id="softGlow">` using `feGaussianBlur` for subtle accent glow
- 3× `<text>` blocks for kicker, title, and body copy, each with explicit `width`
- 1× CTA `<rect>` plus 1× CTA `<text>` for the action button
- 2× decorative `<line>` accents for premium editorial framing

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkVeil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#081018" stop-opacity="0.92"/>
      <stop offset="48%" stop-color="#081018" stop-opacity="0.74"/>
      <stop offset="78%" stop-color="#081018" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#081018" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="ctaFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00D4FF"/>
      <stop offset="100%" stop-color="#0077FF"/>
    </linearGradient>

    <filter id="wheelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-18" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="segRight" clipPathUnits="userSpaceOnUse">
      <path d="M1320 64 A470 470 0 0 1 1320 656 L1176 539 A285 285 0 0 0 1176 181 Z"/>
    </clipPath>
    <clipPath id="segBottom" clipPathUnits="userSpaceOnUse">
      <path d="M1251 725 A470 470 0 0 1 659 725 L776 586 A285 285 0 0 0 1133 586 Z"/>
    </clipPath>
    <clipPath id="segLeft" clipPathUnits="userSpaceOnUse">
      <path d="M590 656 A470 470 0 0 1 590 64 L733 181 A285 285 0 0 0 733 539 Z"/>
    </clipPath>
    <clipPath id="segTop" clipPathUnits="userSpaceOnUse">
      <path d="M659 -5 A470 470 0 0 1 1251 -5 L1133 134 A285 285 0 0 0 776 134 Z"/>
    </clipPath>
  </defs>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/destination-showcase/mountain-lake-golden-hour-1920x1080.jpg"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#darkVeil)"/>

  <circle cx="955" cy="360" r="332" fill="#00BFFF" opacity="0.12" filter="url(#softGlow)"/>

  <g id="morphWheel" transform="rotate(0 955 360)">
    <path d="M1320 64 A470 470 0 0 1 1320 656 L1176 539 A285 285 0 0 0 1176 181 Z"
          fill="#03101A" opacity="0.38" filter="url(#wheelShadow)"/>
    <path d="M1251 725 A470 470 0 0 1 659 725 L776 586 A285 285 0 0 0 1133 586 Z"
          fill="#03101A" opacity="0.34" filter="url(#wheelShadow)"/>
    <path d="M590 656 A470 470 0 0 1 590 64 L733 181 A285 285 0 0 0 733 539 Z"
          fill="#03101A" opacity="0.30" filter="url(#wheelShadow)"/>
    <path d="M659 -5 A470 470 0 0 1 1251 -5 L1133 134 A285 285 0 0 0 776 134 Z"
          fill="#03101A" opacity="0.34" filter="url(#wheelShadow)"/>

    <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
           href="https://images.example.com/destination-showcase/mountain-lake-golden-hour-1920x1080.jpg"
           clip-path="url(#segRight)"/>
    <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
           href="https://images.example.com/destination-showcase/mountain-lake-golden-hour-1920x1080.jpg"
           clip-path="url(#segBottom)"/>
    <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
           href="https://images.example.com/destination-showcase/mountain-lake-golden-hour-1920x1080.jpg"
           clip-path="url(#segLeft)"/>
    <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
           href="https://images.example.com/destination-showcase/mountain-lake-golden-hour-1920x1080.jpg"
           clip-path="url(#segTop)"/>

    <path d="M1320 64 A470 470 0 0 1 1320 656 L1176 539 A285 285 0 0 0 1176 181 Z"
          fill="none" stroke="#FFFFFF" stroke-opacity="0.32" stroke-width="2"/>
    <path d="M1251 725 A470 470 0 0 1 659 725 L776 586 A285 285 0 0 0 1133 586 Z"
          fill="none" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="2"/>
    <path d="M590 656 A470 470 0 0 1 590 64 L733 181 A285 285 0 0 0 733 539 Z"
          fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2"/>
    <path d="M659 -5 A470 470 0 0 1 1251 -5 L1133 134 A285 285 0 0 0 776 134 Z"
          fill="none" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="2"/>
  </g>

  <line x1="86" y1="112" x2="162" y2="112" stroke="#00BFFF" stroke-width="3"/>
  <line x1="86" y1="610" x2="252" y2="610" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1"/>

  <text x="86" y="154" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="3" fill="#7EE8FF">DESTINATION 04</text>

  <text x="82" y="276" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" fill="#FFFFFF">
    <tspan x="82" dy="0">Alpine</tspan>
    <tspan x="82" dy="78">Stillness</tspan>
  </text>

  <text x="88" y="398" width="475" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#DCEAF2" opacity="0.86">
    <tspan x="88" dy="0">A rotating segmented lens reveals each chapter</tspan>
    <tspan x="88" dy="30">of the journey while the dark gradient preserves</tspan>
    <tspan x="88" dy="30">executive-level readability on photographic slides.</tspan>
  </text>

  <rect x="88" y="514" width="178" height="48" rx="4" fill="url(#ctaFill)"/>
  <text x="116" y="545" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="800" letter-spacing="1.5" fill="#FFFFFF">EXPLORE NOW</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on true PowerPoint `bgFill` semantics in SVG; reproduce the reveal by duplicating the same photo and clipping each duplicate with a segment-shaped `clipPath`.
- ❌ Do not apply `clip-path` to a `<g>` or `<path>`; for PPT-Master compatibility, apply each clip path directly to an `<image>`.
- ❌ Do not use `<mask>` to cut holes through the gradient overlay; masks are not safe for this translator and will break or be ignored.
- ❌ Do not use `<use>` to reuse the segment paths; duplicate the path data explicitly for shadows, clips, and highlight strokes.
- ❌ Do not use `marker-end` for rotation arrows or explanatory callouts; if arrows are needed, build them from editable `<line>` and small `<path>` triangles.

## Composition notes
- Keep the wheel huge: center it around the right third of the slide, with the outer ring bleeding beyond the top, bottom, and right edges for immersive scale.
- Reserve the left 45–55% for typography under the darkest part of the gradient; avoid placing important text over the reveal wheel.
- For Morph, duplicate the slide, keep `id="morphWheel"` and the same center point, change `transform="rotate(90 955 360)"`, then swap all five image `href` values to the next photo.
- Use one electric accent color, such as cyan or azure, sparingly in the CTA, small rule line, and glow so the photography remains the hero.