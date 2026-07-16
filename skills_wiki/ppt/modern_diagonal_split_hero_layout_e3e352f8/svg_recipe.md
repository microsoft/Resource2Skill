# SVG Recipe — Modern Diagonal Split Hero Layout

## Visual mechanism
A bold dark polygon cuts diagonally across a contrasting light background, creating a dynamic left-side safe zone for stacked white hero typography. The diagonal edge adds motion and tension, while the right side can stay minimal or carry a muted photo/texture accent.

## SVG primitives needed
- 1× `<rect>` for the full-slide light background base
- 1× `<path>` for the dominant dark diagonal split polygon
- 1× `<path>` for a narrow diagonal accent strip along the split edge
- 1× `<image>` clipped into the right-side exposed wedge for optional premium visual depth
- 1× `<clipPath>` with a `<path>` for the diagonal image crop
- 2× `<linearGradient>` for subtle background and accent shading
- 1× `<radialGradient>` for a soft glow behind the right-side visual area
- 1× `<filter id="softShadow">` applied to the diagonal accent strip / text backing details
- 3× `<text>` elements for eyebrow label, main hero title, and supporting subtitle
- 2× `<line>` elements for small editorial divider accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="lightBg" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#9A9A9A"/>
      <stop offset="55%" stop-color="#7D7D7D"/>
      <stop offset="100%" stop-color="#AFAFAF"/>
    </linearGradient>

    <linearGradient id="darkPanel" x1="0" y1="0" x2="900" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1F1F1F"/>
      <stop offset="62%" stop-color="#2D2D2D"/>
      <stop offset="100%" stop-color="#383838"/>
    </linearGradient>

    <linearGradient id="edgeAccent" x1="760" y1="0" x2="650" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.28"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.00"/>
    </linearGradient>

    <radialGradient id="rightGlow" cx="70%" cy="42%" r="52%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.28"/>
      <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="rightDiagonalCrop">
      <path d="M790 0 L1280 0 L1280 720 L640 720 Z"/>
    </clipPath>
  </defs>

  <!-- light exposed background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#lightBg)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#rightGlow)"/>

  <!-- optional muted hero image, cropped to the exposed right wedge -->
  <image
    href="https://images.example.com/abstract-glass-architecture-gray-hero.jpg"
    x="660" y="-20" width="700" height="780"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#rightDiagonalCrop)"
    opacity="0.34"/>

  <!-- main diagonal dark panel -->
  <path
    d="M0 0 L965 0 L665 720 L0 720 Z"
    fill="url(#darkPanel)"/>

  <!-- premium diagonal highlight along the cut edge -->
  <path
    d="M925 0 L980 0 L690 720 L636 720 Z"
    fill="url(#edgeAccent)"
    filter="url(#softShadow)"/>

  <!-- tiny editorial accents -->
  <line x1="124" y1="168" x2="208" y2="168" stroke="#FFFFFF" stroke-width="3" opacity="0.75"/>
  <line x1="124" y1="181" x2="164" y2="181" stroke="#FFFFFF" stroke-width="3" opacity="0.35"/>

  <!-- eyebrow -->
  <text
    x="124" y="145" width="520"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18"
    font-weight="700"
    letter-spacing="3"
    fill="#FFFFFF"
    opacity="0.78">
    STRATEGY KICKOFF
  </text>

  <!-- stacked hero title -->
  <text
    x="120" y="292" width="660"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="74"
    font-weight="800"
    fill="#FFFFFF">
    <tspan x="120" dy="0">Welcome back</tspan>
    <tspan x="120" dy="86">to the next</tspan>
    <tspan x="120" dy="86">big chapter</tspan>
  </text>

  <!-- subtitle -->
  <text
    x="126" y="584" width="560"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="23"
    font-weight="400"
    fill="#FFFFFF"
    opacity="0.72">
    A sharper opening slide for bold announcements, section breaks, and keynote hero moments.
  </text>

  <!-- small right-side label, kept subtle so the title remains dominant -->
  <text
    x="930" y="616" width="250"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="16"
    font-weight="700"
    letter-spacing="2"
    fill="#FFFFFF"
    opacity="0.45">
    MODERN / DIAGONAL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a rectangle-only split; the diagonal cut must be a real `<path>` polygon to create the motion cue.
- ❌ Placing title text too close to the diagonal edge, especially near the lower right where the dark safe zone narrows.
- ❌ Applying `clip-path` to the dark polygon or accent shapes; only use clipping on `<image>` elements for reliable editable translation.
- ❌ Relying on animation markup for the wipe reveal; build the static composition and apply PowerPoint animation manually if needed.
- ❌ Low-contrast typography over the light side; keep the main message fully inside the dark panel.

## Composition notes
- Keep the dark polygon anchored to the full left edge, reaching roughly 72–78% of slide width at the top and 50–55% at the bottom.
- Place the hero title in the upper-middle left, with generous margins: about 110–140 px from the left and at least 160 px from the top.
- Use the right wedge as visual atmosphere, not a competing content area; muted photos, glow, or subtle labels work best.
- Maintain a restrained palette: dark charcoal, medium gray, white typography, and one optional soft accent highlight along the diagonal.