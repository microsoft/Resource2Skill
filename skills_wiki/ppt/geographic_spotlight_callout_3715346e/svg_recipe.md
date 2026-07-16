# SVG Recipe — Geographic Spotlight Callout

## Visual mechanism
A pale vector map establishes geographic context while translucent, conical beams connect precise map pins to larger circular information callouts. The cones share the pin/callout accent color, creating an elegant “spotlight” relationship without hiding the map underneath.

## SVG primitives needed
- 1× `<rect>` for the slide background gradient
- 5× `<path>` for a simplified editable map silhouette and geographic islands
- 6× `<line>` for subtle latitude/longitude grid cues
- 3× `<path>` for translucent spotlight cones from map pins to callout portraits
- 3× `<circle>` for map pins, plus 3× larger halo circles
- 3× `<rect>` for soft rounded information cards behind each callout
- 3× `<image>` clipped to circular `<clipPath>` regions for headshots / office photos
- 3× `<circle>` for circular photo borders matching the location accent color
- Multiple `<text>` elements with explicit `width` for title, labels, metrics, and captions
- 2× `<linearGradient>` for premium background/card fills
- 2× `<filter>` definitions: one shadow filter for cards/photos, one glow filter for pin halos

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="65%" stop-color="#F5F8FC"/>
      <stop offset="100%" stop-color="#EAF0F8"/>
    </linearGradient>

    <linearGradient id="cardFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.96"/>
      <stop offset="100%" stop-color="#F3F6FA" stop-opacity="0.94"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pinGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>

    <clipPath id="clipSeattle"><circle cx="190" cy="174" r="58"/></clipPath>
    <clipPath id="clipAustin"><circle cx="384" cy="574" r="58"/></clipPath>
    <clipPath id="clipToronto"><circle cx="1032" cy="208" r="58"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <text x="76" y="66" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1E293B">North America Field Network</text>
  <text x="78" y="98" width="570" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#64748B">Spotlight callouts connect each regional office to its exact market position.</text>

  <g opacity="0.72">
    <line x1="240" y1="155" x2="1030" y2="155" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 9"/>
    <line x1="210" y1="280" x2="1080" y2="280" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 9"/>
    <line x1="250" y1="405" x2="1050" y2="405" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 9"/>
    <line x1="385" y1="115" x2="385" y2="560" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 9"/>
    <line x1="610" y1="100" x2="610" y2="575" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 9"/>
    <line x1="835" y1="118" x2="835" y2="545" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 9"/>
  </g>

  <g id="editable-map" fill="#D9DEE7" stroke="#C6CEDA" stroke-width="2">
    <path d="M247,198 C286,145 368,112 464,112 C550,113 615,145 671,178 C735,215 811,198 862,226 C914,254 916,316 875,350 C827,390 742,386 704,424 C671,458 626,461 583,436 C541,412 485,421 434,387 C386,355 344,339 302,350 C260,361 217,329 220,281 C222,246 228,222 247,198 Z"/>
    <path d="M383,366 C426,348 487,368 522,399 C559,432 612,442 657,425 C710,405 780,421 813,468 C835,499 812,546 756,558 C693,572 628,548 569,562 C506,577 442,554 410,512 C377,469 332,444 333,407 C334,386 354,374 383,366 Z"/>
    <path d="M525,548 C566,564 601,602 604,640 C558,638 522,622 498,596 C477,573 488,542 525,548 Z"/>
    <path d="M846,359 C876,354 904,371 912,396 C921,423 895,445 860,438 C832,433 815,408 823,385 C827,372 835,363 846,359 Z"/>
    <path d="M929,252 C961,243 997,255 1016,282 C1035,309 1023,341 991,349 C958,357 927,336 916,309 C907,285 910,259 929,252 Z"/>
  </g>

  <g id="spotlight-cones">
    <path d="M356,235 L136,122 C167,105 213,105 244,122 Z" fill="#2F5597" opacity="0.22"/>
    <path d="M570,450 L332,532 C363,514 405,514 436,532 Z" fill="#00A6A6" opacity="0.23"/>
    <path d="M820,256 L981,157 C1011,142 1053,142 1083,157 Z" fill="#D97706" opacity="0.24"/>
  </g>

  <g id="cards" filter="url(#softShadow)">
    <rect x="92" y="100" width="250" height="174" rx="24" fill="url(#cardFill)" stroke="#E2E8F0"/>
    <rect x="286" y="500" width="258" height="172" rx="24" fill="url(#cardFill)" stroke="#E2E8F0"/>
    <rect x="934" y="134" width="258" height="176" rx="24" fill="url(#cardFill)" stroke="#E2E8F0"/>
  </g>

  <image x="132" y="116" width="116" height="116" clip-path="url(#clipSeattle)"
         href="https://images.example.com/headshot-female-operations-lead-seattle.jpg"/>
  <circle cx="190" cy="174" r="61" fill="none" stroke="#2F5597" stroke-width="7"/>

  <image x="326" y="516" width="116" height="116" clip-path="url(#clipAustin)"
         href="https://images.example.com/headshot-product-director-austin.jpg"/>
  <circle cx="384" cy="574" r="61" fill="none" stroke="#00A6A6" stroke-width="7"/>

  <image x="974" y="150" width="116" height="116" clip-path="url(#clipToronto)"
         href="https://images.example.com/headshot-market-lead-toronto.jpg"/>
  <circle cx="1032" cy="208" r="61" fill="none" stroke="#D97706" stroke-width="7"/>

  <g id="map-pins">
    <circle cx="356" cy="235" r="22" fill="#2F5597" opacity="0.25" filter="url(#pinGlow)"/>
    <circle cx="356" cy="235" r="9" fill="#2F5597" stroke="#FFFFFF" stroke-width="4"/>
    <circle cx="570" cy="450" r="22" fill="#00A6A6" opacity="0.25" filter="url(#pinGlow)"/>
    <circle cx="570" cy="450" r="9" fill="#00A6A6" stroke="#FFFFFF" stroke-width="4"/>
    <circle cx="820" cy="256" r="22" fill="#D97706" opacity="0.25" filter="url(#pinGlow)"/>
    <circle cx="820" cy="256" r="9" fill="#D97706" stroke="#FFFFFF" stroke-width="4"/>
  </g>

  <g font-family="Segoe UI, Microsoft YaHei">
    <text x="258" y="147" width="72" font-size="13" font-weight="700" fill="#2F5597">SEATTLE</text>
    <text x="258" y="172" width="72" font-size="25" font-weight="700" fill="#0F172A">42</text>
    <text x="258" y="196" width="78" font-size="12" fill="#64748B">field engineers</text>
    <text x="126" y="252" width="180" font-size="12" fill="#475569">Pacific operations hub</text>

    <text x="454" y="548" width="72" font-size="13" font-weight="700" fill="#008B8B">AUSTIN</text>
    <text x="454" y="573" width="72" font-size="25" font-weight="700" fill="#0F172A">18%</text>
    <text x="454" y="597" width="78" font-size="12" fill="#64748B">YoY growth</text>
    <text x="320" y="650" width="190" font-size="12" fill="#475569">Customer success command center</text>

    <text x="1100" y="181" width="74" font-size="13" font-weight="700" fill="#D97706">TORONTO</text>
    <text x="1100" y="206" width="72" font-size="25" font-weight="700" fill="#0F172A">9</text>
    <text x="1100" y="230" width="80" font-size="12" fill="#64748B">enterprise pilots</text>
    <text x="968" y="288" width="180" font-size="12" fill="#475569">Northeast market expansion</text>

    <text x="342" y="228" width="90" font-size="12" font-weight="700" fill="#1E293B">Seattle</text>
    <text x="556" y="443" width="90" font-size="12" font-weight="700" fill="#1E293B">Austin</text>
    <text x="806" y="249" width="90" font-size="12" font-weight="700" fill="#1E293B">Toronto</text>
  </g>

  <rect x="76" y="636" width="188" height="32" rx="16" fill="#EAF0F8" stroke="#CBD5E1"/>
  <circle cx="96" cy="652" r="5" fill="#2F5597"/>
  <circle cx="132" cy="652" r="5" fill="#00A6A6"/>
  <circle cx="168" cy="652" r="5" fill="#D97706"/>
  <text x="188" y="657" width="68" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">live offices</text>
</svg>
```

## Avoid in this skill
- ❌ Using simple straight arrows instead of spotlight cones; the visual relationship becomes generic and less premium.
- ❌ Applying `clip-path` to the cone or card shapes; use clipping only on `<image>` elements for reliable PPT translation.
- ❌ Putting the map photo/raster above the cones; the cone must sit over the map but beneath pins and callout cards.
- ❌ Making the cone fully opaque; it should preserve the geographic context below.
- ❌ Using `marker-end` arrowheads on paths; if directional arrows are needed, use separate `<line>` elements with marker attributes directly on each line.

## Composition notes
- Keep the map low contrast and centered, occupying roughly 60–70% of slide width so the callout cards can live in surrounding negative space.
- Align each cone’s narrow point to the exact center of its map pin and its wide end to the circular photo diameter.
- Use one accent color per location and repeat it consistently across pin, cone, border, and label text.
- Layer order matters: background → map/grid → translucent cones → cards/photos → pins/text.