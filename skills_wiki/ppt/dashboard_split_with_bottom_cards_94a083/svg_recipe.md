# SVG Recipe — Dashboard Split with Bottom Cards

## Visual mechanism
A high-density executive dashboard split: a large visual panel anchors the left side, stacked KPI cards create a sharp right rail, and compact bottom cards summarize operational takeaways. The look comes from layered rounded panels, clipped hero imagery, glowing gradient accents, and disciplined metric typography.

## SVG primitives needed
- 1× `<rect>` for full-slide background
- 4× `<linearGradient>` for background depth, accent strokes, KPI fills, and bottom-card highlights
- 2× `<radialGradient>` for soft ambient glow fields
- 2× `<filter>` using blur / offset / merge for card shadows and accent glow
- 1× `<clipPath>` with rounded `<rect>` applied to the hero `<image>`
- 1× `<image>` for the left dashboard / operations hero visual
- 10–14× `<rect>` for hero container, KPI cards, bottom cards, micro UI overlays, and dividers
- 5–7× `<path>` for geometric accent ribbons, chart shapes, and decorative dashboard overlays
- 3× `<line>` for small trend indicators and card separators
- 20–30× `<text>` elements with explicit `width` attributes for title, KPIs, labels, and card copy
- 3× `<circle>` / `<ellipse>` for status dots, glow nodes, and chart markers

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="52%" stop-color="#0B1728"/>
      <stop offset="100%" stop-color="#101827"/>
    </linearGradient>
    <linearGradient id="heroStroke" x1="90" y1="110" x2="790" y2="500">
      <stop offset="0%" stop-color="#57E6FF"/>
      <stop offset="45%" stop-color="#5A7CFF"/>
      <stop offset="100%" stop-color="#B66DFF"/>
    </linearGradient>
    <linearGradient id="kpiFill" x1="850" y1="118" x2="1180" y2="442">
      <stop offset="0%" stop-color="#152842"/>
      <stop offset="100%" stop-color="#0D1829"/>
    </linearGradient>
    <linearGradient id="cardAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#20D6C7"/>
      <stop offset="55%" stop-color="#4A8BFF"/>
      <stop offset="100%" stop-color="#B66DFF"/>
    </linearGradient>
    <radialGradient id="cyanGlow" cx="28%" cy="26%" r="55%">
      <stop offset="0%" stop-color="#1FE8FF" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#1FE8FF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="violetGlow" cx="86%" cy="58%" r="44%">
      <stop offset="0%" stop-color="#8F5BFF" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#8F5BFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
    <clipPath id="heroClip">
      <rect x="76" y="130" width="720" height="360" rx="30"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="290" cy="150" rx="420" ry="260" fill="url(#cyanGlow)"/>
  <ellipse cx="1090" cy="420" rx="340" ry="260" fill="url(#violetGlow)"/>

  <path d="M0 616 C190 570 312 604 470 560 C620 518 736 548 880 500 C1052 442 1160 470 1280 424 L1280 720 L0 720 Z"
        fill="#0B1220" opacity="0.72"/>
  <path d="M1018 56 L1260 56 L1260 196 C1172 184 1116 150 1074 112 C1052 92 1032 76 1018 56 Z"
        fill="#1B2E4D" opacity="0.62" filter="url(#softGlow)"/>

  <text x="76" y="70" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#F4F8FF">
    Q4 Platform Health Command Center
  </text>
  <text x="78" y="104" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9FB3C8">
    Real-time split dashboard with executive KPIs, signal quality, and bottom-line operational actions
  </text>

  <rect x="76" y="130" width="720" height="360" rx="30" fill="#0D1A2C" filter="url(#shadow)"/>
  <rect x="76" y="130" width="720" height="360" rx="30" fill="none" stroke="url(#heroStroke)" stroke-width="2.4" opacity="0.9"/>
  <image href="https://images.example.com/hero-photo-dark-network-operations-dashboard.jpg"
         x="76" y="130" width="720" height="360" preserveAspectRatio="xMidYMid slice" clip-path="url(#heroClip)"/>

  <rect x="104" y="160" width="260" height="64" rx="18" fill="#07111F" opacity="0.78"/>
  <circle cx="132" cy="192" r="8" fill="#18E0B5"/>
  <text x="150" y="186" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#EAF3FF">LIVE OPERATIONS</text>
  <text x="150" y="205" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8FA6BD">42 regions synchronized</text>

  <path d="M136 414 C206 382 258 394 318 360 C384 322 432 338 492 302 C560 262 620 274 704 232"
        fill="none" stroke="#28E6C8" stroke-width="4" stroke-linecap="round"/>
  <path d="M136 432 C214 420 286 456 362 418 C438 380 486 404 560 372 C626 344 676 344 736 318"
        fill="none" stroke="#6F8DFF" stroke-width="3" stroke-linecap="round" opacity="0.9"/>
  <circle cx="704" cy="232" r="7" fill="#28E6C8" filter="url(#softGlow)"/>
  <circle cx="736" cy="318" r="6" fill="#8FA2FF"/>

  <rect x="548" y="158" width="204" height="104" rx="22" fill="#07111F" opacity="0.76"/>
  <text x="572" y="192" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A8BD">Throughput index</text>
  <text x="572" y="232" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">98.4</text>
  <text x="705" y="232" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#28E6C8">%</text>

  <rect x="842" y="130" width="360" height="102" rx="24" fill="url(#kpiFill)" filter="url(#shadow)"/>
  <rect x="842" y="130" width="5" height="102" rx="3" fill="#28E6C8"/>
  <text x="870" y="164" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FB3C8">Revenue retained</text>
  <text x="870" y="207" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">$18.7M</text>
  <text x="1060" y="174" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#28E6C8">▲ 12.8%</text>
  <line x1="1060" y1="198" x2="1162" y2="198" stroke="#28E6C8" stroke-width="3" stroke-linecap="round"/>

  <rect x="842" y="254" width="360" height="102" rx="24" fill="url(#kpiFill)" filter="url(#shadow)"/>
  <rect x="842" y="254" width="5" height="102" rx="3" fill="#5A7CFF"/>
  <text x="870" y="288" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FB3C8">Latency reduction</text>
  <text x="870" y="331" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">31ms</text>
  <text x="1060" y="298" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#80A0FF">▼ 24%</text>
  <line x1="1060" y1="322" x2="1162" y2="322" stroke="#5A7CFF" stroke-width="3" stroke-linecap="round"/>

  <rect x="842" y="378" width="360" height="112" rx="24" fill="url(#kpiFill)" filter="url(#shadow)"/>
  <rect x="842" y="378" width="5" height="112" rx="3" fill="#B66DFF"/>
  <text x="870" y="412" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FB3C8">Risk exposure</text>
  <text x="870" y="455" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">Low</text>
  <text x="1060" y="424" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#CFA7FF">4 alerts</text>
  <line x1="1060" y1="448" x2="1162" y2="448" stroke="#B66DFF" stroke-width="3" stroke-linecap="round"/>

  <rect x="76" y="536" width="354" height="126" rx="26" fill="#0F1C30" filter="url(#shadow)"/>
  <rect x="76" y="536" width="354" height="5" rx="3" fill="url(#cardAccent)"/>
  <text x="104" y="578" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">Stabilize priority regions</text>
  <text x="104" y="610" width="284" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A8B9CA">Route extra capacity to APAC edge clusters before Monday demand spike.</text>
  <text x="104" y="640" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#28E6C8">Owner: SRE</text>

  <rect x="462" y="536" width="354" height="126" rx="26" fill="#0F1C30" filter="url(#shadow)"/>
  <rect x="462" y="536" width="354" height="5" rx="3" fill="url(#cardAccent)"/>
  <text x="490" y="578" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">Convert signal into actions</text>
  <text x="490" y="610" width="284" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A8B9CA">Push anomaly scoring into account plans for top 50 enterprise renewals.</text>
  <text x="490" y="640" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#80A0FF">Due: 10 business days</text>

  <rect x="848" y="536" width="354" height="126" rx="26" fill="#0F1C30" filter="url(#shadow)"/>
  <rect x="848" y="536" width="354" height="5" rx="3" fill="url(#cardAccent)"/>
  <text x="876" y="578" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">Board-ready narrative</text>
  <text x="876" y="610" width="284" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A8B9CA">Frame improvements as margin protection, not just infrastructure hygiene.</text>
  <text x="876" y="640" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#CFA7FF">Status: ready</text>
</svg>
```

## Avoid in this skill
- ❌ Using a plain two-column table; the technique relies on visual hierarchy, not a grid of equal boxes.
- ❌ Applying `clip-path` to KPI card rectangles for rounded corners; draw rounded `<rect>` shapes directly and reserve clipping for the hero `<image>`.
- ❌ Putting filters on `<line>` trend indicators; shadows and glows should be on cards, circles, paths, or text instead.
- ❌ Overloading the bottom cards with full paragraphs; keep them as executive action capsules.

## Composition notes
- Keep the headline in the top-left 10–15% of the slide; the title should align with the hero panel, not the KPI rail.
- Allocate roughly 60% width to the clipped hero/dashboard image and 30% width to the stacked metric rail.
- Bottom cards should form a strong horizontal base, each with one key action, one short explanation, and one ownership/status tag.
- Use one cool accent family across the slide — cyan, blue, violet — so the split dashboard feels technical but cohesive.