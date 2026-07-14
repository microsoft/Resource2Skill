# SVG Recipe — Custom Motion Path Animation & Visualization

## Visual mechanism
Show the motion as a premium “trajectory diagram”: a bold curved arrow communicates the custom motion path, while ghosted start/end object positions and small numbered keyframes make timing and bounce behavior legible even before animation is applied.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark cinematic background
- 1× `<radialGradient>` for the teal/green spotlight field
- 1× `<linearGradient>` for subtle ball lighting
- 2× `<filter>` definitions: one soft shadow for balls, one glow for the path
- 2× `<ellipse>` for grounded contact shadows under the soccer balls
- 2× grouped editable soccer balls built from `<circle>` and `<path>` panels
- 1× thick `<path>` for the red curved motion trail
- 1× `<path>` arrowhead placed manually at the curve endpoint
- 1× dashed `<path>` for the editable “ghost” motion-path guide
- 4× `<circle>` keyframe nodes along the path
- 4× `<text>` labels for timing/keyframe numbers
- 2× `<rect>` obstacle blocks to imply a custom path avoiding/clearing objects
- 3× `<text>` elements for title, subtitle, and duration annotation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="fieldGlow" cx="42%" cy="45%" r="75%">
      <stop offset="0%" stop-color="#2c8f7a"/>
      <stop offset="45%" stop-color="#145d61"/>
      <stop offset="100%" stop-color="#062a35"/>
    </radialGradient>

    <linearGradient id="ballShade" x1="25%" y1="15%" x2="80%" y2="90%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="55%" stop-color="#dce6e7"/>
      <stop offset="100%" stop-color="#85989d"/>
    </linearGradient>

    <linearGradient id="redTrail" x1="220" y1="520" x2="850" y2="280">
      <stop offset="0%" stop-color="#ff1d25"/>
      <stop offset="70%" stop-color="#ff0c19"/>
      <stop offset="100%" stop-color="#d90013"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pathGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#fieldGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#00151d" opacity="0.18"/>

  <text x="64" y="70" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#ffffff">
    Custom Motion Path
  </text>
  <text x="66" y="106" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#bfeee4">
    Visualize bounce timing, direction, and destination before applying the PowerPoint animation.
  </text>

  <rect x="1110" y="86" width="56" height="126" rx="4" fill="#c41118" opacity="0.92"/>
  <rect x="168" y="94" width="42" height="96" rx="4" fill="#c41118" opacity="0.72"/>

  <path d="M 282 548 C 430 540 568 498 670 420 C 730 374 768 318 833 292"
        fill="none" stroke="#4effd7" stroke-width="5" stroke-dasharray="12 14" stroke-linecap="round" opacity="0.75"/>

  <path d="M 260 548 C 450 538 610 488 712 392 C 762 345 792 311 842 288"
        fill="none" stroke="url(#redTrail)" stroke-width="58" stroke-linecap="round" filter="url(#pathGlow)"/>
  <path d="M 822 286 L 918 242 L 886 348 Z" fill="#ff101d" filter="url(#pathGlow)"/>

  <circle cx="282" cy="548" r="10" fill="#d8fff3" stroke="#053b42" stroke-width="3"/>
  <circle cx="505" cy="510" r="10" fill="#d8fff3" stroke="#053b42" stroke-width="3"/>
  <circle cx="690" cy="410" r="10" fill="#d8fff3" stroke="#053b42" stroke-width="3"/>
  <circle cx="840" cy="292" r="10" fill="#d8fff3" stroke="#053b42" stroke-width="3"/>

  <text x="258" y="586" width="68" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">0.0s</text>
  <text x="482" y="548" width="68" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">0.8s</text>
  <text x="666" y="448" width="68" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">1.6s</text>
  <text x="820" y="332" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">2.0s</text>

  <ellipse cx="315" cy="584" rx="86" ry="22" fill="#001014" opacity="0.48"/>
  <g transform="translate(220 410)" filter="url(#softShadow)">
    <circle cx="90" cy="90" r="82" fill="url(#ballShade)" stroke="#071015" stroke-width="3"/>
    <path d="M90 40 L122 63 L110 103 L70 103 L58 63 Z" fill="#05080a"/>
    <path d="M28 72 L58 63 L70 103 L44 126 L18 106 Z" fill="#05080a"/>
    <path d="M152 72 L122 63 L110 103 L136 126 L162 106 Z" fill="#05080a"/>
    <path d="M61 154 L70 103 L110 103 L119 154 L90 170 Z" fill="#05080a"/>
    <path d="M90 40 L90 10 M122 63 L164 52 M110 103 L145 150 M70 103 L35 150 M58 63 L16 52"
          fill="none" stroke="#101820" stroke-width="5" stroke-linecap="round"/>
    <circle cx="68" cy="72" r="9" fill="#ffffff" opacity="0.58"/>
  </g>

  <ellipse cx="928" cy="308" rx="72" ry="20" fill="#001014" opacity="0.32"/>
  <g transform="translate(835 150) scale(0.95)" filter="url(#softShadow)" opacity="0.88">
    <circle cx="90" cy="90" r="82" fill="url(#ballShade)" stroke="#071015" stroke-width="3"/>
    <path d="M90 40 L122 63 L110 103 L70 103 L58 63 Z" fill="#05080a"/>
    <path d="M28 72 L58 63 L70 103 L44 126 L18 106 Z" fill="#05080a"/>
    <path d="M152 72 L122 63 L110 103 L136 126 L162 106 Z" fill="#05080a"/>
    <path d="M61 154 L70 103 L110 103 L119 154 L90 170 Z" fill="#05080a"/>
    <path d="M90 40 L90 10 M122 63 L164 52 M110 103 L145 150 M70 103 L35 150 M58 63 L16 52"
          fill="none" stroke="#101820" stroke-width="5" stroke-linecap="round"/>
    <circle cx="68" cy="72" r="9" fill="#ffffff" opacity="0.58"/>
  </g>

  <rect x="64" y="612" width="380" height="54" rx="14" fill="#021b22" opacity="0.72" stroke="#2fffd3" stroke-width="1.5"/>
  <text x="88" y="646" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#ffffff">
    Motion path: bounce arc · duration 2.0s
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>`, `<animateMotion>`, or `<animateTransform>`; PPT-Master will not preserve them as editable PowerPoint animation behavior.
- ❌ Do not use `marker-end` on the curved `<path>` for the arrowhead; draw the arrowhead manually as its own `<path>`.
- ❌ Do not put filters on `<line>` elements for timing guides; use `<path>`, `<circle>`, or `<rect>` if glow/shadow is needed.
- ❌ Do not rely on a hidden SVG motion path as the actual PowerPoint animation; this SVG recipe creates the editable visual guide, while the real PPT motion animation should be added separately using the same key points.
- ❌ Do not omit `width` on `<text>` elements; PowerPoint text boxes need explicit widths for stable rendering.

## Composition notes
- Keep the main trajectory across the lower-left to upper-right diagonal so the slide reads as forward progress and momentum.
- Use the thick red curve as the audience-facing motion cue, then place the dashed mint path slightly on top as the “editable animation path” reference.
- Reserve the top-left for the title and explanation; avoid placing text directly over the ball destination or arrowhead.
- Use ghosted destination objects and timestamp nodes to make the animation understandable even in static PDF/exported views.