# SVG Recipe — Tactile Architectural Editorial

## Visual mechanism
A warm terracotta-to-clay gradient is overlaid with a subtle paper photograph and sparse hand-drawn fiber strokes to create a tactile architectural surface. The composition stays highly restrained: a centered editorial text stack, one fine divider, and wide-spaced uppercase typography floating in generous negative space.

## SVG primitives needed
- 2× `<rect>` for the full-slide gradient base and soft dark vignette overlay
- 1× `<image>` for a full-bleed paper / plaster texture overlay
- 18–30× `<path>` for faint irregular paper fibers, drafting scratches, and tactile imperfections
- 4× `<line>` for minimal architectural guide marks and the central copper divider
- 3× `<text>` for italic context, main spaced title, and small editorial caption
- 1× `<linearGradient>` for the vertical terracotta background
- 1× `<radialGradient>` for the subtle center-light / edge-dark vignette
- 1× `<filter id="softShadow">` applied to the text group for extremely restrained depth
- Optional 1× `<filter id="warmBlur">` applied to a large organic path for a hazy clay glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="clayGradient" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#BA6040"/>
      <stop offset="44%" stop-color="#98472F"/>
      <stop offset="100%" stop-color="#4E2416"/>
    </linearGradient>

    <radialGradient id="editorialVignette" cx="50%" cy="43%" r="72%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="55%" stop-color="#2B120B" stop-opacity="0.00"/>
      <stop offset="100%" stop-color="#160804" stop-opacity="0.36"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="0" dy="3" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="warmBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
  </defs>

  <!-- tactile clay field -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#clayGradient)"/>
  <path d="M-40,116 C210,34 342,86 506,42 C724,-16 884,38 1030,14 C1168,-8 1282,28 1344,70 L1344,246 C1102,208 924,278 738,226 C520,164 366,228 174,194 C66,176 12,154 -40,174 Z"
        fill="#D88B62" opacity="0.16" filter="url(#warmBlur)"/>
  <image href="https://images.unsplash.com/photo-1586075010923-2dd4570fb338?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.18"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#editorialVignette)"/>

  <!-- faint paper grain / architectural scratches; intentionally irregular -->
  <path d="M86,94 C152,82 214,95 280,78" fill="none" stroke="#F4C6A3" stroke-width="1" opacity="0.12"/>
  <path d="M960,92 C1038,76 1100,86 1196,68" fill="none" stroke="#F4C6A3" stroke-width="1" opacity="0.10"/>
  <path d="M154,610 C252,594 326,630 438,602" fill="none" stroke="#1F0B06" stroke-width="1.2" opacity="0.13"/>
  <path d="M846,618 C948,596 1046,624 1166,590" fill="none" stroke="#1F0B06" stroke-width="1" opacity="0.14"/>
  <path d="M58,288 C126,282 196,302 264,292" fill="none" stroke="#E7B28D" stroke-width="0.8" opacity="0.12"/>
  <path d="M1018,306 C1088,292 1154,306 1238,286" fill="none" stroke="#E7B28D" stroke-width="0.8" opacity="0.10"/>
  <path d="M378,118 C392,206 374,280 398,362" fill="none" stroke="#2A1008" stroke-width="0.8" opacity="0.10"/>
  <path d="M894,104 C874,204 904,298 880,402" fill="none" stroke="#2A1008" stroke-width="0.8" opacity="0.10"/>
  <path d="M224,444 C318,420 396,454 486,430" fill="none" stroke="#FFD1AD" stroke-width="0.7" opacity="0.09"/>
  <path d="M776,444 C882,414 986,456 1086,426" fill="none" stroke="#FFD1AD" stroke-width="0.7" opacity="0.09"/>
  <path d="M520,646 C594,630 668,652 746,636" fill="none" stroke="#0F0503" stroke-width="1" opacity="0.11"/>

  <!-- restrained drafting guides -->
  <line x1="96" y1="360" x2="244" y2="360" stroke="#E1AA83" stroke-width="1" opacity="0.24"/>
  <line x1="1036" y1="360" x2="1184" y2="360" stroke="#E1AA83" stroke-width="1" opacity="0.24"/>
  <line x1="640" y1="94" x2="640" y2="150" stroke="#E1AA83" stroke-width="1" opacity="0.18"/>
  <line x1="640" y1="570" x2="640" y2="626" stroke="#E1AA83" stroke-width="1" opacity="0.18"/>

  <!-- centered editorial typography -->
  <g filter="url(#softShadow)">
    <text x="290" y="304" width="700"
          text-anchor="middle"
          font-family="Georgia, 'Times New Roman', serif"
          font-size="25"
          font-style="italic"
          fill="#EFE1D4"
          opacity="0.94">
      Key qualities of a compelling architecture presentation
    </text>

    <line x1="510" y1="330" x2="770" y2="330" stroke="#D2A07A" stroke-width="1.3" opacity="0.78"/>

    <text x="640" y="389" width="980"
          text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
          font-size="42"
          font-weight="600"
          fill="#FFFFFF">
      C O N C E P T&nbsp;&nbsp; W R A P P I N G
    </text>

    <text x="430" y="438" width="420"
          text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
          font-size="12"
          font-weight="400"
          fill="#F0C5A6"
          opacity="0.72">
      MATERIAL LOGIC · SPATIAL SEQUENCE · URBAN MEMORY
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ `<pattern>` fills for paper grain; they often translate poorly and can flatten or disappear
- ❌ Heavy dashboards, dense charts, or multi-column layouts; this style depends on silence and editorial restraint
- ❌ Bright saturated accent colors; keep accents in copper, bone, clay, ivory, and charcoal-brown
- ❌ Drop shadows that look like UI cards; any depth should be barely perceptible, as if ink sits on textured paper
- ❌ `mask` or clip-path on non-image elements for texture effects; use a full-bleed `<image>` plus transparent paths instead

## Composition notes
- Keep the text block centered and vertically compact, occupying roughly the middle 20–30% of the slide.
- Preserve large top and bottom negative space; the tactile background is part of the message, not empty filler.
- Use one dominant title, one italic contextual line, and one very small caption at most.
- Let color rhythm move from dark clay edges to a warmer center, with fine copper dividers acting as architectural precision marks.