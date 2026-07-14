# SVG Recipe — Aspect-Perfect Shape Masks

## Visual mechanism
Place a square-cropped photograph inside a non-rectangular mask whose bounding box has the same aspect ratio, then draw the mask outline as a separate editable shape. The photo never stretches; the shape boundary can be circular, polygonal, diamond, or custom-cut while the subject remains naturally proportioned.

## SVG primitives needed
- 1× `<rect>` for the dark keynote-style background
- 2× `<linearGradient>` for background and PowerPoint logo styling
- 1× `<filter id="softShadow">` applied to mask backplates and arrow shapes
- 1× `<clipPath>` with `<circle>` for the left circular photo mask
- 1× `<clipPath>` with `<path>` for the right faceted polygon photo mask
- 2× `<image>` elements using square-cropped source photos, each clipped to a different mask
- 1× `<circle>` and 1× `<path>` as white mask backplates / editable visible borders
- 1× `<path>` for a curved red arrow body and 1× `<path>` for its arrowhead
- 4× `<text>` elements for the headline and footer note
- 4× `<rect>` / `<circle>` elements for a simplified editable PowerPoint badge

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0d0d0d"/>
      <stop offset="0.52" stop-color="#242424"/>
      <stop offset="1" stop-color="#1a1a1a"/>
    </linearGradient>

    <linearGradient id="pptGrad" x1="34" y1="48" x2="178" y2="152" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff8a62"/>
      <stop offset="1" stop-color="#d74726"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="7"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="circleMask" clipPathUnits="userSpaceOnUse">
      <circle cx="322" cy="418" r="258"/>
    </clipPath>

    <clipPath id="facetedMask" clipPathUnits="userSpaceOnUse">
      <path d="M970 128 L1087 164 L1167 266 L1219 410 L1181 554 L1079 653 L970 690 L831 647 L727 548 L691 413 L729 271 L834 165 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- Editable PowerPoint-style badge -->
  <circle cx="112" cy="86" r="67" fill="url(#pptGrad)"/>
  <path d="M112 19 A67 67 0 0 1 179 86 L112 86 Z" fill="#ff9b72" opacity="0.85"/>
  <path d="M112 86 L179 86 A67 67 0 0 1 112 153 Z" fill="#cb3f24" opacity="0.85"/>
  <rect x="35" y="49" width="76" height="75" rx="7" fill="#bf3b21" filter="url(#softShadow)"/>
  <rect x="32" y="48" width="74" height="74" rx="7" fill="#d84a2b"/>
  <text x="56" y="99" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="700" fill="#ffffff">P</text>

  <!-- Headline -->
  <text x="194" y="118" width="1010" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="800" letter-spacing="3" fill="#ffffff">Add Photos like a PRO</text>

  <!-- Left: circle mask with square photo -->
  <circle cx="322" cy="418" r="263" fill="#ffffff" filter="url(#softShadow)"/>
  <image x="64" y="160" width="516" height="516"
         href="https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&amp;w=900&amp;h=900&amp;fit=crop&amp;crop=faces"
         clip-path="url(#circleMask)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="322" cy="418" r="263" fill="none" stroke="#ffffff" stroke-width="7"/>

  <!-- Curved red arrow: path body plus separate arrowhead, no marker-end -->
  <path d="M430 271 C520 199 634 195 725 246"
        fill="none" stroke="#ef1b2d" stroke-width="17" stroke-linecap="round" filter="url(#softShadow)"/>
  <path d="M711 179 C755 185 786 214 810 263 C762 271 727 286 692 306 C699 270 692 238 645 213 C661 180 681 172 711 179 Z"
        fill="#ef1b2d" filter="url(#softShadow)"/>

  <!-- Right: faceted mask with same square photo crop logic -->
  <path d="M970 128 L1087 164 L1167 266 L1219 410 L1181 554 L1079 653 L970 690 L831 647 L727 548 L691 413 L729 271 L834 165 Z"
        fill="#ffffff" filter="url(#softShadow)"/>
  <image x="691" y="128" width="528" height="562"
         href="https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&amp;w=1000&amp;h=1000&amp;fit=crop&amp;crop=faces"
         clip-path="url(#facetedMask)" preserveAspectRatio="xMidYMid slice"/>
  <path d="M970 128 L1087 164 L1167 266 L1219 410 L1181 554 L1079 653 L970 690 L831 647 L727 548 L691 413 L729 271 L834 165 Z"
        fill="none" stroke="#ffffff" stroke-width="7" stroke-linejoin="round"/>

  <!-- Captions emphasize the aspect-safe construction -->
  <text x="105" y="655" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" text-anchor="middle" fill="#ffffff">1:1 photo → circle mask</text>
  <text x="760" y="655" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" text-anchor="middle" fill="#ffffff">same 1:1 crop → polygon mask</text>
  <text x="482" y="689" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#ffffff">No stretching. No squashed portraits.</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to a `<rect>`, `<path>`, or `<g>`; use it only on the `<image>` and draw the visible border as a separate editable shape.
- ❌ Using a tall or wide uncropped portrait inside a square mask unless `preserveAspectRatio="xMidYMid slice"` and a square source/crop URL are used.
- ❌ Using `marker-end` for the arrow; build the arrowhead as its own filled `<path>`.
- ❌ Relying on PowerPoint picture-fill stretching to solve the crop; match the image crop ratio to the mask’s bounding box first.

## Composition notes
- Keep the photo mask bounding boxes square for circles, diamonds, regular polygons, and most avatar-style crops.
- Draw the white mask backplate first, place the clipped image above it, then add a separate stroke outline on top for a crisp editable edge.
- Use a dark or low-detail background so the white mask boundary clearly separates the photo from the slide.
- When demonstrating a transformation, show the same square-cropped image in two different masks with an arrow between them to make the “shape changes, photo stays natural” concept obvious.