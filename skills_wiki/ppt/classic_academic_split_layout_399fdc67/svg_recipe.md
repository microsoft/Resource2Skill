# SVG Recipe — Classic Academic Split-Layout

## Visual mechanism
A rigid vertical split pairs a warm ivory editorial text pane with a full-bleed photographic pane. The authority comes from oversized serif typography, disciplined key-value metadata, and generous negative space, creating the feel of a museum label, academic monograph, or premium magazine spread.

## SVG primitives needed
- 1× `<rect>` for the warm ivory slide background
- 1× `<clipPath>` with a rectangular crop for the right-side image pane
- 1× `<image>` for the full-bleed right-pane hero photograph or texture
- 2× `<linearGradient>` for subtle paper warmth and image-edge shading
- 1× `<filter id="softShadow">` for restrained editorial depth on the left text card accent
- 4× `<path>` for fine marble/paper vein decoration and a botanical academic ornament
- 5× `<line>` for the split boundary, title rule, and metadata separators
- 8× `<text>` blocks with explicit `width` attributes for title, subtitle, section label, body, and key-value details
- 1× `<rect>` for a small shaded annotation plate behind the specimen label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F3EFE4"/>
      <stop offset="58%" stop-color="#EEEADF"/>
      <stop offset="100%" stop-color="#E6DED0"/>
    </linearGradient>

    <linearGradient id="photoShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1E140F" stop-opacity="0.22"/>
      <stop offset="18%" stop-color="#1E140F" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#1E140F" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="rightPaneCrop">
      <rect x="640" y="0" width="640" height="720"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paperWash)"/>

  <path d="M70 95 C155 70, 218 92, 280 54 S405 35, 510 82" fill="none" stroke="#D8CFBF" stroke-width="2" opacity="0.32"/>
  <path d="M85 655 C185 605, 280 642, 360 592 S492 560, 572 615" fill="none" stroke="#D3C7B5" stroke-width="2" opacity="0.28"/>
  <path d="M540 135 C515 180, 515 226, 548 266 C570 292, 584 326, 570 365" fill="none" stroke="#BDAF9A" stroke-width="1.4" opacity="0.42"/>
  <path d="M560 216 C583 197, 610 194, 630 211 C605 228, 582 230, 560 216 Z" fill="#BDAF9A" opacity="0.22"/>

  <image
    href="https://images.example.com/editorial-full-bleed-red-apples-or-classical-marble-texture.jpg"
    xlink:href="https://images.example.com/editorial-full-bleed-red-apples-or-classical-marble-texture.jpg"
    x="640" y="0" width="640" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#rightPaneCrop)"/>

  <rect x="640" y="0" width="96" height="720" fill="url(#photoShade)"/>
  <line x1="640" y1="0" x2="640" y2="720" stroke="#2D1E14" stroke-width="1.5" opacity="0.48"/>

  <text x="86" y="82" width="450"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="15" letter-spacing="3.5"
        fill="#6D5A47">
    BOTANICAL NOTEBOOK / NO. 017
  </text>

  <line x1="86" y1="112" x2="274" y2="112" stroke="#8D755C" stroke-width="1.6"/>

  <text x="82" y="214" width="470"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="76" line-height="0.92"
        fill="#2D1E14">
    <tspan x="82" dy="0">Red</tspan>
    <tspan x="82" dy="72">Delicious</tspan>
  </text>

  <text x="88" y="330" width="420"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="20"
        fill="#5F5042">
    An editorial specimen profile for orchard planning, culinary selection, and seasonal purchasing.
  </text>

  <rect x="84" y="390" width="430" height="186" rx="2" fill="#F8F4EA" opacity="0.76" filter="url(#softShadow)"/>
  <line x1="112" y1="437" x2="486" y2="437" stroke="#C8BBA8" stroke-width="1"/>
  <line x1="112" y1="482" x2="486" y2="482" stroke="#C8BBA8" stroke-width="1"/>
  <line x1="112" y1="527" x2="486" y2="527" stroke="#C8BBA8" stroke-width="1"/>

  <text x="112" y="420" width="120"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="18" letter-spacing="1.4"
        fill="#7A654F">
    SEASON
  </text>
  <text x="278" y="420" width="210"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="22"
        fill="#302016">
    Sep — Jan
  </text>

  <text x="112" y="465" width="120"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="18" letter-spacing="1.4"
        fill="#7A654F">
    FLAVOR
  </text>
  <text x="278" y="465" width="210"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="22"
        fill="#302016">
    Mild, sweet
  </text>

  <text x="112" y="510" width="120"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="18" letter-spacing="1.4"
        fill="#7A654F">
    USES
  </text>
  <text x="278" y="510" width="210"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="22"
        fill="#302016">
    Snacking
  </text>

  <text x="112" y="555" width="120"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="18" letter-spacing="1.4"
        fill="#7A654F">
    COST
  </text>
  <text x="278" y="555" width="210"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="22"
        fill="#302016">
    Low
  </text>

  <text x="86" y="642" width="420"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="14"
        fill="#7C6D5E">
    Archive classification: Malus domestica · Market cultivar · North American harvest calendar
  </text>
</svg>
```

## Avoid in this skill
- ❌ Centered titles or symmetrical grids; the style depends on a strict editorial split and left-aligned reading flow.
- ❌ Busy bullet lists; use restrained key-value rows, short annotations, or museum-label prose.
- ❌ Applying `clip-path` to decorative rectangles or text; only clip the `<image>` for reliable PowerPoint translation.
- ❌ Low-contrast gray typography on ivory; use deep espresso/charcoal for academic authority.
- ❌ Overly rounded cards, neon colors, or dashboard UI styling, which break the classical editorial mood.

## Composition notes
- Keep the split boundary exact and calm: the image pane should touch the top, bottom, and right edges, while the left pane breathes with wide margins.
- Use the left 50% for hierarchy: small uppercase eyebrow, large serif title, short description, then structured metadata.
- Let the right image carry organic texture and color; avoid placing important text over it unless using a dedicated caption system.
- Preserve a warm neutral rhythm: ivory background, espresso typography, muted tan rules, and one rich natural photo palette.