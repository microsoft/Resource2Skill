# SVG Recipe — Thematic Icon Proportion Chart (圖像化佔比圖)

## Visual mechanism
Turn each percentage into a physical fill level inside a recognizable thematic icon, using a muted “empty” silhouette plus a high-contrast filled portion rising from the bottom. Pair each icon with a bold percentage label and a thin connector line so the data reads as both metaphor and measurement.

## SVG primitives needed
- 2× `<rect>` for the mustard slide background and black footer strip
- 3× `<circle>` for icon medallion frames
- 1× `<circle>` for the human figure head
- 1× `<path>` for the human body outline
- 3× full icon `<path>` shapes for muted empty-state heart, droplet, and lightning silhouettes
- 3× partial-fill `<path>` shapes manually drawn as the bottom portion of each icon
- 3× outline `<path>` shapes over the icons to preserve recognizability
- 3× connector `<path>` strokes linking icon rows to the figure
- 5× `<text>` blocks for the Chinese title, subtitle, percentage labels, and footer copy
- 1× `<linearGradient>` for subtle background depth
- 1× `<filter id="softShadow">` applied to medallions and figure for premium separation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="mustardDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F5D86A"/>
      <stop offset="58%" stop-color="#ECC344"/>
      <stop offset="100%" stop-color="#DFAE32"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#mustardDepth)"/>
  <rect x="0" y="622" width="1280" height="98" fill="#050505"/>

  <text x="68" y="222" width="500" font-family="Microsoft YaHei, Segoe UI" font-size="148" font-weight="900" fill="#050505" letter-spacing="4">
    <tspan x="68" dy="0">圖像</tspan>
    <tspan x="68" dy="154">佔比圖</tspan>
  </text>
  <text x="70" y="544" width="560" font-family="Microsoft YaHei, Segoe UI" font-size="58" font-weight="900" fill="#050505" letter-spacing="2">
    如何用 PPT 製作？
  </text>

  <!-- right-side human outline target -->
  <circle cx="1088" cy="103" r="47" fill="#FFF8EA" stroke="#050505" stroke-width="3" filter="url(#softShadow)"/>
  <path d="M987 252
           C987 199 1016 160 1063 160
           L1125 160
           C1173 160 1190 197 1190 252
           L1190 360
           C1190 377 1181 387 1169 387
           C1157 387 1149 377 1149 360
           L1149 252
           L1114 252
           L1114 578
           C1114 594 1104 604 1092 604
           C1080 604 1071 594 1071 578
           L1071 377
           L1055 377
           L1055 578
           C1055 594 1046 604 1034 604
           C1022 604 1012 594 1012 578
           L1012 252
           L987 252
           L987 360
           C987 377 978 387 966 387
           C954 387 946 377 946 360
           L946 252 Z"
        fill="#FFF4CC" fill-opacity="0.62" stroke="#050505" stroke-width="3" filter="url(#softShadow)"/>
  <line x1="987" y1="252" x2="1190" y2="252" stroke="#050505" stroke-width="3"/>

  <!-- row 1: heart / 80% -->
  <circle cx="738" cy="150" r="66" fill="#F6DA72" fill-opacity="0.42" stroke="#050505" stroke-width="2.5" filter="url(#softShadow)"/>
  <path d="M738 194 C713 172 700 161 700 140 C700 124 711 113 725 113 C733 113 740 118 745 126 C750 118 757 113 766 113 C781 113 793 124 793 140 C793 161 771 176 745 197 Z"
        fill="#050505" fill-opacity="0.18"/>
  <path d="M701 132 L789 132
           C792 154 773 174 745 197
           C717 174 699 154 701 132 Z"
        fill="#FFF8EA"/>
  <path d="M738 194 C713 172 700 161 700 140 C700 124 711 113 725 113 C733 113 740 118 745 126 C750 118 757 113 766 113 C781 113 793 124 793 140 C793 161 771 176 745 197 Z"
        fill="none" stroke="#050505" stroke-width="2.2"/>
  <line x1="702" y1="145" x2="791" y2="145" stroke="#050505" stroke-width="2"/>
  <text x="818" y="143" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="900" fill="#050505">80%</text>
  <path d="M804 150 L940 150 L1048 214" fill="none" stroke="#050505" stroke-width="2.4"/>

  <!-- row 2: water drop / 65% -->
  <circle cx="738" cy="330" r="66" fill="#F6DA72" fill-opacity="0.42" stroke="#050505" stroke-width="2.5" filter="url(#softShadow)"/>
  <path d="M738 291 C719 320 710 337 710 352 C710 374 724 389 738 389 C754 389 769 374 769 352 C769 337 758 320 738 291 Z"
        fill="#050505" fill-opacity="0.18"/>
  <path d="M715 324 L762 324
           C767 334 769 343 769 352
           C769 374 754 389 738 389
           C724 389 710 374 710 352
           C710 343 712 334 715 324 Z"
        fill="#FFF8EA"/>
  <path d="M738 291 C719 320 710 337 710 352 C710 374 724 389 738 389 C754 389 769 374 769 352 C769 337 758 320 738 291 Z"
        fill="none" stroke="#050505" stroke-width="2.2"/>
  <line x1="719" y1="323" x2="758" y2="323" stroke="#050505" stroke-width="2"/>
  <text x="818" y="324" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="900" fill="#050505">65%</text>
  <path d="M804 330 L928 330 L1036 274" fill="none" stroke="#050505" stroke-width="2.4"/>

  <!-- row 3: lightning / 52% -->
  <circle cx="738" cy="506" r="66" fill="#F6DA72" fill-opacity="0.42" stroke="#050505" stroke-width="2.5" filter="url(#softShadow)"/>
  <path d="M727 459 L751 459 L741 499 L770 499 L728 559 L735 518 L708 518 Z"
        fill="#050505" fill-opacity="0.18"/>
  <path d="M711 508 L765 508 L728 559 L735 518 L708 518 Z"
        fill="#FFF8EA"/>
  <path d="M727 459 L751 459 L741 499 L770 499 L728 559 L735 518 L708 518 Z"
        fill="none" stroke="#050505" stroke-width="2.2"/>
  <line x1="715" y1="507" x2="761" y2="507" stroke="#050505" stroke-width="2"/>
  <text x="818" y="500" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="900" fill="#050505">52%</text>
  <path d="M804 506 L962 506 L1050 440" fill="none" stroke="#050505" stroke-width="2.4"/>

  <!-- footer -->
  <text x="88" y="685" width="540" font-family="Microsoft YaHei, Segoe UI" font-size="42" font-weight="900" fill="#FFFFFF">
    形象化 <tspan font-size="34" font-weight="400">你的佔比數據！</tspan>
  </text>
  <circle cx="642" cy="670" r="22" fill="#FFFFFF"/>
  <path d="M642 648 L642 670 L623 681 C620 673 621 660 628 654 C632 651 636 649 642 648 Z" fill="#050505"/>
  <path d="M642 670 L662 681 C656 690 644 694 634 689 C637 683 640 676 642 670 Z" fill="#050505"/>
  <text x="700" y="682" width="500" font-family="Microsoft YaHei, Segoe UI" font-size="32" font-weight="400" fill="#FFFFFF" letter-spacing="2">
    10 分鐘學簡報｜簡報藝術烘焙坊
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on `clip-path` on `<path>` or `<rect>` to crop the icon fill; PPT-Master only preserves clipping reliably for `<image>`, so draw the partial-fill geometry as its own path.
- ❌ Do not use `<mask>` to reveal the filled percentage inside the icon; it can hard-fail translation.
- ❌ Do not use `<use>` to repeat icon paths; duplicate the paths directly so every icon remains editable.
- ❌ Do not use native pie charts or stacked bars for the core proportion; the whole technique depends on the icon silhouette carrying the theme.
- ❌ Do not put `marker-end` arrowheads on connector paths; use plain thin connector strokes or explicit line/path geometry.

## Composition notes
- Keep the left 40–45% of the slide for oversized title typography; the visual weight should feel poster-like, not dashboard-like.
- Stack 3 icon rows vertically on the right, with identical medallion sizes and aligned percentage labels for quick comparison.
- Use a bold background color and a very limited palette: mustard ground, charcoal strokes, pale/white fills.
- The percentage fill should always rise from the bottom of the icon; add a thin horizontal “fill line” to make the data level unmistakable.