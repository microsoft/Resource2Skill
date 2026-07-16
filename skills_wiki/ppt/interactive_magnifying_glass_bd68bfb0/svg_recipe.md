# SVG Recipe — Interactive Magnifying Glass

## Visual mechanism
Layer a full-size base image beneath a circularly clipped duplicate image that is scaled up and offset so the lens reveals the correct enlarged detail. Add a metallic lens rim, glass glare, handle, shadow, and a small label to make the focus device feel premium and intentional.

## SVG primitives needed
- 1× `<image>` for the full base screenshot/photo/diagram
- 1× `<image>` for the magnified duplicate, scaled and clipped to a circular lens
- 1× `<clipPath>` with `<rect rx>` for the rounded base image crop
- 1× `<clipPath>` with `<circle>` for the lens crop
- 3× `<circle>` for lens shadow, rim, and inner glass edge
- 2× `<path>` for the magnifying glass handle and metallic handle highlight
- 2× `<linearGradient>` for background and metallic rim/handle
- 1× `<radialGradient>` for subtle glass tint
- 2× `<filter>` using blur/offset for card shadow and lens shadow/glow
- 4× `<rect>` for background panels, title tag, side note card, and subtle overlays
- 4× `<text>` elements with explicit `width` for title, label, zoom badge, and explanatory note
- 2× `<line>` elements for thin callout ticks, if you want to connect label to lens

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0B1020"/>
      <stop offset="0.55" stop-color="#111827"/>
      <stop offset="1" stop-color="#1E293B"/>
    </linearGradient>

    <linearGradient id="rimMetal" x1="610" y1="165" x2="850" y2="435" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.18" stop-color="#D7DEE8"/>
      <stop offset="0.48" stop-color="#7C8796"/>
      <stop offset="0.72" stop-color="#F4F7FB"/>
      <stop offset="1" stop-color="#64748B"/>
    </linearGradient>

    <linearGradient id="handleMetal" x1="800" y1="420" x2="1010" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F8FAFC"/>
      <stop offset="0.45" stop-color="#94A3B8"/>
      <stop offset="1" stop-color="#334155"/>
    </linearGradient>

    <radialGradient id="glassTint" cx="40%" cy="32%" r="70%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="0.45" stop-color="#BAE6FD" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#0EA5E9" stop-opacity="0.06"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="lensShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="baseRoundClip">
      <rect x="90" y="110" width="820" height="500" rx="28"/>
    </clipPath>

    <clipPath id="lensClip">
      <circle cx="735" cy="315" r="125"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M0,610 C210,545 330,705 520,635 C720,560 820,590 990,640 C1115,675 1200,655 1280,620 L1280,720 L0,720 Z"
        fill="#38BDF8" opacity="0.08"/>
  <path d="M1020,0 C1110,80 1160,150 1280,145 L1280,0 Z" fill="#A78BFA" opacity="0.14"/>

  <text x="88" y="62" width="660" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#F8FAFC">Interactive Magnifying Glass</text>
  <text x="90" y="94" width="690" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#CBD5E1">A moving lens reveals a zoomed duplicate of the same visual, cropped to a circular focus area.</text>

  <rect x="76" y="96" width="848" height="528" rx="34" fill="#020617" opacity="0.72" filter="url(#cardShadow)"/>
  <rect x="90" y="110" width="820" height="500" rx="28" fill="#0F172A"/>

  <image x="90" y="110" width="820" height="500" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/product-dashboard-ui-with-dense-metrics-and-map.jpg"
         clip-path="url(#baseRoundClip)"/>

  <rect x="90" y="110" width="820" height="500" rx="28" fill="none" stroke="#334155" stroke-width="2"/>
  <rect x="112" y="132" width="190" height="34" rx="17" fill="#020617" opacity="0.72"/>
  <text x="132" y="155" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" fill="#E2E8F0">Live product view</text>

  <rect x="945" y="130" width="250" height="186" rx="26" fill="#0F172A" opacity="0.88" stroke="#334155"/>
  <text x="972" y="170" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#F8FAFC">Detail spotlight</text>
  <text x="972" y="205" width="195" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#CBD5E1">
    <tspan x="972" dy="0">Duplicate the base image,</tspan>
    <tspan x="972" dy="21">scale it up, then clip it</tspan>
    <tspan x="972" dy="21">inside the circular lens.</tspan>
  </text>
  <rect x="972" y="268" width="76" height="28" rx="14" fill="#0EA5E9"/>
  <text x="993" y="287" width="52" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#FFFFFF">2.25×</text>

  <path d="M812 397 C850 430 888 468 928 510" fill="none" stroke="#111827" stroke-width="46"
        stroke-linecap="round" opacity="0.35" filter="url(#lensShadow)"/>
  <path d="M812 397 C850 430 888 468 928 510" fill="none" stroke="url(#handleMetal)" stroke-width="34"
        stroke-linecap="round"/>
  <path d="M805 390 C842 423 880 461 920 502" fill="none" stroke="#FFFFFF" stroke-width="8"
        stroke-linecap="round" opacity="0.42"/>

  <circle cx="735" cy="315" r="139" fill="#020617" opacity="0.38" filter="url(#lensShadow)"/>

  <image x="-716.25" y="-146.25" width="1845" height="1125" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/product-dashboard-ui-with-dense-metrics-and-map.jpg"
         clip-path="url(#lensClip)"/>

  <circle cx="735" cy="315" r="125" fill="url(#glassTint)" stroke="#E0F2FE" stroke-width="2"/>
  <circle cx="735" cy="315" r="137" fill="none" stroke="url(#rimMetal)" stroke-width="18"/>
  <circle cx="735" cy="315" r="113" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.48"/>
  <path d="M672 238 C703 214 759 210 796 238" fill="none" stroke="#FFFFFF" stroke-width="10"
        stroke-linecap="round" opacity="0.38"/>
  <ellipse cx="695" cy="265" rx="22" ry="12" fill="#FFFFFF" opacity="0.34" transform="rotate(-28 695 265)"/>

  <line x1="1028" y1="268" x2="875" y2="342" stroke="#38BDF8" stroke-width="2" stroke-dasharray="6 8"/>
  <line x1="1048" y1="282" x2="894" y2="393" stroke="#38BDF8" stroke-width="2" stroke-dasharray="6 8"/>

  <rect x="96" y="548" width="356" height="42" rx="21" fill="#020617" opacity="0.62"/>
  <text x="122" y="575" width="315" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#E2E8F0">Morph lens position between slides for an interactive walkthrough.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` for the lens crop; use `<clipPath>` applied directly to the magnified `<image>`.
- ❌ Do not clip vector shapes or groups; `clip-path` should be applied only to `<image>` for reliable PowerPoint translation.
- ❌ Do not use `<use>` to duplicate the base image; place a second explicit `<image>` with the same `href`.
- ❌ Do not put `filter` on `<line>` callouts; filters on lines are dropped.
- ❌ Do not use SVG animation elements. For movement, create two slides with the same named lens elements and use PowerPoint Morph.

## Composition notes
- Keep the base visual large, usually 60–75% of slide width, so the audience understands the surrounding context.
- Make the lens 15–25% of slide width; smaller feels insignificant, larger hides too much of the source image.
- The magnified duplicate must be scaled and offset mathematically so the lens center corresponds to the same point on the base image.
- Use neutral metallic rim colors and soft blue glass highlights so the lens feels premium without competing with the content.