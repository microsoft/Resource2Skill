# SVG Recipe — Isometric Stacked Layers Infographic

## Visual mechanism
Build each “3D” layer from three editable vector faces: a bright top diamond plus two darker side parallelograms. Stack the blocks on a shared isometric axis, add soft grounding shadow and angled index text to make a flat SVG read as a premium layered architecture diagram.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background.
- 1× `<path>` for the soft cast shadow under the stack, with blur filter.
- 15× `<path>` for five isometric layer blocks: top, left face, and right face per layer.
- 5× `<text>` rotated to the isometric angle for layer index numbers on the left faces.
- 5× `<line>` for thin connector rules from stack layers to explanatory labels.
- 5× `<circle>` for connector anchor dots / callout bullets.
- 12× `<text>` for title, subtitle, layer names, and descriptions.
- 1× `<filter id="blurShadow">` using `feGaussianBlur` for the ground shadow.
- Multiple `<linearGradient>` fills for background and subtly lit top faces.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8fbff"/>
      <stop offset="100%" stop-color="#eef3f8"/>
    </linearGradient>

    <linearGradient id="topRed" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff6b7a"/>
      <stop offset="100%" stop-color="#e63946"/>
    </linearGradient>
    <linearGradient id="topOrange" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffc28d"/>
      <stop offset="100%" stop-color="#f4a261"/>
    </linearGradient>
    <linearGradient id="topYellow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffe18a"/>
      <stop offset="100%" stop-color="#e9c46a"/>
    </linearGradient>
    <linearGradient id="topGreen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#49d0c1"/>
      <stop offset="100%" stop-color="#2a9d8f"/>
    </linearGradient>
    <linearGradient id="topBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#23b8e9"/>
      <stop offset="100%" stop-color="#0096c7"/>
    </linearGradient>

    <filter id="blurShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <text x="72" y="72" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1f2937">Layered Architecture Framework</text>
  <text x="74" y="108" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#64748b">Editable isometric blocks for technology stacks, maturity models, and multi-stage operating systems.</text>

  <path d="M420 570 L570 645 L420 720 L270 645 Z" fill="#0f172a" opacity="0.14" filter="url(#blurShadow)"/>

  <!-- Bottom layer: Infrastructure -->
  <path d="M270 449 L420 524 L420 558 L270 483 Z" fill="#006f94"/>
  <path d="M570 449 L420 524 L420 558 L570 483 Z" fill="#005a78"/>
  <path d="M420 374 L570 449 L420 524 L270 449 Z" fill="url(#topBlue)"/>
  <text x="316" y="472" width="80" transform="rotate(26.565 316 472)" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#ffffff" opacity="0.92">01</text>

  <!-- Layer 4: Data platform -->
  <path d="M270 389 L420 464 L420 498 L270 423 Z" fill="#237f75"/>
  <path d="M570 389 L420 464 L420 498 L570 423 Z" fill="#1b665e"/>
  <path d="M420 314 L570 389 L420 464 L270 389 Z" fill="url(#topGreen)"/>
  <text x="316" y="412" width="80" transform="rotate(26.565 316 412)" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#ffffff" opacity="0.92">02</text>

  <!-- Layer 3: Services -->
  <path d="M270 329 L420 404 L420 438 L270 363 Z" fill="#c8a755"/>
  <path d="M570 329 L420 404 L420 438 L570 363 Z" fill="#a98b43"/>
  <path d="M420 254 L570 329 L420 404 L270 329 Z" fill="url(#topYellow)"/>
  <text x="316" y="352" width="80" transform="rotate(26.565 316 352)" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#ffffff" opacity="0.92">03</text>

  <!-- Layer 2: Experience APIs -->
  <path d="M270 269 L420 344 L420 378 L270 303 Z" fill="#cf8952"/>
  <path d="M570 269 L420 344 L420 378 L570 303 Z" fill="#aa7043"/>
  <path d="M420 194 L570 269 L420 344 L270 269 Z" fill="url(#topOrange)"/>
  <text x="316" y="292" width="80" transform="rotate(26.565 316 292)" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#ffffff" opacity="0.92">04</text>

  <!-- Top layer: Product interface -->
  <path d="M270 209 L420 284 L420 318 L270 243 Z" fill="#c4313c"/>
  <path d="M570 209 L420 284 L420 318 L570 243 Z" fill="#9f2731"/>
  <path d="M420 134 L570 209 L420 284 L270 209 Z" fill="url(#topRed)"/>
  <text x="316" y="232" width="80" transform="rotate(26.565 316 232)" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#ffffff" opacity="0.92">05</text>

  <!-- Connector callouts -->
  <line x1="590" y1="230" x2="725" y2="180" stroke="#cbd5e1" stroke-width="2"/>
  <circle cx="590" cy="230" r="5" fill="#e63946"/>
  <text x="750" y="170" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1f2937">Product Interface</text>
  <text x="750" y="196" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748b">Web, mobile, dashboards, and workflow surfaces.</text>

  <line x1="595" y1="292" x2="725" y2="270" stroke="#cbd5e1" stroke-width="2"/>
  <circle cx="595" cy="292" r="5" fill="#f4a261"/>
  <text x="750" y="260" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1f2937">Experience APIs</text>
  <text x="750" y="286" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748b">Composable endpoints tailored to user journeys.</text>

  <line x1="600" y1="354" x2="725" y2="360" stroke="#cbd5e1" stroke-width="2"/>
  <circle cx="600" cy="354" r="5" fill="#e9c46a"/>
  <text x="750" y="350" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1f2937">Core Services</text>
  <text x="750" y="376" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748b">Business logic, orchestration, and domain modules.</text>

  <line x1="595" y1="416" x2="725" y2="450" stroke="#cbd5e1" stroke-width="2"/>
  <circle cx="595" cy="416" r="5" fill="#2a9d8f"/>
  <text x="750" y="440" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1f2937">Data Platform</text>
  <text x="750" y="466" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748b">Streaming, lakehouse, governance, and analytics layer.</text>

  <line x1="590" y1="478" x2="725" y2="540" stroke="#cbd5e1" stroke-width="2"/>
  <circle cx="590" cy="478" r="5" fill="#0096c7"/>
  <text x="750" y="530" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1f2937">Cloud Infrastructure</text>
  <text x="750" y="556" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748b">Compute, network, observability, and security foundation.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<polygon>` for layer faces; use `<path d="...">` so the faces translate consistently as editable PowerPoint freeform shapes.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to fake isometric perspective; calculate the diamond and parallelogram vertices directly.
- ❌ Do not place arrowheads with `marker-end` on connector paths; use plain `<line>` elements plus small `<circle>` endpoints.
- ❌ Do not apply blur or shadow filters to connector `<line>` elements; keep filters on the ground-shadow `<path>` or block face paths only.
- ❌ Do not clip or mask vector block faces; clipping should only be used on `<image>` elements if a photo-textured layer is intentionally added.

## Composition notes
- Keep the isometric stack slightly left of center, leaving the right half for readable callouts and executive-level explanations.
- Render lower layers first and upper layers last so the stack overlaps naturally and preserves the illusion of depth.
- Use a consistent lighting rule: top face brightest, left face medium-dark, right face darkest.
- Reserve generous negative space above the stack for the title; the diagram itself should occupy roughly 60–65% of slide height.