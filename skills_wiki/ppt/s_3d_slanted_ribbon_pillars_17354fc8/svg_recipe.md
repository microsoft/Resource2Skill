# SVG Recipe — 3D Slanted Ribbon Pillars

## Visual mechanism
Four tall ribbon-like pillars are drawn as slanted quadrilateral paths with vertical sides and diagonal top/bottom edges. Each pillar gets a darker triangular fold tucked under its lower-left corner plus a soft offset shadow, creating an editable pseudo-3D origami banner effect.

## SVG primitives needed
- 1× `<rect>` for the light executive-style slide background
- 4× `<path>` for the main slanted pillar bodies
- 4× `<path>` for the dark triangular folded ribbon corners
- 4× `<linearGradient>` for rich vertical pillar fills
- 1× `<filter id="pillarShadow">` using `feOffset + feGaussianBlur + feMerge` for lifted depth
- 1× `<filter id="softGlow">` using `feGaussianBlur` for a subtle background highlight
- 2× `<ellipse>` for soft ambient floor/glow accents
- 14× `<text>` for heading, subtitle, large translucent numbers, pillar titles, and descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="orangeGrad" x1="0" y1="170" x2="0" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ff8b42"/>
      <stop offset="52%" stop-color="#ff6730"/>
      <stop offset="100%" stop-color="#f13a00"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0" y1="170" x2="0" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#42d8e8"/>
      <stop offset="55%" stop-color="#18bad0"/>
      <stop offset="100%" stop-color="#0092ae"/>
    </linearGradient>
    <linearGradient id="limeGrad" x1="0" y1="170" x2="0" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#b6dc42"/>
      <stop offset="55%" stop-color="#91c82c"/>
      <stop offset="100%" stop-color="#64a914"/>
    </linearGradient>
    <linearGradient id="navyGrad" x1="0" y1="170" x2="0" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#66708d"/>
      <stop offset="55%" stop-color="#48546f"/>
      <stop offset="100%" stop-color="#28324f"/>
    </linearGradient>
    <radialGradient id="bgGlow" cx="50%" cy="42%" r="58%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#dfe3ea" stop-opacity="0"/>
    </radialGradient>
    <filter id="pillarShadow" x="-25%" y="-15%" width="150%" height="140%">
      <feOffset dx="10" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .28 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#eef1f5"/>
  <ellipse cx="640" cy="310" rx="520" ry="260" fill="url(#bgGlow)" filter="url(#softGlow)" opacity="0.9"/>
  <ellipse cx="640" cy="650" rx="440" ry="28" fill="#b9c0cc" opacity="0.28" filter="url(#softGlow)"/>

  <text x="95" y="78" width="1090" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="32" font-weight="700" fill="#222a38" letter-spacing="1.5">
    4 OPTIONS INFOGRAPHICS IN POWERPOINT
  </text>
  <text x="96" y="113" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#687181">
    Slanted ribbon pillars convert a basic list into a dimensional, forward-moving strategic narrative.
  </text>

  <g id="pillar-01">
    <path d="M 184 575 L 238 623 L 184 623 Z" fill="#982100"/>
    <path d="M 184 178 L 364 222 L 364 623 L 184 575 Z" fill="url(#orangeGrad)" filter="url(#pillarShadow)"/>
    <path d="M 184 178 L 364 222 L 364 255 L 184 211 Z" fill="#ffffff" opacity="0.14"/>
    <text x="203" y="270" width="145" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="800" fill="#ffffff" opacity="0.22">
      01
    </text>
    <text x="207" y="345" width="125" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff" letter-spacing="1">
      VISION
    </text>
    <text x="208" y="388" width="126" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#ffffff" opacity="0.86">
      Define the north star and align every team around measurable ambition.
    </text>
  </g>

  <g id="pillar-02">
    <path d="M 402 575 L 456 623 L 402 623 Z" fill="#00576a"/>
    <path d="M 402 178 L 582 222 L 582 623 L 402 575 Z" fill="url(#cyanGrad)" filter="url(#pillarShadow)"/>
    <path d="M 402 178 L 582 222 L 582 255 L 402 211 Z" fill="#ffffff" opacity="0.16"/>
    <text x="421" y="270" width="145" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="800" fill="#ffffff" opacity="0.22">
      02
    </text>
    <text x="425" y="345" width="125" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff" letter-spacing="1">
      SPEED
    </text>
    <text x="426" y="388" width="126" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#ffffff" opacity="0.86">
      Compress decision cycles while keeping execution precise, visible, and accountable.
    </text>
  </g>

  <g id="pillar-03">
    <path d="M 620 575 L 674 623 L 620 623 Z" fill="#355c0b"/>
    <path d="M 620 178 L 800 222 L 800 623 L 620 575 Z" fill="url(#limeGrad)" filter="url(#pillarShadow)"/>
    <path d="M 620 178 L 800 222 L 800 255 L 620 211 Z" fill="#ffffff" opacity="0.15"/>
    <text x="639" y="270" width="145" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="800" fill="#ffffff" opacity="0.22">
      03
    </text>
    <text x="643" y="345" width="125" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff" letter-spacing="1">
      TRUST
    </text>
    <text x="644" y="388" width="126" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#ffffff" opacity="0.86">
      Build confidence through transparent signals, clear ownership, and resilient delivery.
    </text>
  </g>

  <g id="pillar-04">
    <path d="M 838 575 L 892 623 L 838 623 Z" fill="#151a2b"/>
    <path d="M 838 178 L 1018 222 L 1018 623 L 838 575 Z" fill="url(#navyGrad)" filter="url(#pillarShadow)"/>
    <path d="M 838 178 L 1018 222 L 1018 255 L 838 211 Z" fill="#ffffff" opacity="0.12"/>
    <text x="857" y="270" width="145" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="800" fill="#ffffff" opacity="0.22">
      04
    </text>
    <text x="861" y="345" width="135" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff" letter-spacing="1">
      SCALE
    </text>
    <text x="862" y="388" width="126" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#ffffff" opacity="0.86">
      Turn proven motion into repeatable systems that grow without losing quality.
    </text>
  </g>

  <text x="1045" y="604" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="600" fill="#8891a0">
    EDITABLE SVG SHAPES
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using normal `<rect>` pillars only; the effect depends on custom slanted `<path>` geometry.
- ❌ Applying `clip-path` or `mask` to the ribbon shapes; use explicit path coordinates for the slants and folds.
- ❌ Putting the fold triangle on top of the main body in a bright color; it should be darker and tucked visually underneath.
- ❌ Using `marker-end` arrows or connector embellishments; they distract from the clean vertical ribbon system and may not translate reliably.
- ❌ Omitting `width` on `<text>` elements; PowerPoint text boxes need explicit width for predictable rendering.

## Composition notes
- Keep the four pillars centered and occupying roughly 70–78% of slide width, leaving generous margins for an executive keynote feel.
- Align all top-left and bottom-left vertices across pillars so the repeated slant reads as an intentional rhythm, not random skew.
- Place large translucent numbers near the upper third; titles should sit around mid-height, with compact descriptions below.
- Use saturated pillar gradients against a pale gray background; the dark triangular folds and soft shadows provide the 3D depth cue.