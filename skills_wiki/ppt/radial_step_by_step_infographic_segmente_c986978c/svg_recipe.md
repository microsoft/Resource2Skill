# SVG Recipe — Radial Step-by-Step Infographic (Segmented Arrow Ring)

## Visual mechanism
A central donut ring is split into colorful wedge segments, each with an outward-pointing arrow tip to imply progression and momentum. Thin radial connector lines link each arrow to concise step descriptions arranged symmetrically around the ring.

## SVG primitives needed
- 1× `<rect>` for the full-slide light background
- 2× decorative `<path>` blobs for subtle premium background atmosphere
- 8× `<path>` for repeated radial arrow-ring segments, rotated around the center
- 1× `<circle>` for the central hub
- 8× `<text>` for large step numbers inside the colored segments
- 16× `<line>` for two-part connector lines from each arrow tip to each label block
- 8× `<circle>` for small connector endpoint nodes
- 17× `<text>` blocks for title, center label, step titles, and body copy
- 2× `<linearGradient>` for background accents and central hub
- 1× `<filter id="softShadow">` applied to segment paths and central circle

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#eef3f8"/>
    </linearGradient>
    <linearGradient id="hubGrad" x1="560" y1="300" x2="720" y2="480">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#e6edf5"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M-40 145 C120 80 225 105 315 30 C390 -35 505 -20 575 70 C660 180 570 270 405 270 C235 270 110 245 -40 305 Z" fill="#dfefff" opacity="0.45"/>
  <path d="M1060 610 C1180 535 1300 570 1360 650 L1360 760 L980 760 C930 700 965 650 1060 610 Z" fill="#fff1d8" opacity="0.55"/>

  <text x="140" y="72" width="1000" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1f2a37" letter-spacing="1.5">
    8 STEP CIRCULAR INFOGRAPHIC
  </text>
  <text x="140" y="104" width="1000" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6b7280">
    A segmented arrow ring for process stages, lifecycle milestones, or capability clusters.
  </text>

  <!-- Arrow-ring segment base: centered at top, then rotated around 640,390 -->
  <path d="M609 301 A94 94 0 0 1 671 301 L689 247 A151 151 0 0 0 664 241 L640 206 L616 241 A151 151 0 0 0 591 247 Z" fill="#E63946" filter="url(#softShadow)"/>
  <path d="M609 301 A94 94 0 0 1 671 301 L689 247 A151 151 0 0 0 664 241 L640 206 L616 241 A151 151 0 0 0 591 247 Z" fill="#F4A261" transform="rotate(45 640 390)" filter="url(#softShadow)"/>
  <path d="M609 301 A94 94 0 0 1 671 301 L689 247 A151 151 0 0 0 664 241 L640 206 L616 241 A151 151 0 0 0 591 247 Z" fill="#E9C46A" transform="rotate(90 640 390)" filter="url(#softShadow)"/>
  <path d="M609 301 A94 94 0 0 1 671 301 L689 247 A151 151 0 0 0 664 241 L640 206 L616 241 A151 151 0 0 0 591 247 Z" fill="#2A9D8F" transform="rotate(135 640 390)" filter="url(#softShadow)"/>
  <path d="M609 301 A94 94 0 0 1 671 301 L689 247 A151 151 0 0 0 664 241 L640 206 L616 241 A151 151 0 0 0 591 247 Z" fill="#457B9D" transform="rotate(180 640 390)" filter="url(#softShadow)"/>
  <path d="M609 301 A94 94 0 0 1 671 301 L689 247 A151 151 0 0 0 664 241 L640 206 L616 241 A151 151 0 0 0 591 247 Z" fill="#7B2CBF" transform="rotate(225 640 390)" filter="url(#softShadow)"/>
  <path d="M609 301 A94 94 0 0 1 671 301 L689 247 A151 151 0 0 0 664 241 L640 206 L616 241 A151 151 0 0 0 591 247 Z" fill="#118AB2" transform="rotate(270 640 390)" filter="url(#softShadow)"/>
  <path d="M609 301 A94 94 0 0 1 671 301 L689 247 A151 151 0 0 0 664 241 L640 206 L616 241 A151 151 0 0 0 591 247 Z" fill="#06D6A0" transform="rotate(315 640 390)" filter="url(#softShadow)"/>

  <circle cx="640" cy="390" r="76" fill="url(#hubGrad)" stroke="#ffffff" stroke-width="5" filter="url(#softShadow)"/>
  <text x="570" y="378" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#334155">
    CORE
  </text>
  <text x="570" y="404" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748b">
    STRATEGY HUB
  </text>

  <text x="620" y="274" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">1</text>
  <text x="708" y="311" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">2</text>
  <text x="745" y="399" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">3</text>
  <text x="708" y="487" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">4</text>
  <text x="620" y="524" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">5</text>
  <text x="532" y="487" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">6</text>
  <text x="495" y="399" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">7</text>
  <text x="532" y="311" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">8</text>

  <line x1="640" y1="206" x2="805" y2="170" stroke="#E63946" stroke-width="2"/>
  <line x1="805" y1="170" x2="855" y2="170" stroke="#E63946" stroke-width="2"/>
  <circle cx="855" cy="170" r="5" fill="#E63946"/>
  <line x1="770" y1="260" x2="805" y2="250" stroke="#F4A261" stroke-width="2"/>
  <line x1="805" y1="250" x2="855" y2="250" stroke="#F4A261" stroke-width="2"/>
  <circle cx="855" cy="250" r="5" fill="#F4A261"/>
  <line x1="824" y1="390" x2="805" y2="365" stroke="#E9C46A" stroke-width="2"/>
  <line x1="805" y1="365" x2="855" y2="365" stroke="#E9C46A" stroke-width="2"/>
  <circle cx="855" cy="365" r="5" fill="#E9C46A"/>
  <line x1="770" y1="520" x2="805" y2="510" stroke="#2A9D8F" stroke-width="2"/>
  <line x1="805" y1="510" x2="855" y2="510" stroke="#2A9D8F" stroke-width="2"/>
  <circle cx="855" cy="510" r="5" fill="#2A9D8F"/>

  <line x1="640" y1="574" x2="475" y2="575" stroke="#457B9D" stroke-width="2"/>
  <line x1="475" y1="575" x2="425" y2="575" stroke="#457B9D" stroke-width="2"/>
  <circle cx="425" cy="575" r="5" fill="#457B9D"/>
  <line x1="510" y1="520" x2="475" y2="505" stroke="#7B2CBF" stroke-width="2"/>
  <line x1="475" y1="505" x2="425" y2="505" stroke="#7B2CBF" stroke-width="2"/>
  <circle cx="425" cy="505" r="5" fill="#7B2CBF"/>
  <line x1="456" y1="390" x2="475" y2="365" stroke="#118AB2" stroke-width="2"/>
  <line x1="475" y1="365" x2="425" y2="365" stroke="#118AB2" stroke-width="2"/>
  <circle cx="425" cy="365" r="5" fill="#118AB2"/>
  <line x1="510" y1="260" x2="475" y2="250" stroke="#06D6A0" stroke-width="2"/>
  <line x1="475" y1="250" x2="425" y2="250" stroke="#06D6A0" stroke-width="2"/>
  <circle cx="425" cy="250" r="5" fill="#06D6A0"/>

  <text x="880" y="160" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#E63946">Discover</text>
  <text x="880" y="184" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b7280">Frame the opportunity, identify audiences, and define the success criteria.</text>
  <text x="880" y="240" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F4A261">Plan</text>
  <text x="880" y="264" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b7280">Translate insight into a clear roadmap with owners, milestones, and risks.</text>
  <text x="880" y="355" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#C7952B">Build</text>
  <text x="880" y="379" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b7280">Create the core assets, operating model, and enabling systems.</text>
  <text x="880" y="500" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2A9D8F">Scale</text>
  <text x="880" y="524" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b7280">Expand adoption through playbooks, governance, and repeatable standards.</text>

  <text x="400" y="565" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#457B9D">Optimize</text>
  <text x="400" y="589" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b7280">Refine performance using feedback loops and operational diagnostics.</text>
  <text x="400" y="495" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#7B2CBF">Measure</text>
  <text x="400" y="519" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b7280">Track leading indicators, outcomes, and executive decision points.</text>
  <text x="400" y="355" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#118AB2">Launch</text>
  <text x="400" y="379" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b7280">Activate the market, communicate value, and align stakeholders.</text>
  <text x="400" y="240" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#06D6A0">Align</text>
  <text x="400" y="264" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b7280">Secure sponsorship, clarify roles, and agree on operating principles.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<marker>` or `marker-end` for connector arrowheads; if arrowheads are needed, draw them manually with small `<path>` triangles.
- ❌ Do not use `<use>` to repeat the ring segment; duplicate the `<path>` and apply `rotate(...)` transforms instead.
- ❌ Do not apply `clip-path` or masks to the segment paths; custom segment geometry should be drawn directly with `<path d="...">`.
- ❌ Do not rely on auto-wrapped text; every `<text>` needs an explicit `width` and should be positioned deliberately.

## Composition notes
- Keep the arrow ring centered slightly below the title line, occupying roughly the middle 40–45% of the slide width.
- Reserve wide side gutters for labels: right-side text should be left-aligned, left-side text should be right-aligned.
- Match connector/node color to the corresponding segment so the eye can quickly pair each step with its description.
- Use a pale background and soft shadows so the vibrant ring remains the primary focal point.