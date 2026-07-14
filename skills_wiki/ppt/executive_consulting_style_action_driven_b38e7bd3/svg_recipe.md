# SVG Recipe — Executive Consulting Action-Driven Layout

## Visual mechanism
A declarative action title states the conclusion first, while a stripped-down evidence chart and concise implication panel prove the claim below. The layout uses disciplined whitespace, muted corporate colors, direct labels, and a thin separator to create a board-ready consulting slide.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<linearGradient>` for a restrained navy accent strip
- 1× `<filter id="softShadow">` for subtle card elevation
- 1× `<line>` for the header/body separator
- 5× `<rect>` for minimalist vertical chart bars
- 1× `<line>` for the chart baseline
- 1× `<path>` for a thin trend annotation arrow, with arrowhead drawn manually as a path
- 3× `<rect>` for evidence and implication cards
- 1× `<path>` for a small executive “so what” accent wedge
- Multiple `<text>` elements with explicit `width` for action title, subtitles, labels, callouts, and footer
- Nested `<tspan>` elements for multi-line consulting labels and emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#002D72"/>
      <stop offset="100%" stop-color="#2B7281"/>
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

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Header: action title -->
  <rect x="48" y="38" width="8" height="92" fill="url(#navyAccent)"/>
  <text x="72" y="58" width="1010" font-family="Georgia, 'Times New Roman', serif" font-size="31" fill="#262626">
    <tspan x="72" dy="0">Homelessness has risen 32% since 2016 despite a temporary 2019 dip,</tspan>
    <tspan x="72" dy="39">requiring additional emergency capacity before winter demand peaks.</tspan>
  </text>
  <text x="72" y="143" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#6E6E6E">
    Direct labels and a single implication box focus leadership on the decision, not the mechanics of the data.
  </text>
  <line x1="48" y1="174" x2="1232" y2="174" stroke="#C8C8C8" stroke-width="1"/>

  <!-- Left evidence card -->
  <rect x="66" y="216" width="720" height="392" rx="4" fill="#FFFFFF" stroke="#E1E1E1" stroke-width="1" filter="url(#softShadow)"/>
  <text x="96" y="252" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#262626">
    Point-in-time homeless population, 2016–2020E
  </text>
  <text x="96" y="278" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#737373">
    Thousands of people counted or estimated
  </text>

  <!-- Minimal chart baseline and bars -->
  <line x1="120" y1="536" x2="728" y2="536" stroke="#AFAFAF" stroke-width="1"/>
  <rect x="142" y="350" width="72" height="186" fill="#D9D9D9"/>
  <rect x="262" y="324" width="72" height="212" fill="#D9D9D9"/>
  <rect x="382" y="314" width="72" height="222" fill="#D9D9D9"/>
  <rect x="502" y="331" width="72" height="205" fill="#D9D9D9"/>
  <rect x="622" y="290" width="72" height="246" fill="#002D72"/>

  <!-- Direct data labels -->
  <text x="137" y="333" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#262626">10.2k</text>
  <text x="257" y="307" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#262626">11.6k</text>
  <text x="377" y="297" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#262626">12.1k</text>
  <text x="497" y="314" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#262626">11.2k</text>
  <text x="617" y="273" width="92" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700" fill="#002D72">13.5k</text>

  <!-- X labels -->
  <text x="137" y="566" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2016</text>
  <text x="257" y="566" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2017</text>
  <text x="377" y="566" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2018</text>
  <text x="497" y="566" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2019</text>
  <text x="617" y="566" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#002D72" font-weight="700">2020E</text>

  <!-- Trend annotation with hand-built arrowhead -->
  <path d="M160 395 C285 285, 430 282, 650 248" fill="none" stroke="#2B7281" stroke-width="3"/>
  <path d="M650 248 L628 240 L638 264 Z" fill="#2B7281"/>
  <text x="352" y="244" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#2B7281" font-weight="700">
    Long-term increase resumes after one-year dip
  </text>

  <!-- Right implication panel -->
  <rect x="830" y="216" width="384" height="392" rx="4" fill="#F7F9FB" stroke="#D8DEE6" stroke-width="1"/>
  <path d="M830 216 L892 216 L830 278 Z" fill="#002D72"/>
  <text x="868" y="260" width="292" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#262626">
    Executive implication
  </text>
  <text x="868" y="296" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#002D72">
    +3.3k
  </text>
  <text x="944" y="296" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#262626">
    additional people versus 2016 baseline
  </text>

  <rect x="868" y="344" width="306" height="1" fill="#D0D7DE"/>
  <text x="868" y="378" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#262626">
    Recommended actions
  </text>
  <text x="868" y="412" width="314" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#333333">
    <tspan x="868" dy="0">1. Fund 250 incremental shelter beds in Q4</tspan>
    <tspan x="868" dy="28">2. Shift outreach teams to high-growth districts</tspan>
    <tspan x="868" dy="28">3. Launch weekly capacity review with agencies</tspan>
  </text>

  <rect x="868" y="520" width="306" height="48" rx="3" fill="#FFFFFF" stroke="#D8DEE6" stroke-width="1"/>
  <text x="888" y="550" width="268" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">
    Decision required today: approve winter surge budget envelope
  </text>

  <!-- Footer -->
  <text x="48" y="674" width="900" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10.5" fill="#7A7A7A">
    Source: Regional Point-in-Time Count Data; Comprehensive Homeless Management Information System. Note: 2020 is management estimate.
  </text>
  <text x="1188" y="674" width="44" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10.5" fill="#7A7A7A">
    04
  </text>
</svg>
```

## Avoid in this skill
- ❌ Topical titles such as “Homelessness statistics”; the title must state the business conclusion.
- ❌ Heavy chart furniture: legends, gridlines, axis boxes, tick clutter, 3D bars, or decorative gradients inside the data bars.
- ❌ Separate legend blocks when direct labels can sit on or near the data.
- ❌ Overusing shadows, icons, and saturated colors; the premium consulting look depends on restraint.
- ❌ SVG arrow markers on paths; draw arrowheads manually with small `<path>` shapes if needed.

## Composition notes
- Reserve the top 18–22% of the slide for the action title, subtitle, and separator; this is the narrative anchor.
- Place the primary evidence visualization in the left two-thirds of the body and the decision implication in the right third.
- Use one accent color only for the key data point and related annotation; keep context data light grey.
- Keep the footer tiny and unobtrusive, but always present for board-level credibility.