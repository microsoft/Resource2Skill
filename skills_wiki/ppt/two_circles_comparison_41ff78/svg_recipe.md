# SVG Recipe — Two Circles Comparison

## Visual mechanism
Two separate circles act as oversized comparison containers, with deliberate scale difference communicating asymmetry in weight, priority, or maturity. Premium treatment comes from soft radial gradients, translucent orbit rings, and spacious typography rather than overlap or complex diagrams.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<rect>` for a subtle glass-like presentation panel
- 2× large filled `<circle>` elements for the primary comparison bubbles
- 4× stroked `<circle>` elements for halos, orbit rings, and scale emphasis
- 3× decorative `<path>` elements for abstract background blobs and visual energy
- 1× `<line>` for the quiet comparison divider between concepts
- 8× `<text>` elements for eyebrow label, title, circle labels, numbers, and supporting descriptions
- 3× `<radialGradient>` fills for luminous bubble depth and background atmosphere
- 2× `<linearGradient>` fills for background and panel sheen
- 2× `<filter>` definitions using blur / offset / merge for editable glow and shadow effects

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#101827"/>
      <stop offset="52%" stop-color="#17233A"/>
      <stop offset="100%" stop-color="#0A1020"/>
    </linearGradient>

    <linearGradient id="panelGrad" x1="150" y1="120" x2="1130" y2="650">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.13"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.045"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>

    <radialGradient id="leftCircleGrad" cx="36%" cy="28%" r="72%">
      <stop offset="0%" stop-color="#B8F3FF"/>
      <stop offset="38%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#075985"/>
    </radialGradient>

    <radialGradient id="rightCircleGrad" cx="34%" cy="26%" r="76%">
      <stop offset="0%" stop-color="#FFF0B3"/>
      <stop offset="42%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#92400E"/>
    </radialGradient>

    <radialGradient id="ambientBlob" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#7C3AED" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="20" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="auraGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-40,115 C120,30 260,95 285,225 C315,382 115,425 20,330 C-65,245 -170,190 -40,115 Z"
        fill="url(#ambientBlob)" filter="url(#auraGlow)"/>
  <path d="M1018,40 C1150,-20 1298,78 1325,210 C1356,360 1195,424 1070,352 C946,281 900,118 1018,40 Z"
        fill="#0EA5E9" opacity="0.15" filter="url(#auraGlow)"/>
  <path d="M930,620 C1035,545 1160,552 1222,636 C1287,724 1138,786 1018,756 C895,726 830,692 930,620 Z"
        fill="#F59E0B" opacity="0.16" filter="url(#auraGlow)"/>

  <rect x="88" y="86" width="1104" height="560" rx="38"
        fill="url(#panelGrad)" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.4"/>

  <text x="112" y="142" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.2" fill="#93C5FD">
    COMPARISON FRAME
  </text>
  <text x="112" y="188" width="630" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="700" fill="#F8FAFC">
    Two models, different weight
  </text>
  <text x="114" y="222" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#CBD5E1">
    Use scale, color, and interior copy to contrast two concepts without implying overlap.
  </text>

  <line x1="640" y1="276" x2="640" y2="560"
        stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.3" stroke-dasharray="7 10"/>

  <circle cx="384" cy="392" r="226" fill="#38BDF8" opacity="0.12" filter="url(#auraGlow)"/>
  <circle cx="384" cy="392" r="206" fill="none" stroke="#7DD3FC" stroke-opacity="0.34" stroke-width="1.6"/>
  <circle cx="384" cy="392" r="184" fill="url(#leftCircleGrad)" filter="url(#softShadow)"/>
  <circle cx="316" cy="316" r="42" fill="#FFFFFF" opacity="0.22"/>
  <circle cx="384" cy="392" r="150" fill="none" stroke="#FFFFFF" stroke-opacity="0.26" stroke-width="1.2" stroke-dasharray="4 12"/>

  <text x="264" y="350" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700"
        letter-spacing="1.4" fill="#E0F2FE">
    ESTABLISHED
  </text>
  <text x="244" y="415" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="56" font-weight="800"
        fill="#FFFFFF">
    CORE
  </text>
  <text x="258" y="462" width="252" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#DFF7FF">
    Larger circle for scale, certainty, or current business gravity
  </text>

  <circle cx="872" cy="400" r="172" fill="#F59E0B" opacity="0.14" filter="url(#auraGlow)"/>
  <circle cx="872" cy="400" r="151" fill="none" stroke="#FCD34D" stroke-opacity="0.34" stroke-width="1.5"/>
  <circle cx="872" cy="400" r="132" fill="url(#rightCircleGrad)" filter="url(#softShadow)"/>
  <circle cx="824" cy="346" r="31" fill="#FFFFFF" opacity="0.22"/>
  <circle cx="872" cy="400" r="106" fill="none" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="1.1" stroke-dasharray="4 11"/>

  <text x="762" y="372" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700"
        letter-spacing="1.2" fill="#FEF3C7">
    EMERGING
  </text>
  <text x="756" y="423" width="232" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="43" font-weight="800"
        fill="#FFFFFF">
    BET
  </text>
  <text x="772" y="462" width="200" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#FFF7D6">
    Smaller circle for focus, optionality, or future upside
  </text>

  <text x="466" y="604" width="350" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="600"
        fill="#E2E8F0">
    Size difference communicates relative magnitude — not hierarchy alone.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Overlapping the circles; this turns the layout into a Venn diagram and changes the meaning.
- ❌ Making both circles the same size unless the comparison is intentionally equal-weight.
- ❌ Dense bullet lists inside the circles; the technique works best with short labels, one metric, or a brief phrase.
- ❌ Using hard black outlines; soft halos and low-opacity rings preserve the playful, premium feel.
- ❌ Applying `clip-path` to circles or text for decorative effects; clipping should only be used on `<image>` elements if extending this shell with photos.

## Composition notes
- Keep the larger circle left or lower-left and the smaller circle right or upper-right for natural asymmetry and visual motion.
- Reserve the top-left 20–30% of the slide for title and context; the circles should carry the main comparison.
- Use one cool and one warm color family so the two concepts are instantly distinguishable.
- Maintain generous negative space around each circle; halos need breathing room to feel intentional rather than crowded.