# SVG Recipe — Kinetic Block Typography & Dynamic Geometric Overlay

## Visual mechanism
A black poster-like slide is packed with oversized block typography, rotated words, punched-up primary colors, and motion cues such as dashed rings, circular micro-type, filmstrip perforations, and slanted accent shards. The composition should feel like a frozen frame from a kinetic typography animation: loud, layered, slightly chaotic, but still readable.

## SVG primitives needed
- 1× `<rect>` for the pitch-black full-slide background.
- 2× `<linearGradient>` for electric blue typography and colored block fills.
- 1× `<filter id="hardShadow">` using `feOffset + feGaussianBlur + feMerge` for chunky poster shadows on big type and blocks.
- 1× `<filter id="softGlow">` using `feGaussianBlur` for neon-style accent glow.
- 2× `<circle>` for dashed kinetic rings and circular focal marks.
- 10–18× small `<rect>` for filmstrip perforations along the edges.
- 5–8× colored `<rect>` letter tiles for the ransom-note keyword blocks.
- 6–10× `<text>` for massive headline words, vertical structural words, individual tile letters, and circular micro-labels.
- 3–6× `<path>` for jagged lightning shards, motion wedges, and underline slashes.
- Optional `<line>` elements for straight motion ticks or arrow-like streaks, without marker-end.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="electricBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1ed6ff"/>
      <stop offset="65%" stop-color="#00a8e8"/>
      <stop offset="100%" stop-color="#0078d4"/>
    </linearGradient>

    <linearGradient id="hotYellow" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#fff15a"/>
      <stop offset="100%" stop-color="#ffc000"/>
    </linearGradient>

    <filter id="hardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="1.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#050505"/>

  <!-- edge filmstrip perforations -->
  <rect x="0" y="0" width="1280" height="34" fill="#000000"/>
  <rect x="0" y="686" width="1280" height="34" fill="#000000"/>
  <rect x="48" y="10" width="28" height="14" fill="#ffffff"/>
  <rect x="118" y="10" width="28" height="14" fill="#ffffff"/>
  <rect x="188" y="10" width="28" height="14" fill="#ffffff"/>
  <rect x="258" y="10" width="28" height="14" fill="#ffffff"/>
  <rect x="328" y="10" width="28" height="14" fill="#ffffff"/>
  <rect x="928" y="696" width="28" height="14" fill="#ffffff"/>
  <rect x="998" y="696" width="28" height="14" fill="#ffffff"/>
  <rect x="1068" y="696" width="28" height="14" fill="#ffffff"/>
  <rect x="1138" y="696" width="28" height="14" fill="#ffffff"/>
  <rect x="1208" y="696" width="28" height="14" fill="#ffffff"/>

  <!-- kinetic geometric overlays -->
  <circle cx="996" cy="192" r="78" fill="none" stroke="#ffffff" stroke-width="5" stroke-dasharray="18 14"/>
  <circle cx="996" cy="192" r="40" fill="none" stroke="#ffc000" stroke-width="3" stroke-dasharray="6 8"/>
  <path d="M1045 112 L1092 82 L1076 142 L1134 132 L1084 172 L1107 224 L1056 196 L1012 232 L1026 174 Z"
        fill="#ffc000" opacity="0.18" filter="url(#softGlow)"/>
  <path d="M74 560 L350 528 L362 552 L86 585 Z" fill="#ffffff" opacity="0.18"/>
  <path d="M842 508 L1200 470 L1214 500 L852 542 Z" fill="#1ed6ff" opacity="0.22"/>
  <path d="M108 138 L172 104 L152 178 L216 162 L150 238 L166 192 Z" fill="#ffc000"/>

  <!-- circular micro typography approximated with rotated editable text -->
  <text x="960" y="128" width="150" fill="#fff15a" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="20" font-weight="900" transform="rotate(-42 960 128)">Kinetic Type</text>
  <text x="1038" y="146" width="150" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="18" font-weight="900" transform="rotate(44 1038 146)">moves fast</text>
  <text x="1030" y="232" width="150" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="18" font-weight="900" transform="rotate(132 1030 232)">learn more</text>
  <text x="914" y="222" width="150" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="18" font-weight="900" transform="rotate(-132 914 222)">watch now</text>
  <text x="957" y="204" width="90" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="28" font-weight="900" transform="rotate(180 996 192)">ABOUT</text>

  <!-- huge headline lockup -->
  <text x="170" y="586" width="505" fill="url(#electricBlue)" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="690" font-weight="900" letter-spacing="-34" filter="url(#hardShadow)">L</text>
  <text x="322" y="505" width="600" fill="url(#electricBlue)" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="300" font-weight="900" letter-spacing="-20" filter="url(#hardShadow)">ETS</text>
  <text x="584" y="676" width="310" fill="url(#electricBlue)" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="198" font-weight="900" letter-spacing="-10" filter="url(#hardShadow)">DO</text>
  <text x="908" y="535" width="260" fill="#f2f2f2" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="340" font-weight="900" letter-spacing="-18" filter="url(#hardShadow)">IT</text>

  <!-- vertical structural text -->
  <text x="76" y="414" width="310" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="52" font-weight="900" transform="rotate(-90 76 414)">THE MOTION FRAME</text>

  <!-- colored block keyword -->
  <rect x="256" y="604" width="70" height="70" rx="4" fill="#dc143c" stroke="#ffffff" stroke-width="4" transform="rotate(-8 291 639)" filter="url(#hardShadow)"/>
  <rect x="334" y="598" width="70" height="70" rx="4" fill="#0070c0" stroke="#ffffff" stroke-width="4" transform="rotate(6 369 633)" filter="url(#hardShadow)"/>
  <rect x="412" y="606" width="70" height="70" rx="4" fill="#00b050" stroke="#ffffff" stroke-width="4" transform="rotate(-11 447 641)" filter="url(#hardShadow)"/>
  <rect x="490" y="596" width="70" height="70" rx="4" fill="#7030a0" stroke="#ffffff" stroke-width="4" transform="rotate(8 525 631)" filter="url(#hardShadow)"/>
  <rect x="568" y="604" width="70" height="70" rx="4" fill="#ff6600" stroke="#ffffff" stroke-width="4" transform="rotate(-5 603 639)" filter="url(#hardShadow)"/>
  <text x="276" y="655" width="40" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="46" font-weight="900" transform="rotate(-8 291 639)">L</text>
  <text x="352" y="649" width="42" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="46" font-weight="900" transform="rotate(6 369 633)">E</text>
  <text x="430" y="657" width="44" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="46" font-weight="900" transform="rotate(-11 447 641)">A</text>
  <text x="508" y="647" width="44" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="46" font-weight="900" transform="rotate(8 525 631)">R</text>
  <text x="585" y="655" width="48" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="46" font-weight="900" transform="rotate(-5 603 639)">N</text>

  <!-- small callout stamp -->
  <rect x="798" y="118" width="118" height="34" rx="17" fill="#ffffff"/>
  <text x="814" y="143" width="90" fill="#000000" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei" font-size="18" font-weight="900">SO...</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<textPath>` for circular typography; approximate circular copy with separate rotated `<text>` objects so it remains editable.
- ❌ Do not rely on `<mask>` to punch holes through letters or filmstrips; use explicit white/black rectangles and paths instead.
- ❌ Do not put `marker-end` on paths for motion arrows; use slanted `<path>` shards or plain `<line>` streaks.
- ❌ Avoid thin, delicate typography. This style needs ultra-bold, heavy letterforms that survive rotation and overlap.
- ❌ Avoid balanced corporate grid spacing; too much alignment makes the kinetic effect feel static.

## Composition notes
- Keep the background nearly pure black and reserve 70–80% of the visual weight for oversized type in the center-left.
- Let at least one word or letter break normal reading flow: rotate a side label, stack letters, or push a giant initial off the slide edge.
- Use bright cyan/blue as the dominant kinetic color, then add yellow and multicolor tile blocks as short, high-impact accents.
- Overlays should feel like motion graphics: dashed rings, slashes, perforations, and offset shadows should cross behind or partly over the type without destroying readability.