# SVG Recipe — Meeting Notes Agenda

## Visual mechanism
A premium meeting-notes agenda slide built like an editorial briefing page: a large headline and compact meta block anchor the top, while the lower two-thirds become a structured, high-density agenda list with numbered checkpoints, dividers, and subtle note-paper styling.

## SVG primitives needed
- 3× <linearGradient> for the warm paper background, card surface, and accent bar
- 2× <filter> for soft card shadow and subtle accent glow
- 8× <rect> for background, card, accent strips, meta capsules, and agenda row highlight bands
- 8× <circle> for numbered agenda markers
- 6× <line> for agenda dividers and editorial guide rules
- 4× <path> for decorative notebook marks, folded-corner detail, and small editorial icons
- 18× <text> for headline, meta information, section labels, agenda numbers, and agenda items
- Nested <tspan> inside selected <text> blocks for inline emphasis and multi-line text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F4EE"/>
      <stop offset="58%" stop-color="#ECE7DE"/>
      <stop offset="100%" stop-color="#DDD6CA"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8F6F1"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#163B4D"/>
      <stop offset="100%" stop-color="#C9864A"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M1040 64 C1110 42 1180 70 1218 122 C1168 108 1118 114 1074 146 C1048 165 1018 160 1002 137 C984 112 998 77 1040 64 Z" fill="#FFFFFF" opacity="0.38"/>
  <path d="M72 606 C164 574 254 596 326 648" fill="none" stroke="#C9864A" stroke-width="3" opacity="0.32" filter="url(#softGlow)"/>

  <rect x="74" y="58" width="1132" height="604" rx="30" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
  <rect x="74" y="58" width="18" height="604" rx="9" fill="url(#accentGrad)"/>
  <rect x="112" y="92" width="2" height="536" fill="#E1D9CE"/>
  <path d="M1176 58 L1206 58 L1206 88 Z" fill="#E9DFD1"/>
  <path d="M1176 58 L1206 88 L1176 88 Z" fill="#D6C7B6" opacity="0.75"/>

  <text x="142" y="124" width="640" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" letter-spacing="2.8" fill="#C9864A">WEEKLY OPERATING REVIEW</text>
  <text x="140" y="184" width="680" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="700" fill="#14242E">
    <tspan x="140" dy="0">Meeting Notes</tspan>
    <tspan x="140" dy="58">&amp; Decision Agenda</tspan>
  </text>
  <text x="142" y="290" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#69737A">
    <tspan x="142" dy="0">Capture context, decisions, owners, and unresolved questions</tspan>
    <tspan x="142" dy="26">in one dense but readable executive briefing format.</tspan>
  </text>

  <rect x="820" y="102" width="312" height="156" rx="22" fill="#F1ECE3" stroke="#E2D8CB"/>
  <text x="850" y="140" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="1.8" fill="#163B4D">MEETING META</text>
  <line x1="850" y1="158" x2="1102" y2="158" stroke="#D5CABD" stroke-width="1"/>
  <text x="850" y="188" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#263740">
    <tspan font-weight="700" fill="#14242E">Date:</tspan><tspan>  18 Mar 2026</tspan>
  </text>
  <text x="850" y="218" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#263740">
    <tspan font-weight="700" fill="#14242E">Owner:</tspan><tspan>  Strategy Office</tspan>
  </text>
  <text x="850" y="248" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#263740">
    <tspan font-weight="700" fill="#14242E">Format:</tspan><tspan>  45 min / hybrid</tspan>
  </text>

  <rect x="140" y="356" width="992" height="42" rx="12" fill="#163B4D"/>
  <text x="164" y="383" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" letter-spacing="2" fill="#FFFFFF">AGENDA FLOW</text>
  <text x="842" y="383" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" text-anchor="end" fill="#D9E5EA">DECISIONS · OWNERS · RISKS</text>

  <rect x="140" y="420" width="992" height="48" rx="12" fill="#F6F1E9"/>
  <circle cx="168" cy="444" r="15" fill="#C9864A"/>
  <text x="160" y="450" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">1</text>
  <text x="198" y="449" width="805" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="650" fill="#1B2C34">Confirm previous action items and open blockers</text>
  <text x="1020" y="449" width="82" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" text-anchor="end" fill="#7A858B">08 min</text>

  <line x1="156" y1="484" x2="1118" y2="484" stroke="#E6DED3" stroke-width="1"/>
  <circle cx="168" cy="510" r="15" fill="#EEF3F5" stroke="#B9C8CE"/>
  <text x="160" y="516" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#163B4D">2</text>
  <text x="198" y="515" width="805" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="650" fill="#1B2C34">Review customer signals, pipeline movement, and demand risks</text>
  <text x="1020" y="515" width="82" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" text-anchor="end" fill="#7A858B">10 min</text>

  <line x1="156" y1="550" x2="1118" y2="550" stroke="#E6DED3" stroke-width="1"/>
  <circle cx="168" cy="576" r="15" fill="#EEF3F5" stroke="#B9C8CE"/>
  <text x="160" y="582" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#163B4D">3</text>
  <text x="198" y="581" width="805" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="650" fill="#1B2C34">Align on product launch dependencies and executive escalations</text>
  <text x="1020" y="581" width="82" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" text-anchor="end" fill="#7A858B">12 min</text>

  <line x1="612" y1="420" x2="612" y2="616" stroke="#E9E1D7" stroke-width="1"/>
  <path d="M962 626 L970 634 L988 610" fill="none" stroke="#C9864A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="140" y="643" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A858B">Note: keep each item outcome-oriented; record decisions as verb-led statements with a named owner.</text>
</svg>
```

## Avoid in this skill
- ❌ Dense paragraphs without row structure; the agenda should scan like a briefing document, not a memo dump
- ❌ Tiny text below ~13 px; this layout is high-density but still presentation-readable
- ❌ <foreignObject> for rich text blocks; use native <text> and <tspan> with explicit width attributes
- ❌ Applying shadows to divider <line> elements; use filters on cards, paths, or rectangles instead
- ❌ Over-decorating the agenda rows; the premium look comes from editorial spacing, quiet rules, and restrained accent color

## Composition notes
- Keep the headline and meeting meta in the top 40% of the slide; reserve the lower 55–60% for agenda rows.
- Use a narrow accent bar or margin rule to create a “notebook page” feeling without consuming content space.
- Agenda items should sit on a consistent baseline grid with clear time/owner metadata aligned to the right.
- Limit the palette to warm paper neutrals, one deep executive color, and one accent color for hierarchy.