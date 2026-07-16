# SVG Recipe — Diegetic Perspective Mockups (3D & Environment Integration)

## Visual mechanism
Turn flat product content into a physical object by drawing it as angled quadrilateral planes: a top screen, visible side extrusions, contact shadows, reflections, and nearby environmental props. The mockup reads as “inside the scene” because the device, UI, shadows, and surrounding paper/glass elements all share the same perspective direction and light source.

## SVG primitives needed
- 1× `<rect>` for the full-slide cinematic background
- 1× `<image>` for a low-opacity environmental photo backdrop, such as a dark desk or studio workspace
- 1× `<clipPath>` with a custom `<path>` for clipping a subtle screen texture/photo into the angled device screen
- 12–18× `<path>` for the device body, perspective screen plane, metallic bevels, paper props, floating glass cards, UI cards, chart surfaces, and decorative highlights
- 3–5× `<ellipse>` for contact shadows, glows, and soft environmental pools of light
- 6–10× `<line>` for editable UI grid lines, notebook ruling, and chart axes
- 8–14× `<text>` with explicit `width` for title, labels, UI microcopy, and callouts
- 4× `<linearGradient>` for cinematic background, metallic edge, luminous screen, and paper/glass surfaces
- 1× `<radialGradient>` for ambient spotlighting behind the device
- 2× `<filter>`: one soft drop shadow for objects and one glow filter for luminous screen elements

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="55%" stop-color="#0B1020"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <radialGradient id="stageGlow" cx="68%" cy="48%" r="54%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.34"/>
      <stop offset="45%" stop-color="#1E40AF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="metalEdge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#CBD5E1"/>
      <stop offset="42%" stop-color="#64748B"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="screenGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="54%" stop-color="#E0F2FE"/>
      <stop offset="100%" stop-color="#BAE6FD"/>
    </linearGradient>
    <linearGradient id="glassGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#67E8F9" stop-opacity="0.12"/>
    </linearGradient>
    <clipPath id="screenClip">
      <path d="M682 171 L971 273 L883 544 L593 429 Z"/>
    </clipPath>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="24" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <image href="https://images.example.com/dark-desk-studio-environment-soft-blue-light.jpg" x="0" y="0" width="1280" height="720" opacity="0.22"/>
  <ellipse cx="840" cy="382" rx="430" ry="290" fill="url(#stageGlow)"/>

  <text x="88" y="120" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="56" font-weight="700" fill="#F8FAFC">
    Product UI, made physical
  </text>
  <text x="92" y="212" width="395" font-family="Segoe UI, Microsoft YaHei" font-size="19" fill="#CBD5E1">
    Embed flat screenshots into a spatial scene with angled planes, bevels, contact shadows, and environmental props.
  </text>
  <line x1="94" y1="278" x2="350" y2="278" stroke="#38BDF8" stroke-width="3" stroke-dasharray="1 14"/>
  <text x="94" y="324" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#67E8F9">
    Perspective is sold by consistency
  </text>
  <text x="94" y="354" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#94A3B8">
    Every screen card, shadow, note, and highlight follows the same down-right vanishing rhythm.
  </text>

  <ellipse cx="824" cy="600" rx="330" ry="52" fill="#000000" opacity="0.42" filter="url(#softShadow)"/>
  <path d="M632 99 L1055 247 L925 641 L500 462 Z" fill="#0F172A" opacity="0.9" filter="url(#softShadow)"/>
  <path d="M632 99 L1055 247 L925 641 L500 462 Z" fill="url(#metalEdge)" stroke="#E2E8F0" stroke-width="2"/>
  <path d="M1055 247 L1082 270 L950 667 L925 641 Z" fill="#334155"/>
  <path d="M500 462 L925 641 L950 667 L521 489 Z" fill="#1E293B"/>
  <path d="M653 130 L1017 258 L903 591 L538 448 Z" fill="#020617" stroke="#94A3B8" stroke-width="2"/>
  <path d="M682 171 L971 273 L883 544 L593 429 Z" fill="url(#screenGrad)" filter="url(#glow)"/>
  <image href="https://images.example.com/analytics-dashboard-interface-light-theme.png" x="590" y="160" width="420" height="400" opacity="0.18" clip-path="url(#screenClip)"/>

  <path d="M700 193 L951 281 L936 328 L684 239 Z" fill="#FFFFFF" opacity="0.94"/>
  <ellipse cx="724" cy="220" rx="15" ry="9" fill="#38BDF8"/>
  <path d="M755 224 L884 270 L879 285 L750 239 Z" fill="#CBD5E1"/>
  <path d="M634 291 L930 395 L887 520 L591 416 Z" fill="#FFFFFF" opacity="0.95"/>
  <line x1="620" y1="392" x2="895" y2="490" stroke="#E2E8F0" stroke-width="2"/>
  <line x1="642" y1="350" x2="914" y2="447" stroke="#E2E8F0" stroke-width="2"/>
  <path d="M640 393 L705 358 L766 387 L823 326 L903 347" fill="none" stroke="#2563EB" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M625 438 L723 473 L707 520 L610 485 Z" fill="#DBEAFE"/>
  <path d="M744 481 L860 522 L844 570 L728 529 Z" fill="#E0F2FE"/>
  <text x="640" y="456" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#0F172A" transform="rotate(20 640 456)">Live metric</text>
  <text x="760" y="502" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#0F172A" transform="rotate(20 760 502)">Forecast</text>

  <path d="M770 68 L1060 166 L1016 286 L727 188 Z" fill="url(#glassGrad)" stroke="#BAE6FD" stroke-width="1.5" opacity="0.72" filter="url(#softShadow)"/>
  <text x="790" y="118" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F8FAFC" transform="rotate(19 790 118)">Spatial annotation</text>
  <text x="796" y="150" width="225" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#CFFAFE" transform="rotate(19 796 150)">A floating pane reinforces depth without covering the product screen.</text>
  <path d="M812 198 L982 255" stroke="#67E8F9" stroke-width="2" stroke-dasharray="8 8" fill="none"/>

  <path d="M756 493 L1110 407 L1164 531 L806 620 Z" fill="#F8FAFC" opacity="0.94" filter="url(#softShadow)"/>
  <path d="M776 512 L1127 430 L1164 531 L806 620 Z" fill="#E2E8F0"/>
  <path d="M798 512 L1066 449" stroke="#CBD5E1" stroke-width="2" fill="none"/>
  <path d="M811 545 L1080 482" stroke="#CBD5E1" stroke-width="2" fill="none"/>
  <path d="M824 577 L1095 514" stroke="#CBD5E1" stroke-width="2" fill="none"/>
  <path d="M965 455 L1130 418 L1165 502 L1000 540 Z" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1.5"/>
  <text x="1000" y="482" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#92400E" transform="rotate(-13 1000 482)">Diegetic layer</text>
  <text x="1010" y="508" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#92400E" transform="rotate(-13 1010 508)">Props make the UI feel placed, not pasted.</text>

  <ellipse cx="1065" cy="308" rx="20" ry="12" fill="#38BDF8" opacity="0.55" filter="url(#glow)"/>
  <path d="M1054 298 L1102 271 L1110 286 L1062 314 Z" fill="#7DD3FC" opacity="0.68"/>
</svg>
```

## Avoid in this skill
- ❌ `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` for perspective; these are dropped. Use hand-authored quadrilateral `<path>` planes instead.
- ❌ `clip-path` on vector shapes to crop UI cards into the screen; clip paths translate reliably only when applied to `<image>`.
- ❌ Perspective-warping a screenshot as a single SVG image; instead, either pre-render the screenshot with perspective externally or rebuild key UI elements as editable angled paths.
- ❌ `marker-end` on paths for callout arrows; if arrows are needed, use editable `<line>` arrows with `marker-end` directly on each line.
- ❌ Filters on `<line>` elements; apply shadow/glow filters to paths, ellipses, rects, circles, or text only.

## Composition notes
- Reserve one side of the slide for copy and let the mockup dominate the opposite side; the angled object should feel like a hero product photograph.
- Keep all perspective planes consistent: if the device slopes down-right, UI cards, notes, highlights, and shadows should echo that same direction.
- Use a dark, low-detail environment so the luminous screen and metallic edges carry the focus.
- Add one or two physical props, such as paper, sticky notes, glass labels, or contact shadows, to make the digital content feel embedded in a real scene.