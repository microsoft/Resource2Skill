# SVG Recipe — Minimal Statement

## Visual mechanism
A single oversized bold statement sits centered vertically on a saturated accent field, with only ultra-subtle tonal geometry and hairline framing to make the emptiness feel intentional. The slide’s power comes from scale, contrast, and restraint rather than supporting content.

## SVG primitives needed
- 1× `<rect>` for the full-slide solid accent background
- 1× `<radialGradient>` for a barely visible center glow behind the statement
- 1× `<linearGradient>` for tonal decorative shapes in the same color family
- 3× `<path>` for abstract low-opacity background forms that add premium depth without competing with the text
- 2× `<line>` for thin horizontal framing rules around the statement block
- 1× `<filter id="softShadow">` with offset/blur/merge for subtle text lift
- 1× `<text>` with nested `<tspan>` lines for the centered bold statement
- 1× small decorative `<circle>` accent dot to create a deliberate editorial detail

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="centerGlow" cx="50%" cy="48%" r="58%">
      <stop offset="0%" stop-color="#315CFF" stop-opacity="0.28"/>
      <stop offset="45%" stop-color="#173A9A" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#081A33" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="tonalShape" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#6CA4FF" stop-opacity="0.03"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="7" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#081A33"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>

  <path d="M-90,86 C95,22 234,62 332,160 C430,258 510,258 648,198 C784,138 922,111 1046,186 C1170,261 1244,395 1374,382 L1374,-60 L-90,-60 Z"
        fill="url(#tonalShape)" opacity="0.42"/>

  <path d="M944,682 C846,603 825,489 892,410 C959,331 1088,323 1180,389 C1272,455 1327,563 1360,736 L944,736 Z"
        fill="#FFFFFF" opacity="0.055"/>

  <path d="M-68,602 C52,534 156,539 239,620 C322,701 418,728 536,697 C654,666 742,672 829,734 L-68,734 Z"
        fill="#5E8DFF" opacity="0.055"/>

  <line x1="270" y1="246" x2="1010" y2="246"
        stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1.4"/>

  <circle cx="640" cy="246" r="4.5" fill="#FFCD4B"/>

  <text x="640" y="315"
        width="920"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76"
        font-weight="800"
        letter-spacing="-2"
        fill="#FFFFFF"
        filter="url(#softShadow)">
    <tspan x="640" dy="0">Clarity is the</tspan>
    <tspan x="640" dy="88">ultimate advantage.</tspan>
  </text>

  <line x1="270" y1="493" x2="1010" y2="493"
        stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1.4"/>

  <path d="M1050,140 C1070,125 1098,130 1110,154 C1122,178 1108,205 1082,211 C1056,217 1032,200 1029,174 C1027,160 1036,149 1050,140 Z"
        fill="#FFCD4B" opacity="0.18"/>

  <path d="M171,148 C194,134 224,145 229,173 C234,201 213,224 185,221 C157,218 140,193 149,168 C153,159 161,153 171,148 Z"
        fill="#FFFFFF" opacity="0.09"/>
</svg>
```

## Avoid in this skill
- ❌ Adding cards, icons, charts, or supporting paragraphs; the layout should remain a single-statement moment.
- ❌ Using a busy photographic background unless heavily simplified; it weakens the minimal billboard effect.
- ❌ Centering the text mathematically but ignoring optical balance; two-line statements usually need slightly more space below than above.
- ❌ Applying filters to `<line>` elements; keep framing rules plain.
- ❌ Omitting `width` on `<text>`; PowerPoint translation depends on explicit text width.

## Composition notes
- Keep the statement block centered vertically, occupying roughly the middle 40% of the slide height.
- Use a strong accent field with white or near-white typography; contrast is the main design asset.
- Decorative forms should stay tonal and low-opacity, mostly pushed to corners and edges.
- Limit the palette to one accent color family plus one small highlight color for a premium keynote feel.