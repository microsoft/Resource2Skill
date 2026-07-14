# SVG Recipe — Modular UI-Style Agenda Decks (Dark/Light Modes)

## Visual mechanism
Replace a conventional agenda list with a modular app-interface layout: dark mode uses vertical cards anchored to a black base rail, while light mode uses a circular hub connected to stacked horizontal ribbons. The visual hierarchy comes from strict grid spacing, glowing accent colors, rounded containers, dashed connector lines, and compact UI-style typography.

## SVG primitives needed
- 12× `<rect>` for full-slide backgrounds, dark-mode cards, bottom anchor rail, accent bars, and light-mode agenda ribbons
- 8× `<circle>` for hub rings, numbered nodes, and ribbon color bullets
- 10× `<path>` for decorative blobs and small editable UI icons inside agenda modules
- 5× `<line>` for dashed connector spokes from the hub to agenda ribbons
- 24× `<text>` for titles, section labels, item numbers, agenda headlines, and descriptions
- 2× `<linearGradient>` for premium dark-card and light-background depth
- 1× `<radialGradient>` for the soft circular hub glow
- 2× `<filter>` definitions: one soft shadow for cards/hub/ribbons and one neon glow for active accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Microsoft YaHei, sans-serif">
  <defs>
    <linearGradient id="darkBg" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="1" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="130" x2="0" y2="550">
      <stop offset="0" stop-color="#263244"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="lightBg" x1="705" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F3F4F6"/>
    </linearGradient>
    <radialGradient id="hubGlow" cx="50%" cy="45%" r="55%">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.68" stop-color="#F8FAFC"/>
      <stop offset="1" stop-color="#E5E7EB"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="greenGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="704" height="720" fill="url(#darkBg)"/>
  <rect x="704" y="0" width="576" height="720" fill="url(#lightBg)"/>
  <path d="M1028 37 C1125 4 1217 51 1253 135 C1283 205 1257 285 1197 320 C1131 359 1046 326 1009 260 C968 187 945 72 1028 37 Z" fill="#EEF2FF"/>

  <text x="54" y="66" width="540" font-size="34" font-weight="700" fill="#FFFFFF">Executive Agenda</text>
  <text x="56" y="98" width="510" font-size="15" fill="#9CA3AF">Dark-mode vertical card system with active-state progress rail</text>
  <rect x="0" y="548" width="704" height="172" fill="#000000" opacity="0.92"/>
  <rect x="54" y="594" width="570" height="10" rx="5" fill="#1F2937"/>
  <rect x="54" y="594" width="142" height="10" rx="5" fill="#4ADE80" filter="url(#greenGlow)"/>

  <rect x="54" y="146" width="132" height="438" rx="24" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <circle cx="120" cy="202" r="27" fill="#4ADE80" filter="url(#greenGlow)"/>
  <text x="108" y="212" width="24" font-size="22" font-weight="800" fill="#052E16">1</text>
  <path d="M96 266 L144 266 M96 286 L132 286 M96 306 L152 306" stroke="#4ADE80" stroke-width="6" stroke-linecap="round" fill="none"/>
  <text x="78" y="365" width="84" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">Opening</text>
  <text x="72" y="397" width="96" font-size="12" fill="#9CA3AF" text-anchor="middle">Context, goals, and decision frame.</text>

  <rect x="210" y="146" width="132" height="438" rx="24" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <circle cx="276" cy="202" r="27" fill="#374151"/>
  <text x="264" y="212" width="24" font-size="22" font-weight="800" fill="#D1D5DB">2</text>
  <path d="M256 262 C256 252 296 252 296 262 L296 306 C296 316 256 316 256 306 Z M266 276 L286 276 M266 292 L286 292" stroke="#60A5FA" stroke-width="5" fill="none" stroke-linecap="round"/>
  <text x="234" y="365" width="84" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">Metrics</text>
  <text x="228" y="397" width="96" font-size="12" fill="#9CA3AF" text-anchor="middle">Review leading indicators and trend signals.</text>

  <rect x="366" y="146" width="132" height="438" rx="24" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <circle cx="432" cy="202" r="27" fill="#374151"/>
  <text x="420" y="212" width="24" font-size="22" font-weight="800" fill="#D1D5DB">3</text>
  <path d="M410 306 L426 264 L456 264 L440 306 Z M420 286 L448 286" stroke="#A78BFA" stroke-width="5" fill="none" stroke-linejoin="round"/>
  <text x="390" y="365" width="84" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">Strategy</text>
  <text x="384" y="397" width="96" font-size="12" fill="#9CA3AF" text-anchor="middle">Priorities, choices, and execution bets.</text>

  <rect x="522" y="146" width="132" height="438" rx="24" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <circle cx="588" cy="202" r="27" fill="#374151"/>
  <text x="576" y="212" width="24" font-size="22" font-weight="800" fill="#D1D5DB">4</text>
  <path d="M566 284 L584 302 L616 264 M566 318 L616 318" stroke="#F97316" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="546" y="365" width="84" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">Actions</text>
  <text x="540" y="397" width="96" font-size="12" fill="#9CA3AF" text-anchor="middle">Owners, dates, and next-step commitments.</text>

  <text x="752" y="68" width="420" font-size="32" font-weight="800" fill="#111827">Light Mode Agenda Hub</text>
  <text x="754" y="98" width="420" font-size="15" fill="#6B7280">Horizontal ribbons connected by a central navigation node</text>
  <circle cx="846" cy="360" r="138" fill="#F3F4F6"/>
  <circle cx="846" cy="360" r="104" fill="url(#hubGlow)" filter="url(#softShadow)"/>
  <circle cx="846" cy="360" r="48" fill="#111827"/>
  <text x="812" y="352" width="68" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">AGENDA</text>
  <text x="820" y="376" width="52" font-size="26" font-weight="800" fill="#4ADE80" text-anchor="middle">05</text>

  <line x1="906" y1="290" x2="962" y2="154" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="7 8"/>
  <line x1="940" y1="326" x2="962" y2="254" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="7 8"/>
  <line x1="948" y1="360" x2="962" y2="354" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="7 8"/>
  <line x1="940" y1="394" x2="962" y2="454" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="7 8"/>
  <line x1="906" y1="430" x2="962" y2="554" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="7 8"/>

  <rect x="962" y="120" width="270" height="68" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="992" cy="154" r="18" fill="#3B82F6"/>
  <text x="1022" y="148" width="180" font-size="16" font-weight="700" fill="#111827">Market pulse</text>
  <text x="1022" y="171" width="190" font-size="12" fill="#6B7280">Signals and customer shifts</text>

  <rect x="962" y="220" width="270" height="68" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="992" cy="254" r="18" fill="#14B8A6"/>
  <text x="1022" y="248" width="180" font-size="16" font-weight="700" fill="#111827">Product roadmap</text>
  <text x="1022" y="271" width="190" font-size="12" fill="#6B7280">Quarterly build priorities</text>

  <rect x="962" y="320" width="270" height="68" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="992" cy="354" r="18" fill="#8B5CF6"/>
  <text x="1022" y="348" width="180" font-size="16" font-weight="700" fill="#111827">Operating model</text>
  <text x="1022" y="371" width="190" font-size="12" fill="#6B7280">Roles, rituals, governance</text>

  <rect x="962" y="420" width="270" height="68" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="992" cy="454" r="18" fill="#F97316"/>
  <text x="1022" y="448" width="180" font-size="16" font-weight="700" fill="#111827">Investment asks</text>
  <text x="1022" y="471" width="190" font-size="12" fill="#6B7280">Funding and trade-off calls</text>

  <rect x="962" y="520" width="270" height="68" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="992" cy="554" r="18" fill="#EAB308"/>
  <text x="1022" y="548" width="180" font-size="16" font-weight="700" fill="#111827">Decision log</text>
  <text x="1022" y="571" width="190" font-size="12" fill="#6B7280">Commitments and owners</text>
</svg>
```

## Avoid in this skill
- ❌ Building the agenda as one flattened screenshot; the value is that every card, ribbon, node, and label remains editable in PowerPoint.
- ❌ Using `<marker-end>` for connector arrows; use plain `<line>` spokes or draw arrowheads manually with small paths if needed.
- ❌ Applying shadows or glow filters to `<line>` elements; filters on lines are dropped, so keep connector lines clean and dashed.
- ❌ Overloading cards with paragraph text; this technique works because each module feels like an app tile, not a document block.
- ❌ Using masks or clip paths on non-image elements for card reveals; rely on native rounded rectangles, circles, paths, and gradients instead.

## Composition notes
- Keep the dark-mode version grid-driven: four equal vertical cards, generous gutters, and a heavy bottom anchor rail that makes the layout feel stable.
- In light mode, reserve the left third for the hub and the right two-thirds for stacked ribbons; dashed spokes should imply flow without dominating.
- Use one active accent in dark mode, typically neon green, and reserve multi-color accents for light-mode ribbon categories.
- Maintain strong negative space around titles and module edges so the agenda feels like a premium UI screen rather than a dense task list.