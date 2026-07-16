# SVG Recipe — Vertical Line Divider

## Visual mechanism
A quiet full-slide section break is organized around one precise vertical accent line, with a large headline locked to one side and small contextual labeling on the other. Subtle gradients, oversized ghost typography, and a softened line glow make the divider feel premium without adding content density.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<path>` for soft abstract background washes that keep the minimalist slide from feeling empty
- 1× `<rect>` for a faint vertical line glow behind the divider
- 1× `<rect>` for the crisp central vertical divider
- 4× `<line>` for small horizontal tick marks that visually anchor the divider
- 1× `<rect>` for a translucent text-side backing plate
- 5× `<text>` for section label, large ghost numeral, headline, subtitle, and micro-caption
- 3× `<linearGradient>` for background depth, accent line color, and glassy text plate
- 1× `<radialGradient>` for the ambient corner wash
- 2× `<filter>` with `feGaussianBlur` / `feOffset+feGaussianBlur+feMerge` for line glow and soft card shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F7F8FA"/>
      <stop offset="0.58" stop-color="#EEF1F5"/>
      <stop offset="1" stop-color="#E7EBF1"/>
    </linearGradient>

    <radialGradient id="ambientWash" cx="0.15" cy="0.18" r="0.9">
      <stop offset="0" stop-color="#DCE7F6" stop-opacity="0.9"/>
      <stop offset="0.5" stop-color="#DCE7F6" stop-opacity="0.24"/>
      <stop offset="1" stop-color="#DCE7F6" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="lineGrad" x1="640" y1="150" x2="640" y2="570" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#8EA9D6" stop-opacity="0"/>
      <stop offset="0.18" stop-color="#2F65D5"/>
      <stop offset="0.5" stop-color="#111827"/>
      <stop offset="0.82" stop-color="#2F65D5"/>
      <stop offset="1" stop-color="#8EA9D6" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="plateGrad" x1="706" y1="214" x2="1130" y2="514" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.82"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.34"/>
    </linearGradient>

    <filter id="lineGlow" x="600" y="120" width="80" height="480" filterUnits="userSpaceOnUse">
      <feGaussianBlur stdDeviation="8"/>
    </filter>

    <filter id="softShadow" x="660" y="180" width="520" height="380" filterUnits="userSpaceOnUse">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="26"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-40,88 C120,10 252,38 345,136 C438,234 394,356 248,390 C102,424 -40,340 -92,230 C-118,176 -99,116 -40,88 Z"
        fill="url(#ambientWash)" opacity="0.78"/>
  <path d="M1004,544 C1096,480 1244,498 1328,586 C1412,674 1370,770 1246,790 C1122,810 972,748 936,664 C914,612 942,588 1004,544 Z"
        fill="#D7DEE9" opacity="0.34"/>

  <text x="164" y="172" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        font-weight="700" letter-spacing="3.5" fill="#536071">
    SECTION 03
  </text>

  <text x="135" y="442" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="188"
        font-weight="700" letter-spacing="-8" fill="#1F2937" opacity="0.055">
    03
  </text>

  <line x1="612" y1="180" x2="636" y2="180" stroke="#9AA8BA" stroke-width="1.2" opacity="0.55"/>
  <line x1="644" y1="180" x2="668" y2="180" stroke="#9AA8BA" stroke-width="1.2" opacity="0.55"/>
  <line x1="612" y1="540" x2="636" y2="540" stroke="#9AA8BA" stroke-width="1.2" opacity="0.55"/>
  <line x1="644" y1="540" x2="668" y2="540" stroke="#9AA8BA" stroke-width="1.2" opacity="0.55"/>

  <rect x="632" y="158" width="16" height="404" rx="8"
        fill="#2F65D5" opacity="0.35" filter="url(#lineGlow)"/>
  <rect x="638.5" y="164" width="3" height="392" rx="1.5"
        fill="url(#lineGrad)"/>

  <rect x="704" y="208" width="440" height="304" rx="28"
        fill="url(#plateGrad)" opacity="0.7" filter="url(#softShadow)"/>

  <text x="744" y="286" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        font-weight="700" letter-spacing="2.8" fill="#2F65D5">
    EXECUTIVE FOCUS
  </text>

  <text x="742" y="356" width="398"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="52"
        font-weight="700" letter-spacing="-1.6" fill="#111827">
    <tspan x="742" dy="0">Strategic</tspan>
    <tspan x="742" dy="58">Priorities</tspan>
  </text>

  <text x="746" y="456" width="356"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19"
        font-weight="400" line-height="1.35" fill="#5D6878">
    <tspan x="746" dy="0">A concise transition into the next chapter,</tspan>
    <tspan x="746" dy="27">anchored by a single vertical rule.</tspan>
  </text>

  <text x="164" y="536" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        font-weight="500" fill="#7A8493">
    Minimal divider shell · low-density section break
  </text>
</svg>
```

## Avoid in this skill
- ❌ Putting the divider line in a `<line>` and applying a glow filter to it; filters on lines are dropped, so use a thin rounded `<rect>` for filtered or gradient divider rules.
- ❌ Centering all text directly over the vertical line; the technique depends on asymmetry and negative space around the divider.
- ❌ Using many small icons or bullet lists; this is a section divider, not a content slide.
- ❌ Relying on `<mask>` or `clip-path` for non-image elements to create line reveals; use layered rects and gradients instead.

## Composition notes
- Keep the vertical divider close to the optical center, usually between x=610 and x=670, with text blocks offset left or right.
- Use generous whitespace: the headline block should occupy roughly one-third of the canvas width, not the full slide.
- Let the vertical rule be the highest-contrast object after the headline; background shapes should remain low-opacity.
- Pair one accent color with neutral typography so the slide reads as a clean executive section break.