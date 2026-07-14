# SVG Recipe — Split Banner Testimonial

## Visual mechanism
A wide hero banner occupies the upper half of the slide, carrying visual context and a concise headline; a calmer lower testimonial panel separates the human proof point with avatar, author details, and an oversized editorial quote. The split horizontal structure feels warm and premium because the top image is cinematic while the bottom uses generous whitespace, soft shadows, and restrained accent marks.

## SVG primitives needed
- 4× `<rect>` for the warm page background, rounded testimonial card, image tint overlay, and small accent blocks
- 2× `<image>` for the panoramic hero photo and circular author portrait
- 2× `<clipPath>` for rounded-corner hero image cropping and circular avatar cropping
- 3× `<linearGradient>` for background wash, hero darkening overlay, and warm gold accent fill
- 1× `<filter id="softShadow">` applied to the testimonial card
- 1× `<filter id="glow">` applied to the decorative accent blob
- 3× `<path>` for editorial organic decoration, oversized quote mark, and subtle swoosh accent
- 1× `<line>` for the thin separation rule between author block and quote
- 7× `<text>` elements for kicker, headline, author name, role, quote lines, and small attribution label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pageWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF8EF"/>
      <stop offset="58%" stop-color="#F6EFE4"/>
      <stop offset="100%" stop-color="#EFE4D5"/>
    </linearGradient>

    <linearGradient id="heroShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1C1714" stop-opacity="0.78"/>
      <stop offset="50%" stop-color="#1C1714" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#1C1714" stop-opacity="0.06"/>
    </linearGradient>

    <linearGradient id="goldAccent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F3C776"/>
      <stop offset="100%" stop-color="#C8873E"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="heroClip">
      <rect x="72" y="52" width="1136" height="316" rx="34" ry="34"/>
    </clipPath>

    <clipPath id="avatarClip">
      <circle cx="176" cy="507" r="48"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#pageWash)"/>

  <path d="M1044 18 C1128 4 1216 46 1242 119 C1268 192 1202 250 1124 238 C1045 226 993 167 1010 91 C1016 61 1021 28 1044 18 Z"
        fill="#F1D0A0" opacity="0.34" filter="url(#glow)"/>

  <image href="https://images.example.com/premium-hospitality-team-in-warm-modern-lobby.jpg"
         x="72" y="52" width="1136" height="316"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroClip)"/>

  <rect x="72" y="52" width="1136" height="316" rx="34" ry="34" fill="url(#heroShade)"/>

  <rect x="104" y="88" width="86" height="6" rx="3" fill="url(#goldAccent)"/>

  <text x="104" y="126" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.5"
        fill="#F6D9A7">
    CLIENT STORY
  </text>

  <text x="104" y="192" width="580"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="700"
        fill="#FFF9F1">
    <tspan x="104" dy="0">A service experience</tspan>
    <tspan x="104" dy="57">people remember.</tspan>
  </text>

  <text x="106" y="292" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400"
        fill="#F6E7D4" opacity="0.92">
    Split the visual promise from the customer proof.
  </text>

  <rect x="104" y="404" width="1072" height="238" rx="30" ry="30"
        fill="#FFFDF8" filter="url(#softShadow)"/>

  <path d="M1058 408 C1118 405 1168 438 1174 496 C1180 554 1132 604 1068 604 C1004 604 956 559 963 501 C970 443 1000 412 1058 408 Z"
        fill="#FAE8CA" opacity="0.62"/>

  <path d="M717 439 C739 423 769 424 786 445 C803 466 794 497 770 510 C744 524 710 513 700 486 C693 467 700 451 717 439 Z"
        fill="#F4C979" opacity="0.20"/>

  <image href="https://images.example.com/portrait-of-confident-female-founder-warm-light.jpg"
         x="128" y="459" width="96" height="96"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#avatarClip)"/>

  <circle cx="176" cy="507" r="51" fill="none" stroke="#F1C27A" stroke-width="4"/>

  <text x="248" y="493" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700"
        fill="#251B14">
    Maya Chen
  </text>

  <text x="248" y="523" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="500"
        fill="#8A7564">
    Chief Customer Officer, Lumina Hotels
  </text>

  <text x="248" y="562" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.8"
        fill="#C8873E">
    VERIFIED TESTIMONIAL
  </text>

  <line x1="558" y1="444" x2="558" y2="602" stroke="#E9DCCD" stroke-width="1.5"/>

  <path d="M635 470 C635 442 653 423 682 417 L690 436 C673 441 665 452 666 468 L693 468 L693 521 L635 521 Z"
        fill="url(#goldAccent)" opacity="0.92"/>

  <text x="724" y="478" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="600"
        fill="#2C2119">
    <tspan x="724" dy="0">“The new onboarding flow</tspan>
    <tspan x="724" dy="40">turned first-time guests into</tspan>
    <tspan x="724" dy="40">loyal advocates almost</tspan>
    <tspan x="724" dy="40">overnight.”</tspan>
  </text>

  <text x="724" y="614" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="500"
        fill="#9B8673">
    38% lift in return bookings within one quarter
  </text>

  <path d="M1118 600 C1138 579 1165 573 1192 582"
        fill="none" stroke="#D49A4D" stroke-width="5" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade the hero image; use a same-size rounded `<rect>` with a gradient fill over the image instead.
- ❌ Do not rely on automatic text wrapping for the quote; create explicit `<tspan>` lines and give every `<text>` a `width`.
- ❌ Do not apply `clip-path` to decorative rectangles or overlays; clipping is only reliable on `<image>` for this workflow.
- ❌ Do not use `<textPath>` for the quote or attribution; keep typography as normal editable text.

## Composition notes
- Keep the hero banner around 40–45% of slide height so it feels cinematic but leaves enough space for the testimonial card.
- Place the headline on the darker side of the hero image; add a gradient overlay to guarantee contrast.
- Use the lower panel for proof: avatar and author metadata on the left, quote on the right, separated by a thin rule.
- Repeat one warm accent color in the hero label, avatar ring, quote mark, and final swoosh to visually connect both halves.