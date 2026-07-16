# SVG Recipe — Impact-First KPI Storytelling

## Visual mechanism
Lead with one oversized business outcome, then use small, quiet “proof” visuals to explain why the number is credible. The slide should feel like an executive headline: high contrast, large typography, disciplined color, and only two or three supporting signals.

## SVG primitives needed
- 1× `<rect>` for the full-slide blue gradient background
- 3× `<path>` for subtle decorative background arcs and the gold hero underline
- 1× `<text>` hero KPI group using nested `<tspan>` for the dominant impact number
- 6× `<text>` for eyebrow, subtitle, proof labels, chart labels, and funnel labels
- 2× `<rect>` for glassy KPI proof cards
- 1× `<path>` for the revenue growth curve
- 2× `<circle>` for chart start/end markers
- 4× `<line>` for minimalist chart axes and guide ticks
- 3× `<path>` trapezoids for the conversion funnel
- 1× `<linearGradient>` for the executive blue background
- 1× `<linearGradient>` for the gold KPI highlight
- 1× `<filter id="softShadow">` applied to proof cards
- 1× `<filter id="goldGlow">` applied to the hero number and growth curve

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#083E76"/>
      <stop offset="55%" stop-color="#0D6BB4"/>
      <stop offset="100%" stop-color="#064A86"/>
    </linearGradient>

    <linearGradient id="goldFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFE37A"/>
      <stop offset="45%" stop-color="#FFCC00"/>
      <stop offset="100%" stop-color="#F3A800"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBlue)"/>

  <path d="M-120 625 C190 510 350 745 650 610 C900 500 1035 585 1410 430"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="70"/>
  <path d="M760 -120 C960 30 930 175 1150 245 C1235 272 1320 265 1390 232"
        fill="none" stroke="#FFCC00" stroke-opacity="0.13" stroke-width="92"/>
  <path d="M-90 95 C135 35 245 82 430 8"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="44"/>

  <text x="92" y="104" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3" fill="#FFFFFF" opacity="0.82">
    Q4 COMMERCIAL IMPACT
  </text>

  <text x="88" y="326" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118" font-weight="800" fill="url(#goldFill)" filter="url(#goldGlow)">
    <tspan x="88" dy="0">$1.1M</tspan>
  </text>

  <path d="M94 352 C218 374 438 374 594 346"
        fill="none" stroke="#FFCC00" stroke-width="10" stroke-linecap="round" opacity="0.95"/>

  <text x="94" y="417" width="650" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="37" font-weight="500" fill="#FFFFFF">
    weekly sales captured after campaign relaunch
  </text>

  <text x="96" y="472" width="590" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" fill="#DCEFFF" opacity="0.92">
    The board takeaway: revenue impact landed first; the operating drivers are summarized on the right.
  </text>

  <rect x="760" y="86" width="420" height="238" rx="28"
        fill="#FFFFFF" fill-opacity="0.13" stroke="#FFFFFF" stroke-opacity="0.22"
        filter="url(#softShadow)"/>
  <text x="798" y="134" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" fill="#FFFFFF">
    Revenue is soaring 83%
  </text>
  <line x1="814" y1="260" x2="1120" y2="260" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="2"/>
  <line x1="814" y1="172" x2="814" y2="260" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="2"/>
  <line x1="814" y1="214" x2="1120" y2="214" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1"/>
  <line x1="814" y1="172" x2="1120" y2="172" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1"/>
  <path d="M816 248 C880 238 920 222 968 203 C1018 184 1055 151 1116 126"
        fill="none" stroke="#FFCC00" stroke-width="7" stroke-linecap="round"
        filter="url(#goldGlow)"/>
  <circle cx="816" cy="248" r="8" fill="#FFFFFF"/>
  <circle cx="1116" cy="126" r="11" fill="#FFCC00"/>
  <text x="792" y="291" width="95" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#DCEFFF">$600K</text>
  <text x="1070" y="291" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#FFCC00">$1.1M</text>

  <rect x="760" y="370" width="420" height="250" rx="28"
        fill="#FFFFFF" fill-opacity="0.13" stroke="#FFFFFF" stroke-opacity="0.22"
        filter="url(#softShadow)"/>
  <text x="798" y="418" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" fill="#FFFFFF">
    Acquisition funnel created the lift
  </text>

  <path d="M820 456 L1120 456 L1088 502 L852 502 Z" fill="#FFCC00" fill-opacity="0.96"/>
  <path d="M855 515 L1085 515 L1053 561 L887 561 Z" fill="#FFE37A" fill-opacity="0.86"/>
  <path d="M890 574 L1050 574 L1020 616 L920 616 Z" fill="#FFFFFF" fill-opacity="0.92"/>

  <text x="842" y="487" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="800" fill="#083E76">330,000 engagements</text>
  <text x="890" y="546" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="800" fill="#083E76">44,000 visitors</text>
  <text x="920" y="603" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="800" fill="#083E76">323% leads</text>

  <text x="92" y="645" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#DCEFFF" opacity="0.82">
    One slide, one message: impact first — proof second.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense KPI dashboards with many equal-weight numbers; the technique depends on one dominant conclusion.
- ❌ Pie charts, table grids, and tiny legends that force executives to decode the slide.
- ❌ Decorative photos or illustrations that compete with the hero KPI.
- ❌ `marker-end` on `<path>` for chart arrows; draw arrowheads manually with small `<path>` triangles if needed.
- ❌ Filters on `<line>` elements; use filters on cards, paths, circles, or text instead.

## Composition notes
- Keep the hero KPI on the left or center-left, occupying most of the visual weight; supporting proof should feel secondary.
- Use a strict palette: deep executive blue, white, and one gold accent for the result and the most important chart signal.
- Reserve at least 35–45% negative space so the slide reads instantly from the back of a boardroom.
- Proof visuals should be minimalist and narrative-driven: one growth line, one funnel, or one driver stack — never a full analytics dashboard.