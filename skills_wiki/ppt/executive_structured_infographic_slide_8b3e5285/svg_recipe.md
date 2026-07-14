# SVG Recipe — Executive Structured Infographic Slide (結構化高階主管摘要卡片排版)

## Visual mechanism
A conclusion-first executive slide: the top band states the single takeaway, while the lower area splits into a strong left-side data visualization and three right-side evidence cards. The layout replaces bullet-heavy narrative with a structured “chart + insight cards” system, using rounded panels, accent lines, restrained shadows, and corporate blue/teal color hierarchy.

## SVG primitives needed
- 1× `<rect>` for the full-slide light gray background
- 2× decorative `<path>` blobs with soft gradients/glow for subtle executive polish
- 1× `<rect>` for the headline conclusion ribbon
- 1× `<rect>` for the conclusion ribbon accent bar
- 2× `<rect>` for the main left/right content panel backgrounds
- 6× donut-segment `<path>` elements for an editable market-share chart
- 1× `<circle>` for the donut center label surface
- 6× small `<rect>` swatches for the donut legend
- 3× rounded `<rect>` insight cards on the right
- 3× narrow `<rect>` accent bars inside insight cards
- 3× `<circle>` numbered badges
- 3× simple `<path>` icons for executive-style evidence cues
- 2× `<line>` separator/guide elements for alignment rhythm
- Multiple `<text>` elements with explicit `width` attributes for title, conclusion, chart labels, legend, and card copy
- 1× `<linearGradient>` for the conclusion ribbon
- 1× `<radialGradient>` for the background glow blobs
- 1× `<filter id="softShadow">` applied to card rectangles
- 1× `<filter id="glow">` applied to decorative background paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="ribbonGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#EAF4FF"/>
      <stop offset="55%" stop-color="#F4FAFF"/>
      <stop offset="100%" stop-color="#E8FFF8"/>
    </linearGradient>
    <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#00BFFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8F9FA"/>
  <path d="M1030 52 C1135 20 1250 70 1276 160 C1308 270 1188 320 1088 286 C990 252 930 100 1030 52 Z" fill="url(#glowGrad)" filter="url(#glow)"/>
  <path d="M-40 520 C70 470 160 528 182 622 C204 716 86 748 -20 706 Z" fill="#36B37E" opacity="0.10" filter="url(#glow)"/>

  <text x="72" y="72" width="980" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#172B4D">品牌格局：特斯拉領先，本土品牌崛起</text>
  <text x="74" y="108" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#6B778C" letter-spacing="1.4">EXECUTIVE MARKET SNAPSHOT · 2024 TAIWAN EV MARKET</text>

  <rect x="72" y="132" width="1136" height="74" rx="18" fill="url(#ribbonGrad)"/>
  <rect x="72" y="132" width="9" height="74" rx="4.5" fill="#00BFFF"/>
  <text x="102" y="164" width="1060" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#253858">2024年台灣電動車市場持續成長；特斯拉仍佔據首位，但 Luxgen 以高性價比切入大眾市場，正在重塑競爭版圖。</text>
  <text x="103" y="190" width="920" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5E6C84">一頁只保留一個結論，下方用圖表與三個證據卡片支撐管理層決策。</text>

  <rect x="72" y="246" width="565" height="410" rx="26" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="678" y="246" width="530" height="410" rx="26" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="106" y="292" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#172B4D">市佔結構：前二品牌拉開差距</text>
  <text x="106" y="318" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B778C">以圓環圖呈現高階主管最需要的「集中度」與「第二名追趕速度」。</text>

  <path d="M355 323 A142 142 0 0 1 438.5 579.9 L406.7 536.2 A88 88 0 0 0 355 377 Z" fill="#172B4D" fill-rule="evenodd"/>
  <path d="M438.5 579.9 A142 142 0 0 1 281.2 586.3 L309.2 540.2 A88 88 0 0 0 406.7 536.2 Z" fill="#00BFFF" fill-rule="evenodd"/>
  <path d="M281.2 586.3 A142 142 0 0 1 213.0 461.4 L267.0 462.8 A88 88 0 0 0 309.2 540.2 Z" fill="#36B37E" fill-rule="evenodd"/>
  <path d="M213.0 461.4 A142 142 0 0 1 231.5 395.0 L278.4 421.6 A88 88 0 0 0 267.0 462.8 Z" fill="#6554C0" fill-rule="evenodd"/>
  <path d="M231.5 395.0 A142 142 0 0 1 250.3 369.0 L290.1 405.5 A88 88 0 0 0 278.4 421.6 Z" fill="#FFAB00" fill-rule="evenodd"/>
  <path d="M250.3 369.0 A142 142 0 0 1 355 323 L355 377 A88 88 0 0 0 290.1 405.5 Z" fill="#C1C7D0" fill-rule="evenodd"/>
  <circle cx="355" cy="465" r="78" fill="#FFFFFF"/>
  <text x="294" y="452" width="122" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#172B4D">40%</text>
  <text x="294" y="482" width="122" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#6B778C">Tesla share</text>
  <text x="294" y="504" width="122" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#97A0AF">市場第一名</text>

  <rect x="500" y="372" width="12" height="12" rx="3" fill="#172B4D"/>
  <text x="520" y="383" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#344563">Tesla 40.0%</text>
  <rect x="500" y="400" width="12" height="12" rx="3" fill="#00BFFF"/>
  <text x="520" y="411" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#344563">Luxgen 18.7%</text>
  <rect x="500" y="428" width="12" height="12" rx="3" fill="#36B37E"/>
  <text x="520" y="439" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#344563">BMW 16.7%</text>
  <rect x="500" y="456" width="12" height="12" rx="3" fill="#6554C0"/>
  <text x="520" y="467" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#344563">Mercedes 7.8%</text>
  <rect x="500" y="484" width="12" height="12" rx="3" fill="#FFAB00"/>
  <text x="520" y="495" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#344563">Kia 3.6%</text>
  <rect x="500" y="512" width="12" height="12" rx="3" fill="#C1C7D0"/>
  <text x="520" y="523" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#344563">Others 13.2%</text>

  <line x1="713" y1="320" x2="1170" y2="320" stroke="#EBECF0" stroke-width="1"/>
  <text x="714" y="292" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#172B4D">三個關鍵支持要點</text>
  <text x="714" y="316" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B778C">每張卡片只講一個管理層可記住的證據。</text>

  <rect x="714" y="346" width="454" height="82" rx="18" fill="#F7FAFC"/>
  <rect x="714" y="346" width="7" height="82" rx="3.5" fill="#172B4D"/>
  <circle cx="754" cy="387" r="19" fill="#172B4D"/>
  <text x="745" y="394" width="18" text-anchor="middle" font-family="Segoe UI" font-size="16" font-weight="800" fill="#FFFFFF">1</text>
  <path d="M790 398 L806 376 L823 388 L842 361" fill="none" stroke="#172B4D" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="864" y="378" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#172B4D">特斯拉持續主導</text>
  <text x="864" y="404" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5E6C84">充電網路與品牌信任度形成護城河，仍是消費者首選。</text>

  <rect x="714" y="452" width="454" height="82" rx="18" fill="#F7FAFC"/>
  <rect x="714" y="452" width="7" height="82" rx="3.5" fill="#00BFFF"/>
  <circle cx="754" cy="493" r="19" fill="#00BFFF"/>
  <text x="745" y="500" width="18" text-anchor="middle" font-family="Segoe UI" font-size="16" font-weight="800" fill="#FFFFFF">2</text>
  <path d="M792 503 C802 478 820 468 846 472 C831 486 817 499 792 503 Z" fill="#00BFFF" opacity="0.9"/>
  <text x="864" y="484" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#172B4D">Luxgen 快速突圍</text>
  <text x="864" y="510" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5E6C84">n7 以親民價格切入大眾市場，成為最具威脅的追趕者。</text>

  <rect x="714" y="558" width="454" height="82" rx="18" fill="#F7FAFC"/>
  <rect x="714" y="558" width="7" height="82" rx="3.5" fill="#36B37E"/>
  <circle cx="754" cy="599" r="19" fill="#36B37E"/>
  <text x="745" y="606" width="18" text-anchor="middle" font-family="Segoe UI" font-size="16" font-weight="800" fill="#FFFFFF">3</text>
  <path d="M792 612 L792 578 L846 578 L846 612 Z M804 590 L834 590 M804 600 L824 600" fill="none" stroke="#36B37E" stroke-width="5" stroke-linecap="round"/>
  <text x="864" y="590" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#172B4D">豪華車廠深化佈局</text>
  <text x="864" y="616" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5E6C84">BMW 與 Mercedes 擴充純電車款，穩固高階客群與品牌溢價。</text>

  <line x1="72" y1="686" x2="1208" y2="686" stroke="#DFE1E6" stroke-width="1"/>
  <text x="72" y="706" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#97A0AF">Source: illustrative market-share model · Designed for executive summary use</text>
</svg>
```

## Avoid in this skill
- ❌ Do not create a dense bullet-list slide; the technique depends on three structured evidence cards, not paragraph-heavy text.
- ❌ Do not use `<foreignObject>` for wrapped HTML text; use native `<text>` with explicit `width` attributes.
- ❌ Do not use `<mask>` or clip paths on non-image elements for the donut chart; use editable `<path>` segments instead.
- ❌ Do not rely on `marker-end` arrowheads for card callouts; if directional cues are needed, draw simple editable lines or paths.
- ❌ Do not over-decorate the background; executive infographic slides need high information clarity and restrained visual emphasis.

## Composition notes
- Reserve the top 25–30% for the title and one-sentence conclusion; this is the executive takeaway zone.
- Use the lower left 45% for the primary visual proof, ideally a donut, bar, quadrant, or concept diagram with a large central number.
- Use the lower right 40–45% for three evenly spaced evidence cards; each card should have one headline, one short sentence, and a small cue icon or badge.
- Keep color rhythm disciplined: deep navy for authority, cyan/green for momentum or growth, and pale gray card surfaces for hierarchy without visual noise.