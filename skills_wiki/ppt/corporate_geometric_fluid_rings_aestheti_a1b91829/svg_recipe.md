# SVG Recipe — Corporate Geometric Fluid Rings Aesthetic

## Visual mechanism
A deep blue-to-indigo gradient field is overlaid with oversized, semi-transparent stroked circles and ellipses so only ring segments are visible, creating a macro “fluid geometry” texture. Crisp white typography and optional frosted content cards sit above the soft rings, giving the slide a premium corporate/SaaS keynote feel without hurting readability.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background.
- 5× `<circle>` / `<ellipse>` for giant translucent geometric rings, each with thick strokes and no fill.
- 3× `<ellipse>` for blurred cyan/violet ambient glow fields.
- 2× `<path>` for subtle diagonal luminous ribbons that add depth behind the rings.
- 2× `<rect>` for foreground glass-like content cards.
- 6× `<text>` for title, subtitle, section labels, and metric copy; every text element has an explicit `width`.
- 2× `<linearGradient>` for the base background and card surface.
- 2× `<radialGradient>` for atmospheric glow color.
- 2× `<filter>` using `feGaussianBlur` and `feOffset+feGaussianBlur+feMerge` for soft glow and card shadow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgIndigo" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#090D23"/>
      <stop offset="48%" stop-color="#101B42"/>
      <stop offset="100%" stop-color="#19326E"/>
    </linearGradient>

    <linearGradient id="cardGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#B8CCFF" stop-opacity="0.08"/>
    </linearGradient>

    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#52D8FF" stop-opacity="0.42"/>
      <stop offset="70%" stop-color="#4B7BFF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#4B7BFF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="violetGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#A781FF" stop-opacity="0.34"/>
      <stop offset="75%" stop-color="#7E55FF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#7E55FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgIndigo)"/>

  <ellipse cx="1030" cy="75" rx="320" ry="180" fill="url(#cyanGlow)" filter="url(#softBlur)" opacity="0.75"/>
  <ellipse cx="125" cy="650" rx="330" ry="210" fill="url(#violetGlow)" filter="url(#softBlur)" opacity="0.72"/>
  <ellipse cx="690" cy="390" rx="390" ry="210" fill="url(#cyanGlow)" filter="url(#softBlur)" opacity="0.24"/>

  <path d="M-60,165 C210,75 385,195 620,122 C835,55 1040,42 1340,122"
        fill="none" stroke="#6A8DFF" stroke-width="34" stroke-opacity="0.055"/>
  <path d="M-90,566 C175,478 375,615 610,535 C850,452 1038,490 1370,405"
        fill="none" stroke="#8FDFFF" stroke-width="22" stroke-opacity="0.07"/>

  <circle cx="165" cy="118" r="432" fill="none" stroke="#6B91FF" stroke-width="118" stroke-opacity="0.15"/>
  <circle cx="1120" cy="170" r="392" fill="none" stroke="#83A5FF" stroke-width="154" stroke-opacity="0.12"/>
  <ellipse cx="940" cy="720" rx="438" ry="392" fill="none" stroke="#507BFF" stroke-width="110" stroke-opacity="0.16"
           transform="rotate(-14 940 720)"/>
  <circle cx="278" cy="775" r="320" fill="none" stroke="#78A0FF" stroke-width="92" stroke-opacity="0.14"/>
  <ellipse cx="1192" cy="625" rx="186" ry="186" fill="none" stroke="#B7C9FF" stroke-width="48" stroke-opacity="0.19"
           stroke-dasharray="260 58"/>

  <circle cx="720" cy="132" r="210" fill="none" stroke="#9DB7FF" stroke-width="2" stroke-opacity="0.20"/>
  <circle cx="82" cy="344" r="168" fill="none" stroke="#E4EEFF" stroke-width="1.5" stroke-opacity="0.13"/>
  <ellipse cx="1110" cy="420" rx="260" ry="210" fill="none" stroke="#C9D8FF" stroke-width="1.5" stroke-opacity="0.14"
           transform="rotate(18 1110 420)"/>

  <text x="92" y="92" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#AFC4FF" letter-spacing="3" font-weight="600">ENTERPRISE CLOUD PLATFORM</text>

  <text x="92" y="205" width="590" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" fill="#FFFFFF" font-weight="600">
    <tspan x="92" dy="0">Fluid systems,</tspan>
    <tspan x="92" dy="68">measurable growth.</tspan>
  </text>

  <text x="96" y="366" width="540" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" fill="#D7E3FF" opacity="0.92">
    Premium geometric depth for corporate strategy, SaaS launches, and technology leadership narratives.
  </text>

  <rect x="742" y="426" width="390" height="138" rx="24" fill="url(#cardGlass)"
        stroke="#DDE8FF" stroke-opacity="0.20" filter="url(#cardShadow)"/>
  <text x="780" y="478" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#BFD1FF" font-weight="600">ACTIVE ACCOUNTS</text>
  <text x="780" y="532" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" fill="#FFFFFF" font-weight="700">24.8M</text>

  <rect x="742" y="586" width="390" height="78" rx="22" fill="#FFFFFF" fill-opacity="0.075"
        stroke="#FFFFFF" stroke-opacity="0.13"/>
  <text x="780" y="636" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" fill="#ECF3FF">Global uptime 99.99%</text>
</svg>
```

## Avoid in this skill
- ❌ Using a flattened bitmap background when the rings can be editable SVG `<circle>` / `<ellipse>` strokes.
- ❌ Thin, fully visible centered circles; the premium look comes from oversized cropped arcs at the slide edges.
- ❌ High-opacity rings behind body text; keep ring stroke opacity around `0.08–0.20` for readability.
- ❌ Applying `filter` to `<line>` elements or relying on SVG masks; use blurred ellipses and transparent strokes instead.
- ❌ Overfilling the slide with cards; the background needs large negative space to feel executive rather than dashboard-like.

## Composition notes
- Keep the main title in a clean open zone, usually left-center or center, with the largest ring mass pushed to corners.
- Use 2–3 giant cropped rings plus 1 smaller accent ring; vary radius, stroke width, and opacity to create depth.
- Pair soft geometry with hard corporate foreground elements: frosted cards, sharp metrics, and crisp white text.
- Color rhythm should stay in deep indigo, royal blue, cyan, and periwinkle; avoid warm accent colors unless used very sparingly.