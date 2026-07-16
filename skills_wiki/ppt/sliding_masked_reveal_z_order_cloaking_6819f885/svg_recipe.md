# SVG Recipe — Sliding Masked Reveal (Z-Order Cloaking)

## Visual mechanism
A bold text block is placed underneath a background-colored “cloaking” shape, so the letters appear perfectly sliced at an invisible boundary. A thin glowing divider is placed on top of the cloak edge, making the text feel as if it is sliding out from the line.

## SVG primitives needed
- 2× `<rect>` for the full-slide background and the glowing vertical reveal divider
- 3× `<linearGradient>` for the soft white background, dark side panel, and orange divider
- 2× `<filter>` for divider glow and soft panel/text depth
- 2× large `<path>` shapes for the black angled side panel and the white cloaking wedge that hides text while matching the slide background
- 2× `<path>` outline hexagons as light technical decoration on the dark panel
- 5× `<text>` elements for the main revealed typography and right-panel label stack
- Optional nested `<tspan>` inside text if you want mixed emphasis within the revealed phrase

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperWhite" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="62%" stop-color="#fbfbfa"/>
      <stop offset="100%" stop-color="#f2f2ef"/>
    </linearGradient>

    <linearGradient id="panelBlack" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050505"/>
      <stop offset="55%" stop-color="#000000"/>
      <stop offset="100%" stop-color="#121212"/>
    </linearGradient>

    <linearGradient id="orangeBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ff9a3d"/>
      <stop offset="48%" stop-color="#f47a2a"/>
      <stop offset="100%" stop-color="#e85f21"/>
    </linearGradient>

    <filter id="dividerGlow" x="-80%" y="-20%" width="260%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softDepth" x="-12%" y="-12%" width="124%" height="124%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Layer 0: real slide background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#paperWhite)"/>

  <!-- Layer 1: the text being revealed; intentionally extends toward the cloak boundary -->
  <text x="170" y="370" width="580"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="142" font-weight="900" fill="#000000"
        letter-spacing="-5">THANK</text>

  <text x="365" y="490" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="142" font-weight="900" fill="#000000"
        letter-spacing="-5">YOU</text>

  <!-- Layer 2: dark destination panel; it can sit under the cloak -->
  <path d="M850 0 H1280 V720 H830
           L958 425
           C981 374 989 326 970 282
           L850 0 Z"
        fill="url(#panelBlack)" filter="url(#softDepth)"/>

  <!-- Layer 3: the z-order cloak. Same fill as the background, placed above the text. -->
  <path d="M718 0 H850
           L970 282
           C989 326 981 374 958 425
           L830 720
           H718 Z"
        fill="url(#paperWhite)"/>

  <!-- Layer 4: visible origin line that hides the hard edge of the cloak -->
  <rect x="708" y="242" width="20" height="264" rx="0"
        fill="url(#orangeBar)" filter="url(#dividerGlow)"/>

  <!-- Layer 5: foreground content on the dark panel -->
  <text x="982" y="390" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="88" font-weight="900" fill="#ffc20a"
        letter-spacing="-3">PPT</text>

  <text x="986" y="462" width="185"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="900" fill="#ffc20a"
        letter-spacing="-1">TEXT</text>

  <text x="930" y="526" width="290"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="50" font-weight="900" fill="#ffc20a"
        letter-spacing="-1">ANIMATION</text>

  <!-- Technical decoration on the black panel -->
  <path d="M985 148 L1036 148 L1061 192 L1036 236 L985 236 L961 192 Z"
        fill="none" stroke="#ffffff" stroke-width="4" stroke-linejoin="round"/>
  <path d="M1068 114 L1107 114 L1127 148 L1107 183 L1068 183 L1048 148 Z"
        fill="none" stroke="#ffffff" stroke-width="4" stroke-linejoin="round"/>

  <!-- Tiny alignment tick to imply the reveal rail continues beyond the main wordmark -->
  <rect x="711" y="518" width="14" height="28" rx="0" fill="#f47a2a" opacity="0.22"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or `clip-path` on text to crop letters; the editable-PPT translation will not preserve that reliably.
- ❌ Do not rely on real PowerPoint `a:bgFill` from SVG; instead, draw the cloaking shape with the same fill as the visible background.
- ❌ Do not animate in SVG with `<animate>` or `<animateTransform>`; create the static cloaked state, then apply a native PowerPoint Fly In animation manually if motion is needed.
- ❌ Do not place the divider behind the cloak; it must be the topmost edge element so it visually explains the slice.

## Composition notes
- Keep the reveal divider near the visual center-left, around x=700–730, with the main text crossing just underneath the cloak edge.
- The cloaking wedge should match the background exactly and sit above the text but below the divider and foreground panel labels.
- Use a heavy black wordmark on a light field, balanced by a high-contrast dark panel on the right.
- Reserve the right third for secondary messaging and small geometric decoration so the reveal effect remains the primary focal point.