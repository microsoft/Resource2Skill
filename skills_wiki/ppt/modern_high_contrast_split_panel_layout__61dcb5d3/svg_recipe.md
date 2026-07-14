# SVG Recipe — High-Contrast Split Panel Layout

## Visual mechanism
A strong editorial title slide built from a full-height solid color panel overlapping a full-bleed hero photo. The high-contrast panel guarantees readable typography while the large image supplies emotion, context, and premium visual polish.

## SVG primitives needed
- 1× `<image>` for the right-side full-bleed hero photograph
- 1× `<clipPath>` with `<polygon>` for an angled photo crop that reinforces the split-panel geometry
- 1× large `<path>` for the left high-contrast geometric panel
- 2× smaller `<path>` elements for seam accents along the split edge
- 4× `<rect>` elements for the background base, image vignette overlay, accent bar, and small editorial tag
- 4× `<text>` elements for kicker, headline, supporting copy, and rotated section metadata
- 1× `<linearGradient>` for darkening the photo near the seam
- 1× `<linearGradient>` for the cyan accent highlight
- 1× `<filter id="panelShadow">` using offset + blur + merge, applied to the main panel for subtle depth
- 1× `<filter id="accentGlow">` using blur + merge, applied to the accent bar for a premium keynote glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoClip">
      <polygon points="420,0 1280,0 1280,720 500,720"/>
    </clipPath>

    <linearGradient id="photoVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.42"/>
      <stop offset="34%" stop-color="#000000" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="cyanAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00D4FF"/>
      <stop offset="100%" stop-color="#7CFFCB"/>
    </linearGradient>

    <filter id="panelShadow" x="-5%" y="-5%" width="125%" height="115%">
      <feOffset dx="18" dy="0" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-40%" y="-250%" width="180%" height="600%">
      <feGaussianBlur stdDeviation="8" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#0D111C"/>

  <image
    href="https://images.example.com/hero-photos/futuristic-architecture-with-blue-light-and-human-silhouette.jpg"
    x="420" y="0" width="860" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoClip)"/>

  <rect x="455" y="0" width="825" height="720" fill="url(#photoVignette)"/>

  <path
    d="M0,0 H585 L530,720 H0 Z"
    fill="#0D111C"
    filter="url(#panelShadow)"/>

  <path
    d="M585,0 L530,720 L548,720 L603,0 Z"
    fill="#111A2C"
    opacity="0.95"/>

  <path
    d="M603,0 L548,720 L556,720 L611,0 Z"
    fill="url(#cyanAccent)"
    opacity="0.9"/>

  <rect
    x="78" y="122" width="74" height="8"
    fill="url(#cyanAccent)"
    rx="4"
    filter="url(#accentGlow)"/>

  <rect
    x="78" y="589" width="142" height="34"
    fill="#151E31"
    rx="17"/>

  <text
    x="78" y="102"
    width="390"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18"
    font-weight="700"
    letter-spacing="4"
    fill="#7CFFCB">
    SECTION 04
  </text>

  <text
    x="76" y="248"
    width="450"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="72"
    font-weight="800"
    letter-spacing="-2"
    fill="#FFFFFF">
    <tspan x="76" dy="0">AI-READY</tspan>
    <tspan x="76" dy="82">OPERATIONS</tspan>
  </text>

  <text
    x="80" y="394"
    width="385"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="22"
    font-weight="400"
    fill="#D7DEE9">
    <tspan x="80" dy="0">Building resilient systems for faster</tspan>
    <tspan x="80" dy="34">decisions, cleaner workflows, and</tspan>
    <tspan x="80" dy="34">measurable enterprise scale.</tspan>
  </text>

  <text
    x="96" y="650"
    width="180"
    transform="rotate(-90 96 650)"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13"
    font-weight="700"
    letter-spacing="3"
    fill="#7F8CA3">
    STRATEGY 2026
  </text>

  <text
    x="100" y="612"
    width="110"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13"
    font-weight="700"
    letter-spacing="1.8"
    fill="#FFFFFF">
    EXEC BRIEF
  </text>
</svg>
```

## Avoid in this skill
- ❌ Placing headline text directly on the photo; the technique depends on keeping all major copy on the solid panel.
- ❌ Centering the split at exactly 50/50 every time; a 40/60 or 45/55 split feels more editorial and less generic.
- ❌ Using low-contrast panel/text pairs such as pale gray on white or navy on black.
- ❌ Applying `clip-path` to the panel path or text; use a native `<path>` for the panel shape and reserve clipping for the `<image>`.
- ❌ Adding many small decorative objects across the photo; the image should remain the emotional focal point.

## Composition notes
- Keep the text panel between 40% and 46% of the slide width, with the image occupying the remaining 60%+ for maximum visual impact.
- Let the panel overlap the image by 40–90 px; this creates depth without needing heavy shadows.
- Use one bright accent color sparingly: a short bar, seam highlight, or small label is enough.
- Use large, confident typography with generous left padding; the panel should feel calm, structured, and premium.