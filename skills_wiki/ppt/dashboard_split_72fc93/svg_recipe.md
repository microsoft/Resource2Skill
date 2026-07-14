# SVG Recipe — Dashboard Split

## Visual mechanism
A dense executive dashboard split into two zones: a wide cinematic operational visual on top and a structured data table below. The hero area creates technical atmosphere with clipped imagery, translucent HUD overlays, and KPI cards, while the lower band converts the story into sortable-looking metrics.

## SVG primitives needed
- 7× `<rect>` for background, slide frame, hero image plate, table container, table header, KPI cards, and progress tracks
- 1× `<image>` clipped into a rounded 16:5 hero viewport
- 1× `<clipPath>` with rounded `<rect>` for the hero image crop
- 2× `<linearGradient>` for dark technical background and table/header accents
- 1× `<filter id="softShadow">` for elevated cards and containers
- 1× `<filter id="glow">` for subtle cyan signal glows on KPI indicators
- 12× `<line>` for dashboard grid rules, table column separators, and scanline accents
- 6× `<path>` for circuit-like overlays and subtle decorative telemetry traces
- 10× `<circle>` for status dots, node indicators, and live-system beacons
- Multiple `<text>` elements with explicit `width` attributes for title, labels, KPI values, and table cells

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="48%" stop-color="#0B1F33"/>
      <stop offset="100%" stop-color="#061018"/>
    </linearGradient>
    <linearGradient id="heroWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0DE0FF" stop-opacity="0.18"/>
      <stop offset="45%" stop-color="#07111F" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#002B3D" stop-opacity="0.72"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0E7AC7"/>
      <stop offset="100%" stop-color="#11D6B5"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0.03  0 0 0 0 0.08  0 0 0 .42 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="heroClip">
      <rect x="56" y="92" width="1168" height="356" rx="24"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M0,78 C210,42 374,52 520,96 C720,156 866,120 1048,72 C1148,46 1222,42 1280,54 L1280,0 L0,0 Z" fill="#123A5A" opacity="0.34"/>
  <path d="M950,0 C1018,74 1086,114 1280,126 L1280,0 Z" fill="#0ED6C8" opacity="0.08"/>

  <text x="56" y="48" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#F4FAFF">Plant Operations Dashboard</text>
  <text x="56" y="72" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA9BD">Real-time equipment health, throughput, and exception queue</text>
  <rect x="1016" y="30" width="208" height="34" rx="17" fill="#0C2B3F" stroke="#1F5E76"/>
  <circle cx="1038" cy="47" r="5" fill="#25F2C2" filter="url(#glow)"/>
  <text x="1052" y="52" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#BDFCF0">LIVE · 14:32 UTC</text>

  <rect x="56" y="92" width="1168" height="356" rx="24" fill="#0A1724" filter="url(#softShadow)"/>
  <image href="https://images.example.com/industrial-control-room-scada-dashboard-hero.jpg" x="56" y="92" width="1168" height="356" preserveAspectRatio="xMidYMid slice" clip-path="url(#heroClip)"/>
  <rect x="56" y="92" width="1168" height="356" rx="24" fill="url(#heroWash)"/>
  <rect x="56" y="92" width="1168" height="356" rx="24" fill="none" stroke="#1D6F8C" stroke-width="1.4"/>

  <line x1="88" y1="166" x2="1192" y2="166" stroke="#9CEBFF" stroke-width="1" opacity="0.16"/>
  <line x1="88" y1="240" x2="1192" y2="240" stroke="#9CEBFF" stroke-width="1" opacity="0.11"/>
  <line x1="88" y1="314" x2="1192" y2="314" stroke="#9CEBFF" stroke-width="1" opacity="0.11"/>
  <line x1="88" y1="388" x2="1192" y2="388" stroke="#9CEBFF" stroke-width="1" opacity="0.16"/>
  <line x1="260" y1="118" x2="260" y2="424" stroke="#9CEBFF" stroke-width="1" opacity="0.10"/>
  <line x1="520" y1="118" x2="520" y2="424" stroke="#9CEBFF" stroke-width="1" opacity="0.10"/>
  <line x1="780" y1="118" x2="780" y2="424" stroke="#9CEBFF" stroke-width="1" opacity="0.10"/>
  <line x1="1040" y1="118" x2="1040" y2="424" stroke="#9CEBFF" stroke-width="1" opacity="0.10"/>

  <path d="M105,365 C178,318 235,340 294,286 C349,237 414,250 472,206" fill="none" stroke="#1CE7FF" stroke-width="3" opacity="0.72"/>
  <path d="M724,375 C782,326 846,335 910,292 C982,244 1040,250 1156,184" fill="none" stroke="#25F2C2" stroke-width="3" opacity="0.62"/>
  <path d="M720,156 L790,156 L812,180 L900,180 L925,204 L1004,204" fill="none" stroke="#B8F7FF" stroke-width="1.4" stroke-dasharray="5 7" opacity="0.58"/>
  <path d="M143,158 L204,158 L224,181 L312,181 L338,205 L425,205" fill="none" stroke="#B8F7FF" stroke-width="1.4" stroke-dasharray="5 7" opacity="0.50"/>

  <circle cx="294" cy="286" r="7" fill="#1CE7FF" filter="url(#glow)"/>
  <circle cx="472" cy="206" r="6" fill="#1CE7FF" filter="url(#glow)"/>
  <circle cx="910" cy="292" r="7" fill="#25F2C2" filter="url(#glow)"/>
  <circle cx="1156" cy="184" r="6" fill="#25F2C2" filter="url(#glow)"/>

  <rect x="86" y="118" width="214" height="92" rx="18" fill="#06131F" opacity="0.82" stroke="#2B7892"/>
  <text x="106" y="146" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8AEFFF">THROUGHPUT</text>
  <text x="106" y="183" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">94.8%</text>
  <text x="216" y="183" width="66" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#25F2C2">+3.2%</text>

  <rect x="930" y="326" width="254" height="90" rx="18" fill="#06131F" opacity="0.84" stroke="#2B7892"/>
  <text x="954" y="354" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8AEFFF">ACTIVE EXCEPTIONS</text>
  <text x="954" y="391" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">12</text>
  <text x="1038" y="389" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFD166">4 require review</text>

  <rect x="56" y="472" width="1168" height="194" rx="22" fill="#081723" stroke="#1E4B61" filter="url(#softShadow)"/>
  <rect x="56" y="472" width="1168" height="42" rx="22" fill="url(#headerGrad)" opacity="0.92"/>
  <rect x="56" y="500" width="1168" height="14" fill="url(#headerGrad)" opacity="0.92"/>

  <text x="82" y="500" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">ASSET</text>
  <text x="284" y="500" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">STATUS</text>
  <text x="476" y="500" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">LOAD</text>
  <text x="720" y="500" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">OUTPUT</text>
  <text x="934" y="500" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">NEXT ACTION</text>

  <line x1="260" y1="514" x2="260" y2="646" stroke="#1E4B61" stroke-width="1"/>
  <line x1="452" y1="514" x2="452" y2="646" stroke="#1E4B61" stroke-width="1"/>
  <line x1="696" y1="514" x2="696" y2="646" stroke="#1E4B61" stroke-width="1"/>
  <line x1="908" y1="514" x2="908" y2="646" stroke="#1E4B61" stroke-width="1"/>
  <line x1="76" y1="558" x2="1204" y2="558" stroke="#1E4B61" stroke-width="1"/>
  <line x1="76" y1="602" x2="1204" y2="602" stroke="#1E4B61" stroke-width="1"/>

  <text x="82" y="544" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#E9F7FF">Mixer A-17</text>
  <circle cx="292" cy="539" r="6" fill="#25F2C2"/>
  <text x="308" y="544" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#BDFCF0">Nominal</text>
  <rect x="476" y="530" width="150" height="12" rx="6" fill="#102B3B"/>
  <rect x="476" y="530" width="124" height="12" rx="6" fill="#25F2C2"/>
  <text x="720" y="544" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E9F7FF">18.4k / hr</text>
  <text x="934" y="544" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9DB4C5">Continue automated run</text>

  <text x="82" y="588" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#E9F7FF">Conveyor C-03</text>
  <circle cx="292" cy="583" r="6" fill="#FFD166"/>
  <text x="308" y="588" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFE4A3">Watch</text>
  <rect x="476" y="574" width="150" height="12" rx="6" fill="#102B3B"/>
  <rect x="476" y="574" width="94" height="12" rx="6" fill="#FFD166"/>
  <text x="720" y="588" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E9F7FF">12.1k / hr</text>
  <text x="934" y="588" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9DB4C5">Inspect vibration trend</text>

  <text x="82" y="632" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#E9F7FF">Packaging P-09</text>
  <circle cx="292" cy="627" r="6" fill="#FF5E7A"/>
  <text x="308" y="632" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFC0CB">Alert</text>
  <rect x="476" y="618" width="150" height="12" rx="6" fill="#102B3B"/>
  <rect x="476" y="618" width="62" height="12" rx="6" fill="#FF5E7A"/>
  <text x="720" y="632" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E9F7FF">7.6k / hr</text>
  <text x="934" y="632" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9DB4C5">Assign maintenance ticket</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to the entire hero overlay group; only clip the `<image>` and recreate rounded overlays with matching `<rect rx>`.
- ❌ Using `<foreignObject>` for the table; build editable rows, dividers, progress bars, and labels from native SVG shapes.
- ❌ Putting shadows on `<line>` grid rules; filters on lines are dropped, so keep lines crisp and use opacity instead.
- ❌ Using `marker-end` on dashboard traces; if arrows are required, draw arrowheads manually with small `<path>` triangles or use direct `<line>` arrows.

## Composition notes
- Reserve the top 50–55% of the slide for the wide clipped visual; it should feel like an operational command center, not a decorative banner.
- Keep the bottom table compact but readable: three rows work well, with column dividers and progress bars providing density without clutter.
- Use cyan/teal as the main signal color, amber for watch states, and red only for true exceptions.
- Place KPI cards inside the hero image at opposite corners to create depth while preserving the central image as the visual focus.