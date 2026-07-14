# SVG Recipe — Neon Cyber Dashboard Gauge

## Visual mechanism
A dark cyber-interface slide centers one KPI inside a 270° radial gauge, using neon cyan as the inactive track and hot crimson as the active value. Layer blurred arc paths behind crisp tick marks, a glowing sweep needle, and oversized digital typography to create a futuristic HUD-style dashboard.

## SVG primitives needed
- 1× `<rect>` for the deep navy slide background
- 2× `<radialGradient>` / `<linearGradient>` fills for background bloom and metallic dial surfaces
- 3× `<filter>` definitions for cyan glow, red glow, and soft panel shadow
- 6× `<path>` arcs for blurred neon gauge tracks, crisp gauge rings, and inner dial outlines
- 41× `<line>` radial tick marks around the 270° gauge span
- 2× `<path>` strokes for the glowing active sweep needle and its crisp overlay
- 5× `<circle>` / `<ellipse>` for central hub, neon cap, and atmospheric glow
- 4× `<rect>` for small HUD panels, progress micro-bars, and decorative data modules
- 7× `<text>` elements with explicit `width` for title, KPI, label, side stats, and footer annotations
- Several `<line>` elements with `stroke-dasharray` for cyber grid accents and calibration guides

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgBloom" cx="50%" cy="46%" r="70%">
      <stop offset="0%" stop-color="#102B4A"/>
      <stop offset="42%" stop-color="#0A101D"/>
      <stop offset="100%" stop-color="#05070D"/>
    </radialGradient>

    <radialGradient id="hubFill" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#213552"/>
      <stop offset="65%" stop-color="#101B2E"/>
      <stop offset="100%" stop-color="#070A12"/>
    </radialGradient>

    <linearGradient id="panelFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#12243D" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#07101D" stop-opacity="0.95"/>
    </linearGradient>

    <filter id="cyanGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="redGlow" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="panelShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBloom)"/>

  <line x1="120" y1="118" x2="1160" y2="118" stroke="#0B7EA4" stroke-opacity="0.28" stroke-width="1" stroke-dasharray="8 12"/>
  <line x1="120" y1="602" x2="1160" y2="602" stroke="#0B7EA4" stroke-opacity="0.22" stroke-width="1" stroke-dasharray="8 12"/>
  <line x1="640" y1="70" x2="640" y2="650" stroke="#0B7EA4" stroke-opacity="0.15" stroke-width="1" stroke-dasharray="5 16"/>

  <text x="120" y="70" width="1040" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" letter-spacing="8" fill="#8BEFFF">PERFORMANCE TELEMETRY</text>
  <text x="120" y="101" width="1040" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="3" fill="#5C7896">NEON CYBER DASHBOARD GAUGE / LIVE KPI STATUS</text>

  <ellipse cx="640" cy="382" rx="360" ry="315" fill="#06101F" opacity="0.78"/>
  <circle cx="640" cy="380" r="184" fill="url(#hubFill)" stroke="#00DDFB" stroke-width="2" filter="url(#cyanGlow)"/>
  <circle cx="640" cy="380" r="151" fill="#08111F" stroke="#16385A" stroke-width="2"/>
  <circle cx="640" cy="380" r="104" fill="#070B13" stroke="#294B70" stroke-width="1.5"/>

  <path d="M 442 578 A 280 280 0 1 1 838 578" fill="none" stroke="#0078FF" stroke-width="30" stroke-opacity="0.36" filter="url(#cyanGlow)"/>
  <path d="M 442 578 A 280 280 0 1 1 838 578" fill="none" stroke="#00E5FF" stroke-width="4" stroke-opacity="0.82"/>
  <path d="M 442 578 A 280 280 0 0 1 822 167" fill="none" stroke="#FF1648" stroke-width="20" stroke-opacity="0.62" filter="url(#redGlow)"/>
  <path d="M 442 578 A 280 280 0 0 1 822 167" fill="none" stroke="#FF174A" stroke-width="5"/>

  <path d="M 514 506 A 178 178 0 1 1 766 506" fill="none" stroke="#00E5FF" stroke-width="2" stroke-opacity="0.35"/>
  <path d="M 532 488 A 153 153 0 1 1 748 488" fill="none" stroke="#102F50" stroke-width="10" stroke-opacity="0.8"/>

  <g stroke-linecap="round">
    <line x1="835" y1="380" x2="930" y2="380" transform="rotate(135 640 380)" stroke="#FF174A" stroke-width="7"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(141.75 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(148.5 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(155.25 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(162 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="835" y1="380" x2="930" y2="380" transform="rotate(168.75 640 380)" stroke="#FF174A" stroke-width="7"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(175.5 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(182.25 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(189 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(195.75 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="835" y1="380" x2="930" y2="380" transform="rotate(202.5 640 380)" stroke="#FF174A" stroke-width="7"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(209.25 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(216 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(222.75 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(229.5 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="835" y1="380" x2="930" y2="380" transform="rotate(236.25 640 380)" stroke="#FF174A" stroke-width="7"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(243 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(249.75 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(256.5 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(263.25 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="835" y1="380" x2="930" y2="380" transform="rotate(270 640 380)" stroke="#FF174A" stroke-width="7"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(276.75 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(283.5 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(290.25 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(297 640 380)" stroke="#FF174A" stroke-width="3"/>
    <line x1="835" y1="380" x2="930" y2="380" transform="rotate(303.75 640 380)" stroke="#FF174A" stroke-width="7"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(310.5 640 380)" stroke="#FF174A" stroke-width="3"/>

    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(317.25 640 380)" stroke="#00E5FF" stroke-width="3"/>
    <line x1="835" y1="380" x2="930" y2="380" transform="rotate(337.5 640 380)" stroke="#00E5FF" stroke-width="7"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(357.75 640 380)" stroke="#00E5FF" stroke-width="3"/>
    <line x1="835" y1="380" x2="930" y2="380" transform="rotate(371.25 640 380)" stroke="#00E5FF" stroke-width="7"/>
    <line x1="880" y1="380" x2="925" y2="380" transform="rotate(391.5 640 380)" stroke="#00E5FF" stroke-width="3"/>
    <line x1="835" y1="380" x2="930" y2="380" transform="rotate(405 640 380)" stroke="#00E5FF" stroke-width="7"/>
  </g>

  <path d="M 640 380 L 822 167" fill="none" stroke="#FF174A" stroke-width="12" stroke-linecap="round" stroke-opacity="0.5" filter="url(#redGlow)"/>
  <path d="M 640 380 L 822 167" fill="none" stroke="#FFE3EA" stroke-width="3" stroke-linecap="round"/>
  <circle cx="640" cy="380" r="28" fill="#FF174A" filter="url(#redGlow)"/>
  <circle cx="640" cy="380" r="13" fill="#FFFFFF"/>

  <text x="500" y="360" width="280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="88" font-weight="800" fill="#FFFFFF">65%</text>
  <text x="520" y="405" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" letter-spacing="4" fill="#8BEFFF">SYSTEM LOAD</text>

  <rect x="130" y="265" width="190" height="130" rx="18" fill="url(#panelFill)" stroke="#0ADCF6" stroke-opacity="0.55" filter="url(#panelShadow)"/>
  <text x="152" y="303" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" letter-spacing="2" fill="#8BEFFF">LATENCY</text>
  <text x="152" y="350" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF">12ms</text>
  <rect x="152" y="369" width="128" height="6" rx="3" fill="#14324F"/>
  <rect x="152" y="369" width="92" height="6" rx="3" fill="#00E5FF"/>

  <rect x="960" y="265" width="190" height="130" rx="18" fill="url(#panelFill)" stroke="#FF174A" stroke-opacity="0.55" filter="url(#panelShadow)"/>
  <text x="982" y="303" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" letter-spacing="2" fill="#FF6A88">RISK INDEX</text>
  <text x="982" y="350" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF">0.31</text>
  <rect x="982" y="369" width="128" height="6" rx="3" fill="#3C1424"/>
  <rect x="982" y="369" width="46" height="6" rx="3" fill="#FF174A"/>

  <text x="370" y="646" width="540" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="3" fill="#4E6E8D">CALIBRATED RANGE 000–100 / ACTIVE SWEEP 65%</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<marker-end>` for the needle; draw the needle as a direct `<path>` stroke instead.
- ❌ Do not apply filters to `<line>` tick marks; duplicate glow should come from blurred `<path>` arcs or filtered hub shapes.
- ❌ Do not use `<textPath>` for curved gauge labels; place small native `<text>` labels manually if needed.
- ❌ Do not use `<mask>` to fade the gauge; PowerPoint translation may fail or ignore it.
- ❌ Do not rely on CSS animations or SVG `<animate>` for the rev-up effect; use PowerPoint animation after translation if needed.

## Composition notes
- Keep the gauge dead center and large: roughly 55–65% of slide height, with the bottom quarter left open for status copy or calibration notes.
- Use cyan for inactive/system elements and crimson for the active KPI sweep; avoid introducing many extra colors.
- The main number should sit inside the inner hub, oversized and editable, with a short all-caps label below it.
- Side panels should be secondary and dimmer than the gauge so the eye returns to the glowing center.