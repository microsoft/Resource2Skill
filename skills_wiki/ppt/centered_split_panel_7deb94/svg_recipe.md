# SVG Recipe — Centered Split Panel

## Visual mechanism
A single centered, floating card is split into two equal-weight zones: a saturated text panel on the left and a clipped photographic panel on the right. The shared outer silhouette, soft shadow, and aligned midline make the two halves feel like one premium section-divider unit rather than two separate boxes.

## SVG primitives needed
- 1× `<rect>` for the full-slide atmospheric background
- 1× `<rect>` for the unified card shadow silhouette
- 1× `<path>` for the left text panel with rounded outer corners and square inner seam
- 1× `<clipPath>` using `<path>` for the right-side rounded image crop
- 1× `<image>` for the hero photograph clipped into the right panel
- 1× `<path>` for a translucent gradient overlay on the image side
- 3× `<linearGradient>` for background, left panel depth, and image-side vignette
- 1× `<filter id="cardShadow">` for the elevated floating-panel shadow
- 1× `<filter id="softGlow">` for subtle decorative glow
- 2× `<circle>` for quiet decorative color accents behind the card
- 1× `<line>` for the small editorial rule above the headline
- 5× `<text>` for eyebrow, headline, body copy, CTA, and image caption
- 1× `<path>` for a small editable arrow/chevron beside the CTA

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F7F8FC"/>
      <stop offset="0.55" stop-color="#EEF2F7"/>
      <stop offset="1" stop-color="#E4EAF3"/>
    </linearGradient>

    <linearGradient id="leftPanelGrad" x1="160" y1="125" x2="590" y2="595" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#132B5C"/>
      <stop offset="0.55" stop-color="#0E2149"/>
      <stop offset="1" stop-color="#091632"/>
    </linearGradient>

    <linearGradient id="imageVignette" x1="590" y1="125" x2="1120" y2="595" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#06142E" stop-opacity="0.50"/>
      <stop offset="0.45" stop-color="#06142E" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#06142E" stop-opacity="0.00"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="22" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="22" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>

    <clipPath id="rightImageClip">
      <path d="M590 125 H1086 Q1120 125 1120 159 V561 Q1120 595 1086 595 H590 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <circle cx="235" cy="150" r="92" fill="#6EA8FF" opacity="0.20" filter="url(#softGlow)"/>
  <circle cx="1055" cy="615" r="118" fill="#FFB86B" opacity="0.18" filter="url(#softGlow)"/>

  <rect x="160" y="125" width="960" height="470" rx="34" fill="#000000" opacity="0.18" filter="url(#cardShadow)"/>

  <path d="M194 125 H590 V595 H194 Q160 595 160 561 V159 Q160 125 194 125 Z"
        fill="url(#leftPanelGrad)"/>

  <image x="590" y="125" width="530" height="470"
         href="https://images.example.com/hero-photo-modern-architecture-glass-facade.jpg"
         clip-path="url(#rightImageClip)"
         preserveAspectRatio="xMidYMid slice"/>

  <path d="M590 125 H1086 Q1120 125 1120 159 V561 Q1120 595 1086 595 H590 Z"
        fill="url(#imageVignette)"/>

  <line x1="222" y1="196" x2="292" y2="196" stroke="#7DB5FF" stroke-width="4" stroke-linecap="round"/>

  <text x="222" y="232" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.4"
        fill="#9EC8FF">
    STRATEGIC SHIFT
  </text>

  <text x="220" y="304" width="340"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="700"
        fill="#FFFFFF">
    <tspan x="220" dy="0">Design for</tspan>
    <tspan x="220" dy="58">the next</tspan>
    <tspan x="220" dy="58">operating era</tspan>
  </text>

  <text x="222" y="458" width="315"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400"
        fill="#C9D7EF">
    <tspan x="222" dy="0">A centered split panel creates a strong</tspan>
    <tspan x="222" dy="28">editorial pause while pairing a concise</tspan>
    <tspan x="222" dy="28">message with a memorable visual anchor.</tspan>
  </text>

  <text x="222" y="552" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700"
        fill="#FFFFFF">
    Explore the framework
  </text>

  <path d="M438 546 L453 552 L438 558"
        fill="none" stroke="#7DB5FF" stroke-width="3"
        stroke-linecap="round" stroke-linejoin="round"/>

  <text x="742" y="548" width="295"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600"
        fill="#FFFFFF" opacity="0.86">
    Image panel: architecture, product, team, customer, or market signal
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the split as two unrelated rectangles with separate shadows; the card should read as one centered unit.
- ❌ Do not apply `clip-path` to overlay rectangles or groups; only clip the `<image>`, and draw matching overlay shapes as paths.
- ❌ Do not use `<mask>` to create the rounded image side; use a `<clipPath>` with a path instead.
- ❌ Do not let text run close to the center seam; keep a generous inner gutter so the image and copy feel balanced.
- ❌ Do not use tiny dashboard-style panels or many columns; this technique depends on low-density, high-impact composition.

## Composition notes
- Keep the whole split card centered with roughly 10–15% slide margin on the left and right, and 15–18% vertical breathing room.
- Allocate the left 42–48% of the card to text and the right 52–58% to imagery; the image side can be slightly wider for cinematic impact.
- Use a saturated dark or brand-colored text panel against a lighter slide background so the centered unit feels elevated.
- Align eyebrow, headline, body, and CTA to one strong left edge; use the image caption sparingly and keep it low-contrast.