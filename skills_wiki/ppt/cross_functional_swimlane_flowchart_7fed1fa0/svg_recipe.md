# SVG Recipe — Cross-Functional Swimlane Flowchart

## Visual mechanism
Divide the canvas into tall, pastel vertical swimlanes that represent accountable teams, then place white flowchart nodes inside the responsible lane. Clean right-angled connector lines cross lane boundaries to make hand-offs visually explicit.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 3× large `<rect>` for pastel swimlane bodies
- 3× `<rect>` for darker lane header bands
- 7× white `<rect>` for rounded start/end and process nodes
- 2× `<path>` for decision diamonds
- 18× `<line>` for elbow connector segments and arrow-ended final segments
- 1× `<marker>` in `<defs>` for line arrowheads
- 1× `<filter id="nodeShadow">` applied to flowchart nodes
- 1× `<linearGradient>` for the subtle page background
- Multiple `<text>` elements with explicit `width` for title, lane labels, node labels, and callouts

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF2F7"/>
    </linearGradient>

    <filter id="nodeShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="6" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth">
      <path d="M 0 0 L 10 5 L 0 10 Z" fill="#4B5563"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#pageBg)"/>

  <text x="80" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1F2937">
    Expense Reimbursement Process
  </text>
  <text x="84" y="88" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#64748B">
    Cross-functional swimlane view showing accountability and hand-offs
  </text>

  <rect x="92" y="120" width="1096" height="530" rx="22" fill="#FFFFFF" opacity="0.78"/>
  <rect x="100" y="128" width="360" height="512" rx="16" fill="#F2F7FC"/>
  <rect x="460" y="128" width="360" height="512" fill="#FEF8F2"/>
  <rect x="820" y="128" width="360" height="512" rx="16" fill="#F8F3FC"/>

  <rect x="100" y="128" width="360" height="58" rx="16" fill="#BFD7EB"/>
  <rect x="460" y="128" width="360" height="58" fill="#F5D7B9"/>
  <rect x="820" y="128" width="360" height="58" rx="16" fill="#E1CDF0"/>

  <text x="280" y="164" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#244761">Applicant</text>
  <text x="640" y="164" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#714218">Manager</text>
  <text x="1000" y="164" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#57366D">Finance</text>

  <line x1="460" y1="128" x2="460" y2="640" stroke="#D6DEE8" stroke-width="1.5"/>
  <line x1="820" y1="128" x2="820" y2="640" stroke="#D6DEE8" stroke-width="1.5"/>

  <rect x="190" y="222" width="180" height="54" rx="27" fill="#FFFFFF" stroke="#708090" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="280" y="254" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#374151">Start request</text>

  <rect x="174" y="324" width="212" height="68" rx="12" fill="#FFFFFF" stroke="#708090" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="280" y="352" width="178" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#374151">
    <tspan x="280" dy="0">Upload receipts</tspan>
    <tspan x="280" dy="19">and expense form</tspan>
  </text>

  <path d="M 640 312 L 758 374 L 640 436 L 522 374 Z" fill="#FFFFFF" stroke="#708090" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="640" y="370" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#374151">
    <tspan x="640" dy="0">Policy</tspan>
    <tspan x="640" dy="19">compliant?</tspan>
  </text>

  <rect x="534" y="496" width="212" height="68" rx="12" fill="#FFFFFF" stroke="#708090" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="640" y="524" width="178" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#374151">
    <tspan x="640" dy="0">Manager approves</tspan>
    <tspan x="640" dy="19">reimbursement</tspan>
  </text>

  <rect x="894" y="322" width="212" height="68" rx="12" fill="#FFFFFF" stroke="#708090" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="1000" y="350" width="178" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#374151">
    <tspan x="1000" dy="0">Return for</tspan>
    <tspan x="1000" dy="19">correction</tspan>
  </text>

  <path d="M 1000 464 L 1118 526 L 1000 588 L 882 526 Z" fill="#FFFFFF" stroke="#708090" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="1000" y="522" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#374151">
    <tspan x="1000" dy="0">Budget</tspan>
    <tspan x="1000" dy="19">available?</tspan>
  </text>

  <rect x="894" y="600" width="212" height="42" rx="21" fill="#FFFFFF" stroke="#708090" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="1000" y="626" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#374151">Pay employee</text>

  <line x1="280" y1="276" x2="280" y2="318" stroke="#4B5563" stroke-width="2.2" marker-end="url(#arrow)"/>
  <line x1="386" y1="358" x2="454" y2="358" stroke="#4B5563" stroke-width="2.2"/>
  <line x1="454" y1="358" x2="454" y2="374" stroke="#4B5563" stroke-width="2.2"/>
  <line x1="454" y1="374" x2="516" y2="374" stroke="#4B5563" stroke-width="2.2" marker-end="url(#arrow)"/>

  <line x1="640" y1="436" x2="640" y2="490" stroke="#4B5563" stroke-width="2.2" marker-end="url(#arrow)"/>
  <line x1="758" y1="374" x2="836" y2="374" stroke="#4B5563" stroke-width="2.2"/>
  <line x1="836" y1="374" x2="836" y2="356" stroke="#4B5563" stroke-width="2.2"/>
  <line x1="836" y1="356" x2="888" y2="356" stroke="#4B5563" stroke-width="2.2" marker-end="url(#arrow)"/>

  <line x1="746" y1="530" x2="826" y2="530" stroke="#4B5563" stroke-width="2.2"/>
  <line x1="826" y1="530" x2="826" y2="526" stroke="#4B5563" stroke-width="2.2"/>
  <line x1="826" y1="526" x2="876" y2="526" stroke="#4B5563" stroke-width="2.2" marker-end="url(#arrow)"/>
  <line x1="1000" y1="588" x2="1000" y2="594" stroke="#4B5563" stroke-width="2.2" marker-end="url(#arrow)"/>

  <line x1="894" y1="356" x2="840" y2="356" stroke="#9CA3AF" stroke-width="2" stroke-dasharray="6 6"/>
  <line x1="840" y1="356" x2="840" y2="250" stroke="#9CA3AF" stroke-width="2" stroke-dasharray="6 6"/>
  <line x1="840" y1="250" x2="376" y2="250" stroke="#9CA3AF" stroke-width="2" stroke-dasharray="6 6" marker-end="url(#arrow)"/>

  <text x="780" y="344" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#B45309">No</text>
  <text x="654" y="470" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#047857">Yes</text>
  <text x="1020" y="596" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#047857">Yes</text>

  <rect x="92" y="662" width="1096" height="1.5" fill="#CBD5E1"/>
  <text x="100" y="692" width="980" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">
    Tip: keep every process node centered inside its owner lane; use elbows only when work changes hands.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using freeform diagonal connector paths for every relationship; swimlanes need crisp orthogonal routing.
- ❌ Applying `filter` to `<line>` connectors; shadows on lines are dropped and make routing look muddy.
- ❌ Putting `marker-end` on `<path>` connectors; use `<line marker-end="url(#arrow)">` on the final elbow segment.
- ❌ Over-saturating lane fills; pastel lanes should separate responsibility without competing with the node labels.
- ❌ Omitting `width` on `<text>` elements; PowerPoint translation needs explicit text box widths.

## Composition notes
- Keep the lane grid dominant: roughly 80–85% of slide width and 70–75% of slide height.
- Use white nodes with subtle shadows so process steps float above pastel accountability zones.
- Align nodes vertically within lanes, then cross horizontally only at hand-off moments.
- Reserve the top 15% of the slide for title/context and the bottom strip for a small process note or legend.