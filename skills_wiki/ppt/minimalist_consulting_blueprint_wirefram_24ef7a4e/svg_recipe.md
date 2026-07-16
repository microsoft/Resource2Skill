# SVG Recipe — Minimalist Consulting Blueprint Style

## Visual mechanism
A stark consulting-style page pairs disciplined editorial typography with a right-side wireframe system diagram, using thin charcoal strokes, abundant whitespace, and one restrained accent color. The slide should feel engineered: every line, node, divider, and label aligns to an invisible grid.

## SVG primitives needed
- 1× `<rect>` for the off-white full-slide background.
- 4× `<rect>` for thin accent bars, module cards, and the blueprint bounding frame.
- 15× `<line>` for structural dividers, grid axes, connection lines, and measurement ticks.
- 5× `<ellipse>` for transparent orbital / wireframe blueprint geometry.
- 10× `<circle>` for system nodes and small junction points.
- 5× `<path>` for central polygon geometry, routed connectors, and bracket-like blueprint annotations.
- 12× `<text>` for consulting-style hierarchy, module labels, captions, and callouts.
- 1× `<linearGradient>` for a barely perceptible background wash.
- 1× `<filter id="nodeShadow">` for a subtle editable node lift, applied only to circles.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f7f7f4"/>
    </linearGradient>
    <filter id="nodeShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="2"/>
      <feGaussianBlur stdDeviation="2"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paperWash)"/>

  <!-- Structural consulting grid -->
  <line x1="72" y1="64" x2="1208" y2="64" stroke="#1e1e1e" stroke-width="1"/>
  <line x1="650" y1="108" x2="650" y2="620" stroke="#d5d5d0" stroke-width="1"/>
  <line x1="72" y1="650" x2="1208" y2="650" stroke="#1e1e1e" stroke-width="1"/>
  <rect x="72" y="92" width="52" height="3" fill="#a02828"/>

  <text x="72" y="122" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2.5" fill="#646464">
    01 / OPERATING MODEL BLUEPRINT
  </text>

  <text x="72" y="194" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700" fill="#1e1e1e">
    <tspan x="72" dy="0">Systemic</tspan>
    <tspan x="72" dy="52">Failure Analysis</tspan>
  </text>

  <text x="72" y="302" width="505" font-family="Georgia, 'Times New Roman', serif" font-size="20" font-style="italic" fill="#646464">
    Deconstructing communication bottlenecks into governed, measurable, and scalable protocols.
  </text>

  <line x1="72" y1="355" x2="570" y2="355" stroke="#1e1e1e" stroke-width="1"/>
  <text x="72" y="388" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="2" fill="#a02828">
    KEY DIAGNOSIS
  </text>

  <rect x="72" y="410" width="498" height="56" fill="none" stroke="#d5d5d0" stroke-width="1"/>
  <rect x="72" y="488" width="498" height="56" fill="none" stroke="#d5d5d0" stroke-width="1"/>
  <rect x="72" y="566" width="498" height="56" fill="none" stroke="#d5d5d0" stroke-width="1"/>

  <text x="94" y="444" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#1e1e1e">
    <tspan font-weight="700">01</tspan><tspan fill="#646464">  Fragmented decision channels create avoidable latency.</tspan>
  </text>
  <text x="94" y="522" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#1e1e1e">
    <tspan font-weight="700">02</tspan><tspan fill="#646464">  Informal escalation paths mask structural accountability gaps.</tspan>
  </text>
  <text x="94" y="600" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#1e1e1e">
    <tspan font-weight="700">03</tspan><tspan fill="#646464">  Governance rituals must become explicit system architecture.</tspan>
  </text>

  <!-- Right-side wireframe blueprint -->
  <g>
    <rect x="720" y="118" width="430" height="430" fill="none" stroke="#1e1e1e" stroke-width="1"/>
    <line x1="720" y1="333" x2="1150" y2="333" stroke="#d5d5d0" stroke-width="1" stroke-dasharray="5 7"/>
    <line x1="935" y1="118" x2="935" y2="548" stroke="#d5d5d0" stroke-width="1" stroke-dasharray="5 7"/>
    <line x1="707" y1="118" x2="720" y2="118" stroke="#1e1e1e" stroke-width="1"/>
    <line x1="707" y1="548" x2="720" y2="548" stroke="#1e1e1e" stroke-width="1"/>
    <line x1="1150" y1="105" x2="1150" y2="118" stroke="#1e1e1e" stroke-width="1"/>
    <line x1="720" y1="105" x2="720" y2="118" stroke="#1e1e1e" stroke-width="1"/>

    <ellipse cx="935" cy="333" rx="168" ry="62" fill="none" stroke="#1e1e1e" stroke-width="1"/>
    <ellipse cx="935" cy="333" rx="168" ry="62" fill="none" stroke="#1e1e1e" stroke-width="1" transform="rotate(60 935 333)"/>
    <ellipse cx="935" cy="333" rx="168" ry="62" fill="none" stroke="#1e1e1e" stroke-width="1" transform="rotate(-60 935 333)"/>
    <ellipse cx="935" cy="333" rx="215" ry="142" fill="none" stroke="#d5d5d0" stroke-width="1" stroke-dasharray="6 8"/>
    <ellipse cx="935" cy="333" rx="96" ry="96" fill="none" stroke="#a02828" stroke-width="1.4"/>

    <path d="M935 250 L1006 292 L1006 374 L935 416 L864 374 L864 292 Z" fill="none" stroke="#1e1e1e" stroke-width="1.2"/>
    <path d="M798 447 C850 397 882 383 935 333 C988 282 1020 270 1072 220" fill="none" stroke="#1e1e1e" stroke-width="1"/>
    <path d="M790 242 L855 286 L918 270 L982 396 L1080 420" fill="none" stroke="#646464" stroke-width="1" stroke-dasharray="4 6"/>
    <path d="M1158 160 L1182 160 L1182 506 L1158 506" fill="none" stroke="#a02828" stroke-width="1.2"/>
    <path d="M751 570 L751 588 L1082 588 L1082 570" fill="none" stroke="#1e1e1e" stroke-width="1"/>

    <line x1="935" y1="333" x2="864" y2="292" stroke="#1e1e1e" stroke-width="1"/>
    <line x1="935" y1="333" x2="1006" y2="292" stroke="#1e1e1e" stroke-width="1"/>
    <line x1="935" y1="333" x2="1006" y2="374" stroke="#1e1e1e" stroke-width="1"/>
    <line x1="935" y1="333" x2="864" y2="374" stroke="#1e1e1e" stroke-width="1"/>
    <line x1="935" y1="333" x2="798" y2="447" stroke="#646464" stroke-width="1"/>
    <line x1="935" y1="333" x2="1072" y2="220" stroke="#646464" stroke-width="1"/>

    <circle cx="935" cy="333" r="20" fill="#ffffff" stroke="#1e1e1e" stroke-width="1.4" filter="url(#nodeShadow)"/>
    <circle cx="864" cy="292" r="7" fill="#ffffff" stroke="#1e1e1e" stroke-width="1.2"/>
    <circle cx="1006" cy="292" r="7" fill="#ffffff" stroke="#1e1e1e" stroke-width="1.2"/>
    <circle cx="1006" cy="374" r="7" fill="#ffffff" stroke="#1e1e1e" stroke-width="1.2"/>
    <circle cx="864" cy="374" r="7" fill="#ffffff" stroke="#1e1e1e" stroke-width="1.2"/>
    <circle cx="798" cy="447" r="8" fill="#ffffff" stroke="#a02828" stroke-width="1.5"/>
    <circle cx="1072" cy="220" r="8" fill="#ffffff" stroke="#a02828" stroke-width="1.5"/>
    <circle cx="790" cy="242" r="4" fill="#1e1e1e"/>
    <circle cx="918" cy="270" r="4" fill="#1e1e1e"/>
    <circle cx="1080" cy="420" r="4" fill="#1e1e1e"/>

    <text x="744" y="146" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="2" fill="#646464">SYSTEM WIREMAP</text>
    <text x="912" y="339" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1e1e1e">CORE</text>
    <text x="1032" y="222" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#646464">Decision input</text>
    <text x="812" y="472" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#646464">Escalation loop</text>
    <text x="826" y="612" width="235" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="1.6" fill="#646464">GOVERNANCE OPERATING LAYER</text>
  </g>

  <text x="72" y="681" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#646464">
    Source: Operating cadence review · Confidential
  </text>
  <text x="1090" y="681" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#646464">
    v1.3 / Draft
  </text>
</svg>
```

## Avoid in this skill
- ❌ Heavy photographic backgrounds; they undermine the blueprint / advisory-report character.
- ❌ Thick filled shapes, large color blocks, or saturated gradients; use mostly strokes and whitespace.
- ❌ Decorative icons that look like clip art; if icons are needed, render them as sparse line-art paths.
- ❌ Dense spreadsheet-like grids; keep grid lines sparse, intentional, and architectural.
- ❌ Arrowheads via `marker-end` on paths; if directional emphasis is required, use simple lines, labels, or small accent nodes.

## Composition notes
- Keep the left 45–50% for editorial hierarchy: small eyebrow, large title, italic subtitle, and disciplined diagnostic modules.
- Reserve the right 40–45% for the wireframe object; it should feel technical but not crowded.
- Use charcoal as the dominant ink, gray for secondary structure, and one brick-red accent for priority signals.
- Leave generous margins around the page; the style depends on silence, precision, and controlled negative space.