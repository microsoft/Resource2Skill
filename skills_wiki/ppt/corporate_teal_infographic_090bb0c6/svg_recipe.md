# SVG Recipe — Corporate Teal Infographic

## Visual mechanism
A polished business infographic built from a strong teal brand panel, diagonal photo geometry, and modular KPI/content cards on a white canvas. The style balances a visually heavy left brand/photo column with a clean right-side grid of icon-led strategy blocks.

## SVG primitives needed
- 1× `<rect>` for the full white slide background.
- 1× `<rect>` for the dominant teal side panel.
- 1× `<image>` clipped into an angled hero-photo crop.
- 1× `<clipPath>` with a `<path>` for the diagonal image crop.
- 2× `<linearGradient>` for teal depth and subtle card accents.
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for soft executive-card depth.
- 1× `<filter id="tealGlow">` using `feGaussianBlur` for a restrained accent glow.
- Multiple `<rect>` elements for white cards, KPI tiles, separators, and mini chart bars.
- Multiple `<circle>` elements for icon medallions and numbered step badges.
- Multiple `<path>` elements for diagonal overlays, abstract corporate geometry, and editable line icons.
- Multiple `<line>` elements for dividers and simple icon/chart strokes.
- Multiple `<text>` elements with explicit `width` attributes for title, section headers, KPI numbers, captions, and body copy.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00B8AA"/>
      <stop offset="100%" stop-color="#007F78"/>
    </linearGradient>
    <linearGradient id="cardAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00A99D"/>
      <stop offset="100%" stop-color="#DFF7F5"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="tealGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
    <clipPath id="angledPhoto">
      <path d="M0,0 H430 L365,720 H0 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="420" height="720" fill="url(#tealGrad)"/>
  <image href="https://images.example.com/corporate-team-strategy-workshop.jpg" x="0" y="0" width="430" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#angledPhoto)" opacity="0.34"/>
  <path d="M0,470 C95,430 185,490 300,440 C350,418 382,410 420,420 L420,720 L0,720 Z" fill="#005F5A" opacity="0.35"/>
  <path d="M348,0 L430,0 L365,720 L292,720 Z" fill="#404040" opacity="0.18"/>
  <circle cx="90" cy="92" r="44" fill="#FFFFFF" opacity="0.18" filter="url(#tealGlow)"/>
  <path d="M72,92 h36 M90,74 v36 M77,79 c23,-20 50,7 30,30 c-18,20 -47,2 -30,-30 Z" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="70" y="178" width="290" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="800" fill="#FFFFFF" letter-spacing="1.5">MARKETING</text>
  <text x="70" y="225" width="290" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="800" fill="#FFFFFF" letter-spacing="1.5">PLAN</text>
  <line x1="70" y1="252" x2="260" y2="252" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
  <text x="70" y="300" width="275" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#EAFDFC">Go-to-market strategy, growth architecture, and revenue execution priorities for the next operating cycle.</text>

  <rect x="70" y="545" width="250" height="88" rx="18" fill="#FFFFFF" opacity="0.16"/>
  <text x="94" y="582" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">4.8×</text>
  <text x="190" y="573" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">PIPELINE VELOCITY</text>
  <text x="190" y="606" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#D7FFFB">forecasted uplift from focused channel mix</text>

  <text x="480" y="82" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#00A99D" letter-spacing="2">GROWTH OPERATING MODEL</text>
  <text x="480" y="126" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" fill="#333333">Supporting the founder with clear, measurable execution</text>
  <text x="480" y="174" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#606060">Monitor every step, document learnings, and create a repeatable playbook for conversion, retention, and account expansion.</text>

  <rect x="480" y="225" width="230" height="145" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="480" y="225" width="230" height="8" rx="4" fill="url(#cardAccent)"/>
  <circle cx="528" cy="284" r="28" fill="#E1F7F5"/>
  <path d="M516,291 L528,271 L540,291 M521,284 H535" fill="none" stroke="#00A99D" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="570" y="277" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="800" fill="#333333">Vision</text>
  <text x="570" y="306" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#666666">Define segments, value narrative, and launch ambition.</text>
  <text x="506" y="345" width="56" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#00A99D">01</text>

  <rect x="740" y="225" width="230" height="145" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="740" y="225" width="230" height="8" rx="4" fill="url(#cardAccent)"/>
  <circle cx="788" cy="284" r="28" fill="#E1F7F5"/>
  <path d="M772,288 c10,-22 40,-22 50,0 M781,276 l7,-10 l7,10 M805,276 l7,-10 l7,10" fill="none" stroke="#00A99D" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="830" y="277" width="125" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="800" fill="#333333">Stabilize</text>
  <text x="830" y="306" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#666666">Install cadence, ownership, and management rituals.</text>
  <text x="766" y="345" width="56" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#00A99D">02</text>

  <rect x="1000" y="225" width="190" height="145" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="1000" y="225" width="190" height="8" rx="4" fill="url(#cardAccent)"/>
  <circle cx="1048" cy="284" r="28" fill="#E1F7F5"/>
  <path d="M1036,270 h25 v28 h-25 Z M1041,280 h15 M1041,290 h10 M1060,297 l10,10 l20,-25" fill="none" stroke="#00A99D" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="1090" y="277" width="82" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="800" fill="#333333">Assess</text>
  <text x="1090" y="306" width="78" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#666666">Pressure-test readiness.</text>
  <text x="1026" y="345" width="56" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#00A99D">03</text>

  <rect x="480" y="410" width="710" height="185" rx="26" fill="#F4F6F6" filter="url(#cardShadow)"/>
  <text x="510" y="455" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#333333">Performance dashboard</text>
  <text x="510" y="484" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#666666">A compact executive view for weekly decisions and board-ready updates.</text>
  <rect x="520" y="525" width="34" height="36" rx="6" fill="#00A99D"/>
  <rect x="565" y="500" width="34" height="61" rx="6" fill="#404040"/>
  <rect x="610" y="476" width="34" height="85" rx="6" fill="#00A99D"/>
  <rect x="655" y="512" width="34" height="49" rx="6" fill="#9FE3DE"/>
  <line x1="510" y1="562" x2="715" y2="562" stroke="#B8B8B8" stroke-width="2"/>

  <rect x="785" y="445" width="118" height="96" rx="18" fill="#FFFFFF"/>
  <text x="808" y="486" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#00A99D">68%</text>
  <text x="808" y="515" width="78" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#666666">qualified leads</text>
  <rect x="925" y="445" width="118" height="96" rx="18" fill="#FFFFFF"/>
  <text x="948" y="486" width="82" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#333333">21d</text>
  <text x="948" y="515" width="78" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#666666">sales cycle</text>
  <rect x="1065" y="445" width="92" height="96" rx="18" fill="#00A99D"/>
  <text x="1085" y="486" width="55" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#FFFFFF">3</text>
  <text x="1085" y="515" width="55" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E9FFFD">priority bets</text>

  <text x="480" y="657" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8A8A8A">CONFIDENTIAL STRATEGY SNAPSHOT  •  FY2026 COMMERCIAL PLANNING</text>
  <text x="1145" y="657" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#00A99D">04 / 12</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the whole slide as a flat screenshot; the power of the technique is editable teal panels, cards, icons, and text.
- ❌ Do not use `<mask>` for the diagonal photo fade; use a `<clipPath>` applied directly to the `<image>`.
- ❌ Do not apply `filter` to `<line>` elements; put shadows on cards or decorative paths instead.
- ❌ Do not rely on complex arrow markers for process flow; if arrows are needed, draw them with simple editable `<line>` and `<path>` shapes.
- ❌ Do not overuse teal everywhere; reserve it for hierarchy, section rhythm, icons, and key metrics.

## Composition notes
- Keep the left 28–33% of the slide visually heavy with teal, photography, and brand/title content; reserve the right side for structured information.
- Use white or very light gray cards on the right with soft shadows so the layout feels executive rather than flat.
- Repeat teal in small controlled doses: card top rules, icon strokes, KPI numbers, and footer/page accents.
- Maintain generous spacing between cards; this style depends on clean alignment and calm negative space.