# SVG Recipe — Icon-Based Network Topology Diagram

## Visual mechanism
A hub-and-spoke network map uses clear infrastructure icons inside location “site cards,” with differentiated connector styles to communicate LAN, WAN, internet, and redundant links at a glance. The premium version keeps the engineering clarity of a topology diagram while adding depth through dark canvas, glowing connection lines, soft cards, and color-coded equipment badges.

## SVG primitives needed
- 1× `<rect>` full-slide gradient background for executive dark canvas
- 4× `<rect>` site/container cards for Central Office, Internet Edge, and two Branch Offices
- 12× `<line>` connectors for WAN links, LAN links inside cards, and redundant branch-to-branch path
- 1× dashed `<line>` for redundant/failover connection
- 4× `<circle>` port dots at site-card connection points
- 1× `<path>` cloud icon for Internet / ISP
- 3× building icons made from grouped `<rect>` shapes
- 3× router icons made from rounded `<rect>`, `<circle>`, and small `<path>`/`<line>` details
- 3× switch icons made from rounded `<rect>` plus small port rectangles
- 1× server-rack icon made from stacked `<rect>` modules
- 3× user/workstation icons made from `<circle>` heads and `<path>` shoulders
- 2× `<linearGradient>` fills for background and cards
- 1× `<radialGradient>` for soft network glow
- 1× `<filter id="cardShadow">` applied to card rectangles
- 1× `<filter id="softGlow">` applied to emphasis nodes and cloud path
- Multiple `<text>` labels with explicit `width` attributes for clean PowerPoint rendering

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#071526"/>
      <stop offset="55%" stop-color="#0B2340"/>
      <stop offset="100%" stop-color="#101827"/>
    </linearGradient>
    <linearGradient id="cardFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.98"/>
      <stop offset="100%" stop-color="#EAF3FF" stop-opacity="0.94"/>
    </linearGradient>
    <linearGradient id="blueChip" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#2563EB"/>
    </linearGradient>
    <radialGradient id="hubGlow" cx="50%" cy="42%" r="45%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <ellipse cx="640" cy="350" rx="470" ry="300" fill="url(#hubGlow)"/>
  <line x1="110" y1="665" x2="1170" y2="665" stroke="#1E3A5F" stroke-width="1"/>
  <line x1="180" y1="105" x2="180" y2="650" stroke="#1E3A5F" stroke-width="1" opacity="0.45"/>
  <line x1="640" y1="90" x2="640" y2="650" stroke="#1E3A5F" stroke-width="1" opacity="0.45"/>
  <line x1="1100" y1="105" x2="1100" y2="650" stroke="#1E3A5F" stroke-width="1" opacity="0.45"/>

  <text x="60" y="55" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#F8FAFC">Enterprise Network Topology</text>
  <text x="62" y="86" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9FB3C8">Hub-and-spoke infrastructure view with WAN, LAN, internet edge, and branch redundancy</text>
  <text x="1015" y="58" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#93C5FD" text-anchor="end">Prepared for architecture review</text>

  <!-- WAN and internet connectors behind site cards -->
  <line x1="640" y1="340" x2="252" y2="430" stroke="#38BDF8" stroke-width="4" stroke-linecap="round"/>
  <line x1="640" y1="340" x2="1028" y2="430" stroke="#38BDF8" stroke-width="4" stroke-linecap="round"/>
  <line x1="252" y1="640" x2="1028" y2="640" stroke="#F59E0B" stroke-width="3" stroke-dasharray="12 10" stroke-linecap="round"/>
  <line x1="300" y1="210" x2="445" y2="220" stroke="#A7F3D0" stroke-width="3" stroke-dasharray="7 7" stroke-linecap="round"/>

  <!-- Site cards -->
  <rect x="445" y="105" width="390" height="235" rx="24" fill="url(#cardFill)" stroke="#7DD3FC" stroke-width="1.5" filter="url(#cardShadow)"/>
  <rect x="85" y="135" width="215" height="150" rx="22" fill="#F8FAFC" stroke="#A7F3D0" stroke-width="1.4" filter="url(#cardShadow)"/>
  <rect x="95" y="430" width="315" height="210" rx="24" fill="url(#cardFill)" stroke="#BAE6FD" stroke-width="1.3" filter="url(#cardShadow)"/>
  <rect x="870" y="430" width="315" height="210" rx="24" fill="url(#cardFill)" stroke="#BAE6FD" stroke-width="1.3" filter="url(#cardShadow)"/>

  <!-- Port dots -->
  <circle cx="640" cy="340" r="8" fill="#38BDF8" filter="url(#softGlow)"/>
  <circle cx="252" cy="430" r="7" fill="#38BDF8" filter="url(#softGlow)"/>
  <circle cx="1028" cy="430" r="7" fill="#38BDF8" filter="url(#softGlow)"/>
  <circle cx="300" cy="210" r="6" fill="#A7F3D0" filter="url(#softGlow)"/>

  <!-- Internet cloud -->
  <path d="M139 214 C126 212 116 202 116 188 C116 173 128 161 144 161 C150 143 167 132 187 134 C204 136 218 147 224 163 C241 162 256 174 256 191 C256 207 244 219 226 219 L144 219 C142 219 141 219 139 214 Z" fill="#DCFCE7" stroke="#059669" stroke-width="3" filter="url(#softGlow)"/>
  <text x="118" y="250" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#064E3B" text-anchor="middle">Internet / ISP</text>
  <text x="118" y="270" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#047857" text-anchor="middle">Public cloud + carrier edge</text>

  <!-- Central office label -->
  <text x="470" y="137" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#0F172A">Central Office</text>
  <text x="470" y="158" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Primary routing, switching, servers, and staff LAN</text>

  <!-- Central building icon -->
  <rect x="474" y="178" width="60" height="76" rx="6" fill="#E0F2FE" stroke="#0284C7" stroke-width="2"/>
  <rect x="488" y="191" width="8" height="9" fill="#0284C7"/>
  <rect x="510" y="191" width="8" height="9" fill="#0284C7"/>
  <rect x="488" y="213" width="8" height="9" fill="#0284C7"/>
  <rect x="510" y="213" width="8" height="9" fill="#0284C7"/>
  <rect x="499" y="235" width="12" height="19" fill="#0369A1"/>

  <!-- Central router, switch, server, users -->
  <rect x="570" y="188" width="92" height="48" rx="14" fill="url(#blueChip)" stroke="#0F172A" stroke-width="1"/>
  <circle cx="591" cy="212" r="5" fill="#E0F2FE"/>
  <circle cx="617" cy="212" r="5" fill="#E0F2FE"/>
  <path d="M632 204 L648 212 L632 220" fill="none" stroke="#E0F2FE" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="575" y="252" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155" text-anchor="middle">Core Router</text>
  <rect x="570" y="276" width="92" height="34" rx="9" fill="#1E293B"/>
  <rect x="582" y="288" width="9" height="8" rx="1" fill="#22C55E"/>
  <rect x="599" y="288" width="9" height="8" rx="1" fill="#22C55E"/>
  <rect x="616" y="288" width="9" height="8" rx="1" fill="#FACC15"/>
  <rect x="633" y="288" width="9" height="8" rx="1" fill="#22C55E"/>
  <text x="575" y="324" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155" text-anchor="middle">Core Switch</text>
  <line x1="616" y1="236" x2="616" y2="276" stroke="#64748B" stroke-width="2"/>

  <rect x="693" y="178" width="74" height="126" rx="10" fill="#E2E8F0" stroke="#475569" stroke-width="2"/>
  <rect x="704" y="191" width="52" height="24" rx="4" fill="#334155"/>
  <rect x="704" y="225" width="52" height="24" rx="4" fill="#334155"/>
  <rect x="704" y="259" width="52" height="24" rx="4" fill="#334155"/>
  <circle cx="746" cy="203" r="3" fill="#22C55E"/>
  <circle cx="746" cy="237" r="3" fill="#22C55E"/>
  <circle cx="746" cy="271" r="3" fill="#FACC15"/>
  <text x="678" y="324" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155" text-anchor="middle">Server VLAN</text>
  <line x1="662" y1="212" x2="693" y2="212" stroke="#64748B" stroke-width="2"/>

  <circle cx="806" cy="222" r="16" fill="#38BDF8"/>
  <path d="M780 267 C785 245 827 245 832 267 Z" fill="#2563EB"/>
  <text x="773" y="289" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155" text-anchor="middle">Users</text>
  <line x1="662" y1="293" x2="780" y2="260" stroke="#64748B" stroke-width="2"/>

  <!-- Branch Office 1 -->
  <text x="120" y="462" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0F172A">Branch Office A</text>
  <text x="120" y="482" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">Local LAN connected to central WAN hub</text>
  <rect x="125" y="505" width="50" height="66" rx="6" fill="#E0F2FE" stroke="#0284C7" stroke-width="2"/>
  <rect x="138" y="519" width="7" height="8" fill="#0284C7"/>
  <rect x="156" y="519" width="7" height="8" fill="#0284C7"/>
  <rect x="147" y="551" width="10" height="20" fill="#0369A1"/>
  <rect x="225" y="500" width="78" height="42" rx="13" fill="url(#blueChip)"/>
  <circle cx="244" cy="521" r="4" fill="#E0F2FE"/>
  <circle cx="266" cy="521" r="4" fill="#E0F2FE"/>
  <rect x="225" y="565" width="78" height="31" rx="8" fill="#1E293B"/>
  <rect x="238" y="576" width="8" height="7" rx="1" fill="#22C55E"/>
  <rect x="253" y="576" width="8" height="7" rx="1" fill="#22C55E"/>
  <rect x="268" y="576" width="8" height="7" rx="1" fill="#FACC15"/>
  <line x1="264" y1="542" x2="264" y2="565" stroke="#64748B" stroke-width="2"/>
  <circle cx="350" cy="526" r="14" fill="#38BDF8"/>
  <path d="M327 566 C332 546 369 546 374 566 Z" fill="#2563EB"/>
  <line x1="303" y1="580" x2="327" y2="558" stroke="#64748B" stroke-width="2"/>
  <text x="220" y="621" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155" text-anchor="middle">Router + Access Switch</text>

  <!-- Branch Office 2 -->
  <text x="895" y="462" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0F172A">Branch Office B</text>
  <text x="895" y="482" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">Mirrored spoke with failover path</text>
  <rect x="900" y="505" width="50" height="66" rx="6" fill="#E0F2FE" stroke="#0284C7" stroke-width="2"/>
  <rect x="913" y="519" width="7" height="8" fill="#0284C7"/>
  <rect x="931" y="519" width="7" height="8" fill="#0284C7"/>
  <rect x="922" y="551" width="10" height="20" fill="#0369A1"/>
  <rect x="1000" y="500" width="78" height="42" rx="13" fill="url(#blueChip)"/>
  <circle cx="1019" cy="521" r="4" fill="#E0F2FE"/>
  <circle cx="1041" cy="521" r="4" fill="#E0F2FE"/>
  <rect x="1000" y="565" width="78" height="31" rx="8" fill="#1E293B"/>
  <rect x="1013" y="576" width="8" height="7" rx="1" fill="#22C55E"/>
  <rect x="1028" y="576" width="8" height="7" rx="1" fill="#22C55E"/>
  <rect x="1043" y="576" width="8" height="7" rx="1" fill="#FACC15"/>
  <line x1="1039" y1="542" x2="1039" y2="565" stroke="#64748B" stroke-width="2"/>
  <circle cx="1125" cy="526" r="14" fill="#38BDF8"/>
  <path d="M1102 566 C1107 546 1144 546 1149 566 Z" fill="#2563EB"/>
  <line x1="1078" y1="580" x2="1102" y2="558" stroke="#64748B" stroke-width="2"/>
  <text x="995" y="621" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155" text-anchor="middle">Router + Access Switch</text>

  <!-- Legend -->
  <rect x="900" y="104" width="285" height="112" rx="18" fill="#0F2745" stroke="#315A84" stroke-width="1"/>
  <text x="922" y="134" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#F8FAFC">Connection legend</text>
  <line x1="925" y1="158" x2="985" y2="158" stroke="#38BDF8" stroke-width="4" stroke-linecap="round"/>
  <text x="1000" y="163" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">Primary WAN link</text>
  <line x1="925" y1="184" x2="985" y2="184" stroke="#F59E0B" stroke-width="3" stroke-dasharray="10 8" stroke-linecap="round"/>
  <text x="1000" y="189" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">Redundant failover</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<use>` or external SVG icon sprites for repeated router/switch icons; duplicate the editable primitives instead.
- ❌ Putting `filter` on connector `<line>` elements; PowerPoint translation drops line filters, so keep glow on endpoint circles or nearby shapes.
- ❌ Using `marker-end` on `<path>` connectors; if arrows are required, use `<line>` with direct marker settings or draw small triangular arrowheads as editable `<path>` shapes.
- ❌ Clipping or masking non-image shapes to create icon silhouettes; use direct `<path>`, `<rect>`, and `<circle>` drawings.
- ❌ Overcrowding the canvas with every physical device; this style works best as an architectural abstraction, not a full rack inventory.

## Composition notes
- Keep the central office card in the upper-middle third, with branch cards balanced at the lower left and lower right to make the hub-and-spoke logic instantly readable.
- Draw long WAN connectors behind the cards first, then place cards/icons on top; use endpoint circles to make connections feel intentional.
- Use solid cool-blue lines for primary connectivity and dashed amber lines for backup, failover, or secondary paths.
- Reserve the top-right or side margin for a compact legend so non-technical stakeholders can decode line styles without interrupting the topology.