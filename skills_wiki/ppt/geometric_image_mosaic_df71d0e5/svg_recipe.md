# SVG Recipe — Geometric Image Mosaic

## Visual mechanism
A single hero photo is revealed only through a tessellated geometric grid, making the image feel engineered, editorial, and premium. The mosaic occupies one side of the slide while a dark negative-space panel supports large title typography.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 1× `<clipPath>` containing a compound triangular `<path>` to crop the hero image into a mosaic
- 1× `<image>` clipped by the geometric mosaic path
- 1× compound `<path>` duplicated as thin white triangle borders over the clipped image
- 3× translucent accent `<path>` triangles for depth and color rhythm
- 1× `<rect>` with a blur/offset filter for a soft shadow behind the mosaic area
- 1× `<linearGradient>` for the background
- 1× `<linearGradient>` for cyan-to-blue accent fills
- 1× `<filter>` for the mosaic shadow
- 4× `<text>` elements for eyebrow, title, subtitle, and metadata; every text element has explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#030712"/>
      <stop offset="0.55" stop-color="#07111f"/>
      <stop offset="1" stop-color="#0b1630"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="620" y1="110" x2="1180" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#67e8f9" stop-opacity="0.70"/>
      <stop offset="0.55" stop-color="#2563eb" stop-opacity="0.38"/>
      <stop offset="1" stop-color="#7c3aed" stop-opacity="0.24"/>
    </linearGradient>

    <filter id="mosaicShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-18" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="triangleMosaicClip">
      <path d="
        M560 0 L680 0 L620 104 Z M680 0 L800 0 L740 104 Z M800 0 L920 0 L860 104 Z M920 0 L1040 0 L980 104 Z M1040 0 L1160 0 L1100 104 Z M1160 0 L1280 0 L1220 104 Z
        M620 104 L740 104 L680 208 Z M740 104 L860 104 L800 208 Z M860 104 L980 104 L920 208 Z M980 104 L1100 104 L1040 208 Z M1100 104 L1220 104 L1160 208 Z M1220 104 L1340 104 L1280 208 Z
        M560 208 L680 208 L620 312 Z M680 208 L800 208 L740 312 Z M800 208 L920 208 L860 312 Z M920 208 L1040 208 L980 312 Z M1040 208 L1160 208 L1100 312 Z M1160 208 L1280 208 L1220 312 Z
        M620 312 L740 312 L680 416 Z M740 312 L860 312 L800 416 Z M860 312 L980 312 L920 416 Z M980 312 L1100 312 L1040 416 Z M1100 312 L1220 312 L1160 416 Z M1220 312 L1340 312 L1280 416 Z
        M560 416 L680 416 L620 520 Z M680 416 L800 416 L740 520 Z M800 416 L920 416 L860 520 Z M920 416 L1040 416 L980 520 Z M1040 416 L1160 416 L1100 520 Z M1160 416 L1280 416 L1220 520 Z
        M620 520 L740 520 L680 624 Z M740 520 L860 520 L800 624 Z M860 520 L980 520 L920 624 Z M980 520 L1100 520 L1040 624 Z M1100 520 L1220 520 L1160 624 Z M1220 520 L1340 520 L1280 624 Z
        M560 624 L680 624 L620 728 Z M680 624 L800 624 L740 728 Z M800 624 L920 624 L860 728 Z M920 624 L1040 624 L980 728 Z M1040 624 L1160 624 L1100 728 Z M1160 624 L1280 624 L1220 728 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M0 0 C180 90 250 230 210 370 C170 520 250 635 390 720 L0 720 Z"
        fill="#0f172a" opacity="0.68"/>

  <rect x="555" y="0" width="725" height="720" fill="#020617" opacity="0.35" filter="url(#mosaicShadow)"/>

  <image href="https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&amp;fit=crop&amp;w=1280&amp;q=85"
         x="430" y="0" width="900" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#triangleMosaicClip)"/>

  <path d="
        M560 0 L680 0 L620 104 Z M680 0 L800 0 L740 104 Z M800 0 L920 0 L860 104 Z M920 0 L1040 0 L980 104 Z M1040 0 L1160 0 L1100 104 Z M1160 0 L1280 0 L1220 104 Z
        M620 104 L740 104 L680 208 Z M740 104 L860 104 L800 208 Z M860 104 L980 104 L920 208 Z M980 104 L1100 104 L1040 208 Z M1100 104 L1220 104 L1160 208 Z M1220 104 L1340 104 L1280 208 Z
        M560 208 L680 208 L620 312 Z M680 208 L800 208 L740 312 Z M800 208 L920 208 L860 312 Z M920 208 L1040 208 L980 312 Z M1040 208 L1160 208 L1100 312 Z M1160 208 L1280 208 L1220 312 Z
        M620 312 L740 312 L680 416 Z M740 312 L860 312 L800 416 Z M860 312 L980 312 L920 416 Z M980 312 L1100 312 L1040 416 Z M1100 312 L1220 312 L1160 416 Z M1220 312 L1340 312 L1280 416 Z
        M560 416 L680 416 L620 520 Z M680 416 L800 416 L740 520 Z M800 416 L920 416 L860 520 Z M920 416 L1040 416 L980 520 Z M1040 416 L1160 416 L1100 520 Z M1160 416 L1280 416 L1220 520 Z
        M620 520 L740 520 L680 624 Z M740 520 L860 520 L800 624 Z M860 520 L980 520 L920 624 Z M980 520 L1100 520 L1040 624 Z M1100 520 L1220 520 L1160 624 Z M1220 520 L1340 520 L1280 624 Z
        M560 624 L680 624 L620 728 Z M680 624 L800 624 L740 728 Z M800 624 L920 624 L860 728 Z M920 624 L1040 624 L980 728 Z M1040 624 L1160 624 L1100 728 Z M1160 624 L1280 624 L1220 728 Z"
        fill="none" stroke="#ffffff" stroke-width="3.5" stroke-opacity="0.88"/>

  <path d="M620 104 L740 104 L680 208 Z" fill="url(#accentGrad)" opacity="0.65"/>
  <path d="M980 312 L1100 312 L1040 416 Z" fill="#22d3ee" opacity="0.30"/>
  <path d="M740 520 L860 520 L800 624 Z" fill="#a78bfa" opacity="0.28"/>

  <line x1="96" y1="126" x2="210" y2="126" stroke="#38bdf8" stroke-width="4"/>
  <text x="96" y="112" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="3" fill="#7dd3fc">GEOMETRIC IMAGE MOSAIC</text>

  <text x="92" y="228" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" fill="#f8fafc">
    <tspan x="92" dy="0">The Shape</tspan>
    <tspan x="92" dy="68">of Insight</tspan>
  </text>

  <text x="96" y="386" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" fill="#cbd5e1">
    <tspan x="96" dy="0">A single strategic image fragmented</tspan>
    <tspan x="96" dy="32">into a structured visual system.</tspan>
  </text>

  <text x="96" y="635" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" fill="#94a3b8">EXECUTIVE BRIEFING  ·  DATA / DESIGN / GROWTH</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to reveal the mosaic; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not apply `clip-path` to ordinary `<path>` or `<rect>` elements; the translator only preserves clipping reliably for images.
- ❌ Do not use `<pattern>` fills for the tessellation; draw the triangle outlines explicitly as editable paths.
- ❌ Do not rely on `<use>` to repeat triangle cells; duplicate the path data or use one compound path.
- ❌ Do not place text over the busy mosaic unless a dark overlay panel is added for contrast.

## Composition notes
- Reserve 40–45% of the slide for quiet title space; let the mosaic dominate the remaining right side.
- Use thin white or pale borders to make each geometric image cell legible without overpowering the photo.
- Choose photos with strong texture, lights, architecture, technology, or landscape detail; flat photos make the mosaic feel empty.
- Add only a few translucent accent triangles so the photo remains the hero while the color rhythm connects to the deck palette.