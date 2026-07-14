# SVG Recipe — Left Window Graphic Divider

## Visual mechanism
A large abstract “window” sits on the left edge of the slide as a chapter-marker graphic: four luminous panes reveal fragments of a cool-toned image while thin dividers and soft shadows make the shape feel architectural. The right side remains clean and text-forward, using the window as a strong visual divider between section identity and content.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<path>` for oversized ambient light blobs behind the window
- 4× `<image>` clipped into rounded-rectangle panes for the window photo fragments
- 4× `<clipPath>` with rounded `<rect>` crops for each pane image
- 4× `<rect>` for glass tint overlays on top of each image pane
- 1× `<rect>` for the outer window frame
- 2× `<rect>` for vertical and horizontal window mullions
- 4× `<rect>` for subtle inner highlight strokes on each pane
- 1× `<line>` for the slim divider between graphic and text areas
- 3× `<text>` elements for section eyebrow, headline, and body copy
- 2× `<filter>` definitions: one soft shadow for the window group, one blur/glow for background light
- 4× `<linearGradient>` definitions for background, pane tint, frame stroke, and divider accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#08111f"/>
      <stop offset="45%" stop-color="#0c1829"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>

    <linearGradient id="paneTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.26"/>
      <stop offset="42%" stop-color="#6ee7ff" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0.34"/>
    </linearGradient>

    <linearGradient id="frameStroke" x1="140" y1="120" x2="500" y2="600" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#f8fafc" stop-opacity="0.88"/>
      <stop offset="45%" stop-color="#67e8f9" stop-opacity="0.46"/>
      <stop offset="100%" stop-color="#2563eb" stop-opacity="0.44"/>
    </linearGradient>

    <linearGradient id="dividerGrad" x1="0" y1="180" x2="0" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0"/>
      <stop offset="45%" stop-color="#38bdf8" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
    </linearGradient>

    <filter id="windowShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>

    <clipPath id="paneTL" clipPathUnits="userSpaceOnUse">
      <rect x="145" y="126" width="150" height="178" rx="26"/>
    </clipPath>
    <clipPath id="paneTR" clipPathUnits="userSpaceOnUse">
      <rect x="315" y="126" width="150" height="178" rx="26"/>
    </clipPath>
    <clipPath id="paneBL" clipPathUnits="userSpaceOnUse">
      <rect x="145" y="324" width="150" height="224" rx="26"/>
    </clipPath>
    <clipPath id="paneBR" clipPathUnits="userSpaceOnUse">
      <rect x="315" y="324" width="150" height="224" rx="26"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <path d="M-40,105 C75,22 191,38 257,125 C324,213 266,330 148,343 C33,356 -70,263 -40,105 Z"
        fill="#0ea5e9" opacity="0.22" filter="url(#softGlow)"/>
  <path d="M252,542 C391,456 545,502 563,617 C581,733 392,779 254,704 C159,653 144,609 252,542 Z"
        fill="#22d3ee" opacity="0.12" filter="url(#softGlow)"/>

  <g transform="rotate(-3 305 337)" filter="url(#windowShadow)">
    <rect x="118" y="98" width="374" height="480" rx="42"
          fill="#07111f" opacity="0.92" stroke="url(#frameStroke)" stroke-width="3"/>

    <image href="https://images.example.com/cool-blue-city-architecture-glass-detail.jpg"
           x="105" y="95" width="410" height="500" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#paneTL)"/>
    <image href="https://images.example.com/cool-blue-city-architecture-glass-detail.jpg"
           x="105" y="95" width="410" height="500" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#paneTR)"/>
    <image href="https://images.example.com/cool-blue-city-architecture-glass-detail.jpg"
           x="105" y="95" width="410" height="500" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#paneBL)"/>
    <image href="https://images.example.com/cool-blue-city-architecture-glass-detail.jpg"
           x="105" y="95" width="410" height="500" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#paneBR)"/>

    <rect x="145" y="126" width="150" height="178" rx="26" fill="url(#paneTint)"/>
    <rect x="315" y="126" width="150" height="178" rx="26" fill="url(#paneTint)"/>
    <rect x="145" y="324" width="150" height="224" rx="26" fill="url(#paneTint)"/>
    <rect x="315" y="324" width="150" height="224" rx="26" fill="url(#paneTint)"/>

    <rect x="298" y="114" width="14" height="448" rx="7" fill="#dbeafe" opacity="0.86"/>
    <rect x="134" y="306" width="342" height="14" rx="7" fill="#dbeafe" opacity="0.86"/>

    <rect x="145" y="126" width="150" height="178" rx="26" fill="none" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2"/>
    <rect x="315" y="126" width="150" height="178" rx="26" fill="none" stroke="#ffffff" stroke-opacity="0.36" stroke-width="2"/>
    <rect x="145" y="324" width="150" height="224" rx="26" fill="none" stroke="#ffffff" stroke-opacity="0.34" stroke-width="2"/>
    <rect x="315" y="324" width="150" height="224" rx="26" fill="none" stroke="#ffffff" stroke-opacity="0.42" stroke-width="2"/>
  </g>

  <line x1="575" y1="156" x2="575" y2="566" stroke="url(#dividerGrad)" stroke-width="2"/>

  <text x="645" y="178" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="3" fill="#67e8f9">
    SECTION 04
  </text>

  <text x="642" y="282" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="700" fill="#f8fafc">
    <tspan x="642" dy="0">Spatial</tspan>
    <tspan x="642" dy="66">Narrative</tspan>
    <tspan x="642" dy="66">Systems</tspan>
  </text>

  <text x="648" y="514" width="450" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="400" fill="#cbd5e1">
    A clean chapter divider using a left-side window graphic to signal a transition into a new theme, product area, or strategic pillar.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to cut window panes out of a single large frame; masks are not reliable in the PPT translation path.
- ❌ Applying `clip-path` to `<rect>` or `<g>` for the frame; only clip the `<image>` elements.
- ❌ Creating perspective with `skewX`, `skewY`, or `matrix(...)`; use mild `rotate(...)`, layering, and proportion instead.
- ❌ Building the window from plain outlined rectangles only; the technique depends on luminous panes, depth, and a strong left-side graphic presence.
- ❌ Putting filter effects on `<line>` elements; keep shadows/glows on rects, paths, text, circles, or ellipses.

## Composition notes
- Keep the window graphic anchored to the left third, slightly oversized and gently rotated so it feels like a deliberate section-marker object rather than a chart.
- Reserve the right half for sparse typography: small eyebrow, large headline, and one short body paragraph.
- Use cool cyan highlights sparingly on the panes, divider line, and section label to create rhythm across the slide.
- Maintain generous negative space around the headline; the window carries the visual weight, so the text block should remain calm and executive.