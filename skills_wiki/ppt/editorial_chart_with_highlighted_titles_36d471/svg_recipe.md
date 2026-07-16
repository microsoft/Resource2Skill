# SVG Recipe — Panel Title Chart Slide

## Visual mechanism
A large editable chart card fills the slide while a high-contrast editorial title panel overlaps its upper-left edge, making the narrative context feel attached to the data. Subtle background gradients, translucent chart fills, and a data callout create a premium report-style composition without sacrificing chart readability.

## SVG primitives needed
- 2× `<rect>` for full-slide background and chart card base
- 2× `<path>` for soft decorative background blobs
- 1× `<rect>` for the prominent headline/subtitle panel
- 1× `<path>` for the title panel accent wedge
- 7× `<line>` for chart gridlines and axes
- 8× `<text>` for headline, subtitle, chart title, axis labels, legend, callout, and source
- 8× `<rect>` for vertical comparison bars
- 2× `<path>` for line-chart area fill and line stroke
- 5× `<circle>` for data points
- 1× `<rect>` and 1× `<path>` for the annotation callout
- 3× `<linearGradient>` for background, panel, and chart area fill
- 1× `<filter id="softShadow">` applied to the chart card, panel, and callout

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="58%" stop-color="#EEF3FA"/>
      <stop offset="100%" stop-color="#E8EEF7"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#172A54"/>
      <stop offset="100%" stop-color="#3156A3"/>
    </linearGradient>
    <linearGradient id="areaGrad" x1="0" y1="210" x2="0" y2="565">
      <stop offset="0%" stop-color="#2F80ED" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#2F80ED" stop-opacity="0.02"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M982 28 C1095 -42 1278 18 1328 142 C1372 251 1285 333 1174 312 C1068 292 1050 197 964 172 C879 148 870 97 982 28 Z" fill="#DCE8FF" opacity="0.7"/>
  <path d="M-92 542 C16 480 119 516 145 604 C173 698 67 768 -52 738 C-161 711 -203 607 -92 542 Z" fill="#CFE7F6" opacity="0.55"/>

  <rect x="116" y="150" width="1048" height="470" rx="28" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="116" y="150" width="1048" height="470" rx="28" fill="none" stroke="#DDE6F1" stroke-width="1.2"/>

  <rect x="84" y="70" width="650" height="176" rx="22" fill="url(#panelGrad)" filter="url(#softShadow)"/>
  <path d="M684 70 L734 70 L734 246 L620 246 C668 216 693 158 684 70 Z" fill="#6EC6FF" opacity="0.28"/>
  <text x="124" y="127" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#FFFFFF">
    Revenue momentum is shifting to enterprise
  </text>
  <text x="126" y="177" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#DDEBFF">
    Expansion accounts now drive the majority of growth, offsetting slower SMB acquisition.
  </text>

  <text x="160" y="304" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#15213B">
    Quarterly recurring revenue by segment
  </text>
  <text x="160" y="333" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#6B778C">
    USD millions, trailing five quarters
  </text>

  <line x1="186" y1="520" x2="1086" y2="520" stroke="#9AA8B8" stroke-width="1.3"/>
  <line x1="186" y1="440" x2="1086" y2="440" stroke="#E5EAF1" stroke-width="1"/>
  <line x1="186" y1="360" x2="1086" y2="360" stroke="#E5EAF1" stroke-width="1"/>
  <line x1="186" y1="280" x2="1086" y2="280" stroke="#E5EAF1" stroke-width="1"/>
  <line x1="186" y1="520" x2="186" y2="280" stroke="#9AA8B8" stroke-width="1.3"/>

  <text x="136" y="525" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#7A8797">0</text>
  <text x="128" y="445" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#7A8797">25</text>
  <text x="128" y="365" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#7A8797">50</text>
  <text x="128" y="285" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#7A8797">75</text>

  <rect x="255" y="404" width="34" height="116" rx="7" fill="#D8E3F7"/>
  <rect x="298" y="372" width="34" height="148" rx="7" fill="#95B9F2"/>
  <rect x="415" y="388" width="34" height="132" rx="7" fill="#D8E3F7"/>
  <rect x="458" y="336" width="34" height="184" rx="7" fill="#95B9F2"/>
  <rect x="575" y="360" width="34" height="160" rx="7" fill="#D8E3F7"/>
  <rect x="618" y="307" width="34" height="213" rx="7" fill="#95B9F2"/>
  <rect x="735" y="340" width="34" height="180" rx="7" fill="#D8E3F7"/>
  <rect x="778" y="286" width="34" height="234" rx="7" fill="#95B9F2"/>

  <path d="M272 474 C350 456 382 428 432 422 C504 414 544 374 624 366 C704 358 735 328 792 318 C855 306 914 276 1010 238 L1010 520 L272 520 Z" fill="url(#areaGrad)"/>
  <path d="M272 474 C350 456 382 428 432 422 C504 414 544 374 624 366 C704 358 735 328 792 318 C855 306 914 276 1010 238" fill="none" stroke="#1F6FEB" stroke-width="5" stroke-linecap="round"/>

  <circle cx="272" cy="474" r="7" fill="#FFFFFF" stroke="#1F6FEB" stroke-width="4"/>
  <circle cx="432" cy="422" r="7" fill="#FFFFFF" stroke="#1F6FEB" stroke-width="4"/>
  <circle cx="624" cy="366" r="7" fill="#FFFFFF" stroke="#1F6FEB" stroke-width="4"/>
  <circle cx="792" cy="318" r="7" fill="#FFFFFF" stroke="#1F6FEB" stroke-width="4"/>
  <circle cx="1010" cy="238" r="8" fill="#FFFFFF" stroke="#1F6FEB" stroke-width="4"/>

  <rect x="904" y="174" width="186" height="72" rx="16" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M1000 246 L1018 246 L1009 264 Z" fill="#FFFFFF"/>
  <text x="926" y="204" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#15213B">Q4 enterprise ARR</text>
  <text x="926" y="229" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#1F6FEB">+34%</text>

  <rect x="860" y="312" width="14" height="14" rx="3" fill="#95B9F2"/>
  <text x="882" y="324" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#4D5A6E">Enterprise</text>
  <rect x="860" y="338" width="14" height="14" rx="3" fill="#D8E3F7"/>
  <text x="882" y="350" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#4D5A6E">SMB</text>
  <circle cx="867" cy="374" r="7" fill="#FFFFFF" stroke="#1F6FEB" stroke-width="4"/>
  <text x="882" y="379" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#4D5A6E">Total ARR trend</text>

  <text x="248" y="555" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#7A8797">Q4 FY23</text>
  <text x="408" y="555" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#7A8797">Q1 FY24</text>
  <text x="600" y="555" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#7A8797">Q2</text>
  <text x="768" y="555" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#7A8797">Q3</text>
  <text x="986" y="555" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#7A8797">Q4</text>

  <text x="116" y="664" width="600" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8A96A8">
    Source: Company reporting system and finance forecast, refreshed January 2026
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using an actual embedded chart object; build the featured chart from editable SVG bars, paths, lines, circles, and labels.
- ❌ Placing the title above the chart with no overlap; the defining gesture is the panel physically anchoring the chart narrative.
- ❌ Applying blur or shadow filters to grid `<line>` elements; keep filters on cards, panels, paths, or text only.
- ❌ Overcrowding the chart with many series or dense tick labels; this layout works best with one primary trend and one supporting comparison.

## Composition notes
- Keep the title panel in the upper-left 45–60% of the slide width, overlapping the chart card by roughly 40–80 px.
- Reserve the lower two-thirds for the chart; use generous internal padding so gridlines and labels do not collide with the panel.
- Use a dark saturated panel color, then repeat the same hue in the primary chart line to tie headline and data together.
- Leave quiet negative space around the legend and source line; the editorial panel and final data point should be the two visual anchors.