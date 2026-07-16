# SVG Recipe — Asymmetric Minimalist Catalog Reveal

## Visual mechanism
Create a premium catalog-cover layout by clipping a large product photograph into a right-side diagonal wedge while leaving a wide white editorial space on the left. Use pastel geometric accents and small dotted matrices to make the diagonal seam feel intentional, refined, and lightly structured.

## SVG primitives needed
- 1× `<rect>` for the full-slide white/off-white base
- 1× `<image>` for the edge-to-edge product/catalog photograph, clipped into the asymmetric diagonal right panel
- 1× `<clipPath>` with a `<path>` defining the angled photo crop
- 3× `<path>` for pastel geometric wedges and triangular accents
- 1× `<rect>` with subtle shadow for a small catalog metadata label
- 1× `<filter id="softShadow">` applied to the metadata label rectangle
- 1× `<linearGradient>` for a mint-to-aqua accent seam and triangle fills
- 70+× `<circle>` for dotted grid micro-textures that bridge empty space and the photo edge
- 1× `<line>` for a thin editorial divider
- 8× `<text>` elements with explicit `width` attributes for title, subtitle, metadata, and small catalog labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="mintGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D9FFF4"/>
      <stop offset="55%" stop-color="#AFF4E2"/>
      <stop offset="100%" stop-color="#8BE2D2"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="rightDiagonalPhoto">
      <path d="M600 0 H1280 V720 H770 Z"/>
    </clipPath>
  </defs>

  <!-- Base editorial field -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Pastel seam behind the clipped photo -->
  <path d="M548 0 H626 L800 720 H720 Z" fill="url(#mintGlow)" opacity="0.92"/>

  <!-- Edge-to-edge product photography clipped into an asymmetric diagonal panel -->
  <image href="https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         x="520" y="0" width="820" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#rightDiagonalPhoto)"/>

  <!-- Bottom-right pastel triangle overlay to sharpen the catalog reveal -->
  <path d="M1138 604 L1280 720 H1018 Z" fill="url(#mintGlow)" opacity="0.82"/>
  <path d="M1008 0 H1112 L1060 72 Z" fill="#AFF4E2" opacity="0.58"/>

  <!-- Tiny editorial arrows in the top-left margin -->
  <path d="M82 56 L112 72 L82 88 Z" fill="#AFF4E2"/>
  <path d="M124 56 L154 72 L124 88 Z" fill="#AFF4E2" opacity="0.72"/>
  <path d="M166 56 L196 72 L166 88 Z" fill="#AFF4E2" opacity="0.46"/>

  <!-- Dotted grid crossing the diagonal seam -->
  <g fill="#AFF4E2" opacity="0.9">
    <circle cx="608" cy="426" r="4"/><circle cx="632" cy="426" r="4"/><circle cx="656" cy="426" r="4"/><circle cx="680" cy="426" r="4"/>
    <circle cx="608" cy="450" r="4"/><circle cx="632" cy="450" r="4"/><circle cx="656" cy="450" r="4"/><circle cx="680" cy="450" r="4"/>
    <circle cx="608" cy="474" r="4"/><circle cx="632" cy="474" r="4"/><circle cx="656" cy="474" r="4"/><circle cx="680" cy="474" r="4"/>
    <circle cx="608" cy="498" r="4"/><circle cx="632" cy="498" r="4"/><circle cx="656" cy="498" r="4"/><circle cx="680" cy="498" r="4"/>
    <circle cx="608" cy="522" r="4"/><circle cx="632" cy="522" r="4"/><circle cx="656" cy="522" r="4"/><circle cx="680" cy="522" r="4"/>
    <circle cx="608" cy="546" r="4"/><circle cx="632" cy="546" r="4"/><circle cx="656" cy="546" r="4"/><circle cx="680" cy="546" r="4"/>
    <circle cx="608" cy="570" r="4"/><circle cx="632" cy="570" r="4"/><circle cx="656" cy="570" r="4"/><circle cx="680" cy="570" r="4"/>
    <circle cx="608" cy="594" r="4"/><circle cx="632" cy="594" r="4"/><circle cx="656" cy="594" r="4"/><circle cx="680" cy="594" r="4"/>
    <circle cx="608" cy="618" r="4"/><circle cx="632" cy="618" r="4"/><circle cx="656" cy="618" r="4"/><circle cx="680" cy="618" r="4"/>
    <circle cx="608" cy="642" r="4"/><circle cx="632" cy="642" r="4"/><circle cx="656" cy="642" r="4"/><circle cx="680" cy="642" r="4"/>
  </g>

  <!-- Secondary dot texture in the quiet white space -->
  <g fill="#AFF4E2" opacity="0.36">
    <circle cx="90" cy="610" r="3.5"/><circle cx="114" cy="610" r="3.5"/><circle cx="138" cy="610" r="3.5"/><circle cx="162" cy="610" r="3.5"/><circle cx="186" cy="610" r="3.5"/>
    <circle cx="90" cy="634" r="3.5"/><circle cx="114" cy="634" r="3.5"/><circle cx="138" cy="634" r="3.5"/><circle cx="162" cy="634" r="3.5"/><circle cx="186" cy="634" r="3.5"/>
    <circle cx="90" cy="658" r="3.5"/><circle cx="114" cy="658" r="3.5"/><circle cx="138" cy="658" r="3.5"/><circle cx="162" cy="658" r="3.5"/><circle cx="186" cy="658" r="3.5"/>
  </g>

  <!-- Editorial text system -->
  <text x="82" y="160" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" letter-spacing="4" fill="#1E1E1E">
    CLEAN BEAUTY CATALOG
  </text>

  <text x="78" y="276" width="500" font-family="Georgia, 'Sitka Display', serif" font-size="82" line-height="0.92" fill="#1E1E1E">
    <tspan x="78" dy="0">Products</tspan>
    <tspan x="78" dy="82">Showcase</tspan>
  </text>

  <line x1="82" y1="394" x2="210" y2="394" stroke="#1E1E1E" stroke-width="2" opacity="0.9"/>

  <text x="82" y="438" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" fill="#1E1E1E">
    <tspan x="82" dy="0">A curated reveal of seasonal essentials,</tspan>
    <tspan x="82" dy="30">soft color systems, and tactile formulas.</tspan>
  </text>

  <text x="82" y="526" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" letter-spacing="2.5" fill="#777777">
    EDITION 04  /  SPRING COLLECTION
  </text>

  <!-- Floating catalog label -->
  <rect x="888" y="512" width="258" height="96" rx="22" fill="#FFFFFF" opacity="0.94" filter="url(#softShadow)"/>
  <text x="914" y="552" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" letter-spacing="3" fill="#1E1E1E">
    FEATURED SET
  </text>
  <text x="914" y="584" width="210" font-family="Georgia, 'Sitka Display', serif" font-size="28" fill="#1E1E1E">
    Daily Rituals
  </text>

  <!-- Small vertical catalog code on photo edge -->
  <text x="1196" y="92" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" letter-spacing="3" fill="#FFFFFF" opacity="0.9" transform="rotate(90 1196 92)">
    MINIMALIST REVEAL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` for the dotted grids; create real `<circle>` dots so the texture remains editable in PowerPoint.
- ❌ Do not use `<mask>` to create the diagonal photo crop; use a `<clipPath>` applied directly to the `<image>`.
- ❌ Do not apply `clip-path` to non-image shapes for the seam; use regular `<path>` polygons for editable accent wedges.
- ❌ Do not make the split perfectly vertical; the premium editorial effect depends on a slight diagonal imbalance.
- ❌ Do not overcrowd the left text zone; the white negative space is a core part of the visual mechanism.

## Composition notes
- Keep the left 40–45% mostly white, with the title occupying the upper-middle and body copy below it.
- Let the product photo dominate the right 55–60%, clipped by a diagonal edge that is narrower at the top and wider at the bottom.
- Place dotted matrices near the diagonal seam and in one quiet corner; they should feel like texture, not a chart.
- Use one signature pastel accent color repeatedly in the seam, triangles, and dots to unify the asymmetric layout.