# SVG Recipe — Continuous Film Strip Timeline

## Visual mechanism
A full-width charcoal film strip cuts horizontally across the slide, with repeating sprocket holes and alternating photo/neutral frames creating a cinematic left-to-right timeline. Captions sit beneath the strip so the strip remains the visual “reel” while milestone text reads like scene notes.

## SVG primitives needed
- 1× `<rect>` for the clean slide background
- 1× `<ellipse>` with radial gradient for a soft stage-light glow behind the strip
- 1× `<rect>` for the main film strip body
- 36× `<rect>` for white rounded sprocket holes with subtle shadow
- 7× `<rect>` for frame wells, neutral frames, borders, and dividers
- 3× `<image>` clipped into rounded photo frames
- 3× `<clipPath>` using rounded `<rect>` crops for editable photo cards
- 1× `<linearGradient>` for the charcoal film body
- 1× `<radialGradient>` for the background glow
- 2× `<filter>` for film-strip shadow and sprocket-hole depth
- 4× `<line>` for milestone connectors
- 8× `<text>` blocks with explicit `width` for title, labels, and captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="filmGrad" x1="0" y1="190" x2="0" y2="510" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#383838"/>
      <stop offset="0.48" stop-color="#242424"/>
      <stop offset="1" stop-color="#171717"/>
    </linearGradient>
    <radialGradient id="stageGlow" cx="50%" cy="46%" r="60%">
      <stop offset="0" stop-color="#EEF3FF"/>
      <stop offset="0.55" stop-color="#F8FAFC"/>
      <stop offset="1" stop-color="#FFFFFF"/>
    </radialGradient>
    <filter id="stripShadow" x="-5%" y="-15%" width="110%" height="135%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="holeDepth" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="-3" dy="-3" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="clipFounding"><rect x="105" y="255" width="205" height="154" rx="10"/></clipPath>
    <clipPath id="clipScale"><rect x="575" y="255" width="205" height="154" rx="10"/></clipPath>
    <clipPath id="clipFuture"><rect x="1045" y="255" width="205" height="154" rx="10"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <ellipse cx="640" cy="342" rx="620" ry="255" fill="url(#stageGlow)"/>

  <text x="70" y="76" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#151515">
    Continuous Film Strip Timeline
  </text>
  <text x="72" y="110" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">
    A cinematic milestone reel: each frame advances the company story one scene at a time.
  </text>

  <rect x="-30" y="190" width="1340" height="320" fill="url(#filmGrad)" filter="url(#stripShadow)"/>

  <rect x="-22" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="53" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="128" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="203" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="278" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="353" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="428" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="503" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="578" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="653" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="728" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="803" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="878" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="953" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="1028" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="1103" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="1178" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="1253" y="214" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>

  <rect x="-22" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="53" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="128" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="203" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="278" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="353" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="428" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="503" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="578" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="653" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="728" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="803" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="878" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="953" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="1028" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="1103" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="1178" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>
  <rect x="1253" y="438" width="36" height="48" rx="9" fill="#FFFFFF" filter="url(#holeDepth)"/>

  <rect x="-135" y="248" width="205" height="168" rx="12" fill="#555555"/>
  <rect x="100" y="250" width="215" height="164" rx="14" fill="#0F0F0F"/>
  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=900&amp;h=650&amp;fit=crop" x="105" y="255" width="205" height="154" clip-path="url(#clipFounding)"/>
  <rect x="335" y="250" width="215" height="164" rx="14" fill="#646464"/>
  <rect x="575" y="250" width="215" height="164" rx="14" fill="#0F0F0F"/>
  <image href="https://images.unsplash.com/photo-1556761175-b413da4baf72?w=900&amp;h=650&amp;fit=crop" x="575" y="255" width="205" height="154" clip-path="url(#clipScale)"/>
  <rect x="810" y="250" width="215" height="164" rx="14" fill="#646464"/>
  <rect x="1040" y="250" width="215" height="164" rx="14" fill="#0F0F0F"/>
  <image href="https://images.unsplash.com/photo-1518770660439-4636190af475?w=900&amp;h=650&amp;fit=crop" x="1045" y="255" width="205" height="154" clip-path="url(#clipFuture)"/>

  <rect x="346" y="262" width="193" height="140" rx="9" fill="#747474"/>
  <rect x="821" y="262" width="193" height="140" rx="9" fill="#747474"/>
  <path d="M382 334 C408 306, 441 305, 468 331 C488 351, 512 348, 526 324" fill="none" stroke="#BDBDBD" stroke-width="5" stroke-linecap="round"/>
  <path d="M850 350 L885 314 L919 342 L953 302 L1000 368" fill="none" stroke="#BDBDBD" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <line x1="205" y1="510" x2="205" y2="545" stroke="#111827" stroke-width="2"/>
  <line x1="442" y1="510" x2="442" y2="545" stroke="#9CA3AF" stroke-width="2" stroke-dasharray="5 5"/>
  <line x1="682" y1="510" x2="682" y2="545" stroke="#111827" stroke-width="2"/>
  <line x1="918" y1="510" x2="918" y2="545" stroke="#9CA3AF" stroke-width="2" stroke-dasharray="5 5"/>

  <text x="105" y="575" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#111827">2014 · Founding</text>
  <text x="105" y="602" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">The first team forms around a focused product vision.</text>
  <text x="345" y="575" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#111827">2017 · Product Fit</text>
  <text x="345" y="602" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">An empty frame creates breathing room for a key inflection point.</text>
  <text x="575" y="575" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#111827">2020 · Scale</text>
  <text x="575" y="602" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Operations mature and the story gains commercial momentum.</text>
  <text x="815" y="575" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#111827">2024 · Platform</text>
  <text x="815" y="602" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Neutral frames can carry charts, icons, or short evidence notes.</text>
</svg>
```

## Avoid in this skill
- ❌ Using SVG `<pattern>` to generate sprocket holes; it will not translate reliably to editable PowerPoint.
- ❌ Using `<mask>` or clip paths on the film-strip body to punch real holes; instead, place white rounded rectangles over the strip.
- ❌ Using `<use>` to repeat perforations; duplicate the rounded rectangles explicitly.
- ❌ Applying filters to `<line>` milestone connectors; shadows/glows on lines may be dropped.
- ❌ Moving the film strip vertically between slides; it breaks the continuous Push-transition illusion.

## Composition notes
- Keep the film strip locked to the same `y` and height on every slide; only the frame content and captions change between “reel segments.”
- Let the strip occupy roughly the middle 40–45% of slide height, leaving top space for a headline and bottom space for milestone captions.
- Alternate vivid photo frames with neutral gray frames to create rhythm and prevent the timeline from feeling overcrowded.
- For multi-slide continuity, allow partial frames to enter or exit at the slide edges and use a horizontal PowerPoint Push transition.