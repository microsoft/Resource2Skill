# SVG Recipe — Slanted Split-Screen Stat Comparison

## Visual mechanism
A dramatic diagonal split divides the slide into opposing dark/light territories, with each side hosting a large dashed circular stat container. The slanted white divider, oversized percentages, and contrasting accent colors create instant “loss vs. gain” tension.

## SVG primitives needed
- 2× `<rect>` for the full-slide base background and subtle right-side outline accents
- 6× `<path>` for the slanted split panels, diagonal divider, divider shadow, and angular background flares
- 6× `<circle>` for dashed stat rings, progress arcs, and inner containment rings
- 8× `<text>` for headline microcopy, large percentage stats, and all-caps labels
- 3× `<linearGradient>` for premium dark-side, light-side, and divider edge color depth
- 2× `<filter>` using `feOffset`, `feGaussianBlur`, and `feMerge` for divider shadow and soft ring glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftBg" x1="0" y1="0" x2="620" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#10232E"/>
      <stop offset="0.55" stop-color="#142D39"/>
      <stop offset="1" stop-color="#0B1820"/>
    </linearGradient>

    <linearGradient id="rightBg" x1="620" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F4F7FA"/>
      <stop offset="1" stop-color="#DDE5EB"/>
    </linearGradient>

    <linearGradient id="dividerSheen" x1="560" y1="0" x2="720" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.45" stop-color="#F5F8FA"/>
      <stop offset="1" stop-color="#D6DEE5"/>
    </linearGradient>

    <filter id="dividerShadow" x="-20%" y="-10%" width="140%" height="120%">
      <feOffset dx="16" dy="0" in="SourceAlpha" result="off"/>
      <feGaussianBlur stdDeviation="12" in="off" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ringGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="5" in="SourceGraphic" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Base fields -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#rightBg)"/>
  <path d="M0 0 L704 0 L576 720 L0 720 Z" fill="url(#leftBg)"/>

  <!-- Subtle angular atmosphere on dark side -->
  <path d="M0 410 L320 720 L0 720 Z" fill="#1D6174" opacity="0.30"/>
  <path d="M120 0 L610 0 L360 310 Z" fill="#00BFFF" opacity="0.09"/>
  <path d="M0 0 L240 0 L0 240 Z" fill="#FFFFFF" opacity="0.04"/>

  <!-- Subtle geometric accents on light side -->
  <rect x="932" y="118" width="126" height="126" rx="4" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.75"/>
  <rect x="1092" y="478" width="118" height="118" rx="4" fill="none" stroke="#B8C5CE" stroke-width="6" opacity="0.55"/>
  <path d="M1030 42 L1215 42 L1215 46 L1030 46 Z" fill="#FFFFFF" opacity="0.7"/>
  <path d="M882 660 L1138 660 L1138 664 L882 664 Z" fill="#B8C5CE" opacity="0.55"/>

  <!-- Slanted divider: shadow then white blade -->
  <path d="M676 0 L758 0 L630 720 L548 720 Z" fill="#000000" opacity="0.28" filter="url(#dividerShadow)"/>
  <path d="M658 0 L724 0 L596 720 L530 720 Z" fill="url(#dividerSheen)"/>
  <path d="M652 0 L662 0 L534 720 L524 720 Z" fill="#00BFFF" opacity="0.65"/>
  <path d="M720 0 L730 0 L602 720 L592 720 Z" fill="#2ECC71" opacity="0.70"/>

  <!-- Left stat ring -->
  <g transform="translate(338 370)">
    <circle cx="0" cy="0" r="170" fill="none" stroke="#35515B" stroke-width="22" stroke-dasharray="3 18" opacity="0.85"/>
    <circle cx="0" cy="0" r="170" fill="none" stroke="#00BFFF" stroke-width="22" stroke-linecap="round"
            stroke-dasharray="260 810" transform="rotate(-90)" filter="url(#ringGlow)"/>
    <circle cx="0" cy="0" r="128" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.18"/>
  </g>

  <!-- Right stat ring -->
  <g transform="translate(942 370)">
    <circle cx="0" cy="0" r="170" fill="none" stroke="#C0CBD3" stroke-width="22" stroke-dasharray="3 18" opacity="0.95"/>
    <circle cx="0" cy="0" r="170" fill="none" stroke="#2ECC71" stroke-width="22" stroke-linecap="round"
            stroke-dasharray="742 328" transform="rotate(-90)" filter="url(#ringGlow)"/>
    <circle cx="0" cy="0" r="128" fill="none" stroke="#21323B" stroke-width="2" opacity="0.13"/>
  </g>

  <!-- Small comparison headline -->
  <text x="74" y="74" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        letter-spacing="3" fill="#77E3FF" opacity="0.95">CUSTOMER MOVEMENT</text>
  <text x="812" y="74" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        letter-spacing="3" fill="#5D6B73" text-anchor="end" opacity="0.75">FY2026 SNAPSHOT</text>

  <!-- Left center-facing label -->
  <text x="548" y="294" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800"
        letter-spacing="2.5" fill="#00BFFF" text-anchor="end">DROPPED</text>
  <text x="548" y="324" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700"
        letter-spacing="1" fill="#FFFFFF" text-anchor="end">THIS YEAR</text>

  <!-- Right center-facing label -->
  <text x="732" y="294" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800"
        letter-spacing="2.5" fill="#2ECC71">GAINED</text>
  <text x="732" y="324" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700"
        letter-spacing="1" fill="#21323B">THIS YEAR</text>

  <!-- Large left stat -->
  <text x="338" y="392" width="320" font-family="Segoe UI, Microsoft YaHei" font-weight="800"
        text-anchor="middle" fill="#FFFFFF">
    <tspan font-size="118">26</tspan><tspan font-size="54" dy="-38">%</tspan>
  </text>
  <text x="338" y="452" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        letter-spacing="3" text-anchor="middle" fill="#9BC7D2">CHURN / LOSS</text>

  <!-- Large right stat -->
  <text x="942" y="392" width="320" font-family="Segoe UI, Microsoft YaHei" font-weight="800"
        text-anchor="middle" fill="#182A32">
    <tspan font-size="118">74</tspan><tspan font-size="54" dy="-38">%</tspan>
  </text>
  <text x="942" y="452" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        letter-spacing="3" text-anchor="middle" fill="#65747C">NET GROWTH</text>
</svg>
```

## Avoid in this skill
- ❌ Using a plain vertical split; the diagonal blade is the core tension-builder.
- ❌ Applying `filter` to `<line>` for the divider shadow; use a thick slanted `<path>` instead.
- ❌ Using `mask` or clipping non-image shapes to create the diagonal; draw the split panels directly with `<path>`.
- ❌ Letting the dashed rings become too thin or low contrast; they should feel like large KPI instruments, not decorative outlines.
- ❌ Forgetting explicit `width` on `<text>` elements; PowerPoint text boxes may render unpredictably without it.

## Composition notes
- Keep the divider slightly right-leaning from top to bottom, with the labels pulled toward it to make the center seam the visual anchor.
- Place the large percentages inside oversized rings, roughly centered in each half, leaving the corners for subtle geometric texture.
- Use cyan accents on the dark side and green accents on the light side so the two stats feel related but clearly opposed.
- Preserve generous negative space around the rings; the slide should read as two monumental numbers, not a dense dashboard.