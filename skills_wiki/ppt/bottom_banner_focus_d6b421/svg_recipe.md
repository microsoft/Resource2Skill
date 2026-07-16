# SVG Recipe — Bottom Banner Focus

## Visual mechanism
A cinematic, mostly empty slide uses a heavyweight bottom banner as the visual anchor for the primary headline, while a compact floating center panel carries optional supporting copy. Subtle technical grid lines, glows, and angled geometry point the eye downward without competing with the banner.

## SVG primitives needed
- 2× `<rect>` for full-slide background and soft central content panel
- 2× `<path>` for the bold bottom banner silhouette and angled accent geometry
- 10–14× `<line>` for faint technical grid / guide lines in the upper field
- 3–5× `<circle>` / `<ellipse>` for ambient glow nodes and focus dots
- 3× `<text>` blocks for eyebrow label, supporting body, and bottom headline
- 3× `<linearGradient>` for background depth, banner fill, and accent strokes
- 1× `<radialGradient>` for atmospheric spotlight glow
- 2× `<filter>` definitions: one soft drop shadow for panels/banner, one blur glow for decorative shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#08111F"/>
      <stop offset="52%" stop-color="#101B2E"/>
      <stop offset="100%" stop-color="#05070D"/>
    </linearGradient>

    <linearGradient id="bannerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00D1FF"/>
      <stop offset="42%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>

    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.06"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7DD3FC" stop-opacity="0"/>
      <stop offset="45%" stop-color="#7DD3FC" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#A78BFA" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="spotGlow" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.34"/>
      <stop offset="62%" stop-color="#2563EB" stop-opacity="0.09"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0.02  0 0 0 0 0.08  0 0 0 0.35 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="640" cy="310" rx="470" ry="260" fill="url(#spotGlow)" filter="url(#glow)" opacity="0.9"/>

  <line x1="120" y1="86" x2="1160" y2="86" stroke="#93C5FD" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="120" y1="146" x2="1160" y2="146" stroke="#93C5FD" stroke-opacity="0.08" stroke-width="1"/>
  <line x1="120" y1="206" x2="1160" y2="206" stroke="#93C5FD" stroke-opacity="0.07" stroke-width="1"/>
  <line x1="120" y1="266" x2="1160" y2="266" stroke="#93C5FD" stroke-opacity="0.06" stroke-width="1"/>
  <line x1="120" y1="326" x2="1160" y2="326" stroke="#93C5FD" stroke-opacity="0.05" stroke-width="1"/>
  <line x1="180" y1="56" x2="180" y2="430" stroke="#93C5FD" stroke-opacity="0.06" stroke-width="1"/>
  <line x1="330" y1="56" x2="330" y2="430" stroke="#93C5FD" stroke-opacity="0.06" stroke-width="1"/>
  <line x1="480" y1="56" x2="480" y2="430" stroke="#93C5FD" stroke-opacity="0.06" stroke-width="1"/>
  <line x1="800" y1="56" x2="800" y2="430" stroke="#93C5FD" stroke-opacity="0.06" stroke-width="1"/>
  <line x1="950" y1="56" x2="950" y2="430" stroke="#93C5FD" stroke-opacity="0.06" stroke-width="1"/>
  <line x1="1100" y1="56" x2="1100" y2="430" stroke="#93C5FD" stroke-opacity="0.06" stroke-width="1"/>

  <path d="M126 388 C260 320, 346 336, 456 292 S690 230, 812 278 S1018 336, 1158 244"
        fill="none" stroke="url(#accentGrad)" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
  <path d="M76 506 L380 456 L660 486 L1002 430 L1210 468"
        fill="none" stroke="#38BDF8" stroke-opacity="0.28" stroke-width="2" stroke-dasharray="9 12"/>

  <circle cx="456" cy="292" r="5" fill="#67E8F9"/>
  <circle cx="812" cy="278" r="5" fill="#A78BFA"/>
  <circle cx="1158" cy="244" r="5" fill="#67E8F9"/>
  <circle cx="456" cy="292" r="24" fill="#38BDF8" opacity="0.20" filter="url(#glow)"/>
  <circle cx="812" cy="278" r="28" fill="#A78BFA" opacity="0.22" filter="url(#glow)"/>

  <rect x="354" y="188" width="572" height="184" rx="28"
        fill="url(#panelGrad)" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.2" filter="url(#shadow)"/>
  <line x1="386" y1="234" x2="506" y2="234" stroke="url(#accentGrad)" stroke-width="3" stroke-linecap="round"/>

  <text x="386" y="224" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="3" fill="#93C5FD">
    STRATEGIC FOCUS
  </text>
  <text x="386" y="272" width="508" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="600" fill="#F8FAFC">
    Build momentum where the signal is strongest
  </text>
  <text x="386" y="316" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#CBD5E1">
    Use the center panel for one short proof point, context line, or transition sentence before the bottom banner lands the main idea.
  </text>

  <path d="M0 486 C210 456, 374 498, 548 476 C778 448, 982 430, 1280 468 L1280 720 L0 720 Z"
        fill="url(#bannerGrad)" filter="url(#shadow)"/>
  <path d="M0 486 C210 456, 374 498, 548 476 C778 448, 982 430, 1280 468"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.46" stroke-width="2"/>

  <path d="M836 534 L1280 486 L1280 720 L1018 720 Z"
        fill="#FFFFFF" fill-opacity="0.10"/>
  <path d="M965 512 L1280 478 L1280 548 L944 594 Z"
        fill="#020617" fill-opacity="0.18"/>

  <text x="92" y="592" width="1070" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" fill="#FFFFFF" letter-spacing="-1.5">
    Bottom Banner Focus
    <tspan fill="#DBEAFE" font-weight="600"> for executive emphasis</tspan>
  </text>
  <text x="96" y="642" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#E0F2FE" letter-spacing="2.2">
    ONE MESSAGE · HIGH CONTRAST · CLEAR LANDING ZONE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Putting the headline in the center and treating the banner as decoration; the bottom band must be the primary focus zone.
- ❌ Using `filter` on grid `<line>` elements; keep line work simple because line filters may be dropped.
- ❌ Omitting `width` on `<text>` elements; the headline and panel copy need fixed text boxes for reliable PowerPoint rendering.
- ❌ Overfilling the upper field with charts, icons, or dense copy; the technique depends on negative space above the banner.

## Composition notes
- Reserve the lower 28–34% of the slide for the bold banner and main headline.
- Keep the central panel compact, roughly 40–50% slide width, with only one short body message.
- Let the top half breathe: use faint grid lines, glow nodes, or a single abstract trajectory path for atmosphere.
- Use a saturated banner gradient against a dark background so the headline reads instantly from a distance.