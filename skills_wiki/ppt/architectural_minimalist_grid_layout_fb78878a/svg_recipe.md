# SVG Recipe — Architectural Minimalist Grid Layout

## Visual mechanism
A strict editorial grid divides a white canvas into disciplined information zones, using fine charcoal wireframes and tiny uppercase labels to create an architectural-board feeling. One large central diagram acts as the focal “perspective,” while a single vibrant accent color repeats across small diagrams, data ticks, and section highlights to unify the whole slide.

## SVG primitives needed
- 1× `<rect>` for the pure white canvas background
- 5× `<rect>` for thin-stroked content panels/cards
- 7× `<rect>` for accent bars, data blocks, and label chips
- 30× `<line>` for the invisible-feeling construction grid, gutters, axes, rulers, and data ticks
- 24× `<path>` for architectural wireframe diagrams: site plan, central perspective, section cutaway, circulation arrows, and analytic shapes
- 1× `<linearGradient id="accentWash">` for subtle yellow accent fills
- 1× `<filter id="accentGlow">` with `feGaussianBlur` for a restrained luminous accent on the central form
- 17× `<text>` for uppercase title, micro labels, numerical callouts, and captions, each with explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFE36A"/>
      <stop offset="60%" stop-color="#FFD400"/>
      <stop offset="100%" stop-color="#FFB800"/>
    </linearGradient>
    <filter id="accentGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- faint architectural construction grid -->
  <g stroke="#F1F1F1" stroke-width="1">
    <line x1="72" y1="110" x2="1208" y2="110"/>
    <line x1="72" y1="150" x2="1208" y2="150"/>
    <line x1="72" y1="190" x2="1208" y2="190"/>
    <line x1="72" y1="230" x2="1208" y2="230"/>
    <line x1="72" y1="270" x2="1208" y2="270"/>
    <line x1="72" y1="310" x2="1208" y2="310"/>
    <line x1="72" y1="350" x2="1208" y2="350"/>
    <line x1="72" y1="390" x2="1208" y2="390"/>
    <line x1="72" y1="430" x2="1208" y2="430"/>
    <line x1="72" y1="470" x2="1208" y2="470"/>
    <line x1="72" y1="510" x2="1208" y2="510"/>
    <line x1="72" y1="550" x2="1208" y2="550"/>
    <line x1="72" y1="590" x2="1208" y2="590"/>
    <line x1="72" y1="630" x2="1208" y2="630"/>
    <line x1="72" y1="110" x2="72" y2="650"/>
    <line x1="332" y1="110" x2="332" y2="650"/>
    <line x1="380" y1="110" x2="380" y2="650"/>
    <line x1="900" y1="110" x2="900" y2="650"/>
    <line x1="948" y1="110" x2="948" y2="650"/>
    <line x1="1208" y1="110" x2="1208" y2="650"/>
  </g>

  <!-- header -->
  <text x="72" y="62" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" letter-spacing="4" fill="#212121">URBAN RENEWAL HUB</text>
  <text x="74" y="91" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="10" letter-spacing="2.2" fill="#8C8C8C">PROBLEM → SOLUTION → RESILIENT CITY SYSTEM</text>
  <rect x="980" y="44" width="74" height="8" fill="url(#accentWash)"/>
  <text x="1066" y="53" width="142" font-family="Segoe UI, Microsoft YaHei" font-size="10" letter-spacing="2" fill="#212121">GRID INDEX 04</text>

  <!-- panel frames -->
  <rect x="72" y="150" width="260" height="180" fill="#FFFFFF" stroke="#2A2A2A" stroke-width="1.2"/>
  <rect x="72" y="390" width="260" height="180" fill="#FFFFFF" stroke="#2A2A2A" stroke-width="1.2"/>
  <rect x="380" y="150" width="520" height="420" fill="#FFFFFF" stroke="#212121" stroke-width="1.4"/>
  <rect x="948" y="150" width="260" height="180" fill="#FFFFFF" stroke="#2A2A2A" stroke-width="1.2"/>
  <rect x="948" y="390" width="260" height="180" fill="#FFFFFF" stroke="#2A2A2A" stroke-width="1.2"/>

  <!-- micro labels -->
  <text x="72" y="138" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="10" letter-spacing="2" fill="#212121">01 / SITE PLAN</text>
  <text x="72" y="378" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="10" letter-spacing="2" fill="#212121">02 / SECTION CUT</text>
  <text x="380" y="138" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="10" letter-spacing="2" fill="#212121">03 / CENTRAL PERSPECTIVE</text>
  <text x="948" y="138" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="10" letter-spacing="2" fill="#212121">04 / FLOW METRICS</text>
  <text x="948" y="378" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="10" letter-spacing="2" fill="#212121">05 / PROGRAM LOGIC</text>

  <!-- left top: site plan -->
  <g stroke="#333333" stroke-width="1.4" fill="none">
    <path d="M100 182 L300 190 L292 305 L112 292 Z"/>
    <path d="M124 205 L278 210 L264 281 L138 270 Z" fill="#F4F4F4"/>
    <path d="M148 228 L208 222 L232 260 L172 272 Z" fill="url(#accentWash)" stroke="#333333"/>
    <path d="M104 252 C145 244 183 245 226 236 C250 231 276 232 298 224" stroke-dasharray="4 4"/>
    <path d="M116 292 L170 252 L226 236 L292 305"/>
    <path d="M132 194 L132 316"/>
    <path d="M260 190 L260 304"/>
  </g>
  <rect x="92" y="310" width="42" height="5" fill="#FFD400"/>
  <text x="148" y="316" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#777777">active civic core within existing block</text>

  <!-- left bottom: section cut -->
  <g stroke="#333333" stroke-width="1.5" fill="none">
    <path d="M98 532 L308 532" stroke-width="8"/>
    <path d="M120 510 L300 510"/>
    <path d="M132 448 L132 510 L202 510 L202 448 Z"/>
    <path d="M202 474 L282 474 L282 510 L202 510"/>
    <path d="M148 463 L188 463 L188 486 L148 486 Z" fill="url(#accentWash)" stroke="#333333"/>
    <path d="M132 486 L202 486"/>
    <path d="M132 466 L202 466"/>
    <path d="M222 488 L264 488"/>
    <path d="M98 432 L310 432" stroke="#D9D9D9" stroke-dasharray="3 5"/>
  </g>
  <text x="94" y="418" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#777777">street / plinth / public roof</text>
  <text x="218" y="553" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="9" letter-spacing="1.2" fill="#212121">+18.0 M</text>

  <!-- center: large perspective diagram -->
  <g stroke="#212121" stroke-width="1.5" fill="none">
    <line x1="404" y1="455" x2="876" y2="455"/>
    <line x1="640" y1="210" x2="640" y2="544" stroke="#BDBDBD" stroke-dasharray="4 6"/>
    <path d="M458 526 L528 258 L752 258 L830 526 Z" fill="#F5F5F5"/>
    <path d="M528 258 L640 214 L752 258"/>
    <path d="M458 526 L640 214 L830 526"/>
    <path d="M528 258 L528 526"/>
    <path d="M752 258 L752 526"/>
    <path d="M492 396 L788 396"/>
    <path d="M512 318 L766 318"/>
    <path d="M484 448 L802 448"/>
    <path d="M548 526 L592 304 L688 304 L736 526 Z" fill="url(#accentWash)" stroke="#333333" filter="url(#accentGlow)"/>
    <path d="M592 304 L640 282 L688 304"/>
    <path d="M592 304 L736 526"/>
    <path d="M688 304 L548 526"/>
    <path d="M430 526 C500 490 570 480 640 455 C708 431 770 414 854 370" stroke="#9A9A9A" stroke-dasharray="5 7"/>
    <path d="M428 526 C516 545 676 548 852 526" stroke="#9A9A9A"/>
  </g>
  <rect x="406" y="166" width="70" height="7" fill="#FFD400"/>
  <text x="492" y="174" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="10" letter-spacing="2" fill="#212121">PRIMARY PUBLIC VOLUME</text>
  <text x="410" y="548" width="208" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#777777">wireframe massing with highlighted civic atrium</text>

  <!-- right top: flow metrics -->
  <g stroke="#333333" stroke-width="1.2" fill="none">
    <line x1="990" y1="292" x2="1168" y2="292"/>
    <line x1="990" y1="192" x2="990" y2="292"/>
    <line x1="1026" y1="292" x2="1026" y2="282"/>
    <line x1="1062" y1="292" x2="1062" y2="274"/>
    <line x1="1098" y1="292" x2="1098" y2="262"/>
    <line x1="1134" y1="292" x2="1134" y2="244"/>
    <path d="M990 270 C1024 258 1048 254 1076 235 C1102 218 1128 204 1168 197"/>
    <path d="M990 246 C1030 250 1057 239 1088 220 C1115 204 1139 191 1168 188" stroke="#FFD400" stroke-width="3"/>
  </g>
  <rect x="1018" y="260" width="18" height="32" fill="#FFD400"/>
  <rect x="1054" y="242" width="18" height="50" fill="#FFD400"/>
  <rect x="1090" y="224" width="18" height="68" fill="#FFD400"/>
  <rect x="1126" y="204" width="18" height="88" fill="#FFD400"/>
  <text x="986" y="178" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="9" letter-spacing="1.5" fill="#777777">PEDESTRIAN CAPTURE</text>
  <text x="1148" y="202" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#212121">+42%</text>

  <!-- right bottom: program logic -->
  <g stroke="#333333" stroke-width="1.2" fill="none">
    <path d="M990 430 L1066 430 L1066 478 L990 478 Z" fill="#F6F6F6"/>
    <path d="M1092 430 L1168 430 L1168 478 L1092 478 Z" fill="#F6F6F6"/>
    <path d="M990 502 L1066 502 L1066 546 L990 546 Z" fill="url(#accentWash)"/>
    <path d="M1092 502 L1168 502 L1168 546 L1092 546 Z" fill="#F6F6F6"/>
    <line x1="1066" y1="454" x2="1092" y2="454"/>
    <line x1="1028" y1="478" x2="1028" y2="502"/>
    <line x1="1130" y1="478" x2="1130" y2="502"/>
    <path d="M1028 502 C1054 488 1102 488 1130 502" stroke="#FFD400" stroke-width="2.5"/>
  </g>
  <text x="1002" y="458" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="9" text-anchor="middle" fill="#212121">TRANSIT</text>
  <text x="1130" y="458" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="9" text-anchor="middle" fill="#212121">MARKET</text>
  <text x="1028" y="529" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="9" text-anchor="middle" fill="#212121">CIVIC</text>
  <text x="1130" y="529" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="9" text-anchor="middle" fill="#212121">HOUSING</text>

  <!-- footer and vertical annotation -->
  <line x1="72" y1="650" x2="1208" y2="650" stroke="#212121" stroke-width="1"/>
  <text x="72" y="676" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="10" letter-spacing="1.6" fill="#777777">MINIMAL GRID BOARD — monochrome information system with one chromatic anchor</text>
  <text x="1210" y="650" width="220" transform="rotate(-90 1210 650)" font-family="Segoe UI, Microsoft YaHei" font-size="9" letter-spacing="2" fill="#9A9A9A">NEGATIVE SPACE IS THE PRIMARY STRUCTURE</text>
</svg>
```

## Avoid in this skill
- ❌ Dense chart junk, heavy fills, or multicolor palettes; this layout depends on restraint and one accent color only.
- ❌ Photo-heavy collages unless images are converted into clean clipped monochrome architectural assets.
- ❌ Applying `filter` to `<line>` grid strokes; use filters only on accent `<path>`, `<rect>`, or text.
- ❌ Using `<pattern>` for the construction grid; draw faint editable `<line>` elements instead.
- ❌ Overfilling the margins with annotations; the premium effect comes from generous white space.

## Composition notes
- Keep a rigid three-zone structure: small support diagrams left, dominant perspective in the center, metrics/logic on the right.
- Use wide gutters and tiny uppercase captions to make the slide feel like an exhibition board rather than a dashboard.
- Repeat the accent color exactly 4–6 times: one major central highlight plus small data and label echoes.
- Let white space occupy at least half the canvas; the grid should feel precise but almost invisible.