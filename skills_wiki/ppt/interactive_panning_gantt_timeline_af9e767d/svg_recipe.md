# SVG Recipe — Interactive Panning Gantt Timeline

## Visual mechanism
A wide Gantt canvas is drawn far beyond the visible slide, then partially hidden beneath a fixed white left-side panel containing row labels. Duplicate the slide and change only the `transform="translate(...)"` on the scrolling timeline group; PowerPoint Morph creates the app-like horizontal panning effect while headers and navigation stay anchored.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 1× large rounded `<rect>` for the white app surface
- 1× `<filter id="cardShadow">` for the floating dashboard container
- 1× `<filter id="barGlow">` for premium soft glow behind task bars
- 1× `<linearGradient>` for the active navigation pill
- 18× `<line>` for visible vertical week grid lines
- 6× `<line>` for left-panel row dividers
- 10× rounded `<rect>` for task bars and nav pills
- 8× small `<path>` arrowheads at the end of dashed task-progress lines
- 8× dashed `<line>` for progress arrows inside task bars
- 34× `<text>` elements with explicit `width` for title, nav, month/week labels, row labels, and task labels
- 1× fixed white `<rect>` mask panel layered above the scrolling grid
- 1× subtle right-edge `<rect>` gradient/fade to imply the timeline continues off-screen

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="activePill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#374151"/>
    </linearGradient>
    <linearGradient id="rightFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.92"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="20"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="barGlow" x="-40%" y="-80%" width="180%" height="260%">
      <feGaussianBlur stdDeviation="11"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F3F6FA"/>
  <rect x="56" y="48" width="1168" height="624" rx="34" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="56" y="48" width="1168" height="624" rx="34" fill="#FFFFFF" stroke="#E5E7EB"/>

  <!-- Scrolling infinite timeline state: change translate(-130 0) to translate(-430 0), etc. on duplicate slides for Morph panning -->
  <g id="panningTimelineCanvas" transform="translate(-130 0)">
    <line x1="390" y1="188" x2="390" y2="626" stroke="#D8DCE3"/>
    <line x1="452" y1="188" x2="452" y2="626" stroke="#D8DCE3"/>
    <line x1="514" y1="188" x2="514" y2="626" stroke="#D8DCE3"/>
    <line x1="576" y1="188" x2="576" y2="626" stroke="#D8DCE3"/>
    <line x1="638" y1="188" x2="638" y2="626" stroke="#D8DCE3"/>
    <line x1="700" y1="188" x2="700" y2="626" stroke="#D8DCE3"/>
    <line x1="762" y1="188" x2="762" y2="626" stroke="#D8DCE3"/>
    <line x1="824" y1="188" x2="824" y2="626" stroke="#D8DCE3"/>
    <line x1="886" y1="188" x2="886" y2="626" stroke="#D8DCE3"/>
    <line x1="948" y1="188" x2="948" y2="626" stroke="#D8DCE3"/>
    <line x1="1010" y1="188" x2="1010" y2="626" stroke="#D8DCE3"/>
    <line x1="1072" y1="188" x2="1072" y2="626" stroke="#D8DCE3"/>
    <line x1="1134" y1="188" x2="1134" y2="626" stroke="#D8DCE3"/>
    <line x1="1196" y1="188" x2="1196" y2="626" stroke="#D8DCE3"/>
    <line x1="1258" y1="188" x2="1258" y2="626" stroke="#D8DCE3"/>
    <line x1="1320" y1="188" x2="1320" y2="626" stroke="#D8DCE3"/>
    <line x1="1382" y1="188" x2="1382" y2="626" stroke="#D8DCE3"/>
    <line x1="1444" y1="188" x2="1444" y2="626" stroke="#D8DCE3"/>

    <text x="420" y="160" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#111827">JANUARY</text>
    <text x="665" y="160" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#111827">FEBRUARY</text>
    <text x="980" y="160" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#111827">MARCH</text>

    <text x="370" y="205" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 1</text>
    <text x="432" y="205" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 2</text>
    <text x="494" y="205" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 3</text>
    <text x="556" y="205" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 4</text>
    <text x="618" y="205" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 5</text>
    <text x="680" y="205" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 6</text>
    <text x="742" y="205" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 7</text>
    <text x="804" y="205" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 8</text>
    <text x="866" y="205" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 9</text>
    <text x="928" y="205" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 10</text>
    <text x="990" y="205" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 11</text>
    <text x="1052" y="205" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 12</text>
    <text x="1114" y="205" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 13</text>
    <text x="1176" y="205" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 14</text>
    <text x="1238" y="205" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Week 15</text>

    <rect x="390" y="250" width="310" height="40" rx="20" fill="#85F5B9" opacity="0.78" filter="url(#barGlow)" stroke="#22C55E"/>
    <text x="410" y="276" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#064E3B">W1 / Kick-off</text>
    <line x1="528" y1="270" x2="660" y2="248" stroke="#065F46" stroke-width="1.4" stroke-dasharray="5 4"/>
    <path d="M660 248 L650 243 L652 254 Z" fill="#065F46"/>

    <rect x="515" y="302" width="300" height="40" rx="20" fill="#FFC8A8" opacity="0.82" filter="url(#barGlow)" stroke="#F97316"/>
    <text x="535" y="328" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#7C2D12">W3 / Task name</text>
    <line x1="665" y1="322" x2="785" y2="302" stroke="#7C2D12" stroke-width="1.4" stroke-dasharray="5 4"/>
    <path d="M785 302 L775 297 L777 308 Z" fill="#7C2D12"/>

    <rect x="640" y="354" width="285" height="40" rx="20" fill="#FEF56D" opacity="0.82" filter="url(#barGlow)" stroke="#D6C900"/>
    <text x="660" y="380" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#6B5E00">W6 / Task name</text>
    <line x1="795" y1="374" x2="895" y2="355" stroke="#6B5E00" stroke-width="1.4" stroke-dasharray="5 4"/>
    <path d="M895 355 L885 350 L887 361 Z" fill="#6B5E00"/>

    <rect x="765" y="405" width="350" height="40" rx="20" fill="#8DE9F7" opacity="0.8" filter="url(#barGlow)" stroke="#06B6D4"/>
    <text x="785" y="431" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#155E75">W8 / Task name</text>
    <line x1="940" y1="425" x2="1080" y2="405" stroke="#155E75" stroke-width="1.4" stroke-dasharray="5 4"/>
    <path d="M1080 405 L1070 400 L1072 411 Z" fill="#155E75"/>

    <rect x="535" y="458" width="330" height="40" rx="20" fill="#F394FF" opacity="0.78" filter="url(#barGlow)" stroke="#D946EF"/>
    <text x="555" y="484" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#86198F">W4 / Task name</text>
    <line x1="710" y1="478" x2="830" y2="458" stroke="#86198F" stroke-width="1.4" stroke-dasharray="5 4"/>
    <path d="M830 458 L820 453 L822 464 Z" fill="#86198F"/>

    <rect x="820" y="490" width="370" height="40" rx="20" fill="#B978FF" opacity="0.78" filter="url(#barGlow)" stroke="#9333EA"/>
    <text x="840" y="516" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#581C87">W9 / Task name</text>
    <line x1="1010" y1="510" x2="1155" y2="490" stroke="#581C87" stroke-width="1.4" stroke-dasharray="5 4"/>
    <path d="M1155 490 L1145 485 L1147 496 Z" fill="#581C87"/>

    <rect x="930" y="538" width="300" height="40" rx="20" fill="#FF8D8D" opacity="0.82" filter="url(#barGlow)" stroke="#EF4444"/>
    <text x="950" y="564" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#7F1D1D">W11 / Task name</text>
    <line x1="1105" y1="558" x2="1205" y2="540" stroke="#7F1D1D" stroke-width="1.4" stroke-dasharray="5 4"/>
    <path d="M1205 540 L1195 535 L1197 546 Z" fill="#7F1D1D"/>

    <rect x="690" y="586" width="440" height="40" rx="20" fill="#8CFF84" opacity="0.82" filter="url(#barGlow)" stroke="#22C55E"/>
    <text x="710" y="612" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#14532D">W7 / Task name</text>
    <line x1="890" y1="606" x2="1050" y2="585" stroke="#14532D" stroke-width="1.4" stroke-dasharray="5 4"/>
    <path d="M1050 585 L1040 580 L1042 591 Z" fill="#14532D"/>
  </g>

  <!-- Static white mask panel: covers the moving grid and bars on the left -->
  <rect x="56" y="48" width="312" height="624" rx="34" fill="#FFFFFF"/>
  <rect x="345" y="172" width="1" height="454" fill="#111827" opacity="0.45"/>

  <text x="82" y="105" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#111827">2026</text>
  <rect x="158" y="78" width="48" height="32" rx="16" fill="#FFFFFF" stroke="#9CA3AF"/>
  <text x="170" y="101" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111827">Q1</text>
  <rect x="212" y="74" width="48" height="32" rx="16" fill="url(#activePill)"/>
  <text x="224" y="97" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Q2</text>
  <rect x="266" y="70" width="48" height="32" rx="16" fill="#FFFFFF" stroke="#9CA3AF"/>
  <text x="278" y="93" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111827">Q3</text>

  <text x="82" y="154" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#030712">PROJECT</text>
  <text x="82" y="190" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#030712">TIMELINE</text>

  <line x1="88" y1="292" x2="334" y2="292" stroke="#D1D5DB"/>
  <line x1="88" y1="344" x2="334" y2="344" stroke="#D1D5DB"/>
  <line x1="88" y1="396" x2="334" y2="396" stroke="#D1D5DB"/>
  <line x1="88" y1="448" x2="334" y2="448" stroke="#D1D5DB"/>
  <line x1="88" y1="500" x2="334" y2="500" stroke="#D1D5DB"/>
  <line x1="88" y1="552" x2="334" y2="552" stroke="#D1D5DB"/>
  <text x="92" y="272" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#111827">1. Project Kick-off & Goals</text>
  <text x="92" y="324" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#111827">2. Research & Discovery</text>
  <text x="92" y="376" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#111827">3. Scope & Planning</text>
  <text x="92" y="428" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#111827">4. Design Concepts</text>
  <text x="92" y="480" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#111827">5. Production & Build</text>
  <text x="92" y="532" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#111827">6. Final Revisions</text>

  <rect x="1120" y="48" width="104" height="624" fill="url(#rightFade)"/>
  <text x="566" y="82" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#6B7280">PANNING VIEW</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or `mask="url(#...)"`; use a solid white overlay panel to hide the moving timeline instead.
- ❌ Do not apply `clip-path` to timeline bars, grid lines, or groups; PowerPoint translation only preserves image clipping reliably.
- ❌ Do not use `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` to fake perspective; those transforms are dropped.
- ❌ Do not put `marker-end` on `<path>` elements for task arrows; use dashed `<line>` plus small editable `<path>` triangle arrowheads.
- ❌ Do not filter `<line>` elements; use filters on rounded rectangles for task-bar glow/shadow instead.

## Composition notes
- Keep the fixed left mask panel at roughly 24–28% of slide width; it anchors the viewer while the wide Gantt canvas pans underneath.
- The scrolling group should extend far beyond the right edge, with month labels, week lines, and task bars all inside the same translated group.
- Use soft pastel bars with darker dashed progress arrows so dense roadmap information remains legible.
- Add a slight right-edge fade to imply more content outside the viewport and reinforce the “interactive app” illusion.