# SVG Recipe — Dark Tech Blueprint (Cyber-Manual Aesthetic)

## Visual mechanism
A deep charcoal/navy canvas is structured like a technical operating manual: glowing cyan ribbons, thin blueprint frames, slash separators, micro-labels, and oversized low-opacity watermark typography. The effect depends on disciplined alignment, high contrast, and UI-like construction details that make the slide feel like a premium cyber dashboard.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark base background
- 1× `<rect>` with radial/linear gradient fill for ambient cyan glow wash
- 8–14× thin `<line>` elements for blueprint grid and measurement guides
- 6–10× `<rect>` elements for UI badges, ribbons, panels, and outlined technical containers
- 4–8× `<path>` elements for corner brackets, slash motifs, circuit traces, and angled accent cuts
- 10–16× `<text>` elements for title hierarchy, micro-labels, technical metadata, and watermark text
- 1× `<radialGradient>` for soft cyan light bloom
- 2× `<linearGradient>` for dark panels and electric cyan ribbon fills
- 1× `<filter id="cyanGlow">` applied to cyan blocks/paths for neon separation
- 1× `<filter id="panelShadow">` applied to structural panels for depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="ambientCyan" cx="50%" cy="68%" r="62%">
      <stop offset="0%" stop-color="#2CB5C3" stop-opacity="0.42"/>
      <stop offset="38%" stop-color="#1A5D68" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#101419" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="bgPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E252C"/>
      <stop offset="100%" stop-color="#11161B"/>
    </linearGradient>

    <linearGradient id="cyanRibbon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1C8EA0"/>
      <stop offset="45%" stop-color="#2CB5C3"/>
      <stop offset="100%" stop-color="#00D4FF"/>
    </linearGradient>

    <filter id="cyanGlow" x="-30%" y="-80%" width="160%" height="260%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- dark technical canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="#101419"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#ambientCyan)"/>

  <!-- blueprint grid -->
  <line x1="90" y1="70" x2="1190" y2="70" stroke="#33414A" stroke-width="1" opacity="0.55"/>
  <line x1="90" y1="650" x2="1190" y2="650" stroke="#33414A" stroke-width="1" opacity="0.55"/>
  <line x1="90" y1="120" x2="1190" y2="120" stroke="#253039" stroke-width="1" stroke-dasharray="6 10" opacity="0.55"/>
  <line x1="90" y1="600" x2="1190" y2="600" stroke="#253039" stroke-width="1" stroke-dasharray="6 10" opacity="0.55"/>
  <line x1="120" y1="55" x2="120" y2="665" stroke="#253039" stroke-width="1" stroke-dasharray="5 12" opacity="0.5"/>
  <line x1="1160" y1="55" x2="1160" y2="665" stroke="#253039" stroke-width="1" stroke-dasharray="5 12" opacity="0.5"/>
  <line x1="320" y1="90" x2="320" y2="630" stroke="#1C8EA0" stroke-width="1" opacity="0.28"/>
  <line x1="960" y1="90" x2="960" y2="630" stroke="#1C8EA0" stroke-width="1" opacity="0.28"/>

  <!-- faded watermark -->
  <text x="640" y="360" width="1000" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="112" font-weight="800"
        letter-spacing="8" fill="#FFFFFF" opacity="0.035">CYBER MANUAL</text>

  <!-- top UI badge -->
  <rect x="90" y="78" width="282" height="42" fill="#F2F7F8" stroke="#2CB5C3" stroke-width="2"/>
  <text x="112" y="105" width="240"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700"
        fill="#151A1F">工作型PPT // 品控手册</text>

  <!-- top-right metadata -->
  <rect x="924" y="78" width="266" height="42" fill="none" stroke="#2CB5C3" stroke-width="1.5" opacity="0.9"/>
  <text x="946" y="104" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600"
        letter-spacing="1.5" fill="#A8B5BC">SYSTEM / VERSION 04.2</text>

  <!-- angular corner brackets -->
  <path d="M90 150 L90 104 L136 104" fill="none" stroke="#2CB5C3" stroke-width="3"/>
  <path d="M1190 150 L1190 104 L1144 104" fill="none" stroke="#2CB5C3" stroke-width="3"/>
  <path d="M90 570 L90 616 L136 616" fill="none" stroke="#2CB5C3" stroke-width="3"/>
  <path d="M1190 570 L1190 616 L1144 616" fill="none" stroke="#2CB5C3" stroke-width="3"/>

  <!-- central structural panel -->
  <rect x="165" y="205" width="950" height="310" rx="4" fill="url(#bgPanel)" stroke="#31424C" stroke-width="1.5" filter="url(#panelShadow)"/>
  <rect x="185" y="225" width="910" height="270" rx="2" fill="none" stroke="#2CB5C3" stroke-width="1" stroke-dasharray="10 9" opacity="0.7"/>

  <!-- electric title ribbon -->
  <rect x="230" y="300" width="820" height="86" fill="url(#cyanRibbon)" filter="url(#cyanGlow)"/>
  <path d="M230 300 L278 300 L252 386 L230 386 Z" fill="#125B68" opacity="0.7"/>
  <path d="M1050 300 L1002 386 L1050 386 Z" fill="#E9FFFF" opacity="0.26"/>

  <text x="640" y="360" width="780" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="800"
        letter-spacing="12" fill="#11171B">准 备 规 范</text>

  <text x="640" y="417" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700"
        letter-spacing="8" fill="#D7F9FF">PREPARING SPECIFICATION</text>

  <!-- slash separator row -->
  <text x="640" y="270" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        letter-spacing="4" fill="#95A3AA">QUALITY CONTROL / OPERATING RULES / TECH GUIDE</text>

  <!-- micro technical tags -->
  <rect x="230" y="456" width="98" height="30" fill="none" stroke="#2CB5C3" stroke-width="1"/>
  <text x="247" y="476" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700"
        fill="#B8C8CE">PART 01</text>

  <rect x="342" y="456" width="178" height="30" fill="#172026" stroke="#31424C" stroke-width="1"/>
  <text x="358" y="476" width="145"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12"
        letter-spacing="1.2" fill="#7FEAF4">STANDARDIZED PROCESS</text>

  <rect x="760" y="456" width="290" height="30" fill="#172026" stroke="#31424C" stroke-width="1"/>
  <text x="779" y="476" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12"
        letter-spacing="1.4" fill="#9AA8AF">DEFENSE / BUILD / VERIFY / RELEASE</text>

  <!-- lower data ribbon -->
  <rect x="90" y="588" width="1100" height="28" fill="#182027" stroke="#2CB5C3" stroke-width="1" opacity="0.92"/>
  <rect x="90" y="588" width="230" height="28" fill="#2CB5C3"/>
  <text x="112" y="607" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="800"
        letter-spacing="1.8" fill="#101419">CYBER-BLUEPRINT INDEX</text>
  <text x="348" y="607" width="780"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12"
        letter-spacing="2.2" fill="#8D9AA2">NODE 03 / INTERNAL MANUAL / ACCESS LEVEL: TEAM / UPDATED 2026</text>

  <!-- circuit traces and small nodes -->
  <path d="M150 170 H260 V205 H330" fill="none" stroke="#2CB5C3" stroke-width="1.4" opacity="0.55"/>
  <path d="M1130 170 H1020 V205 H950" fill="none" stroke="#2CB5C3" stroke-width="1.4" opacity="0.55"/>
  <circle cx="260" cy="170" r="4" fill="#2CB5C3" opacity="0.8"/>
  <circle cx="1020" cy="170" r="4" fill="#2CB5C3" opacity="0.8"/>
  <circle cx="330" cy="205" r="3" fill="#E9FFFF" opacity="0.8"/>
  <circle cx="950" cy="205" r="3" fill="#E9FFFF" opacity="0.8"/>

  <!-- decorative slash marks -->
  <path d="M104 535 L120 500" stroke="#2CB5C3" stroke-width="5" opacity="0.8"/>
  <path d="M128 535 L144 500" stroke="#2CB5C3" stroke-width="5" opacity="0.45"/>
  <path d="M1136 220 L1152 185" stroke="#2CB5C3" stroke-width="5" opacity="0.8"/>
  <path d="M1160 220 L1176 185" stroke="#2CB5C3" stroke-width="5" opacity="0.45"/>

  <!-- footer coordinates -->
  <text x="90" y="680" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11"
        letter-spacing="2" fill="#5F6D75">X: 0128 / Y: 0720 / DARK TECH BLUEPRINT</text>
  <text x="820" y="680" width="370"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11"
        letter-spacing="2" fill="#5F6D75" text-anchor="end">CONFIDENTIAL OPERATING FRAMEWORK</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use soft pastel backgrounds; the cyber-manual effect needs a near-black base with controlled cyan highlights.
- ❌ Do not make every element glow; reserve glow for the main ribbon, nodes, or one hero accent so the layout stays premium rather than noisy.
- ❌ Do not use rounded, playful UI cards everywhere; keep most geometry sharp, rectilinear, and blueprint-like.
- ❌ Do not rely on `marker-end` arrows for circuit diagrams; use plain `<line>` or `<path>` traces and separate small circles/nodes instead.
- ❌ Do not place text without explicit `width` attributes; PowerPoint text boxes need fixed widths for predictable rendering.

## Composition notes
- Keep the main title/ribbon centered and dominant, with at least 20–25% of the canvas left as dark negative space around it.
- Use cyan rhythm sparingly: one bright ribbon, a few thin frames, and small metadata accents are enough.
- Align all labels to a grid; this style looks best when badges, guides, and panels feel engineered rather than decorative.
- Background watermark text should be huge but extremely low opacity so it adds depth without competing with the foreground title.