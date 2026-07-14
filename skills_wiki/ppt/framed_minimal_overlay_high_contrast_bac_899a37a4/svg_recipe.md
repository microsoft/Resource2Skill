# SVG Recipe — Framed Minimal Overlay (High-Contrast Background Juxtaposition)

## Visual mechanism
A dense, colorful full-bleed background is intentionally contrasted with a stark charcoal rectangular overlay that creates a clean legibility zone. A thin inset white frame and restrained white typography make the overlay feel like a premium editorial plaque rather than a basic text box.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark-to-light background base
- 12–18× `<path>` for overlapping colorful geometric shards in the background
- 2–3× `<ellipse>` for soft blurred glow fields behind the shards
- 1× `<rect>` for the solid charcoal overlay plate
- 1× `<rect>` for the inset white frame, transparent fill
- 1× `<line>` for the delicate typographic separator
- 2× `<text>` elements for the title and subtitle, each with explicit `width`
- 4× `<linearGradient>` for background atmosphere and shard depth
- 1× `<radialGradient>` for colored glow accents
- 1× `<filter id="plateShadow">` applied to the overlay plate
- 1× `<filter id="softGlow">` applied to background ellipses

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#f7fbff"/>
      <stop offset="0.45" stop-color="#dbe8f7"/>
      <stop offset="1" stop-color="#101827"/>
    </linearGradient>

    <linearGradient id="redShard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ff7a5c"/>
      <stop offset="1" stop-color="#c81e4a"/>
    </linearGradient>

    <linearGradient id="blueShard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#28d8ff"/>
      <stop offset="1" stop-color="#2354d8"/>
    </linearGradient>

    <linearGradient id="greenShard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#a8ff78"/>
      <stop offset="1" stop-color="#22a66a"/>
    </linearGradient>

    <linearGradient id="goldShard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffe76a"/>
      <stop offset="1" stop-color="#f09a20"/>
    </linearGradient>

    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#38e8ff" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#38e8ff" stop-opacity="0"/>
    </radialGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <filter id="plateShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <ellipse cx="270" cy="180" rx="310" ry="150" fill="url(#cyanGlow)" filter="url(#softGlow)" opacity="0.9"/>
  <ellipse cx="930" cy="500" rx="360" ry="190" fill="url(#cyanGlow)" filter="url(#softGlow)" opacity="0.45"/>

  <path d="M-80 130 L240 35 L415 190 L90 290 Z" fill="url(#redShard)" opacity="0.90"/>
  <path d="M145 -55 L470 20 L420 250 L90 175 Z" fill="url(#blueShard)" opacity="0.82"/>
  <path d="M455 30 L760 -30 L845 210 L530 285 Z" fill="url(#goldShard)" opacity="0.86"/>
  <path d="M770 0 L1095 90 L1000 310 L690 215 Z" fill="url(#greenShard)" opacity="0.82"/>
  <path d="M1030 -50 L1360 35 L1270 285 L970 170 Z" fill="url(#redShard)" opacity="0.78"/>

  <path d="M-65 330 L250 230 L380 430 L40 535 Z" fill="url(#greenShard)" opacity="0.83"/>
  <path d="M250 240 L585 185 L660 410 L320 470 Z" fill="url(#blueShard)" opacity="0.80"/>
  <path d="M520 250 L835 180 L900 390 L585 465 Z" fill="url(#redShard)" opacity="0.76"/>
  <path d="M835 210 L1165 145 L1220 370 L900 440 Z" fill="url(#goldShard)" opacity="0.78"/>
  <path d="M1110 230 L1400 165 L1360 490 L1060 540 Z" fill="url(#blueShard)" opacity="0.72"/>

  <path d="M35 560 L340 435 L485 730 L160 820 Z" fill="url(#goldShard)" opacity="0.80"/>
  <path d="M350 495 L660 395 L800 720 L455 815 Z" fill="url(#greenShard)" opacity="0.74"/>
  <path d="M650 505 L990 385 L1120 720 L760 820 Z" fill="url(#blueShard)" opacity="0.76"/>
  <path d="M975 515 L1325 420 L1390 745 L1050 825 Z" fill="url(#redShard)" opacity="0.78"/>

  <path d="M0 0 L1280 0 L1280 720 L0 720 Z" fill="#000000" opacity="0.10"/>
  <path d="M720 0 L1280 0 L1280 720 L1010 720 Z" fill="#000000" opacity="0.22"/>

  <rect x="690" y="334" width="520" height="278" fill="#282828" filter="url(#plateShadow)"/>
  <rect x="720" y="364" width="460" height="218" fill="none" stroke="#ffffff" stroke-width="2"/>

  <text x="750" y="428" width="400" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="600" fill="#ffffff" text-anchor="middle">
    <tspan x="950" dy="0">MARKET SIGNALS</tspan>
    <tspan x="950" dy="52">REDEFINED</tspan>
  </text>

  <line x1="855" y1="508" x2="1045" y2="508" stroke="#ffffff" stroke-width="1.5" opacity="0.9"/>

  <text x="790" y="548" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="300" letter-spacing="1.6" fill="#ffffff" text-anchor="middle">
    <tspan x="950">2026 STRATEGIC OUTLOOK</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Placing white text directly on the chaotic background; the technique depends on a controlled dark legibility zone.
- ❌ Making the overlay semi-transparent unless the background is very subdued; too much bleed-through weakens the high-contrast plaque effect.
- ❌ Using `<mask>` or `clip-path` on non-image elements to create the frame; use a normal transparent-fill `<rect>` with a white stroke.
- ❌ Using `<pattern>` fills for the busy background; build the complexity with editable colored paths and gradients instead.
- ❌ Over-decorating the overlay itself; the plaque should remain minimal so the background can stay visually energetic.

## Composition notes
- Position the overlay asymmetrically, typically right-of-center and below the vertical midpoint, leaving the background visible as the main visual hook.
- Keep the plate around 35–45% of slide width and 35–45% of slide height; it should feel substantial but not dominate the slide.
- Use a tight internal margin: the inset frame should sit about 24–32 px from the plate edge, with typography centered inside it.
- Let the background carry color variety while the overlay uses only charcoal, white, and subtle shadow for an executive, high-contrast rhythm.