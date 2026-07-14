# SVG Recipe — Cinematic Title Card with Video Background

## Visual mechanism
A full-bleed cinematic video/poster frame is darkened with layered gradients and vignette overlays so large expressive text can sit dramatically over motion. The title is split into staggered calligraphic lines with a small red seal accent, designed so PowerPoint can later apply subtle wipe/fade entrance animations to each editable text shape.

## SVG primitives needed
- 1× `<image>` for the full-screen video poster/background frame; replace with a poster frame from the intended looping video
- 1× `<clipPath>` with a full-slide rounded/rect crop applied to the background image
- 3× `<linearGradient>` for cinematic darkening, warm horizon glow, and text sheen
- 1× `<radialGradient>` for central atmospheric light
- 2× `<filter>` definitions: one soft shadow for text/cards, one glow for atmospheric highlights
- 4× `<rect>` for full-frame color grading overlays, top/bottom letterbox bars, and subtle dark scrims
- 2× `<path>` for organic mist/light beams and ink-brush underline gestures
- 4× `<text>` for staggered title lines, subtitle, and small caption; every text has explicit `width`
- 1× `<rect>` plus 2× `<text>` for the red seal brand/signature accent
- Optional small `<circle>` elements for cinematic dust/bokeh specks

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="fullFrameClip">
      <rect x="0" y="0" width="1280" height="720"/>
    </clipPath>

    <linearGradient id="gradeDark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#02040A" stop-opacity="0.72"/>
      <stop offset="45%" stop-color="#0B1424" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.78"/>
    </linearGradient>

    <linearGradient id="bottomBurn" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.88"/>
    </linearGradient>

    <linearGradient id="titleSheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="48%" stop-color="#F8F0DC"/>
      <stop offset="100%" stop-color="#D9E9FF"/>
    </linearGradient>

    <radialGradient id="moonGlow" cx="58%" cy="34%" r="48%">
      <stop offset="0%" stop-color="#B9D7FF" stop-opacity="0.38"/>
      <stop offset="42%" stop-color="#466B9C" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="atmosGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <!-- Replace this poster with a frame from the actual looping video used in PowerPoint. -->
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/video-poster-cinematic-mountain-river-night-blue-gold.jpg"
         clip-path="url(#fullFrameClip)"/>

  <!-- Cinematic color grade and readable-title scrims -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#gradeDark)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#moonGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomBurn)"/>
  <rect x="0" y="0" width="1280" height="58" fill="#000000" opacity="0.62"/>
  <rect x="0" y="662" width="1280" height="58" fill="#000000" opacity="0.70"/>

  <!-- Atmospheric beams/mist to imply motion in the underlying video -->
  <path d="M-80 470 C180 385, 352 410, 558 344 C795 268, 1004 250, 1370 170 L1370 268 C1030 318, 820 360, 590 438 C340 522, 148 508, -80 586 Z"
        fill="#DCEEFF" opacity="0.10" filter="url(#atmosGlow)"/>
  <path d="M120 530 C298 488, 454 506, 618 468 C790 428, 910 360, 1128 372"
        fill="none" stroke="#F8D78E" stroke-width="3" stroke-linecap="round" opacity="0.36"/>

  <!-- Sparse dust/bokeh particles; keep subtle so they read as cinematic texture -->
  <circle cx="214" cy="178" r="2.4" fill="#FFFFFF" opacity="0.42"/>
  <circle cx="982" cy="148" r="3.2" fill="#FFE7AD" opacity="0.36"/>
  <circle cx="1086" cy="492" r="2.1" fill="#FFFFFF" opacity="0.30"/>
  <circle cx="746" cy="238" r="1.8" fill="#DCEEFF" opacity="0.38"/>
  <circle cx="386" cy="604" r="2.6" fill="#FFE7AD" opacity="0.26"/>

  <!-- Small cinematic eyebrow label -->
  <text x="164" y="176" width="540"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" letter-spacing="5"
        fill="#C9D7E8" opacity="0.86">
    FINAL CHAPTER · STRATEGIC JOURNEY
  </text>
  <line x1="164" y1="196" x2="426" y2="196" stroke="#D7B56D" stroke-width="2" opacity="0.72"/>

  <!-- Main calligraphic title; separate text boxes allow staggered PPT wipe/fade animations -->
  <text x="154" y="326" width="760"
        font-family="KaiTi, STKaiti, Microsoft YaHei, serif"
        font-size="82" font-weight="700"
        fill="url(#titleSheen)" filter="url(#softShadow)">
    道阻且长
  </text>

  <text x="286" y="432" width="770"
        font-family="KaiTi, STKaiti, Microsoft YaHei, serif"
        font-size="82" font-weight="700"
        fill="url(#titleSheen)" filter="url(#softShadow)">
    行则将至
  </text>

  <!-- Brush underline gives the title a handwritten finish without using SVG textPath -->
  <path d="M272 462 C406 486, 588 482, 750 468 C834 461, 920 450, 1012 458"
        fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"
        opacity="0.38" filter="url(#softShadow)"/>
  <path d="M294 479 C468 504, 682 496, 920 474"
        fill="none" stroke="#D7B56D" stroke-width="2.5" stroke-linecap="round"
        opacity="0.68"/>

  <!-- Red seal accent: editable shape + text, positioned like a signature stamp -->
  <rect x="1018" y="364" width="78" height="78" rx="8"
        fill="#A90F13" opacity="0.94" filter="url(#softShadow)"/>
  <text x="1034" y="397" width="48"
        font-family="Microsoft YaHei, Segoe UI, sans-serif"
        font-size="19" font-weight="700" fill="#FFEFE8" opacity="0.96">
    笃
  </text>
  <text x="1034" y="424" width="48"
        font-family="Microsoft YaHei, Segoe UI, sans-serif"
        font-size="19" font-weight="700" fill="#FFEFE8" opacity="0.96">
    行
  </text>

  <!-- Closing subtitle -->
  <text x="164" y="574" width="760"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400"
        fill="#EAF2FF" opacity="0.86">
    Every long road becomes possible when the first step is taken with conviction.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the wipe/fade; create static editable elements in SVG, then apply PowerPoint animations after translation.
- ❌ Do not try to embed an MP4 directly as an SVG `<image>`; use a poster frame in SVG and place the actual looping video as a full-slide PowerPoint media layer behind the imported SVG artwork.
- ❌ Do not use `<mask>` for vignette effects; use editable gradient-filled rectangles instead.
- ❌ Do not use `<textPath>` for calligraphic text; keep each phrase as a normal `<text>` box so it remains editable and animatable.
- ❌ Do not put filters on `<line>` elements; use shadows/glows on text, paths, rectangles, circles, or ellipses only.

## Composition notes
- Keep the video/poster full bleed, but darken it heavily with gradient overlays so the title remains legible over motion.
- Place the main title in the central-left 55–65% of the slide, with line two offset to the right for a cinematic stagger rather than a rigid centered block.
- Reserve the lower-left area for a quiet subtitle; avoid crowding the red seal, which should feel like a signature mark.
- In PowerPoint, animate the eyebrow label, first title line, second title line, seal, and subtitle with staggered fade or wipe-from-left timings of roughly 0.15–0.30 seconds apart.