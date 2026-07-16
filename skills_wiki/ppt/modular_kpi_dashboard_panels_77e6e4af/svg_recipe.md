# SVG Recipe — Modular KPI Dashboard Panels

## Visual mechanism
A high-density executive dashboard is built from repeated dark “widget” cards on a vivid gradient background. Each card has a consistent hierarchy—header label, oversized KPI number, small icon, and compact chart—so many metrics can be scanned quickly without feeling chaotic.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background.
- 2× decorative `<path>` blobs for soft background energy behind the dashboard.
- 6× main rounded `<rect>` panel bodies with magenta outlines and shadows.
- 6× header `<rect>` strips for panel titles.
- 6× small icon containers using `<circle>` or `<rect>`.
- 6–10× `<path>` for simple editable icons, sparklines, filled area charts, and mini trend shapes.
- 20–35× small `<rect>` elements for bar charts, progress meters, and status bands.
- 4–8× `<circle>` elements for donut/ring indicators and icon badges.
- 8–12× `<line>` elements for chart gridlines and separators.
- Multiple `<text>` elements with explicit `width` attributes for titles, KPI values, labels, percentages, and footnotes.
- 1× `<linearGradient id="bgGrad">` for the orange-to-red background.
- 1× `<linearGradient id="panelGrad">` for dimensional dark panel fills.
- 1× `<filter id="cardShadow">` applied to panel rectangles.
- 1× `<filter id="softGlow">` applied to selected accent paths/text for a premium dashboard glow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff9a1f"/>
      <stop offset="52%" stop-color="#e85b18"/>
      <stop offset="100%" stop-color="#9c261f"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#183f6c"/>
      <stop offset="100%" stop-color="#102a4d"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="9"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M-40,110 C160,30 250,80 400,0 L400,190 C230,250 120,230 -40,290 Z" fill="#ffffff" opacity="0.08"/>
  <path d="M930,640 C1050,520 1210,550 1340,430 L1340,760 L920,760 Z" fill="#ffd37c" opacity="0.12"/>

  <text x="56" y="54" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#ffffff">HSE Monthly Performance Dashboard</text>
  <text x="995" y="52" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#ffe8d0" text-anchor="end">June 2026 • Executive View</text>

  <!-- Panel 1 -->
  <rect x="48" y="92" width="368" height="178" rx="18" fill="url(#panelGrad)" stroke="#ff3ca6" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="48" y="92" width="368" height="44" rx="18" fill="#1d4b80"/>
  <text x="70" y="121" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">Total Recordable Incidents</text>
  <circle cx="376" cy="114" r="17" fill="#ff7b22"/>
  <path d="M376,103 L386,122 L366,122 Z" fill="#ffffff"/>
  <text x="70" y="189" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#f37220">12</text>
  <text x="152" y="190" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#6bbe2b">▼ 18%</text>
  <line x1="250" y1="166" x2="382" y2="166" stroke="#496f99" stroke-width="1"/>
  <line x1="250" y1="206" x2="382" y2="206" stroke="#496f99" stroke-width="1"/>
  <path d="M252,219 C274,190 290,202 310,176 C332,147 354,176 382,141" fill="none" stroke="#6bbe2b" stroke-width="4"/>
  <path d="M252,219 C274,190 290,202 310,176 C332,147 354,176 382,141 L382,236 L252,236 Z" fill="#6bbe2b" opacity="0.18"/>
  <text x="70" y="242" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#dbe9f8">Rolling 6-month incident trend</text>

  <!-- Panel 2 -->
  <rect x="456" y="92" width="368" height="178" rx="18" fill="url(#panelGrad)" stroke="#ff3ca6" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="456" y="92" width="368" height="44" rx="18" fill="#1d4b80"/>
  <text x="478" y="121" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">Lost Time Injury Rate</text>
  <circle cx="783" cy="114" r="17" fill="#2bb3ff"/>
  <path d="M775,122 C776,112 782,105 791,103 C787,112 787,117 793,123 Z" fill="#ffffff"/>
  <text x="478" y="190" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="50" font-weight="800" fill="#f37220">0.84</text>
  <text x="478" y="242" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#dbe9f8">Target ≤ 1.00</text>
  <circle cx="708" cy="187" r="50" fill="none" stroke="#395d86" stroke-width="15"/>
  <circle cx="708" cy="187" r="50" fill="none" stroke="#ffc928" stroke-width="15" stroke-dasharray="215 314" stroke-linecap="round" transform="rotate(-90 708 187)"/>
  <text x="674" y="194" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#ffffff" text-anchor="middle">84%</text>
  <text x="632" y="245" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#dbe9f8" text-anchor="middle">of threshold consumed</text>

  <!-- Panel 3 -->
  <rect x="864" y="92" width="368" height="178" rx="18" fill="url(#panelGrad)" stroke="#ff3ca6" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="864" y="92" width="368" height="44" rx="18" fill="#1d4b80"/>
  <text x="886" y="121" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">Training Completion</text>
  <circle cx="1192" cy="114" r="17" fill="#6bbe2b"/>
  <path d="M1182,115 L1189,122 L1203,105" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
  <text x="886" y="190" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="50" font-weight="800" fill="#f37220">96%</text>
  <rect x="886" y="218" width="286" height="14" rx="7" fill="#395d86"/>
  <rect x="886" y="218" width="275" height="14" rx="7" fill="#6bbe2b"/>
  <text x="886" y="248" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#dbe9f8">1,248 employees certified this month</text>
  <line x1="1145" y1="156" x2="1145" y2="210" stroke="#557aa4" stroke-width="1"/>
  <rect x="1162" y="184" width="10" height="26" fill="#ffcf33"/>
  <rect x="1178" y="165" width="10" height="45" fill="#6bbe2b"/>
  <rect x="1194" y="176" width="10" height="34" fill="#2bb3ff"/>

  <!-- Panel 4 -->
  <rect x="48" y="300" width="368" height="320" rx="18" fill="url(#panelGrad)" stroke="#ff3ca6" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="48" y="300" width="368" height="44" rx="18" fill="#1d4b80"/>
  <text x="70" y="329" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">Audit Findings by Site</text>
  <text x="70" y="391" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#f37220">43</text>
  <text x="145" y="391" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">open items</text>
  <line x1="96" y1="438" x2="360" y2="438" stroke="#496f99" stroke-width="1"/>
  <line x1="96" y1="486" x2="360" y2="486" stroke="#496f99" stroke-width="1"/>
  <line x1="96" y1="534" x2="360" y2="534" stroke="#496f99" stroke-width="1"/>
  <rect x="112" y="460" width="34" height="98" fill="#ff4b1f"/>
  <rect x="162" y="415" width="34" height="143" fill="#ffc928"/>
  <rect x="212" y="500" width="34" height="58" fill="#2bb3ff"/>
  <rect x="262" y="380" width="34" height="178" fill="#6bbe2b"/>
  <rect x="312" y="448" width="34" height="110" fill="#b7c7d9"/>
  <text x="105" y="586" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#dbe9f8">North</text>
  <text x="154" y="586" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#dbe9f8">East</text>
  <text x="207" y="586" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#dbe9f8">West</text>
  <text x="257" y="586" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#dbe9f8">Plant</text>
  <text x="305" y="586" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#dbe9f8">HQ</text>

  <!-- Panel 5 -->
  <rect x="456" y="300" width="368" height="320" rx="18" fill="url(#panelGrad)" stroke="#ff3ca6" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="456" y="300" width="368" height="44" rx="18" fill="#1d4b80"/>
  <text x="478" y="329" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">Risk Register Heat Map</text>
  <text x="478" y="391" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#f37220">7</text>
  <text x="528" y="391" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">critical risks</text>
  <rect x="518" y="430" width="54" height="38" rx="6" fill="#304f75"/>
  <rect x="578" y="430" width="54" height="38" rx="6" fill="#6bbe2b"/>
  <rect x="638" y="430" width="54" height="38" rx="6" fill="#ffc928"/>
  <rect x="698" y="430" width="54" height="38" rx="6" fill="#ff7b22"/>
  <rect x="518" y="474" width="54" height="38" rx="6" fill="#6bbe2b"/>
  <rect x="578" y="474" width="54" height="38" rx="6" fill="#ffc928"/>
  <rect x="638" y="474" width="54" height="38" rx="6" fill="#ff7b22"/>
  <rect x="698" y="474" width="54" height="38" rx="6" fill="#ff4b1f"/>
  <rect x="518" y="518" width="54" height="38" rx="6" fill="#ffc928"/>
  <rect x="578" y="518" width="54" height="38" rx="6" fill="#ff7b22"/>
  <rect x="638" y="518" width="54" height="38" rx="6" fill="#ff4b1f"/>
  <rect x="698" y="518" width="54" height="38" rx="6" fill="#c90045"/>
  <text x="520" y="586" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#dbe9f8">Likelihood × impact matrix, refreshed weekly</text>

  <!-- Panel 6 -->
  <rect x="864" y="300" width="368" height="320" rx="18" fill="url(#panelGrad)" stroke="#ff3ca6" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="864" y="300" width="368" height="44" rx="18" fill="#1d4b80"/>
  <text x="886" y="329" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">Corrective Action Closure</text>
  <text x="886" y="391" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#f37220">78%</text>
  <text x="886" y="420" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#dbe9f8">Closed within SLA</text>
  <line x1="900" y1="482" x2="1180" y2="482" stroke="#496f99" stroke-width="1"/>
  <line x1="900" y1="530" x2="1180" y2="530" stroke="#496f99" stroke-width="1"/>
  <path d="M904,548 C936,512 970,535 1002,488 C1038,436 1078,472 1112,430 C1136,401 1156,415 1180,386" fill="none" stroke="#2bb3ff" stroke-width="5"/>
  <path d="M904,548 C936,512 970,535 1002,488 C1038,436 1078,472 1112,430 C1136,401 1156,415 1180,386" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.8"/>
  <circle cx="1180" cy="386" r="7" fill="#2bb3ff" filter="url(#softGlow)"/>
  <text x="900" y="586" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#dbe9f8">Acceleration after new escalation protocol</text>
</svg>
```

## Avoid in this skill
- ❌ Native PowerPoint chart objects inside SVG; build mini charts from editable SVG primitives instead.
- ❌ Overly thin gridlines or tiny labels below 10–11 px; they become unreadable in a dense dashboard.
- ❌ Heavy photographic backgrounds; they compete with KPI panels and reduce contrast.
- ❌ Using `<clipPath>` on panel shapes for rounded headers; clipping only translates reliably on `<image>`.
- ❌ Applying filters to `<line>` elements; use filters only on cards, paths, circles, rectangles, or text.

## Composition notes
- Keep a strong title band at the top, then use a consistent 3-column modular grid with equal gutters.
- Reserve the brightest colors for KPI values and chart marks; the cards themselves should stay dark and stable.
- Use repeated internal structure—header, number, icon, chart, caption—so every panel feels related.
- Balance density with breathing room: charts can be compact, but each panel needs at least one clear focal number.