# SVG Recipe — Minimalist Contact Outro

## Visual mechanism
A high-contrast black outro slide centers all attention on one bold brand name and two clean contact actions. Subtle premium details — a soft radial glow, thin frame lines, restrained accent strokes, and pill-shaped contact cards — add polish without distracting from the call-to-action.

## SVG primitives needed
- 1× `<rect>` for the full-slide black background
- 1× `<rect>` with radial gradient fill for the soft central vignette/glow
- 1× `<rect>` for a thin inset frame around the slide
- 2× `<path>` for minimal corner accent strokes
- 1× `<circle>` for a compact logo seal above the company name
- 1× `<path>` for the editable monogram/logo mark
- 5× `<text>` blocks for brand name, descriptor, contact labels, and final CTA
- 1× thin `<rect>` for the central divider rule
- 2× rounded `<rect>` contact pills for phone and website
- 3× `<path>` icon strokes for phone handset and website/globe symbol
- 2× `<line>` elements for globe detail strokes
- 1× `<radialGradient>` for the background light falloff
- 1× `<linearGradient>` for restrained champagne/white accent strokes
- 1× `<filter id="softGlow">` applied to the logo/accent paths
- 1× `<filter id="pillShadow">` applied to the contact pill rectangles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgVignette" cx="50%" cy="45%" r="70%">
      <stop offset="0%" stop-color="#1b1b1b"/>
      <stop offset="48%" stop-color="#070707"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <linearGradient id="champagneStroke" x1="220" y1="90" x2="1060" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.85"/>
      <stop offset="45%" stop-color="#c8b37a" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.25"/>
    </linearGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pillShadow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="0" dy="8" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="14" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgVignette)"/>

  <rect x="112" y="70" width="1056" height="580" rx="30" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.12"/>

  <path d="M162 156 C162 106 198 104 248 104" fill="none" stroke="url(#champagneStroke)" stroke-width="2.5" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M1118 564 C1118 614 1082 616 1032 616" fill="none" stroke="url(#champagneStroke)" stroke-width="2.5" stroke-linecap="round" filter="url(#softGlow)"/>

  <circle cx="640" cy="156" r="34" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.72" filter="url(#softGlow)"/>
  <path d="M625 173 L625 139 L654 173 L654 139" fill="none" stroke="#ffffff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="640" y="266" width="980" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
        font-size="72" font-weight="800" fill="#ffffff">
    NORTHSTAR DIGITAL
  </text>

  <text x="640" y="322" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
        font-size="27" font-weight="600" fill="#ffffff" opacity="0.84">
    <tspan x="640" dy="0">Strategy, search, and growth marketing</tspan>
    <tspan x="640" dy="38">for ambitious local brands</tspan>
  </text>

  <rect x="490" y="398" width="300" height="1.5" rx="0.75" fill="url(#champagneStroke)" opacity="0.72"/>

  <rect x="292" y="445" width="316" height="72" rx="36" fill="#101010" stroke="#ffffff" stroke-width="1" opacity="0.96" filter="url(#pillShadow)"/>
  <path d="M334 470 C341 489 358 498 379 503 C384 504 388 500 391 494 L383 486 C380 489 377 490 374 489 C364 485 356 478 352 468 C351 465 352 462 355 459 L347 451 C341 454 332 462 334 470 Z"
        fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>
  <text x="472" y="491" width="230" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
        font-size="27" font-weight="700" fill="#ffffff">
    (312) 555-0198
  </text>

  <rect x="672" y="445" width="316" height="72" rx="36" fill="#101010" stroke="#ffffff" stroke-width="1" opacity="0.96" filter="url(#pillShadow)"/>
  <circle cx="714" cy="481" r="19" fill="none" stroke="#ffffff" stroke-width="2"/>
  <path d="M701 481 C706 474 722 474 727 481 C722 488 706 488 701 481 Z" fill="none" stroke="#ffffff" stroke-width="1.8"/>
  <line x1="695" y1="481" x2="733" y2="481" stroke="#ffffff" stroke-width="1.6"/>
  <line x1="714" y1="462" x2="714" y2="500" stroke="#ffffff" stroke-width="1.6"/>
  <text x="837" y="491" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
        font-size="27" font-weight="700" fill="#ffffff">
    northstar.co
  </text>

  <text x="640" y="586" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
        font-size="21" font-weight="500" fill="#ffffff" opacity="0.62">
    Book a 15-minute consultation · hello@northstar.co
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<foreignObject>` for HTML-style centered text; PowerPoint translation will fail.
- ❌ Applying `filter` to `<line>` elements; use filtered `<path>` or `<rect>` instead for glow/shadow effects.
- ❌ Relying on a single giant text element without explicit `width`; every `<text>` needs its own `width` for clean PPTX rendering.
- ❌ Overdecorating the outro with charts, dense icons, or multiple columns; the final-slide impact comes from restraint.
- ❌ Using `<mask>` or clipping non-image elements to create fades; use gradients and opacity instead.

## Composition notes
- Keep the main company name centered slightly above the vertical midpoint; the contact actions should sit below it as the next focal layer.
- Preserve wide negative space on all sides so the final slide feels intentional, calm, and premium.
- Use pure white for primary text, softened white for secondary copy, and one restrained warm accent for hierarchy.
- Contact details work best as two centered pills or a stacked pair on narrower layouts; never let them compete with the brand name.