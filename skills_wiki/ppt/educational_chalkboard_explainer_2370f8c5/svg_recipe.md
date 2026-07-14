# SVG Recipe — Educational Chalkboard Explainer

## Visual mechanism
A matte dark-green board becomes the full-slide canvas, with white chalk-like typography, hand-drawn strokes, and a golden-yellow section callout. The look is built from slightly imperfect lines, semi-transparent duplicate strokes, simple node diagrams, and generous negative space to make technical material feel like a live classroom explanation.

## SVG primitives needed
- 1× `<rect>` for the full-slide chalkboard background
- 1× `<linearGradient>` for a subtle board vignette
- 1× `<filter id="chalkGlow">` for soft chalk bloom on major text and line-art paths
- 1× `<filter id="softDust">` for blurred chalk dust accents
- 20+× small `<circle>` elements for chalk specks and erased-board texture
- 6× `<text>` blocks for title, subtitle, diagram labels, formula notes, and bottom section title
- 10× `<line>` elements for network topology connections and small sketch ticks
- 8× `<circle>` elements for hand-drawn topology nodes
- 10+× `<path>` elements for chalk underlines, cloud/router sketch, globe/network icon, freehand braces, and accent strokes
- 2× `<rect>` elements for chalk stick and small label tab details

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="boardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1d4641"/>
      <stop offset="55%" stop-color="#173431"/>
      <stop offset="100%" stop-color="#102825"/>
    </linearGradient>
    <filter id="chalkGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.15" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softDust" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.2"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#boardGrad)"/>

  <!-- faint erased chalk texture -->
  <circle cx="92" cy="88" r="2.2" fill="#ffffff" opacity="0.14" filter="url(#softDust)"/>
  <circle cx="204" cy="610" r="3.5" fill="#ffffff" opacity="0.10" filter="url(#softDust)"/>
  <circle cx="352" cy="112" r="2.8" fill="#ffffff" opacity="0.09" filter="url(#softDust)"/>
  <circle cx="518" cy="642" r="2.5" fill="#ffffff" opacity="0.13" filter="url(#softDust)"/>
  <circle cx="740" cy="76" r="3.2" fill="#ffffff" opacity="0.08" filter="url(#softDust)"/>
  <circle cx="924" cy="594" r="2.7" fill="#ffffff" opacity="0.12" filter="url(#softDust)"/>
  <circle cx="1138" cy="126" r="3.7" fill="#ffffff" opacity="0.09" filter="url(#softDust)"/>
  <circle cx="1194" cy="676" r="2.4" fill="#ffffff" opacity="0.12" filter="url(#softDust)"/>
  <path d="M72 205 C190 180,260 220,376 196" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.05"/>
  <path d="M845 282 C970 248,1088 292,1202 258" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.05"/>
  <path d="M122 510 C280 472,420 526,574 488" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.04"/>

  <!-- corner chalkboard icon -->
  <path d="M78 74 C108 42,164 42,194 74 C164 106,108 106,78 74Z" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.82" filter="url(#chalkGlow)"/>
  <path d="M95 74 H177 M136 48 C120 68,120 84,136 101 M136 48 C152 68,152 84,136 101" fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.75"/>
  <circle cx="136" cy="74" r="5" fill="#ffbf00" opacity="0.95"/>

  <!-- title block -->
  <text x="640" y="126" width="1060" text-anchor="middle"
        font-family="Segoe Print, Comic Sans MS, Segoe UI, Microsoft YaHei" font-size="70"
        font-weight="700" fill="#ffffff" filter="url(#chalkGlow)">COMPUTER NETWORKS</text>
  <path d="M735 154 C820 143,903 160,986 150 C1034 145,1082 150,1126 158"
        fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" opacity="0.88"/>
  <path d="M740 164 C828 155,920 170,1000 159 C1052 153,1092 160,1120 166"
        fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" opacity="0.55"/>

  <text x="640" y="202" width="880" text-anchor="middle"
        font-family="Segoe Print, Comic Sans MS, Segoe UI, Microsoft YaHei" font-size="34"
        fill="#ffffff" opacity="0.92">A bottom-up approach to how packets move</text>

  <!-- central chalk topology diagram -->
  <text x="640" y="276" width="760" text-anchor="middle"
        font-family="Segoe Print, Comic Sans MS, Segoe UI, Microsoft YaHei" font-size="30"
        font-weight="700" fill="#ffbf00">Network Topology — Part 1</text>

  <line x1="420" y1="405" x2="550" y2="345" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity="0.82" stroke-dasharray="10 8"/>
  <line x1="550" y1="345" x2="690" y2="405" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity="0.82" stroke-dasharray="10 8"/>
  <line x1="690" y1="405" x2="835" y2="346" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity="0.82" stroke-dasharray="10 8"/>
  <line x1="550" y1="345" x2="620" y2="492" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity="0.72"/>
  <line x1="690" y1="405" x2="620" y2="492" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity="0.72"/>
  <line x1="420" y1="405" x2="620" y2="492" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.48"/>
  <line x1="835" y1="346" x2="620" y2="492" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.48"/>

  <circle cx="420" cy="405" r="34" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.88" filter="url(#chalkGlow)"/>
  <circle cx="550" cy="345" r="34" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.88" filter="url(#chalkGlow)"/>
  <circle cx="690" cy="405" r="34" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.88" filter="url(#chalkGlow)"/>
  <circle cx="835" cy="346" r="34" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.88" filter="url(#chalkGlow)"/>
  <circle cx="620" cy="492" r="40" fill="none" stroke="#ffbf00" stroke-width="6" opacity="0.96" filter="url(#chalkGlow)"/>

  <text x="420" y="415" width="90" text-anchor="middle" font-family="Segoe Print, Comic Sans MS, Segoe UI" font-size="24" fill="#ffffff">PC</text>
  <text x="550" y="355" width="100" text-anchor="middle" font-family="Segoe Print, Comic Sans MS, Segoe UI" font-size="23" fill="#ffffff">SW</text>
  <text x="690" y="415" width="100" text-anchor="middle" font-family="Segoe Print, Comic Sans MS, Segoe UI" font-size="23" fill="#ffffff">AP</text>
  <text x="835" y="356" width="120" text-anchor="middle" font-family="Segoe Print, Comic Sans MS, Segoe UI" font-size="23" fill="#ffffff">DB</text>
  <text x="620" y="503" width="130" text-anchor="middle" font-family="Segoe Print, Comic Sans MS, Segoe UI" font-size="24" font-weight="700" fill="#ffbf00">RTR</text>

  <!-- side explanation notes -->
  <path d="M210 318 C238 302,270 300,302 315 C288 342,245 355,214 336 Z" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.78"/>
  <path d="M236 330 C258 319,274 322,292 334" fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.65"/>
  <text x="178" y="384" width="260" font-family="Segoe Print, Comic Sans MS, Segoe UI, Microsoft YaHei" font-size="25" fill="#ffffff">
    <tspan x="178" dy="0">nodes = devices</tspan>
    <tspan x="178" dy="36">edges = links</tspan>
  </text>

  <path d="M942 314 C982 287,1056 291,1094 328 C1132 326,1156 350,1152 382 C1160 418,1124 438,1086 428 C1058 452,992 446,972 420 C930 421,908 394,918 362 C908 340,920 323,942 314Z"
        fill="none" stroke="#ffffff" stroke-width="4" opacity="0.78" filter="url(#chalkGlow)"/>
  <text x="944" y="486" width="260" font-family="Segoe Print, Comic Sans MS, Segoe UI, Microsoft YaHei" font-size="25" fill="#ffffff">
    <tspan x="944" dy="0">packet path:</tspan>
    <tspan x="944" dy="35" fill="#ffbf00">source → router → service</tspan>
  </text>

  <!-- chalk tray -->
  <line x1="120" y1="648" x2="1160" y2="648" stroke="#ffffff" stroke-width="3" opacity="0.32"/>
  <rect x="922" y="632" width="128" height="13" rx="6" fill="#ffffff" opacity="0.86"/>
  <rect x="1062" y="632" width="92" height="13" rx="6" fill="#ffbf00" opacity="0.94"/>
  <text x="640" y="626" width="980" text-anchor="middle"
        font-family="Segoe Print, Comic Sans MS, Segoe UI, Microsoft YaHei" font-size="36"
        font-weight="700" fill="#ffbf00" filter="url(#chalkGlow)">Sketch the system first. Optimize it second.</text>
</svg>
```

## Avoid in this skill
- ❌ Perfectly crisp geometric grids; the chalkboard style needs slight irregularity, duplicate strokes, and organic linework.
- ❌ Applying filters to `<line>` elements; use filters only on text, paths, circles, ellipses, or rects.
- ❌ Tiny dense data tables; chalkboard explainers work best for simplified concepts, not spreadsheet-like precision.
- ❌ Photo-heavy layouts; images can break the academic board metaphor unless they are intentionally clipped as reference cards.
- ❌ Relying on unsupported chalk fonts only; specify handwritten fallbacks such as Segoe Print, Comic Sans MS, then Segoe UI.

## Composition notes
- Keep the main title centered in the top third, with a loose chalk underline offset to one side for hand-drawn emphasis.
- Reserve the middle of the slide for one clear diagram: topology, flow, formula, architecture sketch, or cause-effect chain.
- Use white for primary teaching marks and golden yellow only for the lesson title, key node, or takeaway sentence.
- Leave generous dark-green negative space around elements so the board feels intentional rather than cluttered.