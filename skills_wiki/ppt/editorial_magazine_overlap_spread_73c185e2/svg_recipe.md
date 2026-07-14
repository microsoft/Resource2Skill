# SVG Recipe — Editorial Magazine Overlap Spread

## Visual mechanism
A crisp editorial split spread pairs a narrow white copy panel with a large right-side bleed photograph, then breaks the grid with a saturated headline block that overlaps both zones. Subtle shadow, rotated watermark typography, thin rules, and restrained body copy make the slide feel like a premium magazine opening spread rather than a standard image-and-text layout.

## SVG primitives needed
- 1× `<image>` for the large right-side bleed photograph
- 1× `<clipPath>` with `<rect>` for cropping the photograph to the image side of the spread
- 1× `<rect>` for the white editorial text panel
- 1× `<rect>` with gradient fill and shadow filter for the overlapping accent headline block
- 1× `<filter id="paperShadow">` applied to the accent block for paper-stack depth
- 1× `<linearGradient>` for a richer accent block fill
- 1× `<rect>` translucent overlay on the photo for contrast and mood
- 1× rotated `<text>` for the pale vertical watermark
- 5× `<text>` blocks for eyebrow, headline, section label, body copy, and data/stat callout
- 3× `<line>` elements for thin editorial divider rules
- 2× `<path>` elements for small magazine-style decorative quote/slash accents
- 2× small `<rect>` elements for accent chips and sidebar structure

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoClip">
      <rect x="448" y="0" width="832" height="720"/>
    </clipPath>

    <linearGradient id="cyanBlock" x1="0" y1="0" x2="760" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#00AEEF"/>
      <stop offset="0.58" stop-color="#00A3E2"/>
      <stop offset="1" stop-color="#0077B6"/>
    </linearGradient>

    <linearGradient id="photoShade" x1="448" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.28"/>
      <stop offset="0.55" stop-color="#000000" stop-opacity="0.04"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.24"/>
    </linearGradient>

    <filter id="paperShadow" x="-10%" y="-25%" width="130%" height="160%">
      <feOffset dx="18" dy="18"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- right-side photographic bleed -->
  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>
  <image
    href="https://images.example.com/editorial-fashion-architecture-hero-photo.jpg"
    x="448" y="0" width="832" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoClip)"/>
  <rect x="448" y="0" width="832" height="720" fill="url(#photoShade)"/>

  <!-- left editorial panel -->
  <rect x="0" y="0" width="448" height="720" fill="#ffffff"/>
  <line x1="448" y1="0" x2="448" y2="720" stroke="#E9E9E9" stroke-width="1"/>

  <!-- pale rotated watermark -->
  <text x="-648" y="118" width="620"
        transform="rotate(-90)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="86" font-weight="800"
        letter-spacing="7"
        fill="#F1F1F1">EDITORIAL</text>

  <!-- small editorial eyebrow -->
  <text x="58" y="92" width="285"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="800"
        letter-spacing="3"
        fill="#00AEEF">INSIGHT REPORT / 2026</text>
  <line x1="58" y1="116" x2="198" y2="116" stroke="#00AEEF" stroke-width="3"/>
  <line x1="210" y1="116" x2="370" y2="116" stroke="#D9D9D9" stroke-width="1"/>

  <!-- overlapping accent headline block -->
  <rect x="0" y="142" width="770" height="190" fill="url(#cyanBlock)" filter="url(#paperShadow)"/>
  <rect x="728" y="142" width="42" height="190" fill="#004E7A" fill-opacity="0.22"/>

  <text x="56" y="199" width="640"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800"
        letter-spacing="1.5"
        fill="#ffffff">
    <tspan x="56" dy="0">THE TRUE STORY</tspan>
    <tspan x="56" dy="57">OF DESIGN</tspan>
  </text>

  <!-- left panel body copy -->
  <text x="58" y="392" width="318"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="800"
        letter-spacing="2.3"
        fill="#111111">FIELD NOTES</text>
  <line x1="58" y1="414" x2="104" y2="414" stroke="#00AEEF" stroke-width="4"/>

  <text x="58" y="452" width="318"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700"
        fill="#222222">When visual systems become strategic assets.</text>

  <text x="58" y="500" width="326"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        line-height="1.45"
        fill="#666666">
    <tspan x="58" dy="0">High-performing brands use space,</tspan>
    <tspan x="58" dy="24">contrast, and rhythm to make complex</tspan>
    <tspan x="58" dy="24">ideas feel inevitable. This spread turns</tspan>
    <tspan x="58" dy="24">one image, one claim, and one signal</tspan>
    <tspan x="58" dy="24">metric into a confident opening page.</tspan>
  </text>

  <!-- compact data/stat editorial callout -->
  <rect x="58" y="626" width="8" height="44" fill="#00AEEF"/>
  <text x="82" y="657" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="40" font-weight="800"
        fill="#111111">37%</text>
  <text x="176" y="646" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600"
        fill="#777777">
    <tspan x="176" dy="0">higher recall when</tspan>
    <tspan x="176" dy="18">layouts use contrast</tspan>
  </text>

  <!-- decorative magazine marks on photo -->
  <path d="M946 514 L986 514 L954 604 L914 604 Z" fill="#00AEEF" fill-opacity="0.88"/>
  <path d="M1002 514 L1042 514 L1010 604 L970 604 Z" fill="#ffffff" fill-opacity="0.82"/>
  <text x="930" y="645" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700"
        letter-spacing="2.2"
        fill="#ffffff">VISUAL CULTURE SERIES</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the right photo area from tiled rectangles or placeholder gradients only; the editorial impact depends on a real bleed image.
- ❌ Do not use `<mask>` to fade the photo edge; use a translucent gradient rectangle overlay instead.
- ❌ Do not clip text or rectangles with `clip-path`; only the `<image>` crop should use `clip-path`.
- ❌ Do not use `textPath` for the vertical watermark; rotate a normal `<text>` element instead.
- ❌ Do not center everything symmetrically; the technique needs intentional asymmetry and overlap.

## Composition notes
- Keep the left panel to roughly 35% of the canvas and the photo to the remaining 65%; the accent headline block should cross the boundary by at least 250–320 px.
- Use the accent block as the visual bridge: it starts flush at the left edge, sits in the upper third, and casts a soft shadow over the photo.
- Preserve generous white space in the lower-left panel; body copy should feel curated, not dense.
- Let color appear in a tight rhythm: eyebrow, divider rule, headline block, and one small stat accent should share the same cyan or brand color.