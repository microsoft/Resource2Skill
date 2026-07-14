# SVG Recipe — Glowing Concentric Data Nodes

## Visual mechanism
A dark tech-textured background supports three evenly spaced bullseye nodes, each built from stacked concentric circles with cyan outer glow, dark depth shadows, and glossy blue radial fills. The title and labels stay centered to reinforce the precise “data dial” / futuristic control-panel feel.

## SVG primitives needed
- 1× `<rect>` for the deep radial-gradient slide background
- 30× `<path>` for staggered hexagonal background tiles and cyan circuit-like highlight seams
- 9× `<circle>` for the three concentric node stacks
- 3× `<text>` for the center node letters
- 2× `<text>` for the two-line premium title
- 4× `<rect>` for title underlines / overlines
- 1× `<image>` clipped into a circular mini signature/avatar accent
- 1× `<clipPath>` with `<circle>` for the round photo crop
- 3× `<radialGradient>` for glossy node fills
- 1× `<linearGradient>` for blue edge highlights
- 3× `<filter>` definitions for node glow, tile shadow, and text shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="45%" r="75%">
      <stop offset="0%" stop-color="#252a2d"/>
      <stop offset="58%" stop-color="#111417"/>
      <stop offset="100%" stop-color="#05070a"/>
    </radialGradient>
    <radialGradient id="outerNode" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#174d99"/>
      <stop offset="65%" stop-color="#0b357c"/>
      <stop offset="100%" stop-color="#041b4d"/>
    </radialGradient>
    <radialGradient id="midNode" cx="42%" cy="32%" r="72%">
      <stop offset="0%" stop-color="#20a7df"/>
      <stop offset="70%" stop-color="#0872b4"/>
      <stop offset="100%" stop-color="#043f82"/>
    </radialGradient>
    <radialGradient id="innerNode" cx="40%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#6ea1e5"/>
      <stop offset="70%" stop-color="#4778c6"/>
      <stop offset="100%" stop-color="#2d5aa7"/>
    </radialGradient>
    <linearGradient id="cyanEdge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#004cff"/>
      <stop offset="50%" stop-color="#00d9ff"/>
      <stop offset="100%" stop-color="#00145c"/>
    </linearGradient>
    <filter id="nodeGlow" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="13" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="tileShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="2" dy="3" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="avatarClip"><circle cx="1120" cy="575" r="49"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <g opacity="0.78" stroke="#06080a" stroke-width="2">
    <path d="M41 0 L122 0 L162 68 L122 136 L41 136 L0 68 Z" fill="#191c1f"/>
    <path d="M203 0 L284 0 L324 68 L284 136 L203 136 L162 68 Z" fill="#202326"/>
    <path d="M365 0 L446 0 L486 68 L446 136 L365 136 L324 68 Z" fill="#171a1d"/>
    <path d="M527 0 L608 0 L648 68 L608 136 L527 136 L486 68 Z" fill="#212427"/>
    <path d="M689 0 L770 0 L810 68 L770 136 L689 136 L648 68 Z" fill="#171a1d"/>
    <path d="M851 0 L932 0 L972 68 L932 136 L851 136 L810 68 Z" fill="#222528"/>
    <path d="M1013 0 L1094 0 L1134 68 L1094 136 L1013 136 L972 68 Z" fill="#191c1f"/>
    <path d="M1175 0 L1256 0 L1296 68 L1256 136 L1175 136 L1134 68 Z" fill="#202326"/>
    <path d="M122 136 L203 136 L243 204 L203 272 L122 272 L81 204 Z" fill="#171a1d" filter="url(#tileShadow)"/>
    <path d="M284 136 L365 136 L405 204 L365 272 L284 272 L243 204 Z" fill="#232629"/>
    <path d="M446 136 L527 136 L567 204 L527 272 L446 272 L405 204 Z" fill="#181b1e" filter="url(#tileShadow)"/>
    <path d="M608 136 L689 136 L729 204 L689 272 L608 272 L567 204 Z" fill="#24272a"/>
    <path d="M770 136 L851 136 L891 204 L851 272 L770 272 L729 204 Z" fill="#171a1d" filter="url(#tileShadow)"/>
    <path d="M932 136 L1013 136 L1053 204 L1013 272 L932 272 L891 204 Z" fill="#222528"/>
    <path d="M1094 136 L1175 136 L1215 204 L1175 272 L1094 272 L1053 204 Z" fill="#181b1e"/>
    <path d="M41 272 L122 272 L162 340 L122 408 L41 408 L0 340 Z" fill="#202326"/>
    <path d="M365 272 L446 272 L486 340 L446 408 L365 408 L324 340 Z" fill="#171a1d" filter="url(#tileShadow)"/>
    <path d="M527 272 L608 272 L648 340 L608 408 L527 408 L486 340 Z" fill="#232629"/>
    <path d="M689 272 L770 272 L810 340 L770 408 L689 408 L648 340 Z" fill="#181b1e"/>
    <path d="M851 272 L932 272 L972 340 L932 408 L851 408 L810 340 Z" fill="#222528" filter="url(#tileShadow)"/>
    <path d="M1013 272 L1094 272 L1134 340 L1094 408 L1013 408 L972 340 Z" fill="#171a1d"/>
    <path d="M203 408 L284 408 L324 476 L284 544 L203 544 L162 476 Z" fill="#181b1e"/>
    <path d="M527 408 L608 408 L648 476 L608 544 L527 544 L486 476 Z" fill="#202326" filter="url(#tileShadow)"/>
    <path d="M689 408 L770 408 L810 476 L770 544 L689 544 L648 476 Z" fill="#171a1d"/>
    <path d="M1013 408 L1094 408 L1134 476 L1094 544 L1013 544 L972 476 Z" fill="#222528"/>
  </g>

  <g fill="none" stroke="url(#cyanEdge)" stroke-width="5" opacity="0.9">
    <path d="M446 136 L486 68 L567 68 L608 136"/>
    <path d="M770 136 L810 68 L891 68 L932 136"/>
    <path d="M405 204 L446 272 L527 272"/>
    <path d="M729 204 L770 272 L851 272 L891 204"/>
    <path d="M486 340 L527 408 L608 408 L648 340"/>
    <path d="M648 476 L689 544 L770 544 L810 476"/>
  </g>

  <text x="640" y="68" width="560" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="56" font-weight="700" fill="#ffffff" stroke="#1b1b1b" stroke-width="1" filter="url(#textShadow)">SPINNING CIRCLES</text>
  <rect x="386" y="77" width="556" height="4" fill="#ffffff"/>
  <rect x="386" y="84" width="556" height="2" fill="#ffffff" opacity="0.85"/>
  <text x="640" y="150" width="360" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="56" font-weight="700" fill="#ffffff" stroke="#1b1b1b" stroke-width="1" filter="url(#textShadow)">TUTORIAL</text>
  <rect x="508" y="158" width="312" height="4" fill="#ffffff"/>
  <rect x="508" y="165" width="312" height="2" fill="#ffffff" opacity="0.85"/>

  <g transform="translate(230 360)">
    <circle cx="0" cy="0" r="148" fill="url(#outerNode)" stroke="#113a88" stroke-width="4" filter="url(#nodeGlow)"/>
    <circle cx="0" cy="0" r="119" fill="url(#midNode)" stroke="#66e8ff" stroke-width="2"/>
    <circle cx="0" cy="0" r="101" fill="url(#innerNode)" stroke="#92bdf6" stroke-width="2" filter="url(#tileShadow)"/>
    <path d="M-104 5 A105 105 0 0 1 52 -91" fill="none" stroke="#d9ffff" stroke-width="4" opacity="0.9"/>
    <text x="0" y="21" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="78" font-weight="800" fill="#ffffff">A</text>
  </g>

  <g transform="translate(640 360)">
    <circle cx="0" cy="0" r="148" fill="url(#outerNode)" stroke="#113a88" stroke-width="4" filter="url(#nodeGlow)"/>
    <circle cx="0" cy="0" r="119" fill="url(#midNode)" stroke="#66e8ff" stroke-width="2"/>
    <circle cx="0" cy="0" r="101" fill="url(#innerNode)" stroke="#92bdf6" stroke-width="2" filter="url(#tileShadow)"/>
    <path d="M-104 5 A105 105 0 0 1 52 -91" fill="none" stroke="#d9ffff" stroke-width="4" opacity="0.9"/>
    <text x="0" y="21" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="78" font-weight="800" fill="#ffffff">B</text>
  </g>

  <g transform="translate(1050 350)">
    <circle cx="0" cy="0" r="148" fill="url(#outerNode)" stroke="#113a88" stroke-width="4" filter="url(#nodeGlow)"/>
    <circle cx="0" cy="0" r="119" fill="url(#midNode)" stroke="#66e8ff" stroke-width="2"/>
    <circle cx="0" cy="0" r="101" fill="url(#innerNode)" stroke="#92bdf6" stroke-width="2" filter="url(#tileShadow)"/>
    <path d="M-104 5 A105 105 0 0 1 52 -91" fill="none" stroke="#d9ffff" stroke-width="4" opacity="0.9"/>
    <text x="0" y="21" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="78" font-weight="800" fill="#ffffff">C</text>
  </g>

  <image href="https://images.example.com/close-up-green-leaf-with-water-drops.jpg" x="1071" y="526" width="98" height="98" clip-path="url(#avatarClip)"/>
  <circle cx="1120" cy="575" r="50" fill="none" stroke="#0b0b0b" stroke-width="3"/>
  <text x="1120" y="655" width="210" text-anchor="middle" font-family="Georgia, serif" font-size="24" font-style="italic" fill="#ffffff" filter="url(#textShadow)">Designed by</text>
  <text x="1120" y="694" width="300" text-anchor="middle" font-family="Georgia, serif" font-size="25" font-style="italic" fill="#ffffff" filter="url(#textShadow)">EasyAnimation_PowerPoint</text>
</svg>
```

## Avoid in this skill
- ❌ `<pattern>` for the hex background; manually draw repeated editable hex paths instead.
- ❌ Applying `filter` to `<line>` elements for glowing seams; use stroked `<path>` segments so the effect translates reliably.
- ❌ SVG animation for the spinning circles; keep the slide static and add any Spin emphasis manually in PowerPoint if needed.
- ❌ `clip-path` on circles or groups; only clip the optional signature/avatar `<image>`.

## Composition notes
- Keep the three nodes horizontally aligned across the central band, with the middle node exactly on the slide centerline and equal optical spacing between nodes.
- Use the brightest cyan only as an accent: outer glows, hex seams, and thin ring highlights; let navy and dark gray dominate.
- Reserve the top 20–25% for the dramatic title and underlines so the nodes do not compete with the headline.
- The background should be busy but low-contrast; node glow and white lettering must remain the strongest visual hierarchy.