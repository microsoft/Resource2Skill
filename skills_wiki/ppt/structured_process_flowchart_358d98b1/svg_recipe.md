# SVG Recipe — Structured Process Flowchart

## Visual mechanism
A structured flowchart translates a workflow into a standardized visual grammar: pill terminators for start/end, rectangles for tasks, parallelograms for input/output, and diamonds for decisions. Directional connectors and branch labels make the sequence, approvals, loops, and outcomes immediately scannable.

## SVG primitives needed
- 1× `<rect>` full-slide background with soft gradient fill.
- 2× large `<rect>` panels for the flowchart canvas and the legend/notes area.
- 2× `<rect rx>` pill terminators for Start and End.
- 4× `<rect>` process boxes for action steps.
- 1× `<path>` parallelogram for data/input step.
- 1× `<path>` diamond for decision point.
- 9× `<line>` connectors with `marker-end` applied directly to each arrow segment that needs an arrowhead.
- 4× small `<circle>` step-number badges.
- Multiple `<text>` labels with explicit `width=` attributes for titles, shape labels, connector labels, and legend text.
- 3× `<linearGradient>` definitions for background, accent fills, and terminators.
- 2× `<filter>` definitions for soft panel shadows and node shadows, applied only to shapes, not lines.
- 1× `<marker>` definition for arrowheads used directly on `<line>` elements.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#EEF4FF"/>
      <stop offset="100%" stop-color="#F7F7FB"/>
    </linearGradient>
    <linearGradient id="pillGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#0F766E"/>
    </linearGradient>
    <linearGradient id="decisionGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EFF6FF"/>
    </linearGradient>
    <filter id="panelShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="nodeShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrowSlate" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
      <path d="M2,2 L10,6 L2,10 Z" fill="#475569"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="70" y="54" width="740" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="700" fill="#0F172A">
    Employee Leave Approval Workflow
  </text>
  <text x="72" y="82" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#64748B">
    A standardized process map showing intake, validation, decision branching, revision loop, and final recording.
  </text>

  <rect x="58" y="100" width="858" height="566" rx="26" fill="#FFFFFF" opacity="0.96" filter="url(#panelShadow)"/>
  <rect x="86" y="126" width="140" height="28" rx="14" fill="#EFF6FF" stroke="#BFDBFE"/>
  <text x="106" y="146" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#2563EB">
    PROCESS MAP
  </text>

  <rect x="410" y="124" width="150" height="48" rx="24" fill="url(#pillGrad)" filter="url(#nodeShadow)"/>
  <text x="410" y="153" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">
    Start
  </text>

  <path d="M360 196 L590 196 L630 258 L400 258 Z" fill="#FFFFFF" stroke="#475569" stroke-width="2" filter="url(#nodeShadow)"/>
  <circle cx="398" cy="212" r="13" fill="#DBEAFE" stroke="#60A5FA"/>
  <text x="390" y="217" width="16" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#1D4ED8">1</text>
  <text x="395" y="226" width="215" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#111827">
    Submit leave request
  </text>
  <text x="395" y="246" width="215" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#64748B">
    dates, reason, backup owner
  </text>

  <rect x="365" y="288" width="240" height="70" rx="12" fill="#FFFFFF" stroke="#475569" stroke-width="2" filter="url(#nodeShadow)"/>
  <rect x="365" y="288" width="240" height="8" rx="4" fill="#14B8A6"/>
  <circle cx="390" cy="314" r="13" fill="#CCFBF1" stroke="#2DD4BF"/>
  <text x="382" y="319" width="16" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#0F766E">2</text>
  <text x="385" y="323" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#111827">
    Validate policy
  </text>
  <text x="385" y="344" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#64748B">
    balance, blackout dates, coverage
  </text>

  <path d="M500 382 L635 452 L500 522 L365 452 Z" fill="url(#decisionGrad)" stroke="#475569" stroke-width="2.2" filter="url(#nodeShadow)"/>
  <text x="405" y="443" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">
    Meets approval
  </text>
  <text x="405" y="464" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#111827">
    criteria?
  </text>

  <rect x="125" y="417" width="210" height="72" rx="12" fill="#FFFFFF" stroke="#475569" stroke-width="2" filter="url(#nodeShadow)"/>
  <rect x="125" y="417" width="210" height="8" rx="4" fill="#F97316"/>
  <text x="145" y="447" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#111827">
    Return for revision
  </text>
  <text x="145" y="468" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#64748B">
    missing detail or conflict
  </text>

  <rect x="670" y="417" width="210" height="72" rx="12" fill="#FFFFFF" stroke="#475569" stroke-width="2" filter="url(#nodeShadow)"/>
  <rect x="670" y="417" width="210" height="8" rx="4" fill="#22C55E"/>
  <text x="690" y="447" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#111827">
    Manager approves
  </text>
  <text x="690" y="468" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#64748B">
    confirm coverage plan
  </text>

  <rect x="125" y="548" width="210" height="64" rx="12" fill="#FFF7ED" stroke="#FB923C" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="145" y="578" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#9A3412">
    Employee updates
  </text>
  <text x="145" y="598" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#9A3412">
    resubmit to intake
  </text>

  <rect x="670" y="548" width="210" height="64" rx="12" fill="#F0FDF4" stroke="#22C55E" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="690" y="578" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#166534">
    HR records absence
  </text>
  <text x="690" y="598" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#166534">
    payroll and calendar updated
  </text>

  <rect x="410" y="612" width="150" height="44" rx="22" fill="url(#pillGrad)" filter="url(#nodeShadow)"/>
  <text x="410" y="639" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">
    End
  </text>

  <line x1="485" y1="172" x2="495" y2="196" stroke="#475569" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <line x1="495" y1="258" x2="485" y2="288" stroke="#475569" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <line x1="485" y1="358" x2="500" y2="382" stroke="#475569" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <line x1="365" y1="452" x2="335" y2="452" stroke="#475569" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <line x1="635" y1="452" x2="670" y2="452" stroke="#475569" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <line x1="230" y1="489" x2="230" y2="548" stroke="#475569" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <line x1="775" y1="489" x2="775" y2="548" stroke="#475569" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <line x1="670" y1="580" x2="560" y2="634" stroke="#475569" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <line x1="125" y1="580" x2="86" y2="580" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 5"/>
  <line x1="86" y1="580" x2="86" y2="227" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 5"/>
  <line x1="86" y1="227" x2="400" y2="227" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#arrowSlate)"/>

  <text x="287" y="435" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#C2410C">No</text>
  <text x="642" y="435" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#15803D">Yes</text>
  <text x="98" y="218" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="600" fill="#64748B">Revision loop</text>

  <rect x="956" y="118" width="258" height="486" rx="24" fill="#0F172A" opacity="0.96" filter="url(#panelShadow)"/>
  <text x="986" y="164" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#FFFFFF">
    Flowchart grammar
  </text>
  <text x="986" y="195" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#CBD5E1">
    Keep shape meanings consistent so viewers can decode the process without a legend.
  </text>

  <rect x="990" y="238" width="54" height="28" rx="14" fill="#2563EB"/>
  <text x="1060" y="258" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E2E8F0">Start / End</text>
  <rect x="990" y="292" width="58" height="34" rx="6" fill="#FFFFFF" stroke="#94A3B8"/>
  <text x="1060" y="314" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E2E8F0">Process step</text>
  <path d="M1019 357 L1050 378 L1019 399 L988 378 Z" fill="#EFF6FF" stroke="#94A3B8"/>
  <text x="1060" y="382" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E2E8F0">Decision gate</text>
  <path d="M990 430 L1040 430 L1054 460 L1004 460 Z" fill="#FFFFFF" stroke="#94A3B8"/>
  <text x="1060" y="452" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E2E8F0">Input / Output</text>

  <line x1="990" y1="512" x2="1060" y2="512" stroke="#94A3B8" stroke-width="2" marker-end="url(#arrowSlate)"/>
  <text x="1074" y="517" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E2E8F0">Flow direction</text>
  <text x="986" y="566" width="206" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#93C5FD">
    Design rule:
  </text>
  <text x="986" y="587" width="206" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#CBD5E1">
    Align centers, use one arrow style, and label only the branch conditions that change the path.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<path>` connectors with `marker-end`; arrowheads may disappear. Use `<line>` connectors and put `marker-end` directly on each arrow line.
- ❌ Applying shadows or blur filters to connector lines; filters on `<line>` are dropped.
- ❌ Mixing too many shape meanings, colors, or line styles; it weakens the standardized flowchart grammar.
- ❌ Long paragraphs inside nodes; flowchart labels should be short action phrases or decision questions.
- ❌ Placing arrows too close to text; keep connector paths visually separate from labels and node interiors.

## Composition notes
- Keep the main flowchart in a large clean canvas occupying roughly 70% of the slide; use the side panel only for legend, assumptions, or process notes.
- Maintain consistent vertical spacing between primary steps and align central nodes on the same axis for executive-level polish.
- Use color sparingly: neutral outlines for structure, one green path for success, one orange path for revision or exception handling.
- Decision diamonds should sit at branch points with short “Yes/No” labels placed near the outgoing arrows, not inside the connector lines.