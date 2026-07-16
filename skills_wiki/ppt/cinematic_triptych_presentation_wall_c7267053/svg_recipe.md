# SVG Recipe — Cinematic Triptych Presentation Wall

## Visual mechanism
A dark boardroom-style slide is organized as three physical display panels: two dim ambient side screens and one saturated center hero screen. Thick black bezels, subtle glass reflections, wall shadows, and a broadcast-style caption make the content feel like it is being revealed on a premium presentation wall.

## SVG primitives needed
- 1× `<rect>` for the full dark cinematic wall background
- 1× `<path>` for a soft architectural wall glow behind the monitors
- 3× large `<rect>` for monitor shadow plates using `filter`
- 3× large `<rect>` for black monitor bezels
- 3× inner `<rect>` for screen glass surfaces and subtle edge strokes
- 3× `<clipPath>` with rounded rectangles for cropping screen images
- 3× `<image>` for the left ambient panel, center hero reveal, and right ambient panel
- 4× translucent `<path>` / `<rect>` overlays for diagonal glossy reflections and dark side-panel dimming
- 1× `<filter id="wallShadow">` for heavy mounted-screen drop shadows
- 1× `<filter id="softGlow">` for the center screen aura
- Multiple `<linearGradient>` and `<radialGradient>` fills for wall depth, bevel highlights, glass glare, and caption styling
- 4× `<text>` elements with explicit `width` for eyebrow label, main title, subtitle, and small technical caption

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="wallVignette" cx="50%" cy="42%" r="78%">
      <stop offset="0%" stop-color="#27313a"/>
      <stop offset="48%" stop-color="#14191f"/>
      <stop offset="100%" stop-color="#050608"/>
    </radialGradient>

    <linearGradient id="bezelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#20242a"/>
      <stop offset="18%" stop-color="#070809"/>
      <stop offset="72%" stop-color="#0b0c0e"/>
      <stop offset="100%" stop-color="#25292f"/>
    </linearGradient>

    <linearGradient id="glassGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1e3036"/>
      <stop offset="45%" stop-color="#0e151a"/>
      <stop offset="100%" stop-color="#25313a"/>
    </linearGradient>

    <linearGradient id="captionGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0b0d10"/>
      <stop offset="50%" stop-color="#1a1d22"/>
      <stop offset="100%" stop-color="#0b0d10"/>
    </linearGradient>

    <filter id="wallShadow" x="-20%" y="-25%" width="140%" height="160%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="leftScreenClip" clipPathUnits="userSpaceOnUse">
      <rect x="68" y="188" width="234" height="132" rx="4"/>
    </clipPath>
    <clipPath id="centerScreenClip" clipPathUnits="userSpaceOnUse">
      <rect x="324" y="118" width="632" height="356" rx="6"/>
    </clipPath>
    <clipPath id="rightScreenClip" clipPathUnits="userSpaceOnUse">
      <rect x="978" y="188" width="234" height="132" rx="4"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#wallVignette)"/>
  <path d="M120 130 C260 82 420 72 640 78 C860 72 1030 82 1160 130 L1210 530 C1000 584 820 600 640 596 C460 600 275 584 70 530 Z"
        fill="#2b333b" opacity="0.16"/>

  <rect x="36" y="154" width="298" height="200" rx="10" fill="#000000" opacity="0.72" filter="url(#wallShadow)"/>
  <rect x="292" y="82" width="696" height="428" rx="14" fill="#000000" opacity="0.82" filter="url(#wallShadow)"/>
  <rect x="946" y="154" width="298" height="200" rx="10" fill="#000000" opacity="0.72" filter="url(#wallShadow)"/>

  <rect x="44" y="164" width="282" height="176" rx="8" fill="url(#bezelGrad)"/>
  <rect x="304" y="94" width="672" height="404" rx="12" fill="url(#bezelGrad)"/>
  <rect x="954" y="164" width="282" height="176" rx="8" fill="url(#bezelGrad)"/>

  <rect x="68" y="188" width="234" height="132" rx="4" fill="url(#glassGrad)" stroke="#313941" stroke-width="1"/>
  <rect x="324" y="118" width="632" height="356" rx="6" fill="#111820" stroke="#3a444d" stroke-width="1.4"/>
  <rect x="978" y="188" width="234" height="132" rx="4" fill="url(#glassGrad)" stroke="#313941" stroke-width="1"/>

  <image x="68" y="188" width="234" height="132" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/dim-corporate-lobby-reflection-left-panel.jpg"
         clip-path="url(#leftScreenClip)" opacity="0.42"/>
  <image x="324" y="118" width="632" height="356" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/vivid-red-electric-grand-tourer-hero-reveal.jpg"
         clip-path="url(#centerScreenClip)"/>
  <image x="978" y="188" width="234" height="132" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/dim-city-night-reflection-right-panel.jpg"
         clip-path="url(#rightScreenClip)" opacity="0.42"/>

  <rect x="68" y="188" width="234" height="132" rx="4" fill="#020406" opacity="0.48"/>
  <rect x="978" y="188" width="234" height="132" rx="4" fill="#020406" opacity="0.48"/>

  <path d="M70 190 L246 190 L302 247 L302 298 C228 258 154 232 70 224 Z" fill="#ffffff" opacity="0.08"/>
  <path d="M326 120 L746 120 L956 330 L956 402 C780 310 572 240 326 214 Z" fill="#ffffff" opacity="0.10"/>
  <path d="M980 190 L1156 190 L1212 247 L1212 298 C1138 258 1064 232 980 224 Z" fill="#ffffff" opacity="0.08"/>

  <rect x="316" y="110" width="648" height="372" rx="10" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.10"/>
  <rect x="324" y="474" width="632" height="4" fill="#ffcc32" opacity="0.92" filter="url(#softGlow)"/>

  <rect x="410" y="538" width="460" height="78" rx="8" fill="url(#captionGrad)" stroke="#2f353c" stroke-width="1"/>
  <text x="640" y="562" width="460" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="2.5" fill="#f5c542">WORLD PREMIERE DISPLAY</text>
  <text x="640" y="591" width="460" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        fill="#ffffff">THE ELECTRIC GRAND TOURER</text>
  <text x="640" y="614" width="460" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13"
        fill="#aeb7c0">Performance briefing · investor preview · design reveal</text>

  <line x1="44" y1="366" x2="1236" y2="366" stroke="#ffffff" stroke-width="1" opacity="0.05"/>
  <text x="68" y="674" width="260"
        font-family="Segoe UI, Microsoft YaHei" font-size="11" letter-spacing="1.5"
        fill="#66717c">TRIPTYCH WALL / CENTER SCREEN PRIORITY</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to glossy overlay rectangles; the translator only preserves clipping reliably on `<image>`, so size overlays exactly to the screen bounds instead.
- ❌ Using `<mask>` for vignettes or monitor reflections; build the effect with gradients, opacity, and simple paths.
- ❌ Using `skewX`, `skewY`, or matrix transforms for perspective monitors; keep the wall frontal or use manually drawn paths if perspective is essential.
- ❌ Putting shadows on `<line>` elements; use shadow filters on monitor backing rectangles instead.
- ❌ Overloading the slide with text; this technique works best when the screens dominate.

## Composition notes
- Keep the center screen roughly 50–55% of slide width, with side panels much smaller and darker to create a broadcast-wall hierarchy.
- Use heavy negative space above and below the monitor row so the wall feels architectural rather than like a dashboard.
- The brightest saturation should live only inside the center hero image; side panels should be dim, bluish, and reflective.
- Anchor the caption directly beneath the center monitor, aligned to its midpoint, so it reads like a premium lower-third title card.