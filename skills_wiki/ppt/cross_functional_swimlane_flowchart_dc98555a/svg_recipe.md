# SVG Recipe — Cross-Functional Swimlane Flowchart

## Visual mechanism
A swimlane flowchart maps a process across horizontal responsibility tracks, using lane labels on the left and a border-light workflow canvas on the right. Floating process nodes, decision diamonds, database symbols, and elbow/curved connectors create a readable hand-off story without looking like a rigid table.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<linearGradient>` for warm process-node fills
- 1× `<filter id="softShadow">` for subtle node elevation
- 6× `<line>` for swimlane dividers and the left label divider
- 10× `<rect>` for rounded process/terminator nodes and small connector labels
- 3× `<path>` for decision diamonds
- 1× `<ellipse>` plus 2× `<path>` for the database/system cylinder
- Multiple `<line>` segments for orthogonal connectors
- Multiple small filled `<path>` triangles for arrowheads instead of marker arrows
- 3× curved `<path>` connectors for branch routing between lanes
- 1× simplified PowerPoint-style icon built from `<path>`, `<rect>`, `<circle>`, and `<line>`
- Multiple `<text>` elements with explicit `width` for lane labels, node labels, title, and branch labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="goldNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFC400"/>
      <stop offset="100%" stop-color="#F5A900"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="3" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FBFCFE"/>

  <text x="235" y="112" width="560" font-family="Segoe UI" font-size="78" font-weight="800" font-style="italic" fill="#30364F">Swimlane</text>

  <!-- simplified PowerPoint emblem -->
  <path d="M998 35 L1138 10 L1138 250 L998 226 Z" fill="#D3482E"/>
  <rect x="1138" y="39" width="104" height="178" rx="4" fill="none" stroke="#D3482E" stroke-width="6"/>
  <text x="1041" y="170" width="80" font-family="Segoe UI" font-size="84" font-weight="800" fill="#FFFFFF">P</text>
  <circle cx="1178" cy="103" r="36" fill="#D3482E"/>
  <path d="M1178 67 L1178 103 L1213 103 A36 36 0 0 0 1178 67 Z" fill="#FFFFFF"/>
  <line x1="1138" y1="156" x2="1216" y2="156" stroke="#D3482E" stroke-width="8"/>
  <line x1="1138" y1="186" x2="1216" y2="186" stroke="#D3482E" stroke-width="8"/>

  <!-- swimlane frame -->
  <line x1="230" y1="165" x2="230" y2="660" stroke="#2B75A8" stroke-width="3"/>
  <line x1="30" y1="285" x2="1278" y2="285" stroke="#2B75A8" stroke-width="2.5"/>
  <line x1="30" y1="410" x2="1278" y2="410" stroke="#2B75A8" stroke-width="2.5"/>
  <line x1="30" y1="535" x2="1278" y2="535" stroke="#2B75A8" stroke-width="2.5"/>
  <line x1="30" y1="660" x2="1278" y2="660" stroke="#2B75A8" stroke-width="2.5"/>

  <text x="54" y="248" width="150" font-family="Segoe UI" font-size="31" fill="#111111">Customer</text>
  <text x="80" y="372" width="120" font-family="Segoe UI" font-size="34" fill="#111111">Area 1</text>
  <text x="80" y="497" width="120" font-family="Segoe UI" font-size="34" fill="#111111">Area 2</text>
  <text x="80" y="622" width="120" font-family="Segoe UI" font-size="34" fill="#111111">Area 3</text>

  <!-- connectors behind nodes -->
  <g stroke="#8B8B8B" stroke-width="3" fill="none">
    <line x1="382" y1="225" x2="430" y2="225"/>
    <line x1="570" y1="225" x2="616" y2="225"/>
    <line x1="392" y1="225" x2="392" y2="350"/>
    <line x1="392" y1="350" x2="425" y2="350"/>
    <line x1="505" y1="280" x2="505" y2="302"/>
    <line x1="565" y1="350" x2="586" y2="350"/>
    <line x1="736" y1="225" x2="748" y2="225"/>
    <line x1="748" y1="225" x2="748" y2="350"/>
    <line x1="748" y1="350" x2="766" y2="350"/>
    <line x1="650" y1="386" x2="650" y2="485"/>
    <line x1="650" y1="485" x2="755" y2="485"/>
    <line x1="712" y1="610" x2="766" y2="610"/>
    <line x1="1160" y1="350" x2="1280" y2="347"/>
    <line x1="1160" y1="485" x2="1280" y2="485"/>
    <path d="M495 398 C500 470 520 575 584 610"/>
    <path d="M895 485 C980 475 962 365 1030 350"/>
    <path d="M895 610 C980 610 944 500 1030 485"/>
  </g>

  <!-- arrowheads -->
  <g fill="#8B8B8B">
    <path d="M430 225 L416 216 L416 234 Z"/>
    <path d="M616 225 L602 216 L602 234 Z"/>
    <path d="M425 350 L411 341 L411 359 Z"/>
    <path d="M505 302 L496 288 L514 288 Z"/>
    <path d="M586 350 L572 341 L572 359 Z"/>
    <path d="M766 350 L752 341 L752 359 Z"/>
    <path d="M755 485 L741 476 L741 494 Z"/>
    <path d="M766 610 L752 601 L752 619 Z"/>
    <path d="M584 610 L566 600 L574 621 Z"/>
    <path d="M1030 350 L1014 344 L1020 363 Z"/>
    <path d="M1030 485 L1014 476 L1014 494 Z"/>
  </g>

  <!-- process nodes -->
  <rect x="258" y="191" width="124" height="68" rx="34" fill="url(#goldNode)" filter="url(#softShadow)"/>
  <text x="296" y="248" width="54" font-family="Segoe UI" font-size="16" font-weight="700" fill="#FFFFFF">Start</text>

  <rect x="432" y="178" width="138" height="90" rx="8" fill="url(#goldNode)" filter="url(#softShadow)"/>
  <text x="470" y="248" width="70" font-family="Segoe UI" font-size="16" font-weight="700" fill="#FFFFFF">Step 1</text>

  <ellipse cx="680" cy="199" rx="56" ry="20" fill="#F7FBFF" stroke="#557A9B" stroke-width="2"/>
  <path d="M624 199 L624 265 C624 292 736 292 736 265 L736 199" fill="#F7FBFF" stroke="#557A9B" stroke-width="2"/>
  <path d="M624 265 C624 292 736 292 736 265" fill="none" stroke="#557A9B" stroke-width="2"/>
  <text x="634" y="244" width="92" font-family="Segoe UI" font-size="14" fill="#404854">Database or</text>
  <text x="646" y="262" width="70" font-family="Segoe UI" font-size="14" fill="#404854">System</text>

  <path d="M495 302 L565 350 L495 398 L425 350 Z" fill="#FFFFFF" stroke="#79B56E" stroke-width="3" filter="url(#softShadow)"/>
  <text x="455" y="370" width="80" font-family="Segoe UI" font-size="14" font-weight="700" fill="#555555">Decision</text>
  <text x="464" y="389" width="62" font-family="Segoe UI" font-size="14" font-weight="700" fill="#555555">Point</text>

  <rect x="586" y="316" width="128" height="68" rx="8" fill="url(#goldNode)" filter="url(#softShadow)"/>
  <text x="628" y="356" width="54" font-family="Segoe UI" font-size="16" font-weight="700" fill="#FFFFFF">Step 3</text>

  <rect x="766" y="307" width="128" height="86" rx="8" fill="url(#goldNode)" filter="url(#softShadow)"/>
  <text x="809" y="356" width="52" font-family="Segoe UI" font-size="16" font-weight="700" fill="#FFFFFF">Step 2</text>

  <path d="M825 442 L895 485 L825 528 L755 485 Z" fill="#FFFFFF" stroke="#79B56E" stroke-width="3" filter="url(#softShadow)"/>
  <text x="787" y="501" width="78" font-family="Segoe UI" font-size="14" font-weight="700" fill="#555555">Decision</text>
  <text x="797" y="520" width="58" font-family="Segoe UI" font-size="14" font-weight="700" fill="#555555">Point</text>

  <rect x="1030" y="316" width="130" height="68" rx="8" fill="url(#goldNode)" filter="url(#softShadow)"/>
  <text x="1072" y="356" width="56" font-family="Segoe UI" font-size="16" font-weight="700" fill="#FFFFFF">Step 4</text>

  <rect x="1030" y="451" width="130" height="68" rx="8" fill="url(#goldNode)" filter="url(#softShadow)"/>
  <text x="1072" y="491" width="56" font-family="Segoe UI" font-size="16" font-weight="700" fill="#FFFFFF">Step 4</text>

  <rect x="584" y="576" width="128" height="68" rx="8" fill="url(#goldNode)" filter="url(#softShadow)"/>
  <text x="626" y="616" width="54" font-family="Segoe UI" font-size="16" font-weight="700" fill="#FFFFFF">Step 2</text>

  <rect x="766" y="576" width="128" height="68" rx="8" fill="url(#goldNode)" filter="url(#softShadow)"/>
  <text x="808" y="616" width="54" font-family="Segoe UI" font-size="16" font-weight="700" fill="#FFFFFF">Step 3</text>

  <!-- branch labels -->
  <rect x="546" y="285" width="56" height="30" fill="#FFFFFF" stroke="#B6B6B6" stroke-width="2"/>
  <text x="562" y="306" width="30" font-family="Segoe UI" font-size="15" fill="#555555">Yes</text>
  <rect x="454" y="477" width="56" height="30" fill="#FFFFFF" stroke="#B6B6B6" stroke-width="2"/>
  <text x="472" y="499" width="24" font-family="Segoe UI" font-size="15" fill="#555555">No</text>
  <rect x="934" y="408" width="92" height="30" fill="#FFFFFF" stroke="#B6B6B6" stroke-width="2"/>
  <text x="950" y="430" width="62" font-family="Segoe UI" font-size="15" fill="#555555">This way</text>
  <rect x="926" y="502" width="80" height="30" fill="#FFFFFF" stroke="#B6B6B6" stroke-width="2"/>
  <text x="938" y="524" width="58" font-family="Segoe UI" font-size="15" fill="#555555">That way</text>
</svg>
```

## Avoid in this skill
- ❌ Using a real `<table>`-like dense grid with vertical column borders; it makes the slide look like a spreadsheet rather than a process narrative.
- ❌ `marker-end` on `<path>` connectors; use small filled arrowhead paths or direct `<line>` arrows instead.
- ❌ Applying `filter` to `<line>` connectors; shadows should be reserved for nodes, diamonds, and important labels.
- ❌ Using `<textPath>` for curved branch labels; use small white label rectangles placed over the connector route.
- ❌ Clipping or masking non-image elements; keep nodes as editable native shapes.

## Composition notes
- Keep the lane label column narrow, around 15–20% of slide width, and reserve the rest for horizontal process progression.
- Use subtle blue lane dividers and minimal borders so the process shapes remain the visual focus.
- Place nodes on lane centerlines; vertical movement between lanes should clearly signal a hand-off.
- Use warm gold nodes for process actions, white/green diamonds for decisions, and small white branch labels to keep routing legible.