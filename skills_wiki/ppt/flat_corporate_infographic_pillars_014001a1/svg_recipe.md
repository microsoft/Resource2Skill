# SVG Recipe — Flat Corporate Infographic Pillars

## Visual mechanism
A rigid three-column infographic uses flat, high-contrast header blocks with centered downward tabs that visually plug into lighter body cards. Each pillar is anchored by an overlapping circular number badge, creating a clean executive-summary structure for parallel business topics.

## SVG primitives needed
- 1× `<rect>` for the full-slide white background
- 1× `<rect>` for the thin crimson title accent rule
- 3× `<rect>` for light-gray pillar body blocks with subtle borders
- 3× `<path>` for the custom tabbed header shapes: rectangle plus downward-pointing triangular notch
- 3× `<circle>` for white icon medallions inside each header
- 3× `<circle>` for bottom number badges overlapping each body block
- 3× `<path>` for simple white mini-icons inside the header medallions
- Multiple `<text>` elements with explicit `width` for title, card titles, body bullets, badge numbers, and footer labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Slide title -->
  <text x="64" y="72" width="920" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#464B50" letter-spacing="0.5">
    COMPLETED, OUTSTANDING AND NEW ITEMS
  </text>
  <rect x="64" y="104" width="1152" height="4" fill="#D33141"/>
  <text x="64" y="135" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7A7A7A">
    Quarterly operating review — status summary across key workstreams
  </text>

  <!-- Pillar 01 body -->
  <rect x="86" y="286" width="322" height="338" fill="#F5F5F5" stroke="#DCDCDC" stroke-width="1.5"/>
  <path d="M86 174 L408 174 L408 286 L279 286 L247 319 L215 286 L86 286 Z" fill="#464B50"/>
  <circle cx="247" cy="224" r="27" fill="#FFFFFF"/>
  <path d="M234 224 L243 233 L262 211" fill="none" stroke="#464B50" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="118" y="271" width="258" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" letter-spacing="0.6">
    COMPLETED ITEMS
  </text>
  <text x="118" y="354" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#323232">
    Delivered this quarter
  </text>
  <text x="118" y="390" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666666">
    <tspan x="118" dy="0">• Migration wave one closed</tspan>
    <tspan x="118" dy="28">• Vendor contracts finalized</tspan>
    <tspan x="118" dy="28">• Reporting cadence adopted</tspan>
    <tspan x="118" dy="28">• Risk register refreshed</tspan>
  </text>
  <rect x="118" y="528" width="258" height="1.5" fill="#D8D8D8"/>
  <text x="118" y="562" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#858585">
    Proof points are signed off and archived in the PMO workspace.
  </text>
  <circle cx="247" cy="624" r="36" fill="#464B50"/>
  <text x="211" y="637" width="72" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#FFFFFF">
    01
  </text>

  <!-- Pillar 02 body -->
  <rect x="479" y="286" width="322" height="338" fill="#F5F5F5" stroke="#DCDCDC" stroke-width="1.5"/>
  <path d="M479 174 L801 174 L801 286 L672 286 L640 319 L608 286 L479 286 Z" fill="#D33141"/>
  <circle cx="640" cy="224" r="27" fill="#FFFFFF"/>
  <path d="M640 207 L640 227" fill="none" stroke="#D33141" stroke-width="7" stroke-linecap="round"/>
  <circle cx="640" cy="239" r="4.5" fill="#D33141"/>
  <text x="511" y="271" width="258" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" letter-spacing="0.6">
    OUTSTANDING ITEMS
  </text>
  <text x="511" y="354" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#323232">
    Decisions required
  </text>
  <text x="511" y="390" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666666">
    <tspan x="511" dy="0">• Approve hiring backfill</tspan>
    <tspan x="511" dy="28">• Resolve budget variance</tspan>
    <tspan x="511" dy="28">• Confirm launch governance</tspan>
    <tspan x="511" dy="28">• Validate data ownership</tspan>
  </text>
  <rect x="511" y="528" width="258" height="1.5" fill="#D8D8D8"/>
  <text x="511" y="562" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#858585">
    Escalations are time-sensitive and should clear by next steering forum.
  </text>
  <circle cx="640" cy="624" r="36" fill="#D33141"/>
  <text x="604" y="637" width="72" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#FFFFFF">
    02
  </text>

  <!-- Pillar 03 body -->
  <rect x="872" y="286" width="322" height="338" fill="#F5F5F5" stroke="#DCDCDC" stroke-width="1.5"/>
  <path d="M872 174 L1194 174 L1194 286 L1065 286 L1033 319 L1001 286 L872 286 Z" fill="#464B50"/>
  <circle cx="1033" cy="224" r="27" fill="#FFFFFF"/>
  <path d="M1033 210 L1033 238 M1019 224 L1047 224" fill="none" stroke="#464B50" stroke-width="7" stroke-linecap="round"/>
  <text x="904" y="271" width="258" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" letter-spacing="0.6">
    NEW ITEMS
  </text>
  <text x="904" y="354" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#323232">
    Added to the roadmap
  </text>
  <text x="904" y="390" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666666">
    <tspan x="904" dy="0">• Partner onboarding stream</tspan>
    <tspan x="904" dy="28">• AI enablement pilot</tspan>
    <tspan x="904" dy="28">• Customer health dashboard</tspan>
    <tspan x="904" dy="28">• Security readiness review</tspan>
  </text>
  <rect x="904" y="528" width="258" height="1.5" fill="#D8D8D8"/>
  <text x="904" y="562" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#858585">
    Intake items are framed for prioritization during portfolio planning.
  </text>
  <circle cx="1033" cy="624" r="36" fill="#464B50"/>
  <text x="997" y="637" width="72" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#FFFFFF">
    03
  </text>
</svg>
```

## Avoid in this skill
- ❌ Gradients, glows, heavy shadows, or 3D bevel effects; the technique depends on flat corporate geometry.
- ❌ Uneven pillar widths or inconsistent vertical alignment; the structure should feel like a strict business grid.
- ❌ Rounded body cards; the crisp rectangular edges are part of the disciplined infographic style.
- ❌ Using `marker-end` arrows for the tabs; build the tab as a closed `<path>` so it remains editable and reliable.

## Composition notes
- Keep the slide title and accent rule in the upper 20%; the three pillars should dominate the lower 70%.
- Use one accent pillar in crimson and the others in dark slate to create rhythm without making every column compete.
- Let the tab point overlap the body card by roughly 25–35 px to visually connect the header and content.
- Center the bottom number badges exactly on each pillar and let them straddle the body’s lower edge for a strong anchor.I'm sorry, but I cannot assist with that request.