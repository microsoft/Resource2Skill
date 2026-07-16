# SVG Recipe — Consulting-Grade "Dot-Dash" Action Slide (The SCR Framework)

## Visual mechanism
A persuasive consulting slide built around typographic hierarchy: a small SCR kicker, a dominant action title, a thin accent divider, and proof points organized as bold “dot” statements with indented grey “dash” evidence. Use disciplined white space and only one restrained accent color so the executive conclusion feels authoritative rather than decorative.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for the crisp blue divider rule under the action title
- 1× `<rect>` for a subtle right-side evidence card
- 1× `<filter id="cardShadow">` applied to the evidence card for a premium but restrained lift
- 6× `<circle>` for dot bullets and SCR progress markers
- 1× `<path>` for a small editable sparkline inside the evidence card
- 1× `<linearGradient>` for the right evidence card’s pale executive-blue fill
- Multiple `<text>` elements with explicit `width` attributes for kicker, title lines, dot statements, dash evidence, SCR labels, and data callouts
- Nested `<tspan>` inside selected `<text>` elements for inline emphasis and data highlighting

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="evidenceBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FBFF"/>
      <stop offset="100%" stop-color="#EAF3FB"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Kicker / SCR context -->
  <text x="76" y="56" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.2" fill="#00519B">SITUATION</text>

  <circle cx="1038" cy="50" r="8" fill="#00519B"/>
  <text x="1054" y="56" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#00519B">Situation</text>
  <circle cx="1142" cy="50" r="7" fill="#D4DCE5"/>
  <text x="1158" y="56" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#7A8591">Complication</text>
  <circle cx="1242" cy="50" r="7" fill="#D4DCE5"/>

  <!-- Action title -->
  <text x="76" y="104" width="980" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#262626">
    Though the point-in-time count dropped in 2019,
  </text>
  <text x="76" y="148" width="980" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#262626">
    homelessness continues to increase across the county
  </text>

  <rect x="76" y="184" width="1128" height="3" fill="#00519B"/>

  <!-- Body: dot-dash proof structure -->
  <circle cx="91" cy="244" r="5.5" fill="#262626"/>
  <text x="114" y="251" width="710" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#262626">
    More than 22,000 households experience homelessness in Seattle each year
  </text>
  <text x="139" y="289" width="690" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#595959">
    – 22,500 households were homeless for at least some of 2018
  </text>
  <text x="139" y="320" width="690" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#595959">
    – 30% of households experiencing homelessness were chronically homeless
  </text>

  <circle cx="91" cy="391" r="5.5" fill="#262626"/>
  <text x="114" y="398" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#262626">
    Despite robust economic growth, housing supply and incomes have not kept pace
  </text>
  <text x="139" y="436" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#595959">
    – Rents have grown faster than incomes, increasing pressure on the poorest households
  </text>
  <text x="139" y="467" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#595959">
    – Since 2010, the region has lost 112,000 units affordable to low-income earners
  </text>

  <circle cx="91" cy="538" r="5.5" fill="#262626"/>
  <text x="114" y="545" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#262626">
    The system is serving more people, but inflow is outpacing exits to stable housing
  </text>
  <text x="139" y="583" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#595959">
    – Prevention and rapid rehousing capacity remain below the scale of annual need
  </text>
  <text x="139" y="614" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#595959">
    – The implication is a required shift from program optimization to system throughput
  </text>

  <!-- Right evidence card -->
  <rect x="895" y="245" width="310" height="310" rx="18" fill="url(#evidenceBlue)" filter="url(#cardShadow)"/>
  <text x="925" y="286" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.6" fill="#00519B">KEY EVIDENCE</text>
  <text x="925" y="345" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="700" fill="#262626">
    <tspan fill="#00519B">22.5K</tspan>
  </text>
  <text x="925" y="377" width="238" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#595959">households experienced homelessness in 2018</text>

  <path d="M930 478 C960 450, 982 462, 1008 430 C1038 394, 1062 420, 1092 385 C1124 348, 1150 356, 1172 323"
        fill="none" stroke="#00519B" stroke-width="4" stroke-linecap="round"/>
  <rect x="930" y="500" width="242" height="1.5" fill="#B9CFE2"/>
  <text x="930" y="526" width="78" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#7A8591">2010</text>
  <text x="1094" y="526" width="78" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" text-anchor="end" fill="#7A8591">2019</text>
  <text x="925" y="590" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#595959">
    Use the card only when one statistic makes the argument materially sharper.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense charts, dashboards, or decorative illustrations that compete with the action title
- ❌ Center-aligned titles; this style depends on a strong left reading edge
- ❌ Multiple accent colors; the consulting look is created by restraint
- ❌ Auto-wrapped SVG text without explicit `width`; every text box must declare its intended width
- ❌ Heavy shadows, gradients, or 3D effects on the main body; reserve visual polish for one small evidence card if needed

## Composition notes
- Keep the top 25% for the kicker, action title, and divider; the conclusion must dominate before the reader reaches the evidence.
- Body copy should occupy the left two-thirds, with dot statements bold and dash evidence indented beneath each statement.
- Use the right third only for a single proof card, SCR tracker, or empty white space; never fill it with secondary arguments.
- Maintain a strict color rhythm: charcoal for conclusions, grey for evidence, blue only for structure and emphasis.