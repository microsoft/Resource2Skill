# SVG Recipe — Swimlane Process Flowchart

## Visual mechanism
A swimlane process flowchart uses horizontal role bands as a responsibility map, then places flowchart nodes along a left-to-right timeline to show sequence and hand-offs. The premium look comes from subtle alternating lanes, a disciplined header column, soft node shadows, bright accent process nodes, and clean elbow connectors with explicit arrowheads.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 1× `<linearGradient>` for accent process-node fills
- 1× `<linearGradient>` for the title accent rule
- 1× `<filter id="softShadow">` applied to nodes only
- 4× large `<rect>` for alternating swimlane bands
- 1× `<rect>` for the left lane-header column
- 6× `<line>` for lane dividers, header separator, and timeline guides
- 8× `<text>` for title, subtitle, and lane headers
- 5× rounded `<rect>` for process/action nodes
- 1× `<ellipse>` for the start event
- 1× `<path>` for a decision diamond
- 1× `<path>` plus 1× `<ellipse>` for a database / system node
- Multiple `<line>` connectors; use separate straight segments for elbows, with `marker-end` only on the final `<line>`
- Small `<rect>` + `<text>` callouts for connector labels such as “YES” and “NO”

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="orangeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFB34D"/>
      <stop offset="100%" stop-color="#FF7A00"/>
    </linearGradient>
    <linearGradient id="ruleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF8C00"/>
      <stop offset="55%" stop-color="#FFB24A"/>
      <stop offset="100%" stop-color="#FFE1B8"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrowOrange" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#FF8C00"/>
    </marker>
    <marker id="arrowGrey" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#8B8F99"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <text x="54" y="46" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#2F3338">Cross-Functional Onboarding Flow</text>
  <text x="56" y="76" width="740" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777E8A">Ownership, hand-offs, decisions, and system touchpoints across teams</text>
  <rect x="54" y="88" width="410" height="5" rx="2.5" fill="url(#ruleGrad)"/>

  <rect x="48" y="110" width="1184" height="140" fill="#F7F7FB"/>
  <rect x="48" y="250" width="1184" height="140" fill="#FFFFFF"/>
  <rect x="48" y="390" width="1184" height="140" fill="#F7F7FB"/>
  <rect x="48" y="530" width="1184" height="140" fill="#FFFFFF"/>
  <rect x="48" y="110" width="168" height="560" fill="#F1F2F6"/>

  <line x1="48" y1="110" x2="1232" y2="110" stroke="#DDE1E8" stroke-width="1"/>
  <line x1="48" y1="250" x2="1232" y2="250" stroke="#DDE1E8" stroke-width="1"/>
  <line x1="48" y1="390" x2="1232" y2="390" stroke="#DDE1E8" stroke-width="1"/>
  <line x1="48" y1="530" x2="1232" y2="530" stroke="#DDE1E8" stroke-width="1"/>
  <line x1="48" y1="670" x2="1232" y2="670" stroke="#DDE1E8" stroke-width="1"/>
  <line x1="216" y1="110" x2="216" y2="670" stroke="#CFD4DC" stroke-width="2"/>

  <text x="188" y="185" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#5B616B">Customer</text>
  <text x="188" y="325" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#5B616B">Sales Team</text>
  <text x="188" y="465" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#5B616B">Operations</text>
  <text x="188" y="605" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#5B616B">System / DB</text>

  <line x1="300" y1="126" x2="300" y2="660" stroke="#ECEFF4" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="520" y1="126" x2="520" y2="660" stroke="#ECEFF4" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="740" y1="126" x2="740" y2="660" stroke="#ECEFF4" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="960" y1="126" x2="960" y2="660" stroke="#ECEFF4" stroke-width="1" stroke-dasharray="5 8"/>

  <ellipse cx="316" cy="180" rx="64" ry="30" fill="#FFFFFF" stroke="#FF8C00" stroke-width="2.2" filter="url(#softShadow)"/>
  <text x="316" y="185" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3D424A">Request</text>

  <rect x="430" y="293" width="142" height="54" rx="14" fill="url(#orangeGrad)" filter="url(#softShadow)"/>
  <text x="501" y="315" width="126" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Capture</text>
  <text x="501" y="332" width="126" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">requirements</text>

  <path d="M700 282 L785 320 L700 358 L615 320 Z" fill="#FFFFFF" stroke="#FF8C00" stroke-width="2.2" filter="url(#softShadow)"/>
  <text x="700" y="316" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#3D424A">Qualified</text>
  <text x="700" y="333" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#3D424A">opportunity?</text>

  <rect x="835" y="433" width="150" height="56" rx="14" fill="url(#orangeGrad)" filter="url(#softShadow)"/>
  <text x="910" y="456" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Schedule</text>
  <text x="910" y="473" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">fulfillment</text>

  <rect x="1030" y="433" width="142" height="56" rx="14" fill="url(#orangeGrad)" filter="url(#softShadow)"/>
  <text x="1101" y="456" width="122" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Complete</text>
  <text x="1101" y="473" width="122" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">handover</text>

  <path d="M835 578 C835 562 985 562 985 578 L985 625 C985 641 835 641 835 625 Z" fill="#F4F5F7" stroke="#9EA4AF" stroke-width="1.8" filter="url(#softShadow)"/>
  <ellipse cx="910" cy="578" rx="75" ry="16" fill="#FFFFFF" stroke="#9EA4AF" stroke-width="1.8"/>
  <text x="910" y="610" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#5B616B">Update CRM</text>

  <rect x="1030" y="153" width="142" height="54" rx="27" fill="#FFFFFF" stroke="#FF8C00" stroke-width="2.2" filter="url(#softShadow)"/>
  <text x="1101" y="176" width="122" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#3D424A">Customer</text>
  <text x="1101" y="193" width="122" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#3D424A">confirmed</text>

  <line x1="380" y1="180" x2="410" y2="180" stroke="#FF8C00" stroke-width="2.4"/>
  <line x1="410" y1="180" x2="410" y2="320" stroke="#FF8C00" stroke-width="2.4"/>
  <line x1="410" y1="320" x2="430" y2="320" stroke="#FF8C00" stroke-width="2.4" marker-end="url(#arrowOrange)"/>

  <line x1="572" y1="320" x2="615" y2="320" stroke="#FF8C00" stroke-width="2.4" marker-end="url(#arrowOrange)"/>

  <rect x="805" y="298" width="42" height="22" rx="11" fill="#FFFFFF" stroke="#E5E8EE"/>
  <text x="826" y="314" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#FF8C00">YES</text>
  <line x1="785" y1="320" x2="812" y2="320" stroke="#FF8C00" stroke-width="2.4"/>
  <line x1="812" y1="320" x2="812" y2="461" stroke="#FF8C00" stroke-width="2.4"/>
  <line x1="812" y1="461" x2="835" y2="461" stroke="#FF8C00" stroke-width="2.4" marker-end="url(#arrowOrange)"/>

  <rect x="690" y="382" width="38" height="22" rx="11" fill="#FFFFFF" stroke="#E5E8EE"/>
  <text x="709" y="398" width="34" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#8B8F99">NO</text>
  <line x1="700" y1="358" x2="700" y2="602" stroke="#8B8F99" stroke-width="2.1"/>
  <line x1="700" y1="602" x2="835" y2="602" stroke="#8B8F99" stroke-width="2.1" marker-end="url(#arrowGrey)"/>

  <line x1="985" y1="461" x2="1030" y2="461" stroke="#FF8C00" stroke-width="2.4" marker-end="url(#arrowOrange)"/>
  <line x1="910" y1="489" x2="910" y2="562" stroke="#8B8F99" stroke-width="2.1" marker-end="url(#arrowGrey)"/>
  <line x1="1101" y1="433" x2="1101" y2="207" stroke="#FF8C00" stroke-width="2.4" marker-end="url(#arrowOrange)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not draw elbow connectors as a single `<path marker-end="...">`; path arrowheads may disappear. Use multiple `<line>` segments and put `marker-end` on the final segment only.
- ❌ Do not rely on heavy table borders around every lane; it makes the slide look like a spreadsheet instead of an executive process map.
- ❌ Do not apply filters to connector lines; shadows/glows on `<line>` are dropped. Keep shadows on nodes only.
- ❌ Do not place lane labels inside the process area; reserve a fixed left header column so ownership remains instantly readable.
- ❌ Do not omit explicit `width` attributes on `<text>` elements; PowerPoint rendering depends on them.

## Composition notes
- Keep the left 15–18% of the canvas as a dedicated lane-header column; the remaining width is the process timeline.
- Use alternating ultra-light lane fills to guide reading without overpowering the flowchart nodes.
- Make process steps vivid and consistent, then reserve white fill with accent stroke for decisions and terminal/customer states.
- Route connectors orthogonally with generous spacing; each vertical move should visually signal a cross-functional hand-off.