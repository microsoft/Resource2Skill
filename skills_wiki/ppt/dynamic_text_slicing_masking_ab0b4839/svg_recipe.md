# SVG Recipe — Dynamic Text Slicing & Masking

## Visual mechanism
Treat the headline as a physical object cut by a jagged diagonal fault line: the upper fragments stay cool/dark, while the lower fragments slip slightly downward/right and switch to hot contrast colors. In SVG-to-PPT workflows, the most reliable editable version is to build or pre-vectorize the word into separate `<path>` fragments rather than trying to clip live `<text>`.

## SVG primitives needed
- 1× `<image>` for a cinematic full-slide background photo.
- 2× `<rect>` for dark gradient overlays and atmosphere.
- 3× `<linearGradient>` for the sky wash, warm lower-slice coloring, and ribbon accent.
- 1× `<filter id="heroShadow">` using `feOffset + feGaussianBlur + feMerge` for depth behind the sliced word.
- 1× `<filter id="faultGlow">` using `feGaussianBlur` for the glowing fracture seam.
- N× `<path>` for thick stroked vector-letter skeletons and their separate top/bottom sliced fragments.
- 2× `<path>` for the zig-zag fault seam and its glow.
- 2× `<path>` for bottom caption ribbons with chevron notches.
- Several small `<circle>` elements for star/spark accents.
- 4× `<text>` elements with explicit `width` for labels, captions, and small supporting typography.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="nightWash" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#150A3D" stop-opacity="0.35"/>
      <stop offset="0.48" stop-color="#37206F" stop-opacity="0.48"/>
      <stop offset="1" stop-color="#03071F" stop-opacity="0.94"/>
    </linearGradient>

    <linearGradient id="hotSlice" x1="0" y1="360" x2="0" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#B72E75"/>
      <stop offset="0.55" stop-color="#E8465F"/>
      <stop offset="1" stop-color="#FFB037"/>
    </linearGradient>

    <linearGradient id="ribbonGrad" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#E33C68"/>
      <stop offset="0.55" stop-color="#C72D6C"/>
      <stop offset="1" stop-color="#EF4D64"/>
    </linearGradient>

    <filter id="heroShadow" x="-80" y="-80" width="1440" height="880">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="12"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .45 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="faultGlow" x="-80" y="-80" width="1440" height="880">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/cinematic-starry-mountain-lake-night-sky.jpg"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#nightWash)"/>
  <rect x="0" y="505" width="1280" height="215" fill="#01051A" opacity="0.52"/>

  <circle cx="185" cy="88" r="1.8" fill="#FFFFFF" opacity="0.85"/>
  <circle cx="308" cy="132" r="1.2" fill="#FFFFFF" opacity="0.65"/>
  <circle cx="754" cy="92" r="1.5" fill="#FFFFFF" opacity="0.78"/>
  <circle cx="1018" cy="146" r="1.4" fill="#FFFFFF" opacity="0.7"/>
  <circle cx="1125" cy="71" r="2.1" fill="#F5D8FF" opacity="0.9"/>

  <text x="72" y="94" width="530" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="700" fill="#F9E9B8" letter-spacing="3">
    TYPOGRAPHIC FAULT LINE
  </text>
  <text x="76" y="132" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#E8E2FF" opacity="0.8">
    Split vector letters into independently styled fragments
  </text>

  <g id="sliced-word" filter="url(#heroShadow)" stroke-linecap="butt" stroke-linejoin="bevel">
    <!-- heavy editable vector-letter outlines -->
    <g fill="none" stroke="#FFF6D8" stroke-width="82" opacity="0.96">
      <path d="M155 272 H275 L170 500 H294"/>
      <path d="M354 272 V500"/>
      <path d="M535 292 H428 V478 H548 V410 H490"/>
      <path d="M595 392 H678"/>
      <path d="M726 272 H846 L741 500 H865"/>
      <path d="M908 500 L974 272 L1040 500 M934 418 H1014"/>
      <path d="M1202 292 H1095 V478 H1215 V410 H1157"/>
    </g>

    <g fill="none" stroke="#A8A927" stroke-width="68" opacity="0.95">
      <path d="M155 272 H275 L170 500 H294"/>
      <path d="M354 272 V500"/>
      <path d="M535 292 H428 V478 H548 V410 H490"/>
      <path d="M595 392 H678"/>
      <path d="M726 272 H846 L741 500 H865"/>
      <path d="M908 500 L974 272 L1040 500 M934 418 H1014"/>
      <path d="M1202 292 H1095 V478 H1215 V410 H1157"/>
    </g>

    <!-- cool upper fragments -->
    <g fill="none" stroke="#031F63" stroke-width="54">
      <path d="M155 272 H275 L231 365"/>
      <path d="M354 272 V365"/>
      <path d="M535 292 H428 V363"/>
      <path d="M595 392 H637"/>
      <path d="M726 272 H846 L803 364"/>
      <path d="M927 365 L974 272 L1021 365"/>
      <path d="M1202 292 H1095 V363"/>
    </g>

    <!-- warm lower fragments, slipped down/right to create physical slicing -->
    <g fill="none" stroke="url(#hotSlice)" stroke-width="54" transform="translate(18 10)">
      <path d="M214 386 L170 500 H294"/>
      <path d="M354 392 V500"/>
      <path d="M428 392 V478 H548 V410 H490"/>
      <path d="M637 392 H678"/>
      <path d="M786 386 L741 500 H865"/>
      <path d="M908 500 L934 418 H1014 L1040 500"/>
      <path d="M1095 392 V478 H1215 V410 H1157"/>
    </g>

    <!-- crisp light edge on the displaced lower half -->
    <g fill="none" stroke="#FFF8D8" stroke-width="4" opacity="0.8" transform="translate(18 10)">
      <path d="M214 386 L170 500 H294"/>
      <path d="M428 392 V478 H548 V410 H490"/>
      <path d="M786 386 L741 500 H865"/>
      <path d="M908 500 L934 418 H1014 L1040 500"/>
    </g>
  </g>

  <path d="M145 373 L260 351 L355 382 L452 356 L575 393 L668 372 L790 353 L902 394 L1012 357 L1130 382 L1228 350"
        fill="none" stroke="#FF4F87" stroke-width="13" opacity="0.38" filter="url(#faultGlow)"/>
  <path d="M145 373 L260 351 L355 382 L452 356 L575 393 L668 372 L790 353 L902 394 L1012 357 L1130 382 L1228 350"
        fill="none" stroke="#FFF7C6" stroke-width="4" opacity="0.95"/>

  <path d="M0 548 H565 L610 590 H0 Z" fill="url(#ribbonGrad)" opacity="0.96"/>
  <path d="M715 548 H1280 V590 H755 L705 568 Z" fill="url(#ribbonGrad)" opacity="0.96"/>

  <text x="118" y="582" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="900" fill="#FFFFFF">
    AMAZING
  </text>
  <text x="770" y="582" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="900" fill="#FFFFFF">
    Text Effects
  </text>

  <text x="40" y="662" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#E83A67">
    Dzyner<tspan fill="#FFFFFF">ByDesign</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on `clip-path` applied to `<text>` for the slice; PPT-Master ignores clipping on non-image elements. Use pre-sliced vector `<path>` fragments or thick editable path-stroke letterforms.
- ❌ Do not use SVG `<mask>` to hide parts of live text; masks are a hard-fail / unreliable path for this workflow.
- ❌ Do not use `<textPath>` for curved or diagonal type slicing; it will not translate cleanly.
- ❌ Avoid thin fonts. The effect needs very heavy strokes so the fragments remain legible after displacement.
- ❌ Avoid large offsets between fragments; if the halves move too far, the word stops reading as one typographic object.

## Composition notes
- Make the sliced word the hero: reserve roughly 60–75% of slide width and center it slightly above the vertical midpoint.
- Use a high-contrast pairing: cool upper fragments against hot lower fragments, with a pale outline to keep readability over photo backgrounds.
- Keep the fault line crisp and visible; a thin bright seam plus a blurred colored glow sells the “cut” without clutter.
- Place supporting labels or ribbons below the word so they do not compete with the fractured typography.