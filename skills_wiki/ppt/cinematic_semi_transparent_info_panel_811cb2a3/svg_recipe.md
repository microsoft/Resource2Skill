# SVG Recipe — Cinematic Semi-Transparent Info Panel

## Visual mechanism
A full-bleed cinematic photograph remains visible while a localized dark translucent matte panel creates a high-contrast reading zone for crisp editorial typography. The panel is flush-left, with a thin framed title box and custom `+` list markers to create an architectural, premium keynote feel.

## SVG primitives needed
- 1× `<image>` for the full-bleed architectural / contextual background photo.
- 1× `<linearGradient>` for a subtle right-to-left vignette that improves text contrast without hiding the image.
- 1× `<filter id="panelShadow">` using `feOffset + feGaussianBlur + feMerge` for a soft cinematic depth behind the matte panel.
- 1× `<rect>` for the semi-transparent black information panel.
- 1× `<rect>` for the thin white bordered title box.
- 2× `<line>` for minimal architectural guide rules inside the panel.
- 1× `<text>` with nested `<tspan>` for the title, allowing the section number to be styled separately.
- 1× `<text>` for the muted subtitle / descriptor.
- 5× paired `<text>` elements for custom `+` markers and list item labels.
- 1× `<text>` for a small rotated edge label that adds a cinematic technical-detail accent.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinemaVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#050505" stop-opacity="0.25"/>
      <stop offset="45%" stop-color="#050505" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#050505" stop-opacity="0.42"/>
    </linearGradient>

    <linearGradient id="panelSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1a1a1a" stop-opacity="0.82"/>
      <stop offset="58%" stop-color="#060606" stop-opacity="0.68"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.76"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="18" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed cinematic background -->
  <image
    href="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&amp;w=1920&amp;h=1080&amp;fit=crop"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Subtle whole-slide tonal control -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.12"/>

  <!-- Flush-left semi-transparent matte -->
  <rect
    x="0" y="86" width="520" height="552"
    fill="url(#panelSheen)"
    opacity="0.92"
    filter="url(#panelShadow)"/>

  <!-- Very thin architectural edge highlight -->
  <line x1="519" y1="86" x2="519" y2="638" stroke="#ffffff" stroke-width="1" opacity="0.18"/>
  <line x1="70" y1="506" x2="448" y2="506" stroke="#ffffff" stroke-width="1" opacity="0.22"/>

  <!-- Bordered title module -->
  <rect
    x="70" y="158" width="390" height="76"
    fill="none"
    stroke="#ffffff"
    stroke-width="1.6"
    opacity="0.96"/>

  <text
    x="94" y="206"
    width="340"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="25"
    font-weight="700"
    letter-spacing="1.1"
    fill="#ffffff">
    <tspan fill="#d8d8d8">01.</tspan>
    <tspan dx="9">SITE INFORMATION</tspan>
  </text>

  <!-- Subtitle -->
  <text
    x="70" y="276"
    width="405"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="15"
    font-weight="400"
    letter-spacing="1.8"
    fill="#b9b9b9">
    ENVIRONMENTAL CONTEXT / FIELD NOTES
  </text>

  <!-- Custom plus-list body -->
  <text x="76" y="346" width="24" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="23" font-weight="300" fill="#ffffff">+</text>
  <text x="112" y="346" width="330" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="24" font-weight="300" fill="#ffffff">local climate</text>

  <text x="76" y="392" width="24" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="23" font-weight="300" fill="#ffffff">+</text>
  <text x="112" y="392" width="330" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="24" font-weight="300" fill="#ffffff">prevailing winds</text>

  <text x="76" y="438" width="24" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="23" font-weight="300" fill="#ffffff">+</text>
  <text x="112" y="438" width="330" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="24" font-weight="300" fill="#ffffff">solar aspect</text>

  <text x="76" y="484" width="24" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="23" font-weight="300" fill="#ffffff">+</text>
  <text x="112" y="484" width="330" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="24" font-weight="300" fill="#ffffff">vegetation</text>

  <text x="76" y="556" width="24" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="23" font-weight="300" fill="#ffffff">+</text>
  <text x="112" y="556" width="330" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="24" font-weight="300" fill="#ffffff">building context</text>

  <!-- Small technical accent -->
  <text
    x="34" y="608"
    width="210"
    transform="rotate(-90 34 608)"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="10"
    letter-spacing="2.4"
    fill="#ffffff"
    opacity="0.42">
    SITE READINESS / 2026
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a fully opaque panel; the technique depends on preserving the emotional background image through the matte.
- ❌ Do not place text directly over the photo without the dark underlay; readability becomes image-dependent and inconsistent.
- ❌ Do not use native SVG bullet lists or HTML-like text blocks; use explicit `+` marker text so everything remains editable.
- ❌ Do not apply `clip-path` to the matte or text; clipping is only reliable on `<image>` elements.
- ❌ Do not use `<mask>` for glass effects; use translucent fills, gradients, and supported shadows instead.

## Composition notes
- Keep the panel flush to the left edge and limit it to roughly 38–42% of slide width so the image has room to breathe.
- Use generous vertical padding: title near the upper third, subtitle below, list beginning with clear separation.
- Maintain a restrained palette: white typography, muted gray subtitle, nearly black transparent matte.
- Let the right side remain mostly empty or image-led; the visual tension comes from dense information on the left and cinematic space on the right.