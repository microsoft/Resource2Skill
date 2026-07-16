# SVG Recipe — Centered Hero Cover

## Visual mechanism
A full-bleed cinematic hero image sets the emotional tone, while layered dark gradients create a calm central stage for a logo, oversized centered headline, and concise subtitle. The composition is minimalist but premium: image texture at the edges, high contrast in the center, and a single elegant focal stack.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero photograph
- 1× `<image>` for the centered logo mark
- 1× `<clipPath>` with rounded `<rect>` for the logo image crop
- 3× `<rect>` for dark scrims, gradient overlays, and the logo tile
- 2× `<radialGradient>` for vignette and center spotlight control
- 2× `<linearGradient>` for top/bottom contrast and subtle color wash
- 1× `<filter id="softShadow">` applied to the logo tile
- 1× `<filter id="titleGlow">` applied to the headline text
- 2× `<path>` for subtle editorial light streaks / premium decorative motion
- 4× `<text>` blocks for eyebrow, headline, subtitle, and small footer metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="topBottomScrim" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.82"/>
      <stop offset="36%" stop-color="#020617" stop-opacity="0.28"/>
      <stop offset="70%" stop-color="#020617" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.88"/>
    </linearGradient>

    <linearGradient id="coolWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#0F172A" stop-opacity="0.58"/>
      <stop offset="45%" stop-color="#111827" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#2563EB" stop-opacity="0.25"/>
    </linearGradient>

    <radialGradient id="centerClarity" cx="50%" cy="45%" r="52%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.05"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.70"/>
    </radialGradient>

    <radialGradient id="logoHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.22"/>
      <stop offset="55%" stop-color="#93C5FD" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-15%" y="-30%" width="130%" height="160%">
      <feGaussianBlur stdDeviation="2.4" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="logoCrop">
      <rect x="594" y="132" width="92" height="92" rx="24" ry="24"/>
    </clipPath>
  </defs>

  <image
    href="https://images.example.com/hero-photo-modern-glass-headquarters-at-dusk.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#topBottomScrim)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#coolWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerClarity)"/>

  <path
    d="M-40 565 C180 465 310 505 485 430 C650 358 785 238 1045 276 C1160 293 1240 260 1320 210 L1320 720 L-40 720 Z"
    fill="#0EA5E9"
    opacity="0.10"/>

  <path
    d="M1320 88 C1115 176 960 128 778 192 C622 247 492 356 292 326 C158 306 50 342 -40 404 L-40 -20 L1320 -20 Z"
    fill="#FFFFFF"
    opacity="0.055"/>

  <ellipse cx="640" cy="178" rx="150" ry="118" fill="url(#logoHalo)" opacity="0.95"/>

  <rect
    x="594" y="132" width="92" height="92" rx="24" ry="24"
    fill="#FFFFFF"
    opacity="0.94"
    filter="url(#softShadow)"/>

  <image
    href="https://images.example.com/logo-minimal-navy-monogram.png"
    x="594" y="132" width="92" height="92"
    preserveAspectRatio="xMidYMid meet"
    clip-path="url(#logoCrop)"/>

  <text
    x="640" y="278" width="720"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="15"
    font-weight="700"
    letter-spacing="4"
    fill="#C7D2FE"
    opacity="0.92">
    ANNUAL STRATEGY BRIEFING
  </text>

  <text
    x="640" y="368" width="900"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="68"
    font-weight="800"
    letter-spacing="-2"
    fill="#FFFFFF"
    filter="url(#titleGlow)">
    <tspan x="640" dy="0">Building the Next</tspan>
    <tspan x="640" dy="78">Growth Horizon</tspan>
  </text>

  <text
    x="640" y="530" width="760"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="23"
    font-weight="400"
    fill="#E5E7EB"
    opacity="0.90">
    A focused operating agenda for scale, resilience, and market leadership
  </text>

  <line
    x1="566" y1="574" x2="714" y2="574"
    stroke="#93C5FD"
    stroke-width="2"
    stroke-linecap="round"
    opacity="0.72"/>

  <text
    x="640" y="624" width="620"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="14"
    font-weight="600"
    letter-spacing="1.8"
    fill="#CBD5E1"
    opacity="0.76">
    EXECUTIVE SESSION · Q4 2026
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a flat color background instead of a full-bleed image; it removes the “hero cover” impact.
- ❌ Placing headline text directly over a busy photo without gradient scrims or vignette control.
- ❌ Applying `clip-path` to text or decorative shapes; use it only on the logo/image crop.
- ❌ Using `<mask>` for the vignette; use editable gradient-filled rectangles instead.
- ❌ Overloading the cover with bullets, charts, or multiple content zones; this shell should stay low-density.

## Composition notes
- Keep all key content in the central vertical stack: logo around y=130–225, title around y=300–445, subtitle around y=520.
- Preserve strong negative space around the headline; the image should support mood, not compete for attention.
- Use dark overlays and cool accent gradients to guarantee white typography remains legible.
- Let the hero photo show most clearly near the outer thirds and corners, while the center remains calm and high contrast.