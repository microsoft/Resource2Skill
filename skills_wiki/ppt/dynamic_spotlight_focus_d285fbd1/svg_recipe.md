# SVG Recipe — Dynamic Spotlight Focus

## Visual mechanism
A blurred full-slide visual becomes a low-distraction canvas while a sharp, magnified circular crop reveals one detail with high contrast. Across slides, duplicate the composition and move the spotlight circle plus its clipped image offset so PowerPoint Morph creates the illusion of a guided magnifying lens gliding over the scene.

## SVG primitives needed
- 2× `<image>` for the same source visual: one pre-blurred full-slide background, one sharp oversized image clipped inside the spotlight
- 1× `<clipPath>` with a `<circle>` for the spotlight crop applied only to the sharp `<image>`
- 4× `<circle>` for glow halo, white spotlight rim, secondary blue rim, and small callout anchor dot
- 2× `<rect>` for dark base/vignette overlay and the semi-transparent information card
- 2× `<path>` for the dotted journey curve and premium card accent stripe
- 1× `<line>` for a simple callout leader without arrowhead
- 4× `<text>` blocks with explicit `width` attributes for slide label, card eyebrow, headline, and description
- 1× `<radialGradient>` for the darkened edge vignette
- 1× `<linearGradient>` for the glassy dark callout card
- 1× `<filter id="shadow">` applied to the spotlight rim/card for depth
- 1× `<filter id="glow">` applied to the spotlight halo for luminous focus

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="spotClip">
      <circle cx="805" cy="302" r="142"/>
    </clipPath>

    <radialGradient id="vignette" cx="50%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="68%" stop-color="#000000" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </radialGradient>

    <linearGradient id="cardFill" x1="116" y1="462" x2="610" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#111827" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.78"/>
    </linearGradient>

    <filter id="shadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#060914"/>

  <image href="https://images.example.com/product-dashboard-ui-blurred-background.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="#07111A" opacity="0.28"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <path d="M260 212 C420 148 590 178 805 302 C930 374 1030 396 1110 318"
        fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.30"
        stroke-dasharray="8 14"/>

  <circle cx="260" cy="212" r="38" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.22"/>
  <circle cx="1110" cy="318" r="44" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.18"/>

  <circle cx="805" cy="302" r="166" fill="#59C7FF" opacity="0.26" filter="url(#glow)"/>

  <image href="https://images.example.com/product-dashboard-ui-sharp-original.jpg"
         x="-624" y="-242" width="2304" height="1296" preserveAspectRatio="none"
         clip-path="url(#spotClip)"/>

  <circle cx="805" cy="302" r="142" fill="none" stroke="#FFFFFF" stroke-width="7" filter="url(#shadow)"/>
  <circle cx="805" cy="302" r="151" fill="none" stroke="#7DD3FC" stroke-width="2" stroke-opacity="0.72"/>

  <line x1="708" y1="409" x2="590" y2="478" stroke="#DFF6FF" stroke-width="2" stroke-opacity="0.72"/>
  <circle cx="708" cy="409" r="6" fill="#DFF6FF"/>

  <rect x="116" y="462" width="494" height="168" rx="24" fill="url(#cardFill)" filter="url(#shadow)"/>
  <path d="M140 462 H330 C346 462 358 474 358 490 V490 H140 Z"
        fill="#38BDF8" opacity="0.95"/>

  <text x="48" y="58" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="600" fill="#E5F6FF" opacity="0.82" letter-spacing="2">
    DYNAMIC SPOTLIGHT FOCUS
  </text>

  <text x="142" y="492" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        font-weight="700" fill="#00111A" letter-spacing="1.6">
    02 / PRODUCT TOUR
  </text>

  <text x="142" y="535" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="30"
        font-weight="700" fill="#FFFFFF">
    Revenue forecast engine
  </text>

  <text x="142" y="574" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="17"
        fill="#D5E7F2">
    <tspan x="142" dy="0">The lens crops into the exact model-control area,</tspan>
    <tspan x="142" dy="25">keeping the full interface visible but intentionally soft.</tspan>
  </text>

  <text x="930" y="650" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        fill="#BFEFFF" opacity="0.70" text-anchor="middle">
    Duplicate slide → move lens → adjust image offset → apply Morph
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the moving lens; create separate slides and use PowerPoint Morph.
- ❌ Do not apply `clip-path` to a `<circle>` or `<g>` expecting it to crop content; apply the clip path directly to the sharp `<image>`.
- ❌ Do not use `<mask>` to punch a clear hole through a blurred overlay; masks are not reliable for this translation path.
- ❌ Do not put `filter` on a `<line>` for the callout leader; use plain lines and place shadow/glow on circles or rectangles instead.
- ❌ Do not use `<use>` to duplicate focus rings; draw each circle/path explicitly so the PPT shapes remain editable.

## Composition notes
- Keep the blurred image full-bleed; the entire slide should feel like one continuous visual field, not a panel layout.
- Place the spotlight off-center whenever possible, then balance it with the explanation card in an open negative-space region.
- Use neutral UI colors: white rim, cool blue glow, and dark translucent cards so the source image remains the visual hero.
- For Morph slides, preserve the same element order and approximate object identities; only change the spotlight `cx/cy`, clip circle, and sharp image `x/y` pan values.