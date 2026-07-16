# SVG Recipe — Icon-Based Network Topology Diagram with Status Monitoring

## Visual mechanism
A clean network map uses editable icon groups for routers, switches, servers, access points, and endpoints, connected by thin topology lines. A separate right-side monitoring panel repeats the same device names with color-coded health chips so the audience can instantly correlate topology position with operational status.

## SVG primitives needed
- 1× full-slide `<rect>` for the soft technical background.
- 2× `<linearGradient>` for premium blue device fills and neutral panel/card fills.
- 2× `<filter>` definitions: one soft card shadow and one status glow applied only to shapes, not lines.
- 10–14× `<line>` for network links, including dashed red degraded/down links.
- 8× device-card `<rect>` shapes for editable node containers.
- 20+× `<rect>`, `<circle>`, `<ellipse>`, and `<path>` shapes for standardized network icons: cloud, router, switch, server, database, access point, camera, and PCs.
- 1× right-side monitoring-panel `<rect>` plus table-row `<rect>` elements.
- 8× status indicator `<circle>` or rounded `<rect>` chips using green, amber, and red fills.
- Multiple `<text width="...">` labels for title, device names, IP addresses, row labels, and status values.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7fbff"/>
      <stop offset="55%" stop-color="#eef4fb"/>
      <stop offset="100%" stop-color="#e7eef7"/>
    </linearGradient>
    <linearGradient id="deviceBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2f8fe8"/>
      <stop offset="100%" stop-color="#075aa7"/>
    </linearGradient>
    <linearGradient id="panelFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f2f6fb"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="statusGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M0,92 C180,35 294,90 438,49 C580,8 707,33 830,88 C1004,166 1138,74 1280,116 L1280,0 L0,0 Z" fill="#dbeafe" opacity="0.42"/>
  <text x="52" y="58" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#102033">Network Topology &amp; Status</text>
  <text x="54" y="88" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#53677c">Live operational snapshot — topology, degraded links, and device health</text>

  <rect x="42" y="118" width="850" height="548" rx="28" fill="#ffffff" opacity="0.78" stroke="#d3dfec"/>
  <text x="70" y="152" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#5b7088">PRIMARY LAN SEGMENT</text>
  <rect x="70" y="168" width="790" height="1.5" fill="#d6e2ef"/>

  <!-- topology links -->
  <line x1="222" y1="231" x2="410" y2="319" stroke="#75869a" stroke-width="3"/>
  <line x1="410" y1="319" x2="270" y2="498" stroke="#75869a" stroke-width="3"/>
  <line x1="410" y1="319" x2="560" y2="500" stroke="#75869a" stroke-width="3"/>
  <line x1="410" y1="319" x2="645" y2="319" stroke="#75869a" stroke-width="3"/>
  <line x1="645" y1="319" x2="744" y2="200" stroke="#75869a" stroke-width="3"/>
  <line x1="645" y1="319" x2="757" y2="498" stroke="#e23a3a" stroke-width="3.5" stroke-dasharray="9 8"/>
  <line x1="222" y1="231" x2="132" y2="185" stroke="#75869a" stroke-width="3"/>
  <line x1="744" y1="200" x2="822" y2="152" stroke="#e23a3a" stroke-width="3.5" stroke-dasharray="9 8"/>

  <!-- internet cloud -->
  <g transform="translate(70 138)">
    <path d="M48,65 C29,65 17,53 17,38 C17,25 27,15 40,16 C47,4 61,0 75,6 C84,0 101,3 109,16 C127,18 139,30 139,46 C139,59 128,68 112,68 L48,68 Z" fill="#ffffff" stroke="#9fb2c7" stroke-width="2" filter="url(#shadow)"/>
    <path d="M50,37 C70,25 83,25 105,38" fill="none" stroke="#2f8fe8" stroke-width="3"/>
    <text x="30" y="94" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#182a3b">Internet</text>
    <text x="18" y="113" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#63778b">WAN uplink</text>
  </g>

  <!-- edge router -->
  <g transform="translate(170 188)">
    <rect x="0" y="0" width="104" height="86" rx="18" fill="#ffffff" stroke="#c8d6e6" filter="url(#shadow)"/>
    <ellipse cx="52" cy="34" rx="34" ry="21" fill="url(#deviceBlue)" stroke="#053f78" stroke-width="2"/>
    <path d="M34,29 L21,20 M70,29 L83,20 M34,39 L21,48 M70,39 L83,48" stroke="#b6ffcf" stroke-width="3" fill="none"/>
    <circle cx="88" cy="15" r="6" fill="#00b050" filter="url(#statusGlow)"/>
    <text x="-10" y="108" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#162638">Edge-RTR</text>
    <text x="-18" y="126" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#65778b">10.11.32.1</text>
  </g>

  <!-- core switch -->
  <g transform="translate(358 276)">
    <rect x="0" y="0" width="112" height="86" rx="18" fill="#ffffff" stroke="#c8d6e6" filter="url(#shadow)"/>
    <rect x="19" y="27" width="74" height="31" rx="7" fill="url(#deviceBlue)" stroke="#053f78" stroke-width="2"/>
    <path d="M32,42 L79,42 M71,35 L82,42 L71,49 M43,49 L31,57 L43,65" stroke="#b6ffcf" stroke-width="3" fill="none"/>
    <circle cx="96" cy="15" r="6" fill="#00b050" filter="url(#statusGlow)"/>
    <text x="-5" y="108" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#162638">Core-SW1</text>
    <text x="-14" y="126" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#65778b">10.11.32.2</text>
  </g>

  <!-- server -->
  <g transform="translate(218 455)">
    <rect x="0" y="0" width="104" height="86" rx="18" fill="#ffffff" stroke="#c8d6e6" filter="url(#shadow)"/>
    <rect x="37" y="15" width="32" height="57" rx="5" fill="#687786" stroke="#2d3b49" stroke-width="2"/>
    <circle cx="47" cy="28" r="3" fill="#00b050"/>
    <rect x="44" y="41" width="18" height="3" rx="1.5" fill="#aebbc8"/>
    <rect x="44" y="52" width="18" height="3" rx="1.5" fill="#aebbc8"/>
    <circle cx="88" cy="15" r="6" fill="#00b050" filter="url(#statusGlow)"/>
    <text x="-14" y="108" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#162638">App-Server01</text>
    <text x="-18" y="126" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#65778b">10.11.32.187</text>
  </g>

  <!-- database -->
  <g transform="translate(508 455)">
    <rect x="0" y="0" width="104" height="86" rx="18" fill="#ffffff" stroke="#c8d6e6" filter="url(#shadow)"/>
    <ellipse cx="52" cy="25" rx="29" ry="12" fill="#7d8996" stroke="#2f3d4b" stroke-width="2"/>
    <path d="M23,25 L23,58 C23,66 36,72 52,72 C68,72 81,66 81,58 L81,25" fill="#687786" stroke="#2f3d4b" stroke-width="2"/>
    <path d="M23,42 C23,50 36,56 52,56 C68,56 81,50 81,42" fill="none" stroke="#aebbc8" stroke-width="2"/>
    <circle cx="88" cy="15" r="6" fill="#00b050" filter="url(#statusGlow)"/>
    <text x="-10" y="108" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#162638">DB-Cluster</text>
    <text x="-18" y="126" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#65778b">10.11.32.21</text>
  </g>

  <!-- access point -->
  <g transform="translate(692 157)">
    <rect x="0" y="0" width="104" height="86" rx="18" fill="#ffffff" stroke="#c8d6e6" filter="url(#shadow)"/>
    <circle cx="52" cy="44" r="21" fill="url(#deviceBlue)" stroke="#053f78" stroke-width="2"/>
    <path d="M35,31 C45,21 60,21 69,31 M28,24 C42,9 64,9 78,24" stroke="#b6ffcf" stroke-width="3" fill="none"/>
    <rect x="47" y="43" width="10" height="18" rx="3" fill="#ffffff"/>
    <circle cx="88" cy="15" r="6" fill="#00b050" filter="url(#statusGlow)"/>
    <text x="-7" y="108" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#162638">AP-01</text>
    <text x="-18" y="126" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#65778b">10.11.32.57</text>
  </g>

  <!-- camera down -->
  <g transform="translate(705 455)">
    <rect x="0" y="0" width="104" height="86" rx="18" fill="#ffffff" stroke="#f0b1b1" filter="url(#shadow)"/>
    <rect x="28" y="29" width="42" height="24" rx="5" fill="#6f7d8d" stroke="#303d4c" stroke-width="2"/>
    <path d="M70,34 L86,27 L86,55 L70,48 Z" fill="#6f7d8d" stroke="#303d4c" stroke-width="2"/>
    <circle cx="43" cy="41" r="8" fill="#1d2b3a"/>
    <circle cx="88" cy="15" r="6" fill="#ff3b30" filter="url(#statusGlow)"/>
    <text x="-9" y="108" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#162638">Camera-01</text>
    <text x="-18" y="126" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#65778b">10.11.32.17</text>
  </g>

  <!-- remote user down -->
  <g transform="translate(785 102)">
    <rect x="0" y="0" width="104" height="86" rx="18" fill="#ffffff" stroke="#f0b1b1" filter="url(#shadow)"/>
    <rect x="25" y="23" width="54" height="35" rx="4" fill="#778492" stroke="#303d4c" stroke-width="2"/>
    <rect x="44" y="58" width="17" height="9" fill="#303d4c"/>
    <rect x="34" y="67" width="37" height="5" rx="2" fill="#303d4c"/>
    <circle cx="88" cy="15" r="6" fill="#ff3b30" filter="url(#statusGlow)"/>
    <text x="-9" y="108" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#162638">Mary-PC</text>
    <text x="-18" y="126" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#65778b">10.11.32.14</text>
  </g>

  <!-- status monitoring panel -->
  <rect x="928" y="72" width="302" height="594" rx="30" fill="url(#panelFill)" stroke="#cfdbea" filter="url(#shadow)"/>
  <text x="958" y="116" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#102033">Status Monitor</text>
  <text x="958" y="140" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6a7d91">Updated 09:42 UTC · 8 devices</text>
  <rect x="958" y="164" width="242" height="36" rx="12" fill="#ecf3fb"/>
  <text x="976" y="187" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#53677c">DEVICE</text>
  <text x="1115" y="187" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#53677c">HEALTH</text>

  <rect x="958" y="214" width="242" height="42" rx="12" fill="#ffffff" stroke="#e0e8f2"/>
  <circle cx="978" cy="235" r="7" fill="#00b050"/><text x="995" y="240" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1f3042">Edge-RTR</text><rect x="1115" y="223" width="58" height="24" rx="12" fill="#dff6e8"/><text x="1130" y="240" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#00833b">UP</text>
  <rect x="958" y="264" width="242" height="42" rx="12" fill="#ffffff" stroke="#e0e8f2"/>
  <circle cx="978" cy="285" r="7" fill="#00b050"/><text x="995" y="290" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1f3042">Core-SW1</text><rect x="1115" y="273" width="58" height="24" rx="12" fill="#dff6e8"/><text x="1130" y="290" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#00833b">UP</text>
  <rect x="958" y="314" width="242" height="42" rx="12" fill="#ffffff" stroke="#e0e8f2"/>
  <circle cx="978" cy="335" r="7" fill="#00b050"/><text x="995" y="340" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1f3042">App-Server01</text><rect x="1115" y="323" width="58" height="24" rx="12" fill="#dff6e8"/><text x="1130" y="340" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#00833b">UP</text>
  <rect x="958" y="364" width="242" height="42" rx="12" fill="#ffffff" stroke="#e0e8f2"/>
  <circle cx="978" cy="385" r="7" fill="#00b050"/><text x="995" y="390" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1f3042">DB-Cluster</text><rect x="1115" y="373" width="58" height="24" rx="12" fill="#dff6e8"/><text x="1130" y="390" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#00833b">UP</text>
  <rect x="958" y="414" width="242" height="42" rx="12" fill="#ffffff" stroke="#e0e8f2"/>
  <circle cx="978" cy="435" r="7" fill="#00b050"/><text x="995" y="440" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1f3042">AP-01</text><rect x="1115" y="423" width="58" height="24" rx="12" fill="#dff6e8"/><text x="1130" y="440" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#00833b">UP</text>
  <rect x="958" y="464" width="242" height="42" rx="12" fill="#fff5f5" stroke="#ffc4c4"/>
  <circle cx="978" cy="485" r="7" fill="#ff3b30"/><text x="995" y="490" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1f3042">Camera-01</text><rect x="1115" y="473" width="68" height="24" rx="12" fill="#ffe1df"/><text x="1128" y="490" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#c91d17">DOWN</text>
  <rect x="958" y="514" width="242" height="42" rx="12" fill="#fff5f5" stroke="#ffc4c4"/>
  <circle cx="978" cy="535" r="7" fill="#ff3b30"/><text x="995" y="540" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1f3042">Mary-PC</text><rect x="1115" y="523" width="68" height="24" rx="12" fill="#ffe1df"/><text x="1128" y="540" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#c91d17">DOWN</text>

  <rect x="958" y="582" width="242" height="54" rx="16" fill="#102033"/>
  <text x="978" y="606" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ffffff">Incident focus</text>
  <text x="978" y="626" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#b9c7d6">Wireless branch link and camera feed require triage.</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<foreignObject>` or HTML tables for the monitoring panel; build rows with editable `<rect>`, `<circle>`, and `<text>` instead.
- ❌ Applying `<filter>` to connector `<line>` elements; shadows/glows should go on node cards and status dots only.
- ❌ Using `marker-end` on `<path>` for topology arrows; if direction is needed, use simple `<line>` connectors plus small editable arrowhead `<path>` triangles.
- ❌ Placing `clip-path` on icon groups or non-image shapes; unsupported clipping can be ignored and break visual consistency.
- ❌ Overcrowding the topology with too many endpoints; dense technical accuracy should be summarized into segments or collapsed nodes.

## Composition notes
- Keep the topology map on the left 70% of the canvas and reserve the right 25–30% for the status panel.
- Put the highest-importance infrastructure near the visual center: router → core switch → server/database, with endpoints radiating outward.
- Use neutral gray-blue connector lines for healthy links and red dashed lines for degraded/down paths.
- Repeat status colors in both places: small dots on device cards and larger chips in the monitoring table for instant cross-reference.