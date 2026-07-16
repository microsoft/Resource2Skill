# SVG Recipe — Split-Panel Stencil Typography

## Visual mechanism
A strict 50/50 split pairs a full-bleed monochrome image with a stark white typography panel. Massive stacked words sit flush to the center seam and are styled as dark recessed “cut-outs,” using offset shadows and subtle highlights to imitate carved stencil depth while remaining editable SVG text.

## SVG primitives needed
- 1× `<image>` for the full-bleed monochrome photo on the left half
- 1× `<clipPath>` with `<rect>` to crop the photo exactly to the left panel
- 3× `<rect>` for the right dark ground layer, white stencil surface, and center seam shadow
- 1× `<linearGradient>` for the seam shadow at the split
- 1× `<linearGradient>` for the recessed typography fill
- 1× `<filter id="letterInsetShadow">` applied to large text to fake tactile depth
- 1× `<filter id="softPanelShadow">` applied to a narrow seam rectangle for editorial separation
- 5× large `<text>` lines for the stacked stencil statement
- 2× small `<text>` labels for understated slide metadata / attribution
- Optional thin `<line>` accents to reinforce the split-layout geometry

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="leftPhotoCrop">
      <rect x="0" y="0" width="640" height="720"/>
    </clipPath>

    <linearGradient id="seamFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.28"/>
      <stop offset="38%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="recessedInk" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3a3a3a"/>
      <stop offset="48%" stop-color="#1f1f1f"/>
      <stop offset="100%" stop-color="#090909"/>
    </linearGradient>

    <filter id="letterInsetShadow" x="-8%" y="-8%" width="120%" height="120%">
      <feOffset dx="5" dy="6" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softPanelShadow" x="-80%" y="-10%" width="260%" height="120%">
      <feOffset dx="-5" dy="0" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- left editorial image panel -->
  <rect x="0" y="0" width="640" height="720" fill="#f4f4f2"/>
  <image
    href="https://images.example.com/monochrome-close-crop-portrait-silhouette.jpg"
    x="0" y="0" width="640" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#leftPhotoCrop)"/>

  <!-- soft wash to desaturate / editorialize the image area -->
  <rect x="0" y="0" width="640" height="720" fill="#ffffff" opacity="0.18"/>
  <rect x="0" y="0" width="640" height="720" fill="#000000" opacity="0.05"/>

  <!-- right panel: dark ground under the stencil surface -->
  <rect x="640" y="0" width="640" height="720" fill="#1e1e1e"/>
  <rect x="640" y="0" width="640" height="720" fill="#ffffff"/>
  <rect x="640" y="0" width="26" height="720" fill="url(#seamFade)" filter="url(#softPanelShadow)"/>

  <!-- small split marker -->
  <line x1="640" y1="54" x2="640" y2="666" stroke="#111111" stroke-opacity="0.16" stroke-width="1"/>

  <!-- recessed stencil typography: duplicate highlight, then dark carved text -->
  <text x="662" y="112" width="560"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="114" font-weight="900" fill="#ffffff" opacity="0.55"
        transform="translate(-3 -3)">STAY</text>
  <text x="662" y="112" width="560"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="114" font-weight="900" fill="url(#recessedInk)"
        filter="url(#letterInsetShadow)">STAY</text>

  <text x="662" y="226" width="590"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="100" font-weight="900" fill="#ffffff" opacity="0.45"
        transform="translate(-3 -3)">HUNGRY</text>
  <text x="662" y="226" width="590"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="100" font-weight="900" fill="url(#recessedInk)"
        filter="url(#letterInsetShadow)">HUNGRY</text>

  <text x="662" y="342" width="560"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="114" font-weight="900" fill="#ffffff" opacity="0.50"
        transform="translate(-3 -3)">STAY</text>
  <text x="662" y="342" width="560"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="114" font-weight="900" fill="url(#recessedInk)"
        filter="url(#letterInsetShadow)">STAY</text>

  <text x="662" y="456" width="560"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="114" font-weight="900" fill="#ffffff" opacity="0.48"
        transform="translate(-3 -3)">FOOL</text>
  <text x="662" y="456" width="560"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="114" font-weight="900" fill="url(#recessedInk)"
        filter="url(#letterInsetShadow)">FOOL</text>

  <text x="662" y="570" width="560"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="114" font-weight="900" fill="#ffffff" opacity="0.48"
        transform="translate(-3 -3)">ISH.</text>
  <text x="662" y="570" width="560"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="114" font-weight="900" fill="url(#recessedInk)"
        filter="url(#letterInsetShadow)">ISH.</text>

  <!-- quiet editorial metadata -->
  <text x="676" y="646" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#111111" opacity="0.42"
        letter-spacing="2">MANIFESTO / 01</text>
  <text x="1030" y="646" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#111111" opacity="0.34"
        text-anchor="end">designed for conviction</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to punch real transparent text holes; the translator hard-fails or ignores mask workflows.
- ❌ Do not apply `clip-path` to text or rectangles to simulate knockout typography; clipping is reliable only on `<image>`.
- ❌ Do not rely on `<foreignObject>` or HTML/CSS blend modes for text masking; they will not translate into editable PowerPoint shapes.
- ❌ Do not use thin/light fonts; the stencil illusion needs ultra-bold, compressed, high-mass letterforms.
- ❌ Do not center the type block inside the right panel; the power of the composition comes from pushing the words close to the split seam.

## Composition notes
- Keep the split exact: left image from `x=0–640`, right stencil panel from `x=640–1280`.
- Place the large typography within 20–35 px of the center seam so the words feel physically anchored to the split.
- Use monochrome or very low-saturation imagery; the visual hierarchy should be dominated by the massive carved type.
- Tight vertical spacing makes the statement read as one architectural block rather than separate headline lines.