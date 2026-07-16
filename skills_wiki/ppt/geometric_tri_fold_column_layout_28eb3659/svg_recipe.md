# SVG Recipe — Geometric Tri-Fold Column Layout

## Visual mechanism
A widescreen slide is divided into three tall white “brochure panels” on a pale gray canvas, then unified by overlapping angled ribbons at the top and bottom. The columns create disciplined editorial structure while the slanted geometric bands add energy, hierarchy, and a premium printed-piece feel.

## SVG primitives needed
- 1× `<rect>` for the full-slide light gray background
- 3× `<rect>` for the white tri-fold paper panels
- 2× narrow `<rect>` overlays for subtle fold/gutter shading between panels
- 7× `<path>` parallelogram/trapezoid shapes for the layered top and bottom geometric ribbons
- 1× `<linearGradient>` for a soft paper fill on the panels
- 1× `<filter id="panelShadow">` applied to the three panel rectangles for light paper depth
- 1× `<filter id="softGlow">` applied to small accent circles for polished emphasis
- 9× `<text>` blocks with explicit `width` attributes for column titles, subtitles, body copy, and metrics
- 6× `<circle>` / `<ellipse>` accent shapes for compact icon-like data markers
- 3× small `<path>` pictogram lines inside each column to avoid a plain text-only brochure

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperGrad" x1="0" y1="42" x2="0" y2="678" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#FAFAFA"/>
    </linearGradient>

    <filter id="panelShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feOffset dx="0" dy="3" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F2F2F2"/>

  <!-- White tri-fold brochure panels -->
  <rect x="54" y="42" width="370" height="636" rx="3" fill="url(#paperGrad)" filter="url(#panelShadow)"/>
  <rect x="455" y="42" width="370" height="636" rx="3" fill="url(#paperGrad)" filter="url(#panelShadow)"/>
  <rect x="856" y="42" width="370" height="636" rx="3" fill="url(#paperGrad)" filter="url(#panelShadow)"/>

  <!-- Subtle physical fold shadows in the gutters -->
  <rect x="426" y="54" width="18" height="612" fill="#DADDE3" opacity="0.35"/>
  <rect x="827" y="54" width="18" height="612" fill="#DADDE3" opacity="0.35"/>

  <!-- Top right-leaning ribbon stack: back to front -->
  <path d="M602 42 L754 42 L703 112 L550 112 Z" fill="#FFC000"/>
  <path d="M340 42 L654 42 L603 112 L290 112 Z" fill="#00B09B"/>
  <path d="M54 42 L416 42 L365 112 L54 112 Z" fill="#203864"/>

  <!-- Bottom left-leaning ribbon stack: back to front -->
  <path d="M872 608 L1226 608 L1226 678 L960 678 Z" fill="#D9D9D9"/>
  <path d="M610 608 L905 608 L816 678 L520 678 Z" fill="#FFC000"/>
  <path d="M214 608 L665 608 L576 678 L125 678 Z" fill="#00B09B"/>
  <path d="M54 608 L260 608 L171 678 L54 678 Z" fill="#203864"/>

  <!-- Left column -->
  <text x="88" y="154" width="305" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#203864">
    <tspan x="88" dy="0">INNOVATION</tspan>
    <tspan x="88" dy="34">AND DESIGN</tspan>
  </text>
  <text x="88" y="236" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" letter-spacing="1.5" fill="#00B09B">
    STRATEGIC OPPORTUNITY
  </text>
  <text x="88" y="276" width="305" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#595959">
    <tspan x="88" dy="0">Use the first fold for the executive thesis:</tspan>
    <tspan x="88" dy="27">what is changing, why it matters, and how</tspan>
    <tspan x="88" dy="27">the organization can respond with speed.</tspan>
  </text>
  <circle cx="111" cy="428" r="28" fill="#203864" filter="url(#softGlow)"/>
  <path d="M98 431 L108 441 L126 416" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="154" y="414" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#203864">42%</text>
  <text x="154" y="456" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#666666">
    faster concept validation across priority segments
  </text>

  <!-- Middle column -->
  <text x="489" y="154" width="305" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#203864">
    <tspan x="489" dy="0">OPERATING</tspan>
    <tspan x="489" dy="34">MODEL</tspan>
  </text>
  <text x="489" y="236" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" letter-spacing="1.5" fill="#00B09B">
    THREE-PART SYSTEM
  </text>
  <text x="489" y="276" width="305" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#595959">
    <tspan x="489" dy="0">Frame the second fold as the mechanism:</tspan>
    <tspan x="489" dy="27">shared standards, reusable platforms, and</tspan>
    <tspan x="489" dy="27">clear ownership for decision velocity.</tspan>
  </text>
  <ellipse cx="523" cy="430" rx="34" ry="26" fill="#00B09B" filter="url(#softGlow)"/>
  <path d="M507 430 C516 410, 535 410, 544 430 C535 450, 516 450, 507 430 Z" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <text x="571" y="414" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#203864">3×</text>
  <text x="571" y="456" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#666666">
    reusable playbooks for launch, scale, and sustain phases
  </text>

  <!-- Right column -->
  <text x="890" y="154" width="305" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#203864">
    <tspan x="890" dy="0">MEASURABLE</tspan>
    <tspan x="890" dy="34">IMPACT</tspan>
  </text>
  <text x="890" y="236" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" letter-spacing="1.5" fill="#00B09B">
    EXECUTION SCORECARD
  </text>
  <text x="890" y="276" width="305" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#595959">
    <tspan x="890" dy="0">Use the final fold for proof: milestones,</tspan>
    <tspan x="890" dy="27">accountabilities, leading indicators, and</tspan>
    <tspan x="890" dy="27">the financial outcomes that matter most.</tspan>
  </text>
  <circle cx="924" cy="430" r="28" fill="#FFC000" filter="url(#softGlow)"/>
  <path d="M912 443 L936 443 L936 421 L948 421 L924 402 L900 421 L912 421 Z" fill="#FFFFFF"/>
  <text x="967" y="414" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#203864">$18M</text>
  <text x="967" y="456" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#666666">
    addressable margin opportunity over the next planning cycle
  </text>

  <!-- Small footer labels inside the columns, above the bottom ribbon -->
  <text x="88" y="574" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#9A9A9A">01 / DISCOVER</text>
  <text x="489" y="574" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#9A9A9A">02 / BUILD</text>
  <text x="890" y="574" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#9A9A9A">03 / SCALE</text>
</svg>
```

## Avoid in this skill
- ❌ Using only three plain rectangles and bullet lists; the technique depends on angled overlapping ribbons to feel like a designed tri-fold brochure.
- ❌ Applying `clip-path` to the ribbon shapes; use direct `<path>` polygons instead, because clips on non-image elements are ignored.
- ❌ Relying on `transform="skewX(...)"` to create the slant; draw the parallelogram points explicitly with `<path d="...">`.
- ❌ Overfilling each column with long paragraphs; narrow brochure columns need short line lengths and strong typographic hierarchy.
- ❌ Putting shadows on `<line>` elements; if fold seams need depth, use translucent `<rect>` gutter overlays instead.

## Composition notes
- Keep the three panels nearly full height with small outer margins; the white columns should read as physical paper laid on a pale gray surface.
- Let the top ribbon occupy roughly the first 10–12% of the slide and the bottom ribbon the last 10%; this frames content without stealing reading space.
- Use navy as the anchoring color, teal as the connective accent, and yellow sparingly for energy and focal statistics.
- Align text consistently inside each panel with generous left padding; vary only the metric/icon modules to keep the tri-fold structured but not monotonous.