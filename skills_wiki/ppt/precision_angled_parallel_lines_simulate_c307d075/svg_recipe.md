# SVG Recipe — Precision Angled Parallel Lines (Simulated Ruler Technique)

## Visual mechanism
A precision drafting scene where a translucent digital ruler is rotated to a fixed angle and multiple “ink” strokes are drawn in the same rotated coordinate system, guaranteeing exact parallel spacing. The visual trick is to draw all lines horizontally in local coordinates, then rotate the entire construction group around a shared center.

## SVG primitives needed
- 1× `<rect>` for the warm drafting-paper background
- 18× `<line>` for a faint measurement grid
- 7× `<line>` for saturated parallel ink strokes
- 1× rotated `<rect>` for the ruler body
- 33× `<line>` for ruler tick marks of alternating lengths
- 6× `<text>` for title, subtitle, ruler numbers, angle badge, and annotation
- 1× `<circle>` for the upright angle indicator badge
- 1× `<path>` for a dashed angle arc around the badge
- 1× `<path>` for a stylized pen nib aligned with the ink lines
- 2× `<linearGradient>` for paper and ruler material
- 1× `<radialGradient>` for the badge highlight
- 1× `<filter id="softShadow">` applied to the ruler, badge, and pen nib

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fffdf8"/>
      <stop offset="100%" stop-color="#f5f0e7"/>
    </linearGradient>

    <linearGradient id="rulerGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.92"/>
      <stop offset="52%" stop-color="#f2f4f6" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#dfe3e7" stop-opacity="0.86"/>
    </linearGradient>

    <radialGradient id="badgeGrad" cx="35%" cy="28%" r="72%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#eef1f4"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="160%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paperGrad)"/>

  <!-- faint drafting grid -->
  <line x1="80" y1="120" x2="1200" y2="120" stroke="#ded8cc" stroke-width="1" opacity="0.45"/>
  <line x1="80" y1="180" x2="1200" y2="180" stroke="#ded8cc" stroke-width="1" opacity="0.45"/>
  <line x1="80" y1="240" x2="1200" y2="240" stroke="#ded8cc" stroke-width="1" opacity="0.45"/>
  <line x1="80" y1="300" x2="1200" y2="300" stroke="#ded8cc" stroke-width="1" opacity="0.45"/>
  <line x1="80" y1="360" x2="1200" y2="360" stroke="#ded8cc" stroke-width="1" opacity="0.45"/>
  <line x1="80" y1="420" x2="1200" y2="420" stroke="#ded8cc" stroke-width="1" opacity="0.45"/>
  <line x1="80" y1="480" x2="1200" y2="480" stroke="#ded8cc" stroke-width="1" opacity="0.45"/>
  <line x1="80" y1="540" x2="1200" y2="540" stroke="#ded8cc" stroke-width="1" opacity="0.45"/>
  <line x1="160" y1="70" x2="160" y2="650" stroke="#ded8cc" stroke-width="1" opacity="0.35"/>
  <line x1="280" y1="70" x2="280" y2="650" stroke="#ded8cc" stroke-width="1" opacity="0.35"/>
  <line x1="400" y1="70" x2="400" y2="650" stroke="#ded8cc" stroke-width="1" opacity="0.35"/>
  <line x1="520" y1="70" x2="520" y2="650" stroke="#ded8cc" stroke-width="1" opacity="0.35"/>
  <line x1="640" y1="70" x2="640" y2="650" stroke="#ded8cc" stroke-width="1" opacity="0.35"/>
  <line x1="760" y1="70" x2="760" y2="650" stroke="#ded8cc" stroke-width="1" opacity="0.35"/>
  <line x1="880" y1="70" x2="880" y2="650" stroke="#ded8cc" stroke-width="1" opacity="0.35"/>
  <line x1="1000" y1="70" x2="1000" y2="650" stroke="#ded8cc" stroke-width="1" opacity="0.35"/>
  <line x1="1120" y1="70" x2="1120" y2="650" stroke="#ded8cc" stroke-width="1" opacity="0.35"/>

  <text x="72" y="72" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1f2933">Precision parallel construction</text>
  <text x="74" y="105" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#65707a">All strokes share one rotated local coordinate system: angle −24°, spacing 42 px.</text>

  <!-- ink strokes: draw horizontal, then rotate the whole group -->
  <g transform="translate(640 372) rotate(-24)">
    <line x1="-545" y1="100" x2="545" y2="100" stroke="#e7352f" stroke-width="5" stroke-linecap="round"/>
    <line x1="-545" y1="142" x2="545" y2="142" stroke="#e7352f" stroke-width="5" stroke-linecap="round"/>
    <line x1="-545" y1="184" x2="545" y2="184" stroke="#e7352f" stroke-width="5" stroke-linecap="round"/>
    <line x1="-545" y1="226" x2="545" y2="226" stroke="#e7352f" stroke-width="5" stroke-linecap="round"/>
    <line x1="-545" y1="268" x2="545" y2="268" stroke="#e7352f" stroke-width="5" stroke-linecap="round"/>
    <line x1="-545" y1="310" x2="545" y2="310" stroke="#e7352f" stroke-width="5" stroke-linecap="round"/>
    <line x1="-545" y1="352" x2="545" y2="352" stroke="#e7352f" stroke-width="5" stroke-linecap="round"/>

    <path d="M 505 180 L 590 164 L 616 184 L 590 204 Z" fill="#242a31" stroke="#0f1720" stroke-width="2" filter="url(#softShadow)"/>
    <path d="M 584 176 L 616 184 L 584 192 Z" fill="#f7c948"/>
  </g>

  <!-- simulated ruler: same rotation as ink lines -->
  <g transform="translate(640 372) rotate(-24)">
    <rect x="-575" y="-62" width="1150" height="124" rx="10" fill="url(#rulerGrad)" stroke="#aeb7bf" stroke-width="2" filter="url(#softShadow)"/>

    <line x1="-540" y1="62" x2="-540" y2="28" stroke="#7b8794" stroke-width="2"/>
    <line x1="-505" y1="62" x2="-505" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-470" y1="62" x2="-470" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-435" y1="62" x2="-435" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-400" y1="62" x2="-400" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-365" y1="62" x2="-365" y2="34" stroke="#7b8794" stroke-width="2"/>
    <line x1="-330" y1="62" x2="-330" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-295" y1="62" x2="-295" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-260" y1="62" x2="-260" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-225" y1="62" x2="-225" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-190" y1="62" x2="-190" y2="28" stroke="#7b8794" stroke-width="2"/>
    <line x1="-155" y1="62" x2="-155" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-120" y1="62" x2="-120" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-85" y1="62" x2="-85" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-50" y1="62" x2="-50" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="-15" y1="62" x2="-15" y2="34" stroke="#7b8794" stroke-width="2"/>
    <line x1="20" y1="62" x2="20" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="55" y1="62" x2="55" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="90" y1="62" x2="90" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="125" y1="62" x2="125" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="160" y1="62" x2="160" y2="28" stroke="#7b8794" stroke-width="2"/>
    <line x1="195" y1="62" x2="195" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="230" y1="62" x2="230" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="265" y1="62" x2="265" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="300" y1="62" x2="300" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="335" y1="62" x2="335" y2="34" stroke="#7b8794" stroke-width="2"/>
    <line x1="370" y1="62" x2="370" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="405" y1="62" x2="405" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="440" y1="62" x2="440" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="475" y1="62" x2="475" y2="44" stroke="#8c98a4" stroke-width="1.5"/>
    <line x1="510" y1="62" x2="510" y2="28" stroke="#7b8794" stroke-width="2"/>

    <text x="-555" y="-16" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#687481">0</text>
    <text x="-205" y="-16" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#687481">10</text>
    <text x="145" y="-16" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#687481">20</text>
    <text x="495" y="-16" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#687481">30</text>
  </g>

  <!-- upright angle badge, independent of ruler rotation -->
  <path d="M 702 372 A 62 62 0 0 1 696 399" fill="none" stroke="#e7352f" stroke-width="3" stroke-dasharray="6 6"/>
  <circle cx="640" cy="372" r="54" fill="url(#badgeGrad)" stroke="#c7d0d9" stroke-width="2" filter="url(#softShadow)"/>
  <text x="594" y="383" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" text-anchor="middle" fill="#1f2933">−24°</text>

  <text x="842" y="590" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#4b5563">Parallelism comes from equal local y-offsets before rotation — not from hand placement.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not draw each angled line by eyeballing separate endpoint coordinates; tiny rounding differences will break the precision effect.
- ❌ Do not use `marker-end` arrowheads on paths for measurement callouts; use plain `<line>` or separate triangle `<path>` shapes instead.
- ❌ Do not apply filters to `<line>` elements; shadows/glows on lines are dropped by the translator.
- ❌ Do not use `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` to fake angle geometry; use `rotate(angle cx cy)` or grouped `translate(...) rotate(...)`.
- ❌ Do not use SVG `<pattern>` fills for graph paper; build the grid from editable `<line>` elements.

## Composition notes
- Anchor the whole construction around a single center point; rotate the ruler and ink-line groups by the same angle so the visual reads as engineered rather than decorative.
- Keep the badge upright and above the rotated elements; it clarifies the angle while creating a premium “instrument overlay” focal point.
- Use strong contrast between the ruler’s pale gray material and the saturated ink strokes; the ruler should feel translucent but still physically present.
- Leave open space in the upper-left for the title and in the lower-right for a concise geometric explanation.