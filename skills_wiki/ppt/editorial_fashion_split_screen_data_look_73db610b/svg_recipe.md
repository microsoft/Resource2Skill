# SVG Recipe — Editorial Fashion Split-Screen & Data Lookbook

## Visual mechanism
A premium lookbook slide splits the canvas into a disciplined editorial data pane on the left and a full-bleed fashion image on the right. Dense technical information is converted into solid color-block table cells, making specifications feel like magazine art direction rather than a spreadsheet.

## SVG primitives needed
- 3× `<rect>` for the off-white left panel, full-bleed right image overlay, and vertical divider
- 14× `<rect>` for color-blocked table cells, data chips, and editorial label bars
- 2× `<path>` for subtle organic gold accent shapes in the left pane
- 1× `<image>` for the right-half full-bleed fashion editorial photo
- 1× `<clipPath>` with `<rect>` to crop the photo to the exact right-side split
- 2× `<linearGradient>` for the photo vignette overlay and gold accent wash
- 1× `<filter id="softShadow">` applied to the data table backing card
- 16× `<text>` with explicit `width` attributes for kicker, headline, table labels, specs, quote, and image caption
- 1× `<line>` for the restrained editorial rule under the section header

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="rightPhotoClip">
      <rect x="640" y="0" width="640" height="720"/>
    </clipPath>

    <linearGradient id="photoShade" x1="640" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.08"/>
      <stop offset="0.55" stop-color="#000000" stop-opacity="0.02"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.46"/>
    </linearGradient>

    <linearGradient id="goldWash" x1="80" y1="80" x2="520" y2="540" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFCC33" stop-opacity="0.36"/>
      <stop offset="1" stop-color="#FFCC33" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="640" height="720" fill="#F8F8F6"/>
  <image href="https://images.unsplash.com/photo-editorial-minimalist-female-fashion-architectural-blazer.jpg"
         x="640" y="0" width="640" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#rightPhotoClip)"/>
  <rect x="640" y="0" width="640" height="720" fill="url(#photoShade)"/>
  <rect x="636" y="0" width="8" height="720" fill="#141414"/>

  <path d="M72,112 C140,52 236,62 288,128 C334,188 286,270 194,258 C112,248 28,192 72,112 Z"
        fill="url(#goldWash)"/>
  <path d="M510,612 C562,582 594,610 590,648 C586,694 506,696 462,672 C426,652 456,642 510,612 Z"
        fill="#FFCC33" opacity="0.14"/>

  <text x="72" y="74" width="220" font-family="Segoe UI" font-size="14" font-weight="700" letter-spacing="4" fill="#1E1E1E">
    CONCEPT 01
  </text>
  <line x1="72" y1="96" x2="154" y2="96" stroke="#FFCC33" stroke-width="5"/>
  <text x="72" y="150" width="480" font-family="Segoe UI" font-size="46" font-weight="800" letter-spacing="-1.5" fill="#1E1E1E">
    AVANT-GARDE MINIMALISM
  </text>
  <text x="74" y="198" width="448" font-family="Segoe UI" font-size="15" fill="#5D5D5D">
    A restrained silhouette system for AI-assisted luxury womenswear direction.
  </text>

  <rect x="70" y="244" width="506" height="264" rx="18" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.98"/>

  <rect x="92" y="270" width="132" height="48" rx="6" fill="#1E2D3C"/>
  <rect x="232" y="270" width="214" height="48" rx="6" fill="#64788C"/>
  <rect x="454" y="270" width="98" height="48" rx="6" fill="#C8C8C8"/>
  <text x="110" y="300" width="100" font-family="Segoe UI" font-size="12" font-weight="800" letter-spacing="1.3" fill="#FFFFFF">FIELD</text>
  <text x="250" y="300" width="168" font-family="Segoe UI" font-size="12" font-weight="800" letter-spacing="1.3" fill="#FFFFFF">SPECIFICATION</text>
  <text x="470" y="300" width="70" font-family="Segoe UI" font-size="12" font-weight="800" letter-spacing="1.3" fill="#1E1E1E">INDEX</text>

  <rect x="92" y="328" width="132" height="48" rx="6" fill="#1E2D3C"/>
  <rect x="232" y="328" width="214" height="48" rx="6" fill="#EEF0F2"/>
  <rect x="454" y="328" width="98" height="48" rx="6" fill="#D8DDE2"/>
  <text x="110" y="358" width="98" font-family="Segoe UI" font-size="13" font-weight="700" fill="#FFFFFF">SILHOUETTE</text>
  <text x="250" y="358" width="180" font-family="Segoe UI" font-size="13" fill="#202020">Oversized blazer, tapered trouser</text>
  <text x="474" y="358" width="58" font-family="Segoe UI" font-size="13" font-weight="800" fill="#1E2D3C">92%</text>

  <rect x="92" y="386" width="132" height="48" rx="6" fill="#1E2D3C"/>
  <rect x="232" y="386" width="214" height="48" rx="6" fill="#EEF0F2"/>
  <rect x="454" y="386" width="98" height="48" rx="6" fill="#BFC7CF"/>
  <text x="110" y="416" width="98" font-family="Segoe UI" font-size="13" font-weight="700" fill="#FFFFFF">FABRIC</text>
  <text x="250" y="416" width="180" font-family="Segoe UI" font-size="13" fill="#202020">Matte silk-wool, bonded seams</text>
  <text x="474" y="416" width="58" font-family="Segoe UI" font-size="13" font-weight="800" fill="#1E2D3C">86%</text>

  <rect x="92" y="444" width="132" height="48" rx="6" fill="#1E2D3C"/>
  <rect x="232" y="444" width="214" height="48" rx="6" fill="#EEF0F2"/>
  <rect x="454" y="444" width="98" height="48" rx="6" fill="#A8B5C1"/>
  <text x="110" y="474" width="98" font-family="Segoe UI" font-size="13" font-weight="700" fill="#FFFFFF">DETAIL</text>
  <text x="250" y="474" width="180" font-family="Segoe UI" font-size="13" fill="#202020">Hidden placket, asymmetric hem</text>
  <text x="474" y="474" width="58" font-family="Segoe UI" font-size="13" font-weight="800" fill="#1E2D3C">78%</text>

  <text x="72" y="558" width="470" font-family="Segoe UI" font-size="21" font-weight="800" font-style="italic" fill="#1E1E1E">
    “The silhouette becomes the narrative: subtractive, severe, and quietly cinematic.”
  </text>
  <text x="74" y="620" width="440" font-family="Segoe UI" font-size="13" fill="#646464">
    Professional review · prompt architecture · collection viability
  </text>

  <rect x="692" y="584" width="330" height="72" rx="12" fill="#141414" opacity="0.76"/>
  <text x="716" y="616" width="286" font-family="Segoe UI" font-size="14" font-weight="700" letter-spacing="2" fill="#FFCC33">
    LOOKBOOK FRAME
  </text>
  <text x="716" y="642" width="286" font-family="Segoe UI" font-size="15" fill="#FFFFFF">
    Editorial crop, full-bleed right pane, cinematic contrast.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Standard gridline-heavy tables; the look depends on filled editorial cells, not spreadsheet borders.
- ❌ Centering the image with margins; the right pane must feel like a cropped magazine page or campaign still.
- ❌ Applying `clip-path` to table rectangles or overlays; only clip the `<image>` for reliable translation.
- ❌ Thin low-contrast typography for the concept title; use bold, compressed-feeling sans-serif hierarchy.
- ❌ Adding chart axes, legends, or dashboard widgets; data should read as curated product metadata.

## Composition notes
- Keep the split strict: left 50% is analytical and typographic, right 50% is emotional full-bleed imagery.
- Use generous padding on the left pane; the table should align with the headline and quote, not float independently.
- Restrict the palette to charcoal, off-white, gold, navy, slate, and silver for a luxury editorial rhythm.
- Let the photo dominate the emotional tone while the table provides structured proof and decision-ready detail.