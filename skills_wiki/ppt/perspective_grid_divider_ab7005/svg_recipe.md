# SVG Recipe — Perspective Grid Divider

## Visual mechanism
A neon perspective grid recedes toward a central horizon point, creating motion and depth without animation. A floating glassy title label sits above the vanishing point, turning the grid into a high-energy technical section divider.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 1× `<rect>` for a subtle translucent top atmospheric wash
- 1× `<circle>` for the retro horizon sun / focal glow
- 1× `<ellipse>` for the wide horizon glow
- 1× `<path>` for the dark distant mountain silhouette
- 1× `<path>` for the trapezoid floor plane
- 9× `<path>` for horizontal perspective grid bands
- 11× `<path>` for radial perspective rays converging to the vanishing point
- 4× `<path>` for luminous accent streaks and scanline details
- 3× `<rect>` for the floating title card, top accent bar, and small section tag
- 3× `<text>` for section number, main title, and small metadata caption
- 3× `<circle>` for small glowing node accents on the grid
- 3× `<linearGradient>` for background, floor, and card fills
- 2× `<radialGradient>` for horizon and node glows
- 3× `<filter>` using `feGaussianBlur` / shadow merge for neon glow, soft card shadow, and text glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#090B22"/>
      <stop offset="0.48" stop-color="#12153A"/>
      <stop offset="1" stop-color="#030414"/>
    </linearGradient>

    <linearGradient id="floorFill" x1="640" y1="360" x2="640" y2="720">
      <stop offset="0" stop-color="#251247" stop-opacity="0.15"/>
      <stop offset="0.55" stop-color="#151445" stop-opacity="0.52"/>
      <stop offset="1" stop-color="#09071D" stop-opacity="0.95"/>
    </linearGradient>

    <linearGradient id="gridStroke" x1="0" y1="720" x2="1280" y2="360">
      <stop offset="0" stop-color="#FF3BD4"/>
      <stop offset="0.5" stop-color="#6BF7FF"/>
      <stop offset="1" stop-color="#7A5CFF"/>
    </linearGradient>

    <linearGradient id="cardFill" x1="390" y1="210" x2="890" y2="352">
      <stop offset="0" stop-color="#161B4A" stop-opacity="0.92"/>
      <stop offset="0.58" stop-color="#111735" stop-opacity="0.86"/>
      <stop offset="1" stop-color="#090B22" stop-opacity="0.92"/>
    </linearGradient>

    <linearGradient id="accentBar" x1="410" y1="220" x2="870" y2="220">
      <stop offset="0" stop-color="#FF3BD4"/>
      <stop offset="0.45" stop-color="#6BF7FF"/>
      <stop offset="1" stop-color="#FFD166"/>
    </linearGradient>

    <radialGradient id="horizonGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FF3BD4" stop-opacity="0.65"/>
      <stop offset="0.42" stop-color="#6BF7FF" stop-opacity="0.25"/>
      <stop offset="1" stop-color="#090B22" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="sunFill" cx="50%" cy="45%" r="60%">
      <stop offset="0" stop-color="#FFF1A6"/>
      <stop offset="0.45" stop-color="#FF5CCB"/>
      <stop offset="1" stop-color="#6D3DFF"/>
    </radialGradient>

    <filter id="neonGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cardShadow" x="-25%" y="-35%" width="150%" height="170%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-20%" y="-30%" width="140%" height="160%">
      <feGaussianBlur stdDeviation="2.8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <rect x="0" y="0" width="1280" height="330" fill="#182052" opacity="0.22"/>
  <ellipse cx="640" cy="365" rx="520" ry="145" fill="url(#horizonGlow)"/>
  <circle cx="640" cy="348" r="88" fill="url(#sunFill)" opacity="0.82" filter="url(#neonGlow)"/>

  <path d="M0 378 L115 330 L218 362 L346 302 L470 366 L610 318 L742 365 L900 308 L1034 360 L1160 326 L1280 374 L1280 424 L0 424 Z"
        fill="#060817" opacity="0.88"/>

  <path d="M590 360 L690 360 L1280 720 L0 720 Z" fill="url(#floorFill)"/>

  <path d="M610 374 L670 374" stroke="url(#gridStroke)" stroke-width="1.5" opacity="0.7" filter="url(#neonGlow)"/>
  <path d="M570 392 L710 392" stroke="url(#gridStroke)" stroke-width="1.8" opacity="0.75" filter="url(#neonGlow)"/>
  <path d="M520 418 L760 418" stroke="url(#gridStroke)" stroke-width="2" opacity="0.78" filter="url(#neonGlow)"/>
  <path d="M455 452 L825 452" stroke="url(#gridStroke)" stroke-width="2.2" opacity="0.82" filter="url(#neonGlow)"/>
  <path d="M370 494 L910 494" stroke="url(#gridStroke)" stroke-width="2.4" opacity="0.84" filter="url(#neonGlow)"/>
  <path d="M265 545 L1015 545" stroke="url(#gridStroke)" stroke-width="2.7" opacity="0.86" filter="url(#neonGlow)"/>
  <path d="M130 608 L1150 608" stroke="url(#gridStroke)" stroke-width="3" opacity="0.9" filter="url(#neonGlow)"/>
  <path d="M0 680 L1280 680" stroke="url(#gridStroke)" stroke-width="3.4" opacity="0.92" filter="url(#neonGlow)"/>
  <path d="M0 718 L1280 718" stroke="#6BF7FF" stroke-width="4" opacity="0.62"/>

  <path d="M640 360 L-120 720" stroke="url(#gridStroke)" stroke-width="2" opacity="0.55" filter="url(#neonGlow)"/>
  <path d="M640 360 L40 720" stroke="url(#gridStroke)" stroke-width="2" opacity="0.6" filter="url(#neonGlow)"/>
  <path d="M640 360 L185 720" stroke="url(#gridStroke)" stroke-width="2.2" opacity="0.65" filter="url(#neonGlow)"/>
  <path d="M640 360 L330 720" stroke="url(#gridStroke)" stroke-width="2.3" opacity="0.72" filter="url(#neonGlow)"/>
  <path d="M640 360 L485 720" stroke="url(#gridStroke)" stroke-width="2.4" opacity="0.78" filter="url(#neonGlow)"/>
  <path d="M640 360 L640 720" stroke="#6BF7FF" stroke-width="2.8" opacity="0.88" filter="url(#neonGlow)"/>
  <path d="M640 360 L795 720" stroke="url(#gridStroke)" stroke-width="2.4" opacity="0.78" filter="url(#neonGlow)"/>
  <path d="M640 360 L950 720" stroke="url(#gridStroke)" stroke-width="2.3" opacity="0.72" filter="url(#neonGlow)"/>
  <path d="M640 360 L1095 720" stroke="url(#gridStroke)" stroke-width="2.2" opacity="0.65" filter="url(#neonGlow)"/>
  <path d="M640 360 L1240 720" stroke="url(#gridStroke)" stroke-width="2" opacity="0.6" filter="url(#neonGlow)"/>
  <path d="M640 360 L1400 720" stroke="url(#gridStroke)" stroke-width="2" opacity="0.55" filter="url(#neonGlow)"/>

  <path d="M86 116 L254 116" stroke="#6BF7FF" stroke-width="2" stroke-dasharray="10 12" opacity="0.55"/>
  <path d="M1010 126 L1190 126" stroke="#FF3BD4" stroke-width="2" stroke-dasharray="5 10" opacity="0.5"/>
  <path d="M78 560 C210 528 294 520 390 535" stroke="#FF3BD4" stroke-width="2" opacity="0.45" fill="none"/>
  <path d="M910 505 C1012 486 1110 494 1215 532" stroke="#6BF7FF" stroke-width="2" opacity="0.45" fill="none"/>

  <circle cx="458" cy="452" r="5" fill="#FF3BD4" filter="url(#neonGlow)"/>
  <circle cx="820" cy="452" r="5" fill="#6BF7FF" filter="url(#neonGlow)"/>
  <circle cx="640" cy="608" r="6" fill="#FFD166" filter="url(#neonGlow)"/>

  <rect x="382" y="202" width="516" height="154" rx="28" fill="#020514" opacity="0.5" filter="url(#cardShadow)"/>
  <rect x="390" y="194" width="500" height="150" rx="26" fill="url(#cardFill)" stroke="#6BF7FF" stroke-width="1.4" opacity="0.96"/>
  <rect x="420" y="218" width="440" height="5" rx="2.5" fill="url(#accentBar)"/>
  <rect x="420" y="244" width="112" height="28" rx="14" fill="#FF3BD4" opacity="0.18" stroke="#FF3BD4" stroke-width="1"/>

  <text x="438" y="264" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700"
        letter-spacing="2.5" fill="#FFB7EA">SECTION 03</text>

  <text x="420" y="312" width="440" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="800"
        letter-spacing="-0.5" fill="#FFFFFF" filter="url(#textGlow)">Signal Architecture</text>

  <text x="423" y="334" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        letter-spacing="2" fill="#8DEEFF" opacity="0.8">SYSTEM MAP · NEXT-GEN OPERATING MODEL</text>
</svg>
```

## Avoid in this skill
- ❌ Real SVG animation such as `<animate>` or `<animateTransform>`; imply motion with repeated glowing grid lines, streaks, and dashed scanline accents instead.
- ❌ `marker-end` arrows on perspective paths; arrowheads are not needed and can disappear in translation.
- ❌ Applying filters to `<line>` elements; use stroked `<path>` elements for glowing grid rays and bands.
- ❌ Using a raster image for the grid; keep the grid as editable paths so the vanishing point, density, and colors can be adjusted in PowerPoint.
- ❌ Skew or matrix transforms for perspective; explicitly draw the ray and band coordinates.

## Composition notes
- Keep the vanishing point near the horizontal center, slightly below mid-slide; this makes the grid feel cinematic while leaving room for the title card.
- The title card should float above the horizon, not touch the grid, with enough glow and shadow to separate it from the busy lines.
- Use a dark blue / violet background with cyan, magenta, and occasional amber accents for a retro-futuristic rhythm.
- Reserve the upper corners for sparse scanline details only; the main visual energy should converge toward the title and horizon.