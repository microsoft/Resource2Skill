# SVG Recipe — Editorial Dumbbell Plot (Economist-Style Data Visualization)

## Visual mechanism
A minimalist editorial chart compares two moments with paired dots connected by thin horizontal lines, making the gap and direction of change the visual story. The layout borrows newspaper-style authority: a red accent bar, strong left-aligned headline, restrained grid, crisp labels, and one annotated insight.

## SVG primitives needed
- 1× `<rect>` for the off-white editorial slide background
- 1× `<rect>` for the signature red editorial accent mark
- 1× `<rect>` for a subtle callout card with shadow
- 6× `<line>` for faint vertical value gridlines
- 8× `<line>` for dumbbell connectors between baseline and current values
- 16× `<circle>` for paired baseline/current data points
- 1× `<path>` for a curved editorial annotation leader
- 1× `<filter id="softShadow">` applied to the callout card
- 2× `<radialGradient>` fills for dimensional baseline/current dots
- Multiple `<text>` elements with explicit `width` for title, subtitle, axis labels, category labels, value labels, legend, and annotation copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="baseDot" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#d7e0e6"/>
      <stop offset="100%" stop-color="#9aacb8"/>
    </radialGradient>
    <radialGradient id="newDot" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#f3a29a"/>
      <stop offset="100%" stop-color="#d85349"/>
    </radialGradient>
    <filter id="softShadow" x="-15%" y="-20%" width="130%" height="150%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#fbfaf7"/>
  <rect x="58" y="42" width="62" height="8" fill="#e31a1c"/>

  <text x="58" y="92" width="880" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#333333">
    Engagement scores shifted unevenly across departments
  </text>
  <text x="58" y="128" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#777777">
    Employee engagement score by department, 2023 vs 2024 (% favorable)
  </text>

  <circle cx="286" cy="174" r="7" fill="url(#baseDot)"/>
  <text x="302" y="179" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777777">2023</text>
  <circle cx="375" cy="174" r="7" fill="url(#newDot)"/>
  <text x="391" y="179" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777777">2024</text>

  <line x1="285" y1="208" x2="285" y2="632" stroke="#dddddd" stroke-width="1"/>
  <line x1="452" y1="208" x2="452" y2="632" stroke="#dddddd" stroke-width="1" stroke-dasharray="3 5"/>
  <line x1="619" y1="208" x2="619" y2="632" stroke="#dddddd" stroke-width="1" stroke-dasharray="3 5"/>
  <line x1="786" y1="208" x2="786" y2="632" stroke="#dddddd" stroke-width="1" stroke-dasharray="3 5"/>
  <line x1="953" y1="208" x2="953" y2="632" stroke="#dddddd" stroke-width="1" stroke-dasharray="3 5"/>
  <line x1="1120" y1="208" x2="1120" y2="632" stroke="#dddddd" stroke-width="1"/>

  <text x="276" y="196" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8a8a8a">0</text>
  <text x="440" y="196" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8a8a8a">20</text>
  <text x="607" y="196" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8a8a8a">40</text>
  <text x="774" y="196" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8a8a8a">60</text>
  <text x="941" y="196" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8a8a8a">80</text>
  <text x="1102" y="196" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8a8a8a">100</text>

  <text x="58" y="256" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">Production</text>
  <line x1="452" y1="252" x2="577" y2="252" stroke="#d9d9d9" stroke-width="4" stroke-linecap="round"/>
  <circle cx="452" cy="252" r="8" fill="url(#baseDot)"/>
  <circle cx="577" cy="252" r="8" fill="url(#newDot)"/>
  <text x="588" y="257" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d85349">35</text>

  <text x="58" y="307" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">Finance</text>
  <line x1="786" y1="303" x2="870" y2="303" stroke="#d9d9d9" stroke-width="4" stroke-linecap="round"/>
  <circle cx="786" cy="303" r="8" fill="url(#baseDot)"/>
  <circle cx="870" cy="303" r="8" fill="url(#newDot)"/>
  <text x="881" y="308" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d85349">70</text>

  <text x="58" y="358" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">Customer Service</text>
  <line x1="870" y1="354" x2="953" y2="354" stroke="#d9d9d9" stroke-width="4" stroke-linecap="round"/>
  <circle cx="953" cy="354" r="8" fill="url(#baseDot)"/>
  <circle cx="870" cy="354" r="8" fill="url(#newDot)"/>
  <text x="825" y="359" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d85349">70</text>

  <text x="58" y="409" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">Operations</text>
  <line x1="936" y1="405" x2="995" y2="405" stroke="#d9d9d9" stroke-width="4" stroke-linecap="round"/>
  <circle cx="995" cy="405" r="8" fill="url(#baseDot)"/>
  <circle cx="936" cy="405" r="8" fill="url(#newDot)"/>
  <text x="891" y="410" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d85349">78</text>

  <text x="58" y="460" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">IT</text>
  <line x1="661" y1="456" x2="744" y2="456" stroke="#d9d9d9" stroke-width="4" stroke-linecap="round"/>
  <circle cx="661" cy="456" r="8" fill="url(#baseDot)"/>
  <circle cx="744" cy="456" r="8" fill="url(#newDot)"/>
  <text x="755" y="461" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d85349">55</text>

  <text x="58" y="511" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">Procurement</text>
  <line x1="552" y1="507" x2="744" y2="507" stroke="#d9d9d9" stroke-width="4" stroke-linecap="round"/>
  <circle cx="552" cy="507" r="8" fill="url(#baseDot)"/>
  <circle cx="744" cy="507" r="8" fill="url(#newDot)"/>
  <text x="756" y="512" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d85349">55  +23</text>

  <text x="58" y="562" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">Sales</text>
  <line x1="786" y1="558" x2="828" y2="558" stroke="#d9d9d9" stroke-width="4" stroke-linecap="round"/>
  <circle cx="786" cy="558" r="8" fill="url(#baseDot)"/>
  <circle cx="828" cy="558" r="8" fill="url(#newDot)"/>
  <text x="839" y="563" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d85349">65</text>

  <text x="58" y="613" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">HR</text>
  <line x1="911" y1="609" x2="953" y2="609" stroke="#d9d9d9" stroke-width="4" stroke-linecap="round"/>
  <circle cx="911" cy="609" r="8" fill="url(#baseDot)"/>
  <circle cx="953" cy="609" r="8" fill="url(#newDot)"/>
  <text x="964" y="614" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d85349">80</text>

  <rect x="845" y="458" width="258" height="86" rx="12" fill="#ffffff" filter="url(#softShadow)"/>
  <text x="866" y="486" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#333333">Largest improvement</text>
  <text x="866" y="512" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#d85349">Procurement +23 pts</text>
  <text x="866" y="532" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">The widest gap on the common scale.</text>
  <path d="M846 500 C812 494, 785 500, 751 507" fill="none" stroke="#e31a1c" stroke-width="2.2" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Heavy chart boxes, thick axes, or filled bars that compete with the dumbbell gap
- ❌ `marker-end` arrowheads on connector paths; if direction is needed, show it with dot color, labels, or a separate `<line>`
- ❌ Clipping, masking, or filters on gridlines/connectors; keep chart geometry simple and editable
- ❌ Too many value labels; label the important endpoint or delta rather than every number

## Composition notes
- Keep the editorial header flush left, with the red accent above the title as the visual anchor.
- Reserve the widest horizontal area for the common quantitative scale; the dumbbell mechanism needs room for gaps to read clearly.
- Use low-contrast gridlines and neutral connectors so the colored endpoint dots carry the comparison.
- Add only one strong annotation callout; the chart should feel curated, not cluttered.