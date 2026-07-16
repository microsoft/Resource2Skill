# SVG Recipe — Pastel Geometric Split Presentation Theme

## Visual mechanism
A premium split-screen title slide built from oversized pastel geometry: a soft cyan circular arc and circular hero image dominate the left half, while bold stacked typography and a peach-pink subtitle block anchor the right half. The look depends on clean white space, perfect circles, and editorial asymmetry rather than dense charting.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× oversized `<circle>` for the pale cyan off-canvas background arc
- 2× stroked `<circle>` elements for subtle geometric ring accents around the photo
- 1× `<circle>` with soft shadow filter behind the circular image
- 1× `<clipPath>` containing a `<circle>` to crop the hero photo into a perfect circle
- 1× `<image>` for the clipped circular business / analytics hero photo
- 1× `<circle>` for a crisp white photo rim
- 1× large `<rect>` for the pastel pink subtitle anchor block
- 3× `<text>` elements for the stacked title hierarchy
- 2× smaller `<text>` elements for eyebrow label and subtitle copy
- 1× small rounded `<rect>` chip over the photo for an executive metric callout
- 4× mini `<rect>` bars inside the chip for a tiny editable chart accent
- 1× decorative `<path>` for a faint organic pastel highlight behind the title
- 2× `<filter>` definitions: one soft shadow for cards/circles, one gentle glow for accent geometry
- 2× gradient definitions for pastel dimensionality without visual clutter

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cyanSoft" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EEF8FC"/>
      <stop offset="100%" stop-color="#DCEFF8"/>
    </linearGradient>

    <linearGradient id="pinkBlock" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F8E3E4"/>
      <stop offset="100%" stop-color="#F5D9DC"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.10  0 0 0 0 0.12  0 0 0 0 0.16  0 0 0 0.16 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pastelGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="photoCircle">
      <circle cx="338" cy="344" r="246"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Oversized cyan geometry, intentionally cropped off the slide edge -->
  <circle cx="245" cy="270" r="420" fill="url(#cyanSoft)"/>
  <circle cx="245" cy="270" r="360" fill="none" stroke="#FFFFFF" stroke-width="34" opacity="0.55"/>
  <circle cx="338" cy="344" r="278" fill="none" stroke="#D3ECF8" stroke-width="10" opacity="0.9"/>
  <circle cx="500" cy="95" r="38" fill="#F8E3E4" opacity="0.65" filter="url(#pastelGlow)"/>

  <!-- Circular photo with editable SVG clipping -->
  <circle cx="338" cy="344" r="252" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image
    href="https://images.example.com/hero-business-analytics-dashboard-photo.jpg"
    x="92" y="98" width="492" height="492"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoCircle)"/>
  <circle cx="338" cy="344" r="246" fill="none" stroke="#FFFFFF" stroke-width="12"/>

  <!-- Small editable metric chip over the circular photo -->
  <rect x="126" y="500" width="214" height="74" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="150" y="528" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#141414">Revenue +18%</text>
  <rect x="152" y="544" width="16" height="16" rx="4" fill="#F8E3E4"/>
  <rect x="178" y="536" width="16" height="24" rx="4" fill="#E2F0F9"/>
  <rect x="204" y="526" width="16" height="34" rx="4" fill="#F8E3E4"/>
  <rect x="230" y="516" width="16" height="44" rx="4" fill="#BFE1F2"/>
  <text x="262" y="558" width="62" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" fill="#66727A">Q4 view</text>

  <!-- Faint organic highlight behind right-side typography -->
  <path d="M760,112 C840,72 936,82 1004,124 C1082,172 1092,250 1030,286 C964,326 838,292 780,240 C724,190 704,142 760,112 Z"
        fill="#F8E3E4" opacity="0.22"/>

  <!-- Right-side editorial typography -->
  <text x="720" y="126" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700" letter-spacing="2.8" fill="#7F8C93">
    FY2026 QUARTERLY SNAPSHOT
  </text>

  <text x="716" y="246" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="82" font-weight="800" letter-spacing="1.5" fill="#141414">
    SALES
  </text>

  <text x="720" y="322" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="400" fill="#141414">
    Review
  </text>

  <text x="716" y="418" width="510" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="78" font-weight="800" letter-spacing="-1" fill="#141414">
    Analysis
  </text>

  <!-- Peach subtitle block acting as a horizontal anchor -->
  <rect x="670" y="534" width="610" height="96" rx="0" fill="url(#pinkBlock)"/>
  <text x="720" y="575" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="600" fill="#141414">
    <tspan font-weight="800">Northstar Consulting</tspan>
    <tspan font-weight="400"> · Executive Briefing</tspan>
  </text>
  <text x="720" y="607" width="440" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="500" fill="#6F5558">
    Strategy, pipeline health, and growth priorities
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the circular photo; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not clip ordinary shapes or groups; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ Do not use `<pattern>` fills for the pastel geometry; use solid fills or simple gradients instead.
- ❌ Do not apply filters to `<line>` elements; use filtered circles/rectangles for shadows and glows.
- ❌ Do not center all content symmetrically; the style depends on the left visual mass being balanced by right-side typography.

## Composition notes
- Keep the circular photo large, around 38–42% of slide height, and let the cyan circle extend off-canvas to create the signature arc.
- Reserve the right half for sparse, oversized typography; avoid filling it with body copy.
- The peach subtitle block should sit low and run horizontally, acting like a visual underline for the title system.
- Use only two pastel accents plus charcoal text; the premium feel comes from restraint, white space, and exact geometric alignment.