# SVG Recipe — Clean Corporate Fundamentals (Structured Layouts & Flow)

## Visual mechanism
A calm executive layout uses a strong top-left title hierarchy, a structured sequence of content cards, and a right-side visual proof area to create a clear reading path. Corporate blue accents, restrained shadows, and simple arrow geometry guide attention without overwhelming the message.

## SVG primitives needed
- 1× `<rect>` for the full-slide light background
- 1× `<path>` for a subtle decorative corporate-blue corner ribbon
- 1× `<linearGradient>` for the accent ribbon and flow connector fills
- 1× `<filter id="softShadow">` applied to cards and the photo panel
- 1× `<clipPath>` with rounded `<rect>` applied to the hero `<image>`
- 1× `<image>` for a contextual business / analytics photo crop
- 6× `<rect>` for the title accent bar, content cards, KPI strip, and photo frame
- 6× `<circle>` for numbered step badges and bullet dots
- 6× `<line>` for structured dividers and flow connectors
- 3× `<path>` for editable arrowheads / chevrons
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, card headings, bullets, and labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueRibbon" x1="920" y1="0" x2="1280" y2="260" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0070C0"/>
      <stop offset="1" stop-color="#00A3E0"/>
    </linearGradient>

    <linearGradient id="flowBlue" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0070C0"/>
      <stop offset="1" stop-color="#44B7E8"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoClip">
      <rect x="770" y="170" width="390" height="315" rx="28"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F9FC"/>
  <path d="M990,-20 C1095,30 1195,18 1305,-10 L1305,210 C1180,255 1055,212 955,122 C930,96 940,24 990,-20 Z" fill="url(#blueRibbon)" opacity="0.16"/>

  <rect x="78" y="74" width="7" height="86" rx="3.5" fill="#0070C0"/>
  <text x="108" y="104" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#2F343A">
    Operating fundamentals
  </text>
  <text x="110" y="142" width="690" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#657181">
    Structured layout, minimal copy, and directional flow for crisp executive communication
  </text>

  <line x1="78" y1="188" x2="706" y2="188" stroke="#DDE5EE" stroke-width="2"/>

  <rect x="78" y="230" width="560" height="108" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="126" cy="284" r="24" fill="#0070C0"/>
  <text x="118" y="294" width="18" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">1</text>
  <text x="168" y="268" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#30363D">
    Start with hierarchy
  </text>
  <circle cx="176" cy="304" r="4" fill="#0070C0"/>
  <text x="192" y="310" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#5A6673">
    One headline, one message, generous whitespace.
  </text>

  <line x1="358" y1="346" x2="358" y2="382" stroke="#8FBFE6" stroke-width="3"/>
  <path d="M348 378 L358 394 L368 378 Z" fill="#8FBFE6"/>

  <rect x="78" y="394" width="560" height="108" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="126" cy="448" r="24" fill="#0070C0"/>
  <text x="118" y="458" width="18" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">2</text>
  <text x="168" y="432" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#30363D">
    Use concise evidence
  </text>
  <circle cx="176" cy="468" r="4" fill="#0070C0"/>
  <text x="192" y="474" width="395" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#5A6673">
    Replace dense paragraphs with short proof points.
  </text>

  <line x1="358" y1="510" x2="358" y2="546" stroke="#8FBFE6" stroke-width="3"/>
  <path d="M348 542 L358 558 L368 542 Z" fill="#8FBFE6"/>

  <rect x="78" y="558" width="560" height="90" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="126" cy="603" r="24" fill="#0070C0"/>
  <text x="118" y="613" width="18" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">3</text>
  <text x="168" y="592" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#30363D">
    Close with action
  </text>
  <text x="168" y="620" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#5A6673">
    End each slide section with a decision, next step, or owner.
  </text>

  <line x1="650" y1="448" x2="742" y2="448" stroke="url(#flowBlue)" stroke-width="5"/>
  <path d="M735 432 L760 448 L735 464 Z" fill="#44B7E8"/>

  <rect x="750" y="150" width="430" height="395" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="770" y="170" width="390" height="315" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip)"
         href="https://images.example.com/corporate-analytics-team-reviewing-dashboard.jpg"/>
  <rect x="770" y="170" width="390" height="315" rx="28" fill="#0070C0" opacity="0.08"/>

  <text x="790" y="525" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#30363D">
    Visual proof area
  </text>
  <text x="790" y="553" width="335" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#647282">
    Use one relevant image, chart crop, or product screen to anchor the message.
  </text>

  <rect x="770" y="590" width="390" height="58" rx="16" fill="#EAF4FC"/>
  <text x="792" y="626" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#0070C0">
    3×
  </text>
  <text x="854" y="625" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#435160">
    faster audience scanning with structured content blocks
  </text>

  <line x1="78" y1="676" x2="1160" y2="676" stroke="#DDE5EE" stroke-width="1.5"/>
  <text x="78" y="702" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8A96A3">
    Recommended rhythm: title → principle cards → supporting visual → decision cue
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense paragraph blocks that defeat the “minimum viable text” corporate layout
- ❌ Decorative complexity without hierarchy; every shape should support reading order
- ❌ Applying `clip-path` to rectangles or groups; use it only on the `<image>` crop
- ❌ SVG animations for fade transitions; handle slide fades at the PowerPoint transition layer
- ❌ Arrow markers on `<path>` elements; use editable `<line>` connectors plus triangle `<path>` arrowheads

## Composition notes
- Keep the title zone in the upper-left with a small accent bar; this creates instant hierarchy without needing heavy decoration.
- Reserve the left two-thirds for structured content cards and the right third for proof: photo, screenshot, or chart crop.
- Use corporate blue sparingly for sequence badges, connectors, and emphasis; keep most surfaces white or near-white.
- Maintain generous vertical spacing between cards so the slide reads as a guided flow, not a list dump.