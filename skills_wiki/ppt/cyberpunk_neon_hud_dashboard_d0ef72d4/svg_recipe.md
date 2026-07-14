# SVG Recipe — Cyberpunk Neon HUD Dashboard

## Visual mechanism
A deep void background is overlaid with a faint technical grid, then framed by glowing cyan/magenta HUD panels with chamfered corners, corner brackets, scan lines, and compact data widgets. The effect depends on layered duplicate shapes: a blurred neon stroke underneath, a sharp bright stroke above, and semi-transparent dark glass fills for readable chart content.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 12–20× `<line>` for the faint cyber grid and chart axes
- 8–12× `<path>` for chamfered HUD panel frames, neon dividers, waveform traces, radar ticks, and decorative angular accents
- 8–14× `<rect>` for glass panel fills, KPI chips, chart bars, and small status modules
- 4–8× `<circle>` / `<ellipse>` for radar rings, data nodes, and glowing status dots
- 10–18× `<text>` with explicit `width` attributes for the title, system labels, KPIs, and dashboard readouts
- 2× `<linearGradient>` for the void background and panel glass
- 1× `<radialGradient>` for the center glow/vignette
- 2× `<filter>` using `feGaussianBlur` for neon glows applied to paths, circles, rects, and text
- 1× `<filter>` using `feOffset + feGaussianBlur + feMerge` for floating panel shadows

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgVoid" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070315"/>
      <stop offset="45%" stop-color="#0E0A24"/>
      <stop offset="100%" stop-color="#12051C"/>
    </linearGradient>
    <radialGradient id="centerPulse" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#132B55" stop-opacity="0.55"/>
      <stop offset="48%" stop-color="#120A2D" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.88"/>
    </radialGradient>
    <linearGradient id="glassFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0DF7FF" stop-opacity="0.16"/>
      <stop offset="55%" stop-color="#101733" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#FF0080" stop-opacity="0.12"/>
    </linearGradient>
    <filter id="cyanGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="magentaGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="panelShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgVoid)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerPulse)"/>

  <line x1="0" y1="80" x2="1280" y2="80" stroke="#00F6FF" stroke-opacity="0.10"/>
  <line x1="0" y1="160" x2="1280" y2="160" stroke="#00F6FF" stroke-opacity="0.10"/>
  <line x1="0" y1="240" x2="1280" y2="240" stroke="#00F6FF" stroke-opacity="0.10"/>
  <line x1="0" y1="320" x2="1280" y2="320" stroke="#00F6FF" stroke-opacity="0.10"/>
  <line x1="0" y1="400" x2="1280" y2="400" stroke="#00F6FF" stroke-opacity="0.10"/>
  <line x1="0" y1="480" x2="1280" y2="480" stroke="#00F6FF" stroke-opacity="0.10"/>
  <line x1="0" y1="560" x2="1280" y2="560" stroke="#00F6FF" stroke-opacity="0.10"/>
  <line x1="0" y1="640" x2="1280" y2="640" stroke="#00F6FF" stroke-opacity="0.10"/>
  <line x1="80" y1="0" x2="80" y2="720" stroke="#00F6FF" stroke-opacity="0.08"/>
  <line x1="240" y1="0" x2="240" y2="720" stroke="#00F6FF" stroke-opacity="0.08"/>
  <line x1="400" y1="0" x2="400" y2="720" stroke="#00F6FF" stroke-opacity="0.08"/>
  <line x1="560" y1="0" x2="560" y2="720" stroke="#00F6FF" stroke-opacity="0.08"/>
  <line x1="720" y1="0" x2="720" y2="720" stroke="#00F6FF" stroke-opacity="0.08"/>
  <line x1="880" y1="0" x2="880" y2="720" stroke="#00F6FF" stroke-opacity="0.08"/>
  <line x1="1040" y1="0" x2="1040" y2="720" stroke="#00F6FF" stroke-opacity="0.08"/>
  <line x1="1200" y1="0" x2="1200" y2="720" stroke="#00F6FF" stroke-opacity="0.08"/>

  <text x="64" y="62" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" letter-spacing="3" fill="#E9FFFF" filter="url(#cyanGlow)">CYBER DEFENSE OPERATIONS</text>
  <text x="68" y="96" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#00F6FF">SYSTEM INITIALIZATION COMPLETE  //  LIVE THREAT GRID</text>
  <text x="1010" y="62" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" letter-spacing="2" fill="#FF4DB8">ALERT LEVEL: MAGENTA</text>

  <path d="M54 130 L410 130 L436 156 L436 328 L410 354 L54 354 L30 330 L30 154 Z" fill="url(#glassFill)" stroke="#00F6FF" stroke-width="3" filter="url(#panelShadow)"/>
  <path d="M54 130 L410 130 L436 156 L436 328 L410 354 L54 354 L30 330 L30 154 Z" fill="none" stroke="#00F6FF" stroke-width="2" filter="url(#cyanGlow)"/>
  <path d="M844 130 L1200 130 L1226 156 L1226 328 L1200 354 L844 354 L818 328 L818 156 Z" fill="url(#glassFill)" stroke="#FF0080" stroke-width="3" filter="url(#panelShadow)"/>
  <path d="M844 130 L1200 130 L1226 156 L1226 328 L1200 354 L844 354 L818 328 L818 156 Z" fill="none" stroke="#FF0080" stroke-width="2" filter="url(#magentaGlow)"/>
  <path d="M500 176 L780 176 L804 200 L804 610 L780 634 L500 634 L476 610 L476 200 Z" fill="url(#glassFill)" stroke="#8A5CFF" stroke-width="3" filter="url(#panelShadow)"/>
  <path d="M500 176 L780 176 L804 200 L804 610 L780 634 L500 634 L476 610 L476 200 Z" fill="none" stroke="#00F6FF" stroke-opacity="0.65" stroke-width="2" filter="url(#cyanGlow)"/>

  <text x="58" y="166" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" letter-spacing="2" fill="#E9FFFF">NETWORK INTRUSION RATE</text>
  <text x="58" y="206" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#00F6FF" filter="url(#cyanGlow)">12.8%</text>
  <text x="220" y="206" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9BDFFF">DOWN 4.2 PTS FROM LAST SCAN</text>
  <line x1="70" y1="295" x2="380" y2="295" stroke="#8BEFFF" stroke-opacity="0.22"/>
  <line x1="70" y1="245" x2="70" y2="306" stroke="#8BEFFF" stroke-opacity="0.22"/>
  <path d="M70 286 C105 268, 126 272, 160 250 S225 230, 258 258 S324 300, 386 236" fill="none" stroke="#00F6FF" stroke-width="4" filter="url(#cyanGlow)"/>
  <circle cx="386" cy="236" r="5" fill="#FFFFFF" filter="url(#cyanGlow)"/>

  <text x="850" y="166" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" letter-spacing="2" fill="#E9FFFF">THREAT VECTOR MIX</text>
  <rect x="860" y="205" width="270" height="14" rx="7" fill="#13213F" stroke="#00F6FF" stroke-opacity="0.25"/>
  <rect x="860" y="205" width="198" height="14" rx="7" fill="#FF0080" filter="url(#magentaGlow)"/>
  <rect x="860" y="245" width="270" height="14" rx="7" fill="#13213F" stroke="#00F6FF" stroke-opacity="0.25"/>
  <rect x="860" y="245" width="145" height="14" rx="7" fill="#00F6FF" filter="url(#cyanGlow)"/>
  <rect x="860" y="285" width="270" height="14" rx="7" fill="#13213F" stroke="#00F6FF" stroke-opacity="0.25"/>
  <rect x="860" y="285" width="88" height="14" rx="7" fill="#8A5CFF" filter="url(#cyanGlow)"/>
  <text x="1148" y="218" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFB7E0">73%</text>
  <text x="1148" y="258" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#BFFBFF">54%</text>
  <text x="1148" y="298" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#CFC2FF">33%</text>

  <text x="522" y="218" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2" fill="#E9FFFF">GLOBAL SENSOR RADAR</text>
  <circle cx="640" cy="390" r="132" fill="none" stroke="#00F6FF" stroke-opacity="0.24" stroke-width="2"/>
  <circle cx="640" cy="390" r="88" fill="none" stroke="#00F6FF" stroke-opacity="0.28" stroke-width="2"/>
  <circle cx="640" cy="390" r="44" fill="none" stroke="#00F6FF" stroke-opacity="0.32" stroke-width="2"/>
  <line x1="508" y1="390" x2="772" y2="390" stroke="#00F6FF" stroke-opacity="0.20"/>
  <line x1="640" y1="258" x2="640" y2="522" stroke="#00F6FF" stroke-opacity="0.20"/>
  <path d="M640 390 L716 286 A132 132 0 0 1 766 420 Z" fill="#00F6FF" fill-opacity="0.12" stroke="#00F6FF" stroke-width="2" filter="url(#cyanGlow)"/>
  <circle cx="702" cy="318" r="6" fill="#FF0080" filter="url(#magentaGlow)"/>
  <circle cx="566" cy="426" r="5" fill="#00F6FF" filter="url(#cyanGlow)"/>
  <circle cx="725" cy="454" r="4" fill="#FFFFFF" filter="url(#cyanGlow)"/>
  <text x="548" y="584" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#E9FFFF">847,291</text>
  <text x="548" y="610" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="2" fill="#00F6FF">PACKETS ANALYZED / MIN</text>

  <path d="M54 420 L410 420 L436 446 L436 614 L410 640 L54 640 L30 616 L30 446 Z" fill="url(#glassFill)" stroke="#00F6FF" stroke-width="2" filter="url(#panelShadow)"/>
  <text x="58" y="458" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2" fill="#E9FFFF">NODE HEALTH</text>
  <rect x="68" y="504" width="42" height="82" rx="4" fill="#00F6FF" fill-opacity="0.78" filter="url(#cyanGlow)"/>
  <rect x="132" y="476" width="42" height="110" rx="4" fill="#00F6FF" fill-opacity="0.55"/>
  <rect x="196" y="532" width="42" height="54" rx="4" fill="#FF0080" fill-opacity="0.86" filter="url(#magentaGlow)"/>
  <rect x="260" y="492" width="42" height="94" rx="4" fill="#8A5CFF" fill-opacity="0.72"/>
  <rect x="324" y="454" width="42" height="132" rx="4" fill="#00F6FF" fill-opacity="0.88" filter="url(#cyanGlow)"/>

  <path d="M844 420 L1200 420 L1226 446 L1226 614 L1200 640 L844 640 L818 614 L818 446 Z" fill="url(#glassFill)" stroke="#FF0080" stroke-width="2" filter="url(#panelShadow)"/>
  <text x="850" y="458" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2" fill="#E9FFFF">ACTIVE COUNTERMEASURES</text>
  <circle cx="870" cy="510" r="7" fill="#00F6FF" filter="url(#cyanGlow)"/>
  <circle cx="870" cy="552" r="7" fill="#00F6FF" filter="url(#cyanGlow)"/>
  <circle cx="870" cy="594" r="7" fill="#FF0080" filter="url(#magentaGlow)"/>
  <text x="895" y="516" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#CFFBFF">QUARANTINE BOTNET CLUSTER</text>
  <text x="895" y="558" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#CFFBFF">ROTATE ZERO-TRUST KEYS</text>
  <text x="895" y="600" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#FFC4E6">ESCALATE PRIVILEGE ANOMALY</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<pattern>` for the grid; draw explicit low-opacity `<line>` elements so the grid remains editable.
- ❌ Applying `filter` to `<line>` elements; use duplicate glowing `<path>`, `<rect>`, or `<circle>` elements for neon effects instead.
- ❌ Relying on masks or clipping non-image shapes for glass panels; use direct chamfered `<path>` frames with translucent fills.
- ❌ Using `marker-end` for arrowheads in HUD callouts; build arrowheads manually with small `<path>` triangles or use plain lines.
- ❌ Overloading the slide with full-opacity neon strokes; too much glow destroys hierarchy and makes text unreadable.

## Composition notes
- Keep the center as the main “radar/core system” module, with secondary charts in left and right side panels.
- Use a dark slide background with generous negative space between panels; the glow needs breathing room.
- Alternate cyan for stable/active data and magenta for alerts, risk, or exception states.
- Put all text inside framed regions, using small all-caps labels and a few oversized KPI numbers for executive readability.