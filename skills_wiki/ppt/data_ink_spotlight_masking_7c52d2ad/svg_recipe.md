# SVG Recipe — Data-Ink Spotlight Masking (数据焦点镂空蒙版)

## Visual mechanism
A full-bleed contextual photo is darkened by a semi-transparent overlay, but the overlay is drawn as a compound path with a circular “hole” punched out. A donut chart is aligned concentrically around that negative-space cutout, so the data ring frames the revealed image like a spotlight.

## SVG primitives needed
- 1× `<image>` for the full-slide atmospheric background photo
- 1× compound `<path fill-rule="evenodd">` for the editable dark overlay with circular cutout
- 4× annular `<path>` segments for the donut chart data ring
- 1× `<circle>` for a thin dashed decorative halo around the spotlight
- 1× `<circle>` for a soft glow/shadow behind the chart ring
- 4× small `<circle>` markers for the legend dots
- 1× `<rect>` for a subtle left-side text readability gradient panel
- 2× `<linearGradient>` definitions for atmosphere and chart polish
- 1× `<filter id="softShadow">` applied to the chart glow/ring elements
- Multiple `<text>` elements with explicit `width` for title, body copy, KPI, labels, and legend

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftReadability" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#071D17" stop-opacity="0.82"/>
      <stop offset="58%" stop-color="#071D17" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#071D17" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="goldGrad" x1="830" y1="130" x2="1050" y2="570">
      <stop offset="0%" stop-color="#FFE78A"/>
      <stop offset="55%" stop-color="#FFC000"/>
      <stop offset="100%" stop-color="#E49A00"/>
    </linearGradient>

    <linearGradient id="blueGrad" x1="720" y1="210" x2="960" y2="520">
      <stop offset="0%" stop-color="#A8D9FF"/>
      <stop offset="100%" stop-color="#5B9BD5"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="spotGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <!-- Full-bleed contextual image -->
  <image href="https://images.example.com/forest-aerial-river-canopy-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Extra left readability, still editable -->
  <rect x="0" y="0" width="860" height="720" fill="url(#leftReadability)"/>

  <!-- Editable overlay with circular cutout: outer rectangle + inner circle subpath -->
  <path fill="#0F2D23" fill-opacity="0.84" fill-rule="evenodd"
        d="M0 0 H1280 V720 H0 Z
           M1100 360
           A185 185 0 1 0 730 360
           A185 185 0 1 0 1100 360 Z"/>

  <!-- Soft illuminated edge around the spotlight -->
  <circle cx="915" cy="360" r="190" fill="none" stroke="#B8FFD6" stroke-opacity="0.18" stroke-width="18" filter="url(#spotGlow)"/>
  <circle cx="915" cy="360" r="258" fill="none" stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1.5" stroke-dasharray="6 12"/>

  <!-- Donut chart aligned to the cutout; inner radius ≈ cutout radius -->
  <g filter="url(#softShadow)">
    <path d="M915 115
             A245 245 0 0 1 1033 575
             L1007 527
             A190 190 0 0 0 915 170 Z"
          fill="url(#goldGrad)" stroke="#0F2D23" stroke-width="4"/>

    <path d="M1033 575
             A245 245 0 0 1 708 491
             L755 462
             A190 190 0 0 0 1007 527 Z"
          fill="#ED7D31" stroke="#0F2D23" stroke-width="4"/>

    <path d="M708 491
             A245 245 0 0 1 717 216
             L761 248
             A190 190 0 0 0 755 462 Z"
          fill="url(#blueGrad)" stroke="#0F2D23" stroke-width="4"/>

    <path d="M717 216
             A245 245 0 0 1 915 115
             L915 170
             A190 190 0 0 0 761 248 Z"
          fill="#70AD47" stroke="#0F2D23" stroke-width="4"/>
  </g>

  <!-- Center annotation floats inside the revealed photo, not over the dark mask -->
  <text x="835" y="336" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600"
        fill="#FFFFFF" text-anchor="middle" opacity="0.92">MONITORED</text>
  <text x="835" y="394" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700"
        fill="#FFFFFF" text-anchor="middle">68%</text>

  <!-- Left narrative block -->
  <text x="74" y="108" width="560" font-family="Segoe UI, Microsoft YaHei" fill="#FFFFFF">
    <tspan x="74" dy="0" font-size="34" font-weight="700">森林保护监测覆盖</tspan>
    <tspan x="74" dy="43" font-size="18" font-weight="600" letter-spacing="1.5" fill="#BFE8D5">FOREST PROTECTION MONITORING COVERAGE</tspan>
  </text>

  <line x1="76" y1="188" x2="198" y2="188" stroke="#FFC000" stroke-width="4"/>

  <text x="76" y="242" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600" fill="#F5FFF9">
    对森林资源进行定点观测、监测和评估
  </text>

  <text x="76" y="292" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#D7EEE4">
    <tspan x="76" dy="0">通过遥感、样地调查与生态传感网络，持续跟踪森林资源的数量、</tspan>
    <tspan x="76" dy="28">质量、结构和变化趋势，为保护政策与管理措施提供科学依据。</tspan>
    <tspan x="76" dy="44">国家林草一体化监测体系将林地、草地、湿地数据纳入同一张图，</tspan>
    <tspan x="76" dy="28">形成跨区域、跨周期的动态评估能力。</tspan>
  </text>

  <!-- Legend / data readout -->
  <text x="76" y="518" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">覆盖结构 / COVERAGE MIX</text>

  <circle cx="86" cy="556" r="6" fill="#FFC000"/>
  <text x="104" y="562" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E8FFF3">核心保护区 42%</text>

  <circle cx="286" cy="556" r="6" fill="#ED7D31"/>
  <text x="304" y="562" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E8FFF3">缓冲区 24%</text>

  <circle cx="86" cy="590" r="6" fill="#5B9BD5"/>
  <text x="104" y="596" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E8FFF3">水源涵养区 19%</text>

  <circle cx="286" cy="590" r="6" fill="#70AD47"/>
  <text x="304" y="596" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E8FFF3">生态修复区 15%</text>

  <text x="742" y="648" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#C7E7D8" text-anchor="middle">
    Donut inner radius matches the transparent cutout edge
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or `mask="url(...)"` to punch the hole; create the cutout as a compound `<path fill-rule="evenodd">` instead.
- ❌ Do not place `clip-path` on the dark overlay path; clipping is only reliable for `<image>` in this workflow.
- ❌ Do not rasterize the whole overlay + chart into a PNG; the spotlight and donut should remain editable PowerPoint geometry.
- ❌ Do not use `marker-end` or path-based arrows for annotations around the chart; if arrows are needed, use native `<line>` arrows directly.
- ❌ Do not put filters on `<line>` elements; use filtered circles/paths for glow and shadow effects.

## Composition notes
- Keep the text block on the left 45–55% of the slide; the cutout and chart should dominate the right side without competing with the headline.
- The cutout radius should match the donut inner radius almost exactly; this alignment is the whole “data frames the image” mechanism.
- Use a dark overlay color sampled from the photo theme, such as forest green, navy, charcoal, or deep teal, at roughly 75–88% opacity.
- Let the revealed photo remain vivid inside the cutout, while the surrounding masked area becomes calm enough for white typography.