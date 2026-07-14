# SVG Recipe — Sliced Number Infographic

## Visual mechanism
Use oversized, ultra-bold numbers as structural anchors, then fake a diagonal “cut” by layering a soft blurred ellipse shadow and a background-colored rotated rectangle over the lower portion of each numeral. The slice creates depth while leaving a clean content zone for an icon, title, and short explanatory copy.

## SVG primitives needed
- 1× `<rect>` for the slide background.
- 2× decorative `<path>` elements for subtle premium background motion.
- 8× large `<text>` elements for the oversized colored numbers.
- 8× blurred `<ellipse>` elements for the soft diagonal cut shadow.
- 8× rotated `<rect>` elements filled with the exact background color to hide the lower number half.
- 8× `<circle>` elements for icon badges.
- 8× small `<path>` icon drawings inside the badges.
- 16× supporting `<text>` elements for item titles and descriptions.
- 1× `<filter id="cutShadow">` using `feGaussianBlur` for the soft slice shadow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="cutShadow" x="-60%" y="-200%" width="220%" height="500%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F7F5"/>
  <path d="M-80,110 C120,30 235,120 410,70 C590,20 710,-30 890,42 C1040,102 1170,20 1360,65 L1360,0 L-80,0 Z"
        fill="#FFFFFF" opacity="0.58"/>
  <path d="M1010,735 C1088,610 1210,590 1338,650 L1338,735 Z"
        fill="#E9ECE8" opacity="0.7"/>

  <g transform="translate(55 55)">
    <text x="0" y="174" width="130" font-family="Segoe UI Black, Arial Black, Microsoft YaHei" font-size="205" font-weight="900" fill="#76BB02">1</text>
    <ellipse cx="80" cy="176" rx="86" ry="11" fill="#000000" opacity="0.24" filter="url(#cutShadow)" transform="rotate(-13 80 176)"/>
    <rect x="-46" y="175" width="225" height="135" fill="#F7F7F5" transform="rotate(-13 80 175)"/>
    <circle cx="150" cy="106" r="23" fill="#76BB02"/>
    <path d="M142,101 a8,8 0 1,0 16,0 a8,8 0 1,0 -16,0 M157,112 L166,121" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
    <text x="184" y="106" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#303238">RESEARCH</text>
    <text x="184" y="130" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#73777A">
      <tspan x="184" dy="0">Map customer</tspan><tspan x="184" dy="17">signals into insight.</tspan>
    </text>
  </g>

  <g transform="translate(360 55)">
    <text x="0" y="174" width="130" font-family="Segoe UI Black, Arial Black, Microsoft YaHei" font-size="205" font-weight="900" fill="#00C6A4">2</text>
    <ellipse cx="87" cy="176" rx="88" ry="11" fill="#000000" opacity="0.23" filter="url(#cutShadow)" transform="rotate(-13 87 176)"/>
    <rect x="-38" y="175" width="236" height="135" fill="#F7F7F5" transform="rotate(-13 87 175)"/>
    <circle cx="154" cy="106" r="23" fill="#00C6A4"/>
    <path d="M154,92 C145,96 145,108 153,113 L153,120 L161,120 L161,113 C169,108 168,96 154,92 Z M151,124 L163,124" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="188" y="106" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#303238">IDEA</text>
    <text x="188" y="130" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#73777A">
      <tspan x="188" dy="0">Shape the sharpest</tspan><tspan x="188" dy="17">concept direction.</tspan>
    </text>
  </g>

  <g transform="translate(665 55)">
    <text x="0" y="174" width="130" font-family="Segoe UI Black, Arial Black, Microsoft YaHei" font-size="205" font-weight="900" fill="#00A985">3</text>
    <ellipse cx="87" cy="176" rx="88" ry="11" fill="#000000" opacity="0.23" filter="url(#cutShadow)" transform="rotate(-13 87 176)"/>
    <rect x="-40" y="175" width="238" height="135" fill="#F7F7F5" transform="rotate(-13 87 175)"/>
    <circle cx="154" cy="106" r="23" fill="#00A985"/>
    <path d="M143,119 L166,119 M147,119 L147,104 L154,96 L161,104 L161,119 M139,104 L169,104" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="188" y="106" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#303238">STRATEGY</text>
    <text x="188" y="130" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#73777A">
      <tspan x="188" dy="0">Prioritize moves</tspan><tspan x="188" dy="17">that compound.</tspan>
    </text>
  </g>

  <g transform="translate(970 55)">
    <text x="0" y="174" width="130" font-family="Segoe UI Black, Arial Black, Microsoft YaHei" font-size="205" font-weight="900" fill="#00A3AB">4</text>
    <ellipse cx="88" cy="176" rx="86" ry="11" fill="#000000" opacity="0.23" filter="url(#cutShadow)" transform="rotate(-13 88 176)"/>
    <rect x="-42" y="175" width="238" height="135" fill="#F7F7F5" transform="rotate(-13 88 175)"/>
    <circle cx="154" cy="106" r="23" fill="#00A3AB"/>
    <path d="M154,92 C164,101 166,111 159,123 C157,117 151,117 149,123 C142,111 144,101 154,92 Z M154,123 L154,129" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="188" y="106" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#303238">LAUNCH</text>
    <text x="188" y="130" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#73777A">
      <tspan x="188" dy="0">Move pilots into</tspan><tspan x="188" dy="17">market momentum.</tspan>
    </text>
  </g>

  <g transform="translate(55 380)">
    <text x="0" y="174" width="130" font-family="Segoe UI Black, Arial Black, Microsoft YaHei" font-size="205" font-weight="900" fill="#2C82B8">5</text>
    <ellipse cx="87" cy="176" rx="88" ry="11" fill="#000000" opacity="0.24" filter="url(#cutShadow)" transform="rotate(-13 87 176)"/>
    <rect x="-40" y="175" width="238" height="135" fill="#F7F7F5" transform="rotate(-13 87 175)"/>
    <circle cx="154" cy="106" r="23" fill="#2C82B8"/>
    <path d="M154,94 L161,98 L161,106 L154,110 L147,106 L147,98 Z M154,110 L154,123 M144,123 L164,123" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="188" y="106" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#303238">PROCESS</text>
    <text x="188" y="130" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#73777A">
      <tspan x="188" dy="0">Codify the work</tspan><tspan x="188" dy="17">into repeatable flow.</tspan>
    </text>
  </g>

  <g transform="translate(360 380)">
    <text x="0" y="174" width="130" font-family="Segoe UI Black, Arial Black, Microsoft YaHei" font-size="205" font-weight="900" fill="#30578F">6</text>
    <ellipse cx="87" cy="176" rx="88" ry="11" fill="#000000" opacity="0.24" filter="url(#cutShadow)" transform="rotate(-13 87 176)"/>
    <rect x="-40" y="175" width="238" height="135" fill="#F7F7F5" transform="rotate(-13 87 175)"/>
    <circle cx="154" cy="106" r="23" fill="#30578F"/>
    <path d="M154,92 a15,15 0 1,0 0.1,0 M154,101 L154,110 L162,115 M148,88 L160,88" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="188" y="106" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#303238">TIME</text>
    <text x="188" y="130" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#73777A">
      <tspan x="188" dy="0">Sequence delivery</tspan><tspan x="188" dy="17">around milestones.</tspan>
    </text>
  </g>

  <g transform="translate(665 380)">
    <text x="0" y="174" width="130" font-family="Segoe UI Black, Arial Black, Microsoft YaHei" font-size="205" font-weight="900" fill="#363B65">7</text>
    <ellipse cx="87" cy="176" rx="88" ry="11" fill="#000000" opacity="0.25" filter="url(#cutShadow)" transform="rotate(-13 87 176)"/>
    <rect x="-40" y="175" width="238" height="135" fill="#F7F7F5" transform="rotate(-13 87 175)"/>
    <circle cx="154" cy="106" r="23" fill="#363B65"/>
    <path d="M154,92 a8,8 0 1,0 0.1,0 M140,124 C143,114 165,114 168,124 M154,111 L154,121" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="188" y="106" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#303238">EXPERTISE</text>
    <text x="188" y="130" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#73777A">
      <tspan x="188" dy="0">Apply judgment</tspan><tspan x="188" dy="17">where risk is high.</tspan>
    </text>
  </g>

  <g transform="translate(970 380)">
    <text x="0" y="174" width="130" font-family="Segoe UI Black, Arial Black, Microsoft YaHei" font-size="205" font-weight="900" fill="#34353A">8</text>
    <ellipse cx="87" cy="176" rx="88" ry="11" fill="#000000" opacity="0.25" filter="url(#cutShadow)" transform="rotate(-13 87 176)"/>
    <rect x="-40" y="175" width="238" height="135" fill="#F7F7F5" transform="rotate(-13 87 175)"/>
    <circle cx="154" cy="106" r="23" fill="#34353A"/>
    <path d="M154,92 a16,16 0 1,0 0.1,0 M154,101 a7,7 0 1,0 0.1,0 M154,108 L154,118 M144,108 L164,108" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
    <text x="188" y="106" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#303238">GOAL</text>
    <text x="188" y="130" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#73777A">
      <tspan x="188" dy="0">Measure outcomes</tspan><tspan x="188" dy="17">against ambition.</tspan>
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or `clip-path` on the number text to create the slice; the PowerPoint translation will not preserve that reliably.
- ❌ Do not use a gradient background unless the rotated slice-cover rectangles match it perfectly; a mismatched cover reveals the trick.
- ❌ Do not apply filters to `<line>` icons or connectors; if icons need glow/shadow, apply filters only to paths, circles, ellipses, or text.
- ❌ Do not make the numbers too thin; the slice effect needs heavy typography with enough interior mass to look dimensional.

## Composition notes
- Use a 2×4 grid with generous cell spacing; the number should dominate each cell, while copy remains compact and secondary.
- Keep the slice angle consistent across all items, typically around `-10°` to `-15°`, so the slide feels systemized rather than chaotic.
- Place the icon and text slightly to the right of each number’s vertical center; this makes the numeral feel like a visual anchor, not a label.
- Use a sequential color rhythm from bright green through teal and blue into dark indigo/charcoal to imply progression.