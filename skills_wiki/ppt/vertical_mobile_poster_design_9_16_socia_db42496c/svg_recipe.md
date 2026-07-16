# SVG Recipe — Vertical Mobile Poster Design (9:16 Social Media Layout)

## Visual mechanism
A portrait 9:16 poster is staged inside the standard 1280×720 SVG canvas as a centered vertical artboard, using full-bleed photography, a thin inset gold frame, solid text banners, and high-contrast centered typography. The premium look comes from strict symmetry, sampled accent colors, and clear mobile-safe zones.

## SVG primitives needed
- 1× `<image>` for the full-bleed portrait background photo, clipped to a 9:16 poster rectangle
- 1× `<clipPath>` with `<rect>` for cropping the photo to the vertical poster area
- 1× `<linearGradient>` for a subtle dark readability veil over the photo
- 1× `<filter id="posterShadow">` for the floating poster card shadow
- 1× `<filter id="softGlow">` for warm frame/title glow
- 1× outer `<rect>` for the landscape slide background
- 1× poster base `<rect>` for shadow and portrait boundary
- 1× translucent overlay `<rect>` for mobile text readability
- 1× hollow `<rect>` for the inset gold editorial frame
- 2× decorative `<line>` elements for fine divider rules
- 2× solid `<rect>` banner blocks for subtitle and CTA information
- 1× rounded white `<rect>` QR-code plate
- Multiple small `<rect>` elements for an editable mock QR code
- 5× `<text>` elements for event tag, large display title, subtitle, CTA, and footer metadata
- 2× decorative `<path>` flourishes for organic premium poster detailing

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="posterClip">
      <rect x="438" y="0" width="405" height="720" rx="0"/>
    </clipPath>

    <linearGradient id="photoVeil" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#050403" stop-opacity="0.18"/>
      <stop offset="38%" stop-color="#050403" stop-opacity="0.08"/>
      <stop offset="72%" stop-color="#050403" stop-opacity="0.40"/>
      <stop offset="100%" stop-color="#050403" stop-opacity="0.72"/>
    </linearGradient>

    <filter id="posterShadow" x="-20%" y="-10%" width="140%" height="120%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#17130f"/>
  <rect x="438" y="0" width="405" height="720" fill="#0d0b08" filter="url(#posterShadow)"/>

  <image
    x="438" y="0" width="405" height="720"
    href="https://images.example.com/portrait-dark-autumn-harvest-food-photography.jpg"
    clip-path="url(#posterClip)"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="438" y="0" width="405" height="720" fill="url(#photoVeil)"/>

  <path d="M483 88 C512 62, 557 59, 582 82 C551 78, 525 90, 504 116 C495 106, 489 97, 483 88 Z"
        fill="#d2a673" opacity="0.28"/>
  <path d="M797 620 C770 652, 725 658, 694 637 C729 640, 754 626, 776 597 C785 605, 792 613, 797 620 Z"
        fill="#d2a673" opacity="0.22"/>

  <rect x="476" y="46" width="329" height="628"
        fill="none" stroke="#d2a673" stroke-width="3.5" opacity="0.95"/>
  <rect x="488" y="58" width="305" height="604"
        fill="none" stroke="#d2a673" stroke-width="1.1" opacity="0.42"/>

  <line x1="536" y1="134" x2="744" y2="134" stroke="#d2a673" stroke-width="1.2" opacity="0.75"/>
  <line x1="536" y1="586" x2="744" y2="586" stroke="#d2a673" stroke-width="1.2" opacity="0.75"/>

  <text x="640" y="116" width="260" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" letter-spacing="3"
        fill="#f5dfbd" font-weight="600">
    SEASONAL TASTING
  </text>

  <text x="640" y="252" width="310" text-anchor="middle"
        font-family="Microsoft YaHei, Segoe UI" font-size="54" font-weight="700"
        fill="#fff6e8" filter="url(#softGlow)">
    <tspan x="640" dy="0">秋日丰收</tspan>
    <tspan x="640" dy="66">宴</tspan>
  </text>

  <text x="640" y="383" width="288" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18"
        fill="#f2d8b0" letter-spacing="1.5">
    AUTUMN HARVEST DINNER
  </text>

  <rect x="512" y="425" width="256" height="86" rx="0"
        fill="#781e1e" opacity="0.96"/>
  <text x="640" y="458" width="226" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18"
        fill="#ffffff" font-weight="700">
    <tspan x="640" dy="0">Autumn Harvest • Winter Storage</tspan>
    <tspan x="640" dy="27">Warm Forward Journey</tspan>
  </text>

  <rect x="566" y="532" width="148" height="82" rx="8"
        fill="#ffffff" opacity="0.96"/>
  <rect x="580" y="546" width="16" height="16" fill="#111111"/>
  <rect x="600" y="546" width="8" height="8" fill="#111111"/>
  <rect x="624" y="546" width="12" height="12" fill="#111111"/>
  <rect x="660" y="546" width="20" height="20" fill="#111111"/>
  <rect x="688" y="546" width="12" height="12" fill="#111111"/>
  <rect x="580" y="570" width="10" height="10" fill="#111111"/>
  <rect x="600" y="568" width="20" height="12" fill="#111111"/>
  <rect x="636" y="570" width="8" height="8" fill="#111111"/>
  <rect x="654" y="574" width="12" height="12" fill="#111111"/>
  <rect x="684" y="568" width="16" height="16" fill="#111111"/>
  <rect x="582" y="592" width="18" height="10" fill="#111111"/>
  <rect x="614" y="588" width="10" height="18" fill="#111111"/>
  <rect x="640" y="594" width="22" height="8" fill="#111111"/>
  <rect x="674" y="590" width="8" height="16" fill="#111111"/>
  <rect x="692" y="592" width="10" height="10" fill="#111111"/>

  <text x="640" y="636" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#ffffff" font-weight="600">
    Scan to reserve your seat
  </text>

  <text x="640" y="657" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="11"
        fill="#d2a673" letter-spacing="1.2">
    NOV 18 · 19:30 · GARDEN HOUSE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not make the whole SVG canvas portrait; keep `viewBox="0 0 1280 720"` and construct the 9:16 poster as a centered vertical artboard.
- ❌ Do not use `mask` to darken or crop the photo; use a clipped `<image>` plus normal translucent `<rect>` overlays.
- ❌ Do not use `<pattern>` for the QR code or texture; build QR modules with editable small `<rect>` elements or use an image only if editability is not required.
- ❌ Do not rely on text without `width`; every `<text>` needs an explicit `width` for PowerPoint rendering.
- ❌ Do not apply `clip-path` to text, paths, or rectangles; only the background `<image>` should be clipped.
- ❌ Do not use custom web fonts as the only typographic source; specify Microsoft YaHei / Segoe UI fallbacks.

## Composition notes
- Center the 9:16 artboard at `x≈438`, `width≈405`, `height=720`; this preserves a true mobile-poster ratio inside the required 16:9 SVG canvas.
- Keep the gold frame 35–45 px inside the portrait edge so all text remains in a mobile safe zone.
- Put the emotional visual weight in the upper/middle third with the large title; reserve the lower third for subtitle, QR, CTA, and metadata.
- Sample accent colors from the photo: warm gold for frame/detail, deep crimson or dark brown for banners, ivory/white for readable text.