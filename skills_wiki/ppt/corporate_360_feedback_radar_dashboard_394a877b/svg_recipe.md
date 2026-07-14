# SVG Recipe — Corporate 360° Feedback Radar Dashboard

## Visual mechanism
A central editable radar/spider chart compares two 360° feedback series using semi-transparent overlapping polygons, while a right-side stack of KPI cards translates the chart into executive-ready scores and coaching insights. The contrast between organic radial geometry and disciplined card layout creates a polished corporate dashboard.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× large low-opacity `<circle>` for subtle decorative chart atmosphere
- 5× `<path>` for concentric radar grid rings
- 8× `<line>` for radar axes
- 2× `<path>` for editable radar data polygons with translucent fills
- 16× `<circle>` for series point markers
- 8× `<text>` for radar category labels
- 5× `<text>` for radial scale labels
- 2× `<rect>` + 2× `<circle>` + 2× `<text>` for the legend
- 3× shadowed `<rect>` for KPI cards
- 3× narrow accent `<rect>` bars on KPI cards
- Multiple `<text>` elements with explicit `width` for titles, scores, labels, and insight copy
- 2× `<linearGradient>` for premium card accents and title underline
- 1× `<radialGradient>` for the soft background glow
- 1× `<filter id="cardShadow">` applied to KPI cards
- 1× `<filter id="softGlow">` applied to the background decorative circle

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="titleRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#006973"/>
      <stop offset="60%" stop-color="#5FB4AF"/>
      <stop offset="100%" stop-color="#96C850"/>
    </linearGradient>
    <linearGradient id="cardAccent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F6FBFA"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>
    <radialGradient id="radarGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#CDEDEA" stop-opacity="0.75"/>
      <stop offset="70%" stop-color="#DFF3E1" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <circle cx="360" cy="390" r="310" fill="url(#radarGlow)" filter="url(#softGlow)"/>

  <text x="64" y="58" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#006973">
    360° Feedback Radar Dashboard
  </text>
  <text x="66" y="90" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#5C7376">
    Jane Doe · FY26 Leadership Review · Self vs. Manager & Peers
  </text>
  <rect x="64" y="108" width="420" height="5" rx="2.5" fill="url(#titleRule)"/>

  <!-- Radar grid -->
  <path d="M360 343 L393 357 L407 390 L393 423 L360 437 L327 423 L313 390 L327 357 Z" fill="none" stroke="#DDE9E8" stroke-width="1.2"/>
  <path d="M360 296 L426 324 L454 390 L426 456 L360 484 L294 456 L266 390 L294 324 Z" fill="none" stroke="#DDE9E8" stroke-width="1.2"/>
  <path d="M360 249 L460 290 L501 390 L460 490 L360 531 L260 490 L219 390 L260 290 Z" fill="none" stroke="#DDE9E8" stroke-width="1.2"/>
  <path d="M360 202 L493 257 L548 390 L493 523 L360 578 L227 523 L172 390 L227 257 Z" fill="none" stroke="#C9DCDA" stroke-width="1.3"/>
  <path d="M360 155 L526 224 L595 390 L526 556 L360 625 L194 556 L125 390 L194 224 Z" fill="none" stroke="#ABCBC8" stroke-width="1.5"/>

  <!-- Radar axes -->
  <line x1="360" y1="390" x2="360" y2="155" stroke="#B7D2D0" stroke-width="1.2"/>
  <line x1="360" y1="390" x2="526" y2="224" stroke="#B7D2D0" stroke-width="1.2"/>
  <line x1="360" y1="390" x2="595" y2="390" stroke="#B7D2D0" stroke-width="1.2"/>
  <line x1="360" y1="390" x2="526" y2="556" stroke="#B7D2D0" stroke-width="1.2"/>
  <line x1="360" y1="390" x2="360" y2="625" stroke="#B7D2D0" stroke-width="1.2"/>
  <line x1="360" y1="390" x2="194" y2="556" stroke="#B7D2D0" stroke-width="1.2"/>
  <line x1="360" y1="390" x2="125" y2="390" stroke="#B7D2D0" stroke-width="1.2"/>
  <line x1="360" y1="390" x2="194" y2="224" stroke="#B7D2D0" stroke-width="1.2"/>

  <!-- Radar data polygons -->
  <path d="M360 202 L476 274 L548 390 L460 490 L360 625 L211 540 L196 390 L227 257 Z"
        fill="#5FB4AF" fill-opacity="0.16" stroke="#5FB4AF" stroke-width="3"/>
  <path d="M360 179 L493 257 L525 390 L493 523 L360 616 L227 523 L149 390 L234 264 Z"
        fill="#96C850" fill-opacity="0.28" stroke="#96C850" stroke-width="3"/>

  <!-- Point markers: self -->
  <circle cx="360" cy="202" r="5" fill="#FFFFFF" stroke="#5FB4AF" stroke-width="3"/>
  <circle cx="476" cy="274" r="5" fill="#FFFFFF" stroke="#5FB4AF" stroke-width="3"/>
  <circle cx="548" cy="390" r="5" fill="#FFFFFF" stroke="#5FB4AF" stroke-width="3"/>
  <circle cx="460" cy="490" r="5" fill="#FFFFFF" stroke="#5FB4AF" stroke-width="3"/>
  <circle cx="360" cy="625" r="5" fill="#FFFFFF" stroke="#5FB4AF" stroke-width="3"/>
  <circle cx="211" cy="540" r="5" fill="#FFFFFF" stroke="#5FB4AF" stroke-width="3"/>
  <circle cx="196" cy="390" r="5" fill="#FFFFFF" stroke="#5FB4AF" stroke-width="3"/>
  <circle cx="227" cy="257" r="5" fill="#FFFFFF" stroke="#5FB4AF" stroke-width="3"/>

  <!-- Point markers: others -->
  <circle cx="360" cy="179" r="5" fill="#FFFFFF" stroke="#96C850" stroke-width="3"/>
  <circle cx="493" cy="257" r="5" fill="#FFFFFF" stroke="#96C850" stroke-width="3"/>
  <circle cx="525" cy="390" r="5" fill="#FFFFFF" stroke="#96C850" stroke-width="3"/>
  <circle cx="493" cy="523" r="5" fill="#FFFFFF" stroke="#96C850" stroke-width="3"/>
  <circle cx="360" cy="616" r="5" fill="#FFFFFF" stroke="#96C850" stroke-width="3"/>
  <circle cx="227" cy="523" r="5" fill="#FFFFFF" stroke="#96C850" stroke-width="3"/>
  <circle cx="149" cy="390" r="5" fill="#FFFFFF" stroke="#96C850" stroke-width="3"/>
  <circle cx="234" cy="264" r="5" fill="#FFFFFF" stroke="#96C850" stroke-width="3"/>

  <!-- Category labels -->
  <text x="300" y="137" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#006973">Leadership</text>
  <text x="535" y="216" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#006973">Adaptability</text>
  <text x="604" y="395" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#006973">Relationships</text>
  <text x="514" y="582" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#006973">Analytical Thinking</text>
  <text x="318" y="658" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#006973">Integrity</text>
  <text x="85" y="582" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#006973">Teamwork</text>
  <text x="34" y="395" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#006973">Decision Making</text>
  <text x="70" y="216" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#006973">Communication</text>

  <!-- Scale labels -->
  <text x="372" y="346" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F9294">1</text>
  <text x="372" y="299" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F9294">2</text>
  <text x="372" y="252" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F9294">3</text>
  <text x="372" y="205" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F9294">4</text>
  <text x="372" y="158" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F9294">5</text>

  <!-- Legend -->
  <rect x="220" y="668" width="300" height="30" rx="15" fill="#F6FAF9" stroke="#E1ECEA"/>
  <circle cx="246" cy="683" r="6" fill="#5FB4AF"/>
  <text x="260" y="688" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#315A5E">Self Assessment</text>
  <circle cx="395" cy="683" r="6" fill="#96C850"/>
  <text x="409" y="688" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#315A5E">Manager + Peers</text>

  <!-- KPI card 1 -->
  <rect x="730" y="150" width="470" height="132" rx="22" fill="url(#cardAccent)" stroke="#E5EFED" filter="url(#cardShadow)"/>
  <rect x="730" y="150" width="8" height="132" rx="4" fill="#96C850"/>
  <text x="760" y="188" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#96C850">4.13</text>
  <text x="900" y="178" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#006973">Overall external rating</text>
  <text x="900" y="207" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#637577">
    Peers rate Jane strongest in leadership, integrity, and decision quality.
  </text>
  <text x="900" y="244" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#96C850">+0.07 above self-assessment</text>

  <!-- KPI card 2 -->
  <rect x="730" y="315" width="470" height="132" rx="22" fill="url(#cardAccent)" stroke="#E5EFED" filter="url(#cardShadow)"/>
  <rect x="730" y="315" width="8" height="132" rx="4" fill="#5FB4AF"/>
  <text x="760" y="353" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#5FB4AF">4.06</text>
  <text x="900" y="343" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#006973">Self assessment average</text>
  <text x="900" y="372" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#637577">
    Self-view is well calibrated, with slightly lower confidence in analytical thinking.
  </text>
  <text x="900" y="409" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#5FB4AF">Strongest self-score: Integrity</text>

  <!-- KPI card 3 -->
  <rect x="730" y="480" width="470" height="132" rx="22" fill="url(#cardAccent)" stroke="#E5EFED" filter="url(#cardShadow)"/>
  <rect x="730" y="480" width="8" height="132" rx="4" fill="#006973"/>
  <text x="760" y="518" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#006973">+1.0</text>
  <text x="900" y="508" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#006973">Largest positive perception gap</text>
  <text x="900" y="537" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#637577">
    Analytical thinking is rated materially higher by others than by Jane herself.
  </text>
  <text x="900" y="574" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#006973">Coaching theme: claim analytical authority</text>
</svg>
```

## Avoid in this skill
- ❌ Rasterizing the radar chart as a single `<image>`; keep grid rings, axes, polygons, and labels editable.
- ❌ Using `<polygon>` or `<use>` for repeated grid shapes; draw explicit editable `<path>` elements instead.
- ❌ Applying `marker-end` to radar axes or callout lines; if arrows are needed, use plain `<line>` plus custom triangle paths.
- ❌ Omitting `width` on `<text>` elements; PowerPoint text boxes may clip or reflow unexpectedly.
- ❌ Applying filters to `<line>` elements; use filters only on cards, paths, circles, ellipses, rects, or text.

## Composition notes
- Reserve the left 45–50% of the slide for a square radar area; keep labels outside the outer ring with generous breathing room.
- Put KPI cards in a disciplined vertical stack on the right, aligned to one strong x-axis and lifted with subtle shadows.
- Use translucent series fills so overlap remains readable; make outlines and point markers crisp for executive clarity.
- Repeat the two series colors in the legend, KPI scores, and accent bars to create a consistent visual rhythm.