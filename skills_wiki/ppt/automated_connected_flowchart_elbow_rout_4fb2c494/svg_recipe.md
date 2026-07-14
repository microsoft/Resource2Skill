# SVG Recipe — Automated Connected Flowchart (Elbow-Routed Logic Diagram)

## Visual mechanism
A premium flowchart is built from consistently sized nodes placed on a grid, with orthogonal elbow routes that connect from explicit anchor points on each node. Each connector is composed of editable `<line>` segments plus a separate triangular arrowhead, making the routing visually robust and PowerPoint-safe.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× `<rect>` for translucent swimlane / routing zones
- 7× `<rect>` for rounded process nodes
- 1× `<path>` for the decision diamond
- 9× `<path>` for editable triangular arrowheads
- 2× decorative `<path>` blobs for soft keynote-style depth
- 15× `<line>` for orthogonal elbow connector segments
- 15× `<circle>` for subtle connection-site dots and elbow joints
- 16× `<text>` elements for title, subtitle, lane labels, node labels, branch labels, and loop annotation
- 4× `<linearGradient>` for background and node fills
- 1× `<radialGradient>` for decorative glow shapes
- 2× `<filter>` definitions: one drop shadow for nodes/panels and one soft blur glow for background accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="55%" stop-color="#EEF3FB"/>
      <stop offset="100%" stop-color="#E8EEF7"/>
    </linearGradient>
    <linearGradient id="blueNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4776D9"/>
      <stop offset="100%" stop-color="#254EAE"/>
    </linearGradient>
    <linearGradient id="tealNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#22B8A7"/>
      <stop offset="100%" stop-color="#0B7F76"/>
    </linearGradient>
    <linearGradient id="amberNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7B955"/>
      <stop offset="100%" stop-color="#D6811E"/>
    </linearGradient>
    <radialGradient id="softGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#79A7FF" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#79A7FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M945,42 C1090,4 1204,70 1224,178 C1246,296 1116,330 1004,286 C890,242 802,80 945,42 Z" fill="url(#softGlow)" filter="url(#glow)"/>
  <path d="M58,540 C132,452 250,478 304,548 C358,618 318,700 196,710 C84,720 -22,636 58,540 Z" fill="url(#softGlow)" filter="url(#glow)"/>

  <text x="64" y="50" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#172033">Customer Support Logic Flow</text>
  <text x="64" y="82" width="850" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#667085">Elbow-routed connectors snap visually to node anchors; branches remain readable as the diagram scales.</text>

  <rect x="64" y="318" width="432" height="150" rx="24" fill="#FFFFFF" opacity="0.62" stroke="#D8E1EF" filter="url(#shadow)"/>
  <rect x="452" y="74" width="376" height="594" rx="28" fill="#FFFFFF" opacity="0.72" stroke="#D8E1EF" filter="url(#shadow)"/>
  <rect x="784" y="318" width="432" height="350" rx="24" fill="#FFFFFF" opacity="0.62" stroke="#D8E1EF" filter="url(#shadow)"/>

  <text x="92" y="348" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7A8597">PRIORITY BRANCH</text>
  <text x="480" y="104" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7A8597">PRIMARY PROCESS SPINE</text>
  <text x="812" y="348" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7A8597">STANDARD / CLOSURE PATH</text>

  <line x1="640" y1="150" x2="640" y2="164" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="640" y1="226" x2="640" y2="244" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="554" y1="286" x2="347" y2="286" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="347" y1="286" x2="347" y2="340" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="726" y1="286" x2="933" y2="286" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="933" y1="286" x2="933" y2="340" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="347" y1="402" x2="347" y2="519" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="347" y1="519" x2="500" y2="519" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="933" y1="402" x2="933" y2="519" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="933" y1="519" x2="780" y2="519" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="640" y1="550" x2="640" y2="584" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="780" y1="615" x2="850" y2="615" stroke="#7A8597" stroke-width="3" stroke-linecap="round"/>
  <line x1="500" y1="615" x2="420" y2="615" stroke="#B8892B" stroke-width="2.5" stroke-dasharray="8 7" stroke-linecap="round"/>
  <line x1="420" y1="615" x2="420" y2="195" stroke="#B8892B" stroke-width="2.5" stroke-dasharray="8 7" stroke-linecap="round"/>
  <line x1="420" y1="195" x2="500" y2="195" stroke="#B8892B" stroke-width="2.5" stroke-dasharray="8 7" stroke-linecap="round"/>

  <path d="M640 164 L633 151 L647 151 Z" fill="#7A8597"/>
  <path d="M640 244 L633 231 L647 231 Z" fill="#7A8597"/>
  <path d="M347 340 L340 327 L354 327 Z" fill="#7A8597"/>
  <path d="M933 340 L926 327 L940 327 Z" fill="#7A8597"/>
  <path d="M500 519 L487 512 L487 526 Z" fill="#7A8597"/>
  <path d="M780 519 L793 512 L793 526 Z" fill="#7A8597"/>
  <path d="M640 584 L633 571 L647 571 Z" fill="#7A8597"/>
  <path d="M850 615 L837 608 L837 622 Z" fill="#7A8597"/>
  <path d="M500 195 L487 188 L487 202 Z" fill="#B8892B"/>

  <circle cx="347" cy="286" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="933" cy="286" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="347" cy="519" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="933" cy="519" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="640" cy="150" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="640" cy="226" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="640" cy="550" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="780" cy="615" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="500" cy="615" r="4" fill="#FFFFFF" stroke="#B8892B" stroke-width="2"/>
  <circle cx="420" cy="615" r="4" fill="#FFFFFF" stroke="#B8892B" stroke-width="2"/>
  <circle cx="420" cy="195" r="4" fill="#FFFFFF" stroke="#B8892B" stroke-width="2"/>
  <circle cx="500" cy="195" r="4" fill="#FFFFFF" stroke="#B8892B" stroke-width="2"/>
  <circle cx="500" cy="519" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="780" cy="519" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>
  <circle cx="850" cy="615" r="4" fill="#FFFFFF" stroke="#7A8597" stroke-width="2"/>

  <rect x="500" y="88" width="280" height="62" rx="16" fill="url(#blueNode)" stroke="#1E4293" filter="url(#shadow)"/>
  <rect x="500" y="164" width="280" height="62" rx="16" fill="url(#blueNode)" stroke="#1E4293" filter="url(#shadow)"/>
  <path d="M640 244 L726 286 L640 328 L554 286 Z" fill="#FFFFFF" stroke="#4776D9" stroke-width="3" filter="url(#shadow)"/>
  <rect x="207" y="340" width="280" height="62" rx="16" fill="url(#amberNode)" stroke="#B65E11" filter="url(#shadow)"/>
  <rect x="793" y="340" width="280" height="62" rx="16" fill="url(#tealNode)" stroke="#087168" filter="url(#shadow)"/>
  <rect x="500" y="488" width="280" height="62" rx="16" fill="url(#blueNode)" stroke="#1E4293" filter="url(#shadow)"/>
  <rect x="500" y="584" width="280" height="62" rx="16" fill="url(#blueNode)" stroke="#1E4293" filter="url(#shadow)"/>
  <rect x="850" y="584" width="280" height="62" rx="16" fill="#FFFFFF" stroke="#4776D9" stroke-width="2.5" filter="url(#shadow)"/>

  <text x="640" y="125" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Customer submits issue</text>
  <text x="640" y="201" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Classify request</text>
  <text x="640" y="283" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#254EAE"><tspan x="640" dy="0">SLA / severity</tspan><tspan x="640" dy="19">threshold?</tspan></text>
  <text x="347" y="377" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Escalate priority support</text>
  <text x="933" y="377" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Route to standard queue</text>
  <text x="640" y="525" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Assign accountable owner</text>
  <text x="640" y="621" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Resolve and notify</text>
  <text x="990" y="621" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#254EAE">Close ticket</text>

  <text x="430" y="277" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#B65E11">YES</text>
  <text x="850" y="277" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#087168">NO</text>
  <text x="438" y="410" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#B8892B">reopen loop if unresolved</text>
</svg>
```

## Avoid in this skill
- ❌ Do not draw elbow connectors as a single `<path>` with `marker-end`; arrowheads on paths can disappear in translation.
- ❌ Do not inherit `marker-end` from a parent `<g>`; if using line markers elsewhere, put them on each `<line>` directly.
- ❌ Do not use diagonal freehand connectors for process logic; the technique depends on horizontal/vertical routing from explicit anchor points.
- ❌ Do not apply filters to `<line>` connector segments; shadows/glows should be on nodes, panels, or decorative paths only.
- ❌ Do not omit `width` on any `<text>` element; PowerPoint text boxes need explicit width for clean rendering.

## Composition notes
- Keep the primary spine centered, with branch nodes placed symmetrically left and right so elbow routes remain short and readable.
- Use lane panels as subtle routing zones; they clarify branch ownership without competing with the nodes.
- Reserve the strongest fill color for main process nodes, then use amber/teal for decision outcomes and a white outlined node for terminal status.
- Show connector anchors with small dots only when the slide is explaining process structure; remove or reduce opacity for a cleaner executive version.