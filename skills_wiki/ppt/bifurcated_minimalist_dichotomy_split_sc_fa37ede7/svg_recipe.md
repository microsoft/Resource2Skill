# SVG Recipe — Split-Screen Contrast Layout

## Visual mechanism
A perfectly bisected 16:9 canvas gives two opposing concepts equal visual weight, using edge-to-edge high-resolution imagery as the comparison surface. Small museum-style white placards float at the center of each half, while a razor-thin central divider makes the conceptual boundary unmistakable.

## SVG primitives needed
- 2× `<image>` for full-bleed contrasting photos, one cropped to each 640×720 half
- 2× `<clipPath>` with `<rect>` for locking each image to its exact half of the slide
- 2× `<rect>` for subtle dark gradient/scrim overlays that improve placard contrast
- 2× `<rect>` for stark white placard boxes
- 1× `<line>` for the central split divider
- 4× `<text>` for minimalist concept labels and small category captions
- 2× `<linearGradient>` for image-edge toning without obscuring the photos
- 1× `<filter>` with offset blur for the placard shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="leftHalf">
      <rect x="0" y="0" width="640" height="720"/>
    </clipPath>

    <clipPath id="rightHalf">
      <rect x="640" y="0" width="640" height="720"/>
    </clipPath>

    <linearGradient id="leftScrim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.18"/>
      <stop offset="45%" stop-color="#000000" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.22"/>
    </linearGradient>

    <linearGradient id="rightScrim" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.14"/>
      <stop offset="48%" stop-color="#000000" stop-opacity="0.00"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.20"/>
    </linearGradient>

    <filter id="placardShadow" x="-30%" y="-40%" width="160%" height="180%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Left image: old / mechanical / carved -->
  <image
    href="https://source.unsplash.com/1600x1800/?macro,machined,steel,chisel"
    xlink:href="https://source.unsplash.com/1600x1800/?macro,machined,steel,chisel"
    x="-20" y="0" width="700" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#leftHalf)"/>

  <!-- Right image: new / organic / engineered biology -->
  <image
    href="https://source.unsplash.com/1600x1800/?macro,biology,dna,cell"
    xlink:href="https://source.unsplash.com/1600x1800/?macro,biology,dna,cell"
    x="600" y="0" width="700" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#rightHalf)"/>

  <!-- Very restrained tonal overlays; keep images dominant -->
  <rect x="0" y="0" width="640" height="720" fill="url(#leftScrim)"/>
  <rect x="640" y="0" width="640" height="720" fill="url(#rightScrim)"/>

  <!-- Razor center divider -->
  <line x1="640" y1="0" x2="640" y2="720" stroke="#ffffff" stroke-width="1.5"/>
  <line x1="641.5" y1="0" x2="641.5" y2="720" stroke="#000000" stroke-opacity="0.25" stroke-width="0.75"/>

  <!-- Tiny gallery-style context labels -->
  <text x="48" y="52" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="2.2"
        fill="#ffffff" opacity="0.86">
    OLD PARADIGM
  </text>

  <text x="972" y="52" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="2.2"
        fill="#ffffff" opacity="0.86"
        text-anchor="end">
    NEW PARADIGM
  </text>

  <!-- Left museum placard -->
  <rect x="205" y="318" width="230" height="84" rx="0"
        fill="#ffffff" filter="url(#placardShadow)"/>
  <text x="230" y="369" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="400"
        fill="#000000">
    a chisel
  </text>

  <!-- Right museum placard -->
  <rect x="845" y="318" width="230" height="84" rx="0"
        fill="#ffffff" filter="url(#placardShadow)"/>
  <text x="870" y="369" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="400"
        fill="#000000">
    a gene
  </text>

  <!-- Optional lower metadata: keeps the keynote/editorial feeling -->
  <text x="48" y="672" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="400"
        fill="#ffffff" opacity="0.68">
    manufacture by subtraction
  </text>

  <text x="872" y="672" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="400"
        fill="#ffffff" opacity="0.68"
        text-anchor="end">
    design by instruction
  </text>
</svg>
```

## Avoid in this skill
- ❌ Unequal columns unless the story explicitly needs imbalance; the power comes from strict 50/50 parity
- ❌ Busy text blocks or bullet lists over the images; this layout works best with one short phrase per side
- ❌ Rounded, colorful UI-card styling for the placards; use hard-edged black/white museum-label restraint
- ❌ Thick central dividers, arrows, or decorative connectors; they weaken the stark dichotomy
- ❌ Low-resolution or mismatched image styles; both halves should feel equally premium, macro, cinematic, or editorial

## Composition notes
- Keep the split exact: left half `0–640`, right half `640–1280`, full height `720`.
- Center each placard within its own half, not within the whole slide: left around `x=320`, right around `x=960`.
- Let the photos provide almost all color; structural elements should stay true white, black, and subtle shadow.
- Use negative space inside the placards generously: short labels, wide margins, no more than 1–3 words per concept.