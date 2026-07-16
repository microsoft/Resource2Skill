# SVG Recipe — Icon-Based Contact Footer

## Visual mechanism
A cinematic closing slide pairs a wide hero image at the top with a clean white contact footer at the bottom. Contact methods are presented as evenly spaced horizontal modules: each starts with a thin hollow circular icon badge, followed by a concise contact detail.

## SVG primitives needed
- 2× `<rect>` for the mint slide background and white lower content field
- 1× `<image>` for the top hero/banner photo, clipped to a soft rounded rectangle
- 1× `<clipPath>` with rounded `<rect>` for the hero photo crop
- 2× translucent `<path>` wave bands for the organic divider between image and footer
- 1× `<linearGradient>` for the teal photo tint overlay
- 1× `<filter id="softShadow">` applied to the hero image card
- 3× `<circle>` for hollow icon badge outlines
- 8× `<path>` / `<line>` / `<circle>` primitives for phone, email, and web icons
- 7× `<text>` blocks for logo, headline, CTA label, and contact details
- 3× tiny decorative `<path>` sparkle marks around the main headline accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="heroTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00D5A8" stop-opacity="0.48"/>
      <stop offset="55%" stop-color="#081F1B" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.55"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-15%" width="120%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroClip">
      <rect x="55" y="38" width="1170" height="300" rx="26" ry="26"/>
    </clipPath>
  </defs>

  <!-- background -->
  <rect x="0" y="0" width="1280" height="720" fill="#D6F1E8"/>
  <rect x="0" y="338" width="1280" height="382" fill="#FFFFFF"/>

  <!-- top cinematic hero -->
  <g filter="url(#softShadow)" transform="rotate(-2.2 640 188)">
    <image x="55" y="38" width="1170" height="300"
           href="https://images.example.com/hero-underwater-green-canyon-presenter.jpg"
           clip-path="url(#heroClip)" preserveAspectRatio="xMidYMid slice"/>
    <rect x="55" y="38" width="1170" height="300" rx="26" ry="26" fill="url(#heroTint)"/>
  </g>

  <!-- small top-right brand mark -->
  <g transform="translate(970 78)">
    <rect x="0" y="0" width="52" height="35" rx="4" fill="none" stroke="#FFFFFF" stroke-width="3"/>
    <line x1="12" y1="35" x2="5" y2="48" stroke="#FFFFFF" stroke-width="3"/>
    <line x1="40" y1="35" x2="47" y2="48" stroke="#FFFFFF" stroke-width="3"/>
    <circle cx="42" cy="10" r="4" fill="#00D9AD"/>
    <text x="66" y="24" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Interactive Media</text>
  </g>

  <!-- organic wave divider -->
  <path d="M0 330 C95 350 155 318 244 338 C365 364 452 325 560 342 C650 355 735 318 842 336 C956 356 1055 330 1160 346 C1210 354 1248 346 1280 338 L1280 398 L0 398 Z"
        fill="#6F7773" opacity="0.68"/>
  <path d="M0 358 C86 375 166 345 265 362 C366 379 462 348 566 364 C676 381 746 346 850 360 C984 379 1080 352 1182 365 C1228 371 1260 366 1280 362 L1280 405 L0 405 Z"
        fill="#AEB6B2" opacity="0.52"/>

  <!-- headline / CTA copy -->
  <text x="78" y="438" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#111111">
    How to Design a
  </text>
  <text x="78" y="486" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#14C7A5">
    Winning Presentation Deck
  </text>
  <path d="M690 454 l14 -14 M710 467 l17 -3 M688 476 l-8 15" stroke="#14C7A5" stroke-width="4" stroke-linecap="round" fill="none"/>
  <path d="M726 442 c8 0 8 12 0 12 c-8 0 -8 -12 0 -12" fill="none" stroke="#14C7A5" stroke-width="3"/>
  <path d="M708 433 l6 -13 l7 13" fill="none" stroke="#14C7A5" stroke-width="3" stroke-linejoin="round"/>
  <text x="490" y="535" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#6D6D6D" text-anchor="middle">
    Call to Action
  </text>

  <!-- contact footer rail -->
  <line x1="105" y1="585" x2="1175" y2="585" stroke="#DDE5E1" stroke-width="2"/>

  <!-- contact block 1: phone -->
  <g transform="translate(120 615)">
    <circle cx="0" cy="0" r="29" fill="none" stroke="#3B3B3B" stroke-width="3"/>
    <path d="M-10 -15 C-18 -8 -18 8 -8 18 C1 27 15 26 21 17 L12 9 C9 12 5 13 1 10 C-4 6 -7 1 -5 -4 C-3 -8 -1 -10 2 -11 Z"
          fill="none" stroke="#3B3B3B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="48" y="-8" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#3C3C3C">PHONE</text>
    <text x="48" y="20" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="600" fill="#3C3C3C">123.456.7890</text>
  </g>

  <!-- contact block 2: email -->
  <g transform="translate(500 615)">
    <circle cx="0" cy="0" r="29" fill="none" stroke="#3B3B3B" stroke-width="3"/>
    <rect x="-17" y="-12" width="34" height="24" rx="3" fill="none" stroke="#3B3B3B" stroke-width="3"/>
    <path d="M-16 -10 L0 2 L16 -10" fill="none" stroke="#3B3B3B" stroke-width="3" stroke-linejoin="round"/>
    <line x1="-16" y1="12" x2="-3" y2="1" stroke="#3B3B3B" stroke-width="3"/>
    <line x1="16" y1="12" x2="3" y2="1" stroke="#3B3B3B" stroke-width="3"/>
    <text x="48" y="-8" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#3C3C3C">EMAIL</text>
    <text x="48" y="20" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="600" fill="#3C3C3C">hello@company.com</text>
  </g>

  <!-- contact block 3: website -->
  <g transform="translate(900 615)">
    <circle cx="0" cy="0" r="29" fill="none" stroke="#3B3B3B" stroke-width="3"/>
    <circle cx="0" cy="0" r="16" fill="none" stroke="#3B3B3B" stroke-width="3"/>
    <path d="M-16 0 H16 M0 -16 C-8 -7 -8 7 0 16 M0 -16 C8 -7 8 7 0 16"
          fill="none" stroke="#3B3B3B" stroke-width="2.6" stroke-linecap="round"/>
    <text x="48" y="-8" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#3C3C3C">WEB</text>
    <text x="48" y="20" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="600" fill="#3C3C3C">www.company.com</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` for small arrow-like icon details; draw icon strokes directly with `<line>` or `<path>`.
- ❌ Do not clip the wavy divider paths; keep clipping only on the hero `<image>`.
- ❌ Do not rely on emoji-only contact icons; they can render inconsistently. Use simple editable line/path icons inside the circles.
- ❌ Do not crowd the footer with more than three or four contact modules; the icon rhythm depends on generous spacing.

## Composition notes
- Keep the hero image in the top 40–50% of the canvas, with the contact footer anchored in the bottom 15–20%.
- Use the wavy divider to soften the transition from cinematic image to white information area.
- The headline sits left-of-center, while the CTA phrase can be centered to create a formal closing-slide pause.
- Contact blocks should share one baseline and one icon size; vary only the text content, not the module geometry.