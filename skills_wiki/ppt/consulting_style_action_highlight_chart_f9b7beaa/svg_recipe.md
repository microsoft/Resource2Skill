# SVG Recipe — Consulting-Style Action Highlight Chart

## Visual mechanism
A declarative action title tells the audience the conclusion first, while a stripped-down column chart supplies visual evidence. Context bars are muted grey and the single “action” data point is highlighted in a strong consulting blue with direct labels, eliminating the need for legends or heavy axes.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for a thin executive-style accent rule below the header
- 4× `<rect>` for muted historical bars
- 1× `<rect>` for the highlighted action bar
- 1× `<rect>` for the highlighted data-label badge
- 1× `<rect>` for a subtle annotation card
- 3× `<line>` for the minimalist x-axis, benchmark line, and annotation leader
- 2× `<path>` for a small upward callout chevron and decorative insight notch
- Multiple `<text>` elements with explicit `width` for action title, subtitle, axis labels, data labels, annotation, and source note
- 1× `<linearGradient>` for the highlighted bar fill
- 1× `<filter id="softShadow">` for the highlighted bar and annotation card

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueHighlight" x1="0" y1="520" x2="0" y2="170" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#004B8D"/>
      <stop offset="100%" stop-color="#0072BC"/>
    </linearGradient>
    <linearGradient id="ruleFade" x1="80" y1="0" x2="1200" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#005AA0"/>
      <stop offset="55%" stop-color="#005AA0" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#005AA0" stop-opacity="0"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <text x="80" y="72" width="1080" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="35" font-weight="700" fill="#111111">
    Kwanzan Cherry became the best-selling species in 2023, driving overall growth.
  </text>
  <text x="80" y="122" width="900" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#5F6368">
    Total tree sales by species, units sold, 2020–2023
  </text>
  <rect x="80" y="146" width="650" height="4" rx="2" fill="url(#ruleFade)"/>

  <text x="80" y="190" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#7A7A7A">
    UNITS SOLD
  </text>

  <line x1="120" y1="560" x2="1120" y2="560" stroke="#A9A9A9" stroke-width="1.4"/>
  <line x1="120" y1="330" x2="1120" y2="330" stroke="#D8DDE3" stroke-width="1.2" stroke-dasharray="7 8"/>
  <text x="1040" y="318" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8A8F98">
    4-year average
  </text>

  <rect x="190" y="405" width="120" height="155" rx="3" fill="#D2D6DA"/>
  <rect x="415" y="375" width="120" height="185" rx="3" fill="#D2D6DA"/>
  <rect x="640" y="285" width="120" height="275" rx="3" fill="#D2D6DA"/>
  <rect x="865" y="180" width="130" height="380" rx="4" fill="url(#blueHighlight)" filter="url(#softShadow)"/>

  <text x="218" y="388" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" text-anchor="middle" fill="#6B7076">45</text>
  <text x="443" y="358" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" text-anchor="middle" fill="#6B7076">51</text>
  <text x="668" y="268" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" text-anchor="middle" fill="#6B7076">75</text>

  <rect x="876" y="124" width="108" height="42" rx="21" fill="#003E73" filter="url(#softShadow)"/>
  <text x="904" y="153" width="58" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="700" text-anchor="middle" fill="#FFFFFF">103</text>

  <text x="215" y="594" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="600" text-anchor="middle" fill="#5F6368">2020</text>
  <text x="440" y="594" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="600" text-anchor="middle" fill="#5F6368">2021</text>
  <text x="665" y="594" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="600" text-anchor="middle" fill="#5F6368">2022</text>
  <text x="905" y="594" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" text-anchor="middle" fill="#005AA0">2023</text>

  <rect x="1010" y="205" width="178" height="116" rx="12" fill="#FFFFFF" stroke="#E0E5EA" stroke-width="1" filter="url(#softShadow)"/>
  <path d="M1010 250 L986 264 L1010 278 Z" fill="#FFFFFF" stroke="#E0E5EA" stroke-width="1"/>
  <text x="1030" y="235" width="135" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#111111">
    Action insight
  </text>
  <text x="1030" y="262" width="132" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#5F6368">
    2023 sales were
  </text>
  <text x="1030" y="286" width="132" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#005AA0">
    +37% vs. 2022
  </text>
  <text x="1030" y="310" width="132" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#5F6368">
    warranting expanded nursery allocation.
  </text>

  <line x1="995" y1="264" x2="944" y2="199" stroke="#005AA0" stroke-width="2.2"/>
  <path d="M936 190 L955 198 L941 211 Z" fill="#005AA0"/>

  <path d="M80 640 C170 662, 295 661, 380 640" fill="none" stroke="#E9EEF3" stroke-width="3"/>
  <text x="80" y="674" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8A8F98">
    Source: Internal sales reporting; values shown as units sold. Minimal chart design intentionally removes legend and y-axis clutter.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Heavy y-axis scales, legends, gridlines, and multi-color category palettes that compete with the one highlighted takeaway
- ❌ Using a screenshot of a chart; build bars, labels, and callouts as editable SVG shapes
- ❌ Applying `filter` to `<line>` elements for axis shadows; use flat lines and reserve shadows for cards or highlighted bars
- ❌ `marker-end` on `<path>` for callout arrows; draw arrowheads as small editable `<path>` triangles instead
- ❌ Text without explicit `width`, because PowerPoint translation may clip or reflow it unpredictably

## Composition notes
- Reserve the top 18–22% of the slide for the action title and metric subtitle; the title should be a complete business conclusion, not a neutral chart label.
- Keep the chart area spacious, with a low x-axis and generous side margins so the highlighted bar has room for an annotation card.
- Use one accent color only for the “signal” bar, label badge, and callout leader; keep all context bars neutral grey.
- Prefer direct labels above bars and a short source note below the chart to avoid legends and reduce audience eye travel.