# SVG Recipe — Flat Vector Device Mockup

## Visual mechanism
Build a premium phone mockup entirely from layered vector primitives: a dark rounded-rectangle bezel, a clipped screenshot/photo as the screen, pill-shaped side buttons, and a top dynamic-island notch. The device sits over a bold closing-slide composition so the vector mockup feels like a tangible product rather than a flat screenshot.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× `<path>` for large soft decorative background blobs and light streaks
- 1× `<filter id="phoneShadow">` applied to the device body for depth
- 1× `<filter id="softGlow">` applied to background accent blobs
- 1× `<clipPath>` with rounded `<rect>` for clipping the screen image to the phone screen shape
- 1× `<image>` for the app screenshot / UI screen content, clipped by the rounded screen clip path
- 1× large `<rect>` for the outer phone bezel
- 2× subtle `<rect>` overlays for bevel/highlight treatment on the bezel and screen edge
- 4× small rounded `<rect>` shapes for hardware buttons and the dynamic island
- 1× `<circle>` for the camera dot inside the island
- 3× `<text>` elements with explicit `width` for the closing-slide title, subtitle, and CTA label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBlue" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#0B5CFF"/>
      <stop offset="48%" stop-color="#123CCB"/>
      <stop offset="100%" stop-color="#081A5C"/>
    </linearGradient>

    <linearGradient id="aquaGlow" x1="120" y1="100" x2="620" y2="650">
      <stop offset="0%" stop-color="#70F7FF" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#7B61FF" stop-opacity="0.05"/>
    </linearGradient>

    <linearGradient id="bezelEdge" x1="790" y1="64" x2="1086" y2="656">
      <stop offset="0%" stop-color="#3A3A40"/>
      <stop offset="45%" stop-color="#17171A"/>
      <stop offset="100%" stop-color="#050507"/>
    </linearGradient>

    <linearGradient id="screenShade" x1="808" y1="83" x2="1068" y2="637">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.28"/>
      <stop offset="35%" stop-color="#FFFFFF" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.16"/>
    </linearGradient>

    <filter id="phoneShadow" x="-30%" y="-20%" width="160%" height="150%">
      <feOffset dx="0" dy="28"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <clipPath id="screenClip">
      <rect x="808" y="83" width="260" height="554" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBlue)"/>

  <path d="M-70,590 C120,430 240,520 360,365 C455,242 615,225 760,310 C645,485 580,650 410,745 C215,852 60,745 -70,590 Z"
        fill="url(#aquaGlow)" filter="url(#softGlow)" opacity="0.9"/>
  <path d="M990,-80 C1125,-20 1210,105 1328,64 L1328,292 C1195,342 1076,280 1008,168 C960,88 944,8 990,-80 Z"
        fill="#5EEBFF" opacity="0.18" filter="url(#softGlow)"/>
  <path d="M90,120 C235,70 410,92 550,34" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.28" stroke-dasharray="12 18"/>

  <text x="82" y="230" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" fill="#FFFFFF" letter-spacing="-1">
    Launch-ready
    <tspan x="82" dy="64" fill="#9DF7FF">mobile experience</tspan>
  </text>

  <text x="86" y="382" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="500" fill="#D7E9FF" opacity="0.92">
    Present app screens inside a crisp native-vector device that stays editable, scalable, and Morph-friendly.
  </text>

  <rect x="86" y="488" width="214" height="54" rx="27" fill="#FFFFFF" opacity="0.96"/>
  <text x="118" y="523" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#0B47D9">
    View prototype
  </text>

  <g transform="rotate(-7 938 360)">
    <rect x="760" y="210" width="16" height="82" rx="8" fill="#111114"/>
    <rect x="760" y="318" width="16" height="72" rx="8" fill="#111114"/>
    <rect x="1080" y="264" width="16" height="118" rx="8" fill="#111114"/>

    <rect x="790" y="64" width="296" height="592" rx="48" ry="48"
          fill="url(#bezelEdge)" filter="url(#phoneShadow)"/>

    <rect x="800" y="74" width="276" height="572" rx="40" ry="40"
          fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.10"/>

    <image x="808" y="83" width="260" height="554"
           href="https://images.example.com/mobile-app-dashboard-screenshot-tall.jpg"
           preserveAspectRatio="xMidYMid slice"
           clip-path="url(#screenClip)"/>

    <rect x="808" y="83" width="260" height="554" rx="34" ry="34"
          fill="none" stroke="#0A0A0C" stroke-width="4"/>

    <path d="M826,112 C880,86 985,88 1046,140 L1046,194 C970,142 892,148 826,210 Z"
          fill="url(#screenShade)" opacity="0.7"/>

    <rect x="878" y="104" width="120" height="33" rx="17" ry="17" fill="#050506"/>
    <circle cx="977" cy="120.5" r="5.5" fill="#1D2E3F"/>
    <circle cx="977" cy="120.5" r="2.2" fill="#4C78A8" opacity="0.75"/>

    <rect x="916" y="628" width="46" height="4" rx="2" fill="#FFFFFF" opacity="0.32"/>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use a PNG phone frame mockup; the point is to keep the bezel, buttons, notch, and screen geometry editable as PowerPoint shapes.
- ❌ Do not apply `clip-path` to groups, paths, or rectangles for screen masking; apply the rounded clip path directly to the `<image>`.
- ❌ Do not use `<mask>` to cut the screen hole out of the bezel; layer the clipped screen image above the dark bezel instead.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to create perspective; use clean rotation and scale only, or keep the device front-facing.
- ❌ Do not forget explicit `width` on text elements, or PowerPoint text wrapping may differ from the SVG preview.

## Composition notes
- Place the device on the right third or right half of the slide, leaving the left side open for closing-slide copy and CTA text.
- Keep bezel margins mathematically consistent: outer body → inner screen should feel even on all sides, with slightly more room at the top for the island.
- Use a bold gradient or saturated background so the nearly black phone silhouette reads clearly.
- Add only subtle highlights and shadows; the mockup should remain flat-vector and editable, not look like a raster photorealistic render.