# SVG Recipe — Thematic Collage Hero Slide

## Visual mechanism
A symmetrical editorial collage: a muted thematic texture fills the slide, a vivid central artwork card anchors the composition, and a circular globe/photo breaks the card’s top edge for layered depth. Large serif title typography sits directly over the centerpiece with shadow and translucent overlays for legibility.

## SVG primitives needed
- 2× `<image>` for full-slide textured background and central cultural hero artwork
- 1× `<image>` clipped by circular `<clipPath>` for the overlapping globe accent
- 2× `<clipPath>` for rounded-rectangle hero image crop and circular globe crop
- 4× `<rect>` for sepia wash, hero frame, dark readability overlay, and title plaque
- 6× `<path>` for subtle map-contour strokes, side ornaments, scroll/book-like cultural accents, and decorative corner flourishes
- 2× `<circle>` / `<ellipse>` for globe rim and soft halo accents
- 1× `<linearGradient>` for cinematic dark overlay on the central image
- 1× `<radialGradient>` for spotlighting the center while keeping edges quiet
- 2× `<filter>` with blur/offset for card shadow and text/globe depth
- 4× `<text>` elements with explicit `width` for subtitle, title shadow, title, and small eyebrow label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="heroDarken" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.18"/>
      <stop offset="48%" stop-color="#000000" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.62"/>
    </linearGradient>
    <radialGradient id="bgSpotlight" cx="50%" cy="48%" r="68%">
      <stop offset="0%" stop-color="#f0d9ad" stop-opacity="0.28"/>
      <stop offset="70%" stop-color="#8b6840" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#3a2a1e" stop-opacity="0.42"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="heroClip">
      <rect x="224" y="210" width="832" height="420" rx="18" ry="18"/>
    </clipPath>
    <clipPath id="globeClip">
      <circle cx="640" cy="188" r="126"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#c8a46c"/>
  <image href="https://images.example.com/sepia-relief-world-map-ancient-trade-routes.jpg" x="0" y="0" width="1280" height="720" opacity="0.44" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="#9b6f3f" opacity="0.38"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgSpotlight)"/>

  <path d="M65 182 C165 128, 248 155, 340 108 S540 58, 644 128 S844 205, 1004 140 S1180 102, 1245 158" fill="none" stroke="#5e432d" stroke-width="2" opacity="0.26"/>
  <path d="M42 520 C190 455, 262 528, 390 468 S625 388, 760 472 S1018 555, 1216 474" fill="none" stroke="#fff0c6" stroke-width="2" opacity="0.18"/>
  <path d="M105 316 C210 282, 326 330, 430 290 C550 242, 634 294, 760 270 C916 240, 1010 304, 1178 268" fill="none" stroke="#6d4e34" stroke-width="1.5" stroke-dasharray="10 10" opacity="0.32"/>

  <path d="M166 224 C126 246, 108 300, 134 342 C164 390, 226 382, 254 334 C281 287, 229 244, 166 224 Z" fill="#3f2b20" opacity="0.24"/>
  <path d="M1014 234 C1065 215, 1132 244, 1147 302 C1161 358, 1116 399, 1058 382 C1008 368, 978 298, 1014 234 Z" fill="#3f2b20" opacity="0.22"/>

  <rect x="204" y="190" width="872" height="460" rx="28" fill="#2a1d18" opacity="0.32" filter="url(#cardShadow)"/>
  <rect x="214" y="200" width="852" height="440" rx="24" fill="#e8c687" opacity="0.85"/>
  <image href="https://images.example.com/vibrant-afro-asian-cultural-art-collage-textile-architecture.jpg" x="224" y="210" width="832" height="420" clip-path="url(#heroClip)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="224" y="210" width="832" height="420" rx="18" fill="url(#heroDarken)"/>

  <ellipse cx="640" cy="194" rx="156" ry="42" fill="#2b1b12" opacity="0.28" filter="url(#softShadow)"/>
  <circle cx="640" cy="188" r="135" fill="#f0d38e" opacity="0.94" filter="url(#softShadow)"/>
  <image href="https://images.example.com/earth-globe-satellite-view-indian-ocean-africa-asia.jpg" x="514" y="62" width="252" height="252" clip-path="url(#globeClip)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="640" cy="188" r="126" fill="none" stroke="#fff4c9" stroke-width="8" opacity="0.88"/>
  <circle cx="640" cy="188" r="137" fill="none" stroke="#5b341d" stroke-width="3" opacity="0.48"/>

  <path d="M112 478 L214 452 L246 542 L142 574 Z M134 501 L224 478 M146 532 L236 508" fill="#b77943" stroke="#4a2e20" stroke-width="4" opacity="0.92"/>
  <path d="M1058 470 C1098 450, 1158 462, 1190 498 L1168 578 C1138 546, 1084 536, 1046 558 Z" fill="#6f3e28" stroke="#f2d08c" stroke-width="5" opacity="0.92"/>
  <path d="M1068 493 C1102 478, 1143 486, 1168 512 M1062 522 C1098 507, 1134 514, 1160 538" fill="none" stroke="#f7dfaa" stroke-width="3" opacity="0.85"/>

  <path d="M252 232 L300 232 L300 248 L272 248 L272 276 L252 276 Z" fill="#fff0c8" opacity="0.75"/>
  <path d="M1028 232 L980 232 L980 248 L1008 248 L1008 276 L1028 276 Z" fill="#fff0c8" opacity="0.75"/>
  <path d="M252 610 L300 610 L300 594 L272 594 L272 566 L252 566 Z" fill="#fff0c8" opacity="0.72"/>
  <path d="M1028 610 L980 610 L980 594 L1008 594 L1008 566 L1028 566 Z" fill="#fff0c8" opacity="0.72"/>

  <rect x="318" y="380" width="644" height="146" rx="18" fill="#000000" opacity="0.24"/>
  <text x="640" y="356" width="520" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" letter-spacing="5" fill="#ffe7aa" opacity="0.95">CHAPTER ONE</text>
  <text x="646" y="454" width="760" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="74" font-weight="700" letter-spacing="2" fill="#1b0e08" opacity="0.68">AFRO-ASIAN</text>
  <text x="640" y="448" width="760" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="74" font-weight="700" letter-spacing="2" fill="#fff8dd">AFRO-ASIAN</text>
  <text x="640" y="526" width="760" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="66" font-weight="700" letter-spacing="3" fill="#fff8dd" filter="url(#softShadow)">LITERATURE</text>
  <text x="640" y="586" width="460" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#f8ddb0" opacity="0.95">A cultural journey across memory, language, and place</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to make the globe circular; use `<clipPath>` on the `<image>` instead.
- ❌ Applying `clip-path` to decorative rectangles or paths; PPT-Master only preserves clipping reliably on images.
- ❌ Building the collage from flat rectangles only; this technique depends on layered photos, organic paths, shadows, and texture.
- ❌ Putting the title on an empty white area; the editorial effect comes from typography superimposed over the hero artwork.
- ❌ Overusing saturated background imagery behind the card; keep the outer map/texture muted so the central collage stays dominant.

## Composition notes
- Keep the central image around 65% of slide width and 55–60% of slide height, centered horizontally with generous textured margins.
- Let the circular globe overlap the top edge of the hero rectangle by roughly one third of its diameter to create a 2.5D breakout effect.
- Use warm sepia, ochre, ivory, and dark umber as the base rhythm; reserve saturated color for the central artwork.
- Title text should be large, centered, serif, and high contrast, with a dark translucent plaque or shadow behind it for legibility.