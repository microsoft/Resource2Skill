# SVG Recipe — Diamond Focus Cover

## Visual mechanism
A full-bleed field of rotated square “diamonds” creates motion toward the center, where a larger rotated rounded rectangle becomes the focal text plaque. Optional image-filled diamond tiles add premium depth while preserving a crisp geometric cover-slide structure.

## SVG primitives needed
- 1× `<rect>` for the dark full-slide background
- 6× `<linearGradient>` / `<radialGradient>` for background atmosphere, diamond fills, and the central focus plaque
- 2× `<filter>` using blur/shadow for glow and elevated focus
- 4× `<clipPath>` with diamond-shaped `<path>` crops applied to repeated `<image>` elements
- 4× `<image>` for optional hero-photo fragments inside selected diamond tiles
- 18× `<path>` for diamond tiles, outlined grid diamonds, accent shards, and the central rotated plaque substitute
- 3× `<rect>` rotated 45° for rounded diamond panels and small glass highlights
- 4× `<line>` for fine geometric connector strokes
- 4× `<text>` with explicit `width` attributes for eyebrow, headline, subtitle, and footer metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="48%" stop-color="#102B46"/>
      <stop offset="100%" stop-color="#061018"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#2DE2E6" stop-opacity="0.34"/>
      <stop offset="45%" stop-color="#1D77FF" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#07111F" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="plaqueGrad" x1="430" y1="150" x2="850" y2="570">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#EAF7FF"/>
      <stop offset="100%" stop-color="#A9E8FF"/>
    </linearGradient>
    <linearGradient id="cyanGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#32F5FF" stop-opacity="0.76"/>
      <stop offset="100%" stop-color="#2563EB" stop-opacity="0.22"/>
    </linearGradient>
    <linearGradient id="violetGlass" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.70"/>
      <stop offset="100%" stop-color="#22D3EE" stop-opacity="0.20"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="blueGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
    <clipPath id="photoDiamondA"><path d="M118 98 L258 238 L118 378 L-22 238 Z"/></clipPath>
    <clipPath id="photoDiamondB"><path d="M1060 58 L1230 228 L1060 398 L890 228 Z"/></clipPath>
    <clipPath id="photoDiamondC"><path d="M220 430 L350 560 L220 690 L90 560 Z"/></clipPath>
    <clipPath id="photoDiamondD"><path d="M1018 434 L1148 564 L1018 694 L888 564 Z"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>

  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=1400&amp;q=80" x="-60" y="0" width="620" height="720" opacity="0.72" clip-path="url(#photoDiamondA)"/>
  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=1400&amp;q=80" x="720" y="-40" width="620" height="720" opacity="0.62" clip-path="url(#photoDiamondB)"/>
  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=1400&amp;q=80" x="-20" y="250" width="560" height="520" opacity="0.50" clip-path="url(#photoDiamondC)"/>
  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=1400&amp;q=80" x="760" y="260" width="560" height="520" opacity="0.45" clip-path="url(#photoDiamondD)"/>

  <path d="M118 98 L258 238 L118 378 L-22 238 Z" fill="none" stroke="#7DD3FC" stroke-width="2.2" opacity="0.72"/>
  <path d="M1060 58 L1230 228 L1060 398 L890 228 Z" fill="none" stroke="#67E8F9" stroke-width="2.2" opacity="0.64"/>
  <path d="M220 430 L350 560 L220 690 L90 560 Z" fill="none" stroke="#A78BFA" stroke-width="2" opacity="0.58"/>
  <path d="M1018 434 L1148 564 L1018 694 L888 564 Z" fill="none" stroke="#22D3EE" stroke-width="2" opacity="0.50"/>

  <path d="M425 55 L510 140 L425 225 L340 140 Z" fill="url(#cyanGlass)" stroke="#BFF7FF" stroke-width="1.5" opacity="0.72"/>
  <path d="M835 48 L928 141 L835 234 L742 141 Z" fill="url(#violetGlass)" stroke="#C4B5FD" stroke-width="1.5" opacity="0.64"/>
  <path d="M92 392 L170 470 L92 548 L14 470 Z" fill="#0EA5E9" opacity="0.18" stroke="#38BDF8" stroke-width="1.2"/>
  <path d="M1195 330 L1270 405 L1195 480 L1120 405 Z" fill="#8B5CF6" opacity="0.20" stroke="#A78BFA" stroke-width="1.2"/>
  <path d="M506 560 L574 628 L506 696 L438 628 Z" fill="#22D3EE" opacity="0.16" stroke="#67E8F9" stroke-width="1.3"/>
  <path d="M780 548 L852 620 L780 692 L708 620 Z" fill="#6366F1" opacity="0.20" stroke="#A5B4FC" stroke-width="1.3"/>

  <path d="M640 100 L710 170 L640 240 L570 170 Z" fill="none" stroke="#E0F2FE" stroke-width="1.2" opacity="0.28" stroke-dasharray="8 10"/>
  <path d="M640 480 L718 558 L640 636 L562 558 Z" fill="none" stroke="#E0F2FE" stroke-width="1.2" opacity="0.24" stroke-dasharray="8 10"/>
  <path d="M380 300 L448 368 L380 436 L312 368 Z" fill="none" stroke="#67E8F9" stroke-width="1" opacity="0.22"/>
  <path d="M900 292 L972 364 L900 436 L828 364 Z" fill="none" stroke="#C4B5FD" stroke-width="1" opacity="0.22"/>

  <line x1="260" y1="238" x2="500" y2="360" stroke="#67E8F9" stroke-width="1.2" opacity="0.22"/>
  <line x1="1020" y1="228" x2="780" y2="360" stroke="#A5B4FC" stroke-width="1.2" opacity="0.22"/>
  <line x1="350" y1="560" x2="520" y2="430" stroke="#67E8F9" stroke-width="1.2" opacity="0.18"/>
  <line x1="930" y1="560" x2="760" y2="430" stroke="#A78BFA" stroke-width="1.2" opacity="0.18"/>

  <rect x="470" y="190" width="340" height="340" rx="42" fill="#0F2740" opacity="0.54" transform="rotate(45 640 360)" filter="url(#blueGlow)"/>
  <rect x="468" y="188" width="344" height="344" rx="44" fill="url(#plaqueGrad)" stroke="#FFFFFF" stroke-width="2.5" transform="rotate(45 640 360)" filter="url(#softShadow)"/>
  <rect x="514" y="234" width="252" height="252" rx="32" fill="#FFFFFF" opacity="0.24" transform="rotate(45 640 360)"/>
  <path d="M640 152 L848 360 L640 568 L432 360 Z" fill="none" stroke="#38BDF8" stroke-width="3.5" opacity="0.80"/>
  <path d="M640 176 L824 360 L640 544 L456 360 Z" fill="none" stroke="#0F172A" stroke-width="1.2" opacity="0.18"/>

  <text x="500" y="285" width="280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" letter-spacing="3" fill="#0EA5E9">EXECUTIVE BRIEFING</text>
  <text x="415" y="357" width="450" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="800" fill="#07111F">DIAMOND FOCUS</text>
  <text x="455" y="410" width="370" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="500" fill="#24445F">A bold section opener with a geometric grid, image facets, and a clear central message.</text>
  <text x="520" y="595" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" letter-spacing="1.8" fill="#BFF7FF" opacity="0.86">STRATEGY · 2026</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the diamond grid with `<use>` or `<symbol>` repeats; duplicate the individual `<path>` or `<rect>` shapes so PowerPoint receives editable objects.
- ❌ Do not apply `clip-path` to decorative diamond shapes; clipping is only reliable on `<image>` elements, so draw geometric diamonds directly as paths.
- ❌ Do not rotate the main text with the plaque; keep the diamond plaque rotated but place readable, horizontal text above it.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to fake perspective; use rotated rectangles and explicit diamond paths instead.
- ❌ Do not rely on `<pattern>` fills for the grid texture; create a curated set of visible diamond paths for predictable PPT editing.

## Composition notes
- Keep the main text inside the central 420×260 px safe zone; the rotated plaque creates visual drama while the typography stays stable and readable.
- Use image-filled diamonds on the outer thirds of the slide, never behind the headline; they should frame the center rather than compete with it.
- Alternate cyan, violet, and white strokes across the diamond grid to create rhythm without making the background feel busy.
- Preserve dark negative space around the focal plaque; this contrast is what makes the cover feel premium and keynote-like.