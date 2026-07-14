# SVG Recipe — Billboard Typography & Cinematic Contrast

## Visual mechanism
Use a dark, cinematic, defocused background as atmosphere, then dominate the slide with oversized white all-caps typography anchored near the lower center. The message should read instantly like a billboard: one punchy phrase, extreme contrast, no supporting clutter.

## SVG primitives needed
- 1× `<image>` for a full-bleed, pre-blurred cinematic background photo
- 4× `<rect>` for dark color wash, vignette bands, and contrast reinforcement behind type
- 3× `<ellipse>` for soft warm light blooms in the background
- 1× `<path>` for a subtle dark foreground silhouette/shape that adds depth without detail
- 2× `<text>` for the billboard headline and subtitle, each with explicit `width`
- 2× `<linearGradient>` for cinematic background wash and lower contrast ramp
- 2× `<radialGradient>` for warm practical-light glows
- 2× `<filter>` using `feGaussianBlur` / `feOffset+feGaussianBlur+feMerge` for glow and text shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinemaWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#180807" stop-opacity="0.82"/>
      <stop offset="42%" stop-color="#05070A" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#130D08" stop-opacity="0.88"/>
    </linearGradient>

    <linearGradient id="bottomRamp" x1="0" y1="360" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.90"/>
    </linearGradient>

    <radialGradient id="warmLamp" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFD36A" stop-opacity="0.95"/>
      <stop offset="38%" stop-color="#C56A1B" stop-opacity="0.46"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="softAmber" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F6B14B" stop-opacity="0.55"/>
      <stop offset="58%" stop-color="#7A2B12" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="typeShadow" x="-5%" y="-20%" width="110%" height="150%">
      <feOffset dx="0" dy="7" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#06070A"/>

  <image
    href="https://images.example.com/preblurred-warm-cinematic-conference-room-no-identifiable-faces.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"
    opacity="0.72"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaWash)"/>

  <ellipse cx="117" cy="564" rx="115" ry="135" fill="url(#warmLamp)" filter="url(#softGlow)" opacity="0.85"/>
  <ellipse cx="440" cy="140" rx="255" ry="75" fill="url(#softAmber)" filter="url(#softGlow)" opacity="0.62"/>
  <ellipse cx="1120" cy="210" rx="230" ry="135" fill="url(#warmLamp)" filter="url(#softGlow)" opacity="0.58"/>

  <path
    d="M536 190 C580 145 681 145 728 194 C779 247 783 347 751 430 C724 500 681 547 637 549 C594 551 540 504 518 433 C492 349 490 239 536 190 Z"
    fill="#07080B"
    opacity="0.42"/>

  <rect x="0" y="0" width="1280" height="135" fill="#000000" opacity="0.30"/>
  <rect x="0" y="420" width="1280" height="300" fill="url(#bottomRamp)"/>

  <text
    x="640" y="598"
    width="1240"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="124"
    font-weight="900"
    letter-spacing="8"
    fill="#FFFFFF"
    filter="url(#typeShadow)">GOOD VS BAD</text>

  <text
    x="640" y="700"
    width="1180"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="74"
    font-weight="900"
    letter-spacing="9"
    fill="#FFFFFF"
    filter="url(#typeShadow)">PRESENTATION SLIDES</text>
</svg>
```

## Avoid in this skill
- ❌ Long paragraphs or multi-bullet layouts; they destroy the billboard-reading effect.
- ❌ Low-contrast type over a busy photo; always add a dark wash or bottom ramp.
- ❌ Sharp, detailed background faces or objects competing with the headline; use pre-blurred/defocused imagery.
- ❌ Thin fonts, small subtitles, or decorative typefaces; use heavy sans-serif typography.
- ❌ Relying on SVG filters to blur the background photo; use a pre-blurred image asset for dependable PPT translation.

## Composition notes
- Keep the headline huge, all caps, and centered horizontally; let it occupy 75–95% of slide width.
- Anchor the main phrase in the lower third for a cinematic trailer/poster feel, leaving moody negative space above.
- Use warm background highlights against black/navy washes so the white type feels crisp and premium.
- If animating in PowerPoint, reveal each text line separately with a simple Fade or Appear build.