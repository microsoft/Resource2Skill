# SVG Recipe — Flat-Pop Typographic Hero Slide

## Visual mechanism
Massive italic white typography sits on a saturated flat background, with an equally sharp dark duplicate offset down-right to create a zero-blur retro hard shadow. The slide reads like a screen-printed poster: loud color, compressed line spacing, brutal contrast, and a few simple pop-art accent shapes.

## SVG primitives needed
- 1× `<rect>` for the full-bleed vibrant background.
- 2× decorative `<path>` starbursts for flat-pop motion energy behind the title.
- 12× small `<circle>` dots for hand-placed halftone-style accents without using unsupported pattern fills.
- 6× `<text>` elements for the title: 3 dark offset shadow lines and 3 white foreground lines.
- 2× `<text>` elements for small kicker/label copy, each with explicit `width`.
- 2× `<rect>` accent bars for a bold editorial framing device.
- 1× `<linearGradient>` for a subtle accent fill on the lower ribbon; keep the main slide flat.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="ribbonGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFD447"/>
      <stop offset="100%" stop-color="#FF8A00"/>
    </linearGradient>
  </defs>

  <!-- Flat saturated background -->
  <rect x="0" y="0" width="1280" height="720" fill="#E2231A"/>

  <!-- Pop-art burst shapes -->
  <path d="M110 112 L154 132 L190 96 L184 148 L238 158 L187 181 L203 232 L158 199 L116 236 L128 182 L76 162 L130 148 Z"
        fill="#FFD447" opacity="0.95"/>
  <path d="M1044 508 L1088 524 L1123 486 L1120 540 L1174 548 L1125 573 L1145 623 L1098 592 L1059 632 L1067 576 L1014 560 L1068 545 Z"
        fill="#FFFFFF" opacity="0.18"/>

  <!-- Manual halftone dots: editable circles, not a pattern -->
  <circle cx="1002" cy="116" r="10" fill="#4A0905" opacity="0.45"/>
  <circle cx="1044" cy="116" r="10" fill="#4A0905" opacity="0.45"/>
  <circle cx="1086" cy="116" r="10" fill="#4A0905" opacity="0.45"/>
  <circle cx="1023" cy="156" r="10" fill="#4A0905" opacity="0.35"/>
  <circle cx="1065" cy="156" r="10" fill="#4A0905" opacity="0.35"/>
  <circle cx="1107" cy="156" r="10" fill="#4A0905" opacity="0.35"/>
  <circle cx="180" cy="548" r="8" fill="#FFFFFF" opacity="0.30"/>
  <circle cx="218" cy="548" r="8" fill="#FFFFFF" opacity="0.30"/>
  <circle cx="256" cy="548" r="8" fill="#FFFFFF" opacity="0.30"/>
  <circle cx="199" cy="584" r="8" fill="#FFFFFF" opacity="0.22"/>
  <circle cx="237" cy="584" r="8" fill="#FFFFFF" opacity="0.22"/>
  <circle cx="275" cy="584" r="8" fill="#FFFFFF" opacity="0.22"/>

  <!-- Hard-shadow title block: duplicate text offset down-right -->
  <g transform="rotate(-4 640 360)">
    <text x="656" y="260" width="980" text-anchor="middle"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
          font-size="106" font-weight="900" font-style="italic"
          letter-spacing="-5" fill="#4A0905">NUTS</text>
    <text x="658" y="370" width="1040" text-anchor="middle"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
          font-size="106" font-weight="900" font-style="italic"
          letter-spacing="-5" fill="#4A0905">&amp; BOLTS</text>
    <text x="660" y="480" width="1100" text-anchor="middle"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
          font-size="106" font-weight="900" font-style="italic"
          letter-spacing="-5" fill="#4A0905">SPEED TRAINING</text>

    <text x="640" y="244" width="980" text-anchor="middle"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
          font-size="106" font-weight="900" font-style="italic"
          letter-spacing="-5" fill="#FFFFFF">NUTS</text>
    <text x="642" y="354" width="1040" text-anchor="middle"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
          font-size="106" font-weight="900" font-style="italic"
          letter-spacing="-5" fill="#FFFFFF">&amp; BOLTS</text>
    <text x="644" y="464" width="1100" text-anchor="middle"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
          font-size="106" font-weight="900" font-style="italic"
          letter-spacing="-5" fill="#FFFFFF">SPEED TRAINING</text>
  </g>

  <!-- Editorial framing accents -->
  <rect x="414" y="92" width="452" height="14" rx="7" fill="#4A0905"/>
  <rect x="440" y="612" width="400" height="18" rx="9" fill="url(#ribbonGrad)"/>

  <!-- Small supporting copy -->
  <text x="640" y="78" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" letter-spacing="5"
        fill="#FFFFFF" opacity="0.88">POWERPOINT WORKSHOP</text>
  <text x="640" y="666" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="800" letter-spacing="3"
        fill="#4A0905">FAST CUTS · BIG TYPE · ZERO BLUR</text>
</svg>
```

## Avoid in this skill
- ❌ Soft blurred drop shadows; the visual signature is a hard, offset duplicate with no blur.
- ❌ `<filter>` shadows if precise editability is more important than automation; duplicated text is easier to adjust in PowerPoint.
- ❌ `<pattern>` halftones; place individual circles instead so the dots remain editable.
- ❌ Thin fonts, long paragraphs, or dashboard-like layouts; this style depends on oversized condensed title energy.
- ❌ `transform="skewX(...)"` to fake italics; use `font-style="italic"` and optional `rotate(...)` only.

## Composition notes
- Keep the title block dominant: roughly 70–85% of slide width and centered vertically.
- Use compressed line spacing by manually setting each line’s `y` value close together.
- Put the dark shadow text 14–22 px down-right from the white text for a punchy 45-degree offset.
- Limit the palette to one flat background, white type, one dark shadow color, and one warm accent.