# SVG Recipe — Line-Art Coloring Page Aesthetic

## Visual mechanism
A dense black-and-white “coloring book” composition: every element is pure white fill with heavy black outlines, including the typography, data marks, frame, and playful filler doodles. The slide feels hand-printable and interactive because there is no shading, no gray, and no color—only bold editable vector outlines waiting to be colored in.

## SVG primitives needed
- 1× `<rect>` for the pure white slide background
- 2× `<rect>` for the heavy outer coloring-page frame and inner inset frame
- 4× `<rect>` for outlined mini chart bars / data blocks
- 4× `<text>` for stacked outlined headline typography and a small caption, each with explicit `width`
- 14× `<path>` for hand-drawn doodles: clouds, hearts, stars, crescent moon, sparkles, rainbow arcs, swirls, and organic filler icons
- 7× `<circle>` for sun center, dots, flower centers, and small fill-space bubbles
- 8× `<ellipse>` for flower petals and rounded organic filler details
- 12× `<line>` for sun rays, sparkle rays, chart axis marks, and simple decorative strokes
- No gradients, shadows, photos, or transparency; the power of the style comes from strict binary line art

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs></defs>

  <!-- White printable page -->
  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- Coloring page frame -->
  <rect x="34" y="34" width="1212" height="652" rx="22" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <rect x="58" y="58" width="1164" height="604" rx="16" fill="none" stroke="#000000" stroke-width="3" stroke-dasharray="14 12"/>

  <!-- Corner cloud -->
  <path d="M112 137 C90 138 74 123 74 102 C74 83 89 68 108 68 C117 48 138 39 158 46 C172 25 204 24 221 47 C246 47 267 67 267 93 C267 120 247 139 219 139 Z"
        fill="#ffffff" stroke="#000000" stroke-width="6" stroke-linejoin="round"/>
  <circle cx="117" cy="101" r="9" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <circle cx="211" cy="95" r="8" fill="#ffffff" stroke="#000000" stroke-width="5"/>

  <!-- Top right heart -->
  <path d="M1082 91 C1082 60 1119 50 1138 78 C1157 50 1194 60 1194 91 C1194 131 1138 164 1138 164 C1138 164 1082 131 1082 91 Z"
        fill="#ffffff" stroke="#000000" stroke-width="7" stroke-linejoin="round"/>
  <path d="M1120 91 C1129 102 1140 104 1155 91" fill="none" stroke="#000000" stroke-width="4" stroke-linecap="round"/>

  <!-- Sun doodle -->
  <circle cx="170" cy="582" r="55" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <line x1="170" y1="493" x2="170" y2="466" stroke="#000000" stroke-width="6" stroke-linecap="round"/>
  <line x1="170" y1="698" x2="170" y2="672" stroke="#000000" stroke-width="6" stroke-linecap="round"/>
  <line x1="81" y1="582" x2="55" y2="582" stroke="#000000" stroke-width="6" stroke-linecap="round"/>
  <line x1="285" y1="582" x2="258" y2="582" stroke="#000000" stroke-width="6" stroke-linecap="round"/>
  <line x1="107" y1="519" x2="88" y2="500" stroke="#000000" stroke-width="6" stroke-linecap="round"/>
  <line x1="233" y1="645" x2="252" y2="664" stroke="#000000" stroke-width="6" stroke-linecap="round"/>

  <!-- Bottom right crescent moon -->
  <path d="M1100 536 C1070 562 1067 609 1095 639 C1120 667 1165 670 1193 647 C1157 650 1127 625 1124 590 C1121 557 1144 529 1176 522 C1150 506 1122 516 1100 536 Z"
        fill="#ffffff" stroke="#000000" stroke-width="7" stroke-linejoin="round"/>

  <!-- Stacked outlined typography -->
  <text x="640" y="235" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="96" font-weight="900"
        fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round">YOU ARE</text>
  <text x="640" y="355" width="940" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="112" font-weight="900"
        fill="#ffffff" stroke="#000000" stroke-width="9" stroke-linejoin="round">PURE</text>
  <text x="640" y="494" width="980" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="118" font-weight="900"
        fill="#ffffff" stroke="#000000" stroke-width="9" stroke-linejoin="round">MAGIC</text>
  <text x="640" y="598" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" letter-spacing="3"
        fill="#ffffff" stroke="#000000" stroke-width="3" stroke-linejoin="round">COLOR THE WINS</text>

  <!-- Outlined mini data chart, treated like a coloring-page object -->
  <line x1="890" y1="196" x2="890" y2="322" stroke="#000000" stroke-width="5" stroke-linecap="round"/>
  <line x1="890" y1="322" x2="1056" y2="322" stroke="#000000" stroke-width="5" stroke-linecap="round"/>
  <rect x="910" y="267" width="28" height="55" rx="8" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <rect x="954" y="235" width="28" height="87" rx="8" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <rect x="998" y="205" width="28" height="117" rx="8" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <path d="M914 250 C947 230 967 247 1001 210 C1017 193 1034 184 1050 176"
        fill="none" stroke="#000000" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="914" cy="250" r="8" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <circle cx="1001" cy="210" r="8" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <circle cx="1050" cy="176" r="8" fill="#ffffff" stroke="#000000" stroke-width="5"/>

  <!-- Four-point stars and sparkles -->
  <path d="M374 102 L390 134 L422 150 L390 166 L374 198 L358 166 L326 150 L358 134 Z"
        fill="#ffffff" stroke="#000000" stroke-width="6" stroke-linejoin="round"/>
  <path d="M1081 410 L1094 436 L1120 449 L1094 462 L1081 488 L1068 462 L1042 449 L1068 436 Z"
        fill="#ffffff" stroke="#000000" stroke-width="6" stroke-linejoin="round"/>
  <path d="M274 402 L286 425 L309 437 L286 449 L274 472 L262 449 L239 437 L262 425 Z"
        fill="#ffffff" stroke="#000000" stroke-width="5" stroke-linejoin="round"/>
  <line x1="438" y1="91" x2="438" y2="61" stroke="#000000" stroke-width="5" stroke-linecap="round"/>
  <line x1="438" y1="171" x2="438" y2="201" stroke="#000000" stroke-width="5" stroke-linecap="round"/>
  <line x1="398" y1="131" x2="368" y2="131" stroke="#000000" stroke-width="5" stroke-linecap="round"/>
  <line x1="478" y1="131" x2="508" y2="131" stroke="#000000" stroke-width="5" stroke-linecap="round"/>

  <!-- Flower cluster -->
  <ellipse cx="1016" cy="570" rx="18" ry="33" fill="#ffffff" stroke="#000000" stroke-width="5" transform="rotate(0 1016 570)"/>
  <ellipse cx="1016" cy="570" rx="18" ry="33" fill="#ffffff" stroke="#000000" stroke-width="5" transform="rotate(60 1016 570)"/>
  <ellipse cx="1016" cy="570" rx="18" ry="33" fill="#ffffff" stroke="#000000" stroke-width="5" transform="rotate(120 1016 570)"/>
  <circle cx="1016" cy="570" r="15" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <path d="M1016 604 C1008 631 993 647 966 654" fill="none" stroke="#000000" stroke-width="5" stroke-linecap="round"/>
  <path d="M992 628 C976 610 950 610 939 631 C959 637 978 638 992 628 Z"
        fill="#ffffff" stroke="#000000" stroke-width="5" stroke-linejoin="round"/>

  <!-- Rainbow arcs as empty coloring bands -->
  <path d="M303 630 C351 560 445 560 493 630" fill="none" stroke="#000000" stroke-width="6" stroke-linecap="round"/>
  <path d="M328 630 C367 585 429 585 468 630" fill="none" stroke="#000000" stroke-width="6" stroke-linecap="round"/>
  <path d="M353 630 C383 607 413 607 443 630" fill="none" stroke="#000000" stroke-width="6" stroke-linecap="round"/>

  <!-- Small filler dots and bubbles -->
  <circle cx="314" cy="273" r="12" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <circle cx="214" cy="289" r="8" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <circle cx="1148" cy="260" r="13" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <circle cx="810" cy="104" r="10" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <ellipse cx="864" cy="596" rx="16" ry="10" fill="#ffffff" stroke="#000000" stroke-width="5" transform="rotate(-20 864 596)"/>

  <!-- Loose hand-drawn swirls -->
  <path d="M140 333 C176 309 210 326 204 357 C198 386 158 382 168 354 C174 337 196 342 193 357"
        fill="none" stroke="#000000" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M1145 343 C1110 326 1084 345 1095 372 C1106 399 1140 385 1129 363"
        fill="none" stroke="#000000" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

## Avoid in this skill
- ❌ Gradients, shadows, blurs, semi-transparent fills, or gray strokes; they break the printable coloring-page illusion
- ❌ Thin hairline strokes; the aesthetic needs bold 4–9 px black outlines that survive projection and printing
- ❌ Photo backgrounds or raster texture overlays; keep everything editable vector line art
- ❌ Overusing perfect geometric grids; the page should feel doodled, playful, and densely hand-filled
- ❌ Applying `clip-path` or masks to vector doodles; use direct editable paths instead

## Composition notes
- Keep the main message centered and oversized, broken into 2–4 short stacked lines with heavy outlined text.
- Fill negative space aggressively with white-filled black-stroked doodles so the slide feels like a complete coloring page, not a sparse poster.
- Use a thick outer frame to create the “printable page” boundary and contain visual clutter.
- Maintain strict rhythm: black stroke, white fill, rounded joins/caps, and no color until the audience or presenter “colors it in.”