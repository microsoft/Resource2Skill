# SVG Recipe — Morphing Rounded Bar Infographic

## Visual mechanism
A clean bar chart becomes more cinematic by turning each value into a vertical pill bar with a circular value badge floating at its top. The bar uses a same-color vertical gradient from airy transparency to saturated color, while the circle badge carries a soft shadow so the data point feels like it has grown upward from the baseline.

## SVG primitives needed
- 1× `<rect>` for the full-slide light gray background
- 2× decorative `<path>` shapes for soft abstract background energy
- 1× `<filter id="softShadow">` applied to value circles
- 1× `<filter id="ambientBlur">` applied to background accent paths
- 5× `<linearGradient>` definitions for individual vertical bar fades
- 5× rounded `<rect>` pill bars, one per data value
- 5× `<circle>` value badges aligned to the tops of the bars
- 5× `<text>` value labels inside the circles
- 5× `<text>` category/year labels beneath the baseline
- 1× `<text>` title
- 1× `<text>` subtitle
- 4× `<line>` elements for subtle chart reference rules
- 3× `<text>` y-axis scale labels
- 1× `<line>` for the baseline

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ambientBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <linearGradient id="barPink" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ff1493" stop-opacity="0.16"/>
      <stop offset="45%" stop-color="#ff1493" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#ff1493" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="barPurple" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8a2be2" stop-opacity="0.16"/>
      <stop offset="45%" stop-color="#8a2be2" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#8a2be2" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="barBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e90ff" stop-opacity="0.16"/>
      <stop offset="45%" stop-color="#1e90ff" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#1e90ff" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="barGold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffc107" stop-opacity="0.18"/>
      <stop offset="45%" stop-color="#ffc107" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="#ffc107" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="barOrange" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ff4500" stop-opacity="0.16"/>
      <stop offset="45%" stop-color="#ff4500" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#ff4500" stop-opacity="1"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f2f2f2"/>

  <path d="M1060 88 C1162 50 1248 96 1296 190 C1232 224 1151 225 1079 190 C1030 166 1012 117 1060 88 Z"
        fill="#ffffff" opacity="0.75" filter="url(#ambientBlur)"/>
  <path d="M-40 530 C84 470 178 515 250 610 C151 660 46 677 -55 632 Z"
        fill="#ffffff" opacity="0.62" filter="url(#ambientBlur)"/>

  <text x="0" y="84" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700"
        letter-spacing="2.5" fill="#595959">PERCENTAGE BY YEAR</text>
  <text x="0" y="122" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="500"
        letter-spacing="0.8" fill="#8a8a8a">Rounded morph bars with floating value caps</text>

  <line x1="222" y1="223" x2="1068" y2="223" stroke="#dedede" stroke-width="1"/>
  <line x1="222" y1="387" x2="1068" y2="387" stroke="#dedede" stroke-width="1"/>
  <line x1="222" y1="510" x2="1068" y2="510" stroke="#e6e6e6" stroke-width="1"/>
  <line x1="222" y1="592" x2="1068" y2="592" stroke="#cfcfcf" stroke-width="2"/>

  <text x="168" y="229" width="50" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#9a9a9a">100%</text>
  <text x="168" y="393" width="50" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#9a9a9a">50%</text>
  <text x="168" y="598" width="50" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#9a9a9a">0%</text>

  <rect x="248" y="223" width="76" height="369" rx="38" fill="url(#barPink)"/>
  <rect x="418" y="428" width="76" height="164" rx="38" fill="url(#barPurple)"/>
  <rect x="588" y="367" width="76" height="225" rx="38" fill="url(#barBlue)"/>
  <rect x="758" y="469" width="76" height="123" rx="38" fill="url(#barGold)"/>
  <rect x="928" y="264" width="76" height="328" rx="38" fill="url(#barOrange)"/>

  <circle cx="286" cy="223" r="38" fill="#ff1493" filter="url(#softShadow)"/>
  <circle cx="456" cy="428" r="38" fill="#8a2be2" filter="url(#softShadow)"/>
  <circle cx="626" cy="367" r="38" fill="#1e90ff" filter="url(#softShadow)"/>
  <circle cx="796" cy="469" r="38" fill="#ffc107" filter="url(#softShadow)"/>
  <circle cx="966" cy="264" r="38" fill="#ff4500" filter="url(#softShadow)"/>

  <text x="248" y="232" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">90%</text>
  <text x="418" y="437" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">40%</text>
  <text x="588" y="376" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">55%</text>
  <text x="758" y="478" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">30%</text>
  <text x="928" y="273" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">80%</text>

  <text x="248" y="642" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#595959">2019</text>
  <text x="418" y="642" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#595959">2020</text>
  <text x="588" y="642" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#595959">2021</text>
  <text x="758" y="642" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#595959">2022</text>
  <text x="928" y="642" width="76" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#595959">2023</text>
</svg>
```

## Avoid in this skill
- ❌ Using square-ended bars; the technique depends on fully rounded pill geometry, usually `rx` equal to half the bar width.
- ❌ Applying `filter` to `<line>` grid rules; shadows/glows on lines are not preserved reliably, so keep reference rules flat.
- ❌ Using `<mask>` to reveal the bars; for editable PPT output, create the start/end states as actual bar positions and let PowerPoint Morph interpolate them.
- ❌ Using `<clipPath>` on bars or circles; clipping non-image shapes will be ignored by the translator.
- ❌ Overcrowding with more than 6–7 bars; the value circles need breathing room to remain premium and readable.

## Composition notes
- Keep the chart baseline in the lower third, around `y=590`, with the title centered above; this leaves enough vertical runway for tall morphing bars.
- Make each bar and circle share the same horizontal center; the circle should slightly dominate the bar width to read as a cap or badge.
- Use one vivid hue per category, but repeat that hue in both the bar gradient and circle fill for a coherent color rhythm.
- For a Morph-ready deck, duplicate the slide: on the first slide, move all bars/circles down to the baseline or below the canvas and set circle text opacity/color low; on the second slide, use the final positions shown above.