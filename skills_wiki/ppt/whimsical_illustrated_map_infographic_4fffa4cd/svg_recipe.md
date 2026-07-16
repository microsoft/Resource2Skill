# SVG Recipe — Whimsical Illustrated Map Infographic

## Visual mechanism
A playful “storybook map” turns a list of places or journey steps into an explorable scene: a thick winding road guides the eye through sticker-like markers, tiny illustrated landmarks, and floating rounded label bubbles. Geographic accuracy is secondary; the impact comes from pastel terrain, hand-drawn curves, high-contrast ink outlines, and editable text.

## SVG primitives needed
- 1× `<rect>` for the full pastel map canvas background.
- 6–10× translucent `<ellipse>` / `<path>` terrain blobs for watercolor-like land texture.
- 2× large stroked `<path>` for the winding road: one dark outline under one cream road fill.
- 1× dashed stroked `<path>` for the road centerline.
- 5× sticker marker groups using `<circle>` for white die-cut border, colored pin body, and inner icon disk.
- 5× rounded `<rect>` label bubbles with dark outlines and soft shadows.
- 5× `<text>` blocks with nested `<tspan>` for editable place names and descriptions.
- 5× small `<line>` connector strokes from labels to markers.
- Multiple decorative `<path>`, `<rect>`, `<circle>`, and `<ellipse>` elements for trees, café, park, river, bridge, compass, clouds, and miniature buildings.
- 2× `<linearGradient>` / `<radialGradient>` for premium pastel depth.
- 2× `<filter>` definitions: one soft shadow for stickers/labels, one blur for background terrain blobs.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EAF6DC"/>
      <stop offset="55%" stop-color="#DDF0D8"/>
      <stop offset="100%" stop-color="#F6E8C9"/>
    </linearGradient>
    <radialGradient id="pondGrad" cx="45%" cy="40%" r="70%">
      <stop offset="0%" stop-color="#BDEFFF"/>
      <stop offset="100%" stop-color="#7BCFE7"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="6" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="terrainBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <ellipse cx="130" cy="120" rx="230" ry="115" fill="#CFE8C5" opacity="0.55" filter="url(#terrainBlur)"/>
  <ellipse cx="1110" cy="155" rx="250" ry="130" fill="#F3D7A8" opacity="0.38" filter="url(#terrainBlur)"/>
  <ellipse cx="920" cy="640" rx="320" ry="130" fill="#C6E4BB" opacity="0.45" filter="url(#terrainBlur)"/>
  <path d="M30,525 C160,470 225,520 330,475 C430,432 510,463 602,425 C706,381 805,395 900,430 C1010,472 1118,450 1260,385 L1280,720 L0,720 Z"
        fill="#D8EECF" opacity="0.58"/>

  <path d="M-30,170 C145,88 305,135 390,220 C490,320 352,430 500,505 C645,580 730,420 870,470 C995,515 1015,625 1320,570"
        fill="none" stroke="#463228" stroke-width="78" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>
  <path d="M-30,170 C145,88 305,135 390,220 C490,320 352,430 500,505 C645,580 730,420 870,470 C995,515 1015,625 1320,570"
        fill="none" stroke="#FFF9EA" stroke-width="58" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M-30,170 C145,88 305,135 390,220 C490,320 352,430 500,505 C645,580 730,420 870,470 C995,515 1015,625 1320,570"
        fill="none" stroke="#E7CFA2" stroke-width="5" stroke-linecap="round" stroke-dasharray="18 22" opacity="0.85"/>

  <ellipse cx="1045" cy="260" rx="95" ry="58" fill="url(#pondGrad)" stroke="#463228" stroke-width="5"/>
  <path d="M982,260 C1015,242 1075,247 1111,270" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.7"/>
  <path d="M1015,312 C1050,292 1090,303 1120,286" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.55"/>

  <g transform="translate(80 555)">
    <circle cx="0" cy="0" r="25" fill="#FFFFFF" stroke="#463228" stroke-width="4"/>
    <path d="M-14,5 C-35,-28 28,-28 12,5 C34,4 28,35 0,25 C-28,35 -34,4 -14,5 Z" fill="#7CCB82" stroke="#463228" stroke-width="4"/>
    <rect x="-4" y="18" width="8" height="35" rx="4" fill="#8B5E3C"/>
  </g>
  <g transform="translate(1170 88)">
    <circle cx="0" cy="0" r="20" fill="#FFFFFF" stroke="#463228" stroke-width="4"/>
    <path d="M0,-14 L8,8 L0,4 L-8,8 Z" fill="#FF9B8F" stroke="#463228" stroke-width="3"/>
    <text x="-52" y="48" width="104" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#463228">N</text>
  </g>

  <g transform="translate(165 118)" filter="url(#softShadow)">
    <line x1="48" y1="70" x2="130" y2="112" stroke="#463228" stroke-width="4" stroke-linecap="round"/>
    <rect x="108" y="86" width="252" height="92" rx="28" fill="#FFF7D8" stroke="#463228" stroke-width="4"/>
    <text x="132" y="120" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#463228">Sunrise Bakery</text>
    <text x="132" y="148" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6A5044">
      <tspan x="132" dy="0">Fresh buns at Gate 1</tspan>
      <tspan x="132" dy="19">Start here with coffee</tspan>
    </text>
    <circle cx="0" cy="0" r="42" fill="#FFFFFF" stroke="#463228" stroke-width="5"/>
    <circle cx="0" cy="0" r="29" fill="#FFB6C1"/>
    <path d="M-14,7 C-18,-11 15,-15 17,2 C19,18 -9,21 -14,7 Z" fill="#FFF4E0" stroke="#463228" stroke-width="4"/>
    <path d="M-4,-13 C3,-24 18,-19 18,-6" fill="none" stroke="#463228" stroke-width="4" stroke-linecap="round"/>
  </g>

  <g transform="translate(395 260)" filter="url(#softShadow)">
    <line x1="-42" y1="16" x2="-145" y2="74" stroke="#463228" stroke-width="4" stroke-linecap="round"/>
    <rect x="-390" y="42" width="270" height="96" rx="30" fill="#E8F9FF" stroke="#463228" stroke-width="4"/>
    <text x="-362" y="77" width="218" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#463228">Blue Tile Market</text>
    <text x="-362" y="105" width="218" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6A5044">
      <tspan x="-362" dy="0">Local snacks + produce</tspan>
      <tspan x="-362" dy="19">Best stop for souvenirs</tspan>
    </text>
    <circle cx="0" cy="0" r="42" fill="#FFFFFF" stroke="#463228" stroke-width="5"/>
    <circle cx="0" cy="0" r="29" fill="#99CCFF"/>
    <path d="M-18,12 L18,12 L14,-12 L-14,-12 Z" fill="#FFFFFF" stroke="#463228" stroke-width="4"/>
    <path d="M-20,-12 L20,-12 L12,-23 L-12,-23 Z" fill="#FFCC66" stroke="#463228" stroke-width="4"/>
  </g>

  <g transform="translate(520 505)" filter="url(#softShadow)">
    <line x1="35" y1="-22" x2="100" y2="-95" stroke="#463228" stroke-width="4" stroke-linecap="round"/>
    <rect x="82" y="-178" width="276" height="98" rx="30" fill="#FDE7F3" stroke="#463228" stroke-width="4"/>
    <text x="110" y="-142" width="222" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#463228">Cherry Garden</text>
    <text x="110" y="-114" width="222" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6A5044">
      <tspan x="110" dy="0">Quiet picnic lawn</tspan>
      <tspan x="110" dy="19">Photo spot under blossoms</tspan>
    </text>
    <circle cx="0" cy="0" r="42" fill="#FFFFFF" stroke="#463228" stroke-width="5"/>
    <circle cx="0" cy="0" r="29" fill="#98FB98"/>
    <path d="M0,-21 C-22,-17 -26,7 -6,11 C-14,28 15,29 9,10 C31,5 21,-20 0,-21 Z" fill="#FFFFFF" stroke="#463228" stroke-width="4"/>
    <circle cx="-8" cy="-4" r="4" fill="#FF8FA3"/>
    <circle cx="8" cy="2" r="4" fill="#FF8FA3"/>
  </g>

  <g transform="translate(825 455)" filter="url(#softShadow)">
    <line x1="-30" y1="30" x2="-110" y2="110" stroke="#463228" stroke-width="4" stroke-linecap="round"/>
    <rect x="-385" y="100" width="290" height="100" rx="30" fill="#FFF0C8" stroke="#463228" stroke-width="4"/>
    <text x="-355" y="136" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#463228">Lantern Alley</text>
    <text x="-355" y="164" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6A5044">
      <tspan x="-355" dy="0">Street food after sunset</tspan>
      <tspan x="-355" dy="19">Warm lights, tiny shops</tspan>
    </text>
    <circle cx="0" cy="0" r="42" fill="#FFFFFF" stroke="#463228" stroke-width="5"/>
    <circle cx="0" cy="0" r="29" fill="#FFCC66"/>
    <path d="M-15,-13 L15,-13 L11,13 L-11,13 Z" fill="#FF6F61" stroke="#463228" stroke-width="4"/>
    <line x1="0" y1="-24" x2="0" y2="-13" stroke="#463228" stroke-width="4" stroke-linecap="round"/>
    <path d="M-8,0 C-1,-8 6,-8 10,0" fill="none" stroke="#FFF7D8" stroke-width="3" stroke-linecap="round"/>
  </g>

  <g transform="translate(1085 570)" filter="url(#softShadow)">
    <line x1="-42" y1="-5" x2="-155" y2="-60" stroke="#463228" stroke-width="4" stroke-linecap="round"/>
    <rect x="-402" y="-126" width="286" height="96" rx="30" fill="#E7E0FF" stroke="#463228" stroke-width="4"/>
    <text x="-374" y="-91" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#463228">Moon Tea House</text>
    <text x="-374" y="-63" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6A5044">
      <tspan x="-374" dy="0">Final stop for dessert</tspan>
      <tspan x="-374" dy="19">Try the jasmine pudding</tspan>
    </text>
    <circle cx="0" cy="0" r="42" fill="#FFFFFF" stroke="#463228" stroke-width="5"/>
    <circle cx="0" cy="0" r="29" fill="#DDA0DD"/>
    <path d="M-13,10 C-17,-11 9,-24 20,-6 C10,-8 1,2 6,16 C-1,18 -9,17 -13,10 Z" fill="#FFFFFF" stroke="#463228" stroke-width="4"/>
  </g>

  <g transform="translate(900 118)">
    <rect x="-34" y="10" width="68" height="58" rx="8" fill="#F7C891" stroke="#463228" stroke-width="4"/>
    <path d="M-44,12 L0,-25 L44,12 Z" fill="#FF8F86" stroke="#463228" stroke-width="4"/>
    <rect x="-12" y="34" width="24" height="34" rx="4" fill="#7BCFE7" stroke="#463228" stroke-width="3"/>
    <circle cx="-205" cy="14" r="18" fill="#FFFFFF" opacity="0.75"/>
    <circle cx="-180" cy="10" r="25" fill="#FFFFFF" opacity="0.75"/>
    <circle cx="-150" cy="18" r="16" fill="#FFFFFF" opacity="0.75"/>
  </g>

  <rect x="46" y="34" width="430" height="62" rx="31" fill="#FFFFFF" stroke="#463228" stroke-width="5" filter="url(#softShadow)"/>
  <text x="78" y="74" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#463228">Weekend Food Walk Map</text>
</svg>
```

## Avoid in this skill
- ❌ Do not generate the full map as one raster image if the labels must remain editable; keep all names and descriptions as SVG `<text>`.
- ❌ Do not use `<textPath>` for curved road labels; it will not translate reliably. Place small horizontal labels or signboards instead.
- ❌ Do not apply `filter` to `<line>` connector strokes; shadows on lines may be dropped. Use clean ink-colored lines.
- ❌ Do not use `mask` or `clip-path` on non-image elements for terrain effects; use soft ellipses and organic `<path>` blobs instead.
- ❌ Do not use `marker-end` arrowheads on paths for navigation direction; draw simple dotted centerlines or separate editable arrow shapes if needed.

## Composition notes
- Keep the road as the dominant visual spine, usually an “S” curve occupying 70–85% of the canvas width.
- Place label bubbles outside the road’s main curve and connect them with short ink lines so the map remains readable.
- Use pastel fills with one consistent dark brown outline color; this creates the hand-inked sticker aesthetic.
- Reserve corners for title, compass, clouds, or small landmarks so the slide feels illustrated rather than like a diagram.