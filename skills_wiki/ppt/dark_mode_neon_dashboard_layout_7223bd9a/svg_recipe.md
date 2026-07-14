# SVG Recipe — Dark Mode Neon Dashboard Layout

## Visual mechanism
A near-black executive dashboard canvas is organized into a disciplined card grid, then energized with cyan/magenta/purple neon chart strokes, glowing KPI accents, and restrained gray supporting text. The effect comes from strong contrast, repeated rounded containers, sparse chart furniture, and selective glow only on data marks.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark navy background.
- 8× `<rect>` for rounded dashboard cards and elevated chart panels.
- 14× `<rect>` for neon bar chart columns, KPI progress strips, dividers, and small UI chips.
- 3× `<ellipse>` for soft ambient neon glows behind the dashboard.
- 6× `<path>` for glowing line charts, area fills, decorative trend sparks, and circular gauge arcs.
- 3× `<circle>` for KPI/gauge dots and progress-ring anchors.
- 2× `<line>` for subtle chart baseline/reference guides without filters.
- 24× `<text>` for dashboard title, KPI labels, KPI values, chart labels, axis hints, and callouts; every text element requires `width`.
- 3× `<linearGradient>` for card elevations, neon strokes, and bar fills.
- 1× `<radialGradient>` for the ambient background glow.
- 2× `<filter>`: one shadow filter for cards and one blur glow filter for neon data paths/ellipses.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#202941"/>
      <stop offset="100%" stop-color="#121827"/>
    </linearGradient>
    <linearGradient id="cyanMagenta" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00FFFF"/>
      <stop offset="55%" stop-color="#8A5CFF"/>
      <stop offset="100%" stop-color="#FF1493"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#23304A"/>
      <stop offset="45%" stop-color="#00D5FF"/>
      <stop offset="100%" stop-color="#FF1493"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00FFFF" stop-opacity="0.35"/>
      <stop offset="65%" stop-color="#8A5CFF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#0D111C" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="neonGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#0D111C"/>
  <ellipse cx="1040" cy="100" rx="250" ry="130" fill="url(#ambientGlow)" filter="url(#neonGlow)" opacity="0.65"/>
  <ellipse cx="180" cy="660" rx="300" ry="145" fill="#FF1493" filter="url(#neonGlow)" opacity="0.10"/>
  <ellipse cx="680" cy="370" rx="420" ry="210" fill="#6F45FF" filter="url(#neonGlow)" opacity="0.08"/>

  <text x="56" y="58" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#FFFFFF">PERFORMANCE COMMAND CENTER</text>
  <text x="58" y="84" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="2.5" fill="#00FFFF">Q3 METRICS · LIVE NEON DATA VIEW</text>
  <rect x="1040" y="42" width="170" height="34" rx="17" fill="#182238" stroke="#33415F"/>
  <circle cx="1062" cy="59" r="5" fill="#00FFFF" filter="url(#neonGlow)"/>
  <text x="1076" y="64" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#C8D4EA">SYNCED 02:14</text>

  <rect x="56" y="116" width="360" height="128" rx="22" fill="url(#cardGrad)" stroke="#43506C" filter="url(#softShadow)"/>
  <rect x="460" y="116" width="360" height="128" rx="22" fill="url(#cardGrad)" stroke="#43506C" filter="url(#softShadow)"/>
  <rect x="864" y="116" width="360" height="128" rx="22" fill="url(#cardGrad)" stroke="#43506C" filter="url(#softShadow)"/>

  <text x="84" y="150" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="2" fill="#9EAABC">TOTAL REVENUE</text>
  <text x="84" y="198" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">$1.24M</text>
  <text x="286" y="196" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#00FFFF">+14.2%</text>
  <path d="M86 222 C125 204,150 232,187 211 S251 210,292 190 S340 190,386 164" fill="none" stroke="#00FFFF" stroke-width="4" stroke-linecap="round" filter="url(#neonGlow)"/>

  <text x="488" y="150" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="2" fill="#9EAABC">ACTIVE USERS</text>
  <text x="488" y="198" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">84,592</text>
  <text x="692" y="196" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#B78CFF">+5.8%</text>
  <rect x="490" y="220" width="278" height="8" rx="4" fill="#26334F"/>
  <rect x="490" y="220" width="218" height="8" rx="4" fill="url(#cyanMagenta)" filter="url(#neonGlow)"/>

  <text x="892" y="150" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="2" fill="#9EAABC">DEFECT RATE</text>
  <text x="892" y="198" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">1.2%</text>
  <text x="1060" y="196" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#00FFFF">-2.0%</text>
  <path d="M896 224 C928 198,960 202,990 187 C1032 166,1071 193,1110 156 C1134 134,1160 140,1192 124" fill="none" stroke="#FF1493" stroke-width="4" stroke-linecap="round" filter="url(#neonGlow)"/>

  <rect x="56" y="280" width="740" height="366" rx="26" fill="url(#cardGrad)" stroke="#43506C" filter="url(#softShadow)"/>
  <text x="88" y="322" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="750" fill="#FFFFFF">Revenue Velocity</text>
  <text x="88" y="346" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EAABC">Minimal axes, high-emphasis neon trend line, area fill for momentum.</text>
  <rect x="654" y="305" width="106" height="28" rx="14" fill="#162238" stroke="#2F3D5A"/>
  <text x="676" y="324" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#00FFFF">MONTHLY</text>
  <line x1="92" y1="570" x2="748" y2="570" stroke="#34405C" stroke-width="1"/>
  <line x1="92" y1="438" x2="748" y2="438" stroke="#26324D" stroke-width="1" stroke-dasharray="7 10"/>
  <path d="M96 558 C148 520,177 541,230 484 C285 425,325 455,379 406 C431 358,486 397,540 345 C598 289,657 338,748 292 L748 570 L96 570 Z" fill="#00FFFF" opacity="0.10"/>
  <path d="M96 558 C148 520,177 541,230 484 C285 425,325 455,379 406 C431 358,486 397,540 345 C598 289,657 338,748 292" fill="none" stroke="url(#cyanMagenta)" stroke-width="6" stroke-linecap="round" filter="url(#neonGlow)"/>
  <circle cx="748" cy="292" r="8" fill="#FF1493" filter="url(#neonGlow)"/>
  <text x="650" y="278" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Peak $420K</text>
  <text x="94" y="606" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F8BA3">JAN</text>
  <text x="306" y="606" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F8BA3">APR</text>
  <text x="520" y="606" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F8BA3">JUL</text>
  <text x="704" y="606" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F8BA3">SEP</text>

  <rect x="834" y="280" width="390" height="170" rx="26" fill="url(#cardGrad)" stroke="#43506C" filter="url(#softShadow)"/>
  <text x="866" y="322" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="750" fill="#FFFFFF">Channel Mix</text>
  <rect x="870" y="394" width="22" height="28" rx="5" fill="url(#barGrad)" opacity="0.8"/>
  <rect x="906" y="364" width="22" height="58" rx="5" fill="url(#barGrad)" opacity="0.9"/>
  <rect x="942" y="336" width="22" height="86" rx="5" fill="url(#barGrad)"/>
  <rect x="978" y="378" width="22" height="44" rx="5" fill="url(#barGrad)" opacity="0.85"/>
  <rect x="1014" y="322" width="22" height="100" rx="5" fill="url(#barGrad)"/>
  <rect x="1050" y="348" width="22" height="74" rx="5" fill="url(#barGrad)" opacity="0.95"/>
  <rect x="1086" y="304" width="22" height="118" rx="5" fill="url(#barGrad)" filter="url(#neonGlow)"/>
  <rect x="1122" y="372" width="22" height="50" rx="5" fill="url(#barGrad)" opacity="0.85"/>
  <line x1="864" y1="422" x2="1170" y2="422" stroke="#34405C" stroke-width="1"/>
  <text x="866" y="352" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EAABC">Paid search</text>
  <text x="1068" y="352" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#00FFFF">+22% lift</text>

  <rect x="834" y="476" width="390" height="170" rx="26" fill="url(#cardGrad)" stroke="#43506C" filter="url(#softShadow)"/>
  <text x="866" y="518" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="750" fill="#FFFFFF">System Health</text>
  <circle cx="926" cy="584" r="45" fill="none" stroke="#26334F" stroke-width="16"/>
  <path d="M926 539 A45 45 0 1 1 889 610" fill="none" stroke="#00FFFF" stroke-width="16" stroke-linecap="round" filter="url(#neonGlow)"/>
  <text x="898" y="593" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#FFFFFF">87</text>
  <text x="990" y="570" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9EAABC">Latency stable</text>
  <text x="990" y="598" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9EAABC">Error budget: 64%</text>
  <rect x="990" y="616" width="170" height="8" rx="4" fill="#26334F"/>
  <rect x="990" y="616" width="109" height="8" rx="4" fill="#FF1493" filter="url(#neonGlow)"/>
</svg>
```

## Avoid in this skill
- ❌ Dense spreadsheet-like gridlines, heavy axes, legends, or table borders; they fight the premium dark-mode hierarchy.
- ❌ Applying glow filters to `<line>` elements; use glowing `<path>` strokes for chart curves and keep `<line>` for plain baselines only.
- ❌ Using `marker-end` arrowheads for trend annotations; if arrows are needed, draw them manually with simple lines/paths.
- ❌ Putting `clip-path` or masks on cards, paths, or text; clipping should only be used on `<image>` elements when adding avatars/screenshots.
- ❌ Too many neon colors at equal strength; reserve the brightest cyan/magenta for the data marks and final values.

## Composition notes
- Keep a 50–60 px outer margin and 28–40 px gutters between cards so the dark canvas feels intentional, not empty.
- Put the strongest hierarchy in the top KPI row: large white values, small gray labels, and one neon micro-chart or progress strip per card.
- Use one dominant chart card occupying roughly 55–60% of the slide width, balanced by two smaller insight cards on the right.
- Let glow live behind data, not behind every container; cards should feel elevated through subtle shadows and borders, while chart strokes provide the neon energy.