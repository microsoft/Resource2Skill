# SVG Recipe — Focus Reveal Team Gallery

## Visual mechanism
A row of bottom-anchored stadium portrait cards creates a carousel-like roster: one active person is larger, brighter, full-color, and backed by a vivid accent, while surrounding people are smaller, grayscale, and visually recede. A black bottom fade blends the card bases into the slide, making the gallery feel cinematic rather than grid-like.

## SVG primitives needed
- 1× `<rect>` for the solid black slide background
- 4× pill-shaped `<rect>` for the stadium card bodies
- 4× `<image>` clipped into matching stadium silhouettes for portraits
- 4× `<clipPath>` with rounded-rectangle / stadium `<path>` geometry applied to the portrait images
- 4× semi-transparent `<rect>` overlays on inactive portraits for extra dimming
- 1× `<linearGradient>` for the active magenta card body
- 1× `<linearGradient>` for inactive charcoal card bodies
- 1× `<linearGradient>` for the bottom fade-to-black overlay
- 1× `<filter id="softShadow">` applied to stadium cards for depth
- 1× `<filter id="pinkGlow">` applied to the active card for focus emphasis
- 3× `<text>` blocks for title, active name, and role
- Optional small `<circle>` / `<path>` decorative accent marks to echo the active brand color

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="activePink" x1="0" y1="190" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff5b9f"/>
      <stop offset="0.55" stop-color="#ec407a"/>
      <stop offset="1" stop-color="#64152f"/>
    </linearGradient>

    <linearGradient id="inactiveCharcoal" x1="0" y1="300" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#303030"/>
      <stop offset="0.65" stop-color="#191919"/>
      <stop offset="1" stop-color="#050505"/>
    </linearGradient>

    <linearGradient id="bottomFade" x1="0" y1="470" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0"/>
      <stop offset="0.48" stop-color="#000000" stop-opacity="0.62"/>
      <stop offset="1" stop-color="#000000" stop-opacity="1"/>
    </linearGradient>

    <radialGradient id="stageGlow" cx="52%" cy="60%" r="52%">
      <stop offset="0" stop-color="#ec407a" stop-opacity="0.28"/>
      <stop offset="0.45" stop-color="#ec407a" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pinkGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipLeft">
      <path d="M39 401 C39 337 91 285 155 285 C219 285 271 337 271 401 L271 720 L39 720 Z"/>
    </clipPath>
    <clipPath id="clipActive">
      <path d="M336 337 C336 257 401 192 480 192 C559 192 624 257 624 337 L624 720 L336 720 Z"/>
    </clipPath>
    <clipPath id="clipMid">
      <path d="M680 401 C680 337 732 285 796 285 C860 285 912 337 912 401 L912 720 L680 720 Z"/>
    </clipPath>
    <clipPath id="clipRight">
      <path d="M1000 401 C1000 337 1052 285 1116 285 C1180 285 1232 337 1232 401 L1232 720 L1000 720 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>
  <ellipse cx="640" cy="515" rx="560" ry="300" fill="url(#stageGlow)"/>

  <text x="0" y="120" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" fill="#ffffff">Meet our Team</text>

  <circle cx="676" cy="170" r="5" fill="#ec407a"/>
  <circle cx="702" cy="170" r="5" fill="#ec407a" opacity="0.55"/>
  <circle cx="728" cy="170" r="5" fill="#ec407a" opacity="0.25"/>

  <!-- Inactive card: left -->
  <rect x="39" y="285" width="232" height="500" rx="116" fill="url(#inactiveCharcoal)" filter="url(#softShadow)"/>
  <image x="39" y="285" width="232" height="300" preserveAspectRatio="xMidYMin slice"
         href="https://images.example.com/team/grayscale-content-marketing-lead-portrait.jpg"
         clip-path="url(#clipLeft)"/>
  <rect x="39" y="530" width="232" height="210" fill="#111111" opacity="0.62"/>
  <rect x="39" y="285" width="232" height="500" rx="116" fill="none" stroke="#1f1f1f" stroke-width="1.5"/>

  <!-- Active card -->
  <rect x="336" y="192" width="288" height="590" rx="144" fill="url(#activePink)" filter="url(#pinkGlow)"/>
  <image x="336" y="192" width="288" height="330" preserveAspectRatio="xMidYMin slice"
         href="https://images.example.com/team/full-color-marketing-operations-portrait.jpg"
         clip-path="url(#clipActive)"/>
  <rect x="336" y="192" width="288" height="590" rx="144" fill="none" stroke="#ff79b5" stroke-width="2" opacity="0.75"/>
  <path d="M360 515 C400 545 560 545 600 515" fill="none" stroke="#ff9ccc" stroke-width="3" opacity="0.35"/>

  <!-- Inactive card: center-right -->
  <rect x="680" y="285" width="232" height="500" rx="116" fill="url(#inactiveCharcoal)" filter="url(#softShadow)"/>
  <image x="680" y="285" width="232" height="300" preserveAspectRatio="xMidYMin slice"
         href="https://images.example.com/team/grayscale-social-media-manager-portrait.jpg"
         clip-path="url(#clipMid)"/>
  <rect x="680" y="530" width="232" height="210" fill="#111111" opacity="0.62"/>
  <rect x="680" y="285" width="232" height="500" rx="116" fill="none" stroke="#1f1f1f" stroke-width="1.5"/>

  <!-- Inactive card: right -->
  <rect x="1000" y="285" width="232" height="500" rx="116" fill="url(#inactiveCharcoal)" filter="url(#softShadow)"/>
  <image x="1000" y="285" width="232" height="300" preserveAspectRatio="xMidYMin slice"
         href="https://images.example.com/team/grayscale-events-manager-portrait.jpg"
         clip-path="url(#clipRight)"/>
  <rect x="1000" y="530" width="232" height="210" fill="#111111" opacity="0.62"/>
  <rect x="1000" y="285" width="232" height="500" rx="116" fill="none" stroke="#1f1f1f" stroke-width="1.5"/>

  <text x="692" y="254" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#ff4f97">Anita Break</text>
  <text x="693" y="283" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400" fill="#cfcfcf">Marketing Operations</text>

  <text x="87" y="645" width="140" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#666666">Bill Board</text>
  <text x="748" y="645" width="100" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#666666">Ella Vator</text>
  <text x="1058" y="645" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#666666">Cliff Hanger</text>

  <rect x="0" y="470" width="1280" height="250" fill="url(#bottomFade)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` for the bottom fade; use a normal gradient-filled rectangle instead.
- ❌ Do not apply `clip-path` to a `<g>` containing the whole card; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ Do not rely on SVG grayscale filters for inactive portraits; use pre-grayscaled image assets or grayscale image URLs.
- ❌ Do not place the fade overlay above the active name/role text if the label is near the bottom; it will dull the hierarchy.
- ❌ Do not make all cards the same size; the technique depends on scale contrast.

## Composition notes
- Keep the title in the upper third with generous black negative space; the gallery should feel like it rises from a stage.
- The active card should be 20–30% wider and 80–120 px taller than inactive cards, with its top noticeably higher.
- Put the active name and role close to the active card’s upper-right shoulder, not below the card, so the label remains clear of the bottom fade.
- Use one saturated accent color only; inactive cards should stay charcoal and grayscale to preserve the focus reveal effect.