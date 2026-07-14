# SVG Recipe — Glassmorphism (Frosted Glass Panel Reveal)

## Visual mechanism
A vibrant background is duplicated: the normal version fills the slide, while a pre-blurred duplicate is clipped to the rounded glass panel area so it looks like the background is being refracted through frosted glass. A translucent white tint, luminous border, soft shadow, and crisp foreground text complete the floating glass-card illusion; for the “reveal,” morph between slides where the panel moves/fades into this final state.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient base.
- 1× `<image>` for the sharp full-slide hero/background image.
- 1× `<image>` for the pre-blurred duplicate of the same background, clipped to the glass card.
- 1× `<clipPath>` with a rounded `<rect>` for the frosted-glass crop.
- 4× blurred `<circle>` elements for editable atmospheric color blooms behind the card.
- 1× `<rect>` with `filter id="cardShadow"` for the soft detached panel shadow.
- 2× rounded `<rect>` elements for the glass tint and thin white border.
- 2× `<path>` elements for premium edge glints / reveal streaks.
- 1× small chip illustration made from `<rect>` and `<line>` primitives.
- 5× `<text>` elements with explicit `width` for crisp card typography.
- 3× `<filter>` definitions for background glow, panel shadow, and subtle text glow.
- 3× gradient definitions for the background wash, glass tint, and edge highlight.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#050816"/>
      <stop offset="0.45" stop-color="#111B3D"/>
      <stop offset="1" stop-color="#021B2D"/>
    </linearGradient>

    <linearGradient id="glassTint" x1="270" y1="154" x2="1010" y2="566" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.32"/>
      <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#BDEFFF" stop-opacity="0.18"/>
    </linearGradient>

    <linearGradient id="edgeLight" x1="285" y1="160" x2="995" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="0.35" stop-color="#D7F7FF" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="orbBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="46"/>
    </filter>

    <filter id="cardShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2"/>
    </filter>

    <clipPath id="cardClip">
      <rect x="270" y="154" width="740" height="412" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <image href="https://images.example.com/abstract-neon-city-purple-cyan-1280x720.jpg"
         x="0" y="0" width="1280" height="720" opacity="0.72"/>

  <circle cx="180" cy="150" r="210" fill="#FF4D7D" opacity="0.52" filter="url(#orbBlur)"/>
  <circle cx="1015" cy="130" r="250" fill="#7C3CFF" opacity="0.58" filter="url(#orbBlur)"/>
  <circle cx="1090" cy="560" r="260" fill="#00D5FF" opacity="0.48" filter="url(#orbBlur)"/>
  <circle cx="430" cy="650" r="230" fill="#FFB000" opacity="0.24" filter="url(#orbBlur)"/>

  <path d="M-40 520 C210 420 330 650 560 555 C780 465 880 365 1320 430"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>
  <path d="M-30 125 C205 210 350 40 555 115 C760 190 870 260 1320 170"
        fill="none" stroke="#84F4FF" stroke-opacity="0.16" stroke-width="3"/>

  <rect x="270" y="154" width="740" height="412" rx="34" ry="34"
        fill="#000000" opacity="0.28" filter="url(#cardShadow)"/>

  <image href="https://images.example.com/abstract-neon-city-purple-cyan-1280x720-blur30.jpg"
         x="0" y="0" width="1280" height="720" clip-path="url(#cardClip)" opacity="0.96"/>

  <rect x="270" y="154" width="740" height="412" rx="34" ry="34"
        fill="url(#glassTint)"/>

  <rect x="271.5" y="155.5" width="737" height="409" rx="32" ry="32"
        fill="none" stroke="url(#edgeLight)" stroke-width="2"/>

  <path d="M306 176 C290 176 284 188 284 206 L284 284"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.82" stroke-width="3" stroke-linecap="round"/>
  <path d="M322 165 L956 165"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1.5" stroke-linecap="round"/>

  <rect x="318" y="206" width="90" height="64" rx="12" ry="12"
        fill="#F5E8B8" opacity="0.78"/>
  <rect x="331" y="220" width="64" height="38" rx="6" ry="6"
        fill="none" stroke="#6B5E2E" stroke-opacity="0.42" stroke-width="1.5"/>
  <line x1="363" y1="206" x2="363" y2="270" stroke="#6B5E2E" stroke-opacity="0.32" stroke-width="1"/>
  <line x1="318" y1="238" x2="408" y2="238" stroke="#6B5E2E" stroke-opacity="0.28" stroke-width="1"/>

  <text x="885" y="230" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="36"
        font-weight="700" fill="#FFFFFF" text-anchor="end" filter="url(#textGlow)">VISA</text>

  <text x="318" y="340" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="34"
        font-weight="500" letter-spacing="4" fill="#FFFFFF">
    5412  7512  3412  3456
  </text>

  <text x="318" y="408" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        font-weight="600" letter-spacing="2" fill="#DDF7FF" opacity="0.82">CARDHOLDER</text>

  <text x="318" y="438" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="20"
        font-weight="700" letter-spacing="1.5" fill="#FFFFFF">DREAM LIU</text>

  <text x="738" y="408" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        font-weight="600" letter-spacing="2" fill="#DDF7FF" opacity="0.82">VALID THRU</text>

  <text x="738" y="438" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="20"
        font-weight="700" letter-spacing="1.5" fill="#FFFFFF">12/28</text>

  <text x="318" y="518" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#FFFFFF" opacity="0.72">
    Frosted glass panel reveal · duplicate blur crop + translucent tint
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use CSS `backdrop-filter`; PowerPoint will not reproduce it as an editable native effect.
- ❌ Do not use `<mask>` for the frosted region; use a `<clipPath>` on the blurred duplicate `<image>` instead.
- ❌ Do not clip ordinary `<rect>`, `<circle>`, or `<path>` elements expecting a pane crop; clipping is reliable here on `<image>`.
- ❌ Do not use SVG `<animate>` / `<animateTransform>` for the reveal; create two slides and use PowerPoint Morph/Fade.
- ❌ Do not apply a filter to `<line>` elements; use paths or rects for glows/shadows.

## Composition notes
- Place the glass card over the most colorful/high-contrast part of the background so the blur is visibly doing work.
- Keep the panel at roughly 45–60% slide width; leave atmospheric negative space around it so it feels floating, not boxed in.
- For a reveal sequence, make slide 1 use the same card 40–80 px off-position with lower opacity, then slide 2 uses this final layout with PowerPoint Morph.
- Use crisp white typography on the glass; the blur provides readability, while the border and glints sell the physical glass edge.