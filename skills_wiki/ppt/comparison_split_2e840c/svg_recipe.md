# SVG Recipe — Comparison Split

## Visual mechanism
A centered vertical spine acts as the decision axis, with mirrored pill-shaped comparison bars extending left and right for each feature. Each row uses a central dimension chip, colored product-side bars, and small node accents to make differences scannable without collapsing into a table.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 3× `<path>` for subtle atmospheric background blobs and curved light sweeps
- 2× `<rect>` for left and right product header cards
- 10× `<rect>` for mirrored horizontal pill bars across five comparison dimensions
- 5× `<rect>` for central dimension label chips
- 1× `<rect>` for the central vertical spine
- 5× `<circle>` for spine nodes aligned to each comparison row
- 10× `<circle>` for colored bar-end accent dots
- 2× `<line>` for faint top connector rules under product headers
- Multiple `<text>` elements with explicit `width` attributes for headline, product names, descriptions, feature labels, and values
- 3× `<linearGradient>` for background, left-side bars, and right-side bars
- 1× `<radialGradient>` for central glow
- 2× `<filter>` definitions for soft shadows and glow, applied only to rect/path/circle/text elements

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#071528"/>
      <stop offset="0.48" stop-color="#0E2137"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="leftBar" x1="180" y1="0" x2="560" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#1D4ED8"/>
      <stop offset="1" stop-color="#38BDF8"/>
    </linearGradient>
    <linearGradient id="rightBar" x1="720" y1="0" x2="1100" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#A855F7"/>
      <stop offset="1" stop-color="#EC4899"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="640" cy="385" r="330" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#38BDF8" stop-opacity="0.28"/>
      <stop offset="0.55" stop-color="#2563EB" stop-opacity="0.09"/>
      <stop offset="1" stop-color="#020617" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-25%" y="-35%" width="150%" height="180%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>

  <path d="M-80,122 C120,40 232,145 402,84 C555,28 664,20 812,76 C984,142 1094,80 1362,38 L1362,0 L-80,0 Z"
        fill="#60A5FA" opacity="0.08"/>
  <path d="M-120,632 C130,552 260,690 470,615 C690,536 835,608 1012,560 C1138,526 1224,512 1400,586 L1400,720 L-120,720 Z"
        fill="#A78BFA" opacity="0.09"/>
  <path d="M96,404 C256,306 403,346 528,260 C686,150 839,190 1004,132 C1104,97 1178,91 1236,111"
        fill="none" stroke="#93C5FD" stroke-width="2" opacity="0.14"/>

  <text x="80" y="72" width="1120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#F8FAFC">
    Platform Comparison: Autonomous AI Ops vs Managed Human Ops
  </text>
  <text x="82" y="110" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#A7B5C8">
    A direct split view for evaluating two competing operating models across the same decision dimensions.
  </text>

  <rect x="82" y="148" width="472" height="76" rx="24" fill="#0F2A46" opacity="0.92" filter="url(#softShadow)"/>
  <rect x="92" y="158" width="8" height="56" rx="4" fill="#38BDF8"/>
  <text x="116" y="181" width="400" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="700" fill="#E0F2FE">
    Autonomous AI Ops
  </text>
  <text x="116" y="207" width="400" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#B6C7DA">
    Software-led automation with continuous learning and policy guardrails.
  </text>

  <rect x="726" y="148" width="472" height="76" rx="24" fill="#211433" opacity="0.92" filter="url(#softShadow)"/>
  <rect x="1180" y="158" width="8" height="56" rx="4" fill="#EC4899"/>
  <text x="766" y="181" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="700" fill="#FCE7F3">
    Managed Human Ops
  </text>
  <text x="766" y="207" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CDBDD7">
    Specialist teams execute workflows with expert oversight and escalation.
  </text>

  <line x1="138" y1="246" x2="548" y2="246" stroke="#38BDF8" stroke-width="1.5" stroke-opacity="0.26" stroke-dasharray="7 8"/>
  <line x1="732" y1="246" x2="1142" y2="246" stroke="#EC4899" stroke-width="1.5" stroke-opacity="0.26" stroke-dasharray="7 8"/>

  <rect x="633" y="236" width="14" height="340" rx="7" fill="#E2E8F0" opacity="0.18"/>
  <rect x="637" y="236" width="6" height="340" rx="3" fill="#F8FAFC" opacity="0.44"/>

  <rect x="204" y="266" width="350" height="46" rx="23" fill="url(#leftBar)" opacity="0.95" filter="url(#softShadow)"/>
  <rect x="726" y="266" width="350" height="46" rx="23" fill="url(#rightBar)" opacity="0.95" filter="url(#softShadow)"/>
  <rect x="565" y="260" width="150" height="58" rx="19" fill="#101B2C" stroke="#334155" stroke-width="1.2"/>
  <circle cx="640" cy="289" r="10" fill="#F8FAFC" opacity="0.95"/>
  <circle cx="540" cy="289" r="7" fill="#E0F2FE"/>
  <circle cx="740" cy="289" r="7" fill="#FCE7F3"/>
  <text x="246" y="295" width="268" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">Sub-second remediation loops</text>
  <text x="766" y="295" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">Minutes to hours via queue</text>
  <text x="586" y="294" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#CBD5E1">Latency</text>

  <rect x="246" y="336" width="308" height="46" rx="23" fill="url(#leftBar)" opacity="0.88" filter="url(#softShadow)"/>
  <rect x="726" y="336" width="380" height="46" rx="23" fill="url(#rightBar)" opacity="0.95" filter="url(#softShadow)"/>
  <rect x="565" y="330" width="150" height="58" rx="19" fill="#101B2C" stroke="#334155" stroke-width="1.2"/>
  <circle cx="640" cy="359" r="10" fill="#F8FAFC" opacity="0.95"/>
  <circle cx="540" cy="359" r="7" fill="#E0F2FE"/>
  <circle cx="740" cy="359" r="7" fill="#FCE7F3"/>
  <text x="286" y="365" width="226" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">Algorithmic guardrails</text>
  <text x="766" y="365" width="292" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">Senior expert judgment</text>
  <text x="586" y="364" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#CBD5E1">Supervision</text>

  <rect x="184" y="406" width="370" height="46" rx="23" fill="url(#leftBar)" opacity="0.95" filter="url(#softShadow)"/>
  <rect x="726" y="406" width="320" height="46" rx="23" fill="url(#rightBar)" opacity="0.9" filter="url(#softShadow)"/>
  <rect x="565" y="400" width="150" height="58" rx="19" fill="#101B2C" stroke="#334155" stroke-width="1.2"/>
  <circle cx="640" cy="429" r="10" fill="#F8FAFC" opacity="0.95"/>
  <circle cx="540" cy="429" r="7" fill="#E0F2FE"/>
  <circle cx="740" cy="429" r="7" fill="#FCE7F3"/>
  <text x="226" y="435" width="286" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">Elastic across all workloads</text>
  <text x="766" y="435" width="238" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">Limited by staffing model</text>
  <text x="586" y="434" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#CBD5E1">Scale</text>

  <rect x="266" y="476" width="288" height="46" rx="23" fill="url(#leftBar)" opacity="0.86" filter="url(#softShadow)"/>
  <rect x="726" y="476" width="364" height="46" rx="23" fill="url(#rightBar)" opacity="0.95" filter="url(#softShadow)"/>
  <rect x="565" y="470" width="150" height="58" rx="19" fill="#101B2C" stroke="#334155" stroke-width="1.2"/>
  <circle cx="640" cy="499" r="10" fill="#F8FAFC" opacity="0.95"/>
  <circle cx="540" cy="499" r="7" fill="#E0F2FE"/>
  <circle cx="740" cy="499" r="7" fill="#FCE7F3"/>
  <text x="306" y="505" width="214" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">Lower variable cost</text>
  <text x="766" y="505" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">Predictable service retainer</text>
  <text x="586" y="504" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#CBD5E1">Cost Model</text>

  <rect x="224" y="546" width="330" height="46" rx="23" fill="url(#leftBar)" opacity="0.92" filter="url(#softShadow)"/>
  <rect x="726" y="546" width="342" height="46" rx="23" fill="url(#rightBar)" opacity="0.92" filter="url(#softShadow)"/>
  <rect x="565" y="540" width="150" height="58" rx="19" fill="#101B2C" stroke="#334155" stroke-width="1.2"/>
  <circle cx="640" cy="569" r="10" fill="#F8FAFC" opacity="0.95"/>
  <circle cx="540" cy="569" r="7" fill="#E0F2FE"/>
  <circle cx="740" cy="569" r="7" fill="#FCE7F3"/>
  <text x="266" y="575" width="252" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">APIs, logs, telemetry fabric</text>
  <text x="766" y="575" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="650" fill="#FFFFFF">Runbooks and ticket queues</text>
  <text x="586" y="574" width="108" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#CBD5E1">Integration</text>

  <text x="82" y="655" width="480" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#7DD3FC">
    Best when speed, scale, and telemetry coverage are the buying criteria.
  </text>
  <text x="726" y="655" width="480" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#F9A8D4">
    Best when accountability, exception handling, and domain nuance dominate.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Building the comparison as a plain two-column table; it loses the central “split decision” mechanism.
- ❌ Using identical bar lengths for every row unless the point is perfect parity; slight length variation creates visual hierarchy.
- ❌ Applying filters to `<line>` connector rules; shadows/glows should be on rects, circles, paths, or text only.
- ❌ Putting comparison labels only inside the side bars; every row needs a central dimension chip to keep the mirrored comparison readable.
- ❌ Overloading rows with long paragraphs; this format works best with compact value statements.

## Composition notes
- Keep the central spine fixed around x=640, with a generous 10–20 px gap between the spine/chips and the side bars.
- Put product identities in header cards above the comparison rows; use side-specific colors that repeat through the bars and footer notes.
- Use five rows maximum for executive readability; if more dimensions are required, split into multiple slides.
- Preserve dark negative space around the bars so the colored mirrored pills feel premium rather than like a dense dashboard.