# SVG Recipe — Muted & Accent Color Palette for Scientific Figures

## Visual mechanism
Build the slide around calm, desaturated scientific colors, then reserve one saturated accent for the key result, annotation, or data series. The viewer should immediately see the difference between “default software color” and “publication-ready palette” through paired swatches, miniature chart panels, and a single high-contrast highlight.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 2× `<linearGradient>` for header accent pills and scientific performance/stability ramps
- 2× `<filter>` for soft card shadows and accent glow
- 6× `<rect>` for executive-style figure cards and muted chart panels
- 15× `<rect>` for default-vs-muted palette swatches, stacked scientific layers, bars, and gradient bands
- 8× `<line>` for chart axes, comparison arrows, and callout connectors
- 8× `<path>` for smooth scientific curves, arrowheads, organic annotation ribbons, and highlight brackets
- 12× `<circle>` / `<ellipse>` for scatter points, molecule-like dots, and highlighted data markers
- Multiple `<text>` elements with explicit `width` for section titles, swatch labels, axis labels, annotations, and figure captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbfaf7"/>
      <stop offset="100%" stop-color="#eef3f1"/>
    </linearGradient>
    <linearGradient id="pillGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ef4aa0"/>
      <stop offset="100%" stop-color="#ffb06b"/>
    </linearGradient>
    <linearGradient id="stabilityRamp" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f7c3c7"/>
      <stop offset="42%" stop-color="#f8f3e8"/>
      <stop offset="100%" stop-color="#47d3ba"/>
    </linearGradient>
    <linearGradient id="softBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#eaf1f5"/>
      <stop offset="100%" stop-color="#cfdbe2"/>
    </linearGradient>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="accentGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paperBg)"/>

  <rect x="44" y="28" width="355" height="66" rx="32" fill="url(#pillGrad)" filter="url(#cardShadow)"/>
  <text x="68" y="73" width="300" font-family="Microsoft YaHei, Segoe UI" font-size="34" font-weight="700" fill="#ffffff">2. 颜色间的搭配</text>
  <line x1="430" y1="62" x2="505" y2="62" stroke="#ef4aa0" stroke-width="5"/>
  <text x="525" y="74" width="360" font-family="Microsoft YaHei, Segoe UI" font-size="34" font-weight="700" fill="#238aa0">同色系深浅色 + 单一强调色</text>

  <rect x="60" y="125" width="354" height="250" rx="22" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="84" y="164" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#263238">Default colors feel noisy</text>
  <text x="84" y="190" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#70757a">Mute saturation and deepen value for academic credibility.</text>

  <text x="98" y="227" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8a8f94">DEFAULT</text>
  <text x="252" y="227" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8a8f94">MUTED</text>
  <rect x="90" y="245" width="86" height="38" rx="6" fill="#ff0000"/>
  <rect x="250" y="245" width="86" height="38" rx="6" fill="#b0382a"/>
  <rect x="90" y="294" width="86" height="38" rx="6" fill="#00ff00"/>
  <rect x="250" y="294" width="86" height="38" rx="6" fill="#4f7d45"/>
  <rect x="90" y="343" width="86" height="38" rx="6" fill="#0000ff"/>
  <rect x="250" y="343" width="86" height="38" rx="6" fill="#465f86"/>
  <line x1="188" y1="264" x2="235" y2="264" stroke="#9aa3aa" stroke-width="2"/>
  <path d="M235 264 L225 258 L225 270 Z" fill="#9aa3aa"/>
  <line x1="188" y1="313" x2="235" y2="313" stroke="#9aa3aa" stroke-width="2"/>
  <path d="M235 313 L225 307 L225 319 Z" fill="#9aa3aa"/>
  <line x1="188" y1="362" x2="235" y2="362" stroke="#9aa3aa" stroke-width="2"/>
  <path d="M235 362 L225 356 L225 368 Z" fill="#9aa3aa"/>

  <rect x="455" y="125" width="365" height="250" rx="22" fill="#17263f" filter="url(#cardShadow)"/>
  <text x="484" y="164" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#eef4f7">Dark base + vibrant accent</text>
  <text x="484" y="190" width="302" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#b9c5cf">Most data stays quiet; one finding receives the bright color.</text>
  <line x1="505" y1="325" x2="780" y2="325" stroke="#6b7d93" stroke-width="2"/>
  <line x1="505" y1="225" x2="505" y2="325" stroke="#6b7d93" stroke-width="2"/>
  <rect x="535" y="285" width="30" height="40" fill="#58728d"/>
  <rect x="585" y="268" width="30" height="57" fill="#58728d"/>
  <rect x="635" y="252" width="30" height="73" fill="#58728d"/>
  <rect x="685" y="238" width="30" height="87" fill="#58728d"/>
  <rect x="735" y="205" width="30" height="120" fill="#00bfa5"/>
  <circle cx="750" cy="205" r="10" fill="#00bfa5" filter="url(#accentGlow)"/>
  <path d="M525 300 C570 285, 604 270, 650 260 S725 230, 760 205" fill="none" stroke="#f2d16b" stroke-width="3"/>
  <text x="610" y="352" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#b9c5cf">muted series</text>
  <text x="692" y="222" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#00e0c0">key result</text>

  <rect x="860" y="125" width="360" height="250" rx="22" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="888" y="164" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#263238">Monochrome scientific layers</text>
  <rect x="915" y="200" width="116" height="24" fill="#e8e2f0"/>
  <rect x="915" y="224" width="116" height="36" fill="#b9a7d1"/>
  <rect x="915" y="260" width="116" height="48" fill="#725391"/>
  <rect x="915" y="308" width="116" height="24" fill="#d3c5e1"/>
  <rect x="1048" y="200" width="116" height="24" fill="#e8e2f0"/>
  <rect x="1048" y="224" width="116" height="36" fill="#a48bbe"/>
  <rect x="1048" y="260" width="116" height="48" fill="#60447e"/>
  <rect x="1048" y="308" width="116" height="24" fill="#d3c5e1"/>
  <text x="936" y="352" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b6f76">Planar</text>
  <text x="1068" y="352" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b6f76">Tandem</text>

  <rect x="60" y="415" width="715" height="230" rx="22" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="92" y="453" width="625" height="95" fill="url(#stabilityRamp)" opacity="0.9"/>
  <line x1="92" y1="548" x2="717" y2="548" stroke="#6d747a" stroke-width="1.5"/>
  <line x1="92" y1="453" x2="92" y2="548" stroke="#6d747a" stroke-width="1.5"/>
  <text x="104" y="475" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6e3840">Better stability</text>
  <text x="567" y="475" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#225e55">Better performance</text>
  <circle cx="165" cy="520" r="6" fill="#8b1e2d"/>
  <circle cx="280" cy="500" r="6" fill="#8b1e2d"/>
  <circle cx="405" cy="487" r="6" fill="#8b1e2d"/>
  <circle cx="535" cy="468" r="6" fill="#8b1e2d"/>
  <circle cx="655" cy="520" r="6" fill="#8b1e2d"/>
  <rect x="158" y="487" width="13" height="13" fill="#111111"/>
  <rect x="273" y="478" width="13" height="13" fill="#111111"/>
  <rect x="398" y="460" width="13" height="13" fill="#111111"/>
  <rect x="528" y="452" width="13" height="13" fill="#111111"/>
  <rect x="648" y="456" width="13" height="13" fill="#111111"/>
  <text x="104" y="590" width="580" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#263238">Gradient bands communicate continuous scientific tradeoffs without adding extra legend clutter.</text>
  <text x="104" y="616" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7a7f84">Use soft red → neutral → teal to suggest weak → balanced → strong, not traffic-light alarm colors.</text>

  <rect x="825" y="415" width="395" height="230" rx="22" fill="url(#softBlue)" filter="url(#cardShadow)"/>
  <path d="M880 585 C935 530, 1000 560, 1048 500 S1140 470, 1180 520" fill="none" stroke="#496aa3" stroke-width="3"/>
  <path d="M880 610 C950 575, 995 590, 1058 545 S1135 520, 1180 575" fill="none" stroke="#b23a48" stroke-width="3"/>
  <circle cx="1048" cy="500" r="8" fill="#ff884d" filter="url(#accentGlow)"/>
  <line x1="1048" y1="500" x2="1105" y2="455" stroke="#248ca2" stroke-width="3"/>
  <path d="M1105 455 L1091 456 L1099 467 Z" fill="#248ca2"/>
  <text x="900" y="452" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#263238">Accent only the conclusion</text>
  <text x="900" y="480" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#5f6870">Muted curves remain readable; the orange point names the paper’s takeaway.</text>
  <text x="1060" y="438" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ff884d">highlight</text>

  <path d="M610 392 L680 392 L704 415 L680 438 L610 438 Z" fill="#238aa0"/>
  <text x="625" y="422" width="85" font-family="Microsoft YaHei, Segoe UI" font-size="22" font-weight="700" fill="#ffffff">配色策略</text>
</svg>
```

## Avoid in this skill
- ❌ Rainbow palettes with five or more saturated hues competing for attention; they destroy the hierarchy this technique depends on.
- ❌ Pure RGB primaries such as `#ff0000`, `#00ff00`, and `#0000ff` in final chart elements; show them only as “before” examples.
- ❌ Using the accent color for every label, marker, and arrow; the accent must remain scarce.
- ❌ Dark text on dark muted bases without enough contrast; use off-white text on navy, charcoal, or deep purple panels.
- ❌ Applying gradients randomly as decoration; gradients should encode a meaningful transition such as stability → performance or low → high intensity.

## Composition notes
- Keep the slide background warm white or very pale gray-green so muted scientific colors feel intentional rather than dull.
- Put comparison swatches on the left, example figure panels in the center/right, and one large applied chart near the bottom to show the rule in context.
- Let 70–85% of the visual mass use muted tones; reserve the saturated accent for one point, bar, arrow, or annotation.
- Use captions in gray and titles in dark charcoal/navy to mimic journal figure aesthetics while preserving presentation readability.