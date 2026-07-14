# SVG Recipe — Minimalist Corporate Arc & Monochromatic Contrast

## Visual mechanism
A dark, monochromatic architectural image is treated as a serious corporate backdrop, then grounded by an oversized warm-stone ellipse pushed below the canvas so only a calm sweeping arc is visible. Minimal white typography, generous spacing, and one beige geometric accent create a premium, understated executive aesthetic.

## SVG primitives needed
- 1× `<image>` for the desaturated/darkened full-slide architectural or business-context photograph
- 2× `<rect>` for charcoal darkening overlays and subtle split-panel structure
- 1× oversized `<ellipse>` for the warm beige bottom “peek” arc
- 1× `<path>` for a small outlined geometric logo mark
- 1× `<line>` for a thin corporate divider rule
- 5× `<text>` blocks for title, subtitle, micro-labels, and numeric/index details
- 1× `<linearGradient>` for the dark vignette overlay
- 1× `<radialGradient>` for the soft atmospheric highlight over the photograph
- 1× `<filter id="softShadow">` for restrained depth on the beige arc and text card

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="charcoalVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#18181C" stop-opacity="0.86"/>
      <stop offset="42%" stop-color="#202024" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="#111114" stop-opacity="0.90"/>
    </linearGradient>

    <radialGradient id="photoGlow" cx="55%" cy="32%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.34"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="16"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.02  0 0 0 0 0.02  0 0 0 0 0.025  0 0 0 0.28 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Use a pre-desaturated, low-brightness corporate/architecture photograph. -->
  <image
    href="https://images.example.com/grayscale-dark-modern-architecture-lobby.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Dark monochrome treatment layered over the photo. -->
  <rect x="0" y="0" width="1280" height="720" fill="#26262A" opacity="0.48"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#charcoalVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#photoGlow)"/>

  <!-- Quiet 50/50 corporate severity: a nearly invisible dark content band. -->
  <rect x="0" y="0" width="520" height="720" fill="#1D1D21" opacity="0.54"/>

  <!-- Small geometric mark. Drawn as a path, not a symbol/use. -->
  <path
    d="M625 78 L653 94 L653 126 L625 142 L597 126 L597 94 Z"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="2.5"
    opacity="0.92"/>
  <path
    d="M625 94 L639 102 L639 118 L625 126 L611 118 L611 102 Z"
    fill="none"
    stroke="#BAB2AC"
    stroke-width="2"/>

  <!-- Executive micro-label. -->
  <text x="88" y="102" width="240"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12"
        letter-spacing="3"
        fill="#BAB2AC"
        opacity="0.94">
    STRATEGY / 2026
  </text>

  <line x1="88" y1="128" x2="220" y2="128" stroke="#BAB2AC" stroke-width="1.5" opacity="0.62"/>

  <!-- Main title: wide, restrained, high contrast. -->
  <text x="86" y="262" width="720"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58"
        font-weight="700"
        letter-spacing="5"
        fill="#FFFFFF">
    CREATIVE
  </text>
  <text x="86" y="328" width="760"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58"
        font-weight="700"
        letter-spacing="5"
        fill="#FFFFFF">
    BUSINESS PLAN
  </text>

  <!-- Thin subtitle with generous spacing. -->
  <text x="90" y="382" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="300"
        letter-spacing="1.2"
        fill="#FFFFFF"
        opacity="0.78">
    A premium profile for focused executive decisions
  </text>

  <!-- Right-side understated metadata card, sitting inside the dark photo field. -->
  <rect x="884" y="130" width="250" height="148" rx="2"
        fill="#18181C"
        opacity="0.62"
        filter="url(#softShadow)"/>
  <text x="914" y="178" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        letter-spacing="2.6"
        fill="#BAB2AC">
    PORTFOLIO
  </text>
  <text x="914" y="220" width="200"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="36"
        font-weight="600"
        fill="#FFFFFF">
    01
  </text>
  <text x="964" y="220" width="130"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        fill="#FFFFFF"
        opacity="0.58">
    Corporate transformation overview
  </text>

  <!-- Oversized warm-stone ellipse pushed below slide to make the signature bottom arc. -->
  <ellipse cx="640" cy="846" rx="930" ry="265"
           fill="#BAB2AC"
           stroke="#FFFFFF"
           stroke-width="4"
           filter="url(#softShadow)"/>

  <!-- Subtle text placed over the beige arc to show footer usage. -->
  <text x="90" y="650" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12"
        letter-spacing="2.5"
        fill="#26262A"
        opacity="0.72">
    MINIMAL CORPORATE ARC SYSTEM
  </text>
  <text x="1012" y="650" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12"
        text-anchor="end"
        letter-spacing="2.5"
        fill="#26262A"
        opacity="0.72">
    CONFIDENTIAL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying SVG grayscale/color-matrix filters to photos; use a pre-desaturated image asset and add dark translucent overlays instead.
- ❌ Small decorative curves or many waves; the signature arc should come from one oversized ellipse placed mostly off-canvas.
- ❌ Bright multi-color photography; it breaks the monochromatic corporate severity.
- ❌ Dense text blocks over the photo; keep copy sparse and let negative space create the premium feel.
- ❌ Clipping non-image elements for the arc; use a native ellipse extending beyond the canvas.

## Composition notes
- Keep the title in the left third-to-half of the canvas, with wide letter spacing and strong white contrast against the charcoal image.
- Let the beige arc occupy only the lower 12–22% of the visible slide; most of the ellipse should remain off-screen.
- Use the warm stone accent sparingly: logo detail, micro-labels, and the large bottom arc are usually enough.
- Choose photos with architecture, boardrooms, staircases, or abstract corporate interiors; strong lines read well after desaturation and darkening.