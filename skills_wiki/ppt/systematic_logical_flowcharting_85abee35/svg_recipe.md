# SVG Recipe — Systematic Logical Flowcharting

## Visual mechanism
A logical process is mapped onto a disciplined orthogonal routing system: pill-shaped endpoints, rounded process cards, diamond decisions, and side-branch exception paths. Color-coded borders and labeled elbows make the “happy path” readable at a glance while preserving clear resolution for every Yes/No condition.

## SVG primitives needed
- 1× `<rect>` for the full-slide background.
- 1× `<rect>` for a soft executive-style content panel.
- 6× `<rect>` for pill endpoints and rounded process nodes.
- 3× `<path>` for diamond decision nodes.
- 1× `<path>` for a parallelogram input/output node.
- 12× `<path>` for orthogonal elbow connector routes.
- 12× `<path>` for manually drawn triangular arrowheads at connector ends.
- 1× `<linearGradient>` for the premium off-white slide background.
- 1× `<filter id="softShadow">` applied to node shapes and the panel.
- 1× `<filter id="glowBlue">` applied to the primary start node for subtle emphasis.
- Multiple `<text>` elements with explicit `width` for title, node labels, branch labels, and legend text.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFF"/>
      <stop offset="58%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F2F6FA"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.08  0 0 0 0 0.12  0 0 0 0 0.18  0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowBlue" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.00  0 0 0 0 0.44  0 0 0 0 0.75  0 0 0 0.32 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- subtle blueprint grid -->
  <path d="M80 132 H1200 M80 192 H1200 M80 252 H1200 M80 312 H1200 M80 372 H1200 M80 432 H1200 M80 492 H1200 M80 552 H1200 M80 612 H1200" fill="none" stroke="#DDE7F0" stroke-width="1" stroke-dasharray="2 10"/>
  <path d="M160 110 V640 M280 110 V640 M400 110 V640 M520 110 V640 M640 110 V640 M760 110 V640 M880 110 V640 M1000 110 V640 M1120 110 V640" fill="none" stroke="#E8EEF5" stroke-width="1" stroke-dasharray="2 10"/>

  <text x="80" y="58" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#111827">Office Attendance Decision Flow</text>
  <text x="82" y="86" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">Systematic flowchart with endpoint, process, decision, and exception-routing logic.</text>

  <rect x="835" y="40" width="355" height="54" rx="18" fill="#FFFFFF" stroke="#E5EAF0" stroke-width="1.3" filter="url(#softShadow)"/>
  <rect x="858" y="58" width="18" height="18" rx="5" fill="#FFFFFF" stroke="#0070C0" stroke-width="3"/>
  <text x="884" y="72" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#475467">Endpoint</text>
  <rect x="956" y="58" width="18" height="18" rx="5" fill="#FFFFFF" stroke="#00A651" stroke-width="3"/>
  <text x="982" y="72" width="68" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#475467">Process</text>
  <path d="M1087 49 L1103 67 L1087 85 L1071 67 Z" fill="#FFFFFF" stroke="#C00000" stroke-width="3"/>
  <text x="1114" y="72" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#475467">Decision</text>

  <rect x="330" y="118" width="320" height="492" rx="30" fill="#FFFFFF" stroke="#EEF2F6" stroke-width="1" filter="url(#softShadow)"/>
  <text x="370" y="150" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#98A2B3">PRIMARY HAPPY PATH</text>

  <!-- connector routes behind nodes -->
  <path d="M490 203 V238" fill="none" stroke="#111827" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M484 238 L490 250 L496 238 Z" fill="#111827"/>
  <path d="M490 315 V350" fill="none" stroke="#111827" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M484 350 L490 362 L496 350 Z" fill="#111827"/>
  <path d="M490 426 V466" fill="none" stroke="#111827" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M484 466 L490 478 L496 466 Z" fill="#111827"/>
  <path d="M490 540 V572" fill="none" stroke="#111827" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M484 572 L490 584 L496 572 Z" fill="#111827"/>

  <path d="M630 282 H745 V206 H830" fill="none" stroke="#C00000" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M830 200 L842 206 L830 212 Z" fill="#C00000"/>
  <path d="M630 394 H745 V500 H830" fill="none" stroke="#C00000" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M830 494 L842 500 L830 506 Z" fill="#C00000"/>
  <path d="M350 394 H232 V500 H180" fill="none" stroke="#0070C0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M180 494 L168 500 L180 506 Z" fill="#0070C0"/>
  <path d="M930 240 V455 H628" fill="none" stroke="#7A8699" stroke-width="1.8" stroke-dasharray="7 7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M628 449 L616 455 L628 461 Z" fill="#7A8699"/>

  <!-- nodes -->
  <rect x="380" y="158" width="220" height="66" rx="33" fill="#FFFFFF" stroke="#0070C0" stroke-width="4" filter="url(#glowBlue)"/>
  <text x="490" y="184" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#101828">Employee arrives</text>
  <text x="490" y="204" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475467">Start checkpoint</text>

  <path d="M380 260 H600 L630 282 L600 304 H380 L350 282 Z" fill="#FFFFFF" stroke="#C00000" stroke-width="4" filter="url(#softShadow)"/>
  <text x="490" y="278" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">Is today a scheduled</text>
  <text x="490" y="298" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">office day?</text>

  <rect x="362" y="362" width="256" height="64" rx="14" fill="#FFFFFF" stroke="#00A651" stroke-width="4" filter="url(#softShadow)"/>
  <text x="490" y="389" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">Badge into building</text>
  <text x="490" y="409" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475467">Security system records entry</text>

  <path d="M380 478 H600 L630 508 L600 538 H380 L350 508 Z" fill="#FFFFFF" stroke="#C00000" stroke-width="4" filter="url(#softShadow)"/>
  <text x="490" y="503" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">Arrived before</text>
  <text x="490" y="523" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">9:30 AM?</text>

  <rect x="380" y="584" width="220" height="66" rx="33" fill="#FFFFFF" stroke="#0070C0" stroke-width="4" filter="url(#softShadow)"/>
  <text x="490" y="612" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#101828">Attendance valid</text>
  <text x="490" y="632" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475467">End state</text>

  <!-- side branches -->
  <rect x="842" y="174" width="176" height="66" rx="14" fill="#FFFFFF" stroke="#00A651" stroke-width="4" filter="url(#softShadow)"/>
  <text x="930" y="201" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">Work remotely</text>
  <text x="930" y="221" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475467">Submit status online</text>

  <path d="M850 470 H1010 L1030 500 L1010 530 H850 L830 500 Z" fill="#FFFFFF" stroke="#C00000" stroke-width="4" filter="url(#softShadow)"/>
  <text x="930" y="496" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">Exception</text>
  <text x="930" y="516" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">approved?</text>

  <path d="M126 470 L276 470 L252 530 L102 530 Z" fill="#FFFFFF" stroke="#0070C0" stroke-width="4" filter="url(#softShadow)"/>
  <text x="189" y="496" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">Create late</text>
  <text x="189" y="516" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#101828">arrival note</text>

  <!-- branch labels -->
  <text x="662" y="272" width="44" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#C00000">No</text>
  <text x="511" y="344" width="44" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#475467">Yes</text>
  <text x="676" y="386" width="44" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#C00000">No</text>
  <text x="302" y="386" width="44" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#0070C0">Yes</text>
  <text x="510" y="565" width="44" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#475467">Yes</text>
</svg>
```

## Avoid in this skill
- ❌ `marker-end` on `<path>` connectors; PPT translation may drop the arrowheads. Draw connector strokes and triangular arrowheads as separate editable `<path>` shapes.
- ❌ Curvy, diagonal, or freehand connector routing for logical flows; it weakens the “systematic” reading. Use orthogonal elbows.
- ❌ Low-contrast filled nodes that obscure shape semantics. Keep fills mostly white and use border color to encode meaning.
- ❌ Inconsistent node sizing and spacing; flowcharts depend on visual regularity for fast scanning.
- ❌ Text without explicit `width`; PowerPoint rendering may clip or reflow labels unpredictably.

## Composition notes
- Keep the main happy path on a strong vertical centerline, with decisions branching laterally to exception paths.
- Put connectors behind white-filled nodes so route lines feel continuous without crossing through readable text.
- Use color rhythm consistently: blue for endpoints / I/O, green for actions, red for decisions, gray or black for routing.
- Reserve the top-left for title and context; place a compact legend top-right to make the shape language self-documenting.