# SVG Recipe — Glass Panel Split

## Visual mechanism
A full-bleed photographic background is softened by dark color washes, then a large rounded “glass” panel floats in the center with translucent fill, luminous edges, and a premium shadow. Inside the panel, a clipped editorial hero image occupies one side while oversized headline typography and concise body copy occupy the other.

## SVG primitives needed
- 2× `<image>` for the full-bleed background photo and the clipped hero photo
- 1× `<clipPath>` with rounded `<rect>` for the hero image crop
- 5× `<rect>` for background overlays, glass panel layers, panel border, and split divider
- 3× `<path>` for organic color washes and decorative glass reflections
- 2× `<circle>` / `<ellipse>` for soft glow accents behind the panel
- 3× `<linearGradient>` for background tint, glass fill, and highlight stroke
- 2× `<radialGradient>` for ambient glow blobs
- 2× `<filter>` using blur/shadow primitives for panel elevation and glow
- 4× `<text>` elements with explicit `width` for eyebrow, headline, body, and small metadata label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827" stop-opacity="0.58"/>
      <stop offset="48%" stop-color="#172554" stop-opacity="0.44"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="glassFill" x1="0" y1="80" x2="0" y2="640">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.36"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.17"/>
      <stop offset="100%" stop-color="#C7D2FE" stop-opacity="0.10"/>
    </linearGradient>

    <linearGradient id="glassStroke" x1="190" y1="92" x2="1090" y2="628">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.88"/>
      <stop offset="36%" stop-color="#E0F2FE" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.48"/>
    </linearGradient>

    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#67E8F9" stop-opacity="0.50"/>
      <stop offset="100%" stop-color="#67E8F9" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="roseGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FB7185" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#FB7185" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="22"/>
      <feGaussianBlur stdDeviation="22"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.01 0 0 0 0 0.02 0 0 0 0 0.06 0 0 0 0.46 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>

    <clipPath id="heroClip">
      <rect x="214" y="124" width="390" height="472" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <image href="https://images.example.com/full-bleed-night-city-with-soft-bokeh-lights.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgTint)"/>

  <path d="M-40 568 C190 442 320 666 522 536 C710 416 792 474 958 366 C1118 262 1196 302 1340 230 L1340 760 L-40 760 Z"
        fill="#312E81" opacity="0.36"/>
  <path d="M-20 72 C140 14 266 22 420 88 C606 168 708 92 888 58 C1058 26 1176 64 1310 130 L1310 -30 L-20 -30 Z"
        fill="#0EA5E9" opacity="0.18"/>

  <ellipse cx="982" cy="162" rx="280" ry="160" fill="url(#cyanGlow)" filter="url(#softGlow)"/>
  <circle cx="252" cy="612" r="210" fill="url(#roseGlow)" filter="url(#softGlow)"/>

  <rect x="180" y="92" width="920" height="536" rx="48" ry="48"
        fill="#020617" opacity="0.28" filter="url(#panelShadow)"/>
  <rect x="180" y="92" width="920" height="536" rx="48" ry="48"
        fill="url(#glassFill)"/>
  <rect x="180" y="92" width="920" height="536" rx="48" ry="48"
        fill="none" stroke="url(#glassStroke)" stroke-width="2.2"/>

  <path d="M215 118 C344 86 482 92 620 116 C724 134 866 132 1037 100"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="2.4"/>
  <path d="M1036 152 C1010 246 984 302 1002 390 C1018 468 980 540 913 594"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.6"/>

  <image href="https://images.example.com/editorial-portrait-founder-in-vivid-gradient-light.jpg"
         x="214" y="124" width="390" height="472" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroClip)"/>

  <rect x="214" y="124" width="390" height="472" rx="34" ry="34"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.46" stroke-width="1.4"/>

  <rect x="646" y="146" width="1.5" height="428" rx="1" fill="#FFFFFF" opacity="0.32"/>
  <rect x="676" y="134" width="78" height="28" rx="14" fill="#FFFFFF" opacity="0.18"/>

  <text x="696" y="154" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        font-weight="700" letter-spacing="2.5" fill="#E0F2FE">
    STRATEGY RESET
  </text>

  <text x="694" y="238" width="344" font-family="Segoe UI, Microsoft YaHei"
        font-size="56" font-weight="800" line-height="1.05" fill="#FFFFFF">
    <tspan x="694" dy="0">Designing</tspan>
    <tspan x="694" dy="60">for the next</tspan>
    <tspan x="694" dy="60" fill="#BAE6FD">growth curve</tspan>
  </text>

  <text x="698" y="438" width="330" font-family="Segoe UI, Microsoft YaHei"
        font-size="20" line-height="1.45" fill="#E5E7EB">
    <tspan x="698" dy="0">A glass-panel split creates a sharp editorial</tspan>
    <tspan x="698" dy="30">moment: immersive image on one side, crisp</tspan>
    <tspan x="698" dy="30">executive message on the other.</tspan>
  </text>

  <line x1="698" y1="548" x2="830" y2="548" stroke="#93C5FD" stroke-width="3" stroke-linecap="round"/>
  <text x="852" y="555" width="210" font-family="Segoe UI, Microsoft YaHei"
        font-size="15" font-weight="600" fill="#DBEAFE">
    2026 Executive Keynote
  </text>
</svg>
```

## Avoid in this skill
- ❌ Real backdrop blur using CSS `backdrop-filter`; it will not translate reliably, so simulate frost with translucent fills, gradients, and soft glows.
- ❌ Applying `clip-path` to the glass panel group or to decorative shapes; use clipping only on the hero `<image>`.
- ❌ Using `<mask>` to create frosted transparency or fadeouts; masks can hard-fail the slide.
- ❌ Putting filter effects on divider `<line>` elements; use plain lines or thin rounded `<rect>` shapes for luminous separators.
- ❌ Overfilling the glass panel with dense charts or many bullets; the technique depends on low-density editorial contrast.

## Composition notes
- Keep the central panel large, about 70–75% of slide width and 70–78% of slide height, with generous outer background visible on all sides.
- Use a 40/60 or 45/55 split inside the panel: clipped hero image on the left, headline and body on the right.
- The background should be visually rich but darkened enough that the translucent glass panel remains legible.
- Repeat cool highlights — cyan, blue, soft white — across the glass edge, divider, and accent text to make the panel feel cohesive.