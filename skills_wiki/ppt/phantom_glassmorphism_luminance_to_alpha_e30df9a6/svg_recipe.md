# SVG Recipe — Phantom Glassmorphism (Luminance-to-Alpha Object Masking)

## Visual mechanism
Create a side-by-side “solid object → phantom glass object” comparison by rendering the same organic silhouette twice: once as a saturated 3D form, and once as layered translucent highlights, pale rims, and glows that imply luminance has been converted into alpha. The background must remain visually rich so the glass object visibly borrows color and texture from what sits behind it.

## SVG primitives needed
- 1× `<image>` for the full-bleed textured/photo background that shows through the phantom object
- 2× `<rect>` for dark vignette overlays and frosted label plates
- 2× repeated organic `<path>` silhouettes for the solid object and the phantom object
- 2× small `<path>` stems for the object detail
- 5–8× translucent `<ellipse>` / `<path>` highlight layers inside the phantom object to mimic luminance-to-alpha bands
- 2× `<radialGradient>` for solid 3D shading and glass highlight falloff
- 2× `<linearGradient>` for atmospheric vignette and label glass panels
- 1× `<filter id="softShadow">` applied to the solid object and label plates
- 1× `<filter id="glassGlow">` applied to the phantom silhouette/highlights
- 4–6× `<text>` elements with explicit `width` attributes for title, subtitle, labels, and metric callouts

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="vignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#061018" stop-opacity="0.15"/>
      <stop offset="55%" stop-color="#07111a" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#020508" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="panelGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.26"/>
      <stop offset="48%" stop-color="#d9f5ff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#7ecbff" stop-opacity="0.06"/>
    </linearGradient>

    <radialGradient id="solidPear" cx="35%" cy="26%" r="78%">
      <stop offset="0%" stop-color="#fff0e6"/>
      <stop offset="15%" stop-color="#ff9d8b"/>
      <stop offset="48%" stop-color="#dc2440"/>
      <stop offset="78%" stop-color="#7c071e"/>
      <stop offset="100%" stop-color="#27030b"/>
    </radialGradient>

    <radialGradient id="glassCore" cx="36%" cy="24%" r="78%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.62"/>
      <stop offset="22%" stop-color="#eafff5" stop-opacity="0.42"/>
      <stop offset="55%" stop-color="#b8fff1" stop-opacity="0.16"/>
      <stop offset="82%" stop-color="#ffffff" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="hotHighlight" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="55%" stop-color="#dfffea" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glassGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <image href="https://images.example.com/macro-forest-moss-with-blue-gold-bokeh.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#06131b" opacity="0.18"/>

  <text x="70" y="72" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#ffffff" letter-spacing="2">PHANTOM TRANSPARENCY</text>
  <text x="73" y="112" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#d9f7ff" opacity="0.86">Luminance becomes alpha: shadows vanish, highlights remain as editable glass layers.</text>

  <rect x="120" y="590" width="320" height="72" rx="24" fill="url(#panelGlass)" stroke="#ffffff" stroke-opacity="0.22" filter="url(#softShadow)"/>
  <rect x="840" y="590" width="320" height="72" rx="24" fill="url(#panelGlass)" stroke="#ffffff" stroke-opacity="0.24" filter="url(#softShadow)"/>

  <text x="145" y="622" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">SOLID STATE</text>
  <text x="145" y="648" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffd7dc">opaque color + painted shadow volume</text>

  <text x="865" y="622" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">PHANTOM STATE</text>
  <text x="865" y="648" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#d9fff1">white tint + alpha-weighted luminance</text>

  <!-- Solid object: saturated 3D silhouette -->
  <ellipse cx="286" cy="554" rx="150" ry="28" fill="#000000" opacity="0.33" filter="url(#glassGlow)"/>
  <path d="M311 171 C354 167 390 199 395 252 C443 277 459 341 444 404 C426 481 367 548 295 551 C224 554 164 510 145 437 C128 373 145 296 197 262 C198 213 244 174 311 171 Z"
        fill="url(#solidPear)" filter="url(#softShadow)"/>
  <path d="M310 176 C303 128 326 94 372 83 C379 119 357 154 318 181 Z"
        fill="#3b2010" opacity="0.95"/>
  <ellipse cx="255" cy="263" rx="57" ry="72" fill="#ffffff" opacity="0.24" transform="rotate(-26 255 263)"/>
  <path d="M171 419 C199 505 298 542 371 484" fill="none" stroke="#2b020b" stroke-width="18" stroke-opacity="0.18"/>

  <!-- Phantom object: same silhouette rebuilt with translucent luminance layers -->
  <ellipse cx="992" cy="554" rx="150" ry="28" fill="#d8fff4" opacity="0.16" filter="url(#glassGlow)"/>
  <path d="M1017 171 C1060 167 1096 199 1101 252 C1149 277 1165 341 1150 404 C1132 481 1073 548 1001 551 C930 554 870 510 851 437 C834 373 851 296 903 262 C904 213 950 174 1017 171 Z"
        fill="url(#glassCore)" stroke="#ffffff" stroke-width="3" stroke-opacity="0.55" filter="url(#glassGlow)"/>
  <path d="M1016 176 C1009 128 1032 94 1078 83 C1085 119 1063 154 1024 181 Z"
        fill="#ecfff6" opacity="0.28" stroke="#ffffff" stroke-opacity="0.35" stroke-width="2"/>

  <ellipse cx="958" cy="262" rx="62" ry="78" fill="url(#hotHighlight)" opacity="0.88" transform="rotate(-25 958 262)" filter="url(#glassGlow)"/>
  <ellipse cx="1043" cy="354" rx="96" ry="132" fill="#ffffff" opacity="0.075" transform="rotate(16 1043 354)"/>
  <ellipse cx="961" cy="431" rx="78" ry="118" fill="#bfffee" opacity="0.10" transform="rotate(-18 961 431)"/>
  <path d="M876 410 C914 498 1010 534 1087 484" fill="none" stroke="#ffffff" stroke-width="16" stroke-opacity="0.16"/>
  <path d="M881 344 C914 288 963 248 1035 232" fill="none" stroke="#ffffff" stroke-width="8" stroke-opacity="0.18"/>
  <path d="M1096 278 C1137 334 1137 426 1087 500" fill="none" stroke="#d9fff2" stroke-width="7" stroke-opacity="0.22"/>
  <path d="M900 263 C908 223 944 194 1002 187" fill="none" stroke="#ffffff" stroke-width="5" stroke-opacity="0.42"/>
  <circle cx="934" cy="242" r="9" fill="#ffffff" opacity="0.62"/>
  <circle cx="1093" cy="451" r="6" fill="#eafff8" opacity="0.34"/>

  <!-- Transformation cue -->
  <line x1="504" y1="354" x2="770" y2="354" stroke="#ffffff" stroke-width="2" stroke-opacity="0.32" stroke-dasharray="9 13"/>
  <text x="536" y="333" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#e9fbff" text-anchor="middle">DESATURATE → LEVELS → ALPHA</text>
  <text x="520" y="382" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#bfeeff" text-anchor="middle" opacity="0.78">simulate with editable translucent SVG layers</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<mask>` or luminance masks on shapes; PPT translation will not preserve them reliably, so rebuild the effect with translucent gradients and repeated highlight paths.
- ❌ `clip-path` on the pear/object paths; clipping only translates safely for `<image>`, not vector shapes.
- ❌ `<use href="#object">` to duplicate the silhouette; repeat the path data manually for the solid and phantom versions.
- ❌ Blend modes such as `mix-blend-mode: screen`; PowerPoint will not retain them as editable DrawingML.
- ❌ Overly flat glass objects with only one transparent fill; the phantom effect needs multiple rim, highlight, and contour layers to read as luminance-to-alpha.

## Composition notes
- Keep the background full-bleed and visually complex; the phantom object only feels transparent when texture and color are visible behind it.
- Place the solid object on the left and the phantom object on the right at similar scale so the viewer understands they are the same form in two states.
- Reserve the top-left for the title and the lower corners for small frosted labels; keep the center lightly occupied by a thin transformation cue.
- Use white, mint, and pale cyan for the phantom layers, balanced against one saturated “before” color such as crimson, cobalt, or amber.