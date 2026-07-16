# SVG Recipe — Interactive Morphing Infographic with Circular Menu

## Visual mechanism
A full-slide glowing infographic uses a saturated morph-ready gradient background, translucent glass panels, a central line-art illustration, and a persistent circular menu in the upper-left. Duplicate the slide into multiple states, change the background/illustration/menu highlight/card content, then apply PowerPoint Morph and hyperlinks to create an app-like interactive navigation experience.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background.
- 3× `<circle>` / `<ellipse>` for soft ambient color glows and the central glass halo.
- 1× `<rect>` for the glass title capsule.
- 4× `<rect>` for translucent information cards.
- 4× `<circle>` for numbered/card icon badges.
- 4× `<path>` for curved connector strokes from the central illustration to the cards.
- 8× `<path>` for circular menu wedges, active wedge highlight, divider arcs, and small menu icons.
- 5× `<circle>` for the circular menu base, inner button, active dot, and mini control buttons.
- 10× `<path>` for the central morphable line-art illustration and decorative energy strokes.
- 9× `<text>` blocks with explicit `width` attributes for title, menu labels, card headings, and body copy.
- 2× `<linearGradient>` for the background and glass fills.
- 2× `<radialGradient>` for ambient glow and active menu highlight.
- 2× `<filter>` definitions: one soft shadow for glass panels and one glow for active UI/illustration elements.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07F49E"/>
      <stop offset="48%" stop-color="#1A3FD9"/>
      <stop offset="86%" stop-color="#42047E"/>
    </linearGradient>
    <linearGradient id="glassFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.26"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.16"/>
    </linearGradient>
    <radialGradient id="auraGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="45%" stop-color="#5EFCE8" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="activeGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFF6B8" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="#FF7AE6" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="whiteGlow" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>
  <circle cx="1030" cy="145" r="230" fill="url(#auraGlow)"/>
  <circle cx="290" cy="620" r="260" fill="#FF7AE6" opacity="0.15"/>
  <ellipse cx="670" cy="380" rx="250" ry="210" fill="url(#auraGlow)" opacity="0.75"/>

  <rect x="406" y="42" width="468" height="78" rx="39" fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.8" stroke-width="1.2" filter="url(#softShadow)"/>
  <text x="406" y="92" width="468" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF" letter-spacing="2">IDEA OPERATING SYSTEM</text>

  <circle cx="132" cy="124" r="84" fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.76" stroke-width="1.2" filter="url(#softShadow)"/>
  <path d="M132 40 A84 84 0 0 1 216 124 L166 124 A34 34 0 0 0 132 90 Z" fill="url(#activeGlow)" stroke="#FFFFFF" stroke-width="1.4" filter="url(#whiteGlow)"/>
  <path d="M216 124 A84 84 0 0 1 132 208 L132 158 A34 34 0 0 0 166 124 Z" fill="#FFFFFF" opacity="0.10" stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="1"/>
  <path d="M132 208 A84 84 0 0 1 48 124 L98 124 A34 34 0 0 0 132 158 Z" fill="#FFFFFF" opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="1"/>
  <path d="M48 124 A84 84 0 0 1 132 40 L132 90 A34 34 0 0 0 98 124 Z" fill="#FFFFFF" opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="1"/>
  <circle cx="132" cy="124" r="33" fill="#FFFFFF" opacity="0.16" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="1.2"/>
  <path d="M119 116 L132 103 L145 116 M119 132 L132 145 L145 132" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="132" cy="62" r="5" fill="#FFF6B8"/>
  <text x="42" y="234" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF" opacity="0.9">clickable circular menu</text>

  <rect x="106" y="238" width="286" height="126" rx="30" fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.72" stroke-width="1.1" filter="url(#softShadow)"/>
  <circle cx="148" cy="282" r="22" fill="#FFFFFF" opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.78"/>
  <text x="138" y="290" width="20" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">1</text>
  <text x="180" y="278" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">Sense</text>
  <text x="180" y="308" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.82">Gather signals from customers, teams, and market shifts.</text>

  <rect x="96" y="500" width="306" height="126" rx="30" fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.72" stroke-width="1.1" filter="url(#softShadow)"/>
  <circle cx="142" cy="544" r="22" fill="#FFFFFF" opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.78"/>
  <text x="132" y="552" width="20" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">2</text>
  <text x="176" y="540" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">Prioritize</text>
  <text x="176" y="570" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.82">Rank opportunities by impact, risk, speed, and confidence.</text>

  <rect x="878" y="238" width="302" height="126" rx="30" fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.72" stroke-width="1.1" filter="url(#softShadow)"/>
  <circle cx="922" cy="282" r="22" fill="#FFFFFF" opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.78"/>
  <text x="912" y="290" width="20" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">3</text>
  <text x="956" y="278" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">Prototype</text>
  <text x="956" y="308" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.82">Turn the selected path into a visible, testable experience.</text>

  <rect x="888" y="500" width="292" height="126" rx="30" fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.72" stroke-width="1.1" filter="url(#softShadow)"/>
  <circle cx="932" cy="544" r="22" fill="#FFFFFF" opacity="0.17" stroke="#FFFFFF" stroke-opacity="0.78"/>
  <text x="922" y="552" width="20" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">4</text>
  <text x="966" y="540" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">Scale</text>
  <text x="966" y="570" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.82">Launch repeatable systems, playbooks, and feedback loops.</text>

  <path d="M520 340 C430 300 402 300 392 300" fill="none" stroke="#FFFFFF" stroke-opacity="0.48" stroke-width="1.4" stroke-dasharray="7 8"/>
  <path d="M520 456 C430 522 414 548 402 562" fill="none" stroke="#FFFFFF" stroke-opacity="0.48" stroke-width="1.4" stroke-dasharray="7 8"/>
  <path d="M760 340 C840 300 858 300 878 300" fill="none" stroke="#FFFFFF" stroke-opacity="0.48" stroke-width="1.4" stroke-dasharray="7 8"/>
  <path d="M760 456 C850 522 870 548 888 562" fill="none" stroke="#FFFFFF" stroke-opacity="0.48" stroke-width="1.4" stroke-dasharray="7 8"/>

  <circle cx="640" cy="402" r="142" fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.68" stroke-width="1.3" filter="url(#softShadow)"/>
  <circle cx="640" cy="402" r="100" fill="none" stroke="#FFFFFF" stroke-opacity="0.26" stroke-width="18"/>
  <path d="M604 395 C604 357 630 334 660 337 C695 341 717 371 704 405 C697 424 681 434 678 459 L618 459 C615 433 604 422 604 395 Z" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" filter="url(#whiteGlow)"/>
  <path d="M620 480 L676 480 M626 500 L670 500 M638 520 L658 520" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
  <path d="M640 306 L640 274 M700 326 L722 302 M580 326 L558 302 M737 392 L770 392 M510 392 L543 392" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.88"/>
  <path d="M585 408 C615 386 660 386 695 414" fill="none" stroke="#5EFCE8" stroke-width="3" stroke-linecap="round" opacity="0.9"/>
  <path d="M568 448 C612 486 674 487 714 449" fill="none" stroke="#FFF6B8" stroke-width="3" stroke-linecap="round" opacity="0.72"/>
  <text x="520" y="598" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#FFFFFF" opacity="0.86">morph this illustration between states</text>
</svg>
```

## Avoid in this skill
- ❌ Real SVG animation tags such as `<animate>` or `<animateTransform>`; create the interaction by duplicating slides and using PowerPoint Morph instead.
- ❌ `<mask>` for glassmorphism; use translucent fills, gradients, strokes, and glow/shadow filters instead.
- ❌ Applying `filter` to connector `<line>` elements; use unfiltered `<path>` connectors or apply filters only to shapes.
- ❌ `marker-end` arrowheads on paths; if arrows are required, draw them manually with short `<line>` segments or small `<path>` chevrons.
- ❌ `<use>` / `<symbol>` icon reuse for the menu; duplicate the simple paths directly so the translator keeps every element editable.

## Composition notes
- Keep the circular menu in the upper-left 200×220 px zone so it reads as persistent navigation rather than slide content.
- Reserve the center 360×360 px for the morphable hero illustration; name equivalent PowerPoint objects consistently across duplicated slides, e.g. `!!main_illustration`.
- Place glass information cards symmetrically around the hero with generous negative space; connectors should be faint and secondary.
- Change only a few attributes per state—background gradient, active menu wedge, central illustration, and card text—so the Morph transition feels fluid instead of chaotic.