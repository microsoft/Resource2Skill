# SVG Recipe — Harmonized Data Density (Chart Polish & Focus Highlighting)

## Visual mechanism
Dense chart data is made executive-readable by giving the base data a quiet, harmonized palette while injecting one high-contrast accent at the narrative focus point. The column chart uses generous bar mass with a 50% gap-to-bar rhythm, while the doughnut chart avoids rainbow colors in favor of a monochromatic scale.

## SVG primitives needed
- 2× large `<rect>` for elevated chart cards
- 10× `<rect>` for polished column bars with rounded tops and 50% visual gap spacing
- 6× `<path>` for editable doughnut chart segments using a tonal teal scale
- 6× `<line>` for subdued horizontal gridlines
- 1× `<path>` for a soft decorative background blob
- 1× `<linearGradient>` for the slide background
- 1× `<linearGradient>` for the highlighted column fill
- 1× `<filter id="cardShadow">` applied to card rectangles
- 1× `<filter id="accentGlow">` applied to the highlighted bar and callout badge
- Multiple `<text>` elements with explicit `width` attributes for title, labels, values, annotations, and legends

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>
    <linearGradient id="accentBar" x1="0" y1="560" x2="0" y2="294">
      <stop offset="0%" stop-color="#FF8A50"/>
      <stop offset="100%" stop-color="#FF5722"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="accentGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M905,35 C1015,5 1180,40 1235,135 C1285,222 1225,310 1120,315 C1010,320 930,270 875,205 C820,138 815,62 905,35 Z" fill="#DCEBFA" opacity="0.55"/>

  <text x="70" y="62" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1E2832">Annual Performance Review: Data Highlights</text>
  <text x="70" y="100" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#728091">Optimized spacing, contrast highlighting, and tonal harmony for dense chart storytelling</text>

  <rect x="70" y="145" width="690" height="510" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="805" y="145" width="405" height="510" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <text x="110" y="195" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#263442">Revenue trend</text>
  <text x="110" y="221" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8A96A6">Bars use high density, restrained base color, and one decisive focus highlight.</text>

  <line x1="110" y1="560" x2="720" y2="560" stroke="#E8EDF3" stroke-width="1"/>
  <line x1="110" y1="504" x2="720" y2="504" stroke="#E8EDF3" stroke-width="1"/>
  <line x1="110" y1="448" x2="720" y2="448" stroke="#E8EDF3" stroke-width="1"/>
  <line x1="110" y1="392" x2="720" y2="392" stroke="#E8EDF3" stroke-width="1"/>
  <line x1="110" y1="336" x2="720" y2="336" stroke="#E8EDF3" stroke-width="1"/>
  <line x1="110" y1="280" x2="720" y2="280" stroke="#E8EDF3" stroke-width="1"/>

  <rect x="138" y="448" width="38" height="112" rx="12" fill="#C8D4E3"/>
  <rect x="195" y="406" width="38" height="154" rx="12" fill="#C8D4E3"/>
  <rect x="252" y="434" width="38" height="126" rx="12" fill="#C8D4E3"/>
  <rect x="309" y="364" width="38" height="196" rx="12" fill="#C8D4E3"/>
  <rect x="366" y="294" width="38" height="266" rx="12" fill="url(#accentBar)" filter="url(#accentGlow)"/>
  <rect x="423" y="392" width="38" height="168" rx="12" fill="#C8D4E3"/>
  <rect x="480" y="420" width="38" height="140" rx="12" fill="#C8D4E3"/>
  <rect x="537" y="350" width="38" height="210" rx="12" fill="#C8D4E3"/>
  <rect x="594" y="336" width="38" height="224" rx="12" fill="#C8D4E3"/>
  <rect x="651" y="406" width="38" height="154" rx="12" fill="#C8D4E3"/>

  <text x="157" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A1">Jan</text>
  <text x="214" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A1">Feb</text>
  <text x="271" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A1">Mar</text>
  <text x="328" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A1">Apr</text>
  <text x="385" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FF5722">May</text>
  <text x="442" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A1">Jun</text>
  <text x="499" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A1">Jul</text>
  <text x="556" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A1">Aug</text>
  <text x="613" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A1">Sep</text>
  <text x="670" y="588" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A1">Oct</text>

  <text x="370" y="278" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FF5722">95</text>
  <path d="M430,303 C468,286 497,281 531,285" fill="none" stroke="#FF5722" stroke-width="2.5" stroke-dasharray="5 5"/>
  <rect x="535" y="260" width="150" height="48" rx="18" fill="#FFF0EA" filter="url(#accentGlow)"/>
  <text x="553" y="290" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FF5722">Peak month</text>

  <text x="845" y="195" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#263442">Market mix</text>
  <text x="845" y="221" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8A96A6">A single-family palette replaces rainbow segments for calmer comparison.</text>

  <path d="M965,297 A128,128 0 0,1 1086.7,464.6 L1039.2,449.1 A78,78 0 0,0 965,347 Z" fill="#006D77"/>
  <path d="M1086.7,464.6 A128,128 0 0,1 949,552 L955.2,502.4 A78,78 0 0,0 1039.2,449.1 Z" fill="#168A93"/>
  <path d="M949,552 A128,128 0 0,1 843.3,464.6 L890.8,449.1 A78,78 0 0,0 955.2,502.4 Z" fill="#36A7AE"/>
  <path d="M843.3,464.6 A128,128 0 0,1 849.2,370.5 L894.4,391.8 A78,78 0 0,0 890.8,449.1 Z" fill="#6BC3C7"/>
  <path d="M849.2,370.5 A128,128 0 0,1 903.3,312.8 L927.4,356.7 A78,78 0 0,0 894.4,391.8 Z" fill="#9AD9DB"/>
  <path d="M903.3,312.8 A128,128 0 0,1 965,297 L965,347 A78,78 0 0,0 927.4,356.7 Z" fill="#C5ECEC"/>

  <circle cx="965" cy="425" r="66" fill="#FFFFFF"/>
  <text x="913" y="415" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7E8A98">Top segment</text>
  <text x="906" y="447" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#006D77">30%</text>

  <rect x="845" y="585" width="13" height="13" rx="3" fill="#006D77"/>
  <text x="866" y="597" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#596675">Enterprise</text>
  <rect x="980" y="585" width="13" height="13" rx="3" fill="#36A7AE"/>
  <text x="1001" y="597" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#596675">Mid-market</text>
  <rect x="1098" y="585" width="13" height="13" rx="3" fill="#9AD9DB"/>
  <text x="1119" y="597" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#596675">SMB</text>

  <rect x="845" y="260" width="130" height="52" rx="18" fill="#F3F8FA"/>
  <text x="863" y="282" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8795">Palette rule</text>
  <text x="863" y="303" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#006D77">Monochrome</text>
</svg>
```

## Avoid in this skill
- ❌ Rainbow category colors for the doughnut chart; they destroy tonal harmony and compete with the focus highlight.
- ❌ Skinny default bars with large gaps; this weakens data presence and makes dense monthly data feel scattered.
- ❌ Heavy axis lines, tick marks, and dark gridlines; keep the chart scaffolding quiet so the data remains primary.
- ❌ Applying filters to `<line>` gridlines; PPT translation drops line filters, so keep gridlines simple.
- ❌ Text labels without explicit `width`; labels may clip or reflow unpredictably in PowerPoint.

## Composition notes
- Keep the left 55–60% of the slide for the primary column chart; it carries the insight narrative and needs breathing room.
- Use the right card for secondary distribution context, such as market mix, customer segment, or portfolio share.
- Reserve the strongest accent color for exactly one data point or one callout; all other marks should stay in the same subdued family.
- Maintain a pale background, soft card shadows, and low-contrast gridlines to create a polished consulting-deck feel.