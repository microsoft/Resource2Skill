# SVG Recipe — Interactive 3D Card Flip (Layered Morph Technique)

## Visual mechanism
Stack a card back and card front at the exact same coordinates, then use PowerPoint Morph between duplicate slides to swap which face is visually dominant. The SVG provides editable card assets, shadows, clickable hit areas, and a premium “casino table” stage; the flip illusion is completed in PowerPoint by duplicating the slide and changing z-order / 3D rotation state.

## SVG primitives needed
- 1× `<rect>` for the full-slide felt table background
- 2× `<ellipse>` for soft radial table lighting and vignette depth
- 3× card groups made from layered `<rect>` elements for rounded poker-card bodies, borders, and inner panels
- Many `<circle>` and `<path>` elements for editable geometric card-back ornamentation
- Several `<path>` and `<rect>` elements for the revealed gift icon on the winning card
- 1× `<filter id="cardShadow">` applied to card bodies for physical lift
- 1× `<filter id="goldGlow">` applied to the winning card accent for a reveal glow
- 4× gradients for felt, card backs, gold accents, and subtle face highlights
- 3× transparent `<rect>` hotspots over the cards for later PowerPoint hyperlink assignment
- Multiple `<text>` elements with explicit `width` for title, instructions, indices, and reveal labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="feltGlow" cx="50%" cy="48%" r="72%">
      <stop offset="0%" stop-color="#2fb15a"/>
      <stop offset="48%" stop-color="#0f7f3a"/>
      <stop offset="100%" stop-color="#063f23"/>
    </radialGradient>
    <linearGradient id="backGreen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#38c866"/>
      <stop offset="45%" stop-color="#08783d"/>
      <stop offset="100%" stop-color="#043f27"/>
    </linearGradient>
    <linearGradient id="faceWhite" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#eef1f4"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff4b0"/>
      <stop offset="42%" stop-color="#f4bd39"/>
      <stop offset="100%" stop-color="#a86806"/>
    </linearGradient>
    <filter id="cardShadow" x="-25%" y="-20%" width="150%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="goldGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#feltGlow)"/>
  <ellipse cx="640" cy="370" rx="520" ry="255" fill="#53e878" opacity="0.13"/>
  <ellipse cx="640" cy="730" rx="760" ry="160" fill="#001b13" opacity="0.35"/>

  <text x="90" y="70" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#f1fff4">Pick a Card</text>
  <text x="90" y="108" width="770" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#bce8c7">Duplicate this slide, place the revealed face on top, then apply PowerPoint Morph for the 3D flip moment.</text>

  <g transform="translate(250 220) rotate(-5 95 135)">
    <rect x="0" y="0" width="190" height="270" rx="22" fill="#062918" opacity="0.58" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="190" height="270" rx="22" fill="url(#backGreen)" stroke="#e9fff0" stroke-width="5"/>
    <rect x="18" y="18" width="154" height="234" rx="14" fill="none" stroke="#b7f5c5" stroke-width="2.5"/>
    <path d="M95 40 L128 73 L95 106 L62 73 Z" fill="none" stroke="#d8ffe0" stroke-width="3"/>
    <path d="M95 164 L128 197 L95 230 L62 197 Z" fill="none" stroke="#d8ffe0" stroke-width="3"/>
    <circle cx="55" cy="55" r="12" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="135" cy="55" r="12" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="55" cy="135" r="12" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="135" cy="135" r="12" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="55" cy="215" r="12" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="135" cy="215" r="12" fill="none" stroke="#073d25" stroke-width="4"/>
    <path d="M42 135 C64 105,126 105,148 135 C126 165,64 165,42 135 Z" fill="none" stroke="#aaf2bd" stroke-width="3"/>
    <text x="62" y="315" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" text-anchor="middle" fill="#eaffee">CARD A</text>
  </g>

  <g transform="translate(545 220)">
    <rect x="-8" y="10" width="18" height="250" rx="8" fill="#0b492b" opacity="0.95"/>
    <rect x="0" y="0" width="190" height="270" rx="22" fill="url(#backGreen)" opacity="0.22"/>
    <rect x="0" y="0" width="190" height="270" rx="22" fill="url(#faceWhite)" stroke="#f5f7fa" stroke-width="5" filter="url(#cardShadow)"/>
    <rect x="15" y="15" width="160" height="240" rx="16" fill="none" stroke="#d7dde5" stroke-width="2"/>
    <path d="M95 72 C125 72,150 95,150 124 C150 163,119 189,95 211 C71 189,40 163,40 124 C40 95,65 72,95 72 Z" fill="#fff1bd" filter="url(#goldGlow)"/>
    <rect x="62" y="124" width="66" height="58" rx="8" fill="url(#gold)" stroke="#8f5600" stroke-width="2"/>
    <rect x="58" y="112" width="74" height="20" rx="5" fill="#d91e41"/>
    <rect x="91" y="112" width="8" height="70" fill="#b91533"/>
    <path d="M95 112 C83 98,71 96,68 106 C65 118,82 120,95 112 Z" fill="#ff6178"/>
    <path d="M95 112 C107 98,119 96,122 106 C125 118,108 120,95 112 Z" fill="#ff6178"/>
    <path d="M45 42 L57 58 L45 74 L33 58 Z" fill="#d91e41"/>
    <text x="27" y="39" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" text-anchor="middle" fill="#d91e41">G</text>
    <text x="163" y="239" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" text-anchor="middle" fill="#d91e41" transform="rotate(180 163 239)">G</text>
    <rect x="42" y="214" width="106" height="28" rx="14" fill="#111827" opacity="0.92"/>
    <text x="95" y="235" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#ffeaa0">WINNER</text>
    <text x="42" y="315" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" text-anchor="middle" fill="#fff5c8">REVEALED</text>
  </g>

  <g transform="translate(840 220) rotate(5 95 135)">
    <rect x="0" y="0" width="190" height="270" rx="22" fill="#062918" opacity="0.58" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="190" height="270" rx="22" fill="url(#backGreen)" stroke="#e9fff0" stroke-width="5"/>
    <rect x="18" y="18" width="154" height="234" rx="14" fill="none" stroke="#b7f5c5" stroke-width="2.5"/>
    <path d="M95 38 C122 58,122 88,95 108 C68 88,68 58,95 38 Z" fill="none" stroke="#d8ffe0" stroke-width="3"/>
    <path d="M95 232 C68 212,68 182,95 162 C122 182,122 212,95 232 Z" fill="none" stroke="#d8ffe0" stroke-width="3"/>
    <circle cx="52" cy="64" r="11" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="95" cy="64" r="11" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="138" cy="64" r="11" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="52" cy="135" r="11" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="95" cy="135" r="11" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="138" cy="135" r="11" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="52" cy="206" r="11" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="95" cy="206" r="11" fill="none" stroke="#073d25" stroke-width="4"/>
    <circle cx="138" cy="206" r="11" fill="none" stroke="#073d25" stroke-width="4"/>
    <path d="M42 135 C64 105,126 105,148 135 C126 165,64 165,42 135 Z" fill="none" stroke="#aaf2bd" stroke-width="3"/>
    <text x="62" y="315" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" text-anchor="middle" fill="#eaffee">CARD C</text>
  </g>

  <text x="890" y="86" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#fff6cf">Morph setup note</text>
  <text x="890" y="116" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#c7efd1">Slide 1: card back on top. Slide 2: card front on top. Keep X/Y and size identical so Morph sells the flip.</text>

  <rect x="240" y="205" width="210" height="305" rx="26" fill="#ffffff" opacity="0.01"/>
  <rect x="535" y="205" width="210" height="305" rx="26" fill="#ffffff" opacity="0.01"/>
  <rect x="830" y="205" width="210" height="305" rx="26" fill="#ffffff" opacity="0.01"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; the flip should be a PowerPoint Morph transition, not embedded SVG animation.
- ❌ Do not rely on SVG 3D transforms such as `matrix3d`, `rotateX`, or CSS perspective; they will not translate into editable PowerPoint shapes.
- ❌ Do not use `<use>` for repeating card-back ornaments; duplicate the editable circles/paths directly.
- ❌ Do not use masks for card shadows or reveals; use editable rounded rectangles, gradients, opacity, and supported filters instead.
- ❌ Do not place `clip-path` on card shapes; clipping is only reliable for images in this pipeline.

## Composition notes
- Keep the card front and card back at identical X/Y, width, height, and rotation across Morph states; only z-order and PowerPoint 3D rotation should change.
- Leave generous negative space above the cards for the host prompt and below the cards for labels or reveal copy.
- Use a dark green radial felt background so white/gold card faces read as the focal reveal.
- Add transparent hotspot rectangles last in the SVG so they can be selected in PowerPoint and assigned hyperlinks for interactive “pick a card” navigation.