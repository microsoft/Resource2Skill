# SVG Recipe — Consulting-Style Analytical Data Card Layout

## Visual mechanism
A white executive-report canvas is split into two large rounded “analysis cards”: the top card frames the current problem with a risk-colored line chart, while the bottom card frames the recommended action with a positive-impact bar chart. Each card pairs a declarative consulting headline on the left with a clean, editable data visualization on the right, turning metrics into a narrative sequence.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× large rounded `<rect>` for stacked analytical cards
- 2× slim accent `<rect>` strips to identify risk vs. solution cards
- Multiple small rounded `<rect>` for KPI pills, chart labels, and legend chips
- Multiple `<line>` elements for chart axes, gridlines, and bar-chart baselines
- 4× `<path>` for editable chart lines and small semantic icons
- Multiple `<circle>` elements for line-chart data markers and legend dots
- Multiple `<rect>` bars for the solution impact chart
- Multiple `<text>` elements with explicit `width` for title, headlines, bullets, axes, legends, and KPI values
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` for subtle card elevation
- 2× `<linearGradient>` fills for muted red/green KPI pills and analytical accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="riskTint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#fff1f2"/>
      <stop offset="100%" stop-color="#ffe4e6"/>
    </linearGradient>
    <linearGradient id="successTint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ecfdf5"/>
      <stop offset="100%" stop-color="#dcfce7"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <text x="56" y="46" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="1.4" fill="#6c757d">
    STRATEGY &amp; OPERATIONS · VIDEO ENGAGEMENT ANALYSIS
  </text>
  <text x="56" y="82" width="900" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#212529">
    Tie the first five seconds directly to retention, awareness, and conversion.
  </text>
  <rect x="1044" y="36" width="168" height="34" rx="17" fill="#f1f3f5"/>
  <text x="1064" y="58" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#495057">
    EXEC SUMMARY
  </text>

  <!-- Top analytical card: problem -->
  <rect x="56" y="112" width="1168" height="260" rx="24" fill="#f8f9fa" filter="url(#cardShadow)"/>
  <rect x="56" y="112" width="9" height="260" rx="4.5" fill="#dc3545"/>
  <rect x="88" y="142" width="132" height="30" rx="15" fill="url(#riskTint)"/>
  <path d="M105 162 L113 147 L121 162 Z" fill="#dc3545"/>
  <text x="132" y="163" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#dc3545">
    RISK SIGNAL
  </text>

  <text x="88" y="207" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#212529">
    현황 분석: 5초 내 제품 노출 부재 시 이탈률 리스크
  </text>
  <text x="88" y="246" width="442" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6c757d">
    • 시청자의 60%가 첫 5초 이내에 이탈합니다.
  </text>
  <text x="88" y="274" width="442" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6c757d">
    • 제품 노출 지연은 브랜드 인지도 하락으로 연결됩니다.
  </text>
  <text x="88" y="302" width="442" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6c757d">
    • 초기 주목도 하락은 전환율 33% 감소를 유발합니다.
  </text>
  <rect x="88" y="324" width="150" height="34" rx="17" fill="#fff5f5"/>
  <text x="106" y="347" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#dc3545">
    -80 pts at 5s
  </text>

  <!-- Top line chart -->
  <text x="612" y="151" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#343a40">
    Viewer retention by elapsed seconds
  </text>
  <line x1="620" y1="318" x2="1158" y2="318" stroke="#adb5bd" stroke-width="1.4"/>
  <line x1="620" y1="190" x2="620" y2="318" stroke="#adb5bd" stroke-width="1.4"/>
  <line x1="620" y1="286" x2="1158" y2="286" stroke="#e9ecef" stroke-width="1"/>
  <line x1="620" y1="254" x2="1158" y2="254" stroke="#e9ecef" stroke-width="1"/>
  <line x1="620" y1="222" x2="1158" y2="222" stroke="#e9ecef" stroke-width="1"/>
  <line x1="620" y1="190" x2="1158" y2="190" stroke="#e9ecef" stroke-width="1"/>
  <path d="M620 190 C690 198, 735 205, 781 222 S875 272, 943 286 S1060 310, 1158 318" fill="none" stroke="#dc3545" stroke-width="4" stroke-linecap="round"/>
  <path d="M620 190 C700 191, 770 194, 835 197 S980 207, 1065 218 S1125 224, 1158 229" fill="none" stroke="#0d6efd" stroke-width="4" stroke-linecap="round"/>
  <circle cx="620" cy="190" r="5" fill="#dc3545"/><circle cx="781" cy="222" r="5" fill="#dc3545"/><circle cx="943" cy="286" r="5" fill="#dc3545"/><circle cx="1158" cy="318" r="5" fill="#dc3545"/>
  <circle cx="620" cy="190" r="5" fill="#0d6efd"/><circle cx="835" cy="197" r="5" fill="#0d6efd"/><circle cx="1065" cy="218" r="5" fill="#0d6efd"/><circle cx="1158" cy="229" r="5" fill="#0d6efd"/>
  <text x="610" y="341" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#868e96">0s</text>
  <text x="764" y="341" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#868e96">2s</text>
  <text x="926" y="341" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#868e96">4s</text>
  <text x="1144" y="341" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#868e96">5s</text>
  <circle cx="968" cy="151" r="5" fill="#dc3545"/>
  <text x="980" y="156" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#495057">General video</text>
  <circle cx="1086" cy="151" r="5" fill="#0d6efd"/>
  <text x="1098" y="156" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#495057">Optimized video</text>

  <!-- Bottom analytical card: solution -->
  <rect x="56" y="408" width="1168" height="250" rx="24" fill="#f8f9fa" filter="url(#cardShadow)"/>
  <rect x="56" y="408" width="9" height="250" rx="4.5" fill="#198754"/>
  <rect x="88" y="438" width="148" height="30" rx="15" fill="url(#successTint)"/>
  <path d="M107 455 L113 461 L126 447" fill="none" stroke="#198754" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="138" y="459" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#198754">
    ACTION PLAN
  </text>

  <text x="88" y="503" width="452" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#212529">
    솔루션: 3초 내 브랜드 로고 전면 배치의 효과
  </text>
  <text x="88" y="542" width="442" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6c757d">
    • 첫 화면에 로고와 제품 컷을 동시에 노출합니다.
  </text>
  <text x="88" y="570" width="442" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6c757d">
    • 3초 이전 CTA 삽입으로 고의도 클릭을 회수합니다.
  </text>
  <text x="88" y="598" width="442" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6c757d">
    • 유지율 개선분을 리타겟팅 예산 우선순위에 반영합니다.
  </text>
  <rect x="88" y="620" width="150" height="34" rx="17" fill="#ecfdf5"/>
  <text x="107" y="643" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#198754">
    +33% lift
  </text>

  <!-- Bottom bar chart -->
  <text x="612" y="447" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#343a40">
    Expected impact after creative restructure
  </text>
  <line x1="620" y1="610" x2="1158" y2="610" stroke="#adb5bd" stroke-width="1.4"/>
  <line x1="620" y1="570" x2="1158" y2="570" stroke="#e9ecef" stroke-width="1"/>
  <line x1="620" y1="530" x2="1158" y2="530" stroke="#e9ecef" stroke-width="1"/>
  <line x1="620" y1="490" x2="1158" y2="490" stroke="#e9ecef" stroke-width="1"/>
  <rect x="665" y="550" width="54" height="60" rx="8" fill="#ced4da"/>
  <rect x="740" y="506" width="54" height="104" rx="8" fill="#198754"/>
  <rect x="860" y="532" width="54" height="78" rx="8" fill="#ced4da"/>
  <rect x="935" y="482" width="54" height="128" rx="8" fill="#198754"/>
  <rect x="1055" y="562" width="54" height="48" rx="8" fill="#ced4da"/>
  <rect x="1130" y="520" width="54" height="90" rx="8" fill="#198754"/>
  <text x="654" y="632" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#6c757d">Baseline</text>
  <text x="729" y="632" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#6c757d">Optimized</text>
  <text x="850" y="632" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#6c757d">Recall</text>
  <text x="924" y="632" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#6c757d">Recall+</text>
  <text x="1044" y="632" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#6c757d">CVR</text>
  <text x="1118" y="632" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#6c757d">CVR+</text>
  <text x="742" y="494" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#198754">85%</text>
  <text x="936" y="470" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#198754">+41%</text>
  <text x="1130" y="508" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#198754">+33%</text>
</svg>
```

## Avoid in this skill
- ❌ Native PPT chart placeholders or screenshots when the chart can be rebuilt with editable SVG lines, paths, circles, and bars.
- ❌ Overly dense axes, tick marks, and labels; this layout should feel like a consulting takeaway, not a BI dashboard.
- ❌ Card backgrounds with heavy borders or dark fills that compete with the data story.
- ❌ `marker-end` arrows on paths for annotations; use direct `<line>` elements or simple icon paths instead.
- ❌ Applying `filter` to chart grid `<line>` elements; keep shadows on cards or major shapes only.

## Composition notes
- Keep the slide in a two-card vertical rhythm: top = diagnostic/problem, bottom = recommendation/impact.
- Reserve roughly 40% of each card for the narrative text block and 60% for the supporting chart.
- Use one dominant accent per card: red for risk/current-state decline, green for improvement/action, blue or gray for baseline comparison.
- Maintain generous white space around card edges and between chart components; the premium feel comes from restraint and clear hierarchy.