# SVG Recipe — Precision Geometric Patterning & Step-and-Repeat Arrays

## Visual mechanism
A premium technical slide built from perfectly repeated micro-geometry: a subtle dot matrix background, equal-sized foreground primitives, and ruler-like alignment guides. The visual message is “mathematical control” — every object appears cloned, spaced, and formatted with deliberate precision.

## SVG primitives needed
- 1× `<rect>` for the full-slide background.
- 1× `<linearGradient>` for the soft executive-style canvas wash.
- 1× `<filter id="softShadow">` for depth on foreground geometry cards.
- 1× `<filter id="glow">` for a subtle blue emphasis halo behind the main array.
- 40–70× `<circle>` for the step-and-repeat dot field texture.
- 3× large `<rect>` for equal-size content cards.
- 1× `<rect>` for a perfect square primitive.
- 1× `<circle>` for a perfect circular primitive.
- 1× `<path>` for a perfect isosceles triangle primitive.
- 4–6× `<line>` for orthogonal alignment rails, measurement ticks, and equal-spacing guides.
- 4–6× `<text>` with explicit `width` for title, subtitle, labels, and measurement annotations.
- Optional 2–3× `<path>` for decorative technical brackets or corner accents.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="canvasWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="58%" stop-color="#f8fbff"/>
      <stop offset="100%" stop-color="#edf4ff"/>
    </linearGradient>

    <linearGradient id="goldFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffd96a"/>
      <stop offset="52%" stop-color="#ffc000"/>
      <stop offset="100%" stop-color="#e8a600"/>
    </linearGradient>

    <linearGradient id="blueStroke" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2f5fb8"/>
      <stop offset="100%" stop-color="#6d93df"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#canvasWash)"/>

  <circle cx="630" cy="385" r="245" fill="#dbeafe" opacity="0.36" filter="url(#glow)"/>

  <g opacity="0.78">
    <circle cx="60" cy="64" r="4" fill="#dce7f5"/>
    <circle cx="108" cy="64" r="4" fill="#dce7f5"/>
    <circle cx="156" cy="64" r="4" fill="#dce7f5"/>
    <circle cx="204" cy="64" r="4" fill="#dce7f5"/>
    <circle cx="252" cy="64" r="4" fill="#dce7f5"/>
    <circle cx="300" cy="64" r="4" fill="#dce7f5"/>
    <circle cx="348" cy="64" r="4" fill="#dce7f5"/>
    <circle cx="396" cy="64" r="4" fill="#dce7f5"/>

    <circle cx="60" cy="112" r="4" fill="#dce7f5"/>
    <circle cx="108" cy="112" r="4" fill="#dce7f5"/>
    <circle cx="156" cy="112" r="4" fill="#dce7f5"/>
    <circle cx="204" cy="112" r="4" fill="#dce7f5"/>
    <circle cx="252" cy="112" r="4" fill="#dce7f5"/>
    <circle cx="300" cy="112" r="4" fill="#dce7f5"/>
    <circle cx="348" cy="112" r="4" fill="#dce7f5"/>
    <circle cx="396" cy="112" r="4" fill="#dce7f5"/>

    <circle cx="60" cy="160" r="4" fill="#dce7f5"/>
    <circle cx="108" cy="160" r="4" fill="#dce7f5"/>
    <circle cx="156" cy="160" r="4" fill="#dce7f5"/>
    <circle cx="204" cy="160" r="4" fill="#dce7f5"/>
    <circle cx="252" cy="160" r="4" fill="#dce7f5"/>
    <circle cx="300" cy="160" r="4" fill="#dce7f5"/>
    <circle cx="348" cy="160" r="4" fill="#dce7f5"/>
    <circle cx="396" cy="160" r="4" fill="#dce7f5"/>

    <circle cx="60" cy="208" r="4" fill="#dce7f5"/>
    <circle cx="108" cy="208" r="4" fill="#dce7f5"/>
    <circle cx="156" cy="208" r="4" fill="#dce7f5"/>
    <circle cx="204" cy="208" r="4" fill="#dce7f5"/>
    <circle cx="252" cy="208" r="4" fill="#dce7f5"/>
    <circle cx="300" cy="208" r="4" fill="#dce7f5"/>
    <circle cx="348" cy="208" r="4" fill="#dce7f5"/>
    <circle cx="396" cy="208" r="4" fill="#dce7f5"/>
  </g>

  <text x="72" y="94" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#132033" letter-spacing="1.5">
    PRECISION GEOMETRY
  </text>
  <text x="74" y="132" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="500" fill="#5f6f86">
    Step-and-repeat arrays, locked proportions, and format-painted visual systems
  </text>

  <line x1="188" y1="286" x2="1092" y2="286" stroke="#9fb4ce" stroke-width="2" stroke-dasharray="8 10"/>
  <line x1="188" y1="548" x2="1092" y2="548" stroke="#9fb4ce" stroke-width="2" stroke-dasharray="8 10"/>
  <line x1="312" y1="258" x2="312" y2="576" stroke="#c4d3e6" stroke-width="2" stroke-dasharray="5 9"/>
  <line x1="640" y1="258" x2="640" y2="576" stroke="#c4d3e6" stroke-width="2" stroke-dasharray="5 9"/>
  <line x1="968" y1="258" x2="968" y2="576" stroke="#c4d3e6" stroke-width="2" stroke-dasharray="5 9"/>

  <rect x="212" y="314" width="200" height="200" rx="28" fill="#ffffff" stroke="#d6e2f0" stroke-width="2" filter="url(#softShadow)"/>
  <rect x="540" y="314" width="200" height="200" rx="28" fill="#ffffff" stroke="#d6e2f0" stroke-width="2" filter="url(#softShadow)"/>
  <rect x="868" y="314" width="200" height="200" rx="28" fill="#ffffff" stroke="#d6e2f0" stroke-width="2" filter="url(#softShadow)"/>

  <rect x="248" y="350" width="128" height="128" rx="0" fill="url(#goldFill)" stroke="#101827" stroke-width="6"/>
  <circle cx="640" cy="414" r="64" fill="url(#goldFill)" stroke="#101827" stroke-width="6"/>
  <path d="M968 346 L1040 482 L896 482 Z" fill="url(#goldFill)" stroke="#101827" stroke-width="6"/>

  <line x1="412" y1="414" x2="540" y2="414" stroke="url(#blueStroke)" stroke-width="4" stroke-dasharray="10 10"/>
  <line x1="740" y1="414" x2="868" y2="414" stroke="url(#blueStroke)" stroke-width="4" stroke-dasharray="10 10"/>

  <text x="236" y="594" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#223047" text-anchor="middle">
    128 × 128 square
  </text>
  <text x="560" y="594" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#223047" text-anchor="middle">
    r = 64 circle
  </text>
  <text x="888" y="594" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#223047" text-anchor="middle">
    locked triangle
  </text>

  <path d="M92 642 H236 M92 642 V610 M236 642 V610" fill="none" stroke="#315fae" stroke-width="3"/>
  <text x="252" y="648" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#315fae">
    every offset repeats from a fixed origin and spacing constant
  </text>

  <rect x="1038" y="74" width="112" height="112" rx="18" fill="#132033"/>
  <circle cx="1066" cy="102" r="5" fill="#ffc000"/>
  <circle cx="1094" cy="102" r="5" fill="#ffc000"/>
  <circle cx="1122" cy="102" r="5" fill="#ffc000"/>
  <circle cx="1066" cy="130" r="5" fill="#ffc000"/>
  <circle cx="1094" cy="130" r="5" fill="#ffc000"/>
  <circle cx="1122" cy="130" r="5" fill="#ffc000"/>
  <circle cx="1066" cy="158" r="5" fill="#ffc000"/>
  <circle cx="1094" cy="158" r="5" fill="#ffc000"/>
  <circle cx="1122" cy="158" r="5" fill="#ffc000"/>

  <text x="882" y="214" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#607089">
    Visual shorthand for Shift-constrained shapes, Ctrl+D duplication, and copied formatting.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<pattern>` fills for the dot field; manually repeated circles translate more reliably to editable PowerPoint shapes.
- ❌ Slightly different widths/heights for “perfect” primitives; the whole technique depends on locked proportions.
- ❌ Randomized spacing or hand-placed dots; step-and-repeat arrays should use constant x/y offsets.
- ❌ Applying `filter` to `<line>` alignment guides; use flat dashed strokes for guides and reserve shadows/glows for shapes.
- ❌ `marker-end` arrows on paths; if arrows are needed, use simple lines plus separate triangle paths.

## Composition notes
- Keep the dot matrix light and low-contrast so it reads as precision texture, not data noise.
- Place the main geometric array on a strict horizontal rail with equal card sizes and equal gaps.
- Use one copied visual format across all primitives: same fill, same stroke, same shadow behavior.
- Reserve one accent color, such as golden yellow, for the repeated shapes; let blues and slates handle measurement and structure.