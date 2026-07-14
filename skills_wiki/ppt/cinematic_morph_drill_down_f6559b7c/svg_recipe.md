# SVG Recipe — Cinematic Morph Drill-Down

## Visual mechanism
A set of equal overview cards morphs into an app-like drill-down: one card expands into a large cinematic hero panel while the remaining cards compress into a right-side stack. The illusion depends on preserving object identity between slides with matching `id` / PowerPoint names, so Morph interpolates position, scale, corner radius, shadows, and text hierarchy.

## SVG primitives needed
- 1× `<rect>` for the light blue-gray slide background.
- 3× large/mini `<rect>` card bodies with rounded corners and gradient fills.
- 3× `<image>` elements clipped into rounded card photo areas for cinematic depth.
- 3× `<clipPath>` definitions using rounded `<rect>` crops for the hero and mini-card imagery.
- 2× decorative `<path>` shapes for soft background motion ribbons / spotlight energy.
- 1× `<filter id="cardShadow">` applied to card rectangles for tactile floating depth.
- 1× `<filter id="softGlow">` applied to decorative paths and the active KPI pill.
- 4× `<linearGradient>` definitions for background atmosphere and card fills.
- Multiple `<text>` elements with explicit `width` attributes for title, card labels, KPI detail, and sidebar labels.
- 2× `<line>` elements for subtle metric dividers inside the hero card.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F8FBFF"/>
      <stop offset="55%" stop-color="#EFF5FB"/>
      <stop offset="100%" stop-color="#E6EEF7"/>
    </linearGradient>

    <linearGradient id="blueHero" x1="130" y1="120" x2="860" y2="650">
      <stop offset="0%" stop-color="#4A7BFF"/>
      <stop offset="48%" stop-color="#2D6AFF"/>
      <stop offset="100%" stop-color="#143DD9"/>
    </linearGradient>

    <linearGradient id="purpleMini" x1="930" y1="160" x2="1190" y2="340">
      <stop offset="0%" stop-color="#8E63E7"/>
      <stop offset="100%" stop-color="#6F42C1"/>
    </linearGradient>

    <linearGradient id="cyanMini" x1="930" y1="395" x2="1190" y2="575">
      <stop offset="0%" stop-color="#19D3EA"/>
      <stop offset="100%" stop-color="#00AFCB"/>
    </linearGradient>

    <linearGradient id="whiteFade" x1="130" y1="120" x2="820" y2="620">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="42%" stop-color="#FFFFFF" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>

    <clipPath id="heroPhotoClip">
      <rect x="510" y="170" width="310" height="250" rx="34"/>
    </clipPath>

    <clipPath id="miniPhotoClipQ2">
      <rect x="965" y="190" width="185" height="82" rx="18"/>
    </clipPath>

    <clipPath id="miniPhotoClipQ3">
      <rect x="965" y="425" width="185" height="82" rx="18"/>
    </clipPath>
  </defs>

  <rect id="slide-background" x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path id="cinematic-ribbon-back" d="M-80,520 C170,390 315,420 470,305 C645,175 800,130 1010,185 C1155,224 1260,180 1360,95 L1360,275 C1180,342 1035,316 900,280 C700,228 560,315 410,430 C250,552 100,585 -80,610 Z"
        fill="#CFE0FF" opacity="0.45" filter="url(#softGlow)"/>

  <path id="cinematic-ribbon-front" d="M-60,660 C160,585 300,540 455,470 C620,395 735,365 910,405 C1050,438 1180,430 1340,340 L1340,720 L-60,720 Z"
        fill="#D9F7FF" opacity="0.62"/>

  <text id="!!scene_title" x="72" y="68" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="600" fill="#526173" letter-spacing="0.5">
    QUARTERLY OVERVIEW
  </text>

  <text id="!!scene_subtitle" x="72" y="103" width="740" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" fill="#162033">
    Drill down into Q1 Performance
  </text>

  <rect id="!!card_q1_body" x="86" y="142" width="780" height="500" rx="36"
        fill="url(#blueHero)" filter="url(#cardShadow)"/>

  <image id="!!card_q1_image" x="510" y="170" width="310" height="250"
         href="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=900"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#heroPhotoClip)" opacity="0.88"/>

  <rect id="!!card_q1_photo_sheen" x="510" y="170" width="310" height="250" rx="34"
        fill="url(#whiteFade)" opacity="0.75"/>

  <path id="!!card_q1_orbit" d="M135,520 C250,455 342,455 455,500 C560,542 650,530 775,462"
        fill="none" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.22" stroke-dasharray="12 16"/>

  <text id="!!card_q1_label" x="135" y="214" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#DCE8FF" letter-spacing="1.8">
    SELECTED KPI
  </text>

  <text id="!!card_q1_title" x="132" y="270" width="375" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="800" fill="#FFFFFF">
    Q1 Performance
  </text>

  <text id="!!card_q1_bodytext" x="136" y="330" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#E6EEFF">
    Revenue momentum accelerated across enterprise accounts, with retention and expansion both tracking above plan.
  </text>

  <rect id="!!card_q1_kpi_pill" x="136" y="438" width="216" height="70" rx="22"
        fill="#FFFFFF" opacity="0.18" filter="url(#softGlow)"/>

  <text id="!!card_q1_kpi_value" x="158" y="483" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="36" font-weight="800" fill="#FFFFFF">
    +18.4%
  </text>

  <text id="!!card_q1_kpi_caption" x="160" y="510" width="175" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" fill="#D8E5FF">
    YoY revenue growth
  </text>

  <line id="!!card_q1_metric_divider_1" x1="390" y1="447" x2="390" y2="532" stroke="#FFFFFF" stroke-width="1.5" stroke-opacity="0.25"/>
  <line id="!!card_q1_metric_divider_2" x1="560" y1="447" x2="560" y2="532" stroke="#FFFFFF" stroke-width="1.5" stroke-opacity="0.25"/>

  <text id="!!card_q1_metric_a" x="420" y="478" width="125" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="800" fill="#FFFFFF">92%</text>
  <text id="!!card_q1_metric_a_label" x="420" y="508" width="125" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#D8E5FF">Retention</text>

  <text id="!!card_q1_metric_b" x="590" y="478" width="125" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="800" fill="#FFFFFF">$4.2M</text>
  <text id="!!card_q1_metric_b_label" x="590" y="508" width="145" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#D8E5FF">Expansion ARR</text>

  <rect id="!!card_q2_body" x="924" y="142" width="270" height="205" rx="30"
        fill="url(#purpleMini)" filter="url(#cardShadow)"/>
  <image id="!!card_q2_image" x="965" y="190" width="185" height="82"
         href="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#miniPhotoClipQ2)" opacity="0.55"/>
  <text id="!!card_q2_title" x="956" y="305" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#FFFFFF">Q2 Projections</text>
  <text id="!!card_q2_caption" x="956" y="332" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#EFE6FF">Pipeline model and forecast confidence</text>

  <rect id="!!card_q3_body" x="924" y="377" width="270" height="205" rx="30"
        fill="url(#cyanMini)" filter="url(#cardShadow)"/>
  <image id="!!card_q3_image" x="965" y="425" width="185" height="82"
         href="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#miniPhotoClipQ3)" opacity="0.55"/>
  <text id="!!card_q3_title" x="956" y="540" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#FFFFFF">Q3 Strategy</text>
  <text id="!!card_q3_caption" x="956" y="567" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#D8FAFF">Product focus and market expansion</text>

  <text id="!!morph_hint" x="924" y="630" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" fill="#6B7788">
    Morph target: Q1 expands; Q2/Q3 compress into contextual navigation.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not build this as a single static before/after composite slide; the technique requires two actual slides with matching object identities and PowerPoint Morph applied to the second slide.
- ❌ Do not use `<animate>` or `<animateTransform>` for the motion; PowerPoint will not translate those as editable Morph behavior.
- ❌ Do not rely on `<g>` group-level IDs alone for Morph matching; assign stable `id` values to the individual card rectangles, images, and text objects that need to interpolate.
- ❌ Do not use `clip-path` on text, paths, or rectangles; use it only on `<image>` elements, then mirror the same rounded geometry with editable `<rect>` overlays.
- ❌ Do not use `marker-end` on paths for motion arrows; if arrows are needed, use editable `<line>` arrows with the marker applied directly to each line.

## Composition notes
- Create two slides: State A uses the same `!!card_q1_*`, `!!card_q2_*`, and `!!card_q3_*` IDs in a balanced three-card row; State B uses the snippet’s hero-plus-sidebar layout.
- Keep the expanded card at roughly 60–65% of slide width, leaving a right rail for compressed sibling cards so the audience retains spatial context.
- Use a calm, airy background and saturated card gradients; the contrast makes the Morph feel cinematic rather than mechanical.
- Text hierarchy should morph from short card labels in State A into a full detail hierarchy in State B: eyebrow, large title, explanatory copy, and KPI modules.