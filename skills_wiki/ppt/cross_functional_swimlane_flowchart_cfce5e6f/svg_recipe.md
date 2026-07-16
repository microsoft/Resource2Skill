# SVG Recipe — Cross-Functional Swimlane Flowchart

## Visual mechanism
A cross-functional swimlane flowchart stacks horizontal ownership bands and routes a process through them with orthogonal arrow connectors. The design works by combining a strict column grid, color-coded lane headers, editable flowchart nodes, and decision diamonds that make both sequence and responsibility visible at once.

## SVG primitives needed
- 1× `<rect>` for the clean white slide background.
- 4× `<rect>` for pastel swimlane body bands.
- 4× `<rect>` for saturated vertical lane header blocks.
- 9× `<rect>` for rounded process/start/end nodes with white fills and subtle shadows.
- 2× `<path>` for editable decision diamonds.
- 20+× `<line>` for orthogonal elbow connector segments and faint column guide lines.
- 3× small `<rect>` label backplates for “Yes” / “No” decision labels.
- 20+× `<text>` elements for title, subtitle, lane headers, node labels, and connector labels; every text element uses an explicit `width`.
- 1× `<filter id="softShadow">` applied to nodes and decision diamonds.
- 4× `<linearGradient>` fills for premium-looking lane headers.
- 1× `<marker id="arrow">` used directly on final connector `<line>` segments.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueHeader" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3498DB"/>
      <stop offset="100%" stop-color="#1F618D"/>
    </linearGradient>
    <linearGradient id="greenHeader" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2ECC71"/>
      <stop offset="100%" stop-color="#1E8449"/>
    </linearGradient>
    <linearGradient id="slateHeader" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5D6D7E"/>
      <stop offset="100%" stop-color="#2C3E50"/>
    </linearGradient>
    <linearGradient id="orangeHeader" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E67E22"/>
      <stop offset="100%" stop-color="#BA4A00"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="160%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#334155"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <text x="56" y="54" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#1F2937">
    Cross-Functional E-Commerce Fulfillment Flow
  </text>
  <text x="58" y="84" width="850" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">
    Swimlanes show ownership; connectors show the process handoff sequence across teams.
  </text>

  <rect x="92" y="130" width="1132" height="132" fill="#EAF2F8" stroke="#FFFFFF" stroke-width="2"/>
  <rect x="92" y="262" width="1132" height="132" fill="#E9F7EF" stroke="#FFFFFF" stroke-width="2"/>
  <rect x="92" y="394" width="1132" height="132" fill="#EBEDEF" stroke="#FFFFFF" stroke-width="2"/>
  <rect x="92" y="526" width="1132" height="132" fill="#FDF2E9" stroke="#FFFFFF" stroke-width="2"/>

  <rect x="0" y="130" width="92" height="132" fill="url(#blueHeader)" stroke="#FFFFFF" stroke-width="2"/>
  <rect x="0" y="262" width="92" height="132" fill="url(#greenHeader)" stroke="#FFFFFF" stroke-width="2"/>
  <rect x="0" y="394" width="92" height="132" fill="url(#slateHeader)" stroke="#FFFFFF" stroke-width="2"/>
  <rect x="0" y="526" width="92" height="132" fill="url(#orangeHeader)" stroke="#FFFFFF" stroke-width="2"/>

  <text x="-222" y="54" width="132" transform="rotate(-90)" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">Customer</text>
  <text x="-354" y="54" width="132" transform="rotate(-90)" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">Sales Dept</text>
  <text x="-486" y="54" width="132" transform="rotate(-90)" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">Warehouse</text>
  <text x="-618" y="54" width="132" transform="rotate(-90)" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">Accounting</text>

  <line x1="300" y1="118" x2="300" y2="660" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="480" y1="118" x2="480" y2="660" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="660" y1="118" x2="660" y2="660" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="835" y1="118" x2="835" y2="660" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="1010" y1="118" x2="1010" y2="660" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="5 8"/>

  <line x1="260" y1="196" x2="320" y2="196" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>
  <line x1="460" y1="196" x2="480" y2="196" stroke="#334155" stroke-width="2.4"/>
  <line x1="480" y1="196" x2="480" y2="328" stroke="#334155" stroke-width="2.4"/>
  <line x1="480" y1="328" x2="500" y2="328" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>
  <line x1="650" y1="328" x2="680" y2="328" stroke="#334155" stroke-width="2.4"/>
  <line x1="680" y1="328" x2="680" y2="420" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>
  <line x1="745" y1="460" x2="805" y2="460" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>
  <line x1="680" y1="420" x2="680" y2="358" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>
  <line x1="955" y1="460" x2="1010" y2="460" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>
  <line x1="1080" y1="490" x2="1080" y2="562" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>
  <line x1="1010" y1="592" x2="905" y2="592" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>
  <line x1="775" y1="592" x2="755" y2="592" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>
  <line x1="840" y1="552" x2="1160" y2="552" stroke="#334155" stroke-width="2.4"/>
  <line x1="1160" y1="552" x2="1160" y2="224" stroke="#334155" stroke-width="2.4" marker-end="url(#arrow)"/>

  <rect x="140" y="168" width="120" height="56" rx="28" fill="#FFFFFF" stroke="#2980B9" stroke-width="2" filter="url(#softShadow)"/>
  <text x="200" y="202" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#1E3A5F" text-anchor="middle">Start</text>

  <rect x="320" y="166" width="140" height="60" rx="10" fill="#FFFFFF" stroke="#2980B9" stroke-width="2" filter="url(#softShadow)"/>
  <text x="390" y="191" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1F2937" text-anchor="middle">
    <tspan x="390" dy="0">Place</tspan><tspan x="390" dy="17">Order</tspan>
  </text>

  <rect x="500" y="298" width="150" height="60" rx="10" fill="#FFFFFF" stroke="#27AE60" stroke-width="2" filter="url(#softShadow)"/>
  <text x="575" y="323" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1F2937" text-anchor="middle">
    <tspan x="575" dy="0">Validate</tspan><tspan x="575" dy="17">Order</tspan>
  </text>

  <rect x="645" y="298" width="145" height="60" rx="10" fill="#FFFFFF" stroke="#27AE60" stroke-width="2" filter="url(#softShadow)"/>
  <text x="717" y="323" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1F2937" text-anchor="middle">
    <tspan x="717" dy="0">Backorder</tspan><tspan x="717" dy="16">Notice</tspan>
  </text>

  <path d="M680 420 L745 460 L680 500 L615 460 Z" fill="#FFFFFF" stroke="#34495E" stroke-width="2.2" filter="url(#softShadow)"/>
  <text x="680" y="455" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1F2937" text-anchor="middle">
    <tspan x="680" dy="0">Stock</tspan><tspan x="680" dy="16">Available?</tspan>
  </text>

  <rect x="805" y="430" width="150" height="60" rx="10" fill="#FFFFFF" stroke="#34495E" stroke-width="2" filter="url(#softShadow)"/>
  <text x="880" y="455" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1F2937" text-anchor="middle">
    <tspan x="880" dy="0">Pick &amp;</tspan><tspan x="880" dy="17">Pack</tspan>
  </text>

  <rect x="1010" y="430" width="140" height="60" rx="10" fill="#FFFFFF" stroke="#34495E" stroke-width="2" filter="url(#softShadow)"/>
  <text x="1080" y="465" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1F2937" text-anchor="middle">Ship Items</text>

  <rect x="1010" y="562" width="140" height="60" rx="10" fill="#FFFFFF" stroke="#D35400" stroke-width="2" filter="url(#softShadow)"/>
  <text x="1080" y="587" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1F2937" text-anchor="middle">
    <tspan x="1080" dy="0">Issue</tspan><tspan x="1080" dy="17">Invoice</tspan>
  </text>

  <path d="M840 552 L905 592 L840 632 L775 592 Z" fill="#FFFFFF" stroke="#D35400" stroke-width="2.2" filter="url(#softShadow)"/>
  <text x="840" y="587" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1F2937" text-anchor="middle">
    <tspan x="840" dy="0">Payment</tspan><tspan x="840" dy="16">Received?</tspan>
  </text>

  <rect x="610" y="562" width="145" height="60" rx="10" fill="#FFFFFF" stroke="#D35400" stroke-width="2" filter="url(#softShadow)"/>
  <text x="682" y="587" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1F2937" text-anchor="middle">
    <tspan x="682" dy="0">Payment</tspan><tspan x="682" dy="16">Reminder</tspan>
  </text>

  <rect x="1092" y="168" width="136" height="56" rx="28" fill="#FFFFFF" stroke="#2980B9" stroke-width="2" filter="url(#softShadow)"/>
  <text x="1160" y="193" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E3A5F" text-anchor="middle">
    <tspan x="1160" dy="0">Confirm</tspan><tspan x="1160" dy="16">Delivery</tspan>
  </text>

  <rect x="755" y="442" width="38" height="20" rx="10" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="774" y="456" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#166534" text-anchor="middle">Yes</text>
  <rect x="630" y="382" width="34" height="20" rx="10" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="647" y="396" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#991B1B" text-anchor="middle">No</text>
  <rect x="930" y="534" width="38" height="20" rx="10" fill="#FFFFFF" stroke="#CBD5E1"/>
  <text x="949" y="548" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#166534" text-anchor="middle">Yes</text>
</svg>
```

## Avoid in this skill
- ❌ Do not draw elbow arrows as a single `<path marker-end="...">`; marker-end on paths can disappear. Use separate `<line>` segments and put `marker-end` directly on the final line segment.
- ❌ Do not rely on parent `<g>` inheritance for arrowheads; every arrow-ending `<line>` should carry its own `marker-end`.
- ❌ Do not apply filters to connector `<line>` elements; shadows on lines are not preserved reliably. Apply shadows only to nodes and diamonds.
- ❌ Do not use `<foreignObject>` for wrapped node labels; use native `<text>` with explicit `width` and nested `<tspan>` line breaks.
- ❌ Do not omit `width` on any text element, especially rotated lane headers and small connector labels.

## Composition notes
- Keep the title area shallow; reserve most vertical space for the four process lanes.
- Use muted lane body colors and saturated header blocks so ownership is clear without overpowering the flow nodes.
- Align nodes to a consistent column rhythm; cross-lane connectors should feel intentional, not diagonal or freeform.
- Place decision labels on small white rounded backplates to keep “Yes/No” readable where connectors cross colored lanes.