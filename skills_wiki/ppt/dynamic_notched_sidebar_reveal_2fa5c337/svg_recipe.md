# SVG Recipe — Dynamic Notched Sidebar Reveal

## Visual mechanism
A pure-white left sidebar is drawn as a single editable SVG path whose right edge contains a smooth Bezier notch, revealing the vibrant slide background underneath. The active navigation icon sits inside that colored scoop, while the main canvas uses the same color field for a hub-and-spoke content diagram.

## SVG primitives needed
- 1× `<rect>` for the full-slide vibrant background
- 1× `<path>` for the white sidebar with the scooped Bezier notch
- 1× `<filter id="sidebarShadow">` applied to the sidebar path for subtle depth
- 4× `<circle>` for navigation icon hit areas / rings
- 8–12× `<path>` for simple editable line icons inside the sidebar
- 1× `<circle>` for the central hub
- 4× `<line>` for hub-and-spoke connectors
- 4× `<rect>` for rounded content cards around the hub
- 4× `<circle>` for small endpoint badges on the cards
- Multiple `<text>` elements with explicit `width` for section labels, title, metrics, and card copy
- 2× `<linearGradient>` for the background and card fills
- 1× `<filter id="softGlow">` applied to the central hub for a premium luminous effect

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E34A7C"/>
      <stop offset="55%" stop-color="#D64464"/>
      <stop offset="100%" stop-color="#A92E78"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>
    <filter id="sidebarShadow" x="-20%" y="-10%" width="160%" height="120%">
      <feOffset dx="10" dy="0"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- Sidebar: duplicate this path on the next slide and move only the notch Y-coordinates for Morph -->
  <path filter="url(#sidebarShadow)" fill="#FFFFFF"
        d="M0,0 L172,0 L172,216
           C172,238 132,248 122,272
           C109,304 109,336 122,368
           C132,392 172,402 172,424
           L172,720 L0,720 Z"/>

  <!-- Inactive navigation icons -->
  <circle cx="86" cy="120" r="27" fill="#F5F5F7" stroke="#9A9AA1" stroke-width="3"/>
  <path d="M74,124 L86,112 L98,124 M78,124 L78,138 L94,138 L94,124" fill="none" stroke="#777780" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="86" cy="220" r="27" fill="#F5F5F7" stroke="#9A9AA1" stroke-width="3"/>
  <path d="M73,218 L99,218 M73,229 L99,229 M73,207 L99,207" fill="none" stroke="#777780" stroke-width="3" stroke-linecap="round"/>

  <!-- Active icon sits in the colored notch, not on the white sidebar -->
  <circle cx="166" cy="320" r="34" fill="none" stroke="#FFFFFF" stroke-width="4"/>
  <path d="M152,320 C152,312 158,306 166,306 C174,306 180,312 180,320 C180,328 174,334 166,334 C158,334 152,328 152,320 Z" fill="none" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M166,296 L166,306 M166,334 L166,344 M190,320 L180,320 M152,320 L142,320" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>

  <circle cx="86" cy="520" r="27" fill="#F5F5F7" stroke="#9A9AA1" stroke-width="3"/>
  <path d="M74,530 C76,517 82,510 86,510 C90,510 96,517 98,530 M78,530 L94,530 M86,510 L86,498" fill="none" stroke="#777780" stroke-width="3" stroke-linecap="round"/>

  <text x="42" y="650" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#8A8A92" text-anchor="middle">Q3 MENU</text>

  <!-- Main title -->
  <text x="260" y="82" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#FFFFFF">
    Customer Growth Engine
  </text>
  <text x="264" y="120" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#FFE1EA">
    Active section: activation loops, lifecycle signals, and expansion plays
  </text>

  <!-- Hub-and-spoke connectors -->
  <line x1="720" y1="350" x2="468" y2="226" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="2"/>
  <line x1="720" y1="350" x2="994" y2="226" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="2"/>
  <line x1="720" y1="350" x2="468" y2="512" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="2"/>
  <line x1="720" y1="350" x2="994" y2="512" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="2"/>

  <!-- Central glowing hub -->
  <circle cx="720" cy="350" r="88" fill="#FFFFFF" opacity="0.16" filter="url(#softGlow)"/>
  <circle cx="720" cy="350" r="76" fill="none" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="720" cy="350" r="54" fill="#FFFFFF" fill-opacity="0.18" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="2"/>
  <text x="666" y="338" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">CORE</text>
  <text x="653" y="365" width="134" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFE1EA" text-anchor="middle">activation flywheel</text>

  <!-- Spoke cards -->
  <rect x="300" y="156" width="270" height="126" rx="28" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="1.5"/>
  <circle cx="468" cy="226" r="22" fill="#FFFFFF" fill-opacity="0.2" stroke="#FFFFFF" stroke-width="2"/>
  <text x="326" y="198" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">01 · Onboarding</text>
  <text x="326" y="230" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFE1EA">Reduce time-to-value with guided first-run actions.</text>

  <rect x="890" y="156" width="270" height="126" rx="28" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="1.5"/>
  <circle cx="994" cy="226" r="22" fill="#FFFFFF" fill-opacity="0.2" stroke="#FFFFFF" stroke-width="2"/>
  <text x="916" y="198" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">02 · Signals</text>
  <text x="916" y="230" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFE1EA">Track usage moments that predict expansion intent.</text>

  <rect x="300" y="462" width="270" height="126" rx="28" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="1.5"/>
  <circle cx="468" cy="512" r="22" fill="#FFFFFF" fill-opacity="0.2" stroke="#FFFFFF" stroke-width="2"/>
  <text x="326" y="504" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">03 · Nurture</text>
  <text x="326" y="536" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFE1EA">Personalized lifecycle journeys by role and maturity.</text>

  <rect x="890" y="462" width="270" height="126" rx="28" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="1.5"/>
  <circle cx="994" cy="512" r="22" fill="#FFFFFF" fill-opacity="0.2" stroke="#FFFFFF" stroke-width="2"/>
  <text x="916" y="504" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">04 · Expansion</text>
  <text x="916" y="536" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFE1EA">Surface high-fit accounts for sales-assisted upgrades.</text>

  <!-- Small executive metric strip -->
  <rect x="260" y="626" width="860" height="48" rx="24" fill="#FFFFFF" fill-opacity="0.14" stroke="#FFFFFF" stroke-opacity="0.25"/>
  <text x="292" y="657" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#FFFFFF">+18% activation</text>
  <text x="520" y="657" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#FFFFFF">−22% churn risk</text>
  <text x="748" y="657" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#FFFFFF">3.4× expansion propensity</text>
</svg>
```

## Avoid in this skill
- ❌ Using a PNG mask for the sidebar; draw the notched sidebar as a native `<path>` so the notch remains editable and Morph-friendly.
- ❌ Applying `clip-path` to the sidebar path; clipping only translates reliably for `<image>`, not regular shapes.
- ❌ Building the notch from overlapping white rectangles and circles; it will look segmented and will not morph as smoothly as one continuous Bezier path.
- ❌ Putting arrowheads on `<path>` connectors; if arrows are needed, use individual `<line>` elements with `marker-end` directly on each line.
- ❌ Forgetting explicit `width` on `<text>` elements; PowerPoint text boxes may collapse or wrap unpredictably.

## Composition notes
- Reserve the left 14–18% of the canvas for the sidebar; the notch should cut 45–65 px into the white rail and align exactly with the active icon center.
- Keep the active icon on the colored background inside the scoop; inactive icons remain dark gray on white to make the reveal instantly legible.
- Use the large right-hand field for radial content, with the hub slightly right of center to counterbalance the heavy white sidebar.
- For a Morph sequence, duplicate the slide and edit only the notch control points, active icon position, and background gradient colors.