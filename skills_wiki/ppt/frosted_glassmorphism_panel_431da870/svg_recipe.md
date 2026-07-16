# SVG Recipe — Frosted Glassmorphism Panel

## Visual mechanism
A vibrant abstract background is partially repeated inside a rounded panel as a pre-blurred crop, then covered with a translucent white tint, bright edge stroke, soft shadow, and subtle specular highlights. The result reads as a floating sheet of frosted glass that preserves background color energy while making foreground text legible.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient base.
- 1× `<image>` for the sharp vibrant background layer.
- 1× `<image>` for the pre-blurred duplicate/crop of the same background, clipped to the glass panel.
- 1× `<clipPath>` with rounded `<rect>` for the glass image crop.
- 5× `<ellipse>` for editable ambient mesh-gradient color blooms behind the glass.
- 3× `<rect>` for panel shadow body, glass tint, and inner highlight wash.
- 2× `<path>` for curved specular glass streaks.
- 1× `<filter id="panelShadow">` using offset + blur + merge for depth.
- 1× `<filter id="orbBlur">` using Gaussian blur for soft abstract background blobs.
- 1× `<filter id="softGlow">` for subtle luminous highlights.
- 4× `<text>` blocks with explicit `width` for title, subtitle, label, and microcopy.
- 2× `<linearGradient>` and 1× `<radialGradient>` for premium translucent color and background lighting.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBase" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#13072E"/>
      <stop offset="0.45" stop-color="#24105C"/>
      <stop offset="1" stop-color="#061D3E"/>
    </linearGradient>

    <linearGradient id="glassTint" x1="360" y1="120" x2="880" y2="600">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="0.48" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#BEE9FF" stop-opacity="0.10"/>
    </linearGradient>

    <radialGradient id="innerBloom" cx="35%" cy="20%" r="85%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.30"/>
      <stop offset="0.42" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="orbBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="38"/>
    </filter>

    <filter id="panelShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="0" dy="22" result="off"/>
      <feGaussianBlur in="off" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>

    <clipPath id="glassClip" clipPathUnits="userSpaceOnUse">
      <rect x="330" y="126" width="560" height="468" rx="38" ry="38"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBase)"/>

  <image
    href="https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=1600&q=80"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"
    opacity="0.72"/>

  <ellipse cx="160" cy="110" rx="300" ry="240" fill="#8A3FFC" opacity="0.58" filter="url(#orbBlur)"/>
  <ellipse cx="1040" cy="145" rx="260" ry="210" fill="#00D4FF" opacity="0.50" filter="url(#orbBlur)"/>
  <ellipse cx="975" cy="620" rx="360" ry="210" fill="#FF2EA6" opacity="0.43" filter="url(#orbBlur)"/>
  <ellipse cx="520" cy="690" rx="330" ry="150" fill="#FFC247" opacity="0.38" filter="url(#orbBlur)"/>
  <ellipse cx="650" cy="320" rx="260" ry="190" fill="#39FFB6" opacity="0.20" filter="url(#orbBlur)"/>

  <rect x="330" y="126" width="560" height="468" rx="38" ry="38"
        fill="#050512" opacity="0.28" filter="url(#panelShadow)"/>

  <image
    href="https://images.example.com/same-neon-background-preblurred-crop-for-frosted-glass-panel.jpg"
    x="330" y="126" width="560" height="468"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#glassClip)"
    opacity="0.90"/>

  <rect x="330" y="126" width="560" height="468" rx="38" ry="38"
        fill="url(#glassTint)"
        stroke="#FFFFFF" stroke-opacity="0.58" stroke-width="1.7"/>

  <rect x="342" y="138" width="536" height="444" rx="30" ry="30"
        fill="url(#innerBloom)"
        stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1"/>

  <path d="M370 167 C470 121, 612 124, 742 152"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.56" stroke-width="2.2"
        stroke-linecap="round" filter="url(#softGlow)"/>

  <path d="M805 500 C770 552, 704 579, 622 576"
        fill="none" stroke="#BEE9FF" stroke-opacity="0.28" stroke-width="1.6"
        stroke-linecap="round"/>

  <rect x="382" y="184" width="186" height="34" rx="17" ry="17"
        fill="#FFFFFF" opacity="0.16"
        stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1"/>

  <text x="406" y="206" width="150"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="2" fill="#FFFFFF" opacity="0.92">
    2026 VISION
  </text>

  <text x="382" y="292" width="430"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700"
        fill="#FFFFFF">
    <tspan x="382" dy="0">Frosted</tspan>
    <tspan x="382" dy="66">Interface</tspan>
  </text>

  <text x="386" y="430" width="394"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="400"
        fill="#F1F8FF" opacity="0.88">
    <tspan x="386" dy="0">A premium glass panel that softens</tspan>
    <tspan x="386" dy="30">complex color fields while keeping the</tspan>
    <tspan x="386" dy="30">slide luminous, modern, and readable.</tspan>
  </text>

  <line x1="386" y1="522" x2="520" y2="522"
        stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="1.5"/>

  <text x="386" y="556" width="380"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="500"
        fill="#FFFFFF" opacity="0.74">
    Use for hero titles, product narratives, UX mockups, and high-end technology keynotes.
  </text>

  <circle cx="982" cy="210" r="78" fill="#FFFFFF" opacity="0.08"
          stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1.2"/>
  <circle cx="1018" cy="244" r="18" fill="#FFFFFF" opacity="0.22"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use CSS `backdrop-filter`; it will not translate into editable PowerPoint glass blur.
- ❌ Do not apply `clip-path` to a `<g>`, `<rect>`, or `<path>` for the glass crop; use it only on the blurred `<image>`.
- ❌ Do not rely on a live SVG blur filter on `<image>` for the frosted region; prepare a blurred duplicate/crop image asset instead.
- ❌ Do not make the glass fill too opaque; above ~35–40% white opacity it becomes a flat white card rather than glass.
- ❌ Do not place thin, low-contrast body text directly over the busiest part of the background without the frosted layer.

## Composition notes
- Place the glass panel slightly off-center and let it occupy roughly 40–55% of the slide width; the remaining space should show the vibrant environment.
- Use generous internal padding: title and body text should sit at least 48–64 px from the panel edge.
- Keep the panel edge bright but delicate: a 1–2 px white stroke with partial opacity creates the “catching light” effect.
- Backgrounds need visible color variation; saturated gradients, blurred orbs, neon mesh images, or abstract photos work better than flat fills.