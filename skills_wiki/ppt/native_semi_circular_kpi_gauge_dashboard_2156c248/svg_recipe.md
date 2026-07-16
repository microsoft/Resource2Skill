# SVG Recipe — Native Semi-Circular KPI Gauge Dashboard

## Visual mechanism
Create each KPI as a half-donut gauge: a pale gray semi-circular track underneath a colored progress arc, with the percentage centered inside the arch and explanatory text below. Arrange four identical gauge cards on a strict horizontal grid so the slide reads like a polished executive dashboard.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 4× `<rect>` for rounded white KPI cards with soft shadows
- 4× `<path>` for pale gray semi-circular gauge tracks
- 4× `<path>` for colored semi-circular progress arcs
- 4× `<circle>` for small endpoint beads that make the arc feel intentional and premium
- 4× `<line>` for subtle baseline dividers under each KPI label
- 1× `<text>` for the slide title
- 4× `<text>` for large KPI percentages
- 4× `<text>` for KPI labels
- 4× `<text>` for KPI descriptions
- 1× `<filter id="cardShadow">` applied to cards
- 1× `<filter id="softGlow">` applied to progress arcs/end beads
- 4× `<linearGradient>` for differentiated KPI arc colors

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>

    <linearGradient id="gradTeal" x1="80" y1="385" x2="300" y2="285" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#38A3A5"/>
      <stop offset="100%" stop-color="#57CC99"/>
    </linearGradient>
    <linearGradient id="gradGreen" x1="380" y1="385" x2="600" y2="280" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#57CC99"/>
      <stop offset="100%" stop-color="#80ED99"/>
    </linearGradient>
    <linearGradient id="gradMint" x1="680" y1="385" x2="900" y2="285" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2BB3B1"/>
      <stop offset="100%" stop-color="#7EF5D1"/>
    </linearGradient>
    <linearGradient id="gradBlue" x1="980" y1="385" x2="1200" y2="285" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#22577A"/>
      <stop offset="100%" stop-color="#38A3A5"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FAFAFA"/>

  <text x="72" y="78" width="1140" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="700" fill="#30343B">
    Customer Service Team Benchmarking Dashboard
  </text>
  <text x="74" y="113" width="980" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="400" fill="#8A93A0">
    Four core operating metrics shown as native editable semi-circular KPI gauges
  </text>

  <rect x="62" y="175" width="256" height="390" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="362" y="175" width="256" height="390" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="662" y="175" width="256" height="390" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="962" y="175" width="256" height="390" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <!-- Gauge 1: 35% -->
  <path d="M 85 385 A 105 105 0 0 1 295 385"
        fill="none" stroke="#E8EBEF" stroke-width="24" stroke-linecap="round"/>
  <path d="M 85 385 A 105 105 0 0 1 142.3 291.4"
        fill="none" stroke="url(#gradTeal)" stroke-width="24" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="142.3" cy="291.4" r="9" fill="#38A3A5"/>
  <text x="100" y="376" width="180" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="48" font-weight="800" fill="#263238">35%</text>
  <line x1="108" y1="431" x2="272" y2="431" stroke="#EEF1F4" stroke-width="2"/>
  <text x="82" y="470" width="216" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#30343B">Response Rate</text>
  <text x="92" y="504" width="196" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="400" fill="#8A93A0">First contact within 1hr</text>

  <!-- Gauge 2: 50% -->
  <path d="M 385 385 A 105 105 0 0 1 595 385"
        fill="none" stroke="#E8EBEF" stroke-width="24" stroke-linecap="round"/>
  <path d="M 385 385 A 105 105 0 0 1 490 280"
        fill="none" stroke="url(#gradGreen)" stroke-width="24" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="490" cy="280" r="9" fill="#80ED99"/>
  <text x="400" y="376" width="180" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="48" font-weight="800" fill="#263238">50%</text>
  <line x1="408" y1="431" x2="572" y2="431" stroke="#EEF1F4" stroke-width="2"/>
  <text x="382" y="470" width="216" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#30343B">Resolution</text>
  <text x="392" y="504" width="196" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="400" fill="#8A93A0">Solved on first call</text>

  <!-- Gauge 3: 72% -->
  <path d="M 685 385 A 105 105 0 0 1 895 385"
        fill="none" stroke="#E8EBEF" stroke-width="24" stroke-linecap="round"/>
  <path d="M 685 385 A 105 105 0 0 1 856.4 303.6"
        fill="none" stroke="url(#gradMint)" stroke-width="24" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="856.4" cy="303.6" r="9" fill="#57CC99"/>
  <text x="700" y="376" width="180" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="48" font-weight="800" fill="#263238">72%</text>
  <line x1="708" y1="431" x2="872" y2="431" stroke="#EEF1F4" stroke-width="2"/>
  <text x="682" y="470" width="216" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#30343B">CSAT Score</text>
  <text x="692" y="504" width="196" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="400" fill="#8A93A0">Positive feedback ratio</text>

  <!-- Gauge 4: 98% -->
  <path d="M 985 385 A 105 105 0 0 1 1195 385"
        fill="none" stroke="#E8EBEF" stroke-width="24" stroke-linecap="round"/>
  <path d="M 985 385 A 105 105 0 0 1 1194.8 378.4"
        fill="none" stroke="url(#gradBlue)" stroke-width="24" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="1194.8" cy="378.4" r="9" fill="#22577A"/>
  <text x="1000" y="376" width="180" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="48" font-weight="800" fill="#263238">98%</text>
  <line x1="1008" y1="431" x2="1172" y2="431" stroke="#EEF1F4" stroke-width="2"/>
  <text x="982" y="470" width="216" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#30343B">Uptime</text>
  <text x="992" y="504" width="196" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="400" fill="#8A93A0">System availability</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` or clipping non-image shapes to hide the bottom half of a donut; draw the visible semi-circle directly as an editable `<path>`.
- ❌ Using `<text>` without `width`; PowerPoint may render different wrapping or sizing.
- ❌ Building the gauge from many tiny arc segments; it becomes hard to edit and may look uneven.
- ❌ Applying filters to `<line>` elements; use filters on `<rect>`, `<path>`, `<circle>`, or `<text>` only.
- ❌ Relying on chart objects in SVG; reproduce the donut-gauge look with native paths for predictable editable PowerPoint geometry.

## Composition notes
- Keep the top 20% of the slide for the title and subtitle; the gauges should begin around the upper-middle of the canvas.
- Align all four gauge baselines on the same y-axis so the dashboard feels rigorous and data-driven.
- Use white cards on a very light gray background for executive cleanliness; reserve saturated color only for the progress arcs.
- Place the percentage inside the arch, the KPI name below the gauge, and the description in muted gray to preserve a clear text hierarchy.