# SVG Recipe — Tech Hero Split

## Visual mechanism
A bold cover-slide composition with oversized left-aligned typography balanced by a compact right-side hero/CTA cluster. The “tech” feeling comes from a dark gradient field, luminous rings, thin divider lines, clipped product imagery, and cool cyan/violet accents.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 3× `<rect>` for translucent right-side glass panels, CTA pill, and small metadata chips
- 1× `<image>` clipped into a rounded rectangle for the right-side hero/product visual
- 1× `<clipPath>` using rounded `<rect>` for the image crop
- 5× `<circle>` / `<ellipse>` for large technical rings, glow halos, and orbital accents
- 4× `<path>` for angled decorative shards, CTA chevron, and abstract circuit-like accents
- 3× `<line>` for fine divider/grid details
- 7× `<text>` elements with explicit `width` for logo, nav, headline, subhead, CTA, and small labels
- 3× `<linearGradient>` for background, panel glass, and accent strokes/fills
- 1× `<radialGradient>` for the cyan/violet glow field
- 2× `<filter>` definitions: one soft glow and one card shadow, applied only to shapes/text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#060B18"/>
      <stop offset="0.55" stop-color="#091326"/>
      <stop offset="1" stop-color="#10142A"/>
    </linearGradient>

    <radialGradient id="heroGlow" cx="70%" cy="45%" r="55%">
      <stop offset="0" stop-color="#35E8FF" stop-opacity="0.45"/>
      <stop offset="0.42" stop-color="#635BFF" stop-opacity="0.20"/>
      <stop offset="1" stop-color="#050814" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="glassGrad" x1="760" y1="90" x2="1180" y2="640">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="780" y1="0" x2="1180" y2="720">
      <stop offset="0" stop-color="#39F4FF"/>
      <stop offset="0.55" stop-color="#7B61FF"/>
      <stop offset="1" stop-color="#FF5BC8"/>
    </linearGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoRound">
      <rect x="816" y="162" width="330" height="315" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#heroGlow)"/>

  <circle cx="930" cy="340" r="265" fill="none" stroke="#35E8FF" stroke-width="1.4" opacity="0.24"/>
  <circle cx="930" cy="340" r="205" fill="none" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="8 16" opacity="0.20"/>
  <circle cx="930" cy="340" r="136" fill="none" stroke="url(#accentGrad)" stroke-width="2.4" stroke-dasharray="72 22" opacity="0.72"/>
  <ellipse cx="1002" cy="316" rx="300" ry="82" fill="none" stroke="#5B6CFF" stroke-width="1.2" opacity="0.35" transform="rotate(-18 1002 316)"/>
  <circle cx="1018" cy="188" r="9" fill="#35E8FF" filter="url(#softGlow)" opacity="0.9"/>

  <path d="M1090 58 L1218 20 L1180 144 Z" fill="#35E8FF" opacity="0.08"/>
  <path d="M735 616 L920 548 L1002 720 L760 720 Z" fill="#7B61FF" opacity="0.10"/>
  <path d="M694 128 C752 92 796 86 838 112 C789 142 744 160 694 128 Z" fill="#FFFFFF" opacity="0.06"/>

  <line x1="74" y1="104" x2="532" y2="104" stroke="#FFFFFF" stroke-width="1" opacity="0.13"/>
  <line x1="704" y1="104" x2="1160" y2="104" stroke="#FFFFFF" stroke-width="1" opacity="0.13"/>
  <line x1="706" y1="612" x2="1160" y2="612" stroke="#35E8FF" stroke-width="1" stroke-dasharray="4 10" opacity="0.32"/>

  <text x="74" y="67" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#FFFFFF" letter-spacing="1.5">
    NEXUS AI
  </text>
  <text x="980" y="67" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="500" fill="#AAB6D8" text-anchor="end" letter-spacing="1">
    PLATFORM / 2026
  </text>

  <text x="72" y="245" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="800" fill="#F5F8FF" letter-spacing="-3">
    <tspan x="72" dy="0">Build the</tspan>
    <tspan x="72" dy="92" fill="#35E8FF">adaptive</tspan>
    <tspan x="72" dy="92">enterprise</tspan>
  </text>

  <text x="78" y="528" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="400" fill="#AAB6D8" line-height="1.35">
    <tspan x="78" dy="0">A modern operating layer for AI products,</tspan>
    <tspan x="78" dy="30">automation, and real-time decision systems.</tspan>
  </text>

  <rect x="770" y="126" width="420" height="470" rx="42" fill="url(#glassGrad)" stroke="#FFFFFF" stroke-width="1" opacity="0.88" filter="url(#cardShadow)"/>
  <rect x="794" y="148" width="372" height="350" rx="38" fill="#0E1830" opacity="0.72"/>

  <image x="816" y="162" width="330" height="315" clip-path="url(#photoRound)" preserveAspectRatio="xMidYMid slice"
    href="https://images.example.com/hero-photo-futuristic-ai-server-room-with-blue-light.jpg"/>

  <rect x="824" y="512" width="116" height="30" rx="15" fill="#35E8FF" opacity="0.14"/>
  <text x="846" y="533" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#35E8FF" letter-spacing="1.4">
    LIVE DEMO
  </text>

  <text x="824" y="576" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#FFFFFF">
    See the stack
  </text>

  <rect x="1034" y="538" width="96" height="44" rx="22" fill="url(#accentGrad)"/>
  <text x="1058" y="567" width="52" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#071021">
    START
  </text>
  <path d="M1118 556 L1127 560 L1118 564" fill="none" stroke="#071021" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>

  <path d="M838 214 L884 214 L904 238 L950 238" fill="none" stroke="#35E8FF" stroke-width="1.6" stroke-linecap="round" opacity="0.72"/>
  <path d="M986 414 L1024 414 L1048 386 L1098 386" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity="0.34"/>
</svg>
```

## Avoid in this skill
- ❌ Using a plain two-column grid with equal visual weight; the left headline must dominate and the right side should feel like a curated hero object.
- ❌ Applying blur/shadow filters to `<line>` elements; use filters only on cards, circles, paths, or text.
- ❌ Using `clip-path` on decorative shapes; reserve clipping for the `<image>` crop so it translates cleanly.
- ❌ Overfilling the slide with bullets or dense UI widgets; this is a low-density cover/section-divider treatment.

## Composition notes
- Keep the headline in the left 50–55% of the canvas, with very large type and generous line spacing.
- Place the hero image/card in the right third, slightly above center, so it counterbalances the heavy headline.
- Use cyan/violet accents sparingly: rings, CTA, one headline word, and small metadata chips.
- Preserve dark negative space around the headline and between the text block and right hero cluster for a premium keynote feel.