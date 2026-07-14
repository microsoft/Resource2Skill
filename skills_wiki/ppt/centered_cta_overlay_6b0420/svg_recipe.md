# SVG Recipe — Centered CTA Overlay

## Visual mechanism
A full-bleed cinematic hero photo is dimmed with gradient overlays, then a centered glassmorphic pill stack creates a protected focus zone for the CTA headline. The button sits directly under the title with a saturated glow so the slide reads as one clear action.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero background photo
- 6× `<rect>` for the dark image overlays, concentric glass pills, and CTA button
- 2× `<ellipse>` for soft center and button glows
- 4× `<path>` for premium neon accent arcs around the centered CTA
- 3× `<text>` with explicit `width` attributes for kicker, headline, and button label
- 4× `<linearGradient>` for image shading, glass fills, button fill, and accent strokes
- 2× `<radialGradient>` for vignette and glow effects
- 2× `<filter>` using blur / offset blur for editable glow and shadow depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoShade" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#06111F" stop-opacity="0.35"/>
      <stop offset="0.46" stop-color="#06111F" stop-opacity="0.62"/>
      <stop offset="1" stop-color="#020712" stop-opacity="0.82"/>
    </linearGradient>

    <radialGradient id="vignette" cx="50%" cy="47%" r="68%">
      <stop offset="0" stop-color="#0B1830" stop-opacity="0"/>
      <stop offset="0.62" stop-color="#050B16" stop-opacity="0.34"/>
      <stop offset="1" stop-color="#01040A" stop-opacity="0.88"/>
    </radialGradient>

    <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#42E8FF" stop-opacity="0.26"/>
      <stop offset="0.45" stop-color="#6E5BFF" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#6E5BFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="glassFill" x1="260" y1="160" x2="980" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.26"/>
      <stop offset="0.48" stop-color="#D8F8FF" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.06"/>
    </linearGradient>

    <linearGradient id="buttonGrad" x1="506" y1="494" x2="774" y2="554" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#00E5FF"/>
      <stop offset="0.48" stop-color="#5D7CFF"/>
      <stop offset="1" stop-color="#9A4DFF"/>
    </linearGradient>

    <linearGradient id="cyanStroke" x1="120" y1="160" x2="1160" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#00E5FF" stop-opacity="0"/>
      <stop offset="0.22" stop-color="#00E5FF" stop-opacity="0.72"/>
      <stop offset="0.78" stop-color="#B979FF" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#B979FF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-25%" width="140%" height="150%">
      <feOffset in="SourceAlpha" dx="0" dy="22" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.example.com/full-bleed-night-city-team-launch-hero.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#photoShade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <ellipse cx="640" cy="362" rx="520" ry="255" fill="url(#centerGlow)" filter="url(#softGlow)" opacity="0.95"/>

  <path d="M150 255 C245 125 426 115 545 205" fill="none" stroke="url(#cyanStroke)" stroke-width="3" stroke-linecap="round" opacity="0.76"/>
  <path d="M1130 466 C1026 610 835 622 702 526" fill="none" stroke="url(#cyanStroke)" stroke-width="3" stroke-linecap="round" opacity="0.76"/>
  <path d="M255 520 C330 590 450 610 560 555" fill="none" stroke="#76F6FF" stroke-width="1.5" stroke-linecap="round" opacity="0.38"/>
  <path d="M1020 192 C940 124 800 118 705 178" fill="none" stroke="#C9A6FF" stroke-width="1.5" stroke-linecap="round" opacity="0.38"/>

  <rect x="206" y="158" width="868" height="404" rx="202" fill="url(#glassFill)" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.24" filter="url(#softShadow)"/>
  <rect x="260" y="196" width="760" height="328" rx="164" fill="#FFFFFF" fill-opacity="0.08" stroke="#DDFBFF" stroke-width="1" stroke-opacity="0.26"/>
  <rect x="314" y="234" width="652" height="252" rx="126" fill="#06111F" fill-opacity="0.28" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.18"/>

  <text x="640" y="283" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700"
        letter-spacing="4" fill="#A8F7FF">
    <tspan x="640">LIMITED-TIME GROWTH PROGRAM</tspan>
  </text>

  <text x="640" y="356" width="880" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="68" font-weight="800"
        letter-spacing="-2" fill="#FFFFFF">
    <tspan x="640">Turn attention</tspan>
    <tspan x="640" dy="76">into action</tspan>
  </text>

  <ellipse cx="640" cy="526" rx="190" ry="54" fill="#4FDFFF" opacity="0.18" filter="url(#softGlow)"/>
  <rect x="502" y="492" width="276" height="64" rx="32" fill="url(#buttonGrad)" filter="url(#softShadow)"/>
  <rect x="510" y="499" width="260" height="50" rx="25" fill="#FFFFFF" fill-opacity="0.13" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.32"/>

  <text x="640" y="533" width="260" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800"
        fill="#FFFFFF">
    <tspan x="640">Start the sprint →</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a plain centered rectangle over the photo; the technique relies on layered translucent pills, glows, and gradients to feel premium.
- ❌ Applying `clip-path` or `mask` to the glass overlay shapes; use rounded `<rect>` pills instead so they remain editable.
- ❌ Putting a filter on a `<line>` for accent strokes; use `<path>` curves if you need glowing decorative motion.
- ❌ Relying on text autofit; every `<text>` needs a fixed `width` so PowerPoint preserves the intended centered layout.

## Composition notes
- Keep the CTA stack centered vertically, with the headline occupying the middle 35–40% of the slide.
- Use a darkened photo with a strong vignette so white headline text stays legible over varied imagery.
- The concentric pill overlay should be wider than the text by at least 160 px on each side, creating a calm protected reading zone.
- Reserve the brightest saturation for the button and nearby glow; background accents should remain secondary.