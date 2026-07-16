# SVG Recipe — Publication-Grade Dumbbell Chart

## Visual mechanism
A dumbbell chart plots two comparable values on the same horizontal scale, then connects them with a thin neutral line so the viewer reads the gap immediately. The publication-grade treatment comes from restrained axes, right-aligned category labels, muted “before” dots, vivid “after” dots, and integrated labeling instead of a separate legend.

## SVG primitives needed
- 1× `<rect>` for the off-white chart card background with a subtle shadow
- 1× `<linearGradient>` for the warm editorial slide background
- 1× `<filter id="cardShadow">` applied to the chart card
- 1× `<rect>` for the small editorial accent bar above the headline
- 6× `<line>` for faint vertical gridlines
- 6× `<text>` for top scale labels
- 8× `<text>` for right-aligned category labels
- 8× `<line>` for dumbbell connectors between paired values
- 16× `<circle>` for before/after data dots
- 2× `<text>` for integrated series labels above the first-row dots
- 8× `<text>` for optional right-side delta labels
- 1× `<path>` for a small editorial annotation callout curve
- 1× `<circle>` and 1× `<text>` for a subtle publisher-style monogram mark
- Multiple `<text>` elements for title, subtitle, axis note, source, and callout copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="warmBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7f4ef"/>
      <stop offset="62%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f1eee8"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#warmBg)"/>
  <rect x="58" y="34" width="1164" height="652" rx="0" fill="#fbfaf6" filter="url(#cardShadow)"/>

  <rect x="92" y="70" width="58" height="7" fill="#d93a46"/>
  <text x="92" y="112" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#1f1f1f">
    Employee engagement rose unevenly across departments
  </text>
  <text x="92" y="150" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#666666">
    Internal survey score, share of favorable responses, 2023 versus 2024
  </text>

  <text x="340" y="202" width="800" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#777777">
    % favorable response
  </text>

  <line x1="340" y1="220" x2="340" y2="620" stroke="#ece9e2" stroke-width="1"/>
  <line x1="500" y1="220" x2="500" y2="620" stroke="#ece9e2" stroke-width="1"/>
  <line x1="660" y1="220" x2="660" y2="620" stroke="#ece9e2" stroke-width="1"/>
  <line x1="820" y1="220" x2="820" y2="620" stroke="#ece9e2" stroke-width="1"/>
  <line x1="980" y1="220" x2="980" y2="620" stroke="#ece9e2" stroke-width="1"/>
  <line x1="1140" y1="220" x2="1140" y2="620" stroke="#ece9e2" stroke-width="1"/>

  <text x="340" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#777777">0</text>
  <text x="500" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#777777">20</text>
  <text x="660" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#777777">40</text>
  <text x="820" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#777777">60</text>
  <text x="980" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#777777">80</text>
  <text x="1140" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#777777">100</text>

  <text x="300" y="265" width="210" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">Operations</text>
  <text x="300" y="315" width="210" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">HR</text>
  <text x="300" y="365" width="210" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">Customer Service</text>
  <text x="300" y="415" width="210" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">Finance</text>
  <text x="300" y="465" width="210" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">Sales</text>
  <text x="300" y="515" width="210" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">IT</text>
  <text x="300" y="565" width="210" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">Procurement</text>
  <text x="300" y="615" width="210" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">Production</text>

  <text x="1018" y="238" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#9a9a90">2023</text>
  <text x="954" y="238" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#d93a46">2024</text>

  <line x1="1020" y1="260" x2="964" y2="260" stroke="#d8d6cf" stroke-width="4" stroke-linecap="round"/>
  <line x1="940" y1="310" x2="980" y2="310" stroke="#d8d6cf" stroke-width="4" stroke-linecap="round"/>
  <line x1="980" y1="360" x2="900" y2="360" stroke="#d8d6cf" stroke-width="4" stroke-linecap="round"/>
  <line x1="820" y1="410" x2="900" y2="410" stroke="#d8d6cf" stroke-width="4" stroke-linecap="round"/>
  <line x1="820" y1="460" x2="860" y2="460" stroke="#d8d6cf" stroke-width="4" stroke-linecap="round"/>
  <line x1="700" y1="510" x2="780" y2="510" stroke="#d8d6cf" stroke-width="4" stroke-linecap="round"/>
  <line x1="596" y1="560" x2="780" y2="560" stroke="#d8d6cf" stroke-width="4" stroke-linecap="round"/>
  <line x1="500" y1="610" x2="620" y2="610" stroke="#d8d6cf" stroke-width="4" stroke-linecap="round"/>

  <circle cx="1020" cy="260" r="8" fill="#aaa99f"/>
  <circle cx="964" cy="260" r="8" fill="#d93a46"/>
  <circle cx="940" cy="310" r="8" fill="#aaa99f"/>
  <circle cx="980" cy="310" r="8" fill="#d93a46"/>
  <circle cx="980" cy="360" r="8" fill="#aaa99f"/>
  <circle cx="900" cy="360" r="8" fill="#d93a46"/>
  <circle cx="820" cy="410" r="8" fill="#aaa99f"/>
  <circle cx="900" cy="410" r="8" fill="#d93a46"/>
  <circle cx="820" cy="460" r="8" fill="#aaa99f"/>
  <circle cx="860" cy="460" r="8" fill="#d93a46"/>
  <circle cx="700" cy="510" r="8" fill="#aaa99f"/>
  <circle cx="780" cy="510" r="8" fill="#d93a46"/>
  <circle cx="596" cy="560" r="8" fill="#aaa99f"/>
  <circle cx="780" cy="560" r="8" fill="#d93a46"/>
  <circle cx="500" cy="610" r="8" fill="#aaa99f"/>
  <circle cx="620" cy="610" r="8" fill="#d93a46"/>

  <text x="1174" y="265" width="58" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#777777">−7</text>
  <text x="1174" y="315" width="58" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#d93a46">+5</text>
  <text x="1174" y="365" width="58" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#777777">−10</text>
  <text x="1174" y="415" width="58" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#d93a46">+10</text>
  <text x="1174" y="465" width="58" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#d93a46">+5</text>
  <text x="1174" y="515" width="58" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#d93a46">+10</text>
  <text x="1174" y="565" width="58" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#d93a46">+23</text>
  <text x="1174" y="615" width="58" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#d93a46">+15</text>

  <path d="M835 548 C885 520, 920 510, 955 492" fill="none" stroke="#d93a46" stroke-width="2.5" stroke-linecap="round"/>
  <text x="958" y="486" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#d93a46">
    Largest gain: Procurement
  </text>

  <text x="92" y="660" width="700" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8a8a8a">
    Source: Internal engagement survey, n=4,820. Figures are percentage-point scores rounded to the nearest whole number.
  </text>
  <circle cx="1168" cy="646" r="20" fill="#c9c7bd"/>
  <text x="1168" y="654" width="40" text-anchor="middle" font-family="Georgia, serif" font-size="24" fill="#ffffff">E</text>
</svg>
```

## Avoid in this skill
- ❌ Heavy chart borders, visible x/y axes, or dark gridlines; they reduce the editorial “data-ink” feel.
- ❌ Clustered bars or stacked bars; they obscure the paired-value gap that the dumbbell chart is designed to emphasize.
- ❌ A separate boxed legend when direct labels above the first-row dots can explain the series more elegantly.
- ❌ `marker-end` arrowheads on paths for direction; if arrows are needed, draw them manually with editable lines or paths.
- ❌ Text without explicit `width=` attributes; PowerPoint translation needs fixed text boxes for reliable layout.

## Composition notes
- Keep category labels in the left 20–25% of the canvas and right-align them against the plot area for a clean reading edge.
- Reserve the widest horizontal span for the scale and dots; the connectors should feel airy, not compressed.
- Use one strong accent color only for the “after/current/target” value; keep the baseline value gray.
- Place the title and subtitle above the chart, with a small red editorial bar as a premium publication cue.