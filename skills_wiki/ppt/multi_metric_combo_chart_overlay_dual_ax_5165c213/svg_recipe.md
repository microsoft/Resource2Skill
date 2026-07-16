# SVG Recipe — Dual-Axis Bar and Line Chart

## Visual mechanism
Overlay a muted column chart and a high-contrast line chart inside one shared plot area, using the left Y-axis for the volume metric and the right Y-axis for the rate/count metric. The bars provide mass and scale, while the line with markers exposes trend correlation across the same category axis.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<rect>` for the elevated chart card/container
- 1× `<rect>` for a soft vertical highlight band on the most important category
- 5× `<rect>` for editable rounded bars representing the primary metric
- 6× `<line>` for horizontal gridlines
- 2× `<line>` for left and right Y-axes
- 1× `<line>` for the X-axis baseline
- 1× `<path>` for the secondary metric trend line
- 5× `<circle>` for line markers
- Multiple `<text>` elements with explicit `width` for title, subtitle, axes, tick labels, category labels, legend, and annotation
- 2× `<linearGradient>` for premium card/background and bar fills
- 1× `<filter id="cardShadow">` applied to the chart card
- 1× `<filter id="markerGlow">` applied to line markers

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F6F8FB"/>
      <stop offset="100%" stop-color="#EAF0F7"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5E9DCE"/>
      <stop offset="100%" stop-color="#326F9D"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7FAFD"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode flood-color="#172033" flood-opacity="0.18"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="markerGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="84" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#182235">
    Velocity planned vs. bugs found
  </text>
  <text x="84" y="96" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#657386">
    Dual-axis combo view showing how delivery volume and defect count move across recent sprints.
  </text>

  <rect x="78" y="132" width="1124" height="514" rx="28" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
  <rect x="735" y="190" width="130" height="370" rx="10" fill="#FFF2DF" opacity="0.85"/>

  <text x="180" y="166" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#326F9D">
    Velocity delivered
  </text>
  <rect x="322" y="153" width="28" height="14" rx="4" fill="url(#barGrad)"/>
  <text x="394" y="166" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FF8C00">
    Bugs found
  </text>
  <line x1="485" y1="160" x2="525" y2="160" stroke="#FF8C00" stroke-width="4" stroke-linecap="round"/>
  <circle cx="505" cy="160" r="6" fill="#FFFFFF" stroke="#FF8C00" stroke-width="3"/>

  <line x1="180" y1="560" x2="1060" y2="560" stroke="#B8C2CF" stroke-width="1.5"/>
  <line x1="180" y1="190" x2="180" y2="560" stroke="#AEB9C7" stroke-width="1.5"/>
  <line x1="1060" y1="190" x2="1060" y2="560" stroke="#AEB9C7" stroke-width="1.5"/>

  <line x1="180" y1="560" x2="1060" y2="560" stroke="#D9E0E8" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="180" y1="486" x2="1060" y2="486" stroke="#D9E0E8" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="180" y1="412" x2="1060" y2="412" stroke="#D9E0E8" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="180" y1="338" x2="1060" y2="338" stroke="#D9E0E8" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="180" y1="264" x2="1060" y2="264" stroke="#D9E0E8" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="180" y1="190" x2="1060" y2="190" stroke="#D9E0E8" stroke-width="1" stroke-dasharray="5 8"/>

  <text x="126" y="565" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#326F9D" text-anchor="end">0</text>
  <text x="126" y="491" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#326F9D" text-anchor="end">14</text>
  <text x="126" y="417" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#326F9D" text-anchor="end">28</text>
  <text x="126" y="343" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#326F9D" text-anchor="end">42</text>
  <text x="126" y="269" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#326F9D" text-anchor="end">56</text>
  <text x="126" y="195" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#326F9D" text-anchor="end">70</text>

  <text x="1098" y="565" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FF8C00">0</text>
  <text x="1098" y="491" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FF8C00">1.6</text>
  <text x="1098" y="417" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FF8C00">3.2</text>
  <text x="1098" y="343" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FF8C00">4.8</text>
  <text x="1098" y="269" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FF8C00">6.4</text>
  <text x="1098" y="195" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FF8C00">8</text>

  <text x="92" y="384" width="130" transform="rotate(-90 92 384)" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#326F9D">Velocity points</text>
  <text x="1166" y="384" width="100" transform="rotate(90 1166 384)" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FF8C00">Bug count</text>

  <rect x="223" y="322" width="74" height="238" rx="8" fill="url(#barGrad)" opacity="0.92"/>
  <rect x="403" y="285" width="74" height="275" rx="8" fill="url(#barGrad)" opacity="0.92"/>
  <rect x="583" y="306" width="74" height="254" rx="8" fill="url(#barGrad)" opacity="0.92"/>
  <rect x="763" y="243" width="74" height="317" rx="8" fill="url(#barGrad)" opacity="0.92"/>
  <rect x="943" y="253" width="74" height="307" rx="8" fill="url(#barGrad)" opacity="0.92"/>

  <path d="M260 421 C320 410 380 390 440 375 S560 450 620 468 S740 280 800 236 S920 300 980 329"
        fill="none" stroke="#FF8C00" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="260" cy="421" r="9" fill="#FFFFFF" stroke="#FF8C00" stroke-width="4" filter="url(#markerGlow)"/>
  <circle cx="440" cy="375" r="9" fill="#FFFFFF" stroke="#FF8C00" stroke-width="4" filter="url(#markerGlow)"/>
  <circle cx="620" cy="468" r="9" fill="#FFFFFF" stroke="#FF8C00" stroke-width="4" filter="url(#markerGlow)"/>
  <circle cx="800" cy="236" r="10" fill="#FFFFFF" stroke="#FF8C00" stroke-width="4" filter="url(#markerGlow)"/>
  <circle cx="980" cy="329" r="9" fill="#FFFFFF" stroke="#FF8C00" stroke-width="4" filter="url(#markerGlow)"/>

  <text x="218" y="590" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#465366" text-anchor="middle">Sprint 1</text>
  <text x="398" y="590" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#465366" text-anchor="middle">Sprint 2</text>
  <text x="578" y="590" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#465366" text-anchor="middle">Sprint 3</text>
  <text x="758" y="590" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#182235" text-anchor="middle">Sprint 4</text>
  <text x="938" y="590" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#465366" text-anchor="middle">Sprint 5</text>

  <rect x="865" y="204" width="210" height="74" rx="16" fill="#FFFFFF" stroke="#F2BE75" stroke-width="1.5"/>
  <text x="884" y="229" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#D97800">Sprint 4 anomaly</text>
  <text x="884" y="251" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6675">Highest output coincides with the defect peak.</text>
  <line x1="865" y1="248" x2="810" y2="238" stroke="#F2BE75" stroke-width="2" stroke-dasharray="4 5"/>

  <text x="520" y="628" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8793A3" text-anchor="middle">
    Shared category axis; independent value scales
  </text>
</svg>
```

## Avoid in this skill
- ❌ Rendering the chart as a single bitmap; use editable SVG bars, axes, paths, circles, and text instead.
- ❌ Using `marker-end` arrowheads on trend or annotation paths; they may disappear. Use plain `<line>` or draw arrowheads manually if needed.
- ❌ Applying filters to `<line>` gridlines or axes; filters on lines are dropped, so reserve shadows/glows for cards, paths, circles, or text.
- ❌ Placing the right-axis label too close to the plot; dual-axis charts need clear color binding to prevent metric confusion.
- ❌ Overloading both series with saturated colors; keep bars muted and make the line the high-contrast accent.

## Composition notes
- Keep the chart card as the hero element, occupying roughly 80–88% of slide width and 65–75% of slide height.
- Use color-coded axes: bar color for the left Y-axis, line color for the right Y-axis, with a compact legend above the plot.
- Preserve vertical negative space above the chart for a title/subtitle and inside the card for the legend.
- Highlight only one meaningful category with a soft band or callout; too many annotations will weaken the correlation story.