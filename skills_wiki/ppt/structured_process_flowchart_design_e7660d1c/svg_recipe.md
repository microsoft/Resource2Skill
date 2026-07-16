# SVG Recipe — Structured Process Flowchart Design

## Visual mechanism
A clean, grid-aligned flowchart built from standardized node archetypes — rounded terminators, a decision diamond, process rectangles, and a data/output parallelogram — connected by precise orthogonal elbow arrows. Strong semantic color-coding and subtle drop shadows make the logic readable while giving the diagram a polished PowerPoint keynote feel.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft background
- 1× `<rect>` for a large white rounded diagram canvas/card
- 2× `<rect rx>` for Start/End terminator nodes
- 3× `<rect rx>` for green process nodes
- 1× `<path>` for the red decision diamond
- 1× `<path>` for the orange data/output parallelogram
- 13× `<line>` for orthogonal elbow connector segments
- 5× `<path>` for editable triangular arrowheads
- 1× `<filter id="softShadow">` applied to node/card shapes
- 6× `<linearGradient>` fills for premium background and node color depth
- Multiple `<text>` elements with explicit `width` for title, node labels, branch labels, and legend text
- 4× small legend shapes showing the meaning of each flowchart archetype

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFF"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5D9BFF"/>
      <stop offset="100%" stop-color="#2F72D9"/>
    </linearGradient>
    <linearGradient id="redGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF6B61"/>
      <stop offset="100%" stop-color="#D93025"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#62D77A"/>
      <stop offset="100%" stop-color="#2EA44F"/>
    </linearGradient>
    <linearGradient id="orangeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFD85A"/>
      <stop offset="100%" stop-color="#F4A600"/>
    </linearGradient>
    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF3D00"/>
      <stop offset="100%" stop-color="#FF8A00"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="1110" cy="160" r="130" fill="#FFE3B0" opacity="0.35"/>
  <circle cx="135" cy="590" r="180" fill="#D7E8FF" opacity="0.45"/>

  <text x="82" y="78" width="1120" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#211000" letter-spacing="1.5">STRUCTURED PROCESS FLOWCHART</text>
  <text x="82" y="126" width="1120" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="url(#titleGrad)" letter-spacing="1">GRID-ALIGNED LOGIC MAP WITH ORTHOGONAL CONNECTORS</text>

  <rect x="70" y="165" width="1140" height="485" rx="34" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="94" y="189" width="1092" height="437" rx="24" fill="#FBFCFE" stroke="#E5EAF1" stroke-width="2"/>

  <text x="112" y="232" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#1B2430">Customer onboarding workflow</text>
  <text x="112" y="262" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#647084">Use shape type and color to communicate action, decision, data, and completion at a glance.</text>

  <!-- main flowchart connectors: draw lines behind nodes -->
  <line x1="270" y1="400" x2="312" y2="400" stroke="#9AA2AD" stroke-width="3"/>
  <path d="M312 400 L300 393 L300 407 Z" fill="#9AA2AD"/>

  <line x1="470" y1="400" x2="514" y2="400" stroke="#9AA2AD" stroke-width="3"/>
  <line x1="514" y1="400" x2="514" y2="304" stroke="#9AA2AD" stroke-width="3"/>
  <line x1="514" y1="304" x2="560" y2="304" stroke="#9AA2AD" stroke-width="3"/>
  <path d="M560 304 L548 297 L548 311 Z" fill="#9AA2AD"/>

  <line x1="470" y1="400" x2="560" y2="400" stroke="#9AA2AD" stroke-width="3"/>
  <path d="M560 400 L548 393 L548 407 Z" fill="#9AA2AD"/>

  <line x1="470" y1="400" x2="514" y2="400" stroke="#9AA2AD" stroke-width="3"/>
  <line x1="514" y1="400" x2="514" y2="496" stroke="#9AA2AD" stroke-width="3"/>
  <line x1="514" y1="496" x2="560" y2="496" stroke="#9AA2AD" stroke-width="3"/>
  <path d="M560 496 L548 489 L548 503 Z" fill="#9AA2AD"/>

  <line x1="730" y1="304" x2="765" y2="304" stroke="#9AA2AD" stroke-width="3"/>
  <line x1="730" y1="400" x2="765" y2="400" stroke="#9AA2AD" stroke-width="3"/>
  <line x1="730" y1="496" x2="765" y2="496" stroke="#9AA2AD" stroke-width="3"/>
  <line x1="765" y1="304" x2="765" y2="496" stroke="#9AA2AD" stroke-width="3"/>
  <line x1="765" y1="400" x2="810" y2="400" stroke="#9AA2AD" stroke-width="3"/>
  <path d="M810 400 L798 393 L798 407 Z" fill="#9AA2AD"/>

  <line x1="990" y1="400" x2="1060" y2="400" stroke="#9AA2AD" stroke-width="3"/>
  <path d="M1060 400 L1048 393 L1048 407 Z" fill="#9AA2AD"/>

  <!-- nodes -->
  <rect x="120" y="368" width="150" height="64" rx="32" fill="url(#blueGrad)" filter="url(#softShadow)"/>
  <text x="120" y="406" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF">START</text>

  <path d="M390 330 L470 400 L390 470 L310 400 Z" fill="url(#redGrad)" filter="url(#softShadow)"/>
  <text x="330" y="395" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">DECISION</text>
  <text x="330" y="415" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" fill="#FFE5E2">eligible?</text>

  <rect x="560" y="275" width="170" height="58" rx="8" fill="url(#greenGrad)" filter="url(#softShadow)"/>
  <text x="560" y="309" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">PROCESS 1</text>
  <text x="560" y="326" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#E9FFF0">validate profile</text>

  <rect x="560" y="371" width="170" height="58" rx="8" fill="url(#greenGrad)" filter="url(#softShadow)"/>
  <text x="560" y="405" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">PROCESS 2</text>
  <text x="560" y="422" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#E9FFF0">approve access</text>

  <rect x="560" y="467" width="170" height="58" rx="8" fill="url(#greenGrad)" filter="url(#softShadow)"/>
  <text x="560" y="501" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">PROCESS 3</text>
  <text x="560" y="518" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#E9FFF0">request review</text>

  <path d="M825 368 L990 368 L975 432 L810 432 Z" fill="url(#orangeGrad)" filter="url(#softShadow)"/>
  <text x="810" y="405" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">OUTPUT</text>
  <text x="810" y="422" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFF8D7">welcome pack</text>

  <rect x="1060" y="368" width="140" height="64" rx="32" fill="url(#blueGrad)" filter="url(#softShadow)"/>
  <text x="1060" y="406" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF">END</text>

  <!-- branch labels -->
  <text x="492" y="292" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#6B7280">YES</text>
  <text x="492" y="530" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#6B7280">NO</text>

  <!-- compact legend -->
  <rect x="142" y="570" width="18" height="18" rx="9" fill="url(#blueGrad)"/>
  <text x="168" y="584" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#596273">Start / End</text>
  <path d="M325 561 L342 579 L325 597 L308 579 Z" fill="url(#redGrad)"/>
  <text x="352" y="584" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#596273">Decision</text>
  <rect x="493" y="570" width="25" height="18" rx="4" fill="url(#greenGrad)"/>
  <text x="526" y="584" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#596273">Process</text>
  <path d="M660 570 L690 570 L684 588 L654 588 Z" fill="url(#orangeGrad)"/>
  <text x="702" y="584" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#596273">Data / Output</text>
</svg>
```

## Avoid in this skill
- ❌ Using freehand or diagonal connector paths for the core logic; this technique depends on orthogonal, grid-disciplined elbow routing.
- ❌ Applying `marker-end` to `<path>` connectors; use editable `<line>` segments plus small triangular `<path>` arrowheads instead.
- ❌ Letting node widths vary randomly; inconsistent node sizing breaks the structured process-map feel.
- ❌ Using clip paths or masks on non-image shapes; keep flowchart nodes as direct editable `<rect>` and `<path>` primitives.
- ❌ Overloading the diagram with long sentences inside nodes; use short verbs/nouns and place detail in presenter notes or side annotations.

## Composition notes
- Keep the main flow on a single horizontal spine, with decision branches expanding vertically and reconverging before the output node.
- Reserve generous white space around the diagram; the card should feel like a clean workspace, not a crowded technical schematic.
- Use color semantically and consistently: blue for start/end, red for decisions, green for processes, orange for outputs.
- Put connectors behind nodes, use medium-gray strokes, and apply shadows only to nodes/card shapes so the logic remains crisp.