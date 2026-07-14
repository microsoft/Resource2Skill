# SVG Recipe — Asymmetric Circular Motif & Premium White Space

## Visual mechanism
A giant, perfectly circular photo crop bleeds off one side of the slide while the opposite side remains mostly empty, carrying only bold editorial typography and a few tiny accent/data marks. The premium feel comes from the imbalance: oversized organic geometry versus strict grid-aligned text on a white field.

## SVG primitives needed
- 1× `<rect>` for the pure white canvas background
- 1× `<clipPath>` with `<circle>` to crop the hero photo into a perfect circle
- 1× `<image>` for the oversized editorial/fashion/brand photo
- 2× `<circle>` for the circular photo shadow/backplate and the large plum accent disk
- 5× small `<circle>` elements for floating data dots and logo/detail accents
- 3× `<path>` elements for the abstract premium logo mark and decorative arc motif
- 3× `<line>` elements for thin editorial separators / data connectors
- 5× `<text>` blocks with explicit `width` for headline, caption, label, metric, and contact text
- 1× `<linearGradient>` for the plum accent disk
- 1× `<filter id="softShadow">` applied to the circular photo backplate

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="plumGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B765D0"/>
      <stop offset="55%" stop-color="#9B59B6"/>
      <stop offset="100%" stop-color="#71368A"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-18" dy="24"/>
      <feGaussianBlur stdDeviation="22"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.12  0 0 0 0 0.08  0 0 0 0 0.14  0 0 0 0.22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroCircleClip">
      <circle cx="1128" cy="402" r="378"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Small premium logo mark -->
  <path d="M92 67 C92 48, 120 48, 120 67 C120 86, 92 86, 92 67 Z" fill="none" stroke="#9B59B6" stroke-width="6"/>
  <path d="M118 67 C118 48, 146 48, 146 67 C146 86, 118 86, 118 67 Z" fill="none" stroke="#9B59B6" stroke-width="6"/>
  <path d="M144 67 C144 48, 172 48, 172 67 C172 86, 144 86, 144 67 Z" fill="none" stroke="#9B59B6" stroke-width="6"/>
  <text x="196" y="72" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" letter-spacing="3" fill="#1E1E1E">LUMIÈRE MODE</text>

  <!-- Oversized asymmetric circular motif -->
  <circle cx="1128" cy="402" r="382" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="750" y="24" width="756" height="756"
         href="https://images.example.com/premium-fashion-model-editorial-square.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroCircleClip)"/>

  <!-- Accent disk bleeding off edge -->
  <circle cx="1260" cy="142" r="118" fill="url(#plumGrad)"/>
  <circle cx="822" cy="122" r="14" fill="#9B59B6"/>
  <circle cx="870" cy="122" r="5" fill="#9B59B6" opacity="0.5"/>

  <!-- Left editorial title block -->
  <text x="92" y="222" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="900" letter-spacing="4" fill="#1E1E1E">
    <tspan x="92" dy="0">MORE FUN,</tspan>
    <tspan x="92" dy="82">MORE</tspan>
    <tspan x="92" dy="82">FASHION</tspan>
  </text>

  <line x1="96" y1="504" x2="242" y2="504" stroke="#9B59B6" stroke-width="4"/>
  <text x="96" y="545" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="300" line-height="1.5" fill="#787878">
    <tspan x="96" dy="0">yourwebsite.com</tspan>
    <tspan x="96" dy="34">your@name.com</tspan>
  </text>

  <!-- Sparse floating data accents in the white space -->
  <line x1="525" y1="186" x2="690" y2="186" stroke="#D7C0E2" stroke-width="2" stroke-dasharray="8 10"/>
  <circle cx="525" cy="186" r="6" fill="#9B59B6"/>
  <circle cx="690" cy="186" r="6" fill="#9B59B6"/>
  <text x="546" y="171" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2" fill="#9B59B6">DROP 01</text>

  <text x="536" y="610" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800" fill="#1E1E1E">42%</text>
  <text x="540" y="642" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="400" letter-spacing="1.4" fill="#787878">SEASONAL LIFT</text>
  <line x1="536" y1="660" x2="692" y2="660" stroke="#9B59B6" stroke-width="3"/>

  <!-- Tiny editorial footer -->
  <text x="96" y="668" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="2.2" fill="#B0B0B0">SPRING / SUMMER CAPSULE · 2026</text>
</svg>
```

## Avoid in this skill
- ❌ Do not crop the photo with a `<mask>`; use `clipPath` applied directly to the `<image>`.
- ❌ Do not make the hero image rectangular with rounded corners; the signature is a mathematically perfect circle.
- ❌ Do not center the circle on the slide; push it off-canvas so the slide edge slices the curve.
- ❌ Do not fill the white space with charts, cards, or dense copy; this style depends on restraint.
- ❌ Do not apply filters to `<line>` separators; shadows/glows should be reserved for circles, paths, or text.

## Composition notes
- Keep the left 45–50% of the slide mostly white, with a bold stacked headline aligned to a clean vertical grid.
- Let the circular image dominate the right side, occupying roughly 60–75% of slide height and bleeding beyond at least one edge.
- Use plum/purple sparingly: one accent disk, thin rules, dots, and micro-labels are enough.
- Small data callouts should feel like editorial annotations, not dashboard widgets; place them in open space with thin lines and tiny dots.