# SVG Recipe — Dark Mode High-Contrast Business Aesthetic (Cyber-Corporate Style)

## Visual mechanism
A deep charcoal/black gradient canvas is punctuated by cyber-yellow highlights, creating a premium dark-mode executive dashboard. Data is organized into low-contrast rounded cards, while the most important KPIs and chart signals glow in a single saturated accent color.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark gradient background
- 2× blurred `<ellipse>` elements for atmospheric radial glow spots
- 6× `<rect>` for rounded dashboard cards and accent bars
- 8× `<rect>` for chart bars and KPI micro-progress bars
- 3× `<path>` for decorative cyber-circuit traces, an area chart fill, and a glowing trend line
- 12× `<line>` for chart axes, gridlines, and subtle dividers
- 18× `<text>` elements for title, subtitle, KPI labels, KPI values, axis labels, and callouts
- 2× `<linearGradient>` fills for background and surface cards
- 1× `<linearGradient>` for cyber-yellow bar emphasis
- 1× `<radialGradient>` for ambient glow coloration
- 1× `<filter id="shadow">` applied to card rectangles
- 1× `<filter id="yellowGlow">` applied to yellow accent shapes and trend path

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#2c2c32"/>
      <stop offset="55%" stop-color="#151519"/>
      <stop offset="100%" stop-color="#08080a"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#242428"/>
      <stop offset="100%" stop-color="#18181b"/>
    </linearGradient>

    <linearGradient id="yellowGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffcc00"/>
      <stop offset="100%" stop-color="#ffe680"/>
    </linearGradient>

    <radialGradient id="ambientYellow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffcc00" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#ffcc00" stop-opacity="0"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="yellowGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="1080" cy="95" rx="260" ry="120" fill="url(#ambientYellow)" opacity="0.35" filter="url(#yellowGlow)"/>
  <ellipse cx="210" cy="670" rx="360" ry="150" fill="#2b2b38" opacity="0.45" filter="url(#shadow)"/>

  <path d="M930 44 L1090 44 L1120 74 L1225 74" fill="none" stroke="#ffcc00" stroke-width="2" opacity="0.45" stroke-dasharray="10 10"/>
  <path d="M68 642 L190 642 L226 606 L330 606" fill="none" stroke="#777777" stroke-width="1.5" opacity="0.28" stroke-dasharray="6 8"/>

  <text x="76" y="72" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#ffffff">战略总览与分析</text>
  <text x="78" y="108" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#a7a7a7">Strategic Overview · Cyber-Corporate Performance Dashboard</text>
  <rect x="78" y="134" width="76" height="8" rx="4" fill="#ffcc00" filter="url(#yellowGlow)"/>
  <text x="1042" y="74" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#d0d0d0" text-anchor="end">FY2026 Q2</text>
  <text x="1042" y="100" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#ffcc00" text-anchor="end">LIVE OPS</text>

  <rect x="78" y="182" width="260" height="150" rx="22" fill="url(#cardGrad)" stroke="#3d3d44" stroke-width="1" filter="url(#shadow)"/>
  <text x="104" y="222" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9b9b9b">ARR Growth</text>
  <text x="104" y="274" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#ffcc00">+42%</text>
  <rect x="104" y="300" width="186" height="8" rx="4" fill="#333338"/>
  <rect x="104" y="300" width="142" height="8" rx="4" fill="url(#yellowGrad)" filter="url(#yellowGlow)"/>

  <rect x="366" y="182" width="260" height="150" rx="22" fill="url(#cardGrad)" stroke="#3d3d44" stroke-width="1" filter="url(#shadow)"/>
  <text x="392" y="222" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9b9b9b">Net Retention</text>
  <text x="392" y="274" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#ffffff">118%</text>
  <rect x="392" y="300" width="186" height="8" rx="4" fill="#333338"/>
  <rect x="392" y="300" width="162" height="8" rx="4" fill="#f2f2f2"/>

  <rect x="654" y="182" width="260" height="150" rx="22" fill="url(#cardGrad)" stroke="#3d3d44" stroke-width="1" filter="url(#shadow)"/>
  <text x="680" y="222" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9b9b9b">Pipeline Coverage</text>
  <text x="680" y="274" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#ffffff">3.6×</text>
  <rect x="680" y="300" width="186" height="8" rx="4" fill="#333338"/>
  <rect x="680" y="300" width="126" height="8" rx="4" fill="#a8a8a8"/>

  <rect x="942" y="182" width="260" height="150" rx="22" fill="#ffcc00" opacity="0.96" filter="url(#shadow)"/>
  <text x="968" y="222" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#171717">Critical Signal</text>
  <text x="968" y="274" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#0b0b0b">91</text>
  <text x="1040" y="274" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#0b0b0b">NPS</text>
  <text x="968" y="306" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#2b2b2b">Highest enterprise segment score</text>

  <rect x="78" y="374" width="790" height="276" rx="26" fill="url(#cardGrad)" stroke="#3d3d44" stroke-width="1" filter="url(#shadow)"/>
  <text x="108" y="420" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#ffffff">Regional Revenue Momentum</text>
  <text x="108" y="446" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8e8e8e">Quarterly indexed growth, normalized to Q1 baseline</text>

  <line x1="136" y1="588" x2="812" y2="588" stroke="#4a4a50" stroke-width="1"/>
  <line x1="136" y1="532" x2="812" y2="532" stroke="#34343a" stroke-width="1"/>
  <line x1="136" y1="476" x2="812" y2="476" stroke="#34343a" stroke-width="1"/>
  <line x1="136" y1="420" x2="812" y2="420" stroke="#34343a" stroke-width="1"/>
  <line x1="136" y1="452" x2="812" y2="452" stroke="#ffcc00" stroke-width="1" stroke-dasharray="8 8" opacity="0.55"/>

  <rect x="176" y="520" width="56" height="68" rx="8" fill="#5b5b62"/>
  <rect x="276" y="486" width="56" height="102" rx="8" fill="#777780"/>
  <rect x="376" y="458" width="56" height="130" rx="8" fill="#99999f"/>
  <rect x="476" y="432" width="56" height="156" rx="8" fill="url(#yellowGrad)" filter="url(#yellowGlow)"/>
  <rect x="576" y="466" width="56" height="122" rx="8" fill="#777780"/>
  <rect x="676" y="406" width="56" height="182" rx="8" fill="url(#yellowGrad)" filter="url(#yellowGlow)"/>

  <text x="184" y="620" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9b9b9b">Q1</text>
  <text x="284" y="620" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9b9b9b">Q2</text>
  <text x="384" y="620" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9b9b9b">Q3</text>
  <text x="484" y="620" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffcc00">Q4</text>
  <text x="584" y="620" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9b9b9b">Q5</text>
  <text x="684" y="620" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffcc00">Q6</text>

  <rect x="910" y="374" width="292" height="276" rx="26" fill="url(#cardGrad)" stroke="#3d3d44" stroke-width="1" filter="url(#shadow)"/>
  <text x="940" y="420" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#ffffff">Executive Signal</text>
  <text x="940" y="446" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8e8e8e">Leading indicator composite</text>

  <path d="M942 585 C982 548, 1002 570, 1036 524 C1070 478, 1095 506, 1132 444 C1152 410, 1172 402, 1190 390 L1190 608 L942 608 Z" fill="#ffcc00" opacity="0.12"/>
  <path d="M942 585 C982 548, 1002 570, 1036 524 C1070 478, 1095 506, 1132 444 C1152 410, 1172 402, 1190 390" fill="none" stroke="#ffcc00" stroke-width="4" stroke-linecap="round" filter="url(#yellowGlow)"/>
  <circle cx="1190" cy="390" r="7" fill="#ffcc00" filter="url(#yellowGlow)"/>
  <line x1="940" y1="608" x2="1190" y2="608" stroke="#4a4a50" stroke-width="1"/>
  <line x1="940" y1="520" x2="1190" y2="520" stroke="#34343a" stroke-width="1"/>
  <line x1="940" y1="432" x2="1190" y2="432" stroke="#34343a" stroke-width="1"/>
  <text x="940" y="635" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9b9b9b">Signal strength rising above target band</text>
</svg>
```

## Avoid in this skill
- ❌ Heavy white chart grids; they destroy the premium dark-mode hierarchy.
- ❌ Multiple saturated accent colors; the cyber-corporate effect depends on one disciplined luminous color.
- ❌ Low-contrast dark text on dark cards; keep secondary text grey and primary text white/yellow.
- ❌ Using bitmap screenshots for charts when editable SVG bars, lines, and labels can reproduce the dashboard cleanly.
- ❌ Applying filters to `<line>` elements; use glow on nearby paths, circles, or rectangles instead.

## Composition notes
- Keep the slide background dark and mostly empty; visual energy should come from the yellow highlights, not from dense decoration.
- Use a strict modular grid: KPI cards across the top, primary chart lower-left, secondary signal card lower-right.
- Reserve cyber yellow for the active KPI, key bars, target lines, and endpoint markers.
- Make cards subtly visible with dark gradients, thin borders, and shadows; avoid bright card fills except for a single hero KPI.