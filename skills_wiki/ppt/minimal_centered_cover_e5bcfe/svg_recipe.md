# SVG Recipe — Minimal Centered Cover

## Visual mechanism
A refined corporate cover slide built around a centered typographic lockup floating in abundant whitespace. Subtle off-canvas gradient geometry, hairline rules, and a tiny accent mark add premium polish without competing with the headline.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<path>` for large off-canvas decorative gradient fields
- 1× `<rect>` for a soft central light wash
- 4× `<line>` for delicate framing rules around the title area
- 1× `<rect>` for a small accent pill above the headline
- 3× `<text>` for eyebrow label, headline, and subtitle
- 2× `<linearGradient>` for background and accent fills
- 2× `<radialGradient>` for soft ambient color fields
- 2× `<filter>` with `feGaussianBlur` / `feOffset` for glow and soft shadow effects

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F8FAFC"/>
      <stop offset="0.52" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F3F6FA"/>
    </linearGradient>

    <linearGradient id="accentGold" x1="510" y1="268" x2="770" y2="268" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#B98D3B"/>
      <stop offset="0.5" stop-color="#E3C175"/>
      <stop offset="1" stop-color="#B98D3B"/>
    </linearGradient>

    <radialGradient id="coolGlow" cx="0.5" cy="0.5" r="0.65">
      <stop offset="0" stop-color="#DCEBFF" stop-opacity="0.95"/>
      <stop offset="0.58" stop-color="#EAF3FF" stop-opacity="0.35"/>
      <stop offset="1" stop-color="#EAF3FF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="warmGlow" cx="0.5" cy="0.5" r="0.7">
      <stop offset="0" stop-color="#FFE8B8" stop-opacity="0.75"/>
      <stop offset="0.6" stop-color="#FFF4D8" stop-opacity="0.26"/>
      <stop offset="1" stop-color="#FFF4D8" stop-opacity="0"/>
    </radialGradient>

    <filter id="blurGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M-90 52 C75 -34 207 -28 321 62 C415 136 453 236 405 321 C353 413 220 412 112 371 C3 330 -80 259 -117 175 C-140 123 -133 82 -90 52 Z"
        fill="url(#coolGlow)" filter="url(#blurGlow)" opacity="0.85"/>

  <path d="M1014 566 C1089 455 1248 424 1355 496 C1449 559 1463 686 1388 778 C1308 876 1147 875 1041 800 C943 731 943 671 1014 566 Z"
        fill="url(#warmGlow)" filter="url(#blurGlow)" opacity="0.9"/>

  <rect x="360" y="214" width="560" height="292" rx="28"
        fill="#FFFFFF" opacity="0.38" filter="url(#softShadow)"/>

  <line x1="458" y1="282" x2="554" y2="282" stroke="#CBD5E1" stroke-width="1"/>
  <line x1="726" y1="282" x2="822" y2="282" stroke="#CBD5E1" stroke-width="1"/>
  <line x1="458" y1="454" x2="554" y2="454" stroke="#CBD5E1" stroke-width="1"/>
  <line x1="726" y1="454" x2="822" y2="454" stroke="#CBD5E1" stroke-width="1"/>

  <rect x="600" y="257" width="80" height="4" rx="2" fill="url(#accentGold)"/>

  <text x="640" y="246" width="420" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="3.2"
        fill="#64748B">
    STRATEGY BRIEF
  </text>

  <text x="640" y="351" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="650" letter-spacing="-1.6"
        fill="#0F172A">
    <tspan x="640" dy="0">Building the Next</tspan>
    <tspan x="640" dy="66">Growth Horizon</tspan>
  </text>

  <text x="640" y="455" width="600" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400" line-height="1.35"
        fill="#475569">
    <tspan x="640">A concise executive narrative for market expansion,</tspan>
    <tspan x="640" dy="29">operating focus, and capital allocation priorities.</tspan>
  </text>

  <text x="92" y="646" width="280"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="500" letter-spacing="1.4"
        fill="#94A3B8">
    CONFIDENTIAL · 2026
  </text>

  <text x="1188" y="646" width="220" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="500" letter-spacing="1.4"
        fill="#94A3B8">
    BOARD REVIEW
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense grids, icon rows, or dashboard-like modules that undermine the whitespace-driven cover aesthetic
- ❌ Large photo backgrounds unless heavily muted; the technique depends on typographic quietness
- ❌ Overusing shadows or glows around text; keep type crisp and executive
- ❌ Centering every decorative element with equal weight; the accents should be subtle, asymmetric, and mostly off-canvas

## Composition notes
- Keep the headline lockup centered both horizontally and optically vertically, with the subtitle close enough to read as one unit.
- Reserve at least 45–55% of the slide as calm negative space; decorative gradients should sit near corners or edges.
- Use one restrained accent color, ideally as a tiny rule or pill, not as a large block.
- Footer metadata is optional and should be small, low-contrast, and aligned to the slide margins.