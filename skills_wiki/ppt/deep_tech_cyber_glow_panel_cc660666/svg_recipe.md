# SVG Recipe — Deep Tech Cyber-Glow Panel

## Visual mechanism
A deep navy “cyber space” background is muted by a translucent central glass panel, then energized with layered cyan/magenta neon strokes and blurred glow. The panel becomes a high-contrast focal container while faint network lines, particles, and circuit traces keep the surrounding slide cinematic and technical.

## SVG primitives needed
- 1× `<image>` for the dark abstract technology/network hero background.
- 3× full-slide `<rect>` overlays for darkening, vignette tint, and subtle blue wash.
- 2× `<radialGradient>` fills for off-center cyan and magenta atmospheric glows.
- 2× `<linearGradient>` fills for background depth and neon edge accents.
- 1× `<filter id="cyanGlow">` using `feGaussianBlur` for the glowing panel border and corner brackets.
- 1× `<filter id="magentaGlow">` using `feGaussianBlur` for the magenta accent bar and pulse dots.
- 1× `<filter id="panelShadow">` using `feOffset + feGaussianBlur + feMerge` for panel depth.
- 3× rounded `<rect>` elements for the blurred panel halo, glass fill, and crisp inner border.
- 10–16× `<line>` elements for faint network connections and circuit traces.
- 12–20× `<circle>` elements for background particles, nodes, and small neon points.
- 6–10× `<path>` elements for angular corner brackets, circuit-like strokes, and decorative HUD fragments.
- 3× `<text>` elements with explicit `width` attributes for title, subtitle, and small system label.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B1224"/>
      <stop offset="52%" stop-color="#050811"/>
      <stop offset="100%" stop-color="#02040A"/>
    </linearGradient>

    <radialGradient id="cyanAtmosphere" cx="26%" cy="30%" r="58%">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.28"/>
      <stop offset="45%" stop-color="#006B8F" stop-opacity="0.09"/>
      <stop offset="100%" stop-color="#001018" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="magentaAtmosphere" cx="80%" cy="66%" r="50%">
      <stop offset="0%" stop-color="#FF007F" stop-opacity="0.22"/>
      <stop offset="48%" stop-color="#5B0034" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#09000A" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="panelGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111D32" stop-opacity="0.88"/>
      <stop offset="52%" stop-color="#070B14" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#0A0E17" stop-opacity="0.92"/>
    </linearGradient>

    <linearGradient id="neonStroke" x1="220" y1="0" x2="1060" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF007F"/>
      <stop offset="18%" stop-color="#00E5FF"/>
      <stop offset="78%" stop-color="#00E5FF"/>
      <stop offset="100%" stop-color="#FF007F"/>
    </linearGradient>

    <filter id="cyanGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="magentaGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="panelShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="20" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgDepth)"/>
  <image href="https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.42"/>
  <rect x="0" y="0" width="1280" height="720" fill="#050812" opacity="0.72"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#cyanAtmosphere)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#magentaAtmosphere)"/>

  <line x1="82" y1="116" x2="218" y2="182" stroke="#00E5FF" stroke-width="1.2" opacity="0.22"/>
  <line x1="218" y1="182" x2="356" y2="96" stroke="#00E5FF" stroke-width="1.1" opacity="0.18"/>
  <line x1="930" y1="112" x2="1095" y2="178" stroke="#FF007F" stroke-width="1.2" opacity="0.20"/>
  <line x1="1095" y1="178" x2="1190" y2="90" stroke="#00E5FF" stroke-width="1.0" opacity="0.18"/>
  <line x1="86" y1="592" x2="208" y2="516" stroke="#00E5FF" stroke-width="1.1" opacity="0.17"/>
  <line x1="208" y1="516" x2="328" y2="628" stroke="#FF007F" stroke-width="1.0" opacity="0.18"/>
  <line x1="910" y1="600" x2="1045" y2="532" stroke="#00E5FF" stroke-width="1.1" opacity="0.20"/>
  <line x1="1045" y1="532" x2="1210" y2="622" stroke="#FF007F" stroke-width="1.0" opacity="0.17"/>

  <path d="M64 318 H170 V302 H236" fill="none" stroke="#00E5FF" stroke-width="1.4" stroke-dasharray="10 12" opacity="0.24"/>
  <path d="M1046 316 H1136 V338 H1212" fill="none" stroke="#FF007F" stroke-width="1.4" stroke-dasharray="9 11" opacity="0.25"/>
  <path d="M116 402 H224 V424 H292" fill="none" stroke="#00E5FF" stroke-width="1.2" stroke-dasharray="6 10" opacity="0.18"/>
  <path d="M996 426 H1094 V404 H1190" fill="none" stroke="#00E5FF" stroke-width="1.2" stroke-dasharray="6 10" opacity="0.18"/>

  <circle cx="82" cy="116" r="3.5" fill="#00E5FF" opacity="0.85"/>
  <circle cx="218" cy="182" r="4.5" fill="#FFFFFF" opacity="0.55"/>
  <circle cx="356" cy="96" r="3" fill="#00E5FF" opacity="0.65"/>
  <circle cx="930" cy="112" r="3.5" fill="#FF007F" opacity="0.75"/>
  <circle cx="1095" cy="178" r="4" fill="#00E5FF" opacity="0.70"/>
  <circle cx="1190" cy="90" r="2.8" fill="#FFFFFF" opacity="0.50"/>
  <circle cx="86" cy="592" r="3" fill="#00E5FF" opacity="0.65"/>
  <circle cx="208" cy="516" r="4" fill="#FFFFFF" opacity="0.42"/>
  <circle cx="328" cy="628" r="3.2" fill="#FF007F" opacity="0.75"/>
  <circle cx="910" cy="600" r="3.2" fill="#00E5FF" opacity="0.75"/>
  <circle cx="1045" cy="532" r="4" fill="#FFFFFF" opacity="0.45"/>
  <circle cx="1210" cy="622" r="3.2" fill="#FF007F" opacity="0.75"/>

  <rect x="225" y="190" width="830" height="340" rx="34" fill="none" stroke="url(#neonStroke)" stroke-width="18" opacity="0.70" filter="url(#cyanGlow)"/>
  <rect x="245" y="210" width="790" height="300" rx="28" fill="url(#panelGlass)" filter="url(#panelShadow)"/>
  <rect x="245" y="210" width="790" height="300" rx="28" fill="none" stroke="url(#neonStroke)" stroke-width="3.5"/>
  <rect x="266" y="232" width="5" height="256" rx="2.5" fill="#FF007F" filter="url(#magentaGlow)"/>
  <rect x="1008" y="244" width="4" height="58" rx="2" fill="#00E5FF" opacity="0.85"/>

  <path d="M245 262 V230 Q245 210 277 210 H326" fill="none" stroke="#00E5FF" stroke-width="5" stroke-linecap="round" filter="url(#cyanGlow)"/>
  <path d="M955 210 H1003 Q1035 210 1035 242 V272" fill="none" stroke="#00E5FF" stroke-width="5" stroke-linecap="round" filter="url(#cyanGlow)"/>
  <path d="M245 458 V490 Q245 510 277 510 H330" fill="none" stroke="#FF007F" stroke-width="4.5" stroke-linecap="round" filter="url(#magentaGlow)"/>
  <path d="M950 510 H1003 Q1035 510 1035 478 V448" fill="none" stroke="#00E5FF" stroke-width="4.5" stroke-linecap="round" filter="url(#cyanGlow)"/>

  <circle cx="286" cy="246" r="4" fill="#00E5FF" filter="url(#cyanGlow)"/>
  <circle cx="998" cy="474" r="4" fill="#00E5FF" filter="url(#cyanGlow)"/>
  <circle cx="300" cy="474" r="4" fill="#FF007F" filter="url(#magentaGlow)"/>
  <circle cx="986" cy="246" r="3.5" fill="#FF007F" filter="url(#magentaGlow)"/>

  <text x="640" y="280" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600"
        letter-spacing="4" fill="#00E5FF" opacity="0.95">SECURE AI SYSTEM / LIVE NODE</text>

  <text x="640" y="365" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800"
        letter-spacing="1.5" fill="#FFFFFF">CYBER-GLOW PANEL</text>

  <text x="640" y="420" width="650" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="400"
        fill="#B8C6D8">Frame advanced technology narratives with cinematic neon focus.</text>

  <text x="640" y="466" width="500" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        letter-spacing="3" fill="#7CEFFF" opacity="0.75">DATA SCIENCE · CYBERSECURITY · AI OPS</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` for the panel glass or vignette; use translucent rectangles and gradients instead.
- ❌ Do not apply `filter` to `<line>` elements for glowing networks; PowerPoint translation drops line filters. Use glowing circles/paths for highlights.
- ❌ Do not rely on `<pattern>` for circuit grids; build the visible circuit details with explicit paths and dashed strokes.
- ❌ Do not use `marker-end` for cyber arrows; if directional indicators are needed, draw arrowheads manually with small paths.
- ❌ Do not place `clip-path` on panel rectangles or paths; clipping should only be used on `<image>` elements.

## Composition notes
- Keep the glowing panel centered and sized around 60–70% of slide width so it reads as the main cinematic container.
- Use the brightest cyan/magenta only on borders, corner brackets, nodes, and small accent bars; let the background remain mostly dark.
- Place title and key message inside the panel with generous vertical spacing; reserve the noisy network texture for the outer margins.
- Balance cyan and magenta asymmetrically: cyan should dominate the main frame, while magenta acts as a sharp secondary pulse.