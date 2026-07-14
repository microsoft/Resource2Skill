# SVG Recipe — Diagonal Business Spotlight

## Visual mechanism
A full-bleed business/city photograph is dimmed, then divided by a dominant magenta diagonal parallelogram that becomes the spotlight canvas for key messages. Smaller translucent angled panels create title and metric zones, giving the slide a layered executive-keynote feel with strong forward motion.

## SVG primitives needed
- 1× `<image>` for the full-slide photographic background.
- 1× `<rect>` for the dark gradient dimming overlay across the photo.
- 5× `<path>` for the large diagonal spotlight panel, title glass panel, footer metrics panel, and thin decorative diagonal strips.
- 3× `<circle>` for icon backplates inside the magenta content panel.
- 3× `<path>` for simple editable white business icons.
- 6× `<line>` for diagonal separators, accent rules, and metric dividers.
- 14× `<text>` for title, subtitle/body copy, three content blocks, and footer KPIs.
- 4× `<linearGradient>` for photo dimming, magenta spotlight, dark glass, and pale metric glass effects.
- 1× `<filter id="panelShadow">` applied to angled panels for soft depth.
- 1× `<filter id="softGlow">` applied to the main title accent word for premium emphasis.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoDim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#180A12" stop-opacity="0.82"/>
      <stop offset="55%" stop-color="#071015" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="#03070A" stop-opacity="0.88"/>
    </linearGradient>

    <linearGradient id="magentaSpotlight" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF168F" stop-opacity="0.95"/>
      <stop offset="52%" stop-color="#E2007A" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#7E1647" stop-opacity="0.96"/>
    </linearGradient>

    <linearGradient id="titleGlass" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#070A10" stop-opacity="0.84"/>
      <stop offset="100%" stop-color="#1E1020" stop-opacity="0.44"/>
    </linearGradient>

    <linearGradient id="metricGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .34 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.pexels.com/photos/313782/pexels-photo-313782.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=1600" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#photoDim)"/>

  <path d="M665 -60 L1232 -60 L982 780 L415 780 Z" fill="url(#magentaSpotlight)" filter="url(#panelShadow)"/>
  <path d="M610 -42 L668 -42 L421 780 L363 780 Z" fill="#FFFFFF" opacity="0.16"/>
  <path d="M1128 -30 L1176 -30 L930 764 L882 764 Z" fill="#FFFFFF" opacity="0.11"/>

  <path d="M0 116 L552 42 L455 268 L0 342 Z" fill="url(#titleGlass)" filter="url(#panelShadow)"/>
  <path d="M744 555 L1242 512 L1280 720 L690 720 Z" fill="url(#metricGlass)" filter="url(#panelShadow)"/>

  <line x1="86" y1="305" x2="443" y2="257" stroke="#FFFFFF" stroke-width="2" opacity="0.45"/>
  <line x1="705" y1="114" x2="1098" y2="62" stroke="#FFFFFF" stroke-width="2" opacity="0.36"/>
  <line x1="735" y1="139" x2="1128" y2="87" stroke="#FFFFFF" stroke-width="1" opacity="0.18"/>

  <text x="82" y="164" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="66" font-weight="800" fill="#E2007A" letter-spacing="2" filter="url(#softGlow)">BUSINESS</text>
  <text x="86" y="207" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="600" fill="#FFFFFF" letter-spacing="4">PRESENTATIONS</text>
  <text x="88" y="244" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#DDE3EA" opacity="0.92">Modern market briefing template for growth stories, investor updates, and strategic operating reviews.</text>

  <circle cx="704" cy="183" r="27" fill="#FFFFFF" opacity="0.18"/>
  <path d="M692 188 L700 173 L709 183 L719 164 L723 167 L710 193 L701 183 L695 194 Z" fill="#FFFFFF"/>
  <text x="748" y="169" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#FFFFFF">Market Momentum</text>
  <text x="748" y="197" width="355" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#FFEAF5" opacity="0.90">Highlight a single business force: adoption, demand, category growth, or acceleration in the funnel.</text>

  <line x1="694" y1="246" x2="1110" y2="192" stroke="#FFFFFF" stroke-width="1.5" opacity="0.28" stroke-dasharray="8 9"/>

  <circle cx="760" cy="315" r="27" fill="#FFFFFF" opacity="0.18"/>
  <path d="M746 326 L746 306 L754 306 L754 326 Z M759 326 L759 296 L767 296 L767 326 Z M772 326 L772 312 L780 312 L780 326 Z" fill="#FFFFFF"/>
  <text x="804" y="301" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#FFFFFF">Performance Signal</text>
  <text x="804" y="329" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#FFEAF5" opacity="0.90">Use the diagonal zone for one concise insight supported by metric language and executive framing.</text>

  <line x1="748" y1="379" x2="1160" y2="325" stroke="#FFFFFF" stroke-width="1.5" opacity="0.26" stroke-dasharray="8 9"/>

  <circle cx="816" cy="447" r="27" fill="#FFFFFF" opacity="0.18"/>
  <path d="M802 448 C807 438 825 438 830 448 L830 456 C830 461 802 461 802 456 Z M810 430 C810 423 822 423 822 430 C822 437 810 437 810 430 Z" fill="#FFFFFF"/>
  <text x="860" y="433" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#FFFFFF">Client Impact</text>
  <text x="860" y="461" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#FFEAF5" opacity="0.90">Translate activity into outcomes: retention, expansion, satisfaction, or operating efficiency gains.</text>

  <text x="780" y="632" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="52" font-weight="800" fill="#FFFFFF">500+</text>
  <text x="784" y="662" width="135" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#FFFFFF" opacity="0.84" letter-spacing="1.5">CLIENTS</text>
  <line x1="946" y1="585" x2="946" y2="680" stroke="#FFFFFF" stroke-width="1.5" opacity="0.32"/>
  <text x="984" y="632" width="165" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="52" font-weight="800" fill="#FFFFFF">2K+</text>
  <text x="988" y="662" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#FFFFFF" opacity="0.84" letter-spacing="1.5">PROJECTS</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the diagonal panels with rotated rectangles using `skewX`, `skewY`, or `matrix(...)`; use editable `<path>` parallelograms instead.
- ❌ Do not apply `clip-path` or `mask` to the diagonal color panels; clipping is only reliable on `<image>` elements.
- ❌ Do not rely on `marker-end` for diagonal arrows; if directional cues are needed, draw arrowheads manually with small `<path>` triangles.
- ❌ Do not use low-contrast text directly over the photo; always place text on the dark glass panel or the saturated spotlight panel.
- ❌ Do not use `<pattern>` fills for the glass texture; use gradients, opacity, and thin editable lines.

## Composition notes
- Keep the photographic background full-bleed, but heavily dimmed so the magenta diagonal reads as the primary visual object.
- Reserve the upper-left angled glass panel for the title; keep it compact and let the diagonal edge create motion.
- Place the main explanatory content inside the magenta panel, staggered downward to follow the slide’s diagonal flow.
- Use the bottom-right translucent panel for KPI numbers; it should feel attached to the spotlight panel, not like a separate table.