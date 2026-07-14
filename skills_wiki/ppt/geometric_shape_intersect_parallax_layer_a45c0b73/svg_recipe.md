# SVG Recipe — Geometric Shape Intersect & Parallax Layering

## Visual mechanism
A large rectangular photo is clipped into a crisp geometric silhouette, then paired with offset duplicate outlines to create the illusion that the image and vector frame exist on separate depth planes. The remaining negative space carries bold keynote-style typography with strong shadowing and accent geometry.

## SVG primitives needed
- 1× `<rect>` for the full-slide off-white background
- 2× `<radialGradient>` / `<linearGradient>` fills for warm editorial background glow and dark text treatment
- 2× `<filter>` definitions for soft card shadow and heavy title shadow
- 1× `<clipPath>` with a custom `<path>` hexagon used to crop the hero image
- 1× `<image>` for the hero photograph clipped to the geometric mask
- 4× `<path>` for the geometric frame: shadow carrier, offset cyan outline, offset yellow outline, and front white hairline
- 5× decorative `<path>` shards for parallax accents around the clipped image
- 3× `<rect>` for small metric/status pills and a PowerPoint-like icon tile
- 2× `<circle>` for intersecting icon geometry and background orbital accents
- 8× `<text>` elements for hierarchy: kicker, main title, subtitle, numeric callout, labels, and footer note

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="58%" stop-color="#f5f7fa"/>
      <stop offset="100%" stop-color="#fff0a6"/>
    </linearGradient>

    <radialGradient id="sunGlow" cx="88%" cy="8%" r="70%">
      <stop offset="0%" stop-color="#ffe600" stop-opacity="0.55"/>
      <stop offset="45%" stop-color="#ffd84a" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="titleGold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff400"/>
      <stop offset="100%" stop-color="#ffc700"/>
    </linearGradient>

    <linearGradient id="redType" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#d63a1c"/>
      <stop offset="100%" stop-color="#8e1e12"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleShadow" x="-10%" y="-20%" width="125%" height="150%">
      <feOffset dx="6" dy="7"/>
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroHex">
      <path d="M810 92 L1126 132 L1240 360 L1122 594 L794 626 L668 362 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#sunGlow)"/>
  <circle cx="1178" cy="96" r="4" fill="#ffffff" opacity="0.8"/>
  <circle cx="1118" cy="142" r="2.5" fill="#ffffff" opacity="0.65"/>
  <circle cx="1070" cy="82" r="3" fill="#ffffff" opacity="0.7"/>

  <path d="M766 124 L1082 164 L1196 392 L1078 626 L750 658 L624 394 Z"
        fill="none" stroke="#00bfff" stroke-width="13" opacity="0.85"/>
  <path d="M836 54 L1152 94 L1266 322 L1148 556 L820 588 L694 324 Z"
        fill="none" stroke="#ffe600" stroke-width="8" opacity="0.88"/>

  <path d="M810 92 L1126 132 L1240 360 L1122 594 L794 626 L668 362 Z"
        fill="#ffffff" filter="url(#softShadow)" opacity="0.92"/>

  <image x="632" y="40" width="660" height="640"
         href="https://images.example.com/editorial-glass-architecture-team-hero-photo.jpg"
         clip-path="url(#heroHex)" preserveAspectRatio="xMidYMid slice"/>

  <path d="M810 92 L1126 132 L1240 360 L1122 594 L794 626 L668 362 Z"
        fill="none" stroke="#ffffff" stroke-width="5" opacity="0.85"/>

  <path d="M708 120 L746 88 L770 138 Z" fill="#00bfff" opacity="0.9"/>
  <path d="M1190 188 L1238 172 L1220 226 Z" fill="#ffe600" opacity="0.95"/>
  <path d="M646 502 L702 486 L686 548 Z" fill="#ff6b3a" opacity="0.9"/>
  <path d="M1134 618 L1194 654 L1122 674 Z" fill="#00bfff" opacity="0.65"/>
  <path d="M738 650 L764 606 L804 664 Z" fill="#111827" opacity="0.18"/>

  <text x="54" y="76" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="44"
        font-weight="800" fill="url(#redType)" filter="url(#titleShadow)">2026</text>

  <rect x="54" y="104" width="188" height="44" rx="12" fill="#111827" opacity="0.92"/>
  <text x="74" y="135" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="22"
        font-weight="800" fill="#ffffff" letter-spacing="1.5">NEW RELEASE</text>

  <text x="318" y="112" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="104"
        font-weight="900" fill="url(#titleGold)" filter="url(#titleShadow)">30</text>

  <text x="54" y="224" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="82"
        font-weight="900" fill="url(#titleGold)" filter="url(#titleShadow)" letter-spacing="6">GEOMETRIC</text>

  <text x="54" y="338" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="76"
        font-weight="900" fill="url(#redType)" filter="url(#titleShadow)" letter-spacing="2">PARALLAX</text>

  <text x="54" y="450" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="74"
        font-weight="900" fill="url(#redType)" filter="url(#titleShadow)" letter-spacing="2">LAYERING</text>

  <text x="58" y="512" width="490" font-family="Segoe UI, Microsoft YaHei" font-size="24"
        fill="#313746" opacity="0.9">
    Clip a hero photo into a custom polygon, then offset matching vector outlines to create dimensional shape-intersect depth.
  </text>

  <rect x="58" y="562" width="254" height="66" rx="16" fill="#ffffff" filter="url(#softShadow)"/>
  <circle cx="100" cy="595" r="34" fill="#d84a28"/>
  <circle cx="128" cy="595" r="34" fill="#f47a55" opacity="0.72"/>
  <rect x="62" y="563" width="78" height="64" rx="12" fill="#c83a1e"/>
  <text x="84" y="611" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="48"
        font-weight="700" fill="#ffffff">P</text>
  <text x="334" y="604" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="20"
        font-weight="800" fill="#111827" letter-spacing="1.8">FULLY EDITABLE SVG → PPT</text>

  <text x="54" y="690" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="72"
        font-weight="900" fill="url(#titleGold)" filter="url(#titleShadow)" letter-spacing="5">TIPS &amp; TRICKS</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` for the intersected photo crop; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not apply `clip-path` to vector shapes expecting true boolean intersections; only image clipping is reliably preserved.
- ❌ Do not build the geometric frame with `<use>` clones; duplicate the `<path>` explicitly for each offset layer.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for the parallax offset; draw or translate each outline with explicit coordinates.
- ❌ Do not put shadows on `<line>` elements; use `<path>` outlines or filled carrier paths when a shadow is needed.

## Composition notes
- Reserve roughly 40–45% of the slide width for typography and 55–60% for the oversized clipped image.
- Let the geometric image break the safe margins slightly; this makes the crop feel intentional and editorial rather than like a framed thumbnail.
- Use one vivid outline color and one secondary echo color; too many outline colors will weaken the parallax read.
- Keep shadows strongest on typography and subtle on the geometric image so the offset outlines, not drop shadows, communicate depth.