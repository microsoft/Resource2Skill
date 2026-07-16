# SVG Recipe — Professional Geometric Overlay Title (专业几何斜角蒙版)

## Visual mechanism
A full-bleed contextual photograph is partially covered by a semi-transparent angled geometric panel, creating a premium readable zone for title typography while preserving image energy. The angled cut adds forward motion and makes the slide feel more editorial than a plain rectangle overlay.

## SVG primitives needed
- 1× `<image>` for the full-bleed background photo.
- 1× `<rect>` for a subtle dark vignette/scrim over the photo.
- 1× `<linearGradient>` for controlled photo darkening from the text side outward.
- 1× `<filter id="softShadow">` for a refined shadow on the angled overlay.
- 1× large `<path>` for the main semi-transparent parallelogram title mask.
- 2× thin `<path>` elements for angled accent strips along the cut edge.
- 1× small `<rect>` for an eyebrow label background.
- 1× `<line>` for a minimal editorial divider.
- 4× `<text>` blocks with explicit `width` attributes for eyebrow, main title, subtitle, and metadata.
- Optional decorative `<circle>` elements for restrained brand-detail dots.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoScrim" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#06111f" stop-opacity="0.55"/>
      <stop offset="48%" stop-color="#06111f" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#06111f" stop-opacity="0.48"/>
    </linearGradient>

    <linearGradient id="panelBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10264d" stop-opacity="0.94"/>
      <stop offset="62%" stop-color="#173766" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#0a1730" stop-opacity="0.90"/>
    </linearGradient>

    <linearGradient id="goldAccent" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffb347" stop-opacity="0.98"/>
      <stop offset="100%" stop-color="#f06d2f" stop-opacity="0.95"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="10" dy="0" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textLift" x="-10%" y="-10%" width="120%" height="120%">
      <feOffset dx="0" dy="2" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.example.com/1280x720/global-city-architecture-glass-skyline.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#photoScrim)"/>

  <path
    d="M0 0 L824 0 L586 720 L0 720 Z"
    fill="url(#panelBlue)"
    filter="url(#softShadow)"/>

  <path
    d="M798 0 L832 0 L594 720 L560 720 Z"
    fill="#ffffff"
    opacity="0.16"/>

  <path
    d="M842 0 L867 0 L629 720 L604 720 Z"
    fill="url(#goldAccent)"
    opacity="0.94"/>

  <circle cx="104" cy="102" r="4" fill="#ffffff" opacity="0.65"/>
  <circle cx="126" cy="102" r="4" fill="#ffffff" opacity="0.35"/>
  <circle cx="148" cy="102" r="4" fill="#ffffff" opacity="0.20"/>

  <rect
    x="82" y="128" width="220" height="34" rx="17"
    fill="#ffffff"
    opacity="0.14"/>

  <text
    x="106" y="151"
    width="300"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="16"
    font-weight="700"
    letter-spacing="2.5"
    fill="#ffffff"
    opacity="0.95">
    STRATEGIC BRIEFING
  </text>

  <line
    x1="84" y1="205" x2="308" y2="205"
    stroke="#f59b34"
    stroke-width="5"
    stroke-linecap="round"/>

  <text
    x="82" y="288"
    width="560"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="64"
    font-weight="800"
    fill="#ffffff"
    filter="url(#textLift)">
    <tspan x="82" dy="0">TOWARDS</tspan>
    <tspan x="82" dy="76">THE FUTURE</tspan>
  </text>

  <text
    x="86" y="455"
    width="500"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="24"
    font-weight="400"
    fill="#dfe9f7"
    opacity="0.96">
    Global Market Analysis &amp; Strategic Insights 2024
  </text>

  <text
    x="86" y="520"
    width="460"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18"
    font-weight="400"
    fill="#ffffff"
    opacity="0.68">
    Prepared for Executive Leadership · Q4 Review
  </text>

  <path
    d="M84 582 L284 582"
    stroke="#ffffff"
    stroke-width="1.5"
    stroke-dasharray="8 10"
    opacity="0.45"/>

  <text
    x="86" y="625"
    width="430"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="15"
    font-weight="600"
    letter-spacing="1.4"
    fill="#f7b35a"
    opacity="0.95">
    CONFIDENTIAL · BOARD PRESENTATION
  </text>
</svg>
```

## Avoid in this skill
- ❌ `transform="skewX(...)"` to create the angled panel; use explicit `<path>` coordinates instead.
- ❌ Masking text or shapes with `<mask>`; the angled overlay should be a native editable `<path>`.
- ❌ Placing text directly on the busy photo without a sufficiently opaque geometric panel.
- ❌ Using a flat rectangular overlay only; it loses the dynamic “professional keynote” effect.
- ❌ Overdecorating the image side with charts or icons; the photo should remain the emotional/contextual anchor.

## Composition notes
- Keep the angled panel to roughly 50–65% of slide width; the widest side should contain all text safely inside the shape.
- Place the strongest typography in the upper-middle or center-left zone, not too close to the slanted edge.
- Use one dominant brand color for the panel and one warm accent strip to create contrast and hierarchy.
- Leave the photo side mostly open so the background still feels full-bleed, cinematic, and premium.