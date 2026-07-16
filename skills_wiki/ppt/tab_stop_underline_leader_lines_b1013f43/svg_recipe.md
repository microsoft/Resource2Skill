# SVG Recipe — Tab-Stop Underline Leader Lines

## Visual mechanism
A formal agenda / table-of-contents layout uses left-aligned section names, right-flush page or step numbers, and dotted underline-style leader lines that visually “expand” between them. In SVG, reproduce the tab-stop effect with separately editable `<text>` elements and precisely positioned dashed `<line>` leaders, all ending at one shared right alignment rail.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<linearGradient>` for a soft executive background wash
- 1× `<filter id="cardShadow">` for a subtle elevated agenda card
- 1× `<rect>` for the main white content card
- 1× `<rect>` for the left accent rail
- 1× `<path>` for a quiet decorative corner flourish
- 1× `<text>` for the slide eyebrow / section label
- 1× `<text>` for the main title
- 1× `<text>` for the small right-column label
- 9× `<text>` for agenda item labels
- 9× `<line>` for dotted or dashed leader lines
- 9× `<text>` for right-aligned page / section numbers
- 3× `<circle>` for highlighted major-section markers

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFB"/>
      <stop offset="55%" stop-color="#EEF5F7"/>
      <stop offset="100%" stop-color="#E6EFF2"/>
    </linearGradient>

    <linearGradient id="tealAccent" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1D5772"/>
      <stop offset="100%" stop-color="#58A6B3"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M1020,0 C1125,55 1190,120 1280,96 L1280,0 Z"
        fill="#D7E9EE" opacity="0.75"/>
  <path d="M0,650 C115,610 210,628 320,720 L0,720 Z"
        fill="#DDECEF" opacity="0.6"/>

  <!-- Main card -->
  <rect x="92" y="74" width="1096" height="572" rx="34"
        fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="92" y="74" width="14" height="572" rx="7" fill="url(#tealAccent)"/>

  <!-- Header -->
  <text x="150" y="132" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.5"
        fill="#58A6B3">BOARD PACKET / Q3 REVIEW</text>

  <text x="150" y="184" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="750"
        fill="#1D5772">Table of Contents</text>

  <line x1="150" y1="214" x2="1072" y2="214"
        stroke="#D5E2E6" stroke-width="1.5"/>

  <text x="1010" y="184" width="90"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.5"
        fill="#8AA0A8" text-anchor="end">PAGE</text>

  <!-- Agenda rows: major item -->
  <circle cx="158" cy="268" r="13" fill="#1D5772"/>
  <text x="158" y="273" width="26"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#FFFFFF"
        text-anchor="middle">1</text>
  <text x="188" y="275" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#111820">Executive Summary</text>
  <line x1="424" y1="268" x2="1014" y2="268"
        stroke="#1D5772" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>
  <text x="1072" y="275" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#111820" text-anchor="end">01</text>

  <!-- Agenda rows: regular items -->
  <text x="188" y="323" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="650" fill="#111820">Market Context</text>
  <line x1="376" y1="316" x2="1014" y2="316"
        stroke="#899AA2" stroke-width="1.7" stroke-dasharray="1 7" stroke-linecap="round"/>
  <text x="1072" y="323" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="600" fill="#111820" text-anchor="end">03</text>

  <text x="226" y="366" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#516169">Customer demand signals</text>
  <line x1="482" y1="359" x2="1014" y2="359"
        stroke="#B3C0C5" stroke-width="1.4" stroke-dasharray="1 7" stroke-linecap="round"/>
  <text x="1072" y="366" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" fill="#516169" text-anchor="end">04</text>

  <text x="226" y="406" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#516169">Competitive landscape</text>
  <line x1="456" y1="399" x2="1014" y2="399"
        stroke="#B3C0C5" stroke-width="1.4" stroke-dasharray="1 7" stroke-linecap="round"/>
  <text x="1072" y="406" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" fill="#516169" text-anchor="end">05</text>

  <!-- Agenda rows: major item -->
  <circle cx="158" cy="458" r="13" fill="#58A6B3"/>
  <text x="158" y="463" width="26"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#FFFFFF"
        text-anchor="middle">2</text>
  <text x="188" y="465" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#111820">Financial Performance</text>
  <line x1="486" y1="458" x2="1014" y2="458"
        stroke="#1D5772" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>
  <text x="1072" y="465" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#111820" text-anchor="end">07</text>

  <text x="226" y="508" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#516169">Revenue bridge and margin drivers</text>
  <line x1="544" y1="501" x2="1014" y2="501"
        stroke="#B3C0C5" stroke-width="1.4" stroke-dasharray="1 7" stroke-linecap="round"/>
  <text x="1072" y="508" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" fill="#516169" text-anchor="end">08</text>

  <text x="226" y="548" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#516169">Operating expense outlook</text>
  <line x1="486" y1="541" x2="1014" y2="541"
        stroke="#B3C0C5" stroke-width="1.4" stroke-dasharray="1 7" stroke-linecap="round"/>
  <text x="1072" y="548" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" fill="#516169" text-anchor="end">10</text>

  <!-- Agenda rows: final major item -->
  <circle cx="158" cy="600" r="13" fill="#1D5772"/>
  <text x="158" y="605" width="26"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#FFFFFF"
        text-anchor="middle">3</text>
  <text x="188" y="607" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#111820">Decisions & Next Steps</text>
  <line x1="472" y1="600" x2="1014" y2="600"
        stroke="#1D5772" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>
  <text x="1072" y="607" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#111820" text-anchor="end">12</text>
</svg>
```

## Avoid in this skill
- ❌ Relying on literal tab characters inside one `<text>` element; SVG-to-PPT conversion will not preserve PowerPoint tab-stop behavior.
- ❌ Manually typed dot strings such as `"........"`; they wrap poorly, are hard to align, and look uneven across fonts.
- ❌ Using `marker-end` for leader lines; this technique needs plain dotted or dashed `<line>` elements.
- ❌ Applying `filter` to `<line>` elements; line filters are not reliably translated.
- ❌ Omitting `width` on `<text>` elements; PowerPoint needs explicit text-box width for clean rendering.

## Composition notes
- Keep a single invisible right alignment rail for all page numbers, typically around `x=1070`, and end every leader line just before it.
- Use heavier dotted leaders for major sections and lighter gray dotted leaders for indented subsections.
- Leave generous negative space above the first row; the title and TOC should feel editorial, not like a data table.
- Align leader-line `y` values slightly above the text baseline so they read like an underline applied to the missing tab span.