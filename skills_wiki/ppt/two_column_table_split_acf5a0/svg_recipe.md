# SVG Recipe — Two Column Table Split

## Visual mechanism
A slide-width comparison table is split into two premium “cards” with mirrored column structure, distinct accent colors, and a clean central divider. Each column uses a bold header, stacked table rows, and small semantic icons so the audience can compare two parallel lists without reading a dense grid.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<path>` for soft decorative background blobs
- 2× `<rect>` for main rounded column cards
- 2× `<rect>` for colored header bands
- 8× `<rect>` for alternating row bands inside the two columns
- 6× `<line>` for horizontal row dividers and the vertical split divider
- 8× `<circle>` for row icon badges
- 8× `<path>` for simple check, arrow, warning, and target icons
- 1× `<rect>` for a small center comparison label
- Multiple `<text>` elements with explicit `width` for headline, subtitle, headers, row titles, and row descriptions
- 3× `<linearGradient>` for background and header/card color treatment
- 1× `<filter id="cardShadow">` applied to the card rectangles
- 1× `<filter id="softGlow">` applied to decorative accent blobs

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#EEF4FA"/>
      <stop offset="100%" stop-color="#F7F9FD"/>
    </linearGradient>
    <linearGradient id="leftHead" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1E3A8A"/>
      <stop offset="100%" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="rightHead" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#047857"/>
      <stop offset="100%" stop-color="#10B981"/>
    </linearGradient>
    <linearGradient id="blobGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#93C5FD"/>
      <stop offset="100%" stop-color="#A7F3D0"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-80,130 C60,35 190,70 245,175 C310,300 205,380 55,345 C-70,316 -165,225 -80,130 Z"
        fill="url(#blobGrad)" opacity="0.34" filter="url(#softGlow)"/>
  <path d="M1040,565 C1125,470 1285,475 1355,590 C1415,690 1300,785 1148,750 C1010,720 960,650 1040,565 Z"
        fill="url(#blobGrad)" opacity="0.28" filter="url(#softGlow)"/>

  <text x="72" y="66" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#0F172A">Operating Model Split: Current vs Target</text>
  <text x="74" y="102" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#64748B">Use this shell for side-by-side comparisons, pros and cons, before/after lists, or parallel decision criteria.</text>

  <rect x="70" y="140" width="540" height="500" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="670" y="140" width="540" height="500" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <rect x="70" y="140" width="540" height="92" rx="28" fill="url(#leftHead)"/>
  <rect x="70" y="202" width="540" height="30" fill="#2563EB"/>
  <rect x="670" y="140" width="540" height="92" rx="28" fill="url(#rightHead)"/>
  <rect x="670" y="202" width="540" height="30" fill="#10B981"/>

  <text x="108" y="180" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" fill="#FFFFFF">Current State</text>
  <text x="108" y="208" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#DBEAFE">Fragmented processes and local ownership</text>
  <text x="708" y="180" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" fill="#FFFFFF">Target State</text>
  <text x="708" y="208" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#D1FAE5">Standardized workflow and shared governance</text>

  <line x1="640" y1="155" x2="640" y2="625" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="8 10"/>
  <rect x="603" y="348" width="74" height="34" rx="17" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="620" y="370" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" fill="#64748B">VS</text>

  <rect x="92" y="258" width="496" height="76" rx="16" fill="#F8FAFC"/>
  <rect x="92" y="350" width="496" height="76" rx="16" fill="#FFFFFF"/>
  <rect x="92" y="442" width="496" height="76" rx="16" fill="#F8FAFC"/>
  <rect x="92" y="534" width="496" height="76" rx="16" fill="#FFFFFF"/>
  <rect x="692" y="258" width="496" height="76" rx="16" fill="#F0FDF4"/>
  <rect x="692" y="350" width="496" height="76" rx="16" fill="#FFFFFF"/>
  <rect x="692" y="442" width="496" height="76" rx="16" fill="#F0FDF4"/>
  <rect x="692" y="534" width="496" height="76" rx="16" fill="#FFFFFF"/>

  <line x1="110" y1="342" x2="570" y2="342" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="110" y1="434" x2="570" y2="434" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="110" y1="526" x2="570" y2="526" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="710" y1="342" x2="1170" y2="342" stroke="#DCFCE7" stroke-width="1"/>
  <line x1="710" y1="434" x2="1170" y2="434" stroke="#DCFCE7" stroke-width="1"/>
  <line x1="710" y1="526" x2="1170" y2="526" stroke="#DCFCE7" stroke-width="1"/>

  <circle cx="130" cy="296" r="18" fill="#DBEAFE"/>
  <path d="M121 296 L128 303 L140 288" fill="none" stroke="#2563EB" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="160" y="289" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Ownership</text>
  <text x="160" y="313" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#64748B">Decisions sit inside separate teams with limited cross-functional visibility.</text>

  <circle cx="130" cy="388" r="18" fill="#DBEAFE"/>
  <path d="M121 388 H139 M133 382 L139 388 L133 394" fill="none" stroke="#2563EB" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="160" y="381" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Workflow</text>
  <text x="160" y="405" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#64748B">Handoffs depend on manual updates, meetings, and status chasing.</text>

  <circle cx="130" cy="480" r="18" fill="#DBEAFE"/>
  <path d="M130 469 L142 492 H118 Z M130 477 V484 M130 489 V490" fill="none" stroke="#2563EB" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="160" y="473" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Risk</text>
  <text x="160" y="497" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#64748B">Inconsistent controls create audit exposure and repeated remediation.</text>

  <circle cx="130" cy="572" r="18" fill="#DBEAFE"/>
  <path d="M130 560 C121 560 116 567 116 574 C116 583 124 588 130 588 C136 588 144 583 144 574 C144 567 139 560 130 560 Z M130 568 V580 M124 574 H136" fill="none" stroke="#2563EB" stroke-width="3" stroke-linecap="round"/>
  <text x="160" y="565" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Data</text>
  <text x="160" y="589" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#64748B">Metrics are reconciled after the fact, often with conflicting definitions.</text>

  <circle cx="730" cy="296" r="18" fill="#D1FAE5"/>
  <path d="M721 296 L728 303 L740 288" fill="none" stroke="#059669" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="760" y="289" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Ownership</text>
  <text x="760" y="313" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#64748B">Shared accountability model with clear decision rights and escalation paths.</text>

  <circle cx="730" cy="388" r="18" fill="#D1FAE5"/>
  <path d="M719 388 H741 M735 382 L741 388 L735 394" fill="none" stroke="#059669" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="760" y="381" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Workflow</text>
  <text x="760" y="405" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#64748B">A single intake-to-resolution path with automated routing and service levels.</text>

  <circle cx="730" cy="480" r="18" fill="#D1FAE5"/>
  <path d="M730 466 L744 473 V484 C744 492 738 497 730 500 C722 497 716 492 716 484 V473 Z" fill="none" stroke="#059669" stroke-width="3" stroke-linejoin="round"/>
  <text x="760" y="473" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Controls</text>
  <text x="760" y="497" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#64748B">Embedded policy checks reduce exceptions before they enter production.</text>

  <circle cx="730" cy="572" r="18" fill="#D1FAE5"/>
  <path d="M730 558 C720 558 712 566 712 576 C712 586 720 594 730 594 C740 594 748 586 748 576 C748 566 740 558 730 558 Z M730 566 V576 H740" fill="none" stroke="#059669" stroke-width="3" stroke-linecap="round"/>
  <text x="760" y="565" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Reporting</text>
  <text x="760" y="589" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#64748B">Live performance view with consistent definitions and traceable source data.</text>
</svg>
```

## Avoid in this skill
- ❌ Using a real HTML-style table via `<foreignObject>`; it will not translate and also makes the slide non-editable.
- ❌ Applying `clip-path` to grouped card contents; clipping is only reliable for `<image>` elements.
- ❌ Making the center divider a filtered `<line>`; filters on lines are dropped, so keep divider strokes simple.
- ❌ Overcrowding each row with paragraph-length copy; this layout works best with one bold label plus one concise supporting sentence.
- ❌ Relying only on color to distinguish columns; use labels, icons, and header treatments so the comparison remains clear in grayscale.

## Composition notes
- Keep the headline in the top 15% of the slide and reserve the central 70% for the two equal-width comparison cards.
- Use one accent color per column; repeat it in the header, icon badges, and subtle row backgrounds for rhythm.
- Leave a visible gutter between columns with a dashed divider or small “VS” badge to reinforce the split.
- Four rows per column is the comfortable density; reduce font size only slightly before adding more rows.