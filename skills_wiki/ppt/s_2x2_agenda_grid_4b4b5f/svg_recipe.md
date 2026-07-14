# SVG Recipe — 2x2 Agenda Grid

## Visual mechanism
A premium agenda slide built from four large editorial cards in a 2×2 grid, each anchored by a prominent numbered badge and a short section title. Warm neutrals, soft shadows, ghost numerals, and organic accent shapes make the grid feel polished rather than mechanical.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm background.
- 4× `<rect>` for the rounded agenda cards with soft shadows.
- 4× `<circle>` for numbered badges.
- 4× large low-opacity `<text>` elements for ghost numerals inside each card.
- 12× `<text>` elements for title, eyebrow, card headings, and supporting agenda copy; every text element needs an explicit `width`.
- 6× decorative `<path>` blobs/sweeps for editorial warmth and asymmetry.
- 4× `<line>` elements for subtle card accent dividers.
- 2× `<linearGradient>` for background and badge/card accents.
- 1× `<radialGradient>` for ambient glow.
- 1× `<filter id="softShadow">` for card elevation.
- 1× `<filter id="glow">` for blurred decorative organic shapes.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8F1E6"/>
      <stop offset="55%" stop-color="#F5EADF"/>
      <stop offset="100%" stop-color="#EFE5DA"/>
    </linearGradient>

    <linearGradient id="badgeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#28221D"/>
      <stop offset="100%" stop-color="#6B4B35"/>
    </linearGradient>

    <radialGradient id="amberGlow" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#E9A75A" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#E9A75A" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.25  0 0 0 0 0.18  0 0 0 0 0.12  0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M1040,28 C1140,-22 1260,18 1306,118 C1346,204 1284,290 1184,278 C1072,264 984,194 976,112 C972,72 998,46 1040,28 Z"
        fill="url(#amberGlow)" filter="url(#glow)"/>
  <path d="M-50,522 C54,468 174,504 210,604 C244,700 136,766 18,728 C-70,700 -112,574 -50,522 Z"
        fill="#D9BFA7" opacity="0.22" filter="url(#glow)"/>
  <path d="M730,96 C816,58 930,76 972,138 C1014,200 944,244 856,222 C770,200 684,116 730,96 Z"
        fill="#A76F42" opacity="0.10"/>

  <text x="80" y="74" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.4" fill="#9B6A45">QUARTERLY OPERATING AGENDA</text>
  <text x="80" y="130" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="700" fill="#241E1A">Today’s discussion roadmap</text>
  <text x="82" y="160" width="540" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#76685F">Four focused conversations, sequenced from context to action.</text>

  <rect x="80" y="196" width="535" height="198" rx="30" fill="#FFFCF7" filter="url(#softShadow)"/>
  <path d="M512,196 C590,232 616,302 594,394 L440,394 C488,344 486,270 512,196 Z"
        fill="#EAC49A" opacity="0.22"/>
  <circle cx="127" cy="246" r="30" fill="url(#badgeGrad)"/>
  <text x="110" y="257" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" fill="#FFFFFF">01</text>
  <text x="454" y="356" width="116" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="112" font-weight="800" fill="#3B2F29" opacity="0.055">01</text>
  <text x="178" y="239" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" fill="#2A231F">Market context</text>
  <line x1="178" y1="263" x2="430" y2="263" stroke="#D8C7B6" stroke-width="2"/>
  <text x="178" y="300" width="335" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#74655A">Where demand, category behavior, and competitor movement are shifting.</text>

  <rect x="665" y="196" width="535" height="198" rx="30" fill="#FFFCF7" filter="url(#softShadow)"/>
  <path d="M675,356 C760,304 822,304 872,394 L665,394 L665,332 C668,340 671,348 675,356 Z"
        fill="#C77E56" opacity="0.16"/>
  <circle cx="712" cy="246" r="30" fill="url(#badgeGrad)"/>
  <text x="695" y="257" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" fill="#FFFFFF">02</text>
  <text x="1032" y="356" width="124" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="112" font-weight="800" fill="#3B2F29" opacity="0.055">02</text>
  <text x="763" y="239" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" fill="#2A231F">Customer insights</text>
  <line x1="763" y1="263" x2="1015" y2="263" stroke="#D8C7B6" stroke-width="2"/>
  <text x="763" y="300" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#74655A">What we learned from recent journeys, signals, interviews, and churn patterns.</text>

  <rect x="80" y="424" width="535" height="198" rx="30" fill="#FFFCF7" filter="url(#softShadow)"/>
  <path d="M64,462 C164,414 246,436 296,520 C334,584 268,638 174,610 C92,586 26,510 64,462 Z"
        fill="#8F6A50" opacity="0.12"/>
  <circle cx="127" cy="474" r="30" fill="url(#badgeGrad)"/>
  <text x="110" y="485" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" fill="#FFFFFF">03</text>
  <text x="454" y="584" width="124" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="112" font-weight="800" fill="#3B2F29" opacity="0.055">03</text>
  <text x="178" y="467" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" fill="#2A231F">Strategic choices</text>
  <line x1="178" y1="491" x2="430" y2="491" stroke="#D8C7B6" stroke-width="2"/>
  <text x="178" y="528" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#74655A">The few bets that matter most, with trade-offs, sequencing, and ownership.</text>

  <rect x="665" y="424" width="535" height="198" rx="30" fill="#FFFCF7" filter="url(#softShadow)"/>
  <path d="M1112,424 C1174,458 1206,520 1188,622 L1028,622 C1074,568 1076,494 1112,424 Z"
        fill="#D9A35F" opacity="0.20"/>
  <circle cx="712" cy="474" r="30" fill="url(#badgeGrad)"/>
  <text x="695" y="485" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" fill="#FFFFFF">04</text>
  <text x="1032" y="584" width="126" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="112" font-weight="800" fill="#3B2F29" opacity="0.055">04</text>
  <text x="763" y="467" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" fill="#2A231F">Next actions</text>
  <line x1="763" y1="491" x2="1015" y2="491" stroke="#D8C7B6" stroke-width="2"/>
  <text x="763" y="528" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#74655A">Decisions, owners, milestones, and the operating cadence for follow-through.</text>

  <path d="M82,666 C178,646 250,654 334,680" fill="none" stroke="#B88458" stroke-width="4" stroke-linecap="round" opacity="0.35"/>
</svg>
```

## Avoid in this skill
- ❌ Plain table borders only; it will look like a spreadsheet rather than an executive agenda.
- ❌ Putting long paragraphs in each quadrant; the 2×2 grid works best with one crisp heading and one supporting sentence per card.
- ❌ Using `<clipPath>` on card decorations; clipping only translates reliably on `<image>`, so keep decorative paths inside the card bounds or let them sit subtly behind content.
- ❌ Applying shadows to `<line>` dividers; filters on lines are dropped, so use simple low-contrast strokes.

## Composition notes
- Keep the slide title in the upper-left 20–25% of the canvas; the card grid should begin below it with generous breathing room.
- Use equal card sizes and consistent gaps, but break stiffness with organic accent paths and oversized translucent numerals.
- Number badges should align consistently near the upper-left of each card to create a fast scanning path.
- Use one dominant dark neutral, one warm accent family, and plenty of ivory background to preserve an editorial corporate tone.