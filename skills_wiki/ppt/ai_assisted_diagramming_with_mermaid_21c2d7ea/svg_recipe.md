# SVG Recipe — AI-Assisted Diagramming with Mermaid

## Visual mechanism
Show the “diagrams as code” workflow by pairing a Mermaid-style code panel with its clean rendered diagram output. The slide feels technical and premium: a dark code editor on the left feeds an auto-laid flowchart canvas on the right with crisp nodes, decision diamonds, arrows, labels, and subtle glow/shadow depth.

## SVG primitives needed
- 1× `<rect>` full-slide background with a dark executive gradient
- 2× `<rect>` large rounded cards for the code editor and rendered diagram canvas
- 8–12× `<rect>` for code rows, node boxes, status pills, and UI chrome
- 2× `<path>` for Mermaid-style decision diamonds
- 8–10× `<line>` for editable connectors with `marker-end` applied directly to each line
- 1× `<marker>` definition for arrowheads on lines
- 1× `<filter id="softShadow">` for card and node elevation
- 1× `<filter id="glow">` for the AI/Mermaid accent halo
- 2× `<linearGradient>` for the slide background and accent fills
- Multiple `<text>` elements with explicit `width` attributes for title, code, node labels, and annotations
- Optional decorative `<circle>` elements for soft background lights and UI dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#0B1020"/>
      <stop offset="55%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#172033"/>
    </linearGradient>

    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#22D3EE"/>
    </linearGradient>

    <linearGradient id="nodeFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF2FF"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>

    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
      <path d="M2,2 L10,6 L2,10 Z" fill="#64748B"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <circle cx="1110" cy="110" r="150" fill="#22D3EE" opacity="0.11" filter="url(#glow)"/>
  <circle cx="270" cy="620" r="190" fill="#8B5CF6" opacity="0.12" filter="url(#glow)"/>

  <text x="70" y="68" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F8FAFC">
    AI-assisted diagramming with Mermaid
  </text>
  <text x="72" y="104" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#CBD5E1">
    Describe the logic once. Generate diagram code. Render a structured visual in seconds.
  </text>

  <rect x="70" y="145" width="455" height="485" rx="24" fill="#0F172A" stroke="#334155" stroke-width="1.2" filter="url(#softShadow)"/>
  <rect x="70" y="145" width="455" height="48" rx="24" fill="#111C32"/>
  <circle cx="102" cy="170" r="6" fill="#EF4444"/>
  <circle cx="124" cy="170" r="6" fill="#F59E0B"/>
  <circle cx="146" cy="170" r="6" fill="#22C55E"/>
  <text x="178" y="176" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">
    generated_process_flow.mmd
  </text>

  <rect x="96" y="214" width="394" height="70" rx="14" fill="#182238" stroke="#334155"/>
  <text x="118" y="240" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#E2E8F0">
    AI prompt
  </text>
  <text x="118" y="262" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A7F3D0">
    “Map the intake-to-approval workflow with exception handling.”
  </text>

  <text x="104" y="322" width="390" font-family="Consolas, Segoe UI, Microsoft YaHei" font-size="15" fill="#94A3B8">
    flowchart LR
  </text>
  <text x="104" y="350" width="390" font-family="Consolas, Segoe UI, Microsoft YaHei" font-size="15" fill="#E0E7FF">
    A[Submit request] --&gt; B{Complete?}
  </text>
  <text x="104" y="378" width="390" font-family="Consolas, Segoe UI, Microsoft YaHei" font-size="15" fill="#E0E7FF">
    B -- Yes --&gt; C[Risk scoring]
  </text>
  <text x="104" y="406" width="390" font-family="Consolas, Segoe UI, Microsoft YaHei" font-size="15" fill="#E0E7FF">
    B -- No --&gt; D[Request missing info]
  </text>
  <text x="104" y="434" width="390" font-family="Consolas, Segoe UI, Microsoft YaHei" font-size="15" fill="#E0E7FF">
    C --&gt; E{Auto approve?}
  </text>
  <text x="104" y="462" width="390" font-family="Consolas, Segoe UI, Microsoft YaHei" font-size="15" fill="#E0E7FF">
    E -- Yes --&gt; F[Notify customer]
  </text>
  <text x="104" y="490" width="390" font-family="Consolas, Segoe UI, Microsoft YaHei" font-size="15" fill="#E0E7FF">
    E -- No --&gt; G[Manual review]
  </text>
  <text x="104" y="518" width="390" font-family="Consolas, Segoe UI, Microsoft YaHei" font-size="15" fill="#E0E7FF">
    G --&gt; F
  </text>

  <rect x="96" y="557" width="145" height="34" rx="17" fill="url(#accent)"/>
  <text x="118" y="579" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">
    Render SVG
  </text>
  <text x="260" y="579" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">
    editable shapes in PowerPoint
  </text>

  <line x1="536" y1="388" x2="602" y2="388" stroke="#22D3EE" stroke-width="3" stroke-dasharray="8 8" marker-end="url(#arrow)"/>

  <rect x="620" y="145" width="590" height="485" rx="28" fill="#F8FAFC" stroke="#D9E2F1" stroke-width="1.4" filter="url(#softShadow)"/>
  <rect x="650" y="171" width="166" height="32" rx="16" fill="#EEF2FF"/>
  <text x="672" y="192" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#4F46E5">
    Mermaid output
  </text>
  <text x="844" y="193" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">
    auto-layout flowchart, generated from text
  </text>

  <rect x="682" y="255" width="150" height="58" rx="16" fill="url(#nodeFill)" stroke="#8B5CF6" stroke-width="2"/>
  <text x="712" y="290" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E293B">
    Submit request
  </text>

  <path d="M940 238 L1028 284 L940 330 L852 284 Z" fill="#FFF7ED" stroke="#F97316" stroke-width="2"/>
  <text x="890" y="289" width="102" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E293B">
    Complete?
  </text>

  <rect x="696" y="400" width="150" height="58" rx="16" fill="#ECFEFF" stroke="#06B6D4" stroke-width="2"/>
  <text x="730" y="435" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#164E63">
    Missing info
  </text>

  <rect x="1060" y="255" width="110" height="58" rx="16" fill="#F0FDF4" stroke="#22C55E" stroke-width="2"/>
  <text x="1082" y="290" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#14532D">
    Risk score
  </text>

  <path d="M940 385 L1028 431 L940 477 L852 431 Z" fill="#EEF2FF" stroke="#6366F1" stroke-width="2"/>
  <text x="892" y="436" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E293B">
    Auto approve?
  </text>

  <rect x="1052" y="533" width="128" height="58" rx="16" fill="#F8FAFC" stroke="#94A3B8" stroke-width="2"/>
  <text x="1080" y="568" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#334155">
    Manual review
  </text>

  <rect x="698" y="533" width="150" height="58" rx="16" fill="url(#accent)" stroke="#0EA5E9" stroke-width="2"/>
  <text x="730" y="568" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">
    Notify customer
  </text>

  <line x1="832" y1="284" x2="852" y2="284" stroke="#64748B" stroke-width="2.2" marker-end="url(#arrow)"/>
  <line x1="1028" y1="284" x2="1060" y2="284" stroke="#64748B" stroke-width="2.2" marker-end="url(#arrow)"/>
  <line x1="940" y1="330" x2="940" y2="385" stroke="#64748B" stroke-width="2.2" marker-end="url(#arrow)"/>
  <line x1="852" y1="298" x2="771" y2="400" stroke="#64748B" stroke-width="2.2" stroke-dasharray="6 6" marker-end="url(#arrow)"/>
  <line x1="1060" y1="313" x2="1008" y2="397" stroke="#64748B" stroke-width="2.2" marker-end="url(#arrow)"/>
  <line x1="852" y1="431" x2="848" y2="533" stroke="#64748B" stroke-width="2.2" marker-end="url(#arrow)"/>
  <line x1="1028" y1="431" x2="1116" y2="533" stroke="#64748B" stroke-width="2.2" marker-end="url(#arrow)"/>
  <line x1="1052" y1="562" x2="848" y2="562" stroke="#64748B" stroke-width="2.2" marker-end="url(#arrow)"/>

  <rect x="855" y="250" width="42" height="22" rx="11" fill="#FFF7ED" stroke="#FDBA74"/>
  <text x="866" y="266" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#C2410C">
    Yes
  </text>
  <rect x="784" y="342" width="36" height="22" rx="11" fill="#F1F5F9" stroke="#CBD5E1"/>
  <text x="795" y="358" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#475569">
    No
  </text>
</svg>
```

## Avoid in this skill
- ❌ Inserting the Mermaid render only as a flat bitmap when the goal is editable PowerPoint shapes.
- ❌ Using `<path marker-end="...">` for arrows; arrowheads on paths can disappear. Use `<line marker-end="url(#arrow)">` directly.
- ❌ Relying on Mermaid’s exact browser-rendered SVG internals, which may include unsupported constructs; rebuild the visual grammar with editable SVG primitives.
- ❌ Omitting `width` on `<text>` elements; PowerPoint text boxes may clip or reflow unpredictably.
- ❌ Overcrowding the diagram with too many nodes; the Mermaid aesthetic depends on structured whitespace and clear routing.

## Composition notes
- Keep the left 35–40% of the slide for the Mermaid/code-generation story; use the right 55–60% for the rendered diagram.
- Use a dark code editor against a light diagram canvas to make the transformation from text to visual immediately legible.
- Maintain generous spacing between nodes; connectors should feel algorithmically routed, not hand-crammed.
- Use one strong accent gradient for AI/Mermaid actions, then neutral fills for most diagram nodes to preserve business readability.