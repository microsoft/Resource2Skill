# SVG Recipe — Cyber-Radar Emission Composition

## Visual mechanism
A dark HUD-style slide uses many concentric neon ellipses, slightly tilted in perspective, to imply radar emission from a subject image. Glowing orange blips and a right-side metric stack turn the scene into an executive “active detection system” composition.

## SVG primitives needed
- 1× `<rect>` for the deep navy/black background.
- 1× `<path>` for the diagonal black vignette that darkens the text side and adds cinematic depth.
- 24–32× `<ellipse>` for editable concentric radar rings with fading green stroke opacity.
- 6× `<circle>` per blip: soft orange halo, mid halo, and bright core for each signal point.
- 1× `<image>` for a transparent PNG hero subject, ideally a drone, sensor, satellite, vehicle, or product cutout.
- 2× `<linearGradient>` for subtle background/text accent lighting.
- 2× `<filter>` with `feGaussianBlur` for neon blip glow and soft subject grounding shadow.
- 7–10× `<text>` with explicit `width` attributes for title, subtitle, metric labels, large values, and footer note.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070815"/>
      <stop offset="58%" stop-color="#02030B"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>
    <linearGradient id="neonText" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00ff8a"/>
      <stop offset="100%" stop-color="#0ca86d"/>
    </linearGradient>
    <filter id="orangeGlow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M600,0 L1280,0 L1280,720 L820,720 C755,520 710,320 600,0 Z" fill="#000000" opacity="0.72"/>

  <g transform="rotate(-7 372 430)">
    <ellipse cx="372" cy="430" rx="45"  ry="34"  fill="none" stroke="#00ff80" stroke-width="2.5" opacity="0.78"/>
    <ellipse cx="372" cy="430" rx="66"  ry="50"  fill="none" stroke="#00ff80" stroke-width="2.2" opacity="0.72"/>
    <ellipse cx="372" cy="430" rx="89"  ry="67"  fill="none" stroke="#00ff80" stroke-width="2.1" opacity="0.66"/>
    <ellipse cx="372" cy="430" rx="115" ry="86"  fill="none" stroke="#00ff80" stroke-width="2.0" opacity="0.60"/>
    <ellipse cx="372" cy="430" rx="143" ry="107" fill="none" stroke="#00ff80" stroke-width="1.9" opacity="0.55"/>
    <ellipse cx="372" cy="430" rx="172" ry="129" fill="none" stroke="#00ff80" stroke-width="1.8" opacity="0.50"/>
    <ellipse cx="372" cy="430" rx="202" ry="152" fill="none" stroke="#00ff80" stroke-width="1.7" opacity="0.46"/>
    <ellipse cx="372" cy="430" rx="232" ry="174" fill="none" stroke="#00ff80" stroke-width="1.6" opacity="0.42"/>
    <ellipse cx="372" cy="430" rx="263" ry="197" fill="none" stroke="#00ff80" stroke-width="1.5" opacity="0.38"/>
    <ellipse cx="372" cy="430" rx="294" ry="221" fill="none" stroke="#00ff80" stroke-width="1.45" opacity="0.34"/>
    <ellipse cx="372" cy="430" rx="325" ry="244" fill="none" stroke="#00ff80" stroke-width="1.4" opacity="0.30"/>
    <ellipse cx="372" cy="430" rx="356" ry="267" fill="none" stroke="#00ff80" stroke-width="1.35" opacity="0.26"/>
    <ellipse cx="372" cy="430" rx="388" ry="291" fill="none" stroke="#00ff80" stroke-width="1.3" opacity="0.22"/>
    <ellipse cx="372" cy="430" rx="420" ry="315" fill="none" stroke="#00ff80" stroke-width="1.25" opacity="0.18"/>
    <ellipse cx="372" cy="430" rx="452" ry="339" fill="none" stroke="#00ff80" stroke-width="1.2" opacity="0.14"/>
    <ellipse cx="372" cy="430" rx="485" ry="364" fill="none" stroke="#00ff80" stroke-width="1.1" opacity="0.10"/>
  </g>

  <g filter="url(#orangeGlow)">
    <circle cx="212" cy="602" r="23" fill="#ff6400" opacity="0.20"/>
    <circle cx="212" cy="602" r="12" fill="#ff6400" opacity="0.44"/>
    <circle cx="212" cy="602" r="5"  fill="#ff7a1a"/>
    <circle cx="316" cy="577" r="22" fill="#ff6400" opacity="0.20"/>
    <circle cx="316" cy="577" r="11" fill="#ff6400" opacity="0.45"/>
    <circle cx="316" cy="577" r="5"  fill="#ff7a1a"/>
    <circle cx="537" cy="542" r="20" fill="#ff6400" opacity="0.18"/>
    <circle cx="537" cy="542" r="10" fill="#ff6400" opacity="0.43"/>
    <circle cx="537" cy="542" r="5"  fill="#ff7a1a"/>
    <circle cx="274" cy="360" r="20" fill="#ff6400" opacity="0.16"/>
    <circle cx="274" cy="360" r="10" fill="#ff6400" opacity="0.38"/>
    <circle cx="274" cy="360" r="4"  fill="#ff7a1a"/>
  </g>

  <image x="22" y="42" width="760" height="468" preserveAspectRatio="xMidYMid meet"
         href="https://images.example.com/transparent-white-quadcopter-drone-cutout.png"
         filter="url(#softShadow)"/>

  <text x="1200" y="164" width="410" text-anchor="end"
        font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="42" font-weight="800"
        fill="url(#neonText)">高性能雷达探测</text>
  <text x="1198" y="226" width="360" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" letter-spacing="0.8"
        fill="#e8e8e8">HIGH-PERFORMANCE RADAR</text>
  <text x="1198" y="246" width="360" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" letter-spacing="0.8"
        fill="#e8e8e8">DETECTION</text>

  <text x="1050" y="321" width="260" text-anchor="middle"
        font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="23" fill="#f2f2f2">系统流畅度提升</text>
  <text x="1075" y="384" width="330" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="300" fill="url(#neonText)">
    20<tspan font-size="28">%</tspan> - 27<tspan font-size="28">%</tspan>
  </text>

  <text x="1075" y="477" width="330" text-anchor="middle"
        font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="23" fill="#f2f2f2">雷达探测灵敏度提升</text>
  <text x="1075" y="532" width="330" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="300" fill="url(#neonText)">
    53<tspan font-size="28">%</tspan> - 67<tspan font-size="28">%</tspan>
  </text>

  <text x="840" y="613" width="360"
        font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="14" fill="#ffffff" opacity="0.92">
    应用最新一代雷达传感器，软件系统全面升级流畅度大幅提升
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not bake the radar rings and blips into one flat PNG; keep the emission field as editable `<ellipse>` and `<circle>` shapes.
- ❌ Do not use SVG `<mask>` for the subject or ring fading; PowerPoint translation will fail or ignore it.
- ❌ Do not put glow filters on `<line>` elements; use circles/ellipses/paths for glowing HUD elements.
- ❌ Do not use `<pattern>` fills for scanlines; if scanlines are needed, draw them as low-opacity editable lines or paths.
- ❌ Do not rely on path arrow markers for callouts; use native `<line marker-end="...">` only if the translator supports it, otherwise draw the arrowhead as a small path.

## Composition notes
- Place the radar origin in the left-center/lower-left quadrant, then overlap the transparent subject image so the waves appear to emit from inside the product.
- Reserve the right 35–45% of the slide for clean typography; keep it mostly black for contrast against neon green values.
- Use ring opacity to create depth: bright and tighter near the origin, thinner and almost invisible near the canvas edge.
- Keep orange blips sparse and asymmetric; three to five points are enough to suggest detection without cluttering the premium HUD look.