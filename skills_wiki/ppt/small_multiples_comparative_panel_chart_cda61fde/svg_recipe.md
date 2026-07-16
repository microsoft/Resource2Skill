# SVG Recipe — Small Multiples Panel Chart

## Visual mechanism
A shared category list anchors a grid of aligned horizontal mini bar charts, with each column representing a different KPI. Consistent row spacing, panel widths, and value labeling let viewers scan across products or down metrics without decoding a complex multi-series chart.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 1× large rounded `<rect>` for the main chart card
- 3× rounded `<rect>` panel containers for the individual metric columns
- 15× pale `<rect>` bar tracks for consistent scale reference
- 15× colored rounded `<rect>` bars for KPI values
- 15× `<text>` value labels placed inside or just after bars
- 5× `<text>` category labels forming the shared Y-axis
- 3× `<text>` panel titles plus 3× metric subtitles
- 1× `<path>` decorative background ribbon for executive-style depth
- 3× `<linearGradient>` fills for KPI bars
- 1× `<filter id="cardShadow">` for the elevated chart card
- 1× `<filter id="softGlow">` for subtle accent emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7faff"/>
      <stop offset="100%" stop-color="#eef3f8"/>
    </linearGradient>
    <linearGradient id="barA" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#213246"/>
      <stop offset="100%" stop-color="#3f5772"/>
    </linearGradient>
    <linearGradient id="barB" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1b8fd6"/>
      <stop offset="100%" stop-color="#5cbdf2"/>
    </linearGradient>
    <linearGradient id="barC" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7f9297"/>
      <stop offset="100%" stop-color="#b7c4c7"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M905,0 C1030,52 1120,130 1280,96 L1280,0 Z" fill="#dceeff" opacity="0.85"/>
  <path d="M0,640 C170,590 265,710 430,665 C555,632 610,560 735,590 C850,618 932,710 1085,690 C1168,680 1220,642 1280,650 L1280,720 L0,720 Z" fill="#e7eef7" opacity="0.7"/>

  <text x="72" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#004080">
    Small Multiples — Product KPI Comparison
  </text>
  <text x="74" y="92" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#607080">
    Scan each row to compare one product across metrics; scan each column to identify KPI leaders.
  </text>

  <rect x="60" y="130" width="1160" height="500" rx="28" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="60" y="130" width="8" height="500" rx="4" fill="#3498db"/>

  <text x="95" y="176" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8a97a3" letter-spacing="1">
    PRODUCT
  </text>

  <rect x="270" y="160" width="255" height="415" rx="20" fill="#fbfcfe" stroke="#e6edf5"/>
  <rect x="570" y="160" width="255" height="415" rx="20" fill="#fbfcfe" stroke="#e6edf5"/>
  <rect x="870" y="160" width="255" height="415" rx="20" fill="#fbfcfe" stroke="#e6edf5"/>

  <rect x="292" y="184" width="70" height="5" rx="2.5" fill="url(#barA)"/>
  <rect x="592" y="184" width="70" height="5" rx="2.5" fill="url(#barB)"/>
  <rect x="892" y="184" width="70" height="5" rx="2.5" fill="url(#barC)"/>

  <text x="292" y="216" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2d3e50">Parameter A</text>
  <text x="592" y="216" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2d3e50">Parameter B</text>
  <text x="892" y="216" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2d3e50">Parameter C</text>
  <text x="292" y="238" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7b8793">Awareness lift</text>
  <text x="592" y="238" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7b8793">Conversion efficiency</text>
  <text x="892" y="238" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7b8793">Retention strength</text>

  <text x="95" y="277" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#333333">Product 1</text>
  <text x="95" y="332" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#333333">Product 2</text>
  <text x="95" y="387" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#333333">Product 3</text>
  <text x="95" y="442" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#333333">Product 4</text>
  <text x="95" y="497" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#333333">Product 5</text>

  <rect x="292" y="258" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="292" y="258" width="105" height="22" rx="11" fill="url(#barA)"/><text x="354" y="275" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">35%</text>
  <rect x="292" y="313" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="292" y="313" width="171" height="22" rx="11" fill="url(#barA)"/><text x="425" y="330" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">57%</text>
  <rect x="292" y="368" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="292" y="368" width="51" height="22" rx="11" fill="url(#barA)"/><text x="350" y="385" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#2d3e50">17%</text>
  <rect x="292" y="423" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="292" y="423" width="78" height="22" rx="11" fill="url(#barA)"/><text x="329" y="440" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">26%</text>
  <rect x="292" y="478" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="292" y="478" width="135" height="22" rx="11" fill="url(#barA)"/><text x="389" y="495" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">45%</text>

  <rect x="592" y="258" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="592" y="258" width="195" height="22" rx="11" fill="url(#barB)" filter="url(#softGlow)"/><text x="748" y="275" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">65%</text>
  <rect x="592" y="313" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="592" y="313" width="87" height="22" rx="11" fill="url(#barB)"/><text x="636" y="330" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">29%</text>
  <rect x="592" y="368" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="592" y="368" width="126" height="22" rx="11" fill="url(#barB)"/><text x="679" y="385" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">42%</text>
  <rect x="592" y="423" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="592" y="423" width="36" height="22" rx="11" fill="url(#barB)"/><text x="635" y="440" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#2d3e50">12%</text>
  <rect x="592" y="478" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="592" y="478" width="96" height="22" rx="11" fill="url(#barB)"/><text x="649" y="495" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">32%</text>

  <rect x="892" y="258" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="892" y="258" width="69" height="22" rx="11" fill="url(#barC)"/><text x="922" y="275" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">23%</text>
  <rect x="892" y="313" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="892" y="313" width="111" height="22" rx="11" fill="url(#barC)"/><text x="964" y="330" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">37%</text>
  <rect x="892" y="368" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="892" y="368" width="54" height="22" rx="11" fill="url(#barC)"/><text x="952" y="385" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#2d3e50">18%</text>
  <rect x="892" y="423" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="892" y="423" width="60" height="22" rx="11" fill="url(#barC)"/><text x="919" y="440" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">20%</text>
  <rect x="892" y="478" width="210" height="22" rx="11" fill="#edf2f6"/><rect x="892" y="478" width="36" height="22" rx="11" fill="url(#barC)"/><text x="936" y="495" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#2d3e50">12%</text>

  <rect x="92" y="548" width="995" height="1" fill="#e4ebf2"/>
  <text x="95" y="584" width="920" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#536170">
    Insight: Product 2 leads in awareness, while Product 1 has the strongest conversion profile; retention remains comparatively compressed across the portfolio.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Independent Y-axis labels inside every panel; they break row scanning and waste space.
- ❌ Unequal panel widths or inconsistent bar scales; the viewer must be able to compare lengths across columns.
- ❌ Axis-heavy chart styling with tick marks, dense gridlines, and borders; small multiples work best when the repeated structure is clean.
- ❌ Using a raster chart screenshot; build bars, labels, and panels as SVG shapes so PowerPoint users can edit every value and color.
- ❌ Placing value labels far outside the bars unless the bars are too short; direct bar-end labeling is faster to read.

## Composition notes
- Reserve the left 18–22% of the chart card for shared category labels; all bar rows must align precisely to those labels.
- Use a common baseline and maximum track width across all panels so bar length remains meaningful.
- Give each metric a distinct but related color; repeat that color in the panel title accent to connect label and data.
- Keep generous whitespace between panels so the grid reads as separate mini charts, not one crowded grouped chart.