# SVG Recipe — Holographic Player Card Timeline

## Visual mechanism
A premium “collectible card” becomes the hero chart marker, combining a clipped portrait, metallic typography, curved foil swooshes, and layered shadows. The surrounding field-like background and yard-line timeline turn the card into a milestone in a larger chronological story.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark field background
- 10–16× thin `<rect>` / `<line>` elements for yard lines, hash marks, and timeline structure
- 1× large `<path>` for the custom trading-card silhouette
- 5–8× `<path>` elements for curved holographic swooshes, diagonal foil panels, and corner accents
- 1× clipped `<image>` for the player / subject portrait inside the card
- 1× clipped `<image>` for the team / brand logo badge
- 6–8× `<circle>` / `<ellipse>` elements for timeline nodes, glow halos, and badge backing
- Multiple `<text>` elements with explicit `width` attributes for player name, milestones, stats, and annotations
- 3× `<linearGradient>` definitions for field depth, holographic foil, and metallic gold text
- 1× `<radialGradient>` for soft vignette lighting
- 2× `<filter>` definitions: one drop shadow for the card body and one glow for foil accents / active timeline nodes
- 2× `<clipPath>` definitions applied only to `<image>` elements for rounded portrait crop and circular logo crop

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="fieldGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#183b25"/>
      <stop offset="55%" stop-color="#244d2d"/>
      <stop offset="100%" stop-color="#102619"/>
    </linearGradient>
    <radialGradient id="vignette" cx="42%" cy="44%" r="72%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="68%" stop-color="#102619" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#020806" stop-opacity="0.62"/>
    </radialGradient>
    <linearGradient id="holo" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7fffd4"/>
      <stop offset="22%" stop-color="#7aa5ff"/>
      <stop offset="45%" stop-color="#ff77d9"/>
      <stop offset="67%" stop-color="#ffe66d"/>
      <stop offset="100%" stop-color="#8affc1"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff4b0"/>
      <stop offset="28%" stop-color="#d6a83a"/>
      <stop offset="55%" stop-color="#fff0a6"/>
      <stop offset="80%" stop-color="#9b6a16"/>
      <stop offset="100%" stop-color="#ffe38a"/>
    </linearGradient>
    <linearGradient id="cardRed" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ef2631"/>
      <stop offset="55%" stop-color="#b20e17"/>
      <stop offset="100%" stop-color="#63070d"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="foilGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
    <clipPath id="portraitClip">
      <rect x="142" y="90" width="218" height="286" rx="28"/>
    </clipPath>
    <clipPath id="logoClip">
      <circle cx="332" cy="438" r="40"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#fieldGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <line x1="70" y1="0" x2="70" y2="720" stroke="#ffffff" stroke-opacity="0.10" stroke-width="4"/>
  <line x1="210" y1="0" x2="210" y2="720" stroke="#ffffff" stroke-opacity="0.08" stroke-width="3"/>
  <line x1="350" y1="0" x2="350" y2="720" stroke="#ffffff" stroke-opacity="0.08" stroke-width="3"/>
  <line x1="490" y1="0" x2="490" y2="720" stroke="#ffffff" stroke-opacity="0.08" stroke-width="3"/>
  <line x1="630" y1="0" x2="630" y2="720" stroke="#ffffff" stroke-opacity="0.07" stroke-width="3"/>
  <line x1="770" y1="0" x2="770" y2="720" stroke="#ffffff" stroke-opacity="0.07" stroke-width="3"/>
  <line x1="910" y1="0" x2="910" y2="720" stroke="#ffffff" stroke-opacity="0.10" stroke-width="4"/>
  <rect x="1012" y="0" width="8" height="720" fill="#ffffff" opacity="0.78"/>
  <text x="1038" y="655" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="800" fill="#d5d9d8" opacity="0.55">50</text>

  <g transform="translate(92 76)">
    <path d="M58 12 H360 C386 12 406 33 406 60 V510 C406 538 384 560 356 560 H46 C20 560 0 539 0 513 V78 C0 44 25 19 58 12 Z"
          fill="url(#cardRed)" filter="url(#cardShadow)"/>
    <path d="M18 70 C84 38 130 34 188 46 C130 76 76 125 18 205 Z" fill="url(#holo)" opacity="0.88"/>
    <path d="M406 95 C332 132 298 188 286 262 C326 230 370 210 406 204 Z" fill="url(#holo)" opacity="0.72"/>
    <path d="M0 438 C78 384 150 372 238 398 C170 428 98 478 32 560 H0 Z" fill="url(#holo)" opacity="0.78"/>
    <path d="M56 32 H348 C371 32 386 47 386 70 V496 C386 519 370 538 346 538 H58 C34 538 18 520 18 496 V88 C18 60 32 40 56 32 Z"
          fill="none" stroke="#ffd56f" stroke-width="4" opacity="0.74"/>
    <path d="M38 238 C112 180 190 151 306 137" fill="none" stroke="url(#holo)" stroke-width="11" stroke-linecap="round" opacity="0.95" filter="url(#foilGlow)"/>
    <path d="M76 414 C150 374 232 350 364 346" fill="none" stroke="url(#holo)" stroke-width="8" stroke-linecap="round" opacity="0.88"/>
    <rect x="126" y="74" width="250" height="320" rx="34" fill="#14070a" opacity="0.68"/>
    <image href="https://images.example.com/sports-player-portrait-transparent-png.png" x="142" y="90" width="218" height="286" clip-path="url(#portraitClip)" preserveAspectRatio="xMidYMid slice"/>
    <rect x="142" y="90" width="218" height="286" rx="28" fill="none" stroke="#ffffff" stroke-opacity="0.62" stroke-width="3"/>
    <circle cx="332" cy="438" r="48" fill="#110609" opacity="0.88"/>
    <circle cx="332" cy="438" r="44" fill="url(#gold)"/>
    <image href="https://images.example.com/team-logo-round-emblem.png" x="292" y="398" width="80" height="80" clip-path="url(#logoClip)" preserveAspectRatio="xMidYMid slice"/>
    <text x="38" y="456" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="900" fill="url(#gold)" letter-spacing="1.2">ALEX RIVERS</text>
    <text x="42" y="492" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#ffffff" opacity="0.92">QB · FRANCHISE ERA</text>
    <text x="42" y="526" width="290" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#f4f0e9" opacity="0.86">3 titles · 71% completion · legacy score 98</text>
  </g>

  <rect x="598" y="96" width="330" height="74" rx="22" fill="#06130d" opacity="0.56"/>
  <text x="620" y="132" width="285" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="32" font-weight="850" fill="url(#gold)">PLAYER CARD TIMELINE</text>
  <text x="621" y="160" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#cfe0d4">Milestones mapped like yardage gains toward a championship moment.</text>

  <line x1="682" y1="238" x2="1016" y2="238" stroke="#ffffff" stroke-opacity="0.36" stroke-width="3" stroke-dasharray="10 12"/>
  <line x1="682" y1="360" x2="1016" y2="360" stroke="#ffffff" stroke-opacity="0.24" stroke-width="3" stroke-dasharray="10 12"/>
  <line x1="682" y1="482" x2="1016" y2="482" stroke="#ffffff" stroke-opacity="0.24" stroke-width="3" stroke-dasharray="10 12"/>

  <circle cx="682" cy="238" r="16" fill="url(#holo)" filter="url(#foilGlow)"/>
  <circle cx="682" cy="238" r="7" fill="#ffffff"/>
  <text x="715" y="226" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#ffffff">2016 · Draft Spark</text>
  <text x="715" y="252" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#cbd8cf">Breakout rookie season establishes the card’s origin story.</text>

  <circle cx="790" cy="360" r="13" fill="#ffffff" opacity="0.88"/>
  <circle cx="790" cy="360" r="7" fill="#1b5e39"/>
  <text x="823" y="348" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#ffffff">2019 · Prime Window</text>
  <text x="823" y="374" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#cbd8cf">Efficiency, leadership, and market attention converge.</text>

  <circle cx="906" cy="482" r="13" fill="#ffffff" opacity="0.88"/>
  <circle cx="906" cy="482" r="7" fill="#1b5e39"/>
  <text x="938" y="470" width="225" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#ffffff">2023 · Legacy Season</text>
  <text x="938" y="496" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#cbd8cf">The foil finish marks the highest-value chapter.</text>

  <rect x="610" y="590" width="390" height="52" rx="18" fill="#ffffff" opacity="0.10"/>
  <text x="632" y="622" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#ffffff">Use the card as the active timeline node; repeat on later slides for the next milestone.</text>
</svg>
```

## Avoid in this skill
- ❌ `<mask>` for the shiny foil reveal; use gradient-filled paths instead so the shapes remain editable.
- ❌ `<pattern>` for grass or holographic texture; approximate with gradients, transparent lines, and curved foil paths.
- ❌ Applying `clip-path` to the whole card group; clips should be used only on `<image>` elements.
- ❌ `marker-end` arrows on curved paths; timeline movement should be implied with dashed lines, circles, and spacing.
- ❌ Text without explicit `width`; card names and milestone labels need fixed text boxes for reliable PowerPoint rendering.

## Composition notes
- Keep the holographic card on the left 35–40% of the slide; it should feel like the collectible artifact anchoring the timeline.
- Reserve the right half for milestone labels, yard-line number, and a small explanatory caption with generous negative space.
- Use a dark green / black field base so the red card, gold type, and iridescent accents carry the visual rhythm.
- Let only one node glow strongly; this identifies the active moment while the other timeline events stay secondary.