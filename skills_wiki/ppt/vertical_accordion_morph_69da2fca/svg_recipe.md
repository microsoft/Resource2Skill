# SVG Recipe — Vertical Accordion Morph

## Visual mechanism
A set of full-height vertical panels behave like an accordion: one active panel expands into the main content canvas while the remaining sections compress into narrow navigation tabs. Across consecutive PowerPoint slides, keep the same panel IDs/names and change only x-position, width, and text orientation so Morph creates the expansion/compression illusion.

## SVG primitives needed
- 5× `<rect>` for the title tab, four section panels, and the active content surface
- 1× `<linearGradient>` for the active expanded panel’s premium magenta-to-violet fill
- 1× `<filter id="panelShadow">` applied to panels for layered depth
- 1× `<filter id="softGlow">` applied to decorative paths/circles for keynote-style polish
- 1× `<clipPath>` with rounded `<rect>` for a cropped hero image inside the active panel
- 1× `<image>` for an editorial/product photo that appears only inside the expanded panel
- 6× `<path>` for abstract contour lines, accent ribbons, and the active-panel chevron edge
- 5× `<circle>` for numbered navigation badges
- 12× `<text>` with explicit `width` attributes for vertical tab labels, active heading, body copy, and metrics
- 3× `<line>` for small divider/accent rules in the active panel

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="activeGradient" x1="144" y1="0" x2="1136" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#D93672"/>
      <stop offset="0.48" stop-color="#B02071"/>
      <stop offset="1" stop-color="#601550"/>
    </linearGradient>

    <linearGradient id="photoFade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#E9D5E8"/>
    </linearGradient>

    <filter id="panelShadow" x="-10%" y="-5%" width="130%" height="110%">
      <feOffset dx="10" dy="0" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>

    <clipPath id="photoCardClip">
      <rect x="762" y="126" width="300" height="420" rx="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F3F6"/>

  <!-- Collapsed title tab -->
  <rect id="Title_Tab" x="0" y="0" width="72" height="720" fill="#F2F2F2" filter="url(#panelShadow)"/>
  <circle cx="36" cy="54" r="18" fill="#601550"/>
  <text x="36" y="62" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">A</text>
  <text id="Title_Label" x="36" y="620" width="520" transform="rotate(-90 36 620)"
        font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" letter-spacing="2" fill="#601550">
    STRATEGIC ROADMAP
  </text>

  <!-- Inactive tab 01 -->
  <rect id="Panel_01" x="72" y="0" width="72" height="720" fill="#D93672" filter="url(#panelShadow)"/>
  <circle id="Badge_01" cx="108" cy="56" r="20" fill="#FFFFFF" opacity="0.95"/>
  <text x="108" y="64" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D93672">01</text>
  <text id="Label_01" x="108" y="640" width="520" transform="rotate(-90 108 640)"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF" letter-spacing="1.4">
    MARKET SIGNALS
  </text>

  <!-- Active expanded tab 02 -->
  <rect id="Panel_02" x="144" y="0" width="992" height="720" fill="url(#activeGradient)" filter="url(#panelShadow)"/>
  <path d="M144,0 L1136,0 L1094,360 L1136,720 L144,720 Z" fill="url(#activeGradient)" opacity="0.96"/>
  <path d="M250,92 C390,20 510,28 642,104 S898,178 1016,84"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.18"/>
  <path d="M218,160 C408,88 548,122 680,206 S904,292 1050,210"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.14"/>
  <path d="M188,608 C344,518 488,548 624,610 S862,694 1030,604"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.16"/>
  <path d="M640,56 C706,42 752,62 780,104 C720,118 672,106 640,56 Z"
        fill="#FFFFFF" opacity="0.16" filter="url(#softGlow)"/>
  <circle cx="1018" cy="92" r="70" fill="#FFFFFF" opacity="0.08" filter="url(#softGlow)"/>

  <circle id="Badge_02" cx="204" cy="74" r="29" fill="#FFFFFF"/>
  <text x="204" y="84" width="58" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#B02071">02</text>

  <text id="Active_Kicker" x="198" y="140" width="470"
        font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" letter-spacing="3" fill="#F7C7DD">
    ACTIVE SECTION
  </text>
  <text id="Active_Heading" x="196" y="202" width="520"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#FFFFFF">
    <tspan x="196" dy="0">Customer</tspan>
    <tspan x="196" dy="62">Experience</tspan>
    <tspan x="196" dy="62">Redesign</tspan>
  </text>
  <line x1="198" y1="398" x2="638" y2="398" stroke="#FFFFFF" stroke-width="2" opacity="0.45"/>
  <text id="Active_Body" x="198" y="438" width="486"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#FFFFFF" opacity="0.94">
    <tspan x="198" dy="0">Unify product, service, and success touchpoints</tspan>
    <tspan x="198" dy="34">into a single operating rhythm. The expanded</tspan>
    <tspan x="198" dy="34">panel becomes the working canvas while every</tspan>
    <tspan x="198" dy="34">other section remains visible as a compact tab.</tspan>
  </text>

  <rect x="198" y="592" width="142" height="72" rx="18" fill="#FFFFFF" opacity="0.14"/>
  <text x="222" y="625" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">4.8×</text>
  <text x="222" y="650" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFD8EA">faster insight</text>

  <rect x="370" y="592" width="142" height="72" rx="18" fill="#FFFFFF" opacity="0.14"/>
  <text x="394" y="625" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">31%</text>
  <text x="394" y="650" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFD8EA">less friction</text>

  <rect x="542" y="592" width="142" height="72" rx="18" fill="#FFFFFF" opacity="0.14"/>
  <text x="566" y="625" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">90d</text>
  <text x="566" y="650" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFD8EA">pilot window</text>

  <rect x="750" y="114" width="324" height="444" rx="42" fill="#FFFFFF" opacity="0.16"/>
  <image x="762" y="126" width="300" height="420" clip-path="url(#photoCardClip)"
         href="https://images.example.com/executive-keynote/customer-experience-war-room.jpg"/>
  <rect x="762" y="126" width="300" height="420" rx="34" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.45"/>
  <text x="794" y="510" width="236" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">
    FIELD RESEARCH / SERVICE BLUEPRINT
  </text>

  <!-- Inactive tab 03 -->
  <rect id="Panel_03" x="1136" y="0" width="72" height="720" fill="#601550" filter="url(#panelShadow)"/>
  <circle id="Badge_03" cx="1172" cy="56" r="20" fill="#FFFFFF" opacity="0.95"/>
  <text x="1172" y="64" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#601550">03</text>
  <text id="Label_03" x="1172" y="640" width="520" transform="rotate(-90 1172 640)"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF" letter-spacing="1.4">
    OPERATING MODEL
  </text>

  <!-- Inactive tab 04 -->
  <rect id="Panel_04" x="1208" y="0" width="72" height="720" fill="#050505" filter="url(#panelShadow)"/>
  <circle id="Badge_04" cx="1244" cy="56" r="20" fill="#FFFFFF" opacity="0.95"/>
  <text x="1244" y="64" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#050505">04</text>
  <text id="Label_04" x="1244" y="640" width="520" transform="rotate(-90 1244 640)"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF" letter-spacing="1.4">
    INVESTMENT CASE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; the motion should be produced by PowerPoint Morph between separate slides.
- ❌ Do not rely on `<mask>` to fade panels or reveal content; masks can hard-fail translation. Use opacity, gradients, or separate editable shapes instead.
- ❌ Do not put `clip-path` on panel rectangles or decorative shapes; use clipping only on `<image>` elements.
- ❌ Do not use `<use>` to duplicate tabs or badges. Repeat the actual editable primitives so each tab remains independently morphable.
- ❌ Do not apply filters to `<line>` elements. Use filters only on rectangles, paths, circles, ellipses, or text.
- ❌ Do not use `marker-end` on paths for navigation arrows; if arrows are needed, use `<line>` with direct `marker-end`, or draw the arrowhead manually as a small path.

## Composition notes
- Build one SVG per Morph state: opening overview, section 01 active, section 02 active, etc. Keep the same logical object IDs across slides and change panel `x`/`width` values so PowerPoint can interpolate the accordion movement.
- Reserve 72 px per collapsed tab. With four sections plus a title tab, the active panel typically receives 920–1000 px of width, enough for a headline, body copy, metrics, and one strong image card.
- Keep inactive tab labels rotated `-90` degrees and anchored near the lower third so the navigation stays readable without stealing attention from the active content.
- Use a tight analogous palette from pink to plum to black. The active panel may use a gradient, while collapsed tabs should use flatter fills for clear section identity.