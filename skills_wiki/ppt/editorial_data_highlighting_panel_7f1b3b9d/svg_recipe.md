# SVG Recipe — Editorial Data Highlighting Panel

## Visual mechanism
A wide editorial line chart is turned into a narrative by muting most series into gray “context,” then making one or two key series bold and colored. A translucent vertical focus span sits behind the data to bracket the timeframe being discussed, while the headline states the takeaway rather than merely naming the chart.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 3× narrow `<rect>` for left-edge brand accent bars
- 1× rounded `<rect>` for the chart panel/card
- 1× translucent `<rect>` for the highlighted timeframe span
- 6× `<line>` for faint horizontal gridlines
- 2× `<line>` for minimalist x/y axes
- 2× dashed `<line>` for the focus span boundaries
- 7× muted `<path>` for background/context data series
- 2× bold `<path>` for highlighted narrative data series
- 2× small `<circle>` endpoint markers on highlighted series
- Multiple `<text>` elements with explicit `width` for title, subtitle, axis labels, callouts, and legend
- 1× `<linearGradient>` for the very subtle slide background wash
- 1× `<filter id="softShadow">` applied to the chart card
- 1× `<filter id="labelGlow">` applied to endpoint labels for extra readability

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="62%" stop-color="#FBFAF6"/>
      <stop offset="100%" stop-color="#F4F1EA"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="labelGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paperWash)"/>

  <rect x="0" y="54" width="10" height="118" fill="#F4D03F"/>
  <rect x="0" y="172" width="10" height="92" fill="#D4A017"/>
  <rect x="0" y="264" width="10" height="74" fill="#D45A8C"/>

  <text x="72" y="72" width="1040" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#B08B18" letter-spacing="2.8">
    QUICK STUDY / BUSINESS REVIEW
  </text>
  <text x="72" y="132" width="1000" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#262626">
    A Steady Increase… Except in Japan
  </text>
  <text x="74" y="176" width="880" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#666666">
    Japan’s asset bubble peaked in the early ’90s, then diverged from the global housing-price recovery.
  </text>

  <rect x="72" y="220" width="1136" height="428" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="104" y="258" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#777777" letter-spacing="1.7">
    REAL HOUSING PRICE INDEX, 1975–2017
  </text>

  <line x1="132" y1="579" x2="1155" y2="579" stroke="#ECECEC" stroke-width="1"/>
  <line x1="132" y1="522" x2="1155" y2="522" stroke="#ECECEC" stroke-width="1"/>
  <line x1="132" y1="465" x2="1155" y2="465" stroke="#ECECEC" stroke-width="1"/>
  <line x1="132" y1="408" x2="1155" y2="408" stroke="#ECECEC" stroke-width="1"/>
  <line x1="132" y1="351" x2="1155" y2="351" stroke="#ECECEC" stroke-width="1"/>
  <line x1="132" y1="294" x2="1155" y2="294" stroke="#ECECEC" stroke-width="1"/>

  <rect x="846" y="286" width="286" height="296" fill="#F4D03F" opacity="0.28"/>
  <line x1="846" y1="286" x2="846" y2="582" stroke="#C69B17" stroke-width="1.5" stroke-dasharray="6 7"/>
  <line x1="1132" y1="286" x2="1132" y2="582" stroke="#C69B17" stroke-width="1.5" stroke-dasharray="6 7"/>
  <text x="866" y="314" width="232" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#8B6A00">
    Recovery window
  </text>

  <line x1="132" y1="582" x2="1155" y2="582" stroke="#D8D8D8" stroke-width="1.5"/>
  <line x1="132" y1="286" x2="132" y2="582" stroke="#D8D8D8" stroke-width="1.5"/>

  <path d="M132 548 C190 538 245 530 300 513 S410 486 465 478 S575 458 630 440 S740 415 790 396 S900 364 960 346 S1070 326 1155 307" fill="none" stroke="#B9B9B9" stroke-width="2" opacity="0.68"/>
  <path d="M132 530 C200 520 250 518 315 496 S430 482 500 455 S610 442 680 421 S785 395 845 376 S980 342 1155 318" fill="none" stroke="#B9B9B9" stroke-width="2" opacity="0.55"/>
  <path d="M132 562 C205 548 255 536 318 528 S438 506 500 493 S612 474 675 459 S780 434 850 413 S1000 386 1155 358" fill="none" stroke="#C5C5C5" stroke-width="2" opacity="0.62"/>
  <path d="M132 536 C185 552 254 543 315 525 S435 505 505 488 S620 472 690 442 S780 430 850 400 S990 370 1155 337" fill="none" stroke="#B2B2B2" stroke-width="2" opacity="0.5"/>
  <path d="M132 520 C206 505 268 516 330 502 S460 478 530 462 S650 450 720 425 S830 405 900 385 S1035 362 1155 340" fill="none" stroke="#C8C8C8" stroke-width="2" opacity="0.65"/>
  <path d="M132 558 C205 555 275 545 338 534 S460 518 530 500 S650 480 728 458 S835 440 912 412 S1035 386 1155 370" fill="none" stroke="#BDBDBD" stroke-width="2" opacity="0.58"/>
  <path d="M132 545 C210 532 275 526 340 512 S470 492 540 476 S660 455 735 430 S850 408 925 382 S1040 356 1155 326" fill="none" stroke="#B7B7B7" stroke-width="2" opacity="0.6"/>

  <path d="M132 552 C185 544 245 527 300 500 S392 423 455 337 S545 298 610 334 S720 415 775 465 S865 510 925 516 S1045 508 1155 493" fill="none" stroke="#2E8653" stroke-width="5" stroke-linecap="round"/>
  <path d="M132 542 C205 530 260 518 320 505 S450 480 520 460 S650 435 720 405 S838 374 900 350 S1040 325 1155 302" fill="none" stroke="#C0392B" stroke-width="5" stroke-linecap="round"/>

  <circle cx="1155" cy="493" r="6.5" fill="#2E8653"/>
  <circle cx="1155" cy="302" r="6.5" fill="#C0392B"/>
  <text x="1086" y="486" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#2E8653" filter="url(#labelGlow)">
    Japan
  </text>
  <text x="1010" y="294" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#C0392B" filter="url(#labelGlow)">
    Global average
  </text>

  <text x="104" y="586" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">20</text>
  <text x="104" y="529" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">60</text>
  <text x="98" y="472" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">100</text>
  <text x="98" y="415" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">140</text>
  <text x="98" y="358" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">180</text>

  <text x="126" y="612" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#888888">1975</text>
  <text x="354" y="612" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#888888">1985</text>
  <text x="587" y="612" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#888888">1995</text>
  <text x="820" y="612" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#888888">2005</text>
  <text x="1108" y="612" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#888888">2017</text>

  <rect x="904" y="236" width="252" height="38" rx="19" fill="#262626"/>
  <circle cx="928" cy="255" r="6" fill="#F4D03F"/>
  <text x="944" y="261" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">
    Story focus: 2005–2017
  </text>
</svg>
```

## Avoid in this skill
- ❌ Rendering the entire chart as a flat screenshot; use editable SVG paths, lines, rects, and text instead.
- ❌ Over-coloring every data line; the storytelling depends on gray attenuation versus one or two strong signals.
- ❌ Heavy chart borders, dense tick labels, or dark gridlines that compete with the highlighted timeframe.
- ❌ Applying `clip-path` to chart shapes or using `<mask>` for the focus span; a simple translucent rectangle translates more reliably.
- ❌ Arrowheads on `<path>` callouts; if an arrow is needed, use a `<line>` plus a small editable triangle/path arrowhead.

## Composition notes
- Reserve the top 20–25% of the slide for an editorial takeaway title and concise explanatory subtitle.
- Keep the chart wide and low, occupying roughly the bottom three-quarters of the canvas with generous left/right breathing room.
- Place the translucent focus span behind the lines but above the grid, so it reads as an annotated timeframe rather than a separate shape.
- Use color rhythm sparingly: gray for context, one green/red pair for narrative series, and warm gold only for the focus interval and accent system.