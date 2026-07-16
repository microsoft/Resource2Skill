# SVG Recipe — Minimalist Brand Color Showcase

## Visual mechanism
A centered row of large, slightly overlapping circular color swatches creates a unified palette “chain,” with each color’s name and Hex value precisely aligned beneath its circle. The composition stays premium and calm through generous negative space, warm neutral background tones, and restrained typography.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm neutral background
- 2× `<path>` for soft decorative corner blobs that add depth without distracting from the palette
- 5× `<circle>` for the overlapping brand color swatches
- 5× small `<circle>` for subtle top-left highlight sheens on each swatch
- 1× `<line>` for a thin editorial divider under the subtitle
- 8× `<text>` for eyebrow label, main title, subtitle, and five color labels with nested `<tspan>` styling
- 1× `<linearGradient>` for the background wash
- 2× `<radialGradient>` for soft ambient decorative blobs
- 1× `<filter id="softShadow">` applied to the swatch circles for gentle lift

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWarm" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F5F0DD"/>
      <stop offset="55%" stop-color="#EFEAD5"/>
      <stop offset="100%" stop-color="#E8DFC5"/>
    </linearGradient>

    <radialGradient id="blobPeach" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFB3A0" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#FFB3A0" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="blobSage" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#829E8B" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#829E8B" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="15" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.25  0 0 0 0 0.19  0 0 0 0 0.22  0 0 0 0.18 0"
        result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Warm editorial canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWarm)"/>

  <!-- Low-contrast ambient shapes -->
  <path d="M-95,96 C12,8 149,2 222,84 C293,165 252,290 137,335 C17,382 -103,313 -129,205 C-146,151 -135,128 -95,96 Z"
        fill="url(#blobPeach)"/>
  <path d="M1108,589 C1194,511 1346,532 1394,634 C1437,726 1342,815 1224,787 C1110,760 1029,662 1108,589 Z"
        fill="url(#blobSage)"/>

  <!-- Header typography -->
  <text x="640" y="92" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        font-weight="700" letter-spacing="3.5" fill="#7B665B">
    BRAND SYSTEM / COLOR
  </text>

  <text x="640" y="168" width="980" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="64"
        font-weight="800" letter-spacing="-2" fill="#40303A">
    Boho Color Palette
  </text>

  <text x="640" y="212" width="640" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        font-weight="400" fill="#6D5A62">
    Earthy tones for a calm, tactile, modern brand language
  </text>

  <line x1="520" y1="244" x2="760" y2="244" stroke="#40303A" stroke-width="1.5" stroke-opacity="0.22"/>

  <!-- Overlapping swatch chain; later circles sit above earlier circles -->
  <circle cx="292" cy="382" r="108" fill="#E38150" filter="url(#softShadow)"/>
  <circle cx="466" cy="382" r="108" fill="#FFB3A0" filter="url(#softShadow)"/>
  <circle cx="640" cy="382" r="108" fill="#EFC16D" filter="url(#softShadow)"/>
  <circle cx="814" cy="382" r="108" fill="#B6CDBD" filter="url(#softShadow)"/>
  <circle cx="988" cy="382" r="108" fill="#829E8B" filter="url(#softShadow)"/>

  <!-- Tiny flat highlights; keep subtle so the colors remain accurate -->
  <circle cx="253" cy="338" r="28" fill="#FFFFFF" opacity="0.14"/>
  <circle cx="427" cy="338" r="28" fill="#FFFFFF" opacity="0.16"/>
  <circle cx="601" cy="338" r="28" fill="#FFFFFF" opacity="0.13"/>
  <circle cx="775" cy="338" r="28" fill="#FFFFFF" opacity="0.16"/>
  <circle cx="949" cy="338" r="28" fill="#FFFFFF" opacity="0.12"/>

  <!-- Color labels aligned to each swatch center -->
  <text x="292" y="548" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        font-weight="700" fill="#40303A">
    Rust
    <tspan x="292" dy="28" font-family="Consolas, Cascadia Mono, monospace"
           font-size="17" font-weight="500" letter-spacing="1.2" fill="#6D5A62">#E38150</tspan>
  </text>

  <text x="466" y="548" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        font-weight="700" fill="#40303A">
    Peach
    <tspan x="466" dy="28" font-family="Consolas, Cascadia Mono, monospace"
           font-size="17" font-weight="500" letter-spacing="1.2" fill="#6D5A62">#FFB3A0</tspan>
  </text>

  <text x="640" y="548" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        font-weight="700" fill="#40303A">
    Mustard
    <tspan x="640" dy="28" font-family="Consolas, Cascadia Mono, monospace"
           font-size="17" font-weight="500" letter-spacing="1.2" fill="#6D5A62">#EFC16D</tspan>
  </text>

  <text x="814" y="548" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        font-weight="700" fill="#40303A">
    Mint
    <tspan x="814" dy="28" font-family="Consolas, Cascadia Mono, monospace"
           font-size="17" font-weight="500" letter-spacing="1.2" fill="#6D5A62">#B6CDBD</tspan>
  </text>

  <text x="988" y="548" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        font-weight="700" fill="#40303A">
    Sage
    <tspan x="988" dy="28" font-family="Consolas, Cascadia Mono, monospace"
           font-size="17" font-weight="500" letter-spacing="1.2" fill="#6D5A62">#829E8B</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a plain grid of separated rectangles; the signature effect depends on large circular swatches with intentional overlap.
- ❌ Heavy outlines around swatches; borders make the palette feel like a chart instead of a brand mood artifact.
- ❌ Overly saturated or unrelated colors unless the brand system calls for it; this layout works best when the palette feels curated and tonal.
- ❌ Placing labels according to visible overlap edges; always align labels to the mathematical center of each circle.
- ❌ Applying shadows to `<line>` elements or using unsupported masks/patterns for texture.

## Composition notes
- Keep the swatch chain horizontally centered and let it occupy roughly 70% of the slide width; overlap circles by about 15–20% of their diameter.
- Reserve the top third for title, subtitle, and a small editorial eyebrow label; avoid crowding the palette.
- Put Hex labels below the circles with strict center alignment, even though the circles overlap visually.
- Use a warm low-contrast background and charcoal/plum typography so the color swatches remain the main focal point.