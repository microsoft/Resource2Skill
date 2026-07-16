# SVG Recipe — Narrative-Driven Highlight Chart (Data Storytelling Format)

## Visual mechanism
A minimalist chart separates signal from noise: muted gray context lines establish baseline behavior while one thick accent line carries the argument. The slide title states the takeaway directly, and annotations replace legends so the audience immediately knows what matters.

## SVG primitives needed
- 1× `<rect>` for the clean slide background
- 1× `<linearGradient>` for a subtle accent area fill under the highlighted trend
- 1× `<filter id="softShadow">` for the annotation card shadow
- 5× `<line>` for faint horizontal gridlines
- 12× `<text>` for headline, subtitle, axis labels, month labels, direct labels, and annotation copy
- 4× `<path>` for the highlighted line, two muted comparison lines, and the translucent highlight area
- 5× `<circle>` for emphasized data points and direct-label endpoint dots
- 1× `<rect>` for a soft callout annotation box
- 1× `<line>` for the callout connector

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="loyalArea" x1="0" y1="210" x2="0" y2="600" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0070C0" stop-opacity="0.18"/>
      <stop offset="0.75" stop-color="#0070C0" stop-opacity="0.03"/>
      <stop offset="1" stop-color="#0070C0" stop-opacity="0"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <text x="72" y="74" width="960" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1E1E1E">
    Loyalty members spend <tspan fill="#0070C0">50% more</tspan> during peak season
  </text>
  <text x="72" y="111" width="930" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#777777">
    Average order value by customer segment, indexed monthly — Jan to Dec 2024
  </text>

  <rect x="72" y="142" width="155" height="34" rx="17" fill="#EEF6FC"/>
  <text x="92" y="164" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#0070C0">
    AOV / customer
  </text>

  <!-- Plot area: x 110–1104, y 210–600 -->
  <line x1="110" y1="600" x2="1135" y2="600" stroke="#E8E8E8" stroke-width="1"/>
  <line x1="110" y1="511" x2="1135" y2="511" stroke="#EFEFEF" stroke-width="1"/>
  <line x1="110" y1="423" x2="1135" y2="423" stroke="#EFEFEF" stroke-width="1"/>
  <line x1="110" y1="334" x2="1135" y2="334" stroke="#EFEFEF" stroke-width="1"/>
  <line x1="110" y1="246" x2="1135" y2="246" stroke="#EFEFEF" stroke-width="1"/>

  <text x="76" y="604" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A2A2A2">180</text>
  <text x="76" y="515" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A2A2A2">230</text>
  <text x="76" y="427" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A2A2A2">280</text>
  <text x="76" y="338" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A2A2A2">330</text>
  <text x="76" y="250" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A2A2A2">380</text>

  <!-- Muted context series -->
  <path d="M125 565 C155 560 184 558 214 556 C244 550 273 540 303 538 C333 540 362 548 392 547 C422 541 451 531 481 529 C511 523 540 514 570 511 C600 505 629 496 659 494 C689 488 718 478 748 476 C778 484 807 500 837 502 C867 508 896 512 926 511 C956 505 985 496 1015 494 C1045 488 1074 478 1104 476"
        fill="none" stroke="#B9B9B9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M125 600 C155 596 184 592 214 591 C244 588 273 583 303 582 C333 585 362 591 392 591 C422 586 451 575 481 573 C511 570 540 566 570 565 C600 559 629 550 659 547 C689 542 718 532 748 529 C778 536 807 545 837 547 C867 552 896 557 926 556 C956 552 985 542 1015 538 C1045 532 1074 525 1104 529"
        fill="none" stroke="#D7D7D7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Highlight area and signal series -->
  <path d="M125 547 C155 540 184 531 214 529 C244 520 273 499 303 494 C333 488 362 480 392 476 C422 468 451 448 481 441 C511 425 540 388 570 370 C600 354 629 326 659 317 C689 301 718 257 748 246 C778 260 807 290 837 299 C867 309 896 319 926 317 C956 305 985 287 1015 281 C1045 268 1074 238 1104 228 L1104 600 L125 600 Z"
        fill="url(#loyalArea)" stroke="none"/>
  <path d="M125 547 C155 540 184 531 214 529 C244 520 273 499 303 494 C333 488 362 480 392 476 C422 468 451 448 481 441 C511 425 540 388 570 370 C600 354 629 326 659 317 C689 301 718 257 748 246 C778 260 807 290 837 299 C867 309 896 319 926 317 C956 305 985 287 1015 281 C1045 268 1074 238 1104 228"
        fill="none" stroke="#0070C0" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Highlighted points -->
  <circle cx="748" cy="246" r="7" fill="#FFFFFF" stroke="#0070C0" stroke-width="4"/>
  <circle cx="1104" cy="228" r="8" fill="#0070C0"/>
  <circle cx="1104" cy="476" r="5" fill="#B9B9B9"/>
  <circle cx="1104" cy="529" r="5" fill="#D7D7D7"/>

  <!-- Direct labels replace legend -->
  <text x="1122" y="233" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0070C0">Loyal members</text>
  <text x="1122" y="481" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8F8F8F">Non-loyal</text>
  <text x="1122" y="534" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B0B0B0">Guests</text>

  <!-- Annotation card -->
  <rect x="662" y="160" width="292" height="72" rx="14" fill="#FFF2CC" filter="url(#softShadow)"/>
  <text x="682" y="187" width="248" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#3B3B3B">
    August is the inflection point
  </text>
  <text x="682" y="211" width="248" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5E5E5E">
    loyalty AOV accelerates while other segments flatten
  </text>
  <line x1="753" y1="232" x2="748" y2="246" stroke="#7A6A2A" stroke-width="2"/>
  <circle cx="748" cy="246" r="3" fill="#7A6A2A"/>

  <!-- Month labels -->
  <text x="116" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Jan</text>
  <text x="205" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Feb</text>
  <text x="294" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Mar</text>
  <text x="383" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Apr</text>
  <text x="472" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">May</text>
  <text x="561" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Jun</text>
  <text x="650" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Jul</text>
  <text x="739" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#0070C0" font-weight="700">Aug</text>
  <text x="828" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Sep</text>
  <text x="917" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Oct</text>
  <text x="1006" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Nov</text>
  <text x="1095" y="635" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E8E8E">Dec</text>
</svg>
```

## Avoid in this skill
- ❌ Heavy chart borders, legends, and saturated colors on every series; they destroy the signal-vs-noise hierarchy.
- ❌ Using only generic chart titles like “Monthly AOV”; the headline should state the business conclusion.
- ❌ Dense tick marks or vertical gridlines; keep only faint horizontal reference lines.
- ❌ `marker-end` on `<path>` connectors; if a callout needs a pointer, use a plain `<line>` plus a small `<circle>` endpoint.

## Composition notes
- Reserve the top 15–18% of the slide for the narrative headline and metric subtitle; the chart should start below that, not compete with it.
- Keep the highlighted series visually dominant with 2× the stroke weight of background lines and a single brand accent color.
- Put labels directly at the line endpoints so no legend is needed.
- Use one annotation only for the most important moment; too many callouts turns the chart back into visual noise.