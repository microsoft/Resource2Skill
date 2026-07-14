# SVG Recipe — Editorial Magazine Split-Grid & Color Block

## Visual mechanism
A premium editorial slide is built from a hard 40/60 split: restrained typography on pale negative space and a full-bleed photo panel, joined by a saturated color block that crosses the seam. The visual power comes from sharp geometry, oversized uppercase type, and one bold accent color used sparingly but decisively.

## SVG primitives needed
- 1× `<rect>` for the full pale background
- 1× `<clipPath>` with `<rect>` for the right-side full-bleed image crop
- 1× `<image>` for the editorial hero photograph
- 4× `<rect>` for split-grid panels, accent blocks, and thin rule bars
- 1× `<filter id="blockShadow">` with `feOffset`, `feGaussianBlur`, and `feMerge` for a subtle premium lift on the crossing accent block
- 1× `<linearGradient>` for a translucent dark photo overlay that improves contrast
- 1× `<rect>` using the gradient overlay on top of the image
- 1× `<path>` for an angular editorial cut-in shape over the photo
- 1× `<line>` for the precise split seam
- 8× `<text>` elements for section label, headline, body copy, pull quote, folio, and compact stat labels
- Nested `<tspan>` inside headline/body/stat text for line breaks and typographic hierarchy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoClip">
      <rect x="548" y="0" width="732" height="720"/>
    </clipPath>

    <linearGradient id="photoShade" x1="548" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.12"/>
      <stop offset="0.58" stop-color="#000000" stop-opacity="0.02"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.35"/>
    </linearGradient>

    <filter id="blockShadow" x="-20%" y="-30%" width="140%" height="160%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F4F2EF"/>

  <image
    x="548" y="0" width="732" height="720"
    href="https://images.example.com/editorial-architecture-glass-facade-full-bleed.jpg"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoClip)"/>

  <rect x="548" y="0" width="732" height="720" fill="url(#photoShade)"/>

  <path d="M1040 0 L1280 0 L1280 230 L1166 270 L1116 182 Z" fill="#141414" opacity="0.72"/>
  <rect x="548" y="0" width="10" height="720" fill="#141414"/>
  <line x1="548" y1="0" x2="548" y2="720" stroke="#141414" stroke-width="1"/>

  <rect x="78" y="78" width="86" height="8" fill="#E20074"/>
  <text x="78" y="122" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" letter-spacing="3" fill="#E20074">
    BRAND FIELD REPORT
  </text>

  <text x="74" y="226" width="480" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="78" font-weight="900" letter-spacing="-3" fill="#141414">
    <tspan x="74" dy="0">URBAN</tspan>
    <tspan x="74" dy="78">SIGNAL</tspan>
  </text>

  <rect x="428" y="252" width="384" height="92" fill="#E20074" filter="url(#blockShadow)"/>
  <text x="452" y="290" width="326" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="800" letter-spacing="2.5" fill="#FFFFFF">
    <tspan x="452" dy="0">THE NEW CONSUMER</tspan>
    <tspan x="452" dy="26">ATTENTION GRID</tspan>
  </text>

  <text x="78" y="376" width="385" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#4E4E4E">
    <tspan x="78" dy="0">A split-grid composition turns a standard market update into a visual editorial feature.</tspan>
    <tspan x="78" dy="29">Use one assertive color block to connect evidence, mood, and message across the image boundary.</tspan>
  </text>

  <rect x="78" y="484" width="360" height="1.5" fill="#141414"/>
  <text x="78" y="530" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="900" fill="#141414">
    62%
  </text>
  <text x="78" y="558" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" letter-spacing="1.8" fill="#777777">
    RECALL LIFT
  </text>

  <text x="236" y="530" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="900" fill="#141414">
    3.4x
  </text>
  <text x="238" y="558" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" letter-spacing="1.8" fill="#777777">
    VISUAL STICKINESS
  </text>

  <rect x="990" y="524" width="210" height="118" fill="#FFFFFF" opacity="0.88"/>
  <text x="1014" y="562" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="800" letter-spacing="2" fill="#141414">
    ISSUE 04
  </text>
  <text x="1014" y="606" width="156" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="900" fill="#E20074">
    FIELD NOTES
  </text>

  <text x="78" y="672" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" letter-spacing="1.5" fill="#8A8A8A">
    STRATEGY / VISUAL SYSTEMS / 2026
  </text>
</svg>
```

## Avoid in this skill
- ❌ Soft rounded dashboard cards; this technique depends on sharp editorial cuts and uncompromising rectangular geometry
- ❌ Multiple competing accent colors; use one saturated block color and repeat it only in tiny typographic details
- ❌ Dense bullet lists or tables; the layout should feel like a magazine opener, not a report appendix
- ❌ Applying `clip-path` to decorative rectangles or text; use clipping only on the `<image>` crop for reliable editable PowerPoint output
- ❌ Pattern fills, masks, or skew transforms for print texture; use simple rectangles, image crops, paths, and gradients instead

## Composition notes
- Keep the photo panel at roughly 55–60% of the canvas width, full height, and edge-to-edge for a true magazine spread feel.
- Place the headline in the whitespace with generous margins; let the color block cross from the text zone into the photo zone to create tension.
- Use small uppercase labels and thin rules to make the slide feel structured without adding visual clutter.
- The accent block should be bold enough to dominate the seam but not so large that it competes with the main headline.