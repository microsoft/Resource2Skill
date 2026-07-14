# SVG Recipe — Offset Bar Title Graphic

## Visual mechanism
A centered title lockup built from two wide horizontal bars that are stacked and slightly offset down/right, creating a crisp layered-shadow effect. Small angled trapezoid tags at the bar ends invert the bar colors and add motion without compromising the minimalist executive look.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm background
- 4× `<rect>` for subtle oversized background ribbons that make the flat backdrop feel designed
- 2× `<circle>` for soft ambient glows behind the title graphic
- 2× `<rect>` for the main white title bar and black subtitle bar
- 2× `<path>` for angled end tags attached to the bars
- 2× `<text>` for the main title and subtitle, each with explicit `width=`
- 1× `<linearGradient id="bgGradient">` for a premium muted tan background
- 1× `<linearGradient id="paperSheen">` for a very light highlight on the white bar
- 1× `<radialGradient id="ambientGlow">` for soft background glow accents
- 1× `<filter id="barShadow">` using `feOffset + feGaussianBlur + feMerge` for subtle depth on editable bar shapes
- 1× `<filter id="ambientBlur">` using `feGaussianBlur` for blurred decorative glow circles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#D8B071"/>
      <stop offset="0.55" stop-color="#D1A05E"/>
      <stop offset="1" stop-color="#B98349"/>
    </linearGradient>

    <linearGradient id="paperSheen" x1="315" y1="278" x2="965" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.55" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F0ECE4"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFF3D2" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#FFF3D2" stop-opacity="0"/>
    </radialGradient>

    <filter id="barShadow" x="-8%" y="-20%" width="116%" height="150%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ambientBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>

  <circle cx="238" cy="210" r="150" fill="url(#ambientGlow)" filter="url(#ambientBlur)"/>
  <circle cx="1034" cy="512" r="190" fill="url(#ambientGlow)" filter="url(#ambientBlur)" opacity="0.65"/>

  <rect x="-80" y="95" width="430" height="18" fill="#FFFFFF" opacity="0.13" transform="rotate(-8 135 104)"/>
  <rect x="930" y="130" width="360" height="14" fill="#FFFFFF" opacity="0.12" transform="rotate(-8 1110 137)"/>
  <rect x="55" y="570" width="520" height="16" fill="#1A1714" opacity="0.10" transform="rotate(-8 315 578)"/>
  <rect x="790" y="605" width="430" height="12" fill="#1A1714" opacity="0.10" transform="rotate(-8 1005 611)"/>

  <rect x="335" y="374" width="650" height="72" fill="#101010" filter="url(#barShadow)"/>
  <path d="M985 374 L1030 374 L1008 446 L985 446 Z" fill="#FFFFFF"/>

  <rect x="315" y="278" width="650" height="82" fill="url(#paperSheen)" filter="url(#barShadow)"/>
  <path d="M965 278 L1012 278 L990 360 L965 360 Z" fill="#101010"/>

  <text x="640" y="322"
        width="650"
        text-anchor="middle"
        dominant-baseline="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38"
        font-weight="700"
        letter-spacing="1"
        fill="#101010">PDF 转换工具</text>

  <text x="660" y="411"
        width="650"
        text-anchor="middle"
        dominant-baseline="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25"
        font-weight="500"
        letter-spacing="3"
        fill="#FFFFFF">WWW.ILOVEPDF.COM</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut angled tag shapes; draw the trapezoids directly with `<path>`.
- ❌ Do not put `clip-path` on the bars or text; clipping non-image elements will be ignored.
- ❌ Do not use `<use>` to duplicate bars or tags; create each editable shape explicitly.
- ❌ Do not rely on text auto-fit; every `<text>` must include a fixed `width=`.
- ❌ Do not use `skewX`, `skewY`, or `matrix()` for the angled tags; use path geometry instead.

## Composition notes
- Keep the title lockup centered, occupying roughly 55–65% of slide width and only 20–25% of slide height.
- The offset should be small and deliberate: around 15–25 px horizontally and 12–18 px vertically.
- Use high contrast inside each bar: black text on white, white text on black.
- Let the background stay warm and quiet; decorative ribbons and glows should support the title, not compete with it.