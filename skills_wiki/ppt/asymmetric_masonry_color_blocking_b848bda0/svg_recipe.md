# SVG Recipe — Asymmetric Masonry Color Blocking

## Visual mechanism
An editorial masonry grid divides the slide into unequal rectangular compartments that mix deep color panels, cropped photography, accent text blocks, and offset wireframe borders. The asymmetry creates tension while the strict rectangular geometry keeps the composition polished and easy to scan.

## SVG primitives needed
- 1× `<rect>` for the full-slide neutral background
- 4× `<rect>` with shadow filters for the primary masonry blocks and image shadow plates
- 3× `<rect>` solid fills for the deep anchor panel, coral information panel, and pale caption panel
- 2× `<image>` elements clipped into exact rectangular crops for the dominant and secondary photo compartments
- 2× `<clipPath>` definitions using rounded rectangles for editable photo-card crops
- 2× `<rect>` outline-only wireframes, offset from image blocks to create editorial depth
- 3× `<linearGradient>` definitions for subtle premium color variation inside flat blocks
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for lifted block shadows
- 4× `<text>` elements with explicit `width` attributes for rotated title, body copy, caption, and small label text
- 4× decorative `<path>` accents for small geometric slashes and corner details

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8F9FC"/>
      <stop offset="100%" stop-color="#EEF1F6"/>
    </linearGradient>

    <linearGradient id="anchorGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5A4C83"/>
      <stop offset="100%" stop-color="#332C55"/>
    </linearGradient>

    <linearGradient id="coralGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F59A98"/>
      <stop offset="100%" stop-color="#E87682"/>
    </linearGradient>

    <linearGradient id="paleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F4F5F8"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 .22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="mainPhotoClip">
      <rect x="380" y="88" width="500" height="380" rx="0" ry="0"/>
    </clipPath>

    <clipPath id="sidePhotoClip">
      <rect x="920" y="378" width="270" height="254" rx="0" ry="0"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <!-- Subtle background rhythm -->
  <path d="M106 72 L225 72 L225 78 L106 78 Z" fill="#F08A8A" opacity="0.45"/>
  <path d="M1106 648 L1190 648 L1190 654 L1106 654 Z" fill="#4A3F6B" opacity="0.25"/>
  <path d="M1016 60 L1036 60 L1026 82 Z" fill="#F08A8A" opacity="0.65"/>
  <path d="M326 625 L350 625 L338 650 Z" fill="#4A3F6B" opacity="0.18"/>

  <!-- Left anchor block -->
  <rect x="90" y="88" width="255" height="544" fill="url(#anchorGrad)" filter="url(#softShadow)"/>
  <rect x="116" y="112" width="44" height="5" fill="#F08A8A" opacity="0.95"/>
  <rect x="116" y="126" width="82" height="5" fill="#F08A8A" opacity="0.55"/>

  <text x="218" y="380" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" letter-spacing="4"
        fill="#FFFFFF" text-anchor="middle"
        transform="rotate(-90 218 360)">
    <tspan x="218" dy="-10">CREATIVE</tspan>
    <tspan x="218" dy="64">BLOCKS</tspan>
  </text>

  <text x="116" y="574" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="2"
        fill="#D8D3EC">
    2026 / BRAND SYSTEM
  </text>

  <!-- Main image block with shadow plate and offset wireframe -->
  <rect x="380" y="88" width="500" height="380" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="380" y="88" width="500" height="380"
         href="https://images.example.com/editorial-studio-team-collaboration-wide-photo.jpg"
         clip-path="url(#mainPhotoClip)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="362" y="112" width="500" height="380"
        fill="none" stroke="#F08A8A" stroke-width="5"/>

  <!-- Right coral information block -->
  <rect x="920" y="88" width="270" height="250" fill="url(#coralGrad)" filter="url(#softShadow)"/>
  <text x="948" y="136" width="212"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#FFFFFF">
    Designed for clarity, built for momentum.
  </text>
  <text x="948" y="238" width="214"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#FFF4F4">
    A modular visual system combines structured information with confident editorial energy.
  </text>
  <rect x="948" y="302" width="64" height="6" fill="#FFFFFF" opacity="0.85"/>

  <!-- Right lower image block with offset border -->
  <rect x="920" y="378" width="270" height="254" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="920" y="378" width="270" height="254"
         href="https://images.example.com/minimal-product-detail-closeup-coral-purple.jpg"
         clip-path="url(#sidePhotoClip)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="940" y="356" width="270" height="254"
        fill="none" stroke="#4A3F6B" stroke-width="3" opacity="0.9"/>

  <!-- Bottom center caption block -->
  <rect x="380" y="508" width="500" height="124" fill="url(#paleGrad)" filter="url(#softShadow)"/>
  <text x="414" y="552" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" fill="#4A3F6B">
    Asymmetric compartments prevent overload.
  </text>
  <text x="414" y="586" width="410"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#626579">
    Use the large image as the emotional anchor, then let colored blocks carry concise proof points and positioning language.
  </text>

  <!-- Fine masonry alignment cues -->
  <line x1="380" y1="488" x2="880" y2="488" stroke="#D7DAE4" stroke-width="1" stroke-dasharray="7 8"/>
  <line x1="900" y1="88" x2="900" y2="632" stroke="#D7DAE4" stroke-width="1" stroke-dasharray="7 8"/>
</svg>
```

## Avoid in this skill
- ❌ Do not build the masonry as an evenly spaced dashboard grid; the technique depends on unequal block sizes and deliberate imbalance.
- ❌ Do not use `<pattern>` fills for texture; use gradients, photos, and solid blocks instead so the result remains editable.
- ❌ Do not apply `clip-path` to rectangles or text; only clip the `<image>` elements.
- ❌ Do not use `<use>` to repeat wireframes or decorations; duplicate simple editable shapes directly.
- ❌ Do not put shadows on `<line>` elements; use shadowed rectangles behind blocks and separate outline rectangles for wireframes.

## Composition notes
- Keep a generous outer margin, then let the blocks nearly touch internally; the clean masonry edges are what make the asymmetry feel intentional.
- Put the largest photo in the center-left zone so it becomes the visual anchor, with smaller text/photo blocks stacked on the right.
- Use one dark anchor block for rotated title typography; it gives the layout a strong editorial spine.
- Offset wireframes should be visibly shifted but not chaotic: 15–25 px is usually enough to create depth without breaking the grid.