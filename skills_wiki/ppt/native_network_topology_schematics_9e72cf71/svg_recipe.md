# SVG Recipe — Native Network Topology Schematics

## Visual mechanism
A premium network topology schematic uses grid-aligned technical nodes, soft colored security zones, and crisp orthogonal connectors to make infrastructure relationships readable at a glance. The diagram feels native and editable because every device, connector, icon, label, and arrowhead is built from SVG primitives rather than flattened screenshots.

## SVG primitives needed
- 5× large <rect> for background, topology canvas, cloud/network zone panels, and rack/switch devices
- 12× small <rect> for port indicators, labels, and status chips
- 8× <circle> for router, packet/status dots, and switch ports
- 6× <ellipse> for server/database cylinder tops and bases
- 10× <line> for orthogonal elbow connector segments
- 9× <path> for cloud silhouette, manual arrowheads, shield/security icon, and decorative data-flow chevrons
- 1× <linearGradient> for dark executive background
- 5× <linearGradient> for node and zone fills
- 1× <radialGradient> for subtle topology glow
- 2× <filter> with feOffset+feGaussianBlur+feMerge for node shadows and line glow
- Multiple <text> elements with explicit width attributes for titles, node names, IPs, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="58%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <radialGradient id="halo" cx="50%" cy="42%" r="65%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.20"/>
      <stop offset="70%" stop-color="#38BDF8" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="zoneBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EFF6FF"/>
      <stop offset="100%" stop-color="#DBEAFE"/>
    </linearGradient>
    <linearGradient id="zoneGreen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ECFDF5"/>
      <stop offset="100%" stop-color="#D1FAE5"/>
    </linearGradient>
    <linearGradient id="zoneRed" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF1F2"/>
      <stop offset="100%" stop-color="#FFE4E6"/>
    </linearGradient>
    <linearGradient id="nodeWhite" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>
    <linearGradient id="switchGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#DCFCE7"/>
      <stop offset="100%" stop-color="#BBF7D0"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .20 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="soft"/>
      <feMerge><feMergeNode in="soft"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#halo)"/>
  <path d="M80 132 H1200" stroke="#334155" stroke-width="1" stroke-dasharray="4 10" opacity="0.55"/>
  <path d="M80 232 H1200 M80 332 H1200 M80 432 H1200 M80 532 H1200 M80 632 H1200" stroke="#334155" stroke-width="1" stroke-dasharray="4 10" opacity="0.35"/>
  <path d="M180 110 V660 M380 110 V660 M580 110 V660 M780 110 V660 M980 110 V660 M1180 110 V660" stroke="#334155" stroke-width="1" stroke-dasharray="4 10" opacity="0.25"/>

  <text x="72" y="58" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#F8FAFC">Network Infrastructure Topology</text>
  <text x="72" y="88" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94A3B8">Logical flow from public WAN through edge routing into segmented application and data tiers</text>
  <rect x="992" y="44" width="174" height="34" rx="17" fill="#0F766E" opacity="0.95"/>
  <circle cx="1014" cy="61" r="5" fill="#5EEAD4"/>
  <text x="1028" y="66" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ECFEFF">LIVE DESIGN</text>

  <rect x="70" y="126" width="1140" height="520" rx="28" fill="#FFFFFF" opacity="0.05" stroke="#475569" stroke-width="1.2"/>
  <rect x="105" y="170" width="270" height="420" rx="22" fill="url(#zoneRed)" opacity="0.96" stroke="#FDA4AF" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="425" y="170" width="340" height="420" rx="22" fill="url(#zoneGreen)" opacity="0.96" stroke="#86EFAC" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="815" y="170" width="300" height="420" rx="22" fill="url(#zoneBlue)" opacity="0.96" stroke="#93C5FD" stroke-width="1.5" filter="url(#shadow)"/>

  <text x="126" y="205" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#9F1239">EDGE / DMZ</text>
  <text x="446" y="205" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#166534">CORE SWITCHING</text>
  <text x="836" y="205" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1D4ED8">APPLICATION + DATA</text>

  <path d="M195 262 C170 257 158 238 169 219 C176 204 191 198 205 202 C216 181 247 176 264 196 C284 190 306 202 311 224 C334 226 348 244 342 264 C337 282 320 292 296 292 H202 C181 292 168 280 169 266 C170 263 185 261 195 262 Z" fill="url(#nodeWhite)" stroke="#64748B" stroke-width="2" filter="url(#shadow)"/>
  <text x="204" y="247" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#0F172A">Internet</text>
  <text x="204" y="268" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">Public WAN</text>

  <circle cx="240" cy="380" r="58" fill="#FFF1F2" stroke="#E11D48" stroke-width="2.5" filter="url(#shadow)"/>
  <path d="M208 382 C224 364 255 364 272 382 M216 398 C230 407 251 407 264 398 M240 325 V346 M240 414 V435 M185 380 H207 M273 380 H295" stroke="#E11D48" stroke-width="4" stroke-linecap="round" fill="none"/>
  <text x="181" y="470" width="118" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#0F172A">Edge Router</text>
  <text x="181" y="491" width="118" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">10.0.0.1</text>

  <rect x="470" y="340" width="250" height="82" rx="18" fill="url(#switchGrad)" stroke="#16A34A" stroke-width="2.5" filter="url(#shadow)"/>
  <rect x="492" y="371" width="32" height="20" rx="4" fill="#16A34A"/>
  <rect x="536" y="371" width="32" height="20" rx="4" fill="#16A34A"/>
  <rect x="580" y="371" width="32" height="20" rx="4" fill="#16A34A"/>
  <rect x="624" y="371" width="32" height="20" rx="4" fill="#16A34A"/>
  <rect x="668" y="371" width="32" height="20" rx="4" fill="#16A34A"/>
  <circle cx="505" cy="360" r="4" fill="#BBF7D0"/>
  <circle cx="549" cy="360" r="4" fill="#BBF7D0"/>
  <circle cx="593" cy="360" r="4" fill="#BBF7D0"/>
  <circle cx="637" cy="360" r="4" fill="#BBF7D0"/>
  <circle cx="681" cy="360" r="4" fill="#BBF7D0"/>
  <text x="506" y="324" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#0F172A">Main Switch</text>
  <text x="506" y="445" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">VLAN 10 / 20 / 30</text>

  <rect x="860" y="265" width="168" height="110" rx="18" fill="url(#nodeWhite)" stroke="#2563EB" stroke-width="2.5" filter="url(#shadow)"/>
  <path d="M922 298 h44 a10 10 0 0 1 10 10 v27 a10 10 0 0 1-10 10 h-44 a10 10 0 0 1-10-10 v-27 a10 10 0 0 1 10-10 Z M929 298 v-14 h30 v14" fill="none" stroke="#2563EB" stroke-width="4" stroke-linejoin="round"/>
  <text x="886" y="404" width="118" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#0F172A">API Gateway</text>
  <text x="886" y="425" width="118" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">10.0.20.14</text>

  <rect x="860" y="470" width="168" height="58" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.5"/>
  <ellipse cx="944" cy="470" rx="84" ry="22" fill="#DBEAFE" stroke="#2563EB" stroke-width="2.5"/>
  <ellipse cx="944" cy="528" rx="84" ry="22" fill="#BFDBFE" stroke="#2563EB" stroke-width="2.5" filter="url(#shadow)"/>
  <text x="886" y="490" width="118" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#0F172A">DB Cluster</text>
  <text x="886" y="511" width="118" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">10.0.30.5</text>

  <path d="M1095 300 l34 14 v31 c0 31-21 52-34 60 c-13-8-34-29-34-60 v-31 Z" fill="#ECFDF5" stroke="#059669" stroke-width="2.5" filter="url(#shadow)"/>
  <path d="M1079 349 l11 11 l26-31" stroke="#059669" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <text x="1044" y="432" width="104" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#0F172A">WAF Policy</text>

  <line x1="240" y1="292" x2="240" y2="322" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <path d="M240 334 L231 318 H249 Z" fill="#38BDF8"/>
  <line x1="240" y1="438" x2="240" y2="522" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <line x1="240" y1="522" x2="595" y2="522" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <line x1="595" y1="522" x2="595" y2="422" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <path d="M595 410 L586 426 H604 Z" fill="#38BDF8"/>
  <line x1="720" y1="381" x2="800" y2="381" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <line x1="800" y1="381" x2="800" y2="320" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <line x1="800" y1="320" x2="860" y2="320" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <path d="M872 320 L856 311 V329 Z" fill="#38BDF8"/>
  <line x1="720" y1="381" x2="785" y2="381" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <line x1="785" y1="381" x2="785" y2="505" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <line x1="785" y1="505" x2="860" y2="505" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
  <path d="M872 505 L856 496 V514 Z" fill="#38BDF8"/>

  <circle cx="398" cy="522" r="5" fill="#67E8F9"/>
  <circle cx="442" cy="522" r="5" fill="#67E8F9" opacity="0.75"/>
  <circle cx="486" cy="522" r="5" fill="#67E8F9" opacity="0.50"/>
  <text x="110" y="625" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">Dashed grid, muted security zones, and orthogonal connectors keep the architecture editable while preserving executive polish.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use <path> connectors with marker-end; arrowheads on paths may disappear. Use <line> segments plus manual triangular <path> arrowheads, or marker-end directly on each <line> if your pipeline supports it.
- ❌ Do not rely on screenshots from external diagramming tools; the value of this skill is fully editable native topology components.
- ❌ Do not place connector lines randomly or diagonally through nodes; route them orthogonally through open whitespace.
- ❌ Do not use <use>, <symbol>, <foreignObject>, masks, or textPath for repeated icons or labels; duplicate editable primitives directly.
- ❌ Do not apply filters to <line> if exact PowerPoint fidelity is critical; use glow sparingly and expect plain lines to remain the fallback.

## Composition notes
- Keep the topology inside a large central canvas, with title and metadata above; leave at least 40–60 px of breathing room around the diagram.
- Use colored zones to group responsibility boundaries: DMZ/edge, core network, application/data tier, cloud services, or security layer.
- Make the switch/router layer visually central, then fan out to application and database nodes with clean elbow connectors.
- Use dark outer backgrounds with light node cards for keynote polish, but keep device labels high-contrast and short.