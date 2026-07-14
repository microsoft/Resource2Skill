# SVG Recipe — Hero Metric Infographic Layout

## Visual mechanism
A dark, subtly textured executive background is divided into generous metric zones where oversized numbers dominate, supported by short context labels and vivid accent rules. The impact comes from extreme type hierarchy, strict grid alignment, and restrained neon highlights that make each KPI feel like a headline.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× large translucent `<rect>` panels for metric zones
- 6× small accent `<rect>` bars for title and metric anchors
- 3× oversized `<text>` elements for hero metric values
- 3× supporting `<text>` label blocks for metric context
- 2× title/subtitle `<text>` elements for slide framing
- Multiple `<line>` elements for subtle tech-grid texture and vertical dividers
- Multiple `<circle>` elements for low-opacity data-node decoration and glow accents
- 2× organic/diagonal `<path>` elements for premium background energy
- 2× `<linearGradient>` fills for background and glass panels
- 1× `<radialGradient>` for soft atmospheric glow
- 1× `<filter id="softShadow">` applied to metric panels
- 1× `<filter id="cyanGlow">` applied to accent shapes and glow nodes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#08111F"/>
      <stop offset="55%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>

    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00BFFF"/>
      <stop offset="100%" stop-color="#7DD3FC"/>
    </linearGradient>

    <radialGradient id="orbGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.45"/>
      <stop offset="70%" stop-color="#00BFFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#00BFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M930,-20 C1060,80 1135,175 1295,205 L1295,0 Z" fill="#38BDF8" opacity="0.08"/>
  <path d="M-40,705 C135,560 255,660 430,505 C565,385 640,395 760,250" fill="none" stroke="#38BDF8" stroke-width="2" opacity="0.17"/>

  <circle cx="1050" cy="120" r="190" fill="url(#orbGlow)"/>
  <circle cx="215" cy="585" r="145" fill="url(#orbGlow)" opacity="0.55"/>

  <line x1="80" y1="160" x2="1200" y2="160" stroke="#334155" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="290" x2="1200" y2="290" stroke="#334155" stroke-width="1" opacity="0.25"/>
  <line x1="80" y1="420" x2="1200" y2="420" stroke="#334155" stroke-width="1" opacity="0.25"/>
  <line x1="80" y1="550" x2="1200" y2="550" stroke="#334155" stroke-width="1" opacity="0.25"/>
  <line x1="200" y1="90" x2="200" y2="650" stroke="#334155" stroke-width="1" opacity="0.18"/>
  <line x1="440" y1="90" x2="440" y2="650" stroke="#334155" stroke-width="1" opacity="0.18"/>
  <line x1="680" y1="90" x2="680" y2="650" stroke="#334155" stroke-width="1" opacity="0.18"/>
  <line x1="920" y1="90" x2="920" y2="650" stroke="#334155" stroke-width="1" opacity="0.18"/>
  <line x1="1160" y1="90" x2="1160" y2="650" stroke="#334155" stroke-width="1" opacity="0.18"/>

  <circle cx="195" cy="186" r="4" fill="#38BDF8" opacity="0.55"/>
  <circle cx="438" cy="420" r="3" fill="#38BDF8" opacity="0.45"/>
  <circle cx="918" cy="288" r="4" fill="#38BDF8" opacity="0.55"/>
  <circle cx="1160" cy="550" r="3" fill="#38BDF8" opacity="0.42"/>
  <line x1="195" y1="186" x2="438" y2="420" stroke="#38BDF8" stroke-width="1" opacity="0.18"/>
  <line x1="918" y1="288" x2="1160" y2="550" stroke="#38BDF8" stroke-width="1" opacity="0.18"/>

  <text x="80" y="76" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="33" font-weight="700" fill="#FFFFFF" letter-spacing="1.5">
    GLOBAL IMPACT &amp; SCALE
  </text>
  <text x="82" y="112" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#94A3B8">
    Three numbers that summarize the organization’s reach, velocity, and market trust.
  </text>
  <rect x="80" y="132" width="120" height="6" rx="3" fill="url(#accentGrad)" filter="url(#cyanGlow)"/>

  <line x1="432" y1="224" x2="432" y2="612" stroke="#E2E8F0" stroke-width="1" opacity="0.15"/>
  <line x1="848" y1="224" x2="848" y2="612" stroke="#E2E8F0" stroke-width="1" opacity="0.15"/>

  <g transform="translate(80 230)">
    <rect x="0" y="0" width="330" height="360" rx="26" fill="url(#panelGrad)" stroke="#FFFFFF" stroke-width="1" opacity="0.95" filter="url(#softShadow)"/>
    <rect x="34" y="46" width="72" height="8" rx="4" fill="url(#accentGrad)" filter="url(#cyanGlow)"/>
    <circle cx="270" cy="68" r="26" fill="#00BFFF" opacity="0.12"/>
    <circle cx="270" cy="68" r="6" fill="#38BDF8" filter="url(#cyanGlow)"/>
    <text x="32" y="155" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="76" font-weight="800" fill="#FFFFFF">180K</text>
    <text x="36" y="210" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="600" fill="#BAE6FD">daily active vessels</text>
    <text x="36" y="246" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#CBD5E1">
      <tspan x="36" dy="0">tracked globally across ports,</tspan>
      <tspan x="36" dy="24">routes, and live maritime zones</tspan>
    </text>
  </g>

  <g transform="translate(475 230)">
    <rect x="0" y="0" width="330" height="360" rx="26" fill="url(#panelGrad)" stroke="#FFFFFF" stroke-width="1" opacity="0.95" filter="url(#softShadow)"/>
    <rect x="34" y="46" width="72" height="8" rx="4" fill="url(#accentGrad)" filter="url(#cyanGlow)"/>
    <path d="M224 40 L292 40 L292 108 L270 108 L270 62 L224 62 Z" fill="#38BDF8" opacity="0.16"/>
    <text x="32" y="155" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="82" font-weight="800" fill="#FFFFFF">35B</text>
    <text x="36" y="210" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="600" fill="#BAE6FD">in channel revenue</text>
    <text x="36" y="246" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#CBD5E1">
      <tspan x="36" dy="0">generated through ecosystem</tspan>
      <tspan x="36" dy="24">partners and enterprise programs</tspan>
    </text>
  </g>

  <g transform="translate(870 230)">
    <rect x="0" y="0" width="330" height="360" rx="26" fill="url(#panelGrad)" stroke="#FFFFFF" stroke-width="1" opacity="0.95" filter="url(#softShadow)"/>
    <rect x="34" y="46" width="72" height="8" rx="4" fill="url(#accentGrad)" filter="url(#cyanGlow)"/>
    <circle cx="270" cy="68" r="38" fill="#38BDF8" opacity="0.10"/>
    <path d="M250 70 L264 84 L292 52" fill="none" stroke="#7DD3FC" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="32" y="155" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="82" font-weight="800" fill="#FFFFFF">98%</text>
    <text x="36" y="210" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="600" fill="#BAE6FD">Fortune 500 coverage</text>
    <text x="36" y="246" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#CBD5E1">
      <tspan x="36" dy="0">served with mission-critical</tspan>
      <tspan x="36" dy="24">platforms, support, and insights</tspan>
    </text>
  </g>

  <rect x="80" y="635" width="1120" height="1" fill="#E2E8F0" opacity="0.14"/>
  <text x="80" y="672" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#64748B" letter-spacing="1">
    FY2026 OPERATING SNAPSHOT  ·  CONFIDENTIAL EXECUTIVE BRIEFING
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense tables or long bullet paragraphs; the technique depends on radical content reduction.
- ❌ Equal-sized text hierarchy; the metric value must be visually dominant by a wide margin.
- ❌ Applying filters to `<line>` elements for glowing dividers; use small glowing `<rect>` or `<circle>` accents instead.
- ❌ SVG `<pattern>` backgrounds; build the texture with editable low-opacity lines and circles.
- ❌ Masks or clipped non-image shapes; use direct gradients, opacity, and editable geometry.

## Composition notes
- Keep the title compact in the upper-left; reserve the center and lower two-thirds for the hero numbers.
- Use three metric zones for maximum executive readability; four is possible, but the number size must remain oversized.
- Let each metric breathe with generous internal padding, one short accent rule, and only 1–2 lines of context.
- Use a dark restrained palette with one electric accent color so the audience’s eye jumps immediately to the data.