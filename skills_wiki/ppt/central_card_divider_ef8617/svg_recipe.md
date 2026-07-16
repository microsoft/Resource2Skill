# SVG Recipe — Central Card Divider

## Visual mechanism
A large, centered rounded card anchors the slide, with a saturated top accent band acting as the visual divider and section label. The surrounding canvas stays airy, while soft shadows, subtle background blobs, and small decorative marks make the simple card feel polished and keynote-ready.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<rect>` for the main rounded central card
- 1× `<path>` for the rounded-top accent band on the card
- N× `<path>` for abstract background blobs and decorative strokes
- N× `<circle>` / `<ellipse>` for soft glows, dots, and accent ornaments
- N× `<rect>` for separators, small color chips, and label pills
- N× `<text>` with explicit `width` for section label, headline, subtitle, and metadata
- 2× `<linearGradient>` for premium background and accent-band fills
- 1× `<radialGradient>` for ambient glow
- 2× `<filter>` using blur / offset / merge for card shadow and soft glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F8F6FF"/>
      <stop offset="45%" stop-color="#F4F7FB"/>
      <stop offset="100%" stop-color="#EEF6F1"/>
    </linearGradient>

    <linearGradient id="bandGrad" x1="330" y1="138" x2="950" y2="250">
      <stop offset="0%" stop-color="#6D5DF6"/>
      <stop offset="52%" stop-color="#FF6A88"/>
      <stop offset="100%" stop-color="#FFB84D"/>
    </linearGradient>

    <linearGradient id="chipGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B6F2D1"/>
      <stop offset="100%" stop-color="#4ED7A8"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="72%" stop-color="#FFFFFF" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="22" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.08  0 0 0 0 0.09  0 0 0 0 0.18  0 0 0 0.22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <ellipse cx="640" cy="356" rx="410" ry="250" fill="url(#ambientGlow)" opacity="0.78"/>
  <circle cx="242" cy="128" r="86" fill="#A9D8FF" opacity="0.32" filter="url(#softGlow)"/>
  <circle cx="1062" cy="590" r="112" fill="#FFD7A8" opacity="0.38" filter="url(#softGlow)"/>

  <path d="M108 493 C178 421 279 439 297 518 C313 588 239 642 166 621 C89 599 48 556 108 493 Z"
        fill="#D9D2FF" opacity="0.44"/>
  <path d="M1064 96 C1129 73 1193 113 1186 181 C1178 250 1106 280 1049 244 C993 209 999 119 1064 96 Z"
        fill="#FFE1A6" opacity="0.48"/>

  <path d="M228 246 C257 230 294 233 318 255"
        fill="none" stroke="#7B61FF" stroke-width="8" stroke-linecap="round" opacity="0.28"/>
  <path d="M1014 416 C1052 384 1111 391 1141 431"
        fill="none" stroke="#FF7A90" stroke-width="8" stroke-linecap="round" opacity="0.30"/>

  <rect x="330" y="138" width="620" height="444" rx="36" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="333" y="141" width="614" height="438" rx="33" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="2"/>

  <path d="M330 174
           Q330 138 366 138
           H914
           Q950 138 950 174
           V252
           H330
           Z"
        fill="url(#bandGrad)"/>

  <path d="M360 156 C450 129 559 151 638 183 C748 226 853 213 928 168 L950 168 L950 252 L330 252 L330 202 C338 183 345 166 360 156 Z"
        fill="#FFFFFF" opacity="0.13"/>

  <circle cx="406" cy="197" r="39" fill="#FFFFFF" opacity="0.16"/>
  <circle cx="858" cy="191" r="57" fill="#FFFFFF" opacity="0.13"/>
  <circle cx="890" cy="221" r="10" fill="#FFFFFF" opacity="0.42"/>
  <circle cx="378" cy="223" r="7" fill="#FFFFFF" opacity="0.45"/>

  <text x="385" y="189" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="2.5" fill="#FFFFFF" opacity="0.92">
    SECTION 04
  </text>
  <text x="385" y="224" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="800" fill="#FFFFFF">
    Investment Thesis
  </text>

  <rect x="768" y="175" width="108" height="34" rx="17" fill="#FFFFFF" opacity="0.20"/>
  <text x="792" y="198" width="72" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#FFFFFF">
    Q3 2026
  </text>

  <rect x="388" y="296" width="86" height="8" rx="4" fill="url(#chipGrad)"/>
  <rect x="486" y="296" width="42" height="8" rx="4" fill="#FFB84D"/>
  <rect x="540" y="296" width="26" height="8" rx="4" fill="#6D5DF6"/>

  <text x="388" y="363" width="504" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800" fill="#171827">
    <tspan x="388" dy="0">Building the next</tspan>
    <tspan x="388" dy="55" fill="#6D5DF6">growth platform</tspan>
  </text>

  <text x="390" y="468" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#5D6375">
    <tspan x="390" dy="0">A focused section divider for bold transitions, executive</tspan>
    <tspan x="390" dy="27">narratives, and low-density strategic storytelling.</tspan>
  </text>

  <rect x="390" y="526" width="154" height="38" rx="19" fill="#171827"/>
  <text x="415" y="551" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#FFFFFF">
    START SECTION
  </text>

  <rect x="800" y="518" width="88" height="8" rx="4" fill="#E8EAF3"/>
  <rect x="800" y="536" width="54" height="8" rx="4" fill="#E8EAF3"/>
  <circle cx="750" cy="534" r="24" fill="#F4F6FB"/>
  <path d="M739 535 L748 544 L763 523" fill="none" stroke="#4ED7A8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="335" cy="606" r="5" fill="#6D5DF6" opacity="0.55"/>
  <circle cx="360" cy="616" r="4" fill="#FFB84D" opacity="0.65"/>
  <circle cx="925" cy="112" r="5" fill="#FF6A88" opacity="0.60"/>
  <circle cx="956" cy="108" r="4" fill="#4ED7A8" opacity="0.65"/>
</svg>
```

## Avoid in this skill
- ❌ Using a `<mask>` to carve the accent band into the card; draw the rounded-top band directly as a `<path>` instead.
- ❌ Applying `clip-path` to the card or band shapes; clipping is only reliable for `<image>` elements.
- ❌ Building the central card from many overlapping opaque rectangles that create visible seams at the rounded corners.
- ❌ Putting shadows on `<line>` elements; use thin `<rect>` or `<path>` strokes for decorative dividers if a shadow/glow is needed.
- ❌ Overfilling the canvas with text or icons; the technique depends on a low-density, centered section-card composition.

## Composition notes
- Keep the card centered and dominant, occupying roughly 45–55% of slide width and 55–65% of slide height.
- Reserve the top 20–25% of the card for the colored accent band; it should read as a header divider, not a separate banner.
- Place the headline in the lower white area with generous margins; two short lines work better than a paragraph-heavy layout.
- Use background decoration sparingly at the outer corners so the viewer’s eye returns to the central card.