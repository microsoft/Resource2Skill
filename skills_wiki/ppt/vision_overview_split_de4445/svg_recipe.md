# SVG Recipe — Vision Overview Split

## Visual mechanism
A balanced executive overview slide with a large central magnifying-glass metaphor acting as the “vision lens,” flanked by two opposing speech-bubble callouts. The composition uses low-density text, soft shadows, translucent gradients, and connector lines to imply two perspectives converging into one shared strategic view.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× large translucent `<circle>` / `<ellipse>` background accents for premium depth
- 2× `<path>` speech bubbles with organic tails pointing toward the center
- 1× `<circle>` for the magnifying-glass lens fill
- 1× `<circle>` for the magnifying-glass rim
- 1× `<path>` for the magnifying-glass handle
- 4× `<line>` elements for subtle inner lens axes and split connectors
- 5× small `<circle>` nodes inside the lens to suggest insight, data, or focus points
- 2× `<line>` connector strokes from callouts toward the central lens
- Multiple `<text>` elements with explicit `width` attributes for headline, subtitle, labels, and callout content
- 3× `<linearGradient>` definitions for background, lens, and accent styling
- 1× `<radialGradient>` definition for lens glow
- 1× `<filter id="softShadow">` for speech bubbles and lens
- 1× `<filter id="glow">` for central lens emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="55%" stop-color="#EEF4FB"/>
      <stop offset="100%" stop-color="#E7EEF8"/>
    </linearGradient>

    <linearGradient id="bubbleGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F4F8FE"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4F8DFF"/>
      <stop offset="100%" stop-color="#8F5CFF"/>
    </linearGradient>

    <radialGradient id="lensGrad" cx="45%" cy="38%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.96"/>
      <stop offset="55%" stop-color="#DCEBFF" stop-opacity="0.86"/>
      <stop offset="100%" stop-color="#AFCBFF" stop-opacity="0.68"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <circle cx="118" cy="98" r="92" fill="#7AA7FF" opacity="0.12"/>
  <ellipse cx="1158" cy="626" rx="150" ry="96" fill="#865CFF" opacity="0.10"/>
  <circle cx="1050" cy="110" r="9" fill="#4F8DFF" opacity="0.35"/>
  <circle cx="1084" cy="138" r="5" fill="#8F5CFF" opacity="0.34"/>
  <circle cx="206" cy="608" r="7" fill="#4F8DFF" opacity="0.28"/>

  <text x="170" y="74" width="940" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="700"
        fill="#172033">
    Vision Overview Split
  </text>
  <text x="270" y="116" width="740" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        fill="#607089">
    Two perspectives align through one focused strategic lens
  </text>

  <path d="M88 224
           C88 196 110 174 138 174
           L420 174
           C448 174 470 196 470 224
           L470 372
           C470 400 448 422 420 422
           L266 422
           L220 466
           C214 472 204 467 206 459
           L214 422
           L138 422
           C110 422 88 400 88 372 Z"
        fill="url(#bubbleGrad)" stroke="#D9E4F2" stroke-width="1.5" filter="url(#softShadow)"/>

  <path d="M1192 224
           C1192 196 1170 174 1142 174
           L860 174
           C832 174 810 196 810 224
           L810 372
           C810 400 832 422 860 422
           L1014 422
           L1060 466
           C1066 472 1076 467 1074 459
           L1066 422
           L1142 422
           C1170 422 1192 400 1192 372 Z"
        fill="url(#bubbleGrad)" stroke="#D9E4F2" stroke-width="1.5" filter="url(#softShadow)"/>

  <line x1="470" y1="304" x2="545" y2="330" stroke="#AFC0D6" stroke-width="2.5" stroke-dasharray="7 8"/>
  <line x1="810" y1="304" x2="735" y2="330" stroke="#AFC0D6" stroke-width="2.5" stroke-dasharray="7 8"/>

  <circle cx="640" cy="330" r="116" fill="#79A8FF" opacity="0.20" filter="url(#glow)"/>
  <circle cx="640" cy="330" r="98" fill="url(#lensGrad)" stroke="#3158A8" stroke-width="14" filter="url(#softShadow)"/>
  <circle cx="606" cy="294" r="28" fill="#FFFFFF" opacity="0.46"/>
  <path d="M710 398 L795 483
           C806 494 806 512 795 523
           C784 534 766 534 755 523
           L670 438 Z"
        fill="url(#accentGrad)" stroke="#244A96" stroke-width="6" stroke-linejoin="round"/>

  <line x1="586" y1="330" x2="694" y2="330" stroke="#6F8FCE" stroke-width="2" opacity="0.55"/>
  <line x1="640" y1="276" x2="640" y2="384" stroke="#6F8FCE" stroke-width="2" opacity="0.55"/>
  <line x1="598" y1="370" x2="684" y2="288" stroke="#7D68D8" stroke-width="2" opacity="0.35"/>
  <line x1="604" y1="292" x2="682" y2="374" stroke="#4F8DFF" stroke-width="2" opacity="0.35"/>

  <circle cx="610" cy="310" r="7" fill="#4F8DFF"/>
  <circle cx="672" cy="306" r="6" fill="#8F5CFF"/>
  <circle cx="640" cy="358" r="8" fill="#2CC7A3"/>
  <circle cx="596" cy="368" r="4.5" fill="#3158A8"/>
  <circle cx="690" cy="360" r="4.5" fill="#3158A8"/>

  <text x="128" y="224" width="290"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700"
        fill="#4F8DFF" letter-spacing="1.4">
    CURRENT SIGNALS
  </text>
  <text x="128" y="266" width="298"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="700"
        fill="#172033">
    Market clarity
  </text>
  <text x="128" y="304" width="298"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        fill="#5A687C">
    <tspan x="128" dy="0">Customer behavior, category</tspan>
    <tspan x="128" dy="27">shifts, and operating data</tspan>
    <tspan x="128" dy="27">reveal where momentum is</tspan>
    <tspan x="128" dy="27">already forming.</tspan>
  </text>

  <text x="862" y="224" width="290"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700"
        fill="#8F5CFF" letter-spacing="1.4">
    FUTURE INTENT
  </text>
  <text x="862" y="266" width="298"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="700"
        fill="#172033">
    Strategic focus
  </text>
  <text x="862" y="304" width="298"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        fill="#5A687C">
    <tspan x="862" dy="0">Leadership priorities define</tspan>
    <tspan x="862" dy="27">the future-state choices,</tspan>
    <tspan x="862" dy="27">capabilities, and bets that</tspan>
    <tspan x="862" dy="27">shape the roadmap.</tspan>
  </text>

  <rect x="492" y="560" width="296" height="50" rx="25" fill="#172033" opacity="0.92"/>
  <text x="518" y="592" width="244" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700"
        fill="#FFFFFF">
    Shared vision lens
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` for the magnifying-glass highlight; use translucent circles or ellipses instead.
- ❌ Do not put `filter` on connector `<line>` elements; shadows on lines may be dropped.
- ❌ Do not use `marker-end` for callout arrows; keep connectors as simple dashed or solid lines.
- ❌ Do not use `clip-path` on the lens or speech bubbles unless clipping an `<image>`; non-image clipping may be ignored.
- ❌ Avoid dense paragraphs inside the bubbles; this layout depends on low-density executive messaging.

## Composition notes
- Keep the magnifying glass centered around the slide’s visual midpoint, slightly below the title, so it anchors both callouts.
- Use left and right speech bubbles of equal size to create balance; their tails should angle inward toward the lens.
- Reserve the top 15–18% of the canvas for headline and subtitle, leaving generous negative space.
- Use one cool accent for the left callout and one violet/purple accent for the right callout, then blend both colors in the lens and handle.