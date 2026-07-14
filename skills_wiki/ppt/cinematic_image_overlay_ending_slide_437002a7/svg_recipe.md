# SVG Recipe — Cinematic Image Overlay Ending Slide

## Visual mechanism
A full-bleed emotional photograph is darkened with a translucent black overlay and vignette, then finished with oversized centered white typography. The slide feels cinematic because the image carries atmosphere while the typography remains stark, quiet, and highly legible.

## SVG primitives needed
- 1× `<image>` for the edge-to-edge photographic background
- 1× `<rect>` for the global semi-transparent black readability mask
- 2× `<rect>` with gradient fills for cinematic top/bottom shading and vignette depth
- 2× `<rect>` for subtle letterbox bars
- 1× `<rect>` for the thin centered divider rule
- 3× `<text>` blocks for main title, spaced subtitle, and metadata/footer line
- 2× `<path>` for small symmetrical editorial divider accents
- 1× `<radialGradient>` for the central-to-edge vignette
- 1× `<linearGradient>` for bottom atmospheric fade
- 1× `<filter id="titleShadow">` applied to text for soft depth against the photo

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="vignette" cx="50%" cy="46%" r="72%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </radialGradient>

    <linearGradient id="bottomFade" x1="0" y1="220" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.68"/>
    </linearGradient>

    <filter id="titleShadow" x="-15%" y="-20%" width="130%" height="150%">
      <feOffset dx="0" dy="8" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed cinematic photograph -->
  <image
    href="https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&amp;fit=crop&amp;w=1920&amp;q=90"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Dark readability system -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.62"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomFade)"/>

  <!-- Subtle letterbox bars for cinematic framing -->
  <rect x="0" y="0" width="1280" height="58" fill="#000000" opacity="0.42"/>
  <rect x="0" y="662" width="1280" height="58" fill="#000000" opacity="0.42"/>

  <!-- Main editorial typography -->
  <text
    x="640" y="326"
    width="1040"
    text-anchor="middle"
    font-family="Georgia, 'Times New Roman', serif"
    font-size="108"
    font-weight="700"
    letter-spacing="3"
    fill="#FFFFFF"
    filter="url(#titleShadow)">THANKS</text>

  <!-- Hairline divider with small editorial accents -->
  <rect x="515" y="374" width="250" height="2" fill="#FFFFFF" opacity="0.95"/>

  <path d="M486 375 C470 375, 462 375, 448 375"
        fill="none"
        stroke="#FFFFFF"
        stroke-width="1.2"
        stroke-linecap="round"
        opacity="0.72"/>

  <path d="M794 375 C810 375, 818 375, 832 375"
        fill="none"
        stroke="#FFFFFF"
        stroke-width="1.2"
        stroke-linecap="round"
        opacity="0.72"/>

  <!-- Spaced bilingual subtitle -->
  <text
    x="640" y="425"
    width="760"
    text-anchor="middle"
    font-family="'Segoe UI', 'Microsoft YaHei', sans-serif"
    font-size="24"
    font-weight="400"
    letter-spacing="8"
    fill="#E8E8E8"
    opacity="0.96">感 谢 您 的 观 看</text>

  <!-- Quiet metadata / presenter line -->
  <text
    x="640" y="548"
    width="860"
    text-anchor="middle"
    font-family="'Segoe UI', 'Microsoft YaHei', sans-serif"
    font-size="17"
    font-weight="300"
    letter-spacing="1.6"
    fill="#CFCFCF"
    opacity="0.82">汇报人：Bobbie  |  202X年12月  |  STRATEGY REVIEW</text>

  <!-- Minimal bottom cue, useful for Q&A or final contact -->
  <text
    x="640" y="621"
    width="760"
    text-anchor="middle"
    font-family="'Segoe UI', 'Microsoft YaHei', sans-serif"
    font-size="14"
    font-weight="400"
    letter-spacing="3.5"
    fill="#FFFFFF"
    opacity="0.58">QUESTIONS &amp; DISCUSSION</text>
</svg>
```

## Avoid in this skill
- ❌ Do not place white text directly on the photograph without the dark overlay; busy image detail will destroy legibility.
- ❌ Do not use `<mask>` for the vignette; use translucent `<rect>` layers with gradients instead.
- ❌ Do not overfill the ending slide with bullets, charts, or logos; the power comes from restraint.
- ❌ Do not use small main typography. The title should feel like a cinematic end card, not a normal slide heading.
- ❌ Do not apply filters to divider `<line>` elements; use a thin `<rect>` or plain stroked `<path>` instead.

## Composition notes
- Keep all major text centered on the vertical axis, with the title slightly above exact center and metadata pushed lower.
- Reserve at least 45–55% of the slide as dark photographic negative space around the title.
- Use one emotional photo, one dark mask, one large serif title, and one thin divider; this gives the slide its premium editorial rhythm.
- If the photo is very bright, raise the black overlay opacity toward 0.70; if the photo is already dark, 0.50–0.60 is usually enough.