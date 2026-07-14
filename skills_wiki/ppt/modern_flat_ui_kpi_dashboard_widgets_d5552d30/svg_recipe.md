# SVG Recipe — Modern Flat-UI KPI Dashboard Widgets

## Visual mechanism
A warm off-white slide becomes a premium software-dashboard canvas: floating white KPI cards with subtle shadows isolate metrics, while thick semi-circular gauges translate progress toward targets at a glance. Scattered geometric color blocks and compact status chips add a modern Flat-UI rhythm without competing with the numbers.

## SVG primitives needed
- 1× `<rect>` for the full-slide cream background
- 20–30× small `<rect>` blocks for scattered modular/pixel background decoration
- 5× rounded `<rect>` cards for floating KPI containers
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` applied to card rectangles
- 1× `<linearGradient>` for a subtle teal gauge highlight
- 4× `<path>` semi-circular gauge arcs: light-gray background tracks plus colored progress arcs
- 4× small `<path>` trend sparklines / micro-chart strokes inside KPI cards
- 5× small rounded `<rect>` status chips / category pills
- Multiple `<text>` elements with explicit `width` for titles, metric values, labels, deltas, and captions
- Optional 1× `<circle>` or `<ellipse>` for tiny legend/status dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="tealGauge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2E8B82"/>
      <stop offset="100%" stop-color="#49B6A9"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F9F9F4"/>

  <!-- scattered flat-ui modular blocks -->
  <rect x="48" y="76" width="22" height="22" fill="#DAA520"/>
  <rect x="82" y="76" width="22" height="22" fill="#663399"/>
  <rect x="82" y="110" width="22" height="22" fill="#2E8B82"/>
  <rect x="1146" y="52" width="26" height="26" fill="#E54D4D"/>
  <rect x="1184" y="52" width="26" height="26" fill="#DAA520"/>
  <rect x="1146" y="90" width="26" height="26" fill="#663399"/>
  <rect x="214" y="608" width="18" height="18" fill="#2E8B82"/>
  <rect x="244" y="608" width="18" height="18" fill="#E54D4D"/>
  <rect x="274" y="638" width="18" height="18" fill="#DAA520"/>
  <rect x="1040" y="632" width="20" height="20" fill="#663399"/>
  <rect x="1072" y="632" width="20" height="20" fill="#2E8B82"/>
  <rect x="1104" y="664" width="20" height="20" fill="#E54D4D"/>

  <!-- title -->
  <text x="78" y="76" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#333333">Quality Control Management</text>
  <text x="80" y="112" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777">Executive KPI dashboard · QBR performance snapshot</text>

  <!-- main gauge card -->
  <rect x="76" y="150" width="500" height="398" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="112" y="202" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="21" fill="#333333">Kaizens Created</text>
  <rect x="432" y="174" width="92" height="30" rx="15" fill="#EAF6F4"/>
  <text x="451" y="196" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2E8B82">ON PLAN</text>
  <path d="M 188 378 A 160 160 0 0 1 508 378" fill="none" stroke="#ECECEC" stroke-width="42" stroke-linecap="round"/>
  <path d="M 188 378 A 160 160 0 0 1 420 231" fill="none" stroke="url(#tealGauge)" stroke-width="42" stroke-linecap="round"/>
  <text x="202" y="354" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="800" text-anchor="middle" fill="#333333">104</text>
  <text x="203" y="392" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="16" text-anchor="middle" fill="#777777">of 150 target initiatives</text>
  <text x="125" y="492" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">Completion</text>
  <text x="125" y="522" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#2E8B82">69%</text>
  <path d="M 336 510 C 362 488, 386 520, 414 496 S 466 484, 512 458" fill="none" stroke="#2E8B82" stroke-width="5" stroke-linecap="round"/>

  <!-- top metric cards -->
  <rect x="612" y="150" width="264" height="186" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="642" y="196" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#777777">Total Losses</text>
  <text x="642" y="260" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#333333">1.5K</text>
  <rect x="642" y="282" width="82" height="28" rx="14" fill="#FDECEC"/>
  <text x="658" y="302" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#E54D4D">▼ 32</text>
  <path d="M 740 301 C 766 276, 787 292, 807 268 S 846 248, 858 222" fill="none" stroke="#E54D4D" stroke-width="4" stroke-linecap="round"/>

  <rect x="916" y="150" width="288" height="186" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="946" y="196" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#777777">OEE Recovery</text>
  <text x="946" y="260" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#333333">87%</text>
  <rect x="946" y="282" width="96" height="28" rx="14" fill="#EAF6F4"/>
  <text x="963" y="302" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2E8B82">▲ 5.4%</text>
  <path d="M 1060 300 C 1085 302, 1096 270, 1122 276 S 1162 244, 1182 218" fill="none" stroke="#2E8B82" stroke-width="4" stroke-linecap="round"/>

  <!-- lower gauge card -->
  <rect x="612" y="374" width="322" height="222" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="642" y="420" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#333333">Safety Actions Closed</text>
  <path d="M 678 524 A 94 94 0 0 1 866 524" fill="none" stroke="#ECECEC" stroke-width="28" stroke-linecap="round"/>
  <path d="M 678 524 A 94 94 0 0 1 823 449" fill="none" stroke="#DAA520" stroke-width="28" stroke-linecap="round"/>
  <text x="706" y="515" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" text-anchor="middle" fill="#333333">74%</text>
  <text x="692" y="564" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" text-anchor="middle" fill="#777777">18 remaining this month</text>

  <!-- status summary card -->
  <rect x="972" y="374" width="232" height="222" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="1002" y="420" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#333333">Status Mix</text>
  <circle cx="1022" cy="468" r="8" fill="#2E8B82"/>
  <text x="1042" y="474" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777">Healthy · 62%</text>
  <circle cx="1022" cy="508" r="8" fill="#DAA520"/>
  <text x="1042" y="514" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777">Watch · 24%</text>
  <circle cx="1022" cy="548" r="8" fill="#E54D4D"/>
  <text x="1042" y="554" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777">At risk · 14%</text>
  <rect x="1002" y="578" width="152" height="10" rx="5" fill="#ECECEC"/>
  <rect x="1002" y="578" width="94" height="10" rx="5" fill="#2E8B82"/>
  <rect x="1096" y="578" width="36" height="10" rx="5" fill="#DAA520"/>
  <rect x="1132" y="578" width="22" height="10" rx="5" fill="#E54D4D"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use native chart objects or embedded screenshots for the KPI cards; build gauges and labels from editable SVG paths and text.
- ❌ Do not use `<mask>` to crop gauges into semicircles; draw semicircular `<path>` arcs directly.
- ❌ Do not apply filters to `<line>` elements for sparklines; use `<path>` strokes if you need curved micro-trends.
- ❌ Do not omit `width` on text; dashboard widgets rely on predictable no-autofit text boxes in PowerPoint.
- ❌ Do not overfill the background with decoration; the colored blocks should read as subtle atmosphere, not chart data.

## Composition notes
- Place the largest gauge card on the left or center-left; it should anchor the slide and consume roughly 35–45% of the canvas width.
- Keep at least 28–40 px internal padding inside every card so the widgets feel like modern SaaS UI panels.
- Use color sparingly and semantically: teal for positive/on-plan, red for negative/risk, mustard for caution, purple/yellow mostly as decorative background accents.
- Preserve generous negative space between cards; the floating-card effect works best when shadows have room to breathe.