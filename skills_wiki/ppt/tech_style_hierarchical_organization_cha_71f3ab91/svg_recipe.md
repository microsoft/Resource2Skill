# SVG Recipe — Tech-Style Hierarchical Organization Chart

## Visual mechanism
A strict top-down org tree is restyled as a premium dark-mode technology dashboard: translucent rounded nodes glow with cyan borders, while orthogonal connector paths resemble illuminated circuit traces. The hierarchy remains conventional and readable, but the atmosphere comes from deep navy gradients, subtle gridlines, neon accents, and disciplined symmetry.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 2× `<radialGradient>` and 1× `<linearGradient>` for ambient background bloom and node fills
- 1× `<filter id="softGlow">` applied to connector paths and selected neon strokes
- 1× `<filter id="cardShadow">` applied to rounded node cards
- 1× `<path>` for faint circuit/grid background texture
- 2× `<path>` for decorative angular corner/circuit accents
- 3× `<path>` for main hierarchical orthogonal connector runs
- 13× `<rect>` for root, department, and team rounded-rectangle nodes
- 18× `<circle>` for small glowing connector terminals and status dots
- 13× `<text>` for node labels, each with explicit `width`
- 1× `<text>` for the slide title, with explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#070B16"/>
      <stop offset="55%" stop-color="#0E1730"/>
      <stop offset="100%" stop-color="#17243F"/>
    </linearGradient>
    <radialGradient id="cyanBloom" cx="50%" cy="38%" r="60%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.22"/>
      <stop offset="48%" stop-color="#006DFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#00152A" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="nodeFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1B315F" stop-opacity="0.94"/>
      <stop offset="100%" stop-color="#0D1832" stop-opacity="0.96"/>
    </linearGradient>
    <linearGradient id="rootFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#143D70"/>
      <stop offset="100%" stop-color="#091A38"/>
    </linearGradient>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cardShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="640" cy="318" rx="520" ry="280" fill="url(#cyanBloom)"/>
  <ellipse cx="1120" cy="120" rx="260" ry="150" fill="#225BFF" opacity="0.08"/>
  <ellipse cx="120" cy="650" rx="300" ry="160" fill="#00D6FF" opacity="0.07"/>

  <path d="M80 120 H1200 M80 200 H1200 M80 280 H1200 M80 360 H1200 M80 440 H1200 M80 520 H1200 M80 600 H1200
           M120 90 V645 M240 90 V645 M360 90 V645 M480 90 V645 M600 90 V645 M720 90 V645 M840 90 V645 M960 90 V645 M1080 90 V645"
        stroke="#6BDFFF" stroke-width="1" opacity="0.08" fill="none"/>
  <path d="M58 86 H176 V110 H224 M58 86 V174 H92" stroke="#00BFFF" stroke-width="2" opacity="0.32" fill="none"/>
  <path d="M1222 632 H1098 V606 H1050 M1222 632 V544 H1188" stroke="#00BFFF" stroke-width="2" opacity="0.24" fill="none"/>

  <text x="640" y="58" width="920" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">
    TechNova Operating Structure
  </text>
  <text x="640" y="88" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8DDFFF" opacity="0.9">
    executive hierarchy · product-led organization · 2026
  </text>

  <path d="M640 184 V226 M640 226 H250 V272 M640 226 H510 V272 M640 226 H770 V272 M640 226 H1030 V272"
        stroke="#00BFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.92" filter="url(#softGlow)"/>
  <path d="M250 330 V392 M250 392 H170 V438 M250 392 H330 V438
           M510 330 V392 M510 392 H430 V438 M510 392 H590 V438"
        stroke="#00BFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.82"/>
  <path d="M770 330 V392 M770 392 H690 V438 M770 392 H850 V438
           M1030 330 V392 M1030 392 H950 V438 M1030 392 H1110 V438"
        stroke="#00BFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.82"/>

  <circle cx="640" cy="226" r="5" fill="#00E5FF" filter="url(#softGlow)"/>
  <circle cx="250" cy="392" r="4" fill="#00E5FF"/>
  <circle cx="510" cy="392" r="4" fill="#00E5FF"/>
  <circle cx="770" cy="392" r="4" fill="#00E5FF"/>
  <circle cx="1030" cy="392" r="4" fill="#00E5FF"/>

  <rect x="550" y="122" width="180" height="62" rx="18" fill="url(#rootFill)" stroke="#00D9FF" stroke-width="2.5" filter="url(#cardShadow)"/>
  <circle cx="574" cy="146" r="5" fill="#54F4FF"/>
  <text x="640" y="152" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">General Manager</text>
  <text x="640" y="174" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A9EFFF">Global Operations</text>

  <rect x="165" y="272" width="170" height="58" rx="15" fill="url(#nodeFill)" stroke="#00BFFF" stroke-width="2" filter="url(#cardShadow)"/>
  <rect x="425" y="272" width="170" height="58" rx="15" fill="url(#nodeFill)" stroke="#00BFFF" stroke-width="2" filter="url(#cardShadow)"/>
  <rect x="685" y="272" width="170" height="58" rx="15" fill="url(#nodeFill)" stroke="#00BFFF" stroke-width="2" filter="url(#cardShadow)"/>
  <rect x="945" y="272" width="170" height="58" rx="15" fill="url(#nodeFill)" stroke="#00BFFF" stroke-width="2" filter="url(#cardShadow)"/>

  <text x="250" y="303" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Growth</text>
  <text x="250" y="322" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#A7EFFF">Marketing & Sales</text>
  <text x="510" y="303" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Operations</text>
  <text x="510" y="322" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#A7EFFF">Supply & Delivery</text>
  <text x="770" y="303" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">R&amp;D</text>
  <text x="770" y="322" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#A7EFFF">Platform Innovation</text>
  <text x="1030" y="303" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">People</text>
  <text x="1030" y="322" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#A7EFFF">Talent Systems</text>

  <rect x="106" y="438" width="128" height="48" rx="13" fill="#111F3E" stroke="#39DFFF" stroke-width="1.6"/>
  <rect x="266" y="438" width="128" height="48" rx="13" fill="#111F3E" stroke="#39DFFF" stroke-width="1.6"/>
  <rect x="366" y="438" width="128" height="48" rx="13" fill="#111F3E" stroke="#39DFFF" stroke-width="1.6"/>
  <rect x="526" y="438" width="128" height="48" rx="13" fill="#111F3E" stroke="#39DFFF" stroke-width="1.6"/>
  <rect x="626" y="438" width="128" height="48" rx="13" fill="#111F3E" stroke="#39DFFF" stroke-width="1.6"/>
  <rect x="786" y="438" width="128" height="48" rx="13" fill="#111F3E" stroke="#39DFFF" stroke-width="1.6"/>
  <rect x="886" y="438" width="128" height="48" rx="13" fill="#111F3E" stroke="#39DFFF" stroke-width="1.6"/>
  <rect x="1046" y="438" width="128" height="48" rx="13" fill="#111F3E" stroke="#39DFFF" stroke-width="1.6"/>

  <text x="170" y="468" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">Demand Gen</text>
  <text x="330" y="468" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">Enterprise</text>
  <text x="430" y="468" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">Sourcing</text>
  <text x="590" y="468" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">Delivery</text>
  <text x="690" y="468" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">AI Lab</text>
  <text x="850" y="468" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">Security</text>
  <text x="950" y="468" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">Recruiting</text>
  <text x="1110" y="468" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">Culture Ops</text>

  <circle cx="170" cy="438" r="3.5" fill="#00E5FF"/><circle cx="330" cy="438" r="3.5" fill="#00E5FF"/>
  <circle cx="430" cy="438" r="3.5" fill="#00E5FF"/><circle cx="590" cy="438" r="3.5" fill="#00E5FF"/>
  <circle cx="690" cy="438" r="3.5" fill="#00E5FF"/><circle cx="850" cy="438" r="3.5" fill="#00E5FF"/>
  <circle cx="950" cy="438" r="3.5" fill="#00E5FF"/><circle cx="1110" cy="438" r="3.5" fill="#00E5FF"/>
</svg>
```

## Avoid in this skill
- ❌ SmartArt-like auto-layout assumptions; compute every node and connector coordinate explicitly.
- ❌ `marker-end` arrowheads on connector paths; org charts need clean circuit elbows, not dropped arrow markers.
- ❌ Filters on `<line>` elements; use `<path>` for glowing connector runs if a glow is needed.
- ❌ Overcrowding leaf nodes with long job descriptions; keep each card to one strong label or two short lines.
- ❌ Bright white backgrounds or heavy gray boxes; the technique depends on dark depth plus cyan contrast.

## Composition notes
- Keep the root node centered in the upper third, with department nodes spread evenly across the middle row and leaf teams aligned in a lower row.
- Use generous horizontal spacing; the premium tech look comes from disciplined negative space around each glowing card.
- Let cyan appear in three places only: node borders, connector paths, and tiny terminal dots; this creates a controlled “circuit board” rhythm.
- Background texture should stay subtle—gridlines and ambient blooms must support the hierarchy, not compete with the labels.