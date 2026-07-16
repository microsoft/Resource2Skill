# SVG Recipe — Pill-Shaped Bar Chart with Highlight

## Visual mechanism
Build each horizontal bar from a flat-start rectangle plus a perfectly aligned circular cap, creating a modern “pill terminus” while keeping the origin mathematically crisp. Use an accent color only on the top-performing rows and mute the rest in cool grey so the audience immediately reads the intended takeaway.

## SVG primitives needed
- 1× `<rect>` for the clean white slide background
- 1× decorative `<path>` for a soft executive-style background accent
- 4× pale `<path>` rail shapes showing the 100% bar capacity
- 4× shadow `<path>` shapes behind the active bars to add subtle depth without filtering the bar pieces themselves
- 4× active `<rect>` bar bodies with flat left edges
- 4× active `<circle>` bar tips aligned to the right edge of each bar body
- 4× `<text>` category labels, right-aligned beside the bar origin
- 4× `<text>` percentage labels centered inside the circular tips
- 3× dashed `<line>` vertical reference guides for 50%, 75%, and 100%
- 3× small `<text>` tick labels under the chart
- 1× `<text>` title with nested `<tspan>` for inline color emphasis
- 2× `<linearGradient>` fills for accent and muted bar styling
- 1× `<radialGradient>` for the background accent blob
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to bar shadow paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentBar" x1="390" y1="0" x2="1090" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1AA9C8"/>
      <stop offset="70%" stop-color="#26ACC6"/>
      <stop offset="100%" stop-color="#5ED2E4"/>
    </linearGradient>
    <linearGradient id="mutedBar" x1="390" y1="0" x2="1050" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#8E95A0"/>
      <stop offset="100%" stop-color="#B0B6BF"/>
    </linearGradient>
    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#D8F6FA" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#D8F6FA" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-40%" width="150%" height="190%">
      <feOffset dx="0" dy="7" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <path d="M930,20 C1070,-25 1210,55 1255,175 C1305,310 1195,390 1055,365 C925,342 840,245 858,145 C868,88 890,45 930,20 Z"
        fill="url(#cyanGlow)"/>

  <text x="70" y="76" width="880" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#777C83">
    <tspan x="70" dy="0">Visitors rate their experience most</tspan>
    <tspan x="70" dy="48" fill="#26ACC6" font-size="44">welcoming and fun!</tspan>
  </text>

  <text x="70" y="178" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#8B929A">
    Top-two attributes are highlighted; remaining scores stay muted for quick comparison.
  </text>

  <line x1="770" y1="245" x2="770" y2="620" stroke="#DDE4EA" stroke-width="1.5" stroke-dasharray="5 7"/>
  <line x1="960" y1="245" x2="960" y2="620" stroke="#DDE4EA" stroke-width="1.5" stroke-dasharray="5 7"/>
  <line x1="1150" y1="245" x2="1150" y2="620" stroke="#DDE4EA" stroke-width="1.5" stroke-dasharray="5 7"/>

  <text x="770" y="648" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A3ABB4">50%</text>
  <text x="960" y="648" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A3ABB4">75%</text>
  <text x="1150" y="648" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A3ABB4">100%</text>

  <path d="M390,270 H1122 A28,28 0 0 1 1122,326 H390 Z" fill="#F1F5F8"/>
  <path d="M390,361 H1122 A28,28 0 0 1 1122,417 H390 Z" fill="#F1F5F8"/>
  <path d="M390,452 H1122 A28,28 0 0 1 1122,508 H390 Z" fill="#F1F5F8"/>
  <path d="M390,543 H1122 A28,28 0 0 1 1122,599 H390 Z" fill="#F1F5F8"/>

  <text x="345" y="304" width="275" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#5F656D">
    Welcoming Atmosphere
  </text>
  <text x="345" y="395" width="275" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#5F656D">
    Fun Place to Be
  </text>
  <text x="345" y="486" width="275" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#5F656D">
    Quality Time with Friends &amp; Family
  </text>
  <text x="345" y="577" width="275" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#5F656D">
    Educational Experience
  </text>

  <path d="M390,270 H1046 A28,28 0 0 1 1046,326 H390 Z" fill="#1B90A8" opacity="0.22" filter="url(#softShadow)"/>
  <rect x="390" y="270" width="656" height="56" fill="url(#accentBar)"/>
  <circle cx="1046" cy="298" r="28" fill="url(#accentBar)"/>
  <text x="1046" y="305" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">90%</text>

  <path d="M390,361 H1016 A28,28 0 0 1 1016,417 H390 Z" fill="#1B90A8" opacity="0.18" filter="url(#softShadow)"/>
  <rect x="390" y="361" width="626" height="56" fill="url(#accentBar)"/>
  <circle cx="1016" cy="389" r="28" fill="url(#accentBar)"/>
  <text x="1016" y="396" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">86%</text>

  <path d="M390,452 H985 A28,28 0 0 1 985,508 H390 Z" fill="#6E7781" opacity="0.16" filter="url(#softShadow)"/>
  <rect x="390" y="452" width="595" height="56" fill="url(#mutedBar)"/>
  <circle cx="985" cy="480" r="28" fill="url(#mutedBar)"/>
  <text x="985" y="487" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">82%</text>

  <path d="M390,543 H970 A28,28 0 0 1 970,599 H390 Z" fill="#6E7781" opacity="0.16" filter="url(#softShadow)"/>
  <rect x="390" y="543" width="580" height="56" fill="url(#mutedBar)"/>
  <circle cx="970" cy="571" r="28" fill="url(#mutedBar)"/>
  <text x="970" y="578" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">80%</text>
</svg>
```

## Avoid in this skill
- ❌ Using a single rounded `<rect rx="...">` for the active bar if you need a mathematically flat left origin; it rounds both ends and weakens the chart-axis alignment.
- ❌ Applying `filter` to `<line>` reference guides; line filters are dropped, so keep shadows on paths, circles, rects, or text only.
- ❌ Placing percentage labels outside the bars; the key visual signature is the white value centered inside the circular cap.
- ❌ Over-highlighting every row; reserve the accent color for the one or two bars that carry the insight.
- ❌ Using `marker-end` arrows or chart-axis arrowheads; this composition does not need them and marker behavior is unreliable.

## Composition notes
- Keep category labels in a right-aligned column ending 35–50 px before the bar origin; this creates a crisp implied y-axis without drawing a heavy axis line.
- Use thick bars, roughly 52–64 px high on a 1280×720 canvas, so the circular cap can comfortably hold a bold percentage label.
- Reserve the top 25–30% of the slide for the headline and takeaway; the chart should occupy the lower two-thirds with generous row spacing.
- Use accent color rhythm sparingly: title emphasis and top bars should share the same hue, while gridlines, rails, and lower bars remain quiet cool greys.