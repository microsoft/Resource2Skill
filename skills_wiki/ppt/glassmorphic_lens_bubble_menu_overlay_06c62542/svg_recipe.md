# SVG Recipe — Glassmorphic "Lens Bubble" Menu Overlay

## Visual mechanism
A sharp full-bleed photo is overlaid with circular “lens” bubbles that contain a blurred duplicate of the same photo, clipped to each circle. Semi-transparent white tints, thin borders, glow, centered icons, and white menu labels make the bubbles feel like premium frosted-glass navigation buttons.

## SVG primitives needed
- 1× full-slide `<image>` for the sharp photographic background
- 6× clipped `<image>` duplicates for blurred-background lens interiors
- 6× `<clipPath>` with `<circle>` for circular image crops
- 6× translucent `<circle>` overlays for milky glass tint
- 6× stroked `<circle>` rings for crisp lens borders
- 1× `<filter id="softGlow">` applied to bubble circles for subtle depth
- 1× `<linearGradient>` for the dark slide readability wash
- 1× `<radialGradient>` for highlight sheen inside bubbles
- Multiple `<path>`, `<line>`, and `<circle>` elements for simple white navigation icons
- 7× `<text>` blocks with explicit `width` attributes for title and menu labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgShade" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.34"/>
      <stop offset="45%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.42"/>
    </linearGradient>

    <radialGradient id="lensSheen" cx="32%" cy="22%" r="78%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.34"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.04"/>
    </radialGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="8" result="blur"/>
      <feOffset dx="0" dy="8" result="offsetBlur"/>
      <feMerge>
        <feMergeNode in="offsetBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipMission"><circle cx="260" cy="310" r="92"/></clipPath>
    <clipPath id="clipProblem"><circle cx="510" cy="310" r="92"/></clipPath>
    <clipPath id="clipSolution"><circle cx="760" cy="310" r="92"/></clipPath>
    <clipPath id="clipMarket"><circle cx="1020" cy="310" r="92"/></clipPath>
    <clipPath id="clipModel"><circle cx="420" cy="530" r="92"/></clipPath>
    <clipPath id="clipTeam"><circle cx="860" cy="530" r="92"/></clipPath>
  </defs>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1600607688969-a5bfcd646154?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgShade)"/>

  <text x="640" y="92" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="600"
        fill="#ffffff" letter-spacing="0.5">Table of Contents</text>
  <text x="640" y="128" width="650" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16"
        fill="#ffffff" opacity="0.78" letter-spacing="1.8">SELECT A STRATEGIC LENS</text>

  <!-- Blurred photo lenses: use a pre-blurred duplicate of the exact same background image -->
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipMission)"
         href="https://images.example.com/interior-photo-same-crop-gaussian-blur-25px.jpg"/>
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipProblem)"
         href="https://images.example.com/interior-photo-same-crop-gaussian-blur-25px.jpg"/>
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipSolution)"
         href="https://images.example.com/interior-photo-same-crop-gaussian-blur-25px.jpg"/>
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipMarket)"
         href="https://images.example.com/interior-photo-same-crop-gaussian-blur-25px.jpg"/>
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipModel)"
         href="https://images.example.com/interior-photo-same-crop-gaussian-blur-25px.jpg"/>
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipTeam)"
         href="https://images.example.com/interior-photo-same-crop-gaussian-blur-25px.jpg"/>

  <!-- Glass tint and rim layers -->
  <circle cx="260" cy="310" r="92" fill="url(#lensSheen)" stroke="#ffffff" stroke-opacity="0.58" stroke-width="1.4" filter="url(#softGlow)"/>
  <circle cx="510" cy="310" r="92" fill="url(#lensSheen)" stroke="#ffffff" stroke-opacity="0.58" stroke-width="1.4" filter="url(#softGlow)"/>
  <circle cx="760" cy="310" r="92" fill="url(#lensSheen)" stroke="#ffffff" stroke-opacity="0.58" stroke-width="1.4" filter="url(#softGlow)"/>
  <circle cx="1020" cy="310" r="92" fill="url(#lensSheen)" stroke="#ffffff" stroke-opacity="0.58" stroke-width="1.4" filter="url(#softGlow)"/>
  <circle cx="420" cy="530" r="92" fill="url(#lensSheen)" stroke="#ffffff" stroke-opacity="0.58" stroke-width="1.4" filter="url(#softGlow)"/>
  <circle cx="860" cy="530" r="92" fill="url(#lensSheen)" stroke="#ffffff" stroke-opacity="0.58" stroke-width="1.4" filter="url(#softGlow)"/>

  <!-- Thin inner highlight rings -->
  <circle cx="260" cy="310" r="80" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>
  <circle cx="510" cy="310" r="80" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>
  <circle cx="760" cy="310" r="80" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>
  <circle cx="1020" cy="310" r="80" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>
  <circle cx="420" cy="530" r="80" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>
  <circle cx="860" cy="530" r="80" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>

  <!-- Minimal white icons -->
  <path d="M240 284 L260 267 L280 284 V310 H247 V291 H273 V310" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="510" cy="288" r="20" fill="none" stroke="#ffffff" stroke-width="3"/>
  <line x1="510" y1="288" x2="510" y2="300" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
  <line x1="510" y1="314" x2="510" y2="314" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
  <path d="M738 306 C746 284 770 279 784 294 C770 293 758 301 752 316 C748 311 743 308 738 306 Z" fill="none" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"/>
  <path d="M997 314 L997 294 L1012 294 L1012 314 M1023 314 L1023 281 L1038 281 L1038 314" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
  <path d="M395 512 H445 M405 495 H435 M410 530 H430" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
  <circle cx="848" cy="292" r="12" fill="none" stroke="#ffffff" stroke-width="3"/>
  <circle cx="872" cy="292" r="12" fill="none" stroke="#ffffff" stroke-width="3"/>
  <path d="M830 322 C836 306 860 306 866 322 M854 322 C860 306 884 306 890 322" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>

  <!-- Bubble labels -->
  <text x="260" y="355" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="600" fill="#ffffff">Our Mission</text>
  <text x="510" y="355" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="600" fill="#ffffff">Problem</text>
  <text x="760" y="355" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="600" fill="#ffffff">Solution</text>
  <text x="1020" y="355" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="600" fill="#ffffff">Market</text>
  <text x="420" y="575" width="165" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="600" fill="#ffffff">Business Model</text>
  <text x="860" y="575" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="600" fill="#ffffff">Our Team</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to simulate frosted glass; masks are not safe for translation and may fail the whole slide.
- ❌ Do not apply `clip-path` to circles or rectangles; use `clipPath` only on `<image>` elements for the lens crop.
- ❌ Do not rely on a live blur filter on the background image if exact PPT editability is required; use a pre-blurred duplicate image clipped into each bubble.
- ❌ Do not pack the bubbles too tightly; the sharp background gaps are what make the localized blur feel like real glass.
- ❌ Do not use `marker-end` paths for navigation arrows; if arrows are needed, draw them from `<line>` elements with marker attributes directly on each line.

## Composition notes
- Keep the title in the upper 15–20% of the slide, with the bubbles occupying the middle and lower thirds.
- Use a full-bleed environmental photo with texture and depth; glassmorphism is most visible over detailed backgrounds.
- Maintain a monochrome UI layer: white text, white strokes, and translucent white fills.
- Align each blurred duplicate image exactly to the original background dimensions so the lens content matches the background position underneath.