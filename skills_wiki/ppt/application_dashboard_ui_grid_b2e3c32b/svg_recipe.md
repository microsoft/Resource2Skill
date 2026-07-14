# SVG Recipe — Application Dashboard UI Grid

## Visual mechanism
A modern software-dashboard slide uses a branded header, pale workspace background, and a strict multi-column grid of elevated white cards. Each card has equal visual weight but contains micro-hierarchy through icon chips, bold titles, muted descriptions, status badges, and small UI metrics.

## SVG primitives needed
- 2× `<rect>` for the full-slide background and branded header ribbon
- 6× `<rect>` with rounded corners and shadow filter for elevated dashboard cards
- 6× `<circle>` or rounded `<rect>` icon containers for card-leading symbols
- 6× simple `<path>` icon drawings for app/module glyphs
- 6× small rounded `<rect>` badges for status labels
- 6× progress/metadata mini-bars using paired `<rect>` elements
- 1× `<linearGradient>` for the premium header fill
- 1× `<linearGradient>` for icon accent fills
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for soft UI elevation
- Multiple `<text width="...">` elements for header, subtitle, card titles, descriptions, badges, and metrics

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#25106B"/>
      <stop offset="0.55" stop-color="#673AB7"/>
      <stop offset="1" stop-color="#1486D8"/>
    </linearGradient>
    <linearGradient id="iconGrad" x1="0" y1="0" x2="70" y2="70" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#22D3EE"/>
      <stop offset="1" stop-color="#4F46E5"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.04 0 0 0 0 0.06 0 0 0 0 0.12 0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F6FA"/>
  <rect x="0" y="0" width="1280" height="128" fill="url(#headerGrad)"/>
  <circle cx="1182" cy="32" r="5" fill="#FFC107"/>
  <circle cx="1210" cy="32" r="5" fill="#FFC107"/>
  <circle cx="1238" cy="32" r="5" fill="#FFC107"/>
  <circle cx="1182" cy="60" r="5" fill="#FFC107"/>
  <circle cx="1210" cy="60" r="5" fill="#FFC107"/>
  <circle cx="1238" cy="60" r="5" fill="#FFC107"/>

  <text x="64" y="55" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#FFFFFF">Controls Explorer</text>
  <text x="64" y="91" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#DAD7FF">Application modules, release status, and adoption health in one scannable dashboard</text>
  <rect x="972" y="42" width="190" height="38" rx="19" fill="#FFFFFF" opacity="0.16"/>
  <text x="1000" y="67" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Q4 Product Suite</text>

  <rect x="64" y="164" width="352" height="188" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="88" y="188" width="56" height="56" rx="16" fill="url(#iconGrad)"/>
  <path d="M101 223 L112 209 L123 218 L134 198" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="299" y="190" width="84" height="28" rx="14" fill="#E8F5E9"/>
  <text x="317" y="210" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#2E7D32">Updated</text>
  <text x="88" y="275" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#212121">Chart Studio</text>
  <text x="88" y="304" width="282" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#757575">Thirty chart types with financial, real-time, and embedded analytics views.</text>
  <rect x="88" y="326" width="248" height="8" rx="4" fill="#ECEFF5"/>
  <rect x="88" y="326" width="188" height="8" rx="4" fill="#673AB7"/>

  <rect x="464" y="164" width="352" height="188" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="488" y="188" width="56" height="56" rx="16" fill="#EEF2FF"/>
  <path d="M502 202 H530 V230 H502 Z M511 211 H521 M511 220 H524" fill="none" stroke="#4F46E5" stroke-width="4" stroke-linecap="round"/>
  <rect x="704" y="190" width="78" height="28" rx="14" fill="#E3F2FD"/>
  <text x="725" y="210" width="42" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#1565C0">Core</text>
  <text x="488" y="275" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#212121">DataGrid</text>
  <text x="488" y="304" width="286" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#757575">Grouping, filtering, virtual scrolling, and export workflows for dense data.</text>
  <rect x="488" y="326" width="248" height="8" rx="4" fill="#ECEFF5"/>
  <rect x="488" y="326" width="216" height="8" rx="4" fill="#1486D8"/>

  <rect x="864" y="164" width="352" height="188" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="888" y="188" width="56" height="56" rx="16" fill="#FFF3E0"/>
  <path d="M904 201 H929 V232 H904 Z M910 211 H923 M910 221 H926" fill="none" stroke="#FB8C00" stroke-width="4" stroke-linecap="round"/>
  <rect x="1108" y="190" width="74" height="28" rx="14" fill="#FFF8E1"/>
  <text x="1130" y="210" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#F57F17">New</text>
  <text x="888" y="275" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#212121">PDF Viewer</text>
  <text x="888" y="304" width="286" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#757575">Fast document rendering with search, zoom, selection, and annotations.</text>
  <rect x="888" y="326" width="248" height="8" rx="4" fill="#ECEFF5"/>
  <rect x="888" y="326" width="142" height="8" rx="4" fill="#FFC107"/>

  <rect x="64" y="392" width="352" height="188" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="88" y="416" width="56" height="56" rx="16" fill="#F3E5F5"/>
  <path d="M101 431 H132 M101 444 H132 M101 457 H121" fill="none" stroke="#8E24AA" stroke-width="5" stroke-linecap="round"/>
  <rect x="303" y="418" width="80" height="28" rx="14" fill="#F3E5F5"/>
  <text x="323" y="438" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#6A1B9A">Beta</text>
  <text x="88" y="503" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#212121">ListView</text>
  <text x="88" y="532" width="286" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#757575">Flexible collection layouts with grouping, refresh gestures, and selection states.</text>
  <rect x="88" y="554" width="248" height="8" rx="4" fill="#ECEFF5"/>
  <rect x="88" y="554" width="164" height="8" rx="4" fill="#8E24AA"/>

  <rect x="464" y="392" width="352" height="188" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="488" y="416" width="56" height="56" rx="16" fill="#E0F7FA"/>
  <path d="M501 433 H531 M501 448 H531 M510 424 V463 M524 424 V463" fill="none" stroke="#00ACC1" stroke-width="4" stroke-linecap="round"/>
  <rect x="704" y="418" width="78" height="28" rx="14" fill="#E0F2F1"/>
  <text x="723" y="438" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#00796B">Stable</text>
  <text x="488" y="503" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#212121">Scheduler</text>
  <text x="488" y="532" width="286" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#757575">Calendar planning, appointments, resources, reminders, and availability views.</text>
  <rect x="488" y="554" width="248" height="8" rx="4" fill="#ECEFF5"/>
  <rect x="488" y="554" width="202" height="8" rx="4" fill="#00ACC1"/>

  <rect x="864" y="392" width="352" height="188" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="888" y="416" width="56" height="56" rx="16" fill="#E8F5E9"/>
  <path d="M901 433 L916 456 L933 424" fill="none" stroke="#43A047" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="1092" y="418" width="90" height="28" rx="14" fill="#E8F5E9"/>
  <text x="1113" y="438" width="52" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#2E7D32">Ready</text>
  <text x="888" y="503" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#212121">ComboBox</text>
  <text x="888" y="532" width="286" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#757575">Type-ahead search, token selection, and controlled option lists for forms.</text>
  <rect x="888" y="554" width="248" height="8" rx="4" fill="#ECEFF5"/>
  <rect x="888" y="554" width="176" height="8" rx="4" fill="#43A047"/>

  <text x="64" y="646" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#8A8F9C">Last sync: 10:42 AM · 6 modules · 3 release channels</text>
</svg>
```

## Avoid in this skill
- ❌ Overloading cards with long paragraphs; the dashboard effect depends on fast scanning and consistent card density.
- ❌ Using different card sizes unless one item is intentionally promoted; equal hierarchy requires a disciplined grid.
- ❌ Applying shadows to `<line>` elements; use filtered rounded rectangles for elevation instead.
- ❌ Using `<foreignObject>` for HTML-like UI; build cards from native SVG shapes and text so PowerPoint remains editable.
- ❌ Omitting `width` on `<text>`; fixed text width is required for reliable PowerPoint rendering.

## Composition notes
- Keep the header at roughly 15–20% of slide height, then let the card grid occupy the workspace below with generous outer margins.
- Use identical card widths, heights, corner radius, and gutters to create the “application dashboard” rhythm.
- Put the strongest brand color in the header and repeat it sparingly in icons, progress bars, or badges.
- Use muted gray descriptions and small metadata elements so card titles and status badges remain the main scanning anchors.