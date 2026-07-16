# SVG Recipe — Neon Concentric Radial Dashboard

## Visual mechanism
A futuristic radial dashboard built from concentric progress arcs: each metric is a thick rounded SVG arc with a neon gradient stroke and a blurred duplicate behind it for glow. The chart sits on a dark glassmorphism canvas, with crisp percentage labels connected to the live arc endpoints.

## SVG primitives needed
- 1× `<rect>` for full-slide dark background
- 2× `<radialGradient>` / `<linearGradient>` fills for background atmosphere and title/button accents
- 5× `<circle>` for faint circular track rings behind the data
- 5× glowing duplicate `<path>` arcs with `filter="url(#neonGlow)"` for the soft halo
- 5× foreground `<path>` arcs with thick rounded gradient strokes for editable neon progress rings
- 5× `<line>` connectors from arc endpoints to metric labels
- 5× `<rect>` label cards for floating percentage tags
- Multiple `<text>` elements with explicit `width` attributes for title, body copy, legend, labels, and center value
- 1× `<filter id="softShadow">` for glass card and label depth
- 1× `<filter id="neonGlow">` using `feGaussianBlur` for luminous arcs
- Optional decorative `<circle>` dots for starfield / high-tech ambient particles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="72%" cy="48%" r="70%">
      <stop offset="0%" stop-color="#13264a"/>
      <stop offset="46%" stop-color="#0d111c"/>
      <stop offset="100%" stop-color="#05070d"/>
    </radialGradient>

    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00f5ff"/>
      <stop offset="52%" stop-color="#8dffea"/>
      <stop offset="100%" stop-color="#ff3df2"/>
    </linearGradient>

    <linearGradient id="cyanGrad" x1="650" y1="110" x2="1030" y2="580">
      <stop offset="0%" stop-color="#00f5ff"/>
      <stop offset="100%" stop-color="#0077ff"/>
    </linearGradient>
    <linearGradient id="limeGrad" x1="690" y1="130" x2="1040" y2="530">
      <stop offset="0%" stop-color="#00ff9d"/>
      <stop offset="100%" stop-color="#a8ff00"/>
    </linearGradient>
    <linearGradient id="magentaGrad" x1="700" y1="180" x2="1010" y2="570">
      <stop offset="0%" stop-color="#ff38f2"/>
      <stop offset="100%" stop-color="#7a5cff"/>
    </linearGradient>
    <linearGradient id="orangeGrad" x1="760" y1="220" x2="990" y2="520">
      <stop offset="0%" stop-color="#ffcf4a"/>
      <stop offset="100%" stop-color="#ff4f8b"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="810" y1="260" x2="940" y2="450">
      <stop offset="0%" stop-color="#42a5ff"/>
      <stop offset="100%" stop-color="#00ffe1"/>
    </linearGradient>

    <filter id="neonGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>
  <circle cx="1120" cy="92" r="2.5" fill="#4defff" opacity="0.75"/>
  <circle cx="1186" cy="246" r="1.8" fill="#ff3df2" opacity="0.7"/>
  <circle cx="620" cy="96" r="2" fill="#9dffdf" opacity="0.55"/>
  <circle cx="1085" cy="622" r="2.2" fill="#00f5ff" opacity="0.65"/>
  <circle cx="486" cy="560" r="1.6" fill="#ffffff" opacity="0.35"/>

  <rect x="48" y="56" width="430" height="608" rx="34" fill="#0b1020" opacity="0.68" filter="url(#softShadow)"/>
  <rect x="56" y="64" width="414" height="592" rx="30" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>

  <text x="86" y="128" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="3" fill="#7cecff">LIVE PERFORMANCE</text>
  <text x="84" y="190" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="url(#titleGrad)">
    <tspan x="84" dy="0">NEON</tspan>
    <tspan x="84" dy="62">RADIAL</tspan>
    <tspan x="84" dy="62">DASHBOARD</tspan>
  </text>
  <text x="88" y="410" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#b6c5df" opacity="0.9">
    <tspan x="88" dy="0">Executive metric summary using</tspan>
    <tspan x="88" dy="28">concentric progress tracks, glow</tspan>
    <tspan x="88" dy="28">layers, and endpoint callouts.</tspan>
  </text>

  <rect x="88" y="526" width="190" height="52" rx="26" fill="url(#titleGrad)" filter="url(#softShadow)"/>
  <text x="120" y="560" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#06101a">VIEW DATA</text>
  <line x1="90" y1="618" x2="395" y2="618" stroke="#ffffff" stroke-opacity="0.12"/>
  <text x="88" y="642" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#71809c">Updated 09:45 UTC · enterprise telemetry</text>

  <rect x="560" y="48" width="650" height="624" rx="42" fill="#08101e" opacity="0.5" filter="url(#softShadow)"/>
  <rect x="574" y="62" width="622" height="596" rx="34" fill="none" stroke="#ffffff" stroke-opacity="0.07"/>

  <circle cx="860" cy="360" r="220" fill="none" stroke="#ffffff" stroke-width="30" stroke-opacity="0.055"/>
  <circle cx="860" cy="360" r="180" fill="none" stroke="#ffffff" stroke-width="30" stroke-opacity="0.055"/>
  <circle cx="860" cy="360" r="140" fill="none" stroke="#ffffff" stroke-width="30" stroke-opacity="0.055"/>
  <circle cx="860" cy="360" r="100" fill="none" stroke="#ffffff" stroke-width="30" stroke-opacity="0.055"/>
  <circle cx="860" cy="360" r="60" fill="none" stroke="#ffffff" stroke-width="30" stroke-opacity="0.055"/>

  <path d="M 860 140 A 220 220 0 1 1 754 167" fill="none" stroke="#00f5ff" stroke-width="34" stroke-linecap="round" opacity="0.7" filter="url(#neonGlow)"/>
  <path d="M 860 180 A 180 180 0 1 1 683 326" fill="none" stroke="#00ff9d" stroke-width="34" stroke-linecap="round" opacity="0.7" filter="url(#neonGlow)"/>
  <path d="M 860 220 A 140 140 0 1 1 753 450" fill="none" stroke="#ff38f2" stroke-width="34" stroke-linecap="round" opacity="0.65" filter="url(#neonGlow)"/>
  <path d="M 860 260 A 100 100 0 0 1 866 460" fill="none" stroke="#ffcf4a" stroke-width="34" stroke-linecap="round" opacity="0.65" filter="url(#neonGlow)"/>
  <path d="M 860 300 A 60 60 0 0 1 909 395" fill="none" stroke="#42a5ff" stroke-width="32" stroke-linecap="round" opacity="0.75" filter="url(#neonGlow)"/>

  <path d="M 860 140 A 220 220 0 1 1 754 167" fill="none" stroke="url(#cyanGrad)" stroke-width="20" stroke-linecap="round"/>
  <path d="M 860 180 A 180 180 0 1 1 683 326" fill="none" stroke="url(#limeGrad)" stroke-width="20" stroke-linecap="round"/>
  <path d="M 860 220 A 140 140 0 1 1 753 450" fill="none" stroke="url(#magentaGrad)" stroke-width="20" stroke-linecap="round"/>
  <path d="M 860 260 A 100 100 0 0 1 866 460" fill="none" stroke="url(#orangeGrad)" stroke-width="20" stroke-linecap="round"/>
  <path d="M 860 300 A 60 60 0 0 1 909 395" fill="none" stroke="url(#blueGrad)" stroke-width="18" stroke-linecap="round"/>

  <circle cx="860" cy="360" r="38" fill="#0d1427" stroke="#ffffff" stroke-opacity="0.08"/>
  <text x="808" y="355" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#7cecff">TOTAL</text>
  <text x="790" y="390" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">76%</text>

  <line x1="754" y1="167" x2="650" y2="128" stroke="#00f5ff" stroke-width="2" stroke-opacity="0.7"/>
  <rect x="562" y="98" width="102" height="46" rx="16" fill="#061827" stroke="#00f5ff" stroke-opacity="0.45"/>
  <text x="581" y="128" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#00f5ff">92%</text>

  <line x1="683" y1="326" x2="612" y2="310" stroke="#00ff9d" stroke-width="2" stroke-opacity="0.7"/>
  <rect x="524" y="280" width="102" height="46" rx="16" fill="#071c16" stroke="#00ff9d" stroke-opacity="0.45"/>
  <text x="544" y="310" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#00ff9d">78%</text>

  <line x1="753" y1="450" x2="650" y2="505" stroke="#ff38f2" stroke-width="2" stroke-opacity="0.68"/>
  <rect x="560" y="484" width="102" height="46" rx="16" fill="#1d0a23" stroke="#ff38f2" stroke-opacity="0.45"/>
  <text x="580" y="514" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#ff38f2">64%</text>

  <line x1="866" y1="460" x2="992" y2="540" stroke="#ffcf4a" stroke-width="2" stroke-opacity="0.7"/>
  <rect x="990" y="520" width="102" height="46" rx="16" fill="#221606" stroke="#ffcf4a" stroke-opacity="0.45"/>
  <text x="1010" y="550" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#ffcf4a">49%</text>

  <line x1="909" y1="395" x2="1042" y2="398" stroke="#42a5ff" stroke-width="2" stroke-opacity="0.7"/>
  <rect x="1040" y="374" width="102" height="46" rx="16" fill="#061827" stroke="#42a5ff" stroke-opacity="0.45"/>
  <text x="1060" y="404" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#42a5ff">35%</text>
</svg>
```

## Avoid in this skill
- ❌ Using native pie-chart wedges or filled donut slices; the premium look depends on thick stroked arcs with rounded caps.
- ❌ Applying `filter` to `<line>` connectors; glow filters on lines are dropped, so keep connector lines crisp and unfiltered.
- ❌ Using `<mask>` or clipping tricks to reveal progress rings; encode each progress value directly as an SVG arc path.
- ❌ Relying on `marker-end` for arrowheads; if arrows are needed, draw small triangle `<path>` arrowheads manually.
- ❌ Omitting `width` on text labels; every `<text>` needs an explicit width for predictable editable PowerPoint rendering.

## Composition notes
- Keep the left 35–40% of the slide for title, short narrative, and CTA; reserve the right 60% for the glowing radial hero chart.
- Use a very dark navy background so the neon gradients and glow filters read as luminous rather than merely colorful.
- Duplicate each data arc: one thick blurred arc underneath for aura, one narrower crisp arc above for editable precision.
- Label only the endpoints of arcs, not every ring segment; sparse callouts preserve the premium dashboard feel.