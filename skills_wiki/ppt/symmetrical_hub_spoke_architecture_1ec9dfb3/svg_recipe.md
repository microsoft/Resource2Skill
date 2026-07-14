# SVG Recipe — Symmetrical Hub & Spoke Diagram

## Visual mechanism
A large central hub anchors the system while evenly spaced peripheral modules mirror each other on the left and right. Thin connector lines sit behind the shapes, while a dashed integration ring and subtle shadows make the hub feel like the governing core of a stable architecture.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<ellipse>` for a soft off-canvas background accent
- 1× `<path>` for an organic decorative corner shape
- 6× `<path>` for curved hub-to-node connector strokes
- 1× `<circle>` for the main hub body
- 1× `<circle>` for the dashed integration ring around the hub
- 1× `<circle>` for the inner hub highlight
- 6× `<circle>` for spoke node icon disks
- 6× `<rect>` for subtle node text-card backplates
- 12× `<path>` for simple editable line icons inside the node disks
- 1× `<filter id="softShadow">` applied to hub, nodes, and cards
- 1× `<filter id="hubGlow">` applied to the central hub
- 2× `<linearGradient>` for premium background and node fills
- 1× `<radialGradient>` for the hub fill
- Multiple `<text>` elements with explicit `width` attributes for title, hub label, node titles, and node descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FBF9"/>
      <stop offset="62%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EFF7F3"/>
    </linearGradient>
    <linearGradient id="emeraldGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#32D07D"/>
      <stop offset="100%" stop-color="#159A58"/>
    </linearGradient>
    <radialGradient id="hubGrad" cx="35%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#52697F"/>
      <stop offset="58%" stop-color="#2C3E50"/>
      <stop offset="100%" stop-color="#1E2A36"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="hubGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="105" cy="-85" rx="360" ry="260" fill="#DFF4E9"/>
  <path d="M1090,0 C1200,38 1262,126 1280,238 L1280,0 Z" fill="#EAF6F1"/>

  <text x="640" y="58" width="780" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#26333D">System Integration Architecture</text>
  <text x="640" y="90" width="680" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7D88">A balanced hub-and-spoke view for centralized platforms, APIs, and data flows</text>

  <!-- connector layer -->
  <path d="M548,352 C485,285 432,226 354,210" fill="none" stroke="#B9C8C2" stroke-width="2.2"/>
  <path d="M532,380 C468,380 420,360 354,360" fill="none" stroke="#B9C8C2" stroke-width="2.2"/>
  <path d="M548,408 C485,475 432,494 354,510" fill="none" stroke="#B9C8C2" stroke-width="2.2"/>
  <path d="M732,352 C795,285 848,226 926,210" fill="none" stroke="#B9C8C2" stroke-width="2.2"/>
  <path d="M748,380 C812,380 860,360 926,360" fill="none" stroke="#B9C8C2" stroke-width="2.2"/>
  <path d="M732,408 C795,475 848,494 926,510" fill="none" stroke="#B9C8C2" stroke-width="2.2"/>

  <!-- central hub -->
  <circle cx="640" cy="380" r="140" fill="none" stroke="#27AE60" stroke-width="3" stroke-dasharray="10 10" opacity="0.85"/>
  <circle cx="640" cy="380" r="100" fill="url(#hubGrad)" filter="url(#hubGlow)"/>
  <circle cx="640" cy="380" r="62" fill="none" stroke="#6FE0A2" stroke-width="2.5" opacity="0.75"/>
  <path d="M606,370 L640,346 L674,370 L674,410 L640,434 L606,410 Z" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round"/>
  <path d="M606,370 L640,394 L674,370 M640,394 L640,434" fill="none" stroke="#6FE0A2" stroke-width="4" stroke-linecap="round"/>
  <text x="640" y="545" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2C3E50">Unified Core Platform</text>
  <text x="640" y="570" width="270" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6D7A84">Security · Governance · Data Model</text>

  <!-- left cards and nodes -->
  <rect x="74" y="164" width="230" height="92" rx="18" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="330" cy="210" r="34" fill="url(#emeraldGrad)" filter="url(#softShadow)"/>
  <path d="M318,210 h24 M330,198 v24" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
  <path d="M318,198 h24 v24 h-24 Z" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>
  <text x="284" y="192" width="196" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26333D">Feature Implementation</text>
  <text x="284" y="218" width="196" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#6D7A84">Ship capabilities into the core ecosystem without breaking architecture.</text>

  <rect x="74" y="314" width="230" height="92" rx="18" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="330" cy="360" r="34" fill="url(#emeraldGrad)" filter="url(#softShadow)"/>
  <path d="M316,374 C326,348 340,348 344,326" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
  <path d="M314,374 C324,380 340,379 349,368" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="284" y="342" width="196" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26333D">Platform Customization</text>
  <text x="284" y="368" width="196" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#6D7A84">Configure workflows, rules, and screens for specific operating needs.</text>

  <rect x="74" y="464" width="230" height="92" rx="18" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="330" cy="510" r="34" fill="url(#emeraldGrad)" filter="url(#softShadow)"/>
  <path d="M314,522 h32 M318,510 h24 M322,498 h16" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
  <path d="M315,490 L345,490 L345,526 L315,526 Z" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>
  <text x="284" y="492" width="196" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26333D">Data Harmonization</text>
  <text x="284" y="518" width="196" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#6D7A84">Normalize domain data into a trusted single source of truth.</text>

  <!-- right cards and nodes -->
  <rect x="976" y="164" width="230" height="92" rx="18" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="950" cy="210" r="34" fill="url(#emeraldGrad)" filter="url(#softShadow)"/>
  <path d="M936,201 L950,193 L964,201 L950,209 Z" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>
  <path d="M936,201 v18 L950,227 L964,219 v-18" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>
  <text x="996" y="192" width="196" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26333D">Third-Party Integration</text>
  <text x="996" y="218" width="196" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#6D7A84">Connect external products through stable API and event contracts.</text>

  <rect x="976" y="314" width="230" height="92" rx="18" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="950" cy="360" r="34" fill="url(#emeraldGrad)" filter="url(#softShadow)"/>
  <path d="M938,341 h24 v38 h-24 Z" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>
  <path d="M944,371 h12 M944,348 h12" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="996" y="342" width="196" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26333D">Application Ecosystem</text>
  <text x="996" y="368" width="196" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#6D7A84">Coordinate apps, permissions, and services across the portfolio.</text>

  <rect x="976" y="464" width="230" height="92" rx="18" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="950" cy="510" r="34" fill="url(#emeraldGrad)" filter="url(#softShadow)"/>
  <path d="M932,517 C929,507 936,500 945,501 C949,492 963,494 966,504 C974,505 978,517 968,522 H936 C934,522 933,520 932,517 Z" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>
  <path d="M941,529 h18" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="996" y="492" width="196" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26333D">Hybrid Cloud Hosting</text>
  <text x="996" y="518" width="196" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#6D7A84">Run securely across public, private, and on-prem environments.</text>
</svg>
```

## Avoid in this skill
- ❌ Putting connector shadows on `<line>` elements; filters on lines are dropped, so keep connectors flat and place shadowed nodes above them.
- ❌ Using `marker-end` arrowheads for spoke connectors; hub-and-spoke stability works better with clean non-directional links, and marker behavior can fail.
- ❌ Mirroring text by rotating or skewing groups; use normal left/right text alignment instead.
- ❌ Overcrowding the center with long labels; the hub should remain a simple, dominant symbol.

## Composition notes
- Keep the hub in the central 40–45% of the slide width, leaving clear connector corridors between the hub and node columns.
- Place left and right node centers on identical y-values to preserve architectural symmetry.
- Draw connectors first, then cards, then node circles, then text so the diagram reads as layered and dimensional.
- Use one bright system color for all nodes and a darker slate tone for the hub to visually separate “core platform” from “modules.”