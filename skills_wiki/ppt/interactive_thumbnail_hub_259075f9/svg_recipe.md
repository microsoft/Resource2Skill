# SVG Recipe — Interactive Thumbnail Hub

## Visual mechanism
A neutral “home base” slide presents a curated grid of elevated slide-thumbnail cards, each acting as a visual portal into a section. The thumbnails are styled like premium clickable tiles with shadows, rounded crops, section numbers, and subtle UI cues so the agenda feels like an interactive navigation dashboard rather than a list.

## SVG primitives needed
- 1× `<rect>` for the warm neutral slide background
- 2× `<path>` for soft abstract background ribbons that frame the hub without distracting
- 6× thumbnail card `<rect>` shapes for white card surfaces
- 6× `<image>` elements clipped by rounded `<clipPath>` rectangles for slide-preview thumbnails
- 6× colored accent `<rect>` bars or badges for section identity
- 6× small `<circle>` elements for numbered navigation badges
- 6× thumbnail title `<text>` elements with explicit `width`
- 1× main title `<text>` and 1× subtitle `<text>` with explicit `width`
- 1× small “return hub” preview/control cluster using `<circle>`, `<path>`, and `<text>`
- 1× `<filter id="cardShadow">` applied to cards for depth
- 1× `<filter id="softGlow">` applied to the active/featured card accent
- 2× `<linearGradient>` fills for background and active card styling
- 6× rounded `<clipPath>` definitions, one per thumbnail image crop

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F7F3EC"/>
      <stop offset="0.58" stop-color="#EFEAE1"/>
      <stop offset="1" stop-color="#E9E1D6"/>
    </linearGradient>
    <linearGradient id="activeStroke" x1="0" y1="0" x2="310" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2F80ED"/>
      <stop offset="1" stop-color="#26C6DA"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>

    <clipPath id="thumbClip1"><rect x="116" y="220" width="302" height="170" rx="18"/></clipPath>
    <clipPath id="thumbClip2"><rect x="489" y="220" width="302" height="170" rx="18"/></clipPath>
    <clipPath id="thumbClip3"><rect x="862" y="220" width="302" height="170" rx="18"/></clipPath>
    <clipPath id="thumbClip4"><rect x="116" y="475" width="302" height="170" rx="18"/></clipPath>
    <clipPath id="thumbClip5"><rect x="489" y="475" width="302" height="170" rx="18"/></clipPath>
    <clipPath id="thumbClip6"><rect x="862" y="475" width="302" height="170" rx="18"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M-60,135 C210,35 370,105 560,58 C765,8 960,-22 1345,80 L1345,-80 L-60,-80 Z" fill="#FFFFFF" opacity="0.48"/>
  <path d="M890,728 C1000,620 1130,615 1325,548 L1325,728 Z" fill="#D8C8B8" opacity="0.35"/>

  <text x="80" y="72" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#252525">Interactive Strategy Hub</text>
  <text x="82" y="112" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#6E675F">Choose any module below to zoom into that section, then return home from each slide.</text>

  <rect x="1015" y="54" width="164" height="46" rx="23" fill="#252525" opacity="0.92"/>
  <circle cx="1045" cy="77" r="15" fill="#FFFFFF"/>
  <path d="M1037,78 L1045,70 L1053,78 L1053,86 L1049,86 L1049,80 L1041,80 L1041,86 L1037,86 Z" fill="#252525"/>
  <text x="1066" y="83" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#FFFFFF">Hub slide</text>

  <rect x="94" y="196" width="346" height="226" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="106" y="208" width="322" height="194" rx="22" fill="none" stroke="url(#activeStroke)" stroke-width="4"/>
  <rect x="116" y="220" width="302" height="170" rx="18" fill="#DCE9FF"/>
  <image x="116" y="220" width="302" height="170" clip-path="url(#thumbClip1)" href="https://images.example.com/slide-thumbnail-market-landscape-blue-dashboard.png"/>
  <rect x="116" y="354" width="302" height="36" fill="#101828" opacity="0.62"/>
  <circle cx="139" cy="238" r="18" fill="#2F80ED" filter="url(#softGlow)"/>
  <text x="132" y="244" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">1</text>
  <text x="124" y="378" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Market Landscape</text>

  <rect x="467" y="196" width="346" height="226" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="489" y="220" width="302" height="170" rx="18" fill="#FCE4D6"/>
  <image x="489" y="220" width="302" height="170" clip-path="url(#thumbClip2)" href="https://images.example.com/slide-thumbnail-customer-insights-warm-segments.png"/>
  <rect x="489" y="354" width="302" height="36" fill="#101828" opacity="0.62"/>
  <circle cx="512" cy="238" r="18" fill="#E26D5A"/>
  <text x="505" y="244" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">2</text>
  <text x="497" y="378" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Customer Insights</text>

  <rect x="840" y="196" width="346" height="226" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="862" y="220" width="302" height="170" rx="18" fill="#E7F5E8"/>
  <image x="862" y="220" width="302" height="170" clip-path="url(#thumbClip3)" href="https://images.example.com/slide-thumbnail-growth-roadmap-green-timeline.png"/>
  <rect x="862" y="354" width="302" height="36" fill="#101828" opacity="0.62"/>
  <circle cx="885" cy="238" r="18" fill="#34A853"/>
  <text x="878" y="244" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">3</text>
  <text x="870" y="378" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Growth Roadmap</text>

  <rect x="94" y="451" width="346" height="226" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="116" y="475" width="302" height="170" rx="18" fill="#E9E6FF"/>
  <image x="116" y="475" width="302" height="170" clip-path="url(#thumbClip4)" href="https://images.example.com/slide-thumbnail-operating-model-purple-org-chart.png"/>
  <rect x="116" y="609" width="302" height="36" fill="#101828" opacity="0.62"/>
  <circle cx="139" cy="493" r="18" fill="#7B61FF"/>
  <text x="132" y="499" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">4</text>
  <text x="124" y="633" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Operating Model</text>

  <rect x="467" y="451" width="346" height="226" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="489" y="475" width="302" height="170" rx="18" fill="#FFF2CC"/>
  <image x="489" y="475" width="302" height="170" clip-path="url(#thumbClip5)" href="https://images.example.com/slide-thumbnail-financial-case-gold-waterfall.png"/>
  <rect x="489" y="609" width="302" height="36" fill="#101828" opacity="0.62"/>
  <circle cx="512" cy="493" r="18" fill="#F4A900"/>
  <text x="505" y="499" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">5</text>
  <text x="497" y="633" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Financial Case</text>

  <rect x="840" y="451" width="346" height="226" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="862" y="475" width="302" height="170" rx="18" fill="#E0F7FA"/>
  <image x="862" y="475" width="302" height="170" clip-path="url(#thumbClip6)" href="https://images.example.com/slide-thumbnail-execution-plan-teal-kanban.png"/>
  <rect x="862" y="609" width="302" height="36" fill="#101828" opacity="0.62"/>
  <circle cx="885" cy="493" r="18" fill="#00A6A6"/>
  <text x="878" y="499" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">6</text>
  <text x="870" y="633" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Execution Plan</text>

  <text x="84" y="690" width="900" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#81786E">Implementation note: assign each thumbnail card a PowerPoint Slide Zoom or hyperlink target after import; keep the whole card grouped as the clickable area.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<a>` hyperlinks as the main navigation mechanism; create the visual hub in SVG, then assign PowerPoint Slide Zoom or hyperlink actions to each imported card/group.
- ❌ Do not rely on `<animate>` or animated zoom effects in SVG; PowerPoint’s native Slide Zoom transition should provide the motion.
- ❌ Do not use `<mask>` for thumbnail fades or hover states; use clipped `<image>` elements and editable overlays instead.
- ❌ Do not place `clip-path` on card rectangles or groups; clipping should be applied only to `<image>` thumbnails for reliable translation.
- ❌ Do not make thumbnails too small or text-heavy; the slide-preview cards should read as visual destinations, not miniature full slides.

## Composition notes
- Keep the hub background calm and low-contrast so the thumbnail cards become the primary color and navigation system.
- Use a 3×2 or 3×3 grid with generous gutters; each card should feel like a large button with a clear clickable target.
- Treat one card as “active” or “recommended first” using a brighter stroke or glow to guide presenter flow without enforcing linear order.
- Place any instructions or hub-return explanation in a small footer, not near the thumbnails, so the interface remains visually clean.