# SVG Recipe — Narrative Data Progressive Highlighting (Setup-Conflict-Resolution)

## Visual mechanism
A dense multi-line chart is intentionally de-emphasized into pale context, while one narrative thread is recolored, thickened, and placed above the rest. A translucent vertical time band plus a short annotation turns the chart into a story beat: setup, conflict, or resolution.

## SVG primitives needed
- 2× <rect> for the slide background and elevated chart card
- 1× <linearGradient> for a premium off-white background wash
- 1× <filter id="cardShadow"> applied to the chart card
- 1× <filter id="lineGlow"> applied to the highlighted data path
- 1× <rect> for the narrative time-window highlight band
- 6–10× <line> for axes, gridlines, tick marks, and callout leader lines
- 6–12× <path> for muted background data series
- 1–3× <path> for the currently highlighted data series
- 1× <path> triangle for an editable callout arrowhead
- 3× <rect> for Setup / Conflict / Resolution stage chips
- 10–20× <text> for action title, subtitle, axis labels, stage chips, and annotations
- Optional 1× <circle> or <ellipse> for an emphasized peak point

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbfaf7"/>
      <stop offset="58%" stop-color="#f4f1eb"/>
      <stop offset="100%" stop-color="#ece7dc"/>
    </linearGradient>
    <linearGradient id="focusBandFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffe08a" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#ffbf3f" stop-opacity="0.20"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="lineGlow" x="-8%" y="-8%" width="116%" height="116%">
      <feGaussianBlur stdDeviation="2.8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="86" y="70" width="900" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#242424">
    …Except in Market C
  </text>
  <text x="88" y="106" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#666666">
    This market experienced a 30-year bubble that peaked dramatically in the early ’90s — while the rest of the market remained ordinary.
  </text>

  <rect x="890" y="48" width="88" height="30" rx="15" fill="#e9e6df"/>
  <text x="912" y="69" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#8c867b">SETUP</text>
  <rect x="988" y="48" width="104" height="30" rx="15" fill="#2c213f"/>
  <text x="1010" y="69" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">CONFLICT</text>
  <rect x="1102" y="48" width="120" height="30" rx="15" fill="#e9e6df"/>
  <text x="1123" y="69" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#8c867b">RESOLUTION</text>

  <rect x="80" y="135" width="1120" height="520" rx="28" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="112" y="174" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8a8a8a">GLOBAL HOME PRICE INDEX</text>

  <!-- chart grid -->
  <line x1="150" y1="585" x2="1145" y2="585" stroke="#1f1f1f" stroke-width="1.2"/>
  <line x1="150" y1="200" x2="150" y2="585" stroke="#1f1f1f" stroke-width="1.2"/>
  <line x1="150" y1="500" x2="1145" y2="500" stroke="#e9e9e9" stroke-width="1"/>
  <line x1="150" y1="415" x2="1145" y2="415" stroke="#e9e9e9" stroke-width="1"/>
  <line x1="150" y1="330" x2="1145" y2="330" stroke="#e9e9e9" stroke-width="1"/>
  <line x1="150" y1="245" x2="1145" y2="245" stroke="#e9e9e9" stroke-width="1"/>

  <!-- narrative time window: conflict period -->
  <rect x="420" y="200" width="305" height="385" fill="url(#focusBandFill)"/>
  <line x1="420" y1="200" x2="420" y2="585" stroke="#d7981d" stroke-width="1" stroke-dasharray="5 6" opacity="0.55"/>
  <line x1="725" y1="200" x2="725" y2="585" stroke="#d7981d" stroke-width="1" stroke-dasharray="5 6" opacity="0.55"/>

  <!-- muted context lines -->
  <path d="M150 520 C230 505, 300 492, 380 470 S560 430, 645 410 S840 365, 960 330 S1080 304, 1145 292" fill="none" stroke="#cfcfcf" stroke-width="2" opacity="0.72"/>
  <path d="M150 550 C245 540, 310 510, 390 498 S570 462, 650 432 S840 392, 960 356 S1080 325, 1145 310" fill="none" stroke="#cfcfcf" stroke-width="2" opacity="0.72"/>
  <path d="M150 495 C260 505, 345 482, 430 458 S600 425, 710 398 S920 350, 1020 310 S1100 282, 1145 265" fill="none" stroke="#cfcfcf" stroke-width="2" opacity="0.65"/>
  <path d="M150 465 C250 448, 335 452, 430 438 S590 420, 690 390 S850 365, 950 330 S1075 255, 1145 205" fill="none" stroke="#cfcfcf" stroke-width="2" opacity="0.52"/>
  <path d="M150 505 C245 475, 330 472, 410 455 S560 432, 655 422 S835 380, 950 350 S1075 332, 1145 302" fill="none" stroke="#cfcfcf" stroke-width="2" opacity="0.60"/>
  <path d="M150 535 C235 518, 330 508, 420 492 S605 455, 705 440 S875 396, 990 372 S1090 350, 1145 340" fill="none" stroke="#cfcfcf" stroke-width="2" opacity="0.70"/>

  <!-- highlighted conflict series -->
  <path d="M150 515 C220 505, 285 500, 350 485 C410 465, 455 410, 500 320 C545 230, 590 178, 632 205 C675 232, 700 318, 725 390 C760 488, 820 520, 900 506 C990 488, 1085 455, 1145 438"
        fill="none" stroke="#7b3fb2" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" filter="url(#lineGlow)"/>
  <circle cx="604" cy="188" r="7" fill="#7b3fb2" stroke="#ffffff" stroke-width="3"/>

  <!-- axes labels -->
  <text x="114" y="589" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777" text-anchor="end">50</text>
  <text x="114" y="419" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777" text-anchor="end">150</text>
  <text x="114" y="249" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777" text-anchor="end">250</text>
  <text x="138" y="620" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">1975</text>
  <text x="407" y="620" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">1985</text>
  <text x="585" y="620" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">1992</text>
  <text x="706" y="620" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">1998</text>
  <text x="936" y="620" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">2010</text>
  <text x="1120" y="620" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">2020</text>

  <!-- callout -->
  <rect x="760" y="220" width="295" height="108" rx="18" fill="#2c213f" opacity="0.96"/>
  <text x="786" y="254" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">The anomaly is the story</text>
  <text x="786" y="282" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#d9cdec">
    Keep the other lines visible, but make them quiet enough that the audience cannot mistake the focus.
  </text>
  <line x1="760" y1="292" x2="620" y2="198" stroke="#2c213f" stroke-width="2"/>
  <path d="M613 192 L632 198 L618 211 Z" fill="#2c213f"/>

  <text x="420" y="190" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#a36c00">
    FOCUS WINDOW: 1985–1998
  </text>
</svg>
```

## Avoid in this skill
- ❌ Rendering the chart as a single screenshot; it prevents PowerPoint users from recoloring, editing, or sequencing the individual lines.
- ❌ Highlighting every line with a categorical color; the technique depends on most data being visually muted.
- ❌ Using <polyline> if your translator’s support is uncertain; editable <path d="..."> curves are safer and look more executive.
- ❌ Applying filters to <line> elements; use filters on the highlighted <path> or on background <rect> cards instead.
- ❌ Using <mask>, <textPath>, <pattern>, or animated SVG features for the progressive effect; create separate slides and use PowerPoint Fade/Morph transitions.

## Composition notes
- Keep the chart large, occupying roughly 70–80% of the slide, with the action title aligned to the chart’s left axis.
- Use the same underlying muted paths across all three story slides; only change the title, focus band, highlighted path color, and callout.
- Make the focus band wide enough to read as a time period, not a single data point; use a peak marker only for the most important inflection.
- Color rhythm: pale greys for context, warm translucent yellow for the narrative window, and one saturated accent color per story beat.