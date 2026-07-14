# SVG Recipe — Diagonal Slant Split Agenda Layout

## Visual mechanism
A clean agenda list is anchored on the left while a full-height architectural photo is clipped into a sharp right-side trapezoid. A saturated diagonal accent line traces the photo boundary, creating forward motion and turning a static list into an editorial split-page layout.

## SVG primitives needed
- 2× `<rect>` for the slide base and subtle left-panel background wash
- 1× `<path>` for the slanted pale content panel behind the agenda
- 1× `<image>` clipped into the right-side diagonal trapezoid
- 1× `<clipPath>` with a polygon-like path for the slanted image crop
- 1× `<line>` for the blue diagonal divider
- 5× `<circle>` for large agenda bullets
- 1× `<radialGradient>` for dimensional blue bullet fills
- 1× `<linearGradient>` for the soft background and accent stroke
- 1× `<filter id="bulletShadow">` applied to agenda bullets
- 11× `<text>` for the title and five agenda title/body pairs, each with explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="65%" stop-color="#f2f2f2"/>
      <stop offset="100%" stop-color="#e9e9e9"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="720" y1="0" x2="720" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2f67c8"/>
      <stop offset="100%" stop-color="#5b8fe6"/>
    </linearGradient>

    <radialGradient id="bulletBlue" cx="35%" cy="28%" r="72%">
      <stop offset="0%" stop-color="#6ea3f0"/>
      <stop offset="55%" stop-color="#4778c8"/>
      <stop offset="100%" stop-color="#2f5fae"/>
    </radialGradient>

    <filter id="bulletShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="-8" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoSlantClip">
      <path d="M808 0 L1280 0 L1280 720 L695 720 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <image
    x="0" y="0" width="1280" height="720"
    href="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&amp;w=1800&amp;auto=format&amp;fit=crop"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoSlantClip)"/>

  <path d="M0 0 L820 0 L700 720 L0 720 Z" fill="#f7f7f7" opacity="0.92"/>

  <line x1="803" y1="0" x2="692" y2="720"
        stroke="url(#accentGrad)" stroke-width="8" stroke-linecap="square"/>

  <text x="88" y="108" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="700" fill="#050505">Agenda</text>

  <circle cx="116" cy="228" r="37" fill="url(#bulletBlue)" filter="url(#bulletShadow)"/>
  <circle cx="116" cy="228" r="35" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.75"/>
  <text x="198" y="215" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="500" fill="#111111">Market Landscape</text>
  <text x="199" y="237" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#242424">
    <tspan x="199" dy="0">Signals shaping demand, growth pockets,</tspan>
    <tspan x="199" dy="20">and the competitive posture for the year.</tspan>
  </text>

  <circle cx="116" cy="330" r="37" fill="url(#bulletBlue)" filter="url(#bulletShadow)"/>
  <circle cx="116" cy="330" r="35" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.75"/>
  <text x="198" y="317" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="500" fill="#111111">Strategic Priorities</text>
  <text x="199" y="339" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#242424">
    <tspan x="199" dy="0">Three operating choices that focus capital,</tspan>
    <tspan x="199" dy="20">talent, and leadership attention.</tspan>
  </text>

  <circle cx="116" cy="432" r="37" fill="url(#bulletBlue)" filter="url(#bulletShadow)"/>
  <circle cx="116" cy="432" r="35" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.75"/>
  <text x="198" y="419" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="500" fill="#111111">Operating Model</text>
  <text x="199" y="441" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#242424">
    <tspan x="199" dy="0">Decision rights, governance cadence, and</tspan>
    <tspan x="199" dy="20">cross-functional accountability.</tspan>
  </text>

  <circle cx="116" cy="534" r="37" fill="url(#bulletBlue)" filter="url(#bulletShadow)"/>
  <circle cx="116" cy="534" r="35" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.75"/>
  <text x="198" y="521" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="500" fill="#111111">Investment Roadmap</text>
  <text x="199" y="543" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#242424">
    <tspan x="199" dy="0">Sequenced initiatives, funding gates, and</tspan>
    <tspan x="199" dy="20">milestones through the next four quarters.</tspan>
  </text>

  <circle cx="116" cy="636" r="37" fill="url(#bulletBlue)" filter="url(#bulletShadow)"/>
  <circle cx="116" cy="636" r="35" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.75"/>
  <text x="198" y="623" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="500" fill="#111111">Next Steps</text>
  <text x="199" y="645" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#242424">
    <tspan x="199" dy="0">Immediate actions, owners, and the executive</tspan>
    <tspan x="199" dy="20">decisions required to move forward.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG masks for the photo split; use a `<clipPath>` applied directly to the `<image>`.
- ❌ Do not apply `clip-path` to rectangles or paths for the left panel; PPT-Master only preserves clipping reliably on images.
- ❌ Do not use `marker-end` on the diagonal divider; this layout needs a plain `<line>` with a strong stroke.
- ❌ Do not rely on automatic text wrapping; use explicit `width` on every `<text>` and manual `<tspan>` line breaks for predictable PowerPoint rendering.
- ❌ Do not make the photo boundary vertical; the visual tension comes from the top-right-to-bottom-left slant.

## Composition notes
- Keep the agenda text zone to the left 55–60% of the canvas; the photo should own the right 40–45% and run full height.
- Place the diagonal line exactly on top of the clipped image edge, slightly thicker than a normal rule so it reads as a structural separator.
- Align all bullet circles to one vertical axis; this grounds the list against the aggressive diagonal geometry.
- Use a restrained palette: white/soft gray field, charcoal typography, and one saturated blue accent repeated in the divider and bullets.