# SVG Recipe — Panoramic Typographic Depth with Layered Watermark

## Visual mechanism
A cinematic panoramic background provides a wide atmospheric stage, while an oversized translucent year/wordmark sits behind the crisp title to create depth. The foreground title uses a deep-blue tinted shadow, matching the image palette, so white typography stays legible without looking artificially outlined.

## SVG primitives needed
- 1× `<image>` for the full-slide panoramic sunrise / skyline / horizon background
- 3× `<rect>` for full-slide color grading overlays: navy sky wash, warm horizon glow, bottom vignette
- 2× `<path>` for subtle distant horizon silhouettes that reinforce depth and separate sky from land
- 4× `<text>` for the watermark, main title, spaced subtitle, and metadata line
- 2× `<line>` for delicate metadata divider rules
- 2× `<linearGradient>` for sky and bottom color overlays
- 1× `<radialGradient>` for sunrise / horizon glow
- 2× `<filter>`: one soft tinted drop shadow for the main title, one faint blur/glow for the watermark

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="skyWash" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#071A44" stop-opacity="0.68"/>
      <stop offset="42%" stop-color="#153B78" stop-opacity="0.28"/>
      <stop offset="78%" stop-color="#F2A36F" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#08142E" stop-opacity="0.20"/>
    </linearGradient>

    <radialGradient id="horizonGlow" cx="50%" cy="62%" r="56%">
      <stop offset="0%" stop-color="#FFD19B" stop-opacity="0.44"/>
      <stop offset="38%" stop-color="#D87A5D" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#061638" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="bottomVignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#061638" stop-opacity="0"/>
      <stop offset="58%" stop-color="#061638" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#020813" stop-opacity="0.82"/>
    </linearGradient>

    <filter id="titleShadow" x="-12%" y="-20%" width="124%" height="150%">
      <feOffset dx="0" dy="7" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="5" result="blur"/>
      <feFlood flood-color="#0B1F44" flood-opacity="0.72" result="shadowColor"/>
      <feComposite in="shadowColor" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="watermarkBlur" x="-8%" y="-10%" width="116%" height="125%">
      <feGaussianBlur stdDeviation="1.2"/>
    </filter>
  </defs>

  <image
    x="0" y="0" width="1280" height="720"
    href="https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&amp;w=1920&amp;h=1080&amp;fit=crop"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#skyWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#horizonGlow)"/>

  <path
    d="M0,495 C120,472 206,494 320,475 C448,452 545,485 670,462 C780,442 890,468 1010,450 C1120,434 1205,448 1280,426 L1280,720 L0,720 Z"
    fill="#061638"
    opacity="0.28"/>

  <path
    d="M0,555 C165,520 270,548 410,515 C560,480 690,532 830,500 C995,462 1110,494 1280,470 L1280,720 L0,720 Z"
    fill="#020A19"
    opacity="0.42"/>

  <rect x="0" y="375" width="1280" height="345" fill="url(#bottomVignette)"/>

  <text
    x="640" y="318" width="1180"
    text-anchor="middle"
    font-family="Segoe UI Black, Arial Black, Microsoft YaHei, sans-serif"
    font-size="205"
    font-weight="900"
    letter-spacing="-8"
    fill="#FFFFFF"
    opacity="0.135"
    filter="url(#watermarkBlur)">2026</text>

  <text
    x="640" y="292" width="980"
    text-anchor="middle"
    font-family="Microsoft YaHei, Segoe UI, sans-serif"
    font-size="76"
    font-weight="700"
    fill="#FFFFFF"
    filter="url(#titleShadow)">向新而行</text>

  <text
    x="640" y="356" width="860"
    text-anchor="middle"
    font-family="Georgia, 'Times New Roman', serif"
    font-size="18"
    letter-spacing="8"
    fill="#FFFFFF"
    opacity="0.88">FORWARD STRATEGY REVIEW</text>

  <line x1="385" y1="405" x2="535" y2="405" stroke="#FFFFFF" stroke-width="1.2" opacity="0.72"/>
  <line x1="745" y1="405" x2="895" y2="405" stroke="#FFFFFF" stroke-width="1.2" opacity="0.72"/>

  <text
    x="640" y="413" width="360"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="15"
    letter-spacing="1.6"
    fill="#FFFFFF"
    opacity="0.82">ANNUAL KICK-OFF · JANUARY 2026</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade the photo or watermark; use gradient-filled `<rect>` overlays instead.
- ❌ Do not clip text or apply `clip-path` to text; PPT translation only preserves clipping reliably on `<image>`.
- ❌ Do not use `<textPath>` for arced subtitles; keep all typography centered and horizontal for executive-cover clarity.
- ❌ Do not use pure black shadows on white title text; use a background-tinted navy shadow so the text belongs to the image.
- ❌ Do not overcrowd the sky area with logos, charts, or decorative icons; the depth effect depends on generous negative space.

## Composition notes
- Keep the main typography centered in the upper-middle sky zone, roughly between y=210 and y=415, leaving the horizon and foreground image visible below.
- The watermark should be much larger than the main title, but only 10–18% opaque so it reads as atmosphere, not as competing text.
- Use the deepest color from the panorama for the title shadow, typically navy, indigo, or dark teal rather than black.
- Let the photo carry the emotional tone: wide skyline, mountains, ocean horizon, or sunrise landscape works best because it naturally provides scale and forward motion.