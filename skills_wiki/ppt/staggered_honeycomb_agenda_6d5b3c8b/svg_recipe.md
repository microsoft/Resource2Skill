# SVG Recipe — Staggered Honeycomb Agenda

## Visual mechanism
A compact staggered column of thick-bordered hexagons acts as the numbered agenda spine, while color-matched horizontal banners extend from each hexagon as readable content panels. The alternating left/right honeycomb offsets create motion and connection without needing arrows.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for the dark executive header bar
- 1× `<rect>` for the thin multicolor accent strip under the header
- 5× `<rect>` for colored agenda banners behind the honeycomb
- 5× `<rect>` for darker connector tabs tucked under the hexagons
- 5× `<path>` for foreground hexagons with thick white strokes
- 6× `<path>` for faint background honeycomb outlines
- 12× `<text>` for the title, section kicker, agenda labels, descriptions, and hexagon numbers; every text element uses an explicit `width`
- 6× `<linearGradient>` for premium header and agenda color depth
- 1× `<filter id="softShadow">` applied to banners and hexagons for subtle elevation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1280" y2="0">
      <stop offset="0" stop-color="#050608"/>
      <stop offset="0.55" stop-color="#111827"/>
      <stop offset="1" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="redGrad" x1="285" y1="0" x2="1120" y2="0">
      <stop offset="0" stop-color="#D95258"/>
      <stop offset="1" stop-color="#B93F4B"/>
    </linearGradient>
    <linearGradient id="mintGrad" x1="395" y1="0" x2="1120" y2="0">
      <stop offset="0" stop-color="#A3DDD4"/>
      <stop offset="1" stop-color="#68C4BE"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="285" y1="0" x2="1120" y2="0">
      <stop offset="0" stop-color="#4E8098"/>
      <stop offset="1" stop-color="#31677F"/>
    </linearGradient>
    <linearGradient id="navyGrad" x1="395" y1="0" x2="1120" y2="0">
      <stop offset="0" stop-color="#2D557A"/>
      <stop offset="1" stop-color="#183B5F"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="285" y1="0" x2="1120" y2="0">
      <stop offset="0" stop-color="#1F9BA6"/>
      <stop offset="1" stop-color="#147684"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-25%" width="140%" height="160%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="1280" height="84" fill="url(#headerGrad)"/>
  <rect x="0" y="84" width="1280" height="7" fill="#D95258"/>
  <rect x="255" y="84" width="260" height="7" fill="#A3DDD4"/>
  <rect x="515" y="84" width="255" height="7" fill="#4E8098"/>
  <rect x="770" y="84" width="510" height="7" fill="#2D557A"/>

  <text x="64" y="54" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#FFFFFF" letter-spacing="2">
    PRESENTATION AGENDA
  </text>
  <text x="930" y="52" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#B8C4D6" text-anchor="end" letter-spacing="1.6">
    EXECUTIVE WORKSHOP FLOW
  </text>

  <path d="M1060 142 L1090 90 L1150 90 L1180 142 L1150 194 L1090 194 Z" fill="none" stroke="#EAF0F3" stroke-width="2"/>
  <path d="M1119 246 L1149 194 L1209 194 L1239 246 L1209 298 L1149 298 Z" fill="none" stroke="#EAF0F3" stroke-width="2"/>
  <path d="M1000 350 L1030 298 L1090 298 L1120 350 L1090 402 L1030 402 Z" fill="none" stroke="#EEF3F6" stroke-width="2"/>
  <path d="M1105 455 L1135 403 L1195 403 L1225 455 L1195 507 L1135 507 Z" fill="none" stroke="#EEF3F6" stroke-width="2"/>
  <path d="M78 560 L108 508 L168 508 L198 560 L168 612 L108 612 Z" fill="none" stroke="#F1F5F7" stroke-width="2"/>
  <path d="M153 632 L183 580 L243 580 L273 632 L243 684 L183 684 Z" fill="none" stroke="#F1F5F7" stroke-width="2"/>

  <rect x="285" y="137" width="835" height="66" rx="13" fill="url(#redGrad)" filter="url(#softShadow)"/>
  <rect x="285" y="137" width="42" height="66" rx="10" fill="#9E2936" opacity="0.36"/>
  <rect x="395" y="212" width="725" height="66" rx="13" fill="url(#mintGrad)" filter="url(#softShadow)"/>
  <rect x="395" y="212" width="42" height="66" rx="10" fill="#2D8F91" opacity="0.32"/>
  <rect x="285" y="287" width="835" height="66" rx="13" fill="url(#blueGrad)" filter="url(#softShadow)"/>
  <rect x="285" y="287" width="42" height="66" rx="10" fill="#1D4B60" opacity="0.35"/>
  <rect x="395" y="362" width="725" height="66" rx="13" fill="url(#navyGrad)" filter="url(#softShadow)"/>
  <rect x="395" y="362" width="42" height="66" rx="10" fill="#0C2642" opacity="0.38"/>
  <rect x="285" y="437" width="835" height="66" rx="13" fill="url(#tealGrad)" filter="url(#softShadow)"/>
  <rect x="285" y="437" width="42" height="66" rx="10" fill="#095D68" opacity="0.35"/>

  <text x="350" y="163" width="700" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan font-size="21" font-weight="800" letter-spacing="0.8">OPENING CONTEXT</tspan>
    <tspan x="350" dy="24" font-size="14" font-weight="500" opacity="0.88">Set objectives, audience lens, and success criteria for the session.</tspan>
  </text>
  <text x="460" y="238" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#123D4A">
    <tspan font-size="21" font-weight="800" letter-spacing="0.8">MARKET SIGNALS</tspan>
    <tspan x="460" dy="24" font-size="14" font-weight="600" opacity="0.82">Review customer shifts, competitive pressure, and emerging risks.</tspan>
  </text>
  <text x="350" y="313" width="700" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan font-size="21" font-weight="800" letter-spacing="0.8">INSIGHT SYNTHESIS</tspan>
    <tspan x="350" dy="24" font-size="14" font-weight="500" opacity="0.88">Translate findings into implications for product, revenue, and teams.</tspan>
  </text>
  <text x="460" y="388" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan font-size="21" font-weight="800" letter-spacing="0.8">STRATEGIC CHOICES</tspan>
    <tspan x="460" dy="24" font-size="14" font-weight="500" opacity="0.88">Align on priority bets, trade-offs, ownership, and sequencing.</tspan>
  </text>
  <text x="350" y="463" width="700" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan font-size="21" font-weight="800" letter-spacing="0.8">NEXT STEPS</tspan>
    <tspan x="350" dy="24" font-size="14" font-weight="500" opacity="0.88">Confirm milestones, decision gates, and follow-up governance.</tspan>
  </text>

  <path d="M177 170 L211 111 L279 111 L313 170 L279 229 L211 229 Z" fill="#D95258" stroke="#FFFFFF" stroke-width="10" filter="url(#softShadow)"/>
  <path d="M282 245 L316 186 L384 186 L418 245 L384 304 L316 304 Z" fill="#A3DDD4" stroke="#FFFFFF" stroke-width="10" filter="url(#softShadow)"/>
  <path d="M177 320 L211 261 L279 261 L313 320 L279 379 L211 379 Z" fill="#4E8098" stroke="#FFFFFF" stroke-width="10" filter="url(#softShadow)"/>
  <path d="M282 395 L316 336 L384 336 L418 395 L384 454 L316 454 Z" fill="#2D557A" stroke="#FFFFFF" stroke-width="10" filter="url(#softShadow)"/>
  <path d="M177 470 L211 411 L279 411 L313 470 L279 529 L211 529 Z" fill="#1F9BA6" stroke="#FFFFFF" stroke-width="10" filter="url(#softShadow)"/>

  <text x="245" y="185" width="136" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="900" fill="#FFFFFF">01</text>
  <text x="350" y="260" width="136" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="900" fill="#173D47">02</text>
  <text x="245" y="335" width="136" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="900" fill="#FFFFFF">03</text>
  <text x="350" y="410" width="136" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="900" fill="#FFFFFF">04</text>
  <text x="245" y="485" width="136" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="900" fill="#FFFFFF">05</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the honeycomb with `<use>` clones; duplicate the `<path>` hexagons directly so PowerPoint keeps them editable.
- ❌ Do not rely on arrow markers between agenda steps; the staggered hexagon alignment already implies flow, and `marker-end` on paths will not translate reliably.
- ❌ Do not apply `clip-path` to the hexagons or banners; only use clipping for images, not shapes.
- ❌ Do not make the banners semi-transparent over busy imagery; this layout depends on crisp color blocks and strong text contrast.
- ❌ Do not omit `width` on text elements; agenda labels may truncate or wrap unpredictably in PowerPoint.

## Composition notes
- Keep the honeycomb spine in the left third of the slide; let the banners occupy the middle and right two-thirds for readable agenda copy.
- Draw banners first, then hexagons, so the thick white hexagon borders sit cleanly above the rectangular labels.
- Alternate hexagon x-positions by roughly 100–115 px and y-positions by roughly 70–80 px to create a compact staggered honeycomb rhythm.
- Use one strong color per agenda item, but keep the header neutral and dark so the color-coded process blocks become the primary visual focus.