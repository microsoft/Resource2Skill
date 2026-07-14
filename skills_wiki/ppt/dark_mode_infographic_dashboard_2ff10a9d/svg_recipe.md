# SVG Recipe — Dark Mode Infographic Dashboard

## Visual mechanism
A dark gradient canvas is divided into thin-outlined dashboard panels, where luminous blue charts and oversized white KPI typography create a premium “mission control” data view. The design relies on strict grid alignment, subtle glows, and multiple chart idioms—bars, donut, gauge, sparkline, and line/area chart—to make dense metrics readable at a glance.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background.
- 8× `<rect>` for dashboard panels, KPI cards, slicer chips, and chart frames.
- 20+× `<rect>` for horizontal bars, KPI mini-bars, and UI indicator blocks.
- 1× `<path>` for a decorative glowing data-wave accent behind the dashboard.
- 1× `<path>` for the bottom area chart fill.
- 1× `<path>` for the main line chart stroke.
- 2× `<path>` for the semi-circular gauge track and progress arc.
- 4× `<circle>` for donut chart segments using `stroke-dasharray`.
- 8× `<circle>` for chart data points and small status indicators.
- 15+× `<line>` for chart axes, gridlines, and separators.
- Multiple `<text>` elements with explicit `width` attributes for title, panel labels, KPI numbers, axis labels, and annotations.
- 3× `<linearGradient>` for background, panel fill, and chart area/blue accents.
- 1× `<radialGradient>` for soft blue atmospheric glow.
- 2× `<filter>` using blur/shadow for neon chart emphasis and elevated panels.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#4A5568"/>
      <stop offset="48%" stop-color="#2D3748"/>
      <stop offset="100%" stop-color="#1A202C"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#243247" stop-opacity="0.74"/>
      <stop offset="100%" stop-color="#111827" stop-opacity="0.52"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2B6CB0"/>
      <stop offset="55%" stop-color="#4299E1"/>
      <stop offset="100%" stop-color="#90CDF4"/>
    </linearGradient>
    <linearGradient id="areaGrad" x1="0" y1="520" x2="0" y2="675">
      <stop offset="0%" stop-color="#4299E1" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#4299E1" stop-opacity="0.02"/>
    </linearGradient>
    <radialGradient id="halo" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#4299E1" stop-opacity="0.28"/>
      <stop offset="70%" stop-color="#4299E1" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#4299E1" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="blueGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="760" cy="345" rx="470" ry="285" fill="url(#halo)"/>
  <path d="M40 645 C190 565 310 705 455 625 C610 540 735 595 855 520 C1005 425 1110 495 1240 405"
        fill="none" stroke="#63B3ED" stroke-opacity="0.13" stroke-width="28" filter="url(#blueGlow)"/>

  <text x="50" y="55" width="1180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" letter-spacing="3" fill="#FFFFFF">GLOBAL PERFORMANCE DASHBOARD</text>
  <text x="50" y="82" width="1180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="1.5" fill="#A0AEC0">Q2 EXECUTIVE SUMMARY · LIVE METRICS SNAPSHOT</text>

  <rect x="50" y="110" width="380" height="390" rx="18" fill="url(#panelGrad)" stroke="#4299E1" stroke-opacity="0.65" filter="url(#softShadow)"/>
  <rect x="460" y="110" width="230" height="140" rx="18" fill="url(#panelGrad)" stroke="#4299E1" stroke-opacity="0.55"/>
  <rect x="715" y="110" width="230" height="140" rx="18" fill="url(#panelGrad)" stroke="#4299E1" stroke-opacity="0.55"/>
  <rect x="970" y="110" width="260" height="140" rx="18" fill="url(#panelGrad)" stroke="#4299E1" stroke-opacity="0.55"/>
  <rect x="460" y="275" width="360" height="225" rx="18" fill="url(#panelGrad)" stroke="#4299E1" stroke-opacity="0.55"/>
  <rect x="850" y="275" width="380" height="225" rx="18" fill="url(#panelGrad)" stroke="#4299E1" stroke-opacity="0.55"/>
  <rect x="50" y="530" width="1180" height="155" rx="18" fill="url(#panelGrad)" stroke="#4299E1" stroke-opacity="0.65" filter="url(#softShadow)"/>

  <text x="80" y="145" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#A0AEC0">MONTHLY ACQUISITION VOLUME</text>
  <line x1="145" y1="175" x2="145" y2="455" stroke="#718096" stroke-opacity="0.35"/>
  <line x1="145" y1="455" x2="390" y2="455" stroke="#718096" stroke-opacity="0.35"/>
  <text x="82" y="203" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E0">Jan</text>
  <text x="82" y="253" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E0">Feb</text>
  <text x="82" y="303" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E0">Mar</text>
  <text x="82" y="353" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E0">Apr</text>
  <text x="82" y="403" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E0">May</text>
  <rect x="145" y="185" width="72" height="24" rx="5" fill="#2B6CB0"/>
  <rect x="145" y="235" width="112" height="24" rx="5" fill="#3182CE"/>
  <rect x="145" y="285" width="196" height="24" rx="5" fill="url(#blueGrad)" filter="url(#blueGlow)"/>
  <rect x="145" y="335" width="244" height="24" rx="5" fill="url(#blueGrad)" filter="url(#blueGlow)"/>
  <rect x="145" y="385" width="210" height="24" rx="5" fill="#63B3ED"/>
  <text x="222" y="203" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#FFFFFF">0.98M</text>
  <text x="262" y="253" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#FFFFFF">1.24M</text>
  <text x="346" y="303" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#FFFFFF">2.05M</text>
  <text x="394" y="353" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#FFFFFF">2.61M</text>
  <text x="360" y="403" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#FFFFFF">2.31M</text>

  <text x="485" y="140" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A0AEC0">TOTAL REVENUE</text>
  <text x="485" y="198" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FFFFFF">$48.7M</text>
  <rect x="485" y="218" width="130" height="8" rx="4" fill="#2B6CB0"/>
  <rect x="485" y="218" width="96" height="8" rx="4" fill="#63B3ED"/>
  <text x="620" y="226" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#68D391">+18%</text>

  <text x="740" y="140" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A0AEC0">ACTIVE USERS</text>
  <text x="740" y="198" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FFFFFF">1.82M</text>
  <circle cx="905" cy="184" r="26" fill="#1A365D" stroke="#63B3ED" stroke-width="5"/>
  <text x="879" y="190" width="52" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">92%</text>

  <text x="995" y="140" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A0AEC0">MONTHLY DATA</text>
  <rect x="995" y="158" width="70" height="28" rx="14" fill="#4299E1"/>
  <rect x="1075" y="158" width="70" height="28" rx="14" fill="#1A202C" stroke="#4299E1" stroke-opacity="0.55"/>
  <rect x="1155" y="158" width="50" height="28" rx="14" fill="#1A202C" stroke="#4299E1" stroke-opacity="0.55"/>
  <text x="1017" y="177" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">APR</text>
  <text x="1097" y="177" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A0AEC0">MAY</text>
  <text x="1172" y="177" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A0AEC0">JUN</text>
  <text x="995" y="225" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">North America</text>

  <text x="485" y="305" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#A0AEC0">CHANNEL MIX</text>
  <circle cx="640" cy="390" r="68" fill="none" stroke="#EDF2F7" stroke-opacity="0.18" stroke-width="26"/>
  <circle cx="640" cy="390" r="68" fill="none" stroke="#63B3ED" stroke-width="26" stroke-dasharray="190 427" transform="rotate(-90 640 390)" filter="url(#blueGlow)"/>
  <circle cx="640" cy="390" r="68" fill="none" stroke="#4299E1" stroke-width="26" stroke-dasharray="120 497" transform="rotate(23 640 390)"/>
  <circle cx="640" cy="390" r="68" fill="none" stroke="#2B6CB0" stroke-width="26" stroke-dasharray="82 535" transform="rotate(125 640 390)"/>
  <text x="593" y="397" width="94" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">67%</text>
  <circle cx="733" cy="350" r="5" fill="#63B3ED"/><text x="746" y="355" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#CBD5E0">Direct</text>
  <circle cx="733" cy="377" r="5" fill="#4299E1"/><text x="746" y="382" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#CBD5E0">Paid</text>
  <circle cx="733" cy="404" r="5" fill="#2B6CB0"/><text x="746" y="409" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#CBD5E0">Organic</text>

  <text x="875" y="305" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#A0AEC0">TARGET ATTAINMENT</text>
  <path d="M925 420 A110 110 0 0 1 1155 420" fill="none" stroke="#EDF2F7" stroke-opacity="0.18" stroke-width="28" stroke-linecap="round"/>
  <path d="M925 420 A110 110 0 0 1 1118 342" fill="none" stroke="url(#blueGrad)" stroke-width="28" stroke-linecap="round" filter="url(#blueGlow)"/>
  <text x="982" y="418" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">84%</text>
  <text x="957" y="450" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A0AEC0">annual goal completion</text>

  <text x="80" y="560" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#A0AEC0">RETENTION TREND</text>
  <line x1="85" y1="650" x2="1195" y2="650" stroke="#718096" stroke-opacity="0.35"/>
  <line x1="85" y1="610" x2="1195" y2="610" stroke="#718096" stroke-opacity="0.18"/>
  <line x1="85" y1="570" x2="1195" y2="570" stroke="#718096" stroke-opacity="0.18"/>
  <path d="M95 650 L95 625 C180 618 245 632 330 600 C420 568 490 590 585 575 C690 558 745 610 835 582 C930 552 1005 570 1090 540 C1145 522 1185 535 1195 530 L1195 650 Z" fill="url(#areaGrad)"/>
  <path d="M95 625 C180 618 245 632 330 600 C420 568 490 590 585 575 C690 558 745 610 835 582 C930 552 1005 570 1090 540 C1145 522 1185 535 1195 530"
        fill="none" stroke="#63B3ED" stroke-width="5" stroke-linecap="round" filter="url(#blueGlow)"/>
  <circle cx="330" cy="600" r="5" fill="#FFFFFF" stroke="#63B3ED" stroke-width="3"/>
  <circle cx="585" cy="575" r="5" fill="#FFFFFF" stroke="#63B3ED" stroke-width="3"/>
  <circle cx="835" cy="582" r="5" fill="#FFFFFF" stroke="#63B3ED" stroke-width="3"/>
  <circle cx="1090" cy="540" r="5" fill="#FFFFFF" stroke="#63B3ED" stroke-width="3"/>
  <text x="88" y="672" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A0AEC0">Jan</text>
  <text x="315" y="672" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A0AEC0">Mar</text>
  <text x="570" y="672" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A0AEC0">May</text>
  <text x="820" y="672" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A0AEC0">Jul</text>
  <text x="1075" y="672" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A0AEC0">Sep</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use native SVG `<mask>` to fade charts or panels; use gradients and opacity instead.
- ❌ Do not place chart labels without explicit `width` attributes; dashboard text will otherwise clip unpredictably in PowerPoint.
- ❌ Do not apply filters to `<line>` gridlines; use filters only on panels, paths, circles, or text.
- ❌ Do not rely on real chart objects or embedded HTML; build charts from editable SVG bars, paths, circles, and text.
- ❌ Do not overfill every panel—dark dashboards need negative space so glowing blue data remains legible.

## Composition notes
- Keep the title/header shallow, then devote most of the slide to a strict modular grid: one dominant chart column, three KPI cards, two mid-sized analytic panels, and one full-width trend panel.
- Use bright blue sparingly for data marks and borders; reserve white for the most important numbers only.
- Let the background remain visibly dark between panels to create separation without heavy dividers.
- Use glow on only the hero data series or active value, not every element, to preserve a premium executive-dashboard feel.