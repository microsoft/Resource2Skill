# SVG Recipe — Diagonal Corporate Hero Banner

## Visual mechanism
A washed-out full-bleed corporate photo is overlaid with steep diagonal blocks from the left edge, then crossed by a wide white parallelogram title banner with an offset teal shadow. The combination of angled anchors and a horizontal title bar creates a premium, forward-moving executive keynote look.

## SVG primitives needed
- 1× `<image>` for the full-slide corporate architecture / office background
- 1× `<rect>` for the pale mint tint overlay that fades the photo for readability
- 1× `<linearGradient>` for a subtle right-side light wash over the background
- 5× `<path>` for the dark diagonal anchor, teal separator stripe, teal banner shadow, white parallelogram banner, and small decorative diagonal accents
- 1× `<filter id="softShadow">` applied to the main white banner for a restrained executive-card lift
- 1× `<rect>` for a small brand label chip on the left block
- 4× `<text>` for the eyebrow label, main title, subtitle, and small footer label; every text element includes explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="rightWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E6F5F0" stop-opacity="0.05"/>
      <stop offset="55%" stop-color="#E6F5F0" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="tealDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#36B8AD"/>
      <stop offset="100%" stop-color="#178A83"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed faded photo background -->
  <image
    href="https://images.example.com/corporate-glass-architecture-lobby-1920x1080.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Pale corporate tint wash -->
  <rect x="0" y="0" width="1280" height="720" fill="#E6F5F0" opacity="0.80"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#rightWash)"/>

  <!-- Left diagonal anchor block: 40% top width tapering to 15% bottom width -->
  <path d="M 0 0 L 520 0 L 192 720 L 0 720 Z"
        fill="#32373C"/>

  <!-- Teal separator stripe, parallel to the dark block edge -->
  <path d="M 520 0 L 620 0 L 292 720 L 192 720 Z"
        fill="url(#tealDepth)"/>

  <!-- Thin pale diagonal highlight tucked behind the title banner -->
  <path d="M 628 0 L 666 0 L 338 720 L 300 720 Z"
        fill="#FFFFFF" opacity="0.38"/>

  <!-- Brand chip on the dark diagonal area -->
  <rect x="62" y="82" width="178" height="38" rx="19" fill="#FFFFFF" opacity="0.12"/>
  <text x="86" y="107" width="150"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2"
        fill="#D8F4F0">STRATEGY</text>

  <!-- Small left-side supporting text -->
  <text x="68" y="610" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600"
        fill="#FFFFFF" opacity="0.88">2026 Executive Briefing</text>

  <!-- Accent banner shadow, offset down and right from the main white banner -->
  <path d="M 170 420 L 1160 420 L 1010 540 L 20 540 Z"
        fill="#2DA096" opacity="0.96"/>

  <!-- Main white parallelogram title banner -->
  <path d="M 140 395 L 1130 395 L 980 515 L -10 515 Z"
        fill="#FFFFFF" filter="url(#softShadow)"/>

  <!-- Subtle top edge sheen on the white banner -->
  <path d="M 152 407 L 1112 407 L 1095 421 L 136 421 Z"
        fill="#FFFFFF" opacity="0.72"/>

  <!-- Main title inside the parallelogram -->
  <text x="220" y="465" width="790"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800"
        fill="#2DA096">Company Profile</text>

  <!-- Subtitle line aligned to the title, still contained by the banner geometry -->
  <text x="224" y="498" width="760"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" letter-spacing="1.2"
        fill="#515A5E">MARKET POSITION · OPERATING MODEL · GROWTH AGENDA</text>

  <!-- Small decorative diagonal cuts on the far right to echo the left geometry -->
  <path d="M 1138 384 L 1190 384 L 1128 530 L 1076 530 Z"
        fill="#32373C" opacity="0.16"/>
  <path d="M 1202 370 L 1224 370 L 1162 540 L 1140 540 Z"
        fill="#2DA096" opacity="0.58"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `transform="skewX(...)"` to create parallelograms; draw them directly as `<path>` polygons so PowerPoint keeps the geometry editable.
- ❌ Do not use `<mask>` to fade the background photo; use a semi-transparent tint `<rect>` over the image instead.
- ❌ Do not place the title in a rotated text box; keep the text horizontal and let the banner shape carry the diagonal energy.
- ❌ Do not rely on `marker-end` or filtered `<line>` elements for accent details; use filled `<path>` slashes instead.

## Composition notes
- Keep the left diagonal block visually heavy: about 40% of slide width at the top, tapering to roughly 15% at the bottom.
- Place the title banner in the lower-middle band, around 55–72% down the canvas, so it feels grounded and cinematic.
- Use a pale, high-opacity tint over the photo; the image should provide atmosphere, not compete with the banner.
- Repeat the teal accent in both the separator stripe and the banner shadow to create a strong corporate color rhythm.