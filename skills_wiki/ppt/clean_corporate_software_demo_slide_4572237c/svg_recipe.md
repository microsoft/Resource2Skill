# SVG Recipe — Clean Corporate Software Demo Slide

## Visual mechanism
A crisp executive split layout pairs a left-side value proposition with a right-side “software demo evidence” panel: a polished app-window mockup containing a gridded network diagram. A stable three-part footer anchors legal copy, URL, and brand identity without competing with the hero graphic.

## SVG primitives needed
- 9× `<rect>` for the white background, accent rail, eyebrow pill, hero app card, toolbar strip, footer band, and logo geometry
- 20× `<line>` for app gridlines, network connector lines, and simple device glyphs
- 6× `<ellipse>` for router bodies, router highlights, and soft device shadows
- 12× `<path>` for decorative background curve, 3D switch side faces, router arrows, and switch port/star glyphs
- 17× `<text>` for title, body copy, presenter metadata, device labels, port numbers, footer copy, URL, and logo wordmark
- 2× `<linearGradient>` for the corporate blue device fills and the subtle app toolbar
- 1× `<filter id="cardShadow">` applied to the hero app panel
- 1× `<filter id="softGlow">` applied to the accent illustration and device cards

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueDevice" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#21B4E8"/>
      <stop offset="55%" stop-color="#168CC6"/>
      <stop offset="100%" stop-color="#086C9D"/>
    </linearGradient>
    <linearGradient id="toolbarGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F9FAFB"/>
      <stop offset="100%" stop-color="#E8EBEF"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <path d="M1030 74 C1135 50 1216 100 1240 188 C1272 306 1194 407 1076 393 C1002 384 950 338 938 273 C922 184 954 96 1030 74 Z" fill="#EAF6FC" opacity="0.85"/>
  <rect x="72" y="124" width="6" height="316" rx="3" fill="#3498DB"/>

  <rect x="96" y="126" width="162" height="31" rx="15.5" fill="#EEF7FD"/>
  <text x="116" y="147" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#2479A8" letter-spacing="1.5">SOFTWARE DEMO</text>

  <text x="96" y="220" width="530" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="700" fill="#111827">
    Intelligent Network
  </text>
  <text x="96" y="272" width="530" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="700" fill="#111827">
    Connector
  </text>
  <text x="96" y="332" width="465" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" fill="#333333">
    See how the intelligent connector shape accelerates network documentation, reduces manual routing, and keeps diagrams presentation-ready.
  </text>

  <text x="96" y="430" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700" fill="#222222">Robert Cowham</text>
  <text x="96" y="456" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#666666">Services Director</text>

  <rect x="630" y="104" width="560" height="454" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="630" y="104" width="560" height="52" rx="22" fill="url(#toolbarGrad)"/>
  <rect x="630" y="137" width="560" height="21" fill="#E8EBEF"/>
  <circle cx="657" cy="130" r="6" fill="#F87171"/>
  <circle cx="678" cy="130" r="6" fill="#FBBF24"/>
  <circle cx="699" cy="130" r="6" fill="#34D399"/>
  <text x="730" y="135" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#6B7280">Network Diagram — connector demo</text>

  <line x1="670" y1="190" x2="1150" y2="190" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="670" y1="230" x2="1150" y2="230" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="670" y1="270" x2="1150" y2="270" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="670" y1="310" x2="1150" y2="310" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="670" y1="350" x2="1150" y2="350" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="670" y1="390" x2="1150" y2="390" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="670" y1="430" x2="1150" y2="430" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="710" y1="170" x2="710" y2="520" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="770" y1="170" x2="770" y2="520" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="830" y1="170" x2="830" y2="520" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="890" y1="170" x2="890" y2="520" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="950" y1="170" x2="950" y2="520" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="1010" y1="170" x2="1010" y2="520" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="1070" y1="170" x2="1070" y2="520" stroke="#EDF0F3" stroke-width="1"/>
  <line x1="1130" y1="170" x2="1130" y2="520" stroke="#EDF0F3" stroke-width="1"/>

  <line x1="785" y1="278" x2="785" y2="406" stroke="#6B7280" stroke-width="2"/>
  <line x1="1040" y1="278" x2="1040" y2="406" stroke="#6B7280" stroke-width="2"/>
  <line x1="817" y1="286" x2="1006" y2="414" stroke="#8B949E" stroke-width="2"/>
  <line x1="1008" y1="286" x2="817" y2="414" stroke="#8B949E" stroke-width="2"/>

  <ellipse cx="782" cy="420" rx="64" ry="17" fill="#0B5E8C" opacity="0.20"/>
  <ellipse cx="1038" cy="420" rx="64" ry="17" fill="#0B5E8C" opacity="0.20"/>

  <rect x="735" y="214" width="96" height="72" rx="4" fill="url(#blueDevice)" filter="url(#softGlow)"/>
  <path d="M831 214 L848 203 L848 274 L831 286 Z" fill="#0B78B3"/>
  <path d="M735 214 L752 203 L848 203 L831 214 Z" fill="#3AC2F0"/>
  <rect x="744" y="262" width="78" height="20" rx="3" fill="#FFFFFF" opacity="0.92"/>
  <text x="749" y="277" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#1F2937">SW-BHAM-01</text>
  <circle cx="783" cy="248" r="15" fill="#EF4444"/>
  <text x="775" y="254" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">Si</text>
  <path d="M783 225 L783 241 M762 248 L776 248 M790 248 L804 248 M768 233 L778 243 M798 233 L788 243" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none"/>

  <rect x="992" y="214" width="96" height="72" rx="4" fill="url(#blueDevice)" filter="url(#softGlow)"/>
  <path d="M1088 214 L1105 203 L1105 274 L1088 286 Z" fill="#0B78B3"/>
  <path d="M992 214 L1009 203 L1105 203 L1088 214 Z" fill="#3AC2F0"/>
  <rect x="1001" y="262" width="78" height="20" rx="3" fill="#FFFFFF" opacity="0.92"/>
  <text x="1006" y="277" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#1F2937">SW-BHAM-02</text>
  <circle cx="1040" cy="248" r="15" fill="#EF4444"/>
  <text x="1032" y="254" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">Si</text>
  <path d="M1040 225 L1040 241 M1019 248 L1033 248 M1047 248 L1061 248 M1025 233 L1035 243 M1055 233 L1045 243" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none"/>

  <ellipse cx="785" cy="416" rx="58" ry="25" fill="url(#blueDevice)"/>
  <ellipse cx="785" cy="403" rx="58" ry="25" fill="#16A6D8"/>
  <path d="M754 400 L778 392 L771 400 L795 400 L788 392 L818 402 M756 411 L779 419 L772 411 L795 411 L788 419 L817 410" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none"/>
  <text x="735" y="439" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#1F2937">RTR-BHAM-01</text>

  <ellipse cx="1040" cy="416" rx="58" ry="25" fill="url(#blueDevice)"/>
  <ellipse cx="1040" cy="403" rx="58" ry="25" fill="#16A6D8"/>
  <path d="M1009 400 L1033 392 L1026 400 L1050 400 L1043 392 L1073 402 M1011 411 L1034 419 L1027 411 L1050 411 L1043 419 L1072 410" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none"/>
  <text x="990" y="439" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#1F2937">RTR-BHAM-02</text>

  <text x="756" y="356" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700" fill="#374151">2</text>
  <text x="834" y="371" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700" fill="#374151">3</text>
  <text x="748" y="306" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700" fill="#374151">27</text>

  <rect x="0" y="642" width="1280" height="78" fill="#F7F8FA"/>
  <line x1="72" y1="642" x2="1208" y2="642" stroke="#E2E8F0" stroke-width="1"/>
  <text x="72" y="688" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#777777">© 2026 Square Mile Systems. Product names are trademarks of their owners.</text>
  <text x="538" y="688" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#3498DB">www.squaremilesystems.com</text>
  <rect x="1015" y="662" width="42" height="42" rx="6" fill="#3498DB"/>
  <rect x="1028" y="675" width="16" height="16" rx="2" fill="#FFFFFF"/>
  <text x="1068" y="680" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#111827">SQUARE</text>
  <text x="1068" y="701" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#111827">MILE</text>
</svg>
```

## Avoid in this skill
- ❌ `<pattern>` fills for the software grid; draw a small number of editable `<line>` gridlines instead.
- ❌ `marker-end` on connector paths; if arrows are required, build arrowheads manually with small `<path>` shapes or use plain connector lines.
- ❌ Filters on `<line>` elements for network links; keep shadows/glows on cards, devices, or paths only.
- ❌ Overcrowding the right panel with too many tiny labels; the diagram should read as technical evidence, not a full network specification.
- ❌ Footer text larger than the main body copy; the footer is brand infrastructure, not a fourth content block.

## Composition notes
- Keep the left narrative column to roughly 45% of the slide width, with a strong vertical margin and generous line spacing.
- The right hero panel should feel like a polished software screenshot: toolbar, grid, diagram, and subtle card shadow.
- Use blue as the repeated corporate accent: eyebrow pill, diagram devices, URL, and logo mark.
- Reserve the bottom 10–12% of the slide for the tripartite footer so the slide feels stable during a demo intro or closing frame.