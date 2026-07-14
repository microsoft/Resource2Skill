# SVG Recipe — Corporate Flat-Design KPI Dashboard Layout

## Visual mechanism
A strict four-column card grid converts dense KPI data into contained executive “tiles,” each with a top accent bar, large metric, concise narrative, and mini trend visualization. Soft shadows, restrained teal/navy color rhythm, and generous whitespace create a premium flat-design dashboard that remains fully editable in PowerPoint.

## SVG primitives needed
- 1× `<rect>` for the light-gray slide background
- 2× decorative `<ellipse>` elements for subtle background atmosphere
- 1× `<text>` title and 1× `<text>` subtitle for the dashboard header
- 1× `<line>` for the teal header divider
- 4× large white `<rect>` elements for KPI card bodies, each with a shadow filter
- 4× small teal/navy `<rect>` elements for card top accent bars
- 4× `<circle>` elements for card icon badges
- 4× `<path>` elements for simplified KPI icons inside the badges
- 4× large metric `<text>` elements, 4× quarter/label `<text>` elements, and 4× body-copy `<text>` elements
- 4× `<path>` elements for mini sparkline charts
- 16× small `<circle>` elements for sparkline data points
- 4× pale `<rect>` elements for bottom insight bands inside cards
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for card elevation
- 2× `<linearGradient>` definitions for teal and navy accent styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00B0F0"/>
      <stop offset="100%" stop-color="#26D6C8"/>
    </linearGradient>
    <linearGradient id="navyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1F497D"/>
      <stop offset="100%" stop-color="#163456"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .14 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FAFAFA"/>
  <ellipse cx="1110" cy="105" rx="210" ry="82" fill="#EAF7FB" opacity="0.75"/>
  <ellipse cx="126" cy="682" rx="260" ry="96" fill="#EEF3F8" opacity="0.9"/>

  <text x="86" y="72" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#1F497D">
    Quarterly Sales Summary
  </text>
  <text x="88" y="113" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#787878">
    Performance metrics and key highlights across all regions
  </text>
  <text x="1030" y="76" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#6F7F8F" text-anchor="end">
    FY2026 EXECUTIVE VIEW
  </text>
  <line x1="86" y1="147" x2="1194" y2="147" stroke="#00B0F0" stroke-width="3"/>

  <g transform="translate(86 210)">
    <rect x="0" y="0" width="252" height="400" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="252" height="10" rx="5" fill="url(#tealGrad)"/>
    <circle cx="42" cy="52" r="21" fill="#E9F8FD"/>
    <path d="M31 58 L39 49 L46 54 L56 39" fill="none" stroke="#00B0F0" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="78" y="49" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F497D">Q1 Revenue</text>
    <text x="78" y="70" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#969696">Launch phase</text>
    <text x="24" y="137" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="43" font-weight="700" fill="#1F497D">$2.3M</text>
    <text x="26" y="166" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#00A6DE">+12% versus prior quarter</text>
    <path d="M28 232 C58 212, 76 222, 101 203 S151 185, 177 174 S205 158, 224 145" fill="none" stroke="#00B0F0" stroke-width="4" stroke-linecap="round"/>
    <circle cx="28" cy="232" r="4" fill="#00B0F0"/><circle cx="101" cy="203" r="4" fill="#00B0F0"/><circle cx="177" cy="174" r="4" fill="#00B0F0"/><circle cx="224" cy="145" r="4" fill="#00B0F0"/>
    <rect x="24" y="288" width="204" height="72" rx="12" fill="#F4F8FB"/>
    <text x="40" y="314" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#646464">
      Initial growth from new product rollouts and stronger partner pipeline.
    </text>
  </g>

  <g transform="translate(376 210)">
    <rect x="0" y="0" width="252" height="400" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="252" height="10" rx="5" fill="url(#navyGrad)"/>
    <circle cx="42" cy="52" r="21" fill="#EDF2F7"/>
    <path d="M31 63 L31 48 L39 48 L39 63 M45 63 L45 40 L53 40 L53 63" fill="none" stroke="#1F497D" stroke-width="4" stroke-linecap="round"/>
    <text x="78" y="49" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F497D">Q2 Revenue</text>
    <text x="78" y="70" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#969696">Campaign lift</text>
    <text x="24" y="137" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="43" font-weight="700" fill="#1F497D">$8.8M</text>
    <text x="26" y="166" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#00A6DE">+28% qualified pipeline</text>
    <path d="M28 228 C56 196, 82 211, 106 181 S151 150, 176 162 S205 138, 224 118" fill="none" stroke="#00B0F0" stroke-width="4" stroke-linecap="round"/>
    <circle cx="28" cy="228" r="4" fill="#00B0F0"/><circle cx="106" cy="181" r="4" fill="#00B0F0"/><circle cx="176" cy="162" r="4" fill="#00B0F0"/><circle cx="224" cy="118" r="4" fill="#00B0F0"/>
    <rect x="24" y="288" width="204" height="72" rx="12" fill="#F4F8FB"/>
    <text x="40" y="314" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#646464">
      Targeted marketing accelerated conversion across priority accounts.
    </text>
  </g>

  <g transform="translate(666 210)">
    <rect x="0" y="0" width="252" height="400" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="252" height="10" rx="5" fill="url(#tealGrad)"/>
    <circle cx="42" cy="52" r="21" fill="#E9F8FD"/>
    <path d="M30 51 C37 39, 53 39, 58 51 C53 64, 38 65, 30 51 Z" fill="none" stroke="#00B0F0" stroke-width="4" stroke-linejoin="round"/>
    <text x="78" y="49" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F497D">Q3 Revenue</text>
    <text x="78" y="70" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#969696">Recurring base</text>
    <text x="24" y="137" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="43" font-weight="700" fill="#1F497D">$8.4M</text>
    <text x="26" y="166" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#00A6DE">91% retention strength</text>
    <path d="M28 188 C55 181, 78 188, 104 180 S151 178, 176 170 S204 172, 224 166" fill="none" stroke="#00B0F0" stroke-width="4" stroke-linecap="round"/>
    <circle cx="28" cy="188" r="4" fill="#00B0F0"/><circle cx="104" cy="180" r="4" fill="#00B0F0"/><circle cx="176" cy="170" r="4" fill="#00B0F0"/><circle cx="224" cy="166" r="4" fill="#00B0F0"/>
    <rect x="24" y="288" width="204" height="72" rx="12" fill="#F4F8FB"/>
    <text x="40" y="314" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#646464">
      Enterprise renewals stabilized revenue while expansion deals matured.
    </text>
  </g>

  <g transform="translate(956 210)">
    <rect x="0" y="0" width="252" height="400" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="252" height="10" rx="5" fill="url(#navyGrad)"/>
    <circle cx="42" cy="52" r="21" fill="#EDF2F7"/>
    <path d="M31 58 L42 36 L53 58 Z M42 58 L42 66" fill="none" stroke="#1F497D" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
    <text x="78" y="49" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F497D">Q4 Revenue</text>
    <text x="78" y="70" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#969696">Year-end push</text>
    <text x="24" y="137" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="43" font-weight="700" fill="#1F497D">$9.2M</text>
    <text x="26" y="166" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#00A6DE">Record quarterly close</text>
    <path d="M28 221 C54 220, 78 202, 104 196 S148 157, 176 139 S205 104, 224 92" fill="none" stroke="#00B0F0" stroke-width="4" stroke-linecap="round"/>
    <circle cx="28" cy="221" r="4" fill="#00B0F0"/><circle cx="104" cy="196" r="4" fill="#00B0F0"/><circle cx="176" cy="139" r="4" fill="#00B0F0"/><circle cx="224" cy="92" r="4" fill="#00B0F0"/>
    <rect x="24" y="288" width="204" height="72" rx="12" fill="#F4F8FB"/>
    <text x="40" y="314" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#646464">
      Aggressive enterprise close plan delivered the strongest finish to date.
    </text>
  </g>

  <text x="86" y="668" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9A9A9A">
    Source: Global Sales Operations · Values rounded to nearest $0.1M
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense tables inside the cards; they undermine the “bite-sized KPI” mechanism.
- ❌ Heavy outlines around every card; use white cards plus soft shadows instead.
- ❌ Overusing accent colors on all text; reserve teal for bars, deltas, and trend emphasis.
- ❌ Applying filters to `<line>` sparklines or dividers; use `<path>` for filtered/featured chart strokes if needed.
- ❌ Missing `width` attributes on `<text>`; PowerPoint text boxes may render unpredictably without them.

## Composition notes
- Keep the title block in the top 20–22% of the slide; the KPI cards should own the central visual field.
- Use equal card widths and equal gutters to signal executive rigor and comparability.
- Reserve at least 20–28 px of internal padding per card so metrics feel premium rather than cramped.
- Alternate teal and navy accents subtly across cards to create rhythm while preserving a restrained corporate palette.