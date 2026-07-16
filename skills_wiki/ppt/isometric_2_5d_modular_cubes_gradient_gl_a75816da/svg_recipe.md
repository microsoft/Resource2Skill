# SVG Recipe — Isometric 2.5D Modular Cubes (Gradient & Glassmorphism)

## Visual mechanism
Build each 2.5D cube from three independent editable SVG paths: top rhombus, left face, and right face. Apply translucent gradients, bright edge strokes, soft ground shadows, and floating labels to make the columns feel like glass modules in an executive data chart.

## SVG primitives needed
- 1× `<rect>` for the dark gradient slide background
- 10× `<line>` for the subtle isometric floor/grid reference
- 5× `<path>` for blurred rhombus ground shadows under each cube
- 15× `<path>` for cube faces: 3 editable planes per cube
- 4× `<line>` for the dotted trend connector between cube tops
- 2× `<rect>` for translucent glass callout panels
- 13× `<text>` for title, subtitle, data values, category labels, and callouts
- 7× `<linearGradient>` / `<radialGradient>` definitions for background, cube-face lighting, strokes, and panels
- 2× `<filter>` definitions: one blurred glow/shadow for ground shadows, one soft card shadow for glass panels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bg" cx="62%" cy="38%" r="78%">
      <stop offset="0%" stop-color="#16385F"/>
      <stop offset="48%" stop-color="#0B1426"/>
      <stop offset="100%" stop-color="#050812"/>
    </radialGradient>

    <linearGradient id="topGlass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.88"/>
      <stop offset="42%" stop-color="#9AF7FF" stop-opacity="0.52"/>
      <stop offset="100%" stop-color="#20D7FF" stop-opacity="0.34"/>
    </linearGradient>

    <linearGradient id="leftGlass" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#36E7FF" stop-opacity="0.64"/>
      <stop offset="100%" stop-color="#087BCE" stop-opacity="0.46"/>
    </linearGradient>

    <linearGradient id="rightGlass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1187D8" stop-opacity="0.44"/>
      <stop offset="100%" stop-color="#071224" stop-opacity="0.76"/>
    </linearGradient>

    <linearGradient id="edgeStroke" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="55%" stop-color="#7AF6FF" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#1DD6FF" stop-opacity="0.36"/>
    </linearGradient>

    <linearGradient id="panelGlass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#45DFFF" stop-opacity="0.06"/>
    </linearGradient>

    <linearGradient id="numberGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#A5F7FF"/>
    </linearGradient>

    <filter id="floorGlow" x="-30%" y="-30%" width="160%" height="180%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <line x1="150" y1="610" x2="1040" y2="610" stroke="#2E5A75" stroke-opacity="0.30" stroke-width="1"/>
  <line x1="210" y1="570" x2="1100" y2="570" stroke="#2E5A75" stroke-opacity="0.20" stroke-width="1"/>
  <line x1="270" y1="530" x2="1160" y2="530" stroke="#2E5A75" stroke-opacity="0.14" stroke-width="1"/>
  <line x1="190" y1="645" x2="580" y2="410" stroke="#2E5A75" stroke-opacity="0.22" stroke-width="1"/>
  <line x1="340" y1="650" x2="730" y2="415" stroke="#2E5A75" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="490" y1="650" x2="880" y2="415" stroke="#2E5A75" stroke-opacity="0.16" stroke-width="1"/>
  <line x1="640" y1="650" x2="1030" y2="415" stroke="#2E5A75" stroke-opacity="0.14" stroke-width="1"/>
  <line x1="1020" y1="645" x2="630" y2="410" stroke="#2E5A75" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="870" y1="650" x2="480" y2="415" stroke="#2E5A75" stroke-opacity="0.16" stroke-width="1"/>
  <line x1="720" y1="650" x2="330" y2="415" stroke="#2E5A75" stroke-opacity="0.14" stroke-width="1"/>

  <rect x="74" y="70" width="424" height="116" rx="28" fill="url(#panelGlass)" stroke="#B8F9FF" stroke-opacity="0.22" filter="url(#cardShadow)"/>
  <text x="104" y="116" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">Modular Growth Stack</text>
  <text x="106" y="154" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#BDEFFF" opacity="0.82">Editable SVG paths: top, left and right faces per cube</text>

  <rect x="930" y="82" width="250" height="86" rx="24" fill="url(#panelGlass)" stroke="#B8F9FF" stroke-opacity="0.20"/>
  <text x="960" y="118" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#9BEFFF" opacity="0.85">Glassmorphism cue</text>
  <text x="960" y="148" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">transparent planes</text>

  <path d="M225 610 L305 570 L385 610 L305 650 Z" fill="#00D8FF" opacity="0.16" filter="url(#floorGlow)"/>
  <path d="M360 610 L440 570 L520 610 L440 650 Z" fill="#00D8FF" opacity="0.18" filter="url(#floorGlow)"/>
  <path d="M495 610 L575 570 L655 610 L575 650 Z" fill="#00D8FF" opacity="0.20" filter="url(#floorGlow)"/>
  <path d="M630 610 L710 570 L790 610 L710 650 Z" fill="#00D8FF" opacity="0.22" filter="url(#floorGlow)"/>
  <path d="M765 610 L845 570 L925 610 L845 650 Z" fill="#00D8FF" opacity="0.25" filter="url(#floorGlow)"/>

  <line x1="305" y1="440" x2="440" y2="387" stroke="#9DF8FF" stroke-width="2" stroke-dasharray="7 9" opacity="0.55"/>
  <line x1="440" y1="387" x2="575" y2="327" stroke="#9DF8FF" stroke-width="2" stroke-dasharray="7 9" opacity="0.55"/>
  <line x1="575" y1="327" x2="710" y2="267" stroke="#9DF8FF" stroke-width="2" stroke-dasharray="7 9" opacity="0.55"/>
  <line x1="710" y1="267" x2="845" y2="192" stroke="#9DF8FF" stroke-width="2" stroke-dasharray="7 9" opacity="0.55"/>

  <path d="M247 474 L305 508 L305 590 L247 556 Z" fill="url(#leftGlass)" stroke="url(#edgeStroke)" stroke-width="1.3"/>
  <path d="M363 474 L305 508 L305 590 L363 556 Z" fill="url(#rightGlass)" stroke="url(#edgeStroke)" stroke-width="1.1"/>
  <path d="M247 474 L305 440 L363 474 L305 508 Z" fill="url(#topGlass)" stroke="url(#edgeStroke)" stroke-width="1.6"/>

  <path d="M382 421 L440 455 L440 590 L382 556 Z" fill="url(#leftGlass)" stroke="url(#edgeStroke)" stroke-width="1.3"/>
  <path d="M498 421 L440 455 L440 590 L498 556 Z" fill="url(#rightGlass)" stroke="url(#edgeStroke)" stroke-width="1.1"/>
  <path d="M382 421 L440 387 L498 421 L440 455 Z" fill="url(#topGlass)" stroke="url(#edgeStroke)" stroke-width="1.6"/>

  <path d="M517 361 L575 395 L575 590 L517 556 Z" fill="url(#leftGlass)" stroke="url(#edgeStroke)" stroke-width="1.3"/>
  <path d="M633 361 L575 395 L575 590 L633 556 Z" fill="url(#rightGlass)" stroke="url(#edgeStroke)" stroke-width="1.1"/>
  <path d="M517 361 L575 327 L633 361 L575 395 Z" fill="url(#topGlass)" stroke="url(#edgeStroke)" stroke-width="1.6"/>

  <path d="M652 301 L710 335 L710 590 L652 556 Z" fill="url(#leftGlass)" stroke="url(#edgeStroke)" stroke-width="1.3"/>
  <path d="M768 301 L710 335 L710 590 L768 556 Z" fill="url(#rightGlass)" stroke="url(#edgeStroke)" stroke-width="1.1"/>
  <path d="M652 301 L710 267 L768 301 L710 335 Z" fill="url(#topGlass)" stroke="url(#edgeStroke)" stroke-width="1.6"/>

  <path d="M787 226 L845 260 L845 590 L787 556 Z" fill="url(#leftGlass)" stroke="url(#edgeStroke)" stroke-width="1.3"/>
  <path d="M903 226 L845 260 L845 590 L903 556 Z" fill="url(#rightGlass)" stroke="url(#edgeStroke)" stroke-width="1.1"/>
  <path d="M787 226 L845 192 L903 226 L845 260 Z" fill="url(#topGlass)" stroke="url(#edgeStroke)" stroke-width="1.6"/>

  <text x="245" y="414" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="url(#numberGlow)">24</text>
  <text x="380" y="361" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="url(#numberGlow)">38</text>
  <text x="515" y="301" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="url(#numberGlow)">56</text>
  <text x="650" y="241" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="url(#numberGlow)">71</text>
  <text x="785" y="166" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="url(#numberGlow)">92</text>

  <text x="245" y="666" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#9FCBE0">Q1</text>
  <text x="380" y="666" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#9FCBE0">Q2</text>
  <text x="515" y="666" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#9FCBE0">Q3</text>
  <text x="650" y="666" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#9FCBE0">Q4</text>
  <text x="785" y="666" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#9FCBE0">Q5</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<polygon>` for cube faces if maximum PowerPoint editability is required; use explicit `<path d="...">` planes instead.
- ❌ Do not build the cube as one merged path or bitmap; each face must remain separate so gradients, alpha, and strokes can be edited independently.
- ❌ Do not rely on `transform="skewX(...)"`, `matrix(...)`, or native 3D rotation; calculate the isometric vertices directly.
- ❌ Do not apply filters to `<line>` grid or connector elements; filters on lines are dropped by the translator.
- ❌ Do not omit `width` on `<text>` labels; PowerPoint needs explicit text widths for stable rendering.

## Composition notes
- Keep the tallest cube on the right third and let the sequence climb left-to-right to communicate growth instantly.
- Use dark negative space behind the cubes; glassmorphism needs contrast for transparent faces and glowing edges to read clearly.
- Draw shadows first, then side faces, then top faces, then labels so the top rhombus feels like the lit surface.
- Use consistent cube width/depth while scaling only vertical height for data integrity.