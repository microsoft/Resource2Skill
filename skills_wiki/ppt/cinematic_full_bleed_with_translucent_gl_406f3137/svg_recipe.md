# SVG Recipe — Cinematic Full-Bleed with Translucent Glass Panel

## Visual mechanism
A high-impact, full-bleed contextual photo owns the entire canvas, while a semi-transparent “glass” panel overlays one side to create a controlled reading zone. Large white typography and a few restrained data accents sit inside the panel, preserving cinematic atmosphere while guaranteeing legibility.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero photograph background
- 2× `<rect>` for subtle full-slide tonal overlays/vignettes
- 1× large `<rect>` for the translucent glass content panel
- 1× `<linearGradient>` for the panel fill, giving the glass a premium tinted depth
- 2× `<linearGradient>` overlays for cinematic darkening and edge contrast
- 1× `<filter id="panelShadow">` applied to the glass panel for soft separation from the photo
- 1× `<filter id="softGlow">` applied to highlight chips/accent shapes
- 4× `<line>` for fine editorial divider rules and accents
- 5× small `<rect>` for metric/data chips inside the panel
- 6× `<text>` blocks with explicit `width` attributes for title, eyebrow, body copy, and metrics
- 1× `<path>` for a subtle diagonal glass sheen across the panel

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinemaVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="42%" stop-color="#000000" stop-opacity="0.00"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.52"/>
    </linearGradient>

    <linearGradient id="bottomGrade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#06111C" stop-opacity="0.00"/>
      <stop offset="68%" stop-color="#06111C" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#06111C" stop-opacity="0.46"/>
    </linearGradient>

    <linearGradient id="glassBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B75D1" stop-opacity="0.82"/>
      <stop offset="54%" stop-color="#064F9C" stop-opacity="0.76"/>
      <stop offset="100%" stop-color="#041A34" stop-opacity="0.86"/>
    </linearGradient>

    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.00"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.00"/>
    </linearGradient>

    <filter id="panelShadow" x="-15%" y="-10%" width="130%" height="120%">
      <feOffset dx="-10" dy="0"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <image
    href="https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
    xlink:href="https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomGrade)"/>

  <rect x="560" y="0" width="720" height="720" fill="url(#glassBlue)" filter="url(#panelShadow)"/>
  <path d="M610 0 L840 0 L660 720 L555 720 Z" fill="url(#sheen)" opacity="0.42"/>

  <line x1="628" y1="108" x2="746" y2="108" stroke="#8FE6FF" stroke-width="3"/>
  <line x1="628" y1="526" x2="1098" y2="526" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1"/>
  <line x1="628" y1="609" x2="1098" y2="609" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="1188" y1="84" x2="1188" y2="640" stroke="#8FE6FF" stroke-opacity="0.35" stroke-width="2"/>

  <text x="628" y="86" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#BFEFFF" letter-spacing="2">
    UNESCO HERITAGE PROFILE
  </text>

  <text x="624" y="184" width="510" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" fill="#FFFFFF">
    <tspan x="624" dy="0">THE QUTUB</tspan>
    <tspan x="624" dy="64">MINAR</tspan>
  </text>

  <text x="628" y="330" width="485" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="400" fill="#EAF8FF">
    <tspan x="628" dy="0">A landmark of early Indo-Islamic architecture,</tspan>
    <tspan x="628" dy="34">built as a monumental vertical marker and</tspan>
    <tspan x="628" dy="34">now one of Delhi’s most recognizable symbols.</tspan>
  </text>

  <rect x="628" y="446" width="148" height="58" rx="12" fill="#FFFFFF" opacity="0.12" filter="url(#softGlow)"/>
  <rect x="628" y="446" width="148" height="58" rx="12" fill="#FFFFFF" opacity="0.14"/>
  <rect x="792" y="446" width="148" height="58" rx="12" fill="#FFFFFF" opacity="0.14"/>
  <rect x="956" y="446" width="148" height="58" rx="12" fill="#FFFFFF" opacity="0.14"/>

  <text x="650" y="471" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#FFFFFF">73 m</text>
  <text x="650" y="493" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600" fill="#BFEFFF" letter-spacing="1">HEIGHT</text>

  <text x="814" y="471" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#FFFFFF">1199</text>
  <text x="814" y="493" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600" fill="#BFEFFF" letter-spacing="1">ORIGIN</text>

  <text x="978" y="471" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#FFFFFF">5</text>
  <text x="978" y="493" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600" fill="#BFEFFF" letter-spacing="1">STOREYS</text>

  <text x="628" y="572" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#D8F2FF">
    Use the image to carry emotion; use the glass panel to carry the message.
  </text>

  <text x="628" y="654" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#A7DDF4" letter-spacing="1.5">
    EXECUTIVE LOCATION BRIEF · NEW DELHI
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not place white text directly over a busy photo without a tinted panel or strong gradient backing.
- ❌ Do not use `<mask>` or backdrop-blur style effects; PowerPoint translation will not preserve true frosted-glass blur.
- ❌ Do not make the panel too transparent; below roughly 55–60% opacity, legibility collapses on bright photography.
- ❌ Do not use dense bullets inside the panel; this technique works best with a headline, short paragraph, and a few high-signal data chips.
- ❌ Do not rely on filters on `<line>` elements for glow; use filters only on supported shapes like `<rect>`, `<path>`, or `<text>`.

## Composition notes
- Keep the hero subject in the uncovered 40–50% of the slide; place the panel on the side with less important image detail.
- Use generous internal padding inside the panel, typically 60–80 px from the panel edge to the text.
- Preserve a cinematic hierarchy: enormous title, short supporting copy, then small metric chips or source line.
- Maintain color rhythm by sampling panel color from the image mood: deep blue for sky/architecture, black slate for night/city, teal for water/technology.