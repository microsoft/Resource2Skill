# SVG Recipe — Semantic Logic Flowchart

## Visual mechanism
A polished flowchart uses semantic shape language: rounded rectangles for start/end, diamonds for decisions, and standard rounded action cards for work steps. Color encodes meaning while orthogonal arrow connectors and small inline labels make the decision logic readable at a glance.

## SVG primitives needed
- 1× `<rect>` for the full-slide pale background
- 1× `<path>` for a soft decorative background blob that adds executive-slide polish without interfering with readability
- 5× `<rect>` for process, start, and terminal nodes
- 2× `<path>` for diamond decision nodes
- 10× `<line>` for orthogonal connector segments; apply `marker-end` directly only on the final segment of each directed connector
- 6× small `<rect>` label pills for YES/NO/RETRY/ESCALATE connector labels
- 1× `<marker>` definition for arrowheads used by connector lines
- 1× `<filter id="nodeShadow">` applied to node rectangles and diamond paths
- 1× `<filter id="labelShadow">` applied to connector label pills
- Multiple `<text>` elements with explicit `width` attributes for title, node labels, connector labels, and legend text
- 4× small legend shapes showing the semantic vocabulary

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF4FA"/>
    </linearGradient>
    <linearGradient id="blueNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#1E3A8A"/>
    </linearGradient>
    <linearGradient id="orangeNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FDBA74"/>
      <stop offset="100%" stop-color="#F97316"/>
    </linearGradient>
    <linearGradient id="cyanNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
    <filter id="nodeShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="labelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="2"/>
      <feGaussianBlur stdDeviation="2"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
      <path d="M2,2 L10,6 L2,10 Z" fill="#94A3B8"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M910,28 C1050,-18 1218,22 1262,142 C1310,272 1190,360 1228,500 C1258,610 1166,694 1042,676 C900,654 884,536 928,424 C974,306 790,168 910,28 Z" fill="#DBEAFE" opacity="0.55"/>

  <text x="58" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#1E3A8A">Troubleshooting Flowchart</text>
  <text x="60" y="88" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Semantic logic map: decisions are amber, actions are cyan, terminal outcomes are green or red.</text>
  <line x1="58" y1="108" x2="640" y2="108" stroke="#CBD5E1" stroke-width="2"/>

  <rect x="330" y="126" width="300" height="64" rx="22" fill="url(#blueNode)" stroke="#FFFFFF" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="480" y="151" width="270" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">User reports</text>
  <text x="480" y="171" width="270" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">login failure</text>

  <path d="M480,220 L618,286 L480,352 L342,286 Z" fill="url(#orangeNode)" stroke="#FFFFFF" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="480" y="281" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Password</text>
  <text x="480" y="301" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">recently changed?</text>

  <rect x="340" y="392" width="280" height="68" rx="14" fill="url(#cyanNode)" stroke="#FFFFFF" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="480" y="419" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Send reset link</text>
  <text x="480" y="439" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">and verify MFA</text>

  <rect x="790" y="392" width="280" height="68" rx="14" fill="url(#cyanNode)" stroke="#FFFFFF" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="930" y="419" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Check account lock</text>
  <text x="930" y="439" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">and device policy</text>

  <path d="M480,496 L618,556 L480,616 L342,556 Z" fill="url(#orangeNode)" stroke="#FFFFFF" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="480" y="551" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Can user</text>
  <text x="480" y="571" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">sign in now?</text>

  <rect x="176" y="626" width="260" height="58" rx="18" fill="#22C55E" stroke="#FFFFFF" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="306" y="661" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Resolved — close ticket</text>

  <rect x="790" y="528" width="280" height="68" rx="18" fill="#EF4444" stroke="#FFFFFF" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="930" y="555" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Escalate to IAM</text>
  <text x="930" y="575" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">engineering queue</text>

  <line x1="480" y1="190" x2="480" y2="220" stroke="#94A3B8" stroke-width="3" marker-end="url(#arrow)"/>
  <line x1="480" y1="352" x2="480" y2="392" stroke="#94A3B8" stroke-width="3" marker-end="url(#arrow)"/>
  <line x1="618" y1="286" x2="720" y2="286" stroke="#94A3B8" stroke-width="3"/>
  <line x1="720" y1="286" x2="720" y2="426" stroke="#94A3B8" stroke-width="3"/>
  <line x1="720" y1="426" x2="790" y2="426" stroke="#94A3B8" stroke-width="3" marker-end="url(#arrow)"/>
  <line x1="480" y1="460" x2="480" y2="496" stroke="#94A3B8" stroke-width="3" marker-end="url(#arrow)"/>
  <line x1="342" y1="556" x2="306" y2="556" stroke="#94A3B8" stroke-width="3"/>
  <line x1="306" y1="556" x2="306" y2="626" stroke="#94A3B8" stroke-width="3" marker-end="url(#arrow)"/>
  <line x1="618" y1="556" x2="790" y2="556" stroke="#94A3B8" stroke-width="3" marker-end="url(#arrow)"/>
  <line x1="930" y1="460" x2="930" y2="528" stroke="#94A3B8" stroke-width="3" marker-end="url(#arrow)"/>

  <rect x="505" y="365" width="56" height="24" rx="12" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#labelShadow)"/>
  <text x="533" y="382" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155">YES</text>
  <rect x="645" y="266" width="50" height="24" rx="12" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#labelShadow)"/>
  <text x="670" y="283" width="44" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155">NO</text>
  <rect x="505" y="468" width="70" height="24" rx="12" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#labelShadow)"/>
  <text x="540" y="485" width="64" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155">RETRY</text>
  <rect x="250" y="585" width="56" height="24" rx="12" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#labelShadow)"/>
  <text x="278" y="602" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155">YES</text>
  <rect x="670" y="536" width="50" height="24" rx="12" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#labelShadow)"/>
  <text x="695" y="553" width="44" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155">NO</text>
  <rect x="943" y="487" width="96" height="24" rx="12" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#labelShadow)"/>
  <text x="991" y="504" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#334155">UNRESOLVED</text>

  <rect x="930" y="112" width="250" height="172" rx="22" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#labelShadow)"/>
  <text x="955" y="143" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#1E293B">Shape semantics</text>
  <rect x="956" y="162" width="38" height="22" rx="10" fill="#1E3A8A"/>
  <text x="1008" y="178" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Start / intake</text>
  <path d="M975,198 L998,211 L975,224 L952,211 Z" fill="#F97316"/>
  <text x="1008" y="216" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Decision point</text>
  <rect x="956" y="236" width="38" height="22" rx="6" fill="#0284C7"/>
  <text x="1008" y="252" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Action step</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<path marker-end="...">` for arrows; marker arrowheads on paths may disappear. Use `<line>` segments and put `marker-end` directly on the final `<line>`.
- ❌ Do not rely on auto-routed connectors or SmartArt-like layout; the premium look comes from explicit coordinates, fixed grid spacing, and clean orthogonal routing.
- ❌ Do not apply filters to connector `<line>` elements; shadows should be reserved for nodes and label pills.
- ❌ Do not use clip paths, masks, or patterns for node styling; simple gradients, strokes, and shadows translate more reliably into editable PowerPoint shapes.
- ❌ Do not mix too many colors casually; keep colors semantic: blue=start, amber=decision, cyan=action, green=success, red=exception.

## Composition notes
- Keep the primary workflow on a clear vertical trunk, then route exceptions to the right so the audience can distinguish “happy path” from “branch logic.”
- Use generous vertical gaps between nodes; the connectors and labels need breathing room to avoid a messy whiteboard feel.
- Place connector labels in small white pills that interrupt the line visually, making YES/NO decisions instantly scannable.
- Use a pale background and soft shadows so colorful nodes feel like elevated interface cards rather than flat diagram boxes.