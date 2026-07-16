# SVG Recipe — Radial Burst Metric Visualization

## Visual mechanism
A large central KPI is locked inside a vivid circular anchor while thin variable-length spokes radiate outward across faint concentric rings. The result feels like a premium data instrument: precise, energetic, and naturally focused on the metric.

## SVG primitives needed
- 1× `<rect>` for the dark full-slide background
- 1× `<radialGradient>` for a subtle center glow on the background
- 1× `<linearGradient>` for the saturated orange-red metric ring
- 1× `<filter id="softGlow">` applied to the central accent circle
- 1× `<filter id="textLift">` applied to the main metric text
- 7× `<circle>` for faint concentric radar wireframes
- 48× `<line>` for variable-length radial data spokes
- 2× `<circle>` for the central dark mask and thick accent anchor ring
- 5× `<text>` elements for the main number, unit label, title, subtitle, and body copy
- Optional small `<circle>` endpoint dots for selected “peak” spokes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="39%" r="60%">
      <stop offset="0%" stop-color="#263146"/>
      <stop offset="48%" stop-color="#191E2D"/>
      <stop offset="100%" stop-color="#101521"/>
    </radialGradient>

    <linearGradient id="accentRing" x1="520" y1="170" x2="760" y2="410" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFB36B"/>
      <stop offset="38%" stop-color="#F05D38"/>
      <stop offset="100%" stop-color="#CF2F36"/>
    </linearGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textLift" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="4" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="5" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <!-- Concentric radar field -->
  <circle cx="640" cy="285" r="52" fill="none" stroke="#7C879B" stroke-width="1" opacity="0.18"/>
  <circle cx="640" cy="285" r="92" fill="none" stroke="#7C879B" stroke-width="1" opacity="0.18"/>
  <circle cx="640" cy="285" r="132" fill="none" stroke="#7C879B" stroke-width="1" opacity="0.16"/>
  <circle cx="640" cy="285" r="172" fill="none" stroke="#7C879B" stroke-width="1" opacity="0.14"/>
  <circle cx="640" cy="285" r="212" fill="none" stroke="#7C879B" stroke-width="1" opacity="0.12"/>
  <circle cx="640" cy="285" r="252" fill="none" stroke="#7C879B" stroke-width="1" opacity="0.10"/>
  <circle cx="640" cy="285" r="288" fill="none" stroke="#7C879B" stroke-width="1" opacity="0.07"/>

  <!-- Variable radial data spokes; no filters on lines -->
  <g stroke="#AAB6CA" stroke-width="1.4" stroke-linecap="round" opacity="0.62">
    <line x1="640" y1="177" x2="640" y2="54" transform="rotate(0 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="92" transform="rotate(7.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="68" transform="rotate(15 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="112" transform="rotate(22.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="74" transform="rotate(30 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="128" transform="rotate(37.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="44" transform="rotate(45 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="102" transform="rotate(52.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="88" transform="rotate(60 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="130" transform="rotate(67.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="76" transform="rotate(75 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="118" transform="rotate(82.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="58" transform="rotate(90 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="116" transform="rotate(97.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="96" transform="rotate(105 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="132" transform="rotate(112.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="70" transform="rotate(120 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="104" transform="rotate(127.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="52" transform="rotate(135 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="124" transform="rotate(142.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="82" transform="rotate(150 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="136" transform="rotate(157.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="98" transform="rotate(165 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="60" transform="rotate(172.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="86" transform="rotate(180 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="126" transform="rotate(187.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="72" transform="rotate(195 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="108" transform="rotate(202.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="48" transform="rotate(210 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="120" transform="rotate(217.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="90" transform="rotate(225 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="134" transform="rotate(232.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="66" transform="rotate(240 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="114" transform="rotate(247.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="76" transform="rotate(255 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="44" transform="rotate(262.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="100" transform="rotate(270 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="132" transform="rotate(277.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="64" transform="rotate(285 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="122" transform="rotate(292.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="78" transform="rotate(300 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="138" transform="rotate(307.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="56" transform="rotate(315 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="106" transform="rotate(322.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="84" transform="rotate(330 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="128" transform="rotate(337.5 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="62" transform="rotate(345 640 285)"/>
    <line x1="640" y1="177" x2="640" y2="112" transform="rotate(352.5 640 285)"/>
  </g>

  <!-- Subtle highlight dots on a few longest spokes -->
  <circle cx="640" cy="54" r="3" fill="#F05D38" opacity="0.9"/>
  <circle cx="803" cy="122" r="2.6" fill="#F8A46B" opacity="0.85"/>
  <circle cx="871" cy="285" r="2.6" fill="#F05D38" opacity="0.8"/>
  <circle cx="804" cy="449" r="2.6" fill="#F8A46B" opacity="0.8"/>
  <circle cx="640" cy="526" r="3" fill="#F05D38" opacity="0.9"/>
  <circle cx="471" cy="454" r="2.6" fill="#F8A46B" opacity="0.75"/>
  <circle cx="406" cy="285" r="2.6" fill="#F05D38" opacity="0.8"/>
  <circle cx="473" cy="118" r="2.6" fill="#F8A46B" opacity="0.75"/>

  <!-- Central anchor masks the spoke bases and creates the hero focus -->
  <circle cx="640" cy="285" r="110" fill="#171C2A"/>
  <circle cx="640" cy="285" r="100" fill="none" stroke="url(#accentRing)" stroke-width="18" filter="url(#softGlow)"/>
  <circle cx="640" cy="285" r="72" fill="#1B2132" stroke="#384155" stroke-width="1.2" opacity="0.98"/>

  <text x="640" y="287" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="700" fill="#FFFFFF" filter="url(#textLift)">3.9</text>
  <text x="640" y="328" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="4" fill="#F05D38">MILLION</text>

  <!-- Bottom narrative block -->
  <text x="640" y="520" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#FFFFFF">Educational Pull</text>
  <text x="640" y="560" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" letter-spacing="1.2" fill="#F05D38">KNOWLEDGE FOR GLOBAL IMPACT</text>
  <text x="640" y="604" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#AEB8C8">
    <tspan x="640" dy="0">Participants from 88 countries travel 3.9 million miles annually to receive</tspan>
    <tspan x="640" dy="28">the knowledge that amplifies leadership potential and global impact.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<path>` with `marker-end` for arrow-like spokes; marker arrowheads may disappear. Use plain `<line>` spokes.
- ❌ Do not apply filters to the radial `<line>` elements; line filters are silently dropped.
- ❌ Do not create the burst with `<use>` or `<symbol>` clones; repeated explicit `<line>` elements are safer for editable PPT output.
- ❌ Do not clip or mask non-image elements to hide the spoke center; use a solid central `<circle>` mask instead.
- ❌ Do not rely on SVG animation for the wheel reveal; add PowerPoint-native animation after generation if needed.

## Composition notes
- Keep the radial visualization in the upper 55–60% of the slide, centered horizontally; reserve the lower third for title and explanation.
- The central metric circle should be large enough to interrupt the spokes cleanly, usually 180–240 px in diameter on a 1280×720 canvas.
- Use a dark navy background, cool gray wireframes, and one hot accent color so the metric ring owns the visual hierarchy.
- Vary spoke lengths irregularly but rhythmically; the burst should feel data-driven, not like a perfect decorative sun.