# SVG Recipe — Central Spine Dual Comparison

## Visual mechanism
A balanced two-column comparison is anchored by a vertical center spine made of stacked, interlocking geometric blocks. Warm left-side ribs and cool right-side ribs branch outward from the spine, creating a structured “A vs. B” funnel that reads as parallel, equal-weight evidence.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 4× `<rect>` for subtle horizontal row divider bands
- 4× `<path>` for central spine shadow/backplate silhouettes
- 8× `<path>` for split-color central spine faces, warm on the left and cool on the right
- 8× `<path>` for angled branching comparison ribs
- 4× `<circle>` for numbered milestone badges on the spine
- 1× `<line>` for the thin vertical center seam
- Multiple `<text>` elements with explicit `width` for title, option headers, rib labels, descriptions, and numbers
- 4× `<linearGradient>` for warm and cool rib/spine depth
- 1× `<filter id="spineShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for spine elevation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="warmRib" x1="120" y1="0" x2="600" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F0A184"/>
      <stop offset="1" stop-color="#CD534C"/>
    </linearGradient>
    <linearGradient id="coolRib" x1="680" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2999AF"/>
      <stop offset="1" stop-color="#86D3DE"/>
    </linearGradient>
    <linearGradient id="warmSpine" x1="584" y1="0" x2="640" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#E77F68"/>
      <stop offset="1" stop-color="#B9423F"/>
    </linearGradient>
    <linearGradient id="coolSpine" x1="640" y1="0" x2="696" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#237F96"/>
      <stop offset="1" stop-color="#68C3D3"/>
    </linearGradient>
    <filter id="spineShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="128" width="1280" height="42" fill="#F1F2F4"/>
  <rect x="0" y="262" width="1280" height="42" fill="#F1F2F4"/>
  <rect x="0" y="396" width="1280" height="42" fill="#F1F2F4"/>
  <rect x="0" y="530" width="1280" height="42" fill="#F1F2F4"/>

  <text x="0" y="54" width="1280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#4B4F56">OPTION A VS OPTION B COMPARISON</text>
  <text x="105" y="102" width="430" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#CD534C">OPTION A</text>
  <text x="745" y="102" width="430" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#2999AF">OPTION B</text>

  <path d="M590 140 L245 140 L185 190 L590 190 Z" fill="url(#warmRib)"/>
  <path d="M690 140 L1035 140 L1095 190 L690 190 Z" fill="url(#coolRib)"/>
  <path d="M590 274 L300 274 L250 324 L590 324 Z" fill="url(#warmRib)" opacity="0.94"/>
  <path d="M690 274 L980 274 L1030 324 L690 324 Z" fill="url(#coolRib)" opacity="0.94"/>
  <path d="M590 408 L355 408 L315 458 L590 458 Z" fill="url(#warmRib)" opacity="0.9"/>
  <path d="M690 408 L925 408 L965 458 L690 458 Z" fill="url(#coolRib)" opacity="0.9"/>
  <path d="M590 542 L410 542 L380 592 L590 592 Z" fill="url(#warmRib)" opacity="0.86"/>
  <path d="M690 542 L870 542 L900 592 L690 592 Z" fill="url(#coolRib)" opacity="0.86"/>

  <path d="M640 120 L584 154 L584 202 L640 236 L696 202 L696 154 Z" fill="#FFFFFF" filter="url(#spineShadow)"/>
  <path d="M640 254 L584 288 L584 336 L640 370 L696 336 L696 288 Z" fill="#FFFFFF" filter="url(#spineShadow)"/>
  <path d="M640 388 L584 422 L584 470 L640 504 L696 470 L696 422 Z" fill="#FFFFFF" filter="url(#spineShadow)"/>
  <path d="M640 522 L584 556 L584 604 L640 638 L696 604 L696 556 Z" fill="#FFFFFF" filter="url(#spineShadow)"/>

  <path d="M640 120 L584 154 L584 202 L640 236 Z" fill="url(#warmSpine)"/>
  <path d="M640 120 L696 154 L696 202 L640 236 Z" fill="url(#coolSpine)"/>
  <path d="M640 254 L584 288 L584 336 L640 370 Z" fill="url(#warmSpine)"/>
  <path d="M640 254 L696 288 L696 336 L640 370 Z" fill="url(#coolSpine)"/>
  <path d="M640 388 L584 422 L584 470 L640 504 Z" fill="url(#warmSpine)"/>
  <path d="M640 388 L696 422 L696 470 L640 504 Z" fill="url(#coolSpine)"/>
  <path d="M640 522 L584 556 L584 604 L640 638 Z" fill="url(#warmSpine)"/>
  <path d="M640 522 L696 556 L696 604 L640 638 Z" fill="url(#coolSpine)"/>

  <line x1="640" y1="112" x2="640" y2="646" stroke="#FFFFFF" stroke-width="3" opacity="0.72"/>

  <circle cx="640" cy="178" r="24" fill="#FFFFFF"/>
  <circle cx="640" cy="312" r="24" fill="#FFFFFF"/>
  <circle cx="640" cy="446" r="24" fill="#FFFFFF"/>
  <circle cx="640" cy="580" r="24" fill="#FFFFFF"/>
  <text x="640" y="187" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#4B4F56">1</text>
  <text x="640" y="321" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#4B4F56">2</text>
  <text x="640" y="455" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#4B4F56">3</text>
  <text x="640" y="589" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#4B4F56">4</text>

  <text x="120" y="158" width="420" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Lower implementation cost</text>
  <text x="130" y="216" width="395" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6F747C">Uses the current stack and avoids new procurement cycles.</text>
  <text x="760" y="158" width="420" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Higher automation ceiling</text>
  <text x="755" y="216" width="395" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6F747C">Creates room for scale, orchestration, and AI-assisted workflows.</text>

  <text x="175" y="292" width="365" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Faster path to launch</text>
  <text x="165" y="350" width="360" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6F747C">Can ship as an incremental release with limited retraining.</text>
  <text x="760" y="292" width="365" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Stronger long-term platform</text>
  <text x="755" y="350" width="360" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6F747C">Standardizes data models and reduces future integration friction.</text>

  <text x="230" y="426" width="310" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Minimal change risk</text>
  <text x="205" y="484" width="320" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6F747C">Stakeholders keep familiar workflows and approval paths.</text>
  <text x="760" y="426" width="310" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Cleaner governance model</text>
  <text x="755" y="484" width="320" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6F747C">A single operating model improves ownership and reporting.</text>

  <text x="285" y="560" width="255" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Best for near-term ROI</text>
  <text x="245" y="618" width="280" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6F747C">Optimizes for savings visible within the next two quarters.</text>
  <text x="760" y="560" width="255" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Best for strategic scale</text>
  <text x="755" y="618" width="280" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6F747C">Optimizes for enterprise leverage over a multi-year horizon.</text>
</svg>
```

## Avoid in this skill
- ❌ Using ordinary rectangles for the ribs; the angled cuts are what create the funnel-like comparison structure.
- ❌ Letting one side visually dominate with larger text blocks or brighter colors; the comparison should feel intentionally balanced.
- ❌ Applying filters to `<line>` elements for the center seam; use a simple flat line instead.
- ❌ Placing text without explicit `width`; comparison labels and descriptions need predictable PowerPoint text-box sizing.
- ❌ Using `marker-end` arrows for the ribs; build the directional effect with polygonal `<path>` geometry instead.

## Composition notes
- Keep the central spine on the exact horizontal midpoint, with warm geometry touching its left edge and cool geometry touching its right edge.
- The top ribs should extend farthest outward; each lower row should become slightly shorter to create the stepped funnel effect.
- Use pale gray row bands sparingly behind the structure so the colored ribs and central spine remain the focus.
- Put concise feature labels on the colored ribs and secondary explanation text just outside or below them in neutral gray.