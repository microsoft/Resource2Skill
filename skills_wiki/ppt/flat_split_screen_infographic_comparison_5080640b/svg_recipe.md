# SVG Recipe — Flat Split-Screen Infographic Comparison

## Visual mechanism
A poster-like comparison slide built from two high-contrast vertical color fields and one dark footer band. Oversized percentages dominate each half, while simple flat vector illustrations and compact footer stats provide context without competing for attention.

## SVG primitives needed
- 3× `<rect>` for the left panel, right panel, and full-width footer color blocks
- 4× `<line>` for thin footer dividers and simple chart axes
- 6× `<circle>` for illustration base plates, small data dots, and footer icon badges
- 12× `<rect>` for flat bar-chart columns, footer icon blocks, and label underlines
- 8× `<path>` for pie-chart wedges, simple person/food/data icons, and decorative flat shapes
- 14× `<text>` with explicit `width` attributes for macro percentages, labels, titles, and footer statistics
- Optional `<defs>` color definitions are not required; keep the technique mostly flat and solid-filled

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Flat design: no shadows or gradients needed for the core technique -->
  </defs>

  <!-- Background color blocking -->
  <rect x="0" y="0" width="640" height="528" fill="#FFB800"/>
  <rect x="640" y="0" width="640" height="528" fill="#1F262E"/>
  <rect x="0" y="528" width="1280" height="192" fill="#262626"/>

  <!-- Left panel text -->
  <text x="64" y="88" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#FFFFFF">Total Respondents</text>
  <text x="62" y="228" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="122" font-weight="800" fill="#FFFFFF">98%</text>
  <text x="70" y="282" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="700" fill="#FFFFFF">Respondents</text>
  <rect x="70" y="306" width="170" height="7" fill="#FFFFFF" opacity="0.8"/>

  <!-- Left flat illustration: circular plate with bar chart -->
  <circle cx="500" cy="282" r="150" fill="#E19E00"/>
  <circle cx="500" cy="282" r="116" fill="#F7B312"/>
  <line x1="420" y1="350" x2="580" y2="350" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
  <line x1="420" y1="218" x2="420" y2="350" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.85"/>
  <rect x="442" y="286" width="34" height="64" rx="3" fill="#FFFFFF"/>
  <rect x="492" y="232" width="34" height="118" rx="3" fill="#FFFFFF"/>
  <rect x="542" y="262" width="34" height="88" rx="3" fill="#FFFFFF"/>
  <circle cx="459" cy="265" r="7" fill="#FFFFFF"/>
  <circle cx="509" cy="211" r="7" fill="#FFFFFF"/>
  <circle cx="559" cy="241" r="7" fill="#FFFFFF"/>
  <path d="M459 265 L509 211 L559 241" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Right panel text -->
  <text x="704" y="88" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#FFFFFF">Favorite Food Type</text>
  <text x="702" y="228" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="122" font-weight="800" fill="#FFFFFF">54%</text>
  <text x="710" y="282" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="700" fill="#FFFFFF">Pizza &amp; Burger</text>
  <rect x="710" y="306" width="190" height="7" fill="#FFB800"/>

  <!-- Right flat illustration: circular plate with pie chart and food cue -->
  <circle cx="1100" cy="282" r="150" fill="#2F3B48"/>
  <circle cx="1100" cy="282" r="116" fill="#344250"/>
  <path d="M1100 282 L1100 186 A96 96 0 1 1 1012 320 Z" fill="#FFFFFF"/>
  <path d="M1100 282 L1012 320 A96 96 0 0 1 1100 186 Z" fill="#FFB800"/>
  <circle cx="1100" cy="282" r="46" fill="#344250"/>
  <path d="M1068 380 C1078 358 1122 358 1132 380 L1122 393 L1078 393 Z" fill="#FFB800"/>
  <rect x="1064" y="390" width="72" height="15" rx="7" fill="#FFFFFF"/>
  <path d="M1070 405 L1130 405 L1120 420 L1080 420 Z" fill="#FFB800"/>

  <!-- Footer dividers -->
  <line x1="320" y1="560" x2="320" y2="690" stroke="#FFFFFF" stroke-width="2" opacity="0.15"/>
  <line x1="640" y1="560" x2="640" y2="690" stroke="#FFFFFF" stroke-width="2" opacity="0.15"/>
  <line x1="960" y1="560" x2="960" y2="690" stroke="#FFFFFF" stroke-width="2" opacity="0.15"/>

  <!-- Footer stat 1 -->
  <circle cx="78" cy="621" r="28" fill="#FFB800"/>
  <path d="M78 604 A14 14 0 1 1 77.9 604 M56 650 C61 628 95 628 100 650 Z" fill="#FFFFFF"/>
  <text x="128" y="616" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800" fill="#FFFFFF">55%</text>
  <text x="130" y="653" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#CFCFCF">Male Respondent</text>

  <!-- Footer stat 2 -->
  <circle cx="398" cy="621" r="28" fill="#FFB800"/>
  <path d="M398 603 A14 14 0 1 1 397.9 603 M376 650 C381 628 415 628 420 650 Z" fill="#FFFFFF"/>
  <text x="448" y="616" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800" fill="#FFFFFF">45%</text>
  <text x="450" y="653" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#CFCFCF">Female Respondent</text>

  <!-- Footer stat 3 -->
  <circle cx="718" cy="621" r="28" fill="#FFB800"/>
  <path d="M705 611 L731 611 L725 644 L711 644 Z M704 602 L732 602" fill="none"
        stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="768" y="616" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800" fill="#FFFFFF">20%</text>
  <text x="770" y="653" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#CFCFCF">Kabab &amp; Grills</text>

  <!-- Footer stat 4 -->
  <circle cx="1038" cy="621" r="28" fill="#FFB800"/>
  <path d="M1020 612 C1032 596 1056 596 1068 612 L1059 642 L1029 642 Z" fill="#FFFFFF"/>
  <rect x="1025" y="630" width="38" height="8" rx="4" fill="#FFB800"/>
  <text x="1088" y="616" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800" fill="#FFFFFF">14%</text>
  <text x="1090" y="653" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#CFCFCF">Rice &amp; Curries</text>
</svg>
```

## Avoid in this skill
- ❌ Gradients, glassmorphism, or heavy shadows; they weaken the flat poster-style contrast.
- ❌ Complex chart axes or dashboard tables; the macro percentages should remain the main data story.
- ❌ Clip paths on non-image shapes; use direct `<circle>`, `<rect>`, and `<path>` illustrations instead.
- ❌ `marker-end` arrowheads on paths; this comparison style usually does not need arrows, and path arrowheads will not translate reliably.
- ❌ Text without explicit `width`; every headline, label, and stat needs a fixed width for clean PowerPoint rendering.

## Composition notes
- Keep the top comparison zone around 70–75% of slide height, with the footer occupying the remaining 25–30%.
- Split the canvas exactly 50/50 vertically; align the left edges of both text groups to create a mirrored executive-summary feel.
- Use the illustrations as secondary anchors on the outer/right side of each panel, not as central decorative clutter.
- Repeat the accent yellow in the footer icons and right-panel underline to create rhythm across the dark areas.