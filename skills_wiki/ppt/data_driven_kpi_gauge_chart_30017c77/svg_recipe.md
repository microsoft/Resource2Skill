# SVG Recipe — Data-Driven KPI Gauge Chart

## Visual mechanism
A KPI is shown as a premium speedometer: a thick semi-circular track, a colored progress arc, and a needle pivoting from the center to the measured percentage. The number is repeated as a large executive label so the viewer gets both instant visual status and exact value.

## SVG primitives needed
- 2× `<rect>` for the slide background and raised dashboard card
- 5× `<path>` for the semi-circular gauge track, progress arc, outer status bands, and needle shape
- N× short `<path>` strokes for tick marks along the gauge
- 3× `<circle>` for the pivot hub, inner highlight, and subtle glow
- 10× `<text>` for title, KPI name, value label, status label, scale labels, and legend captions
- 2× `<linearGradient>` for the dark canvas/card finish and KPI progress stroke
- 1× `<radialGradient>` for the pivot highlight
- 2× `<filter>` using blur/offset for card shadow and needle/progress glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#101827"/>
      <stop offset="55%" stop-color="#172033"/>
      <stop offset="100%" stop-color="#0B1020"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="300" y1="90" x2="980" y2="650">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.11"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>

    <linearGradient id="kpiArcGrad" x1="380" y1="430" x2="900" y2="210">
      <stop offset="0%" stop-color="#F97316"/>
      <stop offset="55%" stop-color="#FDBA2D"/>
      <stop offset="100%" stop-color="#22C55E"/>
    </linearGradient>

    <radialGradient id="hubGrad" cx="45%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="42%" stop-color="#CBD5E1"/>
      <stop offset="100%" stop-color="#475569"/>
    </radialGradient>

    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="80" y="76" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F8FAFC">
    Portfolio Performance Gauge
  </text>
  <text x="82" y="112" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#94A3B8">
    Data-driven KPI view · Current quarter attainment against target
  </text>

  <rect x="250" y="128" width="780" height="500" rx="34" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#cardShadow)"/>

  <text x="330" y="190" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="650" fill="#E2E8F0">
    Revenue target attainment
  </text>
  <text x="330" y="220" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#94A3B8">
    Gauge value example: 68% of quarterly plan
  </text>

  <!-- Outer qualitative bands: red/orange/green status ranges -->
  <path d="M 340 430 A 300 300 0 0 1 640 130" fill="none" stroke="#EF4444" stroke-width="10" stroke-linecap="round" opacity="0.85"/>
  <path d="M 640 130 A 300 300 0 0 1 883 254" fill="none" stroke="#F59E0B" stroke-width="10" stroke-linecap="round" opacity="0.85"/>
  <path d="M 883 254 A 300 300 0 0 1 940 430" fill="none" stroke="#22C55E" stroke-width="10" stroke-linecap="round" opacity="0.85"/>

  <!-- Main gauge track and KPI arc. For KPI=68, endpoint angle = 180 - 0.68*180 = 57.6 degrees. -->
  <path d="M 380 430 A 260 260 0 0 1 900 430" fill="none" stroke="#334155" stroke-width="38" stroke-linecap="round"/>
  <path d="M 380 430 A 260 260 0 0 1 779 211" fill="none" stroke="url(#kpiArcGrad)" stroke-width="38" stroke-linecap="round" filter="url(#softGlow)"/>

  <!-- Tick marks along the semicircle -->
  <path d="M 380 430 L 350 430" stroke="#64748B" stroke-width="3" stroke-linecap="round"/>
  <path d="M 414 299 L 386 287" stroke="#475569" stroke-width="2" stroke-linecap="round"/>
  <path d="M 510 203 L 494 176" stroke="#475569" stroke-width="2" stroke-linecap="round"/>
  <path d="M 640 170 L 640 138" stroke="#64748B" stroke-width="3" stroke-linecap="round"/>
  <path d="M 770 203 L 786 176" stroke="#475569" stroke-width="2" stroke-linecap="round"/>
  <path d="M 866 299 L 894 287" stroke="#475569" stroke-width="2" stroke-linecap="round"/>
  <path d="M 900 430 L 930 430" stroke="#64748B" stroke-width="3" stroke-linecap="round"/>

  <!-- Needle: triangular pointer aimed at 68% endpoint -->
  <path d="M 630.7 424.1 L 779 211 L 649.3 435.9 Z" fill="#0F172A" stroke="#CBD5E1" stroke-width="1.2" filter="url(#softGlow)"/>
  <circle cx="640" cy="430" r="38" fill="#0F172A" stroke="#64748B" stroke-width="2"/>
  <circle cx="640" cy="430" r="24" fill="url(#hubGrad)"/>
  <circle cx="631" cy="421" r="6" fill="#FFFFFF" opacity="0.65"/>

  <text x="344" y="475" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#CBD5E1" text-anchor="middle">
    0%
  </text>
  <text x="640" y="112" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#CBD5E1" text-anchor="middle">
    50%
  </text>
  <text x="936" y="475" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#CBD5E1" text-anchor="middle">
    100%
  </text>

  <text x="512" y="548" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="800" fill="#F8FAFC" text-anchor="middle">
    68%
  </text>
  <text x="640" y="585" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="650" fill="#FDBA2D" text-anchor="middle">
    On track, below stretch target
  </text>

  <circle cx="815" cy="178" r="6" fill="#EF4444"/>
  <text x="832" y="184" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#CBD5E1">Risk</text>
  <circle cx="815" cy="204" r="6" fill="#F59E0B"/>
  <text x="832" y="210" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#CBD5E1">On track</text>
  <circle cx="815" cy="230" r="6" fill="#22C55E"/>
  <text x="832" y="236" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#CBD5E1">Target zone</text>
</svg>
```

## Avoid in this skill
- ❌ Using a real SVG `<path>` pie/doughnut generated as hundreds of tiny slices; it becomes hard to edit and visually noisy in PowerPoint.
- ❌ Using `marker-end` for the needle tip; build the needle as a filled `<path>` triangle instead.
- ❌ Applying `filter` to `<line>` tick marks; use short stroked `<path>` elements if you need editable tick strokes.
- ❌ Using `<mask>` to hide the bottom half of a circle; draw the semi-circle directly as an arc path.
- ❌ Omitting `width` on text labels; PowerPoint translation needs explicit text widths for reliable layout.

## Composition notes
- Keep the gauge centered in a card with generous top breathing room; the arc should occupy roughly 55–65% of the card width.
- Map data with `angle = 180 - value/100 * 180`; endpoint is `cx + r*cos(angle)`, `cy - r*sin(angle)`.
- Use a muted full track plus one vivid progress arc; the number label should match or harmonize with the active arc color.
- Reserve the lower third of the card for the large KPI value and short status sentence; do not crowd the gauge arc with long annotations.