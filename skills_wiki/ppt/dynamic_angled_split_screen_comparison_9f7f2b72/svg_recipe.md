# SVG Recipe — Dynamic Angled Split-Screen Comparison

## Visual mechanism
A high-energy comparison slide built from a diagonal split: one side is dark and solid, the other is light with a technical grid texture. Oversized circular metric badges sit in each half, turning the split into a dramatic A/B data comparison rather than a static two-column layout.

## SVG primitives needed
- 1× `<rect>` for the full-slide light cyan base background
- 1× `<linearGradient>` for subtle right-side depth
- 1× `<path>` for the dark angled left trapezoid
- 1× `<path>` for the bright diagonal separator stripe
- 18–28× `<line>` for the manually drawn grid texture on the right side
- 8–12× `<rect>` for translucent floating technical squares
- 2× `<circle>` for the large metric callout badges
- 2× `<circle>` for thin accent rings around the badges
- 1× `<filter id="badgeShadow">` applied to metric circles
- 1× `<filter id="softGlow">` applied to accent circles / separator
- Multiple `<text>` elements with explicit `width` for headings, labels, and metric values

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="rightCyanDepth" x1="560" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#8FE6E2"/>
      <stop offset="0.55" stop-color="#7DCAC8"/>
      <stop offset="1" stop-color="#5FB4B7"/>
    </linearGradient>

    <linearGradient id="separatorGrad" x1="590" y1="650" x2="735" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.85"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="1" stop-color="#DDFEFF" stop-opacity="0.9"/>
    </linearGradient>

    <filter id="badgeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <!-- Right side base: draw first so the left trapezoid can cover the grid cleanly -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#rightCyanDepth)"/>

  <!-- Manual grid texture, intentionally oversized; dark trapezoid masks it by covering it -->
  <line x1="600" y1="0" x2="600" y2="720" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1"/>
  <line x1="660" y1="0" x2="660" y2="720" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1"/>
  <line x1="720" y1="0" x2="720" y2="720" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1"/>
  <line x1="780" y1="0" x2="780" y2="720" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1"/>
  <line x1="840" y1="0" x2="840" y2="720" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1"/>
  <line x1="900" y1="0" x2="900" y2="720" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1"/>
  <line x1="960" y1="0" x2="960" y2="720" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1"/>
  <line x1="1020" y1="0" x2="1020" y2="720" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1"/>
  <line x1="1080" y1="0" x2="1080" y2="720" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1"/>
  <line x1="1140" y1="0" x2="1140" y2="720" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1"/>
  <line x1="1200" y1="0" x2="1200" y2="720" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1"/>

  <line x1="0" y1="80" x2="1280" y2="80" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1"/>
  <line x1="0" y1="140" x2="1280" y2="140" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1"/>
  <line x1="0" y1="200" x2="1280" y2="200" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1"/>
  <line x1="0" y1="260" x2="1280" y2="260" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1"/>
  <line x1="0" y1="320" x2="1280" y2="320" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1"/>
  <line x1="0" y1="380" x2="1280" y2="380" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1"/>
  <line x1="0" y1="440" x2="1280" y2="440" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1"/>
  <line x1="0" y1="500" x2="1280" y2="500" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1"/>
  <line x1="0" y1="560" x2="1280" y2="560" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1"/>
  <line x1="0" y1="620" x2="1280" y2="620" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1"/>

  <!-- Right-side floating technical tiles -->
  <rect x="1018" y="92" width="58" height="58" rx="8" fill="#FFFFFF" opacity="0.16" transform="rotate(12 1047 121)"/>
  <rect x="1110" y="168" width="34" height="34" rx="6" fill="#FFFFFF" opacity="0.20" transform="rotate(-16 1127 185)"/>
  <rect x="970" y="518" width="70" height="70" rx="10" fill="#FFFFFF" opacity="0.13" transform="rotate(-10 1005 553)"/>
  <rect x="1182" y="430" width="42" height="42" rx="7" fill="#FFFFFF" opacity="0.18" transform="rotate(18 1203 451)"/>
  <rect x="760" y="560" width="28" height="28" rx="5" fill="#003B4A" opacity="0.10" transform="rotate(10 774 574)"/>

  <!-- Dark left trapezoid -->
  <path d="M 0 0 L 724 0 L 558 720 L 0 720 Z" fill="#0C3B4A"/>

  <!-- Subtle left-side angular overlays -->
  <path d="M 0 0 L 295 0 L 210 720 L 0 720 Z" fill="#082D39" opacity="0.45"/>
  <path d="M 105 580 L 410 470 L 360 720 L 52 720 Z" fill="#1D6675" opacity="0.22"/>
  <rect x="84" y="116" width="56" height="56" rx="8" fill="#FFFFFF" opacity="0.07" transform="rotate(-14 112 144)"/>
  <rect x="500" y="96" width="36" height="36" rx="5" fill="#00BFFF" opacity="0.16" transform="rotate(17 518 114)"/>
  <rect x="172" y="468" width="42" height="42" rx="6" fill="#FFFFFF" opacity="0.08" transform="rotate(12 193 489)"/>

  <!-- Bright diagonal separator -->
  <path d="M 704 -18 L 744 -18 L 586 738 L 546 738 Z" fill="url(#separatorGrad)" filter="url(#softGlow)"/>
  <path d="M 736 0 L 748 0 L 590 720 L 578 720 Z" fill="#00BFFF" opacity="0.35"/>

  <!-- Left metric badge -->
  <circle cx="372" cy="382" r="143" fill="#071F27" opacity="0.92" filter="url(#badgeShadow)"/>
  <circle cx="372" cy="382" r="156" fill="none" stroke="#00BFFF" stroke-width="4" opacity="0.75"/>
  <circle cx="372" cy="382" r="122" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-opacity="0.18"/>

  <!-- Right metric badge -->
  <circle cx="898" cy="338" r="143" fill="#F3FFFF" opacity="0.96" filter="url(#badgeShadow)"/>
  <circle cx="898" cy="338" r="156" fill="none" stroke="#3CB371" stroke-width="4" opacity="0.85"/>
  <circle cx="898" cy="338" r="122" fill="none" stroke="#0C3B4A" stroke-width="1.5" stroke-opacity="0.12"/>

  <!-- Header labels -->
  <text x="66" y="62" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" letter-spacing="2.8" fill="#8DEEFF">
    CURRENT STATE
  </text>
  <text x="820" y="62" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" letter-spacing="2.8" fill="#0C3B4A" text-anchor="middle">
    TARGET STATE
  </text>

  <!-- Left metric text -->
  <text x="372" y="364" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="800" fill="#FFFFFF" text-anchor="middle">
    26%
  </text>
  <text x="372" y="418" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" letter-spacing="2.3" fill="#8DEEFF" text-anchor="middle">
    DROPPED THIS YEAR
  </text>

  <!-- Right metric text -->
  <text x="898" y="320" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="800" fill="#0C3B4A" text-anchor="middle">
    74%
  </text>
  <text x="898" y="374" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" letter-spacing="2.3" fill="#2E8B57" text-anchor="middle">
    GAINED THIS YEAR
  </text>

  <!-- Supporting comparison copy -->
  <text x="70" y="642" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="400" fill="#CFEFF4">
    Legacy channel performance is compressing under price pressure and slower conversion cycles.
  </text>
  <text x="802" y="642" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#083847">
    New digital motion captures the upside with faster activation and higher retention.
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for the grid texture; PPT translation may drop pattern fills, so draw the grid manually with native `<line>` elements.
- ❌ `clip-path` on grid lines or decorative rectangles; clipping is reliable for `<image>` only, so use layer order instead.
- ❌ `skewX`, `skewY`, or matrix transforms for angled panels; create the diagonal using explicit `<path>` coordinates.
- ❌ `filter` on `<line>` elements for glowing grid strokes; filters on lines may be dropped. Apply glow to filled paths or circles instead.
- ❌ Arrow markers or inherited `marker-end`; this comparison style does not need arrows, and path markers can disappear.

## Composition notes
- Keep the diagonal split decisive: top split around 56–58% of slide width, bottom split around 43–45% to create motion.
- Use one large circular metric per side; each badge should occupy roughly 35–45% of slide height.
- Make the dark side heavier and calmer, then let the light side carry texture, grid lines, and more ambient detail.
- Reserve the lower corners for one-sentence interpretation copy; do not crowd the diagonal separator or metric badges.