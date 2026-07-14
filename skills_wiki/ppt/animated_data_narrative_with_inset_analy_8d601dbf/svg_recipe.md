# SVG Recipe — Animated Data Narrative with Inset Analysis

## Visual mechanism
A large, minimalist time-series column chart establishes the primary trend while a floating inset bar chart occupies the upper-left negative space to explain the key drivers. Each bar is drawn as an independent editable shape so PowerPoint can reveal the narrative sequentially “by category.”

## SVG primitives needed
- 12× `<rect>` for the primary annual publication columns, each as a separate animation-ready object
- 5× `<rect>` for the inset country contribution bars, also separate for sequential fly-in animation
- 1× `<rect>` for the inset analysis card background with a soft shadow
- 1× `<rect>` for a subtle slide background wash
- 2× `<line>` for the primary chart axes
- 1× `<line>` for the inset baseline
- 1× `<path>` for a decorative narrative connector curve between main chart and inset
- 1× `<path>` for a small custom arrowhead at the end of the connector
- Multiple `<text>` elements for title, subtitles, axis labels, data labels, category labels, and sequencing hints
- 1× `<linearGradient>` for the page background
- 1× `<linearGradient>` for the inset card highlight
- 1× `<filter id="softShadow">` applied to the inset card
- 1× `<filter id="softGlow">` applied to the latest-year emphasis column

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFF"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F2F6FB"/>
    </linearGradient>
    <linearGradient id="cardFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F6F9FF"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="74" y="54" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#172033">
    Annual Publications: Growth Story and Contribution Drivers
  </text>
  <text x="76" y="84" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#5B6475">
    Main trend builds first; inset analysis follows to explain the surge by country.
  </text>

  <path d="M526 244 C620 202, 722 196, 832 242 C898 270, 948 322, 994 382" fill="none" stroke="#B8C4D9" stroke-width="2" stroke-dasharray="8 8"/>
  <path d="M994 382 L975 378 L987 363 Z" fill="#B8C4D9"/>

  <rect x="68" y="102" width="480" height="285" rx="24" fill="url(#cardFill)" filter="url(#softShadow)"/>
  <text x="96" y="138" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#172033">
    Inset analysis: country contribution
  </text>
  <text x="96" y="162" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#687386">
    Fly in from left, one category at a time, after the main trend completes.
  </text>

  <line x1="194" y1="344" x2="504" y2="344" stroke="#D7DEE9" stroke-width="1"/>
  <g id="inset-step-01">
    <text x="96" y="204" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#3C4658">Saudi Arabia</text>
    <rect x="194" y="190" width="29" height="18" rx="9" fill="#4472C4"/>
    <text x="232" y="205" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4472C4">16</text>
  </g>
  <g id="inset-step-02">
    <text x="96" y="238" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#3C4658">Spain</text>
    <rect x="194" y="224" width="31" height="18" rx="9" fill="#ED7D31"/>
    <text x="234" y="239" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ED7D31">17</text>
  </g>
  <g id="inset-step-03">
    <text x="96" y="272" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#3C4658">England</text>
    <rect x="194" y="258" width="33" height="18" rx="9" fill="#A5A5A5"/>
    <text x="236" y="273" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#777777">18</text>
  </g>
  <g id="inset-step-04">
    <text x="96" y="306" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#3C4658">USA</text>
    <rect x="194" y="292" width="108" height="18" rx="9" fill="#FFC000"/>
    <text x="312" y="307" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#B88700">60</text>
  </g>
  <g id="inset-step-05">
    <text x="96" y="340" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#3C4658">China</text>
    <rect x="194" y="326" width="300" height="18" rx="9" fill="#70AD47"/>
    <text x="504" y="341" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4D812F">166</text>
  </g>

  <text x="96" y="370" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8A94A6">
    Build 2: categorical driver reveal
  </text>

  <line x1="214" y1="610" x2="1115" y2="610" stroke="#AEB8C7" stroke-width="1.5"/>
  <line x1="214" y1="260" x2="214" y2="610" stroke="#AEB8C7" stroke-width="1.5"/>

  <text x="146" y="438" width="210" transform="rotate(-90 146 438)" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#3C4658">
    Number of publications
  </text>
  <text x="650" y="688" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#3C4658">
    Year
  </text>

  <g id="col-step-01">
    <rect x="264" y="598" width="44" height="12" rx="5" fill="#4472C4"/>
    <text x="276" y="588" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4472C4">3</text>
    <text x="260" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2010</text>
  </g>
  <g id="col-step-02">
    <rect x="334" y="586" width="44" height="24" rx="5" fill="#ED7D31"/>
    <text x="346" y="576" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ED7D31">6</text>
    <text x="330" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2011</text>
  </g>
  <g id="col-step-03">
    <rect x="404" y="602" width="44" height="8" rx="4" fill="#A5A5A5"/>
    <text x="416" y="592" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#777777">2</text>
    <text x="400" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2012</text>
  </g>
  <g id="col-step-04">
    <rect x="474" y="562" width="44" height="48" rx="5" fill="#FFC000"/>
    <text x="483" y="552" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#B88700">12</text>
    <text x="470" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2013</text>
  </g>
  <g id="col-step-05">
    <rect x="544" y="554" width="44" height="56" rx="5" fill="#5B9BD5"/>
    <text x="553" y="544" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4B83B8">14</text>
    <text x="540" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2014</text>
  </g>
  <g id="col-step-06">
    <rect x="614" y="514" width="44" height="96" rx="5" fill="#70AD47"/>
    <text x="623" y="504" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4D812F">24</text>
    <text x="610" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2015</text>
  </g>
  <g id="col-step-07">
    <rect x="684" y="506" width="44" height="104" rx="5" fill="#4472C4"/>
    <text x="693" y="496" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4472C4">26</text>
    <text x="680" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2016</text>
  </g>
  <g id="col-step-08">
    <rect x="754" y="494" width="44" height="116" rx="5" fill="#ED7D31"/>
    <text x="763" y="484" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ED7D31">29</text>
    <text x="750" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2017</text>
  </g>
  <g id="col-step-09">
    <rect x="824" y="422" width="44" height="188" rx="5" fill="#A5A5A5"/>
    <text x="833" y="412" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#777777">47</text>
    <text x="820" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2018</text>
  </g>
  <g id="col-step-10">
    <rect x="894" y="330" width="44" height="280" rx="5" fill="#FFC000"/>
    <text x="903" y="320" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#B88700">70</text>
    <text x="890" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2019</text>
  </g>
  <g id="col-step-11">
    <rect x="964" y="326" width="44" height="284" rx="5" fill="#5B9BD5" filter="url(#softGlow)"/>
    <text x="973" y="316" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4B83B8">71</text>
    <text x="960" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2020</text>
  </g>
  <g id="col-step-12">
    <rect x="1034" y="542" width="44" height="68" rx="5" fill="#70AD47"/>
    <text x="1043" y="532" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4D812F">17</text>
    <text x="1030" y="634" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5D6676">2021</text>
  </g>

  <text x="808" y="260" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#687386">
    Build 1: columns float upward by year
  </text>
  <text x="1008" y="300" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#172033">
    Peak year
  </text>
  <text x="1008" y="321" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#687386">
    Highlight the inflection before explaining the mix.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Combining all columns or all inset bars into one `<path>`; it prevents clean “by category” animation in PowerPoint.
- ❌ Using SVG `<animate>` or `<animateTransform>` to mimic the reveal; create separate editable shapes and apply PowerPoint animations after translation.
- ❌ Applying `filter` to chart axes or guide `<line>` elements; line filters are dropped, so keep shadows/glows on `<rect>`, `<path>`, or `<text>`.
- ❌ Using `marker-end` for connector arrows; draw arrowheads as small editable `<path>` triangles instead.
- ❌ Overloading the chart with gridlines, legends, and heavy borders; the technique depends on negative space and clear narrative sequencing.

## Composition notes
- Keep the main chart in the lower two-thirds of the slide, with enough top-left negative space to host the inset card without covering important columns.
- Treat the inset as an analytical “lens”: smaller, floating, lightly shadowed, and visually calmer than the hero chart.
- Use varied bar colors consistently across both charts, but reserve glow or emphasis for the key peak column only.
- Build order should be: title and axes → main columns left-to-right → peak annotation → inset card → inset bars top-to-bottom.