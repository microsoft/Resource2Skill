# SVG Recipe — Proportional Timeline

## Visual mechanism
A horizontal timeline spine maps event dates to exact x-positions, so wide and narrow gaps visually communicate real elapsed time. Staggered callout cards alternate above and below the axis, with orange connector stems and nodes tying each event back to the proportional scale.

## SVG primitives needed
- 1× `<rect>` for the clean white slide background
- 1× `<line>` for the heavy central timeline spine
- 6× `<line>` for decade tick marks
- 12× `<line>` for vertical event connectors
- 12× `<circle>` for orange event nodes on the axis
- 12× `<rect>` for opaque white event cards that visually mask connector lines
- 12× `<text>` groups for year + event description, each with explicit `width`
- 1× `<linearGradient>` for a subtle background wash
- 1× `<radialGradient>` for soft node highlights
- 1× `<filter id="cardShadow">` for premium soft shadows under cards

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="72%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FFF3EA"/>
    </linearGradient>
    <radialGradient id="nodeFill" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFD6B7"/>
      <stop offset="45%" stop-color="#ED7D31"/>
      <stop offset="100%" stop-color="#C95513"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="80" y="68" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#111111">
    Proportional Regulatory Timeline
  </text>
  <text x="82" y="100" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#666666">
    Events are positioned by date, not evenly spaced — the long quiet periods and rapid policy clusters become visible.
  </text>

  <!-- decade ticks and axis -->
  <line x1="110" y1="410" x2="1170" y2="410" stroke="#111111" stroke-width="8" stroke-linecap="round"/>
  <line x1="110" y1="394" x2="110" y2="426" stroke="#111111" stroke-width="2"/>
  <line x1="322" y1="398" x2="322" y2="422" stroke="#111111" stroke-width="2"/>
  <line x1="534" y1="394" x2="534" y2="426" stroke="#111111" stroke-width="2"/>
  <line x1="746" y1="398" x2="746" y2="422" stroke="#111111" stroke-width="2"/>
  <line x1="958" y1="394" x2="958" y2="426" stroke="#111111" stroke-width="2"/>
  <line x1="1170" y1="398" x2="1170" y2="422" stroke="#111111" stroke-width="2"/>

  <text x="96" y="455" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">1970</text>
  <text x="308" y="455" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">1980</text>
  <text x="520" y="455" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">1990</text>
  <text x="732" y="455" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">2000</text>
  <text x="944" y="455" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">2010</text>
  <text x="1152" y="455" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777777">2020</text>

  <!-- orange connector stems, drawn before cards so white cards mask the line ends -->
  <line x1="195" y1="410" x2="195" y2="190" stroke="#ED7D31" stroke-width="3"/>
  <line x1="280" y1="410" x2="280" y2="510" stroke="#ED7D31" stroke-width="3"/>
  <line x1="407" y1="410" x2="407" y2="300" stroke="#ED7D31" stroke-width="3"/>
  <line x1="428" y1="410" x2="428" y2="585" stroke="#ED7D31" stroke-width="3"/>
  <line x1="470" y1="410" x2="470" y2="190" stroke="#ED7D31" stroke-width="3"/>
  <line x1="513" y1="410" x2="513" y2="510" stroke="#ED7D31" stroke-width="3"/>
  <line x1="534" y1="410" x2="534" y2="300" stroke="#ED7D31" stroke-width="3"/>
  <line x1="576" y1="410" x2="576" y2="585" stroke="#ED7D31" stroke-width="3"/>
  <line x1="682" y1="410" x2="682" y2="190" stroke="#ED7D31" stroke-width="3"/>
  <line x1="725" y1="410" x2="725" y2="510" stroke="#ED7D31" stroke-width="3"/>
  <line x1="1064" y1="410" x2="1064" y2="300" stroke="#ED7D31" stroke-width="3"/>
  <line x1="1085" y1="410" x2="1085" y2="585" stroke="#ED7D31" stroke-width="3"/>

  <!-- cards -->
  <rect x="120" y="110" width="150" height="82" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="205" y="508" width="150" height="82" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="337" y="218" width="140" height="84" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="358" y="585" width="140" height="82" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="400" y="110" width="150" height="82" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="438" y="508" width="150" height="82" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="464" y="218" width="140" height="84" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="506" y="585" width="140" height="82" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="607" y="110" width="150" height="82" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="650" y="508" width="150" height="82" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="994" y="218" width="140" height="84" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="1015" y="585" width="140" height="82" rx="14" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <!-- nodes on top of spine -->
  <circle cx="195" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="280" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="407" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="428" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="470" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="513" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="534" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="576" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="682" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="725" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="1064" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="1085" cy="410" r="12" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="4"/>

  <!-- card text -->
  <text x="136" y="137" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="136" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1974</tspan>
    <tspan x="136" dy="20">CFC ozone risk</tspan><tspan x="136" dy="17">identified</tspan>
  </text>
  <text x="221" y="535" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="221" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1978</tspan>
    <tspan x="221" dy="20">Aerosol bans begin</tspan><tspan x="221" dy="17">in key markets</tspan>
  </text>
  <text x="353" y="245" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="353" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1984</tspan>
    <tspan x="353" dy="20">Antarctic ozone</tspan><tspan x="353" dy="17">hole observed</tspan>
  </text>
  <text x="374" y="612" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="374" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1985</tspan>
    <tspan x="374" dy="20">Vienna Convention</tspan><tspan x="374" dy="17">signed</tspan>
  </text>
  <text x="416" y="137" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="416" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1987</tspan>
    <tspan x="416" dy="20">Montreal Protocol</tspan><tspan x="416" dy="17">adopted</tspan>
  </text>
  <text x="454" y="535" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="454" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1989</tspan>
    <tspan x="454" dy="20">Protocol enters</tspan><tspan x="454" dy="17">into force</tspan>
  </text>
  <text x="480" y="245" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="480" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1990</tspan>
    <tspan x="480" dy="20">London phase-out</tspan><tspan x="480" dy="17">amendment</tspan>
  </text>
  <text x="522" y="612" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="522" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1992</tspan>
    <tspan x="522" dy="20">Copenhagen controls</tspan><tspan x="522" dy="17">tightened</tspan>
  </text>
  <text x="623" y="137" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="623" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1997</tspan>
    <tspan x="623" dy="20">Licensing system</tspan><tspan x="623" dy="17">introduced</tspan>
  </text>
  <text x="666" y="535" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="666" dy="0" font-size="16" font-weight="700" fill="#ED7D31">1999</tspan>
    <tspan x="666" dy="20">Beijing Amendment</tspan><tspan x="666" dy="17">approved</tspan>
  </text>
  <text x="1010" y="245" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="1010" dy="0" font-size="16" font-weight="700" fill="#ED7D31">2015</tspan>
    <tspan x="1010" dy="20">Universal treaty</tspan><tspan x="1010" dy="17">ratification</tspan>
  </text>
  <text x="1031" y="612" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111111">
    <tspan x="1031" dy="0" font-size="16" font-weight="700" fill="#ED7D31">2016</tspan>
    <tspan x="1031" dy="20">Kigali adds HFC</tspan><tspan x="1031" dy="17">controls</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Evenly spacing the event nodes; the whole technique depends on proportional x-positioning.
- ❌ Using `marker-end` arrowheads on connector paths; vertical stems should be simple `<line>` elements.
- ❌ Applying filters to connector `<line>` elements; use shadows only on cards, nodes, paths, or text.
- ❌ Letting event cards have transparent fills; opaque white cards are needed to mask connector line ends cleanly.
- ❌ Overloading every event with long body copy; dense proportional clusters become unreadable quickly.

## Composition notes
- Keep the spine between 55–62% of slide height so there is enough vertical room for both upper and lower callouts.
- Calculate each event x-coordinate as: `axisStartX + ((eventYear - startYear) / (endYear - startYear)) * axisWidth`.
- Use 3–4 staggered vertical tracks to prevent collisions where events cluster tightly in time.
- Maintain a restrained palette: black for the axis, orange for dates/connectors/nodes, white cards, and light gray secondary scale labels.