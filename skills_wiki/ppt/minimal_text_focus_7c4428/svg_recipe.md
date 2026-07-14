# SVG Recipe — Minimal Text Focus

## Visual mechanism
A sparse, high-contrast slide where one oversized typographic statement dominates the center-left, balanced by a narrow decorative vertical text column and a few precision technical accents. The design feels intentional through restraint: large negative space, subtle gradients, hairline rules, and one vivid accent color.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<radialGradient>` for a soft off-center ambient glow
- 1× `<linearGradient>` for the accent stroke treatment
- 1× `<filter id="softShadow">` for a very subtle text/card shadow
- 1× `<filter id="glow">` for the neon accent dot
- 2× `<path>` for abstract technical contour lines
- 8× `<circle>` for small focus markers / calibration dots
- 5× `<line>` for thin alignment rules and divider accents
- 6× `<text>` blocks for main headline, eyebrow, vertical decorative text, micro labels, and footer annotation
- Multiple nested `<tspan>` elements for controlled line breaks and inline color emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="ambient" cx="42%" cy="46%" r="70%">
      <stop offset="0%" stop-color="#1B355E"/>
      <stop offset="48%" stop-color="#0B1220"/>
      <stop offset="100%" stop-color="#05070D"/>
    </radialGradient>

    <linearGradient id="accentLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6EE7F9" stop-opacity="0"/>
      <stop offset="45%" stop-color="#6EE7F9" stop-opacity="1"/>
      <stop offset="100%" stop-color="#A78BFA" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#ambient)"/>

  <path d="M850 96 C970 68 1090 104 1168 174 C1238 237 1252 335 1190 405 C1115 490 969 473 895 388 C834 318 770 260 705 238"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.055" stroke-width="2"/>
  <path d="M112 562 C230 506 314 508 398 562 C493 623 590 624 690 548 C750 503 818 480 896 492"
        fill="none" stroke="#6EE7F9" stroke-opacity="0.16" stroke-width="2"/>

  <line x1="132" y1="170" x2="132" y2="552" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="176" y1="552" x2="620" y2="552" stroke="url(#accentLine)" stroke-width="2"/>
  <line x1="930" y1="104" x2="1148" y2="104" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="930" y1="616" x2="1148" y2="616" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="1088" y1="152" x2="1088" y2="568" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>

  <circle cx="132" cy="170" r="4" fill="#6EE7F9" filter="url(#glow)"/>
  <circle cx="132" cy="552" r="4" fill="#A78BFA"/>
  <circle cx="176" cy="552" r="3" fill="#FFFFFF" fill-opacity="0.45"/>
  <circle cx="620" cy="552" r="3" fill="#FFFFFF" fill-opacity="0.45"/>
  <circle cx="930" cy="104" r="2.5" fill="#6EE7F9" fill-opacity="0.7"/>
  <circle cx="1148" cy="104" r="2.5" fill="#FFFFFF" fill-opacity="0.35"/>
  <circle cx="930" cy="616" r="2.5" fill="#FFFFFF" fill-opacity="0.35"/>
  <circle cx="1148" cy="616" r="2.5" fill="#A78BFA" fill-opacity="0.7"/>

  <text x="176" y="166" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" letter-spacing="4" fill="#6EE7F9" fill-opacity="0.92">
    SECTION 03 / OPERATING PRINCIPLE
  </text>

  <text x="174" y="300" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="700" line-height="1.02" fill="#F8FAFC" filter="url(#softShadow)">
    <tspan x="174" dy="0">Make the</tspan>
    <tspan x="174" dy="82">message feel</tspan>
    <tspan x="174" dy="82" fill="#6EE7F9">inevitable.</tspan>
  </text>

  <text x="178" y="610" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#CBD5E1" fill-opacity="0.72">
    One focal thought, generous silence, and a calibrated side signal.
  </text>

  <text x="1095" y="540" width="360" transform="rotate(-90 1095 540)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="700"
        letter-spacing="13" fill="#FFFFFF" fill-opacity="0.10">
    MINIMAL TEXT FOCUS
  </text>

  <text x="932" y="142" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" letter-spacing="2.2" fill="#FFFFFF" fill-opacity="0.48">
    TYPOGRAPHIC FIELD
  </text>

  <text x="934" y="606" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#FFFFFF" fill-opacity="0.38">
    1280×720 / negative-space composition
  </text>
</svg>
```

## Avoid in this skill
- ❌ Filling the slide with multiple content boxes; this technique depends on low density and one dominant thought.
- ❌ Using `<textPath>` for the vertical label; rotate a normal `<text>` element instead so it remains editable.
- ❌ Applying `clip-path` to typography or decorative rules; clipping is only reliable for `<image>` elements.
- ❌ Overusing shadows or bright glows; the premium look comes from restraint, not effects-heavy decoration.
- ❌ Omitting `width` on text elements; every `<text>` must declare width for clean PowerPoint rendering.

## Composition notes
- Keep the main headline slightly left of center, occupying roughly 55–65% of slide width and no more than 3 lines.
- Reserve the right 15–20% of the slide for the rotated decorative text column and small calibration labels.
- Use one vivid accent color repeatedly but sparingly: one headline word, one dot, and one thin rule.
- Leave large untouched dark space around the headline so the slide works as a section divider, quote, or keynote pause.