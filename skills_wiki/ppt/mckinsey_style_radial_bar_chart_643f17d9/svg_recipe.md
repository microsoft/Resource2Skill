# SVG Recipe — McKinsey-Style Radial Bar Chart

## Visual mechanism
Show 4–8 category percentages as concentric circular bars, each starting from the same 12 o’clock position and sweeping clockwise through a shared maximum span, usually 270°. The result feels more editorial and executive than a default bar chart while still allowing quick part-to-whole comparison.

## SVG primitives needed
- 1× `<rect>` for the clean slide background
- 1× `<rect>` for a thin McKinsey-style title accent rule
- 7× pale `<path>` arcs for the 100% reference tracks
- 7× colored `<path>` arcs for the actual category values
- 7× `<circle>` endpoint badges for value labels
- 1× `<circle>` center hub to create a polished focal point
- Multiple `<text>` elements with explicit `width=` for title, subtitle, legend labels, and value labels
- 2× `<linearGradient>` definitions for dark-blue and cyan-blue arc strokes
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for endpoint badges and center hub
- Optional 1× decorative `<path>` or `<circle>` in very low opacity behind the chart for depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkBlueGrad" x1="520" y1="120" x2="990" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#003A70"/>
      <stop offset="100%" stop-color="#0063A6"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="610" y1="170" x2="1000" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00AFEF"/>
      <stop offset="100%" stop-color="#67D5FF"/>
    </linearGradient>
    <linearGradient id="trackGrad" x1="520" y1="120" x2="1010" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#DCEAF5"/>
      <stop offset="100%" stop-color="#F3F8FC"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <path d="M980 80 C1105 118 1165 215 1138 335 C1112 456 1005 562 860 588 C742 609 641 574 610 500 C579 426 625 330 710 236 C784 154 871 47 980 80 Z"
        fill="#EAF5FB" opacity="0.55"/>

  <rect x="80" y="82" width="64" height="6" fill="#00AFEF"/>
  <text x="80" y="132" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#111827">
    Technology impact by sector
  </text>
  <text x="80" y="184" width="465" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#4B5563">
    Share of transformation value enabled by technology, expressed as radial bars over a 270° maximum span.
  </text>

  <text x="80" y="262" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#6B7280" letter-spacing="1.4">
    SECTOR RESULTS
  </text>

  <rect x="82" y="292" width="9" height="9" rx="2" fill="#004685"/>
  <text x="105" y="302" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#111827">Financial services</text>
  <text x="420" y="302" width="55" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">71%</text>

  <rect x="82" y="326" width="9" height="9" rx="2" fill="#004685"/>
  <text x="105" y="336" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#111827">Telecom, media &amp; technology</text>
  <text x="420" y="336" width="55" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">70%</text>

  <rect x="82" y="360" width="9" height="9" rx="2" fill="#00AFEF"/>
  <text x="105" y="370" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#111827">Consumer</text>
  <text x="420" y="370" width="55" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">39%</text>

  <rect x="82" y="394" width="9" height="9" rx="2" fill="#00AFEF"/>
  <text x="105" y="404" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#111827">Life sciences</text>
  <text x="420" y="404" width="55" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">28%</text>

  <rect x="82" y="428" width="9" height="9" rx="2" fill="#00AFEF"/>
  <text x="105" y="438" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#111827">Travel, logistics &amp; infrastructure</text>
  <text x="420" y="438" width="55" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">22%</text>

  <rect x="82" y="462" width="9" height="9" rx="2" fill="#00AFEF"/>
  <text x="105" y="472" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#111827">Global energy &amp; materials</text>
  <text x="420" y="472" width="55" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">15%</text>

  <rect x="82" y="496" width="9" height="9" rx="2" fill="#00AFEF"/>
  <text x="105" y="506" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#111827">Advanced industries</text>
  <text x="420" y="506" width="55" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">9%</text>

  <!-- 270-degree reference tracks, centered at 750,375 -->
  <path d="M750 123 A252 252 0 1 1 498 375" fill="none" stroke="url(#trackGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 153 A222 222 0 1 1 528 375" fill="none" stroke="url(#trackGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 183 A192 192 0 1 1 558 375" fill="none" stroke="url(#trackGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 213 A162 162 0 1 1 588 375" fill="none" stroke="url(#trackGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 243 A132 132 0 1 1 618 375" fill="none" stroke="url(#trackGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 273 A102 102 0 1 1 648 375" fill="none" stroke="url(#trackGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 303 A72 72 0 1 1 678 375" fill="none" stroke="url(#trackGrad)" stroke-width="18" stroke-linecap="round"/>

  <!-- Value arcs: percentage × 270 degrees -->
  <path d="M750 123 A252 252 0 1 1 699 622" fill="none" stroke="url(#darkBlueGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 153 A222 222 0 1 1 715 594" fill="none" stroke="url(#darkBlueGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 183 A192 192 0 0 1 935 426" fill="none" stroke="url(#cyanGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 213 A162 162 0 0 1 907 335" fill="none" stroke="url(#cyanGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 243 A132 132 0 0 1 864 308" fill="none" stroke="url(#cyanGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 273 A102 102 0 0 1 816 297" fill="none" stroke="url(#cyanGrad)" stroke-width="18" stroke-linecap="round"/>
  <path d="M750 303 A72 72 0 0 1 780 309" fill="none" stroke="url(#cyanGrad)" stroke-width="18" stroke-linecap="round"/>

  <circle cx="750" cy="375" r="38" fill="#FFFFFF" stroke="#E5EEF6" stroke-width="2" filter="url(#softShadow)"/>
  <text x="716" y="368" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#6B7280">MAX</text>
  <text x="716" y="391" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#003A70">270°</text>

  <circle cx="699" cy="622" r="20" fill="#FFFFFF" stroke="#004685" stroke-width="2" filter="url(#softShadow)"/>
  <text x="679" y="629" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#111827">71</text>

  <circle cx="715" cy="594" r="19" fill="#FFFFFF" stroke="#004685" stroke-width="2" filter="url(#softShadow)"/>
  <text x="696" y="600" width="38" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">70</text>

  <circle cx="935" cy="426" r="18" fill="#FFFFFF" stroke="#00AFEF" stroke-width="2" filter="url(#softShadow)"/>
  <text x="917" y="432" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">39</text>

  <circle cx="907" cy="335" r="17" fill="#FFFFFF" stroke="#00AFEF" stroke-width="2"/>
  <text x="890" y="341" width="34" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#111827">28</text>

  <circle cx="864" cy="308" r="17" fill="#FFFFFF" stroke="#00AFEF" stroke-width="2"/>
  <text x="847" y="314" width="34" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#111827">22</text>

  <circle cx="816" cy="297" r="16" fill="#FFFFFF" stroke="#00AFEF" stroke-width="2"/>
  <text x="800" y="303" width="32" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#111827">15</text>

  <circle cx="780" cy="309" r="15" fill="#FFFFFF" stroke="#00AFEF" stroke-width="2"/>
  <text x="765" y="315" width="30" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#111827">9</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to create donut rings; use stroked arc `<path>` elements instead so the arcs remain editable.
- ❌ Do not rely on `<textPath>` for curved labels; PowerPoint translation will drop it. Place labels manually near arc endpoints.
- ❌ Do not use `marker-end` arrowheads for radial annotations; if callouts are needed, use editable `<line>` elements without inherited markers.
- ❌ Do not apply filters to `<line>` elements; use shadows only on `<circle>`, `<rect>`, `<path>`, or `<text>`.
- ❌ Do not overcrowd with more than 8 rings; radial comparison becomes hard to read and loses the McKinsey-style clarity.

## Composition notes
- Put the radial chart on the right two-thirds of the slide and reserve the left third for the headline, explanatory subtitle, and compact legend.
- Use a shared start angle and equal ring spacing; the visual comparison depends on every arc beginning from the same 12 o’clock anchor.
- Highlight the top one or two categories in dark navy, then use cyan or lighter blue for the remaining categories to create hierarchy.
- Keep generous negative space around the open left side of the rings; the incomplete 270° structure should feel intentional, not like a broken donut chart.