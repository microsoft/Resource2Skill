# SVG Recipe — Thematic Process Flowchart

## Visual mechanism
A structured top-to-bottom decision tree is layered over a heavily washed-out contextual photograph, giving the process a real-world theme without competing with the logic. Light, uniform rounded nodes and thick accent-color arrows create a clear executive-ready protocol flow.

## SVG primitives needed
- 1× `<image>` for the full-bleed thematic background photo
- 1× translucent `<rect>` overlay to wash the photo back toward white
- 1× `<linearGradient>` for subtle slide-edge warmth
- 1× `<radialGradient>` for low-opacity thematic accent glow
- 1× `<filter id="softShadow">` applied to flowchart node rectangles
- 8× `<rect>` for rounded flowchart nodes and label chips
- 14× `<line>` for straight arrow connectors and branching elbows
- 1× `<marker>` definition for triangle arrowheads applied directly to each arrow `<line>`
- 10× `<text>` blocks with explicit `width` attributes for title, subtitle, and node labels
- 6× decorative `<path>` / `<circle>` elements for faint thematic medical/technical motifs

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="edgeWarmth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#FFE7D6" stop-opacity="0.55"/>
    </linearGradient>

    <radialGradient id="orangeGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#ED7D31" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#ED7D31" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <marker id="arrowOrange" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto" markerUnits="strokeWidth">
      <path d="M 1 1 L 13 7 L 1 13 Z" fill="#ED7D31"/>
    </marker>
  </defs>

  <!-- Thematic background: use a context-specific photo, then wash it out -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <image href="https://images.example.com/medical-team-masks-soft-clinic-background.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.16"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeWarmth)"/>
  <ellipse cx="1090" cy="590" rx="290" ry="190" fill="url(#orangeGlow)"/>

  <!-- Faint contextual motifs -->
  <circle cx="118" cy="584" r="38" fill="none" stroke="#ED7D31" stroke-width="3" opacity="0.12"/>
  <path d="M118 552 L118 616 M86 584 L150 584" stroke="#ED7D31" stroke-width="8" stroke-linecap="round" opacity="0.10"/>
  <circle cx="1120" cy="150" r="44" fill="none" stroke="#ED7D31" stroke-width="3" opacity="0.10"/>
  <path d="M1092 150 C1106 128,1134 128,1148 150 C1134 172,1106 172,1092 150 Z" fill="none" stroke="#ED7D31" stroke-width="4" opacity="0.10"/>
  <path d="M70 132 C108 92,168 100,196 142 C164 176,104 174,70 132 Z" fill="#ED7D31" opacity="0.06"/>
  <path d="M1020 648 C1068 604,1142 612,1178 660 C1136 694,1060 698,1020 648 Z" fill="#ED7D31" opacity="0.07"/>

  <!-- Header -->
  <text x="640" y="55" width="980" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#303030">
    Do I need to get tested for COVID-19?
  </text>
  <text x="640" y="92" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#666666">
    A symptom-based triage protocol for choosing the next action
  </text>

  <!-- Flowchart nodes -->
  <rect x="420" y="126" width="440" height="66" rx="22" fill="#FFEBDA" stroke="#ED7D31" stroke-width="3" filter="url(#softShadow)"/>
  <text x="640" y="151" width="390" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#404040">
    <tspan x="640" dy="0">Are you experiencing fever, cough,</tspan>
    <tspan x="640" dy="23">shortness of breath, or fatigue?</tspan>
  </text>

  <rect x="470" y="246" width="340" height="64" rx="22" fill="#FFEBDA" stroke="#ED7D31" stroke-width="3" filter="url(#softShadow)"/>
  <text x="640" y="272" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#404040">
    <tspan x="640" dy="0">Call your physician</tspan>
    <tspan x="640" dy="23">or care provider first</tspan>
  </text>

  <rect x="88" y="370" width="285" height="74" rx="22" fill="#FFEBDA" stroke="#ED7D31" stroke-width="3" filter="url(#softShadow)"/>
  <text x="230" y="397" width="245" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#404040">
    <tspan x="230" dy="0">Mild symptoms</tspan>
    <tspan x="230" dy="23">and low risk factors</tspan>
  </text>

  <rect x="498" y="370" width="285" height="74" rx="22" fill="#FFEBDA" stroke="#ED7D31" stroke-width="3" filter="url(#softShadow)"/>
  <text x="640" y="397" width="245" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#404040">
    <tspan x="640" dy="0">Severe symptoms</tspan>
    <tspan x="640" dy="23">or high-risk condition</tspan>
  </text>

  <rect x="908" y="370" width="285" height="74" rx="22" fill="#FFEBDA" stroke="#ED7D31" stroke-width="3" filter="url(#softShadow)"/>
  <text x="1050" y="397" width="245" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#404040">
    <tspan x="1050" dy="0">Unsure or exposed</tspan>
    <tspan x="1050" dy="23">but no clear symptoms</tspan>
  </text>

  <rect x="88" y="535" width="285" height="78" rx="22" fill="#FFF7F1" stroke="#ED7D31" stroke-width="3" filter="url(#softShadow)"/>
  <text x="230" y="562" width="245" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#404040">
    <tspan x="230" dy="0">Self-isolate, monitor,</tspan>
    <tspan x="230" dy="23">and schedule a test</tspan>
  </text>

  <rect x="498" y="535" width="285" height="78" rx="22" fill="#FFF7F1" stroke="#ED7D31" stroke-width="3" filter="url(#softShadow)"/>
  <text x="640" y="562" width="245" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#404040">
    <tspan x="640" dy="0">Seek urgent care</tspan>
    <tspan x="640" dy="23">or emergency evaluation</tspan>
  </text>

  <rect x="908" y="535" width="285" height="78" rx="22" fill="#FFF7F1" stroke="#ED7D31" stroke-width="3" filter="url(#softShadow)"/>
  <text x="1050" y="562" width="245" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#404040">
    <tspan x="1050" dy="0">Use hotline guidance</tspan>
    <tspan x="1050" dy="23">and retest if symptoms appear</tspan>
  </text>

  <!-- Connectors: marker-end goes directly on each line -->
  <line x1="640" y1="192" x2="640" y2="240" stroke="#ED7D31" stroke-width="5" stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="640" y1="310" x2="640" y2="342" stroke="#ED7D31" stroke-width="5" stroke-linecap="round"/>
  <line x1="230" y1="342" x2="1050" y2="342" stroke="#ED7D31" stroke-width="5" stroke-linecap="round"/>
  <line x1="230" y1="342" x2="230" y2="364" stroke="#ED7D31" stroke-width="5" stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="640" y1="342" x2="640" y2="364" stroke="#ED7D31" stroke-width="5" stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="1050" y1="342" x2="1050" y2="364" stroke="#ED7D31" stroke-width="5" stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="230" y1="444" x2="230" y2="529" stroke="#ED7D31" stroke-width="5" stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="640" y1="444" x2="640" y2="529" stroke="#ED7D31" stroke-width="5" stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="1050" y1="444" x2="1050" y2="529" stroke="#ED7D31" stroke-width="5" stroke-linecap="round" marker-end="url(#arrowOrange)"/>

  <!-- Small decision chips -->
  <rect x="188" y="328" width="84" height="28" rx="14" fill="#ED7D31"/>
  <text x="230" y="348" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">LOW</text>
  <rect x="594" y="328" width="92" height="28" rx="14" fill="#ED7D31"/>
  <text x="640" y="348" width="78" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">HIGH</text>
  <rect x="1004" y="328" width="92" height="28" rx="14" fill="#ED7D31"/>
  <text x="1050" y="348" width="78" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">UNCLEAR</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a high-contrast or fully saturated background image; it will fight the flowchart.
- ❌ Do not put `marker-end` on a `<path>` connector; use `<line>` segments and apply `marker-end` directly to each arrow line.
- ❌ Do not apply shadows or filters to connector `<line>` elements; keep filters on node rectangles only.
- ❌ Do not vary node sizes too aggressively; inconsistent boxes make the protocol feel less trustworthy.
- ❌ Do not rely on SVG auto-wrapping for text; use explicit `width` and manual `<tspan>` line breaks.

## Composition notes
- Keep the title and subtitle in the top 15% of the slide; reserve the center and lower area for the process logic.
- Use a single strong accent color for borders, arrows, and decision chips so the viewer can trace the flow instantly.
- Let the background image occupy the full bleed, but reduce it to a subtle texture with opacity and white overlay.
- Branching columns should have generous horizontal spacing; each branch needs its own visual lane from decision to outcome.