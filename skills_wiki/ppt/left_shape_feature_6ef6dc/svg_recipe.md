# SVG Recipe — Minimal Left Circle Feature

## Visual mechanism
A large, partially off-canvas circle on the left acts as a calm visual anchor, while the headline and supporting copy sit in generous negative space on the right. Subtle rings, dots, and technical linework inside the circle add polish without breaking the minimal section-divider feel.

## SVG primitives needed
- 1× `<rect>` for the soft neutral slide background
- 3× `<linearGradient>` / `<radialGradient>` definitions for the circle fill, highlight, and small accent dots
- 2× `<filter>` definitions: one soft shadow for the main circle, one glow for accent elements
- 5× `<circle>` for the main feature circle, outer rings, highlight disk, and accent dots
- 4× `<path>` for internal abstract technical strokes and a soft highlight sweep
- 6× `<line>` for minimal connector ticks and section-rule accents
- 5× `<text>` elements with explicit `width` attributes for kicker, title, body, section number, and micro-label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="circleFill" x1="-260" y1="120" x2="330" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2DD4BF"/>
      <stop offset="0.45" stop-color="#2563EB"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>

    <radialGradient id="circleHighlight" cx="35%" cy="28%" r="68%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="dotFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#A7F3D0"/>
      <stop offset="1" stop-color="#60A5FA"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F8FA"/>

  <circle cx="-42" cy="360" r="272" fill="#E7ECF2"/>
  <circle cx="-42" cy="360" r="246" fill="url(#circleFill)" filter="url(#softShadow)"/>
  <circle cx="-42" cy="360" r="246" fill="url(#circleHighlight)"/>

  <circle cx="-42" cy="360" r="306" fill="none" stroke="#CBD5E1" stroke-width="1.4" stroke-dasharray="9 13"/>
  <circle cx="-42" cy="360" r="194" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.26"/>
  <circle cx="-42" cy="360" r="122" fill="none" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.18" stroke-dasharray="5 9"/>

  <path d="M-212 354 C-156 296 -92 288 -42 328 C15 374 76 382 132 323"
        fill="none" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.34" stroke-linecap="round"/>
  <path d="M-181 420 C-112 464 -35 456 31 405 C78 369 121 366 166 392"
        fill="none" stroke="#A7F3D0" stroke-width="2.4" stroke-opacity="0.45" stroke-linecap="round"/>
  <path d="M-118 213 C-52 184 24 207 67 263"
        fill="none" stroke="#BFDBFE" stroke-width="2" stroke-opacity="0.36" stroke-linecap="round"/>
  <path d="M105 195 C139 239 155 289 151 344 C148 382 136 415 118 443"
        fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-opacity="0.22" stroke-dasharray="4 8"/>

  <circle cx="76" cy="266" r="9" fill="url(#dotFill)" filter="url(#softGlow)"/>
  <circle cx="152" cy="394" r="6" fill="#FFFFFF" fill-opacity="0.78"/>
  <circle cx="-134" cy="476" r="5" fill="#A7F3D0" fill-opacity="0.78"/>

  <line x1="300" y1="226" x2="394" y2="226" stroke="#CBD5E1" stroke-width="1.4"/>
  <line x1="334" y1="252" x2="420" y2="252" stroke="#E2E8F0" stroke-width="1.2"/>
  <line x1="300" y1="494" x2="376" y2="494" stroke="#CBD5E1" stroke-width="1.4"/>
  <line x1="980" y1="516" x2="1080" y2="516" stroke="#2563EB" stroke-width="2"/>
  <line x1="1092" y1="516" x2="1124" y2="516" stroke="#94A3B8" stroke-width="2"/>
  <line x1="1136" y1="516" x2="1162" y2="516" stroke="#94A3B8" stroke-width="2"/>

  <text x="560" y="214" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="3" fill="#2563EB">
    SECTION 03
  </text>

  <text x="560" y="286" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="700" fill="#0F172A">
    <tspan x="560" dy="0">Operational</tspan>
    <tspan x="560" dy="66">Readiness</tspan>
  </text>

  <text x="562" y="388" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="400" fill="#475569">
    <tspan x="562" dy="0">A focused section divider for introducing a new</tspan>
    <tspan x="562" dy="30">feature, capability area, or executive workstream.</tspan>
  </text>

  <text x="1000" y="474" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2" fill="#64748B">
    FEATURE ANCHOR
  </text>

  <text x="1000" y="552" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="500" fill="#94A3B8">
    minimal / technical / calm
  </text>
</svg>
```

## Avoid in this skill
- ❌ Centering the circle fully on the slide; the premium look depends on the circle being cropped by the left edge.
- ❌ Adding heavy charts, tables, or dense bullet lists; this is a low-density divider layout.
- ❌ Using hard black outlines on the circle; keep rings and inner strokes translucent.
- ❌ Placing text over the circle unless the slide is intentionally title-only; the default composition needs clean right-side negative space.
- ❌ Applying filters to `<line>` elements; use filters only on circles, paths, or text.

## Composition notes
- Keep the circle center slightly outside the left edge, with roughly 35–45% of the circle visible on the slide.
- Reserve the right 55–60% of the canvas for headline and short supporting copy.
- Use one saturated accent color from the circle in the kicker or small rule lines to create visual continuity.
- Maintain large vertical breathing room; the headline should feel like a section title, not a content block.