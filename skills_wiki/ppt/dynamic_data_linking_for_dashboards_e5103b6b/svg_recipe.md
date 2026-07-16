# SVG Recipe — Dynamic Data-Linking for Dashboards

## Visual mechanism
A premium dark-mode dashboard is presented as a set of live-looking KPI widgets connected to a single Excel “source of truth” panel. The visual story is not the literal OLE link, but the data-linking metaphor: sheet tabs, sync nodes, dashed connector lines, and refreshed chart cards imply that each widget is dynamically fed by spreadsheet data.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark dashboard background
- 3× `<radialGradient>` / `<linearGradient>` fills for ambient glow, cards, and accent charts
- 2× `<filter>` definitions for soft card shadows and cyan/purple glow
- 1× clipped `<image>` for an executive/profile avatar in the static sidebar
- 1× `<clipPath>` with `<circle>` applied to the avatar image
- 8× large rounded `<rect>` elements for sidebar, Excel source panel, KPI cards, and chart containers
- 20+ small `<rect>` elements for spreadsheet cells, sheet tabs, KPI chips, bar charts, and status pills
- 10+ `<line>` elements for grid rules and data-link connector strokes
- 8× `<circle>` elements for sync nodes, chart points, status indicators, and connector endpoints
- 5× `<path>` elements for decorative glow shapes, donut chart arcs, and line-chart trend strokes
- Multiple `<text>` elements with explicit `width` attributes for title, labels, KPIs, chart captions, and data-source annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="0.55" stop-color="#0B0F17"/>
      <stop offset="1" stop-color="#05070B"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#242B38"/>
      <stop offset="1" stop-color="#151A23"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#33E6FF"/>
      <stop offset="1" stop-color="#6C5CFF"/>
    </linearGradient>
    <radialGradient id="ambient" cx="50%" cy="50%" r="55%">
      <stop offset="0" stop-color="#26D9FF" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#26D9FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
    <clipPath id="avatarClip">
      <circle cx="112" cy="128" r="44"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="1020" cy="110" rx="260" ry="150" fill="url(#ambient)" filter="url(#glow)"/>
  <ellipse cx="520" cy="650" rx="340" ry="120" fill="#6C5CFF" opacity="0.16" filter="url(#glow)"/>

  <rect x="42" y="42" width="214" height="636" rx="32" fill="#101620" stroke="#263244" filter="url(#shadow)"/>
  <image href="https://images.example.com/executive-dashboard-avatar.jpg" x="68" y="84" width="88" height="88" clip-path="url(#avatarClip)"/>
  <circle cx="112" cy="128" r="47" fill="none" stroke="url(#cyanGrad)" stroke-width="3"/>
  <text x="68" y="205" width="140" fill="#F8FAFC" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700">JOHN STANLEY</text>
  <text x="68" y="229" width="150" fill="#94A3B8" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12">Executive dashboard owner</text>
  <rect x="68" y="270" width="150" height="34" rx="17" fill="#112D3A" stroke="#1FD5FF"/>
  <circle cx="88" cy="287" r="5" fill="#2CFFB3"/>
  <text x="102" y="292" width="92" fill="#B9F7FF" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="600">Links active</text>

  <text x="68" y="354" width="140" fill="#64748B" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" letter-spacing="1.5">SOURCE FILE</text>
  <rect x="66" y="374" width="154" height="166" rx="18" fill="#17202B" stroke="#334155"/>
  <rect x="82" y="394" width="122" height="24" rx="7" fill="#1E7A45"/>
  <text x="94" y="411" width="96" fill="#E7FFE8" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700">Excel Workbook</text>
  <line x1="82" y1="438" x2="204" y2="438" stroke="#334155" stroke-width="1"/>
  <line x1="82" y1="462" x2="204" y2="462" stroke="#334155" stroke-width="1"/>
  <line x1="82" y1="486" x2="204" y2="486" stroke="#334155" stroke-width="1"/>
  <line x1="122" y1="426" x2="122" y2="510" stroke="#334155" stroke-width="1"/>
  <line x1="164" y1="426" x2="164" y2="510" stroke="#334155" stroke-width="1"/>
  <rect x="88" y="446" width="24" height="8" rx="4" fill="#33E6FF"/>
  <rect x="130" y="470" width="28" height="8" rx="4" fill="#6C5CFF"/>
  <rect x="172" y="494" width="20" height="8" rx="4" fill="#2CFFB3"/>
  <rect x="82" y="522" width="36" height="10" rx="5" fill="#1E293B"/>
  <rect x="124" y="522" width="36" height="10" rx="5" fill="#1E293B"/>
  <rect x="166" y="522" width="28" height="10" rx="5" fill="#1E293B"/>
  <text x="70" y="596" width="150" fill="#94A3B8" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12">Business_Dashboard_Source.xlsx</text>

  <text x="300" y="82" width="270" fill="#F8FAFC" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="800">Dashboard</text>
  <text x="302" y="111" width="360" fill="#94A3B8" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14">Live-linked widgets refreshed from the master Excel model</text>
  <rect x="960" y="62" width="220" height="40" rx="20" fill="#112D3A" stroke="#1FD5FF"/>
  <circle cx="982" cy="82" r="6" fill="#2CFFB3"/>
  <text x="998" y="87" width="150" fill="#B9F7FF" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700">Updated 09:42 AM</text>

  <line x1="220" y1="454" x2="326" y2="196" stroke="#2DD4FF" stroke-width="2" stroke-dasharray="7 9"/>
  <line x1="220" y1="454" x2="604" y2="196" stroke="#6C5CFF" stroke-width="2" stroke-dasharray="7 9"/>
  <line x1="220" y1="454" x2="890" y2="196" stroke="#2CFFB3" stroke-width="2" stroke-dasharray="7 9"/>
  <line x1="220" y1="454" x2="604" y2="426" stroke="#F59E0B" stroke-width="2" stroke-dasharray="7 9"/>
  <circle cx="220" cy="454" r="8" fill="#0B0F17" stroke="#33E6FF" stroke-width="3"/>
  <circle cx="326" cy="196" r="6" fill="#33E6FF"/>
  <circle cx="604" cy="196" r="6" fill="#6C5CFF"/>
  <circle cx="890" cy="196" r="6" fill="#2CFFB3"/>
  <circle cx="604" cy="426" r="6" fill="#F59E0B"/>

  <rect x="300" y="150" width="250" height="190" rx="24" fill="url(#cardGrad)" stroke="#2B3648" filter="url(#shadow)"/>
  <text x="324" y="184" width="160" fill="#CBD5E1" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700">Traffic Usage</text>
  <text x="324" y="224" width="120" fill="#F8FAFC" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="800">67%</text>
  <path d="M455 276 A54 54 0 1 1 506 223" fill="none" stroke="#273244" stroke-width="18" stroke-linecap="round"/>
  <path d="M455 276 A54 54 0 1 1 498 211" fill="none" stroke="url(#cyanGrad)" stroke-width="18" stroke-linecap="round"/>
  <text x="430" y="255" width="74" fill="#94A3B8" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11">used</text>
  <rect x="324" y="294" width="82" height="18" rx="9" fill="#112D3A"/>
  <text x="338" y="307" width="56" fill="#67E8F9" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10">Sheet: Traffic</text>

  <rect x="580" y="150" width="250" height="190" rx="24" fill="url(#cardGrad)" stroke="#2B3648" filter="url(#shadow)"/>
  <text x="604" y="184" width="160" fill="#CBD5E1" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700">Monthly Payments</text>
  <text x="604" y="220" width="120" fill="#F8FAFC" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800">$421K</text>
  <rect x="610" y="278" width="18" height="34" rx="5" fill="#334155"/>
  <rect x="638" y="258" width="18" height="54" rx="5" fill="#33E6FF"/>
  <rect x="666" y="240" width="18" height="72" rx="5" fill="#6C5CFF"/>
  <rect x="694" y="266" width="18" height="46" rx="5" fill="#33E6FF"/>
  <rect x="722" y="226" width="18" height="86" rx="5" fill="#2CFFB3"/>
  <rect x="750" y="250" width="18" height="62" rx="5" fill="#33E6FF"/>
  <rect x="604" y="294" width="88" height="18" rx="9" fill="#211B38"/>
  <text x="618" y="307" width="62" fill="#C4B5FD" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10">Sheet: Payment</text>

  <rect x="860" y="150" width="330" height="190" rx="24" fill="url(#cardGrad)" stroke="#2B3648" filter="url(#shadow)"/>
  <text x="884" y="184" width="190" fill="#CBD5E1" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700">Expense Trend</text>
  <text x="884" y="220" width="130" fill="#F8FAFC" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800">$39.8K</text>
  <line x1="888" y1="292" x2="1156" y2="292" stroke="#334155" stroke-width="1"/>
  <line x1="888" y1="252" x2="1156" y2="252" stroke="#334155" stroke-width="1"/>
  <path d="M890 286 C925 254 945 270 970 244 S1020 290 1050 260 S1104 224 1156 238" fill="none" stroke="#2CFFB3" stroke-width="4" stroke-linecap="round"/>
  <circle cx="970" cy="244" r="5" fill="#2CFFB3"/>
  <circle cx="1050" cy="260" r="5" fill="#2CFFB3"/>
  <circle cx="1156" cy="238" r="5" fill="#2CFFB3"/>
  <rect x="884" y="294" width="94" height="18" rx="9" fill="#123026"/>
  <text x="898" y="307" width="68" fill="#86EFAC" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10">Sheet: Expense</text>

  <rect x="300" y="380" width="390" height="230" rx="26" fill="url(#cardGrad)" stroke="#2B3648" filter="url(#shadow)"/>
  <text x="326" y="418" width="190" fill="#F8FAFC" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800">Linked Data Health</text>
  <text x="326" y="444" width="260" fill="#94A3B8" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12">Each widget points back to a named range, table, or chart in Excel.</text>
  <rect x="326" y="478" width="318" height="36" rx="12" fill="#151E2A"/>
  <circle cx="350" cy="496" r="6" fill="#2CFFB3"/>
  <text x="368" y="501" width="220" fill="#CBD5E1" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13">Traffic Usage → Chart_Traffic</text>
  <rect x="326" y="524" width="318" height="36" rx="12" fill="#151E2A"/>
  <circle cx="350" cy="542" r="6" fill="#33E6FF"/>
  <text x="368" y="547" width="220" fill="#CBD5E1" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13">Payment → Pivot_Monthly</text>
  <rect x="326" y="570" width="318" height="36" rx="12" fill="#151E2A"/>
  <circle cx="350" cy="588" r="6" fill="#F59E0B"/>
  <text x="368" y="593" width="220" fill="#CBD5E1" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13">Expense Trend → Range_Expense</text>

  <rect x="720" y="380" width="470" height="230" rx="26" fill="url(#cardGrad)" stroke="#2B3648" filter="url(#shadow)"/>
  <text x="748" y="418" width="220" fill="#F8FAFC" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800">Refresh Workflow</text>
  <path d="M760 500 C815 444 885 444 940 500 S1065 556 1128 500" fill="none" stroke="url(#cyanGrad)" stroke-width="6" stroke-linecap="round"/>
  <circle cx="760" cy="500" r="18" fill="#112D3A" stroke="#33E6FF" stroke-width="3"/>
  <circle cx="940" cy="500" r="18" fill="#211B38" stroke="#6C5CFF" stroke-width="3"/>
  <circle cx="1128" cy="500" r="18" fill="#123026" stroke="#2CFFB3" stroke-width="3"/>
  <text x="734" y="552" width="80" fill="#CBD5E1" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle">Excel edit</text>
  <text x="900" y="552" width="90" fill="#CBD5E1" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle">Update links</text>
  <text x="1084" y="552" width="90" fill="#CBD5E1" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle">Deck refresh</text>
  <text x="748" y="588" width="350" fill="#94A3B8" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12">Use this slide as a visual dashboard shell; actual OLE links are inserted in PowerPoint after export.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not try to create actual Excel OLE links with SVG; SVG can depict the dashboard and linking metaphor, but live workbook relationships must be added in PowerPoint or via Open XML tooling.
- ❌ Do not use `<foreignObject>` to embed HTML tables or live spreadsheet snippets; it will hard-fail translation.
- ❌ Do not use `<mask>` for chart reveals or glass effects; use gradients, opacity, and native paths instead.
- ❌ Do not apply `clip-path` to chart shapes or cards; clipping is reliable only on `<image>` elements.
- ❌ Do not put arrowheads on `<path>` connectors; if arrows are needed, use `<line>` elements or draw custom triangle arrowheads as small `<path>` shapes.

## Composition notes
- Keep the left 18–22% of the slide as the static “source of truth” rail, with workbook metadata, owner identity, and sync status.
- Use the upper-right area for high-value KPI widgets; reserve the lower-right area for process/status explanations so the slide reads as both dashboard and data-governance story.
- Maintain a dark neutral base with only 3–4 vivid data colors; repeat each color in connector lines, sheet tags, and chart accents to imply mapping between Excel sheets and dashboard widgets.
- Leave generous gutters between cards so dashed link lines and glow effects feel intentional rather than cluttered.