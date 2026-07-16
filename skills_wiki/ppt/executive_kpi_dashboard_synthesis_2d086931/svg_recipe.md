# SVG Recipe — Executive KPI Dashboard Synthesis

## Visual mechanism
A premium executive dashboard is built from aligned white KPI tiles on a light-gray canvas, combining large headline metrics with miniature trend, funnel, bullet, geography, and mix charts. The design works because every card uses consistent spacing, typography, and muted neutrals while positive/negative accent colors instantly direct attention.

## SVG primitives needed
- 1× `<rect>` full-slide background for the light BI-style canvas.
- 8× `<rect>` card containers with rounded corners and soft shadow filter.
- 3× `<path>` area fills plus 3× `<path>` sparkline strokes for KPI trend backplates.
- 5× `<path>` funnel segments for pipeline conversion, using teal-to-blue tonal fills.
- 6× `<path>` abstract regional map shapes for geographic performance synthesis.
- 7× `<circle>` regional map markers with green/red/teal status colors.
- 12× `<rect>` bullet chart bands, actual bars, and small variance blocks.
- 5× `<line>` bullet chart target markers.
- 1× `<linearGradient>` for teal chart accents.
- 1× `<linearGradient>` for green positive trend fills.
- 1× `<linearGradient>` for red negative trend fills.
- 1× `<filter id="cardShadow">` applied to card rectangles for soft dashboard elevation.
- Multiple `<text>` elements with explicit `width` attributes for titles, KPI values, labels, and annotations.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00A0A0"/>
      <stop offset="100%" stop-color="#006B78"/>
    </linearGradient>
    <linearGradient id="greenFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2E8B57" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#2E8B57" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="redFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#DC143C" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#DC143C" stop-opacity="0.02"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F0F0F0"/>
  <text x="40" y="48" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#303030">Strategic Performance Dashboard</text>
  <text x="40" y="72" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777777">Executive synthesis · Q4 run-rate, conversion, regional performance, margin health</text>
  <rect x="1046" y="32" width="194" height="34" rx="17" fill="#E7F4F4"/>
  <text x="1070" y="54" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#006B78">Updated 09:00 UTC</text>

  <rect x="40" y="94" width="280" height="164" rx="16" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="62" y="124" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#505050">ARR Run Rate</text>
  <path d="M62 226 L62 206 C91 188,111 196,134 178 C164 154,188 170,214 142 C238 118,260 132,298 104 L298 226 Z" fill="url(#greenFade)"/>
  <path d="M62 206 C91 188,111 196,134 178 C164 154,188 170,214 142 C238 118,260 132,298 104" fill="none" stroke="#2E8B57" stroke-width="3"/>
  <text x="62" y="181" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="300" fill="#303030">$128.4M</text>
  <text x="64" y="211" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#2E8B57">▲ 14.8% YoY · ahead of plan</text>

  <rect x="338" y="94" width="280" height="164" rx="16" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="360" y="124" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#505050">Gross Margin</text>
  <path d="M360 226 L360 185 C392 178,414 162,438 168 C464 174,489 145,514 150 C538 155,565 130,596 122 L596 226 Z" fill="url(#greenFade)"/>
  <path d="M360 185 C392 178,414 162,438 168 C464 174,489 145,514 150 C538 155,565 130,596 122" fill="none" stroke="#2E8B57" stroke-width="3"/>
  <text x="360" y="181" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="300" fill="#303030">68.2%</text>
  <text x="362" y="211" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#2E8B57">▲ 320 bps vs. prior quarter</text>

  <rect x="636" y="94" width="280" height="164" rx="16" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="658" y="124" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#505050">Net Churn</text>
  <path d="M658 226 L658 122 C688 139,710 130,736 151 C762 171,786 166,812 187 C838 208,864 194,894 215 L894 226 Z" fill="url(#redFade)"/>
  <path d="M658 122 C688 139,710 130,736 151 C762 171,786 166,812 187 C838 208,864 194,894 215" fill="none" stroke="#DC143C" stroke-width="3"/>
  <text x="658" y="181" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="300" fill="#303030">5.9%</text>
  <text x="660" y="211" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DC143C">▼ 90 bps deterioration · watchlist</text>

  <rect x="934" y="94" width="306" height="164" rx="16" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="956" y="124" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#505050">Board Attention Index</text>
  <circle cx="988" cy="178" r="40" fill="#FFF0EF"/>
  <text x="964" y="190" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#DC143C">3</text>
  <text x="1040" y="164" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#303030">Critical focus areas</text>
  <text x="1040" y="188" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">Enterprise churn, hiring velocity, EMEA pipeline coverage</text>
  <rect x="1040" y="208" width="132" height="10" rx="5" fill="#E0E0E0"/>
  <rect x="1040" y="208" width="82" height="10" rx="5" fill="#DC143C"/>

  <rect x="40" y="278" width="360" height="190" rx="16" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="62" y="309" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#505050">Pipeline Conversion Funnel</text>
  <path d="M78 332 L362 332 L336 358 L104 358 Z" fill="#009B9B"/>
  <path d="M100 365 L340 365 L316 391 L124 391 Z" fill="#008585"/>
  <path d="M124 398 L316 398 L294 424 L146 424 Z" fill="#007070"/>
  <path d="M150 431 L292 431 L272 454 L170 454 Z" fill="#005E68"/>
  <text x="92" y="351" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#FFFFFF">MQL  18.4k</text>
  <text x="120" y="384" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#FFFFFF">SQL  9.7k</text>
  <text x="150" y="417" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#FFFFFF">Opps  4.2k</text>
  <text x="178" y="449" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#FFFFFF">Won  1.6k</text>

  <rect x="418" y="278" width="390" height="190" rx="16" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="440" y="309" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#505050">Regional Revenue Heat</text>
  <path d="M506 368 C531 329,584 318,616 350 C655 390,714 360,744 402 C706 430,662 430,628 414 C594 442,538 424,506 368 Z" fill="#E6EFEF" stroke="#C7DADA" stroke-width="1.5"/>
  <path d="M472 386 C490 354,520 358,536 384 C516 410,492 412,472 386 Z" fill="#D4EAEA"/>
  <path d="M670 338 C704 318,738 330,758 360 C726 372,700 368,670 338 Z" fill="#D4EAEA"/>
  <circle cx="548" cy="371" r="12" fill="#2E8B57"/>
  <circle cx="622" cy="384" r="18" fill="url(#tealGrad)"/>
  <circle cx="704" cy="397" r="10" fill="#DC143C"/>
  <circle cx="582" cy="424" r="8" fill="#2E8B57"/>
  <text x="440" y="444" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">Americas +12%, APAC +8%, EMEA -4% vs. target</text>

  <rect x="826" y="278" width="414" height="190" rx="16" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="848" y="309" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#505050">Operating Health vs Target</text>
  <text x="848" y="344" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">Sales eff.</text>
  <rect x="936" y="334" width="220" height="16" fill="#E0E0E0"/><rect x="936" y="334" width="152" height="16" fill="#C0C0C0"/><rect x="936" y="338" width="174" height="8" fill="#595959"/><line x1="1122" y1="330" x2="1122" y2="354" stroke="#000000" stroke-width="2"/>
  <text x="848" y="382" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">Retention</text>
  <rect x="936" y="372" width="220" height="16" fill="#E0E0E0"/><rect x="936" y="372" width="178" height="16" fill="#C0C0C0"/><rect x="936" y="376" width="196" height="8" fill="#595959"/><line x1="1110" y1="368" x2="1110" y2="392" stroke="#000000" stroke-width="2"/>
  <text x="848" y="420" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">Hiring</text>
  <rect x="936" y="410" width="220" height="16" fill="#E0E0E0"/><rect x="936" y="410" width="132" height="16" fill="#C0C0C0"/><rect x="936" y="414" width="108" height="8" fill="#595959"/><line x1="1094" y1="406" x2="1094" y2="430" stroke="#000000" stroke-width="2"/>

  <rect x="40" y="488" width="570" height="178" rx="16" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="62" y="519" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#505050">Revenue Mix by Segment</text>
  <rect x="68" y="552" width="420" height="26" rx="13" fill="#E8E8E8"/>
  <rect x="68" y="552" width="206" height="26" rx="13" fill="#006B78"/>
  <rect x="274" y="552" width="128" height="26" fill="#00A0A0"/>
  <rect x="402" y="552" width="86" height="26" rx="13" fill="#B9D9D9"/>
  <text x="504" y="571" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#303030">$128M</text>
  <circle cx="78" cy="612" r="6" fill="#006B78"/><text x="92" y="616" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#666666">Enterprise 49%</text>
  <circle cx="226" cy="612" r="6" fill="#00A0A0"/><text x="240" y="616" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#666666">Mid-market 31%</text>
  <circle cx="388" cy="612" r="6" fill="#B9D9D9"/><text x="402" y="616" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#666666">SMB 20%</text>

  <rect x="628" y="488" width="612" height="178" rx="16" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="650" y="519" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#505050">Executive Narrative</text>
  <rect x="652" y="546" width="10" height="78" rx="5" fill="#2E8B57"/>
  <text x="676" y="563" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#303030">Growth remains above plan, but quality of growth is bifurcating.</text>
  <text x="676" y="592" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#666666">Margin expansion and Enterprise ARR offset churn pressure in EMEA. Next review should isolate renewal cohorts, pipeline source quality, and hiring bottlenecks.</text>
  <rect x="676" y="624" width="122" height="24" rx="12" fill="#E7F4F4"/>
  <text x="694" y="641" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#006B78">DRILL DOWN</text>
</svg>
```

## Avoid in this skill
- ❌ Rendering charts as external PNGs when they can be built from editable SVG paths, rects, circles, and text.
- ❌ Overloading the slide with full axes, gridlines, and legends; executive dashboards need scan-friendly summaries.
- ❌ Using `marker-end` for arrows in chart annotations; use explicit `<line>` or small hand-drawn `<path>` chevrons instead.
- ❌ Applying filters to `<line>` target markers; keep shadows on cards and major shapes only.
- ❌ Omitting `width` on text elements; dashboard labels are dense and need predictable PowerPoint text boxes.

## Composition notes
- Keep a strict grid: wide outer margins, equal gutters, and card edges aligned across rows.
- Use large KPI numbers only in the top row; reserve lower rows for diagnostic visuals and narrative synthesis.
- Maintain a neutral white/gray base, then use green for positive movement, red for risk, and teal for neutral business metrics.
- Preserve negative space inside each card; miniature charts should support the KPI, not compete with the headline number.