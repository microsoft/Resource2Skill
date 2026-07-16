# SVG Recipe — Futuristic Cyberpunk HUD Gauge (Segmented Circular Progress)

## Visual mechanism
A dark, cinematic technology background is overlaid with a neon HUD gauge: 32 separated radial arc blocks form the mechanical track, while a glowing cyan sweep arc communicates progress. The large center percentage and micro-labels turn a simple metric into a sci-fi cockpit readout.

## SVG primitives needed
- 1× `<image>` for the full-slide VR / server / cyber technology background
- 3× `<rect>` for dark tint overlays, left text panel, and small HUD label plates
- 32× `<path>` for the segmented circular gauge track
- 1× `<path>` for the glowing foreground progress arc
- 3× `<circle>` for inner HUD rings and dashed calibration rings
- 8× `<line>` for crosshair and bracket ticks around the gauge
- 6× `<text>` with explicit `width` for title, subtitle, metric, and tiny technical labels
- 2× `<linearGradient>` for dark cinematic wash and neon accent fills
- 2× `<filter>` using `feGaussianBlur` / `feOffset` / `feMerge` for neon glow and soft shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050A22" stop-opacity="0.92"/>
      <stop offset="55%" stop-color="#0D143C" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#020615" stop-opacity="0.96"/>
    </linearGradient>
    <linearGradient id="neonStroke" x1="640" y1="120" x2="1050" y2="570" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7FFFFF"/>
      <stop offset="45%" stop-color="#00FFFF"/>
      <stop offset="100%" stop-color="#008CFF"/>
    </linearGradient>
    <filter id="cyanGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="9" result="blur1"/>
      <feGaussianBlur stdDeviation="22" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur2"/>
        <feMergeNode in="blur1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.example.com/cyberpunk-vr-headset-server-room-blue.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#061A3F" opacity="0.38"/>

  <rect x="72" y="118" width="420" height="450" rx="28" fill="#06102D" opacity="0.58" filter="url(#panelShadow)"/>
  <rect x="96" y="150" width="86" height="6" rx="3" fill="#00FFFF"/>
  <text x="96" y="212" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF">
    元宇宙商機市場分析
  </text>
  <text x="96" y="266" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="600" fill="#7FFFFF">
    硬體佔有率 Metaverse
  </text>
  <text x="98" y="336" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#B7D6FF" opacity="0.86">
    2021 X牌VR設備佔有率
  </text>
  <text x="98" y="410" width="320" font-family="Segoe UI" font-size="13" letter-spacing="2" fill="#48BFFF" opacity="0.78">
    MARKET SIGNAL / DEVICE SHARE
  </text>
  <rect x="96" y="438" width="240" height="42" rx="8" fill="#001E42" stroke="#00FFFF" stroke-opacity="0.42"/>
  <text x="116" y="466" width="210" font-family="Segoe UI" font-size="16" font-weight="600" fill="#D8FFFF">
    AI + XR HARDWARE INDEX
  </text>

  <circle cx="850" cy="360" r="274" fill="none" stroke="#0E6DA0" stroke-width="1.5" stroke-dasharray="4 12" opacity="0.65"/>
  <circle cx="850" cy="360" r="238" fill="none" stroke="#00FFFF" stroke-width="1" stroke-dasharray="2 8" opacity="0.42"/>
  <circle cx="850" cy="360" r="138" fill="#06102D" opacity="0.38" stroke="#00FFFF" stroke-width="1.3" stroke-opacity="0.36"/>

  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(0 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.30"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(11.25 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.34"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(22.5 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.38"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(33.75 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.42"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(45 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.46"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(56.25 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.50"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(67.5 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.54"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(78.75 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.58"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(90 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.58"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(101.25 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.54"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(112.5 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.50"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(123.75 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.46"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(135 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.42"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(146.25 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.38"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(157.5 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.34"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(168.75 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.30"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(180 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.25"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(191.25 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.22"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(202.5 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.20"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(213.75 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.20"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(225 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.20"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(236.25 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.20"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(247.5 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.22"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(258.75 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.24"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(270 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.26"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(281.25 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.28"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(292.5 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.30"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(303.75 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.30"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(315 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.30"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(326.25 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.30"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(337.5 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.30"/>
  <path d="M850 150 A210 210 0 0 1 878.6 151.9" transform="rotate(348.75 850 360)" fill="none" stroke="#00A6FF" stroke-width="34" stroke-linecap="butt" opacity="0.30"/>

  <path d="M850 150 A210 210 0 1 1 680.1 483.4" fill="none" stroke="url(#neonStroke)" stroke-width="38" stroke-linecap="round" filter="url(#cyanGlow)"/>
  <line x1="850" y1="86" x2="850" y2="126" stroke="#00FFFF" stroke-width="2" opacity="0.75"/>
  <line x1="850" y1="594" x2="850" y2="634" stroke="#00FFFF" stroke-width="2" opacity="0.45"/>
  <line x1="576" y1="360" x2="616" y2="360" stroke="#00FFFF" stroke-width="2" opacity="0.45"/>
  <line x1="1084" y1="360" x2="1124" y2="360" stroke="#00FFFF" stroke-width="2" opacity="0.75"/>
  <line x1="660" y1="170" x2="688" y2="198" stroke="#3AC8FF" stroke-width="1.5" opacity="0.5"/>
  <line x1="1040" y1="170" x2="1012" y2="198" stroke="#3AC8FF" stroke-width="1.5" opacity="0.5"/>
  <line x1="660" y1="550" x2="688" y2="522" stroke="#3AC8FF" stroke-width="1.5" opacity="0.5"/>
  <line x1="1040" y1="550" x2="1012" y2="522" stroke="#3AC8FF" stroke-width="1.5" opacity="0.5"/>

  <text x="753" y="374" width="200" text-anchor="middle" font-family="Segoe UI" font-size="86" font-weight="800" fill="#FFFFFF" filter="url(#cyanGlow)">65%</text>
  <text x="735" y="424" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#94F8FF">DEVICE SHARE</text>
  <text x="954" y="170" width="160" font-family="Segoe UI" font-size="12" letter-spacing="2" fill="#6EEBFF" opacity="0.82">HUD GAUGE 032</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rasterize the whole gauge as one PNG; the segmented ring and progress arc should remain editable paths.
- ❌ Do not use `<mask>` for the progress reveal; masks are not reliable in the PPT translation path.
- ❌ Do not use `<use>` to clone gauge segments, even though it is tempting for 32 repeated arcs.
- ❌ Do not put glow filters on `<line>` elements; use filters on paths, circles, text, or rects only.
- ❌ Do not rely on PowerPoint chart objects for this look; the premium effect comes from custom SVG geometry, glow, and dark compositing.

## Composition notes
- Keep the gauge large and dominant on the right 55–60% of the canvas; it should feel like the slide’s instrument panel.
- Reserve the left 35–40% for title, subtitle, and context labels, using a dark translucent panel to preserve legibility over the image.
- Use neon cyan sparingly but intensely: bright on the progress arc and small labels, muted on the segmented background track.
- The center percentage should sit inside a quieter inner circle so the number reads cleanly against the busy HUD geometry.