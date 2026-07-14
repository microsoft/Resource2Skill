# SVG Recipe — Tech-Geometric Reveal & Neon Layered Typography

## Visual mechanism
A cinematic black tech cover uses a clipped city/tech photo revealed only through angular triangular shards on the right, while the title is built from offset layers: neon outline behind, dark glitch shadow, and crisp white foreground text. The combination of hard geometric cuts, high contrast, and small chromatic offsets creates a futuristic PowerPoint/product-launch mood.

## SVG primitives needed
- 1× `<rect>` for the black slide base
- 2× `<radialGradient>` / `<linearGradient>` for subtle background glow and logo color
- 1× `<filter id="softGlow">` applied to neon typography and fine geometric accents
- 1× `<filter id="textShadow">` applied to dark offset title layers
- 6× `<clipPath>` with triangular/custom polygon paths to crop the same city image into separate shards
- 6× `<image>` instances using the same hero photo, each clipped to a different triangular shard
- 10× `<path>` for thick black geometric dividers, triangle borders, and angled tech linework
- 3× `<circle>` / `<rect>` / `<text>` elements for a simple editable PowerPoint-style brand mark
- 8× layered `<text>` elements for neon outline, dark extrusion, main title, subtitle, and micro-labels
- Several `<line>` elements for small cyber UI ticks and diagonal accent strokes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="72%" cy="48%" r="60%">
      <stop offset="0%" stop-color="#10293A" stop-opacity="0.75"/>
      <stop offset="45%" stop-color="#061017" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="1"/>
    </radialGradient>

    <linearGradient id="pptOrange" x1="150" y1="125" x2="240" y2="205">
      <stop offset="0%" stop-color="#FF8B59"/>
      <stop offset="100%" stop-color="#D64222"/>
    </linearGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="6" dy="7" result="off"/>
      <feGaussianBlur in="off" stdDeviation="1.4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="triTop">
      <path d="M1120 16 L1240 220 L1000 220 Z"/>
    </clipPath>
    <clipPath id="triMidL">
      <path d="M968 246 L1108 486 L828 486 Z"/>
    </clipPath>
    <clipPath id="triMidR">
      <path d="M1122 246 L1264 486 L982 486 Z"/>
    </clipPath>
    <clipPath id="triLowL">
      <path d="M828 506 L966 714 L690 714 Z"/>
    </clipPath>
    <clipPath id="triLowM">
      <path d="M970 506 L1110 714 L832 714 Z"/>
    </clipPath>
    <clipPath id="triLowR">
      <path d="M1112 506 L1260 714 L966 714 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <image href="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&amp;fit=crop&amp;w=1600&amp;q=85" x="660" y="-40" width="720" height="820" preserveAspectRatio="xMidYMid slice" clip-path="url(#triTop)"/>
  <image href="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&amp;fit=crop&amp;w=1600&amp;q=85" x="660" y="-40" width="720" height="820" preserveAspectRatio="xMidYMid slice" clip-path="url(#triMidL)"/>
  <image href="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&amp;fit=crop&amp;w=1600&amp;q=85" x="660" y="-40" width="720" height="820" preserveAspectRatio="xMidYMid slice" clip-path="url(#triMidR)"/>
  <image href="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&amp;fit=crop&amp;w=1600&amp;q=85" x="660" y="-40" width="720" height="820" preserveAspectRatio="xMidYMid slice" clip-path="url(#triLowL)"/>
  <image href="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&amp;fit=crop&amp;w=1600&amp;q=85" x="660" y="-40" width="720" height="820" preserveAspectRatio="xMidYMid slice" clip-path="url(#triLowM)"/>
  <image href="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&amp;fit=crop&amp;w=1600&amp;q=85" x="660" y="-40" width="720" height="820" preserveAspectRatio="xMidYMid slice" clip-path="url(#triLowR)"/>

  <path d="M1120 16 L1240 220 L1000 220 Z" fill="none" stroke="#000000" stroke-width="22" stroke-linejoin="miter"/>
  <path d="M968 246 L1108 486 L828 486 Z" fill="none" stroke="#000000" stroke-width="22" stroke-linejoin="miter"/>
  <path d="M1122 246 L1264 486 L982 486 Z" fill="none" stroke="#000000" stroke-width="22" stroke-linejoin="miter"/>
  <path d="M828 506 L966 714 L690 714 Z" fill="none" stroke="#000000" stroke-width="22" stroke-linejoin="miter"/>
  <path d="M970 506 L1110 714 L832 714 Z" fill="none" stroke="#000000" stroke-width="22" stroke-linejoin="miter"/>
  <path d="M1112 506 L1260 714 L966 714 Z" fill="none" stroke="#000000" stroke-width="22" stroke-linejoin="miter"/>

  <path d="M1120 16 L1240 220 L1000 220 Z" fill="none" stroke="#8BCB42" stroke-width="1.4" stroke-opacity="0.55"/>
  <path d="M968 246 L1108 486 L828 486 Z" fill="none" stroke="#00BFFF" stroke-width="1.2" stroke-opacity="0.45"/>
  <path d="M970 506 L1110 714 L832 714 Z" fill="none" stroke="#8BCB42" stroke-width="1.2" stroke-opacity="0.45"/>

  <line x1="508" y1="248" x2="758" y2="248" stroke="#8BCB42" stroke-width="1.3" stroke-opacity="0.55" filter="url(#softGlow)"/>
  <line x1="520" y1="258" x2="742" y2="258" stroke="#8BCB42" stroke-width="1" stroke-opacity="0.35"/>
  <line x1="94" y1="566" x2="355" y2="566" stroke="#00BFFF" stroke-width="1.2" stroke-opacity="0.22"/>
  <line x1="82" y1="579" x2="205" y2="579" stroke="#8BCB42" stroke-width="1.2" stroke-opacity="0.32"/>
  <path d="M70 620 L205 620 L230 647 L455 647" fill="none" stroke="#163A44" stroke-width="2" stroke-opacity="0.9"/>
  <path d="M92 96 L210 96 L236 122 L410 122" fill="none" stroke="#153A20" stroke-width="2" stroke-opacity="0.8"/>

  <circle cx="200" cy="160" r="42" fill="url(#pptOrange)"/>
  <rect x="150" y="136" width="49" height="48" rx="5" fill="#D94A28" stroke="#8D2A18" stroke-width="2"/>
  <text x="163" y="172" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">P</text>
  <text x="276" y="176" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="300" fill="#FFFFFF" opacity="0.95">PowerPoint</text>

  <text x="149" y="354" width="650" font-family="Microsoft YaHei, Segoe UI" font-size="112" font-weight="900" fill="none" stroke="#8BCB42" stroke-width="2.2" stroke-opacity="0.9" letter-spacing="7" filter="url(#softGlow)">PPT 封面</text>
  <text x="158" y="360" width="650" font-family="Microsoft YaHei, Segoe UI" font-size="112" font-weight="900" fill="#050505" stroke="#050505" stroke-width="4" letter-spacing="7" filter="url(#textShadow)">PPT 封面</text>
  <text x="142" y="352" width="650" font-family="Microsoft YaHei, Segoe UI" font-size="112" font-weight="900" fill="#FFFFFF" letter-spacing="7">PPT 封面</text>

  <text x="153" y="513" width="620" font-family="Microsoft YaHei, Segoe UI" font-size="96" font-weight="900" fill="none" stroke="#8BCB42" stroke-width="2" stroke-opacity="0.9" letter-spacing="6" filter="url(#softGlow)">四个小妙招</text>
  <text x="161" y="519" width="620" font-family="Microsoft YaHei, Segoe UI" font-size="96" font-weight="900" fill="#050505" stroke="#050505" stroke-width="4" letter-spacing="6" filter="url(#textShadow)">四个小妙招</text>
  <text x="145" y="511" width="620" font-family="Microsoft YaHei, Segoe UI" font-size="96" font-weight="900" fill="#FFFFFF" letter-spacing="6">四个小妙招</text>

  <text x="150" y="628" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#00BFFF" letter-spacing="3">GEOMETRIC REVEAL / NEON TYPE SYSTEM</text>
  <text x="150" y="654" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#C9D3D8" opacity="0.72">Product launch cover style · cyber-security report · technology keynote</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to reveal the triangular photo grid; define multiple `<clipPath>` shapes and apply them directly to `<image>` elements.
- ❌ Do not apply `clip-path` to rectangles or paths for the shard effect; only clipped images translate reliably.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to fake italic/glitch text; create the effect with small x/y offsets and stroke-only duplicate text layers.
- ❌ Do not use `marker-end` on geometric connector paths; use plain `<line>` or `<path>` strokes without arrowheads.
- ❌ Do not rely on one giant image with black polygons on top if editability matters; separate clipped image shards plus editable divider paths are easier to tune in PowerPoint.

## Composition notes
- Keep the left 55–60% of the slide mostly black so the layered title remains dominant and readable.
- Cluster triangular image shards on the right edge; let some shards crop off-canvas for a more cinematic, oversized feel.
- Use very small neon offsets: 6–10 px is enough for the green/blue outline to read as a glitch layer without making the title blurry.
- Repeat the accent color in three places only: title outline, thin tech lines, and selected triangle borders; this keeps the cyber palette controlled rather than noisy.