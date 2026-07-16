# SVG Recipe — Horizontal Task Progress

## Visual mechanism
A three-row executive progress board: task descriptions sit in a left information column, while the right side uses long horizontal rails, colored completion fills, milestone dots, and percent pills to make status scannable at a glance. The premium feel comes from layered cards, soft gradients, subtle shadows, and a faint technical grid backdrop.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<path>` for a soft decorative gradient blob behind the content
- 1× `<rect>` for the main rounded dashboard panel
- 3× `<rect>` for individual task row cards
- 3× `<rect>` for thin accent strips at the left edge of each row card
- 3× `<rect>` for task number badges
- 3× `<rect>` for progress rail backgrounds
- 3× `<rect>` for completed progress fills
- 3× `<rect>` for percentage/status pills
- 12× `<circle>` for milestone dots along the progress bars
- 3× `<circle>` for active endpoint dots on each completed progress fill
- 6× `<line>` for subtle horizontal and vertical guide rules
- Multiple `<text>` elements with explicit `width` attributes for title, task labels, metadata, and percentages
- 3× `<linearGradient>` for background, panel/card fills, and progress fills
- 1× `<radialGradient>` for the ambient decorative glow
- 2× `<filter>` definitions for soft card shadow and endpoint glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#EEF3F8"/>
      <stop offset="100%" stop-color="#E7EDF5"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="70" x2="0" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F6F8FB"/>
    </linearGradient>
    <linearGradient id="blueFill" x1="620" y1="0" x2="1080" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2F80ED"/>
      <stop offset="100%" stop-color="#56CCF2"/>
    </linearGradient>
    <linearGradient id="greenFill" x1="620" y1="0" x2="1080" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#8BE28B"/>
    </linearGradient>
    <linearGradient id="amberFill" x1="620" y1="0" x2="1080" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#FFD166"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#7DD3FC" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#7DD3FC" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-25%" width="140%" height="160%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="dotGlow" x="-90%" y="-90%" width="280%" height="280%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M885,28 C1038,-26 1196,54 1240,172 C1283,289 1198,402 1049,377 C898,353 786,256 798,151 C804,94 831,48 885,28 Z" fill="url(#ambientGlow)"/>
  <path d="M42,598 C156,538 258,587 319,646 C246,710 118,736 24,690 C-3,664 7,621 42,598 Z" fill="#DCEAFE" opacity="0.55"/>

  <text x="88" y="78" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="700" fill="#102033">Program Execution Progress</text>
  <text x="90" y="114" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#64748B">Three critical workstreams tracked by completion, next gate, and delivery confidence</text>

  <rect x="80" y="150" width="1120" height="500" rx="34" fill="url(#panelGrad)" filter="url(#cardShadow)"/>
  <line x1="560" y1="198" x2="560" y2="606" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="620" y1="210" x2="1100" y2="210" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="4 8"/>
  <line x1="620" y1="606" x2="1100" y2="606" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="4 8"/>

  <text x="104" y="190" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#94A3B8" letter-spacing="1.2">TASK</text>
  <text x="620" y="190" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#94A3B8" letter-spacing="1.2">PROGRESS</text>
  <text x="1005" y="190" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#94A3B8" letter-spacing="1.2">STATUS</text>

  <rect x="104" y="222" width="1052" height="112" rx="24" fill="#FFFFFF" stroke="#E8EEF6" stroke-width="1"/>
  <rect x="104" y="222" width="8" height="112" rx="4" fill="#2F80ED"/>
  <rect x="132" y="252" width="44" height="44" rx="14" fill="#EAF3FF"/>
  <text x="144" y="282" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2F80ED">01</text>
  <text x="196" y="258" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#0F172A">Discovery & Alignment</text>
  <text x="196" y="287" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Stakeholder interviews, scope lock, and risk register validation</text>
  <text x="196" y="313" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Owner: Strategy PMO · Gate: Week 2</text>
  <rect x="620" y="268" width="410" height="16" rx="8" fill="#E8EEF6"/>
  <rect x="620" y="268" width="328" height="16" rx="8" fill="url(#blueFill)"/>
  <circle cx="620" cy="276" r="6" fill="#2F80ED"/>
  <circle cx="757" cy="276" r="6" fill="#2F80ED"/>
  <circle cx="893" cy="276" r="6" fill="#2F80ED"/>
  <circle cx="1030" cy="276" r="6" fill="#CBD5E1"/>
  <circle cx="948" cy="276" r="12" fill="#56CCF2" opacity="0.35" filter="url(#dotGlow)"/>
  <circle cx="948" cy="276" r="7" fill="#FFFFFF" stroke="#2F80ED" stroke-width="4"/>
  <rect x="1050" y="252" width="70" height="40" rx="20" fill="#EAF3FF"/>
  <text x="1066" y="278" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#2F80ED">80%</text>

  <rect x="104" y="360" width="1052" height="112" rx="24" fill="#FFFFFF" stroke="#E8EEF6" stroke-width="1"/>
  <rect x="104" y="360" width="8" height="112" rx="4" fill="#10B981"/>
  <rect x="132" y="390" width="44" height="44" rx="14" fill="#EAFBF3"/>
  <text x="144" y="420" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#10B981">02</text>
  <text x="196" y="396" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#0F172A">Platform Buildout</text>
  <text x="196" y="425" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Core integrations, security controls, and executive dashboard shell</text>
  <text x="196" y="451" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Owner: Engineering · Gate: Week 5</text>
  <rect x="620" y="406" width="410" height="16" rx="8" fill="#E8EEF6"/>
  <rect x="620" y="406" width="230" height="16" rx="8" fill="url(#greenFill)"/>
  <circle cx="620" cy="414" r="6" fill="#10B981"/>
  <circle cx="757" cy="414" r="6" fill="#10B981"/>
  <circle cx="893" cy="414" r="6" fill="#CBD5E1"/>
  <circle cx="1030" cy="414" r="6" fill="#CBD5E1"/>
  <circle cx="850" cy="414" r="12" fill="#8BE28B" opacity="0.35" filter="url(#dotGlow)"/>
  <circle cx="850" cy="414" r="7" fill="#FFFFFF" stroke="#10B981" stroke-width="4"/>
  <rect x="1050" y="390" width="70" height="40" rx="20" fill="#EAFBF3"/>
  <text x="1066" y="416" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#10B981">56%</text>

  <rect x="104" y="498" width="1052" height="112" rx="24" fill="#FFFFFF" stroke="#E8EEF6" stroke-width="1"/>
  <rect x="104" y="498" width="8" height="112" rx="4" fill="#F59E0B"/>
  <rect x="132" y="528" width="44" height="44" rx="14" fill="#FFF6E6"/>
  <text x="144" y="558" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F59E0B">03</text>
  <text x="196" y="534" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#0F172A">Launch Readiness</text>
  <text x="196" y="563" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Training, go-live playbook, support model, and adoption checklist</text>
  <text x="196" y="589" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Owner: Operations · Gate: Week 8</text>
  <rect x="620" y="544" width="410" height="16" rx="8" fill="#E8EEF6"/>
  <rect x="620" y="544" width="119" height="16" rx="8" fill="url(#amberFill)"/>
  <circle cx="620" cy="552" r="6" fill="#F59E0B"/>
  <circle cx="757" cy="552" r="6" fill="#CBD5E1"/>
  <circle cx="893" cy="552" r="6" fill="#CBD5E1"/>
  <circle cx="1030" cy="552" r="6" fill="#CBD5E1"/>
  <circle cx="739" cy="552" r="12" fill="#FFD166" opacity="0.35" filter="url(#dotGlow)"/>
  <circle cx="739" cy="552" r="7" fill="#FFFFFF" stroke="#F59E0B" stroke-width="4"/>
  <rect x="1050" y="528" width="70" height="40" rx="20" fill="#FFF6E6"/>
  <text x="1066" y="554" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#F59E0B">29%</text>

  <text x="960" y="638" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Updated: Monday 09:00</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` on `<path>` for timeline arrows; if directional indicators are needed, use plain `<line>` plus small triangle `<path>` shapes.
- ❌ Do not apply `filter` to `<line>` guide rules; shadows and glows should be applied only to rectangles, circles, paths, or text.
- ❌ Do not use `clip-path` on task cards or groups; clipping is only reliable for `<image>` elements.
- ❌ Avoid building the progress bars from many tiny segments unless the design specifically needs a segmented status meter; a rail plus fill is cleaner and easier to edit.

## Composition notes
- Keep the left 40–45% of the panel for task names, owners, and gate metadata; reserve the right 50–55% for progress rails and percentage pills.
- Use three row cards with generous vertical spacing so each task reads as a distinct milestone, not a dense table.
- Color rhythm should encode status: blue for aligned/on-plan, green for active delivery, amber for early-stage or watch item.
- The strongest visual focus should be the active endpoint dots and percentage pills; keep background grid lines subtle and low-contrast.