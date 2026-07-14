# SVG Recipe — Connected Circular Node Agenda

## Visual mechanism
A large circular hub anchors the left side of the slide, with small colored nodes placed along its outer arc. Thin dashed connectors lead from those nodes into stacked agenda cards on the right, making each agenda item feel like a structured branch from one central theme.

## SVG primitives needed
- 1× `<rect>` for the soft full-slide background
- 2× `<circle>` for the central hub ring and inner title disk
- 1× `<path>` for the dotted circular guide arc around the hub
- 5× `<circle>` for the colored radial nodes
- 5× `<line>` for dashed connectors from hub nodes to agenda cards
- 5× grouped `<rect>` card bodies for agenda item containers
- 5× colored `<rect>` icon blocks attached to the left edge of each card
- 5× small white `<path>` icon drawings inside the icon blocks
- Multiple `<text>` elements with explicit `width` for hub title, agenda titles, and descriptions
- 2× `<filter>` definitions for soft shadows/glows applied to circles and cards
- 2× `<linearGradient>` definitions for background depth and hub/card polish

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="60%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#eef3f6"/>
    </linearGradient>
    <linearGradient id="hubRing" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f4f5f6"/>
      <stop offset="100%" stop-color="#dde2e5"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="nodeGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <text x="86" y="86" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#1b1b1d" letter-spacing="1">Meeting Agenda</text>
  <text x="90" y="126" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#6f7b84">A connected hub-and-spoke overview for aligning priorities, decisions, and next actions.</text>

  <!-- central hub -->
  <circle cx="318" cy="390" r="166" fill="url(#hubRing)"/>
  <circle cx="318" cy="390" r="120" fill="#ffffff" filter="url(#softShadow)"/>
  <path d="M318 230 A160 160 0 0 1 318 550" fill="none" stroke="#6e747a" stroke-width="2" stroke-dasharray="4 8" opacity="0.75"/>
  <text x="216" y="372" width="204" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#111827">Agenda</text>
  <text x="216" y="412" width="204" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#111827">Template</text>
  <text x="238" y="450" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8a949d">Five focus areas</text>

  <!-- connectors behind cards -->
  <line x1="431" y1="277" x2="508" y2="236" stroke="#9aa3aa" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="464" y1="323" x2="508" y2="318" stroke="#9aa3aa" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="478" y1="390" x2="508" y2="400" stroke="#9aa3aa" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="464" y1="457" x2="508" y2="482" stroke="#9aa3aa" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="431" y1="503" x2="508" y2="564" stroke="#9aa3aa" stroke-width="2" stroke-dasharray="5 7"/>

  <!-- radial nodes -->
  <circle cx="431" cy="277" r="8" fill="#219ebc" stroke="#ffffff" stroke-width="3" filter="url(#nodeGlow)"/>
  <circle cx="464" cy="323" r="8" fill="#2a9d8f" stroke="#ffffff" stroke-width="3" filter="url(#nodeGlow)"/>
  <circle cx="478" cy="390" r="8" fill="#7209b7" stroke="#ffffff" stroke-width="3" filter="url(#nodeGlow)"/>
  <circle cx="464" cy="457" r="8" fill="#e76f51" stroke="#ffffff" stroke-width="3" filter="url(#nodeGlow)"/>
  <circle cx="431" cy="503" r="8" fill="#f4a261" stroke="#ffffff" stroke-width="3" filter="url(#nodeGlow)"/>

  <!-- card 1 -->
  <rect x="508" y="204" width="612" height="64" rx="13" fill="#ffffff" stroke="#219ebc" stroke-width="3" filter="url(#softShadow)"/>
  <rect x="508" y="204" width="72" height="64" rx="13" fill="#219ebc"/>
  <path d="M530 225 h28 v21 h-28 z M538 251 h12 M544 225 v-7 M535 234 l7 6 l12-13" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="600" y="232" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#164e63">Introduction &amp; Welcome</text>
  <text x="600" y="254" width="475" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#52616b">Set the context, align expectations, and confirm the purpose of the meeting.</text>

  <!-- card 2 -->
  <rect x="508" y="286" width="612" height="64" rx="13" fill="#ffffff" stroke="#2a9d8f" stroke-width="3" filter="url(#softShadow)"/>
  <rect x="508" y="286" width="72" height="64" rx="13" fill="#2a9d8f"/>
  <path d="M535 306 h22 v31 h-22 z M541 314 h10 M541 322 h10 M541 330 h10 M527 314 h4 M527 322 h4 M527 330 h4" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
  <text x="600" y="314" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#155e56">Project / Topic Overview</text>
  <text x="600" y="336" width="475" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#52616b">Review the background, status, scope, and important facts before discussion.</text>

  <!-- card 3 -->
  <rect x="508" y="368" width="612" height="64" rx="13" fill="#ffffff" stroke="#7209b7" stroke-width="3" filter="url(#softShadow)"/>
  <rect x="508" y="368" width="72" height="64" rx="13" fill="#7209b7"/>
  <path d="M535 395 a8 8 0 1 0 0.1 0 M557 395 a8 8 0 1 0 0.1 0 M546 385 a8 8 0 1 0 0.1 0 M528 414 c4-10 18-10 22 0 M550 414 c4-10 18-10 22 0" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
  <text x="600" y="396" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#4c1d95">Main Discussion</text>
  <text x="600" y="418" width="475" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#52616b">Work through key decisions, challenges, risks, and strategic tradeoffs.</text>

  <!-- card 4 -->
  <rect x="508" y="450" width="612" height="64" rx="13" fill="#ffffff" stroke="#e76f51" stroke-width="3" filter="url(#softShadow)"/>
  <rect x="508" y="450" width="72" height="64" rx="13" fill="#e76f51"/>
  <path d="M535 468 h20 v30 h-20 z M545 468 v-8 l12 8 M541 485 h8 M541 493 h8 M558 491 l6 6 l11-15" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="600" y="478" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#9a3412">Action Plan &amp; Implementation</text>
  <text x="600" y="500" width="475" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#52616b">Translate decisions into owners, milestones, and immediate next steps.</text>

  <!-- card 5 -->
  <rect x="508" y="532" width="612" height="64" rx="13" fill="#ffffff" stroke="#f4a261" stroke-width="3" filter="url(#softShadow)"/>
  <rect x="508" y="532" width="72" height="64" rx="13" fill="#f4a261"/>
  <path d="M534 551 a13 13 0 1 0 0 26 h4 v8 l9-8 h7 M534 560 q6-10 13 0 q-2 5-7 9 M561 557 h10 M561 568 h10 M561 579 h6" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="600" y="560" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#b45309">Q&amp;A and Closing Remarks</text>
  <text x="600" y="582" width="475" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#52616b">Resolve open questions, capture feedback, and confirm follow-up actions.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` for repeated icons; duplicate the small icon paths directly so PowerPoint keeps them editable.
- ❌ Do not apply `filter` to connector `<line>` elements; shadows on lines are dropped. Keep connector lines clean and flat.
- ❌ Do not use `marker-end` on paths for arrowheads; this agenda style works better with plain dashed connectors and circular nodes.
- ❌ Do not rely on `clip-path` for card shapes; use rounded `<rect>` elements directly so each card remains editable.
- ❌ Avoid overcrowding the hub with too many nodes. More than 6–7 spokes makes the radial geometry feel noisy.

## Composition notes
- Keep the hub in the left 35–40% of the slide and reserve the right half for the vertical agenda stack.
- The connector zone between hub and cards should stay mostly empty; this negative space is what makes the branching logic readable.
- Use one accent color per agenda item and repeat it consistently across node, card stroke, and icon block.
- Align card left edges perfectly; let the radial node positions vary while the agenda text remains calm and structured.