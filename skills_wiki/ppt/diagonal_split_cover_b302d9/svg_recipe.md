# SVG Recipe — Diagonal Split Cover

## Visual mechanism
A calm, text-heavy left field is contrasted with a high-energy diagonal split on the right, using layered slanted panels, translucent ribbons, and glow accents to create motion without crowding the cover. The headline sits in a protected negative-space zone while the diagonal geometry acts as a premium brand-forward visual anchor.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<rect>` for the small eyebrow label chip
- 8× `<path>` for the large diagonal split panel, layered accent wedges, translucent overlays, and thin diagonal strokes
- 6× `<line>` for subtle diagonal rhythm lines on the right side
- 4× `<text>` for eyebrow, headline, subhead, and footer/date metadata
- 4× `<linearGradient>` for background, primary diagonal panel, cyan accent, and warm highlight accent
- 1× `<radialGradient>` for a soft luminous bloom behind the diagonal accents
- 2× `<filter>` with `feGaussianBlur` / `feOffset` / `feMerge` for panel shadow and accent glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="58%" stop-color="#EEF4FB"/>
      <stop offset="100%" stop-color="#E4ECF7"/>
    </linearGradient>

    <linearGradient id="deepPanel" x1="675" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#162A4A"/>
      <stop offset="48%" stop-color="#0B1730"/>
      <stop offset="100%" stop-color="#050A18"/>
    </linearGradient>

    <linearGradient id="cyanRibbon" x1="770" y1="90" x2="1180" y2="650">
      <stop offset="0%" stop-color="#54E7FF"/>
      <stop offset="48%" stop-color="#19A9E5"/>
      <stop offset="100%" stop-color="#2767FF"/>
    </linearGradient>

    <linearGradient id="warmRibbon" x1="1000" y1="0" x2="1230" y2="520">
      <stop offset="0%" stop-color="#FFE36E"/>
      <stop offset="48%" stop-color="#FF9A48"/>
      <stop offset="100%" stop-color="#FF4F73"/>
    </linearGradient>

    <radialGradient id="bloom" cx="70%" cy="48%" r="55%">
      <stop offset="0%" stop-color="#48D7FF" stop-opacity="0.32"/>
      <stop offset="50%" stop-color="#497BFF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#497BFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="-16" dy="18" in="SourceAlpha" result="offset"/>
      <feGaussianBlur stdDeviation="18" in="offset" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="10" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M610 0 L1280 0 L1280 720 L500 720 Z" fill="url(#bloom)"/>

  <path d="M770 0 L1280 0 L1280 720 L590 720 Z" fill="url(#deepPanel)" filter="url(#panelShadow)"/>
  <path d="M895 0 L1028 0 L735 720 L604 720 Z" fill="#FFFFFF" fill-opacity="0.06"/>
  <path d="M1002 0 L1114 0 L825 720 L713 720 Z" fill="#FFFFFF" fill-opacity="0.04"/>
  <path d="M1138 0 L1280 0 L1280 295 L1018 720 L883 720 Z" fill="url(#warmRibbon)" fill-opacity="0.92" filter="url(#softGlow)"/>
  <path d="M875 130 L1000 130 L757 720 L632 720 Z" fill="url(#cyanRibbon)" fill-opacity="0.96" filter="url(#softGlow)"/>
  <path d="M1116 390 L1280 185 L1280 310 L1190 423 Z" fill="#FFFFFF" fill-opacity="0.18"/>
  <path d="M702 0 L727 0 L446 720 L421 720 Z" fill="#0D1D36" fill-opacity="0.10"/>
  <path d="M752 0 L762 0 L481 720 L471 720 Z" fill="#28C7FF" fill-opacity="0.55"/>

  <line x1="946" y1="44" x2="720" y2="620" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2"/>
  <line x1="990" y1="72" x2="765" y2="650" stroke="#54E7FF" stroke-opacity="0.34" stroke-width="2"/>
  <line x1="1040" y1="40" x2="812" y2="620" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="1180" y1="78" x2="958" y2="646" stroke="#FFCE63" stroke-opacity="0.34" stroke-width="2"/>
  <line x1="1228" y1="152" x2="1048" y2="612" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1"/>
  <line x1="1262" y1="260" x2="1100" y2="674" stroke="#FF6D92" stroke-opacity="0.32" stroke-width="2"/>

  <rect x="88" y="104" width="188" height="34" rx="17" fill="#0B1730"/>
  <text x="112" y="127" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" letter-spacing="1.8" fill="#FFFFFF">
    EXECUTIVE BRIEF
  </text>

  <text x="86" y="244" width="600" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#0B1730">
    <tspan x="86" y="244">STRATEGY</tspan>
    <tspan x="86" y="326">RESET 2026</tspan>
  </text>

  <text x="92" y="392" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="400" fill="#4C5D73">
    <tspan x="92" y="392">A focused operating model for growth,</tspan>
    <tspan x="92" y="426">resilience, and faster market execution.</tspan>
  </text>

  <text x="92" y="636" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#7A8798">
    MAY 2026  ·  CONFIDENTIAL LEADERSHIP SESSION
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `transform="skewX(...)"` or matrix transforms to create the diagonal split; use explicit `<path d="...">` polygons instead.
- ❌ Do not build the angled right-side design with masked shapes; masks are unsafe for translation and unnecessary here.
- ❌ Do not place filters on `<line>` elements for glowing diagonal strokes; use filled `<path>` ribbons with `filter` when glow is needed.
- ❌ Do not let the diagonal accents intrude into the headline’s reading zone; the cover works because the left side remains quiet and legible.

## Composition notes
- Keep the headline in the left 48–55% of the canvas, with generous top and left margins for executive-cover polish.
- Let the diagonal split begin around x=720–790 at the top and land around x=520–620 at the bottom to create strong forward motion.
- Use one dark dominant panel plus two vivid accent ribbons; too many bright wedges will make the cover feel like a generic tech background.
- Reserve the bottom-left corner for date, confidentiality, company, or event metadata; it balances the heavy right-side geometry.