# SVG Recipe — Modern Corporate Accent

## Visual mechanism
A premium dark canvas is energized by layered, high-saturation geometric accents clustered in one corner, creating an asymmetrical corporate identity frame. Large left-aligned typography sits in generous negative space, with thin rules and subtle glows adding polish without clutter.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 4× `<linearGradient>` for background depth, accent fills, and separator treatment
- 2× `<filter>` definitions for soft shadow and accent glow
- 7× `<rect>` for layered corner accents, translucent panels, and thin separator bars
- 5× `<path>` for diagonal corporate slashes and subtle decorative geometry
- 4× `<line>` for faint technical guide strokes in the accent area
- 5× `<text>` elements with explicit `width` attributes for title, subtitle, kicker, date, and micro-labels
- Nested `<tspan>` elements for multi-line title styling and inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#20242E"/>
      <stop offset="55%" stop-color="#2B2D37"/>
      <stop offset="100%" stop-color="#161922"/>
    </linearGradient>

    <linearGradient id="yellowGrad" x1="840" y1="40" x2="1230" y2="145">
      <stop offset="0%" stop-color="#FFE66A"/>
      <stop offset="52%" stop-color="#FFCC00"/>
      <stop offset="100%" stop-color="#E6A900"/>
    </linearGradient>

    <linearGradient id="cyanGrad" x1="1020" y1="126" x2="1260" y2="190">
      <stop offset="0%" stop-color="#35D4FF"/>
      <stop offset="100%" stop-color="#1687D9"/>
    </linearGradient>

    <linearGradient id="ruleGrad" x1="96" y1="500" x2="460" y2="500">
      <stop offset="0%" stop-color="#FFCC00"/>
      <stop offset="45%" stop-color="#FFCC00"/>
      <stop offset="100%" stop-color="#FFCC00" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="180%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-30%" y="-50%" width="160%" height="220%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-60 660 L330 720 L-60 720 Z" fill="#11141C" opacity="0.72"/>
  <path d="M1080 -60 L1280 -60 L1280 250 L1188 222 Z" fill="#0F131B" opacity="0.75"/>
  <path d="M884 0 L1280 0 L1280 182 L1038 134 Z" fill="#383B46"/>
  <path d="M980 0 L1280 0 L1280 120 L1014 104 Z" fill="#4E525E" opacity="0.72"/>

  <rect x="885" y="38" width="338" height="86" rx="0" fill="url(#yellowGrad)" filter="url(#softShadow)"/>
  <rect x="835" y="68" width="220" height="28" fill="#FFFFFF" opacity="0.16"/>
  <rect x="1054" y="140" width="190" height="38" fill="url(#cyanGrad)" filter="url(#softShadow)"/>
  <rect x="1115" y="104" width="165" height="14" fill="#FFFFFF" opacity="0.18"/>
  <rect x="1214" y="0" width="66" height="220" fill="#FFCC00" opacity="0.18"/>

  <path d="M826 122 L1045 176 L1015 198 L792 140 Z" fill="#FFCC00" opacity="0.18" filter="url(#accentGlow)"/>
  <path d="M1142 198 L1280 228 L1280 260 L1108 220 Z" fill="#35D4FF" opacity="0.22"/>
  <path d="M928 172 L1014 194 L1000 205 L912 183 Z" fill="#FFFFFF" opacity="0.22"/>

  <line x1="862" y1="215" x2="1255" y2="215" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.18" stroke-dasharray="10 10"/>
  <line x1="914" y1="244" x2="1210" y2="244" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.12" stroke-dasharray="5 9"/>
  <line x1="1082" y1="24" x2="1082" y2="254" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.11"/>
  <line x1="1168" y1="0" x2="1168" y2="232" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.10"/>

  <rect x="96" y="486" width="390" height="4" fill="url(#ruleGrad)"/>
  <rect x="96" y="506" width="112" height="2" fill="#35D4FF" opacity="0.85"/>

  <text x="96" y="174" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="3"
        fill="#FFCC00">
    EXECUTIVE PERFORMANCE REVIEW
  </text>

  <text x="92" y="278" width="760"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="64" font-weight="800"
        fill="#FFFFFF">
    <tspan x="92" dy="0">ANNUAL WORK</tspan>
    <tspan x="92" dy="76">REPORT</tspan>
    <tspan fill="#FFCC00"> 2026</tspan>
  </text>

  <text x="98" y="418" width="660"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400"
        fill="#D8DCE6">
    <tspan x="98" dy="0">A concise summary of yearly performance,</tspan>
    <tspan x="98" dy="34">strategic priorities, and forward outlook.</tspan>
  </text>

  <text x="98" y="570" width="460"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600"
        letter-spacing="1.8"
        fill="#AEB5C4">
    STRATEGY · OPERATIONS · GROWTH
  </text>

  <text x="1038" y="646" width="170"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700"
        text-anchor="end"
        fill="#FFFFFF">
    Q4 BOARD BRIEF
  </text>

  <text x="1040" y="674" width="168"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="400"
        text-anchor="end"
        fill="#8F98AA">
    Confidential · January 2026
  </text>
</svg>
```

## Avoid in this skill
- ❌ Overfilling the slide with many accent blocks; the effect depends on one strong corner cluster and ample negative space.
- ❌ Low-contrast text on the charcoal background; keep title text near-white and subtitles light gray.
- ❌ Using filtered `<line>` elements for glow or shadow; filters on lines may be dropped, so use thin `<rect>` or `<path>` elements instead.
- ❌ Placing geometric accents behind the main title; they should frame the composition, not compete with readability.
- ❌ Complex masks, patterns, or symbol reuse for the accent system; use direct editable rectangles and paths.

## Composition notes
- Keep the main message in the left-middle third, with roughly 90–110 px margins from the slide edge.
- Reserve the top-right 25–30% of the canvas for the accent cluster; let some shapes bleed off-slide for a premium editorial feel.
- Use one dominant corporate accent color, one secondary cool accent, and several low-opacity gray/white overlays for depth.
- Maintain strong hierarchy: small uppercase kicker, oversized bold title, restrained subtitle, and minimal footer metadata.