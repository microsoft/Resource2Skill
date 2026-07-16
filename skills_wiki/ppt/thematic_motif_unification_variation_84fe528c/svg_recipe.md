# SVG Recipe — Fragmented Visual Motif

## Visual mechanism
A single geometric anchor—usually a circle, ring, slash, or branded polygon—is scaled beyond the slide boundary so only fragments remain visible. Repeating the same motif in different crops, opacities, and scales creates deck-wide cohesion while allowing every slide layout to feel varied.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark charcoal background
- 4× large `<circle>` elements for the main off-canvas ring motif, inner cutout, translucent layer, and soft glow
- 3× smaller `<circle>` elements for corner fragments and echo motifs
- 4× `<path>` elements for partial orbital arcs and diagonal brand shards
- 6× `<rect>` elements for text panels, section chips, and subtle content containers
- 12–18× small `<circle>` elements for repeated motif dots / color-variation samples
- 1× `<linearGradient>` for the teal-to-mint motif fill
- 1× `<radialGradient>` for the glow field
- 1× `<filter id="softShadow">` for elevated panels
- 1× `<filter id="motifGlow">` for blurred luminous motif accents
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, labels, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="tealMint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#25E3CF"/>
      <stop offset="55%" stop-color="#2ABAAB"/>
      <stop offset="100%" stop-color="#137A73"/>
    </linearGradient>

    <radialGradient id="tealGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2AE6D0" stop-opacity="0.42"/>
      <stop offset="65%" stop-color="#2ABAAB" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#2ABAAB" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="motifGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <!-- background -->
  <rect x="0" y="0" width="1280" height="720" fill="#0E0F11"/>

  <!-- massive right-edge fragmented motif -->
  <circle cx="1124" cy="346" r="390" fill="url(#tealGlow)" filter="url(#motifGlow)" opacity="0.95"/>
  <circle cx="1124" cy="346" r="314" fill="url(#tealMint)" opacity="0.96"/>
  <circle cx="1124" cy="346" r="216" fill="#0E0F11"/>
  <circle cx="1188" cy="282" r="314" fill="none" stroke="#6EF8E9" stroke-width="2.5" opacity="0.32"/>
  <circle cx="1056" cy="420" r="314" fill="none" stroke="#1C766F" stroke-width="34" opacity="0.24"/>

  <!-- arc fragments reinforce the same circular anchor -->
  <path d="M 830 94 A 366 366 0 0 1 1225 180" fill="none" stroke="#2AE6D0" stroke-width="10" stroke-linecap="round" opacity="0.48"/>
  <path d="M 873 632 A 350 350 0 0 0 1236 505" fill="none" stroke="#2ABAAB" stroke-width="5" stroke-linecap="round" stroke-dasharray="38 18" opacity="0.42"/>
  <path d="M 1015 68 L 1118 24 L 1138 58 L 1037 103 Z" fill="#2AE6D0" opacity="0.72"/>
  <path d="M 976 624 L 1084 582 L 1104 617 L 999 660 Z" fill="#155E59" opacity="0.7"/>

  <!-- top-left crop: small recurring fragment for template continuity -->
  <circle cx="-24" cy="-18" r="104" fill="#2ABAAB" opacity="0.9"/>
  <circle cx="-24" cy="-18" r="64" fill="#0E0F11"/>
  <path d="M 30 88 A 118 118 0 0 0 89 26" fill="none" stroke="#6EF8E9" stroke-width="4" stroke-linecap="round" opacity="0.5"/>

  <!-- left information block -->
  <rect x="82" y="112" width="132" height="34" rx="17" fill="#132A29" stroke="#2ABAAB" stroke-width="1"/>
  <text x="102" y="135" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#69EFE2" letter-spacing="1.4">MOTIF SYSTEM</text>

  <text x="82" y="222" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#FFFFFF">
    Fragmented Visual Anchor
  </text>
  <text x="86" y="284" width="550" font-family="Segoe UI, Microsoft YaHei" font-size="23" fill="#B9BDBF">
    Reuse one bold geometric element across the deck — cropped, layered, repeated, and recolored — so diverse slides feel like one brand world.
  </text>

  <rect x="82" y="356" width="510" height="112" rx="24" fill="#15181B" stroke="#2A2F33" stroke-width="1.2" filter="url(#softShadow)"/>
  <text x="116" y="398" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Rule: keep the source shape identical</text>
  <text x="116" y="430" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#AEB4B7">
    Move it off-canvas, scale it, mirror it, or shift opacity — but do not invent a new decorative language on every slide.
  </text>

  <!-- variation rule tiles -->
  <rect x="82" y="510" width="124" height="74" rx="18" fill="#101315" stroke="#2ABAAB" stroke-width="1" opacity="0.95"/>
  <circle cx="190" cy="547" r="38" fill="#2ABAAB" opacity="0.82"/>
  <text x="104" y="554" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Crop</text>

  <rect x="224" y="510" width="124" height="74" rx="18" fill="#101315" stroke="#273033" stroke-width="1"/>
  <circle cx="269" cy="547" r="28" fill="#2ABAAB" opacity="0.28"/>
  <circle cx="306" cy="547" r="28" fill="#2ABAAB" opacity="0.52"/>
  <text x="246" y="554" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Layer</text>

  <rect x="366" y="510" width="124" height="74" rx="18" fill="#101315" stroke="#273033" stroke-width="1"/>
  <circle cx="410" cy="532" r="8" fill="#1A625D"/>
  <circle cx="437" cy="532" r="8" fill="#1A625D"/>
  <circle cx="464" cy="532" r="8" fill="#2AE6D0"/>
  <circle cx="410" cy="561" r="8" fill="#1A625D"/>
  <circle cx="437" cy="561" r="8" fill="#1A625D"/>
  <circle cx="464" cy="561" r="8" fill="#1A625D"/>
  <text x="388" y="554" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Repeat</text>

  <!-- bottom rhythm line and label -->
  <line x1="82" y1="638" x2="520" y2="638" stroke="#283034" stroke-width="2"/>
  <circle cx="82" cy="638" r="5" fill="#2AE6D0"/>
  <text x="104" y="646" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7D8588">
    Same motif, different crop: ideal for Morph transitions between slides.
  </text>

  <!-- faint lower-right echo fragments -->
  <circle cx="748" cy="664" r="42" fill="#2ABAAB" opacity="0.11"/>
  <circle cx="801" cy="670" r="20" fill="#2ABAAB" opacity="0.18"/>
  <circle cx="854" cy="676" r="10" fill="#2ABAAB" opacity="0.32"/>
</svg>
```

## Avoid in this skill
- ❌ Do not build the motif with `<use>` or `<symbol>` clones; duplicate the actual editable SVG shapes instead.
- ❌ Do not rely on `<mask>` or clip paths on vector shapes to create fragments; push shapes beyond the slide bounds so PowerPoint naturally crops them.
- ❌ Do not change motif families from slide to slide, e.g. circle on one slide, triangle burst on the next, wave on the next. Variation should come from scale, crop, opacity, rotation, or color.
- ❌ Do not overcrowd every corner with fragments; the motif should unify the deck, not compete with the message.
- ❌ Avoid tiny decorative patterns made from hundreds of shapes unless they are intentionally used as a secondary motif sample.

## Composition notes
- Place the largest fragment off one edge, usually right or top, occupying 25–45% of the canvas for strong brand presence.
- Reserve the opposite side for title and content; the motif works best when it counterbalances clean negative space.
- Use one saturated accent color for the motif, then add lower-opacity echoes or outline arcs for variation.
- Across a deck, keep the motif’s geometry consistent but vary its position: right crop, top crop, corner crop, repeated micro-pattern, or translucent layered stack.