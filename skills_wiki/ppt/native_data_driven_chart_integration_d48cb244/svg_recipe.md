# SVG Recipe — Native Data-Driven Chart Integration

## Visual mechanism
Convert a small category/series table into a polished clustered column chart by mapping each numeric value to proportional editable bar geometry. The chart sits in a premium “data card” with gridlines, axis labels, legend, and a takeaway annotation so the slide reads like an executive performance review rather than a raw dashboard.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<path>` for a soft decorative background wave
- 2× `<rect>` for the chart card and right-side insight card
- 6× `<line>` for horizontal value gridlines
- 1× `<line>` for the x-axis baseline
- 12× `<path>` for rounded-top clustered column bars generated from data values
- 18× `<text>` for title, subtitle, axis labels, category labels, legend labels, data callout, and KPI notes
- 3× `<circle>` for legend color keys
- 3× `<linearGradient>` for series fills
- 1× `<radialGradient>` for ambient background glow
- 1× `<filter id="cardShadow">` applied to cards
- 1× `<filter id="barGlow">` applied to highlighted bars/callout shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="24%" cy="12%" r="80%">
      <stop offset="0%" stop-color="#EEF5FF"/>
      <stop offset="58%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#E9EEF6"/>
    </radialGradient>

    <linearGradient id="s1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6EA8FF"/>
      <stop offset="100%" stop-color="#3F72C8"/>
    </linearGradient>
    <linearGradient id="s2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFB26B"/>
      <stop offset="100%" stop-color="#ED7D31"/>
    </linearGradient>
    <linearGradient id="s3" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8EDC88"/>
      <stop offset="100%" stop-color="#70AD47"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="barGlow" x="-30%" y="-30%" width="160%" height="170%">
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <path d="M0,92 C210,36 340,118 520,78 C725,32 880,-18 1280,44 L1280,0 L0,0 Z" fill="#DCEBFF" opacity="0.72"/>

  <text x="78" y="70" width="670" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#162033">Quarterly Revenue by Segment</text>
  <text x="80" y="104" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#65748B">Clustered columns translated from a 4-category × 3-series data table; every bar remains editable as native PowerPoint geometry.</text>

  <rect x="70" y="132" width="900" height="510" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="1000" y="132" width="220" height="510" rx="28" fill="#172033" filter="url(#cardShadow)"/>

  <text x="122" y="172" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#1F2A3D">Native clustered column model</text>
  <text x="122" y="199" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7C889A">Values plotted on a 0–5 scale, with grouped bars preserving series order.</text>

  <line x1="170" y1="175" x2="900" y2="175" stroke="#DCE3EE" stroke-width="1"/>
  <line x1="170" y1="247" x2="900" y2="247" stroke="#DCE3EE" stroke-width="1"/>
  <line x1="170" y1="319" x2="900" y2="319" stroke="#DCE3EE" stroke-width="1"/>
  <line x1="170" y1="391" x2="900" y2="391" stroke="#DCE3EE" stroke-width="1"/>
  <line x1="170" y1="463" x2="900" y2="463" stroke="#DCE3EE" stroke-width="1"/>
  <line x1="170" y1="535" x2="900" y2="535" stroke="#9AA7B8" stroke-width="1.4"/>

  <text x="132" y="181" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8798">5</text>
  <text x="132" y="253" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8798">4</text>
  <text x="132" y="325" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8798">3</text>
  <text x="132" y="397" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8798">2</text>
  <text x="132" y="469" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8798">1</text>
  <text x="132" y="541" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8798">0</text>

  <path d="M236,535 L236,233.4 Q236,225.4 244,225.4 L250,225.4 Q258,225.4 258,233.4 L258,535 Z" fill="url(#s1)"/>
  <path d="M266,535 L266,370.2 Q266,362.2 274,362.2 L280,362.2 Q288,362.2 288,370.2 L288,535 Z" fill="url(#s2)"/>
  <path d="M296,535 L296,399 Q296,391 304,391 L310,391 Q318,391 318,399 L318,535 Z" fill="url(#s3)"/>

  <path d="M416,535 L416,363 Q416,355 424,355 L430,355 Q438,355 438,363 L438,535 Z" fill="url(#s1)"/>
  <path d="M446,535 L446,226.2 Q446,218.2 454,218.2 L460,218.2 Q468,218.2 468,226.2 L468,535 Z" fill="url(#s2)"/>
  <path d="M476,535 L476,399 Q476,391 484,391 L490,391 Q498,391 498,399 L498,535 Z" fill="url(#s3)"/>

  <path d="M596,535 L596,291 Q596,283 604,283 L610,283 Q618,283 618,291 L618,535 Z" fill="url(#s1)"/>
  <path d="M626,535 L626,413.4 Q626,405.4 634,405.4 L640,405.4 Q648,405.4 648,413.4 L648,535 Z" fill="url(#s2)"/>
  <path d="M656,535 L656,327 Q656,319 664,319 L670,319 Q678,319 678,327 L678,535 Z" fill="url(#s3)"/>

  <path d="M776,535 L776,219 Q776,211 784,211 L790,211 Q798,211 798,219 L798,535 Z" fill="url(#s1)"/>
  <path d="M806,535 L806,341.4 Q806,333.4 814,333.4 L820,333.4 Q828,333.4 828,341.4 L828,535 Z" fill="url(#s2)"/>
  <path d="M836,535 L836,183 Q836,175 844,175 L850,175 Q858,175 858,183 L858,535 Z" fill="url(#s3)" filter="url(#barGlow)"/>

  <text x="228" y="566" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#536174">Category 1</text>
  <text x="408" y="566" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#536174">Category 2</text>
  <text x="588" y="566" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#536174">Category 3</text>
  <text x="768" y="566" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#536174">Category 4</text>

  <circle cx="380" cy="607" r="7" fill="#4E86E8"/>
  <text x="394" y="612" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#48566A">Series 1</text>
  <circle cx="502" cy="607" r="7" fill="#ED7D31"/>
  <text x="516" y="612" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#48566A">Series 2</text>
  <circle cx="624" cy="607" r="7" fill="#70AD47"/>
  <text x="638" y="612" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#48566A">Series 3</text>

  <path d="M865,188 C900,188 920,205 925,230" fill="none" stroke="#70AD47" stroke-width="2.2" stroke-dasharray="5 5"/>
  <rect x="870" y="202" width="82" height="34" rx="17" fill="#EAF7E7" stroke="#70AD47" stroke-width="1"/>
  <text x="883" y="224" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3D7B2D">Peak 5.0</text>

  <text x="1030" y="184" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#AFC0D8">Takeaway</text>
  <text x="1030" y="244" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#FFFFFF">+42%</text>
  <text x="1032" y="282" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#B9C8DC">Series 3 leads the final category and sets the benchmark for next-quarter planning.</text>
  <rect x="1030" y="336" width="154" height="1" fill="#334157"/>
  <text x="1030" y="386" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Data binding logic</text>
  <text x="1030" y="421" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9C8DC">barHeight = value ÷ maxValue × plotHeight</text>
  <text x="1030" y="479" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9C8DC">Use the same formula for every category to keep comparisons truthful.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not paste the chart as a screenshot; it loses editability and cannot be restyled in PowerPoint.
- ❌ Do not use `<foreignObject>` to embed HTML charts; it will hard-fail translation.
- ❌ Do not use `<pattern>` fills for bars; simple gradients translate more reliably and remain editable.
- ❌ Do not put `filter` on gridlines or axis lines; filters on `<line>` are dropped.
- ❌ Do not rely on `marker-end` for chart annotations; draw arrow/callout geometry manually with lines or paths.

## Composition notes
- Keep the plot area wide and central; clustered columns need horizontal breathing room for category labels and legends.
- Use subtle gridlines and strong bar color contrast so the eye reads data first, decoration second.
- Place a compact insight card to the right when the chart needs executive interpretation, not just raw comparison.
- Maintain a clear data-to-geometry mapping: fixed baseline, fixed max value, and consistent bar width/gap across all categories.