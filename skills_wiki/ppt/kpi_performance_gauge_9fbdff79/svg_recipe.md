# SVG Recipe — KPI Performance Gauge

## Visual mechanism
A premium speedometer-style dial maps one KPI onto a 270° arc, with red/yellow/green performance zones giving instant status context. A dark needle pivots from the center toward the current value, while a large digital readout anchors the exact KPI result.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 1× `<rect>` for the elevated dashboard card container
- 1× `<ellipse>` for a soft ambient shadow beneath the gauge
- 1× `<path>` for the neutral gauge track behind the colored zones
- 3× `<path>` for the red, yellow, and green annular performance-zone arcs
- 2× `<path>` for the needle body and subtle highlight
- 2× `<circle>` for the center hub and hub highlight
- 5× `<line>` for scale tick marks
- Multiple `<text>` elements with explicit `width` for title, KPI value, unit label, min/max labels, and status annotation
- 3× `<linearGradient>` for arc depth, card polish, and needle sheen
- 1× `<radialGradient>` for the hub finish
- 2× `<filter>` definitions for card shadow and soft gauge glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F6F8FB"/>
      <stop offset="100%" stop-color="#E9EEF5"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="110" x2="0" y2="650">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFD"/>
    </linearGradient>

    <linearGradient id="needleGrad" x1="620" y1="400" x2="870" y2="386">
      <stop offset="0%" stop-color="#1F2937"/>
      <stop offset="58%" stop-color="#4B5563"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>

    <radialGradient id="hubGrad" cx="44%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#93C5FD"/>
      <stop offset="45%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#1E3A8A"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <rect x="156" y="74" width="968" height="580" rx="36" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
  <rect x="184" y="102" width="912" height="524" rx="28" fill="none" stroke="#E5EAF2" stroke-width="2"/>

  <text x="230" y="154" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#111827">
    Sales Quota Attainment
  </text>
  <text x="230" y="190" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">
    Current quarter performance against executive target
  </text>

  <ellipse cx="640" cy="586" rx="250" ry="32" fill="#CBD5E1" opacity="0.32" filter="url(#softGlow)"/>

  <!-- neutral track behind colored gauge -->
  <path d="M 456.2 583.8 A 260 260 0 1 1 823.8 583.8 L 770.8 530.8 A 185 185 0 1 0 509.2 530.8 Z"
        fill="#E5E7EB"/>

  <!-- red zone: 0–25 -->
  <path d="M 456.2 583.8 A 260 260 0 0 1 399.8 300.5 L 469.1 329.2 A 185 185 0 0 0 509.2 530.8 Z"
        fill="#D91E18" stroke="#FFFFFF" stroke-width="5"/>

  <!-- yellow zone: 25–75 -->
  <path d="M 399.8 300.5 A 260 260 0 0 1 880.2 300.5 L 810.9 329.2 A 185 185 0 0 0 469.1 329.2 Z"
        fill="#F2C200" stroke="#FFFFFF" stroke-width="5"/>

  <!-- green zone: 75–100 -->
  <path d="M 880.2 300.5 A 260 260 0 0 1 823.8 583.8 L 770.8 530.8 A 185 185 0 0 0 810.9 329.2 Z"
        fill="#50AF47" stroke="#FFFFFF" stroke-width="5"/>

  <!-- subtle inner dial surface -->
  <circle cx="640" cy="400" r="168" fill="#FFFFFF" opacity="0.90"/>
  <circle cx="640" cy="400" r="166" fill="none" stroke="#EDF2F7" stroke-width="2"/>

  <!-- scale ticks -->
  <line x1="447.7" y1="592.3" x2="434.9" y2="605.1" stroke="#64748B" stroke-width="4" stroke-linecap="round"/>
  <line x1="388.7" y1="295.9" x2="371.0" y2="289.0" stroke="#64748B" stroke-width="4" stroke-linecap="round"/>
  <line x1="640.0" y1="128.0" x2="640.0" y2="110.0" stroke="#64748B" stroke-width="4" stroke-linecap="round"/>
  <line x1="891.3" y1="295.9" x2="909.0" y2="289.0" stroke="#64748B" stroke-width="4" stroke-linecap="round"/>
  <line x1="832.3" y1="592.3" x2="845.1" y2="605.1" stroke="#64748B" stroke-width="4" stroke-linecap="round"/>

  <text x="392" y="633" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#475569">0%</text>
  <text x="640" y="94" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#475569">50%</text>
  <text x="888" y="633" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#475569">100%</text>

  <!-- needle at 82% -->
  <path d="M 620 405 L 641 386 L 870 386 L 641 414 Z"
        fill="url(#needleGrad)" filter="url(#cardShadow)"/>
  <path d="M 646 392 L 850 386 L 648 398 Z"
        fill="#FFFFFF" opacity="0.28"/>

  <circle cx="640" cy="400" r="38" fill="url(#hubGrad)" stroke="#FFFFFF" stroke-width="5"/>
  <circle cx="628" cy="386" r="8" fill="#FFFFFF" opacity="0.55"/>

  <text x="480" y="430" width="320" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="66" font-weight="800" fill="#111827">
    82%
  </text>
  <text x="500" y="468" width="280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#2563EB">
    Above target threshold
  </text>

  <rect x="474" y="504" width="332" height="54" rx="27" fill="#ECFDF3" stroke="#BBF7D0"/>
  <circle cx="506" cy="531" r="9" fill="#50AF47"/>
  <text x="528" y="537" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#166534">
    Healthy performance zone
  </text>

  <text x="230" y="592" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">
    Red: &lt;25% · Yellow: 25–75% · Green: &gt;75%
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `marker-end` for the needle; build the pointer as an editable `<path>` triangle or diamond instead.
- ❌ Using SVG `<mask>` to punch out the gauge center; create annular arcs directly with compound `<path>` shapes.
- ❌ Applying filters to tick-mark `<line>` elements; shadows/glows should go on paths, circles, ellipses, or rectangles.
- ❌ Omitting `width` on text labels; PowerPoint text boxes will render unpredictably without explicit widths.
- ❌ Building the gauge as a single flattened image unless the arc design requires a real bitmap texture.

## Composition notes
- Keep the gauge centered and large, occupying roughly 60–70% of slide height; it should read instantly from the back of the room.
- Place the exact KPI value inside the dial, not outside it, so qualitative status and quantitative value are perceived together.
- Use restrained dashboard framing: a soft card, subtle shadow, and minimal labels prevent the colored zones from feeling toy-like.
- Red/yellow/green arcs should be saturated, while the background, ticks, and text remain neutral to preserve executive polish.