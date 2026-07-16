# SVG Recipe — Transparent Accent Split-Screen (Monochrome Overlay)

## Visual mechanism
A grayscale photo fills the left two-thirds of the slide, while a clean white panel reserves the right third for crisp editorial typography. A large semi-transparent mint circle straddles the split line, acting as a visual bridge between texture and copy space.

## SVG primitives needed
- 1× `<image>` for the pre-desaturated monochrome hero photo, clipped to the left 65% of the canvas.
- 1× `<clipPath>` with a `<rect>` for constraining the photo to the split-screen image area.
- 2× `<rect>` for the white copy panel and slim yellow footer accent.
- 2× gradient-filled `<rect>` overlays for subtle photo darkening and edge contrast.
- 1× `<circle>` for the large transparent mint accent bridge.
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for a premium floating accent circle.
- 1× `<filter id="textGlow">` using `feGaussianBlur` for subtle white text readability on the photo.
- 1× `<path>` for a small abstract line motif inside the circle.
- Multiple `<text>` elements with explicit `width` attributes for title, label, subtitle, KPI-style copy, and footer text.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoClip">
      <rect x="0" y="0" width="832" height="720" rx="0"/>
    </clipPath>

    <linearGradient id="photoShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.34"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.22"/>
    </linearGradient>

    <linearGradient id="splitFeather" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.72"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="1.1"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <image
    href="https://images.example.com/grayscale-modern-office-team-collaboration-wide.jpg"
    x="0" y="0" width="832" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoClip)"/>

  <rect x="0" y="0" width="832" height="720" fill="url(#photoShade)"/>
  <rect x="690" y="0" width="170" height="720" fill="url(#splitFeather)"/>

  <rect x="832" y="0" width="448" height="720" fill="#FFFFFF"/>

  <circle
    cx="790" cy="350" r="245"
    fill="#88BFA5"
    opacity="0.85"
    filter="url(#softShadow)"/>

  <path
    d="M676 332 C714 292, 763 292, 798 327 C833 362, 883 362, 918 326"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="5"
    stroke-linecap="round"
    opacity="0.38"/>

  <path
    d="M681 374 C724 420, 792 420, 835 374"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="3"
    stroke-linecap="round"
    opacity="0.24"/>

  <text x="95" y="96" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600"
        letter-spacing="3"
        fill="#FFFFFF"
        opacity="0.86">
    STRATEGY BRIEF
  </text>

  <text x="92" y="180" width="525"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        line-height="1.05"
        fill="#FFFFFF"
        filter="url(#textGlow)">
    <tspan x="92" dy="0">Launch</tspan>
    <tspan x="92" dy="62">Readiness</tspan>
    <tspan x="92" dy="62">Framework</tspan>
  </text>

  <line x1="96" y1="420" x2="280" y2="420"
        stroke="#FFE600" stroke-width="8"
        stroke-linecap="round"/>

  <text x="96" y="466" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#F2F2F2"
        opacity="0.92">
    Align teams, tools, and market signals before the launch window opens.
  </text>

  <text x="680" y="330" width="235"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700"
        letter-spacing="1.4"
        text-anchor="middle"
        fill="#333333">
    OUR MISSION
  </text>

  <text x="667" y="375" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="500"
        text-anchor="middle"
        fill="#333333"
        opacity="0.76">
    Turn scattered launch activity into one coordinated operating rhythm.
  </text>

  <text x="905" y="148" width="270"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700"
        letter-spacing="2.4"
        fill="#88BFA5">
    EXECUTIVE SUMMARY
  </text>

  <text x="905" y="208" width="285"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="800"
        fill="#333333">
    One plan.
    <tspan x="905" dy="48">Every team.</tspan>
  </text>

  <text x="906" y="326" width="285"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400"
        fill="#555555">
    A clean split-screen layout keeps narrative text readable while the monochrome image preserves energy and context.
  </text>

  <rect x="905" y="444" width="235" height="1.5" fill="#D8D8D8"/>

  <text x="905" y="500" width="95"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" font-weight="800"
        fill="#333333">
    65%
  </text>

  <text x="1005" y="492" width="165"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600"
        fill="#666666">
    visual texture
    <tspan x="1005" dy="22">balanced by</tspan>
    <tspan x="1005" dy="22">35% copy space</tspan>
  </text>

  <rect x="0" y="690" width="1280" height="30" fill="#FFE600"/>

  <text x="94" y="711" width="820"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600"
        letter-spacing="0.6"
        fill="#333333">
    MONOCHROME PHOTO + TRANSPARENT BRAND ACCENT + EDITORIAL WHITE SPACE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying an SVG grayscale filter to the `<image>`; use a pre-desaturated image asset instead so the PowerPoint output remains reliable.
- ❌ Placing text directly over the busiest part of the photo without a dark overlay or glow; readability will collapse.
- ❌ Making the accent circle fully opaque; the technique depends on the photo texture subtly showing through.
- ❌ Centering the circle entirely inside one side of the split; it should overlap the boundary to visually connect image and copy areas.
- ❌ Using clip paths on non-image elements for the split; keep clipping only on the photo crop.

## Composition notes
- Keep the split near 65/35: about 830 px for the photo and 450 px for white copy space on a 1280 px canvas.
- Position the accent circle so its center sits slightly left of the split boundary; this makes it feel anchored in the photo while reaching into the white panel.
- Use the accent color once at large scale, then echo it sparingly in small labels or rules.
- Reserve the right panel for short, high-contrast executive copy; the left photo side carries atmosphere, not dense information.