# SVG Recipe — Animated Reveal Cards

## Visual mechanism
A bullet list becomes a row of modular “reveal” cards: each item has a bright top tab, a dark explanatory drawer, and a white icon footer that appears to slide downward. In PowerPoint, animate the footer moving down while the body wipes from the top to create the expanding-card illusion.

## SVG primitives needed
- 1× `<rect>` for the light gray slide background
- 1× `<rect>` for the dark executive title banner
- 4× `<path>` for top-rounded colored card headers
- 4× `<rect>` for dark body reveal panels
- 4× `<path>` for bottom-rounded white footer blocks
- 4× `<rect>` for thin colored separator strips under the headers
- 4× `<text>` for header labels
- 4× `<text>` with nested `<tspan>` for body copy
- 4× icon clusters made from `<circle>`, `<line>`, and `<path>` primitives
- 1× `<filter id="cardShadow">` applied to each full card group for depth
- 1× `<filter id="softGlow">` applied to small accent circles for premium polish
- Multiple `<linearGradient>` fills for the banner, body panels, and colored headers

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7f7f7"/>
      <stop offset="100%" stop-color="#e9ecef"/>
    </linearGradient>
    <linearGradient id="bannerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2f3437"/>
      <stop offset="70%" stop-color="#464646"/>
      <stop offset="100%" stop-color="#5a5f62"/>
    </linearGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#333b3e"/>
      <stop offset="100%" stop-color="#252b2d"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#45bfca"/>
      <stop offset="100%" stop-color="#2792a3"/>
    </linearGradient>
    <linearGradient id="orangeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff9b2f"/>
      <stop offset="100%" stop-color="#d86800"/>
    </linearGradient>
    <linearGradient id="purpleGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8465a0"/>
      <stop offset="100%" stop-color="#584171"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#9ac35d"/>
      <stop offset="100%" stop-color="#6f9c39"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="42" width="1280" height="88" fill="url(#bannerGrad)"/>
  <text x="90" y="97" width="850" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#ffffff">Strategic Growth Pillars</text>
  <text x="930" y="95" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#d7dee2" text-anchor="end">Expandable reveal-card layout</text>

  <g transform="translate(155 208)" filter="url(#cardShadow)">
    <path d="M22 0 H168 Q190 0 190 22 V76 H0 V22 Q0 0 22 0 Z" fill="url(#tealGrad)"/>
    <rect x="0" y="76" width="190" height="218" fill="url(#bodyGrad)"/>
    <rect x="0" y="76" width="190" height="5" fill="#39a0ad"/>
    <path d="M0 294 H190 V348 Q190 370 168 370 H22 Q0 370 0 348 Z" fill="#ffffff"/>
    <text x="95" y="48" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">Focus</text>
    <text x="95" y="128" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#eef5f6">
      <tspan x="95" dy="0">Concentrate capital,</tspan>
      <tspan x="95" dy="24">talent, and attention</tspan>
      <tspan x="95" dy="24">on the few markets</tspan>
      <tspan x="95" dy="24">where we can win.</tspan>
    </text>
    <circle cx="95" cy="332" r="27" fill="#e7f7f8"/>
    <circle cx="95" cy="332" r="13" fill="#39a0ad"/>
    <circle cx="95" cy="332" r="36" fill="#39a0ad" opacity="0.16" filter="url(#softGlow)"/>
    <line x1="95" y1="301" x2="95" y2="317" stroke="#39a0ad" stroke-width="4" stroke-linecap="round"/>
    <line x1="95" y1="347" x2="95" y2="363" stroke="#39a0ad" stroke-width="4" stroke-linecap="round"/>
  </g>

  <g transform="translate(390 208)" filter="url(#cardShadow)">
    <path d="M22 0 H168 Q190 0 190 22 V76 H0 V22 Q0 0 22 0 Z" fill="url(#orangeGrad)"/>
    <rect x="0" y="76" width="190" height="218" fill="url(#bodyGrad)"/>
    <rect x="0" y="76" width="190" height="5" fill="#e67300"/>
    <path d="M0 294 H190 V348 Q190 370 168 370 H22 Q0 370 0 348 Z" fill="#ffffff"/>
    <text x="95" y="48" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">Speed</text>
    <text x="95" y="128" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#fff4e8">
      <tspan x="95" dy="0">Shorten the path</tspan>
      <tspan x="95" dy="24">from signal to launch</tspan>
      <tspan x="95" dy="24">with tighter cycles</tspan>
      <tspan x="95" dy="24">and clear owners.</tspan>
    </text>
    <circle cx="95" cy="332" r="27" fill="#fff0df"/>
    <path d="M83 346 L98 332 L88 332 L104 316 L102 328 L113 328 Z" fill="#e67300"/>
    <circle cx="95" cy="332" r="36" fill="#e67300" opacity="0.14" filter="url(#softGlow)"/>
    <line x1="70" y1="332" x2="80" y2="332" stroke="#e67300" stroke-width="4" stroke-linecap="round"/>
    <line x1="110" y1="332" x2="120" y2="332" stroke="#e67300" stroke-width="4" stroke-linecap="round"/>
  </g>

  <g transform="translate(625 208)" filter="url(#cardShadow)">
    <path d="M22 0 H168 Q190 0 190 22 V76 H0 V22 Q0 0 22 0 Z" fill="url(#purpleGrad)"/>
    <rect x="0" y="76" width="190" height="218" fill="url(#bodyGrad)"/>
    <rect x="0" y="76" width="190" height="5" fill="#644b7d"/>
    <path d="M0 294 H190 V348 Q190 370 168 370 H22 Q0 370 0 348 Z" fill="#ffffff"/>
    <text x="95" y="48" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">Insight</text>
    <text x="95" y="128" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#f3edf8">
      <tspan x="95" dy="0">Translate customer</tspan>
      <tspan x="95" dy="24">behavior into sharper</tspan>
      <tspan x="95" dy="24">decisions, messaging,</tspan>
      <tspan x="95" dy="24">and product bets.</tspan>
    </text>
    <circle cx="95" cy="332" r="27" fill="#f1eaf7"/>
    <path d="M78 333 Q95 306 112 333 Q95 355 78 333 Z" fill="none" stroke="#644b7d" stroke-width="5"/>
    <circle cx="95" cy="333" r="7" fill="#644b7d"/>
    <circle cx="95" cy="332" r="36" fill="#644b7d" opacity="0.14" filter="url(#softGlow)"/>
  </g>

  <g transform="translate(860 208)" filter="url(#cardShadow)">
    <path d="M22 0 H168 Q190 0 190 22 V76 H0 V22 Q0 0 22 0 Z" fill="url(#greenGrad)"/>
    <rect x="0" y="76" width="190" height="218" fill="url(#bodyGrad)"/>
    <rect x="0" y="76" width="190" height="5" fill="#78a53c"/>
    <path d="M0 294 H190 V348 Q190 370 168 370 H22 Q0 370 0 348 Z" fill="#ffffff"/>
    <text x="95" y="48" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">Scale</text>
    <text x="95" y="128" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#f2f8ea">
      <tspan x="95" dy="0">Codify what works</tspan>
      <tspan x="95" dy="24">into repeatable plays</tspan>
      <tspan x="95" dy="24">that teams can adopt</tspan>
      <tspan x="95" dy="24">without friction.</tspan>
    </text>
    <circle cx="95" cy="332" r="27" fill="#edf6e4"/>
    <path d="M80 345 V326 L95 316 L110 326 V345 Z" fill="none" stroke="#78a53c" stroke-width="5" stroke-linejoin="round"/>
    <line x1="95" y1="316" x2="95" y2="345" stroke="#78a53c" stroke-width="5" stroke-linecap="round"/>
    <circle cx="95" cy="332" r="36" fill="#78a53c" opacity="0.14" filter="url(#softGlow)"/>
  </g>

  <text x="640" y="635" width="850" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#727a7e">Animation build: footer moves down while the dark body wipes from top, creating a physical drawer reveal.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the reveal; PowerPoint animation should be applied after translation.
- ❌ Do not rely on `<mask>` to hide/reveal the body panel; masks can hard-fail or translate poorly.
- ❌ Do not use `clip-path` on rectangles or paths for the wipe area; clipping is reliable only on `<image>` elements.
- ❌ Do not create arrows with `marker-end` on paths; if motion cues are needed, use separate editable `<line>` elements.
- ❌ Do not use `<use>` to duplicate card parts; repeat the editable shapes explicitly so each card remains independent in PowerPoint.

## Composition notes
- Keep the four cards horizontally centered with generous gutters; the row should occupy roughly 70–75% of slide width.
- The title banner anchors the slide and prevents the colorful cards from feeling like floating UI widgets.
- Use vivid header colors, but keep all body panels the same dark slate to maintain list consistency.
- For the PowerPoint reveal, group each card’s footer icon/footer block separately from the header and body so the footer can slide down independently.