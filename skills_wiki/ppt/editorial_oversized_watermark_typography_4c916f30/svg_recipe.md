# SVG Recipe — Editorial Oversized Watermark Typography

## Visual mechanism
A massive pale numeral is placed as an architectural background element, bleeding off the slide edge, while sharp foreground typography overlaps it on the center-right. The slide feels editorial because numbering becomes layout structure rather than a bullet label, supported by faint grid lines, restrained monochrome contrast, and one vivid accent.

## SVG primitives needed
- 1× `<rect>` for the off-white full-slide background
- 1× `<linearGradient>` for a barely perceptible paper-like background wash
- 8–12× `<line>` for faint vertical editorial grid/tracking lines and small crop-mark details
- 1× oversized `<text>` for the pale watermark numeral
- 3–5× foreground `<text>` blocks for section label, main headline, body copy, and metadata
- 2–4× `<rect>` for accent bars, label chips, and small structural dividers
- 1× `<path>` for a small editorial chevron/arrow motif near the accent line

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbfbfa"/>
      <stop offset="55%" stop-color="#f7f7f5"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#paperWash)"/>

  <!-- Subtle editorial grid -->
  <line x1="120" y1="0" x2="120" y2="720" stroke="#eeeeec" stroke-width="2"/>
  <line x1="240" y1="0" x2="240" y2="720" stroke="#f0f0ee" stroke-width="1"/>
  <line x1="360" y1="0" x2="360" y2="720" stroke="#eeeeec" stroke-width="2"/>
  <line x1="480" y1="0" x2="480" y2="720" stroke="#f0f0ee" stroke-width="1"/>
  <line x1="600" y1="0" x2="600" y2="720" stroke="#eeeeec" stroke-width="2"/>
  <line x1="720" y1="0" x2="720" y2="720" stroke="#f0f0ee" stroke-width="1"/>
  <line x1="840" y1="0" x2="840" y2="720" stroke="#eeeeec" stroke-width="2"/>
  <line x1="960" y1="0" x2="960" y2="720" stroke="#f0f0ee" stroke-width="1"/>
  <line x1="1080" y1="0" x2="1080" y2="720" stroke="#eeeeec" stroke-width="2"/>
  <line x1="1200" y1="0" x2="1200" y2="720" stroke="#f0f0ee" stroke-width="1"/>

  <!-- Small crop marks for magazine-page feeling -->
  <line x1="64" y1="58" x2="124" y2="58" stroke="#d9d9d6" stroke-width="2"/>
  <line x1="64" y1="58" x2="64" y2="118" stroke="#d9d9d6" stroke-width="2"/>
  <line x1="1156" y1="662" x2="1216" y2="662" stroke="#d9d9d6" stroke-width="2"/>
  <line x1="1216" y1="602" x2="1216" y2="662" stroke="#d9d9d6" stroke-width="2"/>

  <!-- Oversized watermark numeral: placed first so foreground text overlaps it -->
  <text x="-58" y="548"
        width="720"
        font-family="Arial Black, Impact, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="500"
        font-weight="900"
        letter-spacing="-38"
        fill="#e9e9e6">04</text>

  <!-- Tiny editorial navigation label -->
  <rect x="488" y="116" width="148" height="34" rx="17" fill="#111111"/>
  <text x="512" y="139"
        width="110"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        font-weight="700"
        letter-spacing="2.5"
        fill="#ffffff">TYPE / 04</text>

  <!-- Foreground headline overlapping the numeral -->
  <text x="486" y="318"
        width="680"
        font-family="Segoe UI, Arial, Microsoft YaHei, sans-serif"
        font-size="76"
        font-weight="800"
        letter-spacing="-3"
        fill="#111111">MONTSERRAT</text>

  <!-- Accent rule and chevron -->
  <rect x="492" y="366" width="136" height="9" fill="#dc3545"/>
  <rect x="640" y="366" width="46" height="9" fill="#111111"/>
  <path d="M704 362 L726 370.5 L704 379 Z" fill="#dc3545"/>

  <!-- Body copy -->
  <text x="492" y="426"
        width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25"
        font-weight="400"
        line-height="1.35"
        fill="#2b2b2b">
    <tspan x="492" dy="0">A geometric sans-serif with sharp rhythm,</tspan>
    <tspan x="492" dy="36">clean proportions, and confident presence.</tspan>
    <tspan x="492" dy="36">Use it when a slide needs to feel modern,</tspan>
    <tspan x="492" dy="36">editorial, and unmistakably structured.</tspan>
  </text>

  <!-- Metadata column -->
  <line x1="1080" y1="214" x2="1080" y2="510" stroke="#d8d8d5" stroke-width="2"/>
  <text x="1110" y="238"
        width="110"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        font-weight="700"
        letter-spacing="2"
        fill="#9a9a96">WEIGHT</text>
  <text x="1110" y="282"
        width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28"
        font-weight="800"
        fill="#111111">800</text>
  <text x="1110" y="352"
        width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        font-weight="700"
        letter-spacing="2"
        fill="#9a9a96">STYLE</text>
  <text x="1110" y="396"
        width="130"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28"
        font-weight="800"
        fill="#111111">Bold</text>
  <text x="492" y="610"
        width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16"
        font-weight="600"
        letter-spacing="2"
        fill="#8e8e8a">AGENDA SERIES · TYPOGRAPHIC WAYFINDING</text>
</svg>
```

## Avoid in this skill
- ❌ Do not turn the giant numeral into an image; keep it as editable `<text>` so the step number can be changed in PowerPoint.
- ❌ Do not use drop shadows to separate foreground from watermark; the editorial effect depends on flat overlap and low-contrast layering.
- ❌ Do not rely on opacity-only watermarking if exact PPT color fidelity matters; use a very light solid fill such as `#e9e9e6`.
- ❌ Do not center all elements symmetrically; the technique needs asymmetry, edge bleed, and text overlap.
- ❌ Do not use `<textPath>`, `<mask>`, or clipped non-image elements for the typography; they will not translate reliably.

## Composition notes
- Let the watermark numeral occupy roughly the left 50–60% of the canvas and bleed slightly off the left edge.
- Place the headline around the center-right, overlapping the right half of the numeral so the number becomes a structural backdrop.
- Keep the palette mostly off-white, pale gray, and charcoal; reserve one saturated accent color for a short rule or small motif.
- Use generous negative space around the body copy and avoid dense paragraphs; this layout works best with one headline plus 2–4 short supporting lines.