# SVG Recipe — Tech Dashboard Network Topology

## Visual mechanism
A dark-mode monitoring-dashboard canvas frames a network segment as a glowing rounded container, with service nodes arranged on a grid and linked by thin orthogonal connector paths. Each node uses compact dashboard typography, small status indicators, and simple native icons to make the architecture feel operational and credible.

## SVG primitives needed
- 1× `<rect>` full-slide background using a dark linear gradient
- 1× large rounded `<rect>` for the topology boundary / network segment container
- 8–10× rounded `<rect>` for service nodes, header pills, and small metric badges
- 6–8× `<path>` for elbow connectors between nodes
- 8–12× `<path>` for native editable icons such as cloud, shield, database, cube, and server glyphs
- 4–6× `<circle>` / `<ellipse>` for status LEDs, database disks, and ambient glows
- 12–18× subtle `<line>` elements for the dashboard grid
- Multiple `<text>` elements with explicit `width` attributes for node titles, details, section labels, and metrics
- 1× `<linearGradient>` for the dark canvas
- 1× `<linearGradient>` for node fills
- 1× `<radialGradient>` for background glow accents
- 1× `<filter id="softShadow">` applied to node rectangles and the main container
- 1× `<filter id="cyanGlow">` applied to active connector paths or status nodes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="60%" stop-color="#141625"/>
      <stop offset="100%" stop-color="#0B1020"/>
    </linearGradient>
    <linearGradient id="nodeGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#30384F"/>
      <stop offset="100%" stop-color="#252B3D"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#22D3EE"/>
      <stop offset="100%" stop-color="#6366F1"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="1080" cy="110" r="210" fill="url(#ambientGlow)" filter="url(#cyanGlow)" opacity="0.7"/>
  <circle cx="155" cy="620" r="175" fill="#6366F1" opacity="0.08" filter="url(#cyanGlow)"/>

  <g stroke="#334155" stroke-width="1" opacity="0.28">
    <line x1="80" y1="120" x2="1200" y2="120"/><line x1="80" y1="200" x2="1200" y2="200"/>
    <line x1="80" y1="280" x2="1200" y2="280"/><line x1="80" y1="360" x2="1200" y2="360"/>
    <line x1="80" y1="440" x2="1200" y2="440"/><line x1="80" y1="520" x2="1200" y2="520"/>
    <line x1="180" y1="90" x2="180" y2="635"/><line x1="340" y1="90" x2="340" y2="635"/>
    <line x1="500" y1="90" x2="500" y2="635"/><line x1="660" y1="90" x2="660" y2="635"/>
    <line x1="820" y1="90" x2="820" y2="635"/><line x1="980" y1="90" x2="980" y2="635"/>
    <line x1="1140" y1="90" x2="1140" y2="635"/>
  </g>

  <rect x="58" y="46" width="1164" height="610" rx="28" fill="#111827" opacity="0.78" stroke="#334155" stroke-width="1.5" filter="url(#softShadow)"/>
  <rect x="84" y="72" width="1112" height="54" rx="16" fill="#172033" stroke="#2A3650"/>
  <text x="108" y="106" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#F8FAFC">HQ Servers: 10.0.20.0/24</text>
  <text x="596" y="104" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Topology health · live snapshot</text>
  <rect x="920" y="86" width="92" height="24" rx="12" fill="#064E3B" stroke="#10B981"/>
  <circle cx="940" cy="98" r="4" fill="#34D399"/>
  <text x="952" y="103" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#D1FAE5">ONLINE</text>
  <rect x="1024" y="86" width="140" height="24" rx="12" fill="#1E293B" stroke="#475569"/>
  <text x="1042" y="103" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">Latency 12 ms</text>

  <g fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.72">
    <path d="M268 238 H382"/>
    <path d="M500 238 H614"/>
    <path d="M732 238 H846"/>
    <path d="M500 290 V384"/>
    <path d="M732 290 V384"/>
    <path d="M382 500 H306 V540 H382"/>
    <path d="M846 500 H922 V540 H846"/>
  </g>
  <g fill="none" stroke="url(#accentGrad)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" filter="url(#cyanGlow)">
    <path d="M964 238 H1034 V384"/>
    <path d="M614 500 H500 V540 H614"/>
  </g>

  <g font-family="Segoe UI, Microsoft YaHei">
    <g>
      <rect x="126" y="184" width="142" height="108" rx="18" fill="url(#nodeGrad)" stroke="#3B455F" filter="url(#softShadow)"/>
      <path d="M162 224 C164 210 176 203 189 207 C196 195 216 196 223 211 C235 211 243 219 243 230 C243 242 233 250 220 250 H166 C154 250 146 242 146 232 C146 224 153 218 162 224 Z" fill="#38BDF8" opacity="0.9"/>
      <text x="148" y="268" width="98" font-size="16" font-weight="700" fill="#FFFFFF">Cloud Edge</text>
      <text x="148" y="286" width="105" font-size="11" fill="#AAB4C5">443/tcp · WAF</text>
    </g>

    <g>
      <rect x="382" y="184" width="118" height="108" rx="18" fill="url(#nodeGrad)" stroke="#3B455F" filter="url(#softShadow)"/>
      <path d="M441 205 L472 219 V239 C472 259 458 272 441 278 C424 272 410 259 410 239 V219 Z" fill="#22C55E" opacity="0.9"/>
      <path d="M427 239 L437 249 L457 225" fill="none" stroke="#ECFDF5" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="405" y="268" width="78" font-size="16" font-weight="700" fill="#FFFFFF">Firewall</text>
      <text x="405" y="286" width="76" font-size="11" fill="#AAB4C5">10.0.20.1</text>
    </g>

    <g>
      <rect x="614" y="184" width="118" height="108" rx="18" fill="url(#nodeGrad)" stroke="#3B455F" filter="url(#softShadow)"/>
      <rect x="647" y="210" width="52" height="40" rx="7" fill="#60A5FA"/>
      <line x1="655" y1="222" x2="691" y2="222" stroke="#DBEAFE" stroke-width="3"/>
      <line x1="655" y1="235" x2="681" y2="235" stroke="#DBEAFE" stroke-width="3"/>
      <circle cx="694" cy="248" r="5" fill="#34D399"/>
      <text x="636" y="268" width="74" font-size="16" font-weight="700" fill="#FFFFFF">Proxmox</text>
      <text x="636" y="286" width="78" font-size="11" fill="#AAB4C5">8443/tcp</text>
    </g>

    <g>
      <rect x="846" y="184" width="118" height="108" rx="18" fill="url(#nodeGrad)" stroke="#3B455F" filter="url(#softShadow)"/>
      <path d="M905 207 L934 224 L934 258 L905 275 L876 258 L876 224 Z" fill="#818CF8"/>
      <path d="M876 224 L905 241 L934 224 M905 241 V275" fill="none" stroke="#E0E7FF" stroke-width="3"/>
      <text x="873" y="268" width="72" font-size="16" font-weight="700" fill="#FFFFFF">K8s API</text>
      <text x="873" y="286" width="78" font-size="11" fill="#AAB4C5">6443/tcp</text>
    </g>

    <g>
      <rect x="1034" y="384" width="118" height="116" rx="18" fill="url(#nodeGrad)" stroke="#22D3EE" filter="url(#softShadow)"/>
      <circle cx="1062" cy="414" r="6" fill="#22C55E"/>
      <text x="1080" y="419" width="52" font-size="12" font-weight="700" fill="#BAE6FD">ACTIVE</text>
      <path d="M1065 445 C1065 437 1121 437 1121 445 V474 C1121 482 1065 482 1065 474 Z" fill="#38BDF8" opacity="0.85"/>
      <ellipse cx="1093" cy="445" rx="28" ry="8" fill="#93C5FD"/>
      <text x="1064" y="490" width="70" font-size="16" font-weight="700" fill="#FFFFFF">Metrics</text>
    </g>

    <g>
      <rect x="614" y="384" width="118" height="116" rx="18" fill="url(#nodeGrad)" stroke="#3B455F" filter="url(#softShadow)"/>
      <path d="M649 424 H697 C703 424 708 429 708 435 V459 C708 465 703 470 697 470 H649 C643 470 638 465 638 459 V435 C638 429 643 424 649 424 Z" fill="#F59E0B"/>
      <circle cx="651" cy="442" r="4" fill="#FEF3C7"/><circle cx="651" cy="456" r="4" fill="#FEF3C7"/>
      <text x="636" y="490" width="78" font-size="16" font-weight="700" fill="#FFFFFF">GitLab</text>
      <text x="636" y="508" width="80" font-size="11" fill="#AAB4C5">443/tcp</text>
    </g>

    <g>
      <rect x="382" y="384" width="118" height="116" rx="18" fill="url(#nodeGrad)" stroke="#3B455F" filter="url(#softShadow)"/>
      <path d="M416 424 H466 V470 H416 Z" fill="#14B8A6"/>
      <path d="M424 434 H458 M424 446 H458 M424 458 H446" stroke="#CCFBF1" stroke-width="3" stroke-linecap="round"/>
      <text x="405" y="490" width="78" font-size="16" font-weight="700" fill="#FFFFFF">Jenkins</text>
      <text x="405" y="508" width="84" font-size="11" fill="#AAB4C5">8080/tcp</text>
    </g>

    <g>
      <rect x="846" y="384" width="118" height="116" rx="18" fill="url(#nodeGrad)" stroke="#3B455F" filter="url(#softShadow)"/>
      <ellipse cx="905" cy="426" rx="32" ry="10" fill="#C084FC"/>
      <path d="M873 426 V462 C873 476 937 476 937 462 V426" fill="#7C3AED"/>
      <ellipse cx="905" cy="462" rx="32" ry="10" fill="#A78BFA"/>
      <text x="873" y="490" width="76" font-size="16" font-weight="700" fill="#FFFFFF">TrueNAS</text>
      <text x="873" y="508" width="80" font-size="11" fill="#AAB4C5">NFS · SMB</text>
    </g>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` to repeat nodes; duplicate the node groups explicitly so PowerPoint keeps them editable.
- ❌ Do not apply filters to `<line>` connectors; use `<path>` connectors if a glow is needed.
- ❌ Do not use `marker-end` on `<path>` for arrowheads; create small editable arrowhead paths or omit arrows.
- ❌ Do not rely on tiny unreadable labels; every node should have a clear service name and one or two concise technical details.
- ❌ Do not place text without an explicit `width` attribute, or PowerPoint text wrapping may change.

## Composition notes
- Keep the topology inside one large rounded container, with a dashboard header band above it for subnet name, health state, and latency/context metadata.
- Use a strict grid for node placement, but vary node emphasis with accent strokes, LEDs, and glow only on active or critical services.
- Put connectors behind nodes and use muted blue-gray strokes so the structure reads clearly without competing with labels.
- Reserve 10–15% of the canvas as dark negative space around the container to preserve the premium dashboard feel.