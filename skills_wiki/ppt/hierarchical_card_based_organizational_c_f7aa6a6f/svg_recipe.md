# SVG Recipe — Hierarchical Card-Based Organizational Chart

## Visual mechanism
A top-down hierarchy is rendered as a set of polished UI cards instead of plain boxes: each card has a protruding circular avatar mount, a soft shadow, a colored hierarchy accent, and a small numbered ribbon tag. Dashed connector lines sit behind the cards, while color coding distinguishes executive, director, and manager levels.

## SVG primitives needed
- 1× `<rect>` for the pale slide background
- 2× large low-opacity `<circle>` / `<path>` decorative background accents
- 7× shadowed rounded `<rect>` for organizational card bodies
- 7× small accent `<rect>` strips on the left edge of each card
- 21× `<circle>` for avatar mounts: outer colored disk, inner white ring, and avatar head
- 7× `<path>` for avatar shoulder silhouettes
- 7× `<path>` for pentagon/ribbon number tags
- 16× `<line>` for dashed hierarchical connectors
- 22× `<text>` elements for title, node names, roles, and numeric tags
- 1× `<filter id="cardShadow">` applied to rounded card rectangles
- 3× `<linearGradient>` fills for subtle level-based avatar depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="9"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="purpleGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B26AD6"/>
      <stop offset="100%" stop-color="#8E44AD"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#44D9C4"/>
      <stop offset="100%" stop-color="#16A085"/>
    </linearGradient>
    <linearGradient id="redGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF7466"/>
      <stop offset="100%" stop-color="#E74C3C"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F9FC"/>
  <circle cx="1110" cy="105" r="160" fill="#ECE7FF" opacity="0.62"/>
  <path d="M-40,590 C115,505 210,620 345,540 C440,484 505,525 560,604 L560,760 L-40,760 Z" fill="#E8FAF6" opacity="0.7"/>

  <text x="0" y="58" width="1280" text-anchor="middle" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#2C3E50">Organizational Chart</text>
  <text x="0" y="91" width="1280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7A8794">Card-based leadership map with color-coded reporting layers</text>

  <!-- connectors behind cards -->
  <line x1="640" y1="208" x2="640" y2="252" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="400" y1="252" x2="880" y2="252" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="400" y1="252" x2="400" y2="300" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="880" y1="252" x2="880" y2="300" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="400" y1="384" x2="400" y2="444" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="230" y1="444" x2="530" y2="444" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="230" y1="444" x2="230" y2="500" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="530" y1="444" x2="530" y2="500" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="880" y1="384" x2="880" y2="444" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="830" y1="444" x2="1130" y2="444" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="830" y1="444" x2="830" y2="500" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>
  <line x1="1130" y1="444" x2="1130" y2="500" stroke="#B8C0CA" stroke-width="2" stroke-dasharray="7 7"/>

  <!-- CEO -->
  <rect x="480" y="120" width="320" height="88" rx="22" fill="#FFFFFF" stroke="#E4E9EF" filter="url(#cardShadow)"/>
  <rect x="480" y="142" width="7" height="44" rx="3.5" fill="#9B59B6"/>
  <circle cx="500" cy="164" r="38" fill="url(#purpleGrad)"/><circle cx="500" cy="164" r="27" fill="#FFFFFF"/><circle cx="500" cy="154" r="10" fill="#9B59B6"/><path d="M480,184 C484,169 516,169 520,184 Z" fill="#9B59B6"/>
  <path d="M735,110 L790,110 L800,128 L790,146 L735,146 Z" fill="#9B59B6"/>
  <text x="735" y="134" width="65" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">01</text>
  <text x="555" y="158" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#25313D">Maya Chen</text>
  <text x="555" y="184" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7F8C8D">Chief Executive Officer</text>

  <!-- Level 2 left -->
  <rect x="250" y="300" width="300" height="84" rx="20" fill="#FFFFFF" stroke="#E4E9EF" filter="url(#cardShadow)"/>
  <rect x="250" y="321" width="7" height="42" rx="3.5" fill="#E74C3C"/>
  <circle cx="270" cy="342" r="36" fill="url(#redGrad)"/><circle cx="270" cy="342" r="25" fill="#FFFFFF"/><circle cx="270" cy="333" r="9" fill="#E74C3C"/><path d="M252,362 C256,348 284,348 288,362 Z" fill="#E74C3C"/>
  <path d="M492,290 L540,290 L550,306 L540,322 L492,322 Z" fill="#E74C3C"/>
  <text x="492" y="313" width="58" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">02</text>
  <text x="320" y="337" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#25313D">Jon Bell</text>
  <text x="320" y="362" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#7F8C8D">VP, Sales & Growth</text>

  <!-- Level 2 right -->
  <rect x="730" y="300" width="300" height="84" rx="20" fill="#FFFFFF" stroke="#E4E9EF" filter="url(#cardShadow)"/>
  <rect x="730" y="321" width="7" height="42" rx="3.5" fill="#1ABC9C"/>
  <circle cx="750" cy="342" r="36" fill="url(#tealGrad)"/><circle cx="750" cy="342" r="25" fill="#FFFFFF"/><circle cx="750" cy="333" r="9" fill="#1ABC9C"/><path d="M732,362 C736,348 764,348 768,362 Z" fill="#1ABC9C"/>
  <path d="M972,290 L1020,290 L1030,306 L1020,322 L972,322 Z" fill="#1ABC9C"/>
  <text x="972" y="313" width="58" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">03</text>
  <text x="800" y="337" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#25313D">Sofia Patel</text>
  <text x="800" y="362" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#7F8C8D">VP, Product & Design</text>

  <!-- Level 3 cards -->
  <rect x="100" y="500" width="260" height="82" rx="19" fill="#FFFFFF" stroke="#E4E9EF" filter="url(#cardShadow)"/>
  <rect x="100" y="521" width="7" height="40" rx="3.5" fill="#F39C12"/>
  <circle cx="118" cy="541" r="34" fill="#F39C12"/><circle cx="118" cy="541" r="24" fill="#FFFFFF"/><circle cx="118" cy="532" r="8.5" fill="#F39C12"/><path d="M101,560 C105,548 131,548 135,560 Z" fill="#F39C12"/>
  <path d="M307,490 L350,490 L360,505 L350,520 L307,520 Z" fill="#F39C12"/>
  <text x="307" y="512" width="53" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">04</text>
  <text x="165" y="536" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16.5" font-weight="700" fill="#25313D">Lena Ortiz</text>
  <text x="165" y="559" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7F8C8D">Enterprise Sales</text>

  <rect x="400" y="500" width="260" height="82" rx="19" fill="#FFFFFF" stroke="#E4E9EF" filter="url(#cardShadow)"/>
  <rect x="400" y="521" width="7" height="40" rx="3.5" fill="#3498DB"/>
  <circle cx="418" cy="541" r="34" fill="#3498DB"/><circle cx="418" cy="541" r="24" fill="#FFFFFF"/><circle cx="418" cy="532" r="8.5" fill="#3498DB"/><path d="M401,560 C405,548 431,548 435,560 Z" fill="#3498DB"/>
  <path d="M607,490 L650,490 L660,505 L650,520 L607,520 Z" fill="#3498DB"/>
  <text x="607" y="512" width="53" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">05</text>
  <text x="465" y="536" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16.5" font-weight="700" fill="#25313D">Noah Park</text>
  <text x="465" y="559" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7F8C8D">Customer Success</text>

  <rect x="700" y="500" width="260" height="82" rx="19" fill="#FFFFFF" stroke="#E4E9EF" filter="url(#cardShadow)"/>
  <rect x="700" y="521" width="7" height="40" rx="3.5" fill="#2ECC71"/>
  <circle cx="718" cy="541" r="34" fill="#2ECC71"/><circle cx="718" cy="541" r="24" fill="#FFFFFF"/><circle cx="718" cy="532" r="8.5" fill="#2ECC71"/><path d="M701,560 C705,548 731,548 735,560 Z" fill="#2ECC71"/>
  <path d="M907,490 L950,490 L960,505 L950,520 L907,520 Z" fill="#2ECC71"/>
  <text x="907" y="512" width="53" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">06</text>
  <text x="765" y="536" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16.5" font-weight="700" fill="#25313D">Iris Wang</text>
  <text x="765" y="559" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7F8C8D">Product Strategy</text>

  <rect x="1000" y="500" width="260" height="82" rx="19" fill="#FFFFFF" stroke="#E4E9EF" filter="url(#cardShadow)"/>
  <rect x="1000" y="521" width="7" height="40" rx="3.5" fill="#5B7CFA"/>
  <circle cx="1018" cy="541" r="34" fill="#5B7CFA"/><circle cx="1018" cy="541" r="24" fill="#FFFFFF"/><circle cx="1018" cy="532" r="8.5" fill="#5B7CFA"/><path d="M1001,560 C1005,548 1031,548 1035,560 Z" fill="#5B7CFA"/>
  <path d="M1207,490 L1250,490 L1260,505 L1250,520 L1207,520 Z" fill="#5B7CFA"/>
  <text x="1207" y="512" width="53" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">07</text>
  <text x="1065" y="536" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16.5" font-weight="700" fill="#25313D">Owen Reed</text>
  <text x="1065" y="559" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7F8C8D">Design Systems</text>
</svg>
```

## Avoid in this skill
- ❌ Putting shadows or filters on connector `<line>` elements; keep connectors simple dashed lines.
- ❌ Using `<marker>` arrowheads on hierarchy connectors; PowerPoint translation can drop them, and org charts usually read cleaner without arrows.
- ❌ Using `<use>` to duplicate cards; repeat the editable shapes explicitly so every card remains reliable in PPT.
- ❌ Clipping non-image elements for the avatar mount; build the avatar from circles and paths instead.
- ❌ Overcrowding the card text; two lines per card is the practical limit for this compact hierarchy style.

## Composition notes
- Keep the CEO card centered in the upper third, with level-two cards symmetrically below and level-three cards aligned in a wide bottom row.
- Draw dashed connectors before cards so the card shadows and avatar mounts sit visually on top.
- Use white cards against a very pale background; let hierarchy colors appear only in avatar mounts, left accent strips, and number tags.
- Leave generous vertical space between levels so the connectors become part of the design rather than visual clutter.