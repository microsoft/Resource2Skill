# SVG Recipe — Explanatory Storytelling Dashboard

## Visual mechanism
A clean executive dashboard guides the audience through a narrative scan path: headline KPIs first, then the primary time-series trend, then categorical drivers and item-level detail. Whitespace, soft card shadows, restrained gridlines, and one strong accent color create hierarchy without overwhelming the data.

## SVG primitives needed
- 1× `<rect>` full-slide background with a subtle gradient
- 7× `<rect>` card containers for KPI, trend chart, driver panel, insight callout, and detail table
- 20+× `<rect>` for KPI accent strips, horizontal bars, mini heatmap/table cells, and progress fills
- 1× `<path>` filled area under the primary line chart using a gradient
- 2× `<path>` stroked line-series for current vs prior period trend comparison
- 3× `<circle>` numbered story-step dots to reinforce the guided reading path
- 10+× `<line>` for chart axes, gridlines, separators, and table rules
- 1× `<filter id="softShadow">` applied to card rectangles
- 1× `<filter id="greenGlow">` applied to the positive trend highlight
- 3× `<linearGradient>` for background, KPI card sheen, and chart area fill
- Many `<text>` elements with explicit `width` attributes for titles, KPI values, chart labels, annotations, table values, and axis labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFF"/>
      <stop offset="100%" stop-color="#EEF4FA"/>
    </linearGradient>
    <linearGradient id="cardSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7FAFD"/>
    </linearGradient>
    <linearGradient id="areaGreen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#76BC21" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#76BC21" stop-opacity="0.03"/>
    </linearGradient>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="greenGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <text x="48" y="44" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#1C3872">REGIONAL SALES DASHBOARD: SEPTEMBER 2021</text>
  <text x="50" y="72" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7B8794">Narrative view: headline performance → monthly trend → key drivers → store-level actions</text>
  <rect x="1038" y="30" width="194" height="38" rx="19" fill="#FFFFFF" stroke="#D7E0EA"/>
  <text x="1062" y="55" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#26334B">Region: New York</text>

  <circle cx="52" cy="120" r="13" fill="#1C3872"/>
  <text x="47" y="126" width="12" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">1</text>
  <text x="76" y="125" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#26334B">Start with the outcome</text>

  <rect x="48" y="142" width="300" height="104" rx="18" fill="url(#cardSheen)" filter="url(#softShadow)"/>
  <rect x="48" y="142" width="7" height="104" rx="3.5" fill="#76BC21"/>
  <text x="72" y="177" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#7B8794">Total Monthly Revenue</text>
  <text x="72" y="220" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#26334B">$50,618</text>
  <text x="270" y="197" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#76BC21">+1.6%</text>
  <text x="270" y="218" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">M-o-M</text>

  <rect x="370" y="142" width="178" height="104" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="392" y="177" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7B8794">Avg. Order Value</text>
  <text x="392" y="217" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#26334B">$84.20</text>
  <text x="505" y="219" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#C00000">−3%</text>

  <rect x="568" y="142" width="178" height="104" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="590" y="177" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7B8794">Conversion Rate</text>
  <text x="590" y="217" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#26334B">7.8%</text>
  <text x="694" y="219" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#76BC21">+0.4</text>

  <circle cx="52" cy="292" r="13" fill="#1C3872"/>
  <text x="47" y="298" width="12" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">2</text>
  <text x="76" y="297" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#26334B">Explain the trajectory</text>

  <rect x="48" y="314" width="760" height="262" rx="20" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="78" y="350" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#26334B">Revenue by Month</text>
  <text x="650" y="350" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8794">USD, thousands</text>
  <line x1="98" y1="520" x2="760" y2="520" stroke="#CBD5E1" stroke-width="1"/>
  <line x1="98" y1="468" x2="760" y2="468" stroke="#E6ECF3" stroke-width="1"/>
  <line x1="98" y1="416" x2="760" y2="416" stroke="#E6ECF3" stroke-width="1"/>
  <line x1="98" y1="364" x2="760" y2="364" stroke="#E6ECF3" stroke-width="1"/>
  <text x="72" y="524" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8A96A3">40</text>
  <text x="72" y="420" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8A96A3">55</text>
  <text x="72" y="368" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8A96A3">65</text>
  <path d="M98 496 L181 478 L264 404 L347 436 L430 378 L513 398 L596 456 L679 488 L760 450 L760 520 L98 520 Z" fill="url(#areaGreen)"/>
  <path d="M98 498 L181 480 L264 406 L347 438 L430 380 L513 400 L596 458 L679 490 L760 452" fill="none" stroke="#76BC21" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" filter="url(#greenGlow)"/>
  <path d="M98 506 L181 492 L264 430 L347 456 L430 410 L513 426 L596 470 L679 502 L760 480" fill="none" stroke="#A6A6A6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="7 7"/>
  <circle cx="760" cy="452" r="6" fill="#76BC21"/>
  <rect x="635" y="378" width="128" height="44" rx="12" fill="#F1F8E9" stroke="#CDE9B8"/>
  <text x="650" y="397" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#477A11">September rebound</text>
  <text x="650" y="413" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#5B6B46">Promotion lift offset AOV dip</text>
  <text x="94" y="548" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">Jan</text>
  <text x="178" y="548" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">Feb</text>
  <text x="260" y="548" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">Mar</text>
  <text x="344" y="548" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">Apr</text>
  <text x="426" y="548" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">May</text>
  <text x="510" y="548" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">Jun</text>
  <text x="594" y="548" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">Jul</text>
  <text x="676" y="548" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">Aug</text>
  <text x="756" y="548" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7B8794">Sep</text>

  <circle cx="846" cy="120" r="13" fill="#1C3872"/>
  <text x="841" y="126" width="12" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">3</text>
  <text x="870" y="125" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#26334B">Reveal the drivers</text>
  <rect x="840" y="142" width="392" height="434" rx="20" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="870" y="178" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#26334B">Category Contribution</text>
  <text x="870" y="200" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B8794">Share of monthly revenue and variance vs. prior month</text>
  <text x="870" y="242" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#26334B">Electronics</text>
  <rect x="990" y="230" width="190" height="14" rx="7" fill="#E8EEF5"/>
  <rect x="990" y="230" width="158" height="14" rx="7" fill="#76BC21"/>
  <text x="1190" y="243" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#76BC21">+8%</text>
  <text x="870" y="286" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#26334B">Home</text>
  <rect x="990" y="274" width="190" height="14" rx="7" fill="#E8EEF5"/>
  <rect x="990" y="274" width="128" height="14" rx="7" fill="#76BC21"/>
  <text x="1190" y="287" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#76BC21">+4%</text>
  <text x="870" y="330" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#26334B">Apparel</text>
  <rect x="990" y="318" width="190" height="14" rx="7" fill="#E8EEF5"/>
  <rect x="990" y="318" width="105" height="14" rx="7" fill="#76BC21"/>
  <text x="1190" y="331" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#76BC21">+2%</text>
  <text x="870" y="374" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#26334B">Beauty</text>
  <rect x="990" y="362" width="190" height="14" rx="7" fill="#E8EEF5"/>
  <rect x="990" y="362" width="76" height="14" rx="7" fill="#C00000"/>
  <text x="1190" y="375" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#C00000">−5%</text>
  <rect x="870" y="414" width="322" height="108" rx="16" fill="#F7FAFD" stroke="#DCE5EF"/>
  <text x="895" y="444" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#26334B">Narrative takeaway</text>
  <text x="895" y="470" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5F6B7A">Growth is concentrated in high-ticket Electronics; Beauty weakness is the only material drag.</text>
  <text x="895" y="502" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#76BC21">Recommended action: extend bundle promo.</text>

  <rect x="48" y="604" width="1184" height="78" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="76" y="635" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26334B">Store-level watchlist</text>
  <line x1="260" y1="622" x2="260" y2="664" stroke="#E1E8F0"/>
  <text x="286" y="628" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#7B8794">STORE</text>
  <text x="286" y="656" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#26334B">Manhattan East</text>
  <rect x="430" y="638" width="70" height="18" rx="9" fill="#EAF6DF"/>
  <text x="445" y="652" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#477A11">+12%</text>
  <text x="540" y="656" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#26334B">Brooklyn North</text>
  <rect x="690" y="638" width="70" height="18" rx="9" fill="#FDEAEA"/>
  <text x="708" y="652" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#C00000">−7%</text>
  <text x="800" y="656" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#26334B">Queens Center</text>
  <rect x="950" y="638" width="70" height="18" rx="9" fill="#EAF6DF"/>
  <text x="968" y="652" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#477A11">+5%</text>
  <text x="1054" y="656" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5F6B7A">Focus coaching on Beauty attach rate</text>
</svg>
```

## Avoid in this skill
- ❌ Overbuilding the dashboard as many equal-weight boxes; the technique depends on a clear narrative hierarchy, not a uniform grid.
- ❌ Heavy chart borders, dark gridlines, or dense axis labels that compete with the KPI and takeaway.
- ❌ Using bitmap chart screenshots when the chart can be recreated with editable SVG paths, lines, and rectangles.
- ❌ Applying `clip-path` to chart shapes or cards; clipping is only reliable for `<image>` crops.
- ❌ Relying on tiny text tables; keep detail rows selective and readable in presentation mode.

## Composition notes
- Keep the top-left KPI block visually dominant; it should answer “how are we doing?” before the audience reaches any chart.
- Give the main trend chart the largest central card, with generous internal padding and only a few gridlines.
- Place driver bars and the written takeaway on the right to create a natural second read after the trend.
- Use one positive accent color repeatedly for the successful narrative thread, with red reserved only for exceptions or risks.