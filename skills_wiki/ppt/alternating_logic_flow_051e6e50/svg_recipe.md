# SVG Recipe — Alternating Logic Flow

## Visual mechanism
A vertically split slide stages a debate: warm “concern” pills slide out from the central seam on the left, while cool “resolution” pills answer from the right. The central divider uses soft shadow bands and a white slit to make the content feel as if it is peeking in and out from behind a hidden door.

## SVG primitives needed
- 1× `<rect>` for the full white background
- 2× large translucent `<rect>` panels for subtle left/right territory tinting
- 6× custom `<path>` pill shapes with one rounded outer end and one flat center-facing end
- 6× `<text>` labels inside pills, each with explicit `width`
- 1× narrow white `<rect>` for the central slit cover
- 2× gradient-filled `<rect>` seam shadows to create depth beside the divider
- 1× `<line>` for the fine central highlight
- 2× small `<text>` side labels for “CONCERNS” and “RESOLUTIONS”
- 1× title `<text>` and 1× subtitle `<text>` with explicit widths
- 6× small decorative `<circle>` click-step indicators near the seam
- 1× `<filter id="pillShadow">` applied to pill paths
- 1× `<filter id="seamBlur">` applied to seam shadow rectangles
- 2× `<linearGradient>` definitions for warm/cool pill fills
- 2× `<linearGradient>` definitions for left/right seam depth shadows

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="conFill" x1="160" y1="0" x2="610" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F28A2E"/>
      <stop offset="1" stop-color="#D95E02"/>
    </linearGradient>

    <linearGradient id="proFill" x1="670" y1="0" x2="1120" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#31859C"/>
      <stop offset="1" stop-color="#42A7B8"/>
    </linearGradient>

    <linearGradient id="leftSeamShadow" x1="600" y1="0" x2="640" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.28"/>
    </linearGradient>

    <linearGradient id="rightSeamShadow" x1="640" y1="0" x2="680" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.24"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <filter id="pillShadow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="seamBlur" x="-40%" y="-10%" width="180%" height="120%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <rect x="64" y="122" width="520" height="520" rx="34" fill="#D95E02" opacity="0.045"/>
  <rect x="696" y="122" width="520" height="520" rx="34" fill="#31859C" opacity="0.055"/>

  <text x="72" y="66" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#2F3437">
    Objection → Resolution Flow
  </text>
  <text x="74" y="101" width="810" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#6A737B">
    Reveal one concern, then answer it from the opposite side to control the logic beat-by-beat.
  </text>

  <text x="170" y="157" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2" fill="#B84D05">
    CONCERNS
  </text>
  <text x="768" y="157" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2" fill="#287589">
    RESOLUTIONS
  </text>

  <!-- Left-side pills: rounded on the outside, flat at the center seam -->
  <path filter="url(#pillShadow)" d="M 608 190 L 226 190 A 38 38 0 0 0 226 266 L 608 266 Z" fill="url(#conFill)"/>
  <path filter="url(#pillShadow)" d="M 608 310 L 226 310 A 38 38 0 0 0 226 386 L 608 386 Z" fill="url(#conFill)" opacity="0.93"/>
  <path filter="url(#pillShadow)" d="M 608 430 L 226 430 A 38 38 0 0 0 226 506 L 608 506 Z" fill="url(#conFill)" opacity="0.86"/>

  <!-- Right-side pills: flat at the center seam, rounded on the outside -->
  <path filter="url(#pillShadow)" d="M 672 250 L 1054 250 A 38 38 0 0 1 1054 326 L 672 326 Z" fill="url(#proFill)" opacity="0.94"/>
  <path filter="url(#pillShadow)" d="M 672 370 L 1054 370 A 38 38 0 0 1 1054 446 L 672 446 Z" fill="url(#proFill)"/>
  <path filter="url(#pillShadow)" d="M 672 490 L 1054 490 A 38 38 0 0 1 1054 566 L 672 566 Z" fill="url(#proFill)" opacity="0.88"/>

  <text x="258" y="221" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">
    “Migration feels risky”
  </text>
  <text x="258" y="249" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFE7D6">
    legacy systems, downtime, adoption friction
  </text>

  <text x="258" y="341" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">
    “Costs may expand”
  </text>
  <text x="258" y="369" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFE7D6">
    uncertainty around licenses and services
  </text>

  <text x="258" y="461" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">
    “Teams are overloaded”
  </text>
  <text x="258" y="489" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFE7D6">
    limited time for process change
  </text>

  <text x="710" y="281" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">
    Phased rollout lowers risk
  </text>
  <text x="710" y="309" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D9F6FA">
    pilot, validate, expand only after proof
  </text>

  <text x="710" y="401" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">
    Fixed-value packages
  </text>
  <text x="710" y="429" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D9F6FA">
    scope capped to measurable milestones
  </text>

  <text x="710" y="521" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">
    Enablement is embedded
  </text>
  <text x="710" y="549" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D9F6FA">
    playbooks and coaching ship with delivery
  </text>

  <!-- Central seam overlays the flat pill ends, creating the peek-from-divider illusion -->
  <rect x="602" y="0" width="38" height="720" fill="url(#leftSeamShadow)" filter="url(#seamBlur)" opacity="0.72"/>
  <rect x="640" y="0" width="38" height="720" fill="url(#rightSeamShadow)" filter="url(#seamBlur)" opacity="0.68"/>
  <rect x="626" y="0" width="28" height="720" fill="#FFFFFF"/>
  <line x1="640" y1="120" x2="640" y2="612" stroke="#E7EBEF" stroke-width="2"/>

  <!-- Click-step dots show the intended alternating animation rhythm -->
  <circle cx="640" cy="228" r="9" fill="#D95E02"/>
  <circle cx="640" cy="288" r="9" fill="#31859C"/>
  <circle cx="640" cy="348" r="9" fill="#D95E02"/>
  <circle cx="640" cy="408" r="9" fill="#31859C"/>
  <circle cx="640" cy="468" r="9" fill="#D95E02"/>
  <circle cx="640" cy="528" r="9" fill="#31859C"/>

  <text x="568" y="628" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7D858C" text-anchor="middle">
    alternate on each click
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` to simulate the reveal; create the editable end-state shapes in SVG, then apply PowerPoint “Peek In / Peek Out” animations after translation.
- ❌ Do not use `<mask>` to hide the pill ends behind the seam; use an ordinary white center `<rect>` overlay instead.
- ❌ Do not use `clip-path` on the pill paths; clipping only translates reliably for images.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for angled movement cues; keep the seam and pills orthogonal for reliable PPT editing.
- ❌ Do not put arrowheads on `<path>` elements; if directional arrows are needed, use `<line>` with marker settings directly on each line, or draw small triangle paths manually.

## Composition notes
- Keep the central 40–70 px as a protected “mechanical seam”; let pill shapes tuck underneath it so the audience believes they emerge from the divider.
- Use warm color on the objection side and cool color on the answer side; the contrast is the visual logic of the argument.
- Stagger vertical positions slightly between left and right pills to imply a call-and-response rhythm rather than a static comparison table.
- Leave generous white space above for the title and around the outer pill edges; the focus should remain on the center-out reveal motion.