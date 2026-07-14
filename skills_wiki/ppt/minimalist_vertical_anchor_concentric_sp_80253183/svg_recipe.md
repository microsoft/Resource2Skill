# SVG Recipe — Minimalist Vertical Anchor & Concentric Spotlight

## Visual mechanism
A clean employee-profile layout uses a bright cyan vertical rule as the compositional anchor, separating a human portrait from interview/profile copy. The portrait is softened with a circular crop and surrounded by disconnected concentric arcs, creating a premium “spotlight” effect without heavy framing.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× `<rect>` for the vertical cyan anchor and a tiny secondary brand bar
- 1× `<image>` clipped into a circle for the employee portrait
- 1× `<clipPath>` with `<circle>` for the circular portrait crop
- 3× `<circle>` for pale spotlight halos and accent dots
- 5× `<path>` for disconnected concentric arc rings around the portrait
- 1× `<linearGradient>` for the cyan anchor highlight
- 1× `<radialGradient>` for the subtle portrait halo
- 2× `<filter>` definitions for soft shadow and cyan glow
- 7× `<text>` blocks for eyebrow, name, role, quote, metadata, and logo-like lockup
- Nested `<tspan>` elements for multi-line quote/name styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cyanAnchor" x1="0" y1="220" x2="0" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#34C9F4"/>
      <stop offset="0.55" stop-color="#00A3E0"/>
      <stop offset="1" stop-color="#007EBC"/>
    </linearGradient>

    <radialGradient id="portraitHalo" cx="38%" cy="50%" r="42%">
      <stop offset="0" stop-color="#EAF9FF" stop-opacity="0.95"/>
      <stop offset="0.62" stop-color="#D8F2FB" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>

    <clipPath id="portraitClip" clipPathUnits="userSpaceOnUse">
      <circle cx="390" cy="360" r="168"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <circle cx="390" cy="360" r="255" fill="url(#portraitHalo)"/>
  <circle cx="390" cy="360" r="196" fill="#FFFFFF" filter="url(#softShadow)"/>

  <image
    href="https://images.example.com/corporate-interview-portrait-office-window.jpg"
    x="222" y="192" width="336" height="336"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#portraitClip)"/>

  <path d="M 245 160 A 270 270 0 0 1 655 405"
        fill="none" stroke="#00A3E0" stroke-width="16" stroke-linecap="round"/>
  <path d="M 188 395 A 250 250 0 0 1 435 112"
        fill="none" stroke="#8ED0EB" stroke-width="7" stroke-linecap="round"/>
  <path d="M 544 198 A 215 215 0 0 1 548 519"
        fill="none" stroke="#00A3E0" stroke-width="9" stroke-linecap="round"/>
  <path d="M 205 495 A 230 230 0 0 0 359 596"
        fill="none" stroke="#8ED0EB" stroke-width="10" stroke-linecap="round"/>
  <path d="M 295 135 A 202 202 0 0 1 474 124"
        fill="none" stroke="#CBEFF8" stroke-width="6" stroke-linecap="round"/>

  <circle cx="632" cy="360" r="10" fill="#00A3E0" filter="url(#cyanGlow)"/>
  <circle cx="184" cy="297" r="7" fill="#8ED0EB"/>
  <circle cx="505" cy="590" r="5" fill="#00A3E0"/>

  <rect x="645" y="237" width="8" height="246" rx="4" fill="url(#cyanAnchor)"/>
  <rect x="645" y="508" width="8" height="36" rx="4" fill="#8ED0EB"/>

  <text x="695" y="178" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="3" fill="#8ED0EB">
    EMPLOYEE SPOTLIGHT
  </text>

  <text x="694" y="250" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="300" fill="#142850">
    <tspan x="694" dy="0">Meet the people</tspan>
    <tspan x="694" dy="52">behind the work.</tspan>
  </text>

  <text x="694" y="380" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="50" font-weight="600" fill="#C83232">
    Jared Benedict
  </text>

  <text x="697" y="426" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="600" fill="#142850">
    Senior Director, Advisory Services
  </text>

  <text x="697" y="471" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" line-height="1.4" fill="#52627A">
    <tspan x="697" dy="0">“The best part of the work is helping</tspan>
    <tspan x="697" dy="28">teams find clarity in moments of change.”</tspan>
  </text>

  <text x="697" y="562" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2" fill="#00A3E0">
    CULTURE · LEADERSHIP · CLIENT IMPACT
  </text>

  <text x="1055" y="610" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" text-anchor="end" fill="#142850">
    MORGANFRANKLIN
  </text>
  <text x="1055" y="631" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" font-weight="500" text-anchor="end" letter-spacing="1.8" fill="#8BA0B7">
    CONSULTING
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to crop the portrait; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not build the concentric arcs with `<use>` duplicates; draw each arc path explicitly so PowerPoint keeps them editable.
- ❌ Do not apply `clip-path` to rings, text, or regular shapes; clipping is reliable here only on the portrait image.
- ❌ Do not rely on animation primitives for rotating rings; create a strong static arc composition instead.
- ❌ Do not use `<textPath>` for curved captions around the portrait; it will not translate reliably.

## Composition notes
- Keep the portrait cluster on the left 40–45% of the slide and the text block on the right 45–50%, leaving generous whitespace between them.
- The cyan vertical anchor should sit just to the right of the portrait and align with the main text block’s vertical center.
- Use disconnected arcs with varied stroke weights and colors; avoid a full circular border, which makes the design feel less premium.
- Limit the palette to white, deep navy, cyan, pale blue, and one warm personal accent for the employee name.