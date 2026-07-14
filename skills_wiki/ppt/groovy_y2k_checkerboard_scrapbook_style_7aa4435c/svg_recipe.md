# SVG Recipe — Groovy Y2K Checkerboard Scrapbook Style

## Visual mechanism
A retro scrapbook slide built from a big pastel checkerboard field, layered paper cutouts, wavy blobs, grid-paper panels, and hard-offset “sticker” typography. Data is presented inside rounded note cards with thick navy borders so charts feel playful while remaining editable and readable.

## SVG primitives needed
- 1× `<rect>` for the pastel base background.
- 20–30× `<rect>` for manually drawn checkerboard tiles, avoiding non-translatable pattern fills.
- 2× `<path>` for large wavy abstract blob stickers.
- 3–5× `<path>` for concentric retro corner rings.
- 3× `<rect>` for stacked rounded scrapbook cards and hard offset shadows.
- 12–20× `<line>` for grid-paper ruling inside the chart card.
- 5× `<rect>` for rounded bar-chart columns.
- 1× `<polyline>`-like `<path>` for a simple trend line accent.
- 2× `<circle>` / `<ellipse>` for floating sticker dots and Y2K bubble accents.
- 1× `<image>` clipped by a rounded-rectangle `<clipPath>` for an optional scrapbook photo/UI screenshot sticker.
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` for soft lifted paper shadows.
- Multiple duplicated `<text>` elements for hard navy sticker shadows; every `<text>` must include an explicit `width`.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F5F7EE"/>
      <stop offset="100%" stop-color="#DDEBFA"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#789FD0"/>
      <stop offset="100%" stop-color="#BFD9F1"/>
    </linearGradient>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="8" dy="9" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="roundedPhotoClip">
      <rect x="932" y="420" width="198" height="146" rx="28"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#BDD4E7"/>
  <g fill="#8DB0D3">
    <rect x="160" y="0" width="160" height="160"/><rect x="480" y="0" width="160" height="160"/><rect x="800" y="0" width="160" height="160"/><rect x="1120" y="0" width="160" height="160"/>
    <rect x="0" y="160" width="160" height="160"/><rect x="320" y="160" width="160" height="160"/><rect x="640" y="160" width="160" height="160"/><rect x="960" y="160" width="160" height="160"/>
    <rect x="160" y="320" width="160" height="160"/><rect x="480" y="320" width="160" height="160"/><rect x="800" y="320" width="160" height="160"/><rect x="1120" y="320" width="160" height="160"/>
    <rect x="0" y="480" width="160" height="160"/><rect x="320" y="480" width="160" height="160"/><rect x="640" y="480" width="160" height="160"/><rect x="960" y="480" width="160" height="160"/>
    <rect x="160" y="640" width="160" height="80"/><rect x="480" y="640" width="160" height="80"/><rect x="800" y="640" width="160" height="80"/><rect x="1120" y="640" width="160" height="80"/>
  </g>

  <path d="M-20 610 C80 560 120 660 210 605 C285 560 310 640 390 600 L390 750 L-20 750 Z" fill="#F5F7EE" stroke="#2B3E62" stroke-width="8"/>
  <path d="M1000 -40 C1080 40 1175 -30 1250 70 C1315 155 1240 235 1320 300 L1320 -40 Z" fill="#F5F7EE" stroke="#2B3E62" stroke-width="8"/>

  <g transform="translate(0 418)">
    <path d="M0 260 L0 70 A190 190 0 0 1 190 260 Z" fill="#2B3E62"/>
    <path d="M42 260 L42 112 A148 148 0 0 1 190 260 Z" fill="#BDD4E7"/>
    <path d="M82 260 L82 152 A108 108 0 0 1 190 260 Z" fill="#2B3E62"/>
    <path d="M120 260 L120 190 A70 70 0 0 1 190 260 Z" fill="#8DB0D3"/>
  </g>
  <g transform="translate(1280 302) rotate(180)">
    <path d="M0 260 L0 70 A190 190 0 0 1 190 260 Z" fill="#2B3E62"/>
    <path d="M42 260 L42 112 A148 148 0 0 1 190 260 Z" fill="#BDD4E7"/>
    <path d="M82 260 L82 152 A108 108 0 0 1 190 260 Z" fill="#2B3E62"/>
    <path d="M120 260 L120 190 A70 70 0 0 1 190 260 Z" fill="#8DB0D3"/>
  </g>

  <rect x="166" y="108" width="948" height="504" rx="38" fill="#2B3E62"/>
  <rect x="146" y="88" width="948" height="504" rx="38" fill="url(#paperBlue)" stroke="#2B3E62" stroke-width="8" filter="url(#softShadow)"/>

  <g stroke="#AFC8E2" stroke-width="2">
    <line x1="190" y1="228" x2="1052" y2="228"/><line x1="190" y1="276" x2="1052" y2="276"/><line x1="190" y1="324" x2="1052" y2="324"/><line x1="190" y1="372" x2="1052" y2="372"/>
    <line x1="190" y1="420" x2="1052" y2="420"/><line x1="190" y1="468" x2="1052" y2="468"/><line x1="190" y1="516" x2="1052" y2="516"/>
    <line x1="260" y1="190" x2="260" y2="548"/><line x1="340" y1="190" x2="340" y2="548"/><line x1="420" y1="190" x2="420" y2="548"/><line x1="500" y1="190" x2="500" y2="548"/>
    <line x1="580" y1="190" x2="580" y2="548"/><line x1="660" y1="190" x2="660" y2="548"/><line x1="740" y1="190" x2="740" y2="548"/><line x1="820" y1="190" x2="820" y2="548"/><line x1="900" y1="190" x2="900" y2="548"/>
  </g>

  <rect x="267" y="126" width="554" height="88" rx="44" fill="#2B3E62"/>
  <rect x="250" y="110" width="554" height="88" rx="44" fill="#BDD4E7" stroke="#2B3E62" stroke-width="7"/>
  <text x="284" y="174" width="520" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="44" fill="#2B3E62" letter-spacing="1">PROJECT PULSE</text>
  <text x="278" y="167" width="520" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="44" fill="#F5F7EE" letter-spacing="1">PROJECT PULSE</text>

  <text x="215" y="258" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#2B3E62">Weekly creative traction</text>
  <text x="215" y="292" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#2B3E62">Sticker-style data cards keep the chart playful without losing executive clarity.</text>

  <g transform="translate(215 340)">
    <line x1="0" y1="150" x2="520" y2="150" stroke="#2B3E62" stroke-width="5"/>
    <rect x="34" y="66" width="56" height="84" rx="18" fill="url(#barGrad)" stroke="#2B3E62" stroke-width="5"/>
    <rect x="124" y="28" width="56" height="122" rx="18" fill="url(#barGrad)" stroke="#2B3E62" stroke-width="5"/>
    <rect x="214" y="82" width="56" height="68" rx="18" fill="url(#barGrad)" stroke="#2B3E62" stroke-width="5"/>
    <rect x="304" y="42" width="56" height="108" rx="18" fill="url(#barGrad)" stroke="#2B3E62" stroke-width="5"/>
    <rect x="394" y="12" width="56" height="138" rx="18" fill="url(#barGrad)" stroke="#2B3E62" stroke-width="5"/>
    <path d="M62 60 C135 18 190 88 242 70 S340 34 422 18" fill="none" stroke="#F5F7EE" stroke-width="8" stroke-linecap="round"/>
    <path d="M62 60 C135 18 190 88 242 70 S340 34 422 18" fill="none" stroke="#2B3E62" stroke-width="3" stroke-linecap="round" stroke-dasharray="10 9"/>
    <text x="24" y="184" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#2B3E62">IDEA     DESIGN     COPY     SOCIAL     LAUNCH</text>
  </g>

  <rect x="906" y="390" width="250" height="206" rx="32" fill="#2B3E62"/>
  <rect x="884" y="370" width="250" height="206" rx="32" fill="#F5F7EE" stroke="#2B3E62" stroke-width="7"/>
  <image href="https://images.example.com/y2k-scrapbook-team-photo-blue-toned.jpg" x="932" y="420" width="198" height="146" clip-path="url(#roundedPhotoClip)"/>
  <text x="916" y="408" width="204" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="22" fill="#2B3E62">TEAM SNAP</text>

  <circle cx="930" cy="142" r="25" fill="#F5F7EE" stroke="#2B3E62" stroke-width="6"/>
  <circle cx="973" cy="186" r="13" fill="#2B3E62"/>
  <ellipse cx="108" cy="116" rx="42" ry="24" fill="#F5F7EE" stroke="#2B3E62" stroke-width="6" transform="rotate(-18 108 116)"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` for the checkerboard or graph paper; manually draw tiles and grid lines so the result stays editable in PowerPoint.
- ❌ Soft blurred text shadows for the title; the Y2K sticker effect depends on duplicated text with a crisp offset.
- ❌ Clipping blobs or cards with `clip-path`; clipping should only be applied to `<image>` elements.
- ❌ Overly corporate chart styling such as thin gray axes, tiny labels, and muted neutral palettes.
- ❌ `skewX`, `skewY`, or matrix transforms for scrapbook tilts; use small `rotate(angle cx cy)` transforms instead.

## Composition notes
- Keep the largest rounded paper card centered, occupying roughly 70–80% of the slide, with patterned checkerboard visible around all edges.
- Use navy as the structural color for borders, hard shadows, labels, and chart axes; use baby blue and off-white for fill rhythm.
- Let decorative blobs and concentric rings sit partly off-canvas so they feel like oversized stickers framing the data.
- Put the chart in the lower-left or center-left of the card, then balance it with a small photo, stat, or label sticker on the right.